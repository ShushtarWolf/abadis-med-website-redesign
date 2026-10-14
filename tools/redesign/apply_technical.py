"""Patch built HTML for the technical brief items, then write sitemap, robots, redirects.

Does not rebuild page bodies. Generator modules (layout.py, i18n.py, pages_home.py)
emit the same canonical, hreflang and certificate paths on the next build.
"""
from __future__ import annotations
import csv
import hashlib
import html as html_lib
import posixpath
import re
import sys
import pathlib
from urllib.parse import unquote, urljoin, urlsplit, urlunsplit

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from lib import SITE, SITE_ORIGIN, PAGE_MAP
from i18n import ROBOTS_META, canonical_href, hreflang_links

ROOT = SITE.parent
GH_ROOTS = (
    'https://siaamak-ghodsi.github.io/abadis-med-redesign-live/',
    'http://siaamak-ghodsi.github.io/abadis-med-redesign-live/',
    'https://shushtarwolf.github.io/abadis-med-website-redesign/',
    'https://siaamak-ghodsi.github.io/abadis-scroll-scrub-demo/redesign/',
)
PROJECT = 'http://preview.local/abadis-med-redesign-live/'
CERT_URL = re.compile(
    r'cert|imed|\biso\b|/ce[-.]|ce\.jpg|license|patent|membership|\biqs\b|\bisc\b|'
    r'export-medical|industrial-plan|operation-license|/igc|ebcl|amedal|attendance',
    re.I,
)
THUMB_RE = re.compile(
    r'<div data-thumbnail="([^"]+)" data-width="(\d+)" data-height="(\d+)" alt=""\s*>\s*</div>'
)
ATTR_RE = re.compile(
    r'(?P<attr>href|src|poster)=(?P<q>["\'])(?P<url>.*?)(?P=q)',
    re.I,
)
SKIP_URL = ('http://', 'https://', 'mailto:', 'tel:', 'javascript:', 'data:', '#', '//')


def site_path_of(rel: str) -> str:
    if rel.endswith('index.html'):
        rel = rel[:-len('index.html')]
    return rel


def page_dir(rel: str) -> str:
    return posixpath.dirname(rel)


def exists(site_rel: str) -> bool:
    site_rel = site_rel.lstrip('/')
    if site_rel in ('', '.'):
        return (SITE / 'index.html').exists()
    p = SITE / site_rel
    if p.is_file():
        return True
    return (SITE / site_rel.rstrip('/') / 'index.html').exists()


def to_relative(page_rel: str, target: str) -> str:
    """Site-relative target ('' = home, 'contact/' = contact) as a link from this page."""
    directory = exists(target) and not (SITE / target).is_file()
    if target.endswith('index.html'):
        target = posixpath.dirname(target) + '/'
        directory = True
    elif directory and target and not target.endswith('/'):
        target += '/'
    start = page_dir(page_rel) or '.'
    dest = target.rstrip('/') or '.'
    rel = posixpath.relpath(dest, start)
    if directory:
        if rel in ('.', ''):
            return './'
        if not rel.endswith('/'):
            rel += '/'
    return rel


def browser_inner(page_rel: str, url_path: str):
    """Return (site-relative path, escaped_project)."""
    directory = page_dir(page_rel)
    page = PROJECT + (directory + '/' if directory else '')
    absu = urljoin(page, url_path)
    path = urlsplit(absu).path
    root = '/abadis-med-redesign-live/'
    if path == '/abadis-med-redesign-live' or path.startswith(root):
        inner = '' if path == '/abadis-med-redesign-live' else path[len(root):]
        return inner, False
    return path.lstrip('/'), True


def retarget(page_rel: str, url: str) -> str:
    """Point a local URL at a file that exists, with a relative path that stays inside the project."""
    if not url or url.startswith(SKIP_URL):
        return url
    path, query, frag = url, '', ''
    if '#' in path:
        path, frag = path.split('#', 1)
    if '?' in path:
        path, query = path.split('?', 1)
    if not path or path.startswith(SKIP_URL):
        return url
    inner, escaped = browser_inner(page_rel, path)
    inner_norm = posixpath.normpath(inner) if inner not in ('', '.') else ''
    if inner_norm.startswith('..'):
        inner_norm = ''
    ok = exists(inner_norm if inner else '')
    target = inner if ok else None
    if target is None:
        # Written as a site-root path from a nested page (forgot the ../ prefix).
        bare = path.lstrip('./')
        if bare and not bare.startswith('/') and exists(posixpath.normpath(bare)):
            target = posixpath.normpath(bare)
            if exists(target) and (SITE / target).is_dir():
                target = target.rstrip('/') + '/'
            elif exists(target + '/'):
                target = target.rstrip('/') + '/'
    elif (not (SITE / (target.rstrip('/') or '.')).is_file()) and exists(target.rstrip('/') + '/'):
        if not target.endswith('/'):
            target += '/'
    if target is None:
        return url
    # Already correct and inside the project.
    if ok and not escaped and not path.startswith('/'):
        # Normalise only the fragile media/../img form elsewhere.
        return url
    new = to_relative(page_rel, target if target != '/' else '')
    if query:
        new += '?' + query
    if frag:
        new += '#' + frag
    return new


def rewrite_attrs(page_rel: str, text: str) -> str:
    def sub(m):
        url = m.group('url')
        new = retarget(page_rel, url)
        if new == url:
            return m.group(0)
        return f'{m.group("attr")}={m.group("q")}{new}{m.group("q")}'
    return ATTR_RE.sub(sub, text)


def rewrite_srcset(page_rel: str, text: str) -> str:
    def sub(m):
        q, body = m.group(1), m.group(2)
        parts = []
        for piece in body.split(','):
            bit = piece.strip()
            if not bit:
                continue
            bits = bit.split()
            bits[0] = retarget(page_rel, bits[0])
            parts.append(' '.join(bits))
        return f'srcset={q}{", ".join(parts)}{q}'
    return re.sub(r'srcset=(["\'])(.*?)(\1)', lambda m: sub(m) if False else _srcset(page_rel, m), text)


def _srcset(page_rel, m):
    q, body = m.group(1), m.group(2)
    parts = []
    for piece in body.split(','):
        bit = piece.strip()
        if not bit:
            continue
        bits = bit.split()
        bits[0] = retarget(page_rel, bits[0])
        parts.append(' '.join(bits))
    return f'srcset={q}{", ".join(parts)}{q}'


def rewrite_css_urls(page_rel: str, text: str) -> str:
    def sub(m):
        raw = m.group(1).strip('\'"')
        new = retarget(page_rel, raw)
        if new == raw:
            return m.group(0)
        return f'url("{new}")'
    return re.sub(r'url\(\s*([^)]+?)\s*\)', sub, text)


def github_to_relative(page_rel: str, text: str) -> str:
    def sub(m):
        url = m.group(2)
        for root in GH_ROOTS:
            if url.startswith(root):
                rest = url[len(root):]
                if rest.startswith('assets/') or rest.endswith(('.woff2', '.css', '.js', '.png', '.jpg', '.webp')):
                    return m.group(0)
                target = rest if rest else ''
                if target and not exists(target.rstrip('/')) and not exists(target):
                    return m.group(0)
                new = to_relative(page_rel, target)
                return f'{m.group(1)}{new}{m.group(3)}'
        return m.group(0)
    return re.sub(r'(href=")(https?://[^"]+)(")', sub, text)


def inject_cert_thumbs(text: str) -> str:
    def sub(m):
        url, w, h = m.group(1), m.group(2), m.group(3)
        if not CERT_URL.search(url):
            return m.group(0)
        tail = text[m.end():m.end() + 600]
        label = ''
        for bit in re.findall(r'>([^<]{1,80})<', tail):
            bit = bit.strip()
            if bit:
                label = bit
                break
        alt = html_lib.escape(label, quote=True)
        src = html_lib.escape(url, quote=True)
        return (
            f'<div data-thumbnail="{src}" data-width="{w}" data-height="{h}" alt="">'
            f'<img src="{src}" width="{w}" height="{h}" alt="{alt}" loading="lazy" decoding="async" '
            f'style="max-width:100%;height:auto">'
            f'</div>'
        )
    return THUMB_RE.sub(sub, text)


def strip_corrupt_dotdot(text: str) -> str:
    if not re.search(r'content="(?:\.\./)+width=', text):
        return text
    return re.sub(
        r'content="(?:\.\./)+(?!assets/|favicon|shared/|csr/|img/|fonts/|common/)',
        'content="',
        text,
    )


def ensure_head(rel: str, text: str) -> str:
    path = site_path_of(rel)
    text = re.sub(r'[ \t]*<!-- TODO\(launch\):.*?-->\n?', '', text)
    text = re.sub(r'[ \t]*<meta name="robots" content="[^"]*"\s*/?>\n?', '', text)
    text = re.sub(r'[ \t]*<link rel="canonical" href="[^"]*"\s*/?>\n?', '', text)
    text = re.sub(r'[ \t]*<link rel="alternate" hreflang="[^"]*" href="[^"]*"\s*/?>\n?', '', text)
    title_m = re.search(r'<title>(.*?)</title>', text, re.S)
    title = re.sub(r'\s+', ' ', title_m.group(1)).strip() if title_m else ''
    h1s = re.findall(r'<h1\b[^>]*>(.*?)</h1>', text, re.S)
    h1_text = re.sub(r'<[^>]+>', '', h1s[0]).strip() if h1s else ''
    if not re.search(r'<meta name="description" content="[^"]*"', text):
        desc = h1_text or title
        if desc:
            meta = f'<meta name="description" content="{html_lib.escape(desc, quote=True)}">\n'
            if re.search(r'</title>', text):
                text = re.sub(r'(</title>\n?)', r'\1' + meta, text, count=1)
            else:
                text = text.replace('</head>', meta + '</head>', 1)
    links = hreflang_links(path)
    alt = ('\n'.join(f'<link rel="alternate" hreflang="{hl}" href="{href}">' for hl, href in links) + '\n') if links else ''
    block = ROBOTS_META + '\n' + f'<link rel="canonical" href="{canonical_href(path)}">\n' + alt
    # Accept both <meta ...> and <meta ... /> (design prototypes use the latter).
    if re.search(r'<meta name="description"', text):
        text = re.sub(r'(<meta name="description" content="[^"]*"\s*/?>\n?)', r'\1' + block, text, count=1)
    elif re.search(r'<meta name="viewport"', text):
        text = re.sub(r'(<meta name="viewport"[^>]*>\n?)', r'\1' + block, text, count=1)
    else:
        text = text.replace('</head>', block + '</head>', 1)
    if not re.search(r'<h1\b', text) and title:
        hidden = (
            '<h1 style="position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;'
            f'clip:rect(0,0,0,0);white-space:nowrap;border:0">{html_lib.escape(title)}</h1>\n'
        )
        text = re.sub(r'(<body\b[^>]*>\n?)', r'\1' + hidden, text, count=1)
    return text


def patch_html(rel: str, text: str) -> str:
    text = strip_corrupt_dotdot(text)
    text = text.replace('assets/media/../img/', 'assets/img/')
    text = text.replace('arabic/../csr/', 'csr/')
    if rel == 'index.html':
        text = text.replace('href="../contact/"', 'href="contact/"')
        text = text.replace('class="lang-link" href=""', 'class="lang-link" href="./"')
    if rel == 'en/index.html':
        text = text.replace(
            'https://www.abadis-med.com/en/wp-content/uploads/2022/04/Imed-Certificate-scaled.jpg',
            '../assets/img/certs/cert-imed.webp',
        )
        text = text.replace(
            'https://www.abadis-med.com/en/wp-content/uploads/2022/05/ISO-scaled-1.jpg',
            '../assets/img/c/19ffe783abd3-1600.webp',
        )
        text = text.replace(
            'https://www.abadis-med.com/en/wp-content/uploads/2022/05/CE-scaled-1.jpg',
            '../assets/img/certs/cert-ce.webp',
        )
    text = github_to_relative(rel, text)
    text = rewrite_attrs(rel, text)
    text = rewrite_srcset(rel, text)
    text = rewrite_css_urls(rel, text)
    if rel in ('en/about-us/index.html', 'arabic/من-نحن/index.html'):
        text = inject_cert_thumbs(text)
    text = ensure_head(rel, text)
    return text


def patch_all():
    n = 0
    for f in SITE.rglob('*.html'):
        rel = f.relative_to(SITE).as_posix()
        old = f.read_text(encoding='utf-8')
        new = patch_html(rel, old)
        if new != old:
            f.write_text(new, encoding='utf-8')
            n += 1
    print(f'patched {n} html files')


# ---------------------------------------------------------------- redirects
# Old WordPress page path (decoded, trailing slash) -> new site path.
# PAGE_MAP is the source; fragments are dropped so the target is a real page.


def _final(site_path: str) -> str:
    return canonical_href(site_path.split('#', 1)[0])


def _norm_old(url: str) -> str:
    parts = urlsplit(url.strip())
    path = unquote(parts.path or '/')
    if not path.endswith('/') and '.' not in path.rsplit('/', 1)[-1]:
        path += '/'
    return path


SECTION_FOR_IMAGE = [
    ('کیسه', 'products/suction-bag/'),
    ('ساکشن', 'products/suction-bag/'),
    ('suction', 'products/suction-bag/'),
    ('liner', 'products/suction-bag/'),
    ('فیلتر', 'products/filters/'),
    ('filter', 'products/filters/'),
    ('پایه', 'products/stand/'),
    ('holder', 'products/stand/'),
    ('مخزن', 'products/canister/'),
    ('canister', 'products/canister/'),
    ('اتصال', 'products/connectors/'),
    ('connector', 'products/connectors/'),
    ('تیوب', 'products/suction-tube/'),
    ('tube', 'products/suction-tube/'),
    ('کاتالوگ', 'downloads/'),
    ('catalog', 'downloads/'),
    ('نمایند', 'dealers/'),
    ('گواه', 'about/'),
    ('cert', 'about/'),
    ('iso', 'about/'),
    ('imed', 'about/'),
]


def _image_index():
    """basename (lower) and converted-webp hash -> site paths that mention them."""
    idx = {}
    hashes = {}
    for f in SITE.rglob('*.html'):
        rel = f.relative_to(SITE).as_posix()
        if rel.startswith(('dial-', 'template-dials/', 'hero-options/', 'hero-test/', 'zagros-names/')):
            continue
        text = f.read_text(encoding='utf-8', errors='replace').lower()
        path = site_path_of(rel)
        for name in set(re.findall(r'[\w\u0600-\u06ff.%+-]{3,}\.(?:jpe?g|png|webp|gif)', text, re.I)):
            idx.setdefault(unquote(name).lower(), set()).add(path)
        for stem in set(re.findall(r'/([0-9a-f]{12})-\d+\.webp', text)):
            hashes.setdefault(stem, set()).add(path)
    return idx, hashes


def _pick_page(found) -> str:
    """Prefer a Persian section page, then the shortest path that actually uses the file."""
    fa = [p for p in found if not p.startswith(('en/', 'arabic/'))]
    pool = fa or list(found)
    sections = [p for p in pool if p.count('/') <= 2 and not p.startswith(('en/', 'arabic/'))]
    use = sections or pool
    return sorted(use, key=lambda p: (p.count('/'), len(p), p))[0]


def _hash_pages(old_path: str, hashes) -> set:
    found = set()
    variants = {old_path, re.sub(r'-\d+x\d+(?=\.\w+$)', '', old_path)}
    for variant in variants:
        stem = hashlib.sha1(variant.encode()).hexdigest()[:12]
        found |= hashes.get(stem, set())
    return found


def _nearest_page(old_path: str, index, hashes) -> str:
    hit = PAGE_MAP.get(old_path)
    if hit is None:
        bare = old_path.rstrip('/') or '/'
        hit = PAGE_MAP.get(bare + '/' if bare != '/' else '/')
        if hit is None:
            hit = PAGE_MAP.get(bare)
    if hit is not None:
        return hit.split('#', 1)[0]
    by_hash = _hash_pages(old_path, hashes)
    if by_hash:
        return _pick_page(by_hash)
    low = unquote(old_path).lower()
    for needle, dest in SECTION_FOR_IMAGE:
        if needle in low:
            return dest
    name = unquote(old_path.rsplit('/', 1)[-1]).lower()
    # also the unsized original: photo-300x200.jpg -> photo.jpg
    names = {name, re.sub(r'-\d+x\d+(?=\.\w+$)', '', name)}
    found = set()
    for n in names:
        found |= index.get(n, set())
    # About galleries list many unrelated upload names; don't treat that as the destination.
    found -= {'about/', 'en/about-us/', 'arabic/من-نحن/'}
    if found:
        return _pick_page(found)
    return ''


def write_redirects():
    src = ROOT / 'page-urls.txt'
    lines = [ln.strip() for ln in src.read_text(encoding='utf-8').splitlines() if ln.strip()]
    index, hashes = _image_index()
    rows = []
    seen = set()
    for raw in lines:
        if raw in seen:
            continue
        seen.add(raw)
        old_path = _norm_old(raw)
        new_path = _nearest_page(old_path, index, hashes)
        new_url = _final(new_path)
        # Compare decoded paths so a self-map is not emitted as a 301 (that would loop).
        old_final = SITE_ORIGIN + old_path
        same = unquote(old_final.rstrip('/')) == unquote(new_url.rstrip('/'))
        rows.append((raw, new_url, 'none' if same else '301'))
    # Chains: a 301 target must not itself be an old URL that 301s somewhere else.
    redirecting = {unquote(_norm_old(o)): n for o, n, status in rows if status == '301'}
    for old, new, status in rows:
        if status != '301':
            continue
        nxt = unquote(urlsplit(new).path or '/')
        if not nxt.endswith('/') and '.' not in nxt.rsplit('/', 1)[-1]:
            nxt += '/'
        if nxt in redirecting and redirecting[nxt].rstrip('/') != new.rstrip('/'):
            raise SystemExit(f'redirect chain: {old} -> {new} -> {redirecting[nxt]}')
    out = ROOT / 'docs' / 'redirects-301.csv'
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open('w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(['old_url', 'new_url', 'redirect'])
        w.writerows(rows)
    n301 = sum(1 for *_, s in rows if s == '301')
    print(f'redirects {len(rows)} rows, {n301} 301, {len(rows) - n301} unchanged')


def main():
    patch_all()
    from discovery import write_sitemap_and_robots
    write_sitemap_and_robots()
    write_redirects()


if __name__ == '__main__':
    main()
