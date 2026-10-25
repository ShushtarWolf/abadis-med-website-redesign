"""Official contact and social icons for the footer and Contact Us pages.

WhatsApp and Instagram use their original brand marks (green speech-bubble,
camera glyph with the Instagram gradient). Tone icons use currentColor so the
footer and the contact page can tint them.
"""
from __future__ import annotations
import re

_IG_PATH = (
    'M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919'
    '.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225'
    '-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012'
    '-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849'
    ' 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057'
    ' 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69'
    '.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618'
    ' 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072'
    ' 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014'
    '-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0z'
    'm0 5.838a6.162 6.162 0 1 0 0 12.324 6.162 6.162 0 0 0 0-12.324zM12 16a4 4 0 1 1'
    ' 0-8 4 4 0 0 1 0 8zm6.406-11.845a1.44 1.44 0 1 0 0 2.881 1.44 1.44 0 0 0 0-2.881z'
)

_WA_PATH = (
    'M20.52 3.449C18.24 1.245 15.24 0 12.045 0 5.463 0 .104 5.334.101 11.893c0 2.096.549'
    ' 4.14 1.595 5.945L0 24l6.335-1.652a12.1 12.1 0 0 0 5.71 1.447h.006c6.585 0 11.946-5.336'
    ' 11.949-11.896 0-3.176-1.24-6.165-3.495-8.411zm-8.475 18.299h-.004a10.05 10.05 0 0 1-5.122'
    '-1.399l-.367-.217-3.765.983 1.005-3.648-.239-.374a9.96 9.96 0 0 1-1.539-5.33c.002-5.514'
    ' 4.5-9.993 10.05-9.993 2.684 0 5.207 1.044 7.103 2.939a9.94 9.94 0 0 1 2.94 7.087c-.003'
    ' 5.514-4.5 9.993-10.05 9.993zm5.503-7.48c-.3-.15-1.767-.868-2.04-.967-.274-.099-.473-.148'
    '-.673.15-.197.296-.771.964-.944 1.162-.176.199-.349.223-.647.075-.3-.149-1.263-.465-2.405'
    '-1.483-.888-.79-1.488-1.766-1.662-2.064-.173-.297-.018-.458.13-.606.134-.133.298-.347.446'
    '-.52.149-.174.199-.298.298-.497.1-.198.05-.372-.025-.521-.075-.148-.673-1.62-.922-2.22'
    '-.242-.584-.487-.51-.673-.51-.173-.008-.372-.01-.571-.01-.198 0-.52.074-.792.372-.272.297'
    '-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.095 3.2 5.076 4.487.709'
    '.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248'
    '-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z'
)


def _svg(body: str) -> str:
    return f'<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">{body}</svg>'


def svg_phone() -> str:
    return _svg('<path fill="currentColor" d="M6.62 10.79a15.05 15.05 0 0 0 6.59 6.59l2.2-2.2a1 1 0 0 1 1.02-.24c1.12.37 2.33.57 3.57.57a1 1 0 0 1 1 1V20a1 1 0 0 1-1 1C10.85 21 3 13.15 3 3a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.24.2 2.45.57 3.57a1 1 0 0 1-.25 1.02l-2.2 2.2z"/>')


def svg_mail() -> str:
    return _svg('<path fill="currentColor" d="M20 4H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2zm0 4-8 5L4 8V6l8 5 8-5v2z"/>')


def svg_pin() -> str:
    return _svg('<path fill="currentColor" d="M12 2a7 7 0 0 0-7 7c0 5.25 7 13 7 13s7-7.75 7-13a7 7 0 0 0-7-7zm0 9.5A2.5 2.5 0 1 1 12 6a2.5 2.5 0 0 1 0 5.5z"/>')


def svg_fax() -> str:
    return _svg('<path fill="currentColor" d="M19 8h-1V3H6v5H5a3 3 0 0 0-3 3v6h4v4h12v-4h4v-6a3 3 0 0 0-3-3zM8 5h8v3H8V5zm8 14H8v-4h8v4zm4-4h-2v-2H6v2H4v-4a1 1 0 0 1 1-1h14a1 1 0 0 1 1 1v4z"/>')


def svg_postal() -> str:
    return _svg('<path fill="currentColor" d="M12 2 2 7v10l10 5 10-5V7L12 2zm0 2.2 6.8 3.4L12 11 5.2 7.6 12 4.2zM4 9.1l7 3.4v6.8l-7-3.5V9.1zm9 10.2v-6.8l7-3.4v6.7l-7 3.5z"/>')


def svg_clock() -> str:
    return _svg('<path fill="currentColor" d="M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20a8 8 0 1 1 0-16 8 8 0 0 1 0 16zm.5-13H11v6l5.25 3.15.75-1.23-4.5-2.67V7z"/>')


def svg_calendar() -> str:
    return _svg('<path fill="currentColor" d="M7 2h2v2h6V2h2v2h3a1 1 0 0 1 1 1v15a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a1 1 0 0 1 1-1h3V2zm12 8H5v10h14V10zM5 8h14V6H5v2z"/>')


def svg_whatsapp() -> str:
    """Original WhatsApp speech-bubble + handset, brand green #25D366."""
    return _svg(f'<path fill="#25D366" fill-rule="evenodd" d="{_WA_PATH}"/>')


def svg_instagram(uid: str = 'abadis-ig') -> str:
    """Original Instagram camera glyph. Radial stops plus the linear brand colors.

    uid keeps gradient ids unique when the footer and a contact page both draw the mark.
    """
    radial, linear = f'{uid}-r', f'{uid}-l'
    return _svg(
        '<defs>'
        f'<radialGradient id="{radial}" cx="30%" cy="107%" r="150%">'
        '<stop offset="0" stop-color="#f09433"/>'
        '<stop offset="0.25" stop-color="#e6683c"/>'
        '<stop offset="0.5" stop-color="#dc2743"/>'
        '<stop offset="0.75" stop-color="#cc2366"/>'
        '<stop offset="1" stop-color="#bc1888"/>'
        '</radialGradient>'
        f'<linearGradient id="{linear}" x1="0" y1="24" x2="24" y2="0" gradientUnits="userSpaceOnUse">'
        '<stop offset="0" stop-color="#F58529"/>'
        '<stop offset="0.3" stop-color="#DD2A7B"/>'
        '<stop offset="0.65" stop-color="#8134AF"/>'
        '<stop offset="1" stop-color="#515BD4"/>'
        '</linearGradient>'
        '</defs>'
        f'<path fill="url(#{radial})" fill-rule="evenodd" d="{_IG_PATH}"/>'
        f'<path fill="url(#{linear})" fill-opacity="0.72" fill-rule="evenodd" d="{_IG_PATH}"/>'
    )


def svg_telegram() -> str:
    return _svg('<path fill="#26A5E4" d="M21.8 4.3 18.7 20c-.2 1-.8 1.3-1.7.8l-4.6-3.4-2.2 2.1c-.2.3-.5.5-.9.5l.3-4.7 8.6-7.8c.4-.3-.1-.5-.6-.2L6.5 13.1 2 11.7c-1-.3-1-1 .2-1.5L20.3 3.2c.8-.3 1.6.2 1.5 1.1z"/>')


def svg_youtube() -> str:
    return _svg('<path fill="#FF0000" d="M23.5 6.2a3 3 0 0 0-2.1-2.1C19.5 3.6 12 3.6 12 3.6s-7.5 0-9.4.5A3 3 0 0 0 .5 6.2 31.6 31.6 0 0 0 0 12a31.6 31.6 0 0 0 .5 5.8 3 3 0 0 0 2.1 2.1c1.9.5 9.4.5 9.4.5s7.5 0 9.4-.5a3 3 0 0 0 2.1-2.1A31.6 31.6 0 0 0 24 12a31.6 31.6 0 0 0-.5-5.8z"/><path fill="#fff" d="M9.75 15.02V8.98L15.5 12l-5.75 3.02z"/>')


def svg_facebook() -> str:
    return _svg('<path fill="#0866FF" d="M24 12.07C24 5.4 18.63 0 12 0S0 5.4 0 12.07C0 18.1 4.39 23.09 10.13 24v-8.44H7.08v-3.49h3.05V9.41c0-3.02 1.79-4.7 4.53-4.7 1.31 0 2.68.24 2.68.24v2.96h-1.51c-1.49 0-1.95.93-1.95 1.89v2.27h3.32l-.53 3.49h-2.79V24C19.61 23.09 24 18.1 24 12.07z"/>')


def svg_twitter() -> str:
    return _svg('<path fill="#1D9BF0" d="M22.46 6a8.3 8.3 0 0 1-2.36.65 4.1 4.1 0 0 0 1.8-2.27 8.2 8.2 0 0 1-2.6 1 4.1 4.1 0 0 0-7 3.74A11.65 11.65 0 0 1 3.15 4.6a4.1 4.1 0 0 0 1.27 5.48 4.07 4.07 0 0 1-1.86-.51v.05a4.1 4.1 0 0 0 3.29 4.02 4.1 4.1 0 0 1-1.85.07 4.1 4.1 0 0 0 3.83 2.85A8.23 8.23 0 0 1 2 18.41a11.62 11.62 0 0 0 6.29 1.84c7.55 0 11.68-6.25 11.68-11.67v-.53A8.18 8.18 0 0 0 22.46 6z"/>')


def svg_aparat() -> str:
    return _svg('<rect width="24" height="24" rx="6" fill="#ED145B"/><path fill="#fff" d="M9.6 7.8v8.4l6.8-4.2-6.8-4.2z"/>')


def svg_linkedin() -> str:
    """Official LinkedIn “in” mark, brand blue #0A66C2."""
    return _svg('<path fill="#0A66C2" d="M20.45 20.45h-3.56v-5.57c0-1.33-.02-3.04-1.85-3.04-1.85 0-2.13 1.45-2.13 2.94v5.67H9.35V9h3.41v1.56h.05c.47-.9 1.63-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.45v6.29zM5.34 7.43a2.06 2.06 0 1 1 0-4.12 2.06 2.06 0 0 1 0 4.12zM7.12 20.45H3.56V9h3.56v11.45zM22.23 0H1.77C.79 0 0 .77 0 1.73v20.54C0 23.23.79 24 1.77 24h20.46c.98 0 1.77-.77 1.77-1.73V1.73C24 .77 23.21 0 22.23 0z"/>')


def ch(svg: str, sm: bool = False) -> str:
    cls = 'ch-ico ch-ico--sm' if sm else 'ch-ico'
    return f'<span class="{cls}" aria-hidden="true">{svg}</span>'


def brand_buttons(items: list[tuple[str, str, str]]) -> str:
    """items: (href, svg, label)."""
    bits = []
    for href, svg, label in items:
        bits.append(
            f'<a class="brand-btn" href="{href}" target="_blank" rel="noopener">{svg}<span>{label}</span></a>'
        )
    return '<div class="brand-row">' + ''.join(bits) + '</div>'


WA_URL = 'https://wa.me/989100145809'
IG_URL = 'https://www.instagram.com/abadismedical.co'
# Channels already linked on the EN/AR contact pages or the live footer icon row.
TG_URL = 'https://t.me/abadis_med'
YT_URL = 'https://www.youtube.com/channel/UC2J9yTFmf6fHLhKQ6y3gdCw/featured?view_as=subscriber'
FB_URL = 'https://fb.com/AbadisMedCo'
TW_URL = 'https://twitter.com/abadismed'
AP_URL = 'https://www.aparat.com/abadismed'
LI_URL = 'https://www.linkedin.com/company/abadis-medical-co/'
TEL_URL = 'tel:+982192001017'
MAIL_URL = 'mailto:info@abadis-med.com'

_FA_I = re.compile(r'<i\b([^>]*)>\s*</i>', re.I)
_CLASS_ICON = (
    ('fa-telegram', svg_telegram),
    ('fa-whatsapp', svg_whatsapp),
    ('fa-twitter', svg_twitter),
    ('fa-youtube', svg_youtube),
    ('fa-facebook', svg_facebook),
    ('fa-instagram', svg_instagram),
    ('efa-aparat', svg_aparat),
    ('fa-clock', svg_clock),
    ('fa-calendar-times', svg_calendar),
)


def _replace_fa_i(html: str) -> str:
    def repl(m):
        attrs = m.group(1)
        for key, fn in _CLASS_ICON:
            if key in attrs:
                return ch(fn())
        return m.group(0)
    return _FA_I.sub(repl, html)


def _iconize_tel_mail(html: str) -> str:
    def repl(m):
        open_tag, inner, close = m.group(1), m.group(2), m.group(3)
        if 'ch-ico' in inner:
            return m.group(0)
        href_m = re.search(r'href="([^"]*)"', open_tag)
        if not href_m:
            return m.group(0)
        href = href_m.group(1)
        if href.startswith('tel:'):
            icon = svg_phone()
        elif href.startswith('mailto:'):
            icon = svg_mail()
        else:
            return m.group(0)
        return f'{open_tag}{ch(icon, sm=True)}{inner}{close}'
    return re.sub(r'(<a\b[^>]*>)(.*?)(</a>)', repl, html, flags=re.S)


def _swap(html: str, old: str, new: str) -> str:
    if old in html and 'ch-ico' not in old:
        return html.replace(old, new, 1)
    return html


def decorate_contact_html(html: str) -> str:
    """Iconize an EN/AR contact body (WP dump). Idempotent."""
    html = re.sub(
        r'<a\s+target="_blank">(\s*<span>Whatsapp</span>)',
        r'<a href="https://wa.me/989100145809" target="_blank" rel="noopener">\1',
        html,
        count=1,
    )
    html = _replace_fa_i(html)
    if 'class="soc-links"' not in html:
        html = re.sub(
            r'<div>(\s*<span>\s*<a\b[^>]*href="https://t\.me/abadis_med")',
            r'<div class="soc-links">\1',
            html,
            count=1,
        )
    pin, phone, mail, post, clock = svg_pin(), svg_phone(), svg_mail(), svg_postal(), svg_clock()
    swaps = [
        ('<h4><span>Office:</span></h4>', f'<h4 class="with-ico">{ch(pin)}<span>Office:</span></h4>'),
        ('<h4><span>Contact Support Center:</span></h4>', f'<h4 class="with-ico">{ch(phone)}<span>Contact Support Center:</span></h4>'),
        ('<h4><span>Contact Lines:</span></h4>', f'<h4 class="with-ico">{ch(phone)}<span>Contact Lines:</span></h4>'),
        ('<h4><span>Industrial Complex:</span></h4>', f'<h4 class="with-ico">{ch(pin)}<span>Industrial Complex:</span></h4>'),
        ('<h5><span>Internal Numbers:</span></h5>', f'<h5 class="with-ico">{ch(phone)}<span>Internal Numbers:</span></h5>'),
        ('<strong><span>Email:</span></strong>', f'{ch(mail)}<strong><span>Email:</span></strong>'),
        ('<h4><span><strong>Social Networks:</strong></span></h4>', f'<h4 class="with-ico">{ch(svg_instagram())}<span><strong>Social Networks:</strong></span></h4>'),
        ('<h2>Office Hours</h2>', f'<h2 class="with-ico">{ch(clock)}Office Hours</h2>'),
        ('<h2>المكتب المركزي</h2>', f'<h2 class="with-ico">{ch(pin)}المكتب المركزي</h2>'),
        ('<h2>المصنع</h2>', f'<h2 class="with-ico">{ch(pin)}المصنع</h2>'),
        ('<h2>ساعات العمل</h2>', f'<h2 class="with-ico">{ch(clock)}ساعات العمل</h2>'),
        ('<h2>العطل</h2>', f'<h2 class="with-ico">{ch(svg_calendar())}العطل</h2>'),
        ('<strong><span>العنوان:</span></strong>', f'{ch(pin)}<strong><span>العنوان:</span></strong>'),
        ('<strong><span>العنوان :</span></strong>', f'{ch(pin)}<strong><span>العنوان :</span></strong>'),
        ('<strong><span>الهاتف :</span></strong>', f'{ch(phone)}<strong><span>الهاتف :</span></strong>'),
        ('<strong><span>الرقم الداخلي :</span></strong>', f'{ch(phone)}<strong><span>الرقم الداخلي :</span></strong>'),
        ('<strong>ا<span>لرمز البريدي :</span></strong>', f'{ch(post)}<strong>ا<span>لرمز البريدي :</span></strong>'),
        ('<strong>الرمز البريدي : </strong>', f'{ch(post)}<strong>الرمز البريدي : </strong>'),
        ('<strong><span>البريد الإلكتروني :</span></strong>', f'{ch(mail)}<strong><span>البريد الإلكتروني :</span></strong>'),
        ('<strong>شبكات اجتماعية :</strong>', f'{ch(svg_instagram())}<strong>شبكات اجتماعية :</strong>'),
    ]
    for old, new in swaps:
        html = _swap(html, old, new)
    html = _iconize_tel_mail(html)
    return html


def decorate_fa_contact_main(html: str) -> str:
    """Icons on the hand-built FA contact list and the phase-2 block. Idempotent."""
    if 'contact-dl' in html and 'contact-dl' in html and 'dt><span class="ch-ico"' not in html:
        dl = f'''<dl class="contact-dl">
        <dt>{ch(svg_phone())}مرکز تماس:</dt><dd><a href="tel:+982192001017" dir="ltr">02192001017</a></dd>
        <dt>{ch(svg_phone())}تلفن تماس:</dt><dd><a href="tel:+982122671845" dir="ltr">02122671845</a> | <a href="tel:+982122205502" dir="ltr">02122205502</a><br><a href="tel:+982122215503" dir="ltr">02122215503</a> | <a href="tel:+982122218910" dir="ltr">02122218910</a></dd>
        <dt>{ch(svg_fax())}فکس:</dt><dd><span dir="ltr">02141425555</span> | داخلی 28544</dd>
        <dt>{ch(svg_mail())}پست الکترونیک:</dt><dd><a href="mailto:info@abadis-med.com">info@abadis-med.com</a></dd>
        <dt>{ch(svg_whatsapp())}واتس‌اپ:</dt><dd><a href="{WA_URL}" target="_blank" rel="noopener" dir="ltr">+989100145809</a></dd>
        <dt>{ch(svg_instagram())}اینستاگرام:</dt><dd><a href="{IG_URL}" target="_blank" rel="noopener" dir="ltr">abadismedical.co</a></dd>
        <dt>{ch(svg_pin())}دفتر مرکزی:</dt><dd>ایران، تهران، قیطریه، خیابان اندرزگو، پلاک 104، واحد2</dd>
        <dt>{ch(svg_pin())}کارخانه:</dt><dd>ایران،تهران،شهرک صنعتی شمس آباد، بلوار گلستان، کوچه گلشن ۱۹،پلاک۱۷</dd>
      </dl>'''
        html = re.sub(r'<dl class="contact-dl">.*?</dl>', dl, html, count=1, flags=re.S)
    phone, clock, pin, post = svg_phone(), svg_clock(), svg_pin(), svg_postal()
    html = _swap(html, '<h2 style="font-size:1.4rem;margin-bottom:14px">ساعات کاری</h2>',
                 f'<h2 class="with-ico" style="font-size:1.4rem;margin-bottom:14px">{ch(clock)}ساعات کاری</h2>')
    html = _swap(html, '<h2 style="font-size:1.4rem;margin:26px 0 14px">روزهای تعطیل</h2>',
                 f'<h2 class="with-ico" style="font-size:1.4rem;margin:26px 0 14px">{ch(clock)}روزهای تعطیل</h2>')
    html = _swap(html, '<h3>دفتر مرکزی</h3>', f'<h3 class="with-ico">{ch(pin)}دفتر مرکزی</h3>')
    html = _swap(html, '<h3>کارخانه</h3>', f'<h3 class="with-ico">{ch(pin)}کارخانه</h3>')
    html = _swap(html, '<p><strong>داخلی ها:</strong></p>', f'<p class="with-ico">{ch(phone)}<strong>داخلی ها:</strong></p>')
    for lab in ('مدیریت:', 'فروش و پشتیبانی فروش:', 'مالی:'):
        html = _swap(html, f'<p>{lab}', f'<p class="dept-row">{ch(phone, sm=True)}{lab}')
    html = re.sub(
        r'<p><strong>(کدپستی:\s*)</strong>',
        lambda m: f'<p class="with-ico">{ch(post)}<strong>{m.group(1)}</strong>',
        html,
    )
    needle = '<a href="https://yek.link/abadis.med" target="_blank" rel="noopener">https://yek.link/abadis.med</a></p>'
    if 'class="brand-row"' not in html and needle in html:
        row = brand_buttons([
            (WA_URL, svg_whatsapp(), 'واتس‌اپ'),
            (IG_URL, svg_instagram(), 'اینستاگرام'),
        ])
        html = html.replace(needle, needle + row, 1)
    return html


def iconize_extensions(ext_html: str) -> str:
    """Wrap FA phase-2 extension / postal lines. Used by pages_company.contact()."""
    phone, post = svg_phone(), svg_postal()
    ext_html = ext_html.replace(
        '<p><strong>داخلی ها:</strong></p>',
        f'<p class="with-ico">{ch(phone)}<strong>داخلی ها:</strong></p>',
        1,
    )
    for lab in ('مدیریت:', 'فروش و پشتیبانی فروش:', 'مالی:'):
        ext_html = ext_html.replace(f'<p>{lab}', f'<p class="dept-row">{ch(phone, sm=True)}{lab}', 1)
    ext_html = re.sub(
        r'<p><strong>(کدپستی:\s*)</strong>',
        lambda m: f'<p class="with-ico">{ch(post)}<strong>{m.group(1)}</strong>',
        ext_html,
    )
    return ext_html


def _strip_footer_more_sdgs(html: str) -> str:
    """Drop SDG links from the More accordion. About / footer منو keeps the one listing."""
    def repl(block_m):
        return re.sub(
            r'\n[ \t]*<a href="[^"]*sdgs/"[^>]*>[^<]*</a>',
            '',
            block_m.group(0),
        )
    return re.sub(
        r'<details class="foot-acc foot-more"[^>]*>.*?</details>',
        repl,
        html,
        count=1,
        flags=re.S,
    )


def stamp_html(html: str, pills_for, addr_for, kind: str = '') -> tuple[str, list[str]]:
    """Refresh baked footer icons. kind is 'fa-contact', 'en-contact', or 'ar-contact'."""
    notes = []
    html = _strip_footer_more_sdgs(html)
    lang_m = re.search(r'<html[^>]*\blang="([^"]+)"', html)
    lang = 'fa'
    if lang_m:
        raw = lang_m.group(1).lower()
        lang = 'en' if raw.startswith('en') else 'ar' if raw.startswith('ar') else 'fa'
    if '<div class="foot-contact-pills">' in html:
        html2, n = re.subn(
            r'<div class="foot-contact-pills">\s*.*?\s*</div>',
            '<div class="foot-contact-pills">\n        ' + pills_for(lang) + '\n      </div>',
            html,
            count=1,
            flags=re.S,
        )
        if n != 1:
            notes.append('pills-miss')
        else:
            html = html2
    if 'foot-acc foot-address' in html:
        html2, n = re.subn(
            r'(<details class="foot-acc foot-address"[^>]*>\s*<summary>[^<]*</summary>\s*)(?:<(?:p|a)\b[\s\S]*?</(?:p|a)>\s*){1,4}',
            lambda m: m.group(1) + addr_for(lang) + '\n    ',
            html,
            count=1,
        )
        if n != 1:
            notes.append('addr-miss')
        else:
            html = html2

    def _main(fn):
        nonlocal html
        def repl(m):
            return m.group(1) + fn(m.group(2)) + m.group(3)
        html2, n = re.subn(r'(<main id="main">)(.*?)(</main>)', repl, html, count=1, flags=re.S)
        if n == 1:
            html = html2

    if kind == 'fa-contact':
        _main(decorate_fa_contact_main)
    elif kind in ('en-contact', 'ar-contact'):
        _main(decorate_contact_html)
    return html, notes


def stamp_site(root) -> None:
    import pathlib, sys
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    from layout import footer_pills_html, footer_address_html
    root = pathlib.Path(root)
    changed = missed = 0
    for path in root.rglob('*.html'):
        raw = path.read_text(encoding='utf-8')
        if 'site-footer' not in raw and 'contact-dl' not in raw:
            continue
        parts = path.parts
        kind = ''
        if path.name == 'index.html' and 'contact' in parts and 'en' not in parts and 'arabic' not in parts:
            kind = 'fa-contact'
        elif 'contact-us' in parts:
            kind = 'en-contact'
        elif 'اتصل-بنا' in parts:
            kind = 'ar-contact'
        new, notes = stamp_html(raw, footer_pills_html, footer_address_html, kind)
        if notes:
            missed += 1
            print('MISS', path, notes)
        if new != raw:
            path.write_text(new, encoding='utf-8')
            changed += 1
    print(f'stamped {changed} files, misses {missed}')


if __name__ == '__main__':
    import pathlib
    stamp_site(pathlib.Path(__file__).resolve().parents[2] / 'site')
