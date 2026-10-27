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
