"""Products hub + six product family pages (suction bag page is hand-built and kept)."""
import re
from lib import PAGES, esc, strip_tags, best_img, rewrite_html
from layout import page, page_hero, section_mark
from render import table, gallery_link, secs

FAMILIES = [  # slug, live path, hub title (verbatim from live hub), hub image, local fallback image
    ('suction-bag', '/محصولات/کیسه-ساکشن/', 'کیسه های ساکشن', 'https://abadis-med.com/wp-content/uploads/2022/12/کیسه-ساکشن.jpg', 'assets/img/p/p2-main.webp'),
    ('stand', '/محصولات/پایه/', 'پایه و نگهدارنده', 'https://abadis-med.com/wp-content/uploads/2022/12/پایه-ترولی.jpg', 'assets/img/p/p1-g3-t.webp'),
    ('filters', '/محصولات/فیلترها/', 'فیلتر', 'https://abadis-med.com/wp-content/uploads/2022/12/فیلتر1-2-845x684-1.jpg', 'assets/img/filters/anti-1-t.webp'),
    ('suction-tube', '/محصولات/ساکشن-تیوب/', 'ساکشن تیوب', 'https://abadis-med.com/wp-content/uploads/2022/12/ساکشن-تیوب-7e83722522e8aeb7512b7075311316b7__m8ULku2SAG__1-1-300x300.jpg', 'assets/img/p/p1-g4-t.webp'),
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
def local_link(p, path, gid, alt, cls=''):
    from PIL import Image
    from lib import SITE
    w, h = Image.open(SITE / path).size
    t = path.replace('.webp', '-t.webp')
    tw, th = Image.open(SITE / t).size if (SITE / t).exists() else (w, h)
    if not (SITE / t).exists(): t = path
    return (f'<a href="{p}{path}" data-gallery="{gid}" data-w="{w}" data-h="{h}" aria-label="نمایش بزرگ‌تر: {esc(alt)}">'
            f'<img src="{p}{t}" width="{tw}" height="{th}" loading="lazy" decoding="async" alt="{esc(alt)}"></a>')
SUCTION_BAG_ITEMS = ['کیسه ساکشن ۱ لیتری', 'کیسه ساکشن ۲ لیتری', 'کیسه ساکشن ۳ لیتری']

def pick(b):
    h = b.get('href') or ''
    if h.startswith('http') and re.search(r'\.(jpe?g|png|webp)$', h) and best_img(h): return h
    return b['src']

def norm(s): return re.sub(r'[\s\u200c\u200b():]+', '', strip_tags(s))

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
        body = '\n'.join(htmls)
        m = re.match(r'\s*(?:<p>)?\s*<strong>(.*?)</strong>\s*(?:</p>)?', body, re.S)
        if m:
            lead = strip_tags(m.group(1))
            if title is None: title = lead
            if norm(lead) and (norm(lead) in norm(title) or norm(title) in norm(lead) or len(lead) < 60):
                body = body[m.end():]
        out.append({'id': aid, 'title': title or '', 'html': body,
                    'imgs': [(pick(b), b.get('alt', '')) for b in bs if b['t'] == 'img'],
                    'tables': [b['rows'] for b in bs if b['t'] == 'table']})
    return h1, out

def product_block(p, it, n):
    imgs = it['imgs']; gid = it['id']
    media = ''
    links = [gallery_link(p, u_, gid, a or it['title'], 900, 1600) for u_, a in imgs]
    links = [l for l in links if l]
    if not links:
        for src in FALLBACK.get(gid, []):
            if src.startswith('local:'): links.append(local_link(p, src[6:], gid, it['title']))
            else:
                l = gallery_link(p, src, gid, it['title'], 900, 1600)
                if l: links.append(l)
    if links:
        main = links[0].replace('<a ', '<a class="gal-main" ', 1)
        thumbs = ''.join(links[1:])
        media = f'<div class="size-media">{main}{f"<div class=gal-thumbs>{thumbs}</div>" if thumbs else ""}</div>'
    else:
        media = f'<div class="size-media"><div class="gal-main gal-missing"><img src="{p}assets/img/abadis-logo-teal.png" width="658" height="309" alt=""><span>تصویر این محصول در نسخهٔ آرشیوشدهٔ سایت موجود نبود</span></div></div>'
    tables = ''.join(table(t) for t in it['tables'])
    return f'''    <div class="size-block reveal" id="{esc(it["id"])}">
      <h3>{esc(it["title"])}</h3>
      <div class="size-grid">
        {media}
        <div class="size-info prose">{rewrite_html(it["html"], p)}</div>
      </div>
      {tables}
    </div>'''

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
    'other': [(UP + '2022/12/endotracheal-tube-holder-catalog-Fa.pdf', 'کاتالوگ نگهدارنده لوله تراشه (PDF)'),
              (UP + '2022/12/wall-suction-catalog-Fa.pdf', 'کاتالوگ ساکشن دیواری (PDF)'), CAT_ALL],
}
PH = '<span class="ph-data">[در انتظار اطلاعات از شرکت]</span>'

def spec_summary(p, slug, items):
    docs = '، '.join(f'<a href="{esc(h)}" target="_blank" rel="noopener" data-track="catalogue_download">{esc(t)}</a>' for h, t in DOCS.get(slug, [CAT_ALL]))
    models = '، '.join(f'<a href="#{esc(i["id"])}">{esc(i["title"])}</a>' for i in items)
    rows = [('مدل‌ها', models), ('ظرفیت', PH), ('ابعاد', PH + ' (جدول‌های هر مدل در پایین صفحه)'), ('سازگاری', PH),
            ('جنس / مواد', PH), ('لوازم جانبی', PH),
            ('گواهی‌ها', 'گواهی‌های شرکت: IMED، ISO، CE <span class="ph-data">[پوشش این محصول در انتظار تأیید شرکت]</span>'),
            ('کاتالوگ و راهنما', docs + ' · IFU: ' + PH)]
    body = ''.join(f'<tr><th scope="row">{k}</th><td>{v}</td></tr>' for k, v in rows)
    return f'''  <section class="section spec-summary" id="specs"><div class="wrap reveal">
    <h2 style="margin-bottom:14px">مشخصات در یک نگاه</h2>
    <table class="spec-table"><tbody>{body}</tbody></table>
  </div></section>'''

# Products hub. The two category labels are Hamid's (Oct 2026).
# "By product" is the live hub families (data/pages.json "/محصولات/"), same titles and order.
# "By solution" lists systems those family pages already name (stand, canister, other).
# Boss notes and PHASE-1 do not define a second taxonomy; they list these families only.
HUB_UI = {
    'fa': dict(
        nav='دسته‌بندی محصولات', by_product='بر مبنای محصولات', by_solution='بر اساس راهکار',
        view='مشاهده ←', h1='محصولات <em>آبادیس</em>', title='محصولات',
        desc='محصولات مخازن طبی آبادیس: کیسه ساکشن یکبار مصرف، فیلترها، مخزن، پایه و نگهدارنده ها، اتصالات، ساکشن تیوب و سایر محصولات.',
        lead='کیسه ساکشن یکبار مصرف، فیلترها، مخزن، پایه و نگهدارنده ها، اتصالات، ساکشن تیوب و سایر محصولات.',
        crumb='محصولات', alt_suffix=' آبادیس',
        docs=[('../downloads/', 'مرکز دانلود کاتالوگ‌ها'), ('../install-guide/', 'راهنمای نصب'), ('../calculator/', 'محاسبه‌گر صرفه‌جویی')],
        rel='products/index.html', prefix='../', fa_path='products/', canonical='products/',
    ),
    'en': dict(
        nav='Product categories', by_product='By product', by_solution='By solution',
        view='Find Out More', h1='Products', title='Products',
        desc='Suction Bag, Base and Holder, Filter, Suction tube, Canister, Connections and Other Products.',
        lead='Suction Bag, Base and Holder, Filter, Suction tube, Canister, Connections and Other Products.',
        crumb='Products', alt_suffix=' Abadis',
        docs=[('../center-download/', 'Download Center'), ('../installation-manual/', 'Installation Manual'), ('../calculator/', 'Savings calculator')],
        rel='en/products/index.html', prefix='../../', fa_path='products/', canonical='en/products/',
    ),
    'ar': dict(
        nav='تصنيف المنتجات', by_product='حسب المنتجات', by_solution='حسب الحلول',
        view='مشاهدة منتجاتنا', h1='منتجات', title='منتجات',
        desc='كيس الشفط، خزانات، تثبیت، الوصلات، الفلتر، أنبوب الشفط ومنتجات اخری.',
        lead='كيس الشفط، خزانات، تثبیت، الوصلات، الفلتر، أنبوب الشفط ومنتجات اخری.',
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
        ('stand', 'base-and-holder/', 'Base and Holder', 'Trolleys, Wall bracket, Rail bracket'),
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
        ('canister', '../خزانات/', 'خزانات', 'خزانات الشفط، الشفط الجداري'),
        ('connectors', '../الوصلات/', 'الوصلات', ''),
        ('other', '../منتجات-اخری/', 'منتجات اخری', 'فرشاة أسنان الشفط ذات الاستعمال الواحد، حامل أنبوب القصبة الهوائية، Kidney dish'),
    ],
}
# image slug, href, title, parent family (all titles already published on the family pages)
SOLUTIONS = {
    'fa': [
        ('stand', 'stand/#paye', 'پایه ساکشن پرتابل (ترولی)', 'پایه و نگهدارنده'),
        ('stand', 'stand/#wallp', 'گیره و مخزن پرتابل', 'پایه و نگهدارنده'),
        ('canister', 'canister/#sdv', 'ساکشن دیواری', 'مخزن'),
        ('stand', 'stand/#wallg', 'گیره و مخزن دیواری', 'پایه و نگهدارنده'),
        ('other', 'other/#mesvak', 'مسواک ساکشن یکبارمصرف', 'سایر محصولات'),
        ('other', 'other/#negahdarande', 'نگهدارنده لوله تراشه', 'سایر محصولات'),
        ('other', 'other/#receiver', 'رسیور پزشکی یکبارمصرف', 'سایر محصولات'),
        ('other', 'other/#splashvac', 'مکش سطحی چند منظوره (Splash-Vac)\u200b', 'سایر محصولات'),
    ],
    'en': [
        ('stand', 'base-and-holder/#Trolleys', 'Trolleys', 'Base and Holder'),
        ('stand', 'base-and-holder/', 'Rail bracket', 'Base and Holder'),
        ('canister', 'canisters/#b', 'Wall Suction', 'Canister'),
        ('stand', 'base-and-holder/', 'Wall bracket', 'Base and Holder'),
        ('other', 'other-products/#Suction%20Brush', 'Suction Brush', 'Other Products'),
        ('other', 'other-products/#Endotracheal%20Tube%20Holder', 'Endotracheal Tube Holder', 'Other Products'),
        ('other', 'other-products/#Kidney%20dish', 'Disposable Kidney Dish', 'Other Products'),
        ('other', 'other-products/#splashvac', 'Splash-Vac', 'Other Products'),
    ],
    'ar': [
        ('stand', '../تثبیت/', 'قاعدة تثبيت شفط آباديس المحمولة (ترولي)', 'تثبیت'),
        ('stand', '../تثبیت/', 'مشابك الخزان المحمول', 'تثبیت'),
        ('canister', '../خزانات/', 'الشفط الجداري', 'خزانات'),
        ('stand', '../تثبیت/', 'مشابك خزان الحائط', 'تثبیت'),
        ('other', '../منتجات-اخری/', 'فرشاة أسنان الشفط ذات الاستعمال الواحد', 'منتجات اخری'),
        ('other', '../منتجات-اخری/', 'حامل أنبوب القصبة الهوائية', 'منتجات اخری'),
        ('other', '../منتجات-اخری/', 'Kidney dish', 'منتجات اخری'),
    ],
}

def family_src(p):
    srcs = {}
    for slug, path, title, im, fb in FAMILIES:
        r = best_img(im, 640) if im else None
        srcs[slug] = (p + r['src']) if r else ((p + fb) if fb else None)
    return srcs

def _pcard(href, title, sub, src, view, alt):
    ph = (f'<div class="ph"><img src="{src}" alt="{esc(alt)}" loading="lazy" decoding="async"></div>'
          if src else '<div class="ph txt">آبادیس</div>')
    sub_html = f'<span>{esc(sub)}</span>' if sub else ''
    return (f'<a class="pcard reveal" href="{href}">{ph}<strong>{esc(title)}</strong>'
            f'{sub_html}<span class="go">{view}</span></a>')

def hub_main(p, lang, summaries=None):
    ui = HUB_UI[lang]
    srcs = family_src(p)
    fams = []
    for row in HUB_FAMILIES[lang]:
        slug, href, title = row[0], row[1], row[2]
        sub = ('، '.join(summaries[slug]) if summaries else '') if lang == 'fa' else row[3]
        fams.append(_pcard(href, title, sub, srcs.get(slug), ui['view'], title + ui['alt_suffix']))
    sols = [_pcard(href, title, sub, srcs.get(slug), ui['view'], title + ui['alt_suffix'])
            for slug, href, title, sub in SOLUTIONS[lang]]
    docs = ''.join(f'<a href="{h}">{esc(t)}</a>' for h, t in ui['docs'])
    nav = (f'  <nav class="anchors" aria-label="{esc(ui["nav"])}"><div class="wrap">'
           f'<a href="#by-product">{esc(ui["by_product"])}</a>'
           f'<a href="#by-solution">{esc(ui["by_solution"])}</a>'
           f'</div></nav>\n')
    return (page_hero(p, [(ui['crumb'], None)], ui['h1'], ui['lead'], lang=lang) + '\n' + nav
            + f'  <section class="section product-cat" id="by-product"><div class="wrap">'
            + f'<div class="section-head"><h2>{esc(ui["by_product"])}</h2></div>'
            + f'<div class="grid g-3">{"".join(fams)}</div></div></section>\n'
            + f'  <section class="section section--alt product-cat" id="by-solution"><div class="wrap">'
            + f'<div class="section-head"><h2>{esc(ui["by_solution"])}</h2></div>'
            + f'<div class="grid g-3">{"".join(sols)}</div></div></section>\n'
            + f'  <section class="section" style="padding-top:0"><div class="wrap"><div class="doc-links">{docs}</div></div></section>')

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


def build(write):
    p = '../../'
    summaries = {}
    for slug, path, title, im, fb in FAMILIES:
        if slug == 'suction-bag':
            summaries[slug] = SUCTION_BAG_ITEMS; continue
        h1, items = family(path)
        summaries[slug] = [i['title'] for i in items]
        anchors = ''.join(f'<a href="#{esc(i["id"])}">{esc(i["title"])}</a>' for i in items) + '<a href="#specs">مشخصات</a><a href="#more">سایر محصولات</a><a href="#inquiry">استعلام</a>'
        blocks = '\n'.join(product_block(p, it, n) for n, it in enumerate(items))
        lead = '، '.join(i['title'] for i in items)
        main = (page_hero(p, [('محصولات', '../'), (h1, None)], esc(h1), esc(lead))
                + f'\n  <nav class="anchors" aria-label="بخش‌های صفحه"><div class="wrap">{anchors}</div></nav>\n'
                + spec_summary(p, slug, items) + '\n'
                + f'  <section class="section"><div class="wrap">\n{blocks}\n  </div></section>\n'
                + related(p, slug) + '\n' + INQUIRY)
        write(f'products/{slug}/index.html', page(p, 'products', h1, f'{h1} آبادیس: ' + lead, main, lightbox=True, fa_path=f'products/{slug}/'))
    patch_suction_bag_benefits()
    write_products_hub(write, 'fa', summaries)
