"""Move redesign pages to the exact URLs of the live https://abadis-med.com (FA root slugs, /en/, /arabic/).

Idempotent and re-runnable after build.py:  python3 tools/redesign/url_migrate.py [--site site] [--report out.json]

What it does
1. Builds a directory map OLD -> NEW (longest-prefix; a page's non-page files and sub-pages move with it).
   - static table below (pages, products, careers, install guide ...)
   - posts: site/articles/<id>/ and site/news/<id>/ -> /<wordpress slug>/ (data/posts.json, content/fa/*/<id>.md)
2. Moves files, rewriting every reference on the way (href/src/srcset/poster/action/data-*, meta refresh,
   og:url/og:image, CSS url(), inline-script relative strings, absolute https://abadis-med.com/... URLs in
   canonical/hreflang/JSON-LD/share links, and quoted "/old/path/" strings in .js/.json/.xml).
3. Leaves a redirect stub (meta refresh + JS redirect + canonical to the new URL, noindex) at every old path.
4. Writes stubs for real abadis-med.com URLs that have no redesign page (aliases, archives, tags ...),
   pointing at the nearest redesign page (data/url_aliases.json).
5. Rewrites sitemap.xml, _redirects, liara_nginx.conf and redirects-nginx.conf with 301 rules.
"""
import os, re, sys, json, glob, html, shutil, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
ARGS = sys.argv[1:]
def arg(name, default=None):
    if name in ARGS:
        i = ARGS.index(name); return ARGS[i + 1]
    return default
SITE = os.path.abspath(arg('--site', os.path.join(HERE, '..', '..', 'site')))
REPO = os.path.abspath(os.path.join(SITE, '..'))
DATA = os.path.join(HERE, 'data')
STUB_MARK = 'abadis-moved'
HOSTS = ('abadis-med.com', 'www.abadis-med.com')
BASE = 'https://abadis-med.com'

# ---------------------------------------------------------------- 1. map
STATIC = {
    # Persian (FA) pages -> live Persian slugs
    '/about/': '/درباره-ما/',
    '/contact/': '/ارتباط-با-ما/',
    '/products/': '/محصولات/',
    '/products/canister/': '/محصولات/مخزن/',
    '/products/connectors/': '/محصولات/اتصالات/',
    '/products/filters/': '/محصولات/فیلترها/',
    '/products/oral-hygiene/': '/محصولات/سواب-های-دهانی-و-نگهدارنده/',
    '/products/other/': '/محصولات/سایر-محصولات/',
    '/products/waste-bags/': '/محصولات/کیسه-های-تخصصی-و-مدیریت-پسماند/',
    '/products/stand/': '/محصولات/پایه/',
    '/products/suction-bag/': '/محصولات/کیسه-ساکشن/',
    '/products/suction-tube/': '/محصولات/ساکشن-تیوب/',
    '/articles/': '/مقالات/',
    '/news/': '/آخرین-اخبار/',
    '/careers/': '/فرصت-های-همکاری/',
    '/careers/jobs/accountant/': '/_joboffers/کارشناس-حسابداری/',
    '/careers/jobs/collections-officer/': '/_joboffers/کارمند-وصول-مطالبات/',
    '/careers/jobs/export-specialist/': '/_joboffers/کارشناس-صادرات/',
    '/careers/jobs/market-research/': '/_joboffers/کارشناس-تحقیقات-بازار/',
    '/careers/jobs/quality-assurance/': '/_joboffers/کارشناس-تضمین-کیفیت/',
    '/careers/jobs/rnd-specialist/': '/_joboffers/کارشناس-تحقیق-و-توسعه/',
    '/careers/jobs/sales-manager/': '/_joboffers/مدیر-فروش/',
    '/careers/jobs/sales-specialist/': '/_joboffers/کارشناس-فروش/',
    '/careers/jobs/secretary/': '/_joboffers/منشی/',
    '/jobs/': '/موقعیت-های-شغلی/',
    '/calculator/': '/محاسبه-گر/',
    '/csr/': '/مسئولیت-اجتماعی/',
    '/customers/': '/مشتریان-ما/',
    '/dealers/': '/لیست-نمایندگان/',
    '/downloads/': '/کاتالوگ/',
    '/experiences/': '/تجارب-ما/',
    '/faq/': '/پرسش-های-متداول/',
    '/install-guide/': '/راهنمای-نصب/',
    '/install-guide/end-user/': '/راهنمای-نصب/راهنمای-استفاده-کاربر-نهایی/',
    '/install-guide/tanks/': '/راهنمای-نصب/راهنمای-نصب-مخازن/',
    '/sdgs/': '/توسعه-پایدار/',
    # English
    '/en/products/oral-hygiene/': '/en/products/oral-swabs-tube-holders/',
}
# OLD paths whose content already exists at the real URL (same page twice): old becomes a stub only.
DUPLICATES = {
    '/en/careers/': '/en/collaboration-opportunities/',
}

def load_posts():
    m = {}
    pj = os.path.join(DATA, 'posts.json')
    if os.path.isfile(pj):
        for p in json.load(open(pj, encoding='utf-8')):
            path = urllib.parse.unquote(p.get('path') or urllib.parse.urlsplit(p.get('url', '')).path)
            if path:
                m[str(p['id'])] = path if path.endswith('/') else path + '/'
    for md in glob.glob(os.path.join(REPO, 'content', 'fa', '*', '*.md')):
        t = open(md, encoding='utf-8').read(3000)
        i = re.search(r'^id:\s*"?([^"\n]+)"?', t, re.M); s = re.search(r'^slug:\s*"?([^"\n]+)"?', t, re.M)
        if i and s and i.group(1) not in m:
            m[i.group(1)] = '/' + urllib.parse.unquote(s.group(1)).strip('/') + '/'
    return m

def is_stub(fp):
    try:
        return STUB_MARK in open(fp, encoding='utf-8', errors='ignore').read(4000)
    except OSError:
        return False

def page_dirs():
    out = set()
    for dp, dns, fns in os.walk(SITE):
        if 'index.html' in fns:
            rel = os.path.relpath(dp, SITE)
            out.add('/' if rel == '.' else '/' + rel.replace(os.sep, '/') + '/')
    return out

def build_map():
    M = dict(STATIC)
    posts = load_posts()
    unknown = []
    for d in sorted(page_dirs()):
        mm = re.match(r'^/(articles|news)/([^/]+)/$', d)
        if mm and d not in M:
            pid = mm.group(2)
            if pid in posts:
                M[d] = posts[pid]
            elif not is_stub(os.path.join(SITE, d.strip('/'), 'index.html')):
                unknown.append(d)
    return M, unknown

M, UNKNOWN = build_map()
KEYS = sorted(M, key=len, reverse=True)

MANIFEST_FILE = os.path.join(DATA, 'url_moves.json')
MANIFEST = json.load(open(MANIFEST_FILE, encoding='utf-8')) if os.path.isfile(MANIFEST_FILE) else {}

def check_collisions():
    seen = {}
    for old, new in M.items():
        ofp = os.path.join(SITE, old.strip('/'), 'index.html')
        if not os.path.isfile(ofp) or is_stub(ofp): continue
        if new in seen:
            sys.exit(f'collision: {old} and {seen[new]} both map to {new}')
        seen[new] = old
        fp = os.path.join(SITE, new.strip('/'), 'index.html')
        if os.path.isfile(fp) and not is_stub(fp) and new not in M and MANIFEST.get(old) != new:
            sys.exit(f'target exists: {old} -> {new} (a different page already lives there)')

def map_path(p):
    """site path (decoded, leading /) -> new site path"""
    for k in KEYS:
        if p == k[:-1]:          # '/about' -> '/درباره-ما'
            return M[k][:-1]
        if p.startswith(k):
            return M[k] + p[len(k):]
    for k, v in DUPLICATES.items():
        if p == k or p == k[:-1] or p == k + 'index.html':
            return v
    return p

# ---------------------------------------------------------------- 2. rewrite helpers
SKIP_PREFIX = ('#', 'mailto:', 'tel:', 'javascript:', 'data:', 'blob:', 'sms:', 'whatsapp:', 'about:')

def rel_from(target, from_dir):
    """target: site path ('/a/b/' or '/a/f.js'); from_dir: '/x/y/' -> relative ref"""
    is_dir = target.endswith('/')
    r = os.path.relpath(target if target == '/' else target.rstrip('/'), from_dir.rstrip('/') or '/')
    if r == '.': r = './' if is_dir else '.'
    elif is_dir: r += '/'
    return r

def split_ref(ref):
    q = ''
    for ch in ('#', '?'):
        pass
    m = re.match(r'^([^?#]*)(.*)$', ref, re.S)
    return m.group(1), m.group(2)

def fix_ref(ref, old_dir, new_dir, force_abs_host=False):
    """Return rewritten ref (string) or the original if nothing changes."""
    out = _fix_ref(ref, old_dir, new_dir)
    if out is not ref and '&amp;' in ref and '&' in out and '&amp;' not in out:
        out = out.replace('&', '&amp;')
    return out

def _fix_ref(ref, old_dir, new_dir):
    raw = ref
    r = html.unescape(ref.strip()) if '&' in ref else ref.strip()
    if not r or r.startswith(SKIP_PREFIX) or '{' in r or '${' in r or r.startswith('+'):
        return raw
    sp = urllib.parse.urlsplit(r)
    if sp.scheme in ('http', 'https') or r.startswith('//'):
        host = sp.netloc.lower()
        if host not in HOSTS: return raw
        path = urllib.parse.unquote(sp.path) or '/'
        np = map_path(path)
        if np == path: return raw
        tail = r[len(r.split('?')[0].split('#')[0]):]
        pre = r[:r.index(sp.netloc) + len(sp.netloc)]
        return pre + np + tail
    if sp.scheme: return raw
    pathpart, tail = split_ref(r)
    if not pathpart:
        return raw
    dec = urllib.parse.unquote(pathpart)
    if dec.startswith('/'):
        np = map_path(dec)
        return raw if np == dec else np + tail
    full = urllib.parse.urljoin(old_dir, dec)
    if full.startswith('/..') or '/../' in full:
        return raw
    np = map_path(full)
    if np == full and old_dir == new_dir:
        return raw
    if not full.startswith('/'): return raw
    out = rel_from(np, new_dir)
    # keep the original "explicit file" style when not a dir
    return out + tail

ATTR = re.compile(r'''(\s(?:href|src|poster|action|data-[\w-]+|content|imagesrcset|srcset)\s*=\s*)(["'])(.*?)\2''', re.I | re.S)
CSSURL = re.compile(r'''url\(\s*(['"]?)([^'")]+?)\1\s*\)''')
ABSURL = re.compile(r'''https?://(?:www\.)?abadis-med\.com(/[^\s"'<>()\\,&?#]*)?''')
QUOTED_REL = re.compile(r'''(["'`])(\.{1,2}/[^"'`\s]*?)\1''')
QUOTED_ROOT = re.compile(r'''(["'])(/[^"'\s<>]*?)\1''')

ASSET_EXT = re.compile(r'\.(png|jpe?g|webp|avif|gif|svg|ico|glb|gltf|bin|hdr|mp4|webm|json|js|mjs|css|pdf|woff2?|ttf|xlsx)([?#].*)?$', re.I)
def looks_url(v):
    v = v.strip()
    if not v or ' ' in v or v.startswith(('{', '[')): return False
    return v.startswith(('/', './', '../', 'http://', 'https://')) or bool(ASSET_EXT.search(v))

def rewrite_abs(s):
    def f(m):
        path = urllib.parse.unquote(m.group(1) or '/')
        np = map_path(path)
        if np == path: return m.group(0)
        if '%' in (m.group(1) or ''):
            np = urllib.parse.quote(np, safe='/-_.~')
        return m.group(0)[:m.group(0).index('.com') + 4] + np
    return ABSURL.sub(f, s)

def rewrite_html(s, old_dir, new_dir):
    # 1) absolute URLs anywhere (canonical, hreflang, og, JSON-LD, share links)
    s = rewrite_abs(s)
    # 2) attributes
    def attr(m):
        name = m.group(1).strip().lower()
        val = m.group(3)
        if name.startswith('content'):
            if re.match(r'^\s*\d+\s*;\s*url=', val, re.I):
                pre, u = re.match(r'^(\s*\d+\s*;\s*url=)(.*)$', val, re.I | re.S).groups()
                return m.group(1) + m.group(2) + pre + fix_ref(u, old_dir, new_dir) + m.group(2)
            if not looks_url(val) or ' ' in val.strip(): return m.group(0)
            return m.group(1) + m.group(2) + fix_ref(val, old_dir, new_dir) + m.group(2)
        if 'srcset' in name:
            parts = []
            for c in val.split(','):
                cs = c.strip()
                if not cs: parts.append(c); continue
                bits = cs.split(None, 1)
                bits[0] = fix_ref(bits[0], old_dir, new_dir)
                parts.append((' ' if c.startswith(' ') else '') + ' '.join(bits))
            return m.group(1) + m.group(2) + ','.join(parts) + m.group(2)
        if name.startswith('data-') and not looks_url(val):
            return m.group(0)
        return m.group(1) + m.group(2) + fix_ref(val, old_dir, new_dir) + m.group(2)
    s = ATTR.sub(attr, s)
    # 3) CSS url()
    s = CSSURL.sub(lambda m: 'url(' + m.group(1) + fix_ref(m.group(2), old_dir, new_dir) + m.group(1) + ')', s)
    # 4) inline scripts: relative + root strings (document-relative)
    def script(m):
        body = m.group(2)
        if 'application/ld+json' in m.group(1): return m.group(0)
        body = QUOTED_REL.sub(lambda q: q.group(1) + fix_ref(q.group(2), old_dir, new_dir) + q.group(1), body)
        body = QUOTED_ROOT.sub(lambda q: q.group(1) + fix_ref(q.group(2), old_dir, new_dir) + q.group(1) if len(q.group(2)) > 1 else q.group(0), body)
        return m.group(1) + body + m.group(3)
    s = re.sub(r'(<script\b[^>]*>)(.*?)(</script>)', script, s, flags=re.S | re.I)
    return s

def rewrite_css(s, old_dir, new_dir):
    s = rewrite_abs(s)
    return CSSURL.sub(lambda m: 'url(' + m.group(1) + fix_ref(m.group(2), old_dir, new_dir) + m.group(1) + ')', s)

def rewrite_text(s):
    """.js/.json/.xml/.txt: absolute site URLs and quoted root paths only (no document context)."""
    s = rewrite_abs(s)
    def f(q):
        v = q.group(2)
        if len(v) < 2 or v.startswith('//'): return q.group(0)
        pp, tail = split_ref(v)
        dec = urllib.parse.unquote(pp)
        np = map_path(dec)
        return q.group(0) if np == dec else q.group(1) + np + tail + q.group(1)
    return QUOTED_ROOT.sub(f, s)

TEXT_EXT = ('.js', '.mjs', '.json', '.xml', '.txt', '.webmanifest')
VENDOR = re.compile(r'(^|/)(vendor|three\.module\.js|OrbitControls\.js|node_modules)(/|$)')

# ---------------------------------------------------------------- 3. stubs
def stub_html(old_dir, new_target, title='', lang='fa'):
    """new_target: site path with optional #hash"""
    np, tail = split_ref(new_target)
    rel = rel_from(np, old_dir) + tail
    canon = BASE + np
    d = 'ltr' if lang == 'en' else 'rtl'
    t = html.escape(title or np)
    relq = html.escape(rel, quote=True)
    return (f'<!DOCTYPE html><html lang="{lang}" dir="{d}"><head><meta charset="utf-8">\n'
            f'<title>{t}</title><meta name="robots" content="noindex, follow">\n'
            f'<meta name="{STUB_MARK}" content="{html.escape(np + tail, quote=True)}">\n'
            f'<link rel="canonical" href="{canon}">\n'
            f'<meta http-equiv="refresh" content="0; url={relq}">\n'
            f'</head><body><p><a href="{relq}">{t}</a></p>\n'
            f'<script>location.replace({json.dumps(rel)}+(location.hash&&{json.dumps(tail)}===""?location.hash:""))</script>\n'
            f'</body></html>\n')

def title_of(fp):
    try:
        s = open(fp, encoding='utf-8', errors='ignore').read(20000)
    except OSError:
        return ''
    t = re.search(r'<title>(.*?)</title>', s, re.S)
    return html.unescape(re.sub(r'\s+', ' ', t.group(1))).strip() if t else ''

def lang_of_path(p):
    return 'en' if p.startswith('/en/') else 'ar' if p.startswith('/arabic/') else 'fa'

# ---------------------------------------------------------------- main
def main():
    check_collisions()
    report = {'moved': {}, 'stubs': [], 'alias_stubs': [], 'unknown_posts': UNKNOWN, 'duplicates': DUPLICATES}
    pages_before = page_dirs()
    # files to process
    files = []
    for dp, dns, fns in os.walk(SITE):
        if '.git' in dns: dns.remove('.git')
        for fn in fns:
            files.append('/' + os.path.relpath(os.path.join(dp, fn), SITE).replace(os.sep, '/'))
    stub_dirs = {d for d in pages_before if is_stub(os.path.join(SITE, d.strip('/'), 'index.html')) and d in M}
    moves = []   # (src, dst)
    for f in files:
        d = f.rsplit('/', 1)[0] + '/'
        nd = map_path(d)
        # an old directory that already holds our stub: nothing to move
        own = next((k for k in KEYS if d.startswith(k)), None)
        if own and own in stub_dirs and f.endswith('/index.html') and d == own:
            continue
        if any(d.startswith(k) for k in DUPLICATES):
            continue
        moves.append((f, nd + f.rsplit('/', 1)[1]))
    written = 0
    for src, dst in moves:
        sfp = os.path.join(SITE, src.lstrip('/'))
        dfp = os.path.join(SITE, dst.lstrip('/'))
        old_dir = src.rsplit('/', 1)[0] + '/'
        new_dir = dst.rsplit('/', 1)[0] + '/'
        if src.endswith('/index.html') and is_stub(sfp) and src != dst:
            continue
        ext = os.path.splitext(src)[1].lower()
        data = None
        if ext in ('.html', '.htm'):
            s = open(sfp, encoding='utf-8', errors='surrogateescape').read()
            data = rewrite_html(s, old_dir, new_dir)
        elif ext == '.css':
            s = open(sfp, encoding='utf-8', errors='surrogateescape').read()
            data = rewrite_css(s, old_dir, new_dir)
        elif ext in TEXT_EXT and not VENDOR.search(src):
            s = open(sfp, encoding='utf-8', errors='surrogateescape').read()
            data = rewrite_text(s)
        if src != dst:
            os.makedirs(os.path.dirname(dfp), exist_ok=True)
            if data is not None:
                open(dfp, 'w', encoding='utf-8', errors='surrogateescape').write(data)
                os.remove(sfp)
            else:
                shutil.move(sfp, dfp)
            written += 1
            if src.endswith('/index.html'):
                report['moved'][old_dir] = new_dir
        elif data is not None and data != s:
            open(dfp, 'w', encoding='utf-8', errors='surrogateescape').write(data)
            written += 1
    # duplicates: old copy -> stub; the real URL keeps the content
    for old, new in DUPLICATES.items():
        fp = os.path.join(SITE, old.strip('/'), 'index.html')
        if os.path.isfile(fp) and not is_stub(fp):
            t = title_of(fp)
            for f in os.listdir(os.path.dirname(fp)):
                p = os.path.join(os.path.dirname(fp), f)
                if os.path.isfile(p): os.remove(p)
            open(fp, 'w', encoding='utf-8').write(stub_html(old, new, t, lang_of_path(old)))
            report['stubs'].append((old, new))
    # stubs at every moved page dir
    for old, new in sorted(report['moved'].items()):
        fp = os.path.join(SITE, old.strip('/'), 'index.html')
        if os.path.exists(fp) and not is_stub(fp):
            continue  # something real was regenerated there (should not happen)
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        t = title_of(os.path.join(SITE, new.strip('/'), 'index.html'))
        open(fp, 'w', encoding='utf-8').write(stub_html(old, new, t, lang_of_path(new)))
        report['stubs'].append((old, new))
    # remove now-empty dirs left behind (other than stub dirs)
    for dp, dns, fns in os.walk(SITE, topdown=False):
        if dp != SITE and not os.listdir(dp):
            os.rmdir(dp)
    # alias stubs for live URLs with no redesign page
    aliases = json.load(open(os.path.join(DATA, 'url_aliases.json'), encoding='utf-8'))
    for src, info in aliases.items():
        tgt = info['to'] if isinstance(info, dict) else info
        tgt_path, tail = split_ref(tgt)
        tgt = map_path(tgt_path) + tail
        fp = os.path.join(SITE, src.strip('/'), 'index.html')
        if os.path.exists(fp) and not is_stub(fp):
            continue  # a real page exists there
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        t = (info.get('title') if isinstance(info, dict) else '') or title_of(os.path.join(SITE, split_ref(tgt)[0].strip('/'), 'index.html'))
        open(fp, 'w', encoding='utf-8').write(stub_html(src, tgt, t, lang_of_path(src)))
        report['alias_stubs'].append((src, tgt))
    # posts that the live site merged into another post (old slug 301s there on abadis-med.com):
    # content stays at its own old URL, canonical points at the post that replaced it
    mf = os.path.join(DATA, 'url_merged.json')
    report['merged_canonical'] = []
    if os.path.isfile(mf):
        for old, tgt in json.load(open(mf, encoding='utf-8')).items():
            fp = os.path.join(SITE, old.strip('/'), 'index.html')
            if not os.path.isfile(fp) or is_stub(fp): continue
            s = open(fp, encoding='utf-8').read()
            canon = BASE + tgt
            s2 = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{canon}">', s, count=1)
            if s2 != s:
                open(fp, 'w', encoding='utf-8').write(s2)
            report['merged_canonical'].append((old, tgt))
    # manifest of every page move (lets a later build.py + url_migrate.py run overwrite its own earlier output)
    man = dict(MANIFEST); man.update(report['moved'])
    json.dump(dict(sorted(man.items())), open(MANIFEST_FILE, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    # redirect configs
    write_redirects(report)
    report['files_written'] = written
    rp = arg('--report')
    if rp:
        json.dump(report, open(rp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(json.dumps({k: (len(v) if isinstance(v, (list, dict)) else v) for k, v in report.items()}, ensure_ascii=False))

UNPUB_BEGIN = '# BEGIN abadis-unpublished-posts'
UNPUB_END = '# END abadis-unpublished-posts'

def load_unpublished():
    """Posts this pipeline redirected after unpublish. Missing file means none."""
    fp = os.path.join(DATA, 'unpublished-posts.json')
    if not os.path.isfile(fp):
        return []
    try:
        data = json.load(open(fp, encoding='utf-8'))
    except (OSError, json.JSONDecodeError):
        return []
    posts = data.get('posts') if isinstance(data, dict) else None
    return posts if isinstance(posts, list) else []

def unpublished_tables(posts):
    src_to_dst = {}
    for post in posts:
        dst = post.get('target') or '/'
        if not str(dst).endswith('/'):
            dst += '/'
        for src in post.get('sources') or []:
            key = str(src).rstrip('/') or '/'
            if key != (dst.rstrip('/') or '/'):
                src_to_dst[key] = dst if dst.endswith('/') else dst + '/'
    return src_to_dst

def write_redirects(report):
    """_redirects (Netlify/Cloudflare format) + liara_nginx.conf + redirects-nginx.conf"""
    src_to_dst = unpublished_tables(load_unpublished())
    rules = []   # (src, dst)
    seen = set()
    def add(src, dst):
        key = src.rstrip('/') or '/'
        if key in src_to_dst:
            dst = src_to_dst[key]
        else:
            landed = (dst or '').split('#')[0].rstrip('/') or '/'
            if landed in src_to_dst:
                dst = src_to_dst[landed]
        if key in seen or key == (dst.rstrip('/') or '/'): return
        seen.add(key); rules.append((src, dst))
    # every OLD page dir -> NEW (all stubs we manage)
    for dp, dns, fns in os.walk(SITE):
        if 'index.html' in fns:
            fp = os.path.join(dp, 'index.html')
            if is_stub(fp):
                m = re.search(r'<meta name="%s" content="([^"]*)"' % STUB_MARK, open(fp, encoding='utf-8').read(3000))
                rel = os.path.relpath(dp, SITE)
                add('/' + rel.replace(os.sep, '/') + '/', html.unescape(m.group(1)))
    # legacy WordPress-style rules kept from the previous map, retargeted through the new map
    leg = os.path.join(DATA, 'legacy_redirects.txt')
    if os.path.isfile(leg):
        for line in open(leg, encoding='utf-8'):
            f = line.split()
            if len(f) < 2 or line.startswith('#'): continue
            src, dst = urllib.parse.unquote(f[0]), urllib.parse.unquote(f[1])
            p, tail = split_ref(dst)
            dst = map_path(p) + tail
            if os.path.isfile(os.path.join(SITE, src.strip('/'), 'index.html')) and not is_stub(os.path.join(SITE, src.strip('/'), 'index.html')):
                continue
            tp = split_ref(dst)[0]
            if not (tp == '/' or os.path.isfile(os.path.join(SITE, tp.strip('/'), 'index.html'))):
                continue
            add(src if src.endswith('/') else src + '/', dst)
    rules.sort(key=lambda r: r[0])
    # Unpublished slugs are written once, inside the managed block, not again above it.
    main_rules = [r for r in rules if (r[0].rstrip('/') or '/') not in src_to_dst]
    held_rules = [r for r in rules if (r[0].rstrip('/') or '/') in src_to_dst]
    for key, dst in sorted(src_to_dst.items()):
        if (key in seen) or key == (dst.rstrip('/') or '/'):
            continue
        src = key if key.endswith('/') else key + '/'
        if not src.startswith('/'):
            src = '/' + src
        held_rules.append((src if src.endswith('/') else src + '/', dst))
    held_rules.sort(key=lambda r: r[0])
    enc = lambda u: urllib.parse.quote(u, safe='/-_.~#')
    def emit_redirects(fh, rows):
        for s, d in rows:
            fh.write(f'{enc(s)} {enc(d)} 301\n')
            if s != '/' and s.endswith('/'):
                fh.write(f'{enc(s[:-1])} {enc(d)} 301\n')
    def emit_nginx(rows):
        lines = []
        for s, d in rows:
            key = s.rstrip('/')
            pat = re.escape(key).replace('\\/', '/').replace('\\-', '-')
            lines.append(f'rewrite "^{pat}/?$" "https://$host{enc(d)}" permanent;')
        return lines
    with open(os.path.join(SITE, '_redirects'), 'w', encoding='utf-8') as fh:
        fh.write('# 301 map, generated by tools/redesign/url_migrate.py (old redesign paths and unbuilt live URLs -> live-identical URLs)\n')
        emit_redirects(fh, main_rules)
        if held_rules:
            fh.write(UNPUB_BEGIN + '\n')
            emit_redirects(fh, held_rules)
            fh.write(UNPUB_END + '\n')
    nginx = emit_nginx(main_rules)
    held_nginx = emit_nginx(held_rules)
    conf = ['# Liara static (nginx) config, generated by tools/redesign/url_migrate.py',
            '# Included inside the server block by Liara. See docs.liara.ir/paas/static/how-tos/customize-nginx/',
            '# nginx matches the decoded URI, so Persian/Arabic paths are written in UTF-8; targets are percent-encoded.',
            'charset utf-8;', 'error_page 404 /404.html;',
            'gzip on;', 'gzip_vary on;', 'gzip_proxied any;', 'gzip_comp_level 6;',
            'gzip_types text/plain text/css application/json application/javascript text/xml application/xml image/svg+xml;',
            '', f'# 301 map ({len(nginx) + len(held_nginx)} rules)'] + nginx + (
                ['', UNPUB_BEGIN] + held_nginx + [UNPUB_END] if held_nginx else []) + ['',
            'location / {', '  index index.html;', '  try_files $uri $uri/ =404;', '}',
            'location = /404.html { internal; }',
            'location ~ /\\.well-known { allow all; }',
            'location ~* \\.(?:css|js|woff2?|ttf|otf)$ { expires 1y; add_header Cache-Control "public"; try_files $uri =404; }',
            'location ~* \\.(?:jpg|jpeg|png|webp|avif|gif|svg|ico|mp4|webm|glb|pdf|xlsx)$ { expires 1M; add_header Cache-Control "public"; try_files $uri =404; }',
            '']
    open(os.path.join(SITE, 'liara_nginx.conf'), 'w', encoding='utf-8').write('\n'.join(conf))
    open(os.path.join(SITE, 'redirects-nginx.conf'), 'w', encoding='utf-8').write(
        '# 301 map for a plain nginx server block (same rules as liara_nginx.conf), generated by tools/redesign/url_migrate.py\n'
        + '\n'.join(nginx + ((['', UNPUB_BEGIN] + held_nginx + [UNPUB_END]) if held_nginx else [])) + '\n')
    report['redirect_rules'] = len(main_rules) + len(held_rules)
    # sitemap: map locs, drop stubs
    sm = os.path.join(SITE, 'sitemap.xml')
    if os.path.isfile(sm):
        s = open(sm, encoding='utf-8').read()
        def mapu(m):
            u = m.group(2)
            sp = urllib.parse.urlsplit(html.unescape(u))
            p = urllib.parse.unquote(sp.path)
            np = map_path(p)
            if np == p: return m.group(0)
            return m.group(1) + 'https://abadis-med.com' + urllib.parse.quote(np, safe='/-_.~') + m.group(3)
        s = re.sub(r'(<loc>|href=")(https?://(?:www\.)?abadis-med\.com[^<"]*)(</loc>|")', mapu, s)
        def keep(m):
            loc = re.search(r'<loc>([^<]+)</loc>', m.group(0)).group(1)
            p = urllib.parse.unquote(urllib.parse.urlsplit(loc).path)
            fp = os.path.join(SITE, p.strip('/'), 'index.html')
            return '' if (os.path.isfile(fp) and is_stub(fp)) or not os.path.isfile(fp) else m.group(0)
        s = re.sub(r'[ \t]*<url>.*?</url>\n?', keep, s, flags=re.S)
        # sitemap URLs must be ASCII (RFC 3986): percent-encode every path
        def encu(m):
            sp = urllib.parse.urlsplit(html.unescape(m.group(2)))
            path = urllib.parse.quote(urllib.parse.unquote(sp.path), safe='/-_.~')
            return m.group(1) + f'{sp.scheme}://{sp.netloc}{path}' + m.group(3)
        s = re.sub(r'(<loc>|href=")(https?://[^<"]*)(</loc>|")', encu, s)
        open(sm, 'w', encoding='utf-8').write(s)

if __name__ == '__main__':
    main()
