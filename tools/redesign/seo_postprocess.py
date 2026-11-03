"""SEO post-process over the built site (idempotent). Run after build.py:
    python3 tools/redesign/seo_postprocess.py
- self-hosted docs: rewrites abadis-med.com wp-content/uploads doc links to the mirrored copies in site/
- canonical: FA article/news detail pages point to themselves (were pointing to the section)
- JSON-LD (schema.org): Organization on all pages, Product on product pages,
  Article/NewsArticle on posts, BreadcrumbList from the visible .crumbs trail
- alt text: content images with missing/empty alt get a meaningful alt; decorative stay alt=""
- liara_nginx.conf: 301 map + 404 page for Liara static hosting
"""
import re, os, json, glob, html, urllib.parse
ROOT = os.path.join(os.path.dirname(__file__), '..', '..', 'site')
ROOT = os.path.abspath(ROOT)
BASE = 'https://abadis-med.com/'
SKIP_DIRS = ('hero-options', 'home-hero-options', 'contact-hero-options', 'solutions-hero-options', 'news-hero-options',
             'articles-options', 'careers-options', 'hero-test', 'brand', 'dial-designs', 'dial-practical',
             'dial-steppers', 'logo-scroll', 'seed-slingshot', '3d-sketches', 'chatbot-demo')
DECOR = re.compile(r'class="[^"]*\b(lg-dark|path-ico-[a-z]+|sec-mark-[a-z]+|why-logo-dark|zh-bg-layer|i)\b')
ORG = {
 'fa': ('مخازن طبی آبادیس', 'شرکت دانش‌بنیان تولیدکننده کیسه ساکشن یکبارمصرف و ملزومات کنترل عفونت'),
 'en': ('Abadis Medical Reservoirs', 'Knowledge-based manufacturer of disposable suction liner bags and infection-control supplies'),
 'ar': ('خزانات طبي آباديس', 'شركة قائمة على المعرفة لتصنيع أكياس الشفط أحادية الاستخدام ومستلزمات مكافحة العدوى'),
}
NEWS_WORDS = ('اخبار', 'News', 'الأخبار', 'الاخبار', 'أخبار')

def page_url(rel):
    d = os.path.dirname(rel)
    return BASE + (d + '/' if d else '')

def strip_tags(s):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', s))).strip()

def load_docs():
    m = {}
    for u in open(os.path.join(os.path.dirname(__file__), 'data', 'self_hosted_docs.txt')).read().split():
        sp = urllib.parse.urlsplit(u)
        local = urllib.parse.unquote(sp.path).lstrip('/')
        if os.path.isfile(os.path.join(ROOT, local)):
            m[u] = local
    return m

def rewrite_docs(s, rel, docs):
    d = os.path.dirname(rel)
    for u, local in docs.items():
        if u in s:
            s = s.replace(u, os.path.relpath(local, d or '.'))
    return s

def lang_of(s):
    m = re.search(r'<html[^>]*lang="([a-z]{2})', s)
    return m.group(1) if m else 'fa'

def crumbs(s, url):
    m = re.search(r'<p class="crumbs">(.*?)</p>', s, re.S)
    if not m: return None
    parts = re.split(r'\s*›\s*', m.group(1))
    items = []
    for i, p in enumerate(parts):
        a = re.search(r'href="([^"]*)"[^>]*>(.*?)</a>', p, re.S)
        if a:
            items.append((strip_tags(a.group(2)), urllib.parse.urljoin(url, a.group(1))))
        elif strip_tags(p):
            items.append((strip_tags(p), url))
    return items

def jsonld(s, rel):
    lang = lang_of(s)
    url = page_url(rel)
    name, desc = ORG[lang]
    org = {'@type': 'Organization', '@id': BASE + '#organization', 'name': name, 'alternateName': 'Abadis Med',
           'url': BASE if lang == 'fa' else BASE + ('en/' if lang == 'en' else 'arabic/'),
           'logo': BASE + 'assets/img/abadis-logo-teal.png', 'description': desc,
           'telephone': '+982192001017',
           'sameAs': ['https://www.instagram.com/abadis.med/', 'https://www.linkedin.com/company/abadis-medical-co/',
                      'https://www.aparat.com/abadismed', 'https://t.me/abadis_med']}
    graph = [org]
    h1 = re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S)
    h1 = strip_tags(h1.group(1)) if h1 else ''
    md = re.search(r'<meta name="description" content="([^"]*)"', s)
    md = html.unescape(md.group(1)) if md else ''
    img = re.search(r'<meta property="og:image" content="([^"]+)"', s)
    img = urllib.parse.urljoin(url, html.unescape(img.group(1))) if img else None
    cr = crumbs(s, url)
    if 'class="gal-main' in s and h1:
        p = {'@type': 'Product', 'name': h1, 'url': url, 'brand': {'@type': 'Brand', 'name': name},
             'manufacturer': {'@id': BASE + '#organization'}, 'inLanguage': lang}
        if md: p['description'] = md
        if img: p['image'] = img
        graph.append(p)
    elif re.search(r'<article class="article prose', s) and h1:
        news = bool(cr and len(cr) > 2 and any(w in cr[1][0] for w in NEWS_WORDS))
        a = {'@type': 'NewsArticle' if news else 'Article', 'headline': h1[:110], 'url': url,
             'mainEntityOfPage': url, 'inLanguage': lang, 'author': {'@id': BASE + '#organization'},
             'publisher': {'@id': BASE + '#organization'}}
        t = re.search(r'<time datetime="([^"]+)"', s)
        if t: a['datePublished'] = t.group(1)
        if md: a['description'] = md
        if img: a['image'] = img
        graph.append(a)
    if cr and len(cr) > 1:
        graph.append({'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': u} for i, (n, u) in enumerate(cr)]})
    block = ('<script type="application/ld+json" data-abadis-ld>' +
             json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False).replace('</', '<\\/') +
             '</script>\n')
    s = re.sub(r'<script type="application/ld\+json" data-abadis-ld>.*?</script>\n?', '', s, flags=re.S)
    return s.replace('</head>', block + '</head>', 1)

def fix_canonical(s, rel):
    parts = rel.split('/')
    if len(parts) == 3 and parts[0] in ('articles', 'news') and parts[1].isdigit():
        u = page_url(rel)
        s = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{u}">', s, count=1)
        s = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{u}">', s, count=1)
    return s

def fix_alts(s):
    h1 = re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S)
    fallback = strip_tags(h1.group(1)) if h1 else ''
    if not fallback:
        t = re.search(r'<title>(.*?)</title>', s, re.S)
        fallback = strip_tags(t.group(1)).split('|')[0].split('—')[0].strip() if t else ''
    out, last = [], 0
    for m in re.finditer(r'<img\b[^>]*>', s):
        tag = m.group(0)
        has = re.search(r'\salt="([^"]*)"', tag)
        if has and has.group(1).strip():
            continue
        if 'src=' not in tag:
            continue  # lightbox template, filled by JS
        before = s[max(0, m.start() - 400):m.start()]
        decorative = ('aria-hidden' in tag or DECOR.search(tag) or
                      before.rfind('aria-hidden="true"') > before.rfind('</'))
        if decorative:
            alt = ''
        else:
            after = s[m.end():m.end() + 500]
            alt = ''
            for rx in (r'<(figcaption|h[2-4]|strong|b)\b[^>]*>(.*?)</\1>', r'<(span|p|em)\b[^>]*>([^<]*?)</\1>'):
                for c in re.finditer(rx, after, re.S):
                    t = strip_tags(c.group(2))
                    if 2 < len(t) <= 110:
                        alt = t; break
                if alt: break
            alt = alt or fallback
            if not alt: continue
        alt = html.escape(alt, quote=True)
        new = re.sub(r'\salt="[^"]*"', f' alt="{alt}"', tag) if has else tag.replace('<img', f'<img alt="{alt}"', 1)
        if new != tag:
            out.append(s[last:m.start()]); out.append(new); last = m.end()
    out.append(s[last:])
    return ''.join(out)

def liara_conf():
    rules = []
    existing = lambda p: os.path.isfile(os.path.join(ROOT, urllib.parse.unquote(p).strip('/'), 'index.html')) or \
        os.path.isfile(os.path.join(ROOT, urllib.parse.unquote(p).lstrip('/')))
    seen = set()
    for line in open(os.path.join(ROOT, '_redirects')):
        line = line.strip()
        if not line or line.startswith('#'): continue
        f = line.split()
        if len(f) < 2: continue
        src, dst = f[0], f[1]
        key = src.rstrip('/') or '/'
        if key in seen or existing(src) or '*' in src or ':' in src: continue
        seen.add(key)
        pat = re.escape(urllib.parse.unquote(key)).replace('\\/', '/').replace('\\-', '-')
        rules.append(f'rewrite "^{pat}/?$" "{urllib.parse.unquote(dst)}" permanent;')
    conf = ['# Liara static (nginx) config, generated by tools/redesign/seo_postprocess.py',
            '# Included inside the server block by Liara. See docs.liara.ir/paas/static/how-tos/customize-nginx/',
            'charset utf-8;', 'error_page 404 /404.html;',
            'gzip on;', 'gzip_vary on;', 'gzip_proxied any;', 'gzip_comp_level 6;',
            'gzip_types text/plain text/css application/json application/javascript text/xml application/xml image/svg+xml;',
            '', '# 301 map from the old WordPress URLs'] + rules + ['',
            'location / {', '  index index.html;', '  try_files $uri $uri/ =404;', '}',
            'location = /404.html { internal; }',
            'location ~ /\\.well-known { allow all; }',
            'location ~* \\.(?:css|js|woff2?|ttf|otf)$ { expires 1y; add_header Cache-Control "public"; try_files $uri =404; }',
            'location ~* \\.(?:jpg|jpeg|png|webp|avif|gif|svg|ico|mp4|webm|glb|pdf|xlsx)$ { expires 1M; add_header Cache-Control "public"; try_files $uri =404; }',
            '']
    open(os.path.join(ROOT, 'liara_nginx.conf'), 'w').write('\n'.join(conf))
    return len(rules)


NOT_FOUND_MAIN = """<main id="main">
  <section class="page-hero">
    <div class="wrap">
      <p class="crumbs"><a href="/">خانه</a> › خطای ۴۰۴</p>
      <h1>صفحه مورد نظر پیدا نشد</h1>
      <p class="lead">ممکن است نشانی صفحه تغییر کرده باشد یا دیگر وجود نداشته باشد. از پیوندهای زیر استفاده کنید.</p>
    </div>
  </section>
  <section class="section"><div class="wrap" style="max-width:900px">
    <div class="cta-actions" style="display:flex;flex-wrap:wrap;gap:12px">
      <a class="btn" href="/">صفحه اصلی</a>
      <a class="btn" href="/products/">محصولات</a>
      <a class="btn" href="/solutions/">راهکارها</a>
      <a class="btn" href="/articles/">مقالات</a>
      <a class="btn" href="/news/">اخبار</a>
      <a class="btn" href="/downloads/">دانلود کاتالوگ</a>
      <a class="btn" href="/contact/">تماس با ما</a>
    </div>
    <div lang="en" dir="ltr" style="margin-top:40px">
      <h2>Page not found</h2>
      <p>The page you are looking for may have moved. <a href="/en/">Go to the English home page</a> or <a href="/en/products/">browse products</a>.</p>
    </div>
    <div lang="ar" dir="rtl" style="margin-top:24px">
      <h2>الصفحة غير موجودة</h2>
      <p>ربما تم نقل الصفحة التي تبحث عنها. <a href="/arabic/">الذهاب إلى الصفحة الرئيسية بالعربية</a> أو <a href="/arabic/منتجات/">تصفح المنتجات</a>.</p>
    </div>
  </div></section>
</main>"""

def make_404():
    s = open(os.path.join(ROOT, 'faq', 'index.html'), encoding='utf-8').read()
    s = re.sub(r'(href|src|srcset)="\.\./', r'\1="/', s)
    s = re.sub(r'<main id="main">.*?</main>', lambda m: NOT_FOUND_MAIN, s, flags=re.S)
    s = re.sub(r'<title>.*?</title>', '<title>صفحه پیدا نشد (۴۰۴) | مخازن طبی آبادیس</title>', s, count=1, flags=re.S)
    s = re.sub(r'<meta name="robots" content="[^"]*">', '<meta name="robots" content="noindex, follow">', s)
    s = re.sub(r'<link rel="(canonical|alternate)"[^>]*>\n?', '', s)
    s = re.sub(r'<meta property="og:url"[^>]*>\n?', '', s)
    s = re.sub(r'<script type="application/ld\+json" data-abadis-ld>.*?</script>\n?', '', s, flags=re.S)
    open(os.path.join(ROOT, '404.html'), 'w', encoding='utf-8').write(s)


def main():
    make_404()
    docs = load_docs()
    stats = dict(pages=0, ld=0, docs=0)
    for path in glob.glob(os.path.join(ROOT, '**', '*.html'), recursive=True):
        rel = os.path.relpath(path, ROOT)
        s0 = s = open(path, encoding='utf-8').read()
        s = rewrite_docs(s, rel, docs)
        top = rel.split('/')[0]
        if top not in SKIP_DIRS and '<head' in s:
            s = fix_canonical(s, rel)
            if rel != '404.html':
                s = jsonld(s, rel); stats['ld'] += 1
            s = fix_alts(s)
        if s != s0:
            open(path, 'w', encoding='utf-8').write(s); stats['pages'] += 1
    stats['liara_rules'] = liara_conf()
    print(stats)

if __name__ == '__main__':
    main()
