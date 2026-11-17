#!/usr/bin/env python3
"""Refresh article bodies from WP REST when local in-body img count is below WordPress.

Preserves lead-img, FAQ (سوالات متداول), header/footer. Does not run full build.py.
"""
from __future__ import annotations

import hashlib, json, os, pathlib, re, sys, time, urllib.parse as u, urllib.request
from html import unescape

ROOT = pathlib.Path(__file__).resolve().parents[2]
DATA = pathlib.Path(__file__).resolve().parent / 'data'
SITE = ROOT / 'site'
sys.path.insert(0, str(DATA.parent))
import lib  # noqa: E402
from fetch_posts_rest import clean_content, ensure_img, content_img_urls  # noqa: E402

UA = 'Mozilla/5.0 (AbadisRedesign image sync; info@abadis-med.com)'
RAW = lib.RAW


def get_json(url: str):
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': 'application/json'})
    with urllib.request.urlopen(req, timeout=45) as r:
        return json.loads(r.read().decode('utf-8'))


def wp_img_count(html: str) -> int:
    return len(re.findall(r'<img\b', html or '', re.I))


def site_body_imgs(html: str) -> int:
    m = re.search(r'<article[^>]*class="[^"]*prose[^"]*"[^>]*>(.*)</article>', html, re.S | re.I)
    if not m:
        return -1
    body = m.group(1)
    body = re.sub(r'<div class="lead-img">.*?</div>', '', body, count=1, flags=re.S | re.I)
    return len(re.findall(r'<img\b', body, re.I))


def asset_prefix(page: pathlib.Path) -> str:
    page = page.resolve()
    rel = page.relative_to(SITE.resolve())
    depth = len(rel.parts) - 1
    return '../' * depth + 'assets/img/c/'


def normalize_img_tag(tag: str, prefix: str) -> str | None:
    src_m = re.search(r'\bsrc=["\']([^"\']+)["\']', tag, re.I)
    if not src_m:
        return None
    src = unescape(src_m.group(1))
    if '/wp-content/uploads/' not in src:
        return tag
    if src.startswith('/'):
        src = 'https://abadis-med.com' + src
    alt_m = re.search(r'\balt=["\']([^"\']*)["\']', tag, re.I)
    alt = alt_m.group(1) if alt_m else ''
    alt = alt.replace('"', '&quot;')
    w_m = re.search(r'\bwidth=["\'](\d+)["\']', tag, re.I)
    h_m = re.search(r'\bheight=["\'](\d+)["\']', tag, re.I)
    info = lib.best_img(src, 1000)
    if not info:
        info = lib.best_img(src, 1400)
    if not info:
        return None
    w = int(w_m.group(1)) if w_m else info['w']
    h = int(h_m.group(1)) if h_m else info['h']
    name = info['src'].split('/')[-1]
    return (
        f'<img src="{prefix}{name}" width="{w}" height="{h}" '
        f'loading="lazy" decoding="async" alt="{alt}">'
    )


def localize_content(html: str, prefix: str) -> str:
    html = re.sub(r'\s(?:srcset|sizes)=["\'][^"\']*["\']', '', html, flags=re.I)
    html = re.sub(r'\sclass=["\'][^"\']*wp-image[^"\']*["\']', '', html, flags=re.I)
    html = re.sub(r'[?&]utm_[^"\'>\s]+', '', html)
    html = re.sub(r'\sstyle=["\'][^"\']*["\']', '', html, flags=re.I)

    def repl(m):
        nt = normalize_img_tag(m.group(0), prefix)
        return nt if nt else m.group(0)

    html = re.sub(r'<img[^>]+>', repl, html, flags=re.I)
    # unwrap img-only h2/h3 (generator bug)
    html = re.sub(
        r'<h([23])[^>]*>\s*(<img[^>]+>)\s*</h\1>',
        r'<p>\2</p>',
        html,
        flags=re.I,
    )
    return html.strip()


def extract_faq_tail(body: str) -> str:
    m = re.search(r'(<h2[^>]*>\s*سوالات\s+متداول.*)', body, re.S | re.I)
    return m.group(1).strip() if m else ''


def patch_article(page: pathlib.Path, new_inner: str) -> bool:
    html = page.read_text(encoding='utf-8')
    m = re.search(
        r'(<article[^>]*class="[^"]*prose[^"]*"[^>]*>\s*<div class="lead-img">.*?</div>)(.*?)(</article>)',
        html,
        re.S | re.I,
    )
    if not m:
        return False
    faq = extract_faq_tail(m.group(2))
    inner = new_inner
    if faq and faq not in inner:
        inner = inner + '\n' + faq
    patched = html[: m.start(2)] + '\n' + inner + '\n    ' + html[m.end(2) :]
    page.write_text(patched, encoding='utf-8')
    return True


def sync_post(wp_id: str, page: pathlib.Path, imgmap: dict, posts: list) -> bool:
    try:
        post = get_json(f'http://abadis-med.com/wp-json/wp/v2/posts/{wp_id}?_fields=content,modified')
    except Exception as e:
        print('  skip fetch', wp_id, e)
        return False
    raw = post['content']['rendered']
    for url in content_img_urls(raw):
        ensure_img(url, imgmap)
        ensure_img(re.sub(r'-\d+x\d+(\.\w+)$', r'\1', url), imgmap)
    # reload lib imgmap cache
    lib.IMGMAP.update(imgmap)
    lib._IMG_BY_PATH.clear()
    for k, v in imgmap.items():
        if v.get('ok'):
            lib._IMG_BY_PATH[lib._key(k)] = v['file']

    body = clean_content(raw)
    prefix = asset_prefix(page)
    body = localize_content(body, prefix)

    if not patch_article(page, body):
        print('  patch failed', page)
        return False

    idx = next((i for i, p in enumerate(posts) if str(p.get('id')) == str(wp_id)), None)
    if idx is not None:
        posts[idx]['blocks'] = [{'t': 'html', 'html': body}]
        posts[idx]['snapshot'] = time.strftime('rest-%Y%m%d')
        if post.get('modified'):
            posts[idx]['modified'] = post['modified']
    return True


def main():
    from audit_inline_images import fa_posts, get_json as gj

    imgmap = json.load(open(DATA / 'imgmap.json', encoding='utf-8'))
    posts = json.load(open(DATA / 'posts.json', encoding='utf-8'))
    id_file = DATA / 'sync-img-targets.txt'
    if os.environ.get('SYNC_IMG_IDS'):
        want = {x.strip() for x in os.environ['SYNC_IMG_IDS'].split(',') if x.strip()}
        targets = [(wp_id, page, -1, -1) for lang, wp_id, rel, page in fa_posts() if wp_id in want]
    elif id_file.is_file():
        want = {ln.strip() for ln in id_file.read_text(encoding='utf-8').splitlines() if ln.strip()}
        targets = [(wp_id, page, -1, -1) for lang, wp_id, rel, page in fa_posts() if wp_id in want]
    else:
        targets = []
        for lang, wp_id, rel, page in fa_posts():
            html = page.read_text(encoding='utf-8')
            ours = site_body_imgs(html)
            try:
                wp_n = wp_img_count(gj(f'http://abadis-med.com/wp-json/wp/v2/posts/{wp_id}?_fields=content')['content']['rendered'])
            except Exception:
                continue
            if ours >= 0 and wp_n > ours:
                targets.append((wp_id, page, ours, wp_n))

    print(f'Syncing {len(targets)} FA posts (missing images)...', flush=True)
    ok = 0
    for wp_id, page, ours, wp_n in targets:
        print(f'  {wp_id} ours={ours} wp={wp_n} {page.parent.name[:40]}')
        if sync_post(wp_id, page, imgmap, posts):
            ok += 1
        lib._done.clear()
        time.sleep(0.05)

    json.dump(imgmap, open(DATA / 'imgmap.json', 'w'), ensure_ascii=False, indent=2)
    json.dump(posts, open(DATA / 'posts.json', 'w'), ensure_ascii=False, indent=2)
    print(f'Done: {ok}/{len(targets)}')
    # Also build any new webps from RAW
    for k, v in list(imgmap.items()):
        if v.get('ok') and v.get('file'):
            lib.best_img(k, 1000)
            lib.best_img(k, 1400)


if __name__ == '__main__':
    main()