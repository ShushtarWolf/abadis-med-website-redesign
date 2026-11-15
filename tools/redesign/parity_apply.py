#!/usr/bin/env python3
"""Apply EN/AR parity fixes onto the current site/ tree.

Keeps each page's existing header and footer (so the same script can run on
main and on liara-test). Does not rebuild the whole site.
"""
import html as htmllib
import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / 'site'
LIVE = Path(os.environ.get('PARITY_LIVE', '/tmp/en-ar-audit/live'))
V = '20261115a'

def read(p):
    return Path(p).read_text(encoding='utf-8')

def write(p, s):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(s, encoding='utf-8')

def replace_main(path, new_main):
    s = read(path)
    s2, n = re.subn(r'<main\b[^>]*>.*?</main>', new_main, s, count=1, flags=re.S)
    if n != 1:
        raise SystemExit(f'main replace failed: {path}')
    write(path, s2)

def set_meta(path, title, desc=None):
    s = read(path)
    s = re.sub(r'<title>.*?</title>', f'<title>{htmllib.escape(title)}</title>', s, count=1, flags=re.S)
    if desc:
        d = htmllib.escape(desc, quote=True)
        s = re.sub(r'(<meta name="description" content=")[^"]*"', rf'\1{d}"', s, count=1)
        s = re.sub(r'(<meta property="og:title" content=")[^"]*"', rf'\1{htmllib.escape(title, quote=True)}"', s, count=1)
        s = re.sub(r'(<meta property="og:description" content=")[^"]*"', rf'\1{d[:300]}"', s, count=1)
    write(path, s)

def insert_before(path, needle, extra, once=True):
    s = read(path)
    if once and extra.strip()[:40] in s:
        return
    if needle not in s:
        raise SystemExit(f'missing needle in {path}: {needle[:60]}')
    write(path, s.replace(needle, extra + needle, 1))

# ---------------------------------------------------------------- footer / dealers / faq / home title
def patch_ar_footer():
    n = 0
    for p in SITE.joinpath('arabic').rglob('index.html'):
        s = read(p)
        i = s.find('<footer')
        if i < 0:
            continue
        head, foot = s[:i], s[i:]
        foot2 = foot
        foot2 = foot2.replace('aria-label="آپارات"', 'aria-label="Aparat"')
        foot2 = foot2.replace('>آپارات<', '>Aparat<')
        foot2 = foot2.replace('aria-label="ویرگول"', 'aria-label="Virgool"')
        foot2 = foot2.replace('aria-label="ويرگول"', 'aria-label="Virgool"')
        foot2 = foot2.replace('>ویرگول<', '>Virgool<')
        foot2 = foot2.replace('>ويرگول<', '>Virgool<')
        foot2 = foot2.replace('بوليفارد گلستان، گلشن ۱۹', 'بوليفارد غولستان، زقاق غولشان ١٩')
        foot2 = foot2.replace('بوليفارد گلستان، گلشن ۱۹، رقم ۱۷', 'بوليفارد غولستان، زقاق غولشان ١٩، رقم ١٧')
        if foot2 != foot:
            write(p, head + foot2)
            n += 1
    print('ar footers', n)

def patch_dealers():
    repls = {
        'en/representatives/index.html': {
            '<dt>مدیر عامل:</dt>': '<dt>Managing director:</dt>',
            '<dt>شماره تلفن:</dt>': '<dt>Phone:</dt>',
            '<dt>آدرس:</dt>': '<dt>Address:</dt>',
        },
        'arabic/قائمة-الممثلين/index.html': {
            '<dt>مدیر عامل:</dt>': '<dt>المدير العام:</dt>',
            '<dt>شماره تلفن:</dt>': '<dt>رقم الهاتف:</dt>',
            '<dt>آدرس:</dt>': '<dt>العنوان:</dt>',
        },
    }
    for rel, mp in repls.items():
        s = read(SITE / rel)
        for a, b in mp.items():
            s = s.replace(a, b)
        write(SITE / rel, s)
    print('dealers ok')

def patch_faq():
    p = SITE / 'site/en/faqs/index.html' if False else SITE / 'en/faqs/index.html'
    s = read(p)
    s = s.replace('>فاقد مدل<', '>No model<')
    write(p, s)
    ap = SITE / 'arabic/پرسش-های-متداول/index.html'
    s = read(ap)
    s = s.replace('<title>پرسش های متداول — خزانات طبي آباديس</title>',
                  '<title>الأسئلة الشائعة — خزانات طبي آباديس</title>')
    s = s.replace('<h1>پرسش های متداول</h1>', '<h1>الأسئلة الشائعة</h1>')
    s = s.replace('وارانتی محصولات شرکت مخازن طبی آبادیس به چه صورت می باشد؟',
                  'كيف يكون ضمان منتجات شركة خزانات آباديس الطبية؟')
    s = s.replace('alt="پرسش های متداول"', 'alt="الأسئلة الشائعة"')
    write(ap, s)
    print('faq ok')

def patch_home_titles():
    set_meta(SITE / 'en/index.html',
             'Pioneer in Hospital Infection Control and Fluid Management — Abadis Medical Reservoirs',
             'Abadis Med, a knowledge-based company: disposable suction liner bags and solutions for managing hospital fluid and infectious waste.')
    set_meta(SITE / 'arabic/index.html',
             'الرائد في مكافحة العدوى وإدارة السوائل الطبية في المستشفيات — خزانات طبي آباديس',
             'شركة خزانات آباديس الطبية المعرفية: أكياس الشفط ذات الاستخدام الواحد وحلول إدارة السوائل والنفايات المعدية.')
    print('home titles ok')

def patch_sustainability():
    write(SITE / 'arabic/sustainability/index.html',
          '<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="utf-8">'
          '<meta name="robots" content="noindex,nofollow">'
          '<link rel="canonical" href="https://abadis-med.com/arabic/sdgs/">'
          '<meta http-equiv="refresh" content="0; url=../sdgs/">'
          '<title>التنمية المستدامة</title></head><body>'
          '<p><a href="../sdgs/">التنمية المستدامة</a></p>'
          '<script>location.replace("../sdgs/")</script></body></html>\n')
    print('sustainability stub')

# ---------------------------------------------------------------- downloads
AR_DOWNLOADS = '''<main id="main">
  <section class="page-hero"><div class="wrap">
    <p class="crumbs"><a href="../../arabic/">الرئيسية</a> › مركز التنزيل</p>
    <h1>مركز التنزيل</h1>
    <p class="lead">كتالوجات وأدلة تركيب منتجات خزانات آباديس الطبية. عند عدم توفر ملف عربي يُستخدم ملف الإنجليزية.</p>
  </div></section>
  <section class="section"><div class="wrap"><div class="post-grid">
    {cards}
  </div>
  <p class="note" style="margin-top:20px">تُنزَّل الملفات من خادم abadis-med.com.</p>
  </div></section>
</main>'''

def _dl(href, img, alt, title):
    return (
        f'<a class="post-card dl-card reveal" href="{href}" target="_blank" rel="noopener">'
        f'<div class="ph" style="aspect-ratio:1;background:#fff"><img src="../../assets/img/c/{img}" width="600" height="600" loading="lazy" decoding="async" alt="{htmllib.escape(alt)}"></div>'
        f'<div class="body"><h3>{htmllib.escape(title)}</h3><span class="go">تنزيل الكتالوج (PDF)</span></div></a>'
    )

def patch_downloads():
    cards = ''.join([
        _dl('../../en/wp-content/uploads/2025/02/Abadis-Catalouge.pdf', 'fbfb29bd37b3-600.webp', 'الكتالوج الشامل', 'الكتالوج الشامل لآباديس'),
        _dl('../../en/wp-content/uploads/2021/12/suction-bag-catalog-En.pdf', '9b1d8607f71e-600.webp', 'كيس الشفط', 'كيس الشفط أحادي الاستعمال'),
        _dl('../../en/wp-content/uploads/2021/12/filters-catalouge-en.pdf', '3e597a3f88f9-600.webp', 'الفلاتر', 'فلاتر خزانات آباديس الطبية'),
        _dl('../../en/wp-content/uploads/2021/12/wall-suction-en.pdf', 'd981ab7fae6e-600.webp', 'الشفط الجداري', 'الشفط الجداري للبالغين'),
        _dl('../../en/wp-content/uploads/2021/12/endotracheal-tube-holder-catalog-ٍ-En.pdf', 'b6aa51502dbf-600.webp', 'حامل أنبوب الرغامي', 'حامل أنبوب الرغامي'),
        _dl('../../en/wp-content/uploads/2024/02/Installation-on-the-console.pdf', '4c5616648faa-600.webp', 'التركيب على الكونسول', 'دليل التركيب على الكونسول'),
        _dl('../../en/wp-content/uploads/2024/02/Installation-on-a-trolley-base.pdf', 'd1d18e4d4b60-600.webp', 'التركيب على قاعدة الترولي', 'دليل التركيب على قاعدة الترولي'),
        _dl('../../en/wp-content/uploads/2024/02/Installation-on-a-rail-bracket.pdf', '0bcc3e66ff94-600.webp', 'التركيب على القاعدة المحمولة', 'دليل التركيب على القاعدة المحمولة'),
    ])
    replace_main(SITE / 'arabic/مركز-التنزيل/index.html', AR_DOWNLOADS.format(cards=cards))
    set_meta(SITE / 'arabic/مركز-التنزيل/index.html', 'مركز التنزيل — خزانات طبي آباديس',
             'كتالوجات وأدلة تركيب منتجات خزانات آباديس الطبية.')
    print('downloads', cards.count('post-card'))

# ---------------------------------------------------------------- calculator
DIAL_EN = None  # filled by translating the FA dial markup

def _dial_from_fa(lang):
    s = read(SITE / 'محاسبه-گر/index.html')
    main = re.search(r'<main id="main">.*?</main>', s, re.S).group(0)
    # drop the FA footer that is outside main; main ends before footer
    pairs = DIAL[lang]
    for a, b in sorted(pairs, key=lambda x: -len(x[0])):
        main = main.replace(a, b)
    # depth: FA is ../  EN/AR calculator is ../../
    main = main.replace('src="../brand/', 'src="../../brand/')
    main = main.replace('href="../brand/', 'href="../../brand/')
    return main

DIAL = {
 'en': [
    ('ابزار محاسبه', 'Calculator'),
    ('محاسبه‌گر صرفه‌جویی <em>آبادیس</em>', 'Abadis <em>savings</em> calculator'),
    ('دایال را با لمس یا ماوس بچرخانید یا عدد را تایپ کنید؛ سه نمایشگر، صرفه‌جویی آب، هزینه شست‌وشو و ضدعفونی و زمان کادر درمان را همزمان نشان می‌دهند.',
     'Turn the dial by touch or mouse, or type a number. Three displays show water saved, washing and disinfection cost, and staff time together.'),
    ('CH-1 · ورودی: تعداد عمل', 'CH-1 · Input: surgeries'),
    ('بر مبنای تعداد عمل جراحی در سال', 'By surgeries per year'),
    ('دایال را با لمس یا ماوس بچرخانید یا عدد را تایپ کنید', 'Turn the dial by touch or mouse, or type a number'),
    ('مقادیر آماده', 'Presets'),
    ('آبادیس', 'Abadis'),
    ('تعداد عمل در سال (۰ تا ۱۵٬۰۰۰)', 'Surgeries per year (0 to 15,000)'),
    ('تعداد عمل در سال', 'Surgeries per year'),
    ('صرفه‌جویی در مصرف آب', 'Water saved'),
    ('>لیتر<', '>litres<'),
    ('هزینه شست‌وشو و ضدعفونی', 'Washing and disinfection cost'),
    ('>تومان<', '>toman<'),
    ('زمان کادر درمان', 'Staff time'),
    ('>ساعت<', '>hours<'),
    ('مشاوره با کارشناس فروش', 'Talk to a sales specialist'),
    ('CH-2 · ورودی: تعداد تخت', 'CH-2 · Input: beds'),
    ('بر مبنای تعداد تخت', 'By number of beds'),
    ('مرحله ۱: تعداد تخت اتاق عمل را با چرخاندن دایال یا تایپ عدد تنظیم کنید',
     'Step 1: set operating-room beds by turning the dial or typing a number'),
    ('ترکیب‌های آماده (تخت اتاق عمل + ICU|CCU)', 'Presets (operating-room beds + ICU|CCU)'),
    ('>ثابت<', '>Held<'),
    ('تخت اتاق عمل', 'Operating-room beds'),
    ('تعداد تخت اتاق عمل (۰ تا ۷۰۰)', 'Operating-room beds (0 to 700)'),
    ('تخت ICU|CCU', 'ICU|CCU beds'),
    ('تعداد تخت ICU|CCU (۰ تا ۷۰۰)', 'ICU|CCU beds (0 to 700)'),
    ('برای محاسبه دقیق مرکز درمانی خود با ما صحبت کنید', 'Talk to us for a figure matched to your facility'),
    ('کارشناسان فروش مخازن طبی آبادیس آماده پاسخ‌گویی به پرسش‌های شما هستند.',
     'Abadis Medical Reservoirs sales specialists are ready to answer your questions.'),
    ('مرکز تماس:', 'Call centre:'),
    ('صفحه ارتباط با ما', 'Contact page'),
    ('href="../ارتباط-با-ما/"', 'href="../contact-us/"'),
    ('>۱٬۰۰۰<', '>1,000<'),
    ('>۵٬۰۰۰<', '>5,000<'),
    ('>۱۰٬۰۰۰<', '>10,000<'),
    ('>۱۵٬۰۰۰<', '>15,000<'),
    ('>۱۰ + ۱۰<', '>10 + 10<'),
    ('>۲۰ + ۱۰<', '>20 + 10<'),
    ('>۵۰ + ۲۰<', '>50 + 20<'),
    ('>۱۰۰ + ۵۰<', '>100 + 50<'),
    ('>۳۰۰ + ۱۰۰<', '>300 + 100<'),
    ('>۷۰۰ + ۷۰۰<', '>700 + 700<'),
 ],
 'ar': [
    ('ابزار محاسبه', 'الحاسبة'),
    ('محاسبه‌گر صرفه‌جویی <em>آبادیس</em>', 'حاسبة التوفير من <em>آباديس</em>'),
    ('دایال را با لمس یا ماوس بچرخانید یا عدد را تایپ کنید؛ سه نمایشگر، صرفه‌جویی آب، هزینه شست‌وشو و ضدعفونی و زمان کادر درمان را همزمان نشان می‌دهند.',
     'أدر القرص باللمس أو بالفأرة، أو اكتب رقماً. تعرض ثلاث شاشات توفير الماء وتكلفة الغسيل والتعقيم ووقت الكادر معاً.'),
    ('CH-1 · ورودی: تعداد عمل', 'CH-1 · المدخل: عدد العمليات'),
    ('بر مبنای تعداد عمل جراحی در سال', 'بحسب عدد العمليات الجراحية سنوياً'),
    ('دایال را با لمس یا ماوس بچرخانید یا عدد را تایپ کنید', 'أدر القرص باللمس أو بالفأرة، أو اكتب رقماً'),
    ('مقادیر آماده', 'قيم جاهزة'),
    ('آبادیس', 'آباديس'),
    ('تعداد عمل در سال (۰ تا ۱۵٬۰۰۰)', 'عدد العمليات سنوياً (٠ إلى ١٥٬٠٠٠)'),
    ('تعداد عمل در سال', 'عدد العمليات سنوياً'),
    ('صرفه‌جویی در مصرف آب', 'توفير الماء'),
    ('>لیتر<', '>لتر<'),
    ('هزینه شست‌وشو و ضدعفونی', 'تكلفة الغسيل والتعقيم'),
    ('>تومان<', '>تومان<'),
    ('زمان کادر درمان', 'وقت الكادر'),
    ('>ساعت<', '>ساعة<'),
    ('مشاوره با کارشناس فروش', 'التحدث مع أخصائي المبيعات'),
    ('CH-2 · ورودی: تعداد تخت', 'CH-2 · المدخل: عدد الأسرة'),
    ('بر مبنای تعداد تخت', 'بحسب عدد الأسرة'),
    ('مرحله ۱: تعداد تخت اتاق عمل را با چرخاندن دایال یا تایپ عدد تنظیم کنید',
     'الخطوة ١: اضبط عدد أسرة غرفة العمليات بتدوير القرص أو بكتابة الرقم'),
    ('ترکیب‌های آماده (تخت اتاق عمل + ICU|CCU)', 'تركيبات جاهزة (أسرة غرفة العمليات + ICU|CCU)'),
    ('>ثابت<', '>مثبَّت<'),
    ('تخت اتاق عمل', 'أسرة غرفة العمليات'),
    ('تعداد تخت اتاق عمل (۰ تا ۷۰۰)', 'عدد أسرة غرفة العمليات (٠ إلى ٧٠٠)'),
    ('تخت ICU|CCU', 'أسرة ICU|CCU'),
    ('تعداد تخت ICU|CCU (۰ تا ۷۰۰)', 'عدد أسرة ICU|CCU (٠ إلى ٧٠٠)'),
    ('برای محاسبه دقیق مرکز درمانی خود با ما صحبت کنید', 'تحدثوا معنا لحساب يناسب مركزكم العلاجي'),
    ('کارشناسان فروش مخازن طبی آبادیس آماده پاسخ‌گویی به پرسش‌های شما هستند.',
     'أخصائيو مبيعات خزانات آباديس الطبية جاهزون للإجابة عن أسئلتكم.'),
    ('مرکز تماس:', 'مركز الاتصال:'),
    ('صفحه ارتباط با ما', 'صفحة الاتصال'),
    ('href="../ارتباط-با-ما/"', 'href="../اتصل-بنا/"'),
    ('>۱٬۰۰۰<', '>١٬٠٠٠<'),
    ('>۵٬۰۰۰<', '>٥٬٠٠٠<'),
    ('>۱۰٬۰۰۰<', '>١٠٬٠٠٠<'),
    ('>۱۵٬۰۰۰<', '>١٥٬٠٠٠<'),
    ('>۱۰ + ۱۰<', '>١٠ + ١٠<'),
    ('>۲۰ + ۱۰<', '>٢٠ + ١٠<'),
    ('>۵۰ + ۲۰<', '>٥٠ + ٢٠<'),
    ('>۱۰۰ + ۵۰<', '>١٠٠ + ٥٠<'),
    ('>۳۰۰ + ۱۰۰<', '>٣٠٠ + ١٠٠<'),
    ('>۷۰۰ + ۷۰۰<', '>٧٠٠ + ٧٠٠<'),
 ],
}

def patch_calculator():
    for lang, rel, title, desc in (
        ('en', 'en/calculator/index.html', 'Savings calculator — Abadis Medical Reservoirs',
         'Estimate the water, washing and disinfection cost, and staff time a facility saves with Abadis disposable suction bags.'),
        ('ar', 'arabic/الحوسبة/index.html', 'حاسبة التوفير — خزانات طبي آباديس',
         'قدّروا توفير الماء وتكلفة الغسيل والتعقيم ووقت الكادر عند استخدام أكياس الشفط آباديس ذات الاستخدام الواحد.'),
    ):
        main = _dial_from_fa(lang)
        replace_main(SITE / rel, main)
        s = read(SITE / rel)
        s = re.sub(r'<script src="[^"]*calc-i18n\.js"[^>]*>\s*</script>\n?', '', s)
        if 'dial-practical.js' not in s:
            s = s.replace('</body>',
                          f'<script src="../../assets/dial/abadis-common.js?v={V}"></script>\n'
                          f'<script src="../../assets/dial/dial-practical.js?v={V}" defer></script>\n</body>')
        if 'dial.css' not in s:
            s = s.replace('</head>', f'<link rel="stylesheet" href="../../assets/dial/dial.css?v={V}">\n</head>')
        write(SITE / rel, s)
        set_meta(SITE / rel, title, desc)
    # cache-bust the FA page that already loads the scripts
    fa = read(SITE / 'محاسبه-گر/index.html')
    fa = fa.replace('src="../assets/dial/abadis-common.js"', f'src="../assets/dial/abadis-common.js?v={V}"')
    fa = fa.replace('src="../assets/dial/dial-practical.js"', f'src="../assets/dial/dial-practical.js?v={V}"')
    fa = fa.replace('href="../assets/dial/dial.css"', f'href="../assets/dial/dial.css?v={V}"')
    write(SITE / 'محاسبه-گر/index.html', fa)
    print('calculator ok')

if __name__ == '__main__':
    import sys
    step = sys.argv[1] if len(sys.argv) > 1 else 'base'
    if step in ('base', 'all'):
        patch_ar_footer()
        patch_dealers()
        patch_faq()
        patch_home_titles()
        patch_sustainability()
        patch_downloads()
        patch_calculator()
        print('base done')
