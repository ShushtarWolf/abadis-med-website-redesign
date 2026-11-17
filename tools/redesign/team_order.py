"""«تیم اجرایی» on About (FA / EN / AR): photo cards in the exact order of abadis-med.com.

Hamid (2026-11-17): no team videos, people in the same order as the live WordPress site.
Live WP lays the desktop team out as three columns (8/8/7, filled top-to-bottom); the order
below is how those cards read on screen, row by row (right-to-left on FA/AR, left-to-right on EN).
WP's mobile list is a separate widget; FA/EN use its order on phones. The AR mobile widget on WP
is a stale 2023 list, so AR phones use the desktop order.
People on the redesign but no longer on WP are kept, at the end.
Photos are the self-hosted copies in site/assets/img/live/ (same people as FA).
"""
import html as H
import re

# FA: name -> desktop photo (site/assets/img/live/<file>.webp); roles come from data/about_live.json
FA_DESKTOP = [
    'ابوالفضل حسنعلی', 'علیرضا حسنعلی', 'نوید حسنعلی',
    'مژده مهین دوست', 'محمد مهدی احمدی', 'نازنین اخوان طباطبایی',
    'نازنین حسنعلی', 'میلاد پورحسن', 'نیلوفر شرفی',
    'زهرا ناطقی', 'روژان کوکبی', 'هلیا تیموری',
    'امیر محسن زاده', 'محبوبه رعیتی', 'کیمیا قدیمی',
    'مهران خلیلی', 'مائده ناصری', 'میثم اسدالهی',
    'پوریا فرهنگ', 'امیرعرشیا تقوی', 'محمد قائم پناه',
    'علی سینا صالحی', 'الهه رستمی',
]
# WP FA mobile widget: same people, «محمد قائم پناه» before «امیرعرشیا تقوی»
FA_MOBILE = FA_DESKTOP[:19] + ['محمد قائم پناه', 'امیرعرشیا تقوی'] + FA_DESKTOP[21:]

# FA desktop photo per person (from data/about_live.json desktop list)
PHOTO = {
    'ابوالفضل حسنعلی': '55f9b3cbba', 'مژده مهین دوست': 'c5b6cffaeb', 'نازنین حسنعلی': '333dcd804b',
    'زهرا ناطقی': '3029c44205', 'امیر محسن زاده': '49f2290279', 'مهران خلیلی': '93b961e6cf',
    'پوریا فرهنگ': '8cae3c0886', 'علی سینا صالحی': '0fb26406fa', 'علیرضا حسنعلی': '138a5cce28',
    'محمد مهدی احمدی': '3cfc2a6f18', 'میلاد پورحسن': '27a1fa05cc', 'روژان کوکبی': 'd410fec876',
    'محبوبه رعیتی': 'd8ed2b7bc0', 'مائده ناصری': '2c4ba40343', 'امیرعرشیا تقوی': '2920e64a94',
    'الهه رستمی': '88b63fd357', 'نوید حسنعلی': '56b77e8867', 'نازنین اخوان طباطبایی': '3700d638a7',
    'نیلوفر شرفی': '8ad9e59e81', 'هلیا تیموری': 'ab1db755c6', 'کیمیا قدیمی': 'c140820f28',
    'میثم اسدالهی': 'db177ffeb0', 'محمد قائم پناه': '829b160d0f',
    # kept from the redesign, no longer on WP
    'سونا هاشمیان': '8393064825',
}
LOGO_TILE = 'd6c3e2d9fc'   # Abadis logo tile WP used for people without a photo

# EN (abadis-med.com/en/about-us/): (name, role, FA name for the photo)
EN = [
    ('Abolfazl Hassanali', 'Chaiman Of The Board', 'ابوالفضل حسنعلی'),
    ('Alireza Hassanali', 'CEO', 'علیرضا حسنعلی'),
    ('Navid Hassanali', 'CCO', 'نوید حسنعلی'),
    ('Mozhdeh Mahindost', 'CFO', 'مژده مهین دوست'),
    ('Mehdi Ahmadi', 'Factory Manager', 'محمد مهدی احمدی'),
    ('Nazanin Akhavan Tabatabaei', 'Legal Affairs Manager', 'نازنین اخوان طباطبایی'),
    ('Nazanin Hassanali', 'PR Manager', 'نازنین حسنعلی'),
    ('Milad Pour Hassan', 'Consultant', 'میلاد پورحسن'),
    ('Niloufar Sharafi', 'Senior Procurement & Supply Specialist', 'نیلوفر شرفی'),
    ('Zahra Nateghi', 'Sales Account Executive', 'زهرا ناطقی'),
    ('Rojan Kokabi', 'Sales Account Executive', 'روژان کوکبی'),
    ('Helia Teymouri', 'Sales Operations Specialist', 'هلیا تیموری'),
    ('Amir Mohsenzadeh', 'Sales Account Executive', 'امیر محسن زاده'),
    ('Mahbube Rayati', 'Sales Account Executive', 'محبوبه رعیتی'),
    ('Kimia Ghadimi', 'Accountant', 'کیمیا قدیمی'),
    ('Meysam Asadollahi', 'Store Keeper', 'میثم اسدالهی'),
    ('Maedeh Naseri', 'QC Manager', 'مائده ناصری'),
    ('Mehran Khalili', 'Production Supervisor', 'مهران خلیلی'),
    ('Mohammad Ghaem Panah', 'Delivery Driver', 'محمد قائم پناه'),
    ('Amirarshia Taghavi', 'Installation & Service Technician', 'امیرعرشیا تقوی'),
    ('Pouriya Farhang', 'Collector', 'پوریا فرهنگ'),
    ('Ali Sina Salehi', 'IT Manager', 'علی سینا صالحی'),
    ('Elahe Rostami', 'Commerical Expert', 'الهه رستمی'),
    # on the redesign, not on WP any more
    ('Sona Hashemian', 'Sales Account Executive', 'سونا هاشمیان'),
]
# WP EN mobile widget order (indexes into EN)
EN_MOBILE = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17, 16, 15, 20, 19, 18, 21, 22, 23]

# AR (abadis-med.com/arabic/من-نحن/)
AR = [
    ('ابوالفضل حسنعلی', 'رئيس مجلس الإدارة'),
    ('علیرضا حسنعلی', 'المدير التنفيذي'),
    ('نوید حسنعلی', 'نائب المدير لشؤون التسويق والمبيعات'),
    ('مژده مهین دوست', 'مدير مالي'),
    ('محمد مهدی احمدی', 'مدير مصنع'),
    ('نازنین اخوان طباطبایی', 'مدير الشؤون القانونية'),
    ('نازنین حسنعلی', 'مدير العلاقات العامة'),
    ('میلاد پورحسن', 'المستشار الأعلى للرئيس التنفيذي'),
    ('نیلوفر شرفی', 'أخصائي أول في التوريد والشؤون التجارية'),
    ('زهرا ناطقی', 'أخصائي المبيعات وشؤون العملاء'),
    ('روژان کوکبی', 'أخصائي المبيعات وشؤون العملاء'),
    ('هلیا تیموری', 'أخصائي عمليات المبيعات'),
    ('امیر محسن زاده', 'أخصائي المبيعات وشؤون العملاء'),
    ('محبوبه رعیتی', 'أخصائي المبيعات وشؤون العملاء'),
    ('کیمیا قدیمی', 'المحاسبين'),
    ('مهران خلیلی', 'مشرف انتاج'),
    ('مائده ناصری', 'مدير ضمان الجودة'),
    ('میثم اسدالهی', 'حارس مستودع'),
    ('پوریا فرهنگ', 'مُحصِّل'),
    ('امیرعرشیا تقوی', 'أخصائي التركيب والخدمات الفنية'),
    ('محمد قائم پناه', 'مسؤول تسليم البضائع'),
    ('علی سینا صالحی', 'مدير تكنولوجيا المعلومات'),
    ('الهه رستمی', 'أخصائي الشؤون التجارية'),
    # on the redesign, not on WP any more
    ('سونا هاشمیان', 'خبير مبيعات'),
    ('مهرداد صالح\u200cفر', 'خبير التثبيت'),
    ('امیر درفکی', 'موزع'),
    ('سلیمه کر', 'الخدمات اللوجستية'),
]

HEAD = {'en': 'Our Team', 'ar': 'التعرف على الفريق التنفيذي'}


def card(p, name, role, file=None):
    esc = H.escape
    if file:
        ph = (f'<img src="{p}assets/img/live/{file}.webp" alt="{esc(name)} — {esc(role)}" '
              f'loading="lazy" decoding="async">')
    else:
        ph = (f'<img src="{p}assets/img/live/{LOGO_TILE}.webp" alt="{esc(name)} — {esc(role)}" '
              f'loading="lazy" decoding="async" style="object-fit:contain;padding:12%;background:#fff">')
    return (f'<div class="member"><div class="av">{ph}</div>'
            f'<strong>{esc(name)}</strong><span>{esc(role)}</span></div>')


def grid(cards, cls):
    return f'<div class="team-grid {cls}">{"".join(cards)}</div>'


def fa_grids(p, team):
    """FA desktop + mobile grids. `team` = about_live.json['team'] (photos/roles from there)."""
    desk = {m['name']: m for m in team['desktop']}
    mob = {m['name']: m for m in team['mobile']}
    def build(order, src):
        out, used = [], set()
        for n in order:
            m = src.get(n) or desk[n]
            used.add(m['file'])
            out.append(card(p, n, m['role'], m['file']))
        # On the redesign data but not on WP: keep, at the end. The old mobile «سونا هاشمیان»
        # entry carries Zahra Nateghi's photo (same file): WP renamed that card, so it is not doubled.
        for n, m in src.items():
            if n not in order and m['file'] not in used:
                out.append(card(p, n, m['role'], m['file']))
        return out
    return grid(build(FA_DESKTOP, desk), 'team--desktop') + '\n    ' + grid(build(FA_MOBILE, mob), 'team--mobile')


def i18n_section(lang, p):
    if lang == 'en':
        rows = [(n, r, PHOTO.get(fa)) for n, r, fa in EN]
        desk = [card(p, *x) for x in rows]
        mob = [card(p, *rows[i]) for i in EN_MOBILE]
    else:
        rows = [(n, r, PHOTO.get(n)) for n, r in AR]
        desk = [card(p, *x) for x in rows]
        mob = list(desk)
    return (f'<section class="section" id="team"><div class="wrap">'
            f'<h2 style="margin-bottom:20px">{H.escape(HEAD[lang])}</h2>'
            f'{grid(desk, "team--desktop")}{grid(mob, "team--mobile")}'
            f'</div></section>')


_TAG = re.compile(r'<(/?)(div|section)\b[^>]*>', re.I)


def _unmatched_closers(region):
    stack, extra = [], []
    for m in _TAG.finditer(region):
        close, tag = m.group(1), m.group(2).lower()
        if not close:
            stack.append(tag)
        elif stack and stack[-1] == tag:
            stack.pop()
        else:
            extra.append(f'</{tag}>')
    return ''.join(extra), stack


def rebuild_i18n_team(html, lang, p='../../'):
    """Replace the EN/AR About team block (WP mirror markup, or an earlier rebuild) with clean
    photo-card grids in WP order. Keeps the enclosing tags balanced. Idempotent."""
    new = i18n_section(lang, p)
    m = re.search(r'<section class="section" id="team">.*?</section>', html, re.S)
    if m:   # already rebuilt
        return html[:m.start()] + new + html[m.end():]
    heads = (['<h2 id="team">Our Team', '<h2>Our Team</h2>'] if lang == 'en' else
             ['<h2><span id="team"></span>', '<h2>التعرف على الفريق التنفيذي'])
    start = next((i for i in (html.find(h) for h in heads) if i >= 0), -1)
    end = html.find('</main>', start)
    if start < 0 or end < 0:
        raise SystemExit(f'team block not found ({lang})')
    region = html[start:end]
    closers, opened = _unmatched_closers(region)
    if opened:
        raise SystemExit(f'unbalanced team region ({lang}): {opened}')
    return html[:start] + new + closers + html[end:]
