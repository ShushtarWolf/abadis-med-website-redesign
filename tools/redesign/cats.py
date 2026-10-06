import re, urllib.parse as u

NEWS_RE = re.compile(
    r'نمایشگاه|کنگره|مصاحبه|گفت\s*و\s*گو|گفت‌وگو|حضور|رونمایی|برندگان|قرعه|روز پرستار|روز جهانی|روز ملی|'
    r'گرامی|تبریک|تسلیت|دعوت|مجمع|انتخابات|نشست|جلسه|جلسات|دیدار|بازدید|بیانیه|نظرسنجی|اخذ|'
    r'دانش\s*بنیان شد|دانش‌بنیان شد|انتشار|منتشر|بازتاب|برگزار|وبینار|پروانه|حمایت|اهدا|ارسال|'
    r'مذاکرات|نکوداشت|سال تحصیلی|هزار درخت|نجات زاگرس|پویش|کمپین|جشنواره|همایش|افتتاح|عضویت|'
    r'تقدیر|لوح|صادر|رتبه|نوروز|یلدا|محرم|رمضان|آبادیس در|آبادیس به|آبادیس،|مدیرعامل|اطلاعیه|'
    r'بازسازی|جنگ|استخدام|مسابقه|سفر|قرارداد|تفاهم|بازاریابی نسل|هوش تجار'
)
ART_RE = re.compile(r'چیست|بررسی|میزان|تبعیت|دستورالعمل|سیستم|پروتکل|الگوی|ارزیابی|ارزيابي|طراحی و اجرای')


def strip_title(t):
    return re.sub(r'\s*\|\s*مخازن طبی آبادیس\s*$', '', t or '').strip()


def heuristic(title: str) -> str:
    t = strip_title(title)
    if ART_RE.search(t):
        return 'articles'
    return 'news' if NEWS_RE.search(t) else 'articles'


def classify(p, kc):
    """Return 'news' | 'articles' | None (ads/test → careers, not republished as posts).

    Real WordPress categories in known_cats win. `uncategorized` falls back to the
    title heuristic (and callers may list those IDs in a report).
    """
    k = kc.get(u.unquote(p['url']).rstrip('/'))
    t = strip_title(p['title'])
    if k == 'ads' or t in ('تست',):
        return None
    if k == 'newss':
        return 'news'
    if k in ('blog', 'products', 'accessories', 'install', 'device'):
        return 'articles'
    # uncategorized / unknown → heuristic
    return heuristic(t)
