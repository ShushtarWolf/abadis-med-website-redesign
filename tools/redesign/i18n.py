"""i18n helpers for FA / EN / AR static redesign pages.

Post URL scheme (documented): `/en/<post-slug>/` and `/arabic/<post-slug>/`
(matching live WP slugs; AR may include Unicode path segments).
"""
from __future__ import annotations
import json, pathlib, re, urllib.parse as u
from html import escape, unescape
from lib import SITE_ORIGIN

DATA = pathlib.Path(__file__).resolve().parent / 'data'

LANGS = {
    'fa': {
        'lang': 'fa-IR', 'dir': 'rtl', 'root': '', 'og_locale': 'fa_IR',
        'brand': 'مخازن طبی آبادیس',
        'home_label': 'خانه',
        'skip': 'پرش به محتوا',
        'nav_aria': 'منوی اصلی',
        'menu_aria': 'منو',
        'theme_aria': 'حالت نمایش',
        'theme_title': 'تغییر حالت نمایش',
        'lang_aria': 'زبان',
        'footer_menu': 'منو',
        'footer_more': 'بیشتر',
        'footer_contact': 'تماس',
        'footer_address': 'نشانی',
        'footer_blurb': 'با ما در ارتباط باشید...',
        'footer_copy': 'کلیه حقوق مادی و معنوی این وبسایت متعلق است به: مخازن طبی آبادیس · نسخهٔ پیش‌نمایش بازطراحی',
        'contact_center': 'مرکز تماس:',
        'email': 'پست الکترونیک:',
        'whatsapp': 'واتس‌اپ:',
        'addr_hq': 'نشانی دفتر مرکزی:',
        'addr_factory': 'نشانی کارخانه:',
        'addr_hq_val': 'ایران، تهران، قیطریه، خیابان اندرزگو، پلاک 104، واحد2',
        'addr_factory_val': 'ایران،تهران،شهرک صنعتی شمس آباد، بلوار گلستان، کوچه گلشن ۱۹،پلاک۱۷',
        'read_more': 'ادامه مطلب',
        'back': 'بازگشت',
        'news_tag': 'خبر',
        'article_tag': 'مقاله',
        'search': 'جست و جو',
        'count_unit': 'مطلب',
        'empty': 'موردی یافت نشد.',
        'lb_aria': 'گالری تصاویر',
        'lb_close': 'بستن',
        'lb_prev': 'تصویر قبلی',
        'lb_next': 'تصویر بعدی',
    },
    'en': {
        'lang': 'en', 'dir': 'ltr', 'root': 'en/', 'og_locale': 'en_US',
        'brand': 'Abadis Medical Reservoirs',
        'home_label': 'Home',
        'skip': 'Skip to content',
        'nav_aria': 'Main menu',
        'menu_aria': 'Menu',
        'theme_aria': 'Display mode',
        'theme_title': 'Change theme',
        'lang_aria': 'Language',
        'footer_menu': 'Menu',
        'footer_more': 'More',
        'footer_contact': 'Contact',
        'footer_address': 'Address',
        'footer_blurb': 'Get in touch with us...',
        'footer_copy': 'All rights reserved: Abadis Medical Reservoirs · redesign preview',
        'contact_center': 'Call center:',
        'email': 'Email:',
        'whatsapp': 'WhatsApp:',
        'addr_hq': 'Head office:',
        'addr_factory': 'Factory:',
        'addr_hq_val': 'Iran, Tehran, Qeytarieh, Andarzgoo St., No. 104, Unit 2',
        'addr_factory_val': 'Iran, Tehran, Shamsabad Industrial Town, Golestan Blvd, Golshan 19, No. 17',
        'read_more': 'Read more',
        'back': 'Back',
        'news_tag': 'News',
        'article_tag': 'Article',
        'search': 'Search',
        'count_unit': 'items',
        'empty': 'No results.',
        'lb_aria': 'Image gallery',
        'lb_close': 'Close',
        'lb_prev': 'Previous image',
        'lb_next': 'Next image',
    },
    'ar': {
        'lang': 'ar', 'dir': 'rtl', 'root': 'arabic/', 'og_locale': 'ar_AR',
        'brand': 'خزانات طبي آباديس',
        'home_label': 'الرئيسية',
        'skip': 'تخطي إلى المحتوى',
        'nav_aria': 'القائمة الرئيسية',
        'menu_aria': 'القائمة',
        'theme_aria': 'وضع العرض',
        'theme_title': 'تغيير السمة',
        'lang_aria': 'اللغة',
        'footer_menu': 'القائمة',
        'footer_more': 'المزيد',
        'footer_contact': 'اتصل',
        'footer_address': 'العنوان',
        'footer_blurb': 'تواصل معنا...',
        'footer_copy': 'جميع الحقوق محفوظة: خزانات طبي آباديس · معاينة إعادة التصميم',
        'contact_center': 'مركز الاتصال:',
        'email': 'البريد الإلكتروني:',
        'whatsapp': 'واتساب:',
        'addr_hq': 'عنوان المكتب الرئيسي:',
        'addr_factory': 'عنوان المصنع:',
        'addr_hq_val': 'إيران، طهران، قيطريه، شارع أندرزغو، رقم 104، وحدة 2',
        'addr_factory_val': 'إيران، طهران، مدينة شمس آباد الصناعية، بوليفارد گلستان، گلشن ۱۹، رقم ۱۷',
        'read_more': 'اقرأ المزيد',
        'back': 'عودة',
        'news_tag': 'خبر',
        'article_tag': 'مقال',
        'search': 'بحث',
        'count_unit': 'مواد',
        'empty': 'لا توجد نتائج.',
        'lb_aria': 'معرض الصور',
        'lb_close': 'إغلاق',
        'lb_prev': 'الصورة السابقة',
        'lb_next': 'الصورة التالية',
    },
}

# Main nav: (key, href under lang root, label)
NAV = {
    'fa': [
        ('about', 'about/', 'آشنایی با ما'),
        ('products', 'products/', 'محصولات'),
        ('news', 'news/', 'آخرین اخبار'),
        ('dealers', 'dealers/', 'لیست نمایندگان'),
        ('csr', 'csr/', 'توسعه پایدار'),
        ('articles', 'articles/', 'مقالات'),
        ('contact', 'contact/', 'ارتباط با ما'),
        ('calculator', 'calculator/', 'محاسبه‌گر'),
    ],
    'en': [
        ('about', 'about-us/', 'About us'),
        ('products', 'products/', 'Products'),
        ('news', 'latest-news/', 'News'),
        ('dealers', 'representatives/', 'Representatives'),
        ('csr', 'csr/', 'CSR'),
        ('articles', 'blog/', 'Blog'),
        ('contact', 'contact-us/', 'Contact Us'),
        ('calculator', 'calculator/', 'Calculator'),
    ],
    'ar': [
        ('about', 'من-نحن/', 'من نحن'),
        ('products', 'منتجات/', 'منتجات'),
        ('news', 'الاخبار/', 'الاخبار'),
        ('dealers', 'قائمة-الممثلين/', 'قائمة الممثلين'),
        ('contact', 'اتصل-بنا/', 'اتصل بنا'),
        ('calculator', 'الحوسبة/', 'الحوسبة'),
        ('faq', 'پرسش-های-متداول/', 'پرسش های متداول'),
        ('install', 'دليل-التركيب/', 'دليل التركيب'),
    ],
}

SECONDARY = {
    'fa': [
        ('customers', 'customers/', 'مشتریان ما'),
        ('experiences', 'experiences/', 'تجارب ما'),
        ('downloads', 'downloads/', 'مرکز دانلود'),
        ('install', 'install-guide/', 'راهنمای نصب'),
        ('faq', 'faq/', 'پرسش های متداول'),
        ('careers', 'careers/', 'فرصت های همکاری'),
        ('zagros', 'csr/', 'نجات زاگرس'),
    ],
    'en': [
        ('customers', 'our-customers/', 'Our customers'),
        ('downloads', 'center-download/', 'Download Center'),
        ('install', 'installation-manual/', 'Installation Manual'),
        ('faq', 'faqs/', 'FAQs'),
        ('collab', 'collaboration-opportunities/', 'Collaboration'),
        ('sdgs', 'sdgs/', 'SDGs'),
    ],
    'ar': [
        ('downloads', 'مركز-التنزيل/', 'مركز التنزيل'),
        ('products_other', 'منتجات-اخری/', 'منتجات اخری'),
        ('suction', 'كيس-الشفط/', 'كيس الشفط'),
    ],
}

# Pages that exist only in some languages (gaps vs FA redesign)
GAPS = {
    'en_missing': ['careers/jobs (موقعیت‌های شغلی)', 'experiences (تجارب ما)'],
    'ar_missing': [
        'csr', 'sdgs', 'customers (our-customers)', 'careers / collaboration-opportunities',
        'experiences', 'articles/blog',
    ],
}


def load_map():
    return json.load(open(DATA / 'i18n-map.json', encoding='utf-8'))


def strip_tags(h):
    return re.sub(r'\s+', ' ', unescape(re.sub(r'<[^>]+>', ' ', h or ''))).strip()


# Live WP paths that ship under a different local folder (products hub, skipped slugs, FA↔EN).
_I18N_HREF_ALIASES = {
    '/en/suction-bag/': 'en/products/suction-bag/',
    '/en/base-and-holder/': 'en/products/base-and-holder/',
    '/en/filters/': 'en/products/filters/',
    '/en/canisters/': 'en/products/canisters/',
    '/en/canister-2/': 'en/products/canisters/',
    '/en/connections/': 'en/products/connections/',
    '/en/products/oral-hygiene/': 'en/products/other-products/',
    '/en/canister-installation/': 'en/installation-manual/',
    '/en/user-manuals/': 'en/installation-manual/',
    '/en/catalogue/': 'en/center-download/',
    '/arabic/كيسه-ساكشن/': 'arabic/كيس-الشفط/',
    '/arabic/کیسه-ساکشن/': 'arabic/كيس-الشفط/',
    '/arabic/فيلترها/': 'arabic/الفلتر/',
    '/arabic/فیلترها/': 'arabic/الفلتر/',
    '/arabic/الوصلة/': 'arabic/الوصلات/',
    '/arabic/تماس-با-ما/': 'arabic/اتصل-بنا/',
    '/about/': 'about/',
    '/articles/': 'articles/',
    '/calculator/': 'calculator/',
    '/careers/': 'careers/',
    '/contact/': 'contact/',
    '/csr/': 'csr/',
    '/customers/': 'customers/',
    '/dealers/': 'dealers/',
    '/downloads/': 'downloads/',
    '/faq/': 'faq/',
    '/install-guide/': 'install-guide/',
    '/news/': 'news/',
    '/products/': 'products/',
}

_local_paths_cache = None


def _local_site_paths():
    """Set of site-relative dirs that have index.html (e.g. 'en/about-us/', 'news/1124/')."""
    global _local_paths_cache
    if _local_paths_cache is not None:
        return _local_paths_cache
    from lib import SITE
    found = {''}
    if SITE.is_dir():
        for idx in SITE.rglob('index.html'):
            rel = idx.relative_to(SITE).parent.as_posix()
            found.add('' if rel == '.' else rel.rstrip('/') + '/')
    _local_paths_cache = found
    return found


def _norm_abadis_path(url: str):
    """Return (path_with_slash, fragment) for abadis-med.com URLs, else None."""
    if not url:
        return None
    url = url.strip()
    if url.startswith('//'):
        url = 'https:' + url
    m = re.match(r'^(?:https?:)?//(?:www\.)?abadis-med\.com(/[^?#]*)?(?:\?[^#]*)?(#.*)?$', url, re.I)
    if not m:
        return None
    path = u.unquote(m.group(1) or '/')
    if not path.endswith('/') and '.' not in path.rsplit('/', 1)[-1]:
        path += '/'
    return path, (m.group(2) or '')


def map_i18n_href(url: str, lang: str, prefix: str) -> str | None:
    """Map an abadis-med.com href to a site-relative path, or None to keep as-is.

    Keeps wp-content asset URLs (no local page). Rewrites pages/posts that exist
    under /en/, /arabic/, or FA site paths.
    """
    parsed = _norm_abadis_path(url)
    if not parsed:
        return None
    path, frag = parsed
    if path.startswith('/wp-content/') or '/wp-content/' in path or path.startswith('/en/wp-content/') or path.startswith('/arabic/wp-content/'):
        return None
    # Drop Elementor junk hashes; keep real in-page anchors
    if frag.startswith('#elementor') or frag in ('#reply-title',):
        frag = ''

    local = None
    locals_ = _local_site_paths()
    root = LANGS.get(lang, LANGS['fa'])['root']
    # Site home on live → language home
    if path == '/':
        local = root
    elif path in _I18N_HREF_ALIASES:
        local = _I18N_HREF_ALIASES[path]
    else:
        cand = path.lstrip('/')  # e.g. en/about-us/
        if cand in locals_:
            local = cand
        elif not path.startswith('/en/') and not path.startswith('/arabic/'):
            # FA or bare path → lib.internal (PAGE_MAP / POST_MAP)
            try:
                from lib import internal
                hit = internal('https://abadis-med.com' + path)
            except Exception:
                hit = None
            if hit is not None:
                local = hit
            elif cand in locals_:
                local = cand
            elif root and (root + cand) in locals_:
                # bare EN/AR slug without lang prefix
                local = root + cand

    if local is None and root:
        trial = root + path.lstrip('/')
        if trial in locals_:
            local = trial
    if local is None:
        return None
    if local == '':
        href = prefix if prefix else './'
    else:
        href = prefix + local
    if frag and '#' not in href:
        href += frag
    return href


def _ensure_img_alt(tag: str, lang: str) -> str:
    """Add a descriptive alt when the attribute is missing entirely."""
    if re.search(r'\balt\s*=', tag, re.I):
        return tag
    title = re.search(r'\btitle=(["\'])(.*?)\1', tag, re.I)
    aria = re.search(r'\baria-label=(["\'])(.*?)\1', tag, re.I)
    alt = ''
    if title and title.group(2).strip():
        alt = title.group(2).strip()
    elif aria and aria.group(2).strip():
        alt = aria.group(2).strip()
    else:
        # Derive from filename when possible
        src = re.search(r'\bsrc=(["\'])(.*?)\1', tag, re.I)
        if src:
            base = u.unquote(src.group(2).rstrip('/').rsplit('/', 1)[-1])
            base = re.sub(r'\.[a-z0-9]+$', '', base, flags=re.I)
            base = re.sub(r'[-_]+', ' ', base).strip()
            if base and base.lower() not in ('dummy', 'placeholder', 'image', 'img'):
                alt = base
        if not alt:
            alt = {
                'en': 'Abadis Med',
                'ar': 'آبادیس مد',
                'fa': 'مخازن طبی آبادیس',
            }.get(lang, 'Abadis Med')
    alt_esc = alt.replace('&', '&amp;').replace('"', '&quot;')
    if tag.endswith('/>'):
        return tag[:-2] + f' alt="{alt_esc}" />'
    if tag.endswith('>'):
        return tag[:-1] + f' alt="{alt_esc}">'
    return tag + f' alt="{alt_esc}"'


def meta_description(title: str, excerpt_html: str, content_html: str = '', lang: str = 'fa') -> str:
    """Non-empty meta description: excerpt → content lead → title."""
    def scrub(s: str) -> str:
        s = re.sub(r'\[[^\]]+\]', ' ', s or '')  # strip WP/Avia shortcodes
        s = strip_tags(s)
        s = re.sub(r'[\xa0\s]+', ' ', s).strip(' \t\n\r\u200c·-|')
        return s
    d = scrub(excerpt_html or '')
    if len(d) < 12:
        d = scrub(content_html or '')
    if len(d) < 12:
        brand = LANGS.get(lang, LANGS['fa'])['brand']
        d = f'{strip_tags(title)} — {brand}'.strip(' —')
    return d[:180]


def clean_html(html: str, lang: str = 'en', prefix: str = '../') -> str:
    if not html:
        return ''
    h = html
    h = re.sub(r'<script\b[^>]*>.*?</script>', '', h, flags=re.S | re.I)
    h = re.sub(r'<style\b[^>]*>.*?</style>', '', h, flags=re.S | re.I)
    h = re.sub(r'<noscript\b[^>]*>.*?</noscript>', '', h, flags=re.S | re.I)
    h = re.sub(r'<!--.*?-->', '', h, flags=re.S)
    h = re.sub(r'\sstyle=(["\'])(.*?)\1', '', h, flags=re.I | re.S)
    h = re.sub(r'\sdata-(?:elementor|settings|widget_type|id|model-cid)[^=]*=(["\'])(.*?)\1', '', h, flags=re.I)
    h = re.sub(r'\sclass=(["\'])([^"\']*elementor[^"\']*)\1', '', h, flags=re.I)
    h = re.sub(r'\sclass=(["\'])\s*\1', '', h)
    # WP sometimes wraps address fragments as http://no.105/ — unwrap to plain text
    h = re.sub(
        r'<a\b[^>]*\bhref=(["\'])https?://no\.\d+/?\1[^>]*>(.*?)</a>',
        r'\2',
        h,
        flags=re.I | re.S,
    )
    # Phone numbers mis-linked as http://02192001017 → tel:02192001017
    h = re.sub(
        r'\bhref=(["\'])https?://(0\d{6,14})\1',
        r'href=\1tel:\2\1',
        h,
        flags=re.I,
    )
    h = re.sub(r'\sdata-wplink-url-error=(["\'])[^"\']*\1', '', h, flags=re.I)

    def href_sub(m):
        q, url = m.group(1), m.group(2)
        new = map_i18n_href(unescape(url), lang, prefix)
        if new is None:
            return m.group(0)
        return f'href={q}{new}{q}'

    h = re.sub(
        r'''\bhref=(["'])((?:https?:)?//(?:www\.)?abadis-med\.com[^"']*)\1''',
        href_sub,
        h,
        flags=re.I,
    )

    def img_sub(m):
        return _ensure_img_alt(m.group(0), lang)

    h = re.sub(r'<img\b[^>]*>', img_sub, h, flags=re.I)
    return h.strip()


def asset_prefix(lang: str, depth: int) -> str:
    """Relative prefix from a page at `depth` folders under site/ to site root assets."""
    # depth 0 = site/index.html → ''
    # depth 1 = site/about/ → '../'
    # For en/about-us/ depth=2 → '../../'
    root = LANGS[lang]['root']
    # pages live under root; depth includes root segments
    return '../' * depth


def depth_for(rel: str) -> int:
    rel = rel.strip('/')
    if not rel or rel.endswith('.html') and '/' not in rel:
        return 0
    # en/about-us/index.html → 2
    parts = pathlib.PurePosixPath(rel).parts
    # drop index.html
    parts = [p for p in parts if p != 'index.html']
    return len(parts)


def switcher_html(lang: str, fa_path: str, p: str) -> str:
    """Language switcher: FA · EN · AR with full-name title/aria-label. No target=_blank."""
    m = load_map()
    key = fa_path if fa_path.endswith('/') or fa_path == '' else fa_path + '/'
    if key == '/':
        key = ''
    entry = m.get(key) or {}
    # sdgs/ synthetic key: use csr/ pair for FA switcher context
    if not entry and key == 'sdgs/':
        entry = m.get('csr/') or {}
    defaults = {'fa': '', 'en': 'en/', 'ar': 'arabic/'}
    labels = {'fa': 'FA', 'en': 'EN', 'ar': 'AR'}
    names = {'fa': 'فارسی', 'en': 'English', 'ar': 'العربية'}
    parts = []
    for i, code in enumerate(('fa', 'en', 'ar')):
        if i:
            parts.append('<span class="lang-sep" aria-hidden="true">·</span>')
        rel = entry.get(code) if code in entry else None
        if rel is None:
            rel = defaults[code]
        href = p + rel
        cur = ' aria-current="true"' if code == lang else ''
        hl = LANGS[code]['lang']
        name = escape(names[code])
        parts.append(
            f'<a class="lang-link" href="{href}" hreflang="{hl}" lang="{hl}" '
            f'title="{name}" aria-label="{name}"{cur}>{labels[code]}</a>'
        )
    return f'<nav class="lang-switch" aria-label="{escape(LANGS[lang]["lang_aria"])}">{"".join(parts)}</nav>'


def hreflang_tags(fa_path: str, p: str) -> str:
    """Root-relative hreflang so static preview links stay on-site (not abadis-med.com)."""
    m = load_map()
    key = fa_path if fa_path == '' or fa_path.endswith('/') else fa_path + '/'
    entry = m.get(key)
    if not entry:
        return ''
    tags = []
    for code, hreflang in (('fa', 'fa-IR'), ('en', 'en'), ('ar', 'ar')):
        rel = entry.get(code)
        if rel is None:
            continue
        href = '/' + rel.lstrip('/')
        tags.append(f'<link rel="alternate" hreflang="{hreflang}" href="{href}">')
    # x-default → FA URL (entry["fa"] may differ from map key, e.g. sdgs/ → csr/)
    fa_rel = entry.get('fa')
    if fa_rel is not None:
        tags.append(f'<link rel="alternate" hreflang="x-default" href="/{fa_rel.lstrip("/")}">')
    return '\n'.join(tags)


def fa_path_from_site_rel(rel: str) -> str:
    """Best-effort FA path key for a generated page relative path."""
    rel = rel.replace('\\', '/').lstrip('./')
    if rel.endswith('index.html'):
        rel = rel[:-10]
    if not rel or rel == '/':
        return ''
    if not rel.endswith('/'):
        rel += '/'
    # strip en/ arabic/
    if rel.startswith('en/'):
        # reverse lookup
        m = load_map()
        for k, v in m.items():
            if v.get('en') == rel:
                return k
        return ''
    if rel.startswith('arabic/'):
        m = load_map()
        for k, v in m.items():
            if v.get('ar') == rel:
                return k
        return ''
    return rel
