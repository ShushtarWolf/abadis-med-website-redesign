"""Finalist D news hero: seven topic tags + year pills.

Topic names are the 2026-10-27 approval. Counts are computed from the
archive; they are not the counts drawn on the mockup.
"""
import re
from datetime import datetime, timedelta, timezone

from lib import esc, fa, g2j

TOPICS = (
    ('events', 'نمایشگاه', 'نمایشگاه‌ها و رویدادها', 'Exhibitions and events', 'المعارض والفعاليات'),
    ('install', 'نصب', 'نصب و راه‌اندازی در بیمارستان‌ها', 'Hospital installations', 'التركيب والتشغيل في المستشفيات'),
    ('academy', 'آموزش', 'کارگاه‌های آموزشی و آکادمی', 'Workshops and academy', 'ورش العمل والأكاديمية'),
    ('product', 'محصول', 'محصولات و فناوری', 'Products and technology', 'المنتجات والتقنية'),
    ('env', 'زاگرس', 'محیط‌زیست و نجات زاگرس', 'Environment and Save Zagros', 'البيئة وإنقاذ زاغروس'),
    ('honor', 'افتخار', 'افتخارات و گواهینامه‌ها', 'Honors and certificates', 'الأوسمة والشهادات'),
)

_COPY = {
    'fa': {
        'all': 'همه اخبار', 'years': 'همه سال‌ها', 'before': '۱۴۰۰ و قبل',
        'h1': 'آخرین <em>اخبار</em>',
        'lead': 'اخبار، گزارش‌ها، مصاحبه‌ها و رویدادهای شرکت دانش‌بنیان مخازن طبی آبادیس',
        'topics_label': 'موضوع', 'years_label': 'سال',
        'stat_news': 'خبر', 'stat_topics': 'سرفصل', 'stat_years': 'سال پوشش', 'stat_latest': 'تازه‌ترین سال',
        'shown': 'خبر', 'empty': 'خبری با این ترکیب پیدا نشد.', 'reset': 'نمایش همه اخبار',
        'archive': 'آرشیو اخبار', 'feature': 'تازه‌ترین خبر',
    },
    'en': {
        'all': 'All news', 'years': 'All years', 'before': '1400 and earlier',
        'h1': 'Latest <em>news</em>',
        'lead': 'News, reports, interviews and events from Abadis Medical Reservoirs.',
        'topics_label': 'Topic', 'years_label': 'Year',
        'stat_news': 'stories', 'stat_topics': 'topics', 'stat_years': 'years covered', 'stat_latest': 'Latest year',
        'shown': 'shown', 'empty': 'No stories match this combination.', 'reset': 'Show all news',
        'archive': 'News archive', 'feature': 'Latest story',
    },
    'ar': {
        'all': 'كل الأخبار', 'years': 'كل السنوات', 'before': '١٤٠٠ وما قبل',
        'h1': 'آخر <em>الأخبار</em>',
        'lead': 'أخبار وتقارير ومقابلات وفعاليات خزانات آباديس الطبية.',
        'topics_label': 'الموضوع', 'years_label': 'السنة',
        'stat_news': 'خبر', 'stat_topics': 'محاور', 'stat_years': 'سنوات التغطية', 'stat_latest': 'أحدث سنة',
        'shown': 'ظاهر', 'empty': 'لا توجد أخبار لهذا التوليف.', 'reset': 'عرض كل الأخبار',
        'archive': 'أرشيف الأخبار', 'feature': 'أحدث خبر',
    },
}

_AR_DIGITS = str.maketrans('0123456789', '٠١٢٣٤٥٦٧٨٩')
_FA_DIGITS = str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789')
_AR_TO_EN = str.maketrans('٠١٢٣٤٥٦٧٨٩', '0123456789')


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
    if key in ('', 'all', None):
        return _COPY[lang]['all']
    for row in TOPICS:
        if row[0] == key or row[1] == key:
            return row[{'fa': 2, 'en': 3, 'ar': 4}[lang]]
    return key


def classify_text(text):
    """First matching topic. Unmatched items stay under All news only."""
    t = (text or '').replace('\u200c', ' ').replace('\u0640', '').lower()
    t = t.replace('ي', 'ی').replace('ك', 'ک').replace('أ', 'ا').replace('إ', 'ا').replace('آ', 'ا').replace('ة', 'ه')
    if re.search(r'زاگرس|زاغروس|بلوط|هزار درخت|توسعه پایدار|حکمرانی سبز|پساب|zagros|oak forest|sustainab|green governance|wastewater|بیئه|استدامه', t):
        return 'env'
    if re.search(r'کارگاه|وبینار|آکادمی|workshop|webinar|academy|ورشه|اکادیمیه|ندوه', t):
        return 'academy'
    if re.search(r'گواهی|گواهینامه|پروانه بهره|پروانه بهره‌|دانش‌? ?بنیان شد|اختراع|جایزه|فعال‌ترین|فعال ترین|certificate|patent|\baward\b|ce certification|شهاده|براءه|جایزه', t):
        return 'honor'
    if re.search(r'نصب و راه|راه‌اندازی|راه اندازی|راه\u200cاندازی|تجهیز (?:بیمارستان|مرکز|دو مرکز)|جلسات مدیران|رؤسای بیمارستان|روسای بیمارستان|installation|commissioning|deployed|ترکیب و|التشغیل', t):
        return 'install'
    if re.search(r'نمایشگاه|کنگره|همایش|ایران[\s‌]*هلث|ایران[\s‌]*مد|ایران[\s‌]*کلین|سلامت بنیان|ازبکستان|iran health|iranmed|exhibition|congress|expo|uzmed|uzbek|معرض|مؤتمر|موتمر|كونغرس', t):
        return 'events'
    if re.search(r'رونمایی|رو نمایی|محصول جدید|محصولات جدید|فیلتراسیون|فیلتر|کدینگ|فیکسر|unveil|filtration|new product|suction liner|suction bag|suction tube|antibacterial filter|منتج|فلتر|شفط|الکشف عن', t):
        return 'product'
    return ''


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
        if key == 'before':
            label = T['before']
        else:
            label = year_label(int(key), lang)
        buttons.append(
            f'<button type="button" data-news-year="{esc(key)}" aria-pressed="false">{label} <b>{digits(n, lang)}</b></button>'
        )
    return ''.join(buttons)


def _topic_buttons(lang, counts, total):
    T = _COPY[lang]
    bits = [
        f'<button type="button" data-news-topic="all" aria-pressed="true">{esc(T["all"])} <b>{digits(total, lang)}</b></button>'
    ]
    for key, _short, _fa, _en, _ar in TOPICS:
        bits.append(
            f'<button type="button" data-news-topic="{key}" aria-pressed="false">{esc(topic_label(key, lang))} <b>{digits(counts.get(key, 0), lang)}</b></button>'
        )
    return ''.join(bits)


def tally(pairs):
    """pairs: iterable of (topic_key, year_bucket)."""
    topics, years = {}, {}
    distinct = set()
    total = 0
    for topic, bucket in pairs:
        total += 1
        if topic:
            topics[topic] = topics.get(topic, 0) + 1
        years[bucket] = years.get(bucket, 0) + 1
        if str(bucket).isdigit():
            distinct.add(int(bucket))
        else:
            distinct.add(1400)
    latest = max(distinct) if distinct else 0
    return {'total': total, 'topics': topics, 'years': years, 'n_years': len(distinct), 'latest': latest, 'n_topics': len(TOPICS)}


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
    return f'''<section class="news-d" data-news-finalist>
  <div class="wrap">
    {crumbs}
    <h1>{T["h1"]}</h1>
    <p class="lead">{esc(T["lead"])}</p>
    <div class="news-d-stage">
      {feature_html}
      <aside class="news-panel">
        {dash}
        <p class="news-lab">{esc(T["topics_label"])}</p>
        <div class="news-topics" role="group" aria-label="{esc(T["topics_label"])}">{_topic_buttons(lang, stats["topics"], stats["total"])}</div>
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
    href = re.search(r'href="([^"]+)"', card_html)
    img = re.search(r'<img[^>]*src="([^"]+)"', card_html)
    alt = re.search(r'<h3>(.*?)</h3>', card_html)
    excerpt = re.search(r'<p>(.*?)</p>', card_html)
    time_m = re.search(r'<time([^>]*)>(.*?)</time>', card_html)
    title = alt.group(1) if alt else ''
    src = img.group(1) if img else ''
    time_html = f'<time{time_m.group(1)}>{time_m.group(2)}</time>' if time_m else ''
    kicker = _COPY[lang if lang in _COPY else 'fa']['feature']
    img_html = f'<img src="{src}" alt="{esc(re.sub(r"<[^>]+>", "", title))}" decoding="async">' if src else ''
    return (
        f'<a class="news-feature" data-news-feature href="{href.group(1) if href else "#"}">'
        f'{img_html}<div class="news-feature-body"><span class="news-kicker" data-news-kicker>{esc(kicker)}</span>'
        f'{time_html}<h2>{title}</h2><p>{excerpt.group(1) if excerpt else ""}</p></div></a>'
    )


# ------------------------------------------------------------------ Articles Finalist D (Approved A2)
ARTICLE_TOPICS = (
    ('suction', 'ساکشن', 'کیسه و سیستم‌های ساکشن', 'Suction Bags & Systems', 'أكياس وأنظمة الشفط'),
    ('infection', 'عفونت', 'کنترل عفونت و فیلتراسیون', 'Infection Control & Filtration', 'مكافحة العدوى والترشيح'),
    ('airway', 'راه هوایی', 'مراقبت از راه هوایی و ICU', 'Airway Care & ICU', 'رعاية مجرى الهواء والعناية المركزة'),
    ('guide', 'راهنما', 'استانداردها و راهنمای خرید', 'Standards & Buying Guides', 'المعايير وأدلة الشراء'),
    ('env', 'محیط‌زیست', 'حکمرانی سبز و پسماند پزشکی', 'Green Governance & Medical Waste', 'الحوكمة الخضراء والنفايات الطبية'),
    ('surgery', 'جراحی', 'تجهیزات جراحی و بالینی', 'Surgical & Clinical Equipment', 'المعدات الجراحية والسريرية'),
)

_ARTICLE_COPY = {
    'fa': {
        'all': 'همه مقالات', 'years': 'همه سال‌ها', 'before': '۱۴۰۰ و قبل',
        'h1': 'دانشنامه و <em>مقالات علمی</em>',
        'lead': 'مقالات علمی، راهنماهای بالینی، استانداردهای کنترل عفونت و بررسی تخصصی تجهیزات پزشکی آبادیس',
        'slogan_aria': 'دانشنامه تخصصی و مقالات علمی آبادیس، کنترل عفونت و ایمنی بیمارستان، استانداردهای نوین تجهیزات پزشکی، راهنمای جامع مدیران و کادر درمان',
        'slogan_0': 'دانشنامه تخصصی و مقالات علمی آبادیس،',
        'slogan_1': 'کنترل عفونت و ایمنی بیمارستان',
        'slogan_2': 'استانداردهای نوین تجهیزات پزشکی',
        'slogan_3': 'راهنمای جامع مدیران و کادر درمان',
        'topics_label': 'محور علمی و تخصصی', 'years_label': 'سال انتشار',
        'rtime_label': 'زمان مطالعه:', 'rtime_all': 'همه',
        'rtime_fast': 'مطالعه سریع (زیر ۳ دقیقه)', 'rtime_deep': 'مقالات جامع (بالای ۴ دقیقه)',
        'aud_label': 'مخاطب:', 'aud_all': 'همه مخاطبان',
        'aud_clinical': 'کادر درمان و اتاق عمل', 'aud_infection': 'مسئولین کنترل عفونت', 'aud_procurement': 'مدیران خرید',
        'stat_news': 'مقاله تخصصی', 'stat_topics': 'محور علمی', 'stat_years': 'سال پوشش', 'stat_latest': 'تازه‌ترین سال',
        'shown': 'مقاله علمی', 'empty': 'مقاله‌ای با این ترکیب پیدا نشد.', 'reset': 'نمایش همه مقالات',
        'archive': 'آرشیو مقالات علمی و تخصصی', 'feature': 'تازه‌ترین مقاله علمی',
        'card_cta': 'مطالعه مقاله علمی ←',
    },
    'en': {
        'all': 'All articles', 'years': 'All years', 'before': '1400 and earlier',
        'h1': 'Knowledge Hub & <em>Scientific Articles</em>',
        'lead': 'Scientific articles, clinical guides, infection-control standards and medical equipment insights from Abadis.',
        'slogan_aria': 'Abadis Med Knowledge Hub and Scientific Articles, Hospital Infection Control and Safety, Modern Medical Device Standards, Guide for Clinicians and Healthcare Leaders',
        'slogan_0': 'Abadis Med Knowledge Hub & Scientific Articles,',
        'slogan_1': 'Hospital Infection Control & Safety',
        'slogan_2': 'Modern Medical Device Standards',
        'slogan_3': 'Guide for Clinicians & Healthcare Leaders',
        'topics_label': 'Scientific Topic', 'years_label': 'Publication Year',
        'rtime_label': 'Reading time:', 'rtime_all': 'All',
        'rtime_fast': 'Quick read (≤3 min)', 'rtime_deep': 'In-depth (4+ min)',
        'aud_label': 'Audience:', 'aud_all': 'All audiences',
        'aud_clinical': 'OR & Clinical Staff', 'aud_infection': 'Infection Control', 'aud_procurement': 'Hospital Procurement',
        'stat_news': 'articles', 'stat_topics': 'scientific topics', 'stat_years': 'years covered', 'stat_latest': 'Latest year',
        'shown': 'articles shown', 'empty': 'No articles match this combination.', 'reset': 'Show all articles',
        'archive': 'Scientific Articles Archive', 'feature': 'Latest Article',
        'card_cta': 'Read scientific article →',
    },
    'ar': {
        'all': 'كل المقالات', 'years': 'كل السنوات', 'before': '١٤٠٠ وما قبل',
        'h1': 'الموسوعة و<em>المقالات العلمية</em>',
        'lead': 'مقالات علمية وأدلة سريرية ومعايير مكافحة العدوى والمعدات الطبية من آباديس.',
        'slogan_aria': 'الموسوعة المتخصصة والمقالات العلمية في آباديس، مكافحة العدوى وسلامة المستشفيات، المعايير الحديثة للأجهزة الطبية، دليل شامل للكوادر الطبية والمديرين',
        'slogan_0': 'الموسوعة المتخصصة والمقالات العلمية في آباديس،',
        'slogan_1': 'مكافحة العدوى وسلامة المستشفيات',
        'slogan_2': 'المعايير الحديثة للأجهزة الطبية',
        'slogan_3': 'دليل شامل للكوادر الطبية والمديرين',
        'topics_label': 'المحور العلمي', 'years_label': 'سنة النشر',
        'rtime_label': 'وقت القراءة:', 'rtime_all': 'الكل',
        'rtime_fast': 'قراءة سريعة (≤٣ دقائق)', 'rtime_deep': 'مقال شامل (٤+ دقائق)',
        'aud_label': 'الجمهور:', 'aud_all': 'جميع الفئات',
        'aud_clinical': 'غرف العمليات والكادر الطبي', 'aud_infection': 'مكافحة العدوى', 'aud_procurement': 'إدارة المشتريات',
        'stat_news': 'مقالة علمية', 'stat_topics': 'محاور علمية', 'stat_years': 'سنوات التغطية', 'stat_latest': 'أحدث سنة',
        'shown': 'مقالة علمية', 'empty': 'لا توجد مقالات لهذا التوليف.', 'reset': 'عرض كل المقالات',
        'archive': 'أرشيف المقالات العلمية', 'feature': 'أحدث مقالة علمية',
        'card_cta': 'قراءة المقال العلمي ←',
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


def classify_article_text(text):
    """Classify an article into one of the 6 scientific topics."""
    t = (text or '').replace('\u200c', ' ').replace('\u0640', '').lower()
    t = t.replace('ي', 'ی').replace('ك', 'ک').replace('أ', 'ا').replace('إ', 'ا').replace('آ', 'ا').replace('ة', 'ه')
    if re.search(r'راهنمای خرید|قیمت|مقایسه|استاندارد|ایزو|iso|ce|مدیریت خرید|نکات خرید|چک لیست|راهنمای انتخاب|buying guide|price|standard', t):
        return 'guide'
    if re.search(r'پسماند|پساب|محیط زیست|سبز|زاگرس|توسعه پایدار|کربن|صرفه جویی|بازیافت|waste|environment|green|sustainab', t):
        return 'env'
    if re.search(r'فیلتر|عفونت|استریل|آنتی باکتریال|هیدروفوبیک|ضدعفونی|پاتوژن|باکتری|ویروس|infection|filter|steril|antibacterial', t):
        return 'infection'
    if re.search(r'راه هوایی|ایروی|تراشه|لوله تراشه|فیکسر|دهان|مسواک|ونتیلاتور|تنفس|اکسیژن|icu|airway|trachea|oral|intubat', t):
        return 'airway'
    if re.search(r'ساکشن|مخزن|کیسه ساکشن|لاينر|لاینر|بهمن گیر|ترشحات|وکیوم|suction|canister|liner', t):
        return 'suction'
    return 'surgery'


def article_meta_for(title, desc, body_text='', lang='fa'):
    lang = lang if lang in _ARTICLE_COPY else 'fa'
    T = _ARTICLE_COPY[lang]
    topic = classify_article_text((title or '') + ' ' + (desc or ''))
    topic_label = article_topic_label(topic, lang)
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

    if topic in ('guide', 'env'):
        aud_key = 'procurement'
        aud_label = T['aud_procurement']
    elif topic == 'infection':
        aud_key = 'infection'
        aud_label = T['aud_infection']
    else:
        aud_key = 'clinical'
        aud_label = T['aud_clinical']
    return {
        'topic': topic,
        'topic_label': topic_label,
        'mins': mins,
        'rtime_key': rtime_key,
        'rtime_badge': rtime_badge,
        'aud_key': aud_key,
        'aud_label': aud_label,
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
    topics, years = {}, {}
    distinct = set()
    total = 0
    for topic, bucket in pairs:
        total += 1
        if topic:
            topics[topic] = topics.get(topic, 0) + 1
        years[bucket] = years.get(bucket, 0) + 1
        if str(bucket).isdigit():
            distinct.add(int(bucket))
        else:
            distinct.add(1400)
    latest = max(distinct) if distinct else 0
    return {'total': total, 'topics': topics, 'years': years, 'n_years': len(distinct), 'latest': latest, 'n_topics': len(ARTICLE_TOPICS)}


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
  <video class="about-hero-video articles-hero-video" autoplay muted loop playsinline webkit-playsinline disablepictureinpicture disableremoteplayback preload="metadata" tabindex="-1" aria-hidden="true" poster="{prefix}assets/media/hero-customers-poster.jpg?v=20261028k"><source src="{prefix}assets/media/hero-customers.mp4?v=20261028k" type="video/mp4"></video>
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
        <p class="news-lab">{esc(T["years_label"])}</p>
        <div class="news-years" role="group" aria-label="{esc(T["years_label"])}">{_article_year_pills(lang, stats["years"])}</div>
        <div class="ao-extra-filters" role="group" aria-label="{esc(T["rtime_label"])}">
          <span class="ao-filter-label">{esc(T["rtime_label"])}</span>
          <button type="button" class="news-yr" data-art-rtime="all" aria-pressed="true">{esc(T["rtime_all"])}</button>
          <button type="button" class="news-yr" data-art-rtime="fast" aria-pressed="false">{esc(T["rtime_fast"])}</button>
          <button type="button" class="news-yr" data-art-rtime="deep" aria-pressed="false">{esc(T["rtime_deep"])}</button>
        </div>
        <div class="ao-extra-filters" role="group" aria-label="{esc(T["aud_label"])}">
          <span class="ao-filter-label">{esc(T["aud_label"])}</span>
          <button type="button" class="news-yr" data-art-aud="all" aria-pressed="true">{esc(T["aud_all"])}</button>
          <button type="button" class="news-yr" data-art-aud="clinical" aria-pressed="false">{esc(T["aud_clinical"])}</button>
          <button type="button" class="news-yr" data-art-aud="infection" aria-pressed="false">{esc(T["aud_infection"])}</button>
          <button type="button" data-art-aud="procurement" class="news-yr" aria-pressed="false">{esc(T["aud_procurement"])}</button>
        </div>
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
    rt_m = re.search(r'class="art-card-time"[^>]*>([^<]+)</span>', card_html or '')
    au_m = re.search(r'class="art-aud-tag"[^>]*>([^<]+)</span>', card_html or '')
    title = alt.group(1) if alt else ''
    src = img.group(1) if img else ''
    time_html = f'<time{time_m.group(1)}>{time_m.group(2)}</time>' if time_m else ''
    kicker = T['feature']
    rt_txt = rt_m.group(1) if rt_m else ('۳ دقیقه مطالعه' if lang == 'fa' else '3 min read')
    au_txt = au_m.group(1) if au_m else T['aud_clinical']
    img_html = f'<img src="{src}" alt="{esc(re.sub(r"<[^>]+>", "", title))}" decoding="async">' if src else ''
    return (
        f'<a class="news-feature" data-news-feature href="{href.group(1) if href else "#"}">'
        f'{img_html}<div class="news-feature-body">'
        f'<div class="news-feature-tags">'
        f'<span class="news-kicker" data-news-kicker data-default="{esc(kicker)}">{esc(kicker)}</span>'
        f'<span class="art-aud-tag" data-news-feat-rtime>{rt_txt}</span>'
        f'<span class="art-aud-tag" data-news-feat-aud>{au_txt}</span>'
        f'</div>'
        f'{time_html}<h2>{title}</h2><p>{excerpt.group(1) if excerpt else ""}</p></div></a>'
    )
