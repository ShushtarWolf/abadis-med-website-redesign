"""About Us: fixed 118px goals orbit + N3 membership cards.

Approved 2026-10-27 (Hamid): N3 neon border with float/glow, and 10-node
orbit circles at 118px so every FA / EN / AR label fits inside.
"""
import math
import re

from lib import esc

_FA = str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')
_AR = str.maketrans('0123456789', '٠١٢٣٤٥٦٧٨٩')

# (title, sub, ring, degrees). Ring alternates outer / mid, matching the approval.
_NODES = {
    'fa': [
        ('دانش‌بنیان', 'معاونت علمی', 'outer', -90),
        ('سازمان غذا و دارو', 'مجوز رسمی IFDA', 'mid', -54),
        ('انجمن تولیدکنندگان', 'عضو AMEDAL', 'outer', -18),
        ('اتاق بازرگانی ایران', 'عضو ICCIMA', 'mid', 18),
        ('اتاق ایران و سوئیس', 'همکاری اروپا', 'outer', 54),
        ('اتاق ایران و عمان', 'هاب صادرات منطقه', 'mid', 90),
        ('انجمن مهندسان', 'عضو ISOMEE', 'outer', 126),
        ('خانه صنعت و معدن', 'صنعت جوانان ایران', 'mid', 162),
        ('مجمع خیرین سلامت', 'مسئولیت اجتماعی', 'outer', 198),
        ('پوشش ۲۸+ استان', 'نمایندگان و CE', 'mid', 234),
    ],
    'en': [
        ('Knowledge-based', 'Vice-presidency', 'outer', -90),
        ('Food and Drug', 'IFDA licence', 'mid', -54),
        ('Manufacturers', 'AMEDAL member', 'outer', -18),
        ('Iran Chamber', 'ICCIMA member', 'mid', 18),
        ('Iran–Switzerland', 'Europe link', 'outer', 54),
        ('Iran–Oman', 'Export hub', 'mid', 90),
        ('Engineers', 'ISOMEE member', 'outer', 126),
        ('Industry and Mine', 'Youth industry', 'mid', 162),
        ('Health donors', 'Social duty', 'outer', 198),
        ('28+ provinces', 'Reps and CE', 'mid', 234),
    ],
    'ar': [
        ('قائم على المعرفة', 'النيابة العلمية', 'outer', -90),
        ('الغذاء والدواء', 'ترخيص IFDA', 'mid', -54),
        ('جمعية المنتجين', 'عضو AMEDAL', 'outer', -18),
        ('غرفة إيران', 'عضو ICCIMA', 'mid', 18),
        ('إيران وسويسرا', 'صلة أوروبا', 'outer', 54),
        ('إيران وعُمان', 'مركز تصدير', 'mid', 90),
        ('جمعية المهندسين', 'عضو ISOMEE', 'outer', 126),
        ('الصناعة والتعدين', 'صناعة الشباب', 'mid', 162),
        ('متبرعو الصحة', 'واجب اجتماعي', 'outer', 198),
        ('+٢٨ محافظة', 'وكلاء و CE', 'mid', 234),
    ],
}

_HUB = {
    'fa': ('آبادیس · ۱۰ حلقه', 'عضویت‌ها', 'اهداف در حال حرکت'),
    'en': ('Abadis · 10 rings', 'Memberships', 'Goals in motion'),
    'ar': ('آباديس · ١٠ حلقات', 'العضويات', 'أهداف قيد الحركة'),
}

_CAPTION = {
    'fa': 'اهداف و عضویت‌ها در حال حرکت',
    'en': 'Goals and memberships in motion',
    'ar': 'الأهداف والعضويات قيد الحركة',
}

# Logos already published on the About page. Captions are the approved card labels.
_MEMBERS = [
    ('7450ece6c5.webp', False, {
        'fa': ('مرکز شرکت‌های دانش‌بنیان', 'معاونت علمی ریاست‌جمهوری'),
        'en': ('Knowledge-based companies', 'Vice-presidency for Science'),
        'ar': ('مركز الشركات المعرفية', 'نيابة العلوم'),
    }),
    ('61c3a85085.webp', False, {
        'fa': ('سازمان غذا و دارو (IFDA)', 'رگولاتوری و مجوز سلامت'),
        'en': ('Food and Drug Administration', 'Health licensing (IFDA)'),
        'ar': ('منظمة الغذاء والدواء', 'التراخيص الصحية (IFDA)'),
    }),
    ('542e8af734.webp', False, {
        'fa': ('انجمن تولیدکنندگان (AMEDAL)', 'تجهیزات و ملزومات پزشکی'),
        'en': ('Manufacturers’ association', 'AMEDAL member'),
        'ar': ('جمعية المنتجين (AMEDAL)', 'المعدات والمستلزمات الطبية'),
    }),
    ('baae8d9cb8.webp', False, {
        'fa': ('اتاق بازرگانی ایران (ICCIMA)', 'صنایع، معادن و کشاورزی'),
        'en': ('Iran Chamber (ICCIMA)', 'Industries, mines, agriculture'),
        'ar': ('غرفة تجارة إيران (ICCIMA)', 'الصناعات والمناجم والزراعة'),
    }),
    ('0a77e61397.webp', False, {
        'fa': ('اتاق مشترک ایران و سوئیس', 'همکاری‌های فناوری اروپا'),
        'en': ('Iran–Switzerland chamber', 'European technology link'),
        'ar': ('الغرفة الإيرانية السويسرية', 'التعاون التقني الأوروبي'),
    }),
    ('b4f3cd2f76.webp', False, {
        'fa': ('اتاق مشترک ایران و عمان', 'توسعه صادرات منطقه‌ای'),
        'en': ('Iran–Oman chamber', 'Regional export development'),
        'ar': ('الغرفة الإيرانية العُمانية', 'تطوير التصدير الإقليمي'),
    }),
    ('445859ab76.webp', False, {
        'fa': ('انجمن مهندسان (ISOMEE)', 'مهندسی تجهیزات پزشکی'),
        'en': ('Engineers’ association', 'ISOMEE member'),
        'ar': ('جمعية المهندسين (ISOMEE)', 'هندسة المعدات الطبية'),
    }),
    ('033971ca21.webp', False, {
        'fa': ('خانه صنعت و معدن جوانان', 'صنعت و تجارت جوانان ایران'),
        'en': ('Youth industry and mine', 'Iran youth industry'),
        'ar': ('بيت الصناعة والتعدين', 'صناعة الشباب في إيران'),
    }),
    ('884586a9b2.webp', True, {
        'fa': ('مجمع خیرین تجهیزات پزشکی', 'مسئولیت اجتماعی سلامت'),
        'en': ('Medical-equipment donors', 'Health social responsibility'),
        'ar': ('مجمع متبرعي المعدات الطبية', 'المسؤولية الاجتماعية للصحة'),
    }),
]

_MEM_H = {
    'fa': ('عضویت‌ها', 'نشان‌ها و عضویت‌های منتشرشدهٔ آبادیس'),
    'en': ('Memberships', 'Membership marks published by Abadis'),
    'ar': ('العضويات', 'شعارات العضوية المنشورة لآباديس'),
}


def _digits(lang, text):
    text = str(text)
    if lang == 'fa':
        return text.translate(_FA)
    if lang == 'ar':
        return text.translate(_AR)
    return text


def goals_orbit(lang, prefix):
    """Fixed 680px stage, 118px nodes, scaled with the container width."""
    lang = lang if lang in _NODES else 'fa'
    size, r_mid, r_outer, node_d = 680, 198, 274, 118
    cx = cy = size / 2
    ticks = []
    spokes = []
    nodes = []
    for deg in range(0, 360, 6):
        rad = math.radians(deg)
        r1 = size / 2 - 18
        r2 = (size / 2 - 8) if deg % 30 == 0 else (size / 2 - 13)
        x1, y1 = cx + r1 * math.cos(rad), cy + r1 * math.sin(rad)
        x2, y2 = cx + r2 * math.cos(rad), cy + r2 * math.sin(rad)
        cls = 'ab-tick-maj' if deg % 30 == 0 else 'ab-tick-min'
        ticks.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" class="{cls}"/>')
    for i, (title, sub, ring, deg) in enumerate(_NODES[lang], start=1):
        rad = math.radians(deg)
        dist = r_outer if ring == 'outer' else r_mid
        nx, ny = cx + dist * math.cos(rad), cy + dist * math.sin(rad)
        sx, sy = cx + 78 * math.cos(rad), cy + 78 * math.sin(rad)
        mx = cx + ((78 + dist) * 0.5) * math.cos(rad)
        my = cy + ((78 + dist) * 0.5) * math.sin(rad)
        spokes.append(
            f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{nx:.1f}" y2="{ny:.1f}" class="ab-spoke" stroke-dasharray="6 5"/>'
            f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="3.8" class="ab-pulse"/>'
        )
        left, top = nx - node_d / 2, ny - node_d / 2
        ring_cls = 'node-outer' if ring == 'outer' else 'node-mid'
        num = _digits(lang, f'{i:02d}')
        nodes.append(
            f'<div class="ab-node {ring_cls}" style="width:{node_d}px;height:{node_d}px;left:{left:.1f}px;top:{top:.1f}px;">'
            f'<div class="ab-node-inner"><span class="ab-node-num">{num}</span>'
            f'<strong class="ab-node-title">{esc(title)}</strong>'
            f'<span class="ab-node-sub">{esc(sub)}</span></div></div>'
        )
    kicker, title, sub = _HUB[lang]
    caption = _CAPTION[lang]
    return (
        f'<figure class="ab-orbit-fit" id="moving-targets">'
        f'<figcaption class="ab-orbit-cap">{esc(caption)}</figcaption>'
        f'<div class="ab-stage" style="width:{size}px;height:{size}px;">'
        f'<svg viewBox="0 0 {size} {size}" class="ab-svg" aria-hidden="true">'
        f'<circle cx="{cx}" cy="{cy}" r="{size / 2 - 10}" class="ab-bound"/>'
        f'{"".join(ticks)}'
        f'<circle cx="{cx}" cy="{cy}" r="{r_outer}" class="ab-ring-outer" stroke-dasharray="10 7"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{r_mid}" class="ab-ring-mid" stroke-dasharray="5 6"/>'
        f'<circle cx="{cx}" cy="{cy}" r="102" class="ab-ring-inner"/>'
        f'<path d="M {cx - r_outer} {cy} A {r_outer} {r_outer} 0 0 1 {cx} {cy - r_outer}" class="ab-arc"/>'
        f'<path d="M {cx + r_outer} {cy} A {r_outer} {r_outer} 0 0 1 {cx} {cy + r_outer}" class="ab-arc"/>'
        f'{"".join(spokes)}</svg>'
        f'<div class="ab-hub" style="width:154px;height:154px;left:{cx - 77:.1f}px;top:{cy - 77:.1f}px;">'
        f'<span class="ab-hub-kicker">{esc(kicker)}</span>'
        f'<strong class="ab-hub-title">{esc(title)}</strong>'
        f'<span class="ab-hub-sub">{esc(sub)}</span></div>'
        f'{"".join(nodes)}</div></figure>'
    )


def membership_section(lang, prefix):
    """Nine membership logo cards with the N3 neon frame."""
    lang = lang if lang in _MEM_H else 'fa'
    heading, lead = _MEM_H[lang]
    cards = []
    for i, (file, dark, labels) in enumerate(_MEMBERS):
        name, sub = labels[lang]
        dark_cls = ' is-dark-logo' if dark else ''
        delay = f' style="animation-delay:{-0.35 * i:.2f}s"'
        cards.append(
            f'<article class="n3-card ab-member{dark_cls}"{delay}>'
            f'<div class="ab-member-logo"><img src="{prefix}assets/img/live/{file}" alt="{esc(name)}" loading="lazy" decoding="async"></div>'
            f'<strong>{esc(name)}</strong><span>{esc(sub)}</span></article>'
        )
    return (
        f'<section class="section ab-members" id="memberships"><div class="wrap">'
        f'<h2 class="reveal" style="margin-bottom:8px">{esc(heading)}</h2>'
        f'<p class="reveal" style="margin-bottom:16px">{esc(lead)}</p>'
        f'<div class="ab-member-grid">{"".join(cards)}</div>'
        f'</div></section>'
    )


def inject_about_motion(html, lang, prefix):
    """Idempotent: add the orbit, membership grid, and N3 classes on EN/AR About."""
    if lang not in ('en', 'ar') or 'ab-orbit-fit' in html:
        html = _n3_classes(html)
        return html
    why = '<h2>Why Abadis?</h2>' if lang == 'en' else '<h2>لماذا آباديس؟</h2>'
    if why in html:
        html = html.replace(why, why + goals_orbit(lang, prefix), 1)
    team = '<h2>Our Team</h2>' if lang == 'en' else '<h2>التعرف على الفريق التنفيذي</h2>'
    if team in html and 'ab-member-grid' not in html:
        html = html.replace(team, membership_section(lang, prefix) + team, 1)
    return _n3_classes(html)


def _n3_classes(html):
    if 'n3-card' not in html.split('cert-tile', 1)[-1][:80]:
        html = html.replace('class="cert-tile"', 'class="cert-tile n3-card"')
    html = html.replace('class="card partner reveal"', 'class="card partner reveal n3-card"')
    if 'n3-partner-logo' not in html:
        html = re.sub(
            r'(<img\b[^>]*?(?:Group-2\.jpg|virakam\.webp)[^>]*>)',
            r'<span class="n3-card n3-partner-logo">\1</span>',
            html,
        )
    if 'ab-legacy-slide' not in html:
        html = html.replace('class="swiper-slide"', 'class="swiper-slide ab-legacy-slide"')
    return html
