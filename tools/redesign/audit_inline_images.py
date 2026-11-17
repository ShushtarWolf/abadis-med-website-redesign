#!/usr/bin/env python3
"""Compare in-body <img> counts (article prose, excluding lead-img) vs WP REST content."""
from __future__ import annotations

import json, pathlib, re, sys, time, urllib.parse as u, urllib.request
from html import unescape

ROOT = pathlib.Path(__file__).resolve().parents[2]
DATA = pathlib.Path(__file__).resolve().parent / 'data'
SITE = ROOT / 'site'
UA = 'Mozilla/5.0 (AbadisRedesign image audit; info@abadis-med.com)'


def get_json(url: str, timeout=45):
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': 'application/json'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode('utf-8'))


def wp_img_count(html: str) -> int:
    if not html:
        return 0
    return len(re.findall(r'<img\b', html, re.I))


def site_body_imgs(html: str) -> int:
    m = re.search(r'<article[^>]*class="[^"]*prose[^"]*"[^>]*>(.*)</article>', html, re.S | re.I)
    if not m:
        return -1
    body = m.group(1)
    body = re.sub(r'<div class="lead-img">.*?</div>', '', body, count=1, flags=re.S | re.I)
    return len(re.findall(r'<img\b', body, re.I))


def fa_posts():
    posts = json.load(open(DATA / 'posts.json', encoding='utf-8'))
    out = []
    for p in posts:
        pid = str(p.get('id', ''))
        path = (p.get('path') or '').strip('/')
        if not pid or not path:
            continue
        page = SITE / path / 'index.html'
        if not page.is_file():
            continue
        out.append(('fa', pid, str(page.relative_to(ROOT)), page))
    return out


EN_TO_FA = {11013: 19716, 11008: 19701, 11003: 19696, 10998: 19689, 10782: 18814, 10773: 18824, 10798: 18793,
           10769: 18772, 10765: 18768, 10761: 18761, 10758: 18758, 10693: 18681, 10688: 18609, 10684: 18597,
           10703: 18699, 10669: 18529, 10620: 18409, 10611: 18410, 10468: 18140, 10465: 17760, 10447: 18112,
           10452: 18088, 10492: 17992, 10305: 17949, 10298: 17936, 10290: 17929, 10149: 17781, 10162: 17796,
           10495: 17588, 10443: 18195, 10438: 17605, 10498: 17431, 10506: 17305, 10033: 16714, 9990: 16437,
           9950: 16208, 10531: 15884, 9842: 15884, 9967: 15833, 10017: 16445, 10012: 16744, 9830: 15088,
           9795: 15495, 9997: 15300, 9393: 15123, 9206: 15027, 9126: 14956, 9122: 14923, 10026: 15774,
           10021: 15757, 9981: 13840, 9529: 11467, 7138: 10187, 7071: 10719, 6919: 9354, 5948: 6708,
           4405: 3704, 4385: 3524, 1128: 14895, 9977: 16162}


def en_posts():
    fa_by_en = {v: k for k, v in EN_TO_FA.items()}
    out = []
    for page in (SITE / 'en').rglob('index.html'):
        if page.parent.name in ('blog', 'news', 'articles', 'en'):
            continue
        rel = str(page.relative_to(ROOT))
        html = page.read_text(encoding='utf-8', errors='replace')
        if 'post-v2' not in html and 'application/ld+json' not in html:
            continue
        # EN post id from en_posts if slug match is hard — use permalink in canonical
        canon = re.search(r'<link rel="canonical" href="[^"]+/en/([^/]+)/"', html)
        slug = canon.group(1) if canon else page.parent.name
        en_id = None
        try:
            eps = json.load(open(DATA / 'en_posts.json', encoding='utf-8'))
            for e in eps:
                link = (e.get('link') or '')
                if slug in link or slug.replace('-', '') in link.replace('-', ''):
                    en_id = e.get('id')
                    break
                sl = e.get('slug') or ''
                if sl == slug:
                    en_id = e.get('id')
                    break
        except Exception:
            pass
        if en_id is None:
            continue
        fa_id = fa_by_en.get(int(en_id), int(en_id) if str(en_id).isdigit() else None)
        out.append(('en', str(en_id), rel, page, fa_id))
    return out


def main():
    rows = []
    cache = {}
    for lang, wp_id, rel, page, *extra in fa_posts() + en_posts():
        html = page.read_text(encoding='utf-8', errors='replace')
        ours = site_body_imgs(html)
        if wp_id in cache:
            wp_n = cache[wp_id]
        else:
            base = 'http://abadis-med.com/wp-json/wp/v2/posts'
            if lang == 'en':
                base = 'https://www.abadis-med.com/en/wp-json/wp/v2/posts'
            try:
                post = get_json(f'{base}/{wp_id}')
                wp_n = wp_img_count(post.get('content', {}).get('rendered', ''))
                cache[wp_id] = wp_n
            except Exception as e:
                wp_n = -1
                cache[wp_id] = wp_n
            time.sleep(0.15)
        flag = '' if ours == wp_n else 'MISMATCH'
        if flag or '--all' in sys.argv:
            rows.append((flag, lang, wp_id, ours, wp_n, rel))

    rows.sort(key=lambda r: (0 if r[0] else 1, r[1], r[2]))
    print(f'{"flag":8} {"lang":4} {"wp_id":8} {"ours":5} {"wp":5}  path')
    for row in rows:
        print(f'{row[0]:8} {row[1]:4} {row[2]:8} {row[3]:5} {row[4]:5}  {row[5]}')
    mism = [r for r in rows if r[0] == 'MISMATCH']
    print(f'\nTotal checked: {len(rows)}, mismatches: {len(mism)}', file=sys.stderr)


if __name__ == '__main__':
    main()