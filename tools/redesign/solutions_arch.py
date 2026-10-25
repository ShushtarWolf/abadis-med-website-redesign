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
        uneven='این پنج عنوان وضعیتی یکسانی ندارند. سه حوزه نخست بر محصولات موجود متکی‌اند؛ حوزه مراقبت راه هوایی متناسب با محصولات واقعاً قابل عرضه فعال است و فناوری مواد و PVA در بخش «در حال توسعه» معرفی می‌شود.',
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
    ),
    'en': dict(
        h1='Abadis Products & Solutions',
        sub='From specialised suction products to innovative solutions for safer, more efficient care.',
        crumb_p='Products', crumb_s='Solutions',
        by_p='By product', by_s='By solution',
        keep='Current categories stay', new_path='New customer path',
        note='One product can belong to more than one solution. A filter, for example, is used in the suction system and in contamination control, but its canonical product page is built only once.',
        uneven='These five titles are not in the same state. The first three rely on products already on sale. Airway care is active only for the products that can actually be supplied. Materials technology and PVA stay in the In Development section.',
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
    ),
    'ar': dict(
        h1='منتجات وحلول آباديس',
        sub='من منتجات الشفط المتخصصة إلى حلول مبتكرة لرعاية أكثر أماناً وكفاءة.',
        crumb_p='المنتجات', crumb_s='الحلول',
        by_p='حسب المنتج', by_s='حسب الحل',
        keep='يُحفظ التصنيف الحالي', new_path='مسار جديد للعميل',
        note='يمكن أن يظهر منتج واحد في أكثر من حل. الفلتر مثلاً يُستخدم في نظام الشفط وفي السيطرة على التلوث، لكن صفحة تعريفه الأساسية تُبنى مرة واحدة.',
        uneven='هذه العناوين الخمسة ليست في الوضع نفسه. المجالات الثلاثة الأولى تعتمد على منتجات قائمة. العناية بالطريق الهوائي تُفعَّل بقدر المنتجات القابلة للعرض فعلاً، وتقنية المواد وPVA تبقى في قسم «قيد التطوير».',
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
    ),
}

CATALOG = [
    dict(slug='suction-bag', photo='suction-bag',
         href=L('products/suction-bag/', 'products/suction-bag/', 'كيس-الشفط/'),
         title=L('کیسه‌های ساکشن', 'Suction bags', 'أكياس الشفط'),
         sub=L('مدل‌های ۱، ۲ و ۳ لیتری', '1, 2 and 3 litre models', 'موديلات ١ و٢ و٣ لتر')),
    dict(slug='suction-tube', photo='suction-tube',
         href=L('products/suction-tube/', 'suction-tube/', 'أنبوب-الشفط/'),
         title=L('ساکشن تیوب', 'Suction tube', 'أنبوب الشفط'),
         sub=L('لوله‌ها و رابط‌های ساکشن', 'Tubes and suction connectors', 'الأنابيب ووصلات الشفط')),
    dict(slug='filters', photo='filters',
         href=L('products/filters/', 'products/filters/', 'الفلتر/'),
         title=L('فیلترها', 'Filters', 'الفلاتر'),
         sub=L('انواع فیلترهای حفاظتی', 'Protective filter types', 'أنواع الفلاتر الواقية')),
    dict(slug='canister', photo='canister',
         href=L('products/canister/', 'products/canisters/', 'خزانات/'),
         title=L('مخازن', 'Canisters', 'الخزانات'),
         sub=L('مخازن و سیستم‌های دیواری', 'Canisters and wall systems', 'الخزانات والأنظمة الجدارية')),
    dict(slug='stand', photo='stand',
         href=L('products/stand/', 'products/base-and-holder/', 'تثبیت/'),
         title=L('پایه و نگهدارنده', 'Stands and holders', 'الحوامل'),
         sub=L('ترولی، پایه و گیره‌ها', 'Trolley, stand and clamps', 'ترولي وقاعدة ومشابك')),
    dict(slug='connectors', photo='connectors',
         href=L('products/connectors/', 'products/connections/', 'الوصلات/'),
         title=L('اتصالات', 'Connectors', 'الوصلات'),
         sub=L('کانکتورها، رگولاتورها و شیرها', 'Connectors, regulators and valves', 'الوصلات والمنظمات والصمامات')),
    dict(slug='other', photo='other',
         href=L('products/other/', 'products/other-products/', 'منتجات-اخری/'),
         title=L('سایر محصولات', 'Other products', 'منتجات أخرى'),
         sub=L('رسیور و محصولات تخصصی مرتبط', 'Receiver and related specialist products', 'وعاء التجميع والمنتجات التخصصية المرتبطة')),
]
BY_SLUG = {c['slug']: c for c in CATALOG}

PHOTO = {
    'suction-bag': 'assets/img/c/611f0398754f-640.webp',
    'stand': 'assets/img/c/90d179b67447-640.webp',
    'filters': 'assets/img/c/ad713458f652-640.webp',
    'suction-tube': 'assets/img/c/92b676038309-900.webp',
    'canister': 'assets/img/c/38a87bcfaf85-640.webp',
    'connectors': 'assets/img/c/9b6630cc8eaa-640.webp',
    'other': 'assets/img/c/a75210c08710-640.webp',
    'mesvak': 'assets/img/c/a75210c08710-900.webp',
    'negahdarande': 'assets/img/c/d3d867132a50-900.webp',
    'receiver': 'assets/img/c/928b52ffc716-900.webp',
    'sdv': 'assets/img/c/d981ab7fae6e-900.webp',
    'paye': 'assets/img/c/227665fb9960-900.webp',
    'anti': 'assets/img/filters/anti-1-t.webp',
    'rgl': 'assets/img/c/9b6630cc8eaa-640.webp',
}

# slug, hash, status, optional title override, optional photo key
def P(slug, hash='', status='order', title=None, photo=None):
    return dict(slug=slug, hash=hash, status=status, title=title, photo=photo)

SOLS = [
    dict(
        slug='fluid-management', future=False,
        title=L('مدیریت مایعات و ترشحات', 'Fluid management', 'إدارة السوائل والإفرازات'),
        sub=L('جمع‌آوری ایمن و کارآمد مایعات بیمارستانی', 'Safe, efficient collection of hospital fluids', 'جمع آمن وفعّال للسوائل في المستشفى'),
        problem=L(
            'نیاز مراکز درمانی به ساکشن مطمئن، ایمن و متناسب با شرایط استفاده. در این راهکار مسئله، جمع‌آوری مایعات و ترشحات حین عمل یا مراقبت است، بدون شست‌وشوی مکرر مخزن و بدون بازماندن مدار.',
            'Care centres need suction that is reliable, safe and matched to how it is used. Here the problem is collecting fluids and secretions during a procedure or during care, without repeatedly washing the canister and without leaving the circuit open.',
            'تحتاج المراكز العلاجية إلى شفط موثوق وآمن ومناسب لظروف الاستخدام. المسألة هنا جمع السوائل والإفرازات أثناء الإجراء أو الرعاية، من دون غسل الخزان مراراً ومن دون ترك الدارة مفتوحة.'),
        intro=L(
            'سیستم ساکشن آبادیس در این راهکار کیسه یکبارمصرف را داخل مخزن می‌نشاند، تیوب و اتصالات مدار بیمار را به همان مجموعه می‌رسانند و درِ کیسه با فیلتر هیدروفوبیک از سرریز به سمت خلأ محافظت می‌کند. هر جزء صفحه اصلی خودش را دارد.',
            'In this solution the Abadis suction system seats a disposable liner inside the canister. Tubing and connectors bring the patient circuit to that set, and the bag lid with its hydrophobic filter protects the vacuum side from overflow. Each part keeps its own canonical page.',
            'في هذا الحل يضع نظام شفط آباديس كيساً ذا استعمال واحد داخل الخزان. الأنبوب والوصلات يوصلان دارة المريض إلى المجموعة نفسها، وغطاء الكيس بفلتره الكاره للماء يحمي جهة الخلاء من الفيض. كل جزء يحتفظ بصفحته الأساسية.'),
        apps=L(
            ['اتاق عمل (OR)', 'مراقبت‌های ویژه (ICU)', 'اورژانس (ER)', 'بخش‌های بستری، جایی که حجم مایع و دفعات تعویض کیسه با مدل ۱، ۲ یا ۳ لیتری جور درمی‌آید'],
            ['Operating room (OR)', 'Intensive care (ICU)', 'Emergency (ER)', 'Inpatient wards, where fluid volume and how often the bag is changed match the 1, 2 or 3 litre model'],
            ['غرفة العمليات (OR)', 'العناية المركزة (ICU)', 'الطوارئ (ER)', 'أقسام الإقامة، حيث يوافق حجم السائل وتكرار تبديل الكيس موديل ١ أو ٢ أو ٣ لتر']),
        adv=L(
            ['ایمنی مدار بسته و کاهش تماس با مایع', 'نصب روی پایه دیواری یا پرتابل، تکی یا سری', 'مدیریت مایعات با پودر ژل‌کننده داخل کیسه', 'حذف بخش بزرگی از شست‌وشوی مخزن'],
            ['A closed circuit and less contact with fluid', 'Fits a wall stand or a portable stand, single or in series', 'Fluid management with the gelling powder inside the bag', 'Removes most canister washing'],
            ['دارة مغلقة وتلامس أقل مع السائل', 'يُركَّب على قاعدة جدارية أو محمولة، مفرداً أو على التسلسل', 'إدارة السوائل بمسحوق التهلّم داخل الكيس', 'إلغاء الجزء الأكبر من غسل الخزان']),
        economy=L(
            'محاسبه‌گر صرفه‌جویی و نسخه عملی آن، گردش‌کار کیسه یکبارمصرف را با شست‌وشوی مخزن چندبارمصرف مقایسه می‌کنند: آب، ماده شوینده، زمان نیروی انسانی و انرژی. عدد به تعداد تخت، نوع بخش و الگوی مصرف همان مرکز بستگی دارد.',
            'The savings calculator and its practical version compare a disposable-liner workflow with washing a reusable canister: water, detergent, staff time and energy. The figure depends on that centre’s beds, department and usage.',
            'تقارن حاسبة التوفير ونسختها العملية مسار الكيس ذي الاستعمال الواحد بغسل الخزان المتعدد الاستعمال: الماء والمنظّف ووقت الطاقم والطاقة. الرقم يعتمد على أسرّة ذلك المركز وقسمه ونمط استهلاكه.'),
        packs=L(
            [('پکیج اتاق عمل پرتابل', 'ترولی، کیسه ساکشن، تیوب و اتصالات'),
             ('پکیج ساکشن دیواری', 'مخزن یا ساکشن دیواری، کیسه و فیلتر درِ کیسه'),
             ('پکیج سری / آبشاری', 'چند کیسه روی یک پایه، برای حجم بالاتر در یک نوبت')],
            [('Portable operating-room pack', 'Trolley, suction bag, tube and connectors'),
             ('Wall suction pack', 'Canister or wall suction, bag and the bag-lid filter'),
             ('Series / cascade pack', 'Several bags on one stand, for a higher volume in one session')],
            [('حزمة غرفة عمليات محمولة', 'ترولي وكيس شفط وأنبوب ووصلات'),
             ('حزمة شفط جداري', 'خزان أو شفط جداري وكيس وفلتر غطاء الكيس'),
             ('حزمة تسلسلية', 'عدة أكياس على قاعدة واحدة لحجم أعلى في الجلسة نفسها')]),
        parts=[P('suction-bag'), P('canister'), P('suction-tube'), P('connectors'),
               P('other', 'receiver', 'order', L('رسیور پزشکی', 'Kidney dish', 'وعاء كلوي'), 'receiver')],
    ),
    dict(
        slug='hospital-suction-systems', future=False,
        title=L('سیستم‌های ساکشن بیمارستانی', 'Hospital suction systems', 'أنظمة الشفط في المستشفى'),
        sub=L('راهکارهای ثابت، دیواری و پرتابل', 'Fixed, wall and portable solutions', 'حلول ثابتة وجدارية ومحمولة'),
        problem=L(
            'نیاز مراکز درمانی به ساکشن مطمئن، ایمن و متناسب با شرایط استفاده. اینجا مسئله، چیدن خود سیستم است: خروجی دیواری، دستگاه پرتابل، یا ترکیبی از هر دو، با پایه‌ای که مخزن و کیسه را سر جایش نگه می‌دارد.',
            'Care centres need suction that is reliable, safe and matched to how it is used. Here the problem is the system itself: a wall outlet, a portable unit, or both, with a stand that holds the canister and the bag in place.',
            'تحتاج المراكز العلاجية إلى شفط موثوق وآمن ومناسب لظروف الاستخدام. المسألة هنا تركيب النظام نفسه: مخرج جداري أو جهاز محمول أو الاثنان معاً، مع قاعدة تُبقي الخزان والكيس في مكانهما.'),
        intro=L(
            'اجزای آبادیس در این راهکار کنار هم یک سیستم قابل سفارش می‌سازند: پایه یا ترولی، گیره دیواری، مخزن، کیسه، تیوب، رگولاتور و فیلتر حفاظتی. صفحه هیچ‌کدام تکرار نمی‌شود؛ از اینجا فقط به صفحه اصلی همان قطعه می‌روید.',
            'Together the Abadis parts make an orderable system: stand or trolley, wall clamp, canister, bag, tube, regulator and protective filter. None of those pages is copied; this page only links to each part’s canonical page.',
            'تكوّن قطع آباديس معاً نظاماً قابلاً للطلب: قاعدة أو ترولي، مشبك جداري، خزان، كيس، أنبوب، منظّم وفلتر واقٍ. لا تُنسخ أي صفحة؛ من هنا تنتقل فقط إلى الصفحة الأساسية لكل قطعة.'),
        apps=L(
            ['اتاق عمل با ست پرتابل', 'ICU با ساکشن دیواری', 'اورژانس', 'بخش‌هایی که هم خروجی دیواری دارند و هم به ترولی سیار نیاز دارند'],
            ['Operating room with a portable set', 'ICU with wall suction', 'Emergency', 'Wards that have a wall outlet and also need a mobile trolley'],
            ['غرفة العمليات بطقم محمول', 'العناية المركزة بشفط جداري', 'الطوارئ', 'أقسام فيها مخرج جداري وتحتاج أيضاً إلى ترولي متحرك']),
        adv=L(
            ['یک زبان مشترک بین ست دیواری و ست پرتابل', 'نصب و جابه‌جایی با ترولی و گیره', 'حفاظت مدار با فیلتر و کیسه', 'امکان سری کردن کیسه روی همان پایه'],
            ['One shared set of parts for wall and portable kits', 'Install and move with the trolley and clamp', 'Circuit protection from the filter and the bag', 'Bags can be placed in series on the same stand'],
            ['لغة واحدة من القطع للطقم الجداري والمحمول', 'تركيب ونقل بالترولي والمشبك', 'حماية الدارة بالفلتر والكيس', 'إمكانية وضع الأكياس على التسلسل على القاعدة نفسها']),
        economy=L(
            'صرفه‌جویی این راهکار همان فرض محاسبه‌گر است: کمتر شستن مخزن، وقتی کیسه یکبارمصرف جای تخلیه و شست‌وشو را می‌گیرد. انتخاب دیواری یا پرتابل هزینه تجهیزات را عوض می‌کند و در فرم فروش جدا می‌شود.',
            'The saving assumption is the one in the calculator: less canister washing once a disposable bag replaces emptying and washing. Choosing wall or portable changes the equipment cost and is separated in the sales form.',
            'فرضية التوفير هي فرضية الحاسبة: غسل أقل للخزان حين يحل الكيس ذو الاستعمال الواحد محل التفريغ والغسل. اختيار الجداري أو المحمول يغيّر كلفة التجهيز ويُفصَل في نموذج المبيعات.'),
        packs=L(
            [('پکیج اتاق عمل پرتابل', 'ترولی، مخزن، کیسه، تیوب و اتصالات'),
             ('پکیج ساکشن دیواری ICU', 'ساکشن دیواری، کیسه، فیلتر و رگولاتور'),
             ('پکیج ترکیبی', 'خروجی دیواری به‌علاوه ترولی سیار برای جابه‌جایی بین تخت‌ها')],
            [('Portable operating-room pack', 'Trolley, canister, bag, tube and connectors'),
             ('ICU wall-suction pack', 'Wall suction, bag, filter and regulator'),
             ('Combined pack', 'A wall outlet plus a mobile trolley for moving between beds')],
            [('حزمة غرفة عمليات محمولة', 'ترولي وخزان وكيس وأنبوب ووصلات'),
             ('حزمة شفط جداري للعناية', 'شفط جداري وكيس وفلتر ومنظّم'),
             ('حزمة مشتركة', 'مخرج جداري مع ترولي متحرك للتنقل بين الأسرّة')]),
        parts=[P('stand', 'paye', 'order', L('پایه ساکشن پرتابل (ترولی)', 'Portable suction trolley', 'قاعدة الشفط المحمولة'), 'paye'),
               P('canister', 'sdv', 'order', L('ساکشن دیواری', 'Wall suction', 'الشفط الجداري'), 'sdv'),
               P('suction-bag'), P('filters'), P('connectors', 'rgl', 'order', L('رگولاتور', 'Regulator', 'المنظّم'), 'rgl'),
               P('other', 'splashvac', 'soon', L('مکش سطحی چندمنظوره (Splash-Vac)', 'Splash-Vac', 'Splash-Vac'), 'other')],
    ),
    dict(
        slug='contamination-control', future=False,
        title=L('کنترل آلودگی و حفاظت از سیستم ساکشن', 'Contamination control and suction-system protection', 'السيطرة على التلوث وحماية نظام الشفط'),
        sub=L('فیلتراسیون و حفاظت از مدار وکیوم', 'Filtration and protection of the vacuum circuit', 'الترشيح وحماية دارة الخلاء'),
        problem=L(
            'نیاز مراکز درمانی به ساکشن مطمئن، ایمن و متناسب با شرایط استفاده. در این راهکار مسئله، رسیدن مایع یا آلودگی به مدار وکیوم و به ساکشن مرکزی است.',
            'Care centres need suction that is reliable, safe and matched to how it is used. Here the problem is liquid or contamination reaching the vacuum circuit and the central suction.',
            'تحتاج المراكز العلاجية إلى شفط موثوق وآمن ومناسب لظروف الاستخدام. المسألة هنا وصول سائل أو تلوث إلى دارة الخلاء والشفط المركزي.'),
        intro=L(
            'فیلتر آنتی‌باکتریال، فیلتر قطع‌کننده جریان و فیلتر متخلخل کنار فیلتر هیدروفوبیک درِ کیسه کار می‌کنند. هر فیلتر صفحه خودش را در خانواده فیلترها دارد و کیسه هم فقط یک آدرس دارد.',
            'The antibacterial filter, the flow-stopper filter and the porous filter work beside the hydrophobic filter in the bag lid. Each filter has its own place on the filters page, and the bag still has a single address.',
            'يعمل الفلتر المضاد للبكتيريا وفلتر قطع التدفق والفلتر المسامي إلى جانب الفلتر الكاره للماء في غطاء الكيس. لكل فلتر موضعه في صفحة الفلاتر، وللكيس عنوان واحد.'),
        apps=L(
            ['اتاق عمل', 'ICU و هر جا چند مصرف‌کننده به یک خط وکیوم وصل‌اند', 'اورژانس', 'بخش‌هایی که ساکشن مرکزی باید از سرریز مایع محافظت شود'],
            ['Operating room', 'ICU and anywhere several users share one vacuum line', 'Emergency', 'Wards where central suction must be protected from liquid overflow'],
            ['غرفة العمليات', 'العناية المركزة وأي موضع يشترك فيه عدة مستخدمين في خط خلاء واحد', 'الطوارئ', 'أقسام يجب فيها حماية الشفط المركزي من فيض السائل']),
        adv=L(
            ['حفاظت از پمپ و خط ساکشن مرکزی', 'قطع جریان وقتی مایع به فیلتر مسدودشونده می‌رسد', 'کاهش باز شدن مدار برای تخلیه', 'انتخاب فیلتر بر اساس همین صفحات محصول، نه یک صفحه تکراری'],
            ['Protects the pump and the central suction line', 'Stops flow when liquid reaches the shutoff filter', 'The circuit is opened less often for emptying', 'The filter is chosen from these product pages, not from a duplicate page'],
            ['حماية المضخة وخط الشفط المركزي', 'قطع التدفق حين يصل السائل إلى فلتر الإيقاف', 'فتح الدارة أقل لتفريغها', 'يُختار الفلتر من صفحات المنتج هذه لا من صفحة مكررة']),
        economy=L(
            'اثر اقتصادی این راهکار در محاسبه‌گر از مسیر کاهش شست‌وشو و کاهش مواجهه دیده می‌شود، نه از یک عدد جدا برای خود فیلتر. فرض‌ها همان فرض‌های صفحه محاسبه‌گر و نسخه عملی آن است.',
            'In the calculator the economic effect shows up as less washing and less exposure, not as a separate figure for the filter alone. The assumptions are those of the calculator and its practical version.',
            'يظهر الأثر الاقتصادي في الحاسبة عبر غسل أقل وتعرّض أقل، لا كرقم منفصل للفلتر وحده. الفرضيات هي فرضيات الحاسبة ونسختها العملية.'),
        packs=L(
            [('حفاظت خط وکیوم', 'فیلتر آنتی‌باکتریال به‌اضافه کیسه با فیلتر هیدروفوبیک'),
             ('قطع سرریز', 'فیلتر قطع‌کننده جریان روی همان مدار'),
             ('مدار با فیلتر متخلخل', 'جایی که مشخصات فنی فیلتر متخلخل با دستگاه جور است')],
            [('Vacuum-line protection', 'Antibacterial filter plus a bag with a hydrophobic filter'),
             ('Overflow shutoff', 'A flow-stopper filter on the same circuit'),
             ('Porous-filter circuit', 'Where the porous filter’s specification matches the unit')],
            [('حماية خط الخلاء', 'فلتر مضاد للبكتيريا مع كيس بفلتر كاره للماء'),
             ('إيقاف الفيض', 'فلتر قطع التدفق على الدارة نفسها'),
             ('دارة بفلتر مسامي', 'حيث توافق مواصفات الفلتر المسامي الجهاز')]),
        parts=[P('filters', 'anti', 'order', L('فیلتر آنتی‌باکتریال', 'Antibacterial filter', 'الفلتر المضاد للبكتيريا'), 'anti'),
               P('filters', 'ght', 'order', L('فیلتر قطع‌کننده جریان', 'Flow-stopper filter', 'فلتر قطع التدفق'), 'filters'),
               P('filters', 'mot', 'order', L('فیلتر متخلخل', 'Porous filter', 'الفلتر المسامي'), 'filters'),
               P('suction-bag')],
    ),
    dict(
        slug='airway-care', future=False,
        title=L('ایمنی و مراقبت از راه هوایی', 'Airway safety and care', 'سلامة العناية بالطريق الهوائي'),
        sub=L('محصولات تخصصی مراقبت از بیمار', 'Specialist products for patient care', 'منتجات متخصصة للعناية بالمريض'),
        problem=L(
            'نیاز مراکز درمانی به ساکشن مطمئن، ایمن و متناسب با شرایط استفاده. این راهکار فقط به اندازه محصولاتی فعال است که واقعاً عرضه می‌شوند: مسواک ساکشن و نگهدارنده لوله تراشه، به‌اضافه تیوبی که مدار را وصل می‌کند.',
            'Care centres need suction that is reliable, safe and matched to how it is used. This solution is active only for what can actually be supplied: the suction brush and the endotracheal-tube holder, plus the tube that connects the circuit.',
            'تحتاج المراكز العلاجية إلى شفط موثوق وآمن ومناسب لظروف الاستخدام. هذا الحل نشط فقط بقدر ما يُعرض فعلاً: فرشاة الشفط وحامل أنبوب القصبة، مع الأنبوب الذي يصل الدارة.'),
        intro=L(
            'مسواک ساکشن از راه تیوب به دستگاه ساکشن وصل می‌شود. نگهدارنده لوله تراشه لوله را در وضعیت مناسب دهان نگه می‌دارد. هر دو روی صفحه سایر محصولات می‌مانند و اینجا فقط به همان آدرس لینک می‌شوند.',
            'The suction brush connects to the suction unit through the tube. The tube holder keeps the endotracheal tube in place at the mouth. Both stay on the other-products page; this page only links there.',
            'تتصل فرشاة الشفط بجهاز الشفط عبر الأنبوب. يُبقي حامل الأنبوب أنبوب القصبة في وضع مناسب في الفم. كلاهما يبقى في صفحة المنتجات الأخرى؛ هذه الصفحة تربط إلى ذلك العنوان فقط.'),
        apps=L(
            ['ICU و مراقبت از بیمار اینتوبه', 'اورژانس', 'اتاق عمل، وقتی بهداشت دهان یا تثبیت لوله تراشه لازم است', 'بخش‌های بستری با همین دو قلم'],
            ['ICU and care of an intubated patient', 'Emergency', 'Operating room, when oral care or tube fixation is required', 'Inpatient wards, limited to these two items'],
            ['العناية المركزة ورعاية المريض المنبَّب', 'الطوارئ', 'غرفة العمليات حين تلزم عناية الفم أو تثبيت أنبوب القصبة', 'أقسام الإقامة بهذين الصنفين']),
        adv=L(
            ['بهداشت دهان همراه با ساکشن، بدون یک صفحه محصول تازه', 'تثبیت لوله تراشه با بند قابل تنظیم', 'کاهش زخم لب و دهان، همان‌طور که در صفحه نگهدارنده آمده است', 'سفارش فقط برای اقلام قابل عرضه'],
            ['Oral care with suction, without a new product page', 'Tube fixation with an adjustable strap', 'Less injury to the lip and mouth, as the holder page already states', 'Orders only for items that can be supplied'],
            ['عناية بالفم مع الشفط من دون صفحة منتج جديدة', 'تثبيت الأنبوب بحزام قابل للضبط', 'أذى أقل للشفة والفم، كما هو مذكور في صفحة الحامل', 'الطلب فقط للأصناف القابلة للعرض']),
        economy=L(
            'این راهکار عدد صرفه‌جویی مستقل ندارد. اگر کیسه ساکشن هم در همان مرکز مصرف شود، فرض آب و شست‌وشو را باید در محاسبه‌گر دید، نه در این صفحه.',
            'This solution has no saving figure of its own. If the centre also uses suction bags, the water and washing assumptions belong in the calculator, not on this page.',
            'ليس لهذا الحل رقم توفير مستقل. إذا كان المركز يستخدم أكياس الشفط أيضاً، ففرضيات الماء والغسل مكانها الحاسبة لا هذه الصفحة.'),
        packs=L(
            [('پکیج مراقبت راه هوایی', 'مسواک ساکشن، نگهدارنده لوله تراشه و ساکشن تیوب'),
             ('فقط بهداشت دهان', 'مسواک ساکشن به‌اضافه تیوب'),
             ('فقط تثبیت لوله', 'نگهدارنده لوله تراشه')],
            [('Airway-care pack', 'Suction brush, endotracheal-tube holder and suction tube'),
             ('Oral care only', 'Suction brush plus tube'),
             ('Tube fixation only', 'Endotracheal-tube holder')],
            [('حزمة العناية بالطريق الهوائي', 'فرشاة شفط وحامل أنبوب القصبة وأنبوب شفط'),
             ('عناية الفم فقط', 'فرشاة الشفط مع الأنبوب'),
             ('تثبيت الأنبوب فقط', 'حامل أنبوب القصبة')]),
        parts=[P('other', 'mesvak', 'order', L('مسواک ساکشن', 'Suction brush', 'فرشاة الشفط'), 'mesvak'),
               P('other', 'negahdarande', 'order', L('نگهدارنده لوله تراشه', 'Endotracheal tube holder', 'حامل أنبوب القصبة'), 'negahdarande'),
               P('suction-tube')],
    ),
    dict(
        slug='waste-management-pva', future=True,
        title=L('کنترل آلودگی و مدیریت پسماند', 'Contamination control and waste management', 'السيطرة على التلوث وإدارة النفايات'),
        sub=L('فناوری مواد و محصولات آینده', 'Materials technology and future products', 'تقنية المواد والمنتجات المستقبلية'),
        problem=L(
            'نیاز مراکز درمانی به ساکشن مطمئن، ایمن و متناسب با شرایط استفاده، در افق دورتر به جنس خود ظرف و پسماند عفونی هم مربوط می‌شود. محصولات PVA هنوز قابل سفارش نیستند.',
            'Care centres need suction that is reliable, safe and matched to how it is used. Further out, that also concerns the material of the container and infectious waste. PVA products are not orderable yet.',
            'تحتاج المراكز العلاجية إلى شفط موثوق وآمن ومناسب لظروف الاستخدام. على مدى أبعد يخص ذلك أيضاً مادة الوعاء والنفايات المعدية. منتجات PVA ليست قابلة للطلب بعد.'),
        intro=L(
            'آنچه امروز برای مدیریت پسماند مایع عرضه می‌شود همان کیسه ساکشن یکبارمصرف است. فناوری مواد و PVA در حال تحقیق و توسعه است و صفحه محصول جداگانه‌ای ندارد؛ مدخلش روی سایر محصولات به همین راهکار برمی‌گردد.',
            'What is supplied today for liquid-waste handling is the disposable suction bag. Materials technology and PVA are in research and development and have no separate product page; the entry on Other products points back here.',
            'ما يُعرض اليوم للتعامل مع النفايات السائلة هو كيس الشفط ذو الاستعمال الواحد. تقنية المواد وPVA قيد البحث والتطوير ولا صفحة منتج منفصلة لهما؛ المدخل في المنتجات الأخرى يعود إلى هذا الحل.'),
        apps=L(
            ['هنوز به‌عنوان بسته قابل سفارش برای OR یا ICU معرفی نمی‌شود', 'موضوع تحقیق: پسماند عفونی و مواد زیست‌تخریب‌پذیر', 'تا زمان عرضه، جمع‌آوری مایع با کیسه ساکشن فعلی انجام می‌شود'],
            ['Not yet offered as an orderable pack for the OR or ICU', 'Research topic: infectious waste and biodegradable materials', 'Until it is released, fluid collection stays with the current suction bag'],
            ['لا يُقدَّم بعد كحزمة قابلة للطلب لغرفة العمليات أو العناية', 'موضوع البحث: النفايات المعدية والمواد القابلة للتحلل', 'حتى الطرح، يبقى جمع السوائل بكيس الشفط الحالي']),
        adv=L(
            ['جدا ماندن وعده آینده از فهرست قابل سفارش', 'لینک به کیسه فعلی برای نیاز امروز مرکز', 'یک مدخل PVA، بدون ساختن آدرس محصول تکراری'],
            ['The future promise stays off the orderable list', 'A link to the current bag for what the centre needs today', 'One PVA entry, without a duplicate product address'],
            ['يبقى وعد المستقبل خارج قائمة القابل للطلب', 'رابط إلى الكيس الحالي لحاجة المركز اليوم', 'مدخل PVA واحد من دون عنوان منتج مكرر']),
        economy=L(
            'برای PVA عدد صرفه‌جویی منتشر نشده است. هر برآوردی برای کیسه فعلی باید از محاسبه‌گر و نسخه عملی آن خوانده شود، با همان فرض آب، شوینده و زمان نیروی انسانی.',
            'No saving figure has been published for PVA. Any estimate for the current bag has to be read from the calculator and its practical version, with the same water, detergent and staff-time assumptions.',
            'لم يُنشر رقم توفير لـ PVA. أي تقدير للكيس الحالي يُقرأ من الحاسبة ونسختها العملية، بفرضيات الماء والمنظّف ووقت الطاقم نفسها.'),
        packs=L(
            [('بسته قابل سفارش نیست', 'تا پیش از اتمام تحقیق و توسعه، پیکربندی PVA برای فروش تعریف نشده است'),
             ('نیاز امروز', 'کیسه ساکشن ۱، ۲ و ۳ لیتری از صفحه اصلی خودش'),
             ('ادامه کار', 'درخواست مشاوره تا واحد فروش موضوع را در مسیر توسعه ثبت کند')],
            [('No orderable pack', 'Until research and development finishes, no PVA configuration is defined for sale'),
             ('What is needed today', 'The 1, 2 and 3 litre suction bag, from its own canonical page'),
             ('Next step', 'A consult request so sales can log the topic on the development path')],
            [('لا حزمة قابلة للطلب', 'قبل انتهاء البحث والتطوير لا تهيئة PVA معرّفة للبيع'),
             ('حاجة اليوم', 'كيس الشفط ١ و٢ و٣ لتر من صفحته الأساسية'),
             ('الخطوة التالية', 'طلب استشارة حتى تسجّل المبيعات الموضوع في مسار التطوير')]),
        parts=[P('other', 'pva', 'rnd', L('محصولات PVA (مواد پلیمری زیست‌تخریب‌پذیر)', 'PVA products (biodegradable polymers)', 'منتجات PVA (بوليمرات قابلة للتحلل)'), None),
               P('suction-bag')],
    ),
]
BY_SOL = {s['slug']: s for s in SOLS}

RELATED = {
    'suction-bag': ['fluid-management', 'hospital-suction-systems'],
    'stand': ['hospital-suction-systems'],
    'filters': ['contamination-control', 'hospital-suction-systems'],
    'canister': ['fluid-management', 'hospital-suction-systems'],
    'suction-tube': ['hospital-suction-systems', 'fluid-management'],
    'connectors': ['hospital-suction-systems', 'fluid-management'],
    'other': ['airway-care', 'waste-management-pva'],
}

CATALOGUE = 'https://abadis-med.com/wp-content/uploads/2024/12/کاتالوگ-جامع-آبادیس.pdf'
CONTACT = L('contact/', 'contact-us/', 'اتصل-بنا/')


def status_for(tab_id):
    return 'soon' if tab_id == 'splashvac' else 'order'


def badge(lang, status):
    ui = UI[lang]
    label = {'order': ui['order'], 'soon': ui['soon'], 'rnd': ui['rnd'], 'future': ui['future']}[status]
    return f'<span class="ps-badge ps-badge--{status}">{esc(label)}</span>'


def tab_anchor(tab_id, title, lang):
    return (f'<a href="#{esc(tab_id)}" data-ptab="{esc(tab_id)}">{esc(title)}'
            f'{badge(lang, status_for(tab_id))}</a>')


def icons(p, kind):
    # Alireza finalists: M5 for «بر اساس محصول», R9 for «بر اساس راهکار».
    light, dark = ('M5-teal.svg', 'M5-dark.svg') if kind == 'product' else ('R9-teal.svg', 'R9-dark.svg')
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


def solution_main(p, lang, sol):
    ui = UI[lang]
    future = badge(lang, 'future') if sol['future'] else f'<span class="ps-state">{esc(ui["active"])}</span>'
    cta = (f'<div class="ps-actions"><a class="btn btn-primary" href="{href(p, lang, CONTACT[lang])}">{esc(ui["quote"])}</a>'
           f'<button class="btn btn-ghost" type="button" data-sol-open>{esc(ui["config"])}</button></div>')
    hero = page_hero(p, [(ui['crumb_s'], href(p, lang, 'solutions/' if lang != 'ar' else 'الحلول/')), (sol['title'][lang], None)],
                     esc(sol['title'][lang]), esc(sol['sub'][lang]),
                     meta=future + cta, lang=lang)
    philosophy = PHIL.theme_html(lang, sol['slug'], lambda h: href(p, lang, h))
    parts = ''.join(_part(p, lang, part) for part in sol['parts'])
    packs = ''.join(f'<li><strong>{esc(a)}</strong> — {esc(b)}</li>' for a, b in sol['packs'][lang])
    econ_links = (f'<div class="doc-links"><a href="{href(p, lang, "calculator/")}">{esc(ui["s_econ"])}</a>'
                  f'<a href="{p}dial-practical/">dial-practical</a></div>')
    sales = (f'<p>{esc(ui["sales_p"])}</p>{cta}'
             f'<div class="doc-links"><a href="{CATALOGUE}" target="_blank" rel="noopener" data-track="catalogue_download">{esc(ui["cat"])}</a>'
             f'<a href="{href(p, lang, CONTACT[lang])}">{esc(ui["quote"])}</a></div>')
    blocks = [
        ('problem', ui['s_problem'], f'<p>{esc(sol["problem"][lang])}</p>'),
        ('intro', ui['s_intro'], f'<p>{esc(sol["intro"][lang])}</p>'),
        ('parts', ui['s_parts'], f'<div class="ps-parts">{parts}</div>'),
        ('apps', ui['s_apps'], _ul(sol['apps'][lang])),
        ('adv', ui['s_adv'], _ul(sol['adv'][lang])),
        ('econ', ui['s_econ'], f'<p>{esc(sol["economy"][lang])}</p>{econ_links}'),
        ('pick', ui['s_pick'], f'<ul>{packs}</ul>'),
        ('sales', ui['s_sales'], sales),
    ]
    body = ''.join(
        f'<section class="section sol-sec{" section--alt" if i % 2 else ""}" id="{key}"><div class="wrap"><h2>{esc(title)}</h2>{inner}</div></section>'
        for i, (key, title, inner) in enumerate(blocks))
    return hero + '\n' + philosophy + '\n' + body + '\n' + configurator(lang)


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
    legend = (f'<p class="ps-legend"><span>{esc(ui["legend"])}</span>{badge(lang, "order")}'
              f'{badge(lang, "soon")}{badge(lang, "rnd")}</p>')
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
    hero = page_hero(p, [(crumb, None)], esc(ui['h1']), esc(ui['sub']), lang=lang)
    philosophy = ''
    if opening == 'solution':
        philosophy = '\n' + PHIL.hub_html(lang, lambda h: href(p, lang, h))
    return hero + philosophy + '\n  <section class="section" id="browse"><div class="wrap">\n' + architecture(
        p, lang, default='solution' if opening == 'solution' else 'product', layers=False
    ) + '\n  </div></section>'


def home_section(p, lang):
    ui = UI[lang]
    hub = href(p, lang, 'solutions/' if lang != 'ar' else 'الحلول/') + '#phil'
    tease = PHIL.teaser_html(lang, hub)
    return (f'  <section class="section ps-block" id="products"><div class="wrap">'
            f'<div class="section-head reveal"><h2>{esc(ui["h1"])}</h2><p>{esc(ui["sub"])}</p></div>'
            f'{tease}'
            + architecture(p, lang, default='product', layers=False)
            + '</div></section>')


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
        for sol in SOLS:
            rel = rel_t.format(slug=sol['slug'])
            can = can_t.format(slug=sol['slug'])
            fa = f'solutions/{sol["slug"]}/'
            desc = sol['sub'][lang]
            html = page(p, sol['slug'], sol['title'][lang], desc, solution_main(p, lang, sol),
                        lang=lang, fa_path=fa, canonical_path=can)
            written.append(_write(rel, html))
        # hub
        if lang == 'fa':
            rel, p, can, fa = 'solutions/index.html', '../', 'solutions/', 'solutions/'
        elif lang == 'en':
            rel, p, can, fa = 'en/solutions/index.html', '../../', 'en/solutions/', 'solutions/'
        else:
            rel, p, can, fa = 'arabic/الحلول/index.html', '../../', 'arabic/الحلول/', 'solutions/'
        html = page(p, 'solutions', ui['h1'], ui['sub'], hub_main(p, lang, opening='solution'),
                    lang=lang, fa_path=fa, canonical_path=can)
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
    """Header dropdown slugs/paths must match CATALOG / SOLS (guards products↔solutions swap)."""
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


def stamp_nav_html(html, rel):
    m = re.search(r'(<nav class="nav" id="mainNav"[^>]*>)(.*?)(</nav>)', html, re.S)
    if not m or 'data-ps-nav="products"' in m.group(2):
        return html, False
    lang = _lang_of(html)
    found = NAV_PAT[lang].search(m.group(2))
    if not found:
        return html, False
    cur = infer_cur(rel)
    if not cur and 'aria-current="page"' in found.group(0):
        cur = 'products'
    inner = m.group(2)[:found.start()] + nav_pair(found.group(1), lang, cur) + m.group(2)[found.end():]
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
    ('products/other/index.html', 'fa', 'other', '../../'),
    ('en/products/suction-bag/index.html', 'en', 'suction-bag', '../../../'),
    ('en/suction-tube/index.html', 'en', 'suction-tube', '../../'),
    ('en/products/filters/index.html', 'en', 'filters', '../../../'),
    ('en/products/canisters/index.html', 'en', 'canister', '../../../'),
    ('en/products/base-and-holder/index.html', 'en', 'stand', '../../../'),
    ('en/products/connections/index.html', 'en', 'connectors', '../../../'),
    ('en/products/other-products/index.html', 'en', 'other', '../../../'),
    ('arabic/كيس-الشفط/index.html', 'ar', 'suction-bag', '../../'),
    ('arabic/أنبوب-الشفط/index.html', 'ar', 'suction-tube', '../../'),
    ('arabic/الفلتر/index.html', 'ar', 'filters', '../../'),
    ('arabic/خزانات/index.html', 'ar', 'canister', '../../'),
    ('arabic/تثبیت/index.html', 'ar', 'stand', '../../'),
    ('arabic/الوصلات/index.html', 'ar', 'connectors', '../../'),
    ('arabic/منتجات-اخری/index.html', 'ar', 'other', '../../'),
]


def stamp_product_html(html, p, lang, slug):
    html = inject_h1_badge(html, lang, 'order')
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


def stamp_site():
    nav_n = foot_n = 0
    missed = []
    for path in SITE.rglob('*.html'):
        rel = str(path.relative_to(SITE))
        raw = path.read_text(encoding='utf-8')
        html, hit = stamp_nav_html(raw, rel)
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
.nav-caret { width: 0; height: 0; border-inline: 4px solid transparent; border-top: 5px solid currentColor; opacity: .75; }
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


def main():
    install_icons()
    install_nav_fallback()
    pages = write_solution_pages()
    hubs = write_product_hubs()
    homes = stamp_home()
    products = stamp_product_pages()
    nav_n, foot_n, missed = stamp_site()
    print(f'solutions {len(pages)} hubs {hubs} homes {homes} product-pages {products} nav {nav_n} footer {foot_n} missed {len(missed)}')
    for rel in missed[:20]:
        print(' miss', rel)


if __name__ == '__main__':
    main()
