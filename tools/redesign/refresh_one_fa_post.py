#!/usr/bin/env python3
"""Refresh one FA post from WP REST into posts.json, fetch inline images, patch site HTML.

Usage: python3 tools/redesign/refresh_one_fa_post.py POST_ID [site_slug_dir_name]
"""
from __future__ import annotations

import json
import pathlib
import re
import sys
import urllib.parse as u
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[2]
DATA = pathlib.Path(__file__).resolve().parent / 'data'
SITE = ROOT / 'site'

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from fetch_posts_rest import clean_content, strip_tags, content_img_urls, ensure_img, iso_date
from fetch_images import download_one, canon, raw_name_for
import lib
from render import blocks_to_prose
from datetime import datetime, timezone

UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'


def wp_clean_html(raw: str) -> str:
    h = clean_content(raw)
    h = re.sub(r'\?utm_source=[^"\'&\s>]+', '', h)
    h = re.sub(r'&amp;utm_source=[^"\'&\s>]+', '', h)
    h = re.sub(r'<img[^>]*google\.com/s2/favicons[^>]*>\s*', '', h, flags=re.I)
    return h


def fetch_post(post_id: str) -> dict:
    """WP REST post; tries https://www. first (bare http host is often down), then the old URL."""
    q = f'/wp-json/wp/v2/posts/{post_id}?_fields=id,slug,link,title,excerpt,content,date,date_gmt,modified,modified_gmt,featured_media'
    err = None
    for base in ('https://www.abadis-med.com', 'http://abadis-med.com'):
        for _ in range(3):
            try:
                req = urllib.request.Request(base + q, headers={'User-Agent': UA, 'Accept': 'application/json'})
                with urllib.request.urlopen(req, timeout=60) as r:
                    return json.loads(r.read().decode('utf-8'))
            except Exception as e:  # noqa: BLE001
                err = e
    raise err


def reload_imgmap():
    lib.IMGMAP = json.load(open(DATA / 'imgmap.json', encoding='utf-8'))
    lib._IMG_BY_PATH = {}
    for k, v in lib.IMGMAP.items():
        if v.get('ok'):
            lib._IMG_BY_PATH[lib._key(k)] = v['file']
    lib._done = {}


def ensure_webp(url: str, maxw: int = 1000):
    for mw in (maxw, 1000, 1200, 1400):
        r = lib.best_img(url, mw)
        if r:
            return r
    return lib.img(url, maxw)


def main():
    if len(sys.argv) < 2:
        print('usage: refresh_one_fa_post.py POST_ID [site_subdir]', file=sys.stderr)
        sys.exit(2)
    post_id = str(sys.argv[1])
    site_dir = sys.argv[2] if len(sys.argv) > 2 else None

    posts_path = DATA / 'posts.json'
    imgmap_path = DATA / 'imgmap.json'
    posts = json.load(open(posts_path, encoding='utf-8'))
    imgmap = json.load(open(imgmap_path, encoding='utf-8'))
    idx = next((i for i, p in enumerate(posts) if str(p.get('id')) == post_id), None)
    if idx is None:
        print('post not in posts.json:', post_id, file=sys.stderr)
        sys.exit(1)
    rec = posts[idx]
    if not site_dir:
        site_dir = u.unquote((rec.get('path') or '').strip('/'))

    wp = fetch_post(post_id)
    title = strip_tags(wp.get('title', {}).get('rendered', ''))
    excerpt = strip_tags(wp.get('excerpt', {}).get('rendered', ''))
    content = wp_clean_html(wp.get('content', {}).get('rendered', ''))
    # drop duplicate H1 (page hero already has h1)
    content = re.sub(r'^<h1>.*?</h1>\s*', '', content, count=1, flags=re.S | re.I)

    urls = content_img_urls(content)
    RAW = pathlib.Path(__import__('os').environ.get(
        'ABADIS_IMG_RAW',
        str(pathlib.Path(__file__).resolve().parent / '.img-raw'),
    ))
    RAW.mkdir(parents=True, exist_ok=True)
    for url in urls:
        ensure_img(url, imgmap)
        c = canon(url)
        if not (RAW / (imgmap.get(c, {}).get('file') or '')).exists():
            data, final, note = download_one(url)
            if data:
                name = raw_name_for(c)
                (RAW / name).write_bytes(data)
                imgmap[c] = {'ok': True, 'file': name, 'bytes': len(data), 'via': note}
                unsized = re.sub(r'-\d+x\d+(\.\w+)$', r'\1', c)
                if unsized != c:
                    imgmap[unsized] = dict(imgmap[c])
            else:
                print('WARN image fetch failed', url)

    json.dump(imgmap, open(imgmap_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    reload_imgmap()
    for url in urls:
        r = ensure_webp(url)
        print('  webp', url, '->', r['src'] if r else 'MISSING')

    rec['title'] = title
    rec['desc'] = excerpt
    rec['modified'] = iso_date({'date_gmt': wp.get('modified_gmt'), 'date': wp.get('modified')})
    rec['blocks'] = [{'t': 'html', 'html': content}]
    rec['snapshot'] = 'rest-' + datetime.now(timezone.utc).strftime('%Y%m%d')
    rec['mode'] = 'rest'
    posts[idx] = rec
    json.dump(posts, open(posts_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

    html_path = SITE / site_dir / 'index.html'
    if not html_path.exists():
        print('site page missing, posts.json updated only:', html_path)
        return
    p = '../'
    body = blocks_to_prose(rec['blocks'], p, skip_title=title)
    body = re.sub(r'<h1>.*?</h1>\s*', '', body, count=1, flags=re.S | re.I)
    # tables: wrap bare tables like existing page
    body = re.sub(r'<table(\s[^>]*)?>', r'<div class="table-scroll" tabindex="0"><table\1>', body)
    body = re.sub(r'</table>', r'</table></div>', body)

    page = html_path.read_text(encoding='utf-8')
    lead_m = re.search(
        r'(<article class="article prose post-v2">\s*)(<div class="lead-img">.*?</div>\s*)?',
        page,
        flags=re.S,
    )
    if not lead_m:
        print('could not find article block in', html_path, file=sys.stderr)
        sys.exit(1)
    lead = lead_m.group(2) or ''
    new_page, n = re.subn(
        r'<article class="article prose post-v2">\s*(?:<div class="lead-img">.*?</div>\s*)?.*?</article>',
        f'<article class="article prose post-v2">\n      {lead}{body}\n    </article>',
        page,
        count=1,
        flags=re.S,
    )
    if n != 1:
        print('article replace failed', html_path, file=sys.stderr)
        sys.exit(1)
    html_path.write_text(new_page, encoding='utf-8')
    print('Wrote', html_path)


if __name__ == '__main__':
    main()