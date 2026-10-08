#!/usr/bin/env python3
"""Fetch all FA posts from the live WP REST API, update posts.json + known_cats.json.

Adds published, non-ads posts that are missing from posts.json (verbatim content.rendered,
with Elementor/script/inline-style wrappers stripped). Also refreshes known_cats for every
REST post. Optionally downloads featured (+ inline) images into tools/redesign/.img-raw
and marks them ok in imgmap.json.

Usage:
  python3 tools/redesign/fetch_posts_rest.py
"""
from __future__ import annotations

import hashlib, json, os, pathlib, re, sys, time, urllib.parse as u, urllib.request
from datetime import datetime, timezone
from html import unescape

ROOT = pathlib.Path(__file__).resolve().parents[2]
DATA = pathlib.Path(__file__).resolve().parent / 'data'
RAW = pathlib.Path(os.environ.get(
    'ABADIS_IMG_RAW',
    str(pathlib.Path(__file__).resolve().parent / '.img-raw'),
))
BASE = 'http://abadis-med.com/wp-json/wp/v2'
UA = 'AbadisRedesignBot/1.0 (+local rebuild; contact info@abadis-med.com)'

CAT_ID = {
    22: 'newss',
    6: 'blog',
    74: 'ads',
    20: 'accessories',
    21: 'products',
    69: 'install',
    76: 'device',
    1: 'uncategorized',
}


def get_json(url, timeout=60):
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': 'application/json'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode('utf-8')), dict(r.headers)


def strip_tags(h):
    return re.sub(r'\s+', ' ', unescape(re.sub(r'<[^>]+>', ' ', h or ''))).strip()


def clean_content(html: str) -> str:
    """Keep verbatim text; drop scripts/styles/Elementor chrome and inline styles."""
    if not html:
        return ''
    h = html
    h = re.sub(r'<script\b[^>]*>.*?</script>', '', h, flags=re.S | re.I)
    h = re.sub(r'<style\b[^>]*>.*?</style>', '', h, flags=re.S | re.I)
    h = re.sub(r'<noscript\b[^>]*>.*?</noscript>', '', h, flags=re.S | re.I)
    h = re.sub(r'<!--.*?-->', '', h, flags=re.S)
    h = re.sub(r'\sstyle=(["\'])(.*?)\1', '', h, flags=re.I | re.S)
    h = re.sub(r'\sdata-(?:elementor|settings|widget_type|id|model-cid)[^=]*=(["\'])(.*?)\1', '', h, flags=re.I)
    # Drop empty class="" left after elementor class removal later
    h = re.sub(r'\sclass=(["\'])([^"\']*elementor[^"\']*)\1', lambda m: '' if 'elementor' in m.group(2).lower() else m.group(0), h, flags=re.I)
    h = re.sub(r'\sclass=(["\'])\s*\1', '', h)
    h = re.sub(r'<div>\s*</div>', '', h)
    h = re.sub(r'<p>\s*</p>', '', h)
    return h.strip()


def pick_cat(ids):
    names = [CAT_ID[i] for i in ids if i in CAT_ID]
    if 'ads' in names:
        return 'ads'
    if 'newss' in names:
        return 'newss'
    for pref in ('blog', 'products', 'accessories', 'install', 'device'):
        if pref in names:
            return pref
    if 'uncategorized' in names:
        return 'uncategorized'
    return names[0] if names else 'uncategorized'


def iso_date(p):
    raw = p.get('date_gmt') or p.get('date') or ''
    if not raw:
        return datetime.now(timezone.utc).isoformat()
    if raw.endswith('Z'):
        return raw.replace('Z', '+00:00')
    if re.search(r'[+-]\d{2}:\d{2}$', raw):
        return raw
    # WP date_gmt is UTC without offset
    return raw + '+00:00'


def fetch_all_posts():
    fields = 'id,date,date_gmt,modified,modified_gmt,slug,link,title,excerpt,content,featured_media,categories,status'
    out = []
    page = 1
    while True:
        url = f'{BASE}/posts?per_page=50&page={page}&_fields={fields}&status=publish'
        try:
            batch, hdrs = get_json(url)
        except Exception as e:
            if page > 1 and '404' in str(e):
                break
            raise
        if not batch:
            break
        out.extend(batch)
        total_pages = int(hdrs.get('X-WP-TotalPages') or hdrs.get('x-wp-totalpages') or 1)
        print(f'  posts page {page}/{total_pages}: +{len(batch)} (total {len(out)})')
        if page >= total_pages:
            break
        page += 1
        time.sleep(0.15)
    return out


def fetch_media_map(ids):
    """id -> source_url for featured media."""
    ids = sorted({i for i in ids if i})
    out = {}
    for i in range(0, len(ids), 50):
        chunk = ids[i:i + 50]
        q = ','.join(str(x) for x in chunk)
        url = f'{BASE}/media?include={q}&per_page=100&_fields=id,source_url'
        try:
            batch, _ = get_json(url)
        except Exception as e:
            print('  media batch fail', e)
            continue
        for m in batch:
            if m.get('source_url'):
                out[m['id']] = m['source_url']
        time.sleep(0.1)
    return out


def http_to_candidates(url: str):
    """Yield download candidates for a WP upload URL."""
    if not url:
        return
    if url.startswith('//'):
        url = 'https:' + url
    # prefer http (https often blocked)
    http = re.sub(r'^https://', 'http://', url)
    yield http
    # strip -WxH before extension
    unsized = re.sub(r'-\d+x\d+(\.\w+)$', r'\1', http)
    if unsized != http:
        yield unsized
    # Wayback im_
    yield 'https://web.archive.org/web/2026im_/' + url


def download_image(url: str, dest: pathlib.Path) -> bool:
    for cand in http_to_candidates(url):
        try:
            req = urllib.request.Request(cand, headers={'User-Agent': UA})
            with urllib.request.urlopen(req, timeout=20) as r:
                data = r.read()
            if len(data) < 32:
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
            return True
        except Exception:
            continue
    return False


def ensure_img(url: str, imgmap: dict) -> str | None:
    """Download url into RAW if needed; return local file name or None."""
    if not url:
        return None
    key = url
    # normalize key to https form used in imgmap when possible
    keys = {url, re.sub(r'^http://', 'https://', url), re.sub(r'^https://', 'http://', url)}
    for k in list(keys):
        keys.add(re.sub(r'-\d+x\d+(\.\w+)$', r'\1', k))
    for k in keys:
        ent = imgmap.get(k)
        if ent and ent.get('ok') and ent.get('file'):
            if (RAW / ent['file']).exists() or True:
                # file may be absent locally but OUT webp exists; still mark ok
                return ent['file']
    # new file name
    path = u.urlsplit(url).path
    ext = pathlib.Path(u.unquote(path)).suffix.lower() or '.jpg'
    if ext not in ('.jpg', '.jpeg', '.png', '.webp', '.gif', '.svg'):
        ext = '.jpg'
    name = hashlib.sha1(u.unquote(path).encode()).hexdigest()[:16] + ext
    dest = RAW / name
    if not dest.exists():
        ok = download_image(url, dest)
        if not ok:
            for k in keys:
                imgmap[k if k.startswith('http') else url] = {'ok': False, 'err': 'fetch-failed'}
            # store under https canonical
            canon = re.sub(r'^http://', 'https://', url)
            imgmap[canon] = {'ok': False, 'err': 'fetch-failed'}
            return None
    canon = re.sub(r'^http://', 'https://', url)
    imgmap[canon] = {'ok': True, 'file': name, 'bytes': dest.stat().st_size}
    # also index unsized
    unsized = re.sub(r'-\d+x\d+(\.\w+)$', r'\1', canon)
    if unsized != canon:
        imgmap[unsized] = dict(imgmap[canon])
    return name


def content_img_urls(html: str):
    return re.findall(r'src=["\']([^"\']+/wp-content/uploads/[^"\']+)["\']', html or '', flags=re.I)


def main():
    print('Fetching posts from', BASE)
    rest = fetch_all_posts()
    print('REST posts:', len(rest))

    media_ids = [p.get('featured_media') or 0 for p in rest]
    print('Fetching featured media…')
    media = fetch_media_map(media_ids)
    print('  media urls:', len(media))

    posts_path = DATA / 'posts.json'
    cats_path = DATA / 'known_cats.json'
    imgmap_path = DATA / 'imgmap.json'
    local = json.load(open(posts_path, encoding='utf-8'))
    known = json.load(open(cats_path, encoding='utf-8'))
    imgmap = json.load(open(imgmap_path, encoding='utf-8'))

    by_id = {str(p['id']): i for i, p in enumerate(local)}
    by_url = {u.unquote(p['url']).rstrip('/'): i for i, p in enumerate(local)}

    snap = 'rest-' + datetime.now(timezone.utc).strftime('%Y%m%d')
    added = []
    skipped_ads = []
    updated_cats = 0
    uncategorized = []

    for p in rest:
        link = p.get('link') or ''
        link_dec = u.unquote(link).rstrip('/')
        cat = pick_cat(p.get('categories') or [])
        known[link_dec] = cat
        # also store percent-encoded form if different
        if link.rstrip('/') != link_dec:
            known[link.rstrip('/')] = cat
        updated_cats += 1
        if cat == 'uncategorized':
            uncategorized.append({
                'id': p['id'],
                'title': strip_tags(p.get('title', {}).get('rendered', '')),
                'url': link_dec,
            })

        if cat == 'ads':
            skipped_ads.append(p['id'])
            continue
        if (p.get('status') or 'publish') != 'publish':
            continue

        if str(p['id']) in by_id or link_dec in by_url:
            continue

        title = strip_tags(p.get('title', {}).get('rendered', ''))
        excerpt = strip_tags(p.get('excerpt', {}).get('rendered', ''))
        content = clean_content(p.get('content', {}).get('rendered', ''))
        image = media.get(p.get('featured_media') or 0) or ''
        path = u.urlsplit(link_dec).path
        if not path.endswith('/'):
            path += '/'

        # images
        if image:
            ensure_img(image, imgmap)
        for src in content_img_urls(content)[:40]:
            ensure_img(src, imgmap)

        rec = {
            'url': link_dec if link_dec.startswith('http') else ('https://abadis-med.com' + path),
            'path': path,
            'id': str(p['id']),
            'snapshot': snap,
            'title': title,
            'desc': excerpt,
            'image': re.sub(r'^http://', 'https://', image) if image else '',
            'date': iso_date(p),
            'modified': iso_date({'date_gmt': p.get('modified_gmt'), 'date': p.get('modified')}),
            'author': '',
            'mode': 'rest',
            'blocks': [{'t': 'html', 'html': content}],
        }
        # prefer https URL
        if rec['url'].startswith('http://'):
            rec['url'] = 'https://' + rec['url'][len('http://'):]
        local.append(rec)
        by_id[str(p['id'])] = len(local) - 1
        by_url[link_dec] = len(local) - 1
        added.append({'id': rec['id'], 'title': title, 'cat': cat, 'path': path})
        print('  +', rec['id'], cat, title[:70])

    # sort local by date desc for readability
    local.sort(key=lambda x: x.get('date') or '', reverse=True)

    json.dump(local, open(posts_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    json.dump(known, open(cats_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    json.dump(imgmap, open(imgmap_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

    report = {
        'rest_total': len(rest),
        'posts_json_total': len(local),
        'added': added,
        'skipped_ads': skipped_ads,
        'known_cats_entries': len(known),
        'uncategorized': uncategorized,
        'imgmap_ok': sum(1 for v in imgmap.values() if v.get('ok')),
    }
    out = DATA / 'rest-fetch-report.json'
    json.dump(report, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print('Wrote', posts_path, 'posts=', len(local), 'added=', len(added))
    print('known_cats=', len(known), 'ads skipped=', len(skipped_ads))
    print('uncategorized=', len(uncategorized))
    print('report', out)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print('FAIL', e, file=sys.stderr)
        raise
