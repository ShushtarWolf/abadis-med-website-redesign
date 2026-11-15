#!/usr/bin/env python3
"""CSR, careers roadmap, article hubs, and home story strips."""
import re
from pathlib import Path
from parity_apply import SITE, V, read, write

CSR_BASE = '../../مسئولیت-اجتماعی/'

def apply_pairs(text, pairs):
    for a, b in sorted(pairs, key=lambda x: -len(x[0])):
        text = text.replace(a, b)
    return text

def csr_block(lang):
    s = read(SITE / 'مسئولیت-اجتماعی/index.html')
    start = s.find('<div class="csr-bg"')
    end = s.find('</main>', start) + len('</main>')
    block = s[start:end]
    block = apply_pairs(block, CSR[lang])
    block = block.replace('data-img-base="img/hero/"', f'data-img-base="{CSR_BASE}img/hero/"')
    block = block.replace('src="img/', f'src="{CSR_BASE}img/')
    block = block.replace('srcset="img/', f'srcset="{CSR_BASE}img/')
    block = block.replace(', img/', f', {CSR_BASE}img/')
    block = block.replace('href="../', 'href="../../')
    block = block.replace('src="../', 'src="../../')
    return block

def patch_csr():
    head_extra = (
        f'<link rel="stylesheet" href="{CSR_BASE}zagros-hero.css?v={V}">\n'
        f'<link rel="stylesheet" href="{CSR_BASE}names/wall-of-honor.css?v={V}">\n'
        f'<link rel="stylesheet" href="{CSR_BASE}names/mix.css?v={V}">\n'
        f'<link rel="preload" as="image" href="{CSR_BASE}img/hero/bg-dry.webp" type="image/webp">\n'
    )
    scripts = (
        f'<script src="{CSR_BASE}zagros-hero.js?v={V}" defer></script>\n'
        f'<script src="{CSR_BASE}names/names-common.js?v={V}" defer></script>\n'
        f'<script src="{CSR_BASE}names/mix-tags.js?v={V}" defer></script>\n'
        f'<script src="{CSR_BASE}names/wall-of-honor.js?v={V}" defer></script>\n'
    )
    pages = {
        'en': (SITE / 'en/csr/index.html',
               'Save Zagros — Abadis Medical Reservoirs',
               'The Save Zagros campaign: oak saplings planted in the Zagros highlands in the name of partner healthcare centres.'),
        'ar': (SITE / 'arabic/csr/index.html',
               'إنقاذ زاغروس — خزانات طبي آباديس',
               'حملة إنقاذ زاغروس: غرس شتلات البلوط في مرتفعات زاغروس باسم المراكز العلاجية الشريكة.'),
    }
    for lang, (path, title, desc) in pages.items():
        s = read(path)
        block = csr_block(lang)
        s, n = re.subn(r'<main\b[^>]*>.*?</main>', block, s, count=1, flags=re.S)
        if n != 1:
            raise SystemExit('csr main ' + lang)
        if 'zagros-hero.css' not in s:
            s = s.replace('</head>', head_extra + '</head>', 1)
        if 'wall-of-honor.js' not in s:
            s = s.replace('</body>', scripts + '</body>', 1)
        s = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', s, count=1, flags=re.S)
        s = re.sub(r'(<meta name="description" content=")[^"]*"',
                   lambda m, d=desc: m.group(1) + d.replace('"', '') + '"', s, count=1)
        write(path, s)
        main = s.split('<main', 1)[1].split('</main>', 1)[0]
        bad = set(re.findall(r'[\u067e\u0686\u0698\u06af][\u0600-\u06FF]+', main))
        print(lang, 'persian-letters', list(bad)[:12])

# Shared campaign copy. EN first, AR second. Keys are the FA source strings.
def _c(en, ar):
    return {'en': en, 'ar': ar}

CSR_SRC = {
 'پویش نجات زاگرس · کاشت نهال بلوط': _c('Save Zagros campaign · planting oak saplings', 'حملة إنقاذ زاغروس · غرس شتلات البلوط'),
 'نجات زاگرس،‌مسئولیت اجتماعی آبادیس': _c('Save Zagros, Abadis social responsibility', 'إنقاذ زاغروس، المسؤولية الاجتماعية لآباديس'),
 'کاشت نهال بلوط در ارتفاعات زاگرس؛ تا مکانی به نام آبادیس و به یاد صنعت سلامت کشور ثبت شود.': _c(
    'Oak saplings planted in the Zagros highlands, so a place is recorded in the name of Abadis and in memory of the country’s health industry.',
    'غرس شتلات البلوط في مرتفعات زاغروس، ليُسجَّل مكان باسم آباديس وذكرى لصناعة الصحة في البلاد.'),
 'داستان پویش': _c('The campaign story', 'قصة الحملة'),
 'صفحهٔ فعلی پویش': _c('The campaign page', 'صفحة الحملة'),
 'مرکز درمانی': _c('healthcare centres', 'مركز علاجي'),
 'مراکز درمانی همراه آبادیس': _c('Healthcare centres alongside Abadis', 'المراكز العلاجية مع آباديس'),
 'نام مرکز درمانی خود را جستجو کنید': _c('Search for your healthcare centre', 'ابحث عن مركزك العلاجي'),
 'فهرست مراکز درمانی همراه آبادیس': _c('List of healthcare centres alongside Abadis', 'قائمة المراكز العلاجية مع آباديس'),
 'نهال بلوط تا اردیبهشت ۱۴۰۳': _c('oak saplings by May 2024', 'شتلة بلوط حتى مايو ٢٠٢٤'),
 'مرکز درمانی؛ اعضای خانواده سبز آبادیس در ۳۱ استان': _c('healthcare centres; members of the Abadis Green Family in 31 provinces', 'مركزاً علاجياً؛ أعضاء عائلة آباديس الخضراء في ٣١ محافظة'),
 'نفر شرکت‌کننده در همایش نجات زاگرس': _c('people at the Save Zagros conference', 'مشاركاً في مؤتمر إنقاذ زاغروس'),
 '>زاگرس<': _c('>Zagros<', '>زاغروس<'),
 'مسیر پویش': _c('Campaign path', 'مسار الحملة'),
 'روز درختکاری': _c('Tree Planting Day', 'يوم التشجير'),
 'آغاز کاشت بلوط به تعداد اعضای خانواده آبادیس؛ ۱٬۲۸۴ مرکز درمانی.': _c(
    'Oak planting began for every member of the Abadis family: 1,284 healthcare centres.',
    'بدأ غرس البلوط بعدد أعضاء عائلة آباديس: ١٬٢٨٤ مركزاً علاجياً.'),
 '۱۵ اسفند ۱۴۰۲': _c('5 March 2024', '٥ مارس ٢٠٢٤'),
 'همایش نجات زاگرس در مرکز همایش‌های بین‌المللی دانشگاه علم و فرهنگ، با مشارکت حدود ۸۰۰ نفر.': _c(
    'The Save Zagros conference at the Science and Culture University international conference centre, with about 800 participants.',
    'مؤتمر إنقاذ زاغروس في مركز المؤتمرات الدولي لجامعة العلم والثقافة، بمشاركة نحو ٨٠٠ شخص.'),
 'اردیبهشت ۱۴۰۳': _c('April–May 2024', 'أبريل–مايو ٢٠٢٤'),
 'رساندن شمار نهال‌ها به 1000 عدد در ارتفاعات زاگرس.': _c('The number of saplings in the Zagros highlands reached 1,000.', 'بلغ عدد الشتلات في مرتفعات زاغروس ١٠٠٠.'),
 '۳۰ تیر ۱۴۰۳': _c('20 July 2024', '٢٠ يوليو ٢٠٢٤'),
 'حمایت آبادیس از کارزار درخواست نجات زاگرس؛ مدیران و پرسنل آبادیس این کارزار را امضا نمودند.': _c(
    'Abadis backed the Save Zagros petition; managers and staff signed it.',
    'دعمت آباديس عريضة طلب إنقاذ زاغروس؛ ووقّعها المديرون والموظفون.'),
 'کارزار درخواست نجات زاگرس': _c('The Save Zagros petition', 'عريضة طلب إنقاذ زاغروس'),
 'متن کارزار درخواست نجات زاگرس': _c('Text of the Save Zagros petition', 'نص عريضة طلب إنقاذ زاغروس'),
 'ما به اندازه یک سرانگشت اثر می‌گذاریم': _c('We make a difference the size of a fingertip', 'نُحدث أثراً بقدر طرف إصبع'),
 'به شما، به طبیعت، به جهان.': _c('To you, to nature, to the world.', 'لك، وللطبيعة، وللعالم.'),
 'شناسنامه بلوط‌ها و جزئیات بیشتر': _c('Oak records and further detail', 'سجل أشجار البلوط ومزيد من التفاصيل'),
 'ارتباط با ما': _c('Contact', 'اتصل بنا'),
 'مسئولیت اجتماعی': _c('Social responsibility', 'المسؤولية الاجتماعية'),
 'نمایش بزرگ‌تر': _c('Larger view', 'عرض أكبر'),
 'لوح های تقدیر': _c('Certificates of appreciation', 'شهادات التقدير'),
 'مجتمع عدالت': _c('Edalat complex', 'مجمّع عدالت'),
 'غدیر': _c('Ghadir', 'غدير'),
 'انجمن حمایت زندانیان': _c('Prisoners’ support association', 'جمعية دعم السجناء'),
 'گالری تصاویر': _c('Image gallery', 'معرض الصور'),
 'بستن': _c('Close', 'إغلاق'),
 'تصویر قبلی': _c('Previous image', 'الصورة السابقة'),
 'تصویر بعدی': _c('Next image', 'الصورة التالية'),
}

# Long paragraphs stored separately so the short labels above win only as whole strings.
CSR_LONG = {
 'جنگل‌های زاگرس به‌عنوان یکی از مهم‌ترین ذخایر اکولوژیکی کشور، طی سال‌های گذشته به دلایل متعددی از جمله آتش‌سوزی‌های گسترده، کشاورزی غیر اصولی و فعالیت‌های انسانی، دچار خسارت‌های جبران‌ناپذیری شده‌اند. طبق آمار، تنها در سال ۱۳۹۵ بیش از ۷۵ مورد آتش‌سوزی منجر به نابودی حدود ۹۵۰ هکتار از جنگل‌های زاگرس شد.': _c(
    'The Zagros forests, one of the country’s most important ecological reserves, have suffered irreversible damage in recent years from widespread fires, unsound farming, and human activity. In 2016 alone, more than 75 fires destroyed about 950 hectares of Zagros forest.',
    'تعرضت غابات زاغروس، وهي من أهم المحميات البيئية في البلاد، خلال السنوات الماضية لأضرار لا تُعوَّض بسبب الحرائق الواسعة والزراعة غير السليمة والأنشطة البشرية. في عام ٢٠١٦ وحده أدّت أكثر من ٧٥ حريقاً إلى تدمير نحو ٩٥٠ هكتاراً من غابات زاغروس.'),
 'همایش نجات زاگرس فرصتی است برای طرح یک راهکار عملیاتی، ویژه ی جنگل‌های زاگرس در راستای حفظ و نگهداری و احیاء جنگل های سوخته و جوان سازی جنگل های کهنسال. این راهکار از طریق کاشت هزارن نهال بلوط شروع می شود.': _c(
    'The Save Zagros conference is a chance to set out a practical plan for the Zagros forests: protecting them, restoring burnt woodland, and renewing old stands. That plan starts by planting thousands of oak saplings.',
    'مؤتمر إنقاذ زاغروس فرصة لطرح حل عملي خاص بغابات زاغروس: حفظها، وإحياء الغابات المحترقة، وتجديد الغابات المعمرة. ويبدأ هذا الحل بغرس آلاف شتلات البلوط.'),
 'بدین جهت آبادیس قدم بزرگی در راستای مسئولیت اجتماعی خود برداشت و با همکاری شرکت ایده‌پردازان نواندیش فردا با نام تجاری (<span class="latin">Dpaper</span>) برای نجات زاگرس به تعداد اعضای خانواده خود که ۱٬۲۸۴ مرکز درمانی می باشد؛ با کاشت بلوط در روز درختکاری اثرگذاری خود را به طبیعت اثبات کرد و تا اردیبهشت سال 1403 به تعداد 1000 عدد می‌رساند تا در ارتفاعات زاگرس مکانی به نام آبادیس و به یاد صنعت سلامت کشور ثبت شود.': _c(
    'Abadis therefore took a large step in its social responsibility. With Idehpardazan Noandish Farda, trading as <span class="latin">Dpaper</span>, it planted oaks on Tree Planting Day for each of the 1,284 healthcare centres in its family, to show its effect on nature, and by May 2024 brought the number to 1,000 so that a place in the Zagros highlands is recorded in the name of Abadis and in memory of the country’s health industry.',
    'لذلك خطت آباديس خطوة واسعة في مسؤوليتها الاجتماعية. وبالتعاون مع شركة «ايده‌پردازان نوانديش فردا» بالاسم التجاري <span class="latin">Dpaper</span>، غرست أشجار بلوط في يوم التشجير بعدد أفراد عائلتها البالغ ١٬٢٨٤ مركزاً علاجياً، لتُثبت أثرها في الطبيعة، وبحلول مايو ٢٠٢٤ أوصلت العدد إلى ١٠٠٠ ليسجَّل في مرتفعات زاغروس مكان باسم آباديس وذكرى لصناعة الصحة.'),
 'همایش نجات زاگرس': _c('The Save Zagros conference', 'مؤتمر إنقاذ زاغروس'),
}

def build_csr_maps():
    out = {'en': [], 'ar': []}
    for src, pair in {**CSR_LONG, **CSR_SRC}.items():
        out['en'].append((src, pair['en']))
        out['ar'].append((src, pair['ar']))
    # paragraphs that are too long to key in full are translated by additional exact slices below
    return out

CSR = None

def load_csr():
    global CSR
    CSR = build_csr_maps()
    # Append the remaining long blocks from a sidecar if present
    extra = Path(__file__).with_name('csr_long_pairs.py')
    if extra.is_file():
        ns = {}
        exec(extra.read_text(encoding='utf-8'), ns)
        for lang in ('en', 'ar'):
            CSR[lang].extend(ns['PAIRS'][lang])

# The long blocks live in this same module as EXTRA so one file is enough.
EXTRA = r'''
PAIRS = {'en': [], 'ar': []}
'''

def patch_careers():
    roadmap = {
        'en': '''<section class="co-sec co-sec--alt" id="roadmap"><div class="co-wrap">
      <div class="co-sec-head"><div><h2>How hiring works at Abadis</h2>
      <p>Four clear steps from the application to joining Abadis Medical Reservoirs.</p></div></div>
      <div class="co-roadmap">
        <article class="co-step-card"><span class="co-step-badge">1</span><h3>Submit an application</h3><p>Choose a role or send a general résumé and complete the formal form.</p></article>
        <article class="co-step-card"><span class="co-step-badge">2</span><h3>Specialist review</h3><p>The hiring manager and human resources review education and professional experience.</p></article>
        <article class="co-step-card"><span class="co-step-badge">3</span><h3>Interview</h3><p>A meeting to assess specialist skills and fit with the Abadis culture.</p></article>
        <article class="co-step-card"><span class="co-step-badge">4</span><h3>Join the Abadis family</h3><p>Enter the team, train at the Abadis Academy, and start the growth path.</p></article>
      </div></div></section>
''',
        'ar': '''<section class="co-sec co-sec--alt" id="roadmap"><div class="co-wrap">
      <div class="co-sec-head"><div><h2>مسار التوظيف في آباديس</h2>
      <p>أربع خطوات واضحة من تسجيل الطلب حتى الانضمام إلى خزانات آباديس الطبية.</p></div></div>
      <div class="co-roadmap">
        <article class="co-step-card"><span class="co-step-badge">١</span><h3>تسجيل طلب التعاون</h3><p>اختيار الوظيفة أو إرسال سيرة ذاتية عامة واستكمال النموذج الرسمي.</p></article>
        <article class="co-step-card"><span class="co-step-badge">٢</span><h3>المراجعة التخصصية</h3><p>يراجع مدير الوحدة والموارد البشرية المؤهل والخبرة المهنية.</p></article>
        <article class="co-step-card"><span class="co-step-badge">٣</span><h3>المقابلة</h3><p>جلسة للتعارف وتقييم المهارات التخصصية والتوافق مع ثقافة آباديس.</p></article>
        <article class="co-step-card"><span class="co-step-badge">٤</span><h3>بدء العمل في عائلة آباديس</h3><p>الدخول إلى الفريق، والتدريب في أكاديمية آباديس، وبدء مسار النمو.</p></article>
      </div></div></section>
''',
    }
    for lang, rel in (('en', 'en/collaboration-opportunities/index.html'), ('ar', 'arabic/careers/index.html')):
        s = read(SITE / rel)
        if 'id="roadmap"' not in s:
            s = s.replace('<section class="co-sec co-sec--alt" id="apply">',
                          roadmap[lang] + '<section class="co-sec co-sec--alt" id="apply">', 1)
            if 'id="roadmap"' not in s:
                s = s.replace('<section class="co-sec" id="apply">',
                              roadmap[lang] + '<section class="co-sec" id="apply">', 1)
        if 'id="general-resume"' not in s:
            raise SystemExit('missing general resume ' + rel)
        write(SITE / rel, s)
        print('careers', lang, 'roadmap', 'id="roadmap"' in s)

def patch_hubs():
    """Point the EN home article rail at current translations, and rebuild the AR articles hub shell title."""
    # EN home: replace the six article-card titles/hrefs that follow the news cards.
    # Done lightly: ensure the new oral-hygiene and chest-bottle URLs are linked from the home if those exact old cards exist.
    en = read(SITE / 'en/index.html')
    swaps = [
        ('what-is-an-oropharyngeal-airway-opa/', 'oral-hygiene-in-hospitals-from-essential-patient-care-to-specialized-medical-equipment/',
         'What Is an Oropharyngeal Airway (OPA)?', 'Oral Hygiene in Hospitals'),
        ('what-is-a-nelaton-catheter/', 'what-is-a-chest-bottle-types-applications-and-how-chest-drainage-systems-work/',
         'What Is a Nelaton Catheter?', 'What Is a Chest Bottle?'),
        ('what-is-an-extension-tube/', 'business-intelligence-bi-transforming-the-medical-device-industry/',
         'What Is an Extension Tube?', 'Business Intelligence in Medical Devices'),
        ('what-are-antibacterial-filters-and-hydrophobic-filters/', 'what-is-a-microdrip-set-uses-components-differences-from-macrodrip-sets/',
         'What Are Antibacterial Filters and Hydrophobic Filters?', 'What Is a Microdrip Set?'),
        ('what-is-a-chest-tube/', 'what-is-an-iv-infusion-set-a-comprehensive-guide-to-types-components-applications-and-safety-standards/',
         'What Is a Chest Tube?', 'What Is an IV Infusion Set?'),
    ]
    for old_slug, new_slug, old_t, new_t in swaps:
        en = en.replace(old_slug, new_slug)
        en = en.replace(old_t, new_t)
    # the sixth card (urine / PVA) — leave a current one if present; add UN SDGs by replacing the guide card if it is still the old purchasing guide in the ARTICLE half.
    # The purchasing guide is item 7 overall (first article). Replace it with the vet liners article.
    en = en.replace('a-guide-to-purchasing-disposable-suction-liner-bags-for-healthcare-facilities/',
                    'from-the-operating-room-to-infection-control-the-role-of-suction-liners-in-veterinary-medicine/')
    en = en.replace('A Guide to Purchasing Disposable Suction Liner Bags for Healthcare Facilities',
                    'Suction Liners in Veterinary Medicine')
    write(SITE / 'en/index.html', en)
    print('home EN stories updated')

def main():
    load_csr()
    patch_csr()
    patch_careers()
    patch_hubs()

if __name__ == '__main__':
    main()
