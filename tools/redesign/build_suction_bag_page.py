#!/usr/bin/env python3
"""Rebuild the hand-built 1L suction-bag pages (FA / EN / AR) around cinematic v12.

Live abadis-med.com copy is quoted verbatim. Digits are rewritten per language;
measurement runs are wrapped in dir=ltr so the bidi algorithm cannot reorder them.
The old apple / cutaway / product-viewer blocks are not reinserted.
"""
import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from yn_icons import yn_no, yn_yes  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / 'site'

FA_DIG = str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')
AR_DIG = str.maketrans('0123456789', '٠١٢٣٤٥٦٧٨٩')

V = '20261110w'

ARROW = ('<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
         '<path d="M9 5l7 7-7 7" fill="none" stroke="currentColor" stroke-width="2" '
         'stroke-linecap="round" stroke-linejoin="round"/></svg>')
PAUSE = ('<svg class="ico-pause" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M7 5h3.2v14H7zM13.8 5H17v14h-3.2z"/></svg>'
         '<svg class="ico-play" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M8 5.5v13l11-6.5z"/></svg>')


def esc(s):
    return html.escape(s, quote=True)


def digits(s, lang):
    if lang == 'fa':
        return s.translate(FA_DIG)
    if lang == 'ar':
        return s.translate(AR_DIG)
    return s


def meas(s, lang):
    """Persian/Arabic digits. One LTR isolate per measurement run so spaces inside stay one text node."""
    s = digits(s, lang)
    if lang == 'en':
        return esc(s)
    def repl(m):
        return '<bdi dir="ltr">' + esc(m.group(0)) + '</bdi>'
    return re.sub(
        r'\*?[0-9۰-۹٠-٩]+(?:[./,\*×xX\-–][0-9۰-۹٠-٩]+)*(?:cm|g|pcs)?|[A-Za-z][A-Za-z0-9\-]*',
        repl, s)


def yn(flag, lang):
    if flag == 'yes':
        return yn_yes({'fa': 'دارد', 'en': 'Yes', 'ar': 'نعم'}[lang])
    if flag == 'no':
        return yn_no({'fa': 'ندارد', 'en': 'No', 'ar': 'لا'}[lang])
    return esc(str(flag))


def lid(kind, lang):
    name = {
        'teal': {'fa': 'فیروزه‌ای', 'en': 'Teal', 'ar': 'فيروزي'},
        'yellow': {'fa': 'زرد', 'en': 'Yellow', 'ar': 'أصفر'},
        'red': {'fa': 'قرمز', 'en': 'Red', 'ar': 'أحمر'},
    }[kind][lang]
    return f'<span class="lid lid-{kind}" role="img" aria-label="{esc(name)}"></span>'


# code, irc, size, filter, powder, sterile|None, lid
# powder/sterile: yes/no/text (text kept, e.g. the live "×" filter cell)
FA_ROWS = {
    '1': [
        ('۰۴۰۱۱۱۱', '6952056777153306', 'یک لیتری', 'هیدروفوبیک', 'yes', None, 'teal'),
        ('۰۴۰۱۰۱۱', '7817505042353929', 'یک لیتری', 'هیدروفوبیک', 'no', None, 'teal'),
    ],
    '2': [
        ('۰۴۰۱۱۱۲', '9647935197253589', 'دو لیتری', 'هیدروفوبیک', 'yes', None, 'teal'),
        ('۰۴۰۱۱۰۲', '5826314295044204', 'دو لیتری', '×', 'yes', None, 'yellow'),
        ('۰۴۰۱۰۱۲', '4383099410749165', 'دو لیتری', 'هیدروفوبیک', 'no', None, 'teal'),
        ('0401132', '4111380328256244', 'دو لیتری', 'مکانیکی', 'yes', None, 'red'),
        ('0401112', '9647935197253589', 'دو لیتری', 'CIF', 'yes', None, 'yellow'),
    ],
    '3': [
        ('۰۴۰۱۱۱۳', '6579214989949869', 'سه لیتری', 'هیدروفوبیک', 'yes', 'no', 'teal'),
        ('۰۴۰۱۱۰۳', '3226257467113524', 'سه لیتری', '×', 'yes', 'no', 'yellow'),
        ('۰۴۰۱01۳', '7600653363719319', 'سه لیتری', 'هیدروفوبیک', 'no', 'no', 'teal'),
        ('۰۴۰۱12۳', '7600653363719319', 'سه لیتری', 'Dual', 'yes', 'no', 'teal'),
        ('۰۴۰۱۱۳3', '2707894365287680', 'سه لیتری', 'مکانیکی', 'yes', 'no', 'red'),
        ('0401213', '9787915172873298', 'سه لیتری', 'هیدروفوبیک', 'yes', 'no', 'teal'),
        ('0401113-2', '_', 'سه لیتری', 'هیدروفوبیک', 'yes', 'yes', 'teal'),
        ('۰۴۰۱۱۱۳', '6579214989949869', 'سه لیتری', 'CIF', 'yes', 'no', 'yellow'),
    ],
}
EN_ROWS = {
    '1': [
        ('0401111', '', '', 'Hydrophobic', 'yes', None, 'teal', 'Final'),
        ('0401021', '', '', 'Dual', 'no', None, 'teal', 'Final'),
        ('0401031', '', '', 'Mechanical', 'no', None, 'red', 'Final'),
        ('0401011', '', '', 'Hydrophobic', 'no', None, 'teal', 'Final'),
        ('0401121', '', '', 'Dual', 'yes', None, 'teal', 'Final'),
        ('0401131', '', '', 'Mechanical', 'yes', None, 'red', 'Final'),
    ],
    '2': [
        ('0401112', '', '', 'Hydrophobic', 'yes', None, 'teal', 'Final'),
        ('0401002', '', '', '×', 'no', None, 'teal', 'Primary'),
        ('0401022', '', '', 'Dual', 'no', None, 'teal', 'Final'),
        ('0401032', '', '', 'Mechanical', 'no', None, 'red', 'Final'),
        ('0401102', '', '', '×', 'yes', None, 'teal', 'Primary'),
        ('0401012', '', '', 'Hydrophobic', 'no', None, 'teal', 'Final'),
        ('0401122', '', '', 'Dual', 'yes', None, 'teal', 'Final'),
        ('0401132', '', '', 'Mechanical', 'yes', None, 'red', 'Final'),
    ],
    '3': [
        ('0401113', '', '', 'Hydrophobic', 'yes', 'no', 'teal', 'Final'),
        ('0401103', '', '', '×', 'yes', 'no', 'teal', 'Primary'),
        ('0401013', '', '', 'Hydrophobic', 'no', 'no', 'teal', 'Final'),
        ('0401123', '', '', 'Dual', 'yes', 'no', 'teal', 'Final'),
        ('0401133', '', '', 'Mechanical', 'yes', 'no', 'red', 'Final'),
        ('0401213', '', '', 'Hydrophobic', 'yes', 'no', 'teal', 'Final'),
        ('0401133-2', '', '', 'Hydrophobic', 'yes', 'yes', 'teal', 'Final'),
    ],
}
AR_ROWS = {
    '1': [
        ('0401111', '6952056777153306', '1 لتر', 'كاره للماء', 'yes', None, 'teal'),
        ('0401011', '7817505042353929', '1 لتر', 'كاره للماء', 'no', None, 'teal'),
    ],
    '2': [
        ('0401112', '9647935197253589', 'دو لیتری', 'كاره للماء', 'yes', None, 'teal'),
        ('0401102', '5826314295044204', '2 لتر', '×', 'yes', None, 'yellow'),
        ('0401012', '4383099410749165', '2 لتر', 'كاره للماء', 'no', None, 'teal'),
        ('0401132', '4111380328256244', '2 لتر', 'ميكانيكي', 'yes', None, 'red'),
        ('0401112', '9647935197253589', '2 لتر', 'CIF', 'yes', None, 'yellow'),
    ],
    '3': [
        ('0401113', '6579214989949869', '3 لتر', 'كاره للماء', 'yes', 'no', 'teal'),
        ('0401103', '3226257467113524', '3 لتر', '×', 'yes', 'no', 'yellow'),
        ('0401013', '7600653363719319', '3 لتر', 'كاره للماء', 'no', 'no', 'teal'),
        ('0401123', '7600653363719319', '3 لتر', 'Dual', 'yes', 'no', 'teal'),
        ('0401133', '2707894365287680', '3 لتر', 'ميكانيكي', 'yes', 'no', 'red'),
        ('0401213', '9787915172873298', '3 لتر', 'كاره للماء', 'yes', 'no', 'teal'),
        ('0401113-2', '_', '3 لتر', 'كاره للماء', 'yes', 'yes', 'teal'),
        ('0401113', '6579214989949869', '3 لتر', 'CIF', 'yes', 'no', 'yellow'),
    ],
}

UI = {
    'fa': dict(
        h1='کیسه ساکشن یکبارمصرف',
        title='کیسه ساکشن یکبارمصرف — مخازن طبی آبادیس',
        desc='کیسه ساکشن یکبارمصرف آبادیس راهکاری ایمن و بهداشتی برای جمع‌آوری ترشحات و مایعات بدن در بیمارستان‌ها، آمبولانس‌ها و مراکز درمانی است.',
        crumb=('خانه', '../../', 'محصولات', '../../products/', 'کیسه ساکشن'),
        quote='درخواست قیمت', quote_href='../../contact/',
        specs='مشخصات', pause='توقف یا ادامه حرکت',
        intro_h='کیسه ساکشن یکبارمصرف آبادیس',
        intro_p='کیسه ساکشن یکبارمصرف آبادیس راهکاری ایمن و بهداشتی برای جمع‌آوری ترشحات و مایعات بدن در بیمارستان‌ها، آمبولانس‌ها و مراکز درمانی است. پودر ژل‌کننده داخل کیسه، مایعات را به ژل تبدیل می‌کند و خطر ریختن و آلودگی را کم می‌کند. فیلتر هیدروفوبیک هم از سرریز مایع به سمت دستگاه جلوگیری می‌کند و سیستم حفاظت از ساکشن مرکزی، دستگاه را ایمن نگه می‌دارد.',
        nav=[('intro', 'معرفی'), ('features', 'مشخصات'), ('size', 'سایز'), ('gallery', 'تصاویر'), ('codes', 'کدها'), ('packaging', 'بسته‌بندی'), ('uses', 'مصرف'), ('catalog', 'کاتالوگ'), ('order', 'قیمت')],
        uses_h='موارد مصرف',
        packaging_h='بسته‌بندی و کارتن',
        filters_h='فیلترها',
        catalog_h='کاتالوگ',
        catalog_lead='دانلود کاتالوگ و راهنمای استفاده از بخش درخواست قیمت.',
        stats_h='اعداد کلیدی',
        stats=[
            ('۱، ۲ و ۳ لیتر', 'حجم‌های کیسه'),
            ('۱۱ سانتی‌متر', 'قطر کیسه'),
            ('۱۵٫۵\u00a0/\u00a0۲۴٫۵\u00a0/\u00a0۳۹', 'ارتفاع، سانتی\u200cمتر'),
            ('۴۵ عدد', 'در هر کارتن'),
        ],
        gal_h='تصاویر محصول',
        gal_lead='عکس محصول، نماهای تک‌زاویه و طرح خطی ایزومتریک تعاملی.',
        iso_cap='طرح خطی ایزومتریک. برای چرخش، روی طرح بزنید و بکشید.',
        iso_load='نمایش طرح تعاملی',
        iso_filter_cap='طرح خطی ایزومتریک فیلتر قطع‌کننده جریان. برای چرخش، روی طرح بزنید و بکشید.',
        codes_h='کد محصول',
        sizes_h='سایزها',
        sizes_lead='ظرفیت‌ها — ۱ لیتری، ۲ لیتری و ۳ لیتری. تصاویر، جدول کدینگ، ابعاد و بسته‌بندی و موارد مصرف هر سایز در زبانه همان سایز است.',
        spec_h='مشخصات',
        features_h='مشخصات و ویژگی‌ها',
        size_facts_h='سایز',
        pack_table_h='ابعاد، وزن و بسته‌بندی',
        series_lbl='حالت سری',
        vol_lbl='حجم',
        diam_lbl='قطر',
        height_lbl='ارتفاع',
        close_h='درخواست قیمت',
        close_p='برای انتخاب مدل، فیلتر و بسته‌بندی با فروش آبادیس در تماس باشید.',
        call='تماس با فروش',
        catalog='دانلود کاتالوگ',
        catalog_href='../../wp-content/uploads/2022/12/suction-bag-catalog-Fa.pdf',
        guide='راهنمای استفاده کاربر نهایی',
        guide_href='../../install-guide/end-user/',
        how='برای مشاهده نحوه استفاده از کیسه ساکشن ها به این صفحه مراجعه نمایید .',
        heads=['کد محصول', 'IRC', 'نوع فیلتر', 'هیدروفوبیک', 'پودر جاذب', 'رنگ درب', 'استریل'],
        beats=[
            ('.12', '.23', 'پورت بیمار با درپوش بنددار'),
            ('.26', '.37', 'فیلتر قطع‌کننده زیر پورت خلأ از سرریز جلوگیری می‌کند'),
            ('.39', '.50', 'پودر جاذب در ساشه دربسته'),
            ('.53', '.64', 'ترشحات داخل کیسه جمع می‌شود'),
            ('.66', '.78', 'پودر جاذب مایع را ژل می‌کند'),
            ('.80', '.90', 'کیسه پلی‌اتیلن نرم، یکبارمصرف'),
        ],
        hint='اسکرول کنید',
        prev='قبلی', next='بعدی',
        still_alt='کیسه ساکشن ۲ لیتری آبادیس، درب فیروزه‌ای نشسته روی لبه کیسه',
    ),
    'en': dict(
        h1='Disposable Suction Bag',
        title='Disposable Suction Bag — Abadis Medical Reservoirs',
        desc='The Abadis disposable suction bag is a safe and hygienic solution for collecting body fluids and secretions in hospitals, ambulances and treatment centres.',
        crumb=('Home', '../../../en/', 'Products', '../', 'Disposable Suction Bag'),
        quote='Request quote', quote_href='../../contact-us/',
        specs='Specifications', pause='Pause or play motion',
        intro_h='Abadis disposable suction bag',
        intro_p='The Abadis disposable suction bag is a safe and hygienic solution for collecting body fluids and secretions in hospitals, ambulances and treatment centres. The gelling powder inside the bag turns fluids into gel and reduces the risk of spills and contamination. The hydrophobic filter also prevents liquid overflowing toward the device, and the central suction protection system keeps the device safe.',
        nav=[('intro', 'Overview'), ('features', 'Features'), ('size', 'Size'), ('gallery', 'Images'), ('codes', 'Codes'), ('packaging', 'Packaging'), ('uses', 'Usage'), ('catalog', 'Catalog'), ('order', 'Quote')],
        uses_h='Usage',
        packaging_h='Packaging & carton',
        filters_h='Filters',
        catalog_h='Catalog',
        catalog_lead='Download the catalog from the quote section.',
        stats_h='Key numbers',
        stats=[
            ('1, 2 and 3 L', 'Bag volumes'),
            ('11 cm', 'Bag diameter'),
            ('15.5\u00a0/\u00a024.5\u00a0/\u00a039', 'Height, cm'),
            ('45 pcs', 'Per carton'),
        ],
        gal_h='Product images',
        gal_lead='Product photos, single-view drawings, and an interactive isometric line drawing.',
        iso_cap='Isometric line drawing. Tap the drawing and drag to rotate.',
        iso_load='View interactive drawing',
        iso_filter_cap='Isometric line drawing of the flow-stopper filter. Tap the drawing and drag to rotate.',
        codes_h='Product codes',
        sizes_h='Sizes',
        sizes_lead='Capacities — 1 litre, 2 litre and 3 litre. Each size holds its images, coding table, dimensions and packaging, and uses.',
        spec_h='Specifications',
        features_h='Specifications and features',
        size_facts_h='Size',
        pack_table_h='Dimensions, weight and packaging',
        series_lbl='Series mode',
        vol_lbl='Volume',
        diam_lbl='Diameter',
        height_lbl='Height',
        close_h='Request a quote',
        close_p='Abadis sales can help with model, filter and packaging.',
        call='Call sales',
        catalog='Download catalog',
        catalog_href='../../wp-content/uploads/2021/12/suction-bag-catalog-En.pdf',
        guide='End-user guide',
        guide_href='../../installation-manual/',
        export='Export enquiry',
        export_href='../../export/#quote',
        how='',
        heads=['Product code', 'IRC', 'Filter type', 'Hydrophobic', 'Absorbent powder', 'Lid color', 'Sterile', 'Suction bag'],
        beats=[
            ('.12', '.23', 'PATIENT port with tethered cap'),
            ('.26', '.37', 'The flow stopper filter under the VACUUM port stops overflow'),
            ('.39', '.50', 'Absorbent powder sealed in a mesh sachet'),
            ('.53', '.64', 'Fluid collects inside the liner bag'),
            ('.66', '.78', 'Absorbent powder turns fluid into gel'),
            ('.80', '.90', 'Soft PE liner, single use'),
        ],
        hint='Scroll',
        prev='Previous', next='Next',
        still_alt='Abadis 2 litre suction liner with the teal lid seated on the bag rim',
    ),
    'ar': dict(
        h1='كيس الشفط',
        title='كيس الشفط — مخازن طبی آباديس',
        desc='كيس الشفط أحادي الاستعمال من آباديس حل آمن وصحي لجمع المفرزات وسوائل الجسم في المستشفيات وسيارات الإسعاف ومراكز العلاج.',
        crumb=('الرئيسية', '../../', 'منتجات', '../منتجات/', 'كيس الشفط'),
        quote='طلب عرض سعر', quote_href='../اتصل-بنا/',
        specs='المواصفات', pause='إيقاف الحركة أو متابعتها',
        intro_h='كيس الشفط أحادي الاستعمال من آباديس',
        intro_p='كيس الشفط أحادي الاستعمال من آباديس حل آمن وصحي لجمع المفرزات وسوائل الجسم في المستشفيات وسيارات الإسعاف ومراكز العلاج. يحوّل مسحوق التهليم داخل الكيس السوائل إلى هلام ويقلل خطر الانسكاب والتلوث. كما يمنع الفلتر الكاره للماء فيض السائل نحو الجهاز، ويُبقي نظام حماية الشفط المركزي الجهاز آمناً.',
        nav=[('intro', 'مقدمة'), ('features', 'المواصفات'), ('size', 'الحجم'), ('gallery', 'الصور'), ('codes', 'الرموز'), ('packaging', 'التغليف'), ('uses', 'الاستخدام'), ('catalog', 'الكتالوج'), ('order', 'السعر')],
        uses_h='الاستخدامات',
        packaging_h='التغليف والكرتون',
        filters_h='الفلاتر',
        catalog_h='الكتالوج',
        catalog_lead='تنزيل الكتالوج من قسم طلب عرض السعر.',
        stats_h='أرقام أساسية',
        stats=[
            ('١، ٢ و٣ لتر', 'سعات الكيس'),
            ('١١ سم', 'قطر الكيس'),
            ('١٥٫٥\u00a0/\u00a0٢٤٫٥\u00a0/\u00a0٣٩', 'الارتفاع، سم'),
            ('٤٥ قطعة', 'في كل كرتون'),
        ],
        gal_h='صور المنتج',
        gal_lead='صور المنتج ورسوم بزاوية واحدة ورسم خطّي أيزومتري تفاعلي.',
        iso_cap='رسم خطّي أيزومتري. اضغط على الرسم واسحب للدوران.',
        iso_load='عرض الرسم التفاعلي',
        iso_filter_cap='رسم خطّي أيزومتري لفلتر قطع التدفق. اضغط على الرسم واسحب للدوران.',
        codes_h='رموز المنتج',
        sizes_h='الأحجام',
        sizes_lead='السعات — ١ لتر و٢ لتر و٣ لتر. صور كل سعة وجدول الرموز والأبعاد والتغليف والاستخدامات في تبويبها.',
        spec_h='مواصفات المنتج',
        features_h='المواصفات والميزات',
        size_facts_h='الحجم',
        pack_table_h='الأبعاد والوزن والتغليف',
        series_lbl='الوضع المتسلسل',
        vol_lbl='السعة',
        diam_lbl='القطر',
        height_lbl='الارتفاع',
        close_h='طلب عرض سعر',
        close_p='فريق مبيعات آباديس يساعد في اختيار الموديل والفلتر والتعبئة.',
        call='اتصل بالمبيعات',
        catalog='تنزيل الكتالوج',
        catalog_href='../wp-content/uploads/2022/12/suction-bag-catalog-Fa.pdf',
        guide='دليل المستخدم النهائي',
        guide_href='../دليل-التركيب/',
        how='اذهب إلى هذه الصفحة لمعرفة كيفية استخدام أكياس الشفط.',
        heads=['رمز المنتج', 'IRC', 'نوع الفلتر', 'كاره للماء', 'المسحوق الماص', 'لون الغطاء', 'معقّم'],
        beats=[
            ('.12', '.23', 'منفذ المريض بغطاء مربوط'),
            ('.26', '.37', 'فلتر قطع الفيضان تحت منفذ التفريغ يمنع الفيض'),
            ('.39', '.50', 'المسحوق الماص في كيس مغلق'),
            ('.53', '.64', 'تتجمع المفرزات داخل الكيس'),
            ('.66', '.78', 'المسحوق الماص يحوّل السائل إلى هلام'),
            ('.80', '.90', 'كيس بولي إيثيلين ليّن، استعمال واحد'),
        ],
        hint='مرّر للأسفل',
        prev='السابق', next='التالي',
        still_alt='كيس شفط آباديس سعة ٢ لتر مع غطاء فيروزي جالس على حافة الكيس',
    ),
}

# Per-size live spec lines. Strings are the live wording; meas() localises digits.
SPECS = {
    'fa': {
        '1': dict(name='کیسه ساکشن ۱ لیتری', vol='حجم ساکشن: یک لیتر',
                  char='مشخصات: دارای پودر ژل‌کننده، فیلتر هیدروفوبیک(جلوگیری از سر ریز مایعات)، سازگار با کلیه دستگاه‌های ساکشن، دارای سیستم حفاظت از ساکشن مرکزی',
                  types='انواع فیلترهای کیسه‌های نهایی: فیلترهای استفاده‌شده در کیسه‌های آبادیس در ۳ نوع تولید می‌شود که موجب جلوگیری از سرریز مایعات می‌گردد:',
                  dim='ابعاد محصول: قطر: 11cm , ارتفاع: 15/5cm', weight='وزن محصول: 92 الی 105 گرم',
                  pack='نحوه بسته بندی: نایلون', packdim='ابعاد بسته بندی هر محصول : 35*27.5 سانتی متر',
                  qty='تعداد در هر کارتن: ۴۵ عدد', carton='ابعاد کارتن: 57/5 * 42/5 *44',
                  uses_h='موارد مصرف',
                  uses=[('ambulance', 'آمبولانس'), ('infectious', 'عفونی'), ('dentistry', 'دندانپزشکی'), ('eye', 'چشم'), ('children', 'کودکان')]),
        '2': dict(name='کیسه ساکشن ۲ لیتری',
                  vol='حجم ساکشن: ۲ لیتر در حالت تکی، تا ۸ لیتر در حالت سری یک ردیفه بر روی پایه',
                  char='مشخصات: دارای پودر ژل‌کننده، فیلتر هیدروفوبیک(جلوگیری از سر ریز مایعات)، سازگار با کلیه دستگاه‌های ساکشن، دارای سیستم حفاظت از ساکشن مرکزی',
                  types='انواع فیلترهای کیسه‌های نهایی: فیلتر های استفاده شده در کیسه‌های آبادیس در ۳ نوع تولید می‌شود که موجب جلوگیری از سرریز مایعات می‌گردد:',
                  dim='ابعاد محصول: قطر: 11cm , ارتفاع: 24/5cm', weight='وزن محصول: 103 الی 130 گرم',
                  pack='نحوه بسته بندی: نایلون', packdim='ابعاد بسته بندی هر محصول: 35*27.5 سانتی متر',
                  qty='تعداد در هر کارتن: ۴۵ عدد', carton='ابعاد کارتن: 57/5 * 42/5 *44',
                  uses_h='موارد مصرف',
                  uses=[('lung', 'ریه و آندوسکوپی'), ('gi', 'گوارش'), ('icu', 'CCU/ICU'), ('infectious', 'عفونی'), ('men', 'بخش مردان'), ('women', 'بخش زنان')]),
        '3': dict(name='کیسه ساکشن ۳ لیتری',
                  vol='حجم ساکشن: ۳ لیتر در حالت تکی، تا ۱۲ لیتر در حالت سری یک ردیفه بر روی پایه',
                  char='مشخصات: دارای پودر ژل‌کننده، فیلتر هیدروفوبیک(جلوگیری از سر ریز مایعات)، سازگار با کلیه دستگاه‌های ساکشن، دارای سیستم حفاظت از ساکشن مرکزی',
                  types='انواع فیلترهای کیسه‌های نهایی: فیلترهای استفاده شده در کیسه‌های آبادیس در ۳ نوع تولید می‌شود که موجب جلوگیری از سرریز مایعات می‌گردد:',
                  dim='ابعاد محصول: قطر: 11 سانتی متر, ارتفاع: 39 سانتی متر', weight='وزن محصول: 123 الی 200 گرم',
                  pack='نحوه بسته بندی: نایلون', packdim='ابعاد بسته بندی هر محصول: 35*27.5 سانتی متر',
                  qty='تعداد در هر کارتن: ۴۵ عدد', carton='ابعاد کارتن: 49 * 49 *49',
                  uses_h='موارد مصرف',
                  uses=[('infectious', 'عفونی'), ('surgery', 'اتاق عمل'), ('cardio', 'قلب و عروق'), ('men', 'بخش مردان'), ('women', 'بخش زنان'), ('lipo', 'عمل لیپوساکشن')],
                  sterile_h='کیسه ساکشن استریل:',
                  sterile_p='کیسه ساکشن استریل آبادیس مناسب برای عمل‌های لیپوساکشن و سایر عمل‌های جراحی حساس است.',
                  merits_h='مزایا:',
                  merits=['قابلیت نمونه برداری ایمن از مایعات جمع آوری شده.', 'مکش قوی و بالا.',
                          'تولید شده در کلین روم 100,000 مطابق با الزامات تجهیزات پزشکی.',
                          'استریل و آماده استفاده در اتاق عمل.']),
    },
    'en': {
        '1': dict(name='1 Liter Single-Use Disposable Suction Liner Bag', vol='Volume: 1 liter',
                  char='Characteristic: Single-use (disposable) design, Contains gel powder, hydrophobic filter ( flow stopper filter), suitable with all suction devices, has central suction protection system',
                  types='Types of filter: Filters used in Abadis single-use suction liner bags are produced in 3 types that prevent liquids from overflowing.',
                  dim='Product Dimensions : Diameter: 11 cm, Height: 15.5 cm', weight='Product Weight : 92–105 g',
                  pack='Packaging Type : Nylon Bag', packdim='Individual Package Dimensions : 35 × 27.5 cm',
                  qty='Quantity per Carton : 45 pcs', carton='Carton Dimensions : 57.5 × 42.5 × 44 cm',
                  uses_h='Usage',
                  uses=[('ambulance', 'Ambulance'), ('infectious', 'Infectious'), ('dentistry', 'Dentistry'), ('eye', 'Eyes'), ('children', 'Children')],
                  filters=[('Hydrophobic filter', 'Prevent microorganisms and bacteria from entering the suction source and the surrounding environment'),
                           ('Dual filter', 'Prevents the reduction of pressure drop in the surgery that use the electrocautery device.'),
                           ('mechanical filter', 'It has the lowest pressure drop among existing filters')]),
        '2': dict(name='2 Liter Disposable Suction Liner Bag', vol='Volume: 2 Liter',
                  char='Characteristic: Single-use (disposable) design , Contains gel powder, hydrophobic filter ( flow stopper filter), suitable with all suction devices, has central suction protection system',
                  types='Types of filter: Filters used in Abadis single-use suction liner bags are produced in 3 types that prevent liquids from overflowing.',
                  dim='Product Dimensions : Diameter: 11 cm, Height: 24.5 cm', weight='Product Weight : 103–130 g',
                  pack='Packaging Type: Nylon Bag', packdim='Individual Package Dimensions: 35 × 27.5 cm',
                  qty='Quantity per Carton: 45 pcs', carton='Carton Dimensions: 57.5 × 42.5 × 44 cm',
                  uses_h='Usage',
                  uses=[('lung', 'Endoscopy'), ('gi', 'Digestion'), ('icu', 'ccu/icu'), ('infectious', 'Infectious'), ('men', 'Men'), ('women', 'Women')],
                  filters=[('Hydrophobic filter', 'Prevent microorganisms and bacteria from entering the suction source and the surrounding environment'),
                           ('Dual filter', 'Prevents the reduction of pressure drop in the surgery that use the electrocautery device.'),
                           ('mechanical filter', 'It has the lowest pressure drop among existing filters')]),
        '3': dict(name='3 Liter Disposable Suction Liner Bag',
                  vol='Volume: 3 Liters in single, up to 12 liters in single row mode on the base',
                  char='Characteristic: Single-use (disposable) design, Contains gel powder, hydrophobic filter, suitable with all suction devices, has central suction protection system',
                  types='Types of filter: Filters used in Abadis single-use suction bags are produced in 3 types that prevent liquids from overflowing.',
                  dim='Product Dimensions: Diameter: 11 cm, Height: 39 cm', weight='Product Weight : 123–200 g',
                  pack='Packaging Type : Nylon Bag', packdim='Individual Package Dimensions : 35 × 27.5 cm',
                  qty='Quantity per Carton: 45 pcs', carton='Carton Dimensions : 49 × 49 × 49 cm',
                  uses_h='Usage',
                  uses=[('infectious', 'Infectious'), ('surgery', 'Surgery Room'), ('cardio', 'Cardiovascular'), ('men', 'Men'), ('women', 'Women'), ('lipo', 'Liposuction Surgery')],
                  filters=[('Hydrophobic filter', 'Prevent microorganisms and bacteria from entering the suction source and the surrounding environment'),
                           ('Dual filter', 'Prevents the reduction of pressure drop in the surgery that use the electrocautery device.'),
                           ('mechanical filter', 'It has the lowest pressure drop among existing filters')]),
    },
    'ar': {
        '1': dict(name='كيس الشفط بحجم 1 لتر', vol='حجم الشفط: لتر واحد',
                  char='المواصفات: يحتوي على مسحوق هلامية، والفلتر الكاره للماء (يمنع فيض السوائل)، ويتوافق مع جميع أجهزة الشفط، ويحتوي على نظام حماية الشفط المركزي.',
                  types='أنواع فلاتر الأكياس النهائية: تنقسم الفلاتر المستخدمة في أكياس آباديس إلى ثلاثة أنواع، مما يمنع فيض السوائل:',
                  dim_d='القطر: 11 سم', dim_h='الارتفاع: 15.5 سم', weight='وزن المنتج: من 92 إلى 105 غرام',
                  pack='نوع التغليف: كيس نايلون', packdim='أبعاد تغليف كل منتج: 35 × 27.5 سم',
                  qty='الكمية في كل كرتون: 45 قطعة', carton='أبعاد الكرتون: 57.5 × 42.5 × 44 سم',
                  uses_h='الاستخدامات',
                  uses=[('ambulance', 'سياره الإسعاف'), ('infectious', 'مكافحة العدوى'), ('dentistry', 'طب الأسنان'), ('eye', 'عين'), ('children', 'الأطفال')],
                  filters=[('الفلتر الكاره للماء', 'الحيلولة دون دخول الكائنات الحية الدقيقة والبكتيريا الخطيرة إلى مخزن الشفط والبيئة المحيطة به'),
                           ('فلتر dual', 'بالإضافة إلى مزايا الفلتر الكاره للماء، فإنه يمنع انخفاض الضغط في العمليات آلة الدخان'),
                           ('الفلتر الميكانيكي', 'لا تتمتع بمزايا الفلتر الكاره للماء، ولكنه يتميز بأنه أفضل الفلاتر لمنع انخفاض الضغط.')]),
        '2': dict(name='كيس الشفط بحجم 2 لتر',
                  vol='حجم الشفط: 2 لتر عند استخدام الواحد، حتى 8 لترات عند وضع مجموعة واحدة على القاعدة',
                  char='المواصفات: يحتوي على مسحوق هلامية، والفلتر الكاره للماء (يمنع فيض السوائل)، ويتوافق مع جميع أجهزة الشفط، ويحتوي على نظام حماية الشفط المركزي.',
                  types='أنواع فلاتر الأكياس النهائية: تنقسم الفلاتر المستخدمة في أكياس آباديس إلى ثلاثة أنواع، مما يمنع فيض السوائل',
                  dim_d='القطر: 11 سم', dim_h='الارتفاع: 24.5 سم', weight='وزن المنتج: من 103 إلى 130 غرام',
                  pack='نوع التغليف: كيس نايلون', packdim='أبعاد تغليف كل منتج: 35 × 27.5 سم',
                  qty='الكمية في كل كرتون: 45 قطعة', carton='أبعاد الكرتون: 57.5 × 42.5 × 44 سم',
                  uses_h='الاستخدامات',
                  uses=[('lung', 'الرئة والتنظير الداخلي'), ('gi', 'الجهار الهضمي'), ('icu', 'وحدة العناية المركزة / وحدة العناية التاجية'), ('infectious', 'مكافحة العدوى'), ('men', 'قسم الرجال'), ('women', 'قسم النساء')],
                  filters=[('الفلتر الكاره للماء', 'الحيلولة دون دخول الكائنات الحية الدقيقة والبكتيريا الخطيرة إلى مخزن الشفط والبيئة المحيطة به'),
                           ('فلتر dual', 'بالإضافة إلى مزايا الفلتر الكاره للماء، فإنه يمنع انخفاض الضغط في العمليات آلة الدخان'),
                           ('الفلتر الميكانيكي', 'لا تتمتع بمزايا الفلتر الكاره للماء، ولكنه يتميز بأنه أفضل الفلاتر لمنع انخفاض الضغط.')]),
        '3': dict(name='كيس الشفط بحجم 3 لترات',
                  vol='حجم الشفط: 3 لترات عند استخدام الواحد، حتى 12 لتراً عند وضع مجموعة واحدة على القاعدة',
                  char='المواصفات: يحتوي على مسحوق هلامية، والفلتر الكاره للماء (يمنع فيض السوائل)، ويتوافق مع جميع أجهزة الشفط، ويحتوي على نظام حماية الشفط المركزي.',
                  types='أنواع فلاتر الأكياس النهائية: تنقسم الفلاتر المستخدمة في أكياس آباديس إلى ثلاثة أنواع، مما يمنع فيض السوائل.',
                  dim_d='القطر: 11 سم', dim_h='الارتفاع: 39 سم', weight='وزن المنتج: من 123 إلى 200 غرام',
                  pack='نوع التغليف: كيس نايلون', packdim='أبعاد تغليف كل منتج: 35 × 27.5 سم',
                  qty='الكمية في كل كرتون: 45 قطعة', carton='أبعاد الكرتون: 49 × 49 × 49 سم',
                  uses_h='دواعي الإستعمال',
                  uses=[('infectious', 'مكافحة العدوى'), ('surgery', 'غرفة العمليات'), ('cardio', 'القلب والأوعية الدموية'), ('men', 'قسم الرجال'), ('women', 'قسم النساء')],
                  filters=[('الفلتر الكاره للماء', 'الحيلولة دون دخول الكائنات الحية الدقيقة والبكتيريا الخطيرة إلى مخزن الشفط والبيئة المحيطة به'),
                           ('فلتر dual', 'بالإضافة إلى مزايا الفلتر الكاره للماء، فإنه يمنع انخفاض الضغط في العمليات آلة الدخان'),
                           ('الفلتر الميكانيكي', 'لا تتمتع بمزايا الفلتر الكاره للماء، ولكنه يتميز بأنه أفضل الفلاتر لمنع انخفاض الضغط.')]),
    },
}

LIPO_SVG = ('<svg viewBox="0 0 36 36" aria-hidden="true" focusable="false">'
            '<circle cx="18" cy="18" r="17" fill="#e8f3f3"/>'
            '<path d="M10 24c4-8 12-8 16 0" fill="none" stroke="#066163" stroke-width="1.8" stroke-linecap="round"/>'
            '<circle cx="18" cy="15" r="3" fill="none" stroke="#066163" stroke-width="1.8"/></svg>')


def cell_text(value, lang):
    if value in ('yes', 'no'):
        return yn(value, lang)
    if value == '×':
        return yn('no', lang)
    return f'<bdi dir="ltr">{esc(digits(value, lang))}</bdi>' if re.search(r'[A-Za-z0-9]', value) else esc(digits(value, lang))


def code_tables(lang, pfx):
    ui = UI[lang]
    rows_src = {'fa': FA_ROWS, 'en': EN_ROWS, 'ar': AR_ROWS}[lang]
    jump = []
    blocks = []
    heights = {'1': {'fa': 'ارتفاع ۱۵٫۵ سانتی‌متر', 'en': 'Height 15.5 cm', 'ar': 'الارتفاع ١٥٫٥ سم'},
               '2': {'fa': 'ارتفاع ۲۴٫۵ سانتی‌متر', 'en': 'Height 24.5 cm', 'ar': 'الارتفاع ٢٤٫٥ سم'},
               '3': {'fa': 'ارتفاع ۳۹ سانتی‌متر', 'en': 'Height 39 cm', 'ar': 'الارتفاع ٣٩ سم'}}
    names = {'1': {'fa': '۱ لیتری', 'en': '1 litre', 'ar': '١ لتر'},
             '2': {'fa': '۲ لیتری', 'en': '2 litres', 'ar': '٢ لتر'},
             '3': {'fa': '۳ لیتری', 'en': '3 litres', 'ar': '٣ لتر'}}
    for size in ('1', '2', '3'):
        jump.append(f'<a href="#s{size}"><strong>{names[size][lang]}</strong><em>{heights[size][lang]}</em></a>')
        rows = rows_src[size]
        sterile = any(r[5] is not None for r in rows)
        if lang == 'en':
            heads = ['Product code', 'Powder', 'Filter type', 'Suction bag']
            if sterile:
                heads.append('Sterile')
            heads.append('Door')
        else:
            heads = ui['heads'][:5]
            if sterile:
                heads.append(ui['heads'][5])
            heads.append(ui['heads'][6])
        th = ''.join(f'<th scope="col">{esc(h)}</th>' for h in heads)
        body = []
        cards = []
        for row in rows:
            if lang == 'en':
                code, _irc, _sz, kind, powder, ster, lidk, bag = row
                cells = [f'<bdi dir="ltr">{esc(code)}</bdi>', yn(powder, lang), cell_text(kind, lang), esc(bag)]
                pairs = list(zip(heads, [
                    f'<bdi dir="ltr">{esc(code)}</bdi>', yn(powder, lang), cell_text(kind, lang), esc(bag)
                ]))
                if sterile:
                    cells.append('—' if ster is None else yn(ster, lang))
                    pairs.append((heads[-2] if False else 'Sterile', '—' if ster is None else yn(ster, lang)))
                cells.append(lid(lidk, lang))
                pairs.append((heads[-1], lid(lidk, lang)))
                # rebuild pairs cleanly
                pairs = [(heads[0], f'<bdi dir="ltr">{esc(code)}</bdi>'),
                         (heads[1], yn(powder, lang)),
                         (heads[2], cell_text(kind, lang)),
                         (heads[3], esc(bag))]
                if sterile:
                    pairs.append((heads[4], '—' if ster is None else yn(ster, lang)))
                pairs.append((heads[-1], lid(lidk, lang)))
                cells = [v for _, v in pairs]
            else:
                code, irc, sz, kind, powder, ster, lidk = row
                pairs = [
                    (heads[0], f'<bdi dir="ltr">{esc(code)}</bdi>'),
                    (heads[1], f'<bdi dir="ltr">{esc(irc)}</bdi>'),
                    (heads[2], esc(digits(sz, lang))),
                    (heads[3], cell_text(kind, lang)),
                    (heads[4], yn(powder, lang)),
                ]
                if sterile:
                    pairs.append((heads[5], '—' if ster is None else yn(ster, lang)))
                pairs.append((heads[-1], lid(lidk, lang)))
                cells = [v for _, v in pairs]
            body.append('<tr>' + ''.join(f'<td>{c}</td>' for c in cells) + '</tr>')
            dls = ''.join(f'<div><dt>{esc(k)}</dt><dd>{v}</dd></div>' for k, v in pairs)
            cards.append(f'<dl class="code-card">{dls}</dl>')
        blocks.append(f'''<div class="size-block" id="s{size}">
      <h3>{esc(names[size][lang])}</h3>
      <div class="code-table-wrap"><table class="code-table"><thead><tr>{th}</tr></thead><tbody>{''.join(body)}</tbody></table></div>
      <div class="code-cards">{''.join(cards)}</div>
    </div>''')
        blocks.append(spec_one(size, lang, pfx))
    return f'<div class="size-jump">{"".join(jump)}</div>' + ''.join(blocks)



def size_names():
    return {
        '1': {'fa': '۱ لیتری', 'en': '1 litre', 'ar': '١ لتر'},
        '2': {'fa': '۲ لیتری', 'en': '2 litres', 'ar': '٢ لتر'},
        '3': {'fa': '۳ لیتری', 'en': '3 litres', 'ar': '٣ لتر'},
    }


def size_heights():
    return {
        '1': {'fa': 'ارتفاع ۱۵٫۵ سانتی‌متر', 'en': 'Height 15.5 cm', 'ar': 'الارتفاع ١٥٫٥ سم'},
        '2': {'fa': 'ارتفاع ۲۴٫۵ سانتی‌متر', 'en': 'Height 24.5 cm', 'ar': 'الارتفاع ٢٤٫٥ سم'},
        '3': {'fa': 'ارتفاع ۳۹ سانتی‌متر', 'en': 'Height 39 cm', 'ar': 'الارتفاع ٣٩ سم'},
    }


def iso_still(pfx, mid, theme):
    return f'{pfx}assets/img/products/cad-iso/{mid}-iso-{theme}.webp'


def iso_frame(lang, pfx, size='1'):
    ui = UI[lang]
    mid = {'1': 'p01-1l-liner', '2': 'p02-2l-liner', '3': 'p03-3l-liner'}[str(size)]
    cap = ui['iso_cap']
    stills = (
        f'<img class="iso-still iso-still-light" src="{iso_still(pfx, mid, "light")}" alt="{esc(cap)}" width="900" height="1125" loading="lazy" decoding="async">'
        f'<img class="iso-still iso-still-dark" src="{iso_still(pfx, mid, "dark")}" alt="" width="900" height="1125" loading="lazy" decoding="async" aria-hidden="true">'
    )
    return (
        f'<div class="iso-frame gal-frame" data-iso data-iso-kind="liner" data-iso-size="{size}" '
        f'data-iso-id="{mid}" data-iso-src="{pfx}3d-sketches/cad-line-sketches/models/{mid}.glb">'
        f'{stills}'
        f'<button class="iso-load" type="button">{esc(ui["iso_load"])}</button>'
        f'</div>'
    )


DASH = '—'

HYDRO_YES = {'هیدروفوبیک', 'Hydrophobic', 'كاره للماء'}
HYDRO_NO = {'×', 'مکانیکی', 'Mechanical', 'ميكانيكي'}


def hydro_flag(kind):
    if kind in HYDRO_YES:
        return 'yes'
    if kind in HYDRO_NO:
        return 'no'
    return None


def cell_or_dash(value, lang):
    if value in (None, '', '_', DASH):
        return DASH
    if value in ('yes', 'no'):
        return yn(value, lang)
    if value == '×':
        return esc('×')
    if re.search(r'[A-Za-z0-9]', value):
        return f'<bdi dir="ltr">{esc(digits(value, lang))}</bdi>'
    return esc(digits(value, lang))


def code_table_for(size, lang):
    ui = UI[lang]
    rows_src = {'fa': FA_ROWS, 'en': EN_ROWS, 'ar': AR_ROWS}[lang]
    rows = rows_src[size]
    sterile = any(r[5] is not None for r in rows)
    if lang == 'en':
        heads = ui['heads'][:6]
        if sterile:
            heads.append(ui['heads'][6])
        heads.append(ui['heads'][7])
    else:
        heads = ui['heads'][:6]
        if sterile:
            heads.append(ui['heads'][6])
    th = ''.join(f'<th scope="col">{esc(h)}</th>' for h in heads)
    body = []
    for row in rows:
        if lang == 'en':
            code, irc, _sz, kind, powder, ster, lidk, bag = row
        else:
            code, irc, _sz, kind, powder, ster, lidk = row
            bag = None
        pairs = [
            (heads[0], f'<bdi dir="ltr">{esc(code)}</bdi>'),
            (heads[1], cell_or_dash(irc, lang)),
            (heads[2], cell_or_dash(kind, lang)),
            (heads[3], cell_or_dash(hydro_flag(kind), lang)),
            (heads[4], yn(powder, lang)),
            (heads[5], lid(lidk, lang)),
        ]
        if sterile:
            ster_h = ui['heads'][6] if lang != 'en' else 'Sterile'
            pairs.append((ster_h, DASH if ster is None else yn(ster, lang)))
        if lang == 'en':
            pairs.append((heads[-1], esc(bag)))
        cells = [v for _, v in pairs]
        body.append('<tr>' + ''.join(f'<td>{c}</td>' for c in cells) + '</tr>')
    return (
        f'<div class="code-table-shell" data-table-scroll>'
        f'<div class="code-table-wrap">'
        f'<table class="code-table">'
        f'<thead><tr>{th}</tr></thead><tbody>{"".join(body)}</tbody></table>'
        f'</div>'
        f'<span class="code-table-fade" aria-hidden="true"></span>'
        f'</div>'
    )



FEATURES = {
    'fa': dict(
        filters_h='فیلترهای کیسه ساکشن',
        filters_lead='کیسه‌های ساکشن آبادیس بسته به نوع کاربرد با چند نوع فیلتر تولید می‌شوند. وظیفه‌ی همه‌ی آن‌ها جلوگیری از ورود مایعات به دستگاه ساکشن و حفظ ایمنی دستگاه است.',
        filters=[
            ('هیدروفوبیک', 'فیلتر متخلخل از جنس Porous Sintered که با رسیدن مایع به فیلتر، مسیر عبور را می‌بندد و از سرریز مایع به سمت دستگاه جلوگیری می‌کند.'),
            ('مکانیکی', 'مناسب عمل‌های جراحی با حجم بالای چربی.'),
            ('Dual', 'دارای لایه‌ای از پارچه‌ی ملت‌بلون (Meltblown) که فیلتر متخلخل را در برابر دود محافظت می‌کند و به کاهش افت فشار در مسیر مکش کمک می‌کند.'),
            ('CIF', 'نوعی فیلتر متخلخل هیدروفوبیک با فرمولاسیون ویژه، مناسب عمل‌هایی که از الکتروکوتر استفاده می‌شود و دود زیادی تولید می‌کنند.'),
        ],
        codes_note='نوع فیلتر هر کد محصول در جدول کدینگ همان سایز مشخص شده است.',
        powder_h='پودر جاذب (ژل‌کننده)',
        powder_lead='داخل کیسه، پودر جاذبی قرار دارد که مایعات و ترشحات را در تماس به ژل تبدیل می‌کند. این ویژگی:',
        powder=[
            'از ریختن و پاشیده‌شدن مایع هنگام جابه‌جایی و حمل کیسه جلوگیری می‌کند.',
            'خطر آلودگی محیط و تماس پرسنل با ترشحات را کاهش می‌دهد.',
            'دفع ایمن‌تر پسماند عفونی را ممکن می‌کند.',
        ],
        shared_h='ویژگی‌های مشترک',
        shared=[
            'کیسه‌ی نرم پلی‌اتیلن، یکبارمصرف',
            'حفاظت از ساکشن مرکزی',
            'پورت بیمار با درپوش بنددار',
            'سازگار با همه‌ی دستگاه‌های ساکشن پرتابل و مرکزی',
        ],
    ),
    'en': dict(
        filters_h='Suction-bag filters',
        filters_lead='Abadis suction bags are produced with several filter types, depending on the application. All of them keep fluids out of the suction device and protect the device.',
        filters=[
            ('Hydrophobic', 'A porous filter made of Porous Sintered material that closes the path when liquid reaches the filter and prevents overflow toward the device.'),
            ('Mechanical', 'Suitable for surgical procedures with a high volume of fat.'),
            ('Dual', 'Has a layer of Meltblown fabric that protects the porous filter against smoke and helps reduce pressure drop in the suction path.'),
            ('CIF', 'A hydrophobic porous filter with a special formulation, suitable for procedures that use an electrocautery unit and produce a large amount of smoke.'),
        ],
        codes_note='The filter type of each product code is shown in that size’s coding table.',
        powder_h='Absorbent (gelling) powder',
        powder_lead='Inside the bag is an absorbent powder that turns fluids and secretions into gel on contact. This:',
        powder=[
            'prevents liquid spilling and splashing when the bag is moved or carried.',
            'reduces the risk of environmental contamination and of staff contact with secretions.',
            'makes safer disposal of infectious waste possible.',
        ],
        shared_h='Shared features',
        shared=[
            'Soft polyethylene bag, single-use',
            'Central suction protection',
            'Patient port with a tethered cap',
            'Compatible with all portable and central suction devices',
        ],
    ),
    'ar': dict(
        filters_h='فلاتر كيس الشفط',
        filters_lead='تُنتج أكياس الشفط من آباديس بأنواع عدة من الفلاتر بحسب الاستخدام. ومهمة جميعها منع دخول السوائل إلى جهاز الشفط والحفاظ على سلامة الجهاز.',
        filters=[
            ('كاره للماء', 'فلتر مسامي من مادة Porous Sintered يغلق مسار العبور عند وصول السائل إلى الفلتر ويمنع فيض السائل نحو الجهاز.'),
            ('ميكانيكي', 'مناسب للعمليات الجراحية ذات الحجم العالي من الدهون.'),
            ('Dual', 'يحمل طبقة من قماش ملتبلون (Meltblown) تحمي الفلتر المسامي من الدخان وتساعد على تقليل انخفاض الضغط في مسار الشفط.'),
            ('CIF', 'فلتر مسامي كاره للماء بتركيبة خاصة، مناسب للعمليات التي تستخدم جهاز الكي الكهربائي وتولّد دخاناً كثيراً.'),
        ],
        codes_note='يظهر نوع فلتر كل رمز منتج في جدول الترميز الخاص بذلك الحجم.',
        powder_h='المسحوق الماص (المهلّم)',
        powder_lead='داخل الكيس مسحوق ماص يحوّل السوائل والمفرزات عند التلامس إلى هلام. وهذه الميزة:',
        powder=[
            'تمنع انسكاب السائل وتناثره عند نقل الكيس وحمله.',
            'تقلل خطر تلوث البيئة وملامسة العاملين للمفرزات.',
            'تُتيح تخلصاً أكثر أماناً من النفايات المعدية.',
        ],
        shared_h='ميزات مشتركة',
        shared=[
            'كيس بولي إيثيلين ليّن، أحادي الاستعمال',
            'حماية الشفط المركزي',
            'منفذ المريض بغطاء مربوط',
            'متوافق مع جميع أجهزة الشفط المحمولة والمركزية',
        ],
    ),
}


def features_block(lang):
    ui = UI[lang]
    f = FEATURES[lang]
    items = ''.join(
        f'<li><strong>{esc(n)}</strong> {meas(d, lang)}</li>' for n, d in f['filters']
    )
    powder = ''.join(f'<li>{esc(x)}</li>' for x in f['powder'])
    shared = ''.join(f'<li>{esc(x)}</li>' for x in f['shared'])
    return (
        f'<section class="bag-block bag-features" id="features"><div class="wrap">'
        f'<h2>{esc(ui["features_h"])}</h2>'
        f'<h3>{esc(f["filters_h"])}</h3>'
        f'<p class="bag-lead">{meas(f["filters_lead"], lang)}</p>'
        f'<ul class="feat-list">{items}</ul>'
        f'<p class="bag-note">{esc(f["codes_note"])}</p>'
        f'<h3>{esc(f["powder_h"])}</h3>'
        f'<p class="bag-lead">{esc(f["powder_lead"])}</p>'
        f'<ul class="feat-list">{powder}</ul>'
        f'<h3>{esc(f["shared_h"])}</h3>'
        f'<ul class="feat-list feat-shared">{shared}</ul>'
        f'</div></section>'
    )


SIZE_SPLIT = {
    '1': {
        'vol': {
            'fa': 'یک لیتر',
            'en': '1 liter',
            'ar': 'لتر واحد',
        },
        'series': {'fa': None, 'en': None, 'ar': None},
        'diam': {'fa': '۱۱ سانتی‌متر', 'en': '11 cm', 'ar': '١١ سم'},
        'height': {'fa': '۱۵٫۵ سانتی‌متر', 'en': '15.5 cm', 'ar': '١٥٫٥ سم'},
    },
    '2': {
        'vol': {
            'fa': '۲ لیتر در حالت تکی',
            'en': '2 Liter',
            'ar': '2 لتر عند استخدام الواحد',
        },
        'series': {
            'fa': 'تا ۸ لیتر در حالت سری یک ردیفه بر روی پایه',
            'en': None,
            'ar': 'حتى 8 لترات عند وضع مجموعة واحدة على القاعدة',
        },
        'diam': {'fa': '۱۱ سانتی‌متر', 'en': '11 cm', 'ar': '١١ سم'},
        'height': {'fa': '۲۴٫۵ سانتی‌متر', 'en': '24.5 cm', 'ar': '٢٤٫٥ سم'},
    },
    '3': {
        'vol': {
            'fa': '۳ لیتر در حالت تکی',
            'en': '3 Liters in single',
            'ar': '3 لترات عند استخدام الواحد',
        },
        'series': {
            'fa': 'تا ۱۲ لیتر در حالت سری یک ردیفه بر روی پایه',
            'en': 'up to 12 liters in single row mode on the base',
            'ar': 'حتى 12 لتراً عند وضع مجموعة واحدة على القاعدة',
        },
        'diam': {'fa': '۱۱ سانتی‌متر', 'en': '11 cm', 'ar': '١١ سم'},
        'height': {'fa': '۳۹ سانتی‌متر', 'en': '39 cm', 'ar': '٣٩ سم'},
    },
}


def size_facts(size, lang):
    ui = UI[lang]
    d = SIZE_SPLIT[size]
    cells = [
        (ui['vol_lbl'], d['vol'][lang]),
        (ui['diam_lbl'], d['diam'][lang]),
        (ui['height_lbl'], d['height'][lang]),
    ]
    if d['series'][lang]:
        cells.append((ui['series_lbl'], d['series'][lang]))
    td = ''.join(
        f'<div class="size-fact"><span class="size-fact-lbl">{esc(lab)}</span>'
        f'<b class="size-fact-val">{meas(val, lang)}</b></div>'
        for lab, val in cells
    )
    return f'<div class="size-facts" id="s{size}-size" data-sec="size"><h3>{esc(ui["size_facts_h"])}</h3><div class="size-fact-grid">{td}</div></div>'


def pack_table(size, lang):
    ui = UI[lang]
    s = SPECS[lang][size]
    labels = spec_labels(lang)
    keys = ['dim', 'dim_d', 'dim_h', 'weight', 'pack', 'packdim', 'qty', 'carton']
    rows = []
    for key in keys:
        if key not in s:
            continue
        rows.append(f'<tr><th scope="row">{esc(labels.get(key, key))}</th><td>{meas(s[key], lang)}</td></tr>')
    return (
        f'<div class="size-pack" id="s{size}-packaging" data-sec="packaging">'
        f'<h3>{esc(ui["pack_table_h"])}</h3>'
        f'<table class="pack-table"><tbody>{"".join(rows)}</tbody></table>'
        f'</div>'
    )


def sterile_block(size, lang):
    s = SPECS[lang][size]
    if not s.get('sterile_p'):
        return ''
    merits = ''.join(f'<li>{meas(m, lang)}</li>' for m in s['merits'])
    return (
        f'<div class="size-sterile" id="s{size}-sterile">'
        f'<h3>{esc(s["sterile_h"])}</h3><p>{meas(s["sterile_p"], lang)}</p>'
        f'<h3>{esc(s["merits_h"])}</h3><ul>{merits}</ul></div>'
    )


def size_picker(lang):
    ui = UI[lang]
    names = size_names()
    heights = size_heights()
    btns = []
    for i, size in enumerate(('1', '2', '3')):
        sel = 'true' if i == 0 else 'false'
        btns.append(
            f'<button class="size-pick-btn" type="button" role="tab" id="tab-s{size}" '
            f'data-size="{size}" aria-controls="s{size}" aria-selected="{sel}" tabindex="{0 if i == 0 else -1}">'
            f'<strong>{names[size][lang]}</strong><em>{heights[size][lang]}</em></button>'
        )
    inner = ''.join(btns)
    return f'<div class="size-pick size-pick-vert" role="tablist" aria-labelledby="sizes-h">{inner}</div>'


GALLERIES = {
    '1': [
        ('p1-g2.webp', False, {
            'fa': 'نمای کنار کیسه ساکشن و درب فیروزه‌ای با درپوش بنددار',
            'en': 'Side view of the suction liner and teal lid with tethered cap',
            'ar': 'منظر جانبي لكيس الشفط والغطاء الفيروزي مع غطاء مربوط',
        }),
        ('p1-g1.webp', False, {
            'fa': 'نمای زیر درب: پورت بیمار و نشان VACUUM',
            'en': 'Underside of the lid: patient port and the VACUUM mark',
            'ar': 'الجهة السفلى للغطاء: منفذ المريض وعلامة VACUUM',
        }),
        ('p1-g4.webp', False, {
            'fa': 'سه کیسه ساکشن کنار هم با شیلنگ، نصب سری',
            'en': 'Three suction liners side by side with tubing, series mounting',
            'ar': 'ثلاثة أكياس شفط جنباً إلى جنب مع الأنابيب، تركيب متسلسل',
        }),
        ('p1-g3.webp', False, {
            'fa': 'کیسه ساکشن کنار مخزن مدرج پلی‌کربنات',
            'en': 'Suction liner beside the graduated polycarbonate canister',
            'ar': 'كيس الشفط بجانب الخزان المدرج من البولي كربونات',
        }),
    ],
    '2': [
        ('p2-g1.webp', False, {
            'fa': 'درب و فیلتر کیسه ساکشن ۲ لیتری از نمای جانبی',
            'en': 'Side view of the 2-litre suction liner lid and filter',
            'ar': 'منظر جانبي لغطاء وفلتر كيس الشفط سعة ٢ لتر',
        }),
        ('p2-g2.webp', False, {
            'fa': 'کیسه ساکشن ۲ لیتری آبادیس داخل مخزن مدرج با شلنگ',
            'en': '2-litre Abadis suction liner inside the graduated canister with tubing',
            'ar': 'كيس الشفط آباديس سعة ٢ لتر داخل الخزان المدرج مع الأنابيب',
        }),
        ('p2-g3.webp', False, {
            'fa': 'اتصال شلنگ‌ها به درب کیسه ساکشن ۲ لیتری',
            'en': 'Tubing connected to the lid of the 2-litre suction liner',
            'ar': 'توصيل الأنابيب بغطاء كيس الشفط سعة ٢ لتر',
        }),
    ],
    '3': [
        ('p3-g1.webp', False, {
            'fa': 'کیسه ساکشن ۳ لیتری آبادیس در کنار مخزن مدرج',
            'en': '3-litre Abadis suction liner beside the graduated canister',
            'ar': 'كيس الشفط آباديس سعة ٣ لتر بجانب الخزان المدرج',
        }),
        ('p3-g2.webp', False, {
            'fa': 'درب کیسه ساکشن ۳ لیتری در کنار مخزن',
            'en': '3-litre suction liner lid beside the canister',
            'ar': 'غطاء كيس الشفط سعة ٣ لتر بجانب الخزان',
        }),
        ('p3-g3.webp', False, {
            'fa': 'نمای درب و مخزن مدرج ۳ لیتری',
            'en': 'Lid and graduated 3-litre canister',
            'ar': 'منظر الغطاء والخزان المدرج سعة ٣ لتر',
        }),
        ('p3-g4.webp', False, {
            'fa': 'مخزن مدرج و کیسه ساکشن ۳ لیتری از نمای افقی',
            'en': 'Graduated canister and 3-litre suction liner, horizontal view',
            'ar': 'الخزان المدرج وكيس الشفط سعة ٣ لتر من منظر أفقي',
        }),
    ],
}

def gallery_for(size, lang, pfx):
    ui = UI[lang]
    cards = []
    for name, contain, alts in GALLERIES[size]:
        alt = esc(alts[lang])
        klass = 'gal-card gal-contain' if contain else 'gal-card'
        loading = 'eager' if not cards else 'lazy'
        cards.append(
            f'<figure class="{klass}"><div class="gal-frame">'
            f'<img src="{pfx}assets/img/p/{name}" alt="{alt}" width="1200" height="800" loading="{loading}" decoding="async">'
            f'</div><figcaption>{alt}</figcaption></figure>'
        )
    cap = ui['iso_cap']
    cards.append(
        f'<figure class="gal-card gal-iso gal-contain"><div class="gal-frame-slot">'
        f'{iso_frame(lang, pfx, size)}</div><figcaption>{esc(cap)}</figcaption></figure>'
    )
    gal_o = '<div class="gal" data-gal>'
    rail = f'<div class="gal-rail">{"".join(cards)}</div>'
    nav = (
        f'<div class="gal-nav">'
        f'<button class="gal-arrow gal-prev" type="button" aria-label="{esc(ui["prev"])}">{ARROW}</button>'
        f'<div class="gal-dots"></div>'
        f'<button class="gal-arrow gal-next" type="button" aria-label="{esc(ui["next"])}">{ARROW}</button>'
        f'</div></div>'
    )
    return gal_o + rail + nav


def size_sections(lang, pfx):
    ui = UI[lang]
    chunks = []
    for i, size in enumerate(('1', '2', '3')):
        s = SPECS[lang][size]
        hidden = '' if i == 0 else ' hidden'
        facts = size_facts(size, lang)
        gal = (
            f'<div class="size-gal" id="s{size}-gallery" data-sec="gallery">'
            f'<h3>{esc(ui["gal_h"])}</h3>'
            f'{gallery_for(size, lang, pfx)}</div>'
        )
        codes = (
            f'<div class="size-codes" id="s{size}-codes" data-sec="codes">'
            f'<h3>{esc(ui["codes_h"])}</h3>'
            f'{code_table_for(size, lang)}</div>'
        )
        pack = pack_table(size, lang)
        uses = (
            f'<div class="size-uses" id="s{size}-uses" data-sec="uses">'
            f'<h3>{esc(s["uses_h"])}</h3>'
            f'<div class="uses">{render_uses(s, lang, pfx)}</div></div>'
        )
        cat = (
            f'<div class="size-catalog" id="s{size}-catalog" data-sec="catalog">'
            f'<h3>{esc(ui["catalog_h"])}</h3>'
            f'<p class="bag-lead">{esc(ui["catalog_lead"])}</p>'
            f'<a class="btn-ghost" href="{ui["catalog_href"]}" data-track="catalogue_download">{esc(ui["catalog"])}</a>'
            f'<a class="btn-ghost" href="{ui["guide_href"]}">{esc(ui["guide"])}</a>'
            f'</div>'
        )
        chunks.append(
            f'<div class="bag-panel" role="tabpanel" id="s{size}" data-size="{size}" '
            f'aria-labelledby="tab-s{size}"{hidden}>'
            f'{facts}{gal}{codes}{pack}{sterile_block(size, lang)}{uses}{cat}'
            f'</div>'
        )
    return (
        f'<section class="bag-block bag-sizes" id="sizes"><div class="wrap">'
        f'<h2 id="sizes-h">{esc(ui["sizes_h"])}</h2>'
        f'<p class="bag-lead">{meas(ui["sizes_lead"], lang)}</p>'
        f'<div class="size-stage">'
        f'{size_picker(lang)}'
        f'<div class="size-panels">{"".join(chunks)}</div>'
        f'</div></div></section>'
    )



def render_uses(s, lang, pfx):
    uses = []
    for icon, label in s['uses']:
        if icon == 'lipo':
            ic = LIPO_SVG
        else:
            ic = f'<img src="{pfx}assets/img/use/{icon}.webp" width="72" height="72" alt="" loading="lazy" decoding="async">'
        uses.append(
            f'<span class="use"><span class="use-ic" aria-hidden="true">{ic}</span>'
            f'<span class="use-lbl">{esc(digits(label, lang))}</span></span>'
        )
    return ''.join(uses)


def spec_labels(lang):
    return {
        'fa': dict(vol='حجم ساکشن', char='مشخصات', types='فیلترها', dim='ابعاد محصول', weight='وزن محصول',
                  pack='نحوه بسته بندی', packdim='ابعاد بسته بندی هر محصول', qty='تعداد در هر کارتن', carton='ابعاد کارتن'),
        'en': dict(vol='Volume', char='Characteristic', types='Types of filter', dim='Product Dimensions', weight='Product Weight',
                  pack='Packaging Type', packdim='Individual Package Dimensions', qty='Quantity per Carton', carton='Carton Dimensions'),
        'ar': dict(vol='حجم الشفط', char='المواصفات', types='أنواع الفلاتر', dim='أبعاد المنتج', dim_d='القطر', dim_h='الارتفاع',
                  weight='وزن المنتج', pack='نوع التغليف', packdim='أبعاد تغليف كل منتج', qty='الكمية في كل كرتون', carton='أبعاد الكرتون'),
    }[lang]


def spec_one(size, lang, pfx):
    ui = UI[lang]
    s = SPECS[lang][size]
    cards = []
    labels = spec_labels(lang)

    def card(title, body, span=''):
        return f'<article class="spec-card {span}"><h3>{esc(title)}</h3><p>{body}</p></article>'

    keys = ['vol', 'char', 'types', 'dim', 'dim_d', 'dim_h', 'weight']
    for key in keys:
        if key not in s:
            continue
        cards.append(card(labels.get(key, key), meas(s[key], lang), 'span-2' if key in ('char', 'types', 'vol') else ''))
    if s.get('sterile_p'):
        merits = ''.join(f'<li>{meas(m, lang)}</li>' for m in s['merits'])
        cards.append(
            f'<article class="spec-card span-2 sterile"><h3>{esc(s["sterile_h"])}</h3>'
            f'<p>{meas(s["sterile_p"], lang)}</p><h3>{esc(s["merits_h"])}</h3><ul>{merits}</ul></article>'
        )
    if lang == 'fa':
        how = 'برای مشاهده نحوه استفاده از کیسه ساکشن ها به این <a href="' + ui['guide_href'] + '">صفحه</a> مراجعه نمایید .'
        cards.append(f'<article class="spec-card span-2"><p>{how}</p></article>')
    elif ui.get('how'):
        how = 'اذهب إلى هذه <a href="' + ui['guide_href'] + '">الصفحة</a> لمعرفة كيفية استخدام أكياس الشفط.'
        cards.append(f'<article class="spec-card span-2"><p>{how}</p></article>')
    label = {'fa': 'مشخصات محصول:', 'en': 'Product Specifications', 'ar': 'مواصفات المنتج:'}[lang]
    extra = ''
    if lang == 'en' and size == '2':
        extra = '<p>2 Liter Single-Use Disposable Suction Liner Bag</p>'
    elif lang == 'en' and size == '3':
        extra = '<p>3 Liter Single-Use Disposable Suction Liner Bag</p>'
    elif lang == 'ar' and size == '1':
        extra = '<p>كيس الشفط بحجم لتر واحد</p><p>أبعاد المنتج:</p>'
    elif lang == 'ar':
        extra = '<p>أبعاد المنتج:</p>'
    return (
        f'<section class="spec-group" id="spec-{size}"><h3>{esc(digits(s["name"], lang))}</h3>'
        f'<p>{esc(label)}</p>{extra}<div class="spec-grid">{"".join(cards)}</div></section>'
    )


def uses_block(lang, pfx):
    ui = UI[lang]
    chunks = []
    for size in ('1', '2', '3'):
        s = SPECS[lang][size]
        chunks.append(
            f'<section class="use-tier" aria-labelledby="use-{size}">'
            f'<h3 id="use-{size}">{esc(digits(s["name"], lang))}</h3>'
            f'<p class="use-sub">{esc(s["uses_h"])}</p>'
            f'<div class="uses">{render_uses(s, lang, pfx)}</div></section>'
        )
    return f'''<section class="bag-block" id="uses"><div class="wrap">
    <h2>{esc(ui["uses_h"])}</h2>
    <div class="use-tiers">{"".join(chunks)}</div>
  </div></section>'''


def packaging_block(lang):
    ui = UI[lang]
    labels = spec_labels(lang)
    pack_keys = ['pack', 'packdim', 'qty', 'carton']
    chunks = []
    for size in ('1', '2', '3'):
        s = SPECS[lang][size]
        cards = []
        for key in pack_keys:
            if key not in s:
                continue
            cards.append(
                f'<article class="spec-card"><h3>{esc(labels[key])}</h3><p>{meas(s[key], lang)}</p></article>'
            )
        chunks.append(
            f'<section class="pack-tier" aria-labelledby="pack-{size}">'
            f'<h3 id="pack-{size}">{esc(digits(s["name"], lang))}</h3>'
            f'<div class="spec-grid pack-grid">{"".join(cards)}</div></section>'
        )
    return f'''<section class="bag-block" id="packaging"><div class="wrap">
    <h2>{esc(ui["packaging_h"])}</h2>
    <div class="pack-tiers">{"".join(chunks)}</div>
  </div></section>'''

def filters_block(lang, pfx="../../"):
    ui = UI[lang]
    intro = SPECS[lang]['1']['types']
    cards = [f'<article class="spec-card span-2"><p>{meas(intro, lang)}</p></article>']
    filt = SPECS[lang]['1'].get('filters')
    if filt:
        lis = ''.join(f'<li><strong>{meas(n, lang)}</strong>{meas(d, lang)}</li>' for n, d in filt)
        fh = {'en': 'Filter Name', 'ar': 'اسم الفلتر'}[lang]
        if lang == 'en':
            lis = '<li><strong>Description</strong></li>' + lis
        if lang == 'ar':
            lis = '<li><strong>مواصفات الفلتر</strong></li>' + lis
        cards.append(f'<article class="spec-card span-2"><h3>{esc(fh)}</h3><ol class="filter-list">{lis}</ol></article>')
    h2 = esc(ui['filters_h'])
    grid = ''.join(cards)
    return (
        f'<section class="bag-block" id="filters"><div class="wrap">'
        f'<h2>{h2}</h2>'
        f'<div class="spec-grid">{grid}</div>'
        f'</div></section>'
    )


def main_html(lang, pfx):
    ui = UI[lang]
    home, home_h, mid, mid_h, here = ui['crumb']
    beats = ''.join(
        f'<p class="beat" data-a="{a}" data-b="{b}">{esc(t)}</p>' for a, b, t in ui['beats']
    )
    nav = ''.join(f'<a href="#{i}">{esc(digits(n, lang))}</a>' for i, n in ui['nav'])
    stats = ''.join(
        f'<div class="stat"><b class="stat-val">{esc(digits(a, lang))}</b>'
        f'<span class="stat-lbl">{esc(digits(b, lang))}</span></div>'
        for a, b in ui['stats']
    )
    export = ''
    if lang == 'en':
        export = f'<a class="btn-ghost" href="{ui["export_href"]}">{esc(ui["export"])}</a>'
    still = f'{pfx}assets/img/products/3d/p02-cinematic-v12-still-studio.webp'
    return (
        f'<main id="main">'
        f'<div class="cin-track" id="film" data-cin-root data-cin-floors="hero" data-tone="dark" data-cin-module="{pfx}assets/js/p02-cinematic-page.js?v={V}">'
        f'<div class="cin-stage"><div class="cin-view">'
        f'<canvas aria-hidden="true"></canvas>'
        f'<img class="cin-still" src="{still}" width="900" height="1338" alt="{esc(ui["still_alt"])}" fetchpriority="high" decoding="async">'
        f'<div class="cin-bar" aria-hidden="true"></div>'
        f'</div>'
        f'<div class="cin-copy"><h1>{esc(ui["h1"])}</h1><div class="cin-beats">{beats}</div></div>'
        f'</div></div>'
        f'<nav class="bag-sub" aria-label="{esc(ui["specs"])}">'
        f'<div class="wrap bag-sub-row">'
        f'<div class="bag-sub-scroller">{nav}</div>'
        f'<button class="bag-sub-hint" type="button" aria-label="{esc(ui["next"])}">{ARROW}</button>'
        f'<a class="btn-primary" href="{ui["quote_href"]}">{esc(ui["quote"])}</a>'
        f'</div></nav>'
        f'<section class="bag-block bag-intro" id="intro"><div class="wrap">'
        f'<h2>{esc(ui["intro_h"])}</h2>'
        f'<p class="bag-lead">{esc(ui["intro_p"])}</p>'
        f'</div></section>'
        f'{features_block(lang)}'
        f'{size_sections(lang, pfx)}'
        f'<section class="bag-close" id="order"><div class="wrap"><div class="panel">'
        f'<h2>{esc(ui["close_h"])}</h2>'
        f'<p>{esc(ui["close_p"])}</p>'
        f'<div class="cta-row">'
        f'<a class="btn-primary" href="{ui["quote_href"]}">{esc(ui["quote"])}</a>'
        f'<a class="btn-ghost" href="tel:+982192001017">{esc(ui["call"])}</a>'
        f'<a class="btn-ghost" href="{ui["catalog_href"]}" data-track="catalogue_download">{esc(ui["catalog"])}</a>'
        f'{export}'
        f'<a class="btn-ghost" href="{ui["guide_href"]}">{esc(ui["guide"])}</a>'
        f'</div></div></div></section>'
        f'</main>'
    )



PAGES = {
    'fa': ('products/suction-bag/index.html', '../../'),
    'en': ('en/products/suction-bag/index.html', '../../../'),
    'ar': ('arabic/كيس-الشفط/index.html', '../../'),
}


def retitle(html, lang):
    ui = UI[lang]
    html = re.sub(r'<title>.*?</title>', f'<title>{esc(ui["title"])}</title>', html, count=1)
    html = re.sub(r'(<meta name="description" content=")[^"]*(")', lambda m: m.group(1) + esc(ui['desc']) + m.group(2), html, count=1)
    html = re.sub(r'(<meta property="og:title" content=")[^"]*(")', lambda m: m.group(1) + esc(ui['title']) + m.group(2), html, count=1)
    html = re.sub(r'(<meta property="og:description" content=")[^"]*(")', lambda m: m.group(1) + esc(ui['desc']) + m.group(2), html, count=1)
    return html


def rebuild(lang):
    rel, pfx = PAGES[lang]
    path = SITE / rel
    html_s = path.read_text(encoding='utf-8')
    html_s = retitle(html_s, lang)
    html_s = html_s.replace(
        'Abadis disposable suction bags: 1, 2 and 3 litres, with the current product codes.',
        UI['en']['desc'],
    )
    html_s = re.sub(r'\n?<link rel="stylesheet" href="[^"]+/(?:factory-3d|product-3d-pilot|suction-bag-apple)\.css[^"]*">', '', html_s)
    html_s = re.sub(r'suction-bag-page\.css\?v=[^"]+', f'suction-bag-page.css?v={V}', html_s)
    html_s = re.sub(r'suction-bag-ui\.js\?v=[^"]+', f'suction-bag-ui.js?v={V}', html_s)
    if 'suction-bag-page.css' not in html_s:
        html_s = html_s.replace('</head>', f'<link rel="stylesheet" href="{pfx}assets/css/suction-bag-page.css?v={V}">\n</head>', 1)
    if 'importmap' not in html_s:
        imap = ('<script type="importmap">{"imports":{"three":"' + pfx +
                'assets/vendor/three/build/three.module.js","three/addons/":"' + pfx +
                'assets/vendor/three/examples/jsm/"}}</script>\n')
        html_s = html_s.replace('</head>', imap + '</head>', 1)
    if lang == 'fa':
        html_s = html_s.replace(
            'hreflang="en" href="../../products/suction-bag/"',
            'hreflang="en" href="https://abadis-med.com/en/products/suction-bag/"',
        )
    html_s = re.sub(r'<body[^>]*>', '<body class="page-bag" data-bag-rebuild="v12">', html_s, count=1)
    main = main_html(lang, pfx)
    html_s = re.sub(r'<main id="main">.*?</main>', lambda m: main, html_s, count=1, flags=re.S)
    html_s = re.sub(r'\n?<script type="module">.*?</script>', '', html_s, flags=re.S)
    html_s = re.sub(r'\n?<script type="module" src="[^"]*suction-bag-1l[^"]*"[^>]*>\s*</script>', '', html_s)
    if 'suction-bag-ui.js' not in html_s:
        html_s = html_s.replace('</body>', f'<script src="{pfx}assets/js/suction-bag-ui.js?v={V}" defer></script>\n</body>', 1)
    # drop a second h1 if the shell ever had one outside main — it should not
    path.write_text(html_s, encoding='utf-8')
    print(lang, 'h1', html_s.count('<h1>'), 'apple', 'suction-bag-1l-apple' in html_s, 'bytes', path.stat().st_size)


if __name__ == '__main__':
    for lang in ('fa', 'en', 'ar'):
        rebuild(lang)
