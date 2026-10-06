"""Shared <head>, header, footer and hero markup for all redesign pages."""
from lib import esc
from lib import SITE_ORIGIN
from i18n import LANGS, NAV as I18N_NAV, SECONDARY as I18N_SECONDARY, switcher_html, hreflang_tags

# Back-compat aliases (FA)
NAV = I18N_NAV['fa']
SECONDARY = I18N_SECONDARY['fa']

THEME_ICON = '''<svg class="tt-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false">
      <mask id="tt-mask"><rect width="24" height="24" fill="#fff"/><circle class="tt-bite" cx="16.6" cy="7.4" r="6.3" fill="#000"/></mask>
      <g class="tt-rays" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 1.6v2.2M12 20.2v2.2M1.6 12h2.2M20.2 12h2.2M4.6 4.6l1.6 1.6M17.8 17.8l1.6 1.6M4.6 19.4l1.6-1.6M17.8 6.2l1.6-1.6"/></g>
      <circle class="tt-body" cx="12" cy="12" r="8" fill="currentColor" mask="url(#tt-mask)"/>
      <g class="tt-stars" fill="currentColor"><path d="M18.3 6.1l.6 1.6 1.6.6-1.6.6-.6 1.6-.6-1.6-1.6-.6 1.6-.6z"/><path d="M21.4 1.9l.4 1 1 .4-1 .4-.4 1-.4-1-1-.4 1-.4z"/></g>
    </svg>'''
CUR = ' aria-current="page"'


def head(p, title, desc, og=None, lang='fa', fa_path='', canonical_path=None):
    L = LANGS[lang]
    brand = L['brand']
    # Avoid double brand suffix
    full = title if title.rstrip().endswith(brand) else f'{title} — {brand}'
    t = esc(full); d = esc(desc or '')
    ogi = og or f'{p}assets/img/og-image.jpg'
    can_rel = canonical_path if canonical_path is not None else (LANGS[lang]['root'] + (fa_path if lang == 'fa' else ''))
    if lang != 'fa' and canonical_path is None:
        can_rel = None  # caller should pass canonical_path for en/ar
    can_tag = ''
    if canonical_path is not None:
        can_tag = f'<link rel="canonical" href="{SITE_ORIGIN.rstrip("/")}/{canonical_path.lstrip("/")}">\n'
    alts = hreflang_tags(fa_path, p)
    alts_block = (alts + '\n') if alts else ''
    return f'''<!DOCTYPE html>
<html lang="{L['lang']}" dir="{L['dir']}" data-theme="light">
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
{can_tag}{alts_block}<meta property="og:locale" content="{L['og_locale']}"><meta property="og:site_name" content="{esc(brand)}">
<meta property="og:title" content="{t}"><meta property="og:description" content="{d}">
<meta property="og:image" content="{ogi}">
<link rel="preload" href="{p}assets/fonts/kalameh/KalamehWeb-FaNum-Regular.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{p}assets/fonts/kalameh/KalamehWeb-FaNum-Black.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{p}assets/css/site.css">
</head>
<body>
<a class="skip" href="#main">{esc(L['skip'])}</a>
'''


def header(p, cur, lang='fa', fa_path=''):
    L = LANGS[lang]
    root = L['root']
    nav = I18N_NAV[lang]
    links = ''.join(f'<a href="{p}{root}{h}"{CUR if k == cur else ""}>{l}</a>' for k, h, l in nav)
    home = (p or './') if lang == 'fa' else (p + root)
    sw = switcher_html(lang, fa_path, p)
    return f'''<header class="header" id="header">
  <a class="logo" href="{home}" aria-label="{esc(L['brand'])} — {esc(L['home_label'])}">
    <img class="lg-light" src="{p}assets/img/abadis-logo-teal.png" width="658" height="309" alt="{esc(L['brand'])}">
    <img class="lg-dark" src="{p}assets/img/abadis-logo-on-teal.png" width="670" height="309" alt="" aria-hidden="true">
  </a>
  <nav class="nav" id="mainNav" aria-label="{esc(L['nav_aria'])}">{links}</nav>
  <button class="menu-btn" type="button" aria-expanded="false" aria-controls="mainNav" aria-label="{esc(L['menu_aria'])}"><span class="mb-bars" aria-hidden="true"><i></i><i></i><i></i></span></button>
  {sw}
  <button class="theme-toggle" type="button" aria-label="{esc(L['theme_aria'])}" title="{esc(L['theme_title'])}">
    {THEME_ICON}
  </button>
</header>'''


def footer(p, cur=None, lang='fa'):
    L = LANGS[lang]
    root = L['root']
    nav = I18N_NAV[lang]
    sec = I18N_SECONDARY[lang]
    main = '\n        '.join(f'<a href="{p}{root}{h}">{l}</a>' for _, h, l in nav)
    secl = '\n        '.join(f'<a href="{p}{root}{h}"{CUR if k == cur else ""}>{l}</a>' for k, h, l in sec)
    return f'''<footer class="site-footer">
  <div class="wrap foot-inner">
    <div>
      <img src="{p}assets/img/abadis-logo-on-teal.png" width="670" height="309" alt="{esc(L['brand'])}" loading="lazy">
      <p>{esc(L['footer_blurb'])}</p>
      <div class="foot-links">
        {main}
      </div>
    </div>
    <div>
      <h3>{esc(L['footer_more'])}</h3>
      <div class="foot-links">
        {secl}
      </div>
    </div>
    <div>
      <h3>{esc(L['footer_contact'])}</h3>
      <dl>
        <dt>{esc(L['contact_center'])}</dt><dd><a href="tel:+982192001017" dir="ltr">02192001017</a></dd>
        <dt>{esc(L['email'])}</dt><dd><a href="mailto:info@abadis-med.com">info@abadis-med.com</a></dd>
        <dt>{esc(L['whatsapp'])}</dt><dd><a href="https://wa.me/989100145809" target="_blank" rel="noopener" dir="ltr">+989100145809</a></dd>
      </dl>
    </div>
    <div>
      <h3>{esc(L['footer_address'])}</h3>
      <p><b>{esc(L['addr_hq'])}</b><br>{esc(L['addr_hq_val'])}</p>
      <p><b>{esc(L['addr_factory'])}</b><br>{esc(L['addr_factory_val'])}</p>
      <div class="foot-certs"><img src="{p}assets/img/certs/abd-certs-768x119-1-copy.webp" width="768" height="119" alt="CE · ISO 13485:2016 · IMED" loading="lazy"></div>
    </div>
  </div>
  <div class="wrap foot-copy">{esc(L['footer_copy'])}</div>
</footer>'''


def lightbox_html(lang='fa'):
    L = LANGS[lang]
    return f'''<div class="lb" id="lightbox" role="dialog" aria-modal="true" aria-label="{esc(L['lb_aria'])}" hidden>
  <span class="lb-count"></span>
  <button class="lb-close" type="button" aria-label="{esc(L['lb_close'])}">×</button>
  <button class="lb-prev" type="button" aria-label="{esc(L['lb_prev'])}">›</button>
  <figure><img alt=""><figcaption></figcaption></figure>
  <button class="lb-next" type="button" aria-label="{esc(L['lb_next'])}">‹</button>
</div>'''


LIGHTBOX = lightbox_html('fa')


def page(p, cur, title, desc, main, og=None, lightbox=False, scripts='', lang='fa', fa_path='', canonical_path=None):
    if lang == 'fa' and not fa_path and cur:
        guess = {
            'about': 'about/', 'products': 'products/', 'news': 'news/', 'articles': 'articles/',
            'dealers': 'dealers/', 'csr': 'csr/', 'contact': 'contact/', 'calculator': 'calculator/',
            'customers': 'customers/', 'experiences': 'experiences/', 'downloads': 'downloads/',
            'install': 'install-guide/', 'faq': 'faq/', 'careers': 'careers/',
        }.get(cur, '')
        fa_path = fa_path or guess
    if lang == 'fa' and canonical_path is None:
        canonical_path = fa_path
    lb = (lightbox_html(lang) + '\n') if lightbox else ''
    return (head(p, title, desc, og, lang=lang, fa_path=fa_path, canonical_path=canonical_path)
            + header(p, cur, lang=lang, fa_path=fa_path) + '\n<main id="main">\n' + main + '\n</main>\n'
            + lb + footer(p, cur, lang=lang)
            + f'\n<script src="{p}assets/js/site.js" defer></script>\n{scripts}</body>\n</html>\n')


def crumbs(p, trail, lang='fa'):
    L = LANGS[lang]
    home = p + LANGS[lang]['root'] if lang != 'fa' else (p or './')
    if lang == 'fa':
        home = p or './'
    parts = [f'<a href="{home}">{esc(L["home_label"])}</a>']
    for label, h in trail:
        parts.append(f'<a href="{h}">{esc(label)}</a>' if h else esc(label))
    sep = ' › ' if LANGS[lang]['dir'] == 'ltr' else ' ‹ '
    # keep › for both; CSS can mirror
    return '<p class="crumbs">' + ' › '.join(parts) + '</p>'


def mosaic_hero(p, trail, chip, h1, lead='', label=None, lang='fa'):
    return f'''  <section class="hero hero--short" aria-label="{esc(label or chip)}">
    <div class="mosaic" data-tile="12" style="background-image:url('{p}assets/media/or-poster.jpg')" aria-hidden="true">
      <video muted loop playsinline autoplay preload="auto" poster="{p}assets/media/or-poster.jpg" disablepictureinpicture disableremoteplayback tabindex="-1">
        <source src="{p}assets/media/or-mosaic.mp4" type="video/mp4">
      </video>
    </div>
    <div class="hero-inner">
      {crumbs(p, trail, lang=lang)}
      <span class="chip">{esc(chip)}</span>
      <h1>{h1}</h1>
      {f'<p class="lead">{lead}</p>' if lead else ''}
    </div>
  </section>'''


def page_hero(p, trail, h1, lead='', meta='', lang='fa'):
    return f'''  <section class="page-hero">
    <div class="wrap">
      {crumbs(p, trail, lang=lang)}
      <h1>{h1}</h1>
      {f'<p class="lead">{lead}</p>' if lead else ''}
      {meta}
    </div>
  </section>'''
