#!/usr/bin/env python3
"""Download missing EN/AR post images (Yoast OG, featured, in-body) into the raw cache and imgmap.

The FA posts builder already syncs images via fetch_post_images.py; i18n REST snapshots
use /en/wp-content/... paths that are absent from imgmap until this runs.

Usage: python3 tools/redesign/fetch_i18n_post_images.py
"""
import sys, re, json, html, hashlib, pathlib, urllib.parse as u, urllib.request, concurrent.futures as cf

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import lib

DATA = pathlib.Path(__file__).resolve().parent / 'data'
UA = 'Mozilla/5.0 (AbadisRedesign image sync; info@abadis-med.com)'


def refs(wp, lang):
    out = []
    yj = wp.get('yoast_head_json') or {}
    for o in yj.get('og_image') or []:
        url = o.get('url')
        if url:
            out.append(url)
    raw = wp.get('content', {}).get('rendered') or ''
    out += [html.unescape(m) for m in re.findall(r'<img [^>]*src="([^"]+)"', raw)]
    out += [html.unescape(m) for m in re.findall(r"<img [^>]*src='([^']+)'", raw)]
    out += featured_media_url(wp, lang)
    return [x for x in out if x and 'gravatar.com' not in x]


def featured_media_url(wp, lang):
    fm = wp.get('featured_media') or 0
    if not fm:
        return []
    base = 'http://abadis-med.com/'
    if lang == 'en':
        base += 'en/'
    elif lang == 'ar':
        base += 'arabic/'
    api = f'{base}wp-json/wp/v2/media/{fm}?_fields=source_url'
    try:
        r = urllib.request.urlopen(urllib.request.Request(api, headers={'User-Agent': UA}), timeout=30)
        data = json.loads(r.read().decode())
        src = data.get('source_url')
        return [src] if src else []
    except Exception:
        return []


def enc(url):
    if url.startswith('//'):
        url = 'https:' + url
    p = u.urlsplit(url)
    return u.urlunsplit((p.scheme or 'https', p.netloc, u.quote(u.unquote(p.path)), p.query, ''))


def _open(url, t=60):
    r = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=t)
    d = r.read()
    return d if len(d) > 500 and d[:4] in (b'\x89PNG', b'GIF8', b'RIFF') or d[:2] == b'\xff\xd8' else None


def get(url):
    e = enc(url)
    for c in (e, e.replace('https://', 'http://', 1), 'https://web.archive.org/web/2024id_/' + e):
        try:
            d = _open(c)
            if d:
                return d
        except Exception:
            pass
    return None


def one(remote):
    for cand in dict.fromkeys((lib.full_url(remote), remote)):
        d = get(cand)
        if d:
            key = lib._key(cand if cand.startswith('http') else 'https:' + cand)
            ext = (pathlib.PurePath(key).suffix or '.jpg').lower()
            f = hashlib.sha1(key.encode()).hexdigest()[:16] + ext
            (lib.RAW / f).write_bytes(d)
            return cand, f, len(d)
    return remote, None, 0


def main():
    lib.RAW.mkdir(parents=True, exist_ok=True)
    m = json.loads((DATA / 'imgmap.json').read_text(encoding='utf-8'))
    feat_urls = {}
    todo = []
    for lang in ('en', 'ar'):
        posts = json.load(open(DATA / f'{lang}_posts.json', encoding='utf-8'))
        for wp in posts:
            for u in featured_media_url(wp, lang):
                feat_urls[f'{lang}:{wp["id"]}'] = u
            for r in refs(wp, lang):
                if lib.best_img(r, 640):
                    continue
                todo.append(r)
    todo = list(dict.fromkeys(todo))
    ok = fail = 0
    failed = []
    with cf.ThreadPoolExecutor(8) as ex:
        for cand, f, n in ex.map(one, todo):
            k = cand if cand.startswith('http') else 'https:' + cand
            if f:
                m[k] = {'ok': True, 'file': f, 'bytes': n, 'via': 'i18n-post-sync'}
                ok += 1
            else:
                failed.append(cand)
                fail += 1
    (DATA / 'imgmap.json').write_text(json.dumps(m, ensure_ascii=False, indent=2), encoding='utf-8')
    (DATA / 'i18n_featured_urls.json').write_text(json.dumps(feat_urls, ensure_ascii=False, indent=2), encoding='utf-8')
    (DATA / 'i18n-post-img-fetch-failed.json').write_text(json.dumps(failed, ensure_ascii=False, indent=2), encoding='utf-8')
    print('todo', len(todo), 'ok', ok, 'failed', fail, 'featured', len(feat_urls))


if __name__ == '__main__':
    main()