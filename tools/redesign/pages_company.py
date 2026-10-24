"""About, dealers, contact extras, CSR/SDG extras, calculator, and footer pages."""
import re, json, urllib.parse
from lib import PAGES, SITE, esc, strip_tags, best_img, rewrite_html, href, fa, load
from layout import page, page_hero
from render import picture, gallery_link, table, faq_list, aparat, secs, blocks_to_prose

def B(path): return PAGES[path]['blocks']
def ext_attr(ext): return ' target="_blank" rel="noopener"' if ext else ''

# ------------------------------------------------------------------ about
BAG_ICON = '''<svg class="bag-icon" viewBox="0 0 120 160" role="img" aria-label="کیسه ساکشن آبادیس">
  <defs><linearGradient id="bgi" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e8f3f3"/><stop offset="1" stop-color="#c9e6e6"/></linearGradient></defs>
  <rect x="22" y="38" width="76" height="110" rx="14" fill="url(#bgi)" stroke="#066163" stroke-width="4"/>
  <path class="bag-fluid" d="M26 112q17-8 34 0t34 0V134a10 10 0 0 1-10 10H36a10 10 0 0 1-10-10z" fill="#0e7475" opacity=".55"/>
  <rect x="14" y="22" width="92" height="20" rx="8" fill="#066163"/>
  <rect x="30" y="8" width="16" height="16" rx="4" fill="#087673"/><rect x="74" y="8" width="16" height="16" rx="4" fill="#087673"/>
  <path d="M38 60v34M82 60v34" stroke="#05686b" stroke-width="3" stroke-dasharray="3 6" stroke-linecap="round"/>
  <circle cx="60" cy="78" r="13" fill="none" stroke="#015F61" stroke-width="3"/><path d="M60 70v16M52 78h16" stroke="#015F61" stroke-width="3" stroke-linecap="round"/>
</svg>'''
SLOGAN_ABOUT = ['ما به اندازه یک سرانگشت اثر می‌گذاریم،', 'به شما', 'به طبیعت', 'به جهان']   # Abadis-Sign (live)
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
            ph = (f'<video class="team-clip" muted loop playsinline autoplay preload="metadata" disablepictureinpicture disableremoteplayback '
                  f'poster="{v}-poster.webp" aria-label="{esc(m["name"])}" tabindex="-1"><source src="{v}.webm" type="video/webm"><source src="{v}.mp4" type="video/mp4"></video>')
        out.append(f'<div class="member"><div class="av">{ph}</div><strong>{esc(m["name"])}</strong><span>{esc(m["role"])}</span></div>')
    return f'<div class="team-grid {cls}">{"".join(out)}</div>'


def about(write):
    """About page from the LIVE abadis-med.com/درباره-ما/ (data/about_live.json, fetched 2026-10-14).
    Team order is exactly live: desktop list on desktop, mobile list on mobile (the live site has two)."""
    p = '../'; d = load('about_live.json'); bl = B('/درباره-ما/')
    it = d['intro']
    lead = it[1]
    blocks = []
    i = 2
    while i < len(it):
        if i + 2 < len(it) and it[i + 1] == ':':
            blocks.append((it[i], it[i + 2])); i += 3
        else:
            i += 1
    cards = ''.join(f'<div class="card prose reveal"><h3>{esc(t)}</h3><p>{esc(x)}</p></div>' for t, x in blocks)
    hist_h, hist_p = d['history'][0], d['history'][1]
    commit = d['commit']; goals = d['goals']
    commit_h = f'<h3>{esc(commit[0])}</h3><p>{esc(commit[1])}</p><ul>' + ''.join(f'<li>{esc(x)}</li>' for x in commit[2:]) + '</ul>'
    goals_h = f'<h3>{esc(goals[0])}</h3><p>{esc(goals[1])}</p><ul>' + ''.join(f'<li>{esc(x)}</li>' for x in goals[2:]) + '</ul>'
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
            f'<a class="cert-tile" href="{src}" data-gallery="certs" data-w="{w}" data-h="{h}" aria-label="نمایش بزرگ‌تر: مجوز و گواهی {fa(n)}">'
            f'<img src="{src}" width="{w}" height="{h}" alt="مجوز / گواهی‌نامه آبادیس {fa(n)}" loading="lazy" decoding="async"></a>'
        )
    cert_blocks = []
    for key, label in CERT_GROUPS['fa']:
        if not grouped[key]:
            continue
        h3 = f'<h3 lang="en">{esc(label)}</h3>' if key == 'imed' else f'<h3>{esc(label)}</h3>'
        cert_blocks.append(f'<div class="cert-group reveal" id="certs-{key}">{h3}<div class="cert-wall">{"".join(grouped[key])}</div></div>')
    certs_html = f'<div class="cert-groups">{"".join(cert_blocks)}</div>'
    pb = [b for b in bl if b.get('sec') == '70f87b0' and b['t'] in ('img', 'html', 'btn')]
    partners = []
    for k in range(0, len(pb) - 2, 3):
        im, tx, bt = pb[k:k + 3]
        logo = picture(p, im['src'], im.get('alt', ''), 600)
        link = f'<a class="more-link" href="{esc(bt["href"])}" target="_blank" rel="noopener">{esc(bt["text"])} ↗</a>' if bt.get('href') else ''
        partners.append(f'<div class="card partner reveal"><div class="logo-box">{logo}</div>{tx["html"]}{link}</div>')
    slogan = ''.join(f'<span class="slogan-line" style="--i:{n}">{esc(x)}</span>' for n, x in enumerate(SLOGAN_ABOUT))
    hero = f'''  <section class="page-hero about-hero">
    <video class="about-hero-video" muted loop playsinline autoplay preload="metadata" poster="{p}assets/media/hero-or-zagros-poster.jpg" aria-hidden="true" tabindex="-1" disablepictureinpicture disableremoteplayback><source src="{p}assets/media/hero-or-zagros.mp4" type="video/mp4"></video>
    <div class="wrap about-hero-grid">
      <div>{crumbs_html(p)}
        <h1>آشنایی با <em>آبادیس</em></h1>
        <p class="slogan reveal" aria-label="{esc(' '.join(SLOGAN_ABOUT))}">{slogan}</p>
      </div>
      <div class="about-hero-icon">{BAG_ICON}</div>
    </div>
  </section>'''
    main = f'''{hero}
  <nav class="anchors" aria-label="بخش‌های صفحه"><div class="wrap"><a href="#intro">درباره ما</a><a href="#history">تاریخچه</a><a href="#why">چرا آبادیس؟</a><a href="#certs">مجوزها و گواهینامه‌ها</a><a href="#partners">شرکای تجاری</a><a href="#team">تیم اجرایی</a></div></nav>
  <section class="section" id="intro"><div class="wrap" style="max-width:1000px">
    <h2 class="reveal" style="margin-bottom:14px">درباره ما بیشتر بدانید...</h2>
    <p class="reveal" style="text-align:justify">{esc(lead)}</p>
    <div class="grid g-3" style="margin-top:18px;gap:16px">{cards}</div>
  </div></section>
  <section class="section section--alt" id="history"><div class="wrap split">
    <div class="prose reveal"><h2>{esc(hist_h)}</h2><p>{esc(hist_p)}</p></div>
    <div class="liner-box reveal">{BAG_ICON}</div>
  </div></section>
  <section class="section"><div class="wrap grid g-2" style="gap:18px">
    <div class="card prose reveal">{commit_h}</div>
    <div class="card prose reveal">{goals_h}</div>
  </div></section>
  <section class="section section--alt" id="why"><div class="wrap">
    <h2 class="reveal" style="margin-bottom:20px">چرا آبادیس؟</h2>
    <ul class="checks why-list reveal">{whys}</ul>
  </div></section>
  <section class="section" id="certs"><div class="wrap">
    <h2 class="reveal" style="margin-bottom:8px">مجوزها و گواهینامه‌ها</h2>
    <p class="reveal" style="margin-bottom:18px">همهٔ {fa(n)} مجوز، گواهینامه و تقدیرنامهٔ منتشرشده در سایت آبادیس.</p>
    {certs_html}
  </div></section>
  <section class="section section--alt" id="partners"><div class="wrap">
    <h2 class="reveal" style="margin-bottom:20px">شرکای تجاری</h2>
    <div class="grid g-3">{''.join(partners)}</div>
  </div></section>
  <section class="section" id="team"><div class="wrap">
    <h2 class="reveal" style="margin-bottom:20px">آشنایی با تیم اجرایی</h2>
    {_team_html(p, d['team']['desktop'], 'team--desktop')}
    {_team_html(p, d['team']['mobile'], 'team--mobile')}
  </div></section>'''
    write('about/index.html', page(p, 'about', 'آشنایی با ما', lead[:160], main, lightbox=True,
          scripts=f'<script src="{p}assets/js/motion.js" defer></script>\n'))


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
    <p class="note" style="margin-top:18px">ضرایب محاسبه همان ضرایب محاسبه‌گر سایت فعلی آبادیس است.</p>
  </div></section>
  <section class="section" style="padding-top:0"><div class="wrap"><div class="doc-links"><a href="../products/suction-bag/">کیسه ساکشن یکبار مصرف</a><a href="../sdgs/">توسعه پایدار</a><a href="../contact/">ارتباط با ما</a></div></div></section>'''
    js = '''<script>
(function(){
  var nf = new Intl.NumberFormat('fa-IR', {maximumFractionDigits: 1});
  function r(x, d){ var m = Math.pow(10, d); return Math.round(x * m) / m; }
  function v(f, n){ var x = parseFloat(String(f.elements[n].value).replace(/[۰-۹]/g, function(c){return '۰۱۲۳۴۵۶۷۸۹'.indexOf(c)})); return isFinite(x) && x > 0 ? x : 0; }
  function set(id, x){ document.getElementById(id).textContent = nf.format(x); }
  var s = document.getElementById('calcSurg'), b = document.getElementById('calcBeds');
  function surg(){ var S = v(s, 's'); set('cs0', r(S*1.6*9.3, 0)); set('cs1', r(S*2.5*85000, 1)); set('cs2', r(S*1.7/60*2.2*7.1, 1)); }
  function beds(){ var O = v(b, 'o'), I = v(b, 'i'), u = O*254 + I*67; set('cb0', r(u*1.6*9.3, 0)); set('cb1', r((O*200 + I*50)*2.5*85000, 1)); set('cb2', r(u*1.7*2.2*7.1/60, 1)); }
  s.addEventListener('input', surg); b.addEventListener('input', beds); surg(); beds();
})();
</script>
'''
    write('calculator/index.html', page(p, 'calculator', 'محاسبه گر', 'محاسبه‌گر صرفه جویی کیسه ساکشن یکبار مصرف آبادیس: مصرف آب، هزینه شست و شو و ضد عفونی و زمان کادر درمان.', main, scripts=js))

# ------------------------------------------------------------------ SDGs / توسعه پایدار (full generated page)
def _sdg_sections(p, bl):
    """Build section HTML fragments from /توسعه-پایدار/ blocks (verbatim)."""
    icons = ''.join(picture(p, b['src'], '', 240) for b in bl if b['t'] == 'img')
    parts = []
    first = True
    for sid, bs in secs(bl):
        h = next((b['text'] for b in bs if b['t'] == 'h'), '')
        body = ''.join(rewrite_html(b['html'], p) for b in bs if b['t'] == 'html')
        extra = f'<div class="sdg-icons">{icons}</div>' if any(b['t'] == 'img' for b in bs) and icons else ''
        if first:
            parts.append(
                f'<div class="reveal" style="margin-top:34px">'
                f'<h2 style="font-size:1.5rem;margin-bottom:12px">{esc(h)}</h2>'
                f'{extra}<div class="prose">{body}</div></div>'
            )
            first = False
        else:
            parts.append(
                f'<div class="reveal" style="margin-top:34px">'
                f'<h3 style="font-size:1.25rem;margin-bottom:12px">{esc(h)}</h3>'
                f'{extra}<div class="prose">{body}</div></div>'
            )
    return ''.join(parts)


def sdgs(write):
    """FA توسعه پایدار — UN SDG commitment page (old /توسعه-پایدار/)."""
    p = '../'
    bl = B('/توسعه-پایدار/')
    body = _sdg_sections(p, bl)
    lead = next((strip_tags(b['html']) for b in bl if b['t'] == 'html'), '')
    main = f'''{page_hero(p, [('توسعه پایدار', None)], 'توسعه پایدار', lead[:180])}
  <section class="section" id="sdg"><div class="wrap" style="max-width:980px">
    {body}
  </div></section>'''
    write('sdgs/index.html', page(p, 'sdgs', 'توسعه پایدار',
          'سند تعهد شرکت دانش‌بنیان مخازن طبی آبادیس به اهداف توسعه پایدار سازمان ملل (UN SDGs)',
          main, fa_path='sdgs/'))


# ------------------------------------------------------------------ CSR (Zagros hand-built + مسئولیت اجتماعی / SDG summary blocks)
def csr(write):
    p = '../'
    sdg = B('/توسعه-پایدار/'); soc = B('/مسئولیت-اجتماعی/')
    sdg_html = f'''  <section class="section section--alt" id="sdg"><div class="wrap" style="max-width:980px">
    <span class="eyebrow">توسعه پایدار</span>
    {_sdg_sections(p, sdg)}
    <p class="reveal" style="margin-top:28px"><a class="more-link" href="../sdgs/">صفحهٔ توسعه پایدار ←</a></p>
  </div></section>'''
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
    block = '<!-- phase2:csr -->\n' + act_html + '\n' + sdg_html + '\n<!-- /phase2:csr -->\n'
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
    block = f'''<!-- phase2:contact -->
  <section class="section section--alt" id="hours"><div class="wrap grid g-2" style="gap:24px;align-items:start">
    <div class="reveal"><h2 style="font-size:1.4rem;margin-bottom:14px">ساعات کاری</h2><div class="hours">{boxes('ساعات کاری')}</div>
      <h2 style="font-size:1.4rem;margin:26px 0 14px">روزهای تعطیل</h2><div class="hours">{boxes('روزهای تعطیل')}</div></div>
    <div class="card prose reveal"><h3>دفتر مرکزی</h3>{ext}<h3>کارخانه</h3><p><strong>کدپستی: </strong>۱۸۳۴۱۶۵۷۷۶</p><p><strong>شبکه های اجتماعی: </strong><a href="https://yek.link/abadis.med" target="_blank" rel="noopener">https://yek.link/abadis.med</a></p></div>
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
 'fa': dict(h='همه مراکز درمانی همراه آبادیس', s='جستجوی نام مرکز درمانی...', c='مرکز درمانی', e='موردی یافت نشد.', note=''),
 'en': dict(h='All healthcare centres working with Abadis', s='Search a centre name (Persian)...', c='healthcare centres', e='No match found.', note='Centre names are listed in Persian, as recorded by Abadis.'),
 'ar': dict(h='جميع المراكز الصحية المتعاونة مع آباديس', s='ابحث عن اسم المركز...', c='مركزاً صحياً', e='لا توجد نتائج.', note='تُعرض أسماء المراكز بالفارسية كما سجّلتها آباديس.'),
}
def customers_all(lang='fa'):
    """Searchable A–Z list of every centre in site/zagros-names/names.json (same list on fa/en/ar)."""
    import json
    T = CUST_T[lang]
    names = json.loads((SITE / 'zagros-names/names.json').read_text(encoding='utf-8'))
    names = sorted(dict.fromkeys(n.strip() for n in names if n.strip()), key=lambda n: n.replace('آ', 'ا'))
    groups = {}
    for n in names: groups.setdefault(n[0].replace('آ', 'ا'), []).append(n)
    body = ''.join(f'<div class="cust-letter"><h3 aria-hidden="true">{esc(k)}</h3><ul>{"".join(f"<li>{esc(n)}</li>" for n in v)}</ul></div>' for k, v in groups.items())
    num = _num(lang, len(names))
    note = f'<p class="prov-note">{esc(T["note"])}</p>' if T['note'] else ''
    return f'''<section class="section" id="all-customers"><div class="wrap">
    <h2 class="reveal">{esc(T["h"])}</h2>{note}
    <div class="list-tools"><input class="search" id="custAllQ" type="search" placeholder="{esc(T["s"])}" aria-label="{esc(T["s"])}"><span class="count" id="custAllN" data-total="{len(names)}" aria-live="polite">{num} {esc(T["c"])}</span></div>
    <div class="cust-all" id="custAll" lang="fa" dir="rtl">{body}</div>
    <p class="empty-msg" id="custAllE" hidden>{esc(T["e"])}</p>
  </div></section>
  <script>(function(){{var q=document.getElementById('custAllQ'),n=document.getElementById('custAllN'),e=document.getElementById('custAllE'),L=document.querySelectorAll('#custAll li'),G=document.querySelectorAll('#custAll .cust-letter'),lab=n.textContent.replace(/^[^ ]+ /,''),lang=document.documentElement.lang;
  function norm(s){{return s.replace(/[يى]/g,'ی').replace(/ك/g,'ک').replace(/[أإآ]/g,'ا').replace(/[\u200c\s]+/g,' ').trim().toLowerCase();}}
  L.forEach(function(li){{li.dataset.n=norm(li.textContent);}});
  function fmt(x){{return lang==='en'?String(x):x.toLocaleString(lang==='ar'?'ar-EG':'fa-IR',{{useGrouping:false}});}}
  q.addEventListener('input',function(){{var v=norm(q.value),c=0;L.forEach(function(li){{var h=v&&li.dataset.n.indexOf(v)<0;li.hidden=h;if(!h)c++;}});G.forEach(function(g){{g.hidden=!g.querySelector('li:not([hidden])');}});n.textContent=fmt(c)+' '+lab;e.hidden=c>0;}});}})();</script>'''

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
    main = f'''{page_hero(p, [('مشتریان ما', None)], 'مشتریان ما', esc(head))}
  <section class="section"><div class="wrap">
    <div class="list-tools"><input class="search" type="search" placeholder="جستجوی نام مرکز درمانی..." aria-label="جستجوی مشتریان" data-filter="#custGrid"><span class="count" data-count-for="#custGrid">{fa(len(items))} مرکز درمانی</span></div>
    <div class="logo-grid" id="custGrid" data-paged="30">{''.join(cards)}</div>
    <p class="empty-msg" hidden>موردی یافت نشد.</p>
  </div></section>
  {customers_all('fa')}'''
    write('customers/index.html', page(p, 'customers', 'مشتریان ما', head, main))
    return len(items), nimg

# ------------------------------------------------------------------ academy (was «تجارب ما»)
ACADEMY_MARK = '<svg viewBox="0 0 40 40" aria-hidden="true" width="34" height="34"><rect x="2" y="2" width="36" height="36" rx="11" fill="#066163"/><path d="M8 17l12-6 12 6-12 6z" fill="#fff"/><path d="M13 20v6c0 2 3.5 4 7 4s7-2 7-4v-6" fill="none" stroke="#fff" stroke-width="2.2"/><path d="M32 17v7" stroke="#bfe3e2" stroke-width="2.2" stroke-linecap="round"/></svg>'
MOCK_NOTE = '<div class="ac-mock" role="note"><b>نمونهٔ رابط کاربری (Mockup)</b> — آکادمی آبادیس هنوز راه‌اندازی نشده است؛ ورود، ثبت‌نام و دوره‌ها نمایشی‌اند و هیچ داده‌ای ارسال یا ذخیره نمی‌شود.</div>'

def _academy_shell(html, p, cur):
    nav = [('', 'خانه آکادمی', 'home'), ('#courses', 'دوره‌ها', 'courses'), ('#experiences', 'تجارب ما', 'exp'), ('#faq', 'پرسش‌ها', 'faq')]
    links = ''.join(f'<a href="{p}academy/{h}"{" aria-current=\"page\"" if k == cur else ""}>{t}</a>' for h, t, k in nav)
    head = f'''<header class="ac-header" data-tone="light"><div class="wrap ac-bar">
    <a class="ac-brand" href="{p}academy/">{ACADEMY_MARK}<span><b>آکادمی آبادیس</b><small>Abadis Academy</small></span></a>
    <nav class="ac-nav" aria-label="منوی آکادمی">{links}</nav>
    <div class="ac-cta"><a class="ac-back" href="{p}">سایت آبادیس ↗</a><a class="btn btn-primary ac-login" href="{p}academy/login/">ورود / ثبت‌نام</a></div>
  </div></header>'''
    foot = f'''<footer class="ac-footer"><div class="wrap"><span>{ACADEMY_MARK} آکادمی آبادیس — بخشی از <a href="{p}">مخازن طبی آبادیس</a></span><span class="ac-foot-note">نسخهٔ نمایشی؛ نام نهایی بخش در انتظار تأیید است.</span></div></footer>'''
    html = re.sub(r'<header class="header" id="header">.*?</header>', lambda m: head, html, count=1, flags=re.S)
    html = re.sub(r'<footer.*?</footer>', lambda m: foot, html, count=1, flags=re.S)
    return html.replace('<body>', '<body class="academy">', 1)

def experiences(write):
    p = '../'; bl = B('/تجارب-ما/')
    cards = []; cur = None
    for b in bl:
        if b['t'] == 'h': cur = [b['text'], '']; cards.append(cur)
        elif b['t'] == 'html' and cur: cur[1] += rewrite_html(b['html'], p)
    exp = ''.join(f'<article class="ac-card ac-exp reveal"><span class="ac-tag">تجربهٔ مشتری</span><h3>{esc(t)}</h3><div class="prose">{h}</div></article>' for t, h in cards)
    courses = [('کنترل عفونت در اتاق عمل', 'مبانی پیشگیری از عفونت‌های بیمارستانی و نقش سیستم‌های ساکشن یک‌بارمصرف', '۶ درس'),
               ('نصب و راه‌اندازی مخازن آبادیس', 'آموزش گام‌به‌گام نصب کیسه، مخزن و اتصالات', '۴ درس'),
               ('مدیریت پسماند بیمارستانی', 'دفع ایمن پسماند عفونی و سازگاری با استانداردها', '۵ درس')]
    cc = ''.join(f'<article class="ac-card ac-course reveal"><span class="ac-tag ac-tag--soon">به‌زودی · نمونه</span><h3>{t}</h3><p>{d}</p><span class="ac-meta">{n}</span></article>' for t, d, n in courses)
    main = f'''<main id="main">
  <section class="ac-hero"><div class="wrap">{MOCK_NOTE}
    <h1>آکادمی <em>آبادیس</em></h1>
    <p class="ac-lead">محل آموزش، تجربه و دانش کادر درمان درباره کنترل عفونت و سیستم‌های ساکشن.</p>
    <div class="ac-hero-cta"><a class="btn btn-primary" href="{p}academy/login/">ورود به آکادمی</a><a class="btn btn-ghost" href="#experiences">تجارب مشتریان</a></div>
  </div></section>
  <section class="section" id="courses"><div class="wrap"><h2>دوره‌ها <small class="ac-ph">[محتوای نمونه — در انتظار برنامهٔ آموزشی]</small></h2><div class="ac-grid">{cc}</div></div></section>
  <section class="section section--alt" id="experiences"><div class="wrap"><h2>تجارب ما</h2><div class="ac-grid ac-grid--2">{exp}</div></div></section>
  <section class="section" id="faq"><div class="wrap" style="max-width:820px"><h2>پرسش‌ها</h2>
    <details class="ac-card"><summary>آکادمی آبادیس چه زمانی راه‌اندازی می‌شود؟</summary><p class="ac-ph">[در انتظار تصمیم شرکت]</p></details>
    <details class="ac-card"><summary>آیا شرکت در دوره‌ها گواهی دارد؟</summary><p class="ac-ph">[در انتظار تصمیم شرکت]</p></details>
  </div></section>
</main>'''
    html = page(p, 'experiences', 'آکادمی آبادیس', 'آکادمی آبادیس: آموزش و تجربه کادر درمان درباره کنترل عفونت و سیستم‌های ساکشن (نسخهٔ نمایشی).', main)
    html = re.sub(r'<main id="main">\s*<main id="main">', '<main id="main">', html).replace('</main>\n</main>', '</main>')
    write('academy/index.html', _academy_shell(html, p, 'home'))
    pl = '../../'
    login = f'''<main id="main"><section class="ac-auth"><div class="wrap">
  <div class="ac-auth-card">{MOCK_NOTE}
    <a class="ac-brand ac-brand--lg" href="{pl}academy/">{ACADEMY_MARK}<span><b>آکادمی آبادیس</b><small>Abadis Academy</small></span></a>
    <div class="ac-tabs" role="tablist"><button type="button" role="tab" aria-selected="true">ورود</button><button type="button" role="tab" aria-selected="false">ثبت‌نام</button></div>
    <form class="ac-form" onsubmit="event.preventDefault();this.querySelector('.ac-out').hidden=false;" novalidate>
      <label for="acU">شماره موبایل یا ایمیل</label><input id="acU" type="text" autocomplete="username" inputmode="email" placeholder="۰۹۱۲۰۰۰۰۰۰۰">
      <label for="acP">رمز عبور</label><input id="acP" type="password" autocomplete="current-password">
      <div class="ac-row"><label><input type="checkbox"> مرا به خاطر بسپار</label><a href="#" onclick="return false">فراموشی رمز</a></div>
      <button class="btn btn-primary" type="submit">ورود</button>
      <button class="btn btn-ghost" type="button" onclick="this.form.querySelector('.ac-out').hidden=false">ورود با کد یک‌بارمصرف (OTP)</button>
      <p class="ac-out" hidden role="status">این صفحه نمایشی است و ورود هنوز فعال نشده است.</p>
    </form>
    <p class="ac-small">با ورود، <a href="#" onclick="return false">قوانین آکادمی</a> را می‌پذیرید. <span class="ac-ph">[متن قوانین: در انتظار]</span></p>
  </div></div></section></main>'''
    html = page(pl, 'experiences', 'ورود به آکادمی آبادیس', 'ورود به آکادمی آبادیس (نسخهٔ نمایشی)', login)
    html = re.sub(r'<main id="main">\s*<main id="main">', '<main id="main">', html).replace('</main>\n</main>', '</main>')
    html = html.replace('<meta name="robots" content="index', '<meta name="robots" content="noindex')
    write('academy/login/index.html', _academy_shell(html, pl, 'login'))
    stub = '<!doctype html><html lang="fa-IR" dir="rtl"><head><meta charset="utf-8"><meta name="robots" content="noindex"><link rel="canonical" href="../academy/"><meta http-equiv="refresh" content="0; url=../academy/#experiences"><title>آکادمی آبادیس</title></head><body><p><a href="../academy/#experiences">«تجارب ما» به آکادمی آبادیس منتقل شد</a></p><script>location.replace("../academy/#experiences")</script></body></html>'
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
    main = f'''{page_hero(p, [('فرصت‌های همکاری', None)], 'فرصت‌های همکاری', 'جای شما در آبادیس خالیست...', CAREERS_ART)}
  <section class="section" id="jobs"><div class="wrap">
    <h2 class="reveal" style="margin-bottom:18px">موقعیت‌های شغلی</h2>
    <div class="grid g-3">{cards}</div>
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
    write('careers/index.html', page(p, 'careers', 'فرصت‌های همکاری', 'فرصت های همکاری و موقعیت های شغلی شرکت دانش‌بنیان مخازن طبی آبادیس', main, fa_path='careers/'))
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
