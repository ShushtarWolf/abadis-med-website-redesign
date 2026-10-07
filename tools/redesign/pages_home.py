"""Generate site/index.html — Zagros hero + about / why / calculator / news / articles / customers."""
from lib import PAGES, esc, fa
from layout import page
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
HOME_TITLE = 'کیسه ساکشن یکبار مصرف — مخازن طبی آبادیس'
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
      <div class="zh-marks" id="zhMarks" aria-hidden="true"></div>
      <div class="zh-dusk" aria-hidden="true"></div>
      <div class="zh-veil" aria-hidden="true"></div>
      <div class="zh-exit" id="zhExit" aria-hidden="true"></div>
      <section class="csr-hero home-zagros-hero" aria-label="نجات زاگرس">
        <div>
          <span class="chip">پویش نجات زاگرس · کاشت نهال بلوط</span>
          <h1>نجات زاگرس،‌مسئولیت اجتماعی آبادیس</h1>
          <p class="lead">{esc(ZAGROS_LEAD)}</p>
          <div class="hero-actions" style="justify-content:center">
            <a class="btn btn-primary" href="csr/">ادامه در توسعه پایدار</a>
          </div>
        </div>
      </section>
      <div class="zh-hint" id="zhHint" aria-hidden="true"><i></i></div>
    </div>
  </div>'''


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
      <div class="media-frame reveal"><div class="mosaic" data-tile="10" style="background-image:url('assets/media/or-poster.jpg')" aria-hidden="true">
      <video muted loop playsinline autoplay preload="auto" poster="assets/media/or-poster.jpg" disablepictureinpicture disableremoteplayback tabindex="-1">
        <source src="assets/media/or-mosaic.mp4" type="video/mp4">
      </video>
    </div></div>
    </div>
    <div class="wrap" style="margin-top:28px">
      <div class="grid g-3">
        <div class="card stat reveal"><strong>+۶۰۰</strong><span>همراه با بیش از ۶۰۰ مرکز درمانی در سطح کشور</span></div>
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
            out.append(
                f'<a class="card teaser reveal" href="{esc(x["rel"])}">'
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
        <p><a class="more-link" style="margin:0" href="customers/">همهٔ مشتریان ←</a></p></div>
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


def build(write):
    pages_posts.prepare()
    main = '\n'.join([
        zagros_hero('csr/img/hero'),
        about_section(),
        why_section(),
        calculator_section(),
        news_section(),
        articles_section(),
        customers_section(),
    ])
    extra_head = '''<link rel="preload" as="image" href="csr/img/hero/bg-dry.webp" type="image/webp">
<link rel="stylesheet" href="csr/zagros-hero.css">
<link rel="stylesheet" href="assets/css/home.css">'''
    scripts = '<script src="csr/zagros-hero.js" defer></script>\n'
    html = page(
        '', None, HOME_TITLE, HOME_DESC, main,
        fa_path='', canonical_path='',
        extra_head=extra_head, scripts=scripts,
        main_class='home-page', body_class='home',
    )
    write('index.html', html)
