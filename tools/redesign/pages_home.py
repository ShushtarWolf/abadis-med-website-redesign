"""Generate site/index.html — Zagros hero + about / why / calculator / news / articles / customers."""
from lib import PAGES, esc, fa
import pages_dial
from layout import page, section_mark
from render import picture
import pages_posts

# Verbatim home copy (from live / prior home — do not invent)
ABOUT_P = ('پس از سال ها برنامه ریزی و ادامه دادن جریان ایجاد شده و با پویایی و تغییرات سیستم مدیریتی '
           'در سال ۲۰۱۷ شرکت دانش بنیان مخازن طبی آبادیس را بنا نهادیم تا هم تولید کیسه ساکشن یکبار مصرف آبادیس را '
           'آغاز کنیم و هم با اهداف خود در حوزه کنترل عفونت بیمارستانی و تجهیزات پزشکی گام های محکم تری برداریم ؛ '
           'و فهمیدیم که ما برای اثر گذاری آمده ایم…')
GOALS = [
    '۱. مدیریت بهینه زباله‌های عفونی و مایع بیمارستانی',
    '۲. کاهش و کنترل عفونت‌های ناشی از زباله‌ها و سیالات بیمارستانی',
    '۳. فرهنگ‌سازی برای استفاده حداکثری از راهکارها و محصولات ما در مراکز درمانی و بیمارستان‌ها',
]
FACTORY_LEAD = ('کارخانه دانش‌بنیان تجهیزات پزشکی آبادیس در سال ۱۳۹۷ با بهره‌گیری از پیشرفته‌ترین تجهیزات و '
                'ماشین‌آلات و با همکاری نیروهای متخصص راه‌اندازی شد. این کارخانه با ظرفیت تولید سالانه ۵ میلیون '
                'کیسه ساکشن یکبارمصرف، به‌عنوان بزرگ‌ترین تولیدکننده این محصولات در منطقه خاورمیانه شناخته می‌شود.')
WHY_CHECKS = [
    'کاهش هزینه ها',
    'ارائه محصولات با کیفیت',
    'ارتباط مستمر آبادیس با مراکز درمانی',
    'ارسال رایگان',
    'تحویل در کوتاه ترین زمان ممکن',
]
ZAGROS_LEAD = 'کاشت نهال بلوط در ارتفاعات زاگرس؛ تا مکانی به نام آبادیس و به یاد صنعت سلامت کشور ثبت شود.'
HOME_DESC = ('شرکت دانش‌بنیان مخازن طبی آبادیس؛ تولیدکننده کیسه ساکشن یکبار مصرف و '
             'راهکارهای مدیریت سیالات و زباله‌های عفونی بیمارستانی.')
# Ends with brand so layout.head does not double-suffix
HOME_TITLE = 'تولیدکنندهٔ کیسه ساکشن یک‌بارمصرف و راهکارهای مدیریت مایعات بیمارستانی — مخازن طبی آبادیس'
CALC_TEASER = 'جهت محاسبه آنلاین میزان صرفه‌جویی در مصرف آب و زباله‌های عفونی مرکز خود می‌توانید روی دکمه زیر کلیک نمایید.'
LOGO_STRIP_N = 24


def _B(path):
    return PAGES[path]['blocks']


def zagros_hero(img_base):
    """Full-viewport Zagros scroll scene (shared assets under site/csr/img/hero/)."""
    b = img_base.rstrip('/') + '/'
    return f'''  <div class="zh-track" id="hero" data-img-base="{esc(b)}">
    <div class="zh-stage" id="zhStage">
      <div class="zh-bg" aria-hidden="true">
        <picture>
          <source type="image/webp" srcset="{b}bg-dry-1280.webp 1280w, {b}bg-dry.webp 1920w" sizes="(max-aspect-ratio: 16/9) 177.78vh, 100vw">
          <img class="zh-bg-layer zh-bg-dry" src="{b}bg-dry.jpg" srcset="{b}bg-dry-1280.jpg 1280w, {b}bg-dry.jpg 1920w" sizes="(max-aspect-ratio: 16/9) 177.78vh, 100vw" alt="" width="1920" height="1080" decoding="async" fetchpriority="high">
        </picture>
        <picture>
          <source type="image/webp" srcset="{b}bg-mid-1280.webp 1280w, {b}bg-mid.webp 1920w" sizes="(max-aspect-ratio: 16/9) 177.78vh, 100vw">
          <img class="zh-bg-layer zh-bg-mid" src="{b}bg-mid.jpg" srcset="{b}bg-mid-1280.jpg 1280w, {b}bg-mid.jpg 1920w" sizes="(max-aspect-ratio: 16/9) 177.78vh, 100vw" alt="" width="1920" height="1080" decoding="async">
        </picture>
        <picture>
          <source type="image/webp" srcset="{b}bg-green-1280.webp 1280w, {b}bg-green.webp 1920w" sizes="(max-aspect-ratio: 16/9) 177.78vh, 100vw">
          <img class="zh-bg-layer zh-bg-green" src="{b}bg-green.jpg" srcset="{b}bg-green-1280.jpg 1280w, {b}bg-green.jpg 1920w" sizes="(max-aspect-ratio: 16/9) 177.78vh, 100vw" alt="" width="1920" height="1080" decoding="async">
        </picture>
      </div>
      <div class="zh-spots" id="zhSpots" aria-hidden="true"></div>
      <div class="zh-canister" id="zhCanister" aria-hidden="true">
        <span class="zh-canister-glow"></span>
        <picture>
          <source type="image/webp" srcset="{b}canister.webp">
          <img src="{b}canister.png" alt="" width="399" height="900" decoding="async">
        </picture>
      </div>
      <div class="zh-dusk" aria-hidden="true"></div>
      <div class="zh-veil" aria-hidden="true"></div>
      <div class="zh-exit" id="zhExit" aria-hidden="true"></div>
      <div class="zh-hint" id="zhHint" aria-hidden="true"><i></i></div>
    </div>
  </div>'''


# Verbatim from the live abadis-med.com home hero (Revolution Slider slide 1: title image + 3 cert buttons).
LIVE_HERO_H1 = 'شرکت دانش بنیان مخازن طبی آبادیس'


HERO_H1 = 'تولیدکنندهٔ کیسه ساکشن یک‌بارمصرف و راهکارهای مدیریت مایعات بیمارستانی'
# Provable from abadis-med.com: certificates (hero slider) + sizes/filters (product page)
HERO_SUB = 'دارای گواهی‌های IMED، ISO و CE؛ کیسه ساکشن در حجم‌های ۱، ۲ و ۳ لیتری با فیلتر هیدروفوبیک، دوئال و مکانیکی.'
CATALOGUE = 'https://abadis-med.com/wp-content/uploads/2024/12/کاتالوگ-جامع-آبادیس.pdf'


def or_hero(media, zagros='csr/img/hero/'):
    """Above the fold (brief §2): product first. Real Abadis product photo over the graded
    operating-room clip; headline, one provable sub-line, two CTAs, certificate chips."""
    m = media.rstrip('/') + '/'
    return f'''  <section class="home-or home-or--product" id="intro" aria-label="معرفی محصول آبادیس">
    <div class="home-or-media" aria-hidden="true">
      <img class="home-or-fill" src="{m}hero-or-zagros-poster.jpg" alt="" width="640" height="1214" decoding="async" fetchpriority="high">
      <video class="home-or-video" id="homeOrVideo" muted loop playsinline autoplay preload="metadata" poster="{m}hero-or-zagros-poster.jpg" disablepictureinpicture disableremoteplayback tabindex="-1">
        <source src="{m}hero-or-zagros.mp4" type="video/mp4">
      </video>
      <div class="home-or-veil"></div>
    </div>
    <div class="wrap home-hero-grid">
      <div class="home-hero-copy">
        <h1>{esc(HERO_H1)}</h1>
        <p class="home-hero-sub">{esc(HERO_SUB)}</p>
        <div class="hero-actions">
          <a class="btn btn-primary" href="{esc(CATALOGUE)}" target="_blank" rel="noopener" data-track="catalogue_download" data-track-label="home_hero_catalogue">دریافت کاتالوگ</a>
          <a class="btn btn-ghost" href="export/#quote" data-track="contact_click" data-track-label="home_hero_quote">درخواست قیمت / همکاری صادراتی</a>
        </div>
      </div>
      <figure class="home-hero-product">
        <img src="assets/img/p/hero-bags.webp" alt="کیسه ساکشن یکبار مصرف ۱ و ۲ لیتری آبادیس" width="555" height="554" decoding="async" fetchpriority="high">
      </figure>
    </div>
  </section>'''


def trust_section():
    """Trust evidence right after the hero: the three certificates (opens the lightbox)."""
    certs = [('گواهی IMED', 'assets/img/certs/cert-imed.webp', 1131, 1600),
             ('گواهی ISO', 'assets/img/c/19ffe783abd3-1600.webp', 1108, 1523),
             ('گواهی CE', 'assets/img/certs/cert-ce.webp', 1163, 1600)]
    cards = ''.join(
        f'<a class="card cert-card reveal" href="{h}" data-gallery="home-certs" data-w="{w}" data-h="{hh}">'
        f'<img src="{h}" alt="{esc(t)} مخازن طبی آبادیس" width="{w}" height="{hh}" loading="lazy" decoding="async"><strong>{esc(t)}</strong></a>'
        for t, h, w, hh in certs)
    return f'''  <section class="section" id="trust">
    <div class="wrap">
      <div class="section-head reveal"><p class="eyebrow">اعتماد</p><h2>گواهی‌ها و استانداردها</h2></div>
      <div class="grid g-3 cert-grid">{cards}</div>
    </div>
  </section>'''


USES = ['اتاق عمل', 'CCU/ICU', 'اورژانس', 'NICU/PICU', 'ریه و آندوسکوپی', 'گوارش', 'عفونی', 'بخش زنان', 'بخش مردان', 'ECT']


def uses_specs_section():
    uses = ''.join(f'<li>{esc(u)}</li>' for u in USES)
    rows = [('ظرفیت', '۱، ۲ و ۳ لیتر'), ('فیلتراسیون', 'هیدروفوبیک، دوئال و مکانیکی'),
            ('ویژگی‌ها', 'پودر ژل‌کننده، جلوگیری از سرریز مایعات، سیستم حفاظت از ساکشن مرکزی'),
            ('سازگاری', 'کلیه دستگاه‌های ساکشن پرتابل و سانترال'),
            ('نصب', 'تکی و سری روی پایه ثابت (دیواری) و پرتابل — نصب و خدمات پس از فروش رایگان')]
    body = ''.join(f'<tr><th scope="row">{esc(k)}</th><td>{esc(v)}</td></tr>' for k, v in rows)
    return f'''  <section class="section section--alt" id="uses">
    <div class="wrap split">
      <div class="reveal">
        <p class="eyebrow">کاربردها</p>
        <h2>کاربرد در بخش‌های بیمارستان</h2>
        <ul class="checks use-list" style="margin-top:16px">{uses}</ul>
        <p style="margin-top:18px"><a class="more-link" href="products/">همهٔ محصولات ←</a></p>
      </div>
      <div class="reveal">
        <p class="eyebrow">مشخصات</p>
        <h2>کیسه ساکشن یکبار مصرف</h2>
        <table class="spec-table" style="margin-top:14px"><tbody>{body}</tbody></table>
        <p style="margin-top:14px"><a class="more-link" href="products/suction-bag/#specs">مشخصات کامل و کد محصولات ←</a></p>
      </div>
    </div>
  </section>'''


def experiences_teaser():
    out = []
    cur = None
    for b in _B('/تجارب-ما/'):
        if b['t'] == 'h':
            cur = [b['text'], '']; out.append(cur)
        elif b['t'] == 'html' and cur:
            cur[1] += b['html']
    from lib import strip_tags
    cards = ''.join(
        f'<a class="card teaser reveal" href="academy/#experiences"><span class="tag">تجربهٔ مشتری</span><h3>{esc(t)}</h3>'
        f'<p>{esc(strip_tags(h)[:150])}…</p></a>' for t, h in out[:3])
    return f'''  <section class="section section--alt" id="experiences">
    <div class="wrap">
      <div class="section-head reveal"><p class="eyebrow">تجربه‌ها</p><h2>تجارب ما</h2>
        <p><a class="more-link" style="margin:0" href="academy/#experiences">همهٔ تجربه‌ها ←</a></p></div>
      <div class="grid g-3">{cards}</div>
    </div>
  </section>'''


DOCS = [('https://abadis-med.com/wp-content/uploads/2024/12/کاتالوگ-جامع-آبادیس.pdf', 'کاتالوگ جامع آبادیس'),
        ('https://abadis-med.com/wp-content/uploads/2022/12/suction-bag-catalog-Fa.pdf', 'کاتالوگ کیسه ساکشن'),
        ('https://abadis-med.com/wp-content/uploads/2022/12/Filter-catalog-Fa.pdf', 'کاتالوگ فیلترها'),
        ('https://abadis-med.com/wp-content/uploads/2026/01/کاتالوگ-ساکشن-تیوب-1.pdf', 'کاتالوگ ساکشن تیوب')]


def docs_section():
    links = ''.join(f'<a href="{esc(h)}" target="_blank" rel="noopener" data-track="catalogue_download">{esc(t)} (PDF)</a>' for h, t in DOCS)
    return f'''  <section class="section" id="docs">
    <div class="wrap">
      <div class="section-head reveal"><p class="eyebrow">اسناد فنی</p><h2>کاتالوگ‌ها و راهنماها</h2></div>
      <div class="doc-links reveal">{links}<a href="install-guide/">راهنمای نصب</a><a href="faq/">پرسش‌های متداول</a><a href="downloads/">مرکز دانلود</a></div>
    </div>
  </section>'''


def about_section():
    goals = ''.join(f'<li>{esc(g)}</li>' for g in GOALS)
    return f'''  <section class="section section--alt" id="about">
    <div class="wrap split">
      <div class="reveal">
        <p class="eyebrow">آشنایی با ما</p>
        <h2>درباره ما</h2>
        <div class="prose" style="margin-top:14px">
          <p>{esc(ABOUT_P)}</p>
        </div>
        <p style="margin-top:18px"><a class="more-link" href="about/">بیشتر درباره آبادیس ←</a></p>
      </div>
      <div class="reveal">
        <h3 style="font-weight:900;font-size:1.2rem">اهداف ما</h3>
        <ul class="goals">{goals}</ul>
      </div>
    </div>
  </section>'''


def why_section():
    checks = ''.join(f'<li>{esc(c)}</li>' for c in WHY_CHECKS)
    return f'''  <section class="section deep" id="why">
    <div class="wrap split">
      <div class="reveal">
        <p class="eyebrow">کارخانه · اثرگذاری</p>
        <h2>چرا آبادیس</h2>
        <p style="margin-top:12px">{esc(FACTORY_LEAD)}</p>
        <ul class="checks" style="margin-top:22px">{checks}</ul>
      </div>
      <div class="media-frame reveal"><video class="media-video" aria-hidden="true" muted loop playsinline autoplay preload="auto" poster="assets/media/or-poster.jpg" disablepictureinpicture disableremoteplayback tabindex="-1">
        <source src="assets/media/or-mosaic.mp4" type="video/mp4">
      </video></div>
    </div>
    <div class="wrap" style="margin-top:28px">
      <div class="grid g-3">
        <div class="card stat reveal"><strong>+۱٬۰۰۰</strong><span>همراه با بیش از ۱٬۰۰۰ مرکز درمانی در سطح کشور</span></div>
        <div class="card stat reveal"><strong>۵ میلیون</strong><span>ظرفیت تولید سالانه کیسه ساکشن یکبارمصرف</span></div>
        <div class="card stat reveal"><strong>۱۳۹۷</strong><span>راه‌اندازی کارخانه دانش‌بنیان آبادیس</span></div>
      </div>
    </div>
  </section>'''


def calculator_section():
    return f'''  <section class="section section--alt" id="calculator">
    <div class="wrap">
      <div class="home-calc reveal">
        <div>
          <p class="eyebrow">محاسبه‌گر</p>
          <h2>محاسبه‌گر صرفه‌جویی</h2>
          <p>{esc(CALC_TEASER)}</p>
        </div>
        <a class="btn btn-primary" href="calculator/">محاسبه‌گر</a>
      </div>
    </div>
  </section>'''


def _teasers(cat, n=3):
    pages_posts.prepare()
    tag = pages_posts.TAG[cat]
    combined = (
        [('miss', m) for m in pages_posts.MISSING if m['cat'] == cat]
        + [('post', x) for x in pages_posts.POSTS if x['cat'] == cat]
    )
    combined.sort(key=lambda t: t[1]['date'], reverse=True)
    out = []
    for kind, x in combined[:n]:
        if kind == 'miss':
            out.append(
                f'<a class="card teaser reveal" href="{esc(x["url"])}" target="_blank" rel="noopener">'
                f'<span class="tag">{esc(tag)}</span><h3>{esc(x["t"])}</h3></a>'
            )
        else:
            r = pages_posts.thumb('', x)
            ph = (f'<span class="teaser-ph"><img src="{r["src"]}" width="{r["w"]}" height="{r["h"]}" alt="{esc(x["t"])}" loading="lazy" decoding="async"></span>' if r else '')
            out.append(
                f'<a class="card teaser reveal{" has-ph" if r else ""}" href="{esc(x["rel"])}">{ph}'
                f'<span class="tag">{esc(tag)}</span><h3>{esc(x["t"])}</h3></a>'
            )
    return ''.join(out)


def news_section():
    return f'''  <section class="section" id="news">
    <div class="wrap">
      <div class="section-head reveal"><p class="eyebrow">اخبار</p><h2>آخرین اخبار</h2>
        <p><a class="more-link" style="margin:0" href="news/">همهٔ اخبار ←</a></p></div>
      <div class="grid g-3">{_teasers('news')}</div>
    </div>
  </section>'''


def articles_section():
    return f'''  <section class="section section--alt" id="articles">
    <div class="wrap">
      <div class="section-head reveal"><p class="eyebrow">مقالات</p><h2>مقالات</h2>
        <p><a class="more-link" style="margin:0" href="articles/">همهٔ مقالات ←</a></p></div>
      <div class="grid g-3">{_teasers('articles')}</div>
    </div>
  </section>'''


def customers_section():
    p = ''
    bl = _B('/مشتریان-ما/')
    items = bl[1]['items']
    logos = []
    for it in items:
        if len(logos) >= LOGO_STRIP_N:
            break
        im = next((x for x in it['blocks'] if x['t'] == 'img'), None)
        name = next((x['text'] for x in it['blocks'] if x['t'] == 'h'), '')
        if not im:
            continue
        pic = picture(p, im['src'], im.get('alt') or name, 300)
        if not pic:
            continue
        logos.append(
            f'<div class="home-logo" role="group" aria-label="{esc(name)}" title="{esc(name)}">{pic}</div>'
        )
    return f'''  <section class="section" id="customers">
    <div class="wrap">
      <div class="section-head reveal"><p class="eyebrow">مشتریان</p><h2>مشتریان</h2>
        <p>همراه با بیش از {fa(len(items))} مرکز درمانی در سطح کشور.</p>
        <p><a class="more-link" style="margin:0" href="customers/">همهٔ مشتریان</a></p></div>
      <div class="logo-carousel reveal" data-logo-carousel>
        <button type="button" class="logo-carousel-btn logo-carousel-prev" aria-label="قبلی">‹</button>
        <div class="logo-carousel-track" tabindex="0" aria-label="نمونهٔ مشتریان">
          {''.join(logos)}
        </div>
        <button type="button" class="logo-carousel-btn logo-carousel-next" aria-label="بعدی">›</button>
      </div>
      <p class="home-logo-cta reveal"><a class="btn btn-ghost" href="customers/">مشاهدهٔ فهرست مشتریان</a></p>
    </div>
  </section>'''



# ---------------------------------------------------------------- Alireza review (Oct 2026) home
# Live abadis-med.com home, re-read 2026-10-14 (verbatim)
LIVE_ABOUT = ('شرکت دانش‌بنیان مخازن طبی آبادیس با تکیه بر دانش روز و ارائه محصولات و راهکارهای نوآورانه در مدیریت '
              'سیالات و زباله‌های عفونی بیمارستانی، گام‌های موثری در راستای کنترل عفونت‌های بیمارستانی و دستیابی به توسعه پایدار '
              'برداشته است. هدف ما اثرگذاری واقعی در بهبود سلامت مراکز درمانی و حفاظت از محیط زیست است.')
LIVE_VALUES = [('کاهش هزینه‌ها', 'کاهش هزینه‌های مربوط به مواد شست‌و‌شو، مصرف آب، برق و منابع انسانی'),
               ('مدیریت زباله‌های بیمارستانی و عفونی', 'باعث جمع‌آوری بهتر زباله‌های مایع و عفونی می‌گردد.'),
               ('بازیافت پذیر', 'باعث کاهش حجم زباله‌های بیمارستانی و حفظ محیط‌زیست می‌گردد.'),
               ('استفاده آسان', 'حذف فعالیت‌های مربوط به شست‌و‌شوی مخازن و استفاده راحت برای جمع‌آوری ضایعات حین عمل')]
SLOGAN = ['ما به اندازه یک سرانگشت اثر می‌گذاریم،', 'به شما', 'به طبیعت', 'به جهان']
import hashlib as _hl
_UP = 'https://abadis-med.com/wp-content/uploads/'
MEMBERSHIP_URLS = [_UP + '2023/03/' + x for x in ('Template_0000_1-2-copy.webp', 'Template_0000_logo2-copy.webp', 'Template_0000_main-logo-copy.webp',
                   'Template_0000s_0000_logo_1-1-1-copy.webp', 'Template_0001_ISCC1-copy.webp', 'Template_0004_2-copy.webp', 'Template_0006_download-copy.webp')] + \
                  [_UP + '2023/12/-صنعت-و-معدن-جوانان-ایران-e1702381162586.png', _UP + '2023/12/مجمع-خیرین-صنف-تجهیزات-پزشکی.png']
MEMBERSHIPS = [_hl.md5(x.encode()).hexdigest()[:10] for x in MEMBERSHIP_URLS]   # downloaded by /tmp/dl.py naming (md5[:10])


def _live(name):
    return f'assets/img/live/{name}.webp'


def hero_v2():
    return f'''  <section class="hx" data-tone="dark" id="intro" aria-label="کیسه ساکشن یکبار مصرف آبادیس">
    <div class="hx-bg" aria-hidden="true"><span class="hx-grid"></span><span class="hx-ring hx-ring--a"></span><span class="hx-ring hx-ring--b"></span><span class="hx-scan"></span></div>
    <div class="wrap hx-inner">
      <div class="hx-copy">
        <p class="hx-kicker">شرکت دانش‌بنیان مخازن طبی آبادیس</p>
        <h1>{esc(HERO_H1)}</h1>
        <p class="hx-sub">{esc(HERO_SUB)}</p>
        <div class="hero-actions">
          <a class="btn btn-primary" href="{esc(CATALOGUE)}" target="_blank" rel="noopener" data-track="catalogue_download" data-track-label="home_hero_catalogue">دریافت کاتالوگ</a>
          <a class="btn btn-ghost" href="export/#quote" data-track="contact_click" data-track-label="home_hero_quote">درخواست قیمت / همکاری صادراتی</a>
        </div>
      </div>
      <figure class="hx-product">
        <span class="hx-glow" aria-hidden="true"></span>
        <img src="assets/img/p/hero-bags.webp" alt="کیسه ساکشن یکبار مصرف ۱ و ۲ لیتری آبادیس" width="555" height="554" decoding="async" fetchpriority="high">
      </figure>
    </div>
  </section>'''


def about_v2():
    goals = ''.join(f'<li>{esc(g)}</li>' for g in GOALS)
    return f'''  <section class="section" id="about">
    <div class="wrap split">
      <div class="reveal">
        <p class="eyebrow">آشنایی با ما</p>
        <h2>درباره مجموعه دانش بنیان آبادیس</h2>
        <p style="margin-top:12px;text-align:justify">{esc(LIVE_ABOUT)}</p>
        <h3 style="font-weight:900;font-size:1.1rem;margin-top:18px">اهداف ما:</h3>
        <ul class="goals">{goals}</ul>
        <p style="margin-top:18px"><a class="more-link" href="about/">بیشتر بخوانید ←</a></p>
      </div>
      <figure class="video-slot reveal" data-video-slot="home-about">
        <img src="{_live('86201b7b17')}" alt="کارخانه دانش‌بنیان تجهیزات پزشکی آبادیس" width="1024" height="576" loading="lazy" decoding="async">
        <figcaption>جای ویدیوی معرفی آبادیس (فایل ویدیو در انتظار)</figcaption>
      </figure>
    </div>
  </section>'''


# Approved scroll-growth emblem (animator/logo-scroll, animation B) plus the living loop
# and T1 slogan wipe. The SVG is the complete static mark: logo-scroll.js hides and draws
# it only when GSAP loaded and motion is allowed.
IMPACT_MARK = (
    '<svg class="impact-mark logo-grow" aria-hidden="true" focusable="false" viewBox="60 -10 760 820" xmlns="http://www.w3.org/2000/svg">'
    '<g fill="none" stroke="currentColor" stroke-width="10" stroke-linecap="round">'
    '<path class="leaf l0" pathLength="1" d="M400 625 C380 520 300 440 185 470"/>'
    '<path class="leaf l1" pathLength="1" d="M405 625 C420 480 500 390 612 378"/>'
    '<path class="leaf l2" pathLength="1" d="M395 615 Q350 560 262 522"/>'
    '<path class="leaf l3" pathLength="1" d="M410 612 Q450 530 528 500"/>'
    '<path class="stem" pathLength="1" d="M405 625 L405 75"/>'
    '<path class="br b0" style="--i:0" pathLength="1" d="M405 140 L447 93"/>'
    '<path class="br b1" style="--i:1" pathLength="1" d="M405 205 L350 150"/>'
    '<path class="br b2" style="--i:2" pathLength="1" d="M405 285 L465 230"/>'
    '<path class="br b3" style="--i:3" pathLength="1" d="M405 330 L322 248"/>'
    '<path class="br b4" style="--i:4" pathLength="1" d="M405 395 L485 325"/>'
    '<path class="br b5" style="--i:5" pathLength="1" d="M405 455 L318 378"/>'
    '<path class="arc a0 inner" style="--i:0" pathLength="1" d="M225 248 A228 228 0 1 0 555 245"/>'
    '<path class="arc a1 mid" style="--i:1" pathLength="1" d="M210 160 A307 307 0 0 0 112 525"/>'
    '<path class="arc a2 mid" style="--i:2" pathLength="1" d="M603 183 A304 304 0 0 1 390 708"/>'
    '<path class="arc a3 outer" style="--i:3" pathLength="1" d="M392 18 A386 386 0 0 0 185 728"/>'
    '<path class="arc a4 outer" style="--i:4" pathLength="1" d="M535 45 A386 386 0 0 1 725 212"/>'
    '<path class="arc a5 outer" style="--i:5" pathLength="1" d="M775 402 A383 383 0 0 1 390 782"/>'
    '</g><g fill="currentColor">'
    '<circle class="dot bd" style="--i:0;transform-origin:447px 93px" cx="447" cy="93" r="20"/>'
    '<circle class="dot bd" style="--i:1;transform-origin:350px 150px" cx="350" cy="150" r="20"/>'
    '<circle class="dot bd" style="--i:2;transform-origin:465px 230px" cx="465" cy="230" r="20"/>'
    '<circle class="dot bd" style="--i:3;transform-origin:322px 248px" cx="322" cy="248" r="20"/>'
    '<circle class="dot bd" style="--i:4;transform-origin:485px 325px" cx="485" cy="325" r="20"/>'
    '<circle class="dot bd" style="--i:5;transform-origin:318px 378px" cx="318" cy="378" r="20"/>'
    '<circle class="dot ad inner" style="--i:0;transform-origin:225px 248px" cx="225" cy="248" r="20"/>'
    '<circle class="dot ad inner" style="--i:1;transform-origin:555px 245px" cx="555" cy="245" r="20"/>'
    '<circle class="dot ad mid" style="--i:2;transform-origin:210px 160px" cx="210" cy="160" r="20"/>'
    '<circle class="dot ad mid" style="--i:3;transform-origin:112px 525px" cx="112" cy="525" r="20"/>'
    '<circle class="dot ad mid" style="--i:4;transform-origin:603px 183px" cx="603" cy="183" r="20"/>'
    '<circle class="dot ad mid" style="--i:5;transform-origin:390px 708px" cx="390" cy="708" r="20"/>'
    '<circle class="dot ad outer" style="--i:6;transform-origin:392px 18px" cx="392" cy="18" r="20"/>'
    '<circle class="dot ad outer" style="--i:7;transform-origin:185px 728px" cx="185" cy="728" r="20"/>'
    '<circle class="dot ad outer" style="--i:8;transform-origin:535px 45px" cx="535" cy="45" r="20"/>'
    '<circle class="dot ad outer" style="--i:9;transform-origin:725px 212px" cx="725" cy="212" r="20"/>'
    '<circle class="dot ad outer" style="--i:10;transform-origin:775px 402px" cx="775" cy="402" r="20"/>'
    '<circle class="dot ad outer" style="--i:11;transform-origin:390px 782px" cx="390" cy="782" r="20"/>'
    '</g></svg>'
)
GSAP_SRC = 'https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js'
SCROLL_SRC = 'https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/ScrollTrigger.min.js'


def logo_scroll_css(prefix=''):
    """Slogan T1 overrides. Load after home.css."""
    return f'<link rel="stylesheet" href="{prefix}assets/css/slogan-options.css">'


def counter_options_css(prefix=''):
    """M2 water counter. Load after home.css."""
    return f'<link rel="stylesheet" href="{prefix}logo-scroll/counter-options.css">'


def counter_options_script(prefix=''):
    """Replaces home-impact.js. The formula lives in the script; the card only sets data-counter."""
    return f'<script src="{prefix}logo-scroll/counter-options.js" defer></script>\n'


def logo_scroll_scripts(prefix='', existing=''):
    """GSAP 3.12.5 + ScrollTrigger + logo-scroll.js + slogan-options.js.
    Skip GSAP when the page already loads it. Never emit a second GSAP tag."""
    tags = []
    low = existing.lower()
    if 'gsap.min.js' not in low and 'gsap@' not in low:
        tags.append(f'<script src="{GSAP_SRC}" defer></script>')
    if 'scrolltrigger' not in low:
        tags.append(f'<script src="{SCROLL_SRC}" defer></script>')
    if 'logo-scroll.js' not in existing:
        tags.append(f'<script src="{prefix}assets/js/logo-scroll.js" defer></script>')
    if 'slogan-options.js' not in existing:
        tags.append(f'<script src="{prefix}assets/js/slogan-options.js" defer></script>')
    return ('\n'.join(tags) + '\n') if tags else ''


def impact_section():
    lines = ''.join(f'<span class="slogan-line" style="--i:{i}">{esc(t)}</span>' for i, t in enumerate(SLOGAN))
    return f'''  <section class="section deep impact" id="impact">
    <div class="wrap impact-inner">
      <div class="impact-slogan reveal">
        {IMPACT_MARK}
        <p class="slogan" aria-label="{esc(' '.join(SLOGAN))}">{lines}</p>
      </div>
      <div class="impact-counter reveal" data-impact-counter data-counter="m2">
        {section_mark('', 'impact', 'sec-mark--lg')}
        <p class="eyebrow">اثر آبادیس، همین حالا</p>
        <strong class="impact-num" aria-live="off">۰</strong>
        <span class="impact-unit">لیتر آب صرفه‌جویی‌شده از ابتدای سال ۱۴۰۵ (تخمینی)</span>
      </div>
    </div>
  </section>'''


def why_v2():
    checks = ''.join(f'<li>{esc(c)}</li>' for c in WHY_CHECKS)
    vals = ''.join(f'<div class="card value reveal"><h3>{esc(t)}</h3><p>{esc(d)}</p></div>' for t, d in LIVE_VALUES)
    return f'''  <section class="section section--alt" id="why">
    <div class="wrap">
      <div class="section-head reveal has-mark">{section_mark('', 'why')}<div><p class="eyebrow">چرا آبادیس؟</p><h2>ارزش افزوده‌های کیسه ساکشن یکبار مصرف</h2></div></div>
      <div class="grid g-4 values">{vals}</div>
      <div class="split" style="margin-top:28px">
        <div class="reveal"><p>{esc(FACTORY_LEAD)}</p></div>
        <ul class="checks reveal">{checks}</ul>
      </div>
    </div>
  </section>'''


def products_v2():
    import pages_products
    from lib import best_img
    cards = []
    for slug, path, title, im, fb in pages_products.FAMILIES:
        r = best_img(im, 480) if im else None
        src = r['src'] if r else fb
        ph = f'<div class="ph"><img src="{src}" alt="{esc(title)} آبادیس" loading="lazy" decoding="async"></div>' if src else '<div class="ph txt">آبادیس</div>'
        cards.append(f'<a class="mini-card reveal" href="products/{slug}/">{ph}<strong>{esc(title)}</strong></a>')
    return f'''  <section class="section" id="products">
    <div class="wrap">
      <div class="section-head reveal"><p class="eyebrow">محصولات</p><h2>محصولات آبادیس</h2>
        <p><a class="more-link" style="margin:0" href="products/">همهٔ محصولات ←</a></p></div>
      <div class="mini-grid">{''.join(cards)}</div>
    </div>
  </section>'''


def quick_links():
    return f'''  <section class="section quick" id="quick" style="padding-block:28px">
    <div class="wrap quick-row">
      <a class="quick-btn" href="calculator/">{section_mark('', 'calculator', 'sec-mark--sm')}محاسبه‌گر صرفه‌جویی</a>
      <a class="quick-btn" href="csr/">{section_mark('', 'zagros', 'sec-mark--sm')}نجات زاگرس</a>
    </div>
  </section>'''


def posts_v2(cat):
    pages_posts.prepare()
    items = [x for x in pages_posts.POSTS if x['cat'] == cat][:3]
    cards = ''.join(pages_posts.card('', x, from_list=False) for x in items)
    label = 'آخرین اخبار آبادیس' if cat == 'news' else 'مقالات آبادیس'
    more = 'news/' if cat == 'news' else 'articles/'
    alt = ' section--alt' if cat == 'articles' else ''
    return f'''  <section class="section{alt}" id="{cat}">
    <div class="wrap">
      <div class="section-head reveal"><p class="eyebrow">{'اخبار' if cat == 'news' else 'مقالات'}</p><h2>{label}</h2>
        <p><a class="more-link" style="margin:0" href="{more}">مشاهده همه ←</a></p></div>
      <div class="post-grid">{cards}</div>
    </div>
  </section>'''


def memberships_section():
    import pathlib
    from lib import SITE
    logos = ''.join(f'<li><img src="{_live(n)}" alt="عضویت آبادیس" loading="lazy" decoding="async"></li>'
                    for n in MEMBERSHIPS if (SITE / _live(n)).exists())
    return f'''  <section class="section" id="memberships">
    <div class="wrap">
      <div class="section-head reveal"><p class="eyebrow">عضویت‌ها</p><h2>عضویت ها</h2></div>
      <ul class="member-logos reveal">{logos}</ul>
    </div>
  </section>'''


def build(write):
    pages_posts.prepare()
    # Alireza review order (Oct 2026): hero → about (+video slot) → impact (slogan + live counter) → why →
    # products → small calculator / Zagros buttons → news → articles → memberships → customers (UNDECIDED, kept)
    main = '\n'.join([
        hero_v2(),
        about_v2(),
        impact_section(),
        why_v2(),
        products_v2(),
        quick_links(),
        posts_v2('news'),
        posts_v2('articles'),
        memberships_section(),
        customers_section(),
    ])
    extra_head = '''<link rel="preload" as="image" href="assets/img/p/hero-bags.webp" type="image/webp">
<link rel="stylesheet" href="assets/css/home.css">
''' + logo_scroll_css('') + '\n' + counter_options_css('')
    scripts = logo_scroll_scripts('') + counter_options_script('')
    html = page(
        '', None, HOME_TITLE, HOME_DESC, main,
        fa_path='', canonical_path='',
        extra_head=extra_head, scripts=scripts,
        main_class='home-page', body_class='home', lightbox=True,
        html_attrs='data-slogan="t1"',
    )
    write('index.html', html)
