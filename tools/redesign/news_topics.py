"""Finalist D news & articles taxonomy, multi-category + content-format + audience filters.

Updated Oct 2026 per Boss Orders [t280u] (News 7 categories + 4 format tags)
and [t282u] (Articles 6 categories + 3 content-type tags + 7 audience tags).
"""
import re
from datetime import datetime, timedelta, timezone

from lib import esc, fa, g2j

# ------------------------------------------------------------------ News ([t280u])
# 7 News Categories (multi-category supported via data-cats="cat1,cat2")
TOPICS = (
    ('company', 'شرکت', 'اخبار شرکت', 'Company News', 'أخبار الشركة'),
    ('events', 'نمایشگاه', 'نمایشگاه‌ها و رویدادها', 'Exhibitions & Events', 'المعارض والفعاليات'),
    ('product', 'محصول', 'محصولات و نوآوری', 'Products & Innovation', 'المنتجات والابتكار'),
    ('honor', 'افتخار', 'افتخارات', 'Honors & Achievements', 'الإنجازات والتكريمات'),
    ('partnerships', 'همکاری', 'همکاری‌ها و توسعه بازار', 'Partnerships & Market Development', 'الشراكات وتطوير السوق'),
    ('csr', 'مسئولیت', 'مسئولیت اجتماعی', 'Social Responsibility', 'المسؤولية الاجتماعية'),
    ('industry', 'صنعت', 'صنعت و تشکل‌ها', 'Industry & Associations', 'الصناعة والهيئات'),
    ('education', 'آموزش', 'آموزش و پژوهش', 'Education & Research', 'التعليم والبحث العلمي'),
)

# 4 News Content-Format Tags (برچسب نوع محتوا)
NEWS_FORMATS = (
    ('interview', 'مصاحبه', 'Interview', 'مقابلة'),
    ('report', 'گزارش', 'Report', 'تقرير'),
    ('video', 'ویدئو', 'Video', 'فيديو'),
    ('announcement', 'اطلاعیه', 'Announcement', 'إعلان'),
)

_COPY = {
    'fa': {
        'all': 'همه اخبار', 'years': 'همه سال‌ها', 'before': '۱۴۰۰ و قبل',
        'formats_all': 'همه',
        'h1': 'آخرین <em>اخبار</em>',
        'lead': 'اخبار، گزارش‌ها، مصاحبه‌ها، اطلاعیه‌ها و رویدادهای شرکت دانش‌بنیان مخازن طبی آبادیس',
        'topics_label': 'دسته‌بندی اخبار (امکان حضور یک خبر در چند دسته)',
        'formats_label': 'برچسب نوع محتوا:',
        'years_label': 'سال انتشار',
        'stat_news': 'خبر', 'stat_topics': 'محور خبری', 'stat_years': 'سال پوشش', 'stat_latest': 'تازه‌ترین سال',
        'shown': 'خبر نمایش داده‌شده', 'empty': 'خبری با این ترکیب پیدا نشد.', 'reset': 'نمایش همه اخبار',
        'archive': 'آرشیو اخبار', 'feature': 'تازه‌ترین خبر',
        'card_cta': 'مشاهده متن کامل خبر',
    },
    'en': {
        'all': 'All news', 'years': 'All years', 'before': '1400 and earlier',
        'formats_all': 'All formats',
        'h1': 'Latest <em>news</em>',
        'lead': 'News, reports, interviews, announcements and events from Abadis Medical Reservoirs.',
        'topics_label': 'News Categories',
        'formats_label': 'Content Format:',
        'years_label': 'Year',
        'stat_news': 'stories', 'stat_topics': 'categories', 'stat_years': 'years covered', 'stat_latest': 'Latest year',
        'shown': 'stories shown', 'empty': 'No stories match this combination.', 'reset': 'Show all news',
        'archive': 'News archive', 'feature': 'Latest story',
        'card_cta': 'Read full story',
    },
    'ar': {
        'all': 'كل الأخبار', 'years': 'كل السنوات', 'before': '١٤٠٠ وما قبل',
        'formats_all': 'جميع الأنواع',
        'h1': 'آخر <em>الأخبار</em>',
        'lead': 'أخبار وتقارير ومقابلات وإعلانات وفعاليات خزانات آباديس الطبية.',
        'topics_label': 'تصنيف الأخبار',
        'formats_label': 'نوع المحتوى:',
        'years_label': 'السنة',
        'stat_news': 'خبر', 'stat_topics': 'تصنيفات', 'stat_years': 'سنوات التغطية', 'stat_latest': 'أحدث سنة',
        'shown': 'خبر ظاهر', 'empty': 'لا توجد أخبار لهذا التوليف.', 'reset': 'عرض كل الأخبار',
        'archive': 'أرشيف الأخبار', 'feature': 'أحدث خبر',
        'card_cta': 'قراءة الخبر كاملاً',
    },
}

_AR_DIGITS = str.maketrans('0123456789', '٠١٢٣٤٥٦٧٨٩')
_FA_DIGITS = str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789')
_AR_TO_EN = str.maketrans('٠١٢٣٤٥٦٧٨٩', '0123456789')


def _norm(text):
    t = (text or '').replace('\u200c', ' ').replace('\u0640', '').lower()
    return t.replace('ي', 'ی').replace('ك', 'ک').replace('أ', 'ا').replace('إ', 'ا').replace('آ', 'ا').replace('ة', 'ه')


def digits(n, lang):
    s = str(n)
    if lang == 'en':
        return f'{n:,}'
    grouped = ''
    for i, ch in enumerate(s):
        if i and (len(s) - i) % 3 == 0:
            grouped += '٬'
        grouped += ch
    if lang == 'ar':
        return grouped.translate(_AR_DIGITS)
    return fa(grouped)


def year_label(year, lang):
    """Jalali years stay ungrouped: ۱۴۰۵, not ۱٬۴۰۵."""
    s = str(int(year))
    if lang == 'en':
        return s
    if lang == 'ar':
        return s.translate(_AR_DIGITS)
    return fa(s)


def topic_label(key, lang):
    lang = lang if lang in _COPY else 'fa'
    if key in ('', 'all', None):
        return _COPY[lang]['all']
    for row in TOPICS:
        if row[0] == key or row[1] == key:
            return row[{'fa': 2, 'en': 3, 'ar': 4}[lang]]
    return key


def news_format_label(key, lang):
    lang = lang if lang in _COPY else 'fa'
    if key in ('', 'all', None):
        return _COPY[lang]['formats_all']
    for row in NEWS_FORMATS:
        if row[0] == key:
            return row[{'fa': 1, 'en': 2, 'ar': 3}[lang]]
    return key


def classify_news_cats(title, desc='', body=''):
    """Return 1 or more of the 7 boss categories for a news item."""
    t = _norm((title or '') + ' ' + (desc or ''))
    cats = []

    def add(c):
        if c not in cats:
            cats.append(c)

    # Explicit boss multi-category rules:
    # 1. International negotiations at Iran Health -> نمایشگاه‌ها و رویدادها + همکاری‌ها و توسعه بازار
    if re.search(r'مذاکرات بین ?المللی|international negotiations', t):
        add('events')
        add('partnerships')
    # 2. Meetings with hospital directors / chiefs -> همکاری‌ها و توسعه بازار + مسئولیت اجتماعی
    if re.search(r'روسا|رؤسا|روسای بیمارستان|رؤسای بیمارستان|جلسات مدیران.*بیمارستان', t):
        add('partnerships')
        add('csr')
    # 3. IranMed + Baloot Dalahoo -> مسئولیت اجتماعی + نمایشگاه‌ها و رویدادها + همکاری‌ها و توسعه بازار
    if re.search(r'بلوط دالاهو|baloot', t):
        add('csr')
        add('events')
        add('partnerships')

    # Company News (اخبار شرکت)
    if re.search(r'کارخانه|شمس آباد|بازسازی|استخدام|سرمایه های انسانی|نسل چهارم و پنجم|هوش تجاری|پروانه بهره برداری|دانش بنیان شد|کدینگ محصولات|سال تحصیلی|جنگ رمضان|تداوم خدمت رسانی|ارسال ۸ خاور|بحران کرونا|قرعه کشی|برندگان|چرا .* حضور پیدا نکرد|انتشار کتاب|صندوق ایده|نشست تخصصی|factory|human capital|hiring|business intelligence|marketing|corona|covid|شركه آباديس|قرعه|يانصيب|مسابقه|انشطه آباديس', t):
        add('company')

    # Industry & Associations (صنعت و تشکل‌ها)
    if re.search(r'انجمن|اتحادیه|تشکل|امدال|امدل|اساسنامه|انتخابات|مجمع|نامه سرگشاده|مطالبات معوق|چالش های مالی در صنعت|تولید پایدار در شرایط بحرانی|تاریخ شفاهی صنعت|تمپا|سندیکا|صنفی|association|union|amedal|syndicate|نقابه|اتحاد', t):
        add('industry')

    # Exhibitions & Events (نمایشگاه‌ها و رویدادها)
    if re.search(r'نمایشگاه|کنگره|همایش|ایران هلث|ایران مد|ایران کلین|سلامت بنیان|ازبکستان|غرفه|دعوت نامه.*کنگره|دعوت نامه.*نمایشگاه|iran health|iranmed|iranclean|salamat bonyan|exhibition|congress|expo|uzmed|uzbek|معرض|موتمر|كونغرس', t):
        add('events')

    # Products & Innovation (محصولات و نوآوری)
    if re.search(r'رونمایی|رو نمایی|محصول جدید|محصولات جدید|فیلتراسیون|فیلتر|کدینگ محصولات|فیکسر|کیسه ساکشن|مخزن ساکشن|تیوب|ساکشن تیوب|اکسسوری|هوش تجاری|هوش مصنوعی|بازاریابی نسل چهارم|باتل ساکشن|وسایل یکبار مصرف|تغییر در طراحی|کیفیت بالا|بیانیه کیفی|پلیمر|pva|suction|filter|filtration|canister|fixer|tube|unveil|new product|coding|business intelligence|artificial intelligence|منتج|فلتر|شفط|حامل|تثبیت', t):
        add('product')
    elif re.search(r'تا ثریا|رادي?و سلامت|صدا و سیما|صداوسیما|عصر خانواده|ta soraya|radio salamat', t):
        # Product & domestic innovation interviews
        add('product')

    # Honors & Achievements (افتخارات)
    if re.search(r'افتخار|گواهی|گواهینامه|پروانه بهره|دانش بنیان شد|اختراع|جایزه|فعال ترین شرکت|فعالترین شرکت|برگزیده|نخستین شرکت.*مجهز|صرفه جویی ۴۰ میلیون|تکمیل کرد|دستاورد|certificate|patent|\baward\b|ce certification|achievements|knowledge-based|شهاده|براءه|جائزه|قائمه علی المعرفه', t):
        add('honor')

    # Partnerships & Market Development (همکاری‌ها و توسعه بازار)
    if re.search(r'همکاری|مذاکرات|اتاق بازرگانی|عمان|ازبکستان|صادرات|توسعه بازار|شریک تجاری|پیام گستر|crm talk|نصب و راه اندازی|تجهیز بیمارستان|تجهیز دو مرکز|نماینده آبادیس|واسط همکاری|دیدار معاونت بازرگانی|استخدام کارشناس فروش|صندوق سرمایه گذاری|negotiation|cooperation|chamber of commerce|export|uzbekistan|uzmedexpo|investment fund|شراکه|تعاون|غرفه التجاره|تصدیر|صندوق استثمار', t):
        add('partnerships')

    # Social Responsibility (مسئولیت اجتماعی)
    if re.search(r'مسئولیت اجتماعی|زاگرس|زاغروس|بلوط|درخت|توسعه پایدار|حکمرانی سبز|محیط زیست|صرفه جویی.*آب|روز پرستار|روز خبرنگار|جنگ رمضان|ارسال ۸ خاور|در روزهای آغازین جنگ|بحران کرونا|کرونا|نکوداشت|پروفسور.*محرابی|آغاز سال تحصیلی|حال خوش مهر|بازسازی کارخانه.*حادثه|قرعه کشی|مسابقه|برندگان|zagros|oak|sustainab|green governance|water conservation|environment|nurse|corona|covid|professor.*mehrabi|مسؤولیه اجتماعیه|بیئه|استدامه|تمریض|کورونا|یانصیب|مسابقه', t):
        add('csr')

    # Education & Research (آموزش و پژوهش)
    if re.search(r'آموزش|پژوهش|وبینار|کارگاه|آکادمی|مقاله|کنفرانس|ژورنال|isi|medium|تحلیل کیفی|تحلیل آماری|کار آماری|نظرسنجی|سرمایه های انسانی|کتاب|راهنما|پاتوژن|عفونت های بیمارستانی|مهندسی پزشکی|journal|article|isi|medium|webinar|workshop|academy|research|human capital|survey|statistical|guideline|nosocomial|pathogen|تعلیم|بحث|مقاله|ندوه|ورشه|اکادیمیه', t):
        add('education')

    if not cats:
        add('company')
    return cats


def classify_news_formats(title, desc='', blocks=None, body=''):
    """Return 1 or more of the 4 format tags: interview, report, video, announcement."""
    t = _norm((title or '') + ' ' + (desc or ''))
    b = _norm(body or '')
    fmts = []

    def add(f):
        if f not in fmts:
            fmts.append(f)

    has_vid = False
    if blocks:
        for blk in blocks:
            s = str(blk).lower()
            if blk.get('t') == 'aparat' or 'aparat' in s or '<video' in s or 'فیلم' in s or 'تیزر' in s or 'ویدئو' in s or 'ویدیو' in s:
                has_vid = True
                break
    if has_vid or re.search(r'ویدئو|ویدیو|فیلم|تیزر|نماهنگ|گزارش تصویری|video|photo story|photo report|تقرير مصور|فیدیو', t + ' ' + b):
        add('video')

    if re.search(r'مصاحبه|گفت و گو|گفت وگو|گفتگو|رادیو|صدا و سیما|صداوسیما|برنامه «عصر خانواده»|برنامه «تا ثریا»|crm talk|دیدگاه|نظرات دکتر|واکنش به مصاحبه|interview|radio|مقابله|اذاعه', t):
        add('interview')

    if re.search(r'دعوت نامه|دعوت به|اطلاعیه|بیانیه|نامه سرگشاده|فراخوان|استخدام|صادر گردید|دانش بنیان شد|اخذ گواهی|برگزار می شود|برگزار میشود|برندگان|اسامی برندگان|قرعه کشی|معرفی کدینگ|انتشار کتاب|افتتاح|invitation|announcement|statement|hiring|obtaining|unveiling|unveils|اعلان|دعوه|الکشف عن|افتتاح|اسماء الفائزین|الخبر العاجل', t):
        add('announcement')

    if re.search(r'گزارش|تحلیل|بررسی|بازخورد|بازتاب|برگزار شد|ارائه شد|ارائه کرد|منتشر شد|انتشار مقاله|چاپ مقاله|حضور آبادیس|حضور شرکت|حضور نماینده|مجمع|انتخابات|دیدار|جلسات|جلسه|مذاکرات|مراسم|تداوم خدمت رسانی|آغاز فوری|ارسال ۸ خاور|تکمیل کرد|مجهز به هوش تجاری شد|فعالیت های آبادیس|نگاهی به|چرا .* حضور پیدا نکرد|report|analysis|presence|participation|published|publishes|activities|ceremony|negotiations|تقرير|حضور|مشارکه|انشطه|تغطیه', t):
        add('report')

    if not fmts:
        add('report')
    return fmts


def news_meta_for(title, desc='', blocks=None, body='', lang='fa'):
    lang = lang if lang in _COPY else 'fa'
    T = _COPY[lang]
    cats = classify_news_cats(title, desc, body)
    fmts = classify_news_formats(title, desc, blocks=blocks, body=body)
    primary_cat = cats[0]
    cat_labels = [topic_label(c, lang) for c in cats]
    # Primary format badge: prefer interview / video / announcement when present so distinct formats stand out
    primary_fmt = fmts[0]
    for pref in ('interview', 'video', 'announcement', 'report'):
        if pref in fmts:
            primary_fmt = pref
            break
    fmt_labels = [news_format_label(f, lang) for f in fmts]
    return {
        'topic': primary_cat,
        'cats': cats,
        'cats_csv': ','.join(cats),
        'cat_labels': cat_labels,
        'format': primary_fmt,
        'formats': fmts,
        'formats_csv': ','.join(fmts),
        'format_label': news_format_label(primary_fmt, lang),
        'format_labels': fmt_labels,
        'card_cta': T['card_cta'],
    }


def classify_text(text):
    """Back-compat primary topic helper."""
    return classify_news_cats(text)[0]


def jalali_year_of(iso):
    if not iso:
        return 0
    try:
        d = datetime.fromisoformat(str(iso).replace('Z', '+00:00'))
    except ValueError:
        return 0
    if d.tzinfo is None:
        d = d.replace(tzinfo=timezone.utc)
    d = d.astimezone(timezone(timedelta(hours=3, minutes=30)))
    y, _m, _d = g2j(d.year, d.month, d.day)
    return y


def year_bucket(year):
    """1405…1401 stay separate. 1400 and earlier share one pill. 0 means unknown."""
    try:
        year = int(year)
    except (TypeError, ValueError):
        return 'before'
    if year >= 1401:
        return str(year)
    return 'before'


def parse_year_token(token):
    raw = str(token or '').translate(_FA_DIGITS).translate(_AR_TO_EN)
    m = re.search(r'(13|14)\d\d', raw)
    return int(m.group(0)) if m else 0


def _year_pills(lang, counts):
    """counts: bucket -> n. Always offer 1405…1401 plus «1400 and earlier»."""
    T = _COPY[lang]
    order = []
    newer = sorted((int(k) for k in counts if str(k).isdigit() and int(k) > 1405), reverse=True)
    order.extend(str(y) for y in newer)
    order.extend(['1405', '1404', '1403', '1402', '1401', 'before'])
    buttons = [f'<button type="button" data-news-year="all" aria-pressed="true">{esc(T["years"])}</button>']
    for key in order:
        n = counts.get(key, 0)
        label = T['before'] if key == 'before' else year_label(int(key), lang)
        buttons.append(
            f'<button type="button" data-news-year="{esc(key)}" aria-pressed="false">{label} <b>{digits(n, lang)}</b></button>'
        )
    return ''.join(buttons)


def _topic_buttons(lang, counts, total):
    T = _COPY[lang]
    bits = [
        f'<button type="button" data-news-topic="all" aria-pressed="true"><span>{esc(T["all"])}</span> <b>{digits(total, lang)}</b></button>'
    ]
    for key, _short, _fa, _en, _ar in TOPICS:
        bits.append(
            f'<button type="button" data-news-topic="{key}" aria-pressed="false"><span>{esc(topic_label(key, lang))}</span> <b>{digits(counts.get(key, 0), lang)}</b></button>'
        )
    return ''.join(bits)


def _format_buttons(lang, counts, total):
    T = _COPY[lang]
    bits = [
        f'<button type="button" class="news-yr" data-news-format="all" aria-pressed="true"><span>{esc(T["formats_all"])}</span> <b>{digits(total, lang)}</b></button>'
    ]
    for key, _fa, _en, _ar in NEWS_FORMATS:
        bits.append(
            f'<button type="button" class="news-yr" data-news-format="{key}" aria-pressed="false"><span>{esc(news_format_label(key, lang))}</span> <b>{digits(counts.get(key, 0), lang)}</b></button>'
        )
    return ''.join(bits)


def tally(pairs):
    """pairs: iterable of (cats_or_topic, year_bucket) or (cats_list, year_bucket, formats_list)."""
    topics, years, formats = {}, {}, {}
    distinct = set()
    total = 0
    for item in pairs:
        total += 1
        if len(item) == 3:
            cats_val, bucket, fmts_val = item
        else:
            cats_val, bucket = item
            fmts_val = ['report']
        cats_list = [cats_val] if isinstance(cats_val, str) else list(cats_val or [])
        fmts_list = [fmts_val] if isinstance(fmts_val, str) else list(fmts_val or [])
        for c in cats_list:
            if c:
                topics[c] = topics.get(c, 0) + 1
        for f in fmts_list:
            if f:
                formats[f] = formats.get(f, 0) + 1
        years[bucket] = years.get(bucket, 0) + 1
        if str(bucket).isdigit():
            distinct.add(int(bucket))
        else:
            distinct.add(1400)
    latest = max(distinct) if distinct else 0
    return {
        'total': total,
        'topics': topics,
        'formats': formats,
        'years': years,
        'n_years': len(distinct),
        'latest': latest,
        'n_topics': len(TOPICS),
    }


def news_shell(lang, prefix, crumbs, stats, feature_html):
    """Hero + filter chrome. The card grid is appended by the caller."""
    lang = lang if lang in _COPY else 'fa'
    T = _COPY[lang]
    dash = (
        f'<ul class="news-dash">'
        f'<li><b>{digits(stats["total"], lang)}</b><span>{esc(T["stat_news"])}</span></li>'
        f'<li><b>{digits(stats["n_topics"], lang)}</b><span>{esc(T["stat_topics"])}</span></li>'
        f'<li><b>{digits(stats["n_years"], lang)}</b><span>{esc(T["stat_years"])}</span></li>'
        f'<li><b>{year_label(stats["latest"], lang) if stats["latest"] else "—"}</b><span>{esc(T["stat_latest"])}</span></li>'
        f'</ul>'
    )
    news_slogan = {
        'fa': ('تازه‌ترین اخبار، گزارش‌ها و رویدادهای آبادیس،', 'پوشش نمایشگاه‌ها، کنگره‌ها و مجامع تخصصی', 'رونمایی از محصولات و دستاوردهای دانش‌بنیان', 'مسئولیت اجتماعی، نجات زاگرس و توسعه بازار.'),
        'en': ('Latest News, Reports & Events at Abadis Med,', 'Medical Exhibitions, Congresses & Industry Forums', 'Product Unveilings & Knowledge-Based Milestones', 'Social Responsibility, Save Zagros & Global Growth.'),
        'ar': ('آخر أخبار وتقارير وفعاليات شركة آباديس،', 'تغطية المعارض والمؤتمرات والملتقيات التخصصية', 'الكشف عن المنتجات والإنجازات المعرفية', 'المسؤولية الاجتماعية وإنقاذ زاغروس وتطوير السوق.'),
    }[lang]
    return f'''<section class="page-hero about-hero articles-hero">
  <video class="about-hero-video articles-hero-video" autoplay muted loop playsinline webkit-playsinline disablepictureinpicture disableremoteplayback preload="metadata" tabindex="-1" aria-hidden="true" poster="{prefix}assets/media/hero-or-zagros-poster.jpg?v=20261028p"><source src="{prefix}assets/media/hero-or-zagros.mp4?v=20261028p" type="video/mp4"></video>
  <div class="wrap about-hero-grid">
    <div>{crumbs}
      <h1>{T["h1"]}</h1>
      <p class="slogan reveal" aria-label="{esc(' '.join(news_slogan))}"><span class="slogan-line" style="--i:0">{esc(news_slogan[0])}</span><span class="slogan-line" style="--i:1">{esc(news_slogan[1])}</span><span class="slogan-line" style="--i:2">{esc(news_slogan[2])}</span><span class="slogan-line" style="--i:3">{esc(news_slogan[3])}</span></p>
    </div>
  </div>
</section>
<section class="news-d articles-d" data-news-finalist>
  <div class="wrap">
    <div class="news-d-stage">
      {feature_html}
      <aside class="news-panel">
        {dash}
        <p class="news-lab">{esc(T["topics_label"])}</p>
        <div class="news-topics" role="group" aria-label="{esc(T["topics_label"])}">{_topic_buttons(lang, stats["topics"], stats["total"])}</div>
        <div class="ao-extra-filters" role="group" aria-label="{esc(T["formats_label"])}">
          <span class="ao-filter-label">{esc(T["formats_label"])}</span>
          {_format_buttons(lang, stats.get("formats", {}), stats["total"])}
        </div>
        <p class="news-lab">{esc(T["years_label"])}</p>
        <div class="news-years" role="group" aria-label="{esc(T["years_label"])}">{_year_pills(lang, stats["years"])}</div>
        <p class="news-live"><span data-news-count>{digits(stats["total"], lang)}</span> {esc(T["shown"])}</p>
      </aside>
    </div>
  </div>
</section>
<section class="section news-d-page"><div class="wrap">
    <h2 class="news-archive-title">{esc(T["archive"])}</h2>'''


def empty_html(lang):
    T = _COPY[lang if lang in _COPY else 'fa']
    return (
        f'<p class="news-empty" data-news-empty hidden>{esc(T["empty"])} '
        f'<button type="button" data-news-reset>{esc(T["reset"])}</button></p>'
    )


def feature_from_card(card_html, lang):
    """Server-render the lead card from the first archive card. JS replaces it on filter."""
    lang = lang if lang in _COPY else 'fa'
    T = _COPY[lang]
    href = re.search(r'href="([^"]+)"', card_html or '')
    img = re.search(r'<img[^>]*src="([^"]+)"', card_html or '')
    alt = re.search(r'<h3>(.*?)</h3>', card_html or '')
    excerpt = re.search(r'<p>(.*?)</p>', card_html or '')
    time_m = re.search(r'<time([^>]*)>(.*?)</time>', card_html or '')
    fmt_m = re.search(r'class="news-fmt-badge[^"]*"[^>]*>([^<]+)</span>', card_html or '')
    cat_m = re.search(r'class="art-card-badge"[^>]*>([^<]+)</span>', card_html or '')
    title = alt.group(1) if alt else ''
    src = img.group(1) if img else ''
    time_html = f'<time{time_m.group(1)}>{time_m.group(2)}</time>' if time_m else ''
    kicker = T['feature']
    fmt_txt = fmt_m.group(1) if fmt_m else news_format_label('report', lang)
    cat_txt = cat_m.group(1) if cat_m else topic_label('events', lang)
    img_html = f'<img src="{src}" alt="{esc(re.sub(r"<[^>]+>", "", title))}" decoding="async">' if src else ''
    return (
        f'<a class="news-feature" data-news-feature href="{href.group(1) if href else "#"}">'
        f'{img_html}<div class="news-feature-body">'
        f'<div class="news-feature-tags">'
        f'<span class="news-kicker" data-news-kicker data-default="{esc(kicker)}">{esc(kicker)}</span>'
        f'<span class="art-aud-tag" data-news-feat-cat>{esc(cat_txt)}</span>'
        f'<span class="news-fmt-pill" data-news-feat-fmt>{esc(fmt_txt)}</span>'
        f'</div>'
        f'{time_html}<h2>{title}</h2><p>{excerpt.group(1) if excerpt else ""}</p></div></a>'
    )


# ------------------------------------------------------------------ Articles ([t282u])
# 6 Article Categories (multi-category supported via data-cats="cat1,cat2")
ARTICLE_TOPICS = (
    ('abadis_products', 'محصولات آبادیس', 'محصولات آبادیس', 'Abadis Products', 'منتجات آباديس'),
    ('infection_safety', 'کنترل عفونت', 'کنترل عفونت و ایمنی بیمار', 'Infection Control & Patient Safety', 'مكافحة العدوى وسلامة المرضى'),
    ('medical_equipment', 'تجهیزات پزشکی', 'تجهیزات و ملزومات پزشکی', 'Medical Equipment & Supplies', 'المعدات والمستلزمات الطبية'),
    ('quality_standards', 'استانداردها', 'کیفیت و استانداردها', 'Quality & Standards', 'الجودة والمعايير'),
    ('env_sustainability', 'محیط زیست', 'محیط زیست و توسعه پایدار', 'Environment & Sustainable Development', 'البيئة والتنمية المستدامة'),
    ('health_management', 'مدیریت سلامت', 'مدیریت صنعت سلامت', 'Healthcare Industry Management', 'إدارة صناعة الرعاية الصحية'),
)

# 3 Article Content-Type Tags (برچسب نوع محتوا)
ARTICLE_CTYPES = (
    ('research', 'پژوهشی', 'Research', 'بحثي'),
    ('educational', 'آموزشی', 'Educational', 'تعليمي'),
    ('buying_guide', 'راهنمای خرید', 'Buying Guide', 'دليل الشراء'),
)

# 7 Article Audience Tags (برچسب مخاطبین — multi-audience supported via data-audiences="aud1,aud2")
ARTICLE_AUDIENCES = (
    ('clinical_staff', 'کادر درمان', 'Clinical Staff', 'الكادر الطبي والتمريضي'),
    ('infection_specialists', 'کارشناسان کنترل عفونت', 'Infection Control Specialists', 'أخصائيو مكافحة العدوى'),
    ('env_health', 'کارشناسان بهداشت محیط', 'Environmental Health Specialists', 'أخصائيو صحة البيئة'),
    ('biomed_specialists', 'کارشناسان تجهیزات پزشکی', 'Medical Equipment Specialists', 'مهندسو وأخصائيو المعدات الطبية'),
    ('procurement', 'مسئولان خرید و تدارکات', 'Procurement & Purchasing Officers', 'مسؤولو المشتريات والتوريد'),
    ('medtech_execs', 'مدیران شرکت‌های تجهیزات پزشکی', 'Medical Device Company Executives', 'مديرو شركات المعدات الطبية'),
    ('students_researchers', 'دانشجویان و پژوهشگران', 'Students & Researchers', 'الطلاب والباحثون'),
)

_ARTICLE_COPY = {
    'fa': {
        'all': 'همه مقالات', 'years': 'همه سال‌ها', 'before': '۱۴۰۰ و قبل',
        'h1': 'دانشنامه و <em>مقالات علمی</em>',
        'lead': 'مقالات علمی، پژوهشی، آموزشی و راهنماهای خرید تخصصی تجهیزات پزشکی و کنترل عفونت آبادیس',
        'slogan_aria': 'دانشنامه تخصصی و مقالات علمی آبادیس، کنترل عفونت و ایمنی بیمارستان، استانداردهای نوین تجهیزات پزشکی، راهنمای جامع مدیران و کادر درمان',
        'slogan_0': 'دانشنامه تخصصی و مقالات علمی آبادیس،',
        'slogan_1': 'کنترل عفونت و ایمنی بیمارستان',
        'slogan_2': 'استانداردهای نوین تجهیزات پزشکی',
        'slogan_3': 'راهنمای جامع مدیران و کادر درمان',
        'topics_label': 'محور علمی و تخصصی',
        'ctype_label': 'نوع محتوا:',
        'ctype_all': 'همه',
        'aud_label': 'مخاطب:',
        'aud_all': 'همه مخاطبان',
        'years_label': 'سال انتشار',
        'rtime_label': 'زمان مطالعه:', 'rtime_all': 'همه',
        'rtime_fast': 'مطالعه سریع (زیر ۳ دقیقه)', 'rtime_deep': 'مقالات جامع (بالای ۴ دقیقه)',
        'stat_news': 'مقاله تخصصی', 'stat_topics': 'محور علمی', 'stat_years': 'سال پوشش', 'stat_latest': 'تازه‌ترین سال',
        'shown': 'مقاله علمی نمایش داده‌شده', 'empty': 'مقاله‌ای با این ترکیب پیدا نشد.', 'reset': 'نمایش همه مقالات',
        'archive': 'آرشیو مقالات علمی، پژوهشی و آموزشی', 'feature': 'تازه‌ترین مقاله علمی',
        'card_cta': 'مطالعه کامل مقاله علمی',
    },
    'en': {
        'all': 'All articles', 'years': 'All years', 'before': '1400 and earlier',
        'h1': 'Knowledge Hub & <em>Scientific Articles</em>',
        'lead': 'Research, educational articles, buying guides, infection-control standards and medical equipment insights from Abadis.',
        'slogan_aria': 'Abadis Med Knowledge Hub and Scientific Articles, Hospital Infection Control and Safety, Modern Medical Device Standards, Guide for Clinicians and Healthcare Leaders',
        'slogan_0': 'Abadis Med Knowledge Hub & Scientific Articles,',
        'slogan_1': 'Hospital Infection Control & Safety',
        'slogan_2': 'Modern Medical Device Standards',
        'slogan_3': 'Guide for Clinicians & Healthcare Leaders',
        'topics_label': 'Article Categories (6 Pillars)',
        'ctype_label': 'Content Type:',
        'ctype_all': 'All types',
        'aud_label': 'Target Audiences:',
        'aud_all': 'All audiences',
        'years_label': 'Publication Year',
        'rtime_label': 'Reading time:', 'rtime_all': 'All',
        'rtime_fast': 'Quick read (≤3 min)', 'rtime_deep': 'In-depth (4+ min)',
        'stat_news': 'articles', 'stat_topics': 'categories', 'stat_years': 'years covered', 'stat_latest': 'Latest year',
        'shown': 'articles shown', 'empty': 'No articles match this combination.', 'reset': 'Show all articles',
        'archive': 'Scientific Articles Archive', 'feature': 'Latest Article',
        'card_cta': 'Read scientific article',
    },
    'ar': {
        'all': 'كل المقالات', 'years': 'كل السنوات', 'before': '١٤٠٠ وما قبل',
        'h1': 'الموسوعة و<em>المقالات العلمية</em>',
        'lead': 'مقالات بحثية وتعليمية وأدلة شراء ومعايير مكافحة العدوى والمعدات الطبية من آباديس.',
        'slogan_aria': 'الموسوعة المتخصصة والمقالات العلمية في آباديس، مكافحة العدوى وسلامة المستشفيات، المعايير الحديثة للأجهزة الطبية، دليل شامل للكوادر الطبية والمديرين',
        'slogan_0': 'الموسوعة المتخصصة والمقالات العلمية في آباديس،',
        'slogan_1': 'مكافحة العدوى وسلامة المستشفيات',
        'slogan_2': 'المعايير الحديثة للأجهزة الطبية',
        'slogan_3': 'دليل شامل للكوادر الطبية والمديرين',
        'topics_label': 'تصنيف المقالات (٦ محاور)',
        'ctype_label': 'نوع المحتوى:',
        'ctype_all': 'جميع الأنواع',
        'aud_label': 'الجمهور المستهدف:',
        'aud_all': 'جميع الفئات',
        'years_label': 'سنة النشر',
        'rtime_label': 'وقت القراءة:', 'rtime_all': 'الكل',
        'rtime_fast': 'قراءة سريعة (≤٣ دقائق)', 'rtime_deep': 'مقال شامل (٤+ دقائق)',
        'stat_news': 'مقالة علمية', 'stat_topics': 'تصنيفات علمية', 'stat_years': 'سنوات التغطية', 'stat_latest': 'أحدث سنة',
        'shown': 'مقالة علمية', 'empty': 'لا توجد مقالات لهذا التوليف.', 'reset': 'عرض كل المقالات',
        'archive': 'أرشيف المقالات العلمية', 'feature': 'أحدث مقالة علمية',
        'card_cta': 'قراءة المقال العلمي',
    },
}


def article_topic_label(key, lang):
    lang = lang if lang in _ARTICLE_COPY else 'fa'
    if key in ('', 'all', None):
        return _ARTICLE_COPY[lang]['all']
    for row in ARTICLE_TOPICS:
        if row[0] == key or row[1] == key:
            return row[{'fa': 2, 'en': 3, 'ar': 4}[lang]]
    return key


def article_ctype_label(key, lang):
    lang = lang if lang in _ARTICLE_COPY else 'fa'
    if key in ('', 'all', None):
        return _ARTICLE_COPY[lang]['ctype_all']
    for row in ARTICLE_CTYPES:
        if row[0] == key:
            return row[{'fa': 1, 'en': 2, 'ar': 3}[lang]]
    return key


def article_audience_label(key, lang):
    lang = lang if lang in _ARTICLE_COPY else 'fa'
    if key in ('', 'all', None):
        return _ARTICLE_COPY[lang]['aud_all']
    for row in ARTICLE_AUDIENCES:
        if row[0] == key:
            return row[{'fa': 1, 'en': 2, 'ar': 3}[lang]]
    return key


def classify_article_cats(title, desc='', body=''):
    """Return 1 or more of the 6 boss article categories."""
    t = _norm((title or '') + ' ' + (desc or ''))
    cats = []

    def add(c):
        if c not in cats:
            cats.append(c)

    # 1. محصولات آبادیس (abadis_products)
    if re.search(r'آبادیس|ابادیس|کیسه ساکشن|کیسه های یکبار مصرف ساکشن|باتل ساکشن|مخزن ساکشن|مخازن ساکشن|ساکشن تیوب|لوله ساکشن|فیلترهای آبادیس|فیلتر انتی باکتریال|فیلتر هیدروفوبیک|فیلتر متخلخل|فیلترهای کیسه ساکشن|فیکسر|نگهدارنده لوله تراشه|فینگرتیپ|رابط ساکشن|گیره t|رسیور پزشکی|راهنمای نصب مخازن|رگولاتور ساکشن|فیلم pva|پودر جاذب|abadis|suction liner|suction bag|suction canister|suction tube|antibacterial filter|porous filter|endotracheal tube|pva film|super absorbent', t):
        add('abadis_products')

    # 2. کنترل عفونت و ایمنی بیمار (infection_safety)
    if re.search(r'عفونت|پاتوژن|هانتا|کرونا|کووید|بهداشت دست|پنومونی|پریتونیت|آنتی بیوتیک|انتی بیوتیک|مقاومت میکروبی|ضدعفونی|ضد عفونی|استریل|حفاظت فردی|مواجهات شغلی|ایمنی|جان بیماران|تثبیت|نگهدارنده لوله تراشه|شست و شوی مخازن|پساب های عفونی|پسماندهای عفونی|پسماند های عفونی|infection|nosocomial|pathogen|hantavirus|corona|covid|hand hygiene|disinfection|steril|safety', t):
        add('infection_safety')

    # 3. تجهیزات و ملزومات پزشکی (medical_equipment)
    if re.search(r'دستگاه ساکشن|ساکشن دیواری|ساکشن مرکزی|ساکشن پرتابل|انواع دستگاه ساکشن|لوله هوا|ایروی|سوند نلاتون|اکستنشن تیوب|چست تیوب|تزریق چربی|منسوجات پزشکی|تجهیزات پزشکی پلیمری|تجهیزات پزشکی مصرفی|ملزومات پزشکی|تجهیزات و ملزومات پزشکی|وسایل یکبار مصرف پزشکی|رگولاتور|فینگرتیپ|رسیور|فیلتر|پودر جاذب|فیلم pva|suction device|wall suction|airway|opa|nelaton|extension tube|chest tube|equipment|consumable', t):
        add('medical_equipment')

    # 4. کیفیت و استانداردها (quality_standards)
    if re.search(r'استاندارد|ایزو|\biso\b|مدیکال گرید|pvc|کلاس خطر|طبقه بندی تجهیزات پزشکی|t1 تا t4|لیبل اصالت|با کیفیت|دستورالعمل اجرایی|پروتکل جامع|توصیه نامه|شاخص های میکروبی|شاخص های کنترل عفونت|فرآوری مجدد|standard|quality|medical-grade|guideline|protocol', t):
        add('quality_standards')

    # 5. محیط زیست و توسعه پایدار (env_sustainability)
    if re.search(r'محیط زیست|زیست محیطی|توسعه پایدار|حکمرانی سبز|صرفه جویی در مصرف آب|صرفه جویی.*آب|پسماند|زباله|فاضلاب|تصفیه خانه|پلاستیکی|فیلم pva|فتوکاتالیستی|environment|sustainab|green governance|waste|wastewater|effluent|water conservation|pva', t):
        add('env_sustainability')

    # 6. مدیریت صنعت سلامت (health_management)
    if re.search(r'هوش تجاری|مدیریت نقدینگی|تصمیم گیری تولید|شرکت های دانش بنیان|صنایع دانش بنیان|اتحادیه ها و تشکل ها|نمایشگاه های تجهیزات پزشکی|رویدادها و نمایشگاه|برترین شرکت های تجهیزات پزشکی|رسانه ها در صنعت سلامت|سایت های اینترنتی خرید|معرفی سایت های معتبر|معرفی رشته|ژورنال معتبر|مقرون به صرفه|قیمت کیسه ساکشن|راهنمای خرید|مدیریت مصرف|فرصت های تولید داخل|purchasing|cost-effective|journals|industry|management|business intelligence', t):
        add('health_management')

    if not cats:
        add('medical_equipment')
    return cats


def classify_article_text(text):
    """Back-compat single topic return."""
    return classify_article_cats(text)[0]


def classify_article_ctype(title, desc='', body=''):
    """Return 1 of the 3 content-type tags: research, educational, buying_guide."""
    t = _norm((title or '') + ' ' + (desc or ''))
    if re.search(r'راهنمای خرید|قیمت کیسه ساکشن|راهنمای جامع انتخاب|ساکشن مرکزی یا ساکشن پرتابل|مقرون به صرفه|سایت های اینترنتی خرید|لیبل اصالت|با کیفیت|تجهیزات پزشکی مصرفی و ملزومات|چرا کیسه ساکشن|راهنمای انتخاب سایز|purchasing|buying guide|cost-effective|prefer disposable|high quality|top 5 features', t):
        return 'buying_guide'
    if re.search(r'بررسی|ارزیابی|مطالعه موردی|مقایسه ای|الگوی مقاومت|فراوانی پنومونی|میزان دانش|تحقق حکمرانی سبز|تصفیه فاضلاب|ارتقا فرایند بیولوژیک|بهبود اثرات زیست محیطی|هانتاویروس|گزارش توسعه پایدار|بروز عفونت بیمارستانی|حذف انتی بیوتیک|مواجهات شغلی|تبعیت از دستورالعمل|سند تعهد|assessment|evaluation|case study|improving the environmental|hantavirus|sustainability report|surveillance', t):
        return 'research'
    return 'educational'


def classify_article_audiences(title, desc='', cats=None, ctype=''):
    """Return 1 or more of the 7 audience tags for an article."""
    t = _norm((title or '') + ' ' + (desc or ''))
    cats = cats or []
    auds = []

    def add(a):
        if a not in auds:
            auds.append(a)

    # 1. کادر درمان (clinical_staff)
    if re.search(r'پرستار|پزشک|اتاق عمل|اورژانس|icu|مراقبت|بیمار|لوله تراشه|ایروی|نلاتون|چست تیوب|اکستنشن|تزریق چربی|ساکشن|بهداشت دست|دندانپزشکی|کووید|کرونا|هانتا|پنومونی|پریتونیت|مواجهات شغلی|حفاظت فردی|patient|nurse|clinical|airway|opa|nelaton|chest tube|suction|hand hygiene|corona', t):
        add('clinical_staff')

    # 2. کارشناسان کنترل عفونت (infection_specialists)
    if 'infection_safety' in cats or re.search(r'کنترل عفونت|عفونت|پاتوژن|ضدعفونی|استریل|فیلتر|پسماند عفونی|هانتا|کرونا|کووید|مقاومت|ونتیلاتور|پریتونیت|infection|pathogen|disinfection|steril|hantavirus', t):
        add('infection_specialists')

    # 3. کارشناسان بهداشت محیط (env_health)
    if 'env_sustainability' in cats or re.search(r'بهداشت محیط|پسماند|زباله|فاضلاب|تصفیه|آب ورودی|میکروبی و شیمیایی|پساب|محیط زیست|شست و شوی مخازن|uvc|waste|wastewater|effluent|environment|water conservation', t):
        add('env_health')

    # 4. کارشناسان تجهیزات پزشکی (biomed_specialists)
    if 'medical_equipment' in cats or 'abadis_products' in cats or 'quality_standards' in cats or re.search(r'مهندسی پزشکی|تجهیزات پزشکی|ساکشن دیواری|ساکشن مرکزی|ساکشن پرتابل|رگولاتور|فیلتر|مخزن|تیوب|نصب مخازن|استاندارد|ایزو|کلاس خطر|t1 تا t4|لیبل اصالت|equipment|device|canister|filter|tube|standard', t):
        add('biomed_specialists')

    # 5. مسئولان خرید و تدارکات (procurement)
    if ctype == 'buying_guide' or re.search(r'خرید|قیمت|مقرون به صرفه|تدارکات|ملزومات|مصرفی|لیبل اصالت|سایت های اینترنتی|کدینگ|انتخاب سیستم ساکشن|purchasing|cost-effective|consumable', t):
        add('procurement')

    # 6. مدیران شرکت‌های تجهیزات پزشکی (medtech_execs)
    if 'health_management' in cats or re.search(r'هوش تجاری|نقدینگی|تولید|شرکت های تجهیزات پزشکی|دانش بنیان|اتحادیه|تشکل|نمایشگاه|صنعت تجهیزات پزشکی|صنعت سلامت|ایزو|طبقه بندی|توسعه پایدار|حکمرانی سبز|برترین شرکت|پلیمر|pvc|pva|پودر جاذب|industry|knowledge-based|exhibition|pva|polymer', t):
        add('medtech_execs')

    # 7. دانشجویان و پژوهشگران (students_researchers)
    if ctype == 'research' or re.search(r'مقاله|پژوهش|ژورنال|معرفی رشته|مهندسی پزشکی|پرستاری|سایت های معتبر|تاریخچه|تعریف|بررسی|ارزیابی|مقایسه|نانو|فتوکاتالیستی|journal|research|study|assessment', t):
        add('students_researchers')

    if not auds:
        add('clinical_staff')
        add('biomed_specialists')
    return auds


def article_meta_for(title, desc, body_text='', lang='fa'):
    lang = lang if lang in _ARTICLE_COPY else 'fa'
    T = _ARTICLE_COPY[lang]
    cats = classify_article_cats(title, desc, body_text)
    primary_cat = cats[0]
    cat_labels = [article_topic_label(c, lang) for c in cats]
    ctype = classify_article_ctype(title, desc, body_text)
    ctype_label = article_ctype_label(ctype, lang)
    auds = classify_article_audiences(title, desc, cats=cats, ctype=ctype)
    aud_labels = [article_audience_label(a, lang) for a in auds]

    words = max(350, len(((body_text or desc or '') + ' ' + (title or '')).split()))
    mins = max(2, min(8, round(words / 180)))
    rtime_key = 'fast' if mins <= 3 else 'deep'
    mins_fmt = digits(mins, lang)
    if lang == 'fa':
        rtime_badge = f'{mins_fmt} دقیقه مطالعه'
    elif lang == 'ar':
        rtime_badge = f'{mins_fmt} دقائق قراءة'
    else:
        rtime_badge = f'{mins_fmt} min read'

    return {
        'topic': primary_cat,
        'topic_label': cat_labels[0],
        'cats': cats,
        'cats_csv': ','.join(cats),
        'cat_labels': cat_labels,
        'ctype': ctype,
        'ctype_label': ctype_label,
        'mins': mins,
        'rtime_key': rtime_key,
        'rtime_badge': rtime_badge,
        'aud_key': auds[0],
        'aud_label': aud_labels[0],
        'audiences': auds,
        'audiences_csv': ','.join(auds),
        'aud_labels': aud_labels,
        'card_cta': T['card_cta'],
    }


def _article_topic_buttons(lang, counts, total):
    T = _ARTICLE_COPY[lang]
    bits = [
        f'<button type="button" data-news-topic="all" aria-pressed="true"><span>{esc(T["all"])}</span> <b>{digits(total, lang)}</b></button>'
    ]
    for key, _short, _fa, _en, _ar in ARTICLE_TOPICS:
        bits.append(
            f'<button type="button" data-news-topic="{key}" aria-pressed="false"><span>{esc(article_topic_label(key, lang))}</span> <b>{digits(counts.get(key, 0), lang)}</b></button>'
        )
    return ''.join(bits)


def _article_ctype_buttons(lang, counts, total):
    T = _ARTICLE_COPY[lang]
    bits = [
        f'<button type="button" class="news-yr" data-art-ctype="all" aria-pressed="true"><span>{esc(T["ctype_all"])}</span> <b>{digits(total, lang)}</b></button>'
    ]
    for key, _fa, _en, _ar in ARTICLE_CTYPES:
        bits.append(
            f'<button type="button" class="news-yr" data-art-ctype="{key}" aria-pressed="false"><span>{esc(article_ctype_label(key, lang))}</span> <b>{digits(counts.get(key, 0), lang)}</b></button>'
        )
    return ''.join(bits)


def _article_audience_buttons(lang, counts, total):
    T = _ARTICLE_COPY[lang]
    bits = [
        f'<button type="button" class="news-yr" data-art-aud="all" aria-pressed="true"><span>{esc(T["aud_all"])}</span> <b>{digits(total, lang)}</b></button>'
    ]
    for key, _fa, _en, _ar in ARTICLE_AUDIENCES:
        bits.append(
            f'<button type="button" class="news-yr" data-art-aud="{key}" aria-pressed="false"><span>{esc(article_audience_label(key, lang))}</span> <b>{digits(counts.get(key, 0), lang)}</b></button>'
        )
    return ''.join(bits)


def _article_year_pills(lang, counts):
    T = _ARTICLE_COPY[lang]
    order = []
    newer = sorted((int(k) for k in counts if str(k).isdigit() and int(k) > 1405), reverse=True)
    order.extend(str(y) for y in newer)
    order.extend(['1405', '1404', '1403', '1402', '1401', 'before'])
    buttons = [f'<button type="button" data-news-year="all" aria-pressed="true">{esc(T["years"])}</button>']
    for key in order:
        n = counts.get(key, 0)
        label = T['before'] if key == 'before' else year_label(int(key), lang)
        buttons.append(
            f'<button type="button" data-news-year="{esc(key)}" aria-pressed="false">{label} <b>{digits(n, lang)}</b></button>'
        )
    return ''.join(buttons)


def article_tally(pairs):
    """pairs: iterable of (topic_or_cats, year_bucket) or (cats_list, year_bucket, ctype, audiences_list)."""
    topics, years, ctypes, audiences = {}, {}, {}, {}
    distinct = set()
    total = 0
    for item in pairs:
        total += 1
        if len(item) == 4:
            cats_val, bucket, ctype_val, auds_val = item
        else:
            cats_val, bucket = item
            ctype_val = 'educational'
            auds_val = ['clinical_staff']
        cats_list = [cats_val] if isinstance(cats_val, str) else list(cats_val or [])
        auds_list = [auds_val] if isinstance(auds_val, str) else list(auds_val or [])
        for c in cats_list:
            if c:
                topics[c] = topics.get(c, 0) + 1
        if ctype_val:
            ctypes[ctype_val] = ctypes.get(ctype_val, 0) + 1
        for a in auds_list:
            if a:
                audiences[a] = audiences.get(a, 0) + 1
        years[bucket] = years.get(bucket, 0) + 1
        if str(bucket).isdigit():
            distinct.add(int(bucket))
        else:
            distinct.add(1400)
    latest = max(distinct) if distinct else 0
    return {
        'total': total,
        'topics': topics,
        'ctypes': ctypes,
        'audiences': audiences,
        'years': years,
        'n_years': len(distinct),
        'latest': latest,
        'n_topics': len(ARTICLE_TOPICS),
    }


def article_shell(lang, prefix, crumbs, stats, feature_html):
    lang = lang if lang in _ARTICLE_COPY else 'fa'
    T = _ARTICLE_COPY[lang]
    dash = (
        f'<ul class="news-dash">'
        f'<li><b>{digits(stats["total"], lang)}</b><span>{esc(T["stat_news"])}</span></li>'
        f'<li><b>{digits(stats["n_topics"], lang)}</b><span>{esc(T["stat_topics"])}</span></li>'
        f'<li><b>{digits(stats["n_years"], lang)}</b><span>{esc(T["stat_years"])}</span></li>'
        f'<li><b>{year_label(stats["latest"], lang) if stats["latest"] else "—"}</b><span>{esc(T["stat_latest"])}</span></li>'
        f'</ul>'
    )
    return f"""<section class="page-hero about-hero articles-hero">
  <video class="about-hero-video articles-hero-video" autoplay muted loop playsinline webkit-playsinline disablepictureinpicture disableremoteplayback preload="metadata" tabindex="-1" aria-hidden="true" poster="{prefix}assets/media/hero-customers-poster.jpg?v=20261028p"><source src="{prefix}assets/media/hero-customers.mp4?v=20261028p" type="video/mp4"></video>
  <div class="wrap about-hero-grid">
    <div>{crumbs}
      <h1>{T["h1"]}</h1>
      <p class="slogan reveal" aria-label="{esc(T['slogan_aria'])}"><span class="slogan-line" style="--i:0">{esc(T['slogan_0'])}</span><span class="slogan-line" style="--i:1">{esc(T['slogan_1'])}</span><span class="slogan-line" style="--i:2">{esc(T['slogan_2'])}</span><span class="slogan-line" style="--i:3">{esc(T['slogan_3'])}</span></p>
    </div>
  </div>
</section>
<section class="news-d articles-d" data-news-finalist>
  <div class="wrap">
    <div class="news-d-stage">
      {feature_html}
      <aside class="news-panel">
        {dash}
        <p class="news-lab">{esc(T["topics_label"])}</p>
        <div class="news-topics" role="group" aria-label="{esc(T["topics_label"])}">{_article_topic_buttons(lang, stats["topics"], stats["total"])}</div>
        <div class="ao-extra-filters" role="group" aria-label="{esc(T["ctype_label"])}">
          <span class="ao-filter-label">{esc(T["ctype_label"])}</span>
          {_article_ctype_buttons(lang, stats.get("ctypes", {}), stats["total"])}
        </div>
        <div class="ao-extra-filters" role="group" aria-label="{esc(T["aud_label"])}">
          <span class="ao-filter-label">{esc(T["aud_label"])}</span>
          {_article_audience_buttons(lang, stats.get("audiences", {}), stats["total"])}
        </div>
        <p class="news-lab">{esc(T["years_label"])}</p>
        <div class="news-years" role="group" aria-label="{esc(T["years_label"])}">{_article_year_pills(lang, stats["years"])}</div>
        <p class="news-live"><span data-news-count>{digits(stats["total"], lang)}</span> {esc(T["shown"])}</p>
      </aside>
    </div>
  </div>
</section>
<section class="section news-d-page"><div class="wrap">
    <h2 class="news-archive-title">{esc(T["archive"])}</h2>"""


def article_empty_html(lang):
    T = _ARTICLE_COPY[lang if lang in _ARTICLE_COPY else 'fa']
    return (
        f'<p class="news-empty" data-news-empty hidden>{esc(T["empty"])} '
        f'<button type="button" data-news-reset>{esc(T["reset"])}</button></p>'
    )


def article_feature_from_card(card_html, lang):
    lang = lang if lang in _ARTICLE_COPY else 'fa'
    T = _ARTICLE_COPY[lang]
    href = re.search(r'href="([^"]+)"', card_html or '')
    img = re.search(r'<img[^>]*src="([^"]+)"', card_html or '')
    alt = re.search(r'<h3>(.*?)</h3>', card_html or '')
    excerpt = re.search(r'<p>(.*?)</p>', card_html or '')
    time_m = re.search(r'<time([^>]*)>(.*?)</time>', card_html or '')
    ct_m = re.search(r'class="art-ctype-badge[^"]*"[^>]*>([^<]+)</span>', card_html or '')
    rt_m = re.search(r'class="art-card-time"[^>]*>([^<]+)</span>', card_html or '')
    au_m = re.search(r'class="art-aud-tag"[^>]*>([^<]+)</span>', card_html or '')
    title = alt.group(1) if alt else ''
    src = img.group(1) if img else ''
    time_html = f'<time{time_m.group(1)}>{time_m.group(2)}</time>' if time_m else ''
    kicker = T['feature']
    ct_txt = ct_m.group(1) if ct_m else article_ctype_label('educational', lang)
    rt_txt = rt_m.group(1) if rt_m else ('۳ دقیقه مطالعه' if lang == 'fa' else '3 min read')
    au_txt = au_m.group(1) if au_m else article_audience_label('clinical_staff', lang)
    img_html = f'<img src="{src}" alt="{esc(re.sub(r"<[^>]+>", "", title))}" decoding="async">' if src else ''
    return (
        f'<a class="news-feature" data-news-feature href="{href.group(1) if href else "#"}">'
        f'{img_html}<div class="news-feature-body">'
        f'<div class="news-feature-tags">'
        f'<span class="news-kicker" data-news-kicker data-default="{esc(kicker)}">{esc(kicker)}</span>'
        f'<span class="news-fmt-pill" data-news-feat-ctype>{esc(ct_txt)}</span>'
        f'<span class="art-aud-tag" data-news-feat-rtime>{esc(rt_txt)}</span>'
        f'<span class="art-aud-tag" data-news-feat-aud>{esc(au_txt)}</span>'
        f'</div>'
        f'{time_html}<h2>{title}</h2><p>{excerpt.group(1) if excerpt else ""}</p></div></a>'
    )
