"""Real pages for live WordPress archives that were redirect stubs.

Tags, categories, authors, customers, dealers, provinces, the download centre,
menu templates and the job-ad archive list the same items as abadis-med.com.
Old job-ad posts, the FA waste-bag category, /en/catalogue/ and
/en/reservoir-calculator/ are real pages too. True duplicates stay 301s.

    python3 tools/redesign/pages_archives.py [--refresh]

Reads tools/redesign/data/wp_archives.json (fetched from the WP REST API and the
live listing HTML). Rewrites url_aliases.json so url_migrate will not put the
stubs back, then regenerates the 301 map.
"""
import html as htmlmod
import json
import math
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import DATA, SITE, esc, fa, jdate, best_img
from layout import page, page_hero
from i18n import canonical_href

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = DATA / 'wp_archives.json'
CHECKLIST = os.environ.get(
    'ABADIS_URL_CHECKLIST',
    '/tmp/url-audit/url-audit/url-checklist-fa.csv',
)
PER = 10
UA = 'AbadisRedesign/1.0'
CSS = 'assets/css/archives.css?v=20261115a'
FALLBACK = 'assets/img/post-thumb-fallback.webp'

BASES = {
    'fa': 'http://abadis-med.com/wp-json/wp/v2',
    'en': 'http://abadis-med.com/en/wp-json/wp/v2',
    'ar': 'http://abadis-med.com/arabic/wp-json/wp/v2',
}

UI = {
    'fa': dict(
        prev='قبلی', next='بعدی', page='صفحه', pager='صفحه‌بندی',
        more='ادامه', empty='', articles='مقالات', news='آخرین اخبار',
        customers='مشتریان', dealers='نمایندگان', downloads='مرکز دانلود',
        jobs='موقعیت‌های شغلی', products='محصولات',
        tag='برچسب', category='دسته', author='نویسنده', province='استان نمایندگی',
    ),
    'en': dict(
        prev='Previous', next='Next', page='Page', pager='Pagination',
        more='Read', empty='', articles='Articles', news='News',
        customers='Customers', dealers='Representatives', downloads='Download Center',
        jobs='Jobs', products='Products',
        tag='Tag', category='Category', author='Author', province='Province',
    ),
    'ar': dict(
        prev='السابق', next='التالي', page='صفحة', pager='ترقيم الصفحات',
        more='متابعة', empty='', articles='المقالات', news='الاخبار',
        customers='العملاء', dealers='الممثلون', downloads='مركز التنزيل',
        jobs='الوظائف', products='المنتجات',
        tag='وسم', category='تصنيف', author='الكاتب', province='المحافظة',
    ),
}

# Live H1 patterns. Descriptions come from WordPress, never invented.
H1 = {
    ('tag', 'fa'): lambda n: f'برچسب: {n}',
    ('tag', 'en'): lambda n: n,
    ('tag', 'ar'): lambda n: n,
    ('category', 'fa'): lambda n: f'دسته: {n}',
    ('category', 'en'): lambda n: n,
    ('category', 'ar'): lambda n: n,
    ('author', 'fa'): lambda n: f'نویسنده: {n}',
    ('author', 'en'): lambda n: f'Author: {n}',
    ('author', 'ar'): lambda n: f'الكاتب: {n}',
    ('customer-archive', 'fa'): lambda n: 'بایگانی‌ها: مشتریان',
    ('dealer-archive', 'fa'): lambda n: 'بایگانی‌ها: نمایندگان',
    ('dealer-archive', 'en'): lambda n: 'Archives: representatives',
    ('download-archive', 'fa'): lambda n: 'بایگانی‌ها: مرکز دانلود',
    ('job-archive', 'fa'): lambda n: 'بایگانی‌ها: موقعیت های شغلی',
    ('province', 'fa'): lambda n: f'استان نمایندگی : {n}',
}


def num(lang, n):
    return fa(n) if lang == 'fa' else str(n)


def unq(s):
    return urllib.parse.unquote(s or '')


def path_of(link):
    p = unq(urllib.parse.urlsplit(link or '').path) or '/'
    if not p.endswith('/'):
        p += '/'
    return p


def lang_of(path):
    if path.startswith('/en/'):
        return 'en'
    if path.startswith('/arabic/'):
        return 'ar'
    return 'fa'


def rel_link(from_dir, to_path):
    """from_dir and to_path are site paths. to_path may include a #fragment."""
    to_path = unq(to_path)
    frag = ''
    if '#' in to_path:
        to_path, frag = to_path.split('#', 1)
        frag = '#' + frag
    if not to_path.startswith('/'):
        to_path = '/' + to_path
    trailing = to_path.endswith('/')
    src = from_dir.strip('/')
    dst = to_path.strip('/')
    rel = dst if not src else os.path.relpath(dst or '.', src)
    if rel in ('.', ''):
        rel = './' if trailing else '.'
    elif trailing:
        rel += '/'
    return rel + frag


def http_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r), r.headers


def paged(url, fields):
    out, page_n = [], 1
    while page_n < 40:
        sep = '&' if '?' in url else '?'
        u = f'{url}{sep}per_page=100&page={page_n}'
        if fields:
            u += '&_fields=' + fields
        try:
            data, headers = http_json(u)
        except urllib.error.HTTPError as e:
            if e.code == 400 and page_n > 1:
                break
            raise
        if not isinstance(data, list):
            break
        out.extend(data)
        total = int(headers.get('X-WP-TotalPages') or 1)
        if page_n >= total or not data:
            break
        page_n += 1
    return out


def http_text(url):
    parts = urllib.parse.urlsplit(url)
    path = urllib.parse.quote(unq(parts.path), safe='/%')
    url = urllib.parse.urlunsplit((parts.scheme, parts.netloc, path, parts.query, ''))
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 ' + UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.status, unq(r.geturl()), r.read().decode('utf-8', 'replace')


def rendered(obj, key='rendered'):
    v = obj.get(key) if isinstance(obj, dict) else obj
    if isinstance(v, dict):
        v = v.get('rendered') or ''
    return htmlmod.unescape(re.sub(r'<[^>]+>', '', v or '')).strip()


def qtrans(s, lang):
    """Keep one language from a qTranslate string. Empty if that language is empty."""
    s = s or ''
    if '[:' not in s:
        return s
    parts = re.findall(r'\[:([a-z]{2}|[a-z]{2}_[A-Z]{2})\](.*?)(?=\[:)', s, flags=re.S)
    want = {'fa': 'fa', 'en': 'en', 'ar': 'ar'}.get(lang, lang)
    for code, text in parts:
        if code.startswith(want) and text.strip():
            return text.strip()
    return ''


def plain(s):
    s = re.sub(r'<[^>]+>', ' ', s or '')
    return re.sub(r'\s+', ' ', htmlmod.unescape(s)).strip()


def clip(s, n=190):
    s = plain(s)
    return s[:n] + ('…' if len(s) > n else '')


def html_lines(raw):
    s = re.sub(r'<style[\s\S]*?</style>', ' ', raw or '', flags=re.I)
    s = re.sub(r'<script[\s\S]*?</script>', ' ', s, flags=re.I)
    s = re.sub(r'<br\s*/?>', '\n', s, flags=re.I)
    s = re.sub(r'</(p|div|li|h[1-6]|tr)>', '\n', s, flags=re.I)

    def alink(m):
        href = htmlmod.unescape(m.group(1))
        text = plain(m.group(2))
        if not text or href.startswith(('javascript:', '#')):
            return text
        return f'\n[[A|{href}|{text}]]\n'

    s = re.sub(r'<a [^>]*href="([^"]+)"[^>]*>(.*?)</a>', alink, s, flags=re.S)
    s = re.sub(r'<[^>]+>', '', s)
    s = htmlmod.unescape(s)
    lines = []
    for line in s.splitlines():
        line = re.sub(r'\s+', ' ', line).strip()
        if not line or line.startswith('/*!') or 'elementor-' in line:
            continue
        lines.append(line)
    return lines


def lines_to_html(lines, skip_title=''):
    bits = []
    for line in lines:
        if skip_title and line == skip_title and not bits:
            continue
        m = re.fullmatch(r'\[\[A\|([^|\]]+)\|([^\]]*)\]\]', line)
        if m:
            href, text = m.group(1), m.group(2) or m.group(1)
            bits.append(f'<p><a href="{esc(href)}">{esc(text)}</a></p>')
        else:
            bits.append(f'<p>{esc(line)}</p>')
    return '\n'.join(bits)


def scrape_listing(start):
    """Follow a live Elementor post loop. Returns [{path, title}] in live order."""
    items, seen, url, guard = [], set(), start, 0
    while url and guard < 40:
        guard += 1
        try:
            status, final, text = http_text(url)
        except Exception as e:
            print('  scrape fail', url, e)
            break
        if status != 200:
            break
        found = re.findall(
            r'<h3 class="elementor-post__title">\s*<a href="([^"]+)"[^>]*>(.*?)</a>',
            text, re.S)
        if not found:
            break
        new = 0
        for href, title in found:
            path = path_of(href)
            if path in seen:
                continue
            seen.add(path)
            items.append({'path': path, 'title': plain(title)})
            new += 1
        if not new:
            break
        nxt = re.search(r'<a class="page-numbers next" href="([^"]+)"', text)
        url = htmlmod.unescape(nxt.group(1)) if nxt else ''
    return items


def fetch():
    print('fetching WordPress archives…')
    data = {'tax': {}, 'posts': {}, 'cpt': {}, 'media': {}, 'listings': {}, 'jobs': []}
    for lang, base in BASES.items():
        print(' ', lang)
        data['tax'][lang] = {
            'tags': paged(base + '/tags', 'id,name,slug,description,count,link'),
            'categories': paged(base + '/categories', 'id,name,slug,description,count,link'),
            'users': paged(base + '/users', 'id,name,slug,description,link'),
        }
        data['posts'][lang] = paged(
            base + '/posts?orderby=date&order=desc',
            'id,slug,link,title,date,excerpt,tags,categories,author')
        cpt = {}
        if lang == 'fa':
            for rest in ('_customers', '_franchise', '_downloadcenter', '_joboffers', 'jet-menu'):
                cpt[rest] = paged(base + '/' + rest, 'id,slug,link,title,date,content,featured_media,_citynmg')
            cpt['_citynmg'] = paged(base + '/_citynmg', 'id,name,slug,description,count,link')
        elif lang == 'en':
            cpt['jet-menu'] = paged(base + '/jet-menu', 'id,slug,link,title,date')
            cpt['representatives_01'] = paged(base + '/representatives_01', 'id,slug,link,title,date,content')
        else:
            cpt['jet-menu'] = paged(base + '/jet-menu', 'id,slug,link,title,date')
        data['cpt'][lang] = cpt
    # featured images for FA customers and downloads
    ids = []
    for row in data['cpt']['fa'].get('_customers', []) + data['cpt']['fa'].get('_downloadcenter', []):
        if row.get('featured_media'):
            ids.append(str(row['featured_media']))
    ids = sorted(set(ids))
    media = {}
    for i in range(0, len(ids), 50):
        chunk = ','.join(ids[i:i + 50])
        for row in paged(BASES['fa'] + '/media?include=' + chunk, 'id,source_url'):
            media[str(row['id'])] = row.get('source_url') or ''
    data['media'] = media
    # old job-ad posts (root slugs, not the _joboffers CPT)
    slugs = [
        'مدیر-فروش', 'نیروی-فنی', 'کارشناس-تحقیقات-بازار', 'کارشناس-حسابداری',
        'کارشناس-صادرات', 'کارشناس-فروش-2', 'کارشناس-فروش', 'کارمند-وصول-مطالبات',
    ]
    for slug in slugs:
        rows, _ = http_json(BASES['fa'] + '/posts?slug=' + urllib.parse.quote(slug) + '&_fields=slug,link,title,content,excerpt,date')
        if rows:
            data['jobs'].append(rows[0])
    # paginated post indexes (live /مقالات/2/ style)
    for key, url in (
        ('fa-articles', 'http://abadis-med.com/مقالات/'),
        ('fa-news', 'http://abadis-med.com/آخرین-اخبار/'),
        ('en-articles', 'http://abadis-med.com/en/blog/'),
        ('en-news', 'http://abadis-med.com/en/latest-news/'),
        ('ar-articles', 'http://abadis-med.com/arabic/articles/'),
        ('ar-news', 'http://abadis-med.com/arabic/الاخبار/'),
    ):
        print('  listing', key)
        items = scrape_listing(url)
        data['listings'][key] = items
        print('   ', len(items))
    json.dump(data, open(CACHE, 'w', encoding='utf-8'), ensure_ascii=False)
    print('cached', CACHE)
    return data


def load_cache():
    if '--refresh' in sys.argv or not CACHE.is_file():
        return fetch()
    return json.load(open(CACHE, encoding='utf-8'))


def checklist_rows():
    import csv
    rows = []
    if not os.path.isfile(CHECKLIST):
        return rows
    with open(CHECKLIST, newline='', encoding='utf-8-sig') as f:
        for r in csv.DictReader(f):
            url = r['آدرس در abadis-med.com']
            path = path_of(url)
            rows.append((path, r['وضعیت'], r['صفحه'], r['زبان']))
    return rows


def index_posts(rows):
    by_tag, by_cat, by_author = {}, {}, {}
    for row in rows:
        item = {
            'path': path_of(row.get('link') or ''),
            'title': rendered(row.get('title') or {}),
            'date': row.get('date') or '',
            'excerpt': (row.get('excerpt') or {}).get('rendered') or '',
        }
        for tid in row.get('tags') or []:
            by_tag.setdefault(tid, []).append(item)
        for cid in row.get('categories') or []:
            by_cat.setdefault(cid, []).append(item)
        by_author.setdefault(row.get('author'), []).append(item)
    return by_tag, by_cat, by_author


def local_images():
    """Post path -> featured image URL, when the source post has one."""
    out = {}
    pj = DATA / 'posts.json'
    if pj.is_file():
        for p in json.load(open(pj, encoding='utf-8')):
            path = path_of(p.get('path') or p.get('url') or '')
            img = p.get('image') or ''
            if img:
                out[path] = img
    ej = DATA / 'en_posts.json'
    if ej.is_file():
        for p in json.load(open(ej, encoding='utf-8')):
            og = ((p.get('yoast_head_json') or {}).get('og_image') or [])
            url = og[0].get('url') if og else ''
            path = path_of(p.get('link') or '')
            if path and url:
                out[path] = url
    aj = DATA / 'ar_featured.json'
    if aj.is_file():
        for path, url in json.load(open(aj, encoding='utf-8')).items():
            if url:
                out[path_of(path)] = url
    extra = DATA / 'en_extra_featured.json'
    if extra.is_file():
        for path, url in json.load(open(extra, encoding='utf-8')).items():
            if url and path_of(path) not in out:
                out[path_of(path)] = url
    return out


def existing_dirs():
    out = set()
    for dp, dns, fns in os.walk(SITE):
        if 'index.html' in fns:
            rel = os.path.relpath(dp, SITE)
            out.add('/' if rel == '.' else '/' + rel.replace(os.sep, '/') + '/')
    return out


DEALERS = None


def dealer_rows():
    global DEALERS
    if DEALERS is None:
        raw = json.load(open(DATA / 'dealers.json', encoding='utf-8'))
        DEALERS = raw.get('groups') or []
    return DEALERS


def norm_name(s):
    return re.sub(r'[\s\u200c\u200b]+', '', s or '')


def contact_for(province, name):
    pn, nn = norm_name(province), norm_name(name)
    for g in dealer_rows():
        if pn and norm_name(g.get('province')) != pn and pn not in norm_name(g.get('title') or ''):
            continue
        for d in g.get('dealers') or []:
            dn = norm_name(d.get('name'))
            if dn and (dn == nn or dn in nn or nn in dn):
                return d.get('rows') or []
    return []


class Builder:
    def __init__(self, data, write):
        self.data = data
        self.write = write
        self.have = existing_dirs()
        self.images = local_images()
        self.stats = []  # (kind, lang, path)
        self.failed = []
        self.written = set()
        self.indexes = {}
        for lang, rows in data['posts'].items():
            self.indexes[lang] = index_posts(rows)
        self.by_path = {}
        for lang, group in data['cpt'].items():
            for kind, rows in group.items():
                if kind == '_citynmg':
                    continue
                for row in rows:
                    self.by_path[path_of(row.get('link') or '')] = (lang, kind, row)

    def emit(self, site_path, lang, title, desc, main, kind, cur=''):
        site_path = site_path if site_path.endswith('/') else site_path + '/'
        depth = len([p for p in site_path.strip('/').split('/') if p])
        prefix = '../' * depth if depth else './'
        # hreflang is filled by the caller via extra, here self only; alternates added in head_extra
        extra = self.head_extra(site_path, lang, prefix)
        html = page(
            prefix, cur, title, desc or title, main,
            lang=lang, fa_path='', canonical_path=site_path.lstrip('/'),
            extra_head=extra,
        )
        rel = site_path.strip('/') + '/index.html'
        from seo_postprocess import jsonld
        import url_migrate
        html = jsonld(html, rel)
        # layout still emits the pre-migration folders (about/, articles/). Map them
        # to the live slugs the rest of the site already uses.
        html = url_migrate.rewrite_html(html, site_path, site_path)
        self.write(rel, html)
        self.have.add(site_path)
        self.written.add(site_path)
        self.stats.append((kind, lang, site_path))

    def head_extra(self, site_path, lang, prefix):
        code = {'fa': 'fa-IR', 'en': 'en', 'ar': 'ar'}[lang]
        href = canonical_href(site_path)
        alts = [(code, href)]
        for other, opath in self.alternates(site_path, lang):
            alts.append(({'fa': 'fa-IR', 'en': 'en', 'ar': 'ar'}[other], canonical_href(opath)))
        # x-default: FA when that alternate exists, otherwise this page
        xd = href
        for c, h in alts:
            if c == 'fa-IR':
                xd = h
                break
        lines = [f'<link rel="alternate" hreflang="{c}" href="{h}">' for c, h in alts]
        lines.append(f'<link rel="alternate" hreflang="x-default" href="{xd}">')
        css = prefix + CSS
        return '<link rel="stylesheet" href="%s">\n%s\n' % (css, '\n'.join(lines))

    def alternates(self, site_path, lang):
        """Same author slug in another language. Nothing else is a real translation."""
        m = re.match(r'^(/en|/arabic)?/author/([^/]+)/$', site_path)
        if not m:
            return []
        slug = m.group(2)
        out = []
        for other, rows in self.data['tax'].items():
            if other == lang:
                continue
            for u in rows.get('users') or []:
                if unq(u.get('slug') or '') == slug or unq(path_of(u.get('link') or '')).rstrip('/').endswith('/' + slug):
                    out.append((other, path_of(u.get('link') or '')))
                    break
        return out

    def card(self, from_dir, item, lang, img=None):
        ui = UI[lang]
        title = item.get('title') or ''
        href = item.get('path') or item.get('href') or ''
        if href and not href.startswith('http'):
            href = rel_link(from_dir, href)
        meta = ''
        if item.get('date'):
            shown = jdate(item['date']) if lang == 'fa' else item['date'][:10]
            meta = f'<time datetime="{esc(item["date"][:10])}">{esc(shown)}</time>'
        excerpt = clip(item.get('excerpt') or '')
        ph = ''
        src = img or self.images.get(item.get('path') or '')
        asset = src[1:] if src and src.startswith('/assets/') else src
        if asset and asset.startswith('assets/'):
            fp = SITE / asset.split('?', 1)[0]
            dim = ''
            if fp.is_file():
                try:
                    from PIL import Image
                    with Image.open(fp) as im:
                        dim = f' width="{im.size[0]}" height="{im.size[1]}"'
                except OSError:
                    dim = ''
            ph = (f'<div class="ph"><img src="{esc(rel_link(from_dir, "/" + asset))}"{dim} '
                  f'alt="{esc(title)}" loading="lazy" decoding="async"></div>')
        else:
            local = best_img(src, 640) if src else None
            if local:
                ph = (f'<div class="ph"><img src="{esc(rel_link(from_dir, "/" + local["src"]))}" '
                      f'width="{local["w"]}" height="{local["h"]}" alt="{esc(title)}" loading="lazy" decoding="async"></div>')
            elif src and str(src).startswith('http'):
                ph = (f'<div class="ph"><img src="{esc(src)}" alt="{esc(title)}" loading="lazy" decoding="async"></div>')
            elif (SITE / FALLBACK).is_file():
                ph = (f'<div class="ph txt"><img src="{esc(rel_link(from_dir, "/" + FALLBACK))}" '
                      f'width="1280" height="720" alt="{esc(title)}" loading="lazy" decoding="async"></div>')
        body = f'<div class="body">{meta}<h3>{esc(title)}</h3>'
        if excerpt:
            body += f'<p>{esc(excerpt)}</p>'
        rows = item.get('rows') or []
        if rows:
            lis = ''.join(f'<li>{esc(a)}: {esc(b)}</li>' for a, b in rows)
            body += f'<ul class="arch-rows">{lis}</ul>'
        body += f'<span class="go">{esc(ui["more"])}</span></div>'
        return f'<a class="post-card reveal" href="{esc(href)}">{ph}{body}</a>'

    def pager(self, from_dir, base, page_n, pages, lang):
        if pages <= 1:
            return ''
        ui = UI[lang]
        bits = []
        def href(n):
            path = base if n == 1 else (base.rstrip('/') + f'/page/{n}/')
            return rel_link(from_dir, path)
        if page_n > 1:
            bits.append(f'<a href="{esc(href(page_n - 1))}">{esc(ui["prev"])}</a>')
        for n in range(1, pages + 1):
            label = num(lang, n)
            if n == page_n:
                bits.append(f'<span class="is-current" aria-current="page">{label}</span>')
            else:
                bits.append(f'<a href="{esc(href(n))}">{label}</a>')
        if page_n < pages:
            bits.append(f'<a href="{esc(href(page_n + 1))}">{esc(ui["next"])}</a>')
        return f'<nav class="arch-pager" aria-label="{esc(ui["pager"])}">{"".join(bits)}</nav>'

    def listing(self, base, lang, h1, desc, items, kind, crumb, cur=''):
        """crumb items are (label, absolute site path or None)."""
        pages = max(1, math.ceil(len(items) / PER)) or 1
        ui = UI[lang]
        for n in range(1, pages + 1):
            path = base if n == 1 else base.rstrip('/') + f'/page/{n}/'
            chunk = items[(n - 1) * PER:n * PER]
            cards = ''.join(self.card(path, it, lang, it.get('img')) for it in chunk)
            meta = f'<p class="arch-note">{esc(ui["page"])} {num(lang, n)}</p>' if n > 1 else ''
            trail = []
            for label, target in crumb:
                if target is None:
                    trail.append((label, None if n == 1 else rel_link(path, base)))
                else:
                    trail.append((label, rel_link(path, target)))
            if n > 1:
                trail.append((f'{ui["page"]} {num(lang, n)}', None))
            main = f'''{page_hero(self.prefix(path), trail, esc(h1), esc(desc) if desc else '', meta, lang=lang)}
  <section class="section"><div class="wrap"><div class="post-grid">{cards}</div>
  {self.pager(path, base, n, pages, lang)}</div></section>'''
            page_kind = kind if n == 1 else 'pagination'
            self.emit(path, lang, h1, desc or h1, main, page_kind, cur=cur)

    def prefix(self, site_path):
        depth = len([p for p in site_path.strip('/').split('/') if p])
        return '../' * depth if depth else './'

    def section_href(self, lang, which):
        cands = {
            ('fa', 'articles'): '/مقالات/',
            ('fa', 'news'): '/آخرین-اخبار/',
            ('en', 'articles'): '/en/blog/',
            ('en', 'news'): '/en/latest-news/',
            ('ar', 'articles'): '/arabic/articles/',
            ('ar', 'news'): '/arabic/الاخبار/',
            ('fa', 'customers'): '/مشتریان-ما/',
            ('fa', 'dealers'): '/لیست-نمایندگان/',
            ('en', 'dealers'): '/en/representatives/',
            ('fa', 'downloads'): '/کاتالوگ/',
            ('fa', 'jobs'): '/فرصت-های-همکاری/',
            ('fa', 'products'): '/محصولات/',
        }
        return cands.get((lang, which), '/')

    def build_tax(self):
        for lang, tax in self.data['tax'].items():
            by_tag, by_cat, by_author = self.indexes[lang]
            ui = UI[lang]
            sec = self.section_href(lang, 'articles')
            for term in tax.get('tags') or []:
                path = path_of(term.get('link') or '')
                if not self.wanted(path):
                    continue
                name = htmlmod.unescape(term.get('name') or '')
                items = by_tag.get(term.get('id'), [])
                h1 = H1[('tag', lang)](name)
                self.listing(path, lang, h1, plain(qtrans(term.get('description') or '', lang)), items, 'tag',
                             [(ui['articles'], sec), (name, None)])
            for term in tax.get('categories') or []:
                path = path_of(term.get('link') or '')
                if not self.wanted(path):
                    continue
                name = htmlmod.unescape(term.get('name') or '')
                items = by_cat.get(term.get('id'), [])
                h1 = H1[('category', lang)](name)
                self.listing(path, lang, h1, plain(qtrans(term.get('description') or '', lang)), items, 'category',
                             [(ui['articles'], sec), (name, None)])
            for user in tax.get('users') or []:
                path = path_of(user.get('link') or '')
                if not self.wanted(path):
                    continue
                name = htmlmod.unescape(user.get('name') or '')
                items = by_author.get(user.get('id'), [])
                h1 = H1[('author', lang)](name)
                self.listing(path, lang, h1, plain(user.get('description') or ''), items, 'author',
                             [(ui['articles'], sec), (name, None)])

    def wanted(self, path):
        return path in self.want

    def cpt_item(self, row, lang, img_ids=False):
        path = path_of(row.get('link') or '')
        title = rendered(row.get('title') or {})
        content = (row.get('content') or {}).get('rendered') or ''
        item = {
            'path': path, 'title': title, 'date': row.get('date') or '',
            'excerpt': clip(plain(content), 160) if content and 'elementor' not in content[:80] else '',
        }
        if img_ids:
            mid = str(row.get('featured_media') or '')
            item['img'] = self.data.get('media', {}).get(mid) or ''
        return item

    def build_cpt(self):
        fa = self.data['cpt'].get('fa') or {}
        # customers
        rows = fa.get('_customers') or []
        items = [self.cpt_item(r, 'fa', True) for r in rows]
        items.sort(key=lambda x: x['date'], reverse=True)
        base = '/_customers/'
        if self.wanted(base) or any(self.wanted(it['path']) for it in items):
            if self.wanted(base):
                self.listing(base, 'fa', H1[('customer-archive', 'fa')](''), '', items, 'customer',
                             [(UI['fa']['customers'], self.section_href('fa', 'customers')),
                              ('مشتریان', None)], cur='customers')
            for row, item in zip(rows, items):
                if self.wanted(item['path']):
                    self.single(item, 'fa', 'customer', 'customers', base, item.get('img'), '')
        # dealers
        frows = fa.get('_franchise') or []
        # city id -> name
        cities = {c['id']: htmlmod.unescape(c.get('name') or '') for c in (fa.get('_citynmg') or [])}
        ditems = []
        for r in frows:
            it = self.cpt_item(r, 'fa')
            cids = r.get('_citynmg') or []
            prov = cities.get(cids[0], '') if cids else ''
            it['province'] = prov
            it['rows'] = contact_for(prov, it['title'])
            ditems.append(it)
        ditems.sort(key=lambda x: x['date'], reverse=True)
        base = '/_franchise/'
        if self.wanted(base):
            self.listing(base, 'fa', H1[('dealer-archive', 'fa')](''), '', ditems, 'dealer',
                         [(UI['fa']['dealers'], self.section_href('fa', 'dealers')),
                          ('نمایندگان', None)], cur='dealers')
        for it in ditems:
            if self.wanted(it['path']):
                extra = ''
                if it.get('rows'):
                    lis = ''.join(f'<li>{esc(a)}: {esc(b)}</li>' for a, b in it['rows'])
                    extra = f'<ul class="arch-rows">{lis}</ul>'
                if it.get('province'):
                    extra = f'<p>{esc(it["province"])}</p>' + extra
                self.single(it, 'fa', 'dealer', 'dealers', base, '', extra)
        for city in fa.get('_citynmg') or []:
            path = path_of(city.get('link') or '')
            if not self.wanted(path):
                continue
            name = htmlmod.unescape(city.get('name') or '')
            mine = [it for it in ditems if it.get('province') == name]
            self.listing(path, 'fa', H1[('province', 'fa')](name), plain(city.get('description') or ''),
                         mine, 'province',
                         [(UI['fa']['dealers'], self.section_href('fa', 'dealers')),
                          (name, None)], cur='dealers')
        # downloads
        dls = [self.cpt_item(r, 'fa', True) for r in (fa.get('_downloadcenter') or [])]
        dls.sort(key=lambda x: x['date'], reverse=True)
        base = '/_downloadcenter/'
        if self.wanted(base):
            self.listing(base, 'fa', H1[('download-archive', 'fa')](''), '', dls, 'download',
                         [(UI['fa']['downloads'], self.section_href('fa', 'downloads')),
                          ('مرکز دانلود', None)], cur='downloads')
        for it in dls:
            if self.wanted(it['path']):
                self.single(it, 'fa', 'download', 'downloads', base, it.get('img'), '')
        # job archive (CPT entries already have real pages)
        jobs = []
        for r in (fa.get('_joboffers') or []):
            it = self.cpt_item(r, 'fa')
            it['excerpt'] = clip(plain((r.get('content') or {}).get('rendered') or ''), 180)
            jobs.append(it)
        jobs.sort(key=lambda x: x['date'], reverse=True)
        base = '/_joboffers/'
        if self.wanted(base):
            self.listing(base, 'fa', H1[('job-archive', 'fa')](''), '', jobs, 'job-ad',
                         [(UI['fa']['jobs'], self.section_href('fa', 'jobs')),
                          ('موقعیت های شغلی', None)], cur='careers')
        # jet-menu templates
        for lang, group in self.data['cpt'].items():
            for row in group.get('jet-menu') or []:
                it = self.cpt_item(row, lang)
                if self.wanted(it['path']):
                    self.single(it, lang, 'menu-template', '', '', '', '')
        # EN representatives archive + singles that are in the checklist
        en = self.data['cpt'].get('en') or {}
        reps = [self.cpt_item(r, 'en') for r in (en.get('representatives_01') or [])]
        base = '/en/representatives_01/'
        if self.wanted(base):
            self.listing(base, 'en', H1[('dealer-archive', 'en')](''), '', reps, 'dealer',
                         [(UI['en']['dealers'], self.section_href('en', 'dealers')),
                          ('representatives', None)], cur='dealers')
        for it in reps:
            if self.wanted(it['path']):
                self.single(it, 'en', 'dealer', 'dealers', base, '', '')

    def single(self, item, lang, kind, section, archive, img, extra_html):
        path = item['path']
        ui = UI[lang]
        trail = []
        if archive:
            trail.append((ui.get(section) or item['title'], rel_link(path, archive)))
        elif section:
            trail.append((ui[section], rel_link(path, self.section_href(lang, section))))
        trail.append((item['title'], None))
        fig = ''
        if img:
            fig = f'<p><img class="arch-cover" src="{esc(img)}" alt="{esc(item["title"])}" loading="lazy" decoding="async"></p>'
        main = f'''{page_hero(self.prefix(path), trail, esc(item["title"]), '', '', lang=lang)}
  <section class="section"><div class="wrap prose">{fig}{extra_html}</div></section>'''
        cur = {'customers': 'customers', 'dealers': 'dealers', 'downloads': 'downloads', 'jobs': 'careers'}.get(section, '')
        self.emit(path, lang, item['title'], item['title'], main, kind, cur=cur)

    def build_jobs(self):
        for row in self.data.get('jobs') or []:
            path = path_of(row.get('link') or '')
            title = rendered(row.get('title') or {})
            raw = (row.get('content') or {}).get('rendered') or ''
            body = lines_to_html(html_lines(raw), skip_title=title)
            if len(plain(body)) < 20:
                body = f'<p>{esc(plain((row.get("excerpt") or {}).get("rendered") or ""))}</p>'
            # point the careers link at the redesign page
            body = body.replace('https://abadis-med.com/فرصت-های-همکاری/', rel_link(path, '/فرصت-های-همکاری/'))
            body = body.replace('https://abadis-med.com/%d9%81%d8%b1%d8%b5%d8%aa-%d9%87%d8%a7%db%8c-%d9%87%d9%85%da%a9%d8%a7%d8%b1%db%8c/',
                                rel_link(path, '/فرصت-های-همکاری/'))
            item = {'path': path, 'title': title, 'date': row.get('date') or ''}
            # reuse single chrome but with the body
            ui = UI['fa']
            trail = [(ui['jobs'], rel_link(path, '/فرصت-های-همکاری/')), (title, None)]
            main = f'''{page_hero(self.prefix(path), trail, esc(title), '', '', lang='fa')}
  <section class="section"><div class="wrap prose">{body}</div></section>'''
            self.emit(path, 'fa', title, title, main, 'job-ad', cur='careers')

    def build_paged_indexes(self):
        """/مقالات/2/ and the same pattern on news and EN/AR, without touching page 1."""
        specs = (
            ('fa-articles', '/مقالات/', 'fa', 'مقالات', 'articles'),
            ('fa-news', '/آخرین-اخبار/', 'fa', 'آخرین اخبار', 'news'),
            ('en-articles', '/en/blog/', 'en', 'Articles', 'articles'),
            ('en-news', '/en/latest-news/', 'en', 'News', 'news'),
            ('ar-articles', '/arabic/articles/', 'ar', 'المقالات', 'articles'),
            ('ar-news', '/arabic/الاخبار/', 'ar', 'الاخبار', 'news'),
        )
        for key, base, lang, h1, cur in specs:
            items = self.data.get('listings', {}).get(key) or []
            if len(items) <= PER:
                continue
            pages = math.ceil(len(items) / PER)
            ui = UI[lang]
            for n in range(2, pages + 1):
                path = base.rstrip('/') + f'/{n}/'
                chunk = items[(n - 1) * PER:n * PER]
                cards = ''.join(self.card(path, it, lang) for it in chunk)
                meta = f'<p class="arch-note">{esc(ui["page"])} {num(lang, n)}</p>'
                trail = [(h1, rel_link(path, base)), (f'{ui["page"]} {num(lang, n)}', None)]
                # number pager uses /page/N for archives; these indexes use /N/
                nav = self.index_pager(path, base, n, pages, lang)
                main = f'''{page_hero(self.prefix(path), trail, esc(h1), '', meta, lang=lang)}
  <section class="section"><div class="wrap"><div class="post-grid">{cards}</div>
  {nav}</div></section>'''
                self.emit(path, lang, h1, h1, main, 'pagination', cur=cur)

    def index_pager(self, from_dir, base, page_n, pages, lang):
        ui = UI[lang]
        def href(n):
            path = base if n == 1 else base.rstrip('/') + f'/{n}/'
            return rel_link(from_dir, path)
        bits = []
        if page_n > 1:
            bits.append(f'<a href="{esc(href(page_n - 1))}">{esc(ui["prev"])}</a>')
        # window so a 20-page index stays usable
        lo, hi = max(1, page_n - 3), min(pages, page_n + 3)
        nums = [1] if lo > 1 else []
        nums += list(range(lo, hi + 1))
        if hi < pages:
            nums.append(pages)
        last = 0
        for n in nums:
            if n - last > 1:
                bits.append('<span>…</span>')
            label = num(lang, n)
            if n == page_n:
                bits.append(f'<span class="is-current" aria-current="page">{label}</span>')
            else:
                bits.append(f'<a href="{esc(href(n))}">{label}</a>')
            last = n
        if page_n < pages:
            bits.append(f'<a href="{esc(href(page_n + 1))}">{esc(ui["next"])}</a>')
        return f'<nav class="arch-pager" aria-label="{esc(ui["pager"])}">{"".join(bits)}</nav>'

    def build_specials(self):
        self.waste_category()
        self.catalogue()
        self.reservoir()

    def waste_category(self):
        # Live FA category (page 19862) has an empty body. Cards must not use
        # .reveal: iOS Safari skips the first IntersectionObserver callback when
        # html/body use overflow-x:clip, which leaves this short page blank.
        specs = (
            ('/محصولات/کیسه-های-تخصصی-و-مدیریت-پسماند/', 'fa', 'کیسه های تخصصی و مدیریت پسماند',
             'کیسه زباله PVA و رسیور یکبار مصرف',
             [('محصولات', '/محصولات/')],
             [('/محصولات/کیسه-های-تخصصی-و-مدیریت-پسماند-2/', 'کیسه زباله PVA', 'assets/img/c/pva-laundry-bag-900.webp'),
              ('/محصولات/مخزن/#receiver', 'رسیور یکبار مصرف', 'assets/img/c/928b52ffc716-900.webp')]),
            ('/en/products/specialized-bags-waste-management/', 'en', 'Specialized Bags & Waste Management',
             'PVA waste bag and disposable receiver',
             [('Products', '/en/products/')],
             [('/en/products/specialized-bags-waste-management/#pva', 'PVA waste bag', 'assets/img/c/pva-laundry-bag-900.webp'),
              ('/en/products/canisters/#receiver', 'Disposable receiver', 'assets/img/c/928b52ffc716-900.webp')]),
            ('/arabic/أكياس-متخصصة-وإدارة-النفايات/', 'ar', 'أكياس متخصصة وإدارة النفايات',
             'كيس نفايات PVA ووعاء التجميع',
             [('منتجات', '/arabic/منتجات/')],
             [('/arabic/كيس-نفايات-pva/', 'كيس نفايات PVA', 'assets/img/c/pva-laundry-bag-900.webp'),
              ('/arabic/خزانات/#receiver', 'وعاء التجميع', 'assets/img/c/928b52ffc716-900.webp')]),
        )
        for path, lang, h1, lead, trail_bits, items in specs:
            cards = []
            for href, title, img in items:
                cards.append(
                    f'<a class="post-card" href="{esc(rel_link(path, href))}">'
                    f'<div class="ph"><img src="{esc(rel_link(path, "/" + img))}" alt="{esc(title)}" loading="eager" decoding="async"></div>'
                    f'<div class="body"><h3>{esc(title)}</h3><span class="go">{esc(UI[lang]["more"])}</span></div></a>'
                )
            trail = [(label, rel_link(path, dest)) for label, dest in trail_bits] + [(h1, None)]
            main = f'''{page_hero(self.prefix(path), trail, esc(h1), esc(lead), '', lang=lang)}
  <section class="section"><div class="wrap"><div class="post-grid arch-products">{''.join(cards)}</div></div></section>'''
            self.emit(path, lang, h1, lead, main, 'special', cur='products')

    def catalogue(self):
        """Same PDFs the English download centre already publishes, at /en/catalogue/."""
        path = '/en/catalogue/'
        # titles are the live download-centre headings; files are the ones that page links
        docs = [
            ('Abadis Catalouge', 'https://www.abadis-med.com/en/wp-content/uploads/2025/03/Abadis-Med-Catalouge.jpg',
             '../wp-content/uploads/2025/02/Abadis-Catalouge.pdf'),
            ('Wall Suction', 'https://www.abadis-med.com/en/wp-content/uploads/2023/01/ساکشن-دیواری-بزرگسال-1030x1030-1-768x768-1.jpg',
             '../wp-content/uploads/2021/12/wall-suction-en.pdf'),
            ('Abadis Filters', 'https://www.abadis-med.com/en/wp-content/uploads/2021/12/filters-catalouge-en-1-1030x1030.jpg',
             '../wp-content/uploads/2021/12/filters-catalouge-en.pdf'),
            ('Endotracheal Tube Holder', 'https://www.abadis-med.com/en/wp-content/uploads/2021/12/endotracheal-tube-holder-catalog-ٍ-En-1-1030x1030.jpg',
             '../wp-content/uploads/2021/12/endotracheal-tube-holder-catalog-ٍ-En.pdf'),
            ('Abadis Suction Bag', 'https://www.abadis-med.com/en/wp-content/uploads/2024/01/Abadis-Suction-liner-bag-catalouge-2-1030x1030.jpg',
             '../wp-content/uploads/2021/12/suction-bag-catalog-En.pdf'),
            ('Installation on a rail bracket', 'https://www.abadis-med.com/en/wp-content/uploads/2024/02/Installation-on-a-rail-bracket-1-1030x1030.jpg',
             '../wp-content/uploads/2024/02/Installation-on-a-rail-bracket.pdf'),
            ('Installation on a trolley base', 'https://www.abadis-med.com/en/wp-content/uploads/2024/02/Installation-on-a-trolley-1030x1030.jpg',
             '../wp-content/uploads/2024/02/Installation-on-a-trolley-base.pdf'),
            ('Installation on the console', 'https://www.abadis-med.com/en/wp-content/uploads/2024/02/Installation-on-the-console-1030x1030.jpg',
             '../wp-content/uploads/2024/02/Installation-on-the-console.pdf'),
        ]
        cards = []
        for title, img, pdf in docs:
            # pdf path is relative to /en/ (same depth as center-download)
            href = pdf  # ../wp-content/... from /en/catalogue/ resolves to /en/wp-content/
            cards.append(
                f'<a class="post-card dl-card reveal" href="{esc(href)}" target="_blank" rel="noopener">'
                f'<div class="ph" style="background:#fff"><img src="{esc(img)}" alt="{esc(title)}" loading="lazy" decoding="async"></div>'
                f'<div class="body"><h3>{esc(title)}</h3><span class="go">Download Catalogue (PDF)</span></div></a>'
            )
        h1 = 'Catalogue'
        trail = [(h1, None)]
        main = f'''{page_hero(self.prefix(path), trail, esc(h1), '', '', lang='en')}
  <section class="section"><div class="wrap"><div class="post-grid cat-grid">{''.join(cards)}</div></div></section>'''
        self.emit(path, 'en', 'Catalogue', 'Catalogue', main, 'special', cur='downloads')

    def reservoir(self):
        """Serve the English calculator at the live /en/reservoir-calculator/ URL."""
        src = SITE / 'en' / 'calculator' / 'index.html'
        if not src.is_file():
            self.failed.append(('/en/reservoir-calculator/', 'English calculator page is missing'))
            return
        s = src.read_text(encoding='utf-8')
        s = re.sub(r'<link rel="canonical" href="[^"]*">',
                   '<link rel="canonical" href="https://abadis-med.com/en/reservoir-calculator/">', s, count=1)
        s = re.sub(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*">\n?', '', s)
        s = s.replace(
            '<link rel="canonical" href="https://abadis-med.com/en/reservoir-calculator/">',
            '<link rel="canonical" href="https://abadis-med.com/en/reservoir-calculator/">\n'
            '<link rel="alternate" hreflang="en" href="https://abadis-med.com/en/reservoir-calculator/">\n'
            '<link rel="alternate" hreflang="x-default" href="https://abadis-med.com/en/reservoir-calculator/">\n'
            '<link rel="stylesheet" href="../../assets/css/archives.css?v=20261115a">',
            1)
        s = s.replace('<title>Savings calculator — Abadis Medical Reservoirs</title>',
                      '<title>Reservoir calculator — Abadis Medical Reservoirs</title>', 1)
        s = s.replace('content="Savings calculator — Abadis Medical Reservoirs"',
                      'content="Reservoir calculator — Abadis Medical Reservoirs"', 1)
        s = s.replace('https://abadis-med.com/en/calculator/', 'https://abadis-med.com/en/reservoir-calculator/')
        s = s.replace('href="../../en/calculator/"', 'href="../../en/reservoir-calculator/"')
        dest = SITE / 'en' / 'reservoir-calculator' / 'index.html'
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(s, encoding='utf-8')
        self.have.add('/en/reservoir-calculator/')
        self.written.add('/en/reservoir-calculator/')
        self.stats.append(('special', 'en', '/en/reservoir-calculator/'))

    def run(self, want):
        self.want = want
        self.build_tax()
        self.build_cpt()
        self.build_jobs()
        self.build_paged_indexes()
        self.build_specials()
        missing = sorted(p for p in want if p not in self.written)
        for p in missing:
            self.failed.append((p, 'no WordPress term or post matched this URL'))
        return self.stats, self.failed


def wanted_paths():
    want = set()
    for path, status, _title, _lang in checklist_rows():
        if status.startswith('بایگانی/صفحه فرعی وردپرس'):
            want.add(path)
        elif status.startswith('آگهی استخدام قدیمی'):
            want.add(path)
    want.add('/محصولات/کیسه-های-تخصصی-و-مدیریت-پسماند/')
    want.add('/en/catalogue/')
    want.add('/en/reservoir-calculator/')
    return want


def drop_aliases(written):
    fp = DATA / 'url_aliases.json'
    aliases = json.load(open(fp, encoding='utf-8'))
    removed = []
    for key in list(aliases):
        path = key if key.endswith('/') else key + '/'
        if path in written:
            aliases.pop(key)
            removed.append(path)
    json.dump(aliases, open(fp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    fp.write_text(open(fp, encoding='utf-8').read().rstrip() + '\n', encoding='utf-8')
    return removed


def kept_redirects():
    """True duplicates and the test post stay on 301. Other unbuilt URLs are out of scope."""
    rows = []
    for path, status, title, lang in checklist_rows():
        if 'تکراری' in status or path.rstrip('/') == '/تست':
            rows.append({'path': path, 'lang': lang, 'title': title, 'status': status})
    return rows


def build(write):
    data = load_cache()
    want = wanted_paths()
    b = Builder(data, write)
    stats, failed = b.run(want)
    removed = drop_aliases(b.written)
    report = {
        'pages': len(stats),
        'by_type': {},
        'by_type_lang': {},
        'aliases_removed': len(removed),
        'failed': failed,
        'kept_redirects': kept_redirects(),
    }
    for kind, lang, path in stats:
        report['by_type'][kind] = report['by_type'].get(kind, 0) + 1
        key = f'{kind}/{lang}'
        report['by_type_lang'][key] = report['by_type_lang'].get(key, 0) + 1
    out = DATA / 'archive-pages-report.json'
    json.dump(report, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(json.dumps({k: report[k] for k in ('pages', 'by_type', 'by_type_lang', 'aliases_removed')}, ensure_ascii=False, indent=1))
    print('failed', len(failed))
    for p, why in failed[:30]:
        print(' ', p, why)
    return report


def main():
    written_rels = []

    def write(rel, html):
        f = SITE / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(html, encoding='utf-8')
        written_rels.append(rel)

    report = build(write)
    import url_migrate
    box = {}
    url_migrate.write_redirects(box)
    print('rules', box.get('redirect_rules'))
    report['redirect_rules'] = box.get('redirect_rules')
    json.dump(report, open(DATA / 'archive-pages-report.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
