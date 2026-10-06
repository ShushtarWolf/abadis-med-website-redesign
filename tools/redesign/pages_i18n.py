"""Build English (/en/) and Arabic (/arabic/) pages from REST snapshots."""
from __future__ import annotations
import json, pathlib, re, urllib.parse as u
from lib import esc, best_img, SITE
from layout import page, mosaic_hero, page_hero
from i18n import (
    LANGS, NAV, clean_html, strip_tags, load_map, GAPS, DATA,
)

# Skip utility / duplicate EN-AR pages
EN_SKIP_SLUGS = {
    'footer', 'فوتر', 'a1-2', 'دیگر-محصولات-2', 'catalogue', 'user-manuals',
    'canister-installation', 'reservoir-calculator', 'representatives-3',
    'articles',  # use blog
}
AR_SKIP_SLUGS = {'برگه-نمونه', 'الحاسبة'}  # keep الحوسبة as calculator

# Map WP slug → site path under lang root (trailing slash)
EN_PAGE_PATHS = {
    'home': '',
    'about-us': 'about-us/',
    'products': 'products/',
    'suction-bag': 'products/suction-bag/',
    'base-and-holder': 'products/base-and-holder/',
    'filters': 'products/filters/',
    'canisters': 'products/canisters/',
    'connections': 'products/connections/',
    'other-products': 'products/other-products/',
    'suction-tube': 'suction-tube/',
    'calculator': 'calculator/',
    'contact-us': 'contact-us/',
    'faqs': 'faqs/',
    'installation-manual': 'installation-manual/',
    'representatives': 'representatives/',
    'center-download': 'center-download/',
    'latest-news': 'latest-news/',
    'blog': 'blog/',
    'csr': 'csr/',
    'sdgs': 'sdgs/',
    'our-customers': 'our-customers/',
    'collaboration-opportunities': 'collaboration-opportunities/',
}
AR_PAGE_PATHS = {
    'صفحه-اصلی': '',
    'من-نحن': 'من-نحن/',
    'منتجات': 'منتجات/',
    'كيس-الشفط': 'كيس-الشفط/',
    'تثبیت': 'تثبیت/',
    'الفلتر': 'الفلتر/',
    'خزانات': 'خزانات/',
    'الوصلات': 'الوصلات/',
    'منتجات-اخری': 'منتجات-اخری/',
    'أنبوب-الشفط': 'أنبوب-الشفط/',
    'الحوسبة': 'الحوسبة/',
    'اتصل-بنا': 'اتصل-بنا/',
    'پرسش-های-متداول': 'پرسش-های-متداول/',
    'دليل-التركيب': 'دليل-التركيب/',
    'قائمة-الممثلين': 'قائمة-الممثلين/',
    'مركز-التنزيل': 'مركز-التنزيل/',
    'الاخبار': 'الاخبار/',
}

# FA path for hreflang for each EN/AR site path
def _fa_for(lang_path: str, lang: str) -> str:
    """Return i18n-map key for switcher/hreflang (usually the FA path)."""
    m = load_map()
    target = LANGS[lang]['root'] + lang_path
    for key, pair in m.items():
        if pair.get(lang) == target:
            return key
    return ''


def _depth(rel: str) -> int:
    parts = [x for x in pathlib.PurePosixPath(rel).parts if x != 'index.html']
    return len(parts)


def _prefix(depth: int) -> str:
    return '../' * depth


def _slug_decode(slug: str) -> str:
    return u.unquote(slug)


def load_lang_pages(lang: str):
    return json.load(open(DATA / f'{lang}_pages.json', encoding='utf-8'))


def load_lang_posts(lang: str):
    return json.load(open(DATA / f'{lang}_posts.json', encoding='utf-8'))


def page_by_slug(pages, slug):
    slug = _slug_decode(slug)
    for p in pages:
        if _slug_decode(p.get('slug') or '') == slug:
            return p
    return None


def render_content_page(write, lang, site_path, wp, cur_key, chip):
    """Generic prose page from a WP page payload."""
    L = LANGS[lang]
    root = L['root']
    rel = root + site_path + ('index.html' if site_path == '' or site_path.endswith('/') else '/index.html')
    if site_path == '':
        rel = root + 'index.html' if root else 'index.html'
        if root:
            rel = root + 'index.html'
    depth = _depth(rel)
    p = _prefix(depth)
    title = strip_tags(wp.get('title', {}).get('rendered', ''))
    desc = strip_tags(wp.get('excerpt', {}).get('rendered', ''))[:180]
    body = clean_html(wp.get('content', {}).get('rendered', ''))
    fa_path = _fa_for(site_path, lang)
    can = root + site_path
    # home
    if site_path == '':
        main = f'''{mosaic_hero(p, [], chip, esc(title), esc(desc), label=chip, lang=lang)}
  <section class="section"><div class="wrap prose reveal">{body}</div></section>'''
    else:
        trail = [(chip, None)]
        main = f'''{page_hero(p, trail, esc(title), esc(desc), lang=lang)}
  <section class="section"><div class="wrap prose reveal">{body}</div></section>'''
    html = page(p, cur_key, title, desc, main, lang=lang, fa_path=fa_path, canonical_path=can)
    write(rel if rel.endswith('.html') else rel + 'index.html', html)
    return rel


def build_posts(write, lang):
    L = LANGS[lang]
    root = L['root']
    posts = load_lang_posts(lang)
    # indexes
    if lang == 'en':
        news_path, blog_path = 'latest-news/', 'blog/'
        # treat all as news list + blog list (WP often uses categories; put all in both indexes sorted)
        items = sorted(posts, key=lambda x: x.get('date') or '', reverse=True)
        _write_post_index(write, lang, news_path, 'news', L['news_tag'] if False else 'News', items)
        _write_post_index(write, lang, blog_path, 'articles', 'Blog', items)
    else:
        news_path = 'الاخبار/'
        items = sorted(posts, key=lambda x: x.get('date') or '', reverse=True)
        _write_post_index(write, lang, news_path, 'news', 'الاخبار', items)

    for wp in posts:
        slug = _slug_decode(wp.get('slug') or str(wp['id']))
        site_path = f'{slug}/'
        rel = root + site_path + 'index.html'
        depth = _depth(rel)
        p = _prefix(depth)
        title = strip_tags(wp.get('title', {}).get('rendered', ''))
        desc = strip_tags(wp.get('excerpt', {}).get('rendered', ''))[:180]
        body = clean_html(wp.get('content', {}).get('rendered', ''))
        index_href = '../latest-news/' if lang == 'en' else '../الاخبار/'
        index_label = 'News' if lang == 'en' else 'الاخبار'
        # prefer blog parent label for EN when title looks like article — keep News for simplicity
        main = f'''{page_hero(p, [(index_label, index_href), (title[:60], None)], esc(title), '', lang=lang)}
  <section class="section"><div class="wrap">
    <article class="article prose">{body}</article>
    <div class="article-foot"><a href="{index_href}">{esc(L['back'])} ←</a></div>
  </div></section>'''
        # flip arrow for LTR via CSS; keep char
        if lang == 'en':
            main = main.replace('←', '→')
        fa_path = 'news/' if lang == 'en' else 'news/'  # posts not 1:1 mapped
        html = page(p, 'news', title, desc, main, lang=lang, fa_path=fa_path, canonical_path=root + site_path)
        write(rel, html)


def _write_post_index(write, lang, site_path, cur, label, items):
    L = LANGS[lang]
    root = L['root']
    rel = root + site_path + 'index.html'
    depth = _depth(rel)
    p = _prefix(depth)
    cards = []
    for wp in items:
        slug = _slug_decode(wp.get('slug') or str(wp['id']))
        title = strip_tags(wp.get('title', {}).get('rendered', ''))
        desc = strip_tags(wp.get('excerpt', {}).get('rendered', ''))[:160]
        href = f'../{slug}/' if site_path else f'{slug}/'
        # from latest-news/ to /en/slug/ → ../slug/
        href = f'{p}{root}{slug}/'
        cards.append(
            f'<a class="post-card reveal" href="{href}" data-name="{esc(title)}">'
            f'<div class="ph txt"><img src="{p}assets/img/abadis-logo-teal.png" width="658" height="309" alt="" loading="lazy"></div>'
            f'<div class="body"><h3>{esc(title)}</h3><p>{esc(desc)}</p>'
            f'<span class="go">{esc(L["read_more"])}</span></div></a>'
        )
    main = f'''{mosaic_hero(p, [(label, None)], L['brand'], f'<em>{esc(label)}</em>', '', label=label, lang=lang)}
  <section class="section"><div class="wrap">
    <div class="list-tools"><input class="search" type="search" placeholder="{esc(L['search'])}" aria-label="{esc(L['search'])}" data-filter="#postGrid">
    <span class="count" data-count-for="#postGrid">{len(items)} {esc(L['count_unit'])}</span></div>
    <div class="post-grid" id="postGrid" data-paged="12">{''.join(cards)}</div>
    <p class="empty-msg" hidden>{esc(L['empty'])}</p>
  </div></section>'''
    fa = 'news/' if 'news' in site_path or 'اخبار' in site_path or 'latest' in site_path else 'articles/'
    html = page(p, cur, label, label, main, lang=lang, fa_path=fa, canonical_path=root + site_path)
    write(rel, html)


def build_lang(write, lang: str):
    pages = load_lang_pages(lang)
    paths = EN_PAGE_PATHS if lang == 'en' else AR_PAGE_PATHS
    skip = EN_SKIP_SLUGS if lang == 'en' else AR_SKIP_SLUGS
    built = []
    gaps = []

    # Build mapped pages
    for slug, site_path in paths.items():
        wp = page_by_slug(pages, slug)
        if not wp:
            # try alternate slug encodings
            for cand in pages:
                if _slug_decode(cand.get('slug') or '') == slug:
                    wp = cand; break
        if not wp:
            gaps.append(f'{lang}:{slug}')
            continue
        # cur key for nav highlight
        cur = 'about'
        for k, h, _ in NAV[lang]:
            if h == site_path or (site_path and site_path.startswith(h.rstrip('/') + '/')):
                cur = k; break
        if site_path.startswith('products/') or site_path in ('suction-tube/', 'كيس-الشفط/', 'أنبوب-الشفط/'):
            cur = 'products'
        if 'news' in site_path or 'blog' in site_path or 'اخبار' in site_path:
            cur = 'news' if 'blog' not in site_path else 'articles'
        chip = LANGS[lang]['brand']
        rel = render_content_page(write, lang, site_path, wp, cur, chip)
        built.append(rel)

    # Also build any remaining non-skipped pages not in map (rare)
    for wp in pages:
        slug = _slug_decode(wp.get('slug') or '')
        if slug in skip or slug in paths:
            continue
        # skip if already covered
        gaps.append(f'{lang}:unmapped:{slug}')

    build_posts(write, lang)
    return built, gaps


def build(write):
    report = {
        'post_url_scheme': {
            'en': '/en/<post-slug>/',
            'ar': '/arabic/<post-slug>/',
            'note': 'Matches live WP post slugs (Unicode allowed on AR).',
        },
        'en_digits': 'system local() fonts via @font-face KalamehLatinDigits unicode-range U+0030-0039',
        'en_built': [], 'ar_built': [],
        'source_gaps': {
            'en_missing_vs_fa': GAPS['en_missing'],
            'ar_missing_vs_fa': GAPS['ar_missing'],
        },
        'build_gaps': [],
    }
    b, g = build_lang(write, 'en')
    report['en_built'] = b; report['build_gaps'] += g
    b, g = build_lang(write, 'ar')
    report['ar_built'] = b; report['build_gaps'] += g
    out = DATA / 'i18n-build-report.json'
    report['en_posts'] = len(load_lang_posts('en'))
    report['ar_posts'] = len(load_lang_posts('ar'))
    json.dump(report, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print('i18n report', out)
    print('EN pages', len(report['en_built']), 'posts', report['en_posts'])
    print('AR pages', len(report['ar_built']), 'posts', report['ar_posts'])
