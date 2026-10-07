"""About, dealers, contact extras, CSR/SDG extras, calculator, and footer pages."""
import re, json
from lib import PAGES, SITE, esc, strip_tags, best_img, rewrite_html, href, fa, load
from layout import page, mosaic_hero, page_hero
from render import picture, gallery_link, table, faq_list, aparat, secs, blocks_to_prose

def B(path): return PAGES[path]['blocks']
def ext_attr(ext): return ' target="_blank" rel="noopener"' if ext else ''

# ------------------------------------------------------------------ about
def about(write):
    p = '../'; bl = B('/درباره-ما/')
    intro = bl[2]['html']
    first, rest = re.match(r'(<p>.*?</p>)(.*)', intro, re.S).groups()
    hist, commit, goals = [b['html'] for b in bl if b['t'] == 'html'][1:4]
    liner = picture(p, 'https://abadis-med.com/wp-content/uploads/2022/12/ANIMATED-LINER-BAG-01.png', 'کیسه ساکشن آبادیس', 600, 'liner')
    whys = ''.join(f'<div class="why">{picture(p, b["img"], "", 160)}<span>{esc(b["title"])}</span></div>' for b in bl if b['t'] == 'box')
    iso = gallery_link(p, 'https://abadis-med.com/wp-content/uploads/2025/04/ISO.jpg', 'iso', 'گواهینامه ISO', 700, 1600) \
        or gallery_link(p, 'https://abadis-med.com/wp-content/uploads/2025/01/گواهینامه-ایزو-scaled.jpg', 'iso', 'گواهینامه ISO', 700, 1600)
    iso_html = f'<div class="cert-single">{iso}</div>' if iso else '<a class="btn btn-ghost" href="https://abadis-med.com/wp-content/uploads/2025/01/گواهینامه-ایزو-scaled.jpg" target="_blank" rel="noopener">مشاهده مجوز ISO</a>'
    # partners: img, html, btn triplets in section 70f87b0
    pb = [b for b in bl if b.get('sec') == '70f87b0' and b['t'] in ('img', 'html', 'btn')]
    partners = []
    for i in range(0, len(pb) - 2, 3):
        im, tx, bt = pb[i:i + 3]
        logo = picture(p, im['src'], im.get('alt', ''), 600)
        link = f'<a class="more-link" href="{esc(bt["href"])}" target="_blank" rel="noopener">{esc(bt["text"])} ↗</a>' if bt.get('href') else ''
        partners.append(f'<div class="card partner reveal"><div class="logo-box">{logo}</div>{tx["html"]}{link}</div>')
    members = []
    # team member videos from abadismedit (assets/team-videos, merged from team-assets-2026-10-06)
    VIDEOS = {'علیرضا حسنعلی': ('alireza', 'team-member'), 'نوید حسنعلی': ('navid', 'team-member-navid')}
    for b in [b for b in bl if b['t'] == 'member']:
        ph = '' if 'abadis-lg-01' in (b['img'] or '') else picture(p, b['img'], b['name'], 400)
        if b['name'] in VIDEOS:
            d, n = VIDEOS[b['name']]; v = f'{p}assets/team-videos/{d}/{n}'
            ph = (f'<video width="522" height="782" autoplay muted playsinline preload="metadata" poster="{v}-poster.webp" aria-label="{esc(b["name"])}">'
                  f'<source src="{v}.webm" type="video/webm"><source src="{v}.mp4" type="video/mp4"></video>')
        av = f'<div class="av">{ph}</div>' if ph else f'<div class="av" aria-hidden="true">{esc(b["name"][:1])}</div>'
        members.append(f'<div class="member">{av}<strong>{esc(b["name"])}</strong><span>{esc(b["role"])}</span></div>')
    main = f'''{mosaic_hero(p, [('آشنایی با ما', None)], 'شرکت دانش‌بنیان مخازن طبی آبادیس', 'آشنایی با <em>آبادیس</em>', strip_tags(first), label='آشنایی با ما')}
  <nav class="anchors" aria-label="بخش‌های صفحه"><div class="wrap"><a href="#intro">درباره ما</a><a href="#history">تاریخچه</a><a href="#why">چرا آبادیس؟</a><a href="#iso">گواهینامه ISO</a><a href="#partners">شرکای تجاری</a><a href="#team">تیم اجرایی</a></div></nav>
  <section class="section" id="intro"><div class="wrap" style="max-width:920px">
    <h2 class="reveal" style="margin-bottom:18px">درباره ما بیشتر بدانید...</h2>
    <div class="prose reveal">{rest}</div>
  </div></section>
  <section class="section section--alt" id="history"><div class="wrap split">
    <div class="prose reveal">{hist}</div>
    <div class="liner-box reveal">{liner}</div>
  </div></section>
  <section class="section"><div class="wrap grid g-2" style="gap:18px">
    <div class="card prose reveal">{commit}</div>
    <div class="card prose reveal">{goals}</div>
  </div></section>
  <section class="section section--alt" id="why"><div class="wrap">
    <h2 class="reveal" style="margin-bottom:20px">چرا آبادیس؟</h2>
    <div class="why-grid reveal">{whys}</div>
  </div></section>
  <section class="section" id="iso"><div class="wrap" style="text-align:center">
    <h2 class="reveal" style="margin-bottom:20px">گواهینامه ISO</h2>
    <div class="reveal">{iso_html}</div>
  </div></section>
  <section class="section section--alt" id="partners"><div class="wrap">
    <h2 class="reveal" style="margin-bottom:20px">شرکای تجاری</h2>
    <div class="grid g-3">{''.join(partners)}</div>
  </div></section>
  <section class="section" id="team"><div class="wrap">
    <h2 class="reveal" style="margin-bottom:20px">آشنایی با تیم اجرایی</h2>
    <div class="team-grid">{''.join(members)}</div>
  </div></section>'''
    write('about/index.html', page(p, 'about', 'آشنایی با ما', strip_tags(first)[:160], main, lightbox=True))

# ------------------------------------------------------------------ dealers
PROVINCES = ['آذربایجان شرقی', 'آذربایجان غربی', 'اردبیل', 'اصفهان', 'البرز', 'ایلام', 'بوشهر', 'تهران', 'چهارمحال و بختیاری',
             'خراسان جنوبی', 'خراسان رضوی', 'خراسان شمالی', 'خوزستان', 'زنجان', 'سمنان', 'سیستان و بلوچستان', 'فارس', 'قزوین', 'قم',
             'کردستان', 'کرمان', 'کرمانشاه', 'کهگیلویه و بویراحمد', 'گلستان', 'گیلان', 'لرستان', 'مازندران', 'مرکزی', 'هرمزگان', 'همدان', 'یزد']
def dealers(write):
    """Build dealers page from data/dealers.json (live listing + CPT gaps)."""
    p = '../'
    data = load('dealers.json')
    intro = data.get('intro') or 'لیست نمایندگان فروش محصولات مخازن طبی آبادیس در سراسر کشور'
    groups = data['groups']
    have = {g['province'] for g in groups if g.get('dealers')}
    total = sum(len(g.get('dealers') or []) for g in groups)
    chips = ''.join(
        f'<button type="button" data-prov="{esc(pv)}" aria-pressed="false">{esc(pv)}</button>' if pv in have
        else f'<button type="button" class="none" disabled title="بدون نماینده">{esc(pv)}</button>'
        for pv in PROVINCES
    )
    def row(k, v):
        if 'تلفن' in k:
            num = re.sub(r'[^\d۰-۹]', '', v).translate(str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789'))
            v = f'<a href="tel:{num}" dir="ltr">{esc(v)}</a>'
        else:
            v = esc(v)
        return f'<dt>{esc(k)}:</dt><dd>{v}</dd>'
    out = []
    for g in groups:
        pv, title, ds = g['province'], g.get('title') or f'نمایندگان استان {g["province"]}', g.get('dealers') or []
        ents = []
        for d in ds:
            rows = d.get('rows') or []
            dl = f'<dl>{"".join(row(k, v) for k, v in rows)}</dl>' if rows else ''
            ents.append(f'<div class="dealer"><h3>{esc(d["name"])}</h3>{dl}</div>')
        out.append(
            f'<div class="card prov-group reveal" data-prov="{esc(pv)}" id="p-{esc(pv.replace(" ", "-"))}">'
            f'<h2>{esc(title)}</h2>{"".join(ents)}</div>'
        )
    main = f'''{mosaic_hero(p, [('لیست نمایندگان', None)], 'شبکه توزیع فروش آبادیس', 'لیست <em>نمایندگان</em>', esc(intro), label='لیست نمایندگان')}
  <section class="section"><div class="wrap">
    <h2 class="reveal" style="margin-bottom:16px">لیست استان ها</h2>
    <div class="prov-chips reveal" id="provChips">{chips}</div>
    <p class="prov-legend"><span><i></i>دارای نماینده ({fa(len(have))} استان)</span><span><i class="none"></i>بدون نماینده</span><span>{fa(total)} نماینده</span></p>
    <div class="prov-grid" id="dealerList">{''.join(out)}</div>
  </div></section>'''
    write('dealers/index.html', page(p, 'dealers', 'لیست نمایندگان', intro, main))

# ------------------------------------------------------------------ calculator
def calculator(write):
    p = '../'
    labels = ['صرفه جویی در مصرف آب (لیتر)', 'هزینه مربوط به شست و شو و ضد عفونی (تومان)', 'صرفه جویی در زمان کادر درمان (ساعت)']
    def outs(prefix): return ''.join(f'<div><span>{l}</span><output id="{prefix}{i}">۰</output></div>' for i, l in enumerate(labels))
    main = f'''{mosaic_hero(p, [('محاسبه‌گر', None)], 'کیسه ساکشن یکبار مصرف', 'محاسبه <em>گر</em>', 'صرفه جویی در مصرف آب، هزینه شست و شو و ضد عفونی و زمان کادر درمان', label='محاسبه گر')}
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
  <section class="section" style="padding-top:0"><div class="wrap"><div class="doc-links"><a href="../products/suction-bag/">کیسه ساکشن یکبار مصرف</a><a href="../csr/#sdg">توسعه پایدار</a><a href="../contact/">ارتباط با ما</a></div></div></section>'''
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

# ------------------------------------------------------------------ CSR / SDG (inserted into the hand-built csr page)
def csr(write):
    p = '../'
    sdg = B('/توسعه-پایدار/'); soc = B('/مسئولیت-اجتماعی/')
    icons = ''.join(picture(p, b['src'], '', 240) for b in sdg if b['t'] == 'img')
    def sec_html(sid, bl): return [b for b in bl if b.get('sec') == sid]
    parts = []
    for sid, bs in secs(sdg):
        h = next((b['text'] for b in bs if b['t'] == 'h'), '')
        body = ''.join(rewrite_html(b['html'], p) for b in bs if b['t'] == 'html')
        extra = f'<div class="sdg-icons">{icons}</div>' if any(b['t'] == 'img' for b in bs) and icons else ''
        parts.append(f'<div class="reveal" style="margin-top:34px"><h3 style="font-size:1.25rem;margin-bottom:12px">{esc(h)}</h3>{extra}<div class="prose">{body}</div></div>')
    sdg_html = f'''  <section class="section section--alt" id="sdg"><div class="wrap" style="max-width:980px">
    <span class="eyebrow">توسعه پایدار</span>
    {''.join(parts).replace('<div class="reveal" style="margin-top:34px"><h3 style="font-size:1.25rem;margin-bottom:12px">', '<div class="reveal" style="margin-top:34px"><h2 style="font-size:1.5rem;margin-bottom:12px">', 1).replace('</h3>', '</h2>', 1)}
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
<!-- /phase2:contact -->
'''
    f = SITE / 'contact/index.html'; s = f.read_text(encoding='utf-8')
    if '<!-- phase2:contact -->' in s: s = re.sub(r'<!-- phase2:contact -->.*?<!-- /phase2:contact -->\n', lambda m: block, s, flags=re.S)
    else: s = s.replace('</main>', block + '</main>', 1)
    write('contact/index.html', s)

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
        link = f'<a href="{esc(bt["href"])}" target="_blank" rel="noopener">{esc(bt["text"])} ↗</a>' if bt and bt.get('href') else ''
        cards.append(f'<div class="logo-card" data-name="{esc(name)}">{lg}<strong>{esc(name)}</strong>{link}</div>')
    main = f'''{page_hero(p, [('مشتریان ما', None)], 'مشتریان ما', esc(head))}
  <section class="section"><div class="wrap">
    <div class="list-tools"><input class="search" type="search" placeholder="جستجوی نام مرکز درمانی..." aria-label="جستجوی مشتریان" data-filter="#custGrid"><span class="count" data-count-for="#custGrid">{fa(len(items))} مرکز درمانی</span></div>
    <div class="logo-grid" id="custGrid" data-paged="30">{''.join(cards)}</div>
    <p class="empty-msg" hidden>موردی یافت نشد.</p>
  </div></section>'''
    write('customers/index.html', page(p, 'customers', 'مشتریان ما', head, main))
    return len(items), nimg

# ------------------------------------------------------------------ experiences
def experiences(write):
    p = '../'; bl = B('/تجارب-ما/')
    cards = []; cur = None
    for b in bl:
        if b['t'] == 'h': cur = [b['text'], '']; cards.append(cur)
        elif b['t'] == 'html' and cur: cur[1] += rewrite_html(b['html'], p)
    body = ''.join(f'<article class="card prose reveal"><h2 style="font-size:1.3rem;margin-top:0">{esc(t)}</h2>{h}</article>' for t, h in cards)
    main = f'''{page_hero(p, [('تجارب ما', None)], 'تجارب ما')}
  <section class="section"><div class="wrap grid g-2" style="gap:18px;align-items:start">{body}</div></section>'''
    write('experiences/index.html', page(p, 'experiences', 'تجارب ما', strip_tags(cards[0][1])[:160] if cards else '', main))

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

def careers(write):
    jobs = load('jobs.json')
    p = '../'
    cards = ''.join(f'''<div class="card job reveal"><h3>{esc(j["title"])}</h3><span class="dates">تاریخ انتشار: {fa(j["pub"])} · تاریخ انقضاء: {fa(j["exp"])}</span><span class="badge-exp">منقضی شده</span><a class="more-link" href="jobs/{JOB_SLUGS[j["title"]]}/">مشاهده موقعیت ←</a></div>''' for j in jobs)
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
    main = f'''{page_hero(p, [('فرصت های همکاری', None)], 'فرصت های همکاری', 'جای شما در آبادیس خالیست...')}
  <section class="section" id="jobs"><div class="wrap">
    <h2 class="reveal" style="margin-bottom:18px">موقعیت های شغلی</h2>
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
    write('careers/index.html', page(p, 'careers', 'فرصت های همکاری', 'فرصت های همکاری و موقعیت های شغلی شرکت دانش‌بنیان مخازن طبی آبادیس', main, fa_path='careers/'))
    p = '../../../'
    for j in jobs:
        slug = JOB_SLUGS[j['title']]
        meta = f'<div class="meta"><span>تاریخ انتشار: {fa(j["pub"])}</span><span>تاریخ انقضاء آگهی: {fa(j["exp"])}</span><span>منقضی شده</span></div>'
        main = f'''{page_hero(p, [('فرصت های همکاری', '../../'), (j['title'], None)], esc(j['title']), '', meta)}
  <section class="section"><div class="wrap article">
    <div class="card prose reveal">{rewrite_html(j['html'], p)}</div>
    <div class="cta-actions" style="display:flex;gap:12px;flex-wrap:wrap;margin-top:22px"><a class="btn btn-primary" href="../../#apply">ثبت درخواست</a><a class="btn btn-ghost" href="../../#jobs">مشاهده کلیه موقعیت های شغلی</a></div>
  </div></section>'''
        write(f'careers/jobs/{slug}/index.html', page(p, 'careers', j['title'], strip_tags(j['html'])[:150], main))

from lib import JOB_MAP
import urllib.parse as _u
for _j in load('jobs.json'):
    JOB_MAP[_u.unquote(_u.urlsplit(_j['url']).path)] = f"careers/jobs/{JOB_SLUGS[_j['title']]}/"
GROUPS = {'about': about, 'dealers': dealers, 'calculator': calculator, 'csr': csr, 'contact': contact,
          'customers': customers, 'experiences': experiences, 'downloads': downloads, 'install': install, 'faq': faq, 'careers': careers}
