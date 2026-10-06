import re, urllib.parse as u
NEWS_RE = re.compile(r'نمایشگاه|کنگره|مصاحبه|گفت\s*و\s*گو|گفت‌وگو|حضور|رونمایی|برندگان|قرعه|روز پرستار|روز جهانی|روز ملی|گرامی|تبریک|تسلیت|دعوت|مجمع|انتخابات|نشست|جلسه|جلسات|دیدار|بازدید|بیانیه|نظرسنجی|اخذ|دانش\s*بنیان شد|دانش‌بنیان شد|انتشار|منتشر|بازتاب|برگزار|وبینار|پروانه|حمایت|اهدا|ارسال|مذاکرات|نکوداشت|سال تحصیلی|هزار درخت|نجات زاگرس|پویش|کمپین|جشنواره|همایش|افتتاح|عضویت|تقدیر|لوح|صادر|رتبه|نوروز|یلدا|محرم|رمضان|آبادیس در|آبادیس به|آبادیس،|مدیرعامل|اطلاعیه|بازسازی|جنگ|استخدام|مسابقه|سفر|قرارداد|تفاهم')
ART_RE = re.compile(r'چیست|بررسی|میزان|تبعیت|دستورالعمل|سیستم|پروتکل|الگوی|ارزیابی|ارزيابي|طراحی و اجرای')
def strip_title(t): return re.sub(r'\s*\|\s*مخازن طبی آبادیس\s*$', '', t or '').strip()
def classify(p, kc):
    k = kc.get(u.unquote(p['url']).rstrip('/'))
    t = strip_title(p['title'])
    if k == 'ads' or t in ('تست',): return None
    if k == 'newss': return 'news'
    if k in ('blog', 'products', 'accessories', 'install', 'device'): return 'articles'
    if ART_RE.search(t): return 'articles'
    return 'news' if NEWS_RE.search(t) else 'articles'
