"""Products hub + six product family pages (suction bag page is hand-built and kept)."""
import re
from lib import PAGES, esc, strip_tags, best_img, rewrite_html
from layout import page, page_hero, section_mark
from render import table, gallery_link, secs

FAMILIES = [  # slug, live path, hub title (verbatim from live hub), hub image, local fallback image
    ('suction-bag', '/محصولات/کیسه-ساکشن/', 'کیسه های ساکشن', 'https://abadis-med.com/wp-content/uploads/2022/12/کیسه-ساکشن.jpg', 'assets/img/p/p2-main.webp'),
    ('stand', '/محصولات/پایه/', 'پایه و نگهدارنده', 'https://abadis-med.com/wp-content/uploads/2022/12/پایه-ترولی.jpg', 'assets/img/p/p1-g3-t.webp'),
    ('filters', '/محصولات/فیلترها/', 'فیلتر', 'https://abadis-med.com/wp-content/uploads/2022/12/فیلتر1-2-845x684-1.jpg', 'assets/img/filters/anti-1-t.webp'),
    ('suction-tube', '/محصولات/ساکشن-تیوب/', 'ساکشن تیوب', 'https://abadis-med.com/wp-content/uploads/2023/02/7e83722522e8aeb7512b7075311316b7__m8ULku2SAG__1-1-300x300.jpg', None),
    ('canister', '/محصولات/مخزن/', 'مخزن', 'https://abadis-med.com/wp-content/uploads/2022/12/AMR_4901.jpg', 'assets/img/p/p3-g1-t.webp'),
    ('connectors', '/محصولات/اتصالات/', 'اتصالات', 'https://abadis-med.com/wp-content/uploads/2022/12/اتصالات-845x684-1.jpg', 'assets/img/p/p2-g3-t.webp'),
    ('other', '/محصولات/سایر-محصولات/', 'سایر محصولات',
     'https://abadis-med.com/wp-content/uploads/2022/12/19-1024x880.jpg', None),
]
# Fallback photos when the item's own image was never archived by the Wayback Machine.
# Only images that verifiably show that exact product are used (family hub photo / phase-1 asset).
FALLBACK = {
    'msk': ['https://abadis-med.com/wp-content/uploads/2022/12/AMR_4901.jpg'],
    'sdv': ['https://abadis-med.com/wp-content/uploads/2022/12/ساکشن-دیواری-بزرگسال-1030x1030-1.jpg'],
    'paye': ['https://abadis-med.com/wp-content/uploads/2022/12/پایه-ترولی.jpg'],
    'negahdarande': ['https://abadis-med.com/wp-content/uploads/2022/12/نگهدارنده-لوله-تراشه-1030x1030-1.jpg'],
    'anti': ['local:assets/img/filters/anti-1.webp', 'local:assets/img/filters/anti-2.webp'],
    'ght': ['local:assets/img/filters/stop-1.webp', 'local:assets/img/filters/stop-2.webp'],
    'mot': ['local:assets/img/filters/porous-1.webp'],
}
LOCAL_DIMS = {}
def local_link(p, path, gid, alt, cls='', zoom='نمایش بزرگ‌تر'):
    from PIL import Image
    from lib import SITE
    w, h = Image.open(SITE / path).size
    t = path.replace('.webp', '-t.webp')
    tw, th = Image.open(SITE / t).size if (SITE / t).exists() else (w, h)
    if not (SITE / t).exists(): t = path
    return (f'<a href="{p}{path}" data-gallery="{gid}" data-w="{w}" data-h="{h}" aria-label="{esc(zoom)}: {esc(alt)}">'
            f'<img src="{p}{t}" width="{tw}" height="{th}" loading="lazy" decoding="async" alt="{esc(alt)}"></a>')
SUCTION_BAG_ITEMS = ['کیسه ساکشن ۱ لیتری', 'کیسه ساکشن ۲ لیتری', 'کیسه ساکشن ۳ لیتری']

def pick(b):
    h = b.get('href') or ''
    if h.startswith('http') and re.search(r'\.(jpe?g|png|webp)$', h) and best_img(h): return h
    return b['src']

def norm(s): return re.sub(r'[\s\u200c\u200b():]+', '', strip_tags(s))

def any_img(url):
    if not url: return None
    for w in (640, 900, 480, 1000, 1400, 1600):
        r = best_img(url, w)
        if r: return r
    return None

def _overlaps(a, b):
    na, nb = norm(a), norm(b)
    return bool(na and nb and (na in nb or nb in na))

_LABEL = re.compile(
    r'^(کاربردها|مزایا|موارد مصرف|موارد استفاده|ویژگی‌ها|ویژگی ها|ویژگی های محصول|سایز|بسته‌بندی|بسته بندی|'
    r'جنس|اجزاء|اجزای محصول|مکان استفاده محصول|حجم ساکشن|نوع جنس|کاربرد|ظرفیت|مشخصات محصول|ابعاد محصول)$')

def _demote(html):
    """Product title is the h2. Inner headings, including label lines, sit under it."""
    for src, dst in (('h4', 'h5'), ('h3', 'h4'), ('h2', 'h3'), ('h1', 'h3')):
        html = re.sub(fr'<{src}(\b[^>]*)>', f'<{dst}\\1>', html, flags=re.I)
        html = re.sub(fr'</{src}>', f'</{dst}>', html, flags=re.I)
    def repl(m):
        inner = m.group(1)
        parts = re.split(r'<br\s*/?>', inner, maxsplit=1, flags=re.I)
        text = strip_tags(parts[0]).strip()
        core = re.sub(r'\s+', ' ', text).rstrip(':：').strip()
        if not core or len(text) > 80:
            return m.group(0)
        if not (_LABEL.match(core) or ((text.endswith(':') or text.endswith('：')) and len(core) < 48)):
            return m.group(0)
        rest = f'<p>{parts[1].strip()}</p>' if len(parts) > 1 and strip_tags(parts[1]).strip() else ''
        return f'<h3>{esc(core)}</h3>{rest}'
    return re.sub(r'<p>(.*?)</p>', repl, html, flags=re.S)

def family(path):
    bl = PAGES[path]['blocks']
    h1 = next((b['text'] for b in bl if b['t'] == 'h' and b.get('lvl') == 1), PAGES[path]['title'].split('»')[0].strip())
    anchors = [(b['text'], b['href'][1:]) for b in bl if b['t'] == 'h' and (b.get('href') or '').startswith('#')]
    items = []
    for sid, bs in secs(bl):
        if not any(b['t'] == 'html' for b in bs) or not any(b['t'] in ('img', 'table') for b in bs): continue
        items.append(bs)
    out = []
    for i, bs in enumerate(items):
        title, aid = anchors[i] if i < len(anchors) else (None, f'item{i+1}')
        htmls = [b['html'] for b in bs if b['t'] == 'html' and b.get('html')]
        body = '\n'.join(htmls).lstrip()
        m = re.match(r'(?:<p>\s*)?<strong>(.*?)</strong>\s*(?:</p>)?', body, re.S)
        if m:
            lead = strip_tags(m.group(1)).strip()
            if title is None: title = lead
            if _overlaps(lead, title or ''):
                body = body[m.end():].lstrip()
        m2 = re.match(r'([^<]+)', body)
        if m2 and title and _overlaps(m2.group(1).strip(), title):
            body = body[m2.end():].lstrip()
        out.append({'id': aid, 'title': title or '', 'html': body,
                    'imgs': [(pick(b), b.get('alt', '')) for b in bs if b['t'] == 'img'],
                    'tables': [b['rows'] for b in bs if b['t'] == 'table']})
    return h1, out

ZOOM = {'fa': 'نمایش بزرگ‌تر', 'en': 'Larger view', 'ar': 'عرض أكبر'}
MISSING = {
    'fa': 'تصویر این محصول در نسخهٔ آرشیوشدهٔ سایت موجود نبود',
    'en': 'No separate photo of this product is in the archived site',
    'ar': 'لا توجد صورة مستقلة لهذا المنتج في أرشيف الموقع',
}

def product_block(p, it, lang='fa'):
    gid = it['id']
    zoom = ZOOM.get(lang, ZOOM['fa'])
    links = []
    if not it.get('force_missing'):
        links = [gallery_link(p, u_, gid, a or it['title'], 900, 1600, zoom=zoom) for u_, a in it['imgs']]
        links = [l for l in links if l]
        if not links:
            for src in FALLBACK.get(gid, []):
                if src.startswith('local:'): links.append(local_link(p, src[6:], gid, it['title'], zoom=zoom))
                else:
                    l = gallery_link(p, src, gid, it['title'], 900, 1600, zoom=zoom)
                    if l: links.append(l)
    if links:
        main = links[0].replace('<a ', '<a class="gal-main" ', 1)
        thumbs = ''.join(links[1:])
        media = f'<div class="size-media">{main}{f"<div class=gal-thumbs>{thumbs}</div>" if thumbs else ""}</div>'
    else:
        media = (f'<div class="size-media"><div class="gal-main gal-missing">'
                 f'<img src="{p}assets/img/abadis-logo-teal.png" width="658" height="309" alt="">'
                 f'<span>{esc(MISSING.get(lang, MISSING["fa"]))}</span></div></div>')
    tables = ''.join(table(t) for t in it['tables'])
    body = rewrite_html(it['html'], p) if lang == 'fa' else it['html']
    if lang == 'fa':
        body = _demote(body)
    import solutions_arch as S
    return f'''    <article class="ptab size-block" id="{esc(it["id"])}">
      <h2>{esc(it["title"])}{S.badge(lang, S.status_for(it["id"]))}</h2>
      <div class="size-grid">
        {media}
        <div class="size-info prose">{body}</div>
      </div>
      {tables}
    </article>'''

def related(p, here):
    cards = []
    for slug, path, title, im, fb in FAMILIES:
        if slug == here: continue
        r = best_img(im, 480) if im else None
        src = (p + r['src']) if r else (p + fb if fb else None)
        ph = f'<div class="ph"><img src="{src}" alt="" loading="lazy" decoding="async"></div>' if src else '<div class="ph txt">آبادیس</div>'
        cards.append(f'<a class="mini-card" href="../{slug}/">{ph}<strong>{esc(title)}</strong></a>')
    return f'''  <section class="section section--alt" id="more"><div class="wrap">
    <h2 class="reveal" style="margin-bottom:20px">سایر محصولات آبادیس</h2>
    <div class="mini-grid">{''.join(cards)}</div>
  </div></section>'''

INQUIRY = '''  <section class="section" id="inquiry"><div class="wrap">
    <div class="cta-band reveal">
      <h2>آماده سفارش برای مرکز درمانی شما</h2>
      <p>برای لیست قیمت، نمونه و هماهنگی نصب با تیم فروش مخازن طبی آبادیس در تماس باشید.</p>
      <div class="cta-actions"><a class="btn btn-light" href="tel:+982192001017">تماس با فروش</a><a class="btn btn-ghost" href="https://wa.me/989100145809" target="_blank" rel="noopener">درخواست نمونه در واتس‌اپ</a><a class="btn btn-ghost" href="../../export/#quote">درخواست قیمت / همکاری صادراتی</a></div>
    </div>
  </div></section>'''

UP = 'https://abadis-med.com/wp-content/uploads/'
CAT_ALL = (UP + '2024/12/کاتالوگ-جامع-آبادیس.pdf', 'کاتالوگ جامع آبادیس (PDF)')
DOCS = {  # real files linked from the live download centre
    'filters': [(UP + '2022/12/Filter-catalog-Fa.pdf', 'کاتالوگ فیلترها (PDF)'), CAT_ALL],
    'suction-tube': [(UP + '2026/01/کاتالوگ-ساکشن-تیوب-1.pdf', 'کاتالوگ ساکشن تیوب (PDF)'), CAT_ALL],
    'stand': [(UP + '2024/02/راهنمای-نصب-مخازن-بر-روی-پایه-ترولی.pdf', 'راهنمای نصب روی پایه ترولی (PDF)'),
              (UP + '2024/02/راهنمای-نصب-مخازن-بر-روی-پایه-پرتابل.pdf', 'راهنمای نصب روی پایه پرتابل (PDF)'),
              (UP + '2024/02/راهنمای-نصب-مخازن-بر-روی-کنسول.pdf', 'راهنمای نصب روی کنسول (PDF)'), CAT_ALL],
    'canister': [CAT_ALL], 'connectors': [CAT_ALL],
    'other': [(UP + '2022/12/endotracheal-tube-holder-catalog-Fa.pdf', 'کاتالوگ نگهدارنده لوله تراشه (PDF)'), CAT_ALL],
}
def doc_bar(slug, lang='fa'):
    docs = DOCS.get(slug) or []
    if not docs: return ''
    from product_copy import DOC_LABELS
    labels = DOC_LABELS.get(lang, {})
    links = ''.join(
        f'<a href="{esc(h)}" target="_blank" rel="noopener" data-track="catalogue_download">{esc(labels.get(t, t))}</a>'
        for h, t in docs)
    return f'''  <section class="section" id="docs" style="padding-top:0"><div class="wrap"><div class="doc-links">{links}</div></div></section>\n'''

# Products hub. The two category labels are Hamid's (Oct 2026).
# "By product" is the live hub families (data/pages.json "/محصولات/"), same titles and order.
# "By solution" lists systems those family pages already name (stand, canister, other).
# Boss notes and PHASE-1 do not define a second taxonomy; they list these families only.
HUB_UI = {
    'fa': dict(
        nav='دسته‌بندی محصولات', by_product='بر مبنای محصولات', by_solution='بر اساس راهکار',
        view='مشاهده ←',         h1='محصولات و راهکارهای آبادیس', title='محصولات و راهکارهای آبادیس',
        desc='از محصولات تخصصی ساکشن تا راهکارهای نوآورانه برای مراقبت ایمن‌تر و کارآمدتر',
        lead='از محصولات تخصصی ساکشن تا راهکارهای نوآورانه برای مراقبت ایمن‌تر و کارآمدتر',
        crumb='محصولات', alt_suffix=' آبادیس',
        docs=[('../downloads/', 'مرکز دانلود کاتالوگ‌ها'), ('../install-guide/', 'راهنمای نصب'), ('../calculator/', 'محاسبه‌گر صرفه‌جویی')],
        rel='products/index.html', prefix='../', fa_path='products/', canonical='products/',
    ),
    'en': dict(
        nav='Product categories', by_product='By product', by_solution='By solution',
        view='Find Out More',         h1='Abadis Products &amp; Solutions', title='Abadis Products & Solutions',
        desc='From specialised suction products to innovative solutions for safer, more efficient care.',
        lead='From specialised suction products to innovative solutions for safer, more efficient care.',
        crumb='Products', alt_suffix=' Abadis',
        docs=[('../center-download/', 'Download Center'), ('../installation-manual/', 'Installation Manual'), ('../calculator/', 'Savings calculator')],
        rel='en/products/index.html', prefix='../../', fa_path='products/', canonical='en/products/',
    ),
    'ar': dict(
        nav='تصنيف المنتجات', by_product='حسب المنتجات', by_solution='حسب الحلول',
        view='مشاهدة منتجاتنا',         h1='منتجات وحلول آباديس', title='منتجات وحلول آباديس',
        desc='من منتجات الشفط المتخصصة إلى حلول مبتكرة لرعاية أكثر أماناً وكفاءة.',
        lead='من منتجات الشفط المتخصصة إلى حلول مبتكرة لرعاية أكثر أماناً وكفاءة.',
        crumb='منتجات', alt_suffix=' آباديس',
        docs=[('../مركز-التنزيل/', 'مركز التنزيل'), ('../دليل-التركيب/', 'دليل التركيب'), ('../الحوسبة/', 'حاسبة التوفير')],
        rel='arabic/منتجات/index.html', prefix='../../', fa_path='products/', canonical='arabic/منتجات/',
    ),
}
# slug, href from the hub page, title, subtitle (FA subtitle is filled from the family pages)
HUB_FAMILIES = {
    'fa': [
        ('suction-bag', 'suction-bag/', 'کیسه های ساکشن'),
        ('stand', 'stand/', 'پایه و نگهدارنده'),
        ('filters', 'filters/', 'فیلتر'),
        ('suction-tube', 'suction-tube/', 'ساکشن تیوب'),
        ('canister', 'canister/', 'مخزن'),
        ('connectors', 'connectors/', 'اتصالات'),
        ('other', 'other/', 'سایر محصولات'),
    ],
    'en': [
        ('suction-bag', 'suction-bag/', 'Suction Bag', '1 Liter, 2 Liter, 3 Liter'),
        ('stand', 'base-and-holder/', 'Base and Holder', 'Trolley, wall clamp, rear part of the portable clamp'),
        ('filters', 'filters/', 'Filter', 'Antibacterial Filter(Viral Filter), Flow stopper filter, Sintered Filter'),
        ('suction-tube', '../suction-tube/', 'Suction tube', 'Suction Tube, Fingertip'),
        ('canister', 'canisters/', 'Canister', 'Suction Canisters, Wall Suction, Collection Cup, Fat Collection Canister System'),
        ('connectors', 'connections/', 'Connections', 'T connector, Connector, Silicone Slang, Regulator, ON/OFF valve, Accessories'),
        ('other', 'other-products/', 'Other Products', 'Suction Brush, Endotracheal Tube Holder, Disposable Kidney Dish, Splash-Vac'),
    ],
    'ar': [
        ('suction-bag', '../كيس-الشفط/', 'كيس الشفط', ''),
        ('stand', '../تثبیت/', 'تثبیت', 'قاعدة تثبيت شفط آباديس المحمولة (ترولي)، مشابك خزان الحائط، مشابك الخزان المحمول'),
        ('filters', '../الفلتر/', 'الفلتر', ''),
        ('suction-tube', '../أنبوب-الشفط/', 'أنبوب الشفط', ''),
        ('canister', '../خزانات/', 'خزانات', 'خزانات الشفط، الشفط الجداري، كوب جمع العينة، جهاز جمع الدهون'),
        ('connectors', '../الوصلات/', 'الوصلات', ''),
        ('other', '../منتجات-اخری/', 'منتجات اخری', 'فرشاة الشفط، حامل أنبوب القصبة، الوعاء الكلوي، Splash-Vac'),
    ],
}
# photo id, href from the hub, title, parent family
SOL_PHOTO = {
    'paye': 'https://abadis-med.com/wp-content/uploads/2022/12/11.jpg',
    'wallp': 'https://abadis-med.com/wp-content/uploads/2022/12/13.jpg',
    'sdv': 'https://abadis-med.com/wp-content/uploads/2022/12/ساکشن-دیواری-بزرگسال-1030x1030-1.jpg',
    'wallg': 'https://abadis-med.com/wp-content/uploads/2022/12/12.jpg',
    'mesvak': 'https://abadis-med.com/wp-content/uploads/2022/12/19-1024x880.jpg',
    'negahdarande': 'https://abadis-med.com/wp-content/uploads/2022/12/24-1024x683.jpg',
    'receiver': 'https://abadis-med.com/wp-content/uploads/2022/12/26.jpg',
}
SOLUTIONS = {
    'fa': [
        ('paye', 'stand/#paye', 'پایه ساکشن پرتابل (ترولی)', 'پایه و نگهدارنده'),
        ('wallp', 'stand/#wallp', 'پشت گیره مخزن پرتابل', 'پایه و نگهدارنده'),
        ('sdv', 'canister/#sdv', 'ساکشن دیواری', 'مخزن'),
        ('wallg', 'stand/#wallg', 'گیره و مخزن دیواری', 'پایه و نگهدارنده'),
        ('mesvak', 'other/#mesvak', 'مسواک ساکشن یکبارمصرف', 'سایر محصولات'),
        ('negahdarande', 'other/#negahdarande', 'نگهدارنده لوله تراشه', 'سایر محصولات'),
        ('receiver', 'other/#receiver', 'رسیور پزشکی یکبارمصرف', 'سایر محصولات'),
        ('splashvac', 'other/#splashvac', 'مکش سطحی چند منظوره (Splash-Vac)', 'سایر محصولات'),
    ],
    'en': [
        ('paye', 'base-and-holder/#paye', 'Trolleys', 'Base and Holder'),
        ('wallp', 'base-and-holder/#wallp', 'Rear part of the portable canister clamp', 'Base and Holder'),
        ('sdv', 'canisters/#sdv', 'Wall Suction', 'Canister'),
        ('wallg', 'base-and-holder/#wallg', 'Wall bracket', 'Base and Holder'),
        ('mesvak', 'other-products/#mesvak', 'Suction Brush', 'Other Products'),
        ('negahdarande', 'other-products/#negahdarande', 'Endotracheal Tube Holder', 'Other Products'),
        ('receiver', 'other-products/#receiver', 'Disposable Kidney Dish', 'Other Products'),
        ('splashvac', 'other-products/#splashvac', 'Splash-Vac', 'Other Products'),
    ],
    'ar': [
        ('paye', '../تثبیت/#paye', 'قاعدة تثبيت شفط آباديس المحمولة (ترولي)', 'تثبیت'),
        ('wallp', '../تثبیت/#wallp', 'الجزء الخلفي لمشبك الخزان المحمول', 'تثبیت'),
        ('sdv', '../خزانات/#sdv', 'الشفط الجداري', 'خزانات'),
        ('wallg', '../تثبیت/#wallg', 'مشابك خزان الحائط', 'تثبیت'),
        ('mesvak', '../منتجات-اخری/#mesvak', 'فرشاة أسنان الشفط ذات الاستعمال الواحد', 'منتجات اخری'),
        ('negahdarande', '../منتجات-اخری/#negahdarande', 'حامل أنبوب القصبة الهوائية', 'منتجات اخری'),
        ('receiver', '../منتجات-اخری/#receiver', 'وعاء كلوي للاستعمال الواحد', 'منتجات اخری'),
        ('splashvac', '../منتجات-اخری/#splashvac', 'Splash-Vac', 'منتجات اخری'),
    ],
}

def family_src(p):
    srcs = {}
    for slug, path, title, im, fb in FAMILIES:
        r = any_img(im) if im else None
        srcs[slug] = (p + r['src']) if r else ((p + fb) if fb else None)
    return srcs

def solution_src(p, photo_id):
    r = any_img(SOL_PHOTO.get(photo_id))
    return (p + r['src']) if r else None

def _pcard(href, title, sub, src, view, alt):
    ph = (f'<div class="ph"><img src="{src}" alt="{esc(alt)}" loading="lazy" decoding="async"></div>'
          if src else '<div class="ph txt">آبادیس</div>')
    sub_html = f'<span>{esc(sub)}</span>' if sub else ''
    return (f'<a class="pcard reveal" href="{href}">{ph}<strong>{esc(title)}</strong>'
            f'{sub_html}<span class="go">{view}</span></a>')

def hub_main(p, lang, summaries=None):
    import solutions_arch
    return solutions_arch.hub_main(p, lang, opening='product')

def fa_summaries():
    out = {}
    for slug, path, title, im, fb in FAMILIES:
        if slug == 'suction-bag':
            out[slug] = list(SUCTION_BAG_ITEMS)
            continue
        _, items = family(path)
        out[slug] = [i['title'] for i in items]
    return out

def write_products_hub(write, lang, summaries=None):
    ui = HUB_UI[lang]
    if lang == 'fa' and summaries is None:
        summaries = fa_summaries()
    main = hub_main(ui['prefix'], lang, summaries)
    html = page(ui['prefix'], 'products', ui['title'], ui['desc'], main, lang=lang,
                fa_path=ui['fa_path'], canonical_path=ui['canonical'])
    write(ui['rel'], html)
    return ui['rel']

def bag_benefits(lang, p):
    """Home «مزایای کیسه ساکشن» (#why), same copy, on the suction-bag page."""
    if lang == 'fa':
        import pages_home as H
        eyebrow, heading = 'چرا آبادیس؟', 'ارزش افزوده‌های کیسه ساکشن یکبار مصرف'
        values, factory, checks = H.LIVE_VALUES, H.FACTORY_LEAD, H.WHY_CHECKS
    else:
        import pages_home_i18n as I
        t = I.T[lang]
        eyebrow, heading = t['why_eb'], t['why_h']
        values, factory, checks = t['values'], t['factory'], t['checks']
    vals = ''.join(f'<div class="card value reveal"><h3>{esc(a)}</h3><p>{esc(b)}</p></div>' for a, b in values)
    lis = ''.join(f'<li>{esc(c)}</li>' for c in checks)
    return f'''  <section class="section section--alt" id="benefits">
    <div class="wrap">
      <div class="section-head reveal has-mark">{section_mark(p, 'why')}<div><p class="eyebrow">{esc(eyebrow)}</p><h2>{esc(heading)}</h2></div></div>
      <div class="grid g-4 values">{vals}</div>
      <div class="split" style="margin-top:28px">
        <div class="reveal"><p>{esc(factory)}</p></div>
        <ul class="checks reveal">{lis}</ul>
      </div>
    </div>
  </section>'''


def patch_suction_bag_benefits():
    """Hand-built FA page: keep the home benefits block across shell rebuilds."""
    from lib import SITE
    path = SITE / 'products/suction-bag/index.html'
    html = path.read_text(encoding='utf-8')
    block = '<!-- phase2:bag-benefits -->\n' + bag_benefits('fa', '../../') + '\n<!-- /phase2:bag-benefits -->\n'
    if '<!-- phase2:bag-benefits -->' in html:
        html = re.sub(r'<!-- phase2:bag-benefits -->.*?<!-- /phase2:bag-benefits -->\n',
                      lambda m: block, html, count=1, flags=re.S)
    else:
        needle = '  <section class="section spec-summary" id="specs"'
        if needle not in html:
            raise SystemExit('suction-bag: specs section missing, benefits not inserted')
        html = html.replace(needle, block + needle, 1)
        html = html.replace('<a href="#intro">معرفی</a>',
                            '<a href="#intro">معرفی</a><a href="#benefits">مزایا</a>', 1)
    path.write_text(html, encoding='utf-8')
    return 'products/suction-bag/index.html'


# Live rear-part copy. The crawled table repeated the wall clamp 060503; only 060504 belongs here.
WALLP_HTML = (
    '<p>پشت‌گیره مخزن پرتابل آبادیس در کنار گیره مخزن دیواری قرار می‌گیرد و با اتصال به آن، '
    'امکان نصب و نگهداری مخزن ساکشن روی دستگاه‌های ساکشن پرتابل بیمارستانی را فراهم می‌کند. '
    'این قطعه از جنس پلاستیک مقاوم تولید شده و به تثبیت مناسب مخزن روی دستگاه و جلوگیری از '
    'جابه‌جایی آن هنگام استفاده یا حمل دستگاه کمک می‌کند.</p>'
    '<p>پشت‌گیره مخزن پرتابل آبادیس قابلیت شست‌وشو در دمای حداکثر ۹۵ درجه سانتی‌گراد را دارد '
    'و برای استفاده در بیمارستان‌ها و سایر مراکز درمانی مناسب است.</p>'
    '<h2>ابعاد محصول</h2><p>عرض: ۲٫۵ سانتی‌متر</p><p>طول: ۵٫۳ سانتی‌متر</p>'
)
LIPO_HTML = (
    '<p>دستگاه تزریق چربی آبادیس، سامانه‌ای متصل‌شونده به دستگاه لیپوساکشن است که چربی برداشت‌شده را '
    'در یک مخزن مدرج و بسته جمع‌آوری می‌کند. پس از پایان مرحله لیپوساکشن و آماده‌سازی چربی، خروجی مخزن '
    'به بخش پمپ تزریق دستگاه متصل شده و چربی از طریق شیلنگ و کانولای مخصوص به ناحیه گیرنده انتقال می‌یابد. '
    'به این ترتیب، مراحل برداشت و تزریق مجدد چربی در یک گردش‌کار یکپارچه و در همان جلسه جراحی انجام می‌شوند.</p>'
    '<h2>ویژگی‌های محصول</h2><ul>'
    '<li>قابل اتصال به بخش پمپ تزریق دستگاه لیپوساکشن</li>'
    '<li>انتقال چربی در یک مدار بسته و کنترل‌شده</li>'
    '<li>مناسب برای انتقال و تزریق چربی پس از لیپوساکشن</li>'
    '<li>کاهش انتقال‌های دستی و جابه‌جایی چربی میان ظروف مختلف</li>'
    '<li>محدودکردن تماس چربی برداشت‌شده با محیط</li>'
    '<li>امکان کنترل جریان تزریق از طریق پمپ دستگاه</li>'
    '<li>کمک به پیوستگی فرایند برداشت، آماده‌سازی و تزریق چربی</li></ul>'
)
NO_PHOTO = {'collectioncup', 'splashvac', 'lipo'}
IMG_REPLACE = {
    'sdv': 'https://abadis-med.com/wp-content/uploads/2022/12/ساکشن-دیواری-بزرگسال-1030x1030-1.jpg',
}
# rel, prefix, canonical, products-crumb href, h1 override (None = Persian page title)
OUT = {
    'stand': {
        'fa': ('products/stand/index.html', '../../', 'products/stand/', '../', None),
        'en': ('en/products/base-and-holder/index.html', '../../../', 'en/products/base-and-holder/', '../', 'Base and Holder'),
        'ar': ('arabic/تثبیت/index.html', '../../', 'arabic/تثبیت/', '../منتجات/', 'تثبیت'),
    },
    'filters': {
        'fa': ('products/filters/index.html', '../../', 'products/filters/', '../', None),
        'en': ('en/products/filters/index.html', '../../../', 'en/products/filters/', '../', 'Filters'),
        'ar': ('arabic/الفلتر/index.html', '../../', 'arabic/الفلتر/', '../منتجات/', 'الفلتر'),
    },
    'suction-tube': {
        'fa': ('products/suction-tube/index.html', '../../', 'products/suction-tube/', '../', None),
        'en': ('en/suction-tube/index.html', '../../', 'en/suction-tube/', '../products/', 'Suction Tube'),
        'ar': ('arabic/أنبوب-الشفط/index.html', '../../', 'arabic/أنبوب-الشفط/', '../منتجات/', 'أنبوب الشفط'),
    },
    'canister': {
        'fa': ('products/canister/index.html', '../../', 'products/canister/', '../', None),
        'en': ('en/products/canisters/index.html', '../../../', 'en/products/canisters/', '../', 'Canisters'),
        'ar': ('arabic/خزانات/index.html', '../../', 'arabic/خزانات/', '../منتجات/', 'خزانات'),
    },
    'connectors': {
        'fa': ('products/connectors/index.html', '../../', 'products/connectors/', '../', None),
        'en': ('en/products/connections/index.html', '../../../', 'en/products/connections/', '../', 'Connections'),
        'ar': ('arabic/الوصلات/index.html', '../../', 'arabic/الوصلات/', '../منتجات/', 'الوصلات'),
    },
    'other': {
        'fa': ('products/other/index.html', '../../', 'products/other/', '../', None),
        'en': ('en/products/other-products/index.html', '../../../', 'en/products/other-products/', '../', 'Other Products'),
        'ar': ('arabic/منتجات-اخری/index.html', '../../', 'arabic/منتجات-اخری/', '../منتجات/', 'منتجات أخرى'),
    },
    'suction-bag': {
        'en': ('en/products/suction-bag/index.html', '../../../', 'en/products/suction-bag/', '../', 'Suction Bag'),
        'ar': ('arabic/كيس-الشفط/index.html', '../../', 'arabic/كيس-الشفط/', '../منتجات/', 'كيس الشفط'),
    },
}
I18N_PATH = {
    ('en', 'products/base-and-holder/'): 'stand',
    ('en', 'products/filters/'): 'filters',
    ('en', 'products/canisters/'): 'canister',
    ('en', 'products/connections/'): 'connectors',
    ('en', 'products/other-products/'): 'other',
    ('en', 'suction-tube/'): 'suction-tube',
    ('en', 'products/suction-bag/'): 'suction-bag',
    ('ar', 'تثبیت/'): 'stand',
    ('ar', 'الفلتر/'): 'filters',
    ('ar', 'خزانات/'): 'canister',
    ('ar', 'الوصلات/'): 'connectors',
    ('ar', 'منتجات-اخری/'): 'other',
    ('ar', 'أنبوب-الشفط/'): 'suction-tube',
    ('ar', 'كيس-الشفط/'): 'suction-bag',
}
_FA_UI = dict(products='محصولات', specs='کاتالوگ', more_a='سایر محصولات', inquiry_a='استعلام',
              sep='، ', missing_note='')


def prepare_family(slug):
    path = next(p for s, p, *_rest in FAMILIES if s == slug)
    h1, items = family(path)
    if slug == 'stand':
        for it in items:
            if it['id'] == 'wallp':
                it['title'] = 'پشت گیره مخزن پرتابل'
                it['html'] = WALLP_HTML
                it['tables'] = [[['کد کالا', 'نام کالا'], ['060504', 'پشت گیره مخزن پرتابل (پلاستیکی)']]]
    if slug == 'canister':
        items.append({
            'id': 'lipo', 'title': 'دستگاه تزریق چربی (جمع‌آوری چربی)', 'html': LIPO_HTML,
            'imgs': [], 'tables': [[['نام کالا', 'کد کالا'], ['دستگاه تزریق چربی', '']]],
            'force_missing': True,
        })
    for it in items:
        if it['id'] in NO_PHOTO:
            it['imgs'] = []
            it['force_missing'] = True
        elif it['id'] in IMG_REPLACE:
            it['imgs'] = [(IMG_REPLACE[it['id']], it['title'])]
    return h1, items


def items_for(slug, lang):
    h1, items = prepare_family(slug)
    if lang == 'fa':
        return h1, items
    from product_copy import HTML, TITLES, localize_cell
    out = []
    for it in items:
        html, title = HTML[lang].get(it['id']), TITLES[lang].get(it['id'])
        if not html or not title:
            raise SystemExit(f'missing {lang} copy for {it["id"]}')
        tables = [[[localize_cell(lang, c) for c in row] for row in t] for t in it['tables']]
        out.append({**it, 'title': title, 'html': html, 'tables': tables})
    return h1, out


def _tabs(items, blocks, lang='fa', slug='', p=''):
    import solutions_arch as S
    nav = ''.join(S.tab_anchor(it['id'], it['title'], lang) for it in items)
    pva = ('\n' + S.pva_card(p, lang)) if slug == 'other' else ''
    rules = ''.join(
        '.ptabs:not(.js-tabs):has(#%s:target) .ptab-nav a[href="#%s"]{background:var(--brand-3);color:#fff;border-color:transparent}'
        % (it['id'], it['id']) for it in items)
    return f'''  <section class="section" id="range"><div class="wrap">
    <style>{rules}</style>
    <div class="ptabs" data-ptabs>
      <div class="ptab-nav" role="tablist">{nav}</div>{pva}
{blocks}
    </div>
  </div></section>\n'''


def _related_i18n(p, here, lang):
    from product_copy import UI
    ui = UI[lang]
    titles = {row[0]: row[2] for row in HUB_FAMILIES[lang]}
    srcs = family_src(p)
    cards = []
    for slug, _path, _title, _im, _fb in FAMILIES:
        if slug == here: continue
        href = p + OUT[slug][lang][2]
        src = srcs.get(slug)
        ph = f'<div class="ph"><img src="{src}" alt="" loading="lazy" decoding="async"></div>' if src else '<div class="ph txt">Abadis</div>'
        cards.append(f'<a class="mini-card" href="{href}">{ph}<strong>{esc(titles[slug])}</strong></a>')
    return f'''  <section class="section section--alt" id="more"><div class="wrap">
    <h2 class="reveal" style="margin-bottom:20px">{esc(ui["more"])}</h2>
    <div class="mini-grid">{''.join(cards)}</div>
  </div></section>'''


def _inquiry(p, lang):
    if lang == 'fa':
        return INQUIRY
    from product_copy import UI
    ui = UI[lang]
    quote = p + 'export/#quote'
    return f'''  <section class="section" id="inquiry"><div class="wrap">
    <div class="cta-band reveal">
      <h2>{esc(ui["inquiry_h"])}</h2>
      <p>{esc(ui["inquiry_p"])}</p>
      <div class="cta-actions"><a class="btn btn-light" href="tel:+982192001017">{esc(ui["call"])}</a><a class="btn btn-ghost" href="https://wa.me/989100145809" target="_blank" rel="noopener">{esc(ui["wa"])}</a><a class="btn btn-ghost" href="{quote}">{esc(ui["quote"])}</a></div>
    </div>
  </div></section>'''


def write_family_page(write, slug, lang):
    if slug == 'suction-bag':
        return write_bag(write, lang)
    rel, p, can, crumb_href, h1_over = OUT[slug][lang]
    h1, items = items_for(slug, lang)
    if h1_over:
        h1 = h1_over
    from product_copy import UI
    ui = UI[lang] if lang != 'fa' else _FA_UI
    sep = '، ' if lang != 'en' else ', '
    lead = sep.join(i['title'] for i in items)
    products = ui['products']
    import solutions_arch as S
    anchors = ''.join(
        f'<a href="#{esc(i["id"])}">{esc(i["title"])}{S.badge(lang, S.status_for(i["id"]))}</a>' for i in items)
    if DOCS.get(slug):
        anchors += f'<a href="#docs">{esc(ui["specs"])}</a>'
    anchors += f'<a href="#more">{esc(ui["more_a"])}</a><a href="#inquiry">{esc(ui["inquiry_a"])}</a>'
    blocks = '\n'.join(product_block(p, it, lang) for it in items)
    more = related(p, slug) if lang == 'fa' else _related_i18n(p, slug, lang)
    hero = S.inject_h1_badge(
        page_hero(p, [(products, crumb_href), (h1, None)], esc(h1), esc(lead), lang=lang), lang, 'order')
    main = (hero
            + f'\n  <nav class="anchors" aria-label="{esc(products)}"><div class="wrap">{anchors}</div></nav>\n'
            + doc_bar(slug, lang)
            + _tabs(items, blocks, lang, slug, p)
            + S.related_section(p, lang, slug)
            + more + '\n' + _inquiry(p, lang))
    desc = f'{h1} — {lead}'
    write(rel, page(p, 'products', h1, desc, main, lightbox=True, lang=lang,
                    fa_path=f'products/{slug}/', canonical_path=can))
    return rel


def _bag_table(lang, size, p):
    from product_copy import BAG_ROWS, UI
    ui = UI[lang]
    rows = BAG_ROWS[size]
    sterile = any(r[5] is not None for r in rows)
    heads = [ui['code'], ui['irc'], ui['size'], ui['ftype'], ui['powder']]
    if sterile:
        heads.append(ui['sterile'])
    heads.append(ui['lid'])
    body = []
    for code, irc, sz, kind, powder, ster, lid in rows:
        cells = [code, irc or '—', ui[sz], ui[kind], '✓' if powder else '×']
        if sterile:
            cells.append('—' if ster is None else ('✓' if ster else '×'))
        alt = ui['lid_' + lid]
        cells.append(f'<img class="lid" src="{p}assets/img/p/lid-{lid}.webp" width="50" height="20" alt="{esc(alt)}">')
        tds = ''.join(f'<td>{c if c.startswith("<img") else esc(c)}</td>' for c in cells)
        body.append(f'<tr>{tds}</tr>')
    th = ''.join(f'<th>{esc(h)}</th>' for h in heads)
    return f'<div class="table-wrap"><table><thead><tr>{th}</tr></thead><tbody>{"".join(body)}</tbody></table></div>'


def _bag_uses(lang, size, p):
    from product_copy import BAG_USES, UI
    ui = UI[lang]
    idx = 2 if lang == 'en' else 3
    bits = []
    for icon, _fa, en, ar in BAG_USES[size]:
        label = en if lang == 'en' else ar
        bits.append(
            f'<div class="use"><span class="use-ic" style="--ic:url(\'{p}assets/img/use/{icon}.webp\')">'
            f'<img src="{p}assets/img/use/{icon}.webp" width="100" height="100" loading="lazy" alt=""></span>{esc(label)}</div>')
    return f'<h3 class="uses-h">{esc(ui["use"])}</h3><div class="uses">{"".join(bits)}</div>'


def write_bag(write, lang):
    """EN/AR suction bag: 1 L then 2 L then 3 L, current codes, benefits kept by the caller shell."""
    if lang == 'fa':
        return None
    from product_copy import UI
    import solutions_arch as S
    ui = UI[lang]
    rel, p, can, crumb_href, h1 = OUT['suction-bag'][lang]
    filters = '../filters/' if lang == 'en' else '../الفلتر/'
    guide = '../../installation-manual/' if lang == 'en' else '../دليل-التركيب/'
    downloads = '../../center-download/' if lang == 'en' else '../مركز-التنزيل/'
    cat = 'https://abadis-med.com/wp-content/uploads/2022/12/suction-bag-catalog-Fa.pdf'
    if lang == 'en':
        cat = 'https://www.abadis-med.com/en/wp-content/uploads/2021/12/suction-bag-catalog-En.pdf'
    media = {
        '1': ('p1-main.webp', 900, 900, 'p1-g5.webp', 'p1-g5-t.webp', '11 cm', '15.5 cm', '57.5 × 42.5 × 44'),
        '2': ('p2-main.webp', 900, 900, 'p2-g4.webp', 'p2-g4-t.webp', '11 cm', '24.5 cm', '57.5 × 42.5 × 44'),
        '3': ('p3-main.webp', 561, 900, 'p3-g5.webp', 'p3-g5-t.webp', '11 cm', '39 cm', '49 × 49 × 49'),
    }
    blocks = []
    for size, (main_img, w, h, dim, dim_t, dia, height, carton) in media.items():
        title = ui['s' + size]
        meta = ui['s' + size + 'm']
        spec = ui['spec3'] if size == '3' else (ui['intro'] if size == '1' else ui['spec2'])
        extra = f'<p class="note">{esc(ui["note3"])}</p>' if size == '3' else ''
        vol = f'<p class="note"><strong>{esc(ui["vol"])}:</strong> {esc(ui["one_l"])}</p>' if size == '1' else ''
        sterile = ''
        if size == '3':
            sterile = (f'<div class="sterile"><h3>{esc(ui["sterile_h"])}</h3><p>{esc(ui["sterile_p"])}</p></div>')
        blocks.append(f'''    <article class="size-block" id="s{size}">
      <h2>{esc(title)}{S.badge(lang, "order")}</h2>
      <p class="meta">{esc(meta)}</p>
      <div class="size-grid">
        <div class="size-media">
          <a class="gal-main" href="{p}assets/img/p/{main_img}" data-gallery="s{size}" data-w="{w}" data-h="{h}"><img src="{p}assets/img/p/{main_img}" width="{w}" height="{h}" alt="{esc(title)}" loading="lazy" decoding="async"></a>
          <div class="gal-thumbs"><a href="{p}assets/img/p/{dim}" data-gallery="s{size}" data-w="1254" data-h="1254"><img src="{p}assets/img/p/{dim_t}" width="480" height="480" alt="{esc(height)}" loading="lazy" decoding="async"></a></div>
        </div>
        <div class="size-info">
          {vol}{extra}
          <div class="dims"><span>{esc(ui["d_d"])}: {esc(dia)}</span><span>{esc(ui["d_h"])}: {esc(height)}</span><span>{esc(ui["d_c"])}: {esc(ui["pcs"])}</span><span>{esc(ui["d_cd"])}: {esc(carton)}</span></div>
          <p class="meta-line">{esc(spec)}</p>
          <p class="note"><a href="{filters}">{esc(ui["filters_a"])}</a></p>
        </div>
      </div>
      {_bag_table(lang, size, p)}
      {sterile}
      {_bag_uses(lang, size, p)}
    </article>''')
    benefit = 'Benefits' if lang == 'en' else 'المزايا'
    anchors = (f'<a href="#benefits">{esc(benefit)}</a>'
               f'<a href="#s1">{esc(ui["sz1"])}{S.badge(lang, "order")}</a>'
               f'<a href="#s2">{esc(ui["sz2"])}{S.badge(lang, "order")}</a>'
               f'<a href="#s3">{esc(ui["sz3"])}{S.badge(lang, "order")}</a>'
               f'<a href="{filters}">{esc(ui["filters_h"])}</a><a href="#pack">{esc(ui["pack_h"])}</a>')
    intro = f'''  <section class="section" id="intro"><div class="wrap">
    <div class="section-head"><h2>{esc(ui["intro_h"])}</h2></div>
    <div class="card prose"><p>{esc(ui["intro"])}</p><p>{esc(ui["intro2"])}</p><p>{esc(ui["intro3"])}</p></div>
    <div class="grid g-3">
      <article class="card"><h3>{esc(ui["v1"])}</h3><p>{esc(ui["v1p"])}</p></article>
      <article class="card"><h3>{esc(ui["v2"])}</h3><p>{esc(ui["v2p"])}</p></article>
      <article class="card"><h3>{esc(ui["v3"])}</h3><p>{esc(ui["v3p"])}</p></article>
    </div>
  </div></section>'''
    main = (S.inject_h1_badge(page_hero(p, [(ui['products'], crumb_href), (h1, None)], esc(h1), esc(ui['bag_lead']), lang=lang), lang, 'order')
            + '\n' + bag_benefits(lang, p) + '\n'
            + f'  <nav class="anchors"><div class="wrap">{anchors}</div></nav>\n'
            + intro
            + '  <section class="section"><div class="wrap">\n' + '\n'.join(blocks) + '\n  </div></section>\n'
            + f'''  <section class="section section--alt" id="filters"><div class="wrap">
    <h2>{esc(ui["filters_h"])}</h2>
    <p>{esc(ui["filters_p"])}</p>
    <div class="doc-links"><a href="{filters}">{esc(ui["filters_a"])}</a></div>
  </div></section>
  <section class="section" id="pack"><div class="wrap">
    <h2>{esc(ui["pack_h"])}</h2>
    <p>{esc(ui["pack_p"])}</p>
    <div class="doc-links"><a href="{esc(cat)}" target="_blank" rel="noopener" data-track="catalogue_download">{esc(ui["cat"])}</a><a href="{guide}">{esc(ui["guide"])}</a><a href="{downloads}">{esc(ui["downloads"])}</a></div>
  </div></section>\n'''
            + S.related_section(p, lang, 'suction-bag')
            + _inquiry(p, lang))
    write(rel, page(p, 'products', h1, ui['bag_desc'], main, lightbox=True, lang=lang,
                    fa_path='products/suction-bag/', canonical_path=can))
    return rel


def patch_suction_bag_cleanup():
    """Hand-built FA page. Idempotent: 1 L → viewer → 2 L → 3 L, one height, no duplicate SKUs."""
    from lib import SITE
    path = SITE / 'products/suction-bag/index.html'
    html = path.read_text(encoding='utf-8')
    i1, iv, i2 = html.find('id="s1"'), html.find('id="viewer"'), html.find('id="s2"')
    if not (i1 != -1 and iv != -1 and i2 != -1 and i1 < iv < i2):
        m = re.search(r'  <section class="section deep" id="viewer">.*?\n  </section>\n', html, re.S)
        if not m:
            raise SystemExit('suction-bag: viewer section missing')
        viewer = m.group(0)
        html = html[:m.start()] + '\n' + html[m.end():]
        needle = '    <div class="size-block" id="s2">'
        if needle not in html:
            raise SystemExit('suction-bag: 2 L block missing')
        html = html.replace(needle, '  </div></section>\n' + viewer + '  <section class="section"><div class="wrap">\n' + needle, 1)
    html = html.replace('فیلترهایاستفاده‌شده', 'فیلترهای استفاده‌شده')
    html = html.replace('۲ لیتری ۲۳٫۵', '۲ لیتری ۲۴٫۵')
    html = html.replace('۲ لیتری</a> (۵ مدل)', '۲ لیتری</a> (۴ مدل)')
    html = html.replace('۳ لیتری</a> (۸ مدل)', '۳ لیتری</a> (۷ مدل)')
    html = html.replace('<tr><th scope="row">جنس / مواد</th><td><span class="ph-data">[در انتظار اطلاعات از شرکت]</span></td></tr>', '')
    html = html.replace(' · IFU انگلیسی/عربی: <span class="ph-data">[در انتظار اطلاعات از شرکت]</span>', '')
    html = html.replace('فیلتر هیدروفوبیک / مکانیکی / CIF', 'فیلتر هیدروفوبیک / مکانیکی')
    html = re.sub(r'\n<tr><td>۰۴۰۱۱۱۲</td><td dir="ltr" class="irc">9647935197253589</td><td>دو لیتری</td><td>CIF</td>.*?</tr>', '', html, count=1)
    html = re.sub(r'\n<tr><td>۰۴۰۱۱۱۳</td><td dir="ltr" class="irc">6579214989949869</td><td>سه لیتری</td><td>CIF</td>.*?</tr>', '', html, count=1)
    html = html.replace('>۰۴۰۱۱۲۳</td><td dir="ltr" class="irc">7600653363719319<', '>۰۴۰۱۱۲۳</td><td dir="ltr" class="irc">3011241869977602<')
    html = html.replace('href="#filters"', 'href="../filters/"')
    if 'class="filter-card"' in html:
        short = '''  <section class="section section--alt" id="filters"><div class="wrap">
    <h2 class="reveal">فیلترها</h2>
    <p class="sub"><a href="../filters/">فیلتر آنتی‌باکتریال، فیلتر قطع‌کننده جریان و فیلتر متخلخل</a></p>
  </div></section>\n'''
        html2, n = re.subn(r'  <section class="section section--alt" id="filters"><div class="wrap">.*?\n  </div></section>\n',
                           short, html, count=1, flags=re.S)
        if n != 1:
            raise SystemExit('suction-bag: filters chapter not replaced')
        html = html2
    path.write_text(html, encoding='utf-8')
    return 'products/suction-bag/index.html'


def build(write):
    summaries = {}
    for slug, path, title, im, fb in FAMILIES:
        if slug == 'suction-bag':
            summaries[slug] = list(SUCTION_BAG_ITEMS)
            continue
        write_family_page(write, slug, 'fa')
        _h1, items = prepare_family(slug)
        summaries[slug] = [i['title'] for i in items]
    patch_suction_bag_cleanup()
    patch_suction_bag_benefits()
    import solutions_arch
    solutions_arch.stamp_product_pages()
    write_products_hub(write, 'fa', summaries)
    for lang in ('en', 'ar'):
        for slug, _path, _title, _im, _fb in FAMILIES:
            write_family_page(write, slug, lang)
        write_products_hub(write, lang)
