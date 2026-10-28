"""Shared <head>, header, footer and hero markup for all redesign pages."""
import urllib.parse
from lib import esc
from lib import SITE_ORIGIN, FORM_ENDPOINT, FORM_MAILTO
from i18n import (
    LANGS, NAV as I18N_NAV, SECONDARY as I18N_SECONDARY, nav_flat, switcher_html,
    hreflang_tags, canonical_href, ROBOTS_META,
)
from icons import (
    svg_phone, svg_mail, svg_whatsapp, svg_instagram, svg_pin,
    svg_telegram, svg_youtube, svg_facebook, svg_twitter, svg_aparat, svg_linkedin,
    svg_threads, svg_medium, svg_virgool,
    WA_URL, IG_URL, TG_URL, YT_URL, FB_URL, TW_URL, AP_URL, LI_URL,
    TH_URL, MD_URL, VG_URL, TEL_URL, MAIL_URL,
)

# HQ pin already used on the FA contact page (and the EN map embed is the same place).
MAPS_HQ = 'https://www.google.com/maps/search/?api=1&query=35.79866,51.44826'
# Only Neshan place linked on the site (FA contact «مسیریابی با نشان»). No separate factory pin.
NESHAN_HQ = 'https://neshan.org/maps/places/9399a4513b6974a287127c06bd9269b9'

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


def head(p, title, desc, og=None, lang='fa', fa_path='', canonical_path=None, html_attrs=''):
    L = LANGS[lang]
    brand = L['brand']
    # Avoid double brand suffix
    full = title if title.rstrip().endswith(brand) else f'{title} — {brand}'
    t = esc(full); d = esc(desc or '')
    ogi = og or f'{p}assets/img/og-image.jpg'
    can_tag = ''
    if canonical_path is not None:
        # Final URL on abadis-med.com (not the GitHub Pages host).
        can_tag = f'<link rel="canonical" href="{canonical_href(canonical_path)}">\n'
    alts = hreflang_tags(fa_path, p, canonical_path=canonical_path)
    alts_block = (alts + '\n') if alts else ''
    extra = (' ' + html_attrs.strip()) if html_attrs and html_attrs.strip() else ''
    return f'''<!DOCTYPE html>
<html lang="{L['lang']}" dir="{L['dir']}" data-theme="light"{extra}>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t}</title>
<meta name="description" content="{d}">
{ROBOTS_META}
<meta name="theme-color" content="#e8f3f3">
<meta name="abadis-form-endpoint" content="{esc(FORM_ENDPOINT)}">
<meta name="abadis-form-mailto" content="{esc(FORM_MAILTO)}">
<script>(function(){{var t;try{{var q=new URLSearchParams(location.search).get('theme');if(q){{localStorage.setItem('abadis-theme',q)}}t=localStorage.getItem('abadis-theme')}}catch(e){{}}var d=document.documentElement;d.dataset.theme=(t==='dark'||t==='noir')?t:'light';d.classList.add('js')}})();</script>
<link rel="icon" href="{p}favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="{p}assets/img/favicon-32.png">
<link rel="apple-touch-icon" href="{p}assets/img/apple-touch-icon.png">
{can_tag}{alts_block}<meta property="og:locale" content="{L['og_locale']}"><meta property="og:site_name" content="{esc(brand)}">
<meta property="og:title" content="{t}"><meta property="og:description" content="{d}">
<meta property="og:image" content="{ogi}">
<link rel="preload" href="{p}assets/fonts/kalameh/KalamehWeb-FaNum-Regular.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{p}assets/fonts/kalameh/KalamehWeb-FaNum-Black.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{p}assets/css/site.css?v=20261028n">
<link rel="stylesheet" href="{p}assets/css/boss-order.css?v=20261028n">
<link rel="stylesheet" href="{p}assets/css/consent.css">
<link rel="stylesheet" href="{p}assets/css/footer-motion.css">
</head>
<body>
<a class="skip" href="#main">{esc(L['skip'])}</a>
'''


def _href(p, root, h):
    """Join a nav href. A leading '~' is a path from the site root (not the language root)."""
    if h.startswith('~'):
        return p + h[1:]
    return p + root + h


def _nav_item(p, root, cur, item):
    k, h, l = item[0], item[1], item[2]
    kids = item[3] if len(item) > 3 else None
    if not kids:
        return f'<a href="{_href(p, root, h)}"{CUR if k == cur else ""}>{l}</a>'
    child_keys = {row[0] for row in kids}
    open_cur = CUR if (k == cur or cur in child_keys) else ''
    bits = []
    for row in kids:
        ck, ch, cl = row[0], row[1], row[2]
        badge = row[3] if len(row) > 3 and row[3] else ''
        mark = f'<span class="nav-soon">{badge}</span>' if badge else ''
        bits.append(
            f'<a href="{_href(p, root, ch)}" role="menuitem"{CUR if ck == cur else ""}>{cl}{mark}</a>'
        )
    sub_cls = ' nav-sub--catalog' if k in ('products', 'solutions') else ''
    nav_attr = f' data-ps-nav="{k}"' if k in ('products', 'solutions') else ''
    return (
        f'<div class="nav-item has-sub"{nav_attr}>'
        f'<a class="nav-parent" href="{_href(p, root, h)}"{open_cur} aria-haspopup="true" aria-expanded="false">{l}</a>'
        f'<div class="nav-sub{sub_cls}" role="menu">{"".join(bits)}</div>'
        f'</div>'
    )


def header(p, cur, lang='fa', fa_path=''):
    L = LANGS[lang]
    root = L['root']
    nav = I18N_NAV[lang]
    links = ''.join(_nav_item(p, root, cur, item) for item in nav)
    home = (p or './') if lang == 'fa' else (p + root)
    sw = switcher_html(lang, fa_path, p)
    return f'''<header class="header" id="header">
  <a class="logo" href="{home}" aria-label="{esc(L['brand'])} — {esc(L['home_label'])}">
    <img class="lg-light" src="{p}assets/img/abadis-logo-teal.svg" width="646" height="309" alt="{esc(L['brand'])}">
    <img class="lg-dark" src="{p}assets/img/abadis-logo-white.svg" width="646" height="309" alt="" aria-hidden="true">
  </a>
  <nav class="nav" id="mainNav" aria-label="{esc(L['nav_aria'])}">{links}</nav>
  <button class="menu-btn" type="button" aria-expanded="false" aria-controls="mainNav" aria-label="{esc(L['menu_aria'])}"><span class="mb-bars" aria-hidden="true"><i></i><i></i><i></i></span></button>
  {sw}
  <button class="theme-toggle" type="button" aria-label="{esc(L['theme_aria'])}" title="{esc(L['theme_title'])}">
    {THEME_ICON}
  </button>
</header>'''


def _footer_label(lang, key, label):
    """Link text inside the footer. Header nav is unchanged."""
    if lang == 'fa' and key == 'customers':
        return 'خانواده سبز آبادیس'
    return label


_PILL_VALUE = {
    'tel': '021&nbsp;9200&nbsp;1017',
    'mail': 'info@abadis-med.com',
}


def _foot_icon(kind, href, label, icon, extra='', value=''):
    aria = f'{label} {value}'.strip()
    shown = _PILL_VALUE.get(kind, '')
    val = f'<span class="foot-pill-val">{shown}</span>' if shown else ''
    return (
        f'<a class="foot-pill foot-pill--{kind}" href="{esc(href)}"{extra} '
        f'aria-label="{esc(aria)}">'
        f'<span class="foot-pill-ico" aria-hidden="true">{icon}</span>'
        f'{val}'
        f'<span class="sr-only">{esc(aria)}</span></a>'
    )


def _foot_placeholder(kind, label, icon, note):
    """Non-navigating pill when abadis-med.com publishes no official profile URL."""
    aria = f'{label} — {note}'
    return (
        f'<a class="foot-pill foot-pill--{kind} foot-pill--placeholder" hidden '
        f'data-social="{esc(kind)}" data-status="placeholder" data-official-url="" '
        f'data-note="{esc(note)}" aria-disabled="true" tabindex="-1" '
        f'aria-label="{esc(aria)}">'
        f'<span class="foot-pill-ico" aria-hidden="true">{icon}</span>'
        f'<span class="sr-only">{esc(aria)}</span></a>'
    )


def footer_pills_html(lang):
    """Phone and email, then the 11 official channels from abadis-med.com, one color."""
    L = LANGS[lang]
    lab = lambda key: L[key].rstrip(':')
    ext = ' target="_blank" rel="noopener"'
    return '\n        '.join((
        _foot_icon('tel', TEL_URL, lab('contact_center'), svg_phone(), value='02192001017'),
        _foot_icon('mail', MAIL_URL, lab('email'), svg_mail(), value='info@abadis-med.com'),
        _foot_icon('wa', WA_URL, lab('whatsapp'), svg_whatsapp(), ext, '+989100145809'),
        _foot_icon('ig', IG_URL, lab('instagram'), svg_instagram('foot-ig'), ext, 'abadis.med'),
        _foot_icon('tg', TG_URL, lab('telegram'), svg_telegram(), ext),
        _foot_icon('ap', AP_URL, lab('aparat'), svg_aparat(), ext),
        _foot_icon('yt', YT_URL, lab('youtube'), svg_youtube(), ext),
        _foot_icon('li', LI_URL, lab('linkedin'), svg_linkedin(), ext),
        _foot_icon('tw', TW_URL, lab('twitter'), svg_twitter(), ext),
        _foot_icon('fb', FB_URL, lab('facebook'), svg_facebook(), ext),
        _foot_icon('th', TH_URL, lab('threads'), svg_threads(), ext),
        _foot_icon('md', MD_URL, lab('medium'), svg_medium(), ext),
        _foot_icon('vg', VG_URL, lab('virgool'), svg_virgool(), ext),
    ))


def footer_address_html(lang):
    L = LANGS[lang]
    pin = f'<span class="foot-pin" aria-hidden="true">{svg_pin()}</span>'

    def row(label, val, href=None, cue=''):
        maps = f'<span class="foot-addr-maps">{esc(cue)}</span>' if href and cue else ''
        body = f'{pin}<span><b>{esc(label)}</b><br>{esc(val)}{maps}</span>'
        if not href:
            return f'<p class="foot-addr">{body}</p>'
        aria = esc(f'{label} {val} — {cue}')
        return (
            f'<a class="foot-addr foot-addr-link" href="{esc(href)}" target="_blank" rel="noopener" '
            f'aria-label="{aria}">{body}</a>'
        )

    hq_href = factory_href = None
    cue = ''
    if lang == 'fa':
        hq_href = factory_href = NESHAN_HQ
        cue = 'مسیریابی با نشان'
    elif lang == 'en':
        hq_href = MAPS_HQ
        factory_href = 'https://www.google.com/maps/search/?api=1&query=' + urllib.parse.quote(
            L['addr_factory_val'], safe='')
        cue = 'Google Maps'
    return row(L['addr_hq'], L['addr_hq_val'], hq_href, cue) + '\n      ' + row(
        L['addr_factory'], L['addr_factory_val'], factory_href, cue)


def footer(p, cur=None, lang='fa'):
    L = LANGS[lang]
    root = L['root']
    nav = nav_flat(I18N_NAV[lang], footer=True)
    sec = I18N_SECONDARY[lang]
    # Text only. SDGs, calculator, and CSR (نجات زاگرس) do not get section icons.
    main = '\n        '.join(
        f'<a href="{_href(p, root, h)}">{_footer_label(lang, k, l)}</a>' for k, h, l in nav)
    secl = '\n        '.join(
        f'<a href="{_href(p, root, h)}"{CUR if k == cur else ""}>{_footer_label(lang, k, l)}</a>'
        for k, h, l in sec)
    return f'''<footer class="site-footer">
  <div class="wrap foot-inner">
    <div class="foot-col foot-col-brand">
      <div class="foot-brand">
        <img src="{p}assets/img/abadis-logo-white.svg" width="646" height="309" alt="{esc(L['brand'])}" loading="lazy">
        <p>{esc(L['footer_blurb'])}</p>
      </div>
      <details class="foot-acc foot-nav" open>
        <summary>{esc(L['footer_menu'])}</summary>
        <div class="foot-links">
          {main}
        </div>
      </details>
    </div>
    <details class="foot-acc foot-more" open>
      <summary>{esc(L['footer_more'])}</summary>
      <div class="foot-links">
        {secl}
      </div>
    </details>
    <div class="foot-contact">
      <h3>{esc(L['footer_contact'])}</h3>
      <div class="foot-contact-pills">
        {footer_pills_html(lang)}
      </div>
    </div>
    <details class="foot-acc foot-address" open>
      <summary>{esc(L['footer_address'])}</summary>
      {footer_address_html(lang)}
    </details>
  </div>
  <div class="wrap foot-certs-bar">
    <div class="foot-certs"><img src="{p}assets/img/certs/abd-certs-768x119-1-copy.webp" width="768" height="119" alt="CE · ISO 13485:2016 · IMED" loading="lazy"></div>
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


def page(p, cur, title, desc, main, og=None, lightbox=False, scripts='', lang='fa', fa_path='',
         canonical_path=None, extra_head='', main_class='', body_class='', html_attrs=''):
    if lang == 'fa' and not fa_path and cur:
        guess = {
            'about': 'about/', 'products': 'products/', 'news': 'news/', 'articles': 'articles/',
            'dealers': 'dealers/', 'csr': 'csr/', 'sdgs': 'sdgs/', 'contact': 'contact/',
            'calculator': 'calculator/', 'customers': 'customers/', 'experiences': 'academy/',
            'downloads': 'downloads/', 'install': 'install-guide/', 'faq': 'faq/',
            'careers': 'careers/', 'jobs': 'jobs/',
        }.get(cur, '')
        fa_path = fa_path or guess
    if lang == 'fa' and canonical_path is None:
        canonical_path = fa_path
    lb = (lightbox_html(lang) + '\n') if lightbox else ''
    html = head(p, title, desc, og, lang=lang, fa_path=fa_path, canonical_path=canonical_path, html_attrs=html_attrs)
    if extra_head:
        html = html.replace('</head>', extra_head.rstrip() + '\n</head>', 1)
    if body_class:
        html = html.replace('<body>', f'<body class="{body_class}">', 1)
    main_attrs = f' class="{main_class}"' if main_class else ''
    return (html
            + header(p, cur, lang=lang, fa_path=fa_path) + f'\n<main id="main"{main_attrs}>\n' + main + '\n</main>\n'
            + lb + footer(p, cur, lang=lang)
            + f'\n<script src="{p}assets/js/site.js?v=20261028j" defer></script>\n<script src="{p}assets/js/consent.js" defer></script>\n<script src="{p}assets/js/footer-motion.js" defer></script>\n{scripts}</body>\n</html>\n')


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
      <video autoplay muted loop playsinline webkit-playsinline disablepictureinpicture disableremoteplayback preload="metadata" tabindex="-1" aria-hidden="true" poster="{p}assets/media/or-poster.jpg">
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


def section_mark(p, key, extra=''):
    """Approved section icon, light and dark. Impact is the original sign, unmodified."""
    slug = {
        'why': 'why',
        'calculator': 'calculator',
        'sustainable': 'sustainable',
        'sdgs': 'sustainable',
        'zagros': 'zagros',
        'csr': 'zagros',
        'impact': 'impact',
    }[key]
    base = f'{p}brand/section-logos/{slug}'
    cls = 'sec-mark' + (f' {extra}' if extra else '')
    return (
        f'<span class="{cls}" aria-hidden="true">'
        f'<img class="sec-mark-light" src="{base}-icon.svg" alt="" width="120" height="120" decoding="async">'
        f'<img class="sec-mark-dark" src="{base}-icon-dark.svg" alt="" width="120" height="120" decoding="async">'
        f'</span>'
    )


def page_hero(p, trail, h1, lead='', meta='', lang='fa', mark=None):
    inner = f'''{crumbs(p, trail, lang=lang)}
      <h1>{h1}</h1>
      {f'<p class="lead">{lead}</p>' if lead else ''}
      {meta}'''
    if not mark:
        return f'''  <section class="page-hero">
    <div class="wrap">
      {inner}
    </div>
  </section>'''
    return f'''  <section class="page-hero">
    <div class="wrap page-hero-with-mark">
      <div class="page-hero-copy">
      {inner}
      </div>
      {section_mark(p, mark, 'sec-mark--lg')}
    </div>
  </section>'''
