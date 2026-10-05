#!/usr/bin/env python3
"""Generate the static redesign pages in ../site from shared chrome.
Run: python3 tools/build_site.py   (pure stdlib; edit page bodies below)."""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
DEMO = pathlib.Path("/tmp/scrub-demo/abadis/index.html")  # source of verbatim product blocks (optional)
CSR_URL = "https://abadis-med.com/%D9%86%D8%AC%D8%A7%D8%AA-%D8%B2%D8%A7%DA%AF%D8%B1%D8%B3%D8%8C%D9%85%D8%B3%D8%A6%D9%88%D9%84%DB%8C%D8%AA-%D8%A7%D8%AC%D8%AA%D9%85%D8%A7%D8%B9%DB%8C-%D8%A2%D8%A8%D8%A7%D8%AF%DB%8C%D8%B3/"
LIVE = "https://abadis-med.com"

NAV = [("", "خانه", "home"), ("products/", "محصولات", "products"),
       ("csr/", "مسئولیت اجتماعی", "csr"), ("contact/", "ارتباط با ما", "contact")]

THEME_BOOT = """<script>(function(){var t;try{var q=new URLSearchParams(location.search).get('theme');if(q){localStorage.setItem('abadis-theme',q)}t=localStorage.getItem('abadis-theme')}catch(e){}var d=document.documentElement;d.dataset.theme=(t==='dark'||t==='noir')?t:'light';d.classList.add('js')})();</script>"""

def head(p, title, desc, extra=""):
    return f"""<!DOCTYPE html>
<html lang="fa" dir="rtl" data-theme="light">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex,nofollow">
<meta name="theme-color" content="#e8f3f3">
{THEME_BOOT}
<link rel="icon" href="{p}favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="{p}assets/img/favicon-32.png">
<link rel="apple-touch-icon" href="{p}assets/img/apple-touch-icon.png">
<meta property="og:locale" content="fa_IR"><meta property="og:site_name" content="مخازن طبی آبادیس">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">
<meta property="og:image" content="{p}assets/img/og-image.jpg">
<link rel="preload" href="{p}assets/fonts/kalameh/KalamehWeb-FaNum-Regular.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{p}assets/fonts/kalameh/KalamehWeb-FaNum-Black.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{p}assets/css/site.css">
{extra}
</head>
"""

def header(p, active, solid=False):
    links = "".join(
        f'<a href="{p}{href}"{" aria-current=\"page\"" if key == active else ""}>{label}</a>'
        for href, label, key in NAV)
    return f"""<body>
<a class="skip" href="#main">پرش به محتوا</a>
<header class="header{' solid' if solid else ''}" id="header">
  <a class="logo" href="{p}" aria-label="مخازن طبی آبادیس — خانه">
    <img class="lg-light" src="{p}assets/img/abadis-logo.png" width="658" height="309" alt="مخازن طبی آبادیس">
    <img class="lg-dark" src="{p}assets/img/abadis-logo-on-teal.png" width="670" height="309" alt="مخازن طبی آبادیس">
  </a>
  <button class="menu-btn" type="button" aria-expanded="false" aria-controls="mainNav">منو</button>
  <nav class="nav" id="mainNav" aria-label="منوی اصلی">{links}</nav>
  <div class="theme-switch" role="group" aria-label="حالت نمایش">
    <button type="button" data-set="light" aria-pressed="true"><span class="dot"></span>روشن</button>
    <button type="button" data-set="dark" aria-pressed="false"><span class="dot"></span>تیره</button>
    <button type="button" data-set="noir" aria-pressed="false"><span class="dot"></span>نوآر</button>
  </div>
  <a class="header-cta" href="{p}contact/">تماس با فروش</a>
</header>
"""

def footer(p, tail=""):
    return f"""<footer class="site-footer">
  <div class="wrap foot-inner">
    <div>
      <img src="{p}assets/img/abadis-logo-on-teal.png" width="670" height="309" alt="مخازن طبی آبادیس" loading="lazy">
      <p>با ما در ارتباط باشید...</p>
      <div class="foot-links">
        <a href="{p}products/">محصولات آبادیس</a>
        <a href="{p}csr/">نجات زاگرس، مسئولیت اجتماعی آبادیس</a>
        <a href="{p}contact/">ارتباط با ما</a>
        <a href="{LIVE}/" target="_blank" rel="noopener">abadis-med.com</a>
      </div>
    </div>
    <div>
      <h3>تماس</h3>
      <dl>
        <dt>مرکز تماس:</dt><dd><a href="tel:+982192001017" dir="ltr">02192001017</a></dd>
        <dt>تلفن تماس:</dt><dd><a href="tel:+982122671845" dir="ltr">02122671845</a> | <a href="tel:+982122205502" dir="ltr">02122205502</a><br><a href="tel:+982122215503" dir="ltr">02122215503</a> | <a href="tel:+982122218910" dir="ltr">02122218910</a></dd>
        <dt>فکس:</dt><dd><span dir="ltr">02141425555</span> | داخلی 28544</dd>
        <dt>پست الکترونیک:</dt><dd><a href="mailto:info@abadis-med.com">info@abadis-med.com</a></dd>
        <dt>واتس‌اپ:</dt><dd><a href="https://wa.me/989100145809" target="_blank" rel="noopener" dir="ltr">+989100145809</a></dd>
      </dl>
    </div>
    <div>
      <h3>نشانی</h3>
      <p><b>نشانی دفتر مرکزی:</b><br>ایران، تهران، قیطریه، خیابان اندرزگو، پلاک 104، واحد2</p>
      <p><b>نشانی کارخانه:</b><br>ایران،تهران،شهرک صنعتی شمس آباد، بلوار گلستان، کوچه گلشن ۱۹،پلاک۱۷</p>
    </div>
  </div>
  <div class="wrap foot-copy">کلیه حقوق مادی و معنوی این وبسایت متعلق است به: مخازن طبی آبادیس · نسخهٔ پیش‌نمایش بازطراحی</div>
</footer>
<script src="{p}assets/js/site.js" defer></script>
{tail}
</body>
</html>
"""

def mosaic(p, name, tile=12, extra_cls=""):
    return f"""<div class="mosaic{extra_cls}" data-tile="{tile}" style="background-image:url('{p}assets/media/{name}-poster.jpg')" aria-hidden="true">
      <video muted loop playsinline autoplay preload="auto" poster="{p}assets/media/{name}-poster.jpg" disablepictureinpicture disableremoteplayback tabindex="-1">
        <source src="{p}assets/media/{name}-mosaic.mp4" type="video/mp4">
      </video>
    </div>"""

LIGHTBOX = """<div class="lb" id="lightbox" role="dialog" aria-modal="true" aria-label="گالری تصاویر" hidden>
  <span class="lb-count"></span>
  <button class="lb-close" type="button" aria-label="بستن">×</button>
  <button class="lb-prev" type="button" aria-label="تصویر قبلی">›</button>
  <figure><img alt=""><figcaption></figcaption></figure>
  <button class="lb-next" type="button" aria-label="تصویر بعدی">‹</button>
</div>"""

def write(rel, html):
    f = SITE / rel
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(html, encoding="utf-8")
    print("wrote", f.relative_to(ROOT))

# ------------------------------------------------------------------ HOME
def home():
    p = ""
    body = f"""<main id="main">
  <section class="hero" aria-label="معرفی آبادیس">
    {mosaic(p, 'hero', 12)}
    <div class="hero-inner">
      <span class="chip">شرکت دانش‌بنیان · کنترل عفونت بیمارستانی</span>
      <h1>مخازن طبی <em>آبادیس</em></h1>
      <p class="lead">شرکت دانش‌بنیان مخازن طبی آبادیس با تکیه بر دانش روز و ارائه محصولات و راهکارهای نوآورانه در مدیریت سیالات و زباله‌های عفونی بیمارستانی، گام‌های موثری در راستای کنترل عفونت‌های بیمارستانی و دستیابی به توسعه پایدار برداشته است.</p>
      <div class="hero-actions">
        <a class="btn btn-primary" href="products/">محصولات آبادیس</a>
        <a class="btn btn-ghost" href="contact/">مشاوره و تماس با فروش</a>
      </div>
      <p class="hero-slogan">«ما به اندازه یک سرانگشت اثر می‌گذاریم، به شما، به طبیعت، به جهان.»</p>
    </div>
  </section>

  <section class="section" id="products">
    <div class="wrap">
      <div class="section-head reveal"><p class="eyebrow">محصولات</p><h2>محصولات آبادیس</h2>
        <p>کیسه ساکشن یکبار مصرف در حجم‌های ۱، ۲ و ۳ لیتری و تمام اجزای سامانهٔ ساکشن بیمارستانی.</p></div>
      <div class="grid g-4">
        <a class="pcard reveal" href="products/suction-bag/"><div class="ph"><img src="assets/img/p/p2-main.webp" width="900" height="900" alt="کیسه ساکشن ۲ لیتری آبادیس" loading="lazy"></div><strong>کیسه ساکشن</strong><span>یک، دو و سه لیتری؛ با پودر ژل‌کننده و فیلتر هیدروفوبیک</span><span class="go">مشاهده محصول ←</span></a>
        <a class="pcard reveal" href="products/suction-bag/#filters"><div class="ph"><img src="assets/img/filters/anti-1-t.webp" width="480" height="480" alt="فیلتر آنتی باکتریال آبادیس" loading="lazy"></div><strong>فیلترها</strong><span>آنتی باکتریال، قطع کننده جریان و متخلخل</span><span class="go">مشاهده فیلترها ←</span></a>
        <a class="pcard reveal" href="products/"><div class="ph"><img src="assets/img/p/p3-g1-t.webp" width="320" height="480" alt="مخزن مدرج و کیسه ساکشن آبادیس" loading="lazy"></div><strong>مخزن</strong><span>مخازن مدرج سازگار با کیسه‌های آبادیس</span><span class="go">همهٔ محصولات ←</span></a>
        <a class="pcard reveal" href="products/"><div class="ph"><img src="assets/img/p/p1-g4-t.webp" width="480" height="320" alt="کیسه‌های ساکشن با شلنگ‌های اتصال" loading="lazy"></div><strong>اتصالات و ساکشن تیوب</strong><span>پایه و نگهدارنده‌ها، اتصالات، ساکشن تیوب و سایر محصولات</span><span class="go">همهٔ محصولات ←</span></a>
      </div>
    </div>
  </section>

  <section class="section section--alt" id="about">
    <div class="wrap split">
      <div class="reveal">
        <p class="eyebrow">آشنایی با ما</p>
        <h2>درباره ما بیشتر بدانید...</h2>
        <div class="prose" style="margin-top:14px">
          <p>پس از سال ها برنامه ریزی و ادامه دادن جریان ایجاد شده و با پویایی و تغییرات سیستم مدیریتی در سال ۲۰۱۷ شرکت دانش بنیان مخازن طبی آبادیس را بنا نهادیم تا هم تولید کیسه ساکشن یکبار مصرف آبادیس را آغاز کنیم و هم با اهداف خود در حوزه کنترل عفونت بیمارستانی و تجهیزات پزشکی گام های محکم تری برداریم ؛ و فهمیدیم که ما برای اثر گذاری آمده ایم…</p>
        </div>
      </div>
      <div class="reveal">
        <h3 style="font-weight:900;font-size:1.2rem">اهداف ما</h3>
        <ul class="goals">
          <li>۱. مدیریت بهینه زباله‌های عفونی و مایع بیمارستانی</li>
          <li>۲. کاهش و کنترل عفونت‌های ناشی از زباله‌ها و سیالات بیمارستانی</li>
          <li>۳. فرهنگ‌سازی برای استفاده حداکثری از راهکارها و محصولات ما در مراکز درمانی و بیمارستان‌ها</li>
        </ul>
      </div>
    </div>
  </section>

  <section class="section" id="value">
    <div class="wrap">
      <div class="section-head reveal"><p class="eyebrow">چرا یکبار مصرف؟</p><h2>ارزش افزوده‌های کیسه ساکشن یکبار مصرف</h2></div>
      <div class="grid g-4">
        <article class="card reveal"><span class="num">۰۱</span><h3>کاهش هزینه‌ها</h3><p>کاهش هزینه‌های مربوط به مواد شست‌و‌شو، مصرف آب، برق و منابع انسانی</p></article>
        <article class="card reveal"><span class="num">۰۲</span><h3>مدیریت زباله‌های بیمارستانی و عفونی</h3><p>باعث جمع‌آوری بهتر زباله‌های مایع و عفونی می‌گردد.</p></article>
        <article class="card reveal"><span class="num">۰۳</span><h3>بازیافت پذیر</h3><p>باعث کاهش حجم زباله‌های بیمارستانی و حفظ محیط‌زیست می‌گردد.</p></article>
        <article class="card reveal"><span class="num">۰۴</span><h3>استفاده آسان</h3><p>حذف فعالیت‌های مربوط به شست‌و‌شوی مخازن و استفاده راحت برای جمع‌آوری ضایعات حین عمل</p></article>
      </div>
    </div>
  </section>

  <section class="section deep" id="factory">
    <div class="wrap split">
      <div class="reveal">
        <p class="eyebrow">کارخانه</p>
        <h2>کارخانه دانش‌بنیان تجهیزات پزشکی آبادیس</h2>
        <p style="margin-top:12px">کارخانه دانش‌بنیان تجهیزات پزشکی آبادیس در سال ۱۳۹۷ با بهره‌گیری از پیشرفته‌ترین تجهیزات و ماشین‌آلات و با همکاری نیروهای متخصص راه‌اندازی شد. این کارخانه با ظرفیت تولید سالانه ۵ میلیون کیسه ساکشن یکبارمصرف، به‌عنوان بزرگ‌ترین تولیدکننده این محصولات در منطقه خاورمیانه شناخته می‌شود.</p>
        <h3 style="color:#fff;font-weight:800;margin-top:22px">چرا آبادیس؟</h3>
        <ul class="checks">
          <li>کاهش هزینه ها</li><li>ارائه محصولات با کیفیت</li><li>ارتباط مستمر آبادیس با مراکز درمانی</li><li>ارسال رایگان</li><li>تحویل در کوتاه ترین زمان ممکن</li>
        </ul>
      </div>
      <div class="media-frame reveal">{mosaic(p, 'or', 10)}</div>
    </div>
  </section>

  <section class="section section--alt" id="impact">
    <div class="wrap">
      <div class="grid g-3">
        <div class="card stat reveal"><strong>+۶۰۰</strong><span>همراه با بیش از ۶۰۰ مرکز درمانی در سطح کشور</span></div>
        <div class="card stat reveal"><strong>۵ میلیون</strong><span>ظرفیت تولید سالانه کیسه ساکشن یکبارمصرف</span></div>
        <div class="card stat reveal"><strong>۱۳۹۷</strong><span>راه‌اندازی کارخانه دانش‌بنیان آبادیس</span></div>
      </div>
      <div class="card reveal" style="margin-top:16px;display:flex;flex-wrap:wrap;gap:16px;align-items:center;justify-content:space-between">
        <div><h3>محاسبه گر</h3><p>جهت محاسبه آنلاین میزان صرفه‌جویی در مصرف آب و زباله‌های عفونی مرکز خود می‌توانید روی دکمه زیر کلیک نمایید.</p></div>
        <a class="btn btn-primary" href="{LIVE}/محاسبه-گر/" target="_blank" rel="noopener">محاسبه گر</a>
      </div>
    </div>
  </section>

  <section class="section" id="csr-teaser">
    <div class="wrap">
      <a class="card reveal" href="csr/" style="display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:0;padding:0;overflow:hidden;text-decoration:none;color:inherit">
        <div style="background:url('assets/img/zagros-koh.jpg') center/cover;min-height:240px" role="img" aria-label="نقاشی کوه‌های زاگرس و بلوط"></div>
        <div style="padding:30px 26px"><p class="eyebrow">مسئولیت اجتماعی</p><h2 style="font-size:1.5rem">نجات زاگرس، مسئولیت اجتماعی آبادیس</h2><p style="margin-top:10px">کاشت نهال بلوط در ارتفاعات زاگرس به تعداد اعضای خانواده آبادیس؛ تا در ارتفاعات زاگرس مکانی به نام آبادیس و به یاد صنعت سلامت کشور ثبت شود.</p><span class="pcard go" style="all:unset;color:var(--brand);font-weight:800;display:inline-block;margin-top:14px">ادامه ←</span></div>
      </a>
    </div>
  </section>

  <section class="section section--alt" id="news">
    <div class="wrap grid g-2" style="gap:32px">
      <div>
        <div class="section-head reveal"><p class="eyebrow">اخبار</p><h2>آخرین اخبار آبادیس</h2></div>
        <div class="grid">
          <a class="card teaser reveal" href="{LIVE}/آخرین-اخبار/" target="_blank" rel="noopener"><span class="tag">خبر</span><h3>آغاز فوری عملیات بازسازی کارخانه آبادیس پس از حادثه شهرک صنعتی شمس‌آباد</h3></a>
          <a class="card teaser reveal" href="{LIVE}/آخرین-اخبار/" target="_blank" rel="noopener"><span class="tag">خبر</span><h3>آبادیس در روزهای جنگ رمضان؛ تداوم خدمت‌رسانی بدون حتی یک روز توقف</h3></a>
          <a class="card teaser reveal" href="{LIVE}/آخرین-اخبار/" target="_blank" rel="noopener"><span class="tag">خبر</span><h3>استخدام کارشناس فروش در شرکت دانش‌بنیان مخازن طبی آبادیس</h3></a>
        </div>
      </div>
      <div>
        <div class="section-head reveal"><p class="eyebrow">مقالات</p><h2>مقالات آبادیس</h2></div>
        <div class="grid">
          <a class="card teaser reveal" href="{LIVE}/مقالات/" target="_blank" rel="noopener"><span class="tag">مقاله</span><h3>راهنمای خرید کیسه ساکشن یکبار مصرف برای مراکز درمانی</h3></a>
          <a class="card teaser reveal" href="{LIVE}/مقالات/" target="_blank" rel="noopener"><span class="tag">مقاله</span><h3>قیمت کیسه ساکشن یکبار مصرف؛ هر آنچه مدیران خرید مراکز درمانی باید بدانند</h3></a>
          <a class="card teaser reveal" href="{LIVE}/مقالات/" target="_blank" rel="noopener"><span class="tag">مقاله</span><h3>اکستنشن تیوب چیست؟</h3></a>
        </div>
      </div>
    </div>
  </section>

  <section class="section" id="certs">
    <div class="wrap">
      <div class="section-head reveal"><p class="eyebrow">مجوزها</p><h2>تنها دارنده تاییدیه اتحادیه اروپا</h2></div>
      <div class="certs reveal"><a href="{LIVE}/" target="_blank" rel="noopener">مشاهده مجوز CE اروپا</a><a href="{LIVE}/" target="_blank" rel="noopener">مشاهده مجوز IMED</a><a href="{LIVE}/" target="_blank" rel="noopener">مشاهده مجوز ISO</a></div>
      <div class="cta-band reveal" style="margin-top:48px">
        <h2>با آبادیس همراه شوید…</h2>
        <p>برای لیست قیمت، نمونه، نمایندگی و هماهنگی نصب با تیم فروش مخازن طبی آبادیس در تماس باشید.</p>
        <div class="cta-actions"><a class="btn btn-light" href="tel:+982192001017">تماس با فروش</a><a class="btn btn-ghost" href="contact/">فرم درخواست</a></div>
      </div>
    </div>
  </section>
</main>
"""
    write("index.html", head(p, "مخازن طبی آبادیس — کیسه ساکشن یکبار مصرف", "شرکت دانش‌بنیان مخازن طبی آبادیس؛ تولیدکننده کیسه ساکشن یکبار مصرف و راهکارهای مدیریت سیالات و زباله‌های عفونی بیمارستانی.") + header(p, "home") + body + footer(p))

# ------------------------------------------------------------------ PRODUCTS HUB
def products():
    p = "../"
    fams = [("suction-bag/", "کیسه ساکشن", "یک، دو و سه لیتری؛ پودر ژل‌کننده، فیلتر هیدروفوبیک، سازگار با کلیه دستگاه‌های ساکشن", "p/p2-main.webp", True),
            ("suction-bag/#filters", "فیلترها", "فیلتر آنتی باکتریال، قطع کننده جریان (مسدود شونده) و متخلخل", "filters/anti-1-t.webp", True),
            (f"{LIVE}/محصولات/مخزن/", "مخزن", "صفحهٔ محصول در سایت فعلی آبادیس", "p/p3-g1-t.webp", False),
            (f"{LIVE}/محصولات/پایه/", "پایه و نگهدارنده ها", "صفحهٔ محصول در سایت فعلی آبادیس", "p/p1-g3-t.webp", False),
            (f"{LIVE}/محصولات/اتصالات/", "اتصالات", "صفحهٔ محصول در سایت فعلی آبادیس", "p/p2-g3-t.webp", False),
            (f"{LIVE}/محصولات/ساکشن-تیوب/", "ساکشن تیوب", "صفحهٔ محصول در سایت فعلی آبادیس", "p/p1-g4-t.webp", False),
            (f"{LIVE}/محصولات/سایر-محصولات/", "سایر محصولات", "صفحهٔ محصول در سایت فعلی آبادیس", None, False)]
    cards = ""
    for href, name, desc, img, internal in fams:
        ph = f'<div class="ph"><img src="{p}assets/img/{img}" alt="{name} آبادیس" loading="lazy"></div>' if img else '<div class="ph txt">آبادیس</div>'
        ext = "" if internal else ' target="_blank" rel="noopener"'
        go = "مشاهده ←" if internal else "در سایت فعلی ↗"
        cards += f'<a class="pcard reveal" href="{href}"{ext}>{ph}<strong>{name}</strong><span>{desc}</span><span class="go">{go}</span></a>\n'
    body = f"""<main id="main">
  <section class="hero hero--short" aria-label="محصولات آبادیس">
    {mosaic(p, 'or', 12)}
    <div class="hero-inner">
      <p class="crumbs"><a href="{p}">خانه</a> › محصولات</p>
      <span class="chip">کنترل عفونت · مدیریت سیالات بیمارستانی</span>
      <h1>محصولات <em>آبادیس</em></h1>
      <p class="lead">کیسه ساکشن یکبار مصرف، فیلترها، مخزن، پایه و نگهدارنده ها، اتصالات، ساکشن تیوب و سایر محصولات.</p>
    </div>
  </section>
  <section class="section"><div class="wrap"><div class="grid g-3">{cards}</div>
    <p class="note" style="margin-top:22px">صفحات این پیش‌نمایش فعلاً برای کیسه ساکشن و فیلترها ساخته شده‌اند؛ سایر خانواده‌ها به صفحهٔ فعلی همان محصول در abadis-med.com لینک شده‌اند.</p></div></section>
</main>
"""
    write("products/index.html", head(p, "محصولات — مخازن طبی آبادیس", "محصولات مخازن طبی آبادیس: کیسه ساکشن یکبار مصرف، فیلترها، مخزن، پایه، اتصالات و ساکشن تیوب.") + header(p, "products") + body + footer(p))

# ------------------------------------------------------------------ PRODUCT: SUCTION BAG
def demo_blocks():
    src = DEMO.read_text(encoding="utf-8")
    def grab(start_pat, end_pat):
        s = src.index(start_pat); e = src.index(end_pat, s); return src[s:e]
    s1 = grab('<section class="band" id="s1">', '<!-- 2L -->')
    s2 = grab('<section class="band" id="s2"', '<!-- 3L -->')
    s3 = grab('<section class="band" id="s3"', '<section class="band" id="filters"')
    fl = grab('<section class="band" id="filters"', '<section class="band" style="padding-top:0">')
    pk = grab('<section class="band" style="padding-top:0">', '</div>\n\n  <section class="cta-band">')
    out = []
    for blk in (s1, s2, s3, fl, pk):
        blk = blk.replace('./img/', '../../assets/img/')
        blk = re.sub(r'<section class="band"[^>]*>', '', blk, count=1)
        blk = blk.rsplit('</section>', 1)[0]
        blk = blk.replace(' style="color:var(--muted);font-size:0.95rem;margin-bottom:8px;"', ' class="meta-line"')
        blk = blk.replace('<h2>', '<h2 class="reveal">')
        out.append(blk.strip())
    return out

def product():
    p = "../../"
    cache = ROOT / "tools" / "product_blocks.html"  # verbatim product blocks (extracted once from the /abadis/ demo)
    s1, s2, s3, fl, pk = cache.read_text(encoding="utf-8").split("\n<!--SPLIT-->\n") if cache.exists() else demo_blocks()
    # give size blocks anchors
    s1 = s1.replace('<div class="size-block">', '<div class="size-block" id="s1">', 1)
    s2 = s2.replace('<div class="size-block">', '<div class="size-block" id="s2">', 1)
    s3 = s3.replace('<div class="size-block">', '<div class="size-block" id="s3">', 1)
    extra = f"""<script type="importmap">{{"imports":{{"three":"{p}assets/vendor/three/build/three.module.js","three/addons/":"{p}assets/vendor/three/examples/jsm/"}}}}</script>"""
    viewer_js = """<script type="module">
  /* 3D viewer: lazy; rotation ONLY by explicit drag (no hover tracking). */
  const host = document.getElementById('productViewer');
  const ok = (() => { try { const c = document.createElement('canvas'); return !!(c.getContext('webgl2') || c.getContext('webgl')); } catch (_) { return false; } })();
  const fail = () => { host.classList.add('pv-failed'); const l = document.getElementById('viewerLoading'); if (l) l.classList.add('hide'); };
  if (host) { if (!ok) fail(); else { const io = new IntersectionObserver((en) => { if (en.some((x) => x.isIntersecting)) { io.disconnect(); import('../../assets/js/product-viewer.js').then((m) => m.initProductViewer(host)).catch((e) => { console.warn(e); fail(); }); } }, { rootMargin: '500px 0px' }); io.observe(host); } }
</script>"""
    body = f"""<main id="main">
  <section class="hero" aria-label="کیسه ساکشن آبادیس">
    {mosaic(p, 'hero', 12)}
    <div class="hero-inner">
      <p class="crumbs"><a href="{p}">خانه</a> › <a href="{p}products/">محصولات</a> › کیسه ساکشن</p>
      <span class="chip">محصولات · کیسه ساکشن یکبار مصرف</span>
      <h1>کیسه ساکشن <em>آبادیس</em></h1>
      <p class="lead">یک، دو و سه لیتری — با پودر ژل‌کننده، فیلتر هیدروفوبیک و سازگاری کامل با دستگاه‌های ساکشن بیمارستانی</p>
      <div class="hero-actions"><a class="btn btn-primary" href="#s2">مشخصات ۲ لیتری</a><a class="btn btn-ghost" href="{p}contact/">درخواست قیمت و نمونه</a></div>
    </div>
  </section>
  <nav class="anchors" aria-label="بخش‌های صفحه"><div class="wrap">
    <a href="#intro">معرفی</a><a href="#viewer">مدل سه‌بعدی</a><a href="#s1">۱ لیتری</a><a href="#s2">۲ لیتری</a><a href="#s3">۳ لیتری</a><a href="#filters">فیلترها</a><a href="#pack">بسته‌بندی</a><a href="#inquiry">استعلام</a>
  </div></nav>

  <section class="section" id="intro">
    <div class="wrap">
      <div class="section-head reveal"><h2>کیسه ساکشن یکبار مصرف</h2><p>تولید شرکت دانش‌بنیان مخازن طبی آبادیس برای کنترل عفونت و ایمنی جریان کار در مراکز درمانی</p></div>
      <div class="card prose reveal" style="margin-bottom:18px">
        <p>کیسه‌های ساکشن آبادیس در حجم‌های یک، دو و سه لیتری تولید می‌شوند و دارای سه نوع فیلتراسیون هیدروفوبیک، دوئال و مکانیکی هستند.</p>
        <p>ویژگی‌های مشترک: پودر ژل‌کننده، جلوگیری از سرریز مایعات، سازگاری با کلیه دستگاه‌های ساکشن، سیستم حفاظت از ساکشن مرکزی.</p>
        <p>قابل نصب به‌صورت تکی و سری روی پایه ثابت (دیواری) و پرتابل — نصب و خدمات پس از فروش رایگان.</p>
      </div>
      <div class="grid g-3">
        <article class="card reveal"><span class="num">۰۱</span><h3>فیلتر هیدروفوبیک</h3><p>جلوگیری از سرریز مایعات و حفاظت از پمپ و سیستم ساکشن مرکزی.</p></article>
        <article class="card reveal"><span class="num">۰۲</span><h3>پودر ژل‌کننده</h3><p>تبدیل مایع به ژل برای حمل ایمن‌تر و کاهش ریسک نشت.</p></article>
        <article class="card reveal"><span class="num">۰۳</span><h3>سازگاری کامل</h3><p>سازگار با کلیه دستگاه‌های ساکشن پرتابل و سانترال.</p></article>
      </div>
    </div>
  </section>

  <section class="section deep" id="viewer">
    <div class="wrap split">
      <div class="reveal">
        <p class="eyebrow">مدل سه‌بعدی</p>
        <h2>کیسه ساکشن ۲ لیتری</h2>
        <p style="margin-top:10px">برای چرخاندن، مدل را بکشید (فقط با کشیدن می‌چرخد).</p>
        <ul class="checks"><li>حجم ۲ لیتر تکی · تا ۸ لیتر سری یک‌ردیفه</li><li>قطر ۱۱ cm · ارتفاع ۲۴.۵ cm</li><li>فیلتر هیدروفوبیک / مکانیکی / CIF</li><li>۴۵ عدد در هر کارتن</li></ul>
        <a class="btn btn-light" href="#s2">جدول کدهای ۲ لیتری</a>
      </div>
      <div class="product-visual" id="productViewer">
        <img class="pv-fallback" src="{p}assets/img/product-still.webp" width="800" height="800" alt="کیسه ساکشن ۲ لیتری آبادیس" loading="lazy">
        <div class="product-visual-loading pv-loading" id="viewerLoading">بارگذاری مدل…</div>
        <canvas id="productCanvas" class="pv-canvas" aria-label="مدل سه‌بعدی کیسه ساکشن ۲ لیتری؛ برای چرخاندن بکشید"></canvas>
        <div class="product-visual-hint pv-hint">بکشید تا بچرخد</div>
      </div>
    </div>
  </section>

  <section class="section"><div class="wrap">
    {s1}
    {s2}
    {s3}
  </div></section>

  <section class="section section--alt" id="filters"><div class="wrap">
    {fl}
  </div></section>

  <section class="section" id="pack"><div class="wrap">
    {pk}
  </div></section>

  <section class="section" id="inquiry" style="padding-top:0"><div class="wrap">
    <div class="cta-band reveal">
      <h2>آماده سفارش برای مرکز درمانی شما</h2>
      <p>برای لیست قیمت، نمونه و هماهنگی نصب با تیم فروش مخازن طبی آبادیس در تماس باشید.</p>
      <div class="cta-actions"><a class="btn btn-light" href="tel:+982192001017">تماس با فروش</a><a class="btn btn-ghost" href="https://wa.me/989100145809" target="_blank" rel="noopener">درخواست نمونه در واتس‌اپ</a></div>
    </div>
  </div></section>
</main>
{LIGHTBOX}
"""
    write("products/suction-bag/index.html", head(p, "کیسه ساکشن یکبار مصرف — مخازن طبی آبادیس", "کیسه ساکشن یکبار مصرف آبادیس در حجم‌های ۱، ۲ و ۳ لیتری؛ دارای پودر ژل‌کننده، فیلتر هیدروفوبیک و سیستم حفاظت از ساکشن مرکزی.", extra) + header(p, "products") + body + footer(p, viewer_js))

# ------------------------------------------------------------------ CSR / ZAGROS
def csr():
    p = "../"
    body = f"""<div class="csr-bg" data-src="{p}assets/img/zagros-koh.jpg" aria-hidden="true"></div>
<div class="csr-veil" aria-hidden="true"></div>
<main id="main" class="csr-page">
  <section class="csr-hero" aria-label="نجات زاگرس">
    <div>
      <span class="chip">پویش نجات زاگرس · کاشت نهال بلوط</span>
      <h1>نجات زاگرس،‌مسئولیت اجتماعی آبادیس</h1>
      <p class="lead">کاشت نهال بلوط در ارتفاعات زاگرس؛ تا مکانی به نام آبادیس و به یاد صنعت سلامت کشور ثبت شود.</p>
      <div class="hero-actions" style="justify-content:center"><a class="btn btn-primary" href="#story">داستان پویش</a><a class="btn btn-ghost" href="{CSR_URL}" target="_blank" rel="noopener" style="color:var(--brand)">صفحهٔ فعلی پویش ↗</a></div>
    </div>
  </section>

  <section class="section" style="padding-top:0"><div class="wrap">
    <div class="glass csr-stats reveal">
      <div class="stat"><strong>۱۰۰۰</strong><span>نهال بلوط تا اردیبهشت ۱۴۰۳</span></div>
      <div class="stat"><strong>+۴۰۰</strong><span>مرکز درمانی؛ اعضای خانواده آبادیس</span></div>
      <div class="stat"><strong>۸۰۰</strong><span>نفر شرکت‌کننده در همایش نجات زاگرس</span></div>
    </div>
  </div></section>

  <section class="section" id="story"><div class="wrap" style="max-width:920px">
    <div class="glass prose reveal">
      <h2 style="margin-bottom:14px">زاگرس</h2>
      <p>جنگل‌های زاگرس به‌عنوان یکی از مهم‌ترین ذخایر اکولوژیکی کشور، طی سال‌های گذشته به دلایل متعددی از جمله آتش‌سوزی‌های گسترده، کشاورزی غیر اصولی و فعالیت‌های انسانی، دچار خسارت‌های جبران‌ناپذیری شده‌اند. طبق آمار، تنها در سال ۱۳۹۵ بیش از ۷۵ مورد آتش‌سوزی منجر به نابودی حدود ۹۵۰ هکتار از جنگل‌های زاگرس شد.</p>
      <p>همایش نجات زاگرس فرصتی است برای طرح یک راهکار عملیاتی، ویژه ی جنگل‌های زاگرس در راستای حفظ و نگهداری و احیاء جنگل های سوخته و جوان سازی جنگل های کهنسال. این راهکار از طریق کاشت هزارن نهال بلوط شروع می شود.</p>
      <p>بدین جهت آبادیس قدم بزرگی در راستای مسئولیت اجتماعی خود برداشت و با همکاری شرکت ایده‌پردازان نواندیش فردا با نام تجاری (<span class="latin">Dpaper</span>) برای نجات زاگرس به تعداد اعضای خانواده خود که بیش از 400 مرکز درمانی می باشد؛ با کاشت بلوط در روز درختکاری اثرگذاری خود را به طبیعت اثبات کرد و تا اردیبهشت سال 1403 به تعداد 1000 عدد می‌رساند تا در ارتفاعات زاگرس مکانی به نام آبادیس و به یاد صنعت سلامت کشور ثبت شود.</p>
    </div>
  </div></section>

  <section class="section" style="padding-top:0"><div class="wrap" style="max-width:920px">
    <div class="glass prose reveal">
      <h2 style="margin-bottom:14px">همایش نجات زاگرس</h2>
      <p>در تاریخ سه‌شنبه ۱۵ اسفندماه ۱۴۰۲، همزمان با روز درختکاری، همایش نجات زاگرس با حضور فعالان محیط زیست، متخصصان حوزه منابع طبیعی و حامیان این حرکت مردمی در مرکز همایش‌های بین‌المللی دانشگاه علم و فرهنگ برگزار شد. این رویداد به‌صورت حضوری و آنلاین و با مشارکت حدود ۸۰۰ نفر از علاقه‌مندان و کنشگران حوزه محیط زیست برگزار گردید.</p>
      <p>علاوه بر شرکت مخازن طبی آبادیس، شرکت شاتل، دیگر برندهای فعال بخش خصوصی و جمعی از هنرمندان مطرح کشور نیز از حامیان این رویداد و پروژه بزرگ کاشت بلوط در زاگرس بودند.</p>
      <p>در این همایش، بزرگانی که دغدغه حفاظت از محیط زیست را دارند، به سخنرانی و تبادل نظر پرداختند و تأکید کردند که مشارکت صنایع در پویش‌های محیط‌زیستی، گامی مهم در جهت توسعه پایدار است.</p>
      <p>مدیران مخازن طبی آبادیس به پاس همکاری با مراکز درمانی از سال‌های گذشته و همچنین اهدای لوح کاشت نهال بلوط در زاگرس به نام بیمارستان‌های پیشرو در کنترل عفونت به صورت حضوری با روسا و مدیران بیمارستان‌ها دیدار کردند.</p>
      <p>این دیدارها مورد استقبال فراوان رؤسای بیمارستان‌ها قرار گرفت؛ و رؤسای بیمارستان‌ها برای همراهی و همدلی، پویش آبادیس در راستای حفظ محیط زیست و نجات زاگرس را حمایت کردند.</p>
    </div>
  </div></section>

  <section class="section" style="padding-top:0"><div class="wrap" style="max-width:920px">
    <h2 class="reveal" style="margin-bottom:16px">مسیر پویش</h2>
    <div class="timeline">
      <div class="tl reveal"><time>روز درختکاری</time><p>آغاز کاشت بلوط به تعداد اعضای خانواده آبادیس؛ بیش از 400 مرکز درمانی.</p></div>
      <div class="tl reveal"><time>۱۵ اسفند ۱۴۰۲</time><p>همایش نجات زاگرس در مرکز همایش‌های بین‌المللی دانشگاه علم و فرهنگ، با مشارکت حدود ۸۰۰ نفر.</p></div>
      <div class="tl reveal"><time>اردیبهشت ۱۴۰۳</time><p>رساندن شمار نهال‌ها به 1000 عدد در ارتفاعات زاگرس.</p></div>
      <div class="tl reveal"><time>۳۰ تیر ۱۴۰۳</time><p>حمایت آبادیس از کارزار درخواست نجات زاگرس؛ مدیران و پرسنل آبادیس این کارزار را امضا نمودند.</p></div>
    </div>
  </div></section>

  <section class="section" style="padding-top:0"><div class="wrap" style="max-width:920px">
    <div class="glass prose reveal">
      <h2 style="margin-bottom:14px">کارزار درخواست نجات زاگرس</h2>
      <p>هچنین مجموعه آبادیس حامی کارزار درخواست نجات زاگرس که توسط انجمن‌های دوستدار طبیعت در تاریخ ۳۰ تیر ماه ۱۴۰۳ آغاز شده است؛ می‌باشد. مدیران مجموعه آبادیس و پرسنل آن از این کارزار حمایت کرده و این کارزار را امضا نمودند.</p>
      <details class="letter">
        <summary>متن کارزار درخواست نجات زاگرس</summary>
        <p>جناب آقای دکتر پزشکیان ریاست محترم جمهوری اسلامی ایران</p>
        <p>با سلام و احترام و تبریک انتخاب شایسته جنابعالی به ریاست دولت چهاردهم،</p>
        <p>قطعاً استحضار دارید که «زاگرس»، این کهن زیستگاه تمدن ایرانی، در معرض خطر جدی نابودی قرار دارد. آتش‌سوزی‌های مهلک و پیاپی از کهگیلویه و بویراحمد و لرستان تا کرمانشاه و کردستان و آذربایجان، هر ساله هزاران میلیارد تومان خسارت به منابع ملی کشور وارد می‌آورد. با توجه به وابستگی حیات طبیعی ایران به جنگل‌های زاگرس، اثرات مخرب این آتش‌سوزی‌ها به‌ویژه در این جنگل‌ها مشهودتر است.</p>
        <p>۱. ذخایر زیرزمینی آب زاگرس، اصلی‌ترین منابع آبی کشور را تشکیل می‌دهند و نفوذ و تجمع آب در این لایه‌ها به واسطه جنگل‌ها و پوشش گیاهی زاگرس ممکن می‌شود.</p>
        <p>۲. جنگل‌های زاگرس به عنوان فیلتر طبیعی برای جلوگیری از وزش غبار به ایران مرکزی و تعدیل‌کننده اکوسیستم حرارتی و رطوبتی کشور عمل می‌کنند. این جنگل‌ها جذب‌کننده ابرهای باران‌زا به تمام پهنه کشور هستند و ارزش آنها به عنوان بخشی از سرمایه ملی و ذخیرگاه حیاتی و گیاهی و جانوری کشور غیرقابل انکار است. هم‌اکنون یک چهارم از سکونتگاه‌های شهری و روستایی ایران در دامنه‌ها و دشت‌های میانی زاگرس از آذربایجان تا خلیج فارس استقرار یافته‌اند.</p>
        <p>از شما و دولت دانش‌محور جنابعالی تقاضا داریم به‌طور فوری و کارشناسانه به این مسأله ورود کنید. برای همفکری با شما و دولت محترم، رئوس پیشنهادات ما به شرح زیر است:</p>
        <p>۱. تجهیز ادارات منابع طبیعی استان‌های حوزه زاگرس به ادوات و تجهیزات پیشرفته برای مقابله سریع با حریق.</p>
        <p>۲. تهیه و تأمین هواپیماها و هلی‌کوپترهای آب‌پاش از شرکت‌های داخلی و خارجی در فصل تابستان که در آماده‌باش کامل برای ادارات منابع طبیعی یا مدیریت بحران استان‌ها، به ویژه استان کرمانشاه، قرار گیرد.</p>
        <p>۳. استفاده فوری از هلی‌کوپترهای در اختیار هلال‌احمر، هوانیروز و سپاه برای اطفاء حریق جنگل‌ها و تجهیز آنها در اختیار ادارات کل منابع طبیعی و سرجنگلداری قرار داده شود.</p>
        <p>۴. به عنوان یک طرح اضطراری و پیشتاز، لازم است تعداد کافی پست‌های اطفاء حریق و حفاظت از جنگل‌ها با قابلیت پوشش منطقه‌ای و تجهیزات کافی در مناطق خطرزا احداث شود. در مرحله اول، احداث ۱۰ پست در استان کرمانشاه ضروری به نظر می‌رسد.</p>
        <p>۵. سازماندهی روستانشینان منطقه و تأمین تجهیزات لازم برای واکنش و مقابله سریع با آتش‌سوزی‌ها و به رسمیت شناختن این تشکل‌ها که به تجربه کارآیی خود را اثبات کرده‌اند، از جمله اقدامات اساسی و پیشگام خواهد بود.</p>
        <p>۶. لازم است نقشه پهنه‌بندی خطر آتش‌سوزی برای استان کرمانشاه (و سایر استان‌های حوزه زاگرس) تهیه شده و چگونگی واکنش و دسترسی سریع به این مناطق در هنگام بروز خطر آموزش داده شود.</p>
        <p>۷. ادارات کل منابع طبیعی با همکاری مدیریت بحران استان باید برنامه ویژه مدیریت بحران آتش‌سوزی جنگل‌های زاگرس را طی مطالعات تخصصی تهیه کرده و در آن ضمن پیش‌بینی و پیش‌نگری کافی، چگونگی اجرای اقدامات اطفاء و ایجاد موانع فیزیکی در مسیر حریق‌ها را ارائه دهند.</p>
        <p>۸. و سرانجام، علت اصلی آتش‌سوزی‌ها خشکسالی و کمبود رطوبت در پهنه زاگرس است. با انتقال شاخه کوچکی از طرح انتقال آب سیروان سردسیری به حوزه زاگرس و ایجاد مقداری رطوبت، حیات گیاهی پوشش سبز زاگرس تداوم بهتری خواهد یافت. این پیشنهاد لازم است توسط وزارت نیرو، وزارت جهاد کشاورزی و سازمان جنگل‌ها و مراتع کشور مورد مطالعه و اجرایی قرار گیرد.</p>
        <p>در پایان، ما دست در دست شما برای نجات ایران رنجور و خسته، آماده هستیم.</p>
        <p>با احترام و امید به اقدام مؤثر</p>
      </details>
    </div>
  </div></section>

  <section class="section" style="padding-top:0"><div class="wrap" style="max-width:920px">
    <div class="cta-band reveal">
      <h2>ما به اندازه یک سرانگشت اثر می‌گذاریم</h2>
      <p>به شما، به طبیعت، به جهان.</p>
      <div class="cta-actions"><a class="btn btn-light" href="{CSR_URL}" target="_blank" rel="noopener">شناسنامه بلوط‌ها و جزئیات بیشتر</a><a class="btn btn-ghost" href="{p}contact/">ارتباط با ما</a></div>
    </div>
  </div></section>
</main>
"""
    extra = f'<link rel="preload" href="{p}assets/img/zagros-koh.jpg" as="image">'
    write("csr/index.html", head(p, "نجات زاگرس، مسئولیت اجتماعی آبادیس", "پویش نجات زاگرس؛ کاشت نهال بلوط در ارتفاعات زاگرس به نام آبادیس و به یاد صنعت سلامت کشور.", extra) + header(p, "csr", solid=True) + body + footer(p))

# ------------------------------------------------------------------ CONTACT
def contact():
    p = "../"
    body = f"""<main id="main">
  <section class="hero hero--short" aria-label="ارتباط با ما">
    {mosaic(p, 'hero', 14)}
    <div class="hero-inner">
      <p class="crumbs"><a href="{p}">خانه</a> › ارتباط با ما</p>
      <span class="chip">فروش · نمایندگی · مشاوره</span>
      <h1>با ما در ارتباط <em>باشید...</em></h1>
      <p class="lead">برای لیست قیمت، نمونه، نمایندگی و هماهنگی نصب با تیم مخازن طبی آبادیس تماس بگیرید.</p>
    </div>
  </section>
  <section class="section"><div class="wrap grid g-2" style="gap:24px;align-items:start">
    <div class="card reveal">
      <h2 style="font-size:1.4rem;margin-bottom:16px">راه‌های ارتباطی</h2>
      <dl class="contact-dl">
        <dt>مرکز تماس:</dt><dd><a href="tel:+982192001017" dir="ltr">02192001017</a></dd>
        <dt>تلفن تماس:</dt><dd><a href="tel:+982122671845" dir="ltr">02122671845</a> | <a href="tel:+982122205502" dir="ltr">02122205502</a><br><a href="tel:+982122215503" dir="ltr">02122215503</a> | <a href="tel:+982122218910" dir="ltr">02122218910</a></dd>
        <dt>فکس:</dt><dd><span dir="ltr">02141425555</span> | داخلی 28544</dd>
        <dt>پست الکترونیک:</dt><dd><a href="mailto:info@abadis-med.com">info@abadis-med.com</a></dd>
        <dt>واتس‌اپ:</dt><dd><a href="https://wa.me/989100145809" target="_blank" rel="noopener" dir="ltr">+989100145809</a></dd>
        <dt>دفتر مرکزی:</dt><dd>ایران، تهران، قیطریه، خیابان اندرزگو، پلاک 104، واحد2</dd>
        <dt>کارخانه:</dt><dd>ایران،تهران،شهرک صنعتی شمس آباد، بلوار گلستان، کوچه گلشن ۱۹،پلاک۱۷</dd>
      </dl>
      <div class="doc-links"><a href="{LIVE}/لیست-نمایندگان/" target="_blank" rel="noopener">لیست نمایندگان</a><a href="{LIVE}/ارتباط-با-ما/" target="_blank" rel="noopener">صفحهٔ فعلی ارتباط با ما</a></div>
    </div>
    <form class="card form reveal" id="leadForm">
      <h2 style="font-size:1.4rem">فرم درخواست</h2>
      <label>نام و نام خانوادگی<input name="name" required autocomplete="name"></label>
      <label>مرکز درمانی / شرکت<input name="org" autocomplete="organization"></label>
      <label>تلفن تماس<input name="phone" type="tel" dir="ltr" required autocomplete="tel"></label>
      <label>موضوع<select name="topic"><option>استعلام قیمت</option><option>درخواست نمونه</option><option>نمایندگی و همکاری</option><option>صادرات</option><option>پشتیبانی و نصب</option></select></label>
      <label>پیام<textarea name="msg"></textarea></label>
      <button class="btn btn-primary" type="submit">آماده‌سازی ایمیل</button>
      <p class="hint">این پیش‌نمایش سرور فرم ندارد؛ با زدن دکمه، ایمیل آماده در برنامهٔ ایمیل شما باز می‌شود.</p>
      <p class="form-status" id="formStatus" role="status"></p>
    </form>
  </div></section>
</main>
"""
    write("contact/index.html", head(p, "ارتباط با ما — مخازن طبی آبادیس", "راه‌های ارتباط با مخازن طبی آبادیس: مرکز تماس، تلفن، ایمیل، واتس‌اپ و نشانی دفتر مرکزی و کارخانه.") + header(p, "contact") + body + footer(p))

if __name__ == "__main__":
    home(); products(); product(); csr(); contact()
    (SITE / ".nojekyll").write_text("")
