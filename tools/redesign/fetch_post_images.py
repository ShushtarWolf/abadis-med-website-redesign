#!/usr/bin/env python3
"""Download missing news/article images (featured + in-body) from the live abadis-med.com into the raw cache
and register them in data/imgmap.json; build.py then converts them to WebP in site/assets/img/c/.
Usage: python3 tools/redesign/fetch_post_images.py"""
import sys, re, json, html, hashlib, pathlib, urllib.parse as u, urllib.request, concurrent.futures as cf
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import lib, pages_posts
DATA = pathlib.Path(__file__).resolve().parent / 'data'
UA = 'Mozilla/5.0 (AbadisRedesign image sync; info@abadis-med.com)'

def refs(x):
    out = [x['image']] if x.get('image') else []
    for b in x['blocks']:
        if b['t'] == 'img': out.append(b['src'])
        if b['t'] == 'html' and b.get('html'):
            out += [html.unescape(m) for m in re.findall(r'<img [^>]*src="([^"]+)"', b['html'])]
            out += [html.unescape(m) for m in re.findall(r'<img [^>]*src=\'([^\']+)\'', b['html'])]
    return out

def enc(url):
    if url.startswith('//'): url = 'https:' + url
    p = u.urlsplit(url); return u.urlunsplit((p.scheme or 'https', p.netloc, u.quote(u.unquote(p.path)), p.query, ''))

def _open(url, t=60):
    r = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=t)
    d = r.read()
    return d if len(d) > 500 and d[:4] in (b'\x89PNG', b'GIF8', b'RIFF') or d[:2] == b'\xff\xd8' else None

def get(url):
    """live site first (https, then http), then the Wayback Machine original (id_)."""
    e = enc(url)
    for c in (e, e.replace('https://', 'http://', 1), 'https://web.archive.org/web/2024id_/' + e):
        try:
            d = _open(c)
            if d: return d
        except Exception: pass
    return None

def main():
    pages_posts.prepare()
    m = json.loads((DATA / 'imgmap.json').read_text(encoding='utf-8'))
    todo = []
    for x in pages_posts.POSTS:
        for r in refs(x):
            if lib.best_img(r, 640): continue
            todo.append(r)
    todo = list(dict.fromkeys(todo)); lib.RAW.mkdir(parents=True, exist_ok=True)
    def one(r):
        for cand in dict.fromkeys((lib.full_url(r), r)):
            d = get(cand)
            if d:
                key = lib._key(cand if cand.startswith('http') else 'https:' + cand)
                ext = (pathlib.PurePath(key).suffix or '.jpg').lower()
                f = hashlib.sha1(key.encode()).hexdigest()[:16] + ext
                (lib.RAW / f).write_bytes(d)
                return cand, f, len(d)
        return r, None, 0
    ok = fail = 0; failed = []
    with cf.ThreadPoolExecutor(6) as ex:
        for cand, f, n in ex.map(one, todo):
            k = cand if cand.startswith('http') else 'https:' + cand
            if f: m[k] = {'ok': True, 'file': f, 'bytes': n, 'via': 'live-2026-10-14'}; ok += 1
            else: failed.append(cand); fail += 1
    (DATA / 'imgmap.json').write_text(json.dumps(m, ensure_ascii=False, indent=2), encoding='utf-8')
    (DATA / 'post-img-fetch-failed.json').write_text(json.dumps(failed, ensure_ascii=False, indent=2), encoding='utf-8')
    print('todo', len(todo), 'ok', ok, 'failed', fail)
if __name__ == '__main__': main()
