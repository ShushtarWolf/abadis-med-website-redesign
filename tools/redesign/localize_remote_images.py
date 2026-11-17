#!/usr/bin/env python3
"""Self-host the abadis-med.com images that post pages and post cards still hotlink.

EN / AR posts (and a few hand-imported FA posts) were copied from the WordPress REST API with their
<img src="https://(www.)abadis-med.com/...">. Those requests are slow or time out from many networks,
so readers saw articles with no pictures. This pass downloads each image once (live https -> http ->
Wayback original), converts it to WebP in site/assets/img/c/ with the same naming as lib.img(), registers
it in data/imgmap.json, and rewrites the tag to the local file (srcset/sizes dropped, width/height set).

Scope: <img> inside <article> on every page, and post-card thumbnails (<div class="ph">).

It also gives EN / AR posts the featured image at the top of the article (class="lead-img"), the way
the FA post pages and the live WordPress posts show it; the i18n post template never rendered it, so
EN / AR posts without in-body pictures showed no image at all.
Usage: python3 tools/redesign/localize_remote_images.py [--dry]
"""
import sys, re, os, json, html, hashlib, pathlib, urllib.parse as u, urllib.request, urllib.error, concurrent.futures as cf
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import lib
from lib import SITE, DATA, _key, full_url

RAW = lib.RAW
OUT = SITE / 'assets/img/c'
FALLBACK = 'assets/img/post-thumb-fallback.webp'
UA = 'Mozilla/5.0 (AbadisRedesign image sync; info@abadis-med.com)'
REMOTE = re.compile(r'^(?:https?:)?//(?:www\.)?abadis-med\.com/', re.I)
ARTICLE = re.compile(r'<article\b[\s\S]*?</article>')
CARD_PH = re.compile(r'<div class="ph\b[^"]*">\s*<img\b[^>]*>')
IMG = re.compile(r'<img\b[^>]*>')
LINK_IMG = re.compile(r'(<a\b[^>]*\shref=")([^"]+)("[^>]*>\s*)(<img\b[^>]*>)')

def enc(url):
    if url.startswith('//'): url = 'https:' + url
    p = u.urlsplit(html.unescape(url))
    return u.urlunsplit((p.scheme or 'https', p.netloc, u.quote(u.unquote(p.path)), '', ''))

def _open(url, t=40):
    r = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=t)
    d = r.read()
    ok = len(d) > 500 and (d[:4] in (b'\x89PNG', b'GIF8') or d[:2] == b'\xff\xd8' or (d[:4] == b'RIFF' and d[8:12] == b'WEBP'))
    return d if ok else None

DEAD = set()   # 404 on the live site and nothing in the Wayback Machine

def fetch(url):
    e = enc(url)
    gone = False
    http = e.replace('https://', 'http://', 1)
    for c in (e, http, e, 'https://web.archive.org/web/2026id_/' + e, 'https://web.archive.org/web/2024id_/' + e):
        try:
            d = _open(c)
            if d: return d, ('wayback' if 'archive.org' in c else 'ok')
        except urllib.error.HTTPError as ex:
            gone = gone or (ex.code in (404, 410) and 'archive.org' not in c)
        except Exception:
            pass
    if gone: DEAD.add(url)
    return None, None

def out_name(key, maxw):
    return hashlib.sha1(key.encode()).hexdigest()[:12] + f'-{maxw}.webp'

def collect():
    """file -> list of remote src values that need localizing (with the width bucket)."""
    todo = {}
    for f in sorted(SITE.rglob('*.html')):
        s = f.read_text(encoding='utf-8')
        if 'abadis-med.com' not in s: continue
        found = []
        for m in ARTICLE.finditer(s):
            for t in IMG.findall(m.group(0)):
                src = attr(t, 'src')
                if src and REMOTE.match(html.unescape(src)): found.append((html.unescape(src), 1400))
        for m in CARD_PH.finditer(s):
            src = attr(m.group(0), 'src')
            if src and REMOTE.match(html.unescape(src)): found.append((html.unescape(src), 640))
        if found: todo[f] = found
    return todo

def attr(tag, name):
    m = re.search(r'\s' + name + r'="([^"]*)"', tag)
    return m.group(1) if m else None

def ensure(src, maxw, imgmap):
    """Return dict(src, w, h) relative to site root, or None."""
    cands = [full_url(src), src] if full_url(src) != src else [src]
    for c in cands:
        name = out_name(_key(c), maxw)
        if (OUT / name).exists():
            return lib.img(c, maxw) or None
    for c in cands:
        r = lib.img(c, maxw)      # already in the raw cache
        if r: return r
    for c in cands:
        data, via = fetch(c)
        if not data: continue
        ext = os.path.splitext(u.unquote(u.urlsplit(c).path))[1].lower() or '.jpg'
        known = imgmap.get(c) if (imgmap.get(c) or {}).get('ok') else None
        fn = known['file'] if known else hashlib.sha1(_key(c).encode()).hexdigest()[:16] + ext
        RAW.mkdir(parents=True, exist_ok=True)
        (RAW / fn).write_bytes(data)
        if not known: imgmap[c] = {'ok': True, 'file': fn, 'bytes': len(data), 'via': via}
        lib._IMG_BY_PATH[_key(c)] = fn
        r = lib.img(c, maxw)
        if r: return r
    return None

def rel(f, site_rel):
    return os.path.relpath(SITE / site_rel, f.parent).replace(os.sep, '/')

def retag(tag, f, r, keep_lazy=True):
    t = re.sub(r'\s(srcset|sizes|data-src|data-srcset|data-lazy-src)="[^"]*"', '', tag)
    t = re.sub(r'(\ssrc=")[^"]*"', lambda m: m.group(1) + rel(f, r['src']) + '"', t, count=1)
    for a, v in (('width', r['w']), ('height', r['h'])):
        if re.search(r'\s' + a + r'="', t): t = re.sub(r'(\s' + a + r'=")[^"]*"', rf'\g<1>{v}"', t, count=1)
        else: t = t.replace('<img', f'<img {a}="{v}"', 1)
    if 'loading=' not in t: t = t.replace('<img', '<img loading="lazy"', 1)
    if 'decoding=' not in t: t = t.replace('<img', '<img decoding="async"', 1)
    return t

def _stem(url):
    b = u.unquote(u.urlsplit(html.unescape(url)).path).rsplit('/', 1)[-1]
    return re.sub(r'-\d+x\d+$', '', b.rsplit('.', 1)[0]).lower()

def featured_map():
    """site path (e.g. 'en/slug/') -> featured image URL for EN / AR posts."""
    out = {}
    def path_of(link):
        return u.unquote(u.urlsplit(link).path).strip('/') + '/'
    for p in json.load(open(DATA / 'en_posts.json', encoding='utf-8')):
        og = (p.get('yoast_head_json') or {}).get('og_image') or []
        if p.get('featured_media') and og and og[0].get('url'):
            out[path_of(p['link'])] = og[0]['url']
    for k, v in json.load(open(DATA / 'en_extra_featured.json', encoding='utf-8')).items():
        if v: out.setdefault(path_of(k), v)
    for k, v in json.load(open(DATA / 'ar_featured.json', encoding='utf-8')).items():
        if v: out.setdefault(path_of(k), v)
    return out

def add_lead_images():
    n = 0
    for path, url in sorted(featured_map().items()):
        f = SITE / path / 'index.html'
        if not f.is_file(): continue
        s = f.read_text(encoding='utf-8')
        m = re.search(r'(<article class="article prose[^"]*">)([\s\S]*?)</article>', s)
        if not m or 'class="lead-img"' in m.group(2): continue
        first = IMG.search(m.group(2))
        if first:
            fs = html.unescape(attr(first.group(0), 'src') or '')
            same_local = {out_name(_key(c), 1400) for c in (full_url(url), url)}
            if _stem(fs) == _stem(url) or fs.rsplit('/', 1)[-1] in same_local:
                continue
        h1 = re.search(r'<h1[^>]*>([\s\S]*?)</h1>', s)
        alt = html.escape(html.unescape(re.sub(r'<[^>]+>', '', h1.group(1))).strip(), quote=True) if h1 else ''
        lead = f'<div class="lead-img"><img src="{html.escape(url, quote=True)}" alt="{alt}" loading="eager" decoding="async"></div>'
        s = s[:m.end(1)] + '\n' + lead + s[m.end(1):]
        f.write_text(s, encoding='utf-8'); n += 1
    print(n, 'EN/AR posts got their featured image')

def main():
    dry = '--dry' in sys.argv
    if not dry: add_lead_images()
    todo = collect()
    jobs = sorted({x for v in todo.values() for x in v})
    print(len(todo), 'pages,', len(jobs), 'remote images')
    if dry: return
    imgmap = json.load(open(DATA / 'imgmap.json', encoding='utf-8'))
    # download in parallel first (network bound), then convert serially through lib.img
    need = [s for s, w in jobs if not any((OUT / out_name(_key(c), w)).exists() for c in {full_url(s), s})]
    pre = {}
    def dl(s):
        for c in dict.fromkeys([full_url(s), s]):
            if _key(c) in lib._IMG_BY_PATH and (RAW / lib._IMG_BY_PATH[_key(c)]).exists(): return
            d, via = fetch(c)
            if d: pre[c] = (d, via); return
    with cf.ThreadPoolExecutor(6) as ex: list(ex.map(dl, sorted(set(need))))
    for c, (d, via) in pre.items():
        ext = os.path.splitext(u.unquote(u.urlsplit(c).path))[1].lower() or '.jpg'
        known = imgmap.get(c) if (imgmap.get(c) or {}).get('ok') else None
        fn = known['file'] if known else hashlib.sha1(_key(c).encode()).hexdigest()[:16] + ext
        RAW.mkdir(parents=True, exist_ok=True); (RAW / fn).write_bytes(d)
        if not known: imgmap[c] = {'ok': True, 'file': fn, 'bytes': len(d), 'via': via}
        lib._IMG_BY_PATH[_key(c)] = fn
    done = {}
    for s, w in jobs:
        done[(s, w)] = ensure(s, w, imgmap)
    failed = sorted({s for (s, w), r in done.items() if not r})
    changed = 0
    for f, found in todo.items():
        s0 = f.read_text(encoding='utf-8')
        def fix_img(t, w):
            src = html.unescape(attr(t, 'src') or '')
            r = done.get((src, w))
            if r: return retag(t, f, r)
            if src in DEAD and (full_url(src) == src or full_url(src) in DEAD):   # gone from the live site and the archive
                if w == 640:    # card: same fallback thumbnail pages_posts.card() uses
                    return retag(t, f, {'src': FALLBACK, 'w': 1280, 'h': 720})
                return '\x00'   # in-body: drop the dead picture instead of showing a broken icon
            return t
        def fix_article(m):
            a = m.group(0)
            def fix_link(lm):
                img = fix_img(lm.group(4), 1400)
                if img == '\x00': return img
                href = html.unescape(lm.group(2))
                if REMOTE.match(href) and re.search(r'\.(jpe?g|png|gif|webp)$', href, re.I):
                    big = done.get((html.unescape(attr(lm.group(4), 'src') or ''), 1400))
                    if big: return lm.group(1) + rel(f, big['src']) + lm.group(3) + img
                return lm.group(1) + lm.group(2) + lm.group(3) + img
            a = LINK_IMG.sub(fix_link, a)
            a = IMG.sub(lambda im: fix_img(im.group(0), 1400) if REMOTE.match(html.unescape(attr(im.group(0), 'src') or '')) else im.group(0), a)
            a = re.sub(r'<(p|div class="lead-img")>\s*\x00\s*</(p|div)>', '', a)
            return a.replace('\x00', '')
        s1 = ARTICLE.sub(fix_article, s0)
        s1 = CARD_PH.sub(lambda m: re.sub(r'<img\b[^>]*>', lambda im: fix_img(im.group(0), 640), m.group(0)), s1)
        if s1 != s0:
            f.write_text(s1, encoding='utf-8'); changed += 1
    (DATA / 'imgmap.json').write_text(json.dumps(imgmap, ensure_ascii=False, indent=2), encoding='utf-8')
    print(changed, 'pages rewritten;', len(failed), 'images could not be fetched')
    for x in failed: print('  FAILED', x)

if __name__ == '__main__':
    main()
