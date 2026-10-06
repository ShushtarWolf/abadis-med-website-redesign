"""Shared <head>, header, footer and hero markup for all redesign pages."""
from lib import esc

NAV = [  # main menu: unchanged from phase 1 (RTL order)
    ('about', 'about/', 'آشنایی با ما'),
    ('products', 'products/', 'محصولات'),
    ('news', 'news/', 'آخرین اخبار'),
    ('dealers', 'dealers/', 'لیست نمایندگان'),
    ('csr', 'csr/', 'توسعه پایدار'),
    ('articles', 'articles/', 'مقالات'),
    ('contact', 'contact/', 'ارتباط با ما'),
    ('calculator', 'calculator/', 'محاسبه‌گر'),
]
SECONDARY = [  # footer-only pages
    ('customers', 'customers/', 'مشتریان ما'),
    ('experiences', 'experiences/', 'تجارب ما'),
    ('downloads', 'downloads/', 'مرکز دانلود'),
    ('install', 'install-guide/', 'راهنمای نصب'),
    ('faq', 'faq/', 'پرسش های متداول'),
    ('careers', 'careers/', 'فرصت های همکاری'),
    ('zagros', 'csr/', 'نجات زاگرس'),
]
THEME_ICON = '''<svg class="tt-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false">
      <mask id="tt-mask"><rect width="24" height="24" fill="#fff"/><circle class="tt-bite" cx="16.6" cy="7.4" r="6.3" fill="#000"/></mask>
      <g class="tt-rays" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 1.6v2.2M12 20.2v2.2M1.6 12h2.2M20.2 12h2.2M4.6 4.6l1.6 1.6M17.8 17.8l1.6 1.6M4.6 19.4l1.6-1.6M17.8 6.2l1.6-1.6"/></g>
      <circle class="tt-body" cx="12" cy="12" r="8" fill="currentColor" mask="url(#tt-mask)"/>
      <g class="tt-stars" fill="currentColor"><path d="M18.3 6.1l.6 1.6 1.6.6-1.6.6-.6 1.6-.6-1.6-1.6-.6 1.6-.6z"/><path d="M21.4 1.9l.4 1 1 .4-1 .4-.4 1-.4-1-1-.4 1-.4z"/></g>
    </svg>'''
CUR = ' aria-current="page"'

def head(p, title, desc, og=None):
    t = esc(title + ' — مخازن طبی آبادیس'); d = esc(desc or '')
    ogi = og or f'{p}assets/img/og-image.jpg'
    return f'''<!DOCTYPE html>
<html lang="fa" dir="rtl" data-theme="light">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t}</title>
<meta name="description" content="{d}">
<meta name="robots" content="noindex,nofollow">
<meta name="theme-color" content="#e8f3f3">
<script>(function(){{var t;try{{var q=new URLSearchParams(location.search).get('theme');if(q){{localStorage.setItem('abadis-theme',q)}}t=localStorage.getItem('abadis-theme')}}catch(e){{}}var d=document.documentElement;d.dataset.theme=(t==='dark'||t==='noir')?t:'light';d.classList.add('js')}})();</script>
<link rel="icon" href="{p}favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="{p}assets/img/favicon-32.png">
<link rel="apple-touch-icon" href="{p}assets/img/apple-touch-icon.png">
<meta property="og:locale" content="fa_IR"><meta property="og:site_name" content="مخازن طبی آبادیس">
<meta property="og:title" content="{t}"><meta property="og:description" content="{d}">
<meta property="og:image" content="{ogi}">
<link rel="preload" href="{p}assets/fonts/kalameh/KalamehWeb-FaNum-Regular.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{p}assets/fonts/kalameh/KalamehWeb-FaNum-Black.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{p}assets/css/site.css">
</head>
<body>
<a class="skip" href="#main">پرش به محتوا</a>
'''

def header(p, cur):
    links = ''.join(f'<a href="{p}{h}"{CUR if k == cur else ""}>{l}</a>' for k, h, l in NAV)
    home = p or './'
    return f'''<header class="header" id="header">
  <a class="logo" href="{home}" aria-label="مخازن طبی آبادیس — خانه">
    <img class="lg-light" src="{p}assets/img/abadis-logo-teal.png" width="658" height="309" alt="مخازن طبی آبادیس">
    <img class="lg-dark" src="{p}assets/img/abadis-logo-on-teal.png" width="670" height="309" alt="" aria-hidden="true">
  </a>
  <nav class="nav" id="mainNav" aria-label="منوی اصلی">{links}</nav>
  <button class="menu-btn" type="button" aria-expanded="false" aria-controls="mainNav" aria-label="منو"><span class="mb-bars" aria-hidden="true"><i></i><i></i><i></i></span></button>
  <button class="theme-toggle" type="button" aria-label="حالت نمایش" title="تغییر حالت نمایش">
    {THEME_ICON}
  </button>
</header>'''

def footer(p, cur=None):
    main = '\n        '.join(f'<a href="{p}{h}">{l}</a>' for _, h, l in NAV)
    sec = '\n        '.join(f'<a href="{p}{h}"{CUR if k == cur else ""}>{l}</a>' for k, h, l in SECONDARY)
    return f'''<footer class="site-footer">
  <div class="wrap foot-inner">
    <div>
      <img src="{p}assets/img/abadis-logo-on-teal.png" width="670" height="309" alt="مخازن طبی آبادیس" loading="lazy">
      <p>با ما در ارتباط باشید...</p>
      <div class="foot-links">
        {main}
      </div>
    </div>
    <div>
      <h3>بیشتر</h3>
      <div class="foot-links">
        {sec}
      </div>
    </div>
    <div>
      <h3>تماس</h3>
      <dl>
        <dt>مرکز تماس:</dt><dd><a href="tel:+982192001017" dir="ltr">02192001017</a></dd>
        <dt>پست الکترونیک:</dt><dd><a href="mailto:info@abadis-med.com">info@abadis-med.com</a></dd>
        <dt>واتس‌اپ:</dt><dd><a href="https://wa.me/989100145809" target="_blank" rel="noopener" dir="ltr">+989100145809</a></dd>
      </dl>
    </div>
    <div>
      <h3>نشانی</h3>
      <p><b>نشانی دفتر مرکزی:</b><br>ایران، تهران، قیطریه، خیابان اندرزگو، پلاک 104، واحد2</p>
      <p><b>نشانی کارخانه:</b><br>ایران،تهران،شهرک صنعتی شمس آباد، بلوار گلستان، کوچه گلشن ۱۹،پلاک۱۷</p>
      <div class="foot-certs"><img src="{p}assets/img/certs/abd-certs-768x119-1-copy.webp" width="768" height="119" alt="CE · ISO 13485:2016 · IMED" loading="lazy"></div>
    </div>
  </div>
  <div class="wrap foot-copy">کلیه حقوق مادی و معنوی این وبسایت متعلق است به: مخازن طبی آبادیس · نسخهٔ پیش‌نمایش بازطراحی</div>
</footer>'''

LIGHTBOX = '''<div class="lb" id="lightbox" role="dialog" aria-modal="true" aria-label="گالری تصاویر" hidden>
  <span class="lb-count"></span>
  <button class="lb-close" type="button" aria-label="بستن">×</button>
  <button class="lb-prev" type="button" aria-label="تصویر قبلی">›</button>
  <figure><img alt=""><figcaption></figcaption></figure>
  <button class="lb-next" type="button" aria-label="تصویر بعدی">‹</button>
</div>'''

def page(p, cur, title, desc, main, og=None, lightbox=False, scripts=''):
    return (head(p, title, desc, og) + header(p, cur) + '\n<main id="main">\n' + main + '\n</main>\n'
            + (LIGHTBOX + '\n' if lightbox else '') + footer(p, cur) + f'\n<script src="{p}assets/js/site.js" defer></script>\n{scripts}</body>\n</html>\n')

def crumbs(p, trail):
    """trail: list of (label, href or None)."""
    parts = [f'<a href="{p or "./"}">خانه</a>']
    for label, h in trail:
        parts.append(f'<a href="{h}">{esc(label)}</a>' if h else esc(label))
    return '<p class="crumbs">' + ' › '.join(parts) + '</p>'

def mosaic_hero(p, trail, chip, h1, lead='', label=None):
    return f'''  <section class="hero hero--short" aria-label="{esc(label or chip)}">
    <div class="mosaic" data-tile="12" style="background-image:url('{p}assets/media/or-poster.jpg')" aria-hidden="true">
      <video muted loop playsinline autoplay preload="auto" poster="{p}assets/media/or-poster.jpg" disablepictureinpicture disableremoteplayback tabindex="-1">
        <source src="{p}assets/media/or-mosaic.mp4" type="video/mp4">
      </video>
    </div>
    <div class="hero-inner">
      {crumbs(p, trail)}
      <span class="chip">{esc(chip)}</span>
      <h1>{h1}</h1>
      {f'<p class="lead">{lead}</p>' if lead else ''}
    </div>
  </section>'''

def page_hero(p, trail, h1, lead='', meta=''):
    """Compact deep-teal band (no video) for secondary pages and single posts."""
    return f'''  <section class="page-hero">
    <div class="wrap">
      {crumbs(p, trail)}
      <h1>{h1}</h1>
      {f'<p class="lead">{lead}</p>' if lead else ''}
      {meta}
    </div>
  </section>'''
