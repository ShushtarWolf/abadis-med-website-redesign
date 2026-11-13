#!/usr/bin/env python3
"""Rebuild the canister product pages (FA / EN / AR) in the approved suction bag
page style: cinematic hero driven by the vertical 1 / 2 / 3 L size switch, size
panels with the product gallery, a tap-to-load solid 3D viewer, CAD drawings in
a tech-specs tab, and the 0402102 / 0402103 hose sets as labelled set variants.

Every piece of the original page text is carried over verbatim (only regrouped).
The source is the page as of commit BASE, so the build is repeatable.
"""
import html
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / 'site'
BASE = '8e1fad5f'
V = '20261113b'
FA_DIG = str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')
AR_DIG = str.maketrans('0123456789', '٠١٢٣٤٥٦٧٨٩')
TO_LAT = str.maketrans('۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩', '01234567890123456789')

ARROW = ('<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
         '<path d="M9 5l7 7-7 7" fill="none" stroke="currentColor" stroke-width="2" '
         'stroke-linecap="round" stroke-linejoin="round"/></svg>')
CUBE = ('<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M12 3l8 4.5v9L12 21l-8-4.5v-9z'
        'M4 7.5l8 4.5 8-4.5M12 12v9" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg>')
PLAY = ('<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M8 5.5v13l11-6.5z" fill="currentColor"/></svg>')

PAGES = {
    'fa': ('products/canister/index.html', '../../'),
    'en': ('en/products/canisters/index.html', '../../../'),
    'ar': ('arabic/خزانات/index.html', '../../'),
}


def esc(s):
    return html.escape(s, quote=True)


def digits(s, lang):
    if lang == 'fa':
        return s.translate(FA_DIG)
    if lang == 'ar':
        return s.translate(AR_DIG)
    return s


def meas(s, lang):
    s = digits(s, lang)
    if lang == 'en':
        return esc(s)
    return re.sub(r'[0-9۰-۹٠-٩]+(?:[./,×\-٫][0-9۰-۹٠-٩]+)*|[A-Za-z][A-Za-z0-9\-]*',
                  lambda m: '<bdi dir="ltr">' + esc(m.group(0)) + '</bdi>', esc(s))


# ---------- official facts (abadis-med.com product pages and infographics) ----------
SIZES = {
    '1': dict(code='0402011', vol='1', od='13', idia='12.2', h='18', w='220', pack='12.2 × 18', carton='36',
              glb='p05-1l', film='p05-cinematic', photo=('c1-photo.webp', 750, 940)),
    '2': dict(code='0402012', vol='2', od='13.5', idia='12.2', h='27', w='346', pack='12.2 × 27', carton='18',
              glb='p05-2l', film='p05-2l-cinematic', photo=('c2-photo.webp', 670, 1240),
              set=dict(code='0402102', w='370', pack='12.2 × 27', glb='p05-2l-set', film='p05-2l-set-cinematic')),
    '3': dict(code='0402013', vol='3', od='13', idia='12.2', h='42', w='900', pack='12.2 × 42', carton='16',
              glb='p05-3l', film='p05-3l-cinematic', photo=('c3-photo.webp', 626, 1600),
              set=dict(code='0402103', w='925', pack='12.2 × 42', glb='p05-3l-set', film='p05-3l-set-cinematic')),
}

UI = {
    'fa': dict(
        sizes_nav='اندازه‌ها', quote='درخواست قیمت', next='بعدی', prev='قبلی',
        beats=[(.02, .18, 'پلی‌کربنات شفاف، مدرج و قابل اتوکلاو'),
               (.22, .40, 'درجه‌بندی و نشان آبادیس، چاپ‌شده روی بدنه'),
               (.44, .60, 'پایهٔ نصب پشت مخزن، برای پایه، کنسول تخت و دیوار'),
               (.64, .80, 'سه اندازه: ۱، ۲ و ۳ لیتر'),
               (.84, .99, 'مدل سه‌بعدی از فایل CAD واقعی مخزن')],
        hero_pick='اندازهٔ مخزن در فیلم',
        still_alt='مخزن ساکشن پلی‌کربنات شفاف آبادیس با درجه‌بندی چاپی',
        intro_h='مخزن ساکشن پلی‌کربنات آبادیس',
        sizes_h='اندازه‌ها، کدها و مشخصات',
        sizes_lead='اندازه را انتخاب کنید. فیلم بالای صفحه هم همان اندازه را نشان می‌دهد. مخزن‌های ۲ و ۳ لیتری نسخهٔ ست با شلنگ و اتصالات هم دارند.',
        names={'1': '۱ لیتری', '2': '۲ لیتری', '3': '۳ لیتری'},
        hts={'1': 'ارتفاع ۱۸ سانتی‌متر', '2': 'ارتفاع ۲۷ سانتی‌متر', '3': 'ارتفاع ۴۲ سانتی‌متر'},
        facts_h='اندازه', vol='حجم', od='قطر بیرونی', idia='قطر داخلی', ht='ارتفاع', code='کد کالا',
        lit='لیتر', cm='سانتی‌متر', g='گرم',
        gal_h='تصاویر محصول',
        cap_photo='مخزن ساکشن {n} آبادیس، پلی‌کربنات شفاف با درجه‌بندی چاپی',
        cap_trio='مخازن ساکشن ۱، ۲ و ۳ لیتری آبادیس کنار هم',
        cap_dim='ابعاد رسمی مخزن {n}: قطر بیرونی و داخلی و ارتفاع',
        cap_liner2='مخزن ۲ لیتری با کیسه ساکشن، شلنگ‌ها و اتصالات',
        cap_liner3='کیسه ساکشن ۳ لیتری کنار مخزن مدرج',
        iso_cap='طرح خطی ایزومتریک از CAD. برای چرخش، روی دکمه بزنید و بکشید.',
        iso_load='نمایش طرح تعاملی',
        solid_h='مدل سه‌بعدی',
        solid_cap='مدل سه‌بعدی مخزن {n} از فایل CAD واقعی. برای چرخش، روی دکمه بزنید و بکشید.',
        solid_set_cap='مدل سه‌بعدی ست {c}: مخزن از CAD واقعی؛ شلنگ و اتصالات از روی عکس‌های رسمی (تقریبی).',
        solid_load='نمایش مدل سه‌بعدی',
        v_can='مخزن', v_set='ست با شلنگ و اتصالات',
        codes_h='کد کالا',
        tech_h='مشخصات فنی', tab_specs='مشخصات', tab_cad='نقشه‌های CAD',
        pk_w='وزن', pk_dim='ابعاد', pk_pack='بسته‌بندی', pk_qty='تعداد در بسته', pk_carton='تعداد در کارتن',
        nylon='نایلون', one='۱ عدد', pcs='عدد',
        spec_src='منبع: صفحهٔ محصول در abadis-med.com.',
        cad_front='نمای روبه‌رو', cad_top='نمای بالا', cad_set='ست',
        cad_note='نقشه‌ها از فایل CAD واقعی مخزن اندازه‌گیری شده‌اند (قطر بدنه در CAD). در نقشهٔ ست، شلنگ و اتصالات تقریبی است.',
        film='تماشای فیلم سه‌بعدی مخزن {n}', film_set='تماشای فیلم سه‌بعدی ست {c}',
        set_h='نسخهٔ ست {c}: مخزن {n} با شلنگ و اتصالات',
        set_p='همان مخزن {n}، همراه با کیت شلنگ ۰۵۰۱۰۳: شلنگ سیلیکونی ۱۳×۷ (کد ۰۵۰۱۰۱)، رابط سه‌راهی ۰۳۰۴۰۲ از جنس POM و رابط ۰۳۰۴۰۳ از جنس PE.',
        set_facts_h='اجزای ست',
        k_hose='طول شلنگ', k_hose_v='۳۰ سانتی‌متر', k_total='طول با اتصالات', k_total_v='۳۷ سانتی‌متر',
        k_t='رابط سه‌راهی ۰۳۰۴۰۲', k_t_v='POM، ۵٫۶ سانتی‌متر', k_c='رابط ۰۳۰۴۰۳', k_c_v='PE، ۶ سانتی‌متر',
        k_w='وزن ست', set_gal_h='تصاویر ست',
        cap_kit='شلنگ‌ها و اتصالات آبادیس', cap_kit2='شلنگ سیلیکونی با رابط‌ها', cap_kit_t='رابط سه‌راهی ۰۳۰۴۰۲ (POM)',
        cap_kit_c='رابط ۰۳۰۴۰۳ (PE)', cap_kit_dim='طول شلنگ: ۳۰ سانتی‌متر؛ با اتصالات: ۳۷ سانتی‌متر',
        set_iso_cap='طرح خطی ایزومتریک ست. مخزن از CAD واقعی؛ شلنگ و اتصالات تقریبی.',
        set_note='جفت شدن کدهای ست با کیت شلنگ از روی وزن‌های رسمی استنباط شده است (وزن ست منهای وزن مخزن، حدود ۲۵ گرم، برابر وزن کیت شلنگ).',
        range_h='سایر محصولات این گروه',
        dim_lang='fa',
    ),
    'en': dict(
        sizes_nav='Sizes', quote='Request a quote', next='Next', prev='Previous',
        beats=[(.02, .18, 'Transparent polycarbonate, graduated and autoclavable'),
               (.22, .40, 'Graduations and the Abadis mark, printed on the body'),
               (.44, .60, 'Rear mount for stands, bed consoles and walls'),
               (.64, .80, 'Three sizes: 1, 2 and 3 litres'),
               (.84, .99, '3D model from the genuine canister CAD')],
        hero_pick='Canister size in the film',
        still_alt='Abadis transparent polycarbonate suction canister with printed graduations',
        intro_h='Abadis polycarbonate suction canister',
        sizes_h='Sizes, codes and specifications',
        sizes_lead='Pick a size. The film at the top of the page shows the same size. The 2 L and 3 L canisters also come as a set with hose and connectors.',
        names={'1': '1 litre', '2': '2 litres', '3': '3 litres'},
        hts={'1': 'Height 18 cm', '2': 'Height 27 cm', '3': 'Height 42 cm'},
        facts_h='Size', vol='Volume', od='Outer diameter', idia='Inner diameter', ht='Height', code='Product code',
        lit='L', cm='cm', g='g',
        gal_h='Product images',
        cap_photo='Abadis {n} suction canister, transparent polycarbonate with printed graduations',
        cap_trio='Abadis 1, 2 and 3 litre suction canisters side by side',
        cap_dim='Official dimensions of the {n} canister: outer and inner diameter, height',
        cap_liner2='2-litre canister with suction liner, tubing and connectors',
        cap_liner3='3-litre suction liner beside the graduated canister',
        iso_cap='Isometric line drawing from CAD. Tap the button, then drag to turn it.',
        iso_load='Show the interactive drawing',
        solid_h='3D model',
        solid_cap='3D model of the {n} canister from the genuine CAD. Tap the button, then drag to turn it.',
        solid_set_cap='3D model of set {c}: canister from the genuine CAD; hose and connectors modelled from the official photos (estimated).',
        solid_load='Show the 3D model',
        v_can='Canister', v_set='Set with hose and connectors',
        codes_h='Product code',
        tech_h='Technical specifications', tab_specs='Specifications', tab_cad='CAD drawings',
        pk_w='Weight', pk_dim='Dimensions', pk_pack='Packaging', pk_qty='Quantity per pack', pk_carton='Quantity per carton',
        nylon='Nylon', one='1 pc', pcs='pcs',
        spec_src='Source: the product page on abadis-med.com.',
        cad_front='Front view', cad_top='Top view', cad_set='Set',
        cad_note='Drawings are measured from the genuine canister CAD (body diameter in CAD). In the set drawing, the hose and connectors are estimated.',
        film='Watch the {n} canister 3D film', film_set='Watch the set {c} 3D film',
        set_h='Set {c}: {n} canister with hose and connectors',
        set_p='The same {n} canister with hose kit 050103: 13×7 silicone hose (code 050101), T connector 030402 in POM and connector 030403 in PE.',
        set_facts_h='What the set includes',
        k_hose='Hose length', k_hose_v='30 cm', k_total='Length with connectors', k_total_v='37 cm',
        k_t='T connector 030402', k_t_v='POM, 5.6 cm', k_c='Connector 030403', k_c_v='PE, 6 cm',
        k_w='Set weight', set_gal_h='Set images',
        cap_kit='Abadis hoses and connectors', cap_kit2='Silicone hose with connectors', cap_kit_t='T connector 030402 (POM)',
        cap_kit_c='Connector 030403 (PE)', cap_kit_dim='Hose length 30 cm; 37 cm with connectors',
        set_iso_cap='Isometric line drawing of the set. Canister from the genuine CAD; hose and connectors estimated.',
        set_note='The pairing of the set codes with the hose kit is inferred from the official weights (set weight minus canister weight, about 25 g, matches the hose kit).',
        range_h='More in this range',
        dim_lang='en',
    ),
    'ar': dict(
        sizes_nav='المقاسات', quote='طلب السعر', next='التالي', prev='السابق',
        beats=[(.02, .18, 'بولي كربونات شفاف، مُدرَّج وقابل للتعقيم بالأوتوكلاف'),
               (.22, .40, 'التدريج وشعار آباديس مطبوعان على الجسم'),
               (.44, .60, 'قاعدة تثبيت خلفية للحامل وكونسول السرير والجدار'),
               (.64, .80, 'ثلاثة مقاسات: ١ و٢ و٣ لتر'),
               (.84, .99, 'نموذج ثلاثي الأبعاد من ملف CAD الحقيقي للخزان')],
        hero_pick='مقاس الخزان في الفيلم',
        still_alt='خزان شفط آباديس من البولي كربونات الشفاف مع تدريج مطبوع',
        intro_h='خزان الشفط آباديس من البولي كربونات',
        sizes_h='المقاسات والرموز والمواصفات',
        sizes_lead='اختر المقاس. يعرض الفيلم أعلى الصفحة المقاس نفسه. يتوفر خزانا ٢ و٣ لتر أيضاً كطقم مع الخرطوم والوصلات.',
        names={'1': '١ لتر', '2': '٢ لتر', '3': '٣ لتر'},
        hts={'1': 'الارتفاع ١٨ سم', '2': 'الارتفاع ٢٧ سم', '3': 'الارتفاع ٤٢ سم'},
        facts_h='المقاس', vol='السعة', od='القطر الخارجي', idia='القطر الداخلي', ht='الارتفاع', code='رمز المنتج',
        lit='لتر', cm='سم', g='غرام',
        gal_h='صور المنتج',
        cap_photo='خزان شفط آباديس {n}، بولي كربونات شفاف مع تدريج مطبوع',
        cap_trio='خزانات شفط آباديس ١ و٢ و٣ لتر جنباً إلى جنب',
        cap_dim='الأبعاد الرسمية لخزان {n}: القطر الخارجي والداخلي والارتفاع',
        cap_liner2='خزان ٢ لتر مع كيس الشفط والأنابيب والوصلات',
        cap_liner3='كيس شفط ٣ لتر بجانب الخزان المدرج',
        iso_cap='رسم خطي متساوي القياس من CAD. اضغط الزر ثم اسحب للتدوير.',
        iso_load='عرض الرسم التفاعلي',
        solid_h='نموذج ثلاثي الأبعاد',
        solid_cap='نموذج ثلاثي الأبعاد لخزان {n} من ملف CAD الحقيقي. اضغط الزر ثم اسحب للتدوير.',
        solid_set_cap='نموذج ثلاثي الأبعاد للطقم {c}: الخزان من CAD الحقيقي؛ الخرطوم والوصلات من الصور الرسمية (تقديري).',
        solid_load='عرض النموذج ثلاثي الأبعاد',
        v_can='الخزان', v_set='طقم مع الخرطوم والوصلات',
        codes_h='رمز المنتج',
        tech_h='المواصفات الفنية', tab_specs='المواصفات', tab_cad='رسومات CAD',
        pk_w='الوزن', pk_dim='الأبعاد', pk_pack='التغليف', pk_qty='العدد في العبوة', pk_carton='العدد في الكرتون',
        nylon='نايلون', one='١ قطعة', pcs='قطعة',
        spec_src='المصدر: صفحة المنتج على abadis-med.com.',
        cad_front='منظر أمامي', cad_top='منظر علوي', cad_set='الطقم',
        cad_note='الرسومات مقاسة من ملف CAD الحقيقي للخزان (قطر الجسم في CAD). في رسم الطقم، الخرطوم والوصلات تقديرية.',
        film='مشاهدة الفيلم ثلاثي الأبعاد لخزان {n}', film_set='مشاهدة الفيلم ثلاثي الأبعاد للطقم {c}',
        set_h='الطقم {c}: خزان {n} مع الخرطوم والوصلات',
        set_p='خزان {n} نفسه مع طقم الخرطوم ٠٥٠١٠٣: خرطوم سيليكون ١٣×٧ (رمز ٠٥٠١٠١)، ووصلة T رقم ٠٣٠٤٠٢ من POM، ووصلة ٠٣٠٤٠٣ من PE.',
        set_facts_h='مكونات الطقم',
        k_hose='طول الخرطوم', k_hose_v='٣٠ سم', k_total='الطول مع الوصلات', k_total_v='٣٧ سم',
        k_t='وصلة T ٠٣٠٤٠٢', k_t_v='POM، ٥٫٦ سم', k_c='وصلة ٠٣٠٤٠٣', k_c_v='PE، ٦ سم',
        k_w='وزن الطقم', set_gal_h='صور الطقم',
        cap_kit='خراطيم ووصلات آباديس', cap_kit2='خرطوم سيليكون مع الوصلات', cap_kit_t='وصلة T ٠٣٠٤٠٢ (POM)',
        cap_kit_c='وصلة ٠٣٠٤٠٣ (PE)', cap_kit_dim='طول الخرطوم ٣٠ سم؛ ٣٧ سم مع الوصلات',
        set_iso_cap='رسم خطي متساوي القياس للطقم. الخزان من CAD الحقيقي؛ الخرطوم والوصلات تقديرية.',
        set_note='رُبطت رموز الطقم بطقم الخرطوم استنتاجاً من الأوزان الرسمية (وزن الطقم ناقص وزن الخزان، نحو ٢٥ غراماً، يساوي وزن طقم الخرطوم).',
        range_h='منتجات أخرى في هذه المجموعة',
        dim_lang='en',
    ),
}


def grab(pat, s, flags=re.S):
    m = re.search(pat, s, flags)
    if not m:
        raise SystemExit('missing: ' + pat)
    return m


# ---------- markup pieces ----------
def card(src, w, h, cap, cls='gal-card', eager=False):
    return (f'<figure class="{cls}"><div class="gal-frame">'
            f'<img src="{src}" alt="{esc(cap)}" width="{w}" height="{h}" loading="{"eager" if eager else "lazy"}" decoding="async">'
            f'</div><figcaption>{esc(cap)}</figcaption></figure>')


def iso_card(pfx, mid, model, cap, load):
    still = f'{pfx}assets/img/products/cad-iso/{mid}-iso'
    return (f'<figure class="gal-card gal-iso gal-contain"><div class="gal-frame-slot">'
            f'<div class="iso-frame gal-frame" data-iso data-iso-kind="canister" data-iso-id="{mid}" '
            f'data-iso-src="{pfx}3d-sketches/cad-line-sketches/models/{model}.glb?v={V}">'
            f'<img class="iso-still iso-still-light" src="{still}-light.webp?v={V}" alt="{esc(cap)}" width="900" height="1125" loading="lazy" decoding="async">'
            f'<img class="iso-still iso-still-dark" src="{still}-dark.webp?v={V}" alt="" width="900" height="1125" loading="lazy" decoding="async" aria-hidden="true">'
            f'<button class="iso-load" type="button">{esc(load)}</button></div></div>'
            f'<figcaption>{esc(cap)}</figcaption></figure>')


def gallery(cards, ui):
    return (f'<div class="gal" data-gal><div class="gal-rail">{"".join(cards)}</div>'
            f'<div class="gal-nav"><button class="gal-arrow gal-prev" type="button" aria-label="{esc(ui["prev"])}">{ARROW}</button>'
            f'<div class="gal-dots"></div>'
            f'<button class="gal-arrow gal-next" type="button" aria-label="{esc(ui["next"])}">{ARROW}</button></div></div>')


def solid_frame(pfx, mid, cap, load, hidden=False):
    st = f'{pfx}assets/img/products/3d/{mid}-still'
    hid = ' hidden' if hidden else ''
    return (f'<div class="solid-frame" data-solid data-solid-id="{mid}"{hid}>'
            f'<img class="solid-still solid-still-light" src="{st}-light.webp?v={V}" alt="{esc(cap)}" width="1280" height="800" loading="lazy" decoding="async">'
            f'<img class="solid-still solid-still-dark" src="{st}-dark.webp?v={V}" alt="" width="1280" height="800" loading="lazy" decoding="async" aria-hidden="true">'
            f'<button class="solid-load" type="button">{CUBE}<span>{esc(load)}</span></button>'
            f'<p class="solid-caption">{esc(cap)}</p></div>')


def fact_grid(cells, lang):
    return '<div class="size-fact-grid">' + ''.join(
        f'<div class="size-fact"><span class="size-fact-lbl">{esc(a)}</span><b class="size-fact-val">{meas(b, lang)}</b></div>'
        for a, b in cells) + '</div>'


def cad_fig(pfx, mid, view, cap):
    p = f'{pfx}assets/img/canister/cad/{mid}-{view}'
    return (f'<figure class="cad-fig">'
            f'<img class="cad-light" src="{p}-light.webp?v={V}" alt="{esc(cap)}" loading="lazy" decoding="async">'
            f'<img class="cad-dark" src="{p}-dark.webp?v={V}" alt="" loading="lazy" decoding="async" aria-hidden="true">'
            f'<figcaption>{esc(cap)}</figcaption></figure>')


def code_rows(table_html, codes):
    """Rows of the original code table for these codes, verbatim."""
    head = grab(r'<thead>.*?</thead>', table_html).group(0)
    rows = re.findall(r'<tr><td>.*?</td></tr>', table_html)
    keep = [r for r in rows if re.sub(r'<[^>]+>', '', r).translate(TO_LAT).strip().endswith(tuple(codes))]
    return f'<div class="table-wrap code-pick"><table>{head}<tbody>{"".join(keep)}</tbody></table></div>'


def size_panel(size, lang, pfx, ui, table_html):
    d = SIZES[size]
    n = ui['names'][size]
    cm, g = ui['cm'], ui['g']
    facts = fact_grid([
        (ui['vol'], f'{d["vol"]} {ui["lit"]}'),
        (ui['od'], f'{d["od"]} {cm}'),
        (ui['idia'], f'{d["idia"]} {cm}'),
        (ui['ht'], f'{d["h"]} {cm}'),
        (ui['code'], d['code']),
    ], lang)
    dim_src = f'{pfx}assets/img/canister/c{size}-dim-{ui["dim_lang"]}.webp?v={V}'
    pw, ph = d['photo'][1], d['photo'][2]
    cards = [card(f'{pfx}assets/img/canister/{d["photo"][0]}?v={V}', pw, ph, ui['cap_photo'].format(n=n), 'gal-card gal-contain', eager=True),
             card(f'{pfx}assets/img/canister/c-trio-4901.webp?v={V}', 1600, 1301, ui['cap_trio'])]
    if size == '2':
        cards.append(card(f'{pfx}assets/img/canister/c2-liner-hoses-4779.webp?v={V}', 1600, 1600, ui['cap_liner2']))
    if size == '3':
        cards.append(card(f'{pfx}assets/img/p/p3-g1.webp', 1200, 800, ui['cap_liner3']))
    cards.append(card(dim_src, 1200, 1200, ui['cap_dim'].format(n=n), 'gal-card gal-contain gal-diagram'))
    cards.append(iso_card(pfx, d['glb'], f'{d["glb"]}-canister', ui['iso_cap'], ui['iso_load']))
    out = [f'<div class="size-facts" id="s{size}-size" data-sec="size"><h3>{esc(ui["facts_h"])}</h3>{facts}</div>',
           f'<div class="size-gal" id="s{size}-gallery" data-sec="gallery"><h3>{esc(ui["gal_h"])}</h3>{gallery(cards, ui)}</div>']
    # solid 3D viewer (canister, plus the set variant on 2 L / 3 L)
    st = d.get('set')
    toggle = ''
    frames = solid_frame(pfx, d['glb'], ui['solid_cap'].format(n=n), ui['solid_load'])
    if st:
        c = digits(st['code'], lang)
        toggle = (f'<div class="solid-variant" role="group" aria-label="{esc(ui["solid_h"])}">'
                  f'<button type="button" data-solid-show="{d["glb"]}" aria-pressed="true">{esc(ui["v_can"])} <bdi>{digits(d["code"], lang)}</bdi></button>'
                  f'<button type="button" data-solid-show="{st["glb"]}" aria-pressed="false">{esc(ui["v_set"])} <bdi>{c}</bdi></button></div>')
        frames += solid_frame(pfx, st['glb'], ui['solid_set_cap'].format(c=c), ui['solid_load'], hidden=True)
    out.append(f'<div class="size-solid" id="s{size}-model" data-sec="model"><h3>{esc(ui["solid_h"])}</h3>{toggle}<div class="solid-stack">{frames}</div></div>')
    # codes, verbatim rows from the original table
    codes = [d['code']] + ([st['code']] if st else [])
    out.append(f'<div class="size-codes" id="s{size}-codes" data-sec="codes"><h3>{esc(ui["codes_h"])}</h3>{code_rows(table_html, codes)}</div>')
    # set variant
    if st:
        c = digits(st['code'], lang)
        kit_cards = [
            card(f'{pfx}assets/img/canister/kit-23.webp?v={V}', 1030, 885, ui['cap_kit'], 'gal-card gal-contain', eager=False),
            card(f'{pfx}assets/img/canister/kit-dim-{ui["dim_lang"]}.webp?v={V}', 1400, 700, ui['cap_kit_dim'], 'gal-card gal-contain gal-diagram'),
            card(f'{pfx}assets/img/canister/kit-4789.webp?v={V}', 1600, 1067, ui['cap_kit2']),
            card(f'{pfx}assets/img/canister/kit-t-18.webp?v={V}', 1030, 736, ui['cap_kit_t'], 'gal-card gal-contain'),
            card(f'{pfx}assets/img/canister/kit-conn-20.webp?v={V}', 1030, 1030, ui['cap_kit_c'], 'gal-card gal-contain'),
            iso_card(pfx, st['glb'], st['glb'], ui['set_iso_cap'], ui['iso_load']),
        ]
        sf = fact_grid([
            (ui['code'], st['code']),
            (ui['k_w'], f'{st["w"]} {g}'),
            (ui['k_hose'], ui['k_hose_v']),
            (ui['k_total'], ui['k_total_v']),
            (ui['k_t'], ui['k_t_v']),
            (ui['k_c'], ui['k_c_v']),
        ], lang)
        out.append(
            f'<div class="size-set" id="s{size}-set" data-sec="set">'
            f'<p class="set-tag">{esc(ui["cad_set"])} <bdi>{c}</bdi></p>'
            f'<h3>{esc(ui["set_h"].format(c=c, n=n))}</h3>'
            f'<p class="bag-lead">{esc(ui["set_p"].format(n=n))}</p>'
            f'<h4>{esc(ui["set_facts_h"])}</h4>{sf}'
            f'<h4>{esc(ui["set_gal_h"])}</h4>{gallery(kit_cards, ui)}'
            f'<p class="set-note">{esc(ui["set_note"])}</p>'
            f'<p class="film-row"><a class="btn-ghost film-link" href="{pfx}3d-sketches/{st["film"]}/">{PLAY}<span>{esc(ui["film_set"].format(c=c))}</span></a></p>'
            f'</div>')
    # tech specs tabs
    rows = [(ui['pk_w'], f'{d["w"]} {g}'), (ui['pk_dim'], f'{d["pack"]} {cm}'), (ui['pk_pack'], ui['nylon']),
            (ui['pk_qty'], ui['one']), (ui['pk_carton'], f'{d["carton"]} {ui["pcs"]}')]
    spec_tbl = ''.join(f'<tr><th scope="row">{esc(a)}</th><td>{meas(b, lang)}</td></tr>' for a, b in rows)
    if st:
        spec_tbl += (f'<tr><th scope="row">{esc(ui["k_w"])} <bdi>{digits(st["code"], lang)}</bdi></th><td>{meas(st["w"] + " " + g, lang)}</td></tr>')
    cad = [cad_fig(pfx, d['glb'], 'front', ui['cad_front']), cad_fig(pfx, d['glb'], 'top', ui['cad_top'])]
    if st:
        cad += [cad_fig(pfx, st['glb'], 'front', f'{ui["cad_set"]} {digits(st["code"], lang)}: {ui["cad_front"]}'),
                cad_fig(pfx, st['glb'], 'top', f'{ui["cad_set"]} {digits(st["code"], lang)}: {ui["cad_top"]}')]
    tid = f's{size}-tech'
    out.append(
        f'<div class="size-tech" id="{tid}" data-sec="specs"><h3>{esc(ui["tech_h"])}</h3>'
        f'<div class="spec-tabs" role="tablist">'
        f'<button type="button" role="tab" id="{tid}-t1" aria-controls="{tid}-p1" aria-selected="true">{esc(ui["tab_specs"])}</button>'
        f'<button type="button" role="tab" id="{tid}-t2" aria-controls="{tid}-p2" aria-selected="false" tabindex="-1">{esc(ui["tab_cad"])}</button></div>'
        f'<div class="spec-pane" role="tabpanel" id="{tid}-p1" aria-labelledby="{tid}-t1">'
        f'<table class="pack-table"><tbody>{spec_tbl}</tbody></table><p class="spec-src">{esc(ui["spec_src"])}</p></div>'
        f'<div class="spec-pane" role="tabpanel" id="{tid}-p2" aria-labelledby="{tid}-t2" hidden>'
        f'<div class="cad-grid">{"".join(cad)}</div><p class="spec-src">{esc(ui["cad_note"])}</p></div>'
        f'</div>')
    out.append(f'<p class="film-row"><a class="btn-ghost film-link" href="{pfx}3d-sketches/{d["film"]}/">{PLAY}<span>{esc(ui["film"].format(n=n))}</span></a></p>')
    hidden = '' if size == '1' else ' hidden'
    return (f'<div class="bag-panel" role="tabpanel" id="s{size}" data-size="{size}" aria-labelledby="tab-s{size}"{hidden}>'
            + ''.join(out) + '</div>')


def size_picker(ui, lang, cls='size-pick size-pick-vert', btn='size-pick-btn', ids=True):
    b = []
    for i, s in enumerate(('1', '2', '3')):
        sel = 'true' if i == 0 else 'false'
        idattr = f' role="tab" id="tab-s{s}" aria-controls="s{s}" aria-selected="{sel}" tabindex="{0 if i == 0 else -1}"' if ids else f' aria-pressed="{sel}"'
        b.append(f'<button class="{btn}" type="button" data-size="{s}"{idattr}>'
                 f'<strong>{esc(ui["names"][s])}</strong><em>{esc(ui["hts"][s])}</em></button>')
    role = ' role="tablist" aria-labelledby="sizes-h"' if ids else f' role="group" aria-label="{esc(ui["hero_pick"])}"'
    return f'<div class="{cls}"{role}>{"".join(b)}</div>'


def main_html(lang, pfx, orig_main):
    ui = UI[lang]
    crumbs = grab(r'<p class="crumbs">(.*?)</p>', orig_main).group(1)
    h1 = grab(r'<h1>(.*?)</h1>', orig_main).group(1)
    badge = grab(r'<p class="ps-hero-badge">.*?</p>', orig_main).group(0)
    lead = grab(r'<p class="lead">(.*?)</p>', orig_main).group(1)
    anchors = grab(r'<nav class="anchors" aria-label="([^"]*)"><div class="wrap">(.*?)</div></nav>', orig_main)
    docs = grab(r'<section class="section" id="docs"[^>]*><div class="wrap">(.*?)</div></section>', orig_main).group(1)
    ptab_nav = grab(r'<div class="ptab-nav" role="tablist">(.*?)</div>', orig_main).group(1)
    arts = dict(re.findall(r'<article class="ptab size-block" id="(\w+)">(.*?)</article>', orig_main, re.S))
    assert list(arts) == ['msk', 'sdv', 'collectioncup', 'lipo'], list(arts)
    # Collection Cup 0402300: the archive had no photo; use the official one from
    # abadis-med.com (wp-content/uploads/2026/11/Transparent-Container-with-White-Grid-Basket.png).
    # FA keeps the official image as published; EN / AR use the same image with the
    # Persian "coming soon" badge painted out to the white background.
    cc_alt = {'fa': 'محفظه نمونه گیری(Collection Cup)',
              'en': 'Abadis Collection Cup (code 0402300): transparent cup with a white mesh basket inside',
              'ar': 'كوب جمع العينة آباديس (Collection Cup، رمز ٠٤٠٢٣٠٠): وعاء شفاف بداخله سلة شبكية بيضاء'}[lang]
    cc_img = f'{pfx}assets/img/canister/collection-cup-0402300{"" if lang == "fa" else "-en"}.webp?v={V}'
    cc_fig = (f'<a class="gal-main gal-cc" href="{cc_img}" data-gallery="collectioncup" data-w="1254" data-h="1254" '
              f'aria-label="{esc(cc_alt)}"><img src="{cc_img}" width="1254" height="1254" loading="lazy" decoding="async" alt="{esc(cc_alt)}"></a>')
    arts['collectioncup'], n_cc = re.subn(r'<div class="gal-main gal-missing">.*?</div>', lambda m: cc_fig, arts['collectioncup'], count=1, flags=re.S)
    assert n_cc == 1
    tail = grab(r'(<section class="section ps-related" id="related-solutions">.*)</main>', orig_main).group(1)
    msk = arts['msk']
    msk_h2 = grab(r'<h2>.*?</h2>', msk).group(0)
    msk_grid = grab(r'<div class="size-grid">.*?</div>\s*</div>', msk).group(0)
    msk_table = grab(r'<div class="table-wrap">.*?</div>', msk).group(0)
    # sub-nav: the original anchor links, plus the new sizes link
    links = re.findall(r'<a href="#(\w+)">(.*?)</a>', anchors.group(2))
    nav = []
    for i, t in links:
        nav.append(f'<a href="#{i}">{t}</a>')
        if i == 'msk':
            nav.append(f'<a href="#sizes">{esc(ui["sizes_nav"])}</a>')
    beats = ''.join(f'<p class="beat" data-a="{a}" data-b="{b}">{esc(t)}</p>' for a, b, t in ui['beats'])
    still = f'{pfx}assets/img/products/3d/p05-hero-still.webp?v={V}'
    panels = ''.join(size_panel(s, lang, pfx, ui, msk_table) for s in ('1', '2', '3'))
    more = ''.join(
        f'<section class="bag-block can-range" id="{k}"><div class="wrap"><article class="size-block">{arts[k]}</article></div></section>'
        for k in ('sdv', 'collectioncup', 'lipo'))
    return (
        f'<main id="main">'
        f'<div class="cin-track" id="film" data-cin-root data-cin-floors="hero" data-tone="dark" data-cin-module="./p05-cinematic-page.js?v={V}">'
        f'<div class="cin-stage"><div class="cin-view"><canvas aria-hidden="true"></canvas>'
        f'<img class="cin-still" src="{still}" width="900" height="1338" alt="{esc(ui["still_alt"])}" fetchpriority="high" decoding="async">'
        f'<div class="cin-bar" aria-hidden="true"></div></div>'
        f'{size_picker(ui, lang, "cin-size", "cin-size-btn", ids=False)}'
        f'<div class="cin-copy"><p class="cin-crumb">{crumbs}</p><h1>{h1}</h1>{badge}<div class="cin-beats">{beats}</div></div>'
        f'</div></div>'
        f'<nav class="bag-sub" aria-label="{anchors.group(1)}"><div class="wrap bag-sub-row">'
        f'<div class="bag-sub-scroller">{"".join(nav)}</div>'
        f'<button class="bag-sub-hint" type="button" aria-label="{esc(ui["next"])}">{ARROW}</button>'
        f'<a class="btn-primary" href="#inquiry">{esc(ui["quote"])}</a></div></nav>'
        f'<section class="bag-block bag-intro" id="intro"><div class="wrap">'
        f'<h2>{esc(ui["intro_h"])}</h2><p class="bag-lead">{lead}</p></div></section>'
        f'<section class="bag-block can-msk" id="msk"><div class="wrap"><article class="size-block">{msk_h2}{msk_grid}{msk_table}</article></div></section>'
        f'<section class="bag-block bag-sizes" id="sizes"><div class="wrap">'
        f'<h2 id="sizes-h">{esc(ui["sizes_h"])}</h2><p class="bag-lead">{esc(ui["sizes_lead"])}</p>'
        f'<div class="size-stage">{size_picker(ui, lang)}<div class="size-panels">{panels}</div></div>'
        f'</div></section>'
        f'<section class="bag-block can-range-nav" aria-label="{esc(ui["range_h"])}"><div class="wrap">'
        f'<h2>{esc(ui["range_h"])}</h2><div class="ptab-nav range-nav">{ptab_nav}</div></div></section>'
        f'{more}'
        f'<section class="bag-block can-docs" id="docs"><div class="wrap">{docs}</div></section>'
        f'{tail}'
        f'</main>'
    )


def rebuild(lang):
    rel, pfx = PAGES[lang]
    path = SITE / rel
    src = subprocess.run(['git', 'show', f'{BASE}:site/{rel}'], cwd=ROOT, capture_output=True, check=True).stdout.decode('utf-8')
    orig_main = grab(r'<main id="main">.*?</main>', src).group(0)
    s = src
    if 'ABADIS_BAG_FILM_HEADER' not in s:
        s = s.replace('</head>', '<script>window.ABADIS_BAG_FILM_HEADER=true;</script>\n</head>', 1)
    s = s.replace('</head>', f'<link rel="stylesheet" href="{pfx}assets/css/suction-bag-page.css?v={V}">\n'
                             f'<link rel="stylesheet" href="{pfx}assets/css/canister-page.css?v={V}">\n</head>', 1)
    imap = ('<script type="importmap">{"imports":{"three":"' + pfx + 'assets/vendor/three/build/three.module.js",'
            '"three/addons/":"' + pfx + 'assets/vendor/three/examples/jsm/"}}</script>\n')
    s = s.replace('</head>', imap + '</head>', 1)
    s = re.sub(r'<body[^>]*>', '<body class="page-bag page-canister" data-canister-rebuild="v1">', s, count=1)
    s = s.replace(orig_main, main_html(lang, pfx, orig_main), 1)
    s = s.replace('</body>', f'<script src="{pfx}assets/js/suction-bag-ui.js?v={V}" defer></script>\n'
                             f'<script src="{pfx}assets/js/canister-ui.js?v={V}" defer></script>\n</body>', 1)
    path.write_text(s, encoding='utf-8')
    print(lang, path.relative_to(ROOT), 'bytes', len(s.encode()), 'h1', s.count('<h1>'))


if __name__ == '__main__':
    for lang in ('fa', 'en', 'ar'):
        rebuild(lang)
