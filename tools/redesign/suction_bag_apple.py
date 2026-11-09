"""Apple-style 1L suction bag page sections (FA/EN/AR). Additions/reorder only."""
import html as _h

V = '20261109r'


def esc(s):
    return _h.escape(str(s), quote=True)


COPY = {
    'fa': dict(
        sticky_name='کیسه ساکشن ۱ لیتری آبادیس',
        quote='درخواست قیمت',
        quote_href='../../contact/',
        hero_kicker='محصولات · مدیریت مایعات',
        hero_h1='کیسه ساکشن ۱ لیتری آبادیس',
        hero_tag='کنترل عفونت در مسیر ساکشن — فیلتر هیدروفوبیک و پودر ژل‌کننده.',
        cta_quote='درخواست قیمت',
        cta_specs='مشخصات',
        story_beats=[
            dict(a=0.00, b=0.18, pos='top', h='درب فیروزه‌ای <em>یکپارچه</em>', p='قفل رینگ روی لبه کیسه و دهانه مخزن.', num='۱ L'),
            dict(a=0.18, b=0.38, pos='bot', h='فیلتر <em>هیدروفوبیک</em>', p='فیلتر قطع‌کن سرریز (flow stopper) از مسیر ساکشن مرکزی محافظت می‌کند.', num='قطع‌کن سرریز'),
            dict(a=0.38, b=0.58, pos='bot', h='پورت <em>بیمار</em> و <em>وکیوم</em>', p='لوله PATIENT و پورت VACUUM روی درب مشخص شده‌اند.', num='PATIENT · VACUUM'),
            dict(a=0.58, b=0.78, pos='top', h='ابعاد <em>اسمی</em> ۱ لیتری', p='قطر و ارتفاع طبق مشخصات محصول روی سایت آبادیس.', num='⌀ ۱۱ × ۱۵٫۵ cm'),
            dict(a=0.78, b=1.01, pos='bot', h='پودر <em>ژل‌کننده</em>', p='حاوی پودر ژل؛ معمولاً ۴۵ عدد در هر کارتن.', num='۴۵ / کارتن'),
        ],
        stats=[
            ('⌀ ۱۱ cm', 'قطر کیسه'),
            ('۱۵٫۵ cm', 'ارتفاع ۱ لیتری'),
            ('۴۵', 'عدد در کارتن'),
            ('IMED / ISO / CE', 'گواهی‌ها'),
        ],
        gal_h='گالری',
        gal_lead='عکس واقعی محصول و طرح‌های تک‌نما — بدون برگه کاتالوگ.',
        sizes_h='سایزها',
        sizes_lead='۱، ۲ و ۳ لیتر — جدول کد و IRC در هر بخش.',
        sizes=[
            ('#s1', '۱ لیتری', 'ارتفاع ۱۵٫۵ cm · کدهای ۰۴۰۱۱۱۱ و ۰۴۰۱۰۱۱'),
            ('#s2', '۲ لیتری', 'ارتفاع ۲۴٫۵ cm · ۴ مدل'),
            ('#s3', '۳ لیتری', 'ارتفاع ۳۹ cm · ۷ مدل'),
        ],
        compat_h='سازگاری و لوازم',
        compat_lead='سازگار با دستگاه‌های ساکشن پرتابل و سانترال؛ نصب تکی و سری.',
        compat=[
            ('../canister/', 'مخزن ساکشن'),
            ('../stand/', 'پایه و نگهدارنده‌ها'),
            ('../connectors/', 'اتصالات'),
            ('../filters/', 'فیلترها'),
        ],
        close_h='آماده استعلام یا دریافت کاتالوگ؟',
        close_p='تیم فروش آبادیس برای انتخاب مدل، فیلتر و بسته‌بندی کنار شماست.',
        close_sales='تماس با فروش',
        close_cat='دانلود کاتالوگ',
        close_sales_href='tel:+982192001017',
        close_cat_href='https://abadis-med.com/wp-content/uploads/2022/12/suction-bag-catalog-Fa.pdf',
        poster_alt='عکس محصول کیسه ساکشن ۱ لیتری آبادیس',
    ),
    'en': dict(
        sticky_name='Abadis 1L suction liner',
        quote='Request quote',
        quote_href='../../../contact/',
        hero_kicker='Products · Fluid management',
        hero_h1='Abadis 1L suction liner',
        hero_tag='Infection control on the suction path — hydrophobic filter and gelling powder.',
        cta_quote='Request quote',
        cta_specs='Specifications',
        story_beats=[
            dict(a=0.00, b=0.18, pos='top', h='Solid <em>teal</em> HDPE lid', p='Lock ring on the liner rim and canister mouth.', num='1 L'),
            dict(a=0.18, b=0.38, pos='bot', h='Hydrophobic <em>filter</em>', p='Flow-stopper filter protects the central suction path from liquid overflow.', num='Flow stopper'),
            dict(a=0.38, b=0.58, pos='bot', h='PATIENT & <em>VACUUM</em> ports', p='PATIENT tube and VACUUM port marked on the lid.', num='PATIENT · VACUUM'),
            dict(a=0.58, b=0.78, pos='top', h='1L <em>nominal</em> size', p='Diameter and height per Abadis product specifications.', num='Ø11 × 15.5 cm'),
            dict(a=0.78, b=1.01, pos='bot', h='Gelling <em>powder</em>', p='Contains gel powder; typically 45 units per carton.', num='45 / carton'),
        ],
        stats=[
            ('Ø11 cm', 'Liner diameter'),
            ('15.5 cm', '1L height'),
            ('45', 'Units per carton'),
            ('IMED / ISO / CE', 'Certificates'),
        ],
        gal_h='Gallery',
        gal_lead='Real product photos and clean single-view sketches — no catalog sheets.',
        sizes_h='Sizes',
        sizes_lead='1, 2 and 3 litres — full codes and IRC in each section.',
        sizes=[
            ('#s1', '1 litre', 'H 15.5 cm · codes 0401111 & 0401011'),
            ('#s2', '2 litres', 'H 24.5 cm · 4 models'),
            ('#s3', '3 litres', 'H 39 cm · 7 models'),
        ],
        compat_h='Compatibility & accessories',
        compat_lead='Fits portable and central suction; single or series mounting.',
        compat=[
            ('../canisters/', 'Canisters'),
            ('../base-and-holder/', 'Stands & holders'),
            ('../connections/', 'Connections'),
            ('../filters/', 'Filters'),
        ],
        close_h='Ready for a quote or the catalog?',
        close_p='Abadis sales can help pick model, filter and packaging.',
        close_sales='Call sales',
        close_cat='Download catalog',
        close_sales_href='tel:+982192001017',
        close_cat_href='https://www.abadis-med.com/en/wp-content/uploads/2021/12/suction-bag-catalog-En.pdf',
        poster_alt='Abadis 1L suction bag product photo',
    ),
    'ar': dict(
        sticky_name='كيس الشفط سعة ١ لتر من آباديس',
        quote='طلب عرض سعر',
        quote_href='../../اتصل-بنا/',
        hero_kicker='المنتجات · إدارة السوائل',
        hero_h1='كيس الشفط سعة ١ لتر من آباديس',
        hero_tag='التحكم في العدوى على مسار الشفط — فلتر كاره للماء ومسحوق مهلّم.',
        cta_quote='طلب عرض سعر',
        cta_specs='المواصفات',
        story_beats=[
            dict(a=0.00, b=0.18, pos='top', h='غطاء <em>فيروزي</em> صلب', p='حلقة قفل على حافة الكيس وفوهة الخزان.', num='١ لتر'),
            dict(a=0.18, b=0.38, pos='bot', h='فلتر <em>كاره للماء</em>', p='فلتر قطع الفيضان (flow stopper) يحمي مسار الشفط المركزي.', num='قطع الفيضان'),
            dict(a=0.38, b=0.58, pos='bot', h='منافذ <em>المريض</em> و<em>التفريغ</em>', p='أنبوب PATIENT ومنفذ VACUUM على الغطاء.', num='PATIENT · VACUUM'),
            dict(a=0.58, b=0.78, pos='top', h='أبعاد <em>اسمية</em> ١ لتر', p='القطر والارتفاع وفق مواصفات منتج آباديس.', num='⌀ ١١ × ١٥٫٥ سم'),
            dict(a=0.78, b=1.01, pos='bot', h='مسحوق <em>التهليم</em>', p='يحتوي مسحوق التهليم؛ عادة ٤٥ قطعة في الكرتون.', num='٤٥ / كرتون'),
        ],
        stats=[
            ('⌀ ١١ سم', 'قطر الكيس'),
            ('١٥٫٥ سم', 'ارتفاع ١ لتر'),
            ('٤٥', 'قطعة في الكرتون'),
            ('IMED / ISO / CE', 'الشهادات'),
        ],
        gal_h='المعرض',
        gal_lead='صور المنتج الحقيقية ورسوم أحادية الزاوية — بدون ورقات كتالوج.',
        sizes_h='الأحجام',
        sizes_lead='١ و٢ و٣ لتر — الرموز وIRC في كل قسم.',
        sizes=[
            ('#s1', '١ لتر', 'ارتفاع ١٥٫٥ سم'),
            ('#s2', '٢ لتر', 'ارتفاع ٢٤٫٥ سم'),
            ('#s3', '٣ لتر', 'ارتفاع ٣٩ سم'),
        ],
        compat_h='التوافق والملحقات',
        compat_lead='متوافق مع أجهزة الشفط المحمولة والمركزية.',
        compat=[
            ('../خزانات/', 'الخزانات'),
            ('../تثبیت/', 'القواعد والحوامل'),
            ('../الوصلات/', 'الوصلات'),
            ('../الفلتر/', 'الفلاتر'),
        ],
        close_h='جاهز لعرض السعر أو تنزيل الكتالوج؟',
        close_p='فريق مبيعات آباديس يساعد في اختيار الموديل والفلتر والتعبئة.',
        close_sales='اتصل بالمبيعات',
        close_cat='تنزيل الكتالوج',
        close_sales_href='tel:+982192001017',
        close_cat_href='https://abadis-med.com/wp-content/uploads/2022/12/suction-bag-catalog-Fa.pdf',
        poster_alt='صورة منتج كيس الشفط سعة ١ لتر من آباديس',
    ),
}


def head(p):
    return (
        f'<link rel="stylesheet" href="{p}assets/css/suction-bag-apple.css?v={V}">\n'
        f'<link rel="stylesheet" href="{p}assets/css/product-3d-pilot.css?v={V}">\n'
    )


def scripts(p):
    return (
        f'<script type="module" src="{p}assets/js/suction-bag-1l-apple.js?v={V}"></script>\n'
        f'<script type="module" src="{p}assets/js/suction-bag-1l-3d-gate.js?v={V}" '
        f'data-f3d-module="{p}assets/js/suction-bag-1l-3d.js?v={V}"></script>\n'
    )


def sticky(lang='fa'):
    c = COPY[lang]
    return (
        f'<div class="bag-sticky" role="region" aria-label="{esc(c["sticky_name"])}">'
        f'<strong>{esc(c["sticky_name"])}</strong>'
        f'<a class="btn btn-primary" href="{esc(c["quote_href"])}">{esc(c["quote"])}</a></div>\n'
    )


def hero(p, lang='fa'):
    c = COPY[lang]
    poster = p + 'assets/img/p/p1-main.webp'
    return f'''  <section class="bag-hero" id="hero" data-bag-apple-hero aria-label="{esc(c["hero_h1"])}">
    <div class="bag-hero-stage">
      <img class="bag-hero-poster" src="{poster}" width="900" height="900" alt="{esc(c["poster_alt"])}" fetchpriority="high" decoding="async">
      <canvas aria-hidden="true"></canvas>
    </div>
    <div class="bag-hero-fade" aria-hidden="true"></div>
    <div class="bag-hero-copy">
      <p class="bag-hero-kicker">{esc(c["hero_kicker"])}</p>
      <h1>{esc(c["hero_h1"])}</h1>
      <p class="bag-hero-tag">{esc(c["hero_tag"])}</p>
      <div class="bag-hero-ctas">
        <a class="btn-primary" href="{esc(c["quote_href"])}">{esc(c["cta_quote"])}</a>
        <a class="btn-ghost" href="#specs">{esc(c["cta_specs"])}</a>
      </div>
    </div>
  </section>
'''


def story(p, lang='fa'):
    c = COPY[lang]
    beats = ''
    for b in c['story_beats']:
        beats += (
            f'<div class="bag-story-beat {b["pos"]}" data-a="{b["a"]}" data-b="{b["b"]}">'
            f'<h2>{b["h"]}</h2><p>{esc(b["p"])}</p>'
            f'<span class="num">{esc(b["num"])}</span></div>'
        )
    stills = ''.join(
        f'<img class="bag-story-still" src="{p}assets/img/products/3d/apple-stills/still-{i:02d}.webp" '
        f'width="1200" height="900" alt="" loading="lazy" decoding="async" style="opacity:{1 if i==0 else 0}">'
        for i in range(5)
    )
    return f'''  <section class="bag-story" id="story" aria-label="{esc(c["hero_h1"])}">
    <div class="bag-story-track">
      <div class="bag-story-pin" data-bag-apple-story>
        {stills}
        <canvas aria-hidden="true"></canvas>
        <div class="bag-story-bar" aria-hidden="true"></div>
        <div class="bag-story-beats">{beats}</div>
      </div>
    </div>
  </section>
'''


def stats(lang='fa'):
    c = COPY[lang]
    cards = ''.join(
        f'<div class="bag-stat"><b>{esc(v)}</b><span>{esc(l)}</span></div>' for v, l in c['stats']
    )
    return f'  <section class="section bag-stats" id="stats"><div class="wrap"><div class="bag-stats-grid">{cards}</div></div></section>\n'


def gallery(p, lang='fa'):
    c = COPY[lang]
    # Real photos + clean single-view sketches only (no catalog sheets)
    items = [
        # Original light-studio photos only (no cutouts / no black boxes)
        ('assets/img/p/p1-g2.webp', None, None, 1600, 1067),
        ('assets/img/p/p1-g1.webp', None, None, 1543, 1600),
        ('assets/img/p/p1-g3.webp', None, None, 1600, 1067),
        ('assets/img/p/p1-g4.webp', None, None, 1600, 1067),
        ('assets/img/p/p1-g5.webp', None, None, 1254, 1254),
        # Original black-studio hero photo on matching dark card
        ('assets/img/p/p1-main.webp', None, 'studio-main', 900, 900),
        ('assets/img/products/3d/p01-1l-liner-light.webp', 'assets/img/products/3d/p01-1l-liner-dark.webp', 'studio', 1067, 1200),
        ('assets/img/products/3d/p01-sketch-wire-light.webp', 'assets/img/products/3d/p01-sketch-wire-dark.webp', 'wire', 889, 1000),
        ('assets/img/products/3d/p01-1l-liner-iso-light.webp', 'assets/img/products/3d/p01-1l-liner-iso-dark.webp', 'iso', 662, 662),
        ('assets/img/products/3d/p01-gal-side.webp', None, 'side', 750, 1000),
        ('assets/img/products/3d/p01-gal-threeq.webp', None, '3q', 750, 1000),
        ('assets/img/products/3d/p01-gal-top.webp', None, 'top', 750, 1000),
    ]
    cards = []
    for light, dark, label, w, h in items:
        theme_pair = bool(dark and dark.endswith('.webp') and 'products/3d' in dark)
        extra_cls = ' bag-gal-item--studio' if label == 'studio-main' else ''
        if theme_pair:
            alt = c['gal_h'] + ' — ' + str(label)
            inner = (
                f'<span class="theme-sketch"><img class="ts-light" src="{p}{light}" width="{w}" height="{h}" alt="{esc(alt)}" loading="lazy" decoding="async">'
                f'<img class="ts-dark" src="{p}{dark}" width="{w}" height="{h}" alt="" loading="lazy" decoding="async" aria-hidden="true"></span>'
            )
            href = p + light
        else:
            if dark and dark.startswith('assets/img/p/'):
                thumb = p + dark
                href = p + light
            else:
                thumb = p + light
                href = p + light
            alt = c['poster_alt'] if label in (None, 'studio-main') else (c['gal_h'] + ' — ' + str(label))
            inner = f'<img src="{thumb}" width="{w}" height="{h}" alt="{esc(alt)}" loading="lazy" decoding="async">'
        cards.append(
            f'<a class="bag-gal-item{extra_cls}" href="{href}" data-gallery="apple-gal" data-w="{w}" data-h="{h}">'
            f'<figure>{inner}</figure></a>'
        )
    return (
        f'  <section class="section bag-gal" id="gallery"><div class="wrap">'
        f'<div class="bag-gal-head"><h2>{esc(c["gal_h"])}</h2><p>{esc(c["gal_lead"])}</p></div>'
        f'<div class="bag-gal-rail">{"".join(cards)}</div></div></section>\n'
    )


def sizes(lang='fa'):
    c = COPY[lang]
    cards = ''.join(
        f'<a class="bag-size-card" href="{href}"><strong>{esc(t)}</strong><em>{esc(s)}</em></a>'
        for href, t, s in c['sizes']
    )
    return (
        f'  <section class="section bag-sizes" id="sizes"><div class="wrap">'
        f'<div class="bag-section-head"><h2>{esc(c["sizes_h"])}</h2><p>{esc(c["sizes_lead"])}</p></div>'
        f'<div class="bag-sizes-grid">{cards}</div></div></section>\n'
    )


def compat(lang='fa'):
    c = COPY[lang]
    cards = ''.join(f'<a href="{esc(h)}">{esc(t)}</a>' for h, t in c['compat'])
    return (
        f'  <section class="section bag-compat" id="compat"><div class="wrap">'
        f'<div class="bag-section-head"><h2>{esc(c["compat_h"])}</h2><p>{esc(c["compat_lead"])}</p></div>'
        f'<div class="bag-compat-grid">{cards}</div></div></section>\n'
    )


def closing(lang='fa'):
    c = COPY[lang]
    return (
        f'  <section class="bag-close" id="close-cta"><div class="wrap">'
        f'<h2>{esc(c["close_h"])}</h2><p>{esc(c["close_p"])}</p>'
        f'<div class="cta-row">'
        f'<a class="btn-primary" href="{esc(c["close_sales_href"])}">{esc(c["close_sales"])}</a>'
        f'<a class="btn-ghost" href="{esc(c["close_cat_href"])}" target="_blank" rel="noopener">{esc(c["close_cat"])}</a>'
        f'</div></div></section>\n'
    )


def apple_prefix(p, lang='fa'):
    """Hero + sticky + story + stats + gallery + sizes + compat — inserted near top of main."""
    return (
        sticky(lang)
        + hero(p, lang)
        + story(p, lang)
        + stats(lang)
        + gallery(p, lang)
        + sizes(lang)
        + compat(lang)
    )


def apple_suffix(lang='fa'):
    return closing(lang)
