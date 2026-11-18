"""Shared helpers for the Phase-2 static page generator (Siamak redesign).

Content source: Wayback Machine snapshots of abadis-med.com (live site unreachable
from the build box), extracted into tools/redesign/data/*.json.  Copy is verbatim.
"""
import hashlib, html, json, os, pathlib, re, urllib.parse as u
from PIL import Image, ImageSequence

ROOT = pathlib.Path(__file__).resolve().parents[2]
SITE = ROOT / 'site'
DATA = pathlib.Path(__file__).resolve().parent / 'data'
SITE_ORIGIN = 'https://abadis-med.com'
def _forms_enabled():
    """Public site stays on mailto until ABADIS_FORMS_ENABLED is turned on."""
    return os.environ.get('ABADIS_FORMS_ENABLED', '0').strip().lower() not in ('', '0', 'false', 'off', 'no')

def _form_endpoint():
    # Flag defaults off. A URL in the environment or form_endpoint.txt is ignored until the flag is on.
    if not _forms_enabled():
        return ''
    value = os.environ.get('ABADIS_FORM_ENDPOINT', '').strip()
    if value:
        return value
    try:
        return open(os.path.join(os.path.dirname(__file__), 'data', 'form_endpoint.txt'), encoding='utf-8').read().strip()
    except OSError:
        return ''

# Empty ⇒ site.js keeps the mailto fallback. Never commit a live endpoint or secrets.
FORM_ENDPOINT = _form_endpoint()
FORM_MAILTO = 'info@abadis-med.com'
RAW = pathlib.Path(os.environ.get(
    'ABADIS_IMG_RAW',
    str(pathlib.Path(__file__).resolve().parent / '.img-raw'),
))
OUT_IMG = SITE / 'assets/img/c'
esc = html.escape

def load(name):
    return json.load(open(DATA / name, encoding='utf-8'))

PAGES = load('pages.json')
IMGMAP = load('imgmap.json')

def _load_bucket():
    """Source URL -> {url, w, h} for images uploaded to the abadis-media bucket."""
    found = {}
    p = DATA / 'media-bucket.json'
    if not p.is_file():
        return found
    try:
        data = json.load(open(p, encoding='utf-8'))
    except (OSError, json.JSONDecodeError):
        return found
    items = data.get('items') if isinstance(data, dict) else None
    if not isinstance(items, dict):
        return found
    for src, rec in items.items():
        if isinstance(rec, dict) and rec.get('url'):
            found[src] = rec
            found[rec['url']] = rec
    return found

_BUCKET = _load_bucket()

def _bucket_rec(url):
    if not url:
        return None
    if url.startswith('//'):
        url = 'https:' + url
    for cand in (url, url.replace('http://', 'https://', 1), url.replace('https://', 'http://', 1)):
        rec = _BUCKET.get(cand)
        if rec:
            return rec
    base = os.environ.get('ABADIS_MEDIA_PUBLIC_BASE', '').strip().rstrip('/')
    if base and (url == base or url.startswith(base + '/')):
        return {'url': url, 'w': 0, 'h': 0}
    return None

FA = str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')
def fa(s): return str(s).translate(FA)

# ---------------------------------------------------------------- jalali
def g2j(gy, gm, gd):
    g_d_m = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    gy2 = gy + 1 if gm > 2 else gy
    days = 355666 + (365 * gy) + ((gy2 + 3) // 4) - ((gy2 + 99) // 100) + ((gy2 + 399) // 400) + gd + g_d_m[gm - 1]
    jy = -1595 + (33 * (days // 12053)); days %= 12053
    jy += 4 * (days // 1461); days %= 1461
    if days > 365:
        jy += (days - 1) // 365; days = (days - 1) % 365
    if days < 186: jm = 1 + days // 31; jd = 1 + days % 31
    else: jm = 7 + (days - 186) // 30; jd = 1 + (days - 186) % 30
    return jy, jm, jd
JMONTHS = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند']
def jdate(iso):
    """ISO timestamp (UTC or offset) -> 'D Month YYYY' Jalali in Tehran time."""
    if not iso: return ''
    from datetime import datetime, timedelta, timezone
    d = datetime.fromisoformat(iso.replace('Z', '+00:00'))
    if d.tzinfo is None: d = d.replace(tzinfo=timezone.utc)
    d = d.astimezone(timezone(timedelta(hours=3, minutes=30)))
    y, m, dd = g2j(d.year, d.month, d.day)
    return fa(f'{dd} {JMONTHS[m-1]} {y}')

# ---------------------------------------------------------------- images
def _key(url):
    p = u.urlsplit(url)
    return u.unquote(p.path)
_IMG_BY_PATH = {}
for k, v in IMGMAP.items():
    if v.get('ok'): _IMG_BY_PATH[_key(k)] = v['file']
_done = {}
def img(url, maxw=1400):
    """Return dict(src, w, h) relative to site root for a remote abadis image, or None if not archived.

    Prefers an already-built WebP in OUT_IMG (so rebuilds work without the raw cache).
    Converts from RAW only when the output is missing and the raw file exists.
    """
    if not url: return None
    if url.startswith('//'): url = 'https:' + url
    hit = _bucket_rec(url)
    if hit:
        return {'src': hit['url'], 'w': int(hit.get('w') or 0), 'h': int(hit.get('h') or 0), 'external': True}
    key = _key(url)
    f = _IMG_BY_PATH.get(key)
    name = hashlib.sha1(key.encode()).hexdigest()[:12] + f'-{maxw}.webp'
    ck = (key, maxw)
    if ck in _done: return _done[ck]
    OUT_IMG.mkdir(parents=True, exist_ok=True)
    out = OUT_IMG / name
    # Reuse built WebP even when RAW is absent (typical on a PC / fresh clone).
    if out.exists():
        try:
            with Image.open(out) as im:
                nw, nh = im.size
            r = {'src': 'assets/img/c/' + name, 'w': nw, 'h': nh}
            _done[ck] = r
            return r
        except Exception as e:
            print('IMG FAIL', url, e); return None
    if not f or not (RAW / f).exists():
        return None
    try:
        im = Image.open(RAW / f)
        animated = getattr(im, 'is_animated', False) and im.format == 'GIF'
        w, h = im.size
        if w > maxw: nw, nh = maxw, round(h * maxw / w)
        else: nw, nh = w, h
        if animated:
            frames, durs = [], []
            for fr in ImageSequence.Iterator(im):
                frames.append(fr.convert('RGBA').resize((nw, nh), Image.LANCZOS)); durs.append(fr.info.get('duration', 100))
            frames[0].save(out, 'WEBP', save_all=True, append_images=frames[1:], duration=durs, loop=0, quality=70, method=4)
        else:
            mode = 'RGBA' if (im.mode in ('RGBA', 'LA', 'P') and 'transparency' in im.info) or im.mode in ('RGBA', 'LA') else 'RGB'
            im2 = im.convert(mode)
            if (nw, nh) != (w, h): im2 = im2.resize((nw, nh), Image.LANCZOS)
            im2.save(out, 'WEBP', quality=78, method=5)
    except Exception as e:
        print('IMG FAIL', url, e); return None
    r = {'src': 'assets/img/c/' + name, 'w': nw, 'h': nh}
    _done[ck] = r
    return r

def full_url(src_url):
    """Strip WordPress -WxH size suffix so we prefer the biggest archived variant."""
    return re.sub(r'-\d+x\d+(\.\w+)$', r'\1', src_url)
def best_img(url, maxw=1400):
    """Try the original (unsized) upload first, then the given size."""
    if not url: return None
    for cand in (full_url(url), url):
        r = img(cand, maxw)
        if r: return r
    return None

# ---------------------------------------------------------------- links
PAGE_MAP = {
    '/': '', '/درباره-ما/': 'about/', '/محصولات/': 'products/',
    '/محصولات/کیسه-ساکشن/': 'products/suction-bag/', '/محصولات/فیلترها/': 'products/filters/',
    '/محصولات/مخزن/': 'products/canister/', '/محصولات/پایه/': 'products/stand/', '/محصولات/پایه-و-نگهدارنده-ها/': 'products/stand/',
    '/محصولات/اتصالات/': 'products/connectors/', '/محصولات/ساکشن-تیوب/': 'products/suction-tube/',
    '/محصولات/سایر-محصولات/': 'products/other/', '/آخرین-اخبار/': 'news/', '/مقالات/': 'articles/',
    '/لیست-نمایندگان/': 'dealers/', '/توسعه-پایدار/': 'sdgs/', '/مسئولیت-اجتماعی/': 'csr/#activities',
    '/ارتباط-با-ما/': 'contact/', '/محاسبه-گر/': 'calculator/', '/مشتریان-ما/': 'customers/',
    '/تجارب-ما/': 'experiences/', '/کاتالوگ/': 'downloads/', '/راهنمای-نصب/': 'install-guide/',
    '/راهنمای-نصب/راهنمای-نصب-مخازن/': 'install-guide/tanks/',
    '/راهنمای-نصب/راهنمای-استفاده-کاربر-نهایی/': 'install-guide/end-user/',
    '/پرسش-های-متداول/': 'faq/', '/فرصت-های-همکاری/': 'careers/', '/موقعیت-های-شغلی/': 'jobs/',
    '/_joboffers/': 'jobs/',
    # legacy URLs still linked from old posts
    '/محصولات/بهداشت-دهان/': 'products/oral-hygiene/', '/مخزن/': 'products/canister/', '/ساکشن-تیوب/': 'products/suction-tube/',
    '/کیسه-ساکشن/': 'products/suction-bag/', '/کیسه-ساکشن-یکبار-مصرف/': 'products/suction-bag/', '/فیلترها/': 'products/filters/',
    '/محصولات/دیگر-محصولات/': 'products/other/', '/محصولات/اتصالات-2/': 'products/connectors/', '/محصولات/فیلتر/': 'products/filters/', '/محصولات/اکسسوری/': 'products/connectors/',
}
POST_MAP = {}   # decoded path -> site-relative url (filled by posts builder)
# Alternate live slugs that point at an existing post/page (ZWNJ / old redirects / EN slug).
POST_ALIASES = {
    '/شرکتهای-دانشبنیان-در-صنعت-تجهیزات/': 'articles/17269/',
    '/انواع-عفونت‌های-بیمارستانی/': 'articles/713/',
    '/types-of-hospital-infections/': 'articles/713/',
    # Live slug variants longer/shorter than archived path truncation
    '/دستاوردهای-شرکت-مخازن-طبی-آبادیس-در-توسعه-کیسه-های-ساکشن-یکبار-مصرف/': 'articles/17431/',
    '/دستاوردهای-شرکت-مخازن-طبی-آبادیس-در-توسعه-کیسه-ساکشن/': 'articles/17431/',
    # Until /en/ ships (prompt 3), point EN product URLs at the FA equivalent.
    '/en/products/suction-bag/': 'products/suction-bag/',
}
def norm_path(url):
    s = u.urlsplit(url.strip())
    if s.netloc and s.netloc.lower().replace('www.', '') != 'abadis-med.com': return None
    p = u.unquote(s.path or '/')
    if not p.endswith('/') and '.' not in p.rsplit('/', 1)[-1]: p += '/'
    return p, s.fragment
def _slash_variants(p):
    bare = p.rstrip('/') or '/'
    if bare == '/':
        return ['/']
    return [bare + '/', bare]
def _post_lookup(p):
    for c in _slash_variants(p):
        if c in POST_MAP:
            return POST_MAP[c]
        if c in POST_ALIASES:
            return POST_ALIASES[c]
    zp = (p.replace('\u200c', '').rstrip('/') + '/') if p != '/' else '/'
    for k, v in POST_MAP.items():
        if (k.replace('\u200c', '').rstrip('/') + '/') == zp:
            return v
    for k, v in POST_ALIASES.items():
        if (k.replace('\u200c', '').rstrip('/') + '/') == zp:
            return v
    return None
def internal(url):
    """Map an abadis-med.com URL to a site-relative path ('' = home) or None."""
    if not url or url.startswith(('mailto:', 'tel:', '#')): return None
    r = norm_path(url)
    if not r: return None
    p, frag = r
    if p.startswith('/wp-content/'): return None
    hit = PAGE_MAP.get(p)
    if hit is None:
        for c in _slash_variants(p):
            if c in PAGE_MAP:
                hit = PAGE_MAP[c]; break
    if hit is None:
        hit = _post_lookup(p)
    if hit is None and p.startswith('/_joboffers/'):
        hit = JOB_MAP.get(p)
    if hit is None: return None
    if hit == 'products/suction-bag/' and frag in ('one', 'two', 'three'): frag = {'one': 's1', 'two': 's2', 'three': 's3'}[frag]
    if frag and '#' not in hit: hit += '#' + frag
    return hit
JOB_MAP = {}

def placed_src(prefix, r):
    """Page-relative src, or an absolute bucket URL unchanged."""
    src = (r or {}).get('src') or ''
    if r and (r.get('external') or src.startswith(('http://', 'https://', '//'))):
        return src
    return (prefix or '') + src

def dim_attrs(r):
    try:
        w, h = int((r or {}).get('w') or 0), int((r or {}).get('h') or 0)
    except (TypeError, ValueError):
        return ''
    if w > 0 and h > 0:
        return f' width="{w}" height="{h}"'
    return ''

def href(url, p):
    """Return (href, external?) for templates."""
    i = internal(url)
    if i is not None: return p + i if i else (p or './'), False
    if url and url.startswith('//'): url = 'https:' + url
    if url and re.match(r'^[A-Za-z0-9.-]+\.(me|com|ir|org|net|io)/', url): url = 'https://' + url
    return url, bool(url and url.startswith('http'))

def rewrite_html(h, p, imgw=1000, drop_missing_img=True):
    """Rewrite links + images inside sanitized crawl HTML."""
    def a_sub(m):
        url = html.unescape(m.group(1))
        new, ext = href(url, p)
        extra = ' target="_blank" rel="noopener"' if ext else ''
        return f'<a href="{esc(new, quote=True)}"{extra}'
    h = re.sub(r'<a href="([^"]*)"(?: target="_blank")?(?: rel="[^"]*")?', a_sub, h)
    def img_sub(m):
        tag = m.group(0)
        src = re.search(r'src="([^"]+)"', tag)
        alt = re.search(r'alt="([^"]*)"', tag)
        r = best_img(html.unescape(src.group(1)), imgw) if src else None
        if not r: return '' if drop_missing_img else tag
        alt_attr = alt.group(1) if alt else ''
        return f'<img src="{placed_src(p, r)}"{dim_attrs(r)} loading="lazy" decoding="async" alt="{alt_attr}">'
    h = re.sub(r'<img [^>]*>', img_sub, h)
    h = re.sub(r'<figure>\s*(<figcaption>.*?</figcaption>)?\s*</figure>', '', h, flags=re.S)
    h = re.sub(r'<p>\s*</p>', '', h)
    # AB-97: WordPress link embeds whose oEmbed never rendered arrive as a bare URL in a box;
    # show them like the other reference links in the article.
    def embed_sub(m):
        u = html.unescape(m.group(1)); new, ext = href(u, p)
        extra = ' target="_blank" rel="noopener"' if ext else ''
        return f'<p><a href="{esc(new, quote=True)}"{extra}>{esc(u)}</a></p>'
    h = re.sub(r'<figure class="wp-block-embed[^"]*">\s*<div class="wp-block-embed__wrapper">\s*(https?://[^\s<]+)\s*</div>\s*</figure>', embed_sub, h, flags=re.S)
    # R-004 / AB-76: wide WordPress tables scroll sideways on phones
    h = re.sub(r'<figure class="wp-block-table(?![^"]*table-scroll)', '<figure class="wp-block-table table-scroll', h)
    return h

def strip_tags(h): return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', h or ''))).strip()
