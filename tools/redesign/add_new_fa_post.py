#!/usr/bin/env python3
"""Add a WordPress FA post that is newer than posts.json, without a full build.py run.

Usage: python3 tools/redesign/add_new_fa_post.py POST_ID TEMPLATE_POST_ID

* inserts the post into data/posts.json (title/desc/date/image), right before TEMPLATE_POST_ID,
* writes site/<slug>/index.html by cloning the page of TEMPLATE_POST_ID (same category, same depth)
  and swapping title, meta, JSON-LD, hero, dates, lead image, share links and nav,
* adds a "newer" link on the template page,
* then fills the body + inline images with refresh_one_fa_post.py.
"""
from __future__ import annotations
import json, os, pathlib, re, subprocess, sys, urllib.parse as u, urllib.request
from urllib.parse import quote

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
ROOT = HERE.parents[1]; SITE = ROOT / 'site'; DATA = HERE / 'data'
from fetch_posts_rest import strip_tags, iso_date, ensure_img
from fetch_images import download_one, canon, raw_name_for
import refresh_one_fa_post as R
from lib import esc, jdate, fa
import lib

UA = R.UA


def get(url):
    err = None
    for base in ('https://www.abadis-med.com', 'http://abadis-med.com'):
        for _ in range(3):
            try:
                req = urllib.request.Request(base + url, headers={'User-Agent': UA, 'Accept': 'application/json'})
                with urllib.request.urlopen(req, timeout=60) as r:
                    return json.loads(r.read().decode('utf-8'))
            except Exception as e:  # noqa: BLE001
                err = e
    raise err


def fetch_image(url, imgmap):
    RAW = pathlib.Path(os.environ.get('ABADIS_IMG_RAW', str(HERE / '.img-raw')))
    RAW.mkdir(parents=True, exist_ok=True)
    ensure_img(url, imgmap)
    c = canon(url)
    if not (RAW / (imgmap.get(c, {}).get('file') or '')).exists():
        data, final, note = download_one(url)
        if data:
            name = raw_name_for(c)
            (RAW / name).write_bytes(data)
            imgmap[c] = {'ok': True, 'file': name, 'bytes': len(data), 'via': note}


def main():
    pid, tpl_id = sys.argv[1], sys.argv[2]
    posts = json.load(open(DATA / 'posts.json', encoding='utf-8'))
    imgmap = json.load(open(DATA / 'imgmap.json', encoding='utf-8'))
    if any(str(p.get('id')) == pid for p in posts):
        print('already in posts.json'); return
    tpl = next(p for p in posts if str(p.get('id')) == tpl_id)
    wp = get(f'/wp-json/wp/v2/posts/{pid}?_fields=id,slug,link,title,excerpt,content,date,date_gmt,modified,modified_gmt,featured_media')
    image = ''
    if wp.get('featured_media'):
        image = get(f'/wp-json/wp/v2/media/{wp["featured_media"]}?_fields=source_url').get('source_url', '')
    link = u.unquote(wp['link']).rstrip('/')
    slug = link.rsplit('/', 1)[-1]
    rec = {'url': link, 'path': f'/{slug}/', 'id': pid, 'snapshot': 'rest', 'title': strip_tags(wp['title']['rendered']),
           'desc': strip_tags(wp['excerpt']['rendered']), 'image': image,
           'date': iso_date({'date_gmt': wp.get('date_gmt'), 'date': wp.get('date')}),
           'modified': iso_date({'date_gmt': wp.get('modified_gmt'), 'date': wp.get('modified')}),
           'author': '', 'mode': 'rest', 'blocks': []}
    if image:
        fetch_image(image, imgmap)
        json.dump(imgmap, open(DATA / 'imgmap.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
        R.reload_imgmap()
    lead = R.ensure_webp(image, 1200) if image else None
    print('lead', lead, 'card', lib.best_img(image, 640) if image else None)
    idx = next(i for i, p in enumerate(posts) if str(p.get('id')) == tpl_id)
    posts.insert(idx, rec)
    json.dump(posts, open(DATA / 'posts.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

    tslug = tpl['path'].strip('/')
    page = (SITE / tslug / 'index.html').read_text(encoding='utf-8')
    t_old, t_new = tpl['title'], rec['title']
    d_old = re.search(r'<meta name="description" content="([^"]*)"', page).group(1)
    words = len(strip_tags(R.wp_clean_html(wp['content']['rendered'])).split())
    mins = max(1, round(words / 200))
    d = rec['desc']
    new_desc = esc(d[:200] + ('…' if len(d) > 200 else ''))
    p = page
    p = p.replace(quote(t_old), quote(t_new))
    p = p.replace(f'https://abadis-med.com/{tslug}/', f'https://abadis-med.com/{slug}/')
    p = p.replace(d_old, new_desc)
    p = p.replace(esc(t_old), esc(t_new)).replace(t_old, t_new)
    p = p.replace(jdate(tpl['date']), jdate(rec['date']))
    p = re.sub(r'"datePublished": "[^"]*"', f'"datePublished": "{rec["date"][:10]}"', p)
    p = re.sub(r'زمان مطالعه: [^<]*دقیقه', f'زمان مطالعه: {fa(mins)} دقیقه', p)
    lead_html = ''
    if lead:
        p = re.sub(r'(<meta property="og:image" content=")[^"]*', lambda m: m.group(1) + '../' + lead['src'], p)
        p = re.sub(r'("image": "https://abadis-med.com/)[^"]*', lambda m: m.group(1) + lead['src'], p)
        lead_html = f'<div class="lead-img"><img src="../{lead["src"]}" width="{lead["w"]}" height="{lead["h"]}" alt="{esc(t_new)}" decoding="async"></div>'
    p = re.sub(r'<article class="article prose post-v2">.*?</article>',
               lambda m: f'<article class="article prose post-v2">\n      {lead_html}\n    </article>', p, count=1, flags=re.S)
    nav = f'<nav class="post-nav" aria-label="مطالب دیگر"><span></span><a href="../{tslug}/"><span>مطلب قدیمی‌تر</span>{esc(t_old)}</a></nav>'
    p = re.sub(r'<nav class="post-nav".*?</nav>', lambda m: nav, p, count=1, flags=re.S)
    out = SITE / slug / 'index.html'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(p, encoding='utf-8')
    tp = re.sub(r'(<nav class="post-nav" aria-label="مطالب دیگر">)<span></span>',
                lambda m: m.group(1) + f'<a href="../{slug}/"><span>مطلب جدیدتر</span>{esc(t_new)}</a>', page, count=1)
    (SITE / tslug / 'index.html').write_text(tp, encoding='utf-8')
    subprocess.run([sys.executable, str(HERE / 'refresh_one_fa_post.py'), pid, slug], check=True)
    print('wrote', out)


if __name__ == '__main__':
    main()
