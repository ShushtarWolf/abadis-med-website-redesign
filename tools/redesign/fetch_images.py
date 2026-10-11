#!/usr/bin/env python3
"""Recover missing images for the Abadis redesign generator.

For each candidate URL (imgmap not-ok + posts/pages/products/team/customers/SDG/ISO):
  1) try http://abadis-med.com/... (https→http, also unsized -WxH)
  2) try Wayback im_ + CDX
Never overwrite an existing RAW file or an already-built WebP in site/assets/img/c/.

Usage:
  python3 tools/redesign/fetch_images.py
"""
from __future__ import annotations

import concurrent.futures as cf
import hashlib, json, os, pathlib, re, sys, time, urllib.error, urllib.parse as u, urllib.request
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[2]
DATA = pathlib.Path(__file__).resolve().parent / 'data'
SITE = ROOT / 'site'
RAW = pathlib.Path(os.environ.get(
    'ABADIS_IMG_RAW',
    str(pathlib.Path(__file__).resolve().parent / '.img-raw'),
))
OUT_IMG = SITE / 'assets/img/c'
UA = 'AbadisRedesignBot/1.0 (+local rebuild; contact info@abadis-med.com)'
TIMEOUT = 20
MAX_WORKERS = 4
ISO_URLS = [
    'https://abadis-med.com/wp-content/uploads/2025/04/ISO.jpg',
    'https://abadis-med.com/wp-content/uploads/2025/01/گواهینامه-ایزو-scaled.jpg',
]
PRODUCT_URLS = [
    'https://abadis-med.com/wp-content/uploads/2022/12/کیسه-ساکشن.jpg',
    'https://abadis-med.com/wp-content/uploads/2022/12/پایه-ترولی.jpg',
    'https://abadis-med.com/wp-content/uploads/2022/12/فیلتر1-2-845x684-1.jpg',
    'https://abadis-med.com/wp-content/uploads/2022/12/ساکشن-تیوب-7e83722522e8aeb7512b7075311316b7__m8ULku2SAG__1-1-300x300.jpg',
    'https://abadis-med.com/wp-content/uploads/2022/12/AMR_4901.jpg',
    'https://abadis-med.com/wp-content/uploads/2022/12/اتصالات-845x684-1.jpg',
    'https://abadis-med.com/wp-content/uploads/2022/12/ساکشن-دیواری-بزرگسال-1030x1030-1.jpg',
    'https://abadis-med.com/wp-content/uploads/2022/12/نگهدارنده-لوله-تراشه-1030x1030-1.jpg',
    'https://abadis-med.com/wp-content/uploads/2022/12/ANIMATED-LINER-BAG-01.png',
]


def canon(url: str) -> str:
    if not url:
        return ''
    if url.startswith('//'):
        url = 'https:' + url
    url = url.strip()
    return re.sub(r'^http://', 'https://', url)


def path_key(url: str) -> str:
    return u.unquote(u.urlsplit(url).path)


def encode_url(url: str) -> str:
    parts = u.urlsplit(url)
    path = u.quote(u.unquote(parts.path), safe='/')
    return u.urlunsplit((parts.scheme, parts.netloc, path, parts.query, parts.fragment))


def httpize(url: str) -> str:
    return re.sub(r'^https://', 'http://', canon(url))


def unsized(url: str) -> str:
    return re.sub(r'-\d+x\d+(\.\w+)$', r'\1', url)


def out_name_for(url: str, maxw: int = 1400) -> str:
    return hashlib.sha1(path_key(url).encode()).hexdigest()[:12] + f'-{maxw}.webp'


def raw_name_for(url: str) -> str:
    p = path_key(url)
    ext = pathlib.Path(p).suffix.lower() or '.jpg'
    if ext not in ('.jpg', '.jpeg', '.png', '.webp', '.gif', '.svg', '.bmp'):
        ext = '.jpg'
    return hashlib.sha1(p.encode()).hexdigest()[:16] + ext


def already_have(url: str, imgmap: dict) -> bool:
    """True if RAW exists or any common WebP output exists — do not re-download."""
    c = canon(url)
    for key in {c, httpize(c), unsized(c), unsized(httpize(c))}:
        ent = imgmap.get(key) or imgmap.get(canon(key))
        if ent and ent.get('ok') and ent.get('file'):
            if (RAW / ent['file']).exists():
                return True
    name = raw_name_for(c)
    if (RAW / name).exists():
        return True
    # built webps at common maxw used by generator
    for mw in (300, 400, 480, 600, 640, 700, 900, 1000, 1200, 1400, 1600, 240):
        if (OUT_IMG / out_name_for(c, mw)).exists():
            return True
        if (OUT_IMG / out_name_for(unsized(c), mw)).exists():
            return True
    return False


def candidates(url: str):
    c = canon(url)
    http = httpize(c)
    yield encode_url(http)
    us = unsized(http)
    if us != http:
        yield encode_url(us)
    # Wayback im_ on original https
    yield 'https://web.archive.org/web/2026im_/' + encode_url(c)
    if unsized(c) != c:
        yield 'https://web.archive.org/web/2026im_/' + encode_url(unsized(c))


def cdx_lookup(url: str) -> str | None:
    q = u.urlencode({'url': canon(url), 'output': 'json', 'filter': 'statuscode:200', 'limit': '5'})
    api = 'https://web.archive.org/cdx/search/cdx?' + q
    try:
        req = urllib.request.Request(api, headers={'User-Agent': UA})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            rows = json.loads(r.read().decode())
        if not rows or len(rows) < 2:
            return None
        # ["urlkey","timestamp","original","mimetype","statuscode","digest","length"]
        ts, original = rows[1][1], rows[1][2]
        return f'https://web.archive.org/web/{ts}im_/{original}'
    except Exception:
        return None


def download_one(url: str) -> tuple[bytes | None, str | None, str]:
    """Return (bytes, final_url, note)."""
    tried = []
    for cand in candidates(url):
        tried.append(cand)
        try:
            req = urllib.request.Request(cand, headers={'User-Agent': UA, 'Accept': 'image/*,*/*'})
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                data = r.read()
            if len(data) >= 64 and not data[:200].lstrip().lower().startswith(b'<!doctype') and not data[:100].lstrip().lower().startswith(b'<html'):
                return data, cand, 'ok'
        except Exception as e:
            tried.append(f'ERR:{type(e).__name__}')
            continue
    # CDX fallback
    wb = cdx_lookup(url)
    if wb:
        try:
            req = urllib.request.Request(encode_url(wb) if 'uploads' in wb else wb, headers={'User-Agent': UA})
            # wb already absolute; encode path of original embedded awkwardly — request as-is
            req = urllib.request.Request(wb, headers={'User-Agent': UA})
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                data = r.read()
            if len(data) >= 64:
                return data, wb, 'cdx'
        except Exception:
            pass
    return None, None, 'fail'


def collect_urls() -> list[str]:
    imgmap = json.load(open(DATA / 'imgmap.json', encoding='utf-8'))
    posts = json.load(open(DATA / 'posts.json', encoding='utf-8'))
    pages = json.load(open(DATA / 'pages.json', encoding='utf-8'))
    urls: set[str] = set()

    for k, v in imgmap.items():
        if not v.get('ok'):
            urls.add(canon(k))

    for p in posts:
        if p.get('image'):
            urls.add(canon(p['image']))
        for b in p.get('blocks') or []:
            if b.get('t') == 'img' and b.get('src'):
                urls.add(canon(b['src']))
            if b.get('t') == 'html' and b.get('html'):
                for src in re.findall(r'src=["\']([^"\']+/wp-content/uploads/[^"\']+)["\']', b['html'], flags=re.I):
                    urls.add(canon(src))

    # pages: team, customers, sdg, about, products content
    for path, page in pages.items():
        for b in page.get('blocks') or []:
            if b.get('t') == 'img' and b.get('src'):
                urls.add(canon(b['src']))
            if b.get('t') == 'member' and b.get('img'):
                urls.add(canon(b['img']))
            if b.get('t') == 'box' and b.get('img'):
                urls.add(canon(b['img']))
            if b.get('t') == 'gallery':
                for im in b.get('imgs') or []:
                    if im.get('src'):
                        urls.add(canon(im['src']))
            if b.get('t') == 'html' and b.get('html'):
                for src in re.findall(r'src=["\']([^"\']+/wp-content/uploads/[^"\']+)["\']', b['html'], flags=re.I):
                    urls.add(canon(src))
        # customers nested items
        for b in page.get('blocks') or []:
            for it in b.get('items') or []:
                for x in it.get('blocks') or []:
                    if x.get('t') == 'img' and x.get('src'):
                        urls.add(canon(x['src']))

    for url in ISO_URLS + PRODUCT_URLS:
        urls.add(canon(url))

    # drop empties / non-uploads
    out = sorted(x for x in urls if x and '/wp-content/uploads/' in x)
    return out


def sync_post_featured_from_rest(posts: list, imgmap: dict) -> int:
    """Fill empty posts[].image from WP REST featured_media."""
    need = [p for p in posts if not p.get('image') and p.get('id')]
    if not need:
        return 0
    print(f'Syncing featured media for {len(need)} posts without image field…')
    # fetch by id
    updated = 0
    for i in range(0, len(need), 20):
        chunk = need[i:i + 20]
        ids = ','.join(p['id'] for p in chunk)
        api = f'http://abadis-med.com/wp-json/wp/v2/posts?include={ids}&per_page=100&_fields=id,featured_media'
        try:
            req = urllib.request.Request(api, headers={'User-Agent': UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                batch = json.loads(r.read().decode())
        except Exception as e:
            print('  REST posts fail', e)
            continue
        media_ids = [x.get('featured_media') for x in batch if x.get('featured_media')]
        media = {}
        if media_ids:
            q = ','.join(str(m) for m in media_ids)
            murl = f'http://abadis-med.com/wp-json/wp/v2/media?include={q}&per_page=100&_fields=id,source_url'
            try:
                req = urllib.request.Request(murl, headers={'User-Agent': UA})
                with urllib.request.urlopen(req, timeout=60) as r:
                    for m in json.loads(r.read().decode()):
                        media[m['id']] = m.get('source_url') or ''
            except Exception as e:
                print('  REST media fail', e)
        by_id = {str(x['id']): x for x in batch}
        for p in chunk:
            wp = by_id.get(str(p['id']))
            if not wp:
                continue
            src = media.get(wp.get('featured_media') or 0) or ''
            if src:
                p['image'] = canon(src)
                updated += 1
        time.sleep(0.1)
    print(f'  filled image on {updated} posts')
    return updated


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    imgmap = json.load(open(DATA / 'imgmap.json', encoding='utf-8'))
    posts = json.load(open(DATA / 'posts.json', encoding='utf-8'))
    sync_post_featured_from_rest(posts, imgmap)

    urls = collect_urls()
    # re-collect after posts image fill
    for p in posts:
        if p.get('image'):
            urls.append(canon(p['image']))
    urls = sorted(set(urls))

    todo = []
    skipped_have = 0
    for url in urls:
        if already_have(url, imgmap):
            # ensure imgmap marks ok if webp/raw exists but map said false
            c = canon(url)
            name = raw_name_for(c)
            if (RAW / name).exists():
                imgmap[c] = {'ok': True, 'file': name, 'bytes': (RAW / name).stat().st_size}
            else:
                # map to synthetic ok pointing at existing webp via empty raw? generator needs RAW OR existing OUT.
                # Mark ok with file name even if raw missing — img() reuses OUT by hash of path.
                ent = imgmap.get(c) or {}
                if not ent.get('ok'):
                    imgmap[c] = {'ok': True, 'file': ent.get('file') or name, 'note': 'reused-existing-output'}
            skipped_have += 1
            continue
        todo.append(url)

    print(f'Candidates: {len(urls)}  already present: {skipped_have}  to fetch: {len(todo)}')

    log = {
        'started': datetime.now(timezone.utc).isoformat(),
        'ok': [],
        'fail': [],
        'skipped_existing': skipped_have,
    }

    def work(url: str):
        data, final, note = download_one(url)
        return url, data, final, note

    ok_n = fail_n = 0
    with cf.ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futs = [ex.submit(work, url) for url in todo]
        for i, fut in enumerate(cf.as_completed(futs), 1):
            url, data, final, note = fut.result()
            c = canon(url)
            if data:
                name = raw_name_for(c)
                dest = RAW / name
                if not dest.exists():
                    dest.write_bytes(data)
                imgmap[c] = {'ok': True, 'file': name, 'bytes': dest.stat().st_size, 'via': note}
                # also index unsized + http twin
                for k in {unsized(c), httpize(c), unsized(httpize(c))}:
                    imgmap[canon(k)] = dict(imgmap[c])
                log['ok'].append({'url': c, 'file': name, 'bytes': dest.stat().st_size, 'via': final})
                ok_n += 1
            else:
                imgmap[c] = {'ok': False, 'err': 'fetch-failed'}
                log['fail'].append({'url': c})
                fail_n += 1
            if i % 25 == 0 or i == len(todo):
                print(f'  progress {i}/{len(todo)}  ok={ok_n} fail={fail_n}')

    log['finished'] = datetime.now(timezone.utc).isoformat()
    log['ok_count'] = ok_n
    log['fail_count'] = fail_n

    json.dump(imgmap, open(DATA / 'imgmap.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    json.dump(posts, open(DATA / 'posts.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    json.dump(log, open(DATA / 'img-fetch-log.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print(f'Done. fetched_ok={ok_n} fail={fail_n} imgmap_ok={sum(1 for v in imgmap.values() if v.get("ok"))}/{len(imgmap)}')
    print('log → tools/redesign/data/img-fetch-log.json')


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print('FAIL', e, file=sys.stderr)
        raise
