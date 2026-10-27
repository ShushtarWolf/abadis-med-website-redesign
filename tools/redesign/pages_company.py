"""About, dealers, contact extras, CSR/SDG extras, calculator, and footer pages."""
import re, json, urllib.parse
from lib import PAGES, SITE, esc, strip_tags, best_img, rewrite_html, href, fa, load
from layout import page, page_hero, section_mark
from render import picture, gallery_link, table, faq_list, aparat, secs, blocks_to_prose

def B(path): return PAGES[path]['blocks']
def ext_attr(ext): return ' target="_blank" rel="noopener"' if ext else ''

# ------------------------------------------------------------------ about
SLOGAN_ABOUT = ['ما به اندازه یک سرانگشت اثر می‌گذاریم،', 'به شما', 'به طبیعت', 'به جهان']   # Abadis-Sign (live)
SLOGAN_ABOUT_I18N = {
    'fa': SLOGAN_ABOUT,
    'en': ['We affect as much as a fingertip', 'To You', 'To Nature', 'To World'],
    'ar': ['نحن نؤثر بقدر طرف إصبع', 'عليك', 'على الطبيعة', 'على العالم'],
}


def _pva(text):
    """Keep the Latin token PVA in its own direction run."""
    return esc(text).replace('PVA', '<bdi dir="ltr">PVA</bdi>')


def about_copy(lang):
    """Verbatim About narrative from abadis-med.com, 2026-10-20. Not the 17 Oct concept notes."""
    return load('about_copy.json')[lang]


def _paras(items):
    return ''.join(f'<p style="text-align:justify">{_pva(x)}</p>' for x in items)


def _colon_items(items):
    bits = []
    for s in items:
        if ': ' in s:
            h, b = s.split(': ', 1)
            bits.append(f'<li><strong>{esc(h)}</strong> — {_pva(b)}</li>')
        else:
            bits.append(f'<li>{_pva(s)}</li>')
    return ''.join(bits)


def principle_cards(lang):
    """Mission, vision, goals and values, each in its own card. Values use the live «تعهد ما» heading."""
    d = about_copy(lang)
    eyebrows = {
        'fa': ('ماموریت', 'چشم‌انداز', 'اهداف', 'ارزش‌ها', 'چرا آکادمی'),
        'en': ('Mission', 'Vision', 'Goals', 'Values', 'Why the Academy'),
        'ar': ('الرسالة', 'الرؤية', 'الأهداف', 'القيم', 'لماذا الأكاديمية'),
    }[lang]
    academy = next((g for g in d['goals'] if 'Academy' in g or 'آکادمی' in g or 'أكاديمية' in g), d['goals'][0])
    vision = _paras(d['vision']) + f'<ul>{_colon_items(d["pillars"])}</ul>' + _paras(d['vision_close'])
    goals = _paras(d['goals_lead']) + f'<ul>{_colon_items(d["goals"])}</ul>'
    commit = ''.join(f'<li>{esc(x)}</li>' for x in d['commit_items'])
    values = _paras(d['commit_lead']) + f'<ul>{commit}</ul>' + _paras(d['commit_close'])
    bodies = (_paras(d['mission']), vision, goals, values)
    titles = (d['mission_h'], d['vision_h'], d['goals_h'], d['commit_h'])
    cards = ''.join(
        f'<article class="mv-card prose"><p class="eyebrow">{esc(eyebrows[i])}</p>'
        f'<h3>{esc(titles[i].rstrip(":"))}</h3>{bodies[i]}</article>'
        for i in range(4))
    why = (f'<article class="mv-card prose why-academy" id="why-academy"><p class="eyebrow">{esc(eyebrows[4])}</p>'
           f'<p>{esc(academy)}</p><p><a class="more-link" href="../academy/">{esc(eyebrows[4])}</a></p></article>')
    return f'<div class="mv-grid">{cards}</div>{why}'


def live_intro_html(lang):
    d = about_copy(lang)
    return (
        _paras(d['intro'])
        + principle_cards(lang)
        + f'<h3 style="margin-top:22px">{esc(d["achieve_h"].rstrip(":"))}</h3>'
        + _paras(d['achieve'])
    )


def live_story_html(lang):
    d = about_copy(lang)
    phases = ''.join(
        f'<h3 style="margin-top:18px">{esc(ph["h"])}</h3>' + _paras(ph['p']) for ph in d['phases'])
    return (
        f'<h3>{esc(d["history_h"])}</h3>'
        + _paras(d['history']) + phases + _paras(d['history_close'])
    )


def _strip_liner_bag(body):
    """Drop the old animated liner-bag image column beside History, and empty videos."""
    body = re.sub(
        r'<div data-element_type="widget">\s*<div>\s*<img\b[^>]*ANIMATED-LINER-BAG[^>]*>\s*</div>\s*</div>',
        '',
        body,
    )
    body = re.sub(
        r'<div data-element_type="column">\s*<div>\s*</div>\s*</div>',
        '',
        body,
    )
    body = re.sub(r'<video\b[^>]*>\s*</video>', '', body, flags=re.I)
    return body


def slogan_block(lang):
    lines = SLOGAN_ABOUT_I18N[lang]
    spans = ''.join(
        f'<span class="slogan-line" style="--i:{n}">{esc(x)}</span>' for n, x in enumerate(lines))
    return f'<p class="slogan reveal" aria-label="{esc(" ".join(lines))}">{spans}</p>'


def about_hero_video(p):
    return (
        f'<video class="about-hero-video" autoplay muted loop playsinline webkit-playsinline '
        f'disablepictureinpicture disableremoteplayback preload="metadata" tabindex="-1" aria-hidden="true" '
        f'poster="{p}assets/media/hero-or-zagros-poster.jpg">'
        f'<source src="{p}assets/media/hero-or-zagros.mp4" type="video/mp4"></video>'
    )


def about_motion_tags(p):
    """Homepage slogan + emblem scripts for the About hero."""
    from pages_home import logo_scroll_css, logo_scroll_scripts
    return logo_scroll_css(p), logo_scroll_scripts(p)


def about_hero(p, lang, h1_html, crumbs):
    """About hero: poster/video, growing emblem, slogan in header type."""
    from pages_home import IMPACT_MARK
    return f'''  <section class="page-hero about-hero">
    {about_hero_video(p)}
    <div class="wrap about-hero-grid">
      <div>{crumbs}
        <h1>{h1_html}</h1>
        {IMPACT_MARK}
        {slogan_block(lang)}
      </div>
    </div>
  </section>'''


def apply_live_about(body, lang):
    """Swap the pre-20-Oct mission block and the history/goals block for the live page text.

    Certificate galleries, partners and the team stay in the existing markup so the
    IMED → ثبت اختراع → بهره‌برداری → جوایز و مقالات order is untouched.
    """
    body = _strip_liner_bag(body)
    if lang not in ('en', 'ar'):
        return body
    intro, story = live_intro_html(lang), live_story_html(lang)
    if lang == 'en':
        hist_key = 'History and Background of Abadis Knowledge-Based Group'
        goals_end = 'Promoting Awareness and Maximizing the Use of Our Solutions in Hospitals and Healthcare Centers</li></ol>'
        intro_start, intro_end = '<p>Abadis Med, a', 'Central America'
    else:
        hist_key = 'التاريخ والخلفية لمجموعة'
        goals_end = 'نشر ثقافة الاستخدام الأمثل لحلولنا ومنتجاتنا في المراكز العلاجية والمستشفيات</li></ol>'
        intro_start, intro_end = '<p>شركة مخازن طبية', 'أمريكا الوسطى'
    h = body.find(hist_key)
    g = body.find(goals_end)
    if h >= 0 and g > h:
        start = body.rfind('<p', 0, h)
        end = g + len(goals_end)
        if start >= 0:
            body = body[:start] + story + body[end:]
    a = body.find(intro_start)
    b = body.find(intro_end)
    if a >= 0 and b > a:
        end = body.find('</p>', b)
        if end > a:
            body = body[:a] + intro + body[end + 4:]
    return body
TEAM_VIDEOS = {'علیرضا حسنعلی': ('alireza', 'team-member'), 'نوید حسنعلی': ('navid', 'team-member-navid')}

# About «مجوزها و گواهینامه‌ها»: Hamid's order. ISO, CE, export permits and
# industrial-design filings stay inside the nearest group.
CERT_GROUPS = {
    'fa': (('imed', 'IMED'), ('patent', 'ثبت اختراع'), ('operate', 'بهره‌برداری'), ('awards', 'جوایز و مقالات')),
    'en': (('imed', 'IMED'), ('patent', 'Patents'), ('operate', 'Operating license'), ('awards', 'Awards and Articles')),
    'ar': (('imed', 'IMED'), ('patent', 'براءات الاختراع'), ('operate', 'رخصة التشغيل'), ('awards', 'الجوائز والمقالات')),
}


def _cert_base(url):
    path = urllib.parse.unquote(urllib.parse.urlsplit(url).path)
    return path.rstrip('/').rsplit('/', 1)[-1].lower()


def cert_group(url):
    """Which of the four About certificate groups a file belongs to."""
    b = _cert_base(url)
    if 'bahre' in b or 'operation-license' in b or 'بهره' in b:
        return 'operate'
    if b.startswith('sabte') or b.startswith('patent') or 'tarh-sanati' in b or b.startswith('industrial'):
        return 'patent'
    if (b.startswith('iso') or b.startswith('igc') or b.startswith('ce.') or b == 'ce.jpg'
            or b.startswith('پروانه') or b.startswith('imed') or b.startswith('صادرات')
            or b.startswith('export') or b.startswith('filter-license')):
        return 'imed'
    return 'awards'


def _cert_rank(url):
    """Inside a group: the named documents first, ISO/CE and طرح صنعتی beside them."""
    b = _cert_base(url)
    g = cert_group(url)
    if g == 'imed':
        if b.startswith('imed') or b.startswith('پروانه') or b.startswith('filter-license'):
            return 0
        if b.startswith('iso') or b.startswith('igc'):
            return 1
        if b.startswith('ce.') or b == 'ce.jpg':
            return 2
        return 3
    if g == 'patent' and ('fixator' in b or 'tarh-sanati' in b or b.startswith('industrial')):
        return 1
    return 0


def _ordered_certs(certs):
    tagged = []
    for i, c in enumerate(certs):
        url = c.get('url') or c.get('href') or ''
        tagged.append((cert_group(url), _cert_rank(url), i, c))
    order = {k: n for n, (k, _) in enumerate(CERT_GROUPS['fa'])}
    tagged.sort(key=lambda t: (order.get(t[0], 9), t[1], t[2]))
    return tagged


_CERT_ANCHOR = re.compile(
    r'<a\b[^>]*href="[^"]*wp-content/uploads/[^"]+\.(?:jpe?g|png|webp)"[^>]*>[\s\S]*?</a>',
    re.I)


def regroup_i18n_certs(html, lang):
    """Reorder the EN/AR About license galleries into the same four groups. Idempotent."""
    spec = {
        'en': (['<h2>Certificates</h2>', '<h2>Licenses</h2>'], '<h2>Business Partners</h2>'),
        'ar': (['<h2>التراخيص</h2>', '<h2>الشهادات</h2>'], '<h2>الأعضاء</h2>'),
    }.get(lang)
    if not spec or 'class="cert-groups"' in html:
        return html
    heads, end = spec
    found = sorted((html.find(h), h) for h in heads if html.find(h) >= 0)
    if not found:
        return html
    start = found[0][0]
    end_i = html.find(end, start)
    if end_i < 0:
        return html
    region = html[start:end_i]
    anchors = _CERT_ANCHOR.findall(region)
    if not anchors:
        return html
    ranked = []
    for n, a in enumerate(anchors):
        href = re.search(r'href="([^"]+)"', a).group(1)
        ranked.append((cert_group(href), _cert_rank(href), n, a, href))
    order = {k: i for i, (k, _) in enumerate(CERT_GROUPS[lang])}
    ranked.sort(key=lambda t: (order.get(t[0], 9), t[1], t[2]))
    buckets = {k: [] for k, _ in CERT_GROUPS[lang]}
    for g, _r, _n, a, href in ranked:
        buckets[g].append((a, href))
    parts = ['<div class="cert-groups">']
    for key, label in CERT_GROUPS[lang]:
        items = buckets[key]
        if not items:
            continue
        h3 = f'<h3 lang="en">{esc(label)}</h3>' if key == 'imed' else f'<h3>{esc(label)}</h3>'
        tiles = []
        for a, href in items:
            cap = ''
            for bit in re.findall(r'>([^<]{1,120})<', a):
                bit = bit.strip()
                if bit:
                    cap = bit
                    break
            tiles.append(
                f'<figure class="cert-item"><a class="cert-tile" href="{esc(href)}" data-gallery="certs">'
                f'<img src="{esc(href)}" alt="{esc(cap or label)}" loading="lazy" decoding="async"></a>'
                + (f'<figcaption>{esc(cap)}</figcaption>' if cap else '')
                + '</figure>'
            )
        parts.append(f'<div class="cert-group" id="certs-{key}">{h3}<div class="cert-wall">{"".join(tiles)}</div></div>')
    parts.append('</div>')
    new_region = region
    for a in anchors:
        new_region = new_region.replace(a, '', 1)
    for h in heads:
        new_region = new_region.replace(h, '', 1)
    return html[:start] + ''.join(parts) + new_region + html[end_i:]


def _team_html(p, members, cls):
    out = []
    for m in members:
        img = f'{p}assets/img/live/{m["file"]}.webp'
        ph = f'<img src="{img}" alt="{esc(m["name"])} — {esc(m["role"])}" loading="lazy" decoding="async">'
        if m['name'] in TEAM_VIDEOS:   # subtle clip: muted loop autoplay, no controls / play button
            d, n = TEAM_VIDEOS[m['name']]; v = f'{p}assets/team-videos/{d}/{n}'
            ph = (f'<video class="team-clip" autoplay muted loop playsinline webkit-playsinline '
                  f'disablepictureinpicture disableremoteplayback preload="metadata" tabindex="-1" '
                  f'poster="{v}-poster.webp" aria-label="{esc(m["name"])}">'
                  f'<source src="{v}.webm" type="video/webm"><source src="{v}.mp4" type="video/mp4"></video>')
        out.append(f'<div class="member"><div class="av">{ph}</div><strong>{esc(m["name"])}</strong><span>{esc(m["role"])}</span></div>')
    return f'<div class="team-grid {cls}">{"".join(out)}</div>'


# Live «شرکای تجاری» / Business Partners (abadis-med.com/درباره-ما/ and /en/about-us/, 2026-10-27).
# Arabic has no separate live partner block; its cards use the English page's wording.
_PARTNER_H = {'fa': 'شرکای تجاری', 'en': 'Business Partners', 'ar': 'الشركاء التجاريون'}
_PARTNER_LINK = {'fa': 'وب سایت مجموعه', 'en': 'Visit Website', 'ar': 'زيارة الموقع'}
PARTNERS = [
    {
        'img': {
            'fa': 'https://abadis-med.com/wp-content/uploads/2022/12/gulf-innovation-gate-1030x510-1-1024x507.png',
            'en': 'https://www.abadis-med.com/en/wp-content/uploads/2026/10/gulf-innovation-gate-logo.png',
            'ar': 'https://www.abadis-med.com/en/wp-content/uploads/2026/10/gulf-innovation-gate-logo.png',
        },
        'href': 'https://gulfinnovationgate.com/',
        'alt': 'Gulf Innovation Gate',
        'text': {
            'fa': 'شرکت Gulf Innovation Gate، مستقر در مسقط عمان، در زمینه تأمین و توزیع تجهیزات پزشکی یک‌بارمصرف در کشورهای حوزه خلیج فارس فعالیت می‌کند. این شرکت با تمرکز بر کیفیت، ایمنی و نوآوری، به نیازهای مراکز درمانی پاسخ می‌دهد و ارتقای خدمات سلامت و توجه به محیط‌زیست را از محورهای اصلی فعالیت خود می‌داند.',
            'en': 'Based in Muscat, Oman, Gulf Innovation Gate specializes in supplying and distributing disposable medical equipment across the Gulf Cooperation Council (GCC) countries. With a focus on quality, safety, and innovation, the company serves the needs of healthcare facilities while supporting better healthcare and environmental responsibility.',
            'ar': 'تتخذ شركة Gulf Innovation Gate من مسقط في سلطنة عُمان مقرًا لها، وتتخصص في توريد وتوزيع المعدات الطبية ذات الاستخدام الواحد في دول مجلس التعاون الخليجي. وتركّز على الجودة والسلامة والابتكار لتلبية احتياجات المنشآت الصحية، ودعم رعاية صحية أفضل والمسؤولية تجاه البيئة.',
        },
    },
    {
        'img': {
            'fa': 'https://abadis-med.com/wp-content/uploads/2022/12/Group-2.jpg',
            'en': 'https://abadis-med.com/wp-content/uploads/2022/12/Group-2.jpg',
            'ar': 'https://abadis-med.com/wp-content/uploads/2022/12/Group-2.jpg',
        },
        'href': {'fa': 'https://goharangostar.com/fa/', 'en': 'https://goharangostar.com/', 'ar': 'https://goharangostar.com/'},
        'alt': {'fa': 'گوهران گستر نادین', 'en': 'Goharan Gostar Nadin', 'ar': 'گوهران گستر نادین'},
        'text': {
            'fa': 'شرکت دانش‌بنیان گوهران گستر نادین در زمینه توسعه و تولید فیلترهای متخلخل و محصولات پلیمری فعالیت می‌کند. این شرکت با تکیه بر دانش فنی و نوآوری، بر ارائه راهکارهای فیلتراسیون متناسب با نیاز صنایع تمرکز دارد و ارتقای کیفیت و عملکرد محصولات را محور فعالیت خود قرار داده است.',
            'en': 'Goharan Gostar Nadin is a knowledge-based company specializing in the development and manufacture of porous filters and polymer products. Drawing on technical expertise and innovation, the company provides filtration solutions tailored to industrial needs, with a focus on improving product quality and performance.',
            'ar': 'شركة گوهران گستر نادین (Goharan Gostar Nadin) شركة قائمة على المعرفة، تعمل في تطوير وإنتاج الفلاتر المسامية والمنتجات البوليمرية. وتعتمد على الخبرة الفنية والابتكار لتقديم حلول ترشيح تناسب احتياجات الصناعات، وتجعل رفع جودة المنتجات وأدائها محور عملها.',
        },
    },
    {
        'img': {
            'fa': 'https://abadis-med.com/wp-content/uploads/2023/12/v-mn-02-1.webp',
            'en': 'https://abadis-med.com/wp-content/uploads/2023/12/v-mn-02-1.webp',
            'ar': 'https://abadis-med.com/wp-content/uploads/2023/12/v-mn-02-1.webp',
        },
        'href': 'https://virakam.com/',
        'alt': {'fa': 'ویراکام', 'en': 'Virakam', 'ar': 'ویراکام'},
        'text': {
            'fa': 'ویراکام در حوزه هوش تجاری و تحلیل داده فعالیت می‌کند و به کسب‌وکارها کمک می‌کند داده‌های خود را به شناخت دقیق و تصمیم‌های مؤثر تبدیل کنند. ما با طراحی داشبوردهای مدیریتی و راهکارهای تحلیلی، مسیر پایش عملکرد، شناسایی فرصت‌ها و بهبود فرایندهای سازمان را هموار می‌کنیم.',
            'en': 'Virakam specializes in business intelligence and data analytics, helping businesses turn their data into clear insights and informed decisions. Through management dashboards and analytical solutions, we help organizations monitor performance, identify opportunities, and improve their processes.',
            'ar': 'تعمل ويراكام (Virakam) في مجال ذكاء الأعمال وتحليل البيانات، وتساعد المؤسسات على تحويل بياناتها إلى معرفة دقيقة وقرارات فعّالة. ومن خلال لوحات المعلومات الإدارية والحلول التحليلية، تيسّر متابعة الأداء واكتشاف الفرص وتحسين عمليات المؤسسة.',
        },
    },
    {
        'img': {
            'fa': 'https://abadis-med.com/wp-content/uploads/2026/10/logo-ADPmed.jpg',
            'en': 'https://www.abadis-med.com/en/wp-content/uploads/2026/10/logo-adp.png',
            'ar': 'https://www.abadis-med.com/en/wp-content/uploads/2026/10/logo-adp.png',
        },
        'href': {'fa': 'https://abadis-med.com/', 'en': 'https://www.abadis-med.com/en/', 'ar': 'https://abadis-med.com/'},
        'alt': {'fa': 'شرکت ابزار درمان پرشیا', 'en': 'Abzar Darman Persia', 'ar': 'شركة ابزار درمان پرشيا'},
        'text': {
            'fa': 'شرکت ابزار درمان پرشیا در زمینه بازرگانی و تأمین تجهیزات پزشکی فعالیت می‌کند و هدف خود را پاسخ‌گویی به نیازهای مراکز درمانی و فعالان حوزه سلامت قرار داده است. ما با تمرکز بر کیفیت محصولات، تأمین مطمئن و ارتباط مسئولانه با مشتریان، در مسیر ایجاد همکاری‌های پایدار و ارتقای خدمات سلامت گام برمی‌داریم.',
            'en': 'Abzar Darman Persia specializes in trading and supplying medical equipment to meet the needs of healthcare facilities and professionals. With a focus on product quality, reliable supply, and responsive customer service, we strive to build lasting partnerships and support better healthcare.',
            'ar': 'تتخصص شركة ابزار درمان پرشيا (Abzar Darman Persia) في تجارة وتوريد المعدات الطبية، وتهدف إلى تلبية احتياجات المنشآت الصحية والعاملين في القطاع الصحي. ومع التركيز على جودة المنتجات والتوريد الموثوق والتواصل المسؤول مع العملاء، تمضي في بناء شراكات مستدامة والارتقاء بخدمات الصحة.',
        },
    },
]


def _partner_field(spec, key, lang):
    val = spec[key]
    if isinstance(val, dict):
        return val.get(lang) or val.get('fa') or ''
    return val


def partners_html(lang, prefix):
    """Four n3 partner cards. Logos and «وب سایت مجموعه» both open the live site."""
    cards = []
    for spec in PARTNERS:
        href = _partner_field(spec, 'href', lang)
        alt = _partner_field(spec, 'alt', lang)
        url = _partner_field(spec, 'img', lang)
        pic = picture(prefix, url, alt, 600) or picture(prefix, _partner_field(spec, 'img', 'fa'), alt, 600)
        logo = f'<a href="{esc(href)}" target="_blank" rel="noopener">{pic}</a>' if pic else ''
        text = _partner_field(spec, 'text', lang)
        label = _PARTNER_LINK.get(lang, _PARTNER_LINK['en'])
        cards.append(
            f'<div class="card partner reveal n3-card"><div class="logo-box">{logo}</div>'
            f'<p>{esc(text)}</p>'
            f'<a class="more-link" href="{esc(href)}" target="_blank" rel="noopener">{esc(label)}</a></div>'
        )
    return ''.join(cards)


def partners_section(lang, prefix):
    h = _PARTNER_H.get(lang, _PARTNER_H['en'])
    return (
        f'<section class="section section--alt" id="partners"><div class="wrap">'
        f'<h2 class="reveal" style="margin-bottom:20px">{esc(h)}</h2>'
        f'<div class="grid g-4">{partners_html(lang, prefix)}</div>'
        f'</div></section>'
    )


def about(write):
    """About page from the LIVE abadis-med.com/درباره-ما/ (data/about_live.json, fetched 2026-10-14).
    Team order is exactly live: desktop list on desktop, mobile list on mobile (the live site has two)."""
    p = '../'; d = load('about_live.json')
    copy = about_copy('fa')
    lead = copy['intro'][0]
    intro = live_intro_html('fa')
    phases = ''.join(
        f'<h3 class="reveal" style="margin-top:18px">{esc(ph["h"])}</h3>' + _paras(ph['p'])
        for ph in copy['phases'])
    hist = (f'<h2>{esc(copy["history_h"])}</h2>' + _paras(copy['history']) + phases
            + _paras(copy['history_close']))
    whys = ''.join(f'<li>{esc(x)}</li>' for x in d['why'][1:])
    from PIL import Image
    grouped = {k: [] for k, _ in CERT_GROUPS['fa']}
    n = 0
    for g, _rank, _i, c in _ordered_certs(d['certs']):
        f = SITE / f'assets/img/live/{c["file"]}.webp'
        if not f.exists():
            continue
        n += 1
        w, h = Image.open(f).size
        src = f'{p}assets/img/live/{c["file"]}.webp'
        grouped[g].append(
            f'<a class="cert-tile n3-card" href="{src}" data-gallery="certs" data-w="{w}" data-h="{h}" aria-label="نمایش بزرگ‌تر: مجوز و گواهی {fa(n)}">'
            f'<img src="{src}" width="{w}" height="{h}" alt="مجوز / گواهی‌نامه آبادیس {fa(n)}" loading="lazy" decoding="async"></a>'
        )
    cert_blocks = []
    for key, label in CERT_GROUPS['fa']:
        if not grouped[key]:
            continue
        h3 = f'<h3 lang="en">{esc(label)}</h3>' if key == 'imed' else f'<h3>{esc(label)}</h3>'
        cert_blocks.append(f'<div class="cert-group reveal" id="certs-{key}">{h3}<div class="cert-wall">{"".join(grouped[key])}</div></div>')
    certs_html = f'<div class="cert-groups">{"".join(cert_blocks)}</div>'
    hero = about_hero(p, 'fa', 'آشنایی با <em>آبادیس</em>', crumbs_html(p))
    main = f'''{hero}
  <nav class="anchors" aria-label="بخش‌های صفحه"><div class="wrap"><a href="#intro">درباره ما</a><a href="#history">تاریخچه</a><a href="#why">چرا آبادیس؟</a><a href="#memberships">عضویت‌ها</a><a href="#certs">مجوزها و گواهینامه‌ها</a><a href="#partners">شرکای تجاری</a><a href="#team">تیم اجرایی</a></div></nav>
  <section class="section" id="intro"><div class="wrap prose" style="max-width:1000px">
    <h2 class="reveal" style="margin-bottom:14px">درباره ما بیشتر بدانید...</h2>
    {intro}
  </div></section>
  <section class="section section--alt" id="history"><div class="wrap prose" style="max-width:1000px">
    <div class="reveal">{hist}</div>
  </div></section>
  <section class="section section--alt" id="why"><div class="wrap">
    <h2 class="reveal sec-title" style="margin-bottom:20px">{section_mark(p, 'why')}چرا آبادیس؟</h2>
    <ul class="checks why-list reveal">{whys}</ul>
  </div></section>
  {__import__('about_motion').membership_section('fa', p)}
  <section class="section" id="certs"><div class="wrap">
    <h2 class="reveal" style="margin-bottom:8px">مجوزها و گواهینامه‌ها</h2>
    <p class="reveal" style="margin-bottom:18px">همهٔ {fa(n)} مجوز، گواهینامه و تقدیرنامهٔ منتشرشده در سایت آبادیس.</p>
    {certs_html}
  </div></section>
  {partners_section('fa', p)}
  <section class="section" id="team"><div class="wrap">
    <h2 class="reveal" style="margin-bottom:20px">آشنایی با تیم اجرایی</h2>
    {_team_html(p, d['team']['desktop'], 'team--desktop')}
    {_team_html(p, d['team']['mobile'], 'team--mobile')}
  </div></section>'''
    head_css, motion_js = about_motion_tags(p)
    write('about/index.html', page(p, 'about', 'آشنایی با ما', lead[:160], main, lightbox=True,
          extra_head=head_css, html_attrs='data-slogan="t1"',
          scripts=motion_js + f'<script src="{p}assets/js/motion.js" defer></script>\n'))


def crumbs_html(p):
    from layout import crumbs
    return crumbs(p, [('آشنایی با ما', None)])

# ------------------------------------------------------------------ dealers
PROVINCES = ['آذربایجان شرقی', 'آذربایجان غربی', 'اردبیل', 'اصفهان', 'البرز', 'ایلام', 'بوشهر', 'تهران', 'چهارمحال و بختیاری',
             'خراسان جنوبی', 'خراسان رضوی', 'خراسان شمالی', 'خوزستان', 'زنجان', 'سمنان', 'سیستان و بلوچستان', 'فارس', 'قزوین', 'قم',
             'کردستان', 'کرمان', 'کرمانشاه', 'کهگیلویه و بویراحمد', 'گلستان', 'گیلان', 'لرستان', 'مازندران', 'مرکزی', 'هرمزگان', 'همدان', 'یزد']
PROV_T = {
 'en': dict(zip(PROVINCES, ['East Azerbaijan','West Azerbaijan','Ardabil','Isfahan','Alborz','Ilam','Bushehr','Tehran','Chaharmahal and Bakhtiari','South Khorasan','Razavi Khorasan','North Khorasan','Khuzestan','Zanjan','Semnan','Sistan and Baluchestan','Fars','Qazvin','Qom','Kurdistan','Kerman','Kermanshah','Kohgiluyeh and Boyer-Ahmad','Golestan','Gilan','Lorestan','Mazandaran','Markazi','Hormozgan','Hamadan','Yazd'])),
 'ar': dict(zip(PROVINCES, ['أذربيجان الشرقية','أذربيجان الغربية','أردبيل','أصفهان','البرز','إيلام','بوشهر','طهران','جهارمحال وبختياري','خراسان الجنوبية','خراسان رضوي','خراسان الشمالية','خوزستان','زنجان','سمنان','سيستان وبلوشستان','فارس','قزوين','قم','كردستان','كرمان','كرمانشاه','كهكيلويه وبوير أحمد','كلستان','كيلان','لرستان','مازندران','المركزية','هرمزكان','همدان','يزد'])),
}
DEALER_T = {
 'fa': dict(n='نماینده', none='بدون نماینده', aria='نقشه نمایندگان آبادیس در استان‌های ایران', cap='برای دیدن نماینده، روی استان کلیک کنید.', src='مرز استان‌ها: geoBoundaries (CC BY 4.0)', list='لیست استان ها', has='دارای نماینده', prov='استان', title='نمایندگان استان {}', note=''),
 'en': dict(n='representative(s)', none='no representative', aria='Map of Abadis representatives across the provinces of Iran', cap='Tap a province to see its representative.', src='Province borders: geoBoundaries (CC BY 4.0)', list='Provinces', has='Has a representative', prov='provinces', title='Representatives in {}', note='Representative names, phone numbers and addresses are shown as published on the Persian site.'),
 'ar': dict(n='ممثل', none='لا يوجد ممثل', aria='خريطة ممثلي آباديس في محافظات إيران', cap='اضغط على المحافظة لعرض ممثلها.', src='حدود المحافظات: geoBoundaries (CC BY 4.0)', list='المحافظات', has='يوجد ممثل', prov='محافظة', title='ممثلو محافظة {}', note='تُعرض أسماء الممثلين وأرقامهم وعناوينهم كما نُشرت في الموقع الفارسي.'),
}
def _num(lang, n): return fa(n) if lang == 'fa' else (str(n) if lang == 'en' else str(n).translate(str.maketrans('0123456789', '٠١٢٣٤٥٦٧٨٩')))
def _pname(lang, n): return n if lang == 'fa' else PROV_T[lang].get(n, n)

def _iran_map(have, counts, lang='fa'):
    m = load('iran_provinces.json'); T = DEALER_T[lang]
    paths = []; dots = []
    for n, v in m['p'].items():
        on = n in have; lab = esc(_pname(lang, n)) + (f' – {_num(lang, counts[n])} {T["n"]}' if on else f' – {T["none"]}')
        paths.append(f'<path d="{v["d"]}" class="{"has" if on else "none"}" data-prov="{esc(n)}"' + (' tabindex="0" role="button"' if on else '') + f' aria-label="{lab}"><title>{lab}</title></path>')
        if on: dots.append(f'<circle cx="{v["c"][0]}" cy="{v["c"][1]}" r="5.5"/>')
    return (f'<figure class="iran-map reveal"><svg viewBox="0 0 {m["w"]} {m["h"]}" role="img" aria-label="{esc(T["aria"])}">'
            f'<g class="provs">{"".join(paths)}</g><g class="dots" aria-hidden="true">{"".join(dots)}</g></svg>'
            f'<figcaption>{esc(T["cap"])} <small dir="ltr" lang="en" class="latin-digits">{esc(T["src"])}</small></figcaption></figure>'
            """<script>document.querySelectorAll('.iran-map path.has').forEach(function(p){function go(){var b=document.querySelector('#provChips button[data-prov="'+p.dataset.prov+'"]');if(b&&b.getAttribute('aria-pressed')!=='true'){b.click();}document.querySelectorAll('.iran-map path.on').forEach(function(x){x.classList.remove('on')});p.classList.add('on');var g=document.querySelector('.prov-group[data-prov="'+p.dataset.prov+'"]');if(g)g.scrollIntoView({behavior:'smooth',block:'start'});}p.addEventListener('click',go);p.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();go();}});});</script>""")

def dealers_widget(lang):
    """Map + province chips + dealer cards (same data on fa/en/ar)."""
    T = DEALER_T[lang]; data = load('dealers.json'); groups = data['groups']
    have = {g['province'] for g in groups if g.get('dealers')}
    counts = {g['province']: len(g.get('dealers') or []) for g in groups}
    total = sum(counts.values())
    chips = ''.join(
        f'<button type="button" data-prov="{esc(pv)}" aria-pressed="false">{esc(_pname(lang, pv))}</button>' if pv in have
        else f'<button type="button" class="none" disabled title="{esc(T["none"])}">{esc(_pname(lang, pv))}</button>'
        for pv in PROVINCES)
    def row(k, v):
        if 'تلفن' in k:
            num = re.sub(r'[^\d۰-۹]', '', v).translate(str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789'))
            v = f'<a href="tel:{num}" dir="ltr">{esc(v)}</a>'
        else: v = esc(v)
        return f'<dt>{esc(k)}:</dt><dd>{v}</dd>'
    out = []
    for g in groups:
        pv, ds = g['province'], g.get('dealers') or []
        title = (g.get('title') or T['title'].format(pv)) if lang == 'fa' else T['title'].format(_pname(lang, pv))
        ents = ''.join(f'<div class="dealer"{"" if lang == "fa" else " lang=\"fa\" dir=\"rtl\""}><h3>{esc(d["name"])}</h3>' + (f'<dl>{"".join(row(k, v) for k, v in d.get("rows") or [])}</dl>' if d.get('rows') else '') + '</div>' for d in ds)
        out.append(f'<div class="card prov-group reveal" data-prov="{esc(pv)}" id="p-{esc(pv.replace(" ", "-"))}"><h2>{esc(title)}</h2>{ents}</div>')
    note = f'<p class="prov-note">{esc(T["note"])}</p>' if T['note'] else ''
    return f'''<h2 class="reveal" style="margin-bottom:16px">{esc(T["list"])}</h2>
    {_iran_map(have, counts, lang)}
    <div class="prov-chips reveal" id="provChips">{chips}</div>
    <p class="prov-legend"><span><i></i>{esc(T["has"])} ({_num(lang, len(have))} {esc(T["prov"])})</span><span><i class="none"></i>{esc(T["none"])}</span><span>{_num(lang, total)} {esc(T["n"])}</span></p>{note}
    <div class="prov-grid" id="dealerList">{"".join(out)}</div>'''

def dealers(write):
    p = '../'
    intro = load('dealers.json').get('intro') or 'لیست نمایندگان فروش محصولات مخازن طبی آبادیس در سراسر کشور'
    main = f'''{page_hero(p, [('لیست نمایندگان', None)], 'لیست <em>نمایندگان</em>', esc(intro))}
  <section class="section"><div class="wrap">
    {dealers_widget('fa')}
    {__import__('pages_home').membership_orbit(p, 'عضویت آبادیس', 'اهداف در حال حرکت')}
  </div></section>'''
    write('dealers/index.html', page(p, 'dealers', 'لیست نمایندگان', intro, main))

# ------------------------------------------------------------------ calculator
def calculator(write):
    p = '../'
    labels = ['صرفه جویی در مصرف آب (لیتر)', 'هزینه مربوط به شست و شو و ضد عفونی (تومان)', 'صرفه جویی در زمان کادر درمان (ساعت)']
    def outs(prefix): return ''.join(f'<div><span>{l}</span><output id="{prefix}{i}">۰</output></div>' for i, l in enumerate(labels))
    main = f'''{page_hero(p, [('محاسبه‌گر', None)], 'محاسبه <em>گر</em>', 'صرفه جویی در مصرف آب، هزینه شست و شو و ضد عفونی و زمان کادر درمان')}
  <section class="section"><div class="wrap">
    <div class="calc-grid">
      <form class="calc reveal" id="calcSurg" onsubmit="return false">
        <h2>بر مبنای تعداد عمل جراحی در سال</h2>
        <div class="form"><label>تعداد عمل در سال *<input type="number" inputmode="numeric" min="0" step="1" name="s" placeholder="مثلاً ۵۰۰۰"></label></div>
        <div class="calc-out">{outs('cs')}</div>
      </form>
      <form class="calc reveal" id="calcBeds" onsubmit="return false">
        <h2>بر مبنای تعداد تخت در مراکز درمانی</h2>
        <div class="form grid g-2" style="gap:12px"><label>تعداد تخت اتاق عمل *<input type="number" inputmode="numeric" min="0" step="1" name="o"></label><label>تعداد تخت ICU|CCU *<input type="number" inputmode="numeric" min="0" step="1" name="i"></label></div>
        <div class="calc-out">{outs('cb')}</div>
      </form>
    </div>
  </div></section>
  <section class="section" style="padding-top:0"><div class="wrap"><div class="doc-links"><a href="../products/suction-bag/">کیسه ساکشن یکبار مصرف</a><a href="../sdgs/">توسعه پایدار</a><a href="../contact/">ارتباط با ما</a></div></div></section>'''
    js = '''<script>
(function(){
  var nf = new Intl.NumberFormat('fa-IR', {maximumFractionDigits: 1});
  function r(x, d){ var m = Math.pow(10, d); return Math.round(x * m) / m; }
  function v(f, n){ var x = parseFloat(String(f.elements[n].value).replace(/[۰-۹]/g, function(c){return '۰۱۲۳۴۵۶۷۸۹'.indexOf(c)})); return isFinite(x) && x > 0 ? x : 0; }
  function set(id, x){ document.getElementById(id).textContent = nf.format(x); }
  var s = document.getElementById('calcSurg'), b = document.getElementById('calcBeds');
  var LAST_KNOWN_USD_TOMAN = 269500, USD_RATE_KEY = 'abadis-usd-toman';
  var USD_RATE_URL = 'https://api.tgju.org/v1/market/indicator/today-table-data/price_dollar_rl?lang=fa&start=0&length=1';
  var usdToman = LAST_KNOWN_USD_TOMAN;
  try { var saved = JSON.parse(localStorage.getItem(USD_RATE_KEY) || ''); if (saved && isFinite(+saved.toman) && +saved.toman > 0) usdToman = +saved.toman; } catch (e) {}
  function surg(){ var S = v(s, 's'); set('cs0', r(S*1.6*9.971, 0)); set('cs1', r(S*2.5*usdToman, 1)); set('cs2', r(S*1.6*2.2*7.1/60, 1)); }
  function beds(){ var O = v(b, 'o'), I = v(b, 'i'), u = O*254 + I*67; set('cb0', r(u*1.6*9.971, 0)); set('cb1', r((O*254 + I*65)*2.5*usdToman, 1)); set('cb2', r(u*1.7*2.2*7.1/60, 1)); }
  function loadUsd(){ if (typeof fetch !== 'function') return; var ctrl = typeof AbortController === 'function' ? new AbortController() : null; var timer = setTimeout(function(){ if (ctrl) ctrl.abort(); }, 8000); fetch(USD_RATE_URL, ctrl ? {cache:'no-store', signal:ctrl.signal} : {cache:'no-store'}).then(function(res){ if (!res.ok) throw new Error('usd'); return res.json(); }).then(function(data){ var cell = data && data.data && data.data[0] && data.data[0][0]; var n = Number(String(cell == null ? '' : cell).replace(/<[^>]*>/g, '').replace(/[,،٬\\s]/g, '')); if (!isFinite(n) || n < 10000) throw new Error('usd'); usdToman = n / 10; try { localStorage.setItem(USD_RATE_KEY, JSON.stringify({toman:usdToman, rial:n, updatedAt:new Date().toISOString(), source:USD_RATE_URL})); } catch (e) {} surg(); beds(); }).catch(function(){}).then(function(){ clearTimeout(timer); }); }
  s.addEventListener('input', surg); b.addEventListener('input', beds); surg(); beds(); loadUsd();
})();
</script>
'''
    write('calculator/index.html', page(p, 'calculator', 'محاسبه گر', 'محاسبه‌گر صرفه جویی کیسه ساکشن یکبار مصرف آبادیس: مصرف آب، هزینه شست و شو و ضد عفونی و زمان کادر درمان.', main, scripts=js))

# ------------------------------------------------------------------ SDGs / توسعه پایدار (full generated page)
# Seven key goals, in live-page order. The squares are the original UN tiles
# from 9243ca72 (FA webps and the EN page's E-WEB / SDG pngs), recolored so the
# field is #066163 → #0d9488 and the white pictogram, number, and title stay #fff.
# Do not replace these with drawn SVG tiles.
_SDG_FA = [
    ('assets/img/c/a74f1583bbe3-240.webp', 'سلامت و تندرستی', 240),
    ('assets/img/c/92ab4af0990c-240.webp', 'آب پاک و بهداشت', 240),
    ('assets/img/c/15eb17f5c3ff-240.webp', 'انرژی پاک و مقرون‌به‌صرفه', 240),
    ('assets/img/c/7b91c29f0cec-240.webp', 'کار شایسته و رشد اقتصادی', 240),
    ('assets/img/c/c40a4113acaa-240.webp', 'صنعت، نوآوری و زیرساخت', 240),
    ('assets/img/c/efac003f8971-240.webp', 'مصرف و تولید مسئولانه', 240),
    ('assets/img/c/19c49c17129e-240.webp', 'اقدام برای اقلیم', 240),
]
_SDG_EN = [
    ('assets/img/c/796ec2dc3c0f-480.webp', 'Good Health and Well-Being', 480),
    ('assets/img/c/206b6ee4b941-480.webp', 'Clean Water and Sanitation', 480),
    ('assets/img/c/6c9f35a323a6-480.webp', 'Affordable and Clean Energy', 480),
    ('assets/img/c/9aa88d5db7e4-480.webp', 'Decent Work and Economic Growth', 480),
    ('assets/img/c/7abbc7340733-480.webp', 'Industry, Innovation and Infrastructure', 480),
    ('assets/img/c/989df7de169c-480.webp', 'Responsible Consumption and Production', 480),
    ('assets/img/c/231b02bafa3f-480.webp', 'Climate Action', 480),
]

_RAINBOW_GOAL_IMG = re.compile(
    r'<img\b[^>]*(?:E-WEB-Goal|Sustainable_Development_Goal|E_SDG-goals_icons|'
    r'a74f1583bbe3|92ab4af0990c|15eb17f5c3ff|7b91c29f0cec|c40a4113acaa|efac003f8971|19c49c17129e)[^>]*>',
    re.I,
)
_GOAL_OL = re.compile(
    r'<ol(?:\s[^>]*)?>\s*<li>(.*?)</li>\s*</ol>(\s*<ul>.*?</ul>)?',
    re.S | re.I,
)
_GOAL_HEAD = re.compile(
    r'(<h[23][^>]*>[^<]*(?:اهداف کلیدی|Key Objectives)[^<]*</h[23]>)',
    re.I,
)


def sdg_icons(lang, prefix):
    """Seven original UN tiles, teal-recolored. The 1–7 list stays in the prose below."""
    rows = _SDG_EN if lang == 'en' else _SDG_FA
    bits = []
    for i, (src, alt, wh) in enumerate(rows):
        bits.append(
            f'<span class="sdg-logo" style="--sdg-i:{i}">'
            f'<img src="{prefix}{src}" width="{wh}" height="{wh}" loading="lazy" decoding="async" alt="{esc(alt)}">'
            f'</span>'
        )
    return f'<div class="sdg-icons">{"".join(bits)}</div>'


def _strip_rainbow_goals(html):
    """Drop the seven UN rainbow tiles. Leave every other image alone."""
    def repl_section(m):
        block = m.group(0)
        if not _RAINBOW_GOAL_IMG.search(block):
            return block
        cleaned = _RAINBOW_GOAL_IMG.sub('', block)
        text = re.sub(r'<[^>]+>', '', cleaned)
        text = re.sub(r'&nbsp;|\s+', '', text)
        return '' if not text else cleaned
    html = re.sub(r'<section\b[^>]*>.*?</section>', repl_section, html, flags=re.S | re.I)
    return _RAINBOW_GOAL_IMG.sub('', html)


def _merge_goal_lists(html):
    """One ordered list so the seven goals number 1–7, not 1, 1, 1…"""
    matches = list(_GOAL_OL.finditer(html))
    if len(matches) < 2:
        return html
    runs, run = [], [matches[0]]
    for prev, cur in zip(matches, matches[1:]):
        if html[prev.end():cur.start()].strip() == '':
            run.append(cur)
        else:
            runs.append(run)
            run = [cur]
    runs.append(run)
    run = max(runs, key=len)
    if len(run) < 2:
        return html
    items = ''.join(f'<li>{m.group(1)}{m.group(2) or ""}</li>' for m in run)
    start, end = run[0].start(), run[-1].end()
    return html[:start] + f'<ol class="sdg-goals">{items}</ol>' + html[end:]


def _drop_sdg_icons(html):
    """Remove a previous .sdg-icons block, including its nested tiles."""
    key = '<div class="sdg-icons">'
    i = html.find(key)
    if i < 0:
        return html
    j, depth = i + len(key), 1
    while j < len(html) and depth:
        nxt_o = html.find('<div', j)
        nxt_c = html.find('</div>', j)
        if nxt_c < 0:
            return html
        if nxt_o != -1 and nxt_o < nxt_c:
            depth += 1
            j = nxt_o + 4
        else:
            depth -= 1
            j = nxt_c + len('</div>')
    return html[:i] + html[j:]


def finish_sdg_html(html, lang, prefix='../'):
    """Original UN tiles (teal field) + a single 1–7 list. Body copy stays verbatim."""
    html = _drop_sdg_icons(_merge_goal_lists(_strip_rainbow_goals(html)))
    icons = sdg_icons(lang, prefix)
    m = _GOAL_HEAD.search(html)
    if m:
        return html[:m.end()] + icons + html[m.end():]
    m = re.search(r'<ol class="sdg-goals">', html)
    if m:
        return html[:m.start()] + icons + html[m.start():]
    return icons + html


def _sdg_sections(p, bl):
    """Build section HTML fragments from /توسعه-پایدار/ blocks (verbatim)."""
    parts = []
    first = True
    i = 0
    for sid, bs in secs(bl):
        h = next((b['text'] for b in bs if b['t'] == 'h'), '')
        body = ''.join(rewrite_html(b['html'], p) for b in bs if b['t'] == 'html')
        tag = 'h2' if first else 'h3'
        size = '1.5rem' if first else '1.25rem'
        parts.append(
            f'<div class="reveal" style="margin-top:34px;--i:{i}">'
            f'<{tag} style="font-size:{size};line-height:1.35;margin-bottom:12px">{esc(h)}</{tag}>'
            f'<div class="prose">{body}</div></div>'
        )
        first = False
        i += 1
    return finish_sdg_html(''.join(parts), 'fa', p)


def sdgs(write):
    """FA توسعه پایدار — commitment page (old /توسعه-پایدار/)."""
    p = '../'
    bl = B('/توسعه-پایدار/')
    body = _sdg_sections(p, bl)
    lead = next((strip_tags(b['html']) for b in bl if b['t'] == 'html'), '')
    main = f'''{page_hero(p, [('توسعه پایدار', None)], 'توسعه پایدار', esc(lead), mark='sustainable')}
  <section class="section sdg-page" id="sdg"><div class="wrap" style="max-width:980px">
    {body}
  </div></section>'''
    write('sdgs/index.html', page(p, 'sdgs', 'توسعه پایدار',
          'سند تعهد شرکت دانش‌بنیان مخازن طبی آبادیس به اهداف توسعه پایدار سازمان ملل (UN SDGs)',
          main, fa_path='sdgs/'))
    redir = (
        '<!DOCTYPE html><html lang="{lang}" dir="{direction}"><head><meta charset="utf-8">'
        '<meta name="robots" content="noindex,nofollow">'
        '<link rel="canonical" href="{canon}">'
        '<meta http-equiv="refresh" content="0; url={url}">'
        '<title>{title}</title></head><body><p><a href="{url}">{title}</a></p>'
        '<script>location.replace("{url}")</script></body></html>'
    )
    write('sustainability/index.html', redir.format(
        lang='fa', direction='rtl', canon='https://abadis-med.com/sdgs/', url='../sdgs/', title='توسعه پایدار'))
    write('en/sustainability/index.html', redir.format(
        lang='en', direction='ltr', canon='https://abadis-med.com/en/sdgs/', url='../sdgs/', title='SDGs'))
    write('arabic/sustainability/index.html', redir.format(
        lang='ar', direction='rtl', canon='https://abadis-med.com/sdgs/', url='../../sdgs/', title='التنمية المستدامة'))


# ------------------------------------------------------------------ CSR (Zagros hand-built + مسئولیت اجتماعی / SDG summary blocks)
def csr(write):
    p = '../'
    soc = B('/مسئولیت-اجتماعی/')
    acts = []
    videos = {'1290544': ('P1YTe', 'فعالیت های مخازن طبی آبادیس در بحران کرونا'), '875d853': ('sSfGv', 'جشن روز پرستار')}
    for sid, bs in secs(soc):
        if sid == '736e771': continue      # Zagros: already the main story of this page
        h = next((b for b in bs if b['t'] == 'h'), None)
        if not h: continue
        tag = 'h2'
        body = ''.join(rewrite_html(b['html'], p) for b in bs if b['t'] == 'html' and b.get('html'))
        vid = aparat(*videos[sid]) if sid in videos else ''
        imgs = [b for b in bs if b['t'] == 'img']
        gal = [i for b in bs if b['t'] == 'gallery' for i in b['imgs']]
        g = ''.join(gallery_link(p, i['src'], 'g' + sid, i.get('alt', '')) for i in gal) + ''.join(gallery_link(p, (i.get('href') or i['src']) if (i.get('href') or '').endswith(('.jpg', '.png')) else i['src'], 'g' + sid, i.get('alt', '')) for i in imgs)
        cls = 'photo-grid tall contain' if sid == '55cd337' else 'photo-grid'
        acts.append(f'<div class="reveal" style="margin-top:40px"><{tag} style="font-size:1.4rem;margin-bottom:12px">{esc(h["text"])}</{tag}><div class="prose">{body}</div>{vid}{f"<div class={chr(34)}{cls}{chr(34)}>{g}</div>" if g else ""}</div>')
    act_html = f'''  <section class="section" id="activities"><div class="wrap" style="max-width:980px">
    <span class="eyebrow">مسئولیت اجتماعی</span>
    {''.join(acts)}
  </div></section>'''
    f = SITE / 'csr/index.html'; s = f.read_text(encoding='utf-8')
    block = '<!-- phase2:csr -->\n' + act_html + '\n<!-- /phase2:csr -->\n'
    if '<!-- phase2:csr -->' in s: s = re.sub(r'<!-- phase2:csr -->.*?<!-- /phase2:csr -->\n', lambda m: block, s, flags=re.S)
    else: s = s.replace('</main>', block + '</main>', 1)
    if 'id="lightbox"' not in s:
        from layout import LIGHTBOX
        s = s.replace('</main>\n', '</main>\n' + LIGHTBOX + '\n', 1)
    write('csr/index.html', s)

# ------------------------------------------------------------------ contact extras
def contact(write):
    bl = B('/ارتباط-با-ما/')
    def boxes(after):
        out = []; on = False
        for b in bl:
            if b['t'] == 'h': on = (b['text'] == after); continue
            if on and b['t'] == 'box': out.append(f'<div><b>{esc(b["title"])}</b><span>{esc(b["desc"])}</span></div>')
        return ''.join(out)
    office = [b['html'] for b in bl if b['t'] == 'html' and 'داخلی ها' in b['html']][0]
    ext = re.search(r'(<p><strong>داخلی ها:</strong></p>.*)', office, re.S).group(1)
    from icons import (
        svg_clock, svg_pin, svg_postal, ch, iconize_extensions, brand_buttons, social_items,
    )
    ext = iconize_extensions(ext)
    brands = brand_buttons([(url, fn(), label) for url, fn, label, _short in social_items('fa')])
    block = f'''<!-- phase2:contact -->
  <section class="section section--alt" id="hours"><div class="wrap grid g-2" style="gap:24px;align-items:start">
    <div class="reveal"><h2 class="with-ico" style="font-size:1.4rem;margin-bottom:14px">{ch(svg_clock())}ساعات کاری</h2><div class="hours">{boxes('ساعات کاری')}</div>
      <h2 class="with-ico" style="font-size:1.4rem;margin:26px 0 14px">{ch(svg_clock())}روزهای تعطیل</h2><div class="hours">{boxes('روزهای تعطیل')}</div></div>
    <div class="card prose reveal"><h3 class="with-ico">{ch(svg_pin())}دفتر مرکزی</h3>{ext}<h3 class="with-ico">{ch(svg_pin())}کارخانه</h3><p class="with-ico">{ch(svg_postal())}<strong>کدپستی: </strong>۱۸۳۴۱۶۵۷۷۶</p><p><strong>شبکه های اجتماعی: </strong><a href="https://yek.link/abadis.med" target="_blank" rel="noopener">https://yek.link/abadis.med</a></p>{brands}</div>
  </div></section>
  <section class="section" id="map"><div class="wrap"><h2 style="font-size:1.4rem;margin-bottom:14px">موقعیت دفتر مرکزی روی نقشه</h2>
    <div class="map-embed reveal"><iframe title="نقشه دفتر مرکزی آبادیس (نشان)" src="https://neshan.org/maps/iframe/places/9399a4513b6974a287127c06bd9269b9#c35.799-51.448-20z-0p/35.79866645611763/51.44826324948928" loading="lazy" allowfullscreen></iframe></div>
    <p class="map-links"><a href="https://neshan.org/maps/places/9399a4513b6974a287127c06bd9269b9" target="_blank" rel="noopener">مسیریابی با نشان</a> · <a href="https://www.google.com/maps/search/?api=1&amp;query=35.79866,51.44826" target="_blank" rel="noopener">Google Maps</a> · <a href="https://waze.com/ul?ll=35.79866,51.44826&amp;navigate=yes" target="_blank" rel="noopener">Waze</a></p>
  </div></section>
<!-- /phase2:contact -->
'''
    f = SITE / 'contact/index.html'; s = f.read_text(encoding='utf-8')
    if '<!-- phase2:contact -->' in s: s = re.sub(r'<!-- phase2:contact -->.*?<!-- /phase2:contact -->\n', lambda m: block, s, flags=re.S)
    else: s = s.replace('</main>', block + '</main>', 1)
    write('contact/index.html', s)

CUST_T = {
 'fa': dict(h='خانواده سبز آبادیس', lead='۱٬۲۴۲ بیمارستان و ۴۲ مرکز جراحی روی نقشه و در جدول.'),
 'en': dict(h='Abadis green family', lead='1,242 hospitals and 42 surgery centers on the map and in the table.'),
 'ar': dict(h='عائلة آباديس الخضراء', lead='١٬٢٤٢ مستشفى و٤٢ مركز جراحة على الخريطة وفي الجدول.'),
}
def iran_centers_section(p, lang):
    """Live default: the cleaned workbook (1,242 hospitals + 42 surgery centers)."""
    T = CUST_T[lang]
    return f'''<section class="section" id="green-family">
  <div class="wrap">
    <div class="section-head reveal"><h2>{esc(T["h"])}</h2><p>{esc(T["lead"])}</p></div>
    <div data-iran-centers data-src="{p}assets/data/iran-hospitals-centers.json" data-map="{p}assets/data/iran-provinces.json" data-lang="{lang}"></div>
  </div>
</section>
<script src="{p}assets/js/iran-centers.js" defer></script>'''


def customers_all(lang='fa', p='../'):
    return iran_centers_section(p, lang)

# ------------------------------------------------------------------ customers
def customers(write):
    p = '../'; bl = B('/مشتریان-ما/')
    head = bl[0]['text']; items = bl[1]['items']
    cards = []; nimg = 0
    for it in items:
        im = next((x for x in it['blocks'] if x['t'] == 'img'), None)
        name = next((x['text'] for x in it['blocks'] if x['t'] == 'h'), '')
        bt = next((x for x in it['blocks'] if x['t'] == 'btn'), None)
        pic = picture(p, im['src'], im.get('alt') or name, 300) if im else ''
        nimg += bool(pic)
        lg = f'<div class="lg">{pic}</div>' if pic else f'<div class="lg txt" aria-hidden="true">{esc(re.sub(r"^(بیمارستان|مرکز|درمانگاه|کلینیک)\s+", "", name)[:1])}</div>'
        link = f'<a href="{esc(bt["href"])}" target="_blank" rel="noopener">{esc(bt["text"])}</a>' if bt and bt.get('href') else ''
        cards.append(f'<div class="logo-card" data-name="{esc(name)}">{lg}<strong>{esc(name)}</strong>{link}</div>')
    main = f'''{page_hero(p, [('خانواده سبز آبادیس', None)], 'خانواده سبز <em>آبادیس</em>', 'همراهی بیش از ۱٬۲۸۴ مرکز درمانی در سراسر ایران — ۱٬۲۴۲ بیمارستان و ۴۲ مرکز جراحی در ۳۱ استان کشور')}
  {customers_all('fa', p)}
  <section class="section section--alt" id="featured-logos"><div class="wrap">
    <div class="section-head reveal"><h2>مراکز درمانی منتخب با نشان و پیوند مستقیم</h2><p>{esc(head)}</p></div>
    <div class="list-tools"><input class="search" type="search" placeholder="جستجوی نام مرکز درمانی..." aria-label="جستجوی مشتریان" data-filter="#custGrid"><span class="count" data-count-for="#custGrid">{fa(len(items))} مرکز درمانی</span></div>
    <div class="logo-grid" id="custGrid" data-paged="12">{''.join(cards)}</div>
    <p class="empty-msg" hidden>موردی یافت نشد.</p>
  </div></section>'''
    write('customers/index.html', page(p, 'customers', 'خانواده سبز آبادیس', head, main))
    for rel, prefix, lang, title, desc in (
        ('green-family-map/index.html', '../', 'fa', 'خانواده سبز آبادیس', 'نقشه و فهرست بیمارستان‌ها و مراکز جراحی.'),
        ('en/green-family-map/index.html', '../../', 'en', 'Abadis green family', 'Map and list of hospitals and surgery centers.'),
        ('arabic/green-family-map/index.html', '../../', 'ar', 'عائلة آباديس الخضراء', 'خريطة وقائمة المستشفيات ومراكز الجراحة.'),
    ):
        body = f'''{page_hero(prefix, [(title, None)], title, esc(desc), lang=lang)}
  {iran_centers_section(prefix, lang)}'''
        write(rel, page(prefix, 'customers', title, desc, body, lang=lang, fa_path='customers/'))
    return len(items), nimg

# ------------------------------------------------------------------ academy (was «تجارب ما»)
ACADEMY_MARK = '<svg viewBox="0 0 40 40" aria-hidden="true" width="34" height="34"><rect x="2" y="2" width="36" height="36" rx="11" fill="#066163"/><path d="M8 17l12-6 12 6-12 6z" fill="#fff"/><path d="M13 20v6c0 2 3.5 4 7 4s7-2 7-4v-6" fill="none" stroke="#fff" stroke-width="2.2"/><path d="M32 17v7" stroke="#bfe3e2" stroke-width="2.2" stroke-linecap="round"/></svg>'
AC_COPY = {
    'fa': dict(brand='آکادمی آبادیس', back='سایت آبادیس', lock='محتوای تأییدشده — فقط خواندنی',
               h1='آکادمی آبادیس', lead='درگاه سه‌مرحله‌ای آموزش، استخدام و گروه‌های شغلی. بازدید فقط‌خواندنی است.',
               all='همه', p1='فاز ۱ — استقرار', p2='فاز ۲ — استخدام و آزمون‌ها', p3='فاز ۳ — تگ‌ها و گروه‌های شغلی هوشمند',
               ind='صنعتی — مبتنی بر تجربه', hr='داخلی — آموزش HR ویژن',
               mods=[
                   ('field', 'ماژول‌های بالینی و میدانی'),
                   ('field', 'مطالعات موردی بیمارستانی'),
                   ('field', 'عیب‌یابی دستگاه'),
                   ('field', 'راهنمای میدانی کنترل عفونت'),
                   ('hr', 'شرح شغل'),
                   ('hr', 'ویدیوی آشنایی و آموزش بدو ورود'),
                   ('hr', 'پایگاه دانش فنی داخلی'),
                   ('hire', 'آزمون فنی و شغلی'),
                   ('hire', 'پیش‌نمایش MBTI'),
                   ('hire', 'پیش‌نمایش گردش‌کار مصاحبه هوش مصنوعی'),
                   ('tag', 'تگ محتوا'),
                   ('tag', 'تگ شغلی هوش مصنوعی'),
                   ('tag', 'فیلتر گروه‌های شغلی روی دوره، ویدیو و ارزیابی'),
               ]),
    'en': dict(brand='Abadis Academy', back='Abadis site', lock='Verified content — read only',
               h1='Abadis Academy', lead='A three-phase portal for training, hiring and job groups. Visitors can only read.',
               all='All', p1='Phase 1 — Rollout', p2='Phase 2 — Hiring and exams', p3='Phase 3 — Smart tags and job groups',
               ind='Industrial — from field experience', hr='Internal — Vision HR training',
               mods=[
                   ('field', 'Clinical and field modules'),
                   ('field', 'Hospital case studies'),
                   ('field', 'Device troubleshooting'),
                   ('field', 'Infection-control field guides'),
                   ('hr', 'Job descriptions'),
                   ('hr', 'Onboarding and training videos'),
                   ('hr', 'Internal technical knowledge base'),
                   ('hire', 'Technical and role exams'),
                   ('hire', 'MBTI preview'),
                   ('hire', 'AI interview workflow preview'),
                   ('tag', 'Content tags'),
                   ('tag', 'AI job tags'),
                   ('tag', 'Job groups filtering courses, videos and assessments'),
               ]),
    'ar': dict(brand='أكاديمية آباديس', back='موقع آباديس', lock='محتوى موثّق — للقراءة فقط',
               h1='أكاديمية آباديس', lead='بوابة من ثلاث مراحل للتدريب والتوظيف ومجموعات العمل. الزيارة للقراءة فقط.',
               all='الكل', p1='المرحلة ١ — الاستقرار', p2='المرحلة ٢ — التوظيف والاختبارات', p3='المرحلة ٣ — الوسوم ومجموعات العمل الذكية',
               ind='صناعي — مبني على الخبرة', hr='داخلي — تدريب الموارد البشرية',
               mods=[
                   ('field', 'وحدات سريرية وميدانية'),
                   ('field', 'دراسات حالة للمستشفيات'),
                   ('field', 'استكشاف أعطال الأجهزة'),
                   ('field', 'أدلة ميدانية لمكافحة العدوى'),
                   ('hr', 'الوصف الوظيفي'),
                   ('hr', 'فيديو التهيئة والتدريب'),
                   ('hr', 'قاعدة المعرفة الفنية الداخلية'),
                   ('hire', 'اختبارات فنية ووظيفية'),
                   ('hire', 'معاينة MBTI'),
                   ('hire', 'معاينة مسار مقابلة الذكاء الاصطناعي'),
                   ('tag', 'وسوم المحتوى'),
                   ('tag', 'وسوم وظيفية بالذكاء الاصطناعي'),
                   ('tag', 'تصفية مجموعات العمل للدورات والفيديو والتقييم'),
               ]),
}

def _academy_shell(html, p, lang):
    t = AC_COPY[lang]
    head = f'''<header class="ac-header" data-tone="light"><div class="wrap ac-bar">
    <a class="ac-brand" href="{p}academy/">{ACADEMY_MARK}<span><b>{esc(t["brand"])}</b><small>Abadis Academy</small></span></a>
    <div class="ac-cta"><span class="ac-lock">{esc(t["lock"])}</span><a class="ac-back" href="{p}">{esc(t["back"])}</a></div>
  </div></header>'''
    foot = f'''<footer class="ac-footer"><div class="wrap"><span>{ACADEMY_MARK} {esc(t["brand"])}</span><span class="ac-lock">{esc(t["lock"])}</span></div></footer>'''
    html = re.sub(r'<header class="header" id="header">.*?</header>', lambda m: head, html, count=1, flags=re.S)
    html = re.sub(r'<footer.*?</footer>', lambda m: foot, html, count=1, flags=re.S)
    return html.replace('<body>', '<body class="academy">', 1)

def _academy_main(p, lang, stories):
    t = AC_COPY[lang]
    mods = ''.join(
        f'<article class="ac-card ac-mod" data-ac-mod="{k}"><h3>{esc(label)}</h3></article>'
        for k, label in t['mods'])
    phases = (
        f'<section class="ac-phase" id="phase-1"><h2>{esc(t["p1"])}</h2>'
        f'<p class="eyebrow">{esc(t["ind"])}</p><p class="eyebrow">{esc(t["hr"])}</p>'
        f'<div class="ac-grid ac-grid--2" id="experiences">{stories}</div></section>'
        f'<section class="ac-phase" id="phase-2"><h2>{esc(t["p2"])}</h2></section>'
        f'<section class="ac-phase" id="phase-3"><h2>{esc(t["p3"])}</h2></section>'
    )
    filters = ''.join(
        f'<button type="button" data-ac-filter="{k}" aria-pressed="{"true" if k == "all" else "false"}">{esc(lab)}</button>'
        for k, lab in (('all', t['all']), ('field', t['ind']), ('hr', t['hr']), ('hire', t['p2']), ('tag', t['p3'])))
    script = '''<script>(function(){document.querySelectorAll("[data-ac-filter]").forEach(function(btn){btn.addEventListener("click",function(){var key=btn.getAttribute("data-ac-filter");btn.parentElement.querySelectorAll("button").forEach(function(b){b.setAttribute("aria-pressed",b===btn?"true":"false");});document.querySelectorAll("[data-ac-mod]").forEach(function(el){el.hidden=key!=="all"&&el.getAttribute("data-ac-mod")!==key;});});});})();</script>'''
    return f'''<main id="main">
  <section class="ac-hero"><div class="wrap">
    <p class="ac-lock">{esc(t["lock"])}</p>
    <h1>{esc(t["h1"])}</h1>
    <p class="ac-lead">{esc(t["lead"])}</p>
  </div></section>
  <section class="section" id="phases"><div class="wrap">
    <div class="ac-filters" role="group">{filters}</div>
    <div class="ac-grid">{mods}</div>
    <div class="ac-phases">{phases}</div>
  </div></section>
</main>
{script}'''

def experiences(write):
    bl = B('/تجارب-ما/')
    cards = []; cur = None
    for b in bl:
        if b['t'] == 'h':
            cur = [b['text'], '']; cards.append(cur)
        elif b['t'] == 'html' and cur:
            cur[1] += rewrite_html(b['html'], '../')
    stories = ''.join(
        f'<article class="ac-card ac-exp" lang="fa" dir="rtl"><h3>{esc(t)}</h3><div class="prose">{h}</div></article>'
        for t, h in cards)
    specs = (
        ('academy/index.html', '../', 'fa', ''),
        ('en/academy/index.html', '../../', 'en', 'en/'),
        ('arabic/academy/index.html', '../../', 'ar', 'arabic/'),
    )
    for rel, p, lang, fa_path in specs:
        t = AC_COPY[lang]
        main = _academy_main(p, lang, stories)
        html = page(p, 'experiences', t['h1'], t['lead'], main, lang=lang, fa_path='academy/')
        html = re.sub(r'<main id="main">\s*<main id="main">', '<main id="main">', html).replace('</main>\n</main>', '</main>')
        write(rel, _academy_shell(html, p, lang))
        login = (f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8">'
                 f'<meta name="robots" content="noindex,nofollow"><meta http-equiv="refresh" content="0; url=../">'
                 f'<title>{esc(t["h1"])}</title></head><body><p><a href="../">{esc(t["h1"])}</a></p>'
                 f'<script>location.replace("../")</script></body></html>')
        write(rel.replace('index.html', 'login/index.html'), login)
    stub = '<!doctype html><html lang="fa" dir="rtl"><head><meta charset="utf-8"><meta name="robots" content="noindex,nofollow"><link rel="canonical" href="../academy/"><meta http-equiv="refresh" content="0; url=../academy/#experiences"><title>آکادمی آبادیس</title></head><body><p><a href="../academy/#experiences">آکادمی آبادیس</a></p><script>location.replace("../academy/#experiences")</script></body></html>'
    write('experiences/index.html', stub)

# ------------------------------------------------------------------ downloads
def downloads(write):
    p = '../'; bl = B('/کاتالوگ/')
    items = next(b for b in bl if b['t'] == 'listing')['items']
    cards = []
    for it in items:
        im = next((x for x in it['blocks'] if x['t'] == 'img'), None)
        title = next((x['text'] for x in it['blocks'] if x['t'] == 'h'), '')
        bt = next((x for x in it['blocks'] if x['t'] == 'btn'), None)
        pic = picture(p, im['src'], title, 600) if im else ''
        ph = f'<div class="ph">{pic}</div>' if pic else f'<div class="ph txt"><img src="{p}assets/img/abadis-logo-teal.png" width="658" height="309" alt=""></div>'
        cards.append(f'<a class="post-card dl-card reveal" href="{esc(bt["href"])}" target="_blank" rel="noopener">{ph.replace("class=\"ph\"", "class=\"ph\" style=\"aspect-ratio:1;background:#fff\"")}<div class="body"><h3>{esc(title)}</h3><span class="go">{esc(bt["text"])} (PDF) ↓</span></div></a>')
    main = f'''{page_hero(p, [('مرکز دانلود', None)], 'مرکز دانلود', 'کاتالوگ‌ها و راهنماهای محصولات مخازن طبی آبادیس')}
  <section class="section"><div class="wrap"><div class="post-grid">{''.join(cards)}</div>
  <p class="note" style="margin-top:20px">فایل‌ها مستقیماً از سرور abadis-med.com دریافت می‌شوند.</p></div></section>'''
    write('downloads/index.html', page(p, 'downloads', 'مرکز دانلود', 'دانلود کاتالوگ محصولات مخازن طبی آبادیس', main))
    return len(items)

# ------------------------------------------------------------------ install guide (hub + 2)
def install(write):
    p = '../'; bl = B('/راهنمای-نصب/')
    imgs = [b for b in bl if b['t'] == 'img']
    hs = [b for b in bl if b['t'] == 'h']
    targets = ['tanks/', 'end-user/']
    cards = ''.join(f'<a class="pcard reveal" href="{targets[i]}"><div class="ph">{picture(p, imgs[i]["src"], hs[i]["text"], 700)}</div><strong>{esc(hs[i]["text"])}</strong><span class="go">مشاهده راهنما ←</span></a>' for i in range(2))
    side = picture(p, imgs[2]['src'], 'نصب مخازن آبادیس', 700) if len(imgs) > 2 else ''
    main = f'''{page_hero(p, [('راهنمای نصب', None)], 'راهنمای نصب')}
  <section class="section"><div class="wrap install-hub" style="display:grid;grid-template-columns:2fr 1fr;gap:18px;align-items:start">
    <div class="grid g-2">{cards}</div>
    {f'<div class="media-frame reveal" style="border-radius:20px;overflow:hidden">{side}</div>' if side else ''}
  </div></section>
  <section class="section" style="padding-top:0"><div class="wrap"><div class="doc-links"><a href="../faq/">پرسش های متداول</a><a href="../downloads/">مرکز دانلود</a><a href="../products/">محصولات</a></div></div></section>'''
    write('install-guide/index.html', page(p, 'install', 'راهنمای نصب', 'راهنمای نصب مخازن و راهنمای استفاده کاربر نهایی کیسه‌های ساکشن آبادیس', main))
    # tanks
    p = '../../'; bl = B('/راهنمای-نصب/راهنمای-نصب-مخازن/')
    blocks = []; anchors = []
    for sid, bs in secs(bl):
        tabs = next((b for b in bs if b['t'] == 'tabs'), None)
        if not tabs: continue
        h = next(b['text'] for b in bs if b['t'] == 'h')
        aid = f'g{len(blocks)+1}'; anchors.append(f'<a href="#{aid}">{esc(h)}</a>')
        steps = []
        for t in tabs['tabs']:
            pics = ''.join(gallery_link(p, x, aid, t['title'], 700, 1200) for x in t.get('imgs', []))
            steps.append(f'<div class="step reveal">{f"<div class=ph>{pics}</div>" if pics else ""}<div class="tx"><b>{esc(t["title"])}</b>{rewrite_html(t["html"], p)}</div></div>')
        blocks.append(f'<div class="guide-block" id="{aid}"><h2 class="reveal" style="margin-bottom:16px">{esc(h)}</h2><div class="steps">{"".join(steps)}</div></div>')
    main = f'''{page_hero(p, [('راهنمای نصب', '../'), ('راهنمای نصب مخازن', None)], 'راهنمای نصب مخازن')}
  <nav class="anchors" aria-label="بخش‌های صفحه"><div class="wrap">{''.join(anchors)}</div></nav>
  <section class="section"><div class="wrap">{''.join(blocks)}</div></section>'''
    write('install-guide/tanks/index.html', page(p, 'install', 'راهنمای نصب مخازن', 'نحوه نصب مخازن ساکشن آبادیس بر روی پایه پرتابل، کنسول و پایه ترولی', main, lightbox=True))
    # end user
    vids = [('پرتابل', 'LiEf2'), ('تکی', 'Nc7hg'), ('سری', 'Yp2bl')]
    cards = ''.join(f'<div class="reveal"><h2 style="font-size:1.3rem;margin-bottom:12px">{t}</h2>{aparat(c, "راهنمای استفاده کاربر نهایی — " + t)}</div>' for t, c in vids)
    main = f'''{page_hero(p, [('راهنمای نصب', '../'), ('راهنمای استفاده کاربر نهایی', None)], 'راهنمای استفاده کاربر نهایی')}
  <section class="section"><div class="wrap grid g-3" style="gap:20px">{cards}</div>
  <div class="wrap"><p class="note" style="margin-top:18px">ویدیوها از آپارات آبادیس بارگذاری می‌شوند.</p></div></section>'''
    write('install-guide/end-user/index.html', page(p, 'install', 'راهنمای استفاده کاربر نهایی', 'ویدیوهای راهنمای استفاده کاربر نهایی کیسه ساکشن آبادیس: پرتابل، تکی و سری', main))

# ------------------------------------------------------------------ FAQ
def faq(write):
    p = '../'; bl = B('/پرسش-های-متداول/')
    groups = []; cur = None
    for b in bl:
        if b['t'] == 'h' and b['lvl'] == 2: cur = b['text']
        elif b['t'] == 'faq': groups.append((cur, b['items']))
    body = ''.join(f'<div class="faq-group reveal"><h2>{esc(t)}</h2>{faq_list(items, p)}</div>' for t, items in groups)
    nav = ''.join(f'<a href="#f{i}">{esc(t)}</a>' for i, (t, _) in enumerate(groups))
    body = ''.join(f'<div class="faq-group reveal" id="f{i}"><h2>{esc(t)}</h2>{faq_list(items, p)}</div>' for i, (t, items) in enumerate(groups))
    main = f'''{page_hero(p, [('پرسش های متداول', None)], 'پرسش های متداول')}
  <nav class="anchors" aria-label="بخش‌های صفحه"><div class="wrap">{nav}</div></nav>
  <section class="section"><div class="wrap" style="max-width:900px">{body}</div></section>'''
    write('faq/index.html', page(p, 'faq', 'پرسش های متداول', 'پرسش های متداول درباره محصولات، باربری، سفارش و نصب مخازن طبی آبادیس', main))

# ------------------------------------------------------------------ careers + jobs
JOB_SLUGS = {'منشی': 'secretary', 'کارشناس تحقیق و توسعه': 'rnd-specialist', 'کارشناس فروش': 'sales-specialist',
             'کارشناس صادرات': 'export-specialist', 'کارشناس تحقیقات بازار': 'market-research', 'کارشناس تضمین کیفیت': 'quality-assurance',
             'مدیر فروش': 'sales-manager', 'کارشناس حسابداری': 'accountant', 'کارمند وصول مطالبات': 'collections-officer'}
FORM_TITLES = 'مدیرعامل مدیر فروش مدیر بازرگانی مدیر حسابداری مدیر مالی مدیر منابع انسانی مدیر محصول مدیر کارخانه سرپرست فنی کارخانه حسابداری ارشد حسابداری فروش کارشناس فروش انباردار اپراتور دستگاه تزریق کارشناس دستگاه تزریق تحصیلدار کارشناس نصب و راه اندازی کارشناس پشتیبان فروش مسئول دفتر منشی کارمند وصول'
FORM_OPTS = ['مدیرعامل', 'مدیر فروش', 'مدیر بازرگانی', 'مدیر حسابداری', 'مدیر مالی', 'مدیر منابع انسانی', 'مدیر محصول', 'مدیر کارخانه', 'سرپرست فنی کارخانه',
             'حسابداری ارشد', 'حسابداری فروش', 'کارشناس فروش', 'انباردار', 'اپراتور دستگاه تزریق', 'کارشناس دستگاه تزریق', 'تحصیلدار',
             'کارشناس نصب و راه اندازی', 'کارشناس پشتیبان فروش', 'مسئول دفتر', 'منشی', 'کارمند وصول']
# List columns from live Gravity Form #2 (فرصت های همکاری), WP REST 2026-10-06 — no file upload field.
EDU_COLS = ['مقطع تحصیلی', 'نام موسسه آموزشی', 'نوع مدرک آموزشی', 'نام گرایش یا رشته', 'زمان آموزش (شروع - خاتمه)', 'معدل']
WORK_COLS = ['نام سازمان', 'عنوان شغل', 'مدت همکاری(شروع-خاتمه)', 'آخرین دریافتی', 'نام مدیر', 'تلفن تماس', 'علت قطع همکاری']
EXPECT_COLS = ['امنیت شغلی', 'محیط آرام', 'همکاران', 'نزدیکی محل', 'پیشرفت شغلی', 'مرتبط با تحصیلات', 'درآمد', 'پرستیژ']
COMPUTER_COLS = ['نوع نرم افزار', 'میزان آشنایی (متوسط-خوب-عالی)', 'توضیحات']
LANG_OPTS = ['انگلیسی', 'آلمانی', 'اسپانیایی', 'سایر زبان ها']

def _list_field(title, prefix, cols, required=True, note=''):
    req = ' required' if required else ''
    cells = ''.join(
        f'<label>{esc(c)}<input name="{esc(prefix)} — {esc(c)}" autocomplete="off"{req}></label>'
        for c in cols
    )
    note_h = f'<p class="note">{esc(note)}</p>' if note else ''
    return f'''<div class="list-field" data-list-field>
        <h3 class="form-block-title">{esc(title)}{" *" if required else ""}</h3>
        {note_h}
        <div class="list-rows"><div class="list-row grid g-2" style="gap:12px">{cells}</div></div>
        <button type="button" class="btn btn-ghost list-add" data-list-add>افزودن ردیف</button>
      </div>'''

TODAY_J = '1405/07/22'   # build date (Jalali) for active/expired badges

def _active(j):
    return j['exp'] >= TODAY_J

CAREERS_ART = '''<svg class="careers-art" viewBox="0 0 320 220" role="img" aria-label="تیم آبادیس">
  <defs><linearGradient id="cg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0e7475"/><stop offset="1" stop-color="#015F61"/></linearGradient></defs>
  <rect x="18" y="26" width="284" height="170" rx="26" fill="url(#cg)" opacity=".12"/>
  <g fill="none" stroke="#066163" stroke-width="5" stroke-linecap="round" stroke-linejoin="round">
    <rect x="112" y="92" width="96" height="70" rx="12" fill="#e8f3f3"/>
    <path d="M140 92v-12a8 8 0 0 1 8-8h24a8 8 0 0 1 8 8v12"/><path d="M112 120h96"/><circle cx="160" cy="122" r="6" fill="#066163"/>
  </g>
  <g fill="#087673"><circle cx="66" cy="96" r="18"/><path d="M36 160c4-24 18-36 30-36s26 12 30 36z"/>
    <circle cx="254" cy="96" r="18"/><path d="M224 160c4-24 18-36 30-36s26 12 30 36z"/></g>
  <g stroke="#0e7475" stroke-width="3" stroke-dasharray="4 7" fill="none"><path d="M90 104q35-34 70-28"/><path d="M230 104q-35-34-70-28"/></g>
</svg>'''

def _job_cards(p_jobs_prefix, jobs):
    """Fixed job-post card template: title, status badge, dates, link."""
    out = []
    for j in jobs:
        act = _active(j)
        badge = '<span class="badge-act">فعال</span>' if act else '<span class="badge-exp">منقضی شده</span>'
        out.append(
            f'''<article class="card job{' job--active' if act else ''} reveal"><div class="job-top"><h3>{esc(j["title"])}</h3>{badge}</div>'''
            f'''<span class="dates">تاریخ انتشار: {fa(j["pub"])} · تاریخ انقضاء: {fa(j["exp"])}</span>'''
            f'''<a class="more-link" href="{p_jobs_prefix}{JOB_SLUGS[j["title"]]}/">مشاهده موقعیت ←</a></article>''')
    return ''.join(out)


def _job_sections(h):
    """Split a post into the fixed template sections (heading lines that end in ':')."""
    parts = re.split(r'<p>\s*([^<]{2,40}?)\s*[:：]\s*</p>', h)
    if len(parts) < 3:
        return f'<div class="job-sec prose">{h}</div>'
    out = [f'<div class="job-sec prose">{parts[0]}</div>'] if strip_tags(parts[0]).strip() else []
    for i in range(1, len(parts), 2):
        body = parts[i + 1]
        if '<li' not in body:   # one requirement per <p> → list
            items = re.findall(r'<p>(.*?)</p>', body, re.S)
            body = '<ul>' + ''.join(f'<li>{x}</li>' for x in items) + '</ul>' if items else body
        out.append(f'<section class="job-sec"><h2>{esc(parts[i])}</h2><div class="prose">{body}</div></section>')
    return ''.join(out)


def jobs_page(write):
    """Old موقعیت‌های شغلی URL → merged into فرصت‌های همکاری (static redirect stub)."""
    html = ('''<!DOCTYPE html><html lang="fa" dir="rtl"><head><meta charset="utf-8">
<title>فرصت‌های همکاری — مخازن طبی آبادیس</title><meta name="robots" content="noindex">
<link rel="canonical" href="https://abadis-med.com/careers/"><meta http-equiv="refresh" content="0; url=../careers/#jobs">
</head><body><p><a href="../careers/#jobs">فرصت‌های همکاری</a></p><script>location.replace('../careers/#jobs')</script></body></html>''')
    write('jobs/index.html', html)


def careers(write):
    jobs = load('jobs.json')
    p = '../'
    cards = _job_cards('jobs/', jobs)
    opts = ''.join(f'<option>{o}</option>' for o in FORM_OPTS)
    assert ' '.join(FORM_OPTS) == FORM_TITLES
    langs = ''.join(
        f'<label class="check"><input type="checkbox" name="زبان‌های خارجی" value="{esc(x)}"> {esc(x)}</label>'
        for x in LANG_OPTS
    )
    expect = ''.join(
        f'<label>{esc(c)}<input type="number" inputmode="numeric" min="1" max="8" name="انتظار از محیط کار — {esc(c)}" required></label>'
        for c in EXPECT_COLS
    )
    edu = _list_field('سوابق تحصیلی', 'سوابق تحصیلی', EDU_COLS, True)
    work = _list_field('سوابق کاری', 'سوابق کاری', WORK_COLS, True,
                       'برای اضافه کردن ردیف روی «افزودن ردیف» کلیک کنید.')
    current = _list_field('شغل فعلی', 'شغل فعلی', WORK_COLS, True,
                          'چنانچه در حال حاضر مشاغل دیگری دارید نسبت به تکمیل این بخش اقدام نمایید.')
    computer = _list_field('آشنایی با کامپیوتر', 'آشنایی با کامپیوتر', COMPUTER_COLS, True,
                           'برای اضافه کردن ردیف روی «افزودن ردیف» کلیک کنید.')
    opts = '<option>ارسال رزومه عمومی / خارج از ردیف‌های شغلی فعلی</option>' + opts
    main = f'''{page_hero(p, [('فرصت‌های شغلی / همکاری با ما', None)], 'فرصت‌های شغلی / همکاری با ما', 'جای شما در آبادیس خالیست...', CAREERS_ART)}
  <section class="section" id="jobs"><div class="wrap">
    <h2 class="reveal" style="margin-bottom:18px">موقعیت‌های شغلی</h2>
    <div class="grid g-3">{cards}</div>
  </div></section>
  <section class="section" id="general-resume"><div class="wrap" style="max-width:860px">
    <article class="card resume-intro reveal">
      <h2>ارسال رزومه عمومی / خارج از ردیف‌های شغلی فعلی</h2>
      <p><a class="btn btn-primary" href="#apply" id="generalResumeCta">ارسال رزومه عمومی / خارج از ردیف‌های شغلی فعلی</a></p>
    </article>
  </div></section>
  <section class="section section--alt" id="apply"><div class="wrap" style="max-width:860px">
    <div class="card reveal">
      <h2 style="font-size:1.4rem;margin-bottom:6px">ثبت درخواست</h2>
      <p class="note form-offline-hint" style="margin-bottom:16px">پیش‌نمایش: این فرم پس از اتصال به سرور سایت فعال می‌شود؛ فعلاً با ارسال، ایمیل آماده به info@abadis-med.com باز می‌شود.</p>
      <form class="form" data-abadis-form="careers" data-mailto-form="info@abadis-med.com" data-subject="ثبت درخواست همکاری">
        <input type="hidden" name="form_name" value="careers">
        <label class="hp-field" aria-hidden="true">Leave blank<input type="text" name="_gotcha" tabindex="-1" autocomplete="off"></label>
        <label>عنوان شغلی *<select name="عنوان شغلی" required><option value="">انتخاب کنید</option>{opts}</select></label>
        <h3 class="form-block-title">مشخصات فردی *</h3>
        <div class="grid g-2" style="gap:12px">
          <label>نام<input name="نام" required autocomplete="given-name"></label>
          <label>نام خانوادگی<input name="نام خانوادگی" required autocomplete="family-name"></label>
          <label>نام پدر<input name="نام پدر" required></label>
          <label>وضعیت نظام وظیفه<input name="وضعیت نظام وظیفه" required></label>
          <label>تاریخ تولد *<input name="تاریخ تولد" placeholder="۱۳۷۰/۰۱/۰۱" required inputmode="numeric"></label>
          <label>محل تولد<input name="محل تولد" required></label>
          <label>شماره شناسنامه<input name="شماره شناسنامه" required inputmode="numeric"></label>
          <label>محل صدور<input name="محل صدور" required></label>
        </div>
        <label>وضعیت تاهل *<select name="وضعیت تاهل" required><option value="">انتخاب کنید</option><option>مجرد</option><option>متاهل</option></select></label>
        <label>آیا بیماری خاص و یا سابقه بستری شدن در بیمارستان دارید؟ *<select name="بیماری خاص یا سابقه بستری" required><option value="">انتخاب کنید</option><option>بلی</option><option>خیر</option></select></label>
        <label>آدرس محل سکونت *<input name="آدرس محل سکونت" required autocomplete="street-address" placeholder="لطفا نشانی کامل محل سکونت خود را وارد نمایید."></label>
        <div class="grid g-2" style="gap:12px">
          <label>تلفن ثابت *<input name="تلفن ثابت" type="tel" dir="ltr" required inputmode="tel" autocomplete="tel-national"></label>
          <label>تلفن همراه *<input name="تلفن همراه" type="tel" dir="ltr" required inputmode="tel" autocomplete="tel"></label>
        </div>
        {edu}
        {work}
        <div class="grid g-2" style="gap:12px">
          <label>آخرین حقوق دریافتی *<input name="آخرین حقوق دریافتی" required inputmode="numeric"></label>
          <label>حقوق درخواستی *<input name="حقوق درخواستی" required inputmode="numeric"></label>
        </div>
        <label>طریق مراجعه به شرکت جهت استخدام *<input name="طریق مراجعه به شرکت جهت استخدام" required></label>
        <h3 class="form-block-title">انتظار شما از محیط کارتان چیست؟ (به ترتیب شماره گذاری فرمایید) *</h3>
        <p class="note">به هر مورد عددی از ۱ تا ۸ بدهید (بدون تکرار).</p>
        <div class="grid g-2" style="gap:12px">{expect}</div>
        {current}
        <fieldset class="check-set">
          <legend>آشنایی با زبان های خارجی</legend>
          <div class="check-row">{langs}</div>
        </fieldset>
        {computer}
        <label>در مورد توانایی، مهارت ها و شغل مناسب و ایده آل خود در یک پارا گراف توضیح دهید ؟<textarea name="توانایی و مهارت و شغل ایده‌آل" rows="5"></textarea></label>
        <button class="btn btn-primary" type="submit">ثبت درخواست</button>
        <p class="form-status" role="status" aria-live="polite"></p>
      </form>
    </div>
  </div></section>'''
    html = page(p, 'careers', 'فرصت‌های شغلی / همکاری با ما', 'فرصت های همکاری و موقعیت های شغلی شرکت دانش‌بنیان مخازن طبی آبادیس', main, fa_path='careers/')
    html = html.replace('</body>', '<script>document.getElementById("generalResumeCta")&&document.getElementById("generalResumeCta").addEventListener("click",function(){var s=document.querySelector(\'[name="عنوان شغلی"]\');if(s)s.value="ارسال رزومه عمومی / خارج از ردیف‌های شغلی فعلی";});</script>\n</body>', 1)
    write('careers/index.html', html)
    en_path = SITE / 'en/collaboration-opportunities/index.html'
    if en_path.exists() and 'id="general-resume"' not in en_path.read_text(encoding='utf-8'):
        en_raw = en_path.read_text(encoding='utf-8')
        block = ('<section class="section" id="general-resume"><div class="wrap" style="max-width:860px">'
                 '<article class="card resume-intro"><h2>General résumé submission</h2>'
                 '<p><a class="btn btn-primary" href="#apply">General résumé / outside the current openings</a></p>'
                 '</article></div></section>\n')
        en_raw = en_raw.replace('<section class="section"><div class="wrap prose reveal">', block + '<section class="section"><div class="wrap prose reveal">', 1)
        en_path.write_text(en_raw, encoding='utf-8')
    p = '../../../'
    for j in jobs:
        slug = JOB_SLUGS[j['title']]
        act = _active(j)
        st = 'فعال' if act else 'منقضی شده'
        meta = f'<div class="meta"><span>تاریخ انتشار: {fa(j["pub"])}</span><span>تاریخ انقضاء آگهی: {fa(j["exp"])}</span><span class="{"badge-act" if act else "badge-exp"}">{st}</span></div>'
        facts = (f'<aside class="job-facts card"><dl><dt>عنوان شغلی</dt><dd>{esc(j["title"])}</dd><dt>محل کار</dt><dd>مخازن طبی آبادیس</dd>'
                 f'<dt>وضعیت</dt><dd>{st}</dd><dt>مهلت</dt><dd>{fa(j["exp"])}</dd></dl>'
                 f'<a class="btn btn-primary" href="../../#apply">ثبت درخواست</a></aside>')
        main = f'''{page_hero(p, [('فرصت‌های همکاری', '../../'), (j['title'], None)], esc(j['title']), '', meta)}
  <section class="section"><div class="wrap job-layout">
    <div class="job-body card reveal">{_job_sections(rewrite_html(j['html'], p))}</div>
    {facts}
  </div>
  <div class="wrap"><div class="cta-actions" style="display:flex;gap:12px;flex-wrap:wrap;margin-top:22px"><a class="btn btn-primary" href="../../#apply">ثبت درخواست</a><a class="btn btn-ghost" href="../../#jobs">مشاهده کلیه موقعیت‌های شغلی</a></div></div></section>'''
        write(f'careers/jobs/{slug}/index.html', page(p, 'careers', j['title'], strip_tags(j['html'])[:150], main))

from lib import JOB_MAP
import urllib.parse as _u
for _j in load('jobs.json'):
    JOB_MAP[_u.unquote(_u.urlsplit(_j['url']).path)] = f"careers/jobs/{JOB_SLUGS[_j['title']]}/"
GROUPS = {'about': about, 'dealers': dealers, 'calculator': calculator, 'csr': csr, 'sdgs': sdgs,
          'contact': contact, 'customers': customers, 'experiences': experiences, 'downloads': downloads,
          'install': install, 'faq': faq, 'careers': careers, 'jobs': jobs_page}
