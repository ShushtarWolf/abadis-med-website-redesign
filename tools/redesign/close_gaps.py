"""Close the November 2026 content gaps against live https://abadis-med.com.

    python3 tools/redesign/close_gaps.py

Fills three missing Farsi articles, the partial articles, sources/FAQ blocks,
Aparat embeds, two catalogues, EN/AR career forms, and the English archive
pages that are still absent. Does not delete existing copy.
"""
import hashlib
import html
import io
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from bs4 import BeautifulSoup
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import SITE, DATA, esc, jdate, fa, best_img, _key  # noqa: E402

UA = 'Mozilla/5.0 AbadisRedesign/1.0'
CACHE = Path('/tmp/gap-live')
CACHE.mkdir(parents=True, exist_ok=True)
OUT_IMG = SITE / 'assets' / 'img' / 'c'
REPORT = {}

NEW = [
    '/ست-سرم-چیست؟-راهنمای-جامع-انواع،-اجزا،/',
    '/میکروست-چیست؟-کاربرد،-اجزا-و-تفاوت-با-م/',
    '/هوش-تجاری-bi؛-تحول-هوشمند-صنعت-تجهیزات-پ/',
]
EN_TWIN = {
    '/ست-سرم-چیست؟-راهنمای-جامع-انواع،-اجزا،/':
        '/en/what-is-an-iv-infusion-set-a-comprehensive-guide-to-types-components-applications-and-safety-standards/',
    '/میکروست-چیست؟-کاربرد،-اجزا-و-تفاوت-با-م/':
        '/en/what-is-a-microdrip-set-uses-components-differences-from-macrodrip-sets/',
    '/هوش-تجاری-bi؛-تحول-هوشمند-صنعت-تجهیزات-پ/':
        '/en/business-intelligence-bi-transforming-the-medical-device-industry/',
}
PARTIAL = [
    '/تجهیزات-و-محصولات-بیمارستانی/',
    '/زباله-های-پلاستیکی/',
    '/پاتوژن/',
    '/استفاده-مخزن-های-ساکشن-دائم/',
    '/کرونا،سرماخوردگی،آنفلونزا/',
    '/introducing-medical-engineering-sites/',
]
SOURCES = [
    '/مخزن-ساکشن-چیست؟/',
    '/فیلتر-های-متخلخل-در-صنعت-پزشکی/',
    '/ارزیابی-مقایسهای-مدیریت-مصرف-آنتی-بی/',
    '/ارزيابي-و-تحليل-مواجهات-شغلی-کادر-درما/',
    '/تبعیت-از-دستورالعمل-های-پیشگیری-کننده/',
    '/بررسی-علل-ایجاد-پریتونیت-در-بخش-دیالیز/',
    '/الگوی-مقاومت-آنتی-بیوتیکی-باکتریهای/',
    '/strategicity-and-necessity-of-using-disposable-suction-bags-part-ii/',
    '/ارتقا-فرايند-بیولوژيک-تصفیه-خانه-فاضل/',
]
VIDEOS = [ln.strip() for ln in open(
    os.environ.get('ABADIS_VIDEO_LIST', '/tmp/gap-audit/gap-audit/news-missing-videos.txt'),
    encoding='utf-8') if ln.strip()]

SKIP_H = {
    'پیشنهادهایی برای شما', 'نیاز به مشاوره دارید...', 'فهرست مطالب',
    'مطالب مرتبط', 'نظرات', 'پاسخ دهید',
}

NEW_BYTES = {'img': 0, 'pdf': 0}


def norm(s):
    s = html.unescape(s or '')
    s = s.replace('\u200c', '').replace('\u200b', '').replace('ي', 'ی').replace('ك', 'ک').replace('ة', 'ه')
    s = s.translate(str.maketrans('۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩', '01234567890123456789'))
    return re.sub(r'\s+', ' ', s).strip().lower()


def fetch(url):
    key = hashlib.sha1(url.encode()).hexdigest()
    fp = CACHE / (key + '.html')
    if fp.is_file() and fp.stat().st_size > 1000:
        return fp.read_bytes()
    parts = urllib.parse.urlsplit(url)
    path = urllib.parse.quote(urllib.parse.unquote(parts.path), safe='/%')
    url2 = urllib.parse.urlunsplit((parts.scheme, parts.netloc, path, parts.query, ''))
    req = urllib.request.Request(url2, headers={'User-Agent': UA})
    data = urllib.request.urlopen(req, timeout=70).read()
    fp.write_bytes(data)
    return data


def live_url(path):
    host = 'http://www.abadis-med.com' if path.startswith('/en/') else 'http://abadis-med.com'
    return host + path


def soup_of(path):
    return BeautifulSoup(fetch(live_url(path)), 'html.parser')


def content_node(soup):
    w = soup.select_one('[data-widget_type="theme-post-content.default"] .elementor-widget-container')
    return w


def prefix_for(site_path):
    depth = len([p for p in site_path.strip('/').split('/') if p])
    return '../' * depth if depth else './'


def rel_link(from_path, to_path):
    frag = ''
    if '#' in to_path:
        to_path, frag = to_path.split('#', 1)
        frag = '#' + frag
    if not to_path.endswith('/'):
        to_path += '/'
    src = from_path.strip('/')
    dst = to_path.strip('/')
    rel = dst if not src else os.path.relpath(dst or '.', src)
    if rel in ('.', ''):
        rel = './'
    elif to_path.endswith('/'):
        rel += '/'
    return rel + frag


def build_index():
    real, stubs = {}, {}
    for dp, dns, fns in os.walk(SITE):
        if 'index.html' not in fns:
            continue
        rel = os.path.relpath(dp, SITE)
        path = '/' if rel == '.' else '/' + rel.replace(os.sep, '/') + '/'
        fp = Path(dp) / 'index.html'
        head = fp.read_text(encoding='utf-8', errors='ignore')[:1800]
        if 'abadis-moved' in head or 'http-equiv="refresh"' in head:
            stubs[path] = head
        else:
            real[path] = fp
    by_norm = {}
    for p in real:
        by_norm.setdefault(norm(p), p)
    return real, stubs, by_norm


REAL, STUBS, BY_NORM = build_index()


def resolve_path(path):
    if not path:
        return None
    if not path.endswith('/'):
        path += '/'
    if path in REAL:
        return path
    hit = BY_NORM.get(norm(path))
    if hit:
        return hit
    aliases = json.load(open(DATA / 'url_aliases.json', encoding='utf-8'))
    for key in (path, path.rstrip('/')):
        row = aliases.get(key) or aliases.get(key + '/')
        if isinstance(row, dict) and row.get('to'):
            return resolve_path(row['to'])
    return None


def map_href(href, from_path):
    if not href or href.startswith(('mailto:', 'tel:', 'javascript:')):
        return None
    if href.startswith('#'):
        return href, False
    absu = urllib.parse.urljoin('https://abadis-med.com' + from_path, href)
    parts = urllib.parse.urlsplit(absu)
    host = parts.netloc.lower().replace('www.', '')
    if host and host != 'abadis-med.com':
        return absu, True
    path = urllib.parse.unquote(parts.path or '/')
    if path.startswith('/wp-content/'):
        local = SITE / path.lstrip('/')
        if local.is_file():
            return rel_link(from_path, '/' + path.lstrip('/')), False
        return absu, True
    if '.' in path.rsplit('/', 1)[-1] and not path.endswith('/'):
        local = SITE / path.lstrip('/')
        if local.is_file():
            return rel_link(from_path, '/' + path.lstrip('/')), False
        return (absu, True) if host else (href, False)
    dest = resolve_path(path)
    if not dest:
        return None
    out = rel_link(from_path, dest)
    if parts.fragment:
        out += '#' + parts.fragment
    return out, False


def ensure_image(url, maxw=1000):
    if not url or url.startswith('data:'):
        return None
    if 'favicon' in url or 'google.com/s2/' in url:
        return None
    if url.startswith('//'):
        url = 'https:' + url
    parts = urllib.parse.urlsplit(url)
    url = urllib.parse.urlunsplit((
        parts.scheme, parts.netloc,
        urllib.parse.quote(urllib.parse.unquote(parts.path), safe='/%'),
        parts.query, ''))
    got = best_img(url, maxw)
    if got:
        return got
    key = _key(url)
    name = hashlib.sha1(key.encode()).hexdigest()[:12] + f'-{maxw}.webp'
    dest = OUT_IMG / name
    if dest.is_file():
        return best_img(url, maxw)
    raw_url = url
    if raw_url.startswith('https://'):
        raw_url = 'http://' + raw_url[len('https://'):]
    try:
        req = urllib.request.Request(raw_url, headers={'User-Agent': UA})
        with urllib.request.urlopen(req, timeout=50) as r:
            data = r.read(8_000_000)
            if r.read(1):
                return None
    except Exception as e:
        print('  img fail', url[:80], e)
        return None
    try:
        im = Image.open(io.BytesIO(data))
        im.seek(0)
        if im.width < 48 or im.height < 48:
            return None
        im = im.convert('RGB')
        if im.width > maxw:
            nh = round(im.height * maxw / im.width)
            im = im.resize((maxw, nh), Image.LANCZOS)
        dest.parent.mkdir(parents=True, exist_ok=True)
        im.save(dest, 'WEBP', quality=72, method=6)
        NEW_BYTES['img'] += dest.stat().st_size
    except Exception as e:
        print('  img decode', url[:80], e)
        return None
    return best_img(url, maxw)


def inline_html(node, from_path):
    parts = []
    for child in getattr(node, 'children', []) or []:
        if getattr(child, 'name', None) is None:
            parts.append(esc(str(child)))
            continue
        name = child.name.lower()
        if name in ('script', 'style', 'noscript'):
            continue
        if name == 'br':
            parts.append('<br>')
            continue
        if name in ('strong', 'b', 'em', 'i', 'sub', 'sup', 'u'):
            inner = inline_html(child, from_path)
            if inner.strip():
                parts.append(f'<{name}>{inner}</{name}>')
            continue
        if name == 'a':
            inner = inline_html(child, from_path).strip() or esc(child.get_text(' ', strip=True))
            mapped = map_href(child.get('href') or '', from_path)
            if not inner:
                continue
            if not mapped:
                parts.append(inner)
                continue
            href, ext = mapped
            extra = ' target="_blank" rel="noopener"' if ext else ''
            parts.append(f'<a href="{esc(href)}"{extra}>{inner}</a>')
            continue
        if name == 'img':
            parts.append(img_tag(child, from_path) or '')
            continue
        parts.append(inline_html(child, from_path))
    return ''.join(parts)


def img_url_of(tag):
    for attr in ('data-src', 'data-lazy-src', 'data-orig-file', 'src'):
        v = tag.get(attr) or ''
        if v and not v.startswith('data:') and 'placeholder' not in v:
            return v
    return ''


def img_tag(tag, from_path, cls=''):
    url = img_url_of(tag)
    info = ensure_image(url, 1000)
    if not info:
        return ''
    alt = tag.get('alt') or ''
    c = f' class="{cls}"' if cls else ''
    return (f'<img{c} src="{prefix_for(from_path)}{info["src"]}" width="{info["w"]}" height="{info["h"]}" '
            f'alt="{esc(alt)}" loading="lazy" decoding="async">')


def table_html(tag, from_path):
    rows = []
    for tr in tag.find_all('tr'):
        cells = []
        for cell in tr.find_all(['th', 'td']):
            cells.append((cell.name, inline_html(cell, from_path).strip()))
        if cells:
            rows.append(cells)
    if not rows:
        return ''
    head = rows[0] if all(c[0] == 'th' for c in rows[0]) else None
    body = rows[1:] if head else rows
    out = ['<div class="table-wrap"><table>']
    if head:
        out.append('<thead><tr>' + ''.join(f'<th>{c[1]}</th>' for c in head) + '</tr></thead>')
    out.append('<tbody>')
    for row in body:
        out.append('<tr>' + ''.join(f'<td>{c[1]}</td>' for c in row) + '</tr>')
    out.append('</tbody></table></div>')
    return ''.join(out)


def aparat_html(src, title='ویدیو'):
    src = src or ''
    if src.startswith('//'):
        src = 'https:' + src
    m = re.search(r'videohash/([^/]+)', src)
    if m:
        src = f'https://www.aparat.com/video/video/embed/videohash/{m.group(1)}/vt/frame'
    return (f'<div class="video-frame"><iframe src="{esc(src)}" title="{esc(title or "ویدیو")}" '
            f'loading="lazy" allowfullscreen referrerpolicy="no-referrer-when-downgrade"></iframe></div>')


def blocks_from(container, from_path):
    """Top-level content blocks as HTML, skipping chrome headings."""
    if not container:
        return []
    out = []
    last_text = ''
    for el in container.find_all(recursive=False):
        name = (el.name or '').lower()
        if name in ('script', 'style', 'form'):
            continue
        if name == 'iframe':
            out.append(('video', last_text, aparat_html(el.get('src') or '', el.get('title') or 'ویدیو')))
            continue
        if name in ('h1',):
            continue
        if name in ('h2', 'h3', 'h4'):
            text = el.get_text(' ', strip=True)
            if norm(text) in {norm(x) for x in SKIP_H}:
                continue
            inner = inline_html(el, from_path).strip() or esc(text)
            out.append((name, text, f'<{name}>{inner}</{name}>'))
            last_text = text or last_text
            continue
        if name == 'p':
            if el.find('iframe'):
                prev = el.get_text(' ', strip=True)
                for fr in el.find_all('iframe'):
                    out.append(('video', prev, aparat_html(fr.get('src') or '', fr.get('title') or 'ویدیو')))
                rest = inline_html(el, from_path).strip()
                if norm(rest):
                    out.append(('p', rest, f'<p>{rest}</p>'))
                continue
            inner = inline_html(el, from_path).strip()
            if norm(BeautifulSoup(inner, 'html.parser').get_text(' ', strip=True)):
                out.append(('p', inner, f'<p>{inner}</p>'))
                last_text = el.get_text(' ', strip=True) or last_text
            continue
        if name in ('ul', 'ol'):
            items = []
            for li in el.find_all('li', recursive=False):
                inner = inline_html(li, from_path).strip()
                if inner:
                    items.append(f'<li>{inner}</li>')
            if items:
                out.append((name, el.get_text(' ', strip=True), f'<{name}>' + ''.join(items) + f'</{name}>'))
            continue
        if name == 'table':
            html_t = table_html(el, from_path)
            if html_t:
                out.append(('table', el.get_text(' ', strip=True), html_t))
            continue
        if name == 'img':
            tag = img_tag(el, from_path)
            if tag:
                out.append(('img', el.get('alt') or '', f'<figure>{tag}</figure>'))
            continue
        if name in ('figure', 'div', 'section', 'blockquote', 'header', 'pre', 'article', 'main', 'center', 'span'):
            inner_blocks = blocks_from(el, from_path)
            if inner_blocks:
                out.extend(inner_blocks)
            got = ''.join(b[2] for b in inner_blocks)
            for fr in el.find_all('iframe'):
                src = fr.get('src') or ''
                token = (re.search(r'videohash/([^/]+)', src) or re.search(r'/v/([^/?]+)', src))
                token = token.group(1) if token else src
                if token and token not in got:
                    out.append(('video', last_text, aparat_html(src, fr.get('title') or 'ویدیو')))
                    got += token
            if not inner_blocks:
                for im in el.find_all('img'):
                    tag = img_tag(im, from_path)
                    if tag:
                        out.append(('img', im.get('alt') or '', f'<figure>{tag}</figure>'))
    return out


def faq_html(soup):
    w = soup.select_one('[data-widget_type="dce-acf-repeater-v2.default"]')
    if not w:
        # elementor accordion that is not the site chrome
        return ''
    items = []
    for item in w.select('.elementor-accordion-item'):
        q = item.select_one('.elementor-accordion-title')
        a = item.select_one('.elementor-tab-content')
        if not q or not a:
            continue
        qt = q.get_text(' ', strip=True)
        at = a.get_text(' ', strip=True)
        if not qt or not at:
            continue
        items.append((qt, at))
    if not items:
        return ''
    bits = ['<h2>سوالات متداول</h2><div class="faq">']
    for q, a in items:
        bits.append(f'<details class="faq-item"><summary>{esc(q)}</summary><div class="faq-a"><p>{esc(a)}</p></div></details>')
    bits.append('</div>')
    return ''.join(bits), items


def page_plain(html_text):
    body = re.sub(r'<script[\s\S]*?</script>', ' ', html_text, flags=re.I)
    body = re.sub(r'<style[\s\S]*?</style>', ' ', body, flags=re.I)
    return norm(re.sub(r'<[^>]+>', ' ', body))


def present(text, plain):
    n = norm(BeautifulSoup(text, 'html.parser').get_text(' ', strip=True) if '<' in text else text)
    if len(n) < 24:
        return n in plain
    return n[:80] in plain


def local_file(site_path):
    rel = site_path.strip('/')
    fp = SITE / rel / 'index.html'
    if fp.is_file():
        return fp
    # yeh/kaf variants
    want = norm('/' + rel + '/')
    for p, f in REAL.items():
        if norm(p) == want:
            return f
    # directory listing fallback
    parent = SITE
    if not parent.is_dir():
        return None
    target = norm(rel)
    for child in parent.iterdir():
        if child.is_dir() and norm(child.name) == target and (child / 'index.html').is_file():
            return child / 'index.html'
    return fp if fp.is_file() else None


def insert_before_article_end(html_text, snippet):
    m = re.search(r'</article>', html_text)
    if not m:
        return html_text
    return html_text[:m.start()] + '\n' + snippet + '\n' + html_text[m.start():]


def insert_after_heading(html_text, heading, snippet):
    idx = html_text.find(heading)
    if idx < 0:
        return insert_before_article_end(html_text, f'<h2>{esc(heading)}</h2>\n' + snippet)
    nxt = html_text.find('<h2', idx + len(heading))
    art = html_text.find('</article>', idx)
    at = nxt if nxt != -1 else art
    if at < 0:
        return html_text
    return html_text[:at] + snippet + '\n' + html_text[at:]


def fill_page(site_path, soup, videos_only=False):
    fp = local_file(site_path)
    if not fp or not fp.is_file():
        print('  missing local', site_path)
        return {'path': site_path, 'ok': False, 'why': 'no local page'}
    html_text = fp.read_text(encoding='utf-8')
    if 'abadis-moved' in html_text[:2000]:
        return {'path': site_path, 'ok': False, 'why': 'stub'}
    container = content_node(soup)
    blocks = blocks_from(container, site_path)
    added = []
    if videos_only:
        # insert each aparat iframe after the preceding live text
        cursor = 0
        count = 0
        for kind, anchor, block in blocks:
            if kind != 'video':
                continue
            hash_m = re.search(r'videohash/([^/" ]+)', block)
            token = hash_m.group(1) if hash_m else ''
            if token and f'videohash/{token}' in html_text:
                continue
            placed = False
            needle = norm(anchor)
            slice_ = needle[-48:] if len(needle) > 48 else needle
            art_at = html_text.find('<article')
            if len(slice_) >= 18:
                # search only inside the article so a crumb does not catch the embed
                raw = re.sub(r'\s+', ' ', anchor).strip()
                for n in (48, 32, 20):
                    if len(raw) < n:
                        continue
                    bit = raw[-n:]
                    pos = html_text.find(bit, max(cursor, art_at))
                    if pos < 0:
                        pos = html_text.find(bit, art_at if art_at >= 0 else 0)
                    if pos >= 0:
                        end = html_text.find('</p>', pos)
                        if end < 0:
                            end = html_text.find('</h', pos)
                        if end < 0:
                            end = pos + len(bit)
                        else:
                            end = html_text.find('>', end) + 1
                        html_text = html_text[:end] + '\n' + block + '\n' + html_text[end:]
                        cursor = end + len(block)
                        placed = True
                        break
            if not placed:
                html_text = insert_before_article_end(html_text, block)
            count += 1
            added.append(token or 'video')
        fp.write_text(html_text, encoding='utf-8')
        ensure_self_hreflang(fp, site_path)
        return {'path': site_path, 'ok': True, 'videos': count}

    plain = page_plain(html_text)
    # group into sections by h2
    sections = []
    cur = {'h': None, 'hhtml': '', 'blocks': []}
    for kind, text, block in blocks:
        if kind == 'h2':
            if cur['h'] or cur['blocks']:
                sections.append(cur)
            cur = {'h': text, 'hhtml': block, 'blocks': []}
        else:
            cur['blocks'].append((kind, text, block))
    if cur['h'] or cur['blocks']:
        sections.append(cur)
    appended = 0
    for sec in sections:
        heading = sec['h']
        fresh = []
        for kind, text, block in sec['blocks']:
            if kind == 'video':
                token = re.search(r'videohash/([^/" ]+)', block)
                if token and token.group(1) in html_text:
                    continue
                fresh.append(block)
                continue
            probe = text if kind != 'img' else ''
            if probe and present(probe, plain):
                continue
            if kind == 'img':
                src = re.search(r'src="([^"]+)"', block)
                if src and src.group(1) in html_text:
                    continue
            fresh.append(block)
        if not fresh and (not heading or present(heading, plain)):
            continue
        # heading already on the page: only add the missing blocks under it
        if heading and present(heading, plain):
            if not fresh:
                continue
            html_text = insert_after_heading(html_text, heading, '\n'.join(fresh))
        else:
            chunk = []
            if heading and sec['hhtml']:
                chunk.append(sec['hhtml'])
            chunk.extend(fresh)
            if not chunk:
                continue
            html_text = insert_before_article_end(html_text, '\n'.join(chunk))
        appended += len(fresh) + (1 if heading and not present(heading, plain) else 0)
        plain = page_plain(html_text)
        added.append(heading or 'intro')
    faq = faq_html(soup)
    if faq:
        html_faq, items = faq
        missing_q = [q for q, a in items if norm(q) not in plain]
        if missing_q:
            if 'سوالات متداول' in html_text and norm('سوالات متداول') in plain:
                only = ''.join(
                    f'<details class="faq-item"><summary>{esc(q)}</summary><div class="faq-a"><p>{esc(a)}</p></div></details>'
                    for q, a in items if norm(q) not in plain)
                html_text = insert_before_article_end(html_text, f'<div class="faq">{only}</div>')
            else:
                html_text = insert_before_article_end(html_text, html_faq)
            appended += len(missing_q)
            added.append('faq')
    fp.write_text(html_text, encoding='utf-8')
    ensure_self_hreflang(fp, site_path)
    return {'path': site_path, 'ok': True, 'added': appended, 'heads': added[:12]}


def ensure_self_hreflang(fp, site_path, extras=None):
    text = fp.read_text(encoding='utf-8')
    if 'rel="alternate" hreflang=' in text:
        fp.write_text(text, encoding='utf-8')
        return
    origin = 'https://abadis-med.com'
    self_url = origin + site_path
    lang = 'en' if site_path.startswith('/en/') else ('ar' if site_path.startswith('/arabic/') else 'fa-IR')
    lines = [f'<link rel="alternate" hreflang="{lang}" href="{self_url}">']
    xd = self_url
    for code, path in extras or []:
        lines.append(f'<link rel="alternate" hreflang="{code}" href="{origin}{path}">')
        if code == 'fa-IR':
            xd = origin + path
    if lang == 'fa-IR':
        xd = self_url
    lines.append(f'<link rel="alternate" hreflang="x-default" href="{xd}">')
    block = '\n'.join(lines)
    text2, n = re.subn(r'(<link rel="canonical" href="[^"]*">)', r'\1\n' + block, text, count=1)
    if n:
        fp.write_text(text2, encoding='utf-8')


def meta_desc(soup):
    tag = soup.find('meta', attrs={'name': 'description'})
    if tag and tag.get('content'):
        return re.sub(r'\s+', ' ', tag['content']).strip()
    return ''


def h1_of(soup):
    h = soup.find('h1')
    return h.get_text(' ', strip=True) if h else ''


def build_new_articles():
    template = (SITE / 'پاتوژن' / 'index.html').read_text(encoding='utf-8')
    results = []
    # newest first for the hub
    metas = []
    for path in NEW:
        REAL[path] = SITE / path.strip('/') / 'index.html'
        BY_NORM[norm(path)] = path
    for path in NEW:
        print('new', path)
        soup = soup_of(path)
        post = json.load(urllib.request.urlopen(urllib.request.Request(
            'http://abadis-med.com/wp-json/wp/v2/posts?slug=' + urllib.parse.quote(path.strip('/')) +
            '&_fields=date,title,excerpt,featured_media',
            headers={'User-Agent': UA}), timeout=40))
        info = post[0] if post else {}
        title = h1_of(soup) or html.unescape(info.get('title', {}).get('rendered') or path)
        desc = meta_desc(soup) or re.sub(r'<[^>]+>', '', info.get('excerpt', {}).get('rendered') or '')
        desc = re.sub(r'\s+', ' ', desc).strip()[:300]
        date = info.get('date') or ''
        blocks = blocks_from(content_node(soup), path)
        body_bits = []
        lead = ''
        # featured image
        mid = info.get('featured_media') or 0
        if mid:
            try:
                media = json.load(urllib.request.urlopen(urllib.request.Request(
                    f'http://abadis-med.com/wp-json/wp/v2/media/{mid}?_fields=source_url,alt_text',
                    headers={'User-Agent': UA}), timeout=40))
                info_img = ensure_image(media.get('source_url') or '', 1200)
                if info_img:
                    lead = (f'<div class="lead-img"><img src="{prefix_for(path)}{info_img["src"]}" '
                            f'width="{info_img["w"]}" height="{info_img["h"]}" alt="{esc(title)}" decoding="async"></div>')
            except Exception as e:
                print('  featured', e)
        for kind, text, block in blocks:
            if kind == 'h1':
                continue
            body_bits.append(block)
        faq = faq_html(soup)
        if faq:
            body_bits.append(faq[0])
        words = len(re.sub(r'<[^>]+>', ' ', '\n'.join(body_bits)).split())
        mins = max(1, round(words / 200))
        body = (lead + '\n' + '\n'.join(body_bits)).strip()
        page = template
        full_title = f'{title} | مقالات — مخازن طبی آبادیس'
        page = re.sub(r'<title>.*?</title>', f'<title>{esc(full_title)}</title>', page, count=1, flags=re.S)
        page = re.sub(r'(<meta name="description" content=")[^"]*"',
                      lambda m: m.group(1) + esc(desc) + '"', page, count=1)
        page = re.sub(r'(<meta property="og:title" content=")[^"]*"',
                      lambda m: m.group(1) + esc(full_title) + '"', page, count=1)
        page = re.sub(r'(<meta property="og:description" content=")[^"]*"',
                      lambda m: m.group(1) + esc(desc) + '"', page, count=1)
        can = 'https://abadis-med.com' + path
        page = re.sub(r'<link rel="canonical" href="[^"]*">',
                      f'<link rel="canonical" href="{can}">', page, count=1)
        page = re.sub(r'<h1>.*?</h1>', f'<h1>{esc(title)}</h1>', page, count=1, flags=re.S)
        page = re.sub(r'(<p class="crumbs">.*› )[^<]*(</p>)',
                      lambda m: m.group(1) + esc(title) + m.group(2), page, count=1, flags=re.S)
        page = re.sub(
            r'<div class="meta">.*?</div>',
            f'<div class="meta"><span>مقاله</span><span>{esc(jdate(date))}</span><span>زمان مطالعه: {fa(mins)} دقیقه</span></div>',
            page, count=1, flags=re.S)
        page = re.sub(r'(<article class="article prose post-v2">)[\s\S]*?(</article>)',
                      lambda m: m.group(1) + '\n' + body + '\n' + m.group(2), page, count=1)
        # json-ld article fields from the template
        page = page.replace('معرفی متداول ترین پاتوژن ها | تعریف پاتوژن', title)
        page = page.replace('https://abadis-med.com/پاتوژن/', can)
        page = page.replace('پاتوژن یک کلمه ریشه فرانسوی است که در فرهنگ معین به معنی هر عاملی که سبب ایجاد بیماری شود را پاتوژن می گویند.', desc)
        if date:
            page = re.sub(r'"datePublished": "[^"]*"', f'"datePublished": "{date[:10]}"', page, count=1)
        en = EN_TWIN[path]
        extras = [('en', en), ('fa-IR', path)]
        # lang switch
        page = page.replace('href="../en/blog/" hreflang="en"',
                            f'href="{esc(rel_link(path, en))}" hreflang="en"')
        fp = SITE / path.strip('/') / 'index.html'
        fp.parent.mkdir(parents=True, exist_ok=True)
        fp.write_text(page, encoding='utf-8')
        ensure_self_hreflang(fp, path, [('en', en)])
        fixed = fp.read_text(encoding='utf-8')
        en_abs = 'https://abadis-med.com' + en
        if f'hreflang="en" href="{en_abs}"' not in fixed.split('<body', 1)[0]:
            fixed = fixed.replace(
                '<link rel="alternate" hreflang="x-default"',
                f'<link rel="alternate" hreflang="en" href="{en_abs}">\n<link rel="alternate" hreflang="x-default"',
                1)
        lead_src = re.search(r'<div class="lead-img"><img src="([^"]+)"', fixed)
        if lead_src:
            fixed = re.sub(r'<meta property="og:image" content="[^"]*">',
                           f'<meta property="og:image" content="{lead_src.group(1)}">', fixed, count=1)
        fp.write_text(fixed, encoding='utf-8')
        # point the English page at this Farsi URL
        efp = SITE / en.strip('/') / 'index.html'
        if efp.is_file():
            et = efp.read_text(encoding='utf-8')
            et = re.sub(r'href="[^"]*" hreflang="fa-IR"',
                        f'href="{esc(rel_link(en, path))}" hreflang="fa-IR"', et, count=1)
            if 'hreflang="fa-IR" href="' not in et:
                block = (f'<link rel="alternate" hreflang="fa-IR" href="https://abadis-med.com{path}">\n'
                         f'<link rel="alternate" hreflang="en" href="https://abadis-med.com{en}">\n'
                         f'<link rel="alternate" hreflang="x-default" href="https://abadis-med.com{path}">')
                et = re.sub(r'(<link rel="canonical" href="[^"]*">)', r'\1\n' + block, et, count=1)
            efp.write_text(et, encoding='utf-8')
        metas.append((date, path, title, lead))
        results.append({'path': path, 'words': words, 'date': date})
        REAL[path] = fp
    # hub cards, newest first
    metas.sort(key=lambda x: x[0], reverse=True)
    hub = SITE / 'مقالات' / 'index.html'
    ht = hub.read_text(encoding='utf-8')
    cards = []
    for date, path, title, lead in metas:
        year = '1405'
        m = re.search(r'(\d{4})', jdate(date))
        # jdate uses persian digits; derive year from gregorian via jalali already in jdate string
        src = '../assets/img/post-thumb-fallback.webp'
        im = re.search(r'src="([^"]+)"', lead or '')
        if im:
            # lead is ../assets from the article; hub is also one level deep
            src = im.group(1)
        cards.append(
            f'<a class="post-card reveal" href="../{path.strip("/")}/" data-name="{esc(title)}" data-year="{year}">'
            f'<div class="ph txt"><img src="{src}" width="1280" height="720" alt="{esc(title)}" loading="lazy"></div>'
            f'<div class="body"><div class="card-meta"><span class="art-card-badge">مقاله</span></div>'
            f'<h3>{esc(title)}</h3><span class="go">ادامه مطلب</span></div></a>'
        )
    marker = '<div class="post-grid" id="postGrid" data-paged="12">'
    if marker in ht and path_not_in(ht, NEW[0]):
        ht = ht.replace(marker, marker + ''.join(cards), 1)
        hub.write_text(ht, encoding='utf-8')
    drop_redirects(NEW)
    return results


def path_not_in(text, path):
    return path.strip('/') not in text


def drop_redirects(paths):
    fp = DATA / 'url_aliases.json'
    text = fp.read_text(encoding='utf-8')
    for p in paths:
        text = re.sub(
            r'\n *"' + re.escape(p) + r'": \{\n(?:.*\n)*? *\},?',
            '\n', text, count=1)
        text = re.sub(
            r'\n *"' + re.escape(p.rstrip('/')) + r'": \{\n(?:.*\n)*? *\},?',
            '\n', text, count=1)
    text = re.sub(r',\s*\n\s*\}', '\n}', text)
    fp.write_text(text, encoding='utf-8')
    needles = [p.strip('/') for p in paths]
    for rel in ('_redirects', 'liara_nginx.conf', 'redirects-nginx.conf'):
        fp = SITE / rel
        if not fp.is_file():
            continue
        lines = fp.read_text(encoding='utf-8').splitlines(True)
        kept = []
        for line in lines:
            decoded = urllib.parse.unquote(line)
            if any(n in decoded for n in needles):
                continue
            kept.append(line)
        fp.write_text(''.join(kept), encoding='utf-8')
    doc = Path(__file__).resolve().parents[2] / 'docs' / 'url-migration-live-urls.md'
    if doc.is_file():
        lines = doc.read_text(encoding='utf-8').splitlines(True)
        kept = []
        for line in lines:
            if any(n in line for n in needles):
                continue
            kept.append(line)
        doc.write_text(''.join(kept), encoding='utf-8')


def prefetch(paths):
    urls = [live_url(p) for p in paths]
    ok = 0
    with ThreadPoolExecutor(max_workers=6) as ex:
        futs = {ex.submit(fetch, u): u for u in urls}
        for fut in as_completed(futs):
            try:
                fut.result()
                ok += 1
            except Exception as e:
                print('fetch fail', futs[fut], e)
    print('fetched', ok, '/', len(urls))


def run_articles():
    paths = list(dict.fromkeys(PARTIAL + SOURCES + VIDEOS))
    print('prefetch', len(paths) + len(NEW))
    prefetch(paths + NEW)
    out = {'partial': [], 'sources': [], 'videos': [], 'new': []}
    out['new'] = build_new_articles()
    for p in PARTIAL:
        print('partial', p)
        out['partial'].append(fill_page(p, soup_of(p)))
    for p in SOURCES:
        print('sources', p)
        out['sources'].append(fill_page(p, soup_of(p)))
    for p in VIDEOS:
        print('video', p)
        out['videos'].append(fill_page(p, soup_of(p), videos_only=True))
    return out


# ---------------------------------------------------------------- catalogues
def compress_pdf(src, dest):
    dest.parent.mkdir(parents=True, exist_ok=True)
    raw = dest.with_suffix('.raw.pdf')
    raw.write_bytes(src)
    before = raw.stat().st_size
    if before > 400_000:
        cmd = ['gs', '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.4', '-dPDFSETTINGS=/ebook',
               '-dNOPAUSE', '-dQUIET', '-dBATCH', f'-sOutputFile={dest}', str(raw)]
        import subprocess
        subprocess.run(cmd, check=False)
        if dest.is_file() and 0 < dest.stat().st_size < before:
            raw.unlink()
            return before, dest.stat().st_size
        if dest.is_file():
            dest.unlink()
    raw.rename(dest)
    return before, dest.stat().st_size


def add_catalogues():
    print('catalogues')
    fa_html = fetch(live_url('/کاتالوگ/'))
    en_html = fetch('http://www.abadis-med.com/en/center-download/')
    fa_soup = BeautifulSoup(fa_html, 'html.parser')
    en_soup = BeautifulSoup(en_html, 'html.parser')
    want_fa = ('تزرق-چربی', 'سواب-ساکشن')
    want_en = ('Fat_Injection', 'Oral_Suction_Swab')
    saved = []

    def grab(soup, needles, lang):
        found = []
        for a in soup.find_all('a', href=True):
            href = urllib.parse.unquote(a['href'])
            if '.pdf' not in href.lower():
                continue
            if not any(n in href for n in needles):
                continue
            title = ''
            node = a
            for _ in range(8):
                node = node.parent
                if not node:
                    break
                h = node.find(['h2', 'h3', 'h4'])
                if h and h.get_text(strip=True):
                    title = re.sub(r'\s+', ' ', h.get_text(' ', strip=True)).strip()
                    break
            img = None
            node = a
            for _ in range(8):
                node = node.parent
                if not node:
                    break
                img = node.find('img')
                if img:
                    break
            found.append((href, title, img))
        return found

    fa_items = grab(fa_soup, want_fa, 'fa')
    en_items = grab(en_soup, want_en, 'en')
    cards = []
    for href, title, img in fa_items:
        name = urllib.parse.unquote(urllib.parse.urlsplit(href).path).split('/')[-1]
        from pdf_bucket import pdf_bucket_url
        rel = pdf_bucket_url('wp-content/uploads/2026/11/' + name)
        before = after = 0
        cover = img_tag(img, '/کاتالوگ/') if img else ''
        if not cover:
            cover = '<img src="../assets/img/post-thumb-fallback.webp" width="1280" height="720" alt="" loading="lazy">'
        # img_tag includes a full tag; dl-card wants it inside .ph
        if 'src=' not in cover:
            cover = '<img src="../assets/img/post-thumb-fallback.webp" width="1280" height="720" alt="" loading="lazy">'
        cards.append(
            f'<a class="post-card dl-card reveal" href="{esc(rel)}" target="_blank" rel="noopener">'
            f'<div class="ph" style="aspect-ratio:1;background:#fff">{cover}</div>'
            f'<div class="body"><h3>{esc(title or name)}</h3><span class="go">دانلود کاتالوگ (PDF) ↓</span></div></a>'
        )
        saved.append({'lang': 'fa', 'file': name, 'title': title, 'bytes_in': before, 'bytes_out': after})
    if cards:
        fp = SITE / 'کاتالوگ' / 'index.html'
        t = fp.read_text(encoding='utf-8')
        marker = '<div class="post-grid">'
        if marker in t and 'تزرق-چربی' not in t and 'سواب-ساکشن' not in t:
            t = t.replace(marker, marker + ''.join(cards), 1)
            fp.write_text(t, encoding='utf-8')
    en_cards_note = []
    # clone one existing column
    efp = SITE / 'en' / 'center-download' / 'index.html'
    et = efp.read_text(encoding='utf-8')
    for href, title, img in en_items:
        name = urllib.parse.unquote(urllib.parse.urlsplit(href).path).split('/')[-1]
        from pdf_bucket import pdf_bucket_url
        rel = pdf_bucket_url('en/wp-content/uploads/2026/11/' + name)
        before = after = 0
        cover = ''
        if img:
            info = ensure_image(img_url_of(img), 800)
            if info:
                cover = (f'<img width="{info["w"]}" height="{info["h"]}" src="../../{info["src"]}" '
                         f'alt="{esc(title)}" loading="lazy">')
        if not cover:
            cover = '<img width="768" height="768" src="../../assets/img/post-thumb-fallback.webp" alt="" loading="lazy">'
        column = (
            '<div data-element_type="column"><div><div data-element_type="widget"><div>'
            f'{cover}</div></div><div data-element_type="widget"><div><h2>{esc(title or name)}</h2></div></div>'
            '<div data-element_type="widget"><div><div>'
            f'<a href="{esc(rel)}" target="_blank" role="button"><span><span>Download Catalogue</span></span></a>'
            '</div></div></div></div></div>'
        )
        if name not in et:
            # insert before the downloads section closes — after the last column
            idx = et.rfind('data-element_type="column"')
            # append before </main> if present else at end of body content
            at = et.find('</main>')
            if at < 0:
                at = et.find('<footer')
            et = et[:at] + column + '\n' + et[at:]
        en_cards_note.append({'lang': 'en', 'file': name, 'title': title, 'bytes_in': before, 'bytes_out': after})
    efp.write_text(et, encoding='utf-8')
    saved.extend(en_cards_note)
    return saved


# ---------------------------------------------------------------- careers
EXTRA_EN = [
    'Chief Executive Officer', 'Commercial Manager', 'Accounting Manager', 'Finance Manager',
    'Human Resources Manager', 'Product Manager', 'Plant Manager', 'Plant Technical Supervisor',
    'Senior Accountant', 'Sales Accountant', 'Warehouse Keeper', 'Injection-machine Operator',
    'Injection-machine Specialist', 'Courier', 'Installation and Commissioning Specialist',
    'Sales Support Specialist', 'Office Manager',
]
EXTRA_AR = [
    'الرئيس التنفيذي', 'مدير تجاري', 'مدير المحاسبة', 'مدير مالي', 'مدير الموارد البشرية',
    'مدير المنتج', 'مدير المصنع', 'مشرف المصنع الفني', 'محاسب أول', 'محاسب مبيعات',
    'أمين المستودع', 'مشغّل آلة الحقن', 'أخصائي آلة الحقن', 'محصّل', 'أخصائي التركيب والتشغيل',
    'أخصائي دعم المبيعات', 'مسؤول المكتب',
]

COPY = {
    'en': dict(
        subject='Job Application — Abadis Med',
        legend='Application steps',
        steps=['Role and personal details', 'Education and work history', 'Workplace priorities (1 to 8)', 'Languages, software and skills'],
        s1h='Step 1 — Role and personal details',
        s1p='Choose a role, or the general talent pool, and enter your personal details.',
        role='Role you are applying for *',
        choose='Select…',
        general='General talent pool / not listed above',
        first='First name *', last='Last name *', father="Father's name *",
        military='Military service status *',
        birth='Date of birth *', birthph='1370/01/01',
        birthplace='Place of birth *',
        nid='National ID / passport number *',
        issue='Place of issue *',
        marital='Marital status *', single='Single', married='Married',
        illness='Serious illness or hospital admission *', no='No', yes='Yes',
        land='Landline *', mobile='Mobile phone *',
        address='Full home address *', addressph='Province, city, street, number, unit',
        next2='Continue to step 2 — education and work',
        s2h='Step 2 — Education, work history and pay',
        s2p='Add your education, previous roles and current job.',
        edu='Education *', work='Work history *', current='Current job *',
        add='Add a row',
        note_work='Add another row for each additional role.',
        note_current='Complete this if you are employed now.',
        degree='Level', school='School or university', cert='Certificate type', field='Field of study',
        when='Dates (start – end)', gpa='Grade',
        org='Organization', job='Job title', span='Dates (start – end)', pay='Last pay',
        manager='Manager', phone='Phone', why='Reason for leaving',
        lastpay='Last salary *', askpay='Requested salary *',
        heard='How did you hear about Abadis? *',
        heardph='Official Abadis website, LinkedIn, a colleague, Iran Health…',
        rankph='1 to 8',
        back1='Back to step 1', next3='Continue to step 3 — priorities',
        s3h='Step 3 — What you want from a workplace (rank 1 to 8)',
        s3p='Give each of the eight items a rank from 1 to 8.',
        expects=['Job security', 'A calm workplace', 'Colleagues', 'Close to home', 'Career growth', 'Related to my studies', 'Income', 'Prestige'],
        back2='Back to step 2', next4='Continue to step 4 — skills',
        s4h='Step 4 — Languages, software and what you bring',
        s4p='Add languages, software and a short note, then submit.',
        langs='Foreign languages',
        lang_opts=['English', 'German', 'Spanish', 'Other languages'],
        soft='Software *',
        note_soft='List the general or specialist software you use.',
        soft_type='Software', soft_level='Level (fair / good / excellent)', soft_note='Notes',
        about='In one paragraph, describe your skills and the role you want:',
        aboutph='A short summary of results, interests and what you would add to the team…',
        back3='Back to step 3', submit='Submit application',
        foot='After you submit, a structured summary is sent to human resources (info@abadis-med.com).',
        stepof='Step {n} of 4',
        dir='ltr',
    ),
    'ar': dict(
        subject='طلب التعاون — آباديس',
        legend='خطوات الطلب',
        steps=['الفرصة والبيانات الشخصية', 'التحصيل العلمي والخبرة', 'أولويات بيئة العمل (١ إلى ٨)', 'اللغة والحاسوب والمهارات'],
        s1h='الخطوة ١ — الفرصة والبيانات الشخصية',
        s1p='اختر الفرصة أو إرسال سيرة عامة، ثم أدخل البيانات الشخصية.',
        role='المسمى الوظيفي المطلوب *',
        choose='اختر…',
        general='إرسال سيرة ذاتية عامة / خارج الوظائف المعروضة',
        first='الاسم *', last='اسم العائلة *', father='اسم الأب *',
        military='حالة الخدمة العسكرية *',
        birth='تاريخ الميلاد *', birthph='١٣٧٠/٠١/٠١',
        birthplace='مكان الميلاد *',
        nid='رقم الهوية الوطنية / جواز السفر *',
        issue='مكان الإصدار *',
        marital='الحالة الاجتماعية *', single='أعزب', married='متزوج',
        illness='مرض خاص أو سابقة دخول مستشفى *', no='لا', yes='نعم',
        land='الهاتف الأرضي *', mobile='الهاتف المحمول *',
        address='عنوان السكن الكامل *', addressph='المحافظة، المدينة، الشارع، الرقم، الوحدة',
        next2='المتابعة إلى الخطوة ٢ — التحصيل والخبرة',
        s2h='الخطوة ٢ — التحصيل العلمي والخبرة والراتب',
        s2p='أدخل المراحل الدراسية والخبرات السابقة والعمل الحالي.',
        edu='التحصيل العلمي *', work='الخبرة العملية *', current='العمل الحالي *',
        add='إضافة صف',
        note_work='أضف صفاً لكل خبرة إضافية.',
        note_current='أكمل هذا القسم إذا كنت تعمل حالياً.',
        degree='المستوى', school='المؤسسة التعليمية', cert='نوع الشهادة', field='التخصص',
        when='الفترة (البداية - النهاية)', gpa='المعدل',
        org='اسم الجهة', job='المسمى الوظيفي', span='مدة التعاون', pay='آخر راتب',
        manager='اسم المدير', phone='الهاتف', why='سبب انتهاء التعاون',
        lastpay='آخر راتب *', askpay='الراتب المطلوب *',
        heard='كيف تعرفت على آباديس؟ *',
        heardph='الموقع الرسمي لأباديس، لينكدإن، زميل، معرض إيران هلث…',
        rankph='١ إلى ٨',
        back1='العودة إلى الخطوة ١', next3='المتابعة إلى الخطوة ٣ — الأولويات',
        s3h='الخطوة ٣ — أولوياتك في بيئة العمل (من ١ إلى ٨)',
        s3p='أعطِ كل معيار من الثمانية رقماً من ١ إلى ٨ حسب أولويتك.',
        expects=['الأمان الوظيفي', 'بيئة هادئة', 'الزملاء', 'قرب مكان العمل', 'التقدم الوظيفي', 'الارتباط بالدراسة', 'الدخل', 'المكانة'],
        back2='العودة إلى الخطوة ٢', next4='المتابعة إلى الخطوة ٤ — المهارات',
        s4h='الخطوة ٤ — اللغات والبرامج وما تقدمه',
        s4p='أدخل اللغات والبرامج وملخص قدراتك ثم أرسل الطلب.',
        langs='اللغات الأجنبية',
        lang_opts=['الإنجليزية', 'الألمانية', 'الإسبانية', 'لغات أخرى'],
        soft='الحاسوب والبرامج *',
        note_soft='أدخل البرامج العامة أو التخصصية التي تتقنها.',
        soft_type='نوع البرنامج', soft_level='مستوى الإلمام (متوسط - جيد - ممتاز)', soft_note='ملاحظات',
        about='اشرح في فقرة قدراتك والفرصة التي تناسبك:',
        aboutph='ملخص الإنجازات والاهتمامات وما تضيفه إلى فريق آباديس…',
        back3='العودة إلى الخطوة ٣', submit='إرسال طلب التعاون',
        foot='بعد الإرسال تصل خلاصة منظمة من النموذج إلى الموارد البشرية (info@abadis-med.com).',
        stepof='الخطوة {n} من ٤',
        dir='rtl',
    ),
}

PLUS = '<svg viewBox="0 0 20 20" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 4v12M4 10h12" stroke-linecap="round"/></svg>'
WIZARD = r'''
<script>
/* abadis-career-wizard */
(function () {
  document.querySelectorAll('.cf-form').forEach(function (form) {
    function showStep(n) {
      form.querySelectorAll('.cf-step-tab').forEach(function (t) {
        var on = t.getAttribute('data-step-btn') === String(n);
        t.classList.toggle('is-active', on);
        t.setAttribute('aria-selected', on ? 'true' : 'false');
      });
      form.querySelectorAll('.cf-step-pane').forEach(function (p) {
        p.classList.toggle('is-active', p.getAttribute('data-step-pane') === String(n));
      });
    }
    form.querySelectorAll('[data-step-btn]').forEach(function (t) {
      t.addEventListener('click', function () { showStep(t.getAttribute('data-step-btn')); });
    });
    form.querySelectorAll('[data-step-go]').forEach(function (b) {
      b.addEventListener('click', function () { showStep(b.getAttribute('data-step-go')); });
    });
    form.querySelectorAll('[data-cf-list]').forEach(function (block) {
      var addBtn = block.querySelector('[data-cf-add]');
      var rowsWrap = block.querySelector('.cf-list-rows');
      if (!addBtn || !rowsWrap) return;
      addBtn.addEventListener('click', function () {
        var first = rowsWrap.querySelector('.cf-list-row');
        if (!first) return;
        var clone = first.cloneNode(true);
        clone.querySelectorAll('input').forEach(function (inp) { inp.value = ''; });
        rowsWrap.appendChild(clone);
      });
    });
    form.addEventListener('submit', function () {
      var bad = form.querySelector(':invalid');
      if (!bad) return;
      var pane = bad.closest('[data-step-pane]');
      if (pane) showStep(pane.getAttribute('data-step-pane'));
    }, true);
  });
  document.addEventListener('click', function (e) {
    var btn = e.target.closest('[data-select-role]');
    if (!btn) return;
    var sel = document.querySelector('.cf-role-select');
    if (!sel) return;
    e.preventDefault();
    sel.value = btn.getAttribute('data-select-role');
    var formSec = sel.closest('#apply, .co-apply-sec') || sel;
    formSec.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });
})();
</script>
'''


def list_block(title, note, fields, names):
    inputs = ''.join(
        f'<label class="cf-lbl"><span>{esc(lab)}</span><input type="text" name="{esc(nm)}" required autocomplete="off"></label>'
        for lab, nm in zip(fields, names)
    )
    note_html = f'<p class="cf-note">{esc(note)}</p>' if note else ''
    return (
        f'<div class="cf-list-block" data-cf-list><div class="cf-list-head"><h4>{esc(title)}</h4>'
        f'<button type="button" class="cf-btn-add" data-cf-add>{PLUS} {esc(COPY[list_block.lang]["add"])}</button></div>'
        f'{note_html}<div class="cf-list-rows"><div class="cf-list-row">{inputs}</div></div></div>'
    )


def career_form(lang, roles):
    c = COPY[lang]
    list_block.lang = lang
    opts = [f'<option value="">{esc(c["choose"])}</option>',
            f'<option value="{esc(c["general"])}">{esc(c["general"])}</option>']
    seen = {c['general']}
    for role in roles:
        if role in seen:
            continue
        seen.add(role)
        opts.append(f'<option value="{esc(role)}">{esc(role)}</option>')
    extras = EXTRA_EN if lang == 'en' else EXTRA_AR
    for role in extras:
        if role in seen:
            continue
        seen.add(role)
        opts.append(f'<option value="{esc(role)}">{esc(role)}</option>')
    nums = '1234' if lang == 'en' else '١٢٣٤'
    tabs = []
    for i, label in enumerate(c['steps'], 1):
        on = ' is-active' if i == 1 else ''
        sel = 'true' if i == 1 else 'false'
        tabs.append(
            f'<button type="button" class="cf-step-tab{on}" data-step-btn="{i}" role="tab" aria-selected="{sel}">'
            f'<span class="cf-step-num">{nums[i-1]}</span><span class="cf-step-txt">{esc(label)}</span></button>'
        )
    edu_fields = [c['degree'], c['school'], c['cert'], c['field'], c['when'], c['gpa']]
    edu_names = ['سوابق تحصیلی — مقطع تحصیلی', 'سوابق تحصیلی — نام موسسه آموزشی', 'سوابق تحصیلی — نوع مدرک آموزشی',
                 'سوابق تحصیلی — نام گرایش یا رشته', 'سوابق تحصیلی — زمان آموزش (شروع - خاتمه)', 'سوابق تحصیلی — معدل']
    work_fields = [c['org'], c['job'], c['span'], c['pay'], c['manager'], c['phone'], c['why']]
    work_names = ['سوابق کاری — نام سازمان', 'سوابق کاری — عنوان شغل', 'سوابق کاری — مدت همکاری(شروع-خاتمه)',
                  'سوابق کاری — آخرین دریافتی', 'سوابق کاری — نام مدیر', 'سوابق کاری — تلفن تماس', 'سوابق کاری — علت قطع همکاری']
    cur_names = [n.replace('سوابق کاری', 'شغل فعلی') for n in work_names]
    soft_fields = [c['soft_type'], c['soft_level'], c['soft_note']]
    soft_names = ['آشنایی با کامپیوتر — نوع نرم افزار', 'آشنایی با کامپیوتر — میزان آشنایی (متوسط-خوب-عالی)', 'آشنایی با کامپیوتر — توضیحات']
    expects = ''.join(
        f'<label class="cf-lbl cf-expect-item"><span>{esc(lab)}</span>'
        f'<input type="number" min="1" max="8" inputmode="numeric" name="انتظار از محیط کار — {esc(fa_name)}" placeholder="{esc(c["rankph"])}" required></label>'
        for lab, fa_name in zip(c['expects'],
                                ['امنیت شغلی', 'محیط آرام', 'همکاران', 'نزدیکی محل', 'پیشرفت شغلی', 'مرتبط با تحصیلات', 'درآمد', 'پرستیژ'])
    )
    langs = ''.join(
        f'<label class="cf-check"><input type="checkbox" name="زبان‌های خارجی" value="{esc(v)}"><span>{esc(v)}</span></label>'
        for v in c['lang_opts']
    )
    return f'''<form class="cf-form" id="c1-form" data-abadis-form="careers" data-mailto-form="info@abadis-med.com" data-subject="{esc(c["subject"])}" dir="{c["dir"]}">
<input type="hidden" name="form_name" value="careers">
<label class="hp-field" aria-hidden="true">Leave blank<input type="text" name="_gotcha" tabindex="-1" autocomplete="off"></label>
<div class="cf-stepper" role="tablist" aria-label="{esc(c["legend"])}">{''.join(tabs)}</div>
<div class="cf-step-pane is-active" data-step-pane="1">
<div class="cf-pane-head"><h3>{esc(c["s1h"])}</h3><p>{esc(c["s1p"])}</p></div>
<div class="cf-grid-2">
<label class="cf-lbl cf-col-span-2"><span>{esc(c["role"])}</span><select name="عنوان شغلی" class="cf-role-select" required>{''.join(opts)}</select></label>
<label class="cf-lbl"><span>{esc(c["first"])}</span><input type="text" name="نام" required autocomplete="given-name"></label>
<label class="cf-lbl"><span>{esc(c["last"])}</span><input type="text" name="نام خانوادگی" required autocomplete="family-name"></label>
<label class="cf-lbl"><span>{esc(c["father"])}</span><input type="text" name="نام پدر" required></label>
<label class="cf-lbl"><span>{esc(c["military"])}</span><input type="text" name="وضعیت نظام وظیفه" required></label>
<label class="cf-lbl"><span>{esc(c["birth"])}</span><input type="text" name="تاریخ تولد" placeholder="{esc(c["birthph"])}" inputmode="numeric" required></label>
<label class="cf-lbl"><span>{esc(c["birthplace"])}</span><input type="text" name="محل تولد" required></label>
<label class="cf-lbl"><span>{esc(c["nid"])}</span><input type="text" name="شماره شناسنامه" inputmode="numeric" required></label>
<label class="cf-lbl"><span>{esc(c["issue"])}</span><input type="text" name="محل صدور" required></label>
<label class="cf-lbl"><span>{esc(c["marital"])}</span><select name="وضعیت تاهل" required><option value="">{esc(c["choose"])}</option><option>{esc(c["single"])}</option><option>{esc(c["married"])}</option></select></label>
<label class="cf-lbl"><span>{esc(c["illness"])}</span><select name="بیماری خاص یا سابقه بستری" required><option value="">{esc(c["choose"])}</option><option>{esc(c["no"])}</option><option>{esc(c["yes"])}</option></select></label>
<label class="cf-lbl"><span>{esc(c["land"])}</span><input type="tel" dir="ltr" name="تلفن ثابت" required inputmode="tel"></label>
<label class="cf-lbl"><span>{esc(c["mobile"])}</span><input type="tel" dir="ltr" name="تلفن همراه" required inputmode="tel"></label>
<label class="cf-lbl cf-col-span-2"><span>{esc(c["address"])}</span><input type="text" name="آدرس محل سکونت" placeholder="{esc(c["addressph"])}" required></label>
</div>
<div class="cf-step-nav"><span>{esc(c["stepof"].format(n=1 if lang=="en" else "١"))}</span><button type="button" class="cf-btn-primary" data-step-go="2">{esc(c["next2"])}</button></div>
</div>
<div class="cf-step-pane" data-step-pane="2">
<div class="cf-pane-head"><h3>{esc(c["s2h"])}</h3><p>{esc(c["s2p"])}</p></div>
{list_block(c["edu"], "", edu_fields, edu_names)}
{list_block(c["work"], c["note_work"], work_fields, work_names)}
{list_block(c["current"], c["note_current"], work_fields, cur_names)}
<div class="cf-grid-2" style="margin-top:16px">
<label class="cf-lbl"><span>{esc(c["lastpay"])}</span><input type="text" name="آخرین حقوق دریافتی" inputmode="numeric" required></label>
<label class="cf-lbl"><span>{esc(c["askpay"])}</span><input type="text" name="حقوق درخواستی" inputmode="numeric" required></label>
<label class="cf-lbl cf-col-span-2"><span>{esc(c["heard"])}</span><input type="text" name="طریق مراجعه به شرکت جهت استخدام" placeholder="{esc(c["heardph"])}" required></label>
</div>
<div class="cf-step-nav"><button type="button" class="cf-btn-ghost" data-step-go="1">{esc(c["back1"])}</button><button type="button" class="cf-btn-primary" data-step-go="3">{esc(c["next3"])}</button></div>
</div>
<div class="cf-step-pane" data-step-pane="3">
<div class="cf-pane-head"><h3>{esc(c["s3h"])}</h3><p>{esc(c["s3p"])}</p></div>
<div class="cf-expect-grid">{expects}</div>
<div class="cf-step-nav"><button type="button" class="cf-btn-ghost" data-step-go="2">{esc(c["back2"])}</button><button type="button" class="cf-btn-primary" data-step-go="4">{esc(c["next4"])}</button></div>
</div>
<div class="cf-step-pane" data-step-pane="4">
<div class="cf-pane-head"><h3>{esc(c["s4h"])}</h3><p>{esc(c["s4p"])}</p></div>
<fieldset class="cf-fieldset"><legend>{esc(c["langs"])}</legend><div class="cf-checks">{langs}</div></fieldset>
{list_block(c["soft"], c["note_soft"], soft_fields, soft_names)}
<label class="cf-lbl" style="margin-top:16px"><span>{esc(c["about"])}</span><textarea name="توانایی و مهارت و شغل ایده‌آل" rows="4" placeholder="{esc(c["aboutph"])}"></textarea></label>
<div class="cf-step-nav"><button type="button" class="cf-btn-ghost" data-step-go="3">{esc(c["back3"])}</button><button type="submit" class="cf-btn-submit">{esc(c["submit"])}</button></div>
<p class="cf-submit-note">{esc(c["foot"])}</p>
<p class="form-status" role="status" aria-live="polite"></p>
</div>
</form>'''


def install_careers():
    done = []
    for lang, rel in (('en', 'en/collaboration-opportunities/index.html'), ('ar', 'arabic/careers/index.html')):
        fp = SITE / rel
        text = fp.read_text(encoding='utf-8')
        roles = [html.unescape(r) for r in re.findall(r'data-select-role="([^"]+)"', text)]
        form = career_form(lang, roles)
        text2, n = re.subn(r'<form[^>]*data-abadis-form="careers"[\s\S]*?</form>', form, text, count=1)
        if n != 1:
            print('career form not replaced', rel)
            done.append({'lang': lang, 'ok': False})
            continue
        # point the general CTA at the general option
        general = COPY[lang]['general']
        text2 = re.sub(
            r'(<a class="co-resume-cta"[^>]*)(>)',
            lambda m: (m.group(1) if 'data-select-role' in m.group(1) else m.group(1) + f' data-select-role="{esc(general)}"') + m.group(2),
            text2, count=1)
        if 'abadis-career-wizard' not in text2:
            text2 = text2.replace('</body>', WIZARD + '</body>', 1)
        fp.write_text(text2, encoding='utf-8')
        done.append({'lang': lang, 'ok': True, 'roles': len(roles)})
    return done


def install_archives():
    """Empty English categories, and /page/N duplicates of the blog index."""
    import pages_archives
    built = []
    data = pages_archives.load_cache()
    want = set()
    for term in data['tax']['en'].get('categories') or []:
        path = pages_archives.path_of(term.get('link') or '')
        fp = SITE / path.strip('/') / 'index.html'
        if not fp.is_file():
            want.add(path)
    if want:
        written = []

        def write(rel, html_text):
            f = SITE / rel
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(html_text, encoding='utf-8')
            written.append(rel)

        b = pages_archives.Builder(data, write)
        b.want = want
        b.build_tax()
        built.extend(sorted(want))
        print('archive built', built)
    # /en/blog/page/N and /en/latest-news/page/N duplicate the /N/ pages
    kept = []
    rules_r, rules_n = [], []
    for base, nmax in (('/en/blog/', 6), ('/en/latest-news/', 4)):
        for n in range(2, nmax + 1):
            src = f'{base}page/{n}/'
            dst = f'{base}{n}/'
            if (SITE / dst.strip('/') / 'index.html').is_file() and not (SITE / src.strip('/') / 'index.html').is_file():
                enc_src = urllib.parse.quote(src)
                rules_r.append(f'{enc_src} {dst} 301\n')
                rules_n.append(f'rewrite "^{src}?" "{dst}" permanent;\n')
                kept.append({'from': src, 'to': dst, 'why': 'same listing as the /N/ page; live Yoast canonical points at the section index'})
    if rules_r:
        (SITE / '_redirects').write_text((SITE / '_redirects').read_text(encoding='utf-8') + ''.join(rules_r), encoding='utf-8')
        for name in ('liara_nginx.conf', 'redirects-nginx.conf'):
            fp = SITE / name
            t = fp.read_text(encoding='utf-8')
            if '/en/blog/page/' not in t:
                fp.write_text(t.rstrip() + '\n' + ''.join(rules_n), encoding='utf-8')
    return {'built': built, 'kept_redirects': kept}


def link_check(paths):
    broken = []
    for path in paths:
        fp = local_file(path)
        if not fp or not fp.is_file():
            continue
        text = fp.read_text(encoding='utf-8', errors='ignore')
        # only the article body, to ignore chrome
        m = re.search(r'<article[\s\S]*?</article>', text)
        chunk = m.group(0) if m else text
        for href in re.findall(r'href="([^"]+)"', chunk):
            if href.startswith(('http://', 'https://', 'mailto:', 'tel:', '#', 'javascript:')):
                continue
            if href.startswith('//'):
                continue
            target = urllib.parse.urljoin('/' + path.strip('/') + '/', href)
            target = urllib.parse.unquote(urllib.parse.urlsplit(target).path)
            if target.endswith('/'):
                ok = (SITE / target.strip('/') / 'index.html').is_file() or target in ('/',)
                # home
                if target.strip('/') == '' and (SITE / 'index.html').is_file():
                    ok = True
            else:
                ok = (SITE / target.lstrip('/')).is_file()
            if not ok:
                broken.append((path, href))
    return broken


def main():
    rep = {}
    if '--resume' in sys.argv:
        print('resume')
        rep['articles'] = {'new': build_new_articles(), 'partial': [], 'sources': [], 'videos': []}
        for p in PARTIAL + SOURCES:
            print('refill', p)
            rep['articles']['partial' if p in PARTIAL else 'sources'].append(fill_page(p, soup_of(p)))
        for p in VIDEOS:
            print('video', p)
            rep['articles']['videos'].append(fill_page(p, soup_of(p), videos_only=True))
    else:
        rep['articles'] = run_articles()
    rep['catalogues'] = add_catalogues()
    rep['careers'] = install_careers()
    rep['archives'] = install_archives()
    touched = NEW + PARTIAL + SOURCES + VIDEOS
    rep['broken_links'] = link_check(touched)[:40]
    rep['new_bytes'] = NEW_BYTES
    out = DATA / 'gap-close-report.json'
    json.dump(rep, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('videos', sum(x.get('videos', 0) for x in rep['articles']['videos']))
    print('partial added', [(x['path'], x.get('added')) for x in rep['articles']['partial']])
    print('sources added', [(x['path'], x.get('added')) for x in rep['articles']['sources']])
    print('pdfs', rep['catalogues'])
    print('broken', len(rep['broken_links']))
    print('bytes', NEW_BYTES)


if __name__ == '__main__':
    main()
