"""Products & solutions architecture (Alireza, Oct 2026).

Hub, home block, five solution pages (FA / EN / AR), nav stamp, and the
commercial-status badges on canonical product pages. Does not rebuild the
rest of the site and does not call the legacy phase-1 generator.
"""
import os
import re
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from lib import esc, SITE
from i18n import LANGS, NAV
from layout import page, page_hero, _href, _nav_item
import solutions_philosophy as PHIL

UPLOADS = pathlib.Path('/home/ubuntu/.cursor/projects/workspace/uploads')

def L(fa, en, ar):
    return {'fa': fa, 'en': en, 'ar': ar}

UI = {
    'fa': dict(
        h1='محصولات و راهکارهای آبادیس',
        sub='از محصولات تخصصی ساکشن تا راهکارهای نوآورانه برای مراقبت ایمن‌تر و کارآمدتر',
        crumb_p='محصولات', crumb_s='راهکارها',
        by_p='بر اساس محصول', by_s='بر اساس راهکار',
        keep='دسته‌بندی فعلی حفظ شود', new_path='مسیر جدید مشتری',
        note='یک محصول می‌تواند در چند راهکار حضور داشته باشد. برای مثال فیلتر در سیستم ساکشن و راهکار کنترل آلودگی کاربرد دارد، اما صفحه اصلی معرفی فیلتر فقط یک بار ساخته می‌شود.',
        uneven='این سه راهکار وضعیت یکسانی ندارند. مدیریت مایعات بر محصولات موجود متکی است؛ مراقبت راه هوایی متناسب با محصولات قابل عرضه فعال است و کنترل آلودگی و مدیریت پسماند در بخش «آینده» معرفی می‌شود.',
        view='مشاهده صفحه',
        order='قابل سفارش', soon='به‌زودی', rnd='در حال تحقیق و توسعه', future='آینده / در حال توسعه', active='فعال',
        legend='وضعیت تجاری',
        related='راهکارهای مرتبط',
        layers_h='ساختار این صفحه',
        layers=[
            ('محصولات', 'ما چه چیزی تولید و عرضه می‌کنیم؟'),
            ('راهکارها', 'این محصولات در کنار هم چه مسئله‌ای را حل می‌کنند؟'),
            ('کاربردها', 'این راهکارها در کدام بخش‌های بیمارستان استفاده می‌شوند؟'),
            ('نوآوری', 'آبادیس برای حل مسئله آینده روی چه فناوری‌هایی کار می‌کنند؟'),
        ],
        pva_title='محصولات PVA (مواد پلیمری زیست‌تخریب‌پذیر)',
        pva_text='فناوری مواد و محصولات آینده. هنوز صفحه محصول مستقل ندارد و فقط از همین مدخل به راهکار در حال توسعه وصل می‌شود.',
        pva_link='راهکار مدیریت پسماند و PVA',
        quote='استعلام قیمت',
        config='درخواست راهکار مناسب مرکز درمانی من',
        s_problem='۱. معرفی مسئله', s_intro='۲. معرفی راهکار', s_parts='۳. اجزای راهکار',
        s_apps='۴. کاربردها', s_adv='۵. مزیت‌ها', s_econ='۶. ارزش اقتصادی',
        s_pick='۷. انتخاب سیستم', s_sales='۸. تماس با فروش',
        dept='بخش بیمارستان', use='میزان مصرف تقریبی', beds='تعداد تخت',
        ops='تعداد عمل ماهانه', bags='مصرف تقریبی کیسه‌های ساکشن در ماه',
        system='نوع سیستم ساکشن', center='نام مرکز درمانی', person='نام درخواست‌کننده',
        phone='شماره تماس / واتساپ', send='ثبت و دیدن خلاصه',
        summary='خلاصه پیکربندی', reco='پیشنهاد تکمیلی از اجزای همین راهکار',
        wa='ارسال در واتساپ واحد فروش', mail='ارسال ایمیل به فروش',
        close='بستن',
        depts=['اتاق عمل (OR)', 'مراقبت‌های ویژه (ICU / CCU)', 'اورژانس (ER)', 'بخش‌های بستری و جنرال', 'کلینیک / مرکز جراحی محدود', 'کل بیمارستان (تجهیز جامع)'],
        systems=['ساکشن مرکزی دیواری', 'ساکشن پرتابل و ترولی', 'سیستم ترکیبی (دیواری + پرتابل)', 'نیاز به مشاوره کارشناسی'],
        sales_p='درخواست مشاوره، نمونه، کاتالوگ یا پیشنهاد فنی و تجاری. فرم زیر سفارش قطعی ثبت نمی‌کند؛ خلاصه را برای واحد فروش می‌فرستد.',
        cat='کاتالوگ جامع',
        subject='درخواست راهکار آبادیس',
        home='خانه',
        box='راهکار و محصول',
        all_p='مشاهده همه محصولات',
        all_s='مشاهده همه راهکارها',
        prev='قبلی',
        next='بعدی',
        rail_p='محصولات',
        rail_s='راهکارها',
    ),
    'en': dict(
        h1='Abadis Products & Solutions',
        sub='From specialised suction products to innovative solutions for safer, more efficient care.',
        crumb_p='Products', crumb_s='Solutions',
        by_p='By product', by_s='By solution',
        keep='Current categories stay', new_path='New customer path',
        note='One product can belong to more than one solution. A filter, for example, is used in the suction system and in contamination control, but its canonical product page is built only once.',
        uneven='These three solutions are not in the same state. Fluid management relies on products already on sale. Airway care is active for the products that can be supplied. Contamination control and waste management stay in the Future section.',
        view='View page',
        order='Orderable', soon='Coming soon', rnd='In research and development', future='Future / In development', active='Active',
        legend='Commercial status',
        related='Related solutions',
        layers_h='How this page is organised',
        layers=[
            ('Products', 'What do we manufacture and supply?'),
            ('Solutions', 'Which problem do these products solve together?'),
            ('Applications', 'Which hospital departments use these solutions?'),
            ('Innovation', 'Which technologies is Abadis working on to solve the problem of the future?'),
        ],
        pva_title='PVA products (biodegradable polymer materials)',
        pva_text='Materials technology and future products. There is no separate product page yet; this entry only links to the in-development solution.',
        pva_link='Waste management and PVA solution',
        quote='Request a price',
        config='Request the right solution for my centre',
        s_problem='1. The problem', s_intro='2. The solution', s_parts='3. Components',
        s_apps='4. Applications', s_adv='5. Advantages', s_econ='6. Economic value',
        s_pick='7. System selection', s_sales='8. Contact sales',
        dept='Hospital department', use='Approximate use', beds='Number of beds',
        ops='Operations per month', bags='Approximate suction bags per month',
        system='Suction system type', center='Facility name', person='Requester name',
        phone='Phone / WhatsApp', send='Save and show the summary',
        summary='Configuration summary', reco='Complementary products from this solution',
        wa='Send on WhatsApp to sales', mail='Email sales',
        close='Close',
        depts=['Operating room (OR)', 'Intensive care (ICU / CCU)', 'Emergency (ER)', 'Inpatient and general wards', 'Clinic / limited surgery centre', 'Whole hospital'],
        systems=['Central wall suction', 'Portable suction and trolley', 'Combined (wall + portable)', 'Need technical advice'],
        sales_p='Ask for advice, a sample, the catalogue, or a technical and commercial proposal. This form does not place an order; it sends the summary to sales.',
        cat='Full catalogue',
        subject='Abadis solution request',
        home='Home',
        box='Solutions & Products',
        all_p='View all products',
        all_s='View all solutions',
        prev='Previous',
        next='Next',
        rail_p='Products',
        rail_s='Solutions',
    ),
    'ar': dict(
        h1='منتجات وحلول آباديس',
        sub='من منتجات الشفط المتخصصة إلى حلول مبتكرة لرعاية أكثر أماناً وكفاءة.',
        crumb_p='المنتجات', crumb_s='الحلول',
        by_p='حسب المنتج', by_s='حسب الحل',
        keep='يُحفظ التصنيف الحالي', new_path='مسار جديد للعميل',
        note='يمكن أن يظهر منتج واحد في أكثر من حل. الفلتر مثلاً يُستخدم في نظام الشفط وفي السيطرة على التلوث، لكن صفحة تعريفه الأساسية تُبنى مرة واحدة.',
        uneven='هذه الحلول الثلاثة ليست في الوضع نفسه. إدارة السوائل تعتمد على منتجات قائمة. العناية بالطريق الهوائي تُفعَّل بقدر المنتجات القابلة للعرض، والسيطرة على التلوث وإدارة النفايات تبقى في قسم «المستقبل».',
        view='عرض الصفحة',
        order='قابل للطلب', soon='قريباً', rnd='قيد البحث والتطوير', future='مستقبل / قيد التطوير', active='نشط',
        legend='الحالة التجارية',
        related='الحلول المرتبطة',
        layers_h='بنية هذه الصفحة',
        layers=[
            ('المنتجات', 'ماذا ننتج ونعرض؟'),
            ('الحلول', 'أي مسألة تحلّها هذه المنتجات معاً؟'),
            ('الاستخدامات', 'في أي أقسام المستشفى تُستخدم هذه الحلول؟'),
            ('الابتكار', 'على أي تقنيات تعمل آباديس لحل مسألة المستقبل؟'),
        ],
        pva_title='منتجات PVA (مواد بوليمرية قابلة للتحلل)',
        pva_text='تقنية المواد والمنتجات المستقبلية. لا توجد بعد صفحة منتج مستقلة؛ هذا المدخل يصل فقط إلى الحل قيد التطوير.',
        pva_link='حل إدارة النفايات وPVA',
        quote='استعلام السعر',
        config='طلب الحل المناسب لمركزي العلاجي',
        s_problem='١. تعريف المسألة', s_intro='٢. تعريف الحل', s_parts='٣. مكوّنات الحل',
        s_apps='٤. الاستخدامات', s_adv='٥. المزايا', s_econ='٦. القيمة الاقتصادية',
        s_pick='٧. اختيار النظام', s_sales='٨. الاتصال بالمبيعات',
        dept='قسم المستشفى', use='الاستهلاك التقريبي', beds='عدد الأسرّة',
        ops='عدد العمليات شهرياً', bags='الاستهلاك التقريبي لأكياس الشفط شهرياً',
        system='نوع نظام الشفط', center='اسم المركز العلاجي', person='اسم مقدّم الطلب',
        phone='الهاتف / واتساب', send='تسجيل وعرض الملخص',
        summary='ملخص التهيئة', reco='منتجات مكمّلة من مكوّنات هذا الحل',
        wa='إرسال عبر واتساب المبيعات', mail='إرسال بريد إلى المبيعات',
        close='إغلاق',
        depts=['غرفة العمليات (OR)', 'العناية المركزة (ICU / CCU)', 'الطوارئ (ER)', 'أقسام الإقامة والعامة', 'عيادة / مركز جراحة محدودة', 'المستشفى كاملاً'],
        systems=['شفط مركزي جداري', 'شفط محمول وترولي', 'نظام مشترك (جداري + محمول)', 'حاجة إلى استشارة فنية'],
        sales_p='طلب استشارة أو عيّنة أو كتالوج أو عرض فني وتجاري. هذا النموذج لا يثبّت طلباً؛ يرسل الملخص إلى المبيعات.',
        cat='الكتالوج الشامل',
        subject='طلب حل آباديس',
        home='الرئيسية',
        box='الحلول والمنتجات',
        all_p='عرض جميع المنتجات',
        all_s='عرض جميع الحلول',
        prev='السابق',
        next='التالي',
        rail_p='المنتجات',
        rail_s='الحلول',
    ),
}

CATALOG = [
    dict(slug='suction-bag', photo='suction-bag',
         href=L('products/suction-bag/', 'products/suction-bag/', 'كيس-الشفط/'),
         title=L('کیسه ساکشن یکبار مصرف', 'Disposable Suction Bag', 'أكياس الشفط ذات الاستخدام الواحد'),
         sub=L('مدل‌های ۱، ۲ و ۳ لیتری', '1, 2 and 3 litre models', 'موديلات ١ و٢ و٣ لتر')),
    dict(slug='canister', photo='canister',
         href=L('products/canister/', 'products/canisters/', 'خزانات/'),
         title=L('مخزن ساکشن', 'Suction Canister', 'علبة الشفط'),
         sub=L('مخازن و سیستم‌های دیواری', 'Canisters and wall systems', 'الخزانات والأنظمة الجدارية')),
    dict(slug='stand', photo='stand',
         href=L('products/stand/', 'products/base-and-holder/', 'تثبیت/'),
         title=L('پایه و نگهدارنده‌ها', 'Stands & Holders', 'الحوامل والمثبتات'),
         sub=L('ترولی، پایه و گیره‌ها', 'Trolley, stand and clamps', 'ترولي وقاعدة ومشابك')),
    dict(slug='connectors', photo='connectors',
         href=L('products/connectors/', 'products/connections/', 'الوصلات/'),
         title=L('اتصالات', 'Connectors', 'الوصلات'),
         sub=L('کانکتورها و شیرها', 'Connectors and valves', 'الوصلات والصمامات')),
    dict(slug='filters', photo='filters',
         href=L('products/filters/', 'products/filters/', 'الفلتر/'),
         title=L('فیلتر', 'Filter', 'الفلاتر'),
         sub=L('انواع فیلترهای حفاظتی', 'Protective filter types', 'أنواع الفلاتر الواقية')),
    dict(slug='suction-tube', photo='suction-tube',
         href=L('products/suction-tube/', 'suction-tube/', 'أنبوب-الشفط/'),
         title=L('ساکشن تیوب', 'Suction Tube', 'أنبوب الشفط'),
         sub=L('لوله‌ها و رابط‌های ساکشن', 'Tubes and suction connectors', 'الأنابيب ووصلات الشفط')),
    dict(slug='oral', photo='oral',
         href=L('products/oral-hygiene/', 'products/oral-hygiene/', 'نظافة-الفم/'),
         title=L('بهداشت دهان', 'Oral Hygiene', 'نظافة الفم'),
         sub=L('مسواک ساکشن، سواب دهانی، فیکسر لوله تراشه', 'Suction toothbrush, oral swab, tube fixer', 'فرشاة الشفط والمسحة ومثبّت الأنبوب')),
    dict(slug='other', photo='other',
         href=L('products/other/', 'products/other-products/', 'منتجات-اخری/'),
         title=L('سایر محصولات', 'Other Products', 'منتجات أخرى'),
         sub=L('رگولاتور، کیسه زباله PVA، رسیور یکبار مصرف', 'Regulator, PVA waste bag, disposable receiver', 'المنظّم وكيس نفايات PVA ووعاء التجميع')),
]
BY_SLUG = {c['slug']: c for c in CATALOG}

PHOTO = {
    'suction-bag': 'assets/img/c/611f0398754f-640.webp',
    'stand': 'assets/img/c/90d179b67447-1600.webp',
    'filters': 'assets/img/c/ad713458f652-640.webp',
    'suction-tube': 'assets/img/c/92b676038309-1600.webp',
    'canister': 'assets/img/c/38a87bcfaf85-1600.webp',
    'connectors': 'assets/img/c/9b6630cc8eaa-640.webp',
    'other': 'assets/img/c/a75210c08710-1600.webp',
    'oral': 'assets/img/c/a75210c08710-1600.webp',
    'mesvak': 'assets/img/c/a75210c08710-1600.webp',
    'negahdarande': 'assets/img/c/d3d867132a50-1600.webp',
    'receiver': 'assets/img/c/928b52ffc716-1600.webp',
    'sdv': 'assets/img/c/d981ab7fae6e-1600.webp',
    'paye': 'assets/img/c/227665fb9960-1600.webp',
    'anti': 'assets/img/filters/anti-1-t.webp',
    'rgl': 'assets/img/c/9b6630cc8eaa-640.webp',
}

# slug, hash, status, optional title override, optional photo key
def P(slug, hash='', status='order', title=None, photo=None):
    return dict(slug=slug, hash=hash, status=status, title=title, photo=photo)

SOLS = [
    dict(
        slug='fluid-management', future=False,
        title=L('مدیریت مایعات و ترشحات بیمارستانی', 'Hospital Fluid & Secretion Management', 'إدارة السوائل والإفرازات في المستشفى'),
        sub=L('از جمع‌آوری مایعات تا مدیریت یکپارچه سیستم ساکشن', 'From fluid collection to an integrated suction system', 'من جمع السوائل إلى إدارة متكاملة لنظام الشفط'),
        parts=[
            P('suction-bag'), P('canister'), P('connectors'), P('stand'), P('suction-tube'),
            P('filters', 'ght', 'order', L('فیلتر قطع‌کننده جریان', 'Flow-stopper filter', 'فلتر قطع التدفق'), 'filters'),
            P('other', 'rgl', 'order', L('رگولاتور', 'Regulator', 'المنظّم'), 'rgl'),
        ],
    ),
    dict(
        slug='airway-care', future=False,
        title=L('ایمنی و مراقبت از راه هوایی', 'Airway Safety & Care', 'سلامة الطريق الهوائي والعناية به'),
        sub=L('توسعه راهکارهای تخصصی برای مراقبت ایمن‌تر از بیماران', 'Developing specialist solutions for safer patient care', 'تطوير حلول تخصصية لرعاية أكثر أماناً للمرضى'),
        parts=[
            P('oral', 'mesvak', 'order', L('مسواک ساکشن', 'Suction toothbrush', 'فرشاة الشفط'), 'mesvak'),
            P('oral', 'swab', 'rnd', L('سواب دهانی', 'Oral swab', 'المسحة الفموية'), 'mesvak'),
            P('oral', 'negahdarande', 'order', L('فیکسر لوله تراشه', 'Endotracheal-tube fixer', 'مثبّت أنبوب القصبة'), 'negahdarande'),
        ],
    ),
    dict(
        slug='waste-management-pva', future=True,
        title=L('کنترل آلودگی و مدیریت پسماند', 'Contamination Control & Waste Management', 'السيطرة على التلوث وإدارة النفايات'),
        sub=L('فناوری مواد؛ افقی جدید در توسعه راهکارهای پایدار', 'Materials technology, a new horizon for sustainable solutions', 'تقنية المواد؛ أفق جديد لحلول مستدامة'),
        parts=[
            P('other', 'pva', 'rnd', L('کیسه زباله PVA', 'PVA waste bag', 'كيس نفايات PVA'), None),
            P('other', 'receiver', 'order', L('رسیور یکبار مصرف', 'Disposable receiver', 'وعاء تجميع ذو استعمال واحد'), 'receiver'),
        ],
    ),
]
BY_SOL = {s['slug']: s for s in SOLS}

RELATED = {
    'suction-bag': ['fluid-management'],
    'canister': ['fluid-management'],
    'stand': ['fluid-management'],
    'connectors': ['fluid-management'],
    'filters': ['fluid-management'],
    'suction-tube': ['fluid-management'],
    'oral': ['airway-care'],
    'other': ['fluid-management', 'waste-management-pva'],
}

CATALOGUE = 'https://abadis-med.com/wp-content/uploads/2024/12/کاتالوگ-جامع-آبادیس.pdf'
CONTACT = L('contact/', 'contact-us/', 'اتصل-بنا/')


def status_for(tab_id):
    if tab_id == 'splashvac':
        return 'soon'
    if tab_id in ('swab', 'pva'):
        return 'rnd'
    return 'order'


def badge(lang, status):
    # «قابل سفارش» / Coming soon were rollout stamps. Future and R&D stay on PVA.
    if status in ('order', 'soon'):
        return ''
    ui = UI[lang]
    label = {'rnd': ui['rnd'], 'future': ui['future']}[status]
    return f'<span class="ps-badge ps-badge--{status}">{esc(label)}</span>'


def strip_rollout_badges(html):
    html = re.sub(
        r'\s*<p class="ps-hero-badge">(?:(?!</p>).)*ps-badge--(?:order|soon)(?:(?!</p>).)*</p>',
        '', html, flags=re.S)
    html = re.sub(r'<span class="ps-badge ps-badge--(?:order|soon)">.*?</span>', '', html, flags=re.S)
    return html


def tab_anchor(tab_id, title, lang):
    return (f'<a href="#{esc(tab_id)}" data-ptab="{esc(tab_id)}">{esc(title)}'
            f'{badge(lang, status_for(tab_id))}</a>')


def icons(p, kind):
    # Alireza finalists: M5 for «بر اساس محصول», R9 for «بر اساس راهکار».
    light, dark = ('M5-teal.svg', 'M5-dark.svg') if kind == 'product' else ('R9-3-teal.svg', 'R9-3-dark.svg')
    base = f'{p}assets/img/icons/'
    return (f'<span class="path-ico" aria-hidden="true">'
            f'<img class="path-ico-light" src="{base}{light}" alt="" width="48" height="48">'
            f'<img class="path-ico-dark" src="{base}{dark}" alt="" width="48" height="48"></span>')


def root_of(lang):
    return LANGS[lang]['root']


def href(p, lang, h):
    return _href(p, root_of(lang), h)


def prod_href(p, lang, slug, hash_id=''):
    h = BY_SLUG[slug]['href'][lang]
    if hash_id:
        h += '#' + hash_id
    return href(p, lang, h)


def sol_href(p, lang, slug):
    folder = 'solutions/' if lang != 'ar' else 'الحلول/'
    return href(p, lang, f'{folder}{slug}/')


def inject_h1_badge(html, lang, status='order'):
    if 'ps-hero-badge' in html:
        return html
    mark = f'<p class="ps-hero-badge">{badge(lang, status)}</p>'
    return re.sub(r'(<h1\b[^>]*>.*?</h1>)', lambda m: m.group(1) + mark, html, count=1, flags=re.S)


def pva_card(p, lang):
    ui = UI[lang]
    return (f'<article class="ps-pva" id="pva">{badge(lang, "rnd")}'
            f'<h3>{esc(ui["pva_title"])}</h3><p>{esc(ui["pva_text"])}</p>'
            f'<p><a href="{sol_href(p, lang, "waste-management-pva")}">{esc(ui["pva_link"])}</a></p></article>')


def related_section(p, lang, slug):
    ui = UI[lang]
    pills = ''.join(
        f'<a href="{sol_href(p, lang, s)}">{esc(BY_SOL[s]["title"][lang])}'
        f'{badge(lang, "future") if BY_SOL[s]["future"] else ""}</a>'
        for s in RELATED[slug])
    return (f'<section class="section ps-related" id="related-solutions"><div class="wrap">'
            f'<h2>{esc(ui["related"])}</h2><div class="ps-pills">{pills}</div></div></section>\n')


def _ul(items):
    return '<ul>' + ''.join(f'<li>{esc(x)}</li>' for x in items) + '</ul>'


def _part(p, lang, part):
    ui = UI[lang]
    title = part['title'][lang] if part['title'] else BY_SLUG[part['slug']]['title'][lang]
    photo_key = part['photo'] if part['photo'] is not None else (part['hash'] or part['slug'])
    src = PHOTO.get(photo_key)
    img = (f'<img src="{p}{src}" alt="" width="96" height="72" loading="lazy">' if src else icons(p, 'product'))
    if part['hash'] == 'pva':
        url = prod_href(p, lang, 'other', 'pva')
    else:
        url = prod_href(p, lang, part['slug'], part['hash'])
    return (f'<a class="ps-part" href="{url}">{img}<span>{badge(lang, part["status"])}'
            f'<strong>{esc(title)}</strong></span></a>')


def configurator(lang):
    ui = UI[lang]
    depts = ''.join(f'<option>{esc(x)}</option>' for x in ui['depts'])
    systems = ''.join(f'<option>{esc(x)}</option>' for x in ui['systems'])
    return f'''<dialog class="ps-dialog" id="sol-config">
  <form data-sol-form data-subject="{esc(ui["subject"])}" data-reco-label="{esc(ui["reco"])}" method="dialog">
    <h2>{esc(ui["config"])}</h2>
    <div class="ps-fields">
      <label>{esc(ui["dept"])}<select name="dept" data-sum="{esc(ui["dept"])}" required><option value=""></option>{depts}</select></label>
      <p style="margin:0;font-weight:800">{esc(ui["use"])}</p>
      <label>{esc(ui["beds"])}<input name="beds" data-sum="{esc(ui["beds"])}" inputmode="numeric"></label>
      <label>{esc(ui["ops"])}<input name="ops" data-sum="{esc(ui["ops"])}" inputmode="numeric"></label>
      <label>{esc(ui["bags"])}<input name="bags" data-sum="{esc(ui["bags"])}" inputmode="numeric"></label>
      <label>{esc(ui["system"])}<select name="system" data-sum="{esc(ui["system"])}" required><option value=""></option>{systems}</select></label>
      <label>{esc(ui["center"])}<input name="center" data-sum="{esc(ui["center"])}" required></label>
      <label>{esc(ui["person"])}<input name="person" data-sum="{esc(ui["person"])}" required></label>
      <label>{esc(ui["phone"])}<input name="phone" data-sum="{esc(ui["phone"])}" required dir="ltr"></label>
    </div>
    <div class="ps-actions">
      <button class="btn btn-primary" type="submit">{esc(ui["send"])}</button>
      <button class="btn btn-ghost" type="button" onclick="this.closest('dialog').close()">{esc(ui["close"])}</button>
    </div>
  </form>
  <div class="ps-summary" id="sol-summary" hidden>
    <h3>{esc(ui["summary"])}</h3>
    <pre style="white-space:pre-wrap;font:inherit"></pre>
    <div class="ps-actions">
      <a class="btn btn-primary" id="sol-wa" href="https://wa.me/989100145809" target="_blank" rel="noopener">{esc(ui["wa"])}</a>
      <a class="btn btn-ghost" id="sol-mail" href="mailto:info@abadis-med.com">{esc(ui["mail"])}</a>
    </div>
  </div>
</dialog>'''



# ------------------------------------------------------------------ Finalized Visual Solutions Design ([t279u], [t281u])
SOL_SLOGAN_I18N = {
    'fa': [
        'راهکارهای تخصصی آبادیس،',
        'برای مراقبت ایمن‌تر',
        'بهره‌وری بالاتر مراکز درمانی',
        'و حفاظت پایدار از محیط زیست.',
    ],
    'en': [
        'Abadis specialised clinical solutions,',
        'For safer patient care',
        'Higher hospital efficiency',
        'And sustainable environmental protection.',
    ],
    'ar': [
        'حلول آباديس التخصصية،',
        'لرعاية أكثر أماناً',
        'وكفاءة أعلى للمراكز العلاجية',
        'وحماية مستدامة للبيئة.',
    ],
}

SOL_SUBPAGE_SLOGANS = {
    'fluid-management': {
        'fa': [
            'مدیریت یکپارچه مایعات و ترشحات بیمارستانی،',
            'کاهش تماس کادر درمان با ترشحات آلوده',
            'حذف شست‌وشوی مخازن و صرفه‌جویی در مصرف آب',
            'افزایش چابکی اتاق عمل، ICU و اورژانس.',
        ],
        'en': [
            'Integrated Hospital Fluid & Secretion Management,',
            'Reducing staff exposure to contaminated fluids',
            'Eliminating canister washing & saving water',
            'Boosting agility in the OR, ICU, and Emergency.',
        ],
        'ar': [
            'إدارة متكاملة للسوائل والإفرازات في المستشفى،',
            'تقليل تلامس الكادر مع السوائل الملوثة',
            'إلغاء غسل الخزانات وتوفير استهلاك الماء',
            'رفع كفاءة غرفة العمليات والعناية المركزة.',
        ],
    },
    'airway-care': {
        'fa': [
            'ایمنی و مراقبت تخصصی از راه هوایی،',
            'تسهیل بهداشت دهان در بیماران اینتوبه و ICU',
            'تثبیت ایمن لوله تراشه و کاهش ریسک عفونت',
            'طراحی کاربردی متناسب با نیاز پزشکان و پرستاران.',
        ],
        'en': [
            'Specialised Airway Safety & Care,',
            'Streamlining oral hygiene for intubated ICU patients',
            'Secure endotracheal tube fixation & infection control',
            'Practical clinical design for nurses and physicians.',
        ],
        'ar': [
            'سلامة الطريق الهوائي والعناية التخصصية به،',
            'تيسير نظافة الفم لمرضى العناية المركزة',
            'تثبيت آمن لأنبوب القصبة وتقليل مخاطر العدوى',
            'تصميم سريري عملي يلبي حاجات الأطباء والتمريض.',
        ],
    },
    'waste-management-pva': {
        'fa': [
            'کنترل آلودگی و مدیریت هوشمند پسماند بیمارستانی،',
            'تحقیق و توسعه در فیلم‌ها و کیسه‌های محلول در آب PVA',
            'کاهش شست‌وشوی ظروف چندبارمصرف با رسیور یکبارمصرف',
            'گامی نوآورانه برای سلامت انسان و آینده پایدار زمین.',
        ],
        'en': [
            'Contamination Control & Smart Hospital Waste Management,',
            'R&D in water-soluble PVA polymer films and bags',
            'Cutting container washing with disposable receivers',
            'An innovative horizon for human health and sustainability.',
        ],
        'ar': [
            'السيطرة على التلوث وإدارة نفايات المستشفى،',
            'البحث والتطوير في أفلام وأكياس PVA الذؤابة في الماء',
            'تقليل غسل الأوعية عبر أوعية التجميع أحادية الاستعمال',
            'أفق مبتكر لصحة الإنسان ومستقبل الأرض المستدام.',
        ],
    },
}

SOL_HERO_LEAD = {
    'fa': 'از مدیریت مایعات و ترشحات بیمارستانی تا ایمنی راه هوایی و فناوری‌های نوین کنترل آلودگی؛ راهکارهایی یکپارچه بر پایه دانش مهندسی و نیازهای واقعی بالینی.',
    'en': 'From hospital fluid and secretion management to airway safety and advanced contamination-control materials — integrated solutions built on engineering knowledge and real clinical needs.',
    'ar': 'من إدارة السوائل والإفرازات في المستشفى إلى سلامة الطريق الهوائي وتقنيات السيطرة على التلوث؛ حلول متكاملة قائمة على المعرفة الهندسية والحاجات السريرية الحقيقية.',
}

SOL_HERO_H1 = {
    'fa': 'راهکارهای تخصصی <em>آبادیس</em>',
    'en': 'Abadis Specialised <em>Solutions</em>',
    'ar': 'حلول <em>آباديس</em> التخصصية',
}

_SVG_DROPLET = '<svg viewBox="0 0 28 28" width="26" height="26" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 3.5C14 3.5 6 12.2 6 17.5a8 8 0 0 0 16 0C22 12.2 14 3.5 14 3.5z"/><path d="M10.5 18.5a3.5 3.5 0 0 0 3.5 3"/></svg>'
_SVG_LUNGS = '<svg viewBox="0 0 28 28" width="26" height="26" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 4v9"/><path d="M14 10c-2.5 0-4.5-2-6.5-2C4.5 8 3 11 3 15.5 3 20 5 23 8.5 23c2.5 0 3.5-1.8 3.5-4.5V11"/><path d="M14 10c2.5 0 4.5-2 6.5-2 3 0 4.5 3 4.5 7.5 0 4.5-2 7.5-5.5 7.5-2.5 0-3.5-1.8-3.5-4.5V11"/></svg>'
_SVG_LEAF = '<svg viewBox="0 0 28 28" width="26" height="26" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 5C12.5 5 6 10.5 6 19c0 1.5.3 2.8.8 4 1.2.5 2.5.8 4 .8 8.5 0 14-6.5 14-15 0-1.5-.3-2.8-.8-3.8z"/><path d="M6.8 22.2C10.5 17.5 15 14 21 11"/></svg>'
_SVG_ARROW = '<svg viewBox="0 0 20 20" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 10H5"/><path d="M9.5 5.5 5 10l4.5 4.5"/></svg>'
_SVG_WARN = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>'
_SVG_GEAR = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 1 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 1 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 1 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9c.26.6.77 1.02 1.51 1H21a2 2 0 1 1 0-4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>'
_SVG_CLOCK = '<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9.5"/><polyline points="12 7 12 12 15.5 14"/></svg>'
_SVG_CALC = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="2" width="16" height="20" rx="2"/><line x1="8" y1="6" x2="16" y2="6"/><line x1="8" y1="11" x2="10" y2="11"/><line x1="14" y1="11" x2="16" y2="11"/><line x1="8" y1="15" x2="10" y2="15"/><line x1="14" y1="15" x2="16" y2="15"/></svg>'
_SVG_CHAT = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg>'
_SVG_COMPASS = '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/></svg>'
_SVG_CUBE = '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg>'
_SVG_SHIELD = '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/></svg>'

SOL_WAVE_SVG = (
    '<svg class="sol-hcard-wave" viewBox="0 0 320 90" preserveAspectRatio="none" aria-hidden="true">'
    '<path d="M0 55 C80 20, 160 85, 320 30 L320 90 L0 90 Z" fill="#0d9488"/>'
    '<path d="M0 70 C110 40, 210 88, 320 52 L320 90 L0 90 Z" fill="#05686b" opacity="0.6"/>'
    '</svg>'
)


def _sol_slogan_html(lines):
    spans = ''.join(f'<span class="slogan-line" style="--i:{n}">{esc(x)}</span>' for n, x in enumerate(lines))
    return f'<p class="slogan reveal" aria-label="{esc(" ".join(lines))}">{spans}</p>'


def _hero_trio_html(p, lang, active_slug='fluid-management'):
    nums = {'fa': ('۰۱', '۰۲', '۰۳'), 'en': ('01', '02', '03'), 'ar': ('٠١', '٠٢', '٠٣')}[lang]
    discover = {'fa': 'کشف راهکار', 'en': 'Discover solution', 'ar': 'اكتشاف الحل'}[lang]
    act_lbl = {'fa': 'فعال', 'en': 'Active', 'ar': 'نشط'}[lang]
    fut_lbl = {'fa': 'مسیر توسعه', 'en': 'Development path', 'ar': 'مسار التطوير'}[lang]
    icos = (_SVG_DROPLET, _SVG_LUNGS, _SVG_LEAF)
    cards = []
    for i, s in enumerate(SOLS):
        slug = s['slug']
        url = sol_href(p, lang, slug)
        is_fut = s['future']
        b_cls = 'sol-hcard-badge sol-hcard-badge--future' if is_fut else 'sol-hcard-badge'
        b_txt = fut_lbl if is_fut else act_lbl
        act_cls = ' is-active' if slug == active_slug else ''
        cards.append(
            f'<article class="sol-hcard{act_cls}" data-sol-pick="{esc(slug)}" tabindex="0">'
            f'{SOL_WAVE_SVG}'
            f'<div>'
            f'<div class="sol-hcard-top"><span class="sol-hcard-num">{nums[i]}</span><span class="{b_cls}">{esc(b_txt)}</span></div>'
            f'<div style="display:flex;align-items:center;gap:12px;margin:12px 0 8px">'
            f'<span class="sol-hcard-ico">{icos[i]}</span>'
            f'<h3>{esc(s["title"][lang])}</h3>'
            f'</div>'
            f'<p>{esc(s["sub"][lang])}</p>'
            f'</div>'
            f'<div class="sol-hcard-foot">'
            f'<a class="sol-hcard-cta" href="{url}"><span>{esc(discover)}</span>{_SVG_ARROW}</a>'
            f'</div>'
            f'</article>'
        )
    return f'<div class="sol-hero-trio">{"".join(cards)}</div>'


def _comp_card(p, lang, part):
    title = part['title'][lang] if part['title'] else BY_SLUG[part['slug']]['title'][lang]
    photo_key = part['photo'] if part['photo'] is not None else (part['hash'] or part['slug'])
    src = PHOTO.get(photo_key) or 'assets/img/c/611f0398754f-640.webp'
    url = prod_href(p, lang, 'other', 'pva') if part['hash'] == 'pva' else prod_href(p, lang, part['slug'], part['hash'])
    b = badge(lang, part['status'])
    return (
        f'<a class="sol-comp-card" href="{url}">'
        f'<div class="sol-comp-ph"><img src="{p}{src}" alt="{esc(title)}" width="120" height="94" loading="lazy"></div>'
        f'<strong>{esc(title)}</strong>{b}'
        f'</a>'
    )


def _measurable_value_html(p, lang):
    copy = {
        'fa': dict(
            h='ارزش قابل اندازه‌گیری',
            p='کاهش چشمگیر مصرف آب، مواد ضدعفونی‌کننده و زمان آماده‌سازی اتاق عمل و ICU؛ قابل برآورد دقیق با محاسبه‌گر آبادیس بر اساس تعداد تخت و الگوی مصرف هر مرکز درمانی.',
            calc='محاسبه صرفه‌جویی',
            consult='دریافت مشاوره',
            p1=('مسیر انتخاب روشن', 'از نیاز تا راهکار مناسب'),
            p2=('محصولات مرتبط', 'یکپارچه و مکمل'),
            p3=('سه راهکار اصلی', 'پاسخ به نیازهای درمانی مراکز درمانی'),
        ),
        'en': dict(
            h='Measurable Clinical & Economic Value',
            p='Significant reductions in water consumption, chemical disinfectants, and OR/ICU turnaround time — accurately estimated for your facility with the Abadis calculator.',
            calc='Calculate Savings',
            consult='Request Consultation',
            p1=('Clear Selection Path', 'From clinical need to the right solution'),
            p2=('Integrated Products', 'Coordinated and complementary'),
            p3=('Three Core Solutions', 'Answering real hospital care needs'),
        ),
        'ar': dict(
            h='قيمة قابلة للقياس',
            p='خفض ملموس في استهلاك الماء ومواد التعقيم وزمن تجهيز غرف العمليات والعناية المركزة؛ قابل للتقدير بدقة عبر حاسبة آباديس.',
            calc='حساب التوفير',
            consult='طلب استشارة',
            p1=('مسار اختيار واضح', 'من الحاجة إلى الحل المناسب'),
            p2=('منتجات مترابطة', 'متكاملة ومكمّلة'),
            p3=('ثلاثة حلول رئيسية', 'استجابة لحاجات المراكز العلاجية'),
        ),
    }[lang]
    calc_url = href(p, lang, {'fa': 'calculator/', 'en': 'calculator/', 'ar': 'الحوسبة/'}[lang])
    cont_url = href(p, lang, CONTACT[lang])
    return (
        f'<div class="sol-value-banner reveal">'
        f'<div class="sol-value-copy">'
        f'<div class="sol-value-head"><span class="sol-value-ico">{_SVG_CLOCK}</span><h3>{esc(copy["h"])}</h3></div>'
        f'<p>{esc(copy["p"])}</p>'
        f'</div>'
        f'<div class="sol-value-actions">'
        f'<a class="sol-btn-calc" href="{calc_url}">{_SVG_CALC}<span>{esc(copy["calc"])}</span></a>'
        f'<a class="sol-btn-consult" href="{cont_url}">{_SVG_CHAT}<span>{esc(copy["consult"])}</span></a>'
        f'</div>'
        f'</div>'
        f'<div class="sol-bottom-pillars reveal">'
        f'<div class="sol-bpillar"><span class="sol-bpillar-ico">{_SVG_COMPASS}</span><div><strong>{esc(copy["p1"][0])}</strong><span>{esc(copy["p1"][1])}</span></div></div>'
        f'<div class="sol-bpillar"><span class="sol-bpillar-ico">{_SVG_CUBE}</span><div><strong>{esc(copy["p2"][0])}</strong><span>{esc(copy["p2"][1])}</span></div></div>'
        f'<div class="sol-bpillar"><span class="sol-bpillar-ico">{_SVG_SHIELD}</span><div><strong>{esc(copy["p3"][0])}</strong><span>{esc(copy["p3"][1])}</span></div></div>'
        f'</div>'
    )


def _showcase_panel_html(p, lang, sol, is_first=True):
    slug = sol['slug']
    theme = PHIL.BY_SLUG[slug]
    url = sol_href(p, lang, slug)
    view_lbl = {'fa': 'صفحه تخصصی این راهکار', 'en': 'Full Solution Page', 'ar': 'صفحة الحل الكاملة'}[lang]
    parts_lbl = {'fa': 'اجزای این راهکار', 'en': 'Components of This Solution', 'ar': 'مكوّنات هذا الحل'}[lang]
    all_dim_lbl = {'fa': 'همه ابعاد راهکار', 'en': 'All Dimensions', 'ar': 'جميع الأبعاد'}[lang]

    dim_tabs = [f'<button type="button" class="sol-dim-tab is-on" data-dim-btn="all">{esc(all_dim_lbl)}</button>']
    notes_cards = []
    for idx, (ntitle, nbody) in enumerate(theme['notes']):
        dkey = f'd{idx}'
        dim_tabs.append(f'<button type="button" class="sol-dim-tab" data-dim-btn="{dkey}">{esc(ntitle[lang])}</button>')
        ico = _SVG_WARN if idx == 0 else _SVG_GEAR
        notes_cards.append(
            f'<article class="sol-note-card" data-dim-card="{dkey}">'
            f'<div class="sol-note-head">{ico}<span>{esc(ntitle[lang])}</span></div>'
            f'<p>{esc(nbody[lang])}</p>'
            f'</article>'
        )

    axes_cards = ''.join(
        f'<div class="sol-axis-card"><strong>{esc(at[lang])}</strong><p>{esc(ab[lang])}</p></div>'
        for at, ab in theme['axes']
    )
    body_paras = ''.join(f'<p style="margin:0 0 10px;line-height:1.85;text-align:justify">{esc(x[lang])}</p>' for x in theme['body'])
    after_paras = ''.join(f'<p style="margin:10px 0 0;line-height:1.85;font-weight:700">{esc(x[lang])}</p>' for x in theme['after'])

    first_photo_key = sol['parts'][0]['photo'] or sol['parts'][0]['slug']
    main_img = PHOTO.get(first_photo_key) or 'assets/img/c/38a87bcfaf85-1600.webp'
    n0_title, n0_body = theme['notes'][0][0][lang], theme['notes'][0][1][lang]
    n1_title, n1_body = theme['notes'][1][0][lang], theme['notes'][1][1][lang]
    comp_cards = ''.join(_comp_card(p, lang, pt) for pt in sol['parts'])
    hidden_attr = '' if is_first else ' hidden'

    return (
        f'<div class="sol-showcase-card" data-sol-panel="{esc(slug)}"{hidden_attr}>'
        f'<div class="sol-showcase-top">'
        f'<div>'
        f'<p class="sol-showcase-en" dir="ltr">{esc(theme["en"])}</p>'
        f'<h2>{esc(theme["title"][lang])}</h2>'
        f'<p class="sol-showcase-lead">{esc(theme["lead"][lang])}</p>'
        f'</div>'
        f'<a class="btn btn-primary" href="{url}">{esc(view_lbl)}</a>'
        f'</div>'
        f'<div class="sol-dim-tabs" role="tablist">{"".join(dim_tabs)}</div>'
        f'<div class="sol-showcase-split">'
        f'<div>'
        f'{body_paras}'
        f'<h3 style="font-size:1.02rem;font-weight:900;margin:16px 0 8px;color:var(--brand,#05686b)">{esc(theme["axes_h"][lang])}</h3>'
        f'<div class="sol-axes-grid">{axes_cards}</div>'
        f'<div class="sol-notes-grid">{"".join(notes_cards)}</div>'
        f'{after_paras}'
        f'</div>'
        f'<aside class="sol-Visual-stage">'
        f'<div class="sol-visual-img"><img src="{p}{main_img}" alt="{esc(sol["title"][lang])}" width="420" height="300" loading="lazy"></div>'
        f'<div class="sol-highlight-pair">'
        f'<div class="sol-hl-card"><span class="sol-hl-ico">{_SVG_WARN}</span><div><strong>{esc(n0_title)}</strong><p>{esc(n0_body)}</p></div></div>'
        f'<div class="sol-hl-card"><span class="sol-hl-ico">{_SVG_GEAR}</span><div><strong>{esc(n1_title)}</strong><p>{esc(n1_body)}</p></div></div>'
        f'</div>'
        f'</aside>'
        f'</div>'
        f'<div class="sol-parts-strip">'
        f'<h3>{esc(parts_lbl)}</h3>'
        f'<div class="sol-parts-row">{comp_cards}</div>'
        f'</div>'
        f'</div>'
    )


def interactive_showcase_section(p, lang):
    nums = {'fa': ('۰۱', '۰۲', '۰۳'), 'en': ('01', '02', '03'), 'ar': ('٠١', '٠٢', '٠٣')}[lang]
    sw_btns = []
    panels = []
    for i, s in enumerate(SOLS):
        slug = s['slug']
        on = 'true' if i == 0 else 'false'
        sw_btns.append(
            f'<button type="button" class="sol-switch-btn" role="tab" data-sol-switch="{esc(slug)}" aria-selected="{on}">'
            f'<span class="sol-switch-num">{nums[i]}</span><span>{esc(s["title"][lang])}</span></button>'
        )
        panels.append(_showcase_panel_html(p, lang, s, is_first=(i == 0)))
    js = '<script>(function(){var sec=document.getElementById("sol-showcase");if(!sec)return;function selectSol(slug,sc){document.querySelectorAll("[data-sol-switch]").forEach(function(b){b.setAttribute("aria-selected",b.getAttribute("data-sol-switch")===slug?"true":"false");});document.querySelectorAll("[data-sol-pick]").forEach(function(c){c.classList.toggle("is-active",c.getAttribute("data-sol-pick")===slug);});sec.querySelectorAll("[data-sol-panel]").forEach(function(p){p.hidden=p.getAttribute("data-sol-panel")!==slug;});if(sc)sec.scrollIntoView({behavior:"smooth",block:"start"});}document.querySelectorAll("[data-sol-switch]").forEach(function(btn){btn.addEventListener("click",function(){selectSol(btn.getAttribute("data-sol-switch"),false);});});document.querySelectorAll("[data-sol-pick]").forEach(function(card){card.addEventListener("click",function(e){if(e.target.closest("a"))return;selectSol(card.getAttribute("data-sol-pick"),true);});});sec.querySelectorAll(".sol-showcase-card").forEach(function(panel){var tabs=panel.querySelectorAll("[data-dim-btn]"),cards=panel.querySelectorAll("[data-dim-card]");tabs.forEach(function(t){t.addEventListener("click",function(){var k=t.getAttribute("data-dim-btn");tabs.forEach(function(x){x.classList.toggle("is-on",x===t);});cards.forEach(function(c){var m=(k==="all"||c.getAttribute("data-dim-card")===k);c.classList.toggle("is-highlighted",k!=="all"&&m);c.style.opacity=(k==="all"||m)?"1":"0.42";});});});});})();</script>'
    return (
        f'<section class="section sol-showcase-sec" id="sol-showcase"><div class="wrap">'
        f'<div class="sol-switcher-bar" role="tablist">{"".join(sw_btns)}</div>'
        f'{"".join(panels)}'
        f'{_measurable_value_html(p, lang)}'
        f'</div></section>\n{js}'
    )


def solutions_video_hero(p, lang):
    from layout import crumbs
    ui = UI[lang]
    cr = crumbs(p, [(ui['crumb_s'], None)], lang=lang)
    return (
        f'  <section class="page-hero about-hero solutions-hero has-playing-video">\n'
        f'    <video class="about-hero-video solutions-hero-video is-playing" autoplay muted loop playsinline webkit-playsinline disablepictureinpicture disableremoteplayback preload="metadata" tabindex="-1" aria-hidden="true" poster="{p}assets/media/hero-customers-poster.jpg?v=20261028p">\n'
        f'      <source src="{p}assets/media/hero-customers.mp4?v=20261028p" type="video/mp4">\n'
        f'    </video>\n'
        f'    <div class="wrap about-hero-grid">\n'
        f'      <div>\n'
        f'        {cr}\n'
        f'        <h1>{SOL_HERO_H1[lang]}</h1>\n'
        f'        {_sol_slogan_html(SOL_SLOGAN_I18N[lang])}\n'
        f'        <p class="sol-hero-lead">{esc(SOL_HERO_LEAD[lang])}</p>\n'
        f'        {_hero_trio_html(p, lang, "fluid-management")}\n'
        f'      </div>\n'
        f'    </div>\n'
        f'  </section>'
    )


def solution_main(p, lang, sol):
    from layout import crumbs
    ui = UI[lang]
    slug = sol['slug']
    future = badge(lang, 'future') if sol['future'] else f'<span class="sol-hcard-badge">{esc(ui["active"])}</span>'
    cta = (f'<div class="ps-actions"><a class="btn btn-primary" href="{href(p, lang, CONTACT[lang])}">{esc(ui["quote"])}</a>'
           f'<button class="btn btn-ghost" type="button" data-sol-open style="color:#fff;border-color:rgba(255,255,255,.5)">{esc(ui["config"])}</button></div>')
    cr = crumbs(p, [(ui['crumb_s'], href(p, lang, 'solutions/' if lang != 'ar' else 'الحلول/')), (sol['title'][lang], None)], lang=lang)
    vid = 'hero-sdgs' if slug == 'waste-management-pva' else 'hero-customers'
    slogan_lines = SOL_SUBPAGE_SLOGANS.get(slug, SOL_SLOGAN_I18N)[lang]
    hero = (
        f'  <section class="page-hero about-hero solutions-hero has-playing-video">\n'
        f'    <video class="about-hero-video solutions-hero-video is-playing" autoplay muted loop playsinline webkit-playsinline disablepictureinpicture disableremoteplayback preload="metadata" tabindex="-1" aria-hidden="true" poster="{p}assets/media/{vid}-poster.jpg?v=20261028p">\n'
        f'      <source src="{p}assets/media/{vid}.mp4?v=20261028p" type="video/mp4">\n'
        f'    </video>\n'
        f'    <div class="wrap about-hero-grid">\n'
        f'      <div>\n'
        f'        {cr}\n'
        f'        <div style="margin:6px 0">{future}</div>\n'
        f'        <h1>{esc(sol["title"][lang])}</h1>\n'
        f'        {_sol_slogan_html(slogan_lines)}\n'
        f'        <p class="sol-hero-lead">{esc(sol["sub"][lang])}</p>\n'
        f'        {cta}\n'
        f'      </div>\n'
        f'    </div>\n'
        f'  </section>'
    )
    showcase = (
        f'<section class="section sol-showcase-sec" id="sol-detail"><div class="wrap">'
        f'{_showcase_panel_html(p, lang, sol, is_first=True)}'
        f'{_measurable_value_html(p, lang)}'
        f'</div></section>'
    )
    philosophy = PHIL.theme_html(lang, sol['slug'], lambda h: href(p, lang, h))
    parts = ''.join(_part(p, lang, part) for part in sol['parts'])
    cta_light = (f'<div class="ps-actions"><a class="btn btn-primary" href="{href(p, lang, CONTACT[lang])}">{esc(ui["quote"])}</a>'
                 f'<button class="btn btn-ghost" type="button" data-sol-open>{esc(ui["config"])}</button></div>')
    sales = (f'<p>{esc(ui["sales_p"])}</p>{cta_light}'
             f'<div class="doc-links"><a href="{CATALOGUE}" target="_blank" rel="noopener" data-track="catalogue_download">{esc(ui["cat"])}</a>'
             f'<a href="{href(p, lang, CONTACT[lang])}">{esc(ui["quote"])}</a>'
             f'<a href="{href(p, lang, {"fa": "calculator/", "en": "calculator/", "ar": "الحوسبة/"}[lang])}">{esc(ui["s_econ"])}</a></div>')
    body = (
        f'<section class="section sol-sec" id="parts"><div class="wrap"><h2>{esc(ui["s_parts"])}</h2>'
        f'<div class="ps-parts">{parts}</div></div></section>'
        f'<section class="section sol-sec section--alt" id="sales"><div class="wrap"><h2>{esc(ui["s_sales"])}</h2>{sales}</div></section>'
    )
    return hero + '\n' + showcase + '\n' + philosophy + '\n' + body + '\n' + configurator(lang)



def _card(p, lang, href_, title, sub, photo, kind, badge_html=''):
    src = PHOTO.get(photo)
    ph = (f'<div class="ph"><img src="{p}{src}" alt="" loading="lazy"></div>' if src else '')
    return (f'<a class="ps-card" href="{href_}">{ph}<span class="ps-card-top">{icons(p, kind)}{badge_html}</span>'
            f'<strong>{esc(title)}</strong><em>{esc(sub)}</em></a>')


def architecture(p, lang, default='product', layers=False):
    ui = UI[lang]
    prod_links = ''.join(
        f'<li><a href="{prod_href(p, lang, c["slug"])}">{esc(c["title"][lang])}</a></li>' for c in CATALOG)
    sol_links = ''.join(
        f'<li><a href="{sol_href(p, lang, s["slug"])}">{esc(s["title"][lang])}'
        f'{badge(lang, "future") if s["future"] else ""}</a></li>' for s in SOLS)
    overview = f'''<div class="ps-overview">
      <article class="ps-ov"><div class="ps-ov-h">{icons(p, "product")}<h3>{esc(ui["by_p"])}</h3></div>
        <p class="ps-kicker">{esc(ui["keep"])}</p><ul class="ps-links">{prod_links}</ul></article>
      <article class="ps-ov ps-ov--sol"><div class="ps-ov-h">{icons(p, "solution")}<h3>{esc(ui["by_s"])}</h3></div>
        <p class="ps-kicker">{esc(ui["new_path"])}</p><ul class="ps-links">{sol_links}</ul></article>
    </div>
    <p class="ps-note">{esc(ui["note"])}</p>'''
    prod_cards = ''.join(
        _card(p, lang, prod_href(p, lang, c['slug']), c['title'][lang], c['sub'][lang], c['photo'], 'product', badge(lang, 'order'))
        for c in CATALOG)
    sol_cards = ''.join(
        _card(p, lang, sol_href(p, lang, s['slug']), s['title'][lang], s['sub'][lang], s['parts'][0]['photo'] or s['parts'][0]['slug'],
              'solution', badge(lang, 'future') if s['future'] else f'<span class="ps-state">{esc(ui["active"])}</span>')
        for s in SOLS)
    legend = (f'<p class="ps-legend"><span>{esc(ui["legend"])}</span>'
              f'{badge(lang, "future")}{badge(lang, "rnd")}</p>')
    p_on = 'true' if default == 'product' else 'false'
    s_on = 'true' if default == 'solution' else 'false'
    tabs = f'''<div class="ps-root" data-ps data-ps-default="{default}">
      <div class="ps-tabs" role="tablist">
        <a role="tab" href="#by-product" data-ps-tab="product" aria-selected="{p_on}">{icons(p, "product")}{esc(ui["by_p"])}</a>
        <a role="tab" href="#by-solution" data-ps-tab="solution" aria-selected="{s_on}">{icons(p, "solution")}{esc(ui["by_s"])}</a>
      </div>
      <div class="ps-panel{" is-default" if default == "product" else ""}" id="by-product" data-ps-panel="product"{"" if default == "product" else " hidden"}>
        {legend}<div class="ps-grid">{prod_cards}</div></div>
      <div class="ps-panel{" is-default" if default == "solution" else ""}" id="by-solution" data-ps-panel="solution"{"" if default == "solution" else " hidden"}>
        <p class="ps-note">{esc(ui["uneven"])}</p><div class="ps-grid">{sol_cards}</div></div>
    </div>'''
    layer = ''
    if layers:
        items = ''.join(f'<li><strong>{esc(a)}</strong>{esc(b)}</li>' for a, b in ui['layers'])
        layer = f'<h2>{esc(ui["layers_h"])}</h2><ol class="ps-layers">{items}</ol>'
    return overview + tabs + layer


def hub_main(p, lang, opening='product'):
    ui = UI[lang]
    crumb = ui['crumb_s'] if opening == 'solution' else ui['crumb_p']
    if opening == 'solution':
        hero = solutions_video_hero(p, lang)
        showcase = '\n' + interactive_showcase_section(p, lang)
        philosophy = '\n' + PHIL.hub_html(lang, lambda h: href(p, lang, h))
        return hero + showcase + philosophy + '\n  <section class="section section--alt" id="browse"><div class="wrap">\n' + architecture(
            p, lang, default='solution', layers=False
        ) + '\n  </div></section>'
    hero = page_hero(p, [(crumb, None)], esc(ui['h1']), esc(ui['sub']), lang=lang)
    return hero + '\n  <section class="section" id="browse"><div class="wrap">\n' + architecture(
        p, lang, default='product', layers=False
    ) + '\n  </div></section>'


_CHEV_PREV = ('<svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true">'
              '<path d="M14.5 5.5 8 12l6.5 6.5" fill="none" stroke="currentColor" stroke-width="2" '
              'stroke-linecap="round" stroke-linejoin="round"/></svg>')
_CHEV_NEXT = ('<svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true">'
              '<path d="M9.5 5.5 16 12l-6.5 6.5" fill="none" stroke="currentColor" stroke-width="2" '
              'stroke-linecap="round" stroke-linejoin="round"/></svg>')


def carousel(cards_html, n, prev, nxt, region):
    """Horizontal snap rail. Same chrome for solutions/products and news/articles."""
    dots = []
    for i in range(n):
        cur = ' aria-current="true"' if i == 0 else ''
        dots.append(
            f'<button type="button" class="h-dot" data-ps-dot="{i}" aria-label="{esc(region)} {i + 1}"{cur}></button>'
        )
    return (
        f'<div class="h-rail" data-ps-rail>'
        f'<button type="button" class="h-rail-btn" data-ps-prev aria-label="{esc(prev)}">{_CHEV_PREV}</button>'
        f'<div class="h-scroller" data-ps-scroller tabindex="0" role="region" aria-label="{esc(region)}">'
        f'<div class="h-track">{cards_html}</div></div>'
        f'<button type="button" class="h-rail-btn" data-ps-next aria-label="{esc(nxt)}">{_CHEV_NEXT}</button>'
        f'<div class="h-dots" data-ps-dots role="group" aria-label="{esc(region)}">{"".join(dots)}</div>'
        f'</div>'
    )


def home_section(p, lang):
    """One homepage box: product/solution tabs, each a horizontal snap rail."""
    ui = UI[lang]
    hub = href(p, lang, 'solutions/' if lang != 'ar' else 'الحلول/') + '#phil'
    tease = PHIL.teaser_html(lang, hub)
    prod_cards = ''.join(
        _card(p, lang, prod_href(p, lang, c['slug']), c['title'][lang], c['sub'][lang], c['photo'], 'product', badge(lang, 'order'))
        for c in CATALOG)
    sol_cards = ''.join(
        _card(p, lang, sol_href(p, lang, s['slug']), s['title'][lang], s['sub'][lang], s['parts'][0]['photo'] or s['parts'][0]['slug'],
              'solution', badge(lang, 'future') if s['future'] else f'<span class="ps-state">{esc(ui["active"])}</span>')
        for s in SOLS)
    prod_hub = href(p, lang, 'منتجات/' if lang == 'ar' else 'products/')
    sol_hub = href(p, lang, 'الحلول/' if lang == 'ar' else 'solutions/')
    box = f'''<div class="h-box ps-root" data-ps data-ps-home data-ps-default="product">
      <div class="ps-tabs" role="tablist" aria-orientation="horizontal" aria-label="{esc(ui["box"])}">
        <a role="tab" id="tab-by-product" href="#by-product" data-ps-tab="product" aria-selected="true" aria-controls="by-product">{icons(p, "product")}{esc(ui["by_p"])}</a>
        <a role="tab" id="tab-by-solution" href="#by-solution" data-ps-tab="solution" aria-selected="false" aria-controls="by-solution">{icons(p, "solution")}{esc(ui["by_s"])}</a>
      </div>
      <div class="ps-panel is-default" id="by-product" role="tabpanel" aria-labelledby="tab-by-product" data-ps-panel="product">
        {carousel(prod_cards, len(CATALOG), ui["prev"], ui["next"], ui["rail_p"])}</div>
      <div class="ps-panel" id="by-solution" role="tabpanel" aria-labelledby="tab-by-solution" data-ps-panel="solution" hidden>
        {carousel(sol_cards, len(SOLS), ui["prev"], ui["next"], ui["rail_s"])}</div>
      <p class="h-all">
        <a class="btn btn-ghost" data-ps-cta="product" href="{prod_hub}">{esc(ui["all_p"])}</a>
        <a class="btn btn-ghost" data-ps-cta="solution" href="{sol_hub}" hidden style="display:none">{esc(ui["all_s"])}</a>
      </p>
    </div>'''
    return (f'  <section class="section ps-block" id="products"><div class="wrap">'
            f'<div class="section-head reveal"><h2>{esc(ui["box"])}</h2><p>{esc(ui["sub"])}</p></div>'
            f'{tease}{box}</div></section>')


def _write(rel, html):
    f = SITE / rel
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(html, encoding='utf-8')
    return rel


def write_solution_pages():
    written = []
    spec = {
        'fa': ('solutions/{slug}/index.html', '../../', 'solutions/{slug}/'),
        'en': ('en/solutions/{slug}/index.html', '../../../', 'en/solutions/{slug}/'),
        'ar': ('arabic/الحلول/{slug}/index.html', '../../../', 'arabic/الحلول/{slug}/'),
    }
    for lang, (rel_t, p, can_t) in spec.items():
        ui = UI[lang]
        from pages_company import about_motion_tags
        for sol in SOLS:
            rel = rel_t.format(slug=sol['slug'])
            can = can_t.format(slug=sol['slug'])
            fa = f'solutions/{sol["slug"]}/'
            desc = sol['sub'][lang]
            h_css, m_js = about_motion_tags(p)
            html = page(p, sol['slug'], sol['title'][lang], desc, solution_main(p, lang, sol),
                        lang=lang, fa_path=fa, canonical_path=can,
                        extra_head=h_css, scripts=m_js, html_attrs='data-slogan="t1"')
            written.append(_write(rel, html))
        # hub
        if lang == 'fa':
            rel, p, can, fa = 'solutions/index.html', '../', 'solutions/', 'solutions/'
        elif lang == 'en':
            rel, p, can, fa = 'en/solutions/index.html', '../../', 'en/solutions/', 'solutions/'
        else:
            rel, p, can, fa = 'arabic/الحلول/index.html', '../../', 'arabic/الحلول/', 'solutions/'
        h_css, m_js = about_motion_tags(p)
        html = page(p, 'solutions', ui['h1'], ui['sub'], hub_main(p, lang, opening='solution'),
                    lang=lang, fa_path=fa, canonical_path=can,
                    extra_head=h_css, scripts=m_js, html_attrs='data-slogan="t1"')
        written.append(_write(rel, html))
    return written


def install_icons():
    dst = SITE / 'assets/img/icons'
    dst.mkdir(parents=True, exist_ok=True)
    pairs = [
        ('M5-teal_bcf2.svg', 'M5-teal.svg', ('by-product-teal.svg', 'by-product-light.svg')),
        ('M5-dark_a9b5.svg', 'M5-dark.svg', ('by-product-dark.svg',)),
        ('R9-teal_d60a.svg', 'R9-teal.svg', ('by-solution-teal.svg', 'by-solution-light.svg')),
        ('R9-dark_db7e.svg', 'R9-dark.svg', ('by-solution-dark.svg',)),
    ]
    for raw, canon, aliases in pairs:
        src = UPLOADS / raw
        target = dst / canon
        if src.exists():
            target.write_bytes(src.read_bytes())
        elif not target.exists():
            continue
        for alias in aliases:
            link = dst / alias
            if link.is_symlink() or link.exists():
                link.unlink()
            os.symlink(canon, link)


NAV_PAT = {
    'fa': re.compile(r'<a href="((?:\./)?(?:\.\./)*)products/"(?: aria-current="page")?>محصولات</a>'),
    'en': re.compile(r'<a href="((?:\./)?(?:\.\./)*)en/products/"(?: aria-current="page")?>Products</a>'),
    'ar': re.compile(r'<a href="((?:\./)?(?:\.\./)*)arabic/منتجات/"(?: aria-current="page")?>منتجات</a>'),
}

def _lang_of(html):
    m = re.search(r'<html[^>]*\blang="([^"]+)"', html)
    code = (m.group(1) if m else 'fa').lower()
    if code.startswith('en'):
        return 'en'
    if code.startswith('ar'):
        return 'ar'
    return 'fa'


def infer_cur(rel):
    rel = rel.replace('\\', '/')
    for sol in SOLS:
        if f'/{sol["slug"]}/' in ('/' + rel):
            return sol['slug']
    if rel.endswith('solutions/index.html') or rel.endswith('الحلول/index.html'):
        return 'solutions'
    hints = [
        ('suction-bag', ('products/suction-bag/index.html', 'كيس-الشفط/index.html')),
        ('suction-tube', ('products/suction-tube/index.html', 'en/suction-tube/index.html', 'أنبوب-الشفط/index.html')),
        ('filters', ('products/filters/index.html', 'الفلتر/index.html')),
        ('canister', ('products/canister/index.html', 'products/canisters/index.html', 'خزانات/index.html')),
        ('stand', ('products/stand/index.html', 'base-and-holder/index.html', 'تثبیت/index.html')),
        ('connectors', ('products/connectors/index.html', 'products/connections/index.html', 'الوصلات/index.html')),
        ('oral', ('products/oral-hygiene/index.html', 'نظافة-الفم/index.html')),
        ('other', ('products/other/index.html', 'other-products/index.html', 'منتجات-اخری/index.html')),
    ]
    for slug, tails in hints:
        if any(rel.endswith(t) for t in tails):
            return slug
    return ''


def nav_pair(prefix, lang, cur):
    items = [it for it in NAV[lang] if it[0] in ('products', 'solutions')]
    return ''.join(_nav_item(prefix, root_of(lang), cur, it) for it in items)


def assert_nav_catalog_sync():
    """Header dropdown slugs/paths must match CATALOG / SOLS (guards a products/solutions swap)."""
    future = {'fa': 'آینده', 'en': 'Future', 'ar': 'مستقبل'}
    sol_href = {
        'fa': lambda slug: f'solutions/{slug}/',
        'en': lambda slug: f'solutions/{slug}/',
        'ar': lambda slug: f'الحلول/{slug}/',
    }
    for lang in ('fa', 'en', 'ar'):
        nav = {item[0]: item for item in NAV[lang]}
        prod = nav['products'][3]
        sol = nav['solutions'][3]
        if [row[0] for row in prod] != [c['slug'] for c in CATALOG]:
            raise SystemExit(f'NAV[{lang}] product slugs ≠ CATALOG order')
        if [row[1] for row in prod] != [c['href'][lang] for c in CATALOG]:
            raise SystemExit(f'NAV[{lang}] product hrefs ≠ CATALOG')
        if [row[0] for row in sol] != [s['slug'] for s in SOLS]:
            raise SystemExit(f'NAV[{lang}] solution slugs ≠ SOLS (possible menu swap)')
        if [row[1] for row in sol] != [sol_href[lang](s['slug']) for s in SOLS]:
            raise SystemExit(f'NAV[{lang}] solution hrefs ≠ SOLS')
        for row, s in zip(sol, SOLS):
            if s['future'] and (len(row) < 4 or row[3] != future[lang]):
                raise SystemExit(f'NAV[{lang}] solutions future badge missing on {s["slug"]}')


_NAV_PREFIX = {
    'fa': re.compile(r'href="((?:\./)?(?:\.\./)*)products/(?:#by-product)?"'),
    'en': re.compile(r'href="((?:\./)?(?:\.\./)*)en/products/(?:#by-product)?"'),
    'ar': re.compile(r'href="((?:\./)?(?:\.\./)*)arabic/منتجات/(?:#by-product)?"'),
}
_PS_BLOCK = re.compile(
    r'<div class="nav-item has-sub" data-ps-nav="(?:products|solutions)">.*?</div>\s*</div>',
    re.S,
)


def stamp_nav_html(html, rel):
    m = re.search(r'(<nav class="nav" id="mainNav"[^>]*>)(.*?)(</nav>)', html, re.S)
    if not m:
        return html, False
    inner = m.group(2)
    lang = _lang_of(html)
    found = _NAV_PREFIX[lang].search(inner) or NAV_PAT[lang].search(inner)
    if not found:
        return html, False
    cur = infer_cur(rel)
    if not cur and 'aria-current="page"' in found.group(0):
        cur = 'products'
    pair = nav_pair(found.group(1), lang, cur)
    if 'data-ps-nav="products"' in inner:
        inner2, n = _PS_BLOCK.subn(pair, inner, count=1)
        # subn count=1 only replaces the first block. Replace both by splitting.
        blocks = list(_PS_BLOCK.finditer(inner))
        if len(blocks) >= 2 and blocks[0].start() < blocks[1].end():
            inner = inner[:blocks[0].start()] + pair + inner[blocks[1].end():]
        elif n:
            inner = inner2
        else:
            return html, False
    else:
        inner = inner[:found.start()] + pair + inner[found.end():]
    html = html[:m.start()] + m.group(1) + inner + m.group(3) + html[m.end():]
    return html, True


def stamp_footer_html(html):
    lang = _lang_of(html)

    def repl(block):
        if 'data-ps-foot' in block:
            return block
        found = NAV_PAT[lang].search(block)
        if not found:
            return block
        url = href(found.group(1), lang, 'solutions/' if lang != 'ar' else 'الحلول/')
        if url in block:
            return block
        label = next(it[2] for it in NAV[lang] if it[0] == 'solutions')
        link = f'<a href="{url}" data-ps-foot="solutions">{label}</a>'
        return block[:found.end()] + '\n        ' + link + block[found.end():]

    return re.sub(r'<div class="foot-links">.*?</div>', lambda m: repl(m.group(0)), html, flags=re.S)


def badge_tabs(html, lang):
    def repl(m):
        if 'ps-badge' in m.group(0):
            return m.group(0)
        return m.group(0)[:-4] + badge(lang, status_for(m.group(1))) + '</a>'
    return re.sub(r'<a href="#([^"]+)" data-ptab="[^"]+">[^<]*</a>', repl, html)


def badge_size_links(html, lang):
    def repl(m):
        if 'ps-badge' in m.group(0):
            return m.group(0)
        return m.group(1) + m.group(2) + badge(lang, 'order') + m.group(3)
    return re.sub(r'(<a href="#(?:s1|s2|s3)">)([^<]*)(</a>)', repl, html)


def badge_panel_heads(html, lang):
    def repl(m):
        block = m.group(0)
        head, _, rest = block.partition('</h2>')
        if 'ps-badge' in head:
            return block
        status = 'soon' if 'id="splashvac"' in block[:120] else 'order'
        head = re.sub(r'(<h2[^>]*>)', r'\1', head, count=1)
        # insert before the closing that we split off
        return head + badge(lang, status) + '</h2>' + rest
    return re.sub(r'<article class="ptab[^"]*" id="[^"]+">.*?</article>', repl, html, flags=re.S)


PRODUCT_FILES = [
    ('products/suction-bag/index.html', 'fa', 'suction-bag', '../../'),
    ('products/suction-tube/index.html', 'fa', 'suction-tube', '../../'),
    ('products/filters/index.html', 'fa', 'filters', '../../'),
    ('products/canister/index.html', 'fa', 'canister', '../../'),
    ('products/stand/index.html', 'fa', 'stand', '../../'),
    ('products/connectors/index.html', 'fa', 'connectors', '../../'),
    ('products/oral-hygiene/index.html', 'fa', 'oral', '../../'),
    ('products/other/index.html', 'fa', 'other', '../../'),
    ('en/products/suction-bag/index.html', 'en', 'suction-bag', '../../../'),
    ('en/suction-tube/index.html', 'en', 'suction-tube', '../../'),
    ('en/products/filters/index.html', 'en', 'filters', '../../../'),
    ('en/products/canisters/index.html', 'en', 'canister', '../../../'),
    ('en/products/base-and-holder/index.html', 'en', 'stand', '../../../'),
    ('en/products/connections/index.html', 'en', 'connectors', '../../../'),
    ('en/products/oral-hygiene/index.html', 'en', 'oral', '../../../'),
    ('en/products/other-products/index.html', 'en', 'other', '../../../'),
    ('arabic/كيس-الشفط/index.html', 'ar', 'suction-bag', '../../'),
    ('arabic/أنبوب-الشفط/index.html', 'ar', 'suction-tube', '../../'),
    ('arabic/الفلتر/index.html', 'ar', 'filters', '../../'),
    ('arabic/خزانات/index.html', 'ar', 'canister', '../../'),
    ('arabic/تثبیت/index.html', 'ar', 'stand', '../../'),
    ('arabic/الوصلات/index.html', 'ar', 'connectors', '../../'),
    ('arabic/نظافة-الفم/index.html', 'ar', 'oral', '../../'),
    ('arabic/منتجات-اخری/index.html', 'ar', 'other', '../../'),
]


def stamp_product_html(html, p, lang, slug):
    html = strip_rollout_badges(html)
    html = badge_tabs(html, lang)
    html = badge_size_links(html, lang)
    html = badge_panel_heads(html, lang)
    if slug == 'other' and 'id="pva"' not in html:
        html = re.sub(r'(<div class="ptab-nav" role="tablist">.*?</div>)',
                      lambda m: m.group(1) + pva_card(p, lang), html, count=1, flags=re.S)
    if 'id="related-solutions"' not in html:
        html = html.replace('</main>', related_section(p, lang, slug) + '</main>', 1)
    return html


def stamp_product_pages():
    n = 0
    for rel, lang, slug, p in PRODUCT_FILES:
        path = SITE / rel
        if not path.exists():
            continue
        raw = path.read_text(encoding='utf-8')
        new = stamp_product_html(raw, p, lang, slug)
        if new != raw:
            path.write_text(new, encoding='utf-8')
            n += 1
    return n


def stamp_home():
    homes = [('index.html', '', 'fa'), ('en/index.html', '../', 'en'), ('arabic/index.html', '../', 'ar')]
    n = 0
    for rel, p, lang in homes:
        path = SITE / rel
        if not path.exists():
            continue
        raw = path.read_text(encoding='utf-8')
        block = home_section(p, lang).strip('\n')
        if 'class="section ps-block" id="products"' in raw:
            pat = r'[ \t]*<section class="section ps-block" id="products">.*?</section>'
        else:
            pat = r'[ \t]*<section class="section" id="products">.*?</section>'
        new, count = re.subn(pat, lambda m, block=block: block, raw, count=1, flags=re.S)
        if count and new != raw:
            path.write_text(new, encoding='utf-8')
            n += 1
    return n


_SOL_INSERT = {
    'fa': (('icu-anesthesia', 'مراقبت‌های ویژه و بیهوشی'), ('or-efficiency', 'کارایی اتاق عمل')),
    'en': (('icu-anesthesia', 'ICU and anesthesia'), ('or-efficiency', 'OR efficiency')),
    'ar': (('icu-anesthesia', 'العناية المركزة والتخدير'), ('or-efficiency', 'كفاءة غرفة العمليات')),
}


def patch_solution_links(html):
    """Retired. The menu is exactly the three solutions in NAV."""
    return html


def stamp_site():
    nav_n = foot_n = 0
    missed = []
    for path in SITE.rglob('*.html'):
        rel = str(path.relative_to(SITE))
        raw = path.read_text(encoding='utf-8')
        html, hit = stamp_nav_html(raw, rel)
        patched = patch_solution_links(html)
        if patched != html:
            html = patched
            hit = True
        if hit:
            nav_n += 1
        elif 'id="mainNav"' in raw and 'data-ps-nav="products"' not in raw and NAV_PAT[_lang_of(raw)].search(raw):
            # products link exists but not inside the nav regex span
            if '<nav class="nav" id="mainNav"' in raw:
                missed.append(rel)
        foot = stamp_footer_html(html)
        if foot != html:
            foot_n += 1
            html = foot
        if html != raw:
            path.write_text(html, encoding='utf-8')
    return nav_n, foot_n, missed


NAV_FALLBACK = '''
/* ps-nav-fallback: dropdown for pages that do not load the main site.css */
.nav-item { position: relative; }
.nav-parent { display: inline-flex; align-items: center; gap: 6px; }
.nav-caret { display: inline-flex; width: 13px; height: 13px; border: 0; opacity: .84; transition: transform .22s ease; }
.nav-sub { position: absolute; top: calc(100% + 6px); inset-inline-start: 0; z-index: 80; display: none; flex-direction: column; min-width: 16rem; padding: 8px; background: #fff; color: #0a2e32; border-radius: 14px; box-shadow: 0 12px 32px rgba(0,0,0,.16); }
.nav-item.open > .nav-sub, .nav-item:hover > .nav-sub, .nav-item:focus-within > .nav-sub { display: flex; }
.nav-sub a { display: block; padding: 8px 10px; color: inherit; text-decoration: none; }
.nav-soon { margin-inline-start: 6px; font-size: .72rem; }
'''


def install_nav_fallback():
    for rel in ('zagros-names/shared/assets/css/site.css', 'dial-practical/assets/css/site.css', 'common/abadis-common.css'):
        path = SITE / rel
        if not path.exists():
            continue
        text = path.read_text(encoding='utf-8')
        if 'ps-nav-fallback' in text:
            continue
        path.write_text(text.rstrip() + '\n' + NAV_FALLBACK, encoding='utf-8')


def write_product_hubs():
    import pages_products
    out = []
    for lang in ('fa', 'en', 'ar'):
        out.append(pages_products.write_products_hub(_write, lang, summaries=None if lang != 'fa' else {}))
    return out


RETIRED = {
    'hospital-suction-systems': 'fluid-management',
    'icu-anesthesia': 'fluid-management',
    'or-efficiency': 'fluid-management',
    'contamination-control': 'waste-management-pva',
}


def write_redirects():
    """Old solution URLs keep a noindex hop so bookmarks do not 404."""
    written = []
    spec = (
        ('fa', 'solutions/{slug}/index.html', '../{dest}/'),
        ('en', 'en/solutions/{slug}/index.html', '../{dest}/'),
        ('ar', 'arabic/الحلول/{slug}/index.html', '../{dest}/'),
    )
    labels = {
        'fa': 'این صفحه به راهکار به‌روز منتقل شده است.',
        'en': 'This page has moved to the current solution.',
        'ar': 'انتقلت هذه الصفحة إلى الحل الحالي.',
    }
    for slug, dest in RETIRED.items():
        for lang, rel_t, href_t in spec:
            rel = rel_t.format(slug=slug)
            target = href_t.format(dest=dest)
            html = (
                f'<!DOCTYPE html>\n<html lang="{lang}" data-theme="light">\n<head>\n'
                f'<meta charset="UTF-8">\n<meta name="robots" content="noindex,nofollow">\n'
                f'<meta http-equiv="refresh" content="0; url={target}">\n'
                f'<title>{labels[lang]}</title>\n'
                f'<script>location.replace({target!r})</script>\n</head>\n'
                f'<body><p><a href="{target}">{labels[lang]}</a></p></body>\n</html>\n'
            )
            written.append(_write(rel, html))
    return written


def main():
    install_nav_fallback()
    pages = write_solution_pages()
    pages += write_redirects()
    hubs = write_product_hubs()
    homes = stamp_home()
    products = stamp_product_pages()
    nav_n, foot_n, missed = stamp_site()
    print(f'solutions {len(pages)} hubs {hubs} homes {homes} product-pages {products} nav {nav_n} footer {foot_n} missed {len(missed)}')
    for rel in missed[:20]:
        print(' miss', rel)


if __name__ == '__main__':
    main()
