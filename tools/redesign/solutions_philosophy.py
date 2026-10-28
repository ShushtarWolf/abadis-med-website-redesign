"""Solutions philosophy (Alireza, Oct 2026).

FA wording follows the boss PDF. EN and AR mirror the same structure.
The three themes are the three solution pages.
"""
from lib import esc

def T(fa, en, ar):
    return {'fa': fa, 'en': en, 'ar': ar}


def _sol(lang, slug):
    folder = 'solutions/' if lang != 'ar' else 'الحلول/'
    return f'{folder}{slug}/'


def _hub(lang):
    return 'solutions/' if lang != 'ar' else 'الحلول/'


CALC = T('calculator/', 'calculator/', 'الحوسبة/')
GREEN = T('customers/', 'our-customers/', 'customers/')
SDGS = T('sdgs/', 'sdgs/', '~sdgs/')
OTHER = T('products/other/', 'products/other-products/', 'منتجات-اخری/')
ORAL = T('products/oral-hygiene/', 'products/oral-hygiene/', 'نظافة-الفم/')
CAT_HREF = {
    'fa': [
        'products/suction-bag/', 'products/canister/', 'products/stand/', 'products/connectors/',
        'products/filters/', 'products/suction-tube/', 'products/oral-hygiene/', 'products/other/',
    ],
    'en': [
        'products/suction-bag/', 'products/canisters/', 'products/base-and-holder/', 'products/connections/',
        'products/filters/', 'suction-tube/', 'products/oral-hygiene/', 'products/other-products/',
    ],
    'ar': [
        'كيس-الشفط/', 'خزانات/', 'تثبیت/', 'الوصلات/',
        'الفلتر/', 'أنبوب-الشفط/', 'نظافة-الفم/', 'منتجات-اخری/',
    ],
}

PILLARS = [
    T('محصولات', 'Products', 'المنتجات'),
    T('راهکارها', 'Solutions', 'الحلول'),
    T('کاربردها', 'Applications', 'الاستخدامات'),
    T('نوآوری', 'Innovation', 'الابتكار'),
]
PILLAR_TEXT = [
    T('ما چه چیزی تولید و عرضه می‌کنیم؟',
      'What do we manufacture and supply?',
      'ماذا ننتج ونعرض؟'),
    T('این محصولات در کنار هم چه مسئله‌ای را حل می‌کنند؟',
      'Which problem do these products solve together?',
      'أي مسألة تحلّها هذه المنتجات معاً؟'),
    T('این راهکارها در کدام بخش‌های بیمارستان استفاده می‌شوند؟',
      'Which hospital departments use these solutions?',
      'في أي أقسام المستشفى تُستخدم هذه الحلول؟'),
    T('آبادیس برای حل مسئله آینده روی چه فناوری‌هایی کار می‌کنند؟',
      'Which technologies is Abadis working on to solve the problem of the future?',
      'على أي تقنيات تعمل آباديس لحل مسألة المستقبل؟'),
]

PATHS_H = T('تفاوت این دو بخش', 'The difference between these two sections', 'الفرق بين هذين القسمين')
QUESTIONS_H = T('چهار پرسش کلیدی', 'Four key questions', 'أربعة أسئلة أساسية')
PATHS_HEAD = [
    T('ویژگی', 'Aspect', 'البند'),
    T('محصولات', 'Products', 'المنتجات'),
    T('راهکارها', 'Solutions', 'الحلول'),
]
PATHS = [
    (T('رویکرد', 'Approach', 'النهج'),
     T('کاربردی و تجاری', 'Applied and commercial', 'تطبيقي وتجاري'),
     T('مفهومی و راهبردی', 'Conceptual and strategic', 'مفهومي واستراتيجي')),
    (T('تصاویر', 'Images', 'الصور'),
     T('عکس واقعی محصول', 'Real product photos', 'صور حقيقية للمنتج'),
     T('تصاویر مفهومی، علمی و سیستمی', 'Conceptual, scientific and system images', 'صور مفهومية وعلمية ونظامية')),
    (T('محتوا', 'Content', 'المحتوى'),
     T('مشخصات، مدل‌ها، کاتالوگ', 'Specifications, models, catalogue', 'المواصفات والموديلات والكتالوج'),
     T('مسئله، فناوری، مزیت و نتیجه', 'Problem, technology, advantage and result', 'المسألة والتقنية والميزة والنتيجة')),
    (T('لحن', 'Tone', 'النبرة'),
     T('دقیق و فنی', 'Precise and technical', 'دقيق وفني'),
     T('الهام‌بخش و علمی', 'Inspiring and scientific', 'ملهم وعلمي')),
    (T('مسیر کاربر', 'User path', 'مسار المستخدم'),
     T('استعلام و سفارش', 'Enquiry and order', 'الاستعلام والطلب'),
     T('کشف راهکار و سپس مشاهده محصولات', 'Discover the solution, then see the products', 'اكتشاف الحل ثم مشاهدة المنتجات')),
    (T('آینده شرکت', 'Company future', 'مستقبل الشركة'),
     T('محصولات آماده عرضه', 'Products ready to supply', 'منتجات جاهزة للعرض'),
     T('محصولات موجود و مسیر توسعه', 'Existing products and the development path', 'المنتجات القائمة ومسار التطوير')),
]

INTRO_KICK = T('مقدمه', 'Introduction', 'مقدمة')
INTRO_H = T('راهکارهای تخصصی آبادیس', 'Abadis specialised solutions', 'حلول آباديس التخصصية')
INTRO_SUB = T(
    'راهکارهای تخصصی برای مراقبت ایمن‌تر و کارآمدتر',
    'Specialised solutions for safer, more efficient care',
    'حلول تخصصية لرعاية أكثر أماناً وكفاءة')
INTRO = [
    T('در آبادیس باور داریم آینده صنعت تجهیزات پزشکی تنها در تولید محصولات بیشتر نیست، بلکه در توسعه راهکارهایی است که به نیازهای واقعی مراکز درمانی پاسخ دهند.',
      'At Abadis we believe the future of the medical-equipment industry is not only in making more products, but in developing solutions that answer the real needs of care centres.',
      'في آباديس نؤمن أن مستقبل صناعة التجهيزات الطبية ليس في إنتاج مزيد من المنتجات فحسب، بل في تطوير حلول تستجيب للحاجات الحقيقية للمراكز العلاجية.'),
    T('ما با تکیه بر دانش مهندسی، تجربه صنعتی، فناوری‌های نوین و شناخت فرایندهای بیمارستانی، در مسیر ارائه راهکارهایی گام برمی‌داریم که به افزایش ایمنی بیماران و کادر درمان، کنترل عفونت‌های بیمارستانی، بهبود بهره‌وری و حفاظت از محیط زیست کمک کنند.',
      'Drawing on engineering knowledge, industrial experience, new technologies and an understanding of hospital processes, we are building solutions that help raise the safety of patients and care teams, control hospital infections, improve efficiency and protect the environment.',
      'بالاعتماد على المعرفة الهندسية والخبرة الصناعية والتقنيات الجديدة وفهم العمليات في المستشفى، نعمل على حلول تساعد في رفع سلامة المرضى وطاقم الرعاية، والسيطرة على عدوى المستشفيات، وتحسين الكفاءة، وحماية البيئة.'),
    T('این رویکرد، از مدیریت مایعات و ترشحات بیمارستانی آغاز شده و امروز به حوزه‌های جدیدی از مراقبت تخصصی و فناوری مواد گسترش می‌یابد.',
      'This approach began with hospital fluid and secretion management, and today it extends into new fields of specialist care and materials technology.',
      'بدأ هذا النهج من إدارة السوائل والإفرازات في المستشفى، ويمتد اليوم إلى مجالات جديدة من الرعاية التخصصية وتقنية المواد.'),
]

MAP_COL = [
    T('محصولات مرتبط', 'Related products', 'المنتجات المرتبطة'),
    T('راهکار', 'Solution', 'الحل'),
    T('صفحه', 'Page', 'الصفحة'),
]
MAP_H = T('گروه‌بندی راهکارها', 'How the solutions are grouped', 'تجميع الحلول')
CAT_H = T('گروه‌بندی کلی محصولات', 'Overall product grouping', 'التجميع العام للمنتجات')
MAP_NOTE = T(
    'هر یک از سه راهکار صفحه خودش را دارد.',
    'Each of the three solutions has its own page.',
    'لكل حل من الحلول الثلاثة صفحته.')

# theme key -> solution slug
THEME_PAGES = {
    'fluid': ['fluid-management'],
    'airway': ['airway-care'],
    'waste': ['waste-management-pva'],
    'other': ['waste-management-pva'],
}

THEMES = [
    dict(
        key='fluid',
        title=T('مدیریت مایعات و ترشحات', 'Fluid and secretion management', 'إدارة السوائل والإفرازات'),
        products=T(
            'کیسه ساکشن یکبارمصرف، مخزن ساکشن، اتصالات، پایه و نگهدارنده، ساکشن تیوب، فیلتر',
            'Disposable suction liner bag, suction canister, connectors, stand and holder, suction tube, filter',
            'كيس شفط ذو استعمال واحد، خزان الشفط، الوصلات، القاعدة والحامل، أنبوب الشفط، الفلتر'),
    ),
    dict(
        key='airway',
        title=T('ایمنی و مراقبت از راه هوایی (بهداشت دهان)', 'Airway safety and care (oral hygiene)', 'سلامة الطريق الهوائي والعناية به (صحة الفم)'),
        products=T('براش و فیکسر', 'Brush and fixer', 'الفرشاة والمثبّت'),
    ),
    dict(
        key='waste',
        title=T('کنترل آلودگی و مدیریت پسماند', 'Contamination control and waste management', 'السيطرة على التلوث وإدارة النفايات'),
        products=T('کیسه زباله PVA', 'PVA waste bag', 'كيس نفايات PVA'),
    ),
]

PRODUCT_ROWS = [
    T('کیسه ساکشن یکبارمصرف', 'Disposable suction liner bag', 'كيس شفط ذو استعمال واحد'),
    T('مخزن ساکشن', 'Suction canister', 'خزان الشفط'),
    T('پایه و نگهدارنده‌ها', 'Stands and holders', 'القواعد والحاملات'),
    T('اتصالات', 'Connectors', 'الوصلات'),
    T('فیلتر', 'Filter', 'الفلتر'),
    T('ساکشن تیوب', 'Suction tube', 'أنبوب الشفط'),
    T('بهداشت دهان', 'Oral hygiene', 'صحة الفم'),
    T('سایر محصولات', 'Other products', 'منتجات أخرى'),
]
PRODUCT_THEME = ['fluid', 'fluid', 'fluid', 'fluid', 'fluid', 'fluid', 'airway', 'other']

PAGE_NAME = {
    'fluid-management': T('مدیریت مایعات و ترشحات بیمارستانی', 'Hospital Fluid & Secretion Management', 'إدارة السوائل والإفرازات في المستشفى'),
    'airway-care': T('ایمنی و مراقبت از راه هوایی', 'Airway Safety & Care', 'سلامة الطريق الهوائي والعناية به'),
    'waste-management-pva': T('کنترل آلودگی و مدیریت پسماند', 'Contamination Control & Waste Management', 'السيطرة على التلوث وإدارة النفايات'),
}

NOTES_H = T('نکات', 'Notes', 'ملاحظات')

FLUID = dict(
    title=T('۱. مدیریت مایعات و ترشحات بیمارستانی',
            '1. Hospital fluid and secretion management',
            '١. إدارة السوائل والإفرازات في المستشفى'),
    en='Hospital Fluid & Secretion Management',
    lead=T('از جمع‌آوری مایعات تا مدیریت یکپارچه سیستم ساکشن',
           'From fluid collection to an integrated suction system',
           'من جمع السوائل إلى إدارة متكاملة لنظام الشفط'),
    body=[
        T('مدیریت مایعات و ترشحات بیمارستانی، یکی از فرایندهای حساس در حفظ بهداشت، ایمنی و کارایی مراکز درمانی است. تماس با مایعات آلوده، شست‌وشوی تجهیزات چندبارمصرف، مصرف منابع و مدیریت پسماند، از چالش‌های این حوزه به شمار می‌روند.',
          'Managing hospital fluids and secretions is one of the sensitive processes in keeping a care centre hygienic, safe and efficient. Contact with contaminated fluids, washing reusable equipment, the use of resources and waste handling are among the challenges of this field.',
          'إدارة السوائل والإفرازات في المستشفى من العمليات الحساسة في حفظ النظافة والسلامة وكفاءة المراكز العلاجية. التلامس مع السوائل الملوثة، وغسل التجهيزات المتعددة الاستعمال، واستهلاك الموارد، وإدارة النفايات، من تحديات هذا المجال.'),
        T('آبادیس به‌عنوان نخستین و بزرگ‌ترین تولیدکننده کیسه ساکشن یکبارمصرف در ایران، با رویکردی پیشگام در توسعه این محصول، مسیر خود را برای ارائه راهکاری جامع در مدیریت مایعات بیمارستانی آغاز کرد.',
          'Abadis, the first and largest manufacturer of disposable suction liner bags in Iran, took a pioneering approach to this product and began its path toward a complete solution for hospital fluid management.',
          'آباديس، بصفتها أول وأكبر منتج لكيس الشفط ذي الاستعمال الواحد في إيران، وبمنهج ريادي في تطوير هذا المنتج، بدأت مسارها لتقديم حل شامل لإدارة السوائل في المستشفى.'),
        T('این مسیر با تکمیل سیستم ساکشن، توسعه انواع فیلتر، مخازن، رگولاتورها، پایه و ترولی و سایر تجهیزات مرتبط ادامه یافت تا اجزای مختلف فرایند جمع‌آوری مایعات در قالب یک سیستم هماهنگ در اختیار مراکز درمانی قرار گیرند.',
          'The path continued by completing the suction system and developing filters, canisters, regulators, stands, trolleys and other related equipment, so that the parts of fluid collection are available to care centres as one coordinated system.',
          'استمر هذا المسار باكتمال نظام الشفط وتطوير أنواع الفلاتر والخزانات والمنظمات والقواعد والترولي وسائر التجهيزات المرتبطة، حتى صارت أجزاء جمع السوائل في متناول المراكز العلاجية ضمن نظام واحد منسجم.'),
    ],
    axes_h=T('راهکارهای آبادیس در این حوزه بر چهار اصل استوارند:',
             'Abadis solutions in this field rest on four principles:',
             'تستند حلول آباديس في هذا المجال إلى أربعة مبادئ:'),
    axes=[
        (T('ایمنی', 'Safety', 'السلامة'),
         T('کمک به کاهش تماس کادر درمان با مایعات و ترشحات آلوده و پشتیبانی از فرایندهای کنترل عفونت.',
           'Helping reduce the care team’s contact with contaminated fluids and secretions, and supporting infection-control processes.',
           'المساعدة في تقليل تلامس طاقم الرعاية مع السوائل والإفرازات الملوثة، ودعم عمليات السيطرة على العدوى.')),
        (T('کارایی', 'Efficiency', 'الكفاءة'),
         T('تسهیل جمع‌آوری مایعات، کاهش مراحل آماده‌سازی و شست‌وشو و بهبود فرایندهای کاری.',
           'Making fluid collection easier, cutting preparation and washing steps, and improving work processes.',
           'تيسير جمع السوائل، وتقليل مراحل التجهيز والغسل، وتحسين إجراءات العمل.')),
        (T('بهره‌وری اقتصادی', 'Economic efficiency', 'الجدوى الاقتصادية'),
         T('کمک به مدیریت هزینه‌های عملیاتی، منابع انسانی و مصرف تجهیزات.',
           'Helping manage operating costs, staff time and equipment use.',
           'المساعدة في إدارة التكاليف التشغيلية والموارد البشرية واستهلاك التجهيزات.')),
        (T('توسعه پایدار', 'Sustainable development', 'التنمية المستدامة'),
         T('کاهش نیاز به شست‌وشوی مخازن و فراهم‌کردن امکان صرفه‌جویی در مصرف آب، متناسب با شرایط استفاده.',
           'Less need to wash canisters, and a way to save water, matched to how the system is used.',
           'تقليل الحاجة إلى غسل الخزانات، وإتاحة التوفير في استهلاك الماء بما يناسب ظروف الاستخدام.')),
    ],
    after=[
        T('آبادیس با توسعه این راهکارها، در تلاش است مدیریت مایعات بیمارستانی را از یک فعالیت صرفاً عملیاتی به فرایندی ایمن‌تر، کارآمدتر و قابل ارزیابی تبدیل کند.',
          'By developing these solutions, Abadis is working to turn hospital fluid management from a purely operational task into a process that is safer, more efficient and open to evaluation.',
          'بتطوير هذه الحلول، تسعى آباديس إلى نقل إدارة السوائل في المستشفى من نشاط تشغيلي بحت إلى عملية أكثر أماناً وكفاءة وقابلة للتقييم.'),
    ],
    ctas=[
        ('hub', T('کشف راهکارهای مدیریت مایعات', 'Discover fluid-management solutions', 'اكتشاف حلول إدارة السوائل')),
        ('calc', T('محاسبه صرفه‌جویی آب و هزینه', 'Calculate water and cost savings', 'حساب التوفير في الماء والكلفة')),
    ],
    notes=[
        (T('مسئله', 'Problem', 'المسألة'),
         T('جمع‌آوری مایعات و ترشحات، با چالش تماس با آلودگی، شست‌وشوی مخازن و صرف زمان و منابع همراه است.',
           'Collecting fluids and secretions brings contact with contamination, canister washing, and the use of time and resources.',
           'جمع السوائل والإفرازات يصاحبه تلامس مع التلوث وغسل الخزانات واستهلاك الوقت والموارد.')),
        (T('راهکار آبادیس', 'Abadis solution', 'حل آباديس'),
         T('ارائه یک سیستم هماهنگ برای جمع‌آوری و انتقال ایمن‌تر مایعات، متناسب با نیاز هر بخش.',
           'A coordinated system for safer collection and transfer of fluids, matched to each department.',
           'تقديم نظام منسجم لجمع السوائل ونقلها بصورة أكثر أماناً، بما يناسب حاجة كل قسم.')),
        (T('اجزای راهکار', 'Components', 'مكوّنات الحل'),
         T('کیسه ساکشن، مخزن، تیوب، فیلتر هیدروفوبیک، استاپ‌فلو، رگولاتور، پایه و ترولی.',
           'Suction bag, canister, tube, hydrophobic filter, stop-flow, regulator, stand and trolley.',
           'كيس الشفط، الخزان، الأنبوب، الفلتر الكاره للماء، إيقاف التدفق، المنظّم، القاعدة والترولي.')),
        (T('کاربردها', 'Applications', 'الاستخدامات'),
         T('اتاق عمل، مراقبت‌های ویژه، اورژانس و سایر بخش‌های نیازمند ساکشن، متناسب با مشخصات تجهیزات.',
           'Operating room, intensive care, emergency and other departments that need suction, matched to the equipment.',
           'غرفة العمليات، والعناية المركزة، والطوارئ، وسائر الأقسام التي تحتاج إلى الشفط، بما يناسب مواصفات التجهيز.')),
        (T('مزیت‌ها', 'Advantages', 'المزايا'),
         T('کاهش تماس با ترشحات، سهولت تعویض کیسه و کاهش نیاز به شست‌وشوی مخزن.',
           'Less contact with secretions, easier bag changes, and less need to wash the canister.',
           'تلامس أقل مع الإفرازات، وسهولة تبديل الكيس، وحاجة أقل إلى غسل الخزان.')),
        (T('ارزش اقتصادی', 'Economic value', 'القيمة الاقتصادية'),
         T('امکان کاهش مصرف آب و مواد ضدعفونی‌کننده و زمان آماده‌سازی؛ قابل برآورد با محاسبه‌گر آبادیس و شرایط واقعی هر مرکز.',
           'A possible reduction in water, disinfectant and preparation time; it can be estimated with the Abadis calculator and each centre’s real conditions.',
           'إمكانية تقليل استهلاك الماء ومواد التعقيم وزمن التجهيز؛ ويمكن تقديره بحاسبة آباديس والظروف الفعلية لكل مركز.')),
    ],
)

AIRWAY = dict(
    title=T('۲. ایمنی و مراقبت از راه هوایی',
            '2. Airway safety and care',
            '٢. سلامة الطريق الهوائي والعناية به'),
    en='Airway Safety & Care',
    lead=T('توسعه راهکارهای تخصصی برای مراقبت ایمن‌تر از بیماران',
           'Developing specialist solutions for safer patient care',
           'تطوير حلول تخصصية لرعاية أكثر أماناً للمرضى'),
    body=[
        T('مراقبت از راه هوایی و مدیریت ترشحات، از جنبه‌های مهم مراقبت بیماران در بخش‌های ویژه و سایر محیط‌های درمانی است. بهداشت دهان، تثبیت تجهیزات و کاهش خطرات مرتبط با فرایندهای مراقبت، نیازمند استفاده از محصولات تخصصی و روش‌های استاندارد است.',
          'Airway care and secretion management are an important part of looking after patients in intensive units and other care settings. Oral hygiene, securing equipment and reducing the risks tied to care all need specialist products and standard methods.',
          'العناية بالطريق الهوائي وإدارة الإفرازات من جوانب رعاية المرضى المهمة في الأقسام الخاصة وسائر البيئات العلاجية. صحة الفم، وتثبيت التجهيزات، وتقليل المخاطر المرتبطة بإجراءات الرعاية، تحتاج إلى منتجات تخصصية وطرق معيارية.'),
        T('آبادیس با بهره‌گیری از تجربیات خود در مدیریت ترشحات و توسعه تجهیزات پزشکی، مرحله جدیدی از فعالیت‌های تحقیق و توسعه را در حوزه ایمنی و مراقبت از راه هوایی آغاز کرده است.',
          'Using its experience in secretion management and medical-device development, Abadis has opened a new stage of research and development in airway safety and care.',
          'استفادت آباديس من خبرتها في إدارة الإفرازات وتطوير التجهيزات الطبية، وبدأت مرحلة جديدة من البحث والتطوير في سلامة الطريق الهوائي والعناية به.'),
        T('توسعه محصولاتی همچون مسواک ساکشن، فیکسر لوله تراشه و تجهیزات مرتبط، بخشی از این مسیر است.',
          'Developing products such as the suction toothbrush, the endotracheal-tube fixer and related equipment is part of this path.',
          'تطوير منتجات مثل فرشاة الشفط ومثبّت أنبوب القصبة والتجهيزات المرتبطة جزء من هذا المسار.'),
    ],
    axes_h=T('رویکرد آبادیس در این حوزه بر سه محور متمرکز است:',
             'Abadis focuses this field on three axes:',
             'يتركز منهج آباديس في هذا المجال على ثلاثة محاور:'),
    axes=[
        (T('ایمنی بیمار', 'Patient safety', 'سلامة المريض'),
         T('توسعه محصولاتی که به انجام ایمن‌تر فرایندهای مراقبت کمک کنند.',
           'Developing products that help care procedures be carried out more safely.',
           'تطوير منتجات تساعد على تنفيذ إجراءات الرعاية بصورة أكثر أماناً.')),
        (T('سهولت مراقبت', 'Ease of care', 'سهولة الرعاية'),
         T('توجه به طراحی کاربردی و نیازهای پزشکان و پرستاران در محیط‌های بالینی.',
           'Attention to practical design and to what physicians and nurses need in clinical settings.',
           'الاهتمام بالتصميم العملي وحاجات الأطباء والممرضين في البيئات السريرية.')),
        (T('نوآوری تخصصی', 'Specialist innovation', 'ابتكار تخصصي'),
         T('بهره‌گیری از دانش مهندسی و شناخت نیازهای درمانی برای توسعه محصولات جدید.',
           'Using engineering knowledge and an understanding of clinical needs to develop new products.',
           'الاستفادة من المعرفة الهندسية وفهم الحاجات العلاجية لتطوير منتجات جديدة.')),
    ],
    after=[
        T('هدف ما گسترش توانمندی‌های تخصصی آبادیس و مشارکت مؤثرتر در ارتقای کیفیت مراقبت بیمارستانی است.',
          'Our aim is to extend Abadis’s specialist capability and to take a more effective part in raising the quality of hospital care.',
          'هدفنا توسيع القدرات التخصصية لآباديس والمشاركة بفاعلية أكبر في رفع جودة الرعاية في المستشفى.'),
    ],
    ctas=[
        ('other', T('آشنایی با مسیر توسعه محصولات مراقبت از راه هوایی',
                    'The development path for airway-care products',
                    'مسار تطوير منتجات العناية بالطريق الهوائي')),
    ],
    notes=[
        (T('مسئله', 'Problem', 'المسألة'),
         T('مراقبت دهان و راه هوایی بیماران نیازمند مدیریت ترشحات، تثبیت مناسب لوله تراشه و دسترسی به ابزارهای کاربردی است.',
           'Oral and airway care needs secretion management, proper fixation of the endotracheal tube, and practical tools.',
           'عناية الفم والطريق الهوائي للمريض تحتاج إلى إدارة الإفرازات، وتثبيت مناسب لأنبوب القصبة، وأدوات عملية.')),
        (T('راهکار آبادیس', 'Abadis solution', 'حل آباديس'),
         T('توسعه مجموعه‌ای از محصولات مکمل برای تسهیل مراقبت دهان و کمک به ایمنی راه هوایی.',
           'A set of complementary products that make oral care easier and support airway safety.',
           'تطوير مجموعة من المنتجات المكمّلة لتيسير عناية الفم والمساعدة في سلامة الطريق الهوائي.')),
        (T('اجزای راهکار', 'Components', 'مكوّنات الحل'),
         T('مسواک ساکشن، سواب دهانی، فیکسر لوله تراشه و ملزومات مرتبط؛ متناسب با وضعیت توسعه و عرضه هر محصول.',
           'Suction toothbrush, oral swab, endotracheal-tube fixer and related items, according to how far each product is in development and supply.',
           'فرشاة الشفط، والمسحة الفموية، ومثبّت أنبوب القصبة، واللوازم المرتبطة؛ بحسب مرحلة تطوير كل منتج وعرضه.')),
        (T('کاربردها', 'Applications', 'الاستخدامات'),
         T('مراقبت از بیماران بستری، به‌ویژه بیماران دارای لوله تراشه، مطابق دستورالعمل مصرف هر محصول.',
           'Care of inpatients, especially patients with an endotracheal tube, following each product’s instructions for use.',
           'رعاية المرضى المقيمين، ولا سيما من لديهم أنبوب قصبة، وفق تعليمات استعمال كل منتج.')),
        (T('مزیت‌ها', 'Advantages', 'المزايا'),
         T('سهولت مراقبت دهان، کمک به جمع‌آوری ترشحات و تثبیت لوله تراشه.',
           'Easier oral care, help with collecting secretions, and fixation of the endotracheal tube.',
           'سهولة عناية الفم، والمساعدة في جمع الإفرازات، وتثبيت أنبوب القصبة.')),
        (T('ارزش اقتصادی', 'Economic value', 'القيمة الاقتصادية'),
         T('کمک به مدیریت زمان مراقبت و مصرف ملزومات؛ قابل ارزیابی بر اساس الگوی مصرف و فرایندهای هر مرکز.',
           'Help with care time and the use of supplies; it can be judged from each centre’s usage and processes.',
           'المساعدة في إدارة وقت الرعاية واستهلاك اللوازم؛ ويمكن تقييمه وفق نمط الاستهلاك وإجراءات كل مركز.')),
    ],
)

WASTE = dict(
    title=T('۳. کنترل آلودگی و مدیریت پسماند',
            '3. Contamination control and waste management',
            '٣. السيطرة على التلوث وإدارة النفايات'),
    en='Contamination Control & Waste Management',
    lead=T('فناوری مواد؛ افقی جدید در توسعه راهکارهای پایدار',
           'Materials technology; a new horizon for sustainable solutions',
           'تقنية المواد؛ أفق جديد في تطوير الحلول المستدامة'),
    body=[
        T('کنترل آلودگی و مدیریت پسماندهای بیمارستانی، از چالش‌های مهم نظام سلامت و حفاظت از محیط زیست است. افزایش مصرف تجهیزات یکبارمصرف و ضرورت مدیریت ایمن پسماندها، نیاز به توسعه فناوری‌ها و راهکارهای جدید را بیش از گذشته آشکار می‌کند.',
          'Contamination control and hospital-waste management are important challenges for the health system and for protecting the environment. Higher use of disposable equipment, and the need to handle waste safely, make the case for new technologies and solutions clearer than before.',
          'السيطرة على التلوث وإدارة نفايات المستشفى من التحديات المهمة للنظام الصحي ولحماية البيئة. ارتفاع استهلاك التجهيزات ذات الاستعمال الواحد، وضرورة الإدارة الآمنة للنفايات، يُظهران الحاجة إلى تقنيات وحلول جديدة أكثر من قبل.'),
        T('آبادیس در ادامه مسیر نوآوری خود، تحقیق و توسعه در حوزه فناوری مواد و راهکارهای نوین کنترل آلودگی و مدیریت پسماند را از زمینه‌های آینده فعالیت خود قرار داده است.',
          'Continuing its innovation path, Abadis has made research and development in materials technology, and in new contamination-control and waste-management solutions, part of its future work.',
          'في امتداد مسار ابتكارها، جعلت آباديس البحث والتطوير في تقنية المواد وحلول السيطرة على التلوث وإدارة النفايات من مجالات عملها المستقبلية.'),
        T('مطالعه و توسعه محصولات مبتنی بر پلی‌وینیل الکل (PVA)، فیلم‌های محلول در آب و فناوری‌های مرتبط، بخشی از این رویکرد آینده‌نگر است.',
          'Studying and developing products based on polyvinyl alcohol (PVA), water-soluble films and related technologies is part of this forward-looking approach.',
          'دراسة وتطوير منتجات قائمة على كحول البولي فينيل (PVA)، والأفلام الذوّابة في الماء والتقنيات المرتبطة، جزء من هذا المنهج المتطلع إلى المستقبل.'),
    ],
    axes_h=T('این مسیر بر سه اصل استوار است:',
             'This path rests on three principles:',
             'يستند هذا المسار إلى ثلاثة مبادئ:'),
    axes=[
        (T('نوآوری در مواد', 'Innovation in materials', 'الابتكار في المواد'),
         T('بررسی قابلیت‌های مواد پیشرفته برای کاربردهای تخصصی پزشکی و بیمارستانی.',
           'Examining what advanced materials can do for specialist medical and hospital uses.',
           'دراسة قدرات المواد المتقدمة للاستخدامات الطبية والمستشفوية التخصصية.')),
        (T('مدیریت پسماند', 'Waste management', 'إدارة النفايات'),
         T('توسعه راهکارهایی با هدف بهبود فرایندهای جمع‌آوری، نگهداری و مدیریت پسماندهای مرتبط.',
           'Developing solutions aimed at improving how related waste is collected, held and managed.',
           'تطوير حلول تهدف إلى تحسين جمع النفايات المرتبطة وحفظها وإدارتها.')),
        (T('پایداری', 'Sustainability', 'الاستدامة'),
         T('توجه به مصرف منابع و ارزیابی اثرات محیط‌زیستی در طراحی و توسعه محصولات آینده.',
           'Attention to resource use, and to environmental effects, when future products are designed and developed.',
           'الاهتمام باستهلاك الموارد وتقييم الآثار البيئية في تصميم المنتجات المستقبلية وتطويرها.')),
    ],
    after=[
        T('ما معتقدیم ترکیب دانش مهندسی، تحقیق و توسعه و شناخت نیازهای مراکز درمانی می‌تواند زمینه‌ساز نسل جدیدی از محصولات تخصصی پزشکی باشد.',
          'We believe that engineering knowledge, research and development, and an understanding of what care centres need can prepare the ground for a new generation of specialist medical products.',
          'نعتقد أن الجمع بين المعرفة الهندسية والبحث والتطوير وفهم حاجات المراكز العلاجية يمكن أن يمهّد لجيل جديد من المنتجات الطبية التخصصية.'),
    ],
    ctas=[
        ('close', T('آشنایی با فناوری‌ها و برنامه‌های توسعه آینده آبادیس',
                    'Abadis technologies and future development programmes',
                    'تقنيات آباديس وبرامج التطوير المستقبلية')),
    ],
    notes=[
        (T('مسئله', 'Problem', 'المسألة'),
         T('جابه‌جایی اقلام آلوده و مدیریت پسماندهای بیمارستانی، نیازمند کنترل تماس، تفکیک مناسب و مصرف مسئولانه منابع است.',
           'Moving contaminated items and managing hospital waste needs contact control, proper separation and responsible use of resources.',
           'نقل المواد الملوثة وإدارة نفايات المستشفى يحتاج إلى ضبط التلامس، وفرز مناسب، واستهلاك مسؤول للموارد.')),
        (T('راهکار آبادیس', 'Abadis solution', 'حل آباديس'),
         T('تحقیق و توسعه در فناوری مواد و محصولات یکبارمصرف برای بهبود فرایندهای کنترل آلودگی و مدیریت اقلام آلوده.',
           'Research and development in materials technology and disposable products, to improve contamination control and the handling of contaminated items.',
           'البحث والتطوير في تقنية المواد والمنتجات ذات الاستعمال الواحد لتحسين السيطرة على التلوث وإدارة المواد الملوثة.')),
        (T('اجزای راهکار', 'Components', 'مكوّنات الحل'),
         T('رسیور یکبارمصرف برای جمع‌آوری اولیه؛ فیلم‌ها و کیسه‌های محلول در آب مبتنی بر PVA در مسیر تحقیق و توسعه، با کاربرد وابسته به طراحی و اعتبارسنجی.',
           'A disposable receiver for the first collection; PVA-based water-soluble films and bags still in research and development, with use that depends on design and validation.',
           'وعاء تجميع ذو استعمال واحد للجمع الأولي؛ وأفلام وأكياس ذؤابة في الماء قائمة على PVA في مسار البحث والتطوير، واستخدامها مرهون بالتصميم والتحقق.')),
        (T('کاربردها', 'Applications', 'الاستخدامات'),
         T('جمع‌آوری اولیه ترشحات و اقلام مصرف‌شده حین مراقبت؛ کاربردهای آینده برای جابه‌جایی اقلام آلوده، متناسب با محصول نهایی.',
           'First collection of secretions and items used during care; future uses for moving contaminated items, matched to the finished product.',
           'الجمع الأولي للإفرازات والمواد المستهلكة أثناء الرعاية؛ واستخدامات مستقبلية لنقل المواد الملوثة، بحسب المنتج النهائي.')),
        (T('مزیت‌ها', 'Advantages', 'المزايا'),
         T('کاهش نیاز به شست‌وشوی ظروف چندبارمصرف و کمک به سامان‌دهی جمع‌آوری و جابه‌جایی اقلام آلوده.',
           'Less need to wash reusable containers, and help organising the collection and movement of contaminated items.',
           'حاجة أقل إلى غسل الأوعية المتعددة الاستعمال، والمساعدة في تنظيم جمع المواد الملوثة ونقلها.')),
        (T('ارزش اقتصادی', 'Economic value', 'القيمة الاقتصادية'),
         T('امکان کاهش زمان شست‌وشو، مصرف آب و مواد شوینده؛ ارزیابی صرفه اقتصادی و اثر محیط‌زیستی بر اساس چرخه مصرف هر محصول.',
           'A possible reduction in washing time, water and detergent; the economic and environmental effect is judged on each product’s use cycle.',
           'إمكانية تقليل زمن الغسل واستهلاك الماء ومواد التنظيف؛ ويُقيَّم الوفر الاقتصادي والأثر البيئي وفق دورة استهلاك كل منتج.')),
    ],
)

BY_SLUG = {
    'fluid-management': FLUID,
    'airway-care': AIRWAY,
    'waste-management-pva': WASTE,
}

FOLD = {
    'hospital-suction-systems': T(
        'سیستم‌های ساکشن بیمارستانی زیر راهکار مدیریت مایعات و ترشحات قرار دارند.',
        'Hospital suction systems sit under fluid and secretion management.',
        'أنظمة الشفط في المستشفى تندرج تحت إدارة السوائل والإفرازات.'),
    'contamination-control': T(
        'حفاظت از مدار ساکشن کنار راهکار کنترل آلودگی و مدیریت پسماند خوانده می‌شود.',
        'Suction-circuit protection is read alongside contamination control and waste management.',
        'تُقرأ حماية دارة الشفط إلى جانب السيطرة على التلوث وإدارة النفايات.'),
}

CLOSE = dict(
    h=T('فناوری و نوآوری؛ پیونددهنده راهکارهای آبادیس',
        'Technology and innovation, joining Abadis solutions',
        'التقنية والابتكار؛ ما يصل حلول آباديس'),
    body=[
        T('در آبادیس، نوآوری تنها به توسعه یک محصول جدید محدود نمی‌شود؛ بلکه بخشی از نگاه ما به تولید، مدیریت و آینده کسب‌وکار است.',
          'At Abadis, innovation is not limited to developing one new product. It is part of how we look at manufacturing, management and the future of the business.',
          'في آباديس، لا ينحصر الابتكار في تطوير منتج جديد واحد؛ بل هو جزء من نظرتنا إلى الإنتاج والإدارة ومستقبل العمل.'),
        T('بهره‌گیری از هوشمندی کسب‌وکار، هوش تجاری (BI)، تحلیل داده‌ها و ظرفیت‌های هوش مصنوعی (AI)، در کنار تحقیق و توسعه و زیرساخت‌های تولید، به ما کمک می‌کند تصمیم‌گیری، برنامه‌ریزی و فرایندهای سازمانی خود را بهبود بخشیم.',
          'Business intelligence, BI, data analysis and AI capacity, beside research and development and production infrastructure, help us improve decisions, planning and organisational processes.',
          'الاستفادة من ذكاء الأعمال والذكاء التجاري (BI) وتحليل البيانات وقدرات الذكاء الاصطناعي (AI)، إلى جانب البحث والتطوير وبنى الإنتاج، تساعدنا على تحسين القرار والتخطيط والعمليات التنظيمية.'),
        T('ما با رویکردی علمی و مبتنی بر یادگیری مستمر، تلاش می‌کنیم پیوند میان تجربه صنعتی، فناوری و نیازهای واقعی مراکز درمانی را تقویت کنیم.',
          'With a scientific approach based on continuous learning, we work to strengthen the link between industrial experience, technology and the real needs of care centres.',
          'بمنهج علمي قائم على التعلم المستمر، نسعى إلى تقوية الصلة بين الخبرة الصناعية والتقنية والحاجات الحقيقية للمراكز العلاجية.'),
    ],
    earth=T('راهکارهایی برای سلامت انسان و آینده زمین',
            'Solutions for human health and the future of the earth',
            'حلول لصحة الإنسان ومستقبل الأرض'),
    earth_body=[
        T('تعهد آبادیس به توسعه پایدار، بخشی جدایی‌ناپذیر از نگاه ما به نوآوری و تولید است.',
          'Abadis’s commitment to sustainable development is an inseparable part of how we look at innovation and manufacturing.',
          'التزام آباديس بالتنمية المستدامة جزء لا ينفصل عن نظرتنا إلى الابتكار والإنتاج.'),
        T('در خانواده سبز آبادیس، تلاش می‌کنیم توسعه صنعت سلامت با مسئولیت‌پذیری اجتماعی، مدیریت هوشمند منابع و حفاظت از محیط زیست همراه باشد.',
          'In the Abadis green family, we try to keep the growth of the health industry together with social responsibility, intelligent use of resources and protection of the environment.',
          'في العائلة الخضراء لآباديس، نسعى إلى أن يمضي تطور صناعة الصحة مع المسؤولية الاجتماعية والإدارة الذكية للموارد وحماية البيئة.'),
        T('ما به اثرگذاری واقعی باور داریم؛ اثری که از یک محصول آغاز می‌شود و می‌تواند به بهبود فرایندهای مراقبت، کاهش مصرف منابع و ساختن آینده‌ای پایدارتر کمک کند.',
          'We believe in a real effect: an effect that starts with one product and can help improve care processes, reduce resource use and build a more sustainable future.',
          'نؤمن بأثر حقيقي؛ أثر يبدأ من منتج واحد ويمكن أن يساعد في تحسين إجراءات الرعاية، وتقليل استهلاك الموارد، وبناء مستقبل أكثر استدامة.'),
    ],
)

TEASER = T(
    'محصولات، راهکارها، کاربردها و نوآوری',
    'Products, solutions, applications and innovation',
    'المنتجات والحلول والاستخدامات والابتكار')
TEASER_TAIL = T(
    'فلسفه راهکارها',
    'The solutions philosophy',
    'فلسفة الحلول')


def _p(text):
    return f'<p>{esc(text)}</p>'


def _paras(items, lang):
    return ''.join(_p(x[lang]) for x in items)


def _axes(items, lang):
    lis = ''.join(
        f'<li><strong>{esc(title[lang])}: </strong>{esc(text[lang])}</li>'
        for title, text in items)
    return f'<ul class="phil-principles">{lis}</ul>'


def _page_links(lang, url, slugs):
    bits = []
    for slug in slugs:
        bits.append(f'<a href="{url(_sol(lang, slug))}">{esc(PAGE_NAME[slug][lang])}</a>')
    return ' · '.join(bits)


def _cta(lang, url, kind, label):
    if kind == 'calc':
        href = url(CALC[lang])
    elif kind == 'other':
        href = url(ORAL[lang])
    elif kind == 'close':
        href = '#phil-close'
    else:
        href = url(_sol(lang, 'fluid-management'))
    return f'<a href="{href}">{esc(label[lang])}</a>'


def _green(lang, url, text):
    name = {
        'fa': 'خانواده سبز آبادیس',
        'en': 'Abadis green family',
        'ar': 'العائلة الخضراء لآباديس',
    }[lang]
    sdg = {
        'fa': 'توسعه پایدار',
        'en': 'sustainable development',
        'ar': 'التنمية المستدامة',
    }[lang]
    safe = esc(text)
    safe = safe.replace(esc(name), f'<a href="{url(GREEN[lang])}">{esc(name)}</a>', 1)
    safe = safe.replace(esc(sdg), f'<a href="{url(SDGS[lang])}">{esc(sdg)}</a>', 1)
    return safe


def closing_html(lang, url):
    body = _paras(CLOSE['body'], lang)
    earth = f'<p>{_green(lang, url, CLOSE["earth_body"][0][lang])}</p>'
    green = f'<p>{_green(lang, url, CLOSE["earth_body"][1][lang])}</p>'
    rest = _paras(CLOSE['earth_body'][2:], lang)
    return (f'<div class="phil-close phil-close-grid" id="phil-close">'
            f'<article class="phil-close-card"><h3>{esc(CLOSE["h"][lang])}</h3>{body}</article>'
            f'<article class="phil-close-card"><h3>{esc(CLOSE["earth"][lang])}</h3>{earth}{green}{rest}</article></div>')


def hub_html(lang, url):
    pillars = ''.join(
        f'<li><strong>{esc(PILLARS[i][lang])}: </strong>{esc(PILLAR_TEXT[i][lang])}</li>'
        for i in range(4))
    head = ''.join(f'<th scope="col">{esc(h[lang])}</th>' for h in PATHS_HEAD)
    rows = ''.join(
        '<tr>' + ''.join(
            f'<td data-label="{esc(PATHS_HEAD[i][lang])}">{esc(cell[lang])}</td>'
            for i, cell in enumerate(row)) + '</tr>'
        for row in PATHS)
    theme_rows = ''.join(
        f'<tr><td data-label="{esc(MAP_COL[0][lang])}">{esc(theme["products"][lang])}</td>'
        f'<td data-label="{esc(MAP_COL[1][lang])}">{esc(theme["title"][lang])}</td>'
        f'<td data-label="{esc(MAP_COL[2][lang])}">{_page_links(lang, url, THEME_PAGES[theme["key"]])}</td></tr>'
        for theme in THEMES)
    nums = '۱۲۳۴۵۶۷۸' if lang == 'fa' else ('12345678' if lang == 'en' else '١٢٣٤٥٦٧٨')
    catalog = ''.join(
        f'<li><b>{nums[i]}</b> <a href="{url(CAT_HREF[lang][i])}">{esc(PRODUCT_ROWS[i][lang])}</a></li>'
        for i in range(8))
    map_head = ''.join(f'<th scope="col">{esc(h[lang])}</th>' for h in MAP_COL)
    return f'''<section class="section phil-sec" id="phil">
  <div class="wrap">
    <h2>{esc(PATHS_H[lang])}</h2>
    <h3>{esc(QUESTIONS_H[lang])}</h3>
    <ol class="phil-pillars">{pillars}</ol>
    <div class="phil-table-wrap"><table class="phil-table">
      <thead><tr>{head}</tr></thead>
      <tbody>{rows}</tbody>
    </table></div>
    <p class="phil-kicker">{esc(INTRO_KICK[lang])}</p>
    <h2>{esc(INTRO_H[lang])}</h2>
    <p class="phil-lead">{esc(INTRO_SUB[lang])}</p>
    {_paras(INTRO, lang)}
    <h3>{esc(MAP_H[lang])}</h3>
    <div class="phil-table-wrap"><table class="phil-table">
      <thead><tr>{map_head}</tr></thead>
      <tbody>{theme_rows}</tbody>
    </table></div>
    <h3>{esc(CAT_H[lang])}</h3>
    <ol class="phil-catalog">{catalog}</ol>
    {closing_html(lang, url)}
  </div>
</section>'''


def theme_html(lang, slug, url):
    theme = BY_SLUG.get(slug)
    if not theme:
        return ''
    fold = ''
    if slug in FOLD:
        target = 'fluid-management' if slug == 'hospital-suction-systems' else 'waste-management-pva'
        fold = (f'<p class="phil-fold"><a href="{url(_sol(lang, target))}">'
                f'{esc(FOLD[slug][lang])}</a></p>')
    en = f'<p class="phil-en" dir="ltr">{esc(theme["en"])}</p>' if lang != 'en' else ''
    ctas = ' <span aria-hidden="true">|</span> '.join(_cta(lang, url, k, lab) for k, lab in theme['ctas'])
    return f'''<section class="section phil-sec" id="philosophy">
  <div class="wrap">
    {fold}
    <h2>{esc(theme["title"][lang])}</h2>
    {en}
    <p class="phil-lead">{esc(theme["lead"][lang])}</p>
    {_paras(theme["body"], lang)}
    <p>{esc(theme["axes_h"][lang])}</p>
    {_axes(theme["axes"], lang)}
    {_paras(theme["after"], lang)}
    <p class="phil-cta">{ctas}</p>
    {closing_html(lang, url)}
    <h3>{esc(NOTES_H[lang])}</h3>
    {_axes(theme["notes"], lang)}
  </div>
</section>'''


def teaser_html(lang, href):
    return (f'<p class="ps-tease"><a href="{href}">{esc(TEASER[lang])}</a>'
            f' — {esc(TEASER_TAIL[lang])}</p>')
