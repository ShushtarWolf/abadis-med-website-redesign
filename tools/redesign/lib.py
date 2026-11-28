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
# Liara Flask app in tools/forms-liara (service name abadis-forms).
DEFAULT_FORM_ENDPOINT = 'https://abadis-forms.liara.run/submit'

def _forms_enabled():
    """On unless ABADIS_FORMS_ENABLED is explicitly turned off."""
    return os.environ.get('ABADIS_FORMS_ENABLED', '1').strip().lower() not in ('0', 'false', 'off', 'no')

def _form_endpoint():
    # A rebuild or a WordPress publish keeps this URL. Override with
    # ABADIS_FORM_ENDPOINT, or with a single line in data/form_endpoint.txt.
    # ABADIS_FORMS_ENABLED=0 clears it. Never commit SMTP secrets.
    if not _forms_enabled():
        return ''
    value = os.environ.get('ABADIS_FORM_ENDPOINT', '').strip()
    if value:
        return value
    try:
        file_value = open(os.path.join(os.path.dirname(__file__), 'data', 'form_endpoint.txt'), encoding='utf-8').read().strip()
    except OSError:
        file_value = ''
    return file_value or DEFAULT_FORM_ENDPOINT

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
    if v.get('ok') and v.get('file'): _IMG_BY_PATH[_key(k)] = v['file']
_done = {}

# Files recovered after the WordPress move. They are served from the media bucket;
# the old abadis-med.com uploads 404. Paths stay the WordPress upload paths.
MEDIA_PUBLIC = 'https://abadis-media.storage.iran.liara.site/wp-content/uploads/'
RECOVERED_IMAGES = {
    '2017/08/suction_bag.jpg': ('2017/08/suction_bag.webp', 500, 500),
    '2017/08/compare.png': ('2017/08/compare.webp', 346, 142),
    '2019/05/Fixture-2.jpg': ('2019/05/Fixture-2.webp', 600, 400),
    '2021/10/AMR_4806-scaled-1.jpg': ('2021/10/AMR_4806-scaled-1.webp', 1600, 1067),
    '2022/06/پروتکل‌هایی-که-برای-کنترل-عفونت-باید-رعایت-کرد.jpg': (
        '2022/06/پروتکل‌هایی-که-برای-کنترل-عفونت-باید-رعایت-کرد.webp', 768, 511),
}
RECOVERED_VIDEOS = {
    '2019/06/Voice.mp4': '2019/06/Voice.mp4',
    '2019/06/medirence-Abadis-Iranhealth.mp4': '2019/06/medirence-Abadis-Iranhealth.mp4',
    '2020/04/Final.mp4': '2020/04/Final.mp4',
}
VOICE_POSTER = '/assets/img/c/8aa3f73d39c6-1200.webp'
_RECOVERED_ALT = {
    '2017/08/compare.png': 'مقایسه کیسه ساکشن یکبار مصرف آبادیس با کیسه ساکشن معمولی',
    '2017/08/compare.webp': 'مقایسه کیسه ساکشن یکبار مصرف آبادیس با کیسه ساکشن معمولی',
    '2019/05/Fixture-2.jpg': 'فیکسر نگهدارنده لوله تراشه',
    '2019/05/Fixture-2.webp': 'فیکسر نگهدارنده لوله تراشه',
}
_RECOVERED_BY_REL = {}
for _src, (_dest, _w, _h) in RECOVERED_IMAGES.items():
    _RECOVERED_BY_REL[_src] = (_dest, _w, _h)
    _RECOVERED_BY_REL[_dest] = (_dest, _w, _h)

def bucket_url(rel):
    return MEDIA_PUBLIC + '/'.join(u.quote(part) for part in rel.split('/'))

def upload_rel(url):
    if not url: return ''
    if url.startswith('//'): url = 'https:' + url
    path = u.unquote(u.urlsplit(html.unescape(url)).path)
    mark = '/wp-content/uploads/'
    i = path.find(mark)
    if i < 0: return ''
    return path[i + len(mark):]

def recovered_image(url):
    rec = _RECOVERED_BY_REL.get(upload_rel(url))
    if not rec: return None
    dest, w, h = rec
    return {'src': bucket_url(dest), 'w': w, 'h': h, 'external': True}

# WordPress appends -WIDTHxHEIGHT before the extension. One local WebP stands in
# for every size variant of the same upload. See data/wp_local_images.json.
_SIZE_SUFFIX = re.compile(r'-\d+x\d+(?=\.[A-Za-z0-9]+$)')
_UPLOAD_IMG_EXT = re.compile(r'\.(?:jpe?g|png|gif|webp|svg|bmp|avif)$', re.I)
_WP_LOCAL = None
_WP_STEMS = None
_WP_DIM = {}


def unsized_upload_path(path):
    return _SIZE_SUFFIX.sub('', path or '')


def upload_image_path(url):
    """Site path of an abadis-med.com upload image, or '' for anything else.

    Liara bucket URLs and PDFs are not upload images for this lookup.
    """
    if not url:
        return ''
    raw = html.unescape(str(url).strip())
    if raw.startswith('//'):
        raw = 'https:' + raw
    if raw.startswith('http://') or raw.startswith('https://'):
        parts = u.urlsplit(raw)
        host = parts.netloc.lower()
        if host.startswith('www.'):
            host = host[4:]
        if host != 'abadis-med.com':
            return ''
        path = u.unquote(parts.path or '')
    else:
        path = u.unquote(raw.split('#', 1)[0].split('?', 1)[0])
        if 'wp-content/uploads/' not in path:
            return ''
        if not path.startswith('/'):
            path = '/' + path[path.find('wp-content/uploads/'):]
    path = path.split('?', 1)[0].split('#', 1)[0]
    if '/wp-content/uploads/' not in path or not _UPLOAD_IMG_EXT.search(path):
        return ''
    return path


def _wp_local_map():
    global _WP_LOCAL
    if _WP_LOCAL is None:
        fp = DATA / 'wp_local_images.json'
        try:
            _WP_LOCAL = json.load(open(fp, encoding='utf-8'))
        except OSError:
            _WP_LOCAL = {}
    return _WP_LOCAL


def _wp_stem_index():
    global _WP_STEMS
    if _WP_STEMS is None:
        found = {}
        if OUT_IMG.is_dir():
            for f in OUT_IMG.glob('*.webp'):
                m = re.match(r'^([0-9a-f]{12})-(\d+)\.webp$', f.name)
                if m:
                    found.setdefault(m.group(1), []).append(f)
        _WP_STEMS = found
    return _WP_STEMS


def reset_wp_image_cache():
    global _WP_LOCAL, _WP_STEMS
    _WP_LOCAL = None
    _WP_STEMS = None
    _WP_DIM.clear()


def local_wp_image(url):
    """Local WebP for a leftover abadis-med.com upload image, or None.

    Size variants share one file. A hit is {src, w, h} with src relative to site/.
    """
    path = upload_image_path(url)
    if not path:
        return None
    canon = unsized_upload_path(path)
    mapped = _wp_local_map()
    rec = mapped.get(path) or mapped.get(canon)
    if rec and rec.get('src') and (SITE / rec['src']).is_file():
        return {'src': rec['src'], 'w': int(rec.get('w') or 0), 'h': int(rec.get('h') or 0)}
    idx = _wp_stem_index()
    hits = []
    for key in (canon, path):
        stem = hashlib.sha1(key.encode()).hexdigest()[:12]
        hits.extend(idx.get(stem) or [])
    if not hits:
        return None

    def nominal(f):
        m = re.search(r'-(\d+)\.webp$', f.name)
        return int(m.group(1)) if m else 0

    best = max(hits, key=lambda f: (nominal(f), f.stat().st_size if f.is_file() else 0))
    ck = str(best)
    if ck not in _WP_DIM:
        try:
            with Image.open(best) as im:
                _WP_DIM[ck] = im.size
        except Exception:
            return None
    w, h = _WP_DIM[ck]
    return {'src': 'assets/img/c/' + best.name, 'w': w, 'h': h}


_UPLOAD_URL_RE = re.compile(
    r'(?i)(?:https?:)?//(?:www\.)?abadis-med\.com(/(?:en/|arabic/)?wp-content/uploads/[^"\'\\\s,)]+)'
    r'|'
    r'(?<![A-Za-z0-9@])((?:\.\./)+(?:en/|arabic/)?wp-content/uploads/[^"\'\\\s,)]+)'
    r'|'
    r'(?<![A-Za-z0-9@])(/(?:en/|arabic/)?wp-content/uploads/[^"\'\\\s,)]+)'
    r'|'
    r'(?<![A-Za-z0-9@./])((?:en/|arabic/)?wp-content/uploads/[^"\'\\\s,)]+)'
)


def localize_abadis_upload_urls(text, prefix='', page_rel=''):
    """Point leftover upload image URLs at local WebPs (or the media bucket).

    PDFs, Liara URLs and files that already exist on disk are left in place.
    `page_rel` is the HTML path under site/, used to resolve ../ references.
    """
    if not text or 'wp-content/uploads' not in text:
        return text
    import posixpath
    base = posixpath.dirname(page_rel) if page_rel else ''

    def site_path_for(m):
        abs_path, ups, rooted, bare = m.group(1), m.group(2), m.group(3), m.group(4)
        if abs_path:
            return u.unquote(html.unescape(abs_path.split('?', 1)[0].split('#', 1)[0]))
        raw = ups or rooted or bare or ''
        raw = u.unquote(html.unescape(raw.split('?', 1)[0].split('#', 1)[0]))
        if raw.startswith('/'):
            return raw
        if raw.startswith('../') or raw.startswith('./'):
            joined = posixpath.normpath(posixpath.join(base, raw))
            if joined.startswith('..'):
                return ''
            return '/' + joined
        if 'wp-content/uploads/' in raw:
            return '/' + raw[raw.find('wp-content/uploads/'):]
        return ''

    def repl(m):
        path = site_path_for(m)
        if not path or not _UPLOAD_IMG_EXT.search(path):
            return m.group(0)
        # A relative URL that already resolves to a file in the repo is not a hotlink.
        if not m.group(1):
            local_file = SITE / path.lstrip('/')
            if local_file.is_file():
                return m.group(0)
        abs_url = 'https://abadis-med.com' + path
        rel = path.split('/wp-content/uploads/', 1)[-1]
        canon_url = 'https://abadis-med.com/wp-content/uploads/' + unsized_upload_path(rel)
        rec = recovered_image(abs_url) or recovered_image(canon_url)
        if rec:
            return rec['src']
        loc = local_wp_image(abs_url)
        if not loc:
            return m.group(0)
        src = loc['src']
        if src.startswith(('http://', 'https://', '//')):
            return src
        return (prefix or '') + src

    return _UPLOAD_URL_RE.sub(repl, text)

def _video_player(src, poster=''):
    poster_attr = f' poster="{esc(poster, quote=True)}"' if poster else ''
    return (
        '<video class="restored-video" controls preload="none" playsinline '
        'style="width:100%;max-width:640px;height:auto"'
        f'{poster_attr}><source src="{esc(src, quote=True)}" type="video/mp4"></video>'
    )

def _video_for_url(url, posters=None):
    rel = upload_rel(url)
    dest = RECOVERED_VIDEOS.get(rel)
    if not dest: return None
    poster = ''
    if posters:
        poster = posters.get(rel) or posters.get(dest) or ''
    if not poster and dest == '2019/06/Voice.mp4':
        poster = VOICE_POSTER
    return _video_player(bucket_url(dest), poster)

def _balanced_div_end(h, start):
    """End index (exclusive) of the div that begins at start."""
    i, depth, n = start, 0, len(h)
    while i < n:
        open_at = h.lower().find('<div', i)
        close_at = h.lower().find('</div>', i)
        if close_at < 0: return None
        if open_at != -1 and open_at < close_at:
            nxt = h[open_at + 4:open_at + 5]
            if nxt in ('', ' ', '\n', '\t', '\r', '>'):
                depth += 1
                i = open_at + 4
                continue
        depth -= 1
        i = close_at + 6
        if depth == 0: return i
    return None

def restore_recovered_media(h, posters=None):
    """Point recovered images and videos at the media bucket. Add-only for tags that exist."""
    if not h: return h
    def img_sub(m):
        tag = m.group(0)
        sm = re.search(r'\bsrc=(["\'])(.*?)\1', tag, re.I)
        if not sm: return tag
        rec = recovered_image(html.unescape(sm.group(2)))
        if not rec: return tag
        alt_m = re.search(r'\balt=(["\'])(.*?)\1', tag, re.I)
        alt = html.unescape(alt_m.group(2)) if alt_m else ''
        if not alt:
            alt = _RECOVERED_ALT.get(upload_rel(sm.group(2)), '')
        return (f'<img src="{esc(rec["src"], quote=True)}" width="{rec["w"]}" height="{rec["h"]}" '
                f'loading="lazy" decoding="async" alt="{esc(alt)}">')
    h = re.sub(r'<img\b[^>]*>', img_sub, h, flags=re.I)
    out, i = [], 0
    token = '<div class="wp-video"'
    low = h.lower()
    while True:
        j = low.find(token, i)
        if j < 0:
            out.append(h[i:]); break
        end = _balanced_div_end(h, j)
        if end is None:
            out.append(h[i:]); break
        block = h[j:end]
        player = None
        for url in re.findall(r'https?://[^"\'\s>]+\.mp4[^"\'\s<]*', block, re.I):
            player = _video_for_url(html.unescape(url), posters)
            if player: break
        out.append(h[i:j])
        out.append(player if player else block)
        i = end
        low = h.lower()
    h = ''.join(out)
    def video_sub(m):
        block = m.group(0)
        for url in re.findall(r'https?://[^"\'\s>]+\.mp4[^"\'\s<]*', block, re.I):
            player = _video_for_url(html.unescape(url), posters)
            if player: return player
        return block
    h = re.sub(r'<video\b[^>]*>.*?</video>', video_sub, h, flags=re.I | re.S)
    def a_sub(m):
        player = _video_for_url(html.unescape(m.group(2)), posters)
        return player if player else m.group(0)
    h = re.sub(
        r'<a\b[^>]*\bhref=(["\'])(https?://[^"\']+\.mp4[^"\']*)\1[^>]*>.*?</a>',
        a_sub, h, flags=re.I | re.S)
    # Broken MediaElement chrome left beside the replaced player.
    if 'restored-video' in h:
        h = re.sub(
            r'<div class="mejs-[^"]*"[^>]*>\s*(?:<span\b[^>]*>.*?</span>\s*)?</div>\s*',
            '', h, flags=re.I | re.S)
    return h

def img(url, maxw=1400):
    """Return dict(src, w, h) relative to site root for a remote abadis image, or None if not archived.

    Prefers an already-built WebP in OUT_IMG (so rebuilds work without the raw cache).
    Converts from RAW only when the output is missing and the raw file exists.
    """
    if not url: return None
    if url.startswith('//'): url = 'https:' + url
    hit = recovered_image(url)
    if hit: return hit
    hit = local_wp_image(url)
    if hit: return hit
    hit = _bucket_rec(url)
    if hit:
        return {'src': hit['url'], 'w': int(hit.get('w') or 0), 'h': int(hit.get('h') or 0), 'external': True}
    key = _key(url)
    f = _IMG_BY_PATH.get(key)
    stem = hashlib.sha1(key.encode()).hexdigest()[:12]
    name = stem + f'-{maxw}.webp'
    ck = (key, maxw)
    if ck in _done: return _done[ck]
    OUT_IMG.mkdir(parents=True, exist_ok=True)
    out = OUT_IMG / name
    # Reuse a WebP already built for this upload, at any width, so a posts rebuild
    # does not add a second derivative (the site is close to the Liara size cap).
    if not out.exists():
        alts = list(OUT_IMG.glob(stem + '-*.webp'))
        if alts:
            def _w(path):
                try:
                    return int(path.stem.rsplit('-', 1)[-1])
                except ValueError:
                    return 0
            out = max(alts, key=_w)
            name = out.name
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
        if not alt_attr and src:
            alt_attr = _RECOVERED_ALT.get(upload_rel(html.unescape(src.group(1))), '')
        return f'<img src="{placed_src(p, r)}"{dim_attrs(r)} loading="lazy" decoding="async" alt="{esc(alt_attr)}">'
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
    return restore_recovered_media(h)

def strip_tags(h): return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', h or ''))).strip()
