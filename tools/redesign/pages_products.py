"""Products hub + six product family pages (suction bag page is hand-built and kept)."""
import re
from lib import PAGES, esc, strip_tags, best_img, rewrite_html
from layout import page, mosaic_hero
from render import table, gallery_link, secs

FAMILIES = [  # slug, live path, hub title (verbatim from live hub), hub image, local fallback image
    ('suction-bag', '/محصولات/کیسه-ساکشن/', 'کیسه های ساکشن', 'https://abadis-med.com/wp-content/uploads/2022/12/کیسه-ساکشن.jpg', 'assets/img/p/p2-main.webp'),
    ('stand', '/محصولات/پایه/', 'پایه و نگهدارنده', 'https://abadis-med.com/wp-content/uploads/2022/12/پایه-ترولی.jpg', 'assets/img/p/p1-g3-t.webp'),
    ('filters', '/محصولات/فیلترها/', 'فیلتر', 'https://abadis-med.com/wp-content/uploads/2022/12/فیلتر1-2-845x684-1.jpg', 'assets/img/filters/anti-1-t.webp'),
    ('suction-tube', '/محصولات/ساکشن-تیوب/', 'ساکشن تیوب', 'https://abadis-med.com/wp-content/uploads/2022/12/ساکشن-تیوب-7e83722522e8aeb7512b7075311316b7__m8ULku2SAG__1-1-300x300.jpg', 'assets/img/p/p1-g4-t.webp'),
    ('canister', '/محصولات/مخزن/', 'مخزن', 'https://abadis-med.com/wp-content/uploads/2022/12/AMR_4901.jpg', 'assets/img/p/p3-g1-t.webp'),
    ('connectors', '/محصولات/اتصالات/', 'اتصالات', 'https://abadis-med.com/wp-content/uploads/2022/12/اتصالات-845x684-1.jpg', 'assets/img/p/p2-g3-t.webp'),
    ('other', '/محصولات/سایر-محصولات/', 'سایر محصولات',
     'https://abadis-med.com/wp-content/uploads/2022/12/19-1024x880.jpg', None),
]
# Fallback photos when the item's own image was never archived by the Wayback Machine.
# Only images that verifiably show that exact product are used (family hub photo / phase-1 asset).
FALLBACK = {
    'msk': ['https://abadis-med.com/wp-content/uploads/2022/12/AMR_4901.jpg'],
    'sdv': ['https://abadis-med.com/wp-content/uploads/2022/12/ساکشن-دیواری-بزرگسال-1030x1030-1.jpg'],
    'paye': ['https://abadis-med.com/wp-content/uploads/2022/12/پایه-ترولی.jpg'],
    'negahdarande': ['https://abadis-med.com/wp-content/uploads/2022/12/نگهدارنده-لوله-تراشه-1030x1030-1.jpg'],
    'anti': ['local:assets/img/filters/anti-1.webp', 'local:assets/img/filters/anti-2.webp'],
    'ght': ['local:assets/img/filters/stop-1.webp', 'local:assets/img/filters/stop-2.webp'],
    'mot': ['local:assets/img/filters/porous-1.webp'],
}
LOCAL_DIMS = {}
def local_link(p, path, gid, alt, cls=''):
    from PIL import Image
    from lib import SITE
    w, h = Image.open(SITE / path).size
    t = path.replace('.webp', '-t.webp')
    tw, th = Image.open(SITE / t).size if (SITE / t).exists() else (w, h)
    if not (SITE / t).exists(): t = path
    return (f'<a href="{p}{path}" data-gallery="{gid}" data-w="{w}" data-h="{h}" aria-label="نمایش بزرگ‌تر: {esc(alt)}">'
            f'<img src="{p}{t}" width="{tw}" height="{th}" loading="lazy" decoding="async" alt="{esc(alt)}"></a>')
SUCTION_BAG_ITEMS = ['کیسه ساکشن ۱ لیتری', 'کیسه ساکشن ۲ لیتری', 'کیسه ساکشن ۳ لیتری']

def pick(b):
    h = b.get('href') or ''
    if h.startswith('http') and re.search(r'\.(jpe?g|png|webp)$', h) and best_img(h): return h
    return b['src']

def norm(s): return re.sub(r'[\s\u200c\u200b():]+', '', strip_tags(s))

def family(path):
    bl = PAGES[path]['blocks']
    h1 = next((b['text'] for b in bl if b['t'] == 'h' and b.get('lvl') == 1), PAGES[path]['title'].split('»')[0].strip())
    anchors = [(b['text'], b['href'][1:]) for b in bl if b['t'] == 'h' and (b.get('href') or '').startswith('#')]
    items = []
    for sid, bs in secs(bl):
        if not any(b['t'] == 'html' for b in bs) or not any(b['t'] in ('img', 'table') for b in bs): continue
        items.append(bs)
    out = []
    for i, bs in enumerate(items):
        title, aid = anchors[i] if i < len(anchors) else (None, f'item{i+1}')
        htmls = [b['html'] for b in bs if b['t'] == 'html' and b.get('html')]
        body = '\n'.join(htmls)
        m = re.match(r'\s*(?:<p>)?\s*<strong>(.*?)</strong>\s*(?:</p>)?', body, re.S)
        if m:
            lead = strip_tags(m.group(1))
            if title is None: title = lead
            if norm(lead) and (norm(lead) in norm(title) or norm(title) in norm(lead) or len(lead) < 60):
                body = body[m.end():]
        out.append({'id': aid, 'title': title or '', 'html': body,
                    'imgs': [(pick(b), b.get('alt', '')) for b in bs if b['t'] == 'img'],
                    'tables': [b['rows'] for b in bs if b['t'] == 'table']})
    return h1, out

def product_block(p, it, n):
    imgs = it['imgs']; gid = it['id']
    media = ''
    links = [gallery_link(p, u_, gid, a or it['title'], 900, 1600) for u_, a in imgs]
    links = [l for l in links if l]
    if not links:
        for src in FALLBACK.get(gid, []):
            if src.startswith('local:'): links.append(local_link(p, src[6:], gid, it['title']))
            else:
                l = gallery_link(p, src, gid, it['title'], 900, 1600)
                if l: links.append(l)
    if links:
        main = links[0].replace('<a ', '<a class="gal-main" ', 1)
        thumbs = ''.join(links[1:])
        media = f'<div class="size-media">{main}{f"<div class=gal-thumbs>{thumbs}</div>" if thumbs else ""}</div>'
    else:
        media = f'<div class="size-media"><div class="gal-main gal-missing"><img src="{p}assets/img/abadis-logo-teal.png" width="658" height="309" alt=""><span>تصویر این محصول در نسخهٔ آرشیوشدهٔ سایت موجود نبود</span></div></div>'
    tables = ''.join(table(t) for t in it['tables'])
    return f'''    <div class="size-block reveal" id="{esc(it["id"])}">
      <h3>{esc(it["title"])}</h3>
      <div class="size-grid">
        {media}
        <div class="size-info prose">{rewrite_html(it["html"], p)}</div>
      </div>
      {tables}
    </div>'''

def related(p, here):
    cards = []
    for slug, path, title, im, fb in FAMILIES:
        if slug == here: continue
        r = best_img(im, 480) if im else None
        src = (p + r['src']) if r else (p + fb if fb else None)
        ph = f'<div class="ph"><img src="{src}" alt="" loading="lazy" decoding="async"></div>' if src else '<div class="ph txt">آبادیس</div>'
        cards.append(f'<a class="mini-card" href="../{slug}/">{ph}<strong>{esc(title)}</strong></a>')
    return f'''  <section class="section section--alt" id="more"><div class="wrap">
    <h2 class="reveal" style="margin-bottom:20px">سایر محصولات آبادیس</h2>
    <div class="mini-grid">{''.join(cards)}</div>
  </div></section>'''

INQUIRY = '''  <section class="section" id="inquiry"><div class="wrap">
    <div class="cta-band reveal">
      <h2>آماده سفارش برای مرکز درمانی شما</h2>
      <p>برای لیست قیمت، نمونه و هماهنگی نصب با تیم فروش مخازن طبی آبادیس در تماس باشید.</p>
      <div class="cta-actions"><a class="btn btn-light" href="tel:+982192001017">تماس با فروش</a><a class="btn btn-ghost" href="https://wa.me/989100145809" target="_blank" rel="noopener">درخواست نمونه در واتس‌اپ</a></div>
    </div>
  </div></section>'''

def build(write):
    p = '../../'
    summaries = {}
    for slug, path, title, im, fb in FAMILIES:
        if slug == 'suction-bag':
            summaries[slug] = SUCTION_BAG_ITEMS; continue
        h1, items = family(path)
        summaries[slug] = [i['title'] for i in items]
        anchors = ''.join(f'<a href="#{esc(i["id"])}">{esc(i["title"])}</a>' for i in items) + '<a href="#more">سایر محصولات</a><a href="#inquiry">استعلام</a>'
        blocks = '\n'.join(product_block(p, it, n) for n, it in enumerate(items))
        lead = '، '.join(i['title'] for i in items)
        main = (mosaic_hero(p, [('محصولات', '../')], 'محصولات آبادیس', esc(h1), esc(lead), label=h1)
                + f'\n  <nav class="anchors" aria-label="بخش‌های صفحه"><div class="wrap">{anchors}</div></nav>\n'
                + f'  <section class="section"><div class="wrap">\n{blocks}\n  </div></section>\n'
                + related(p, slug) + '\n' + INQUIRY)
        write(f'products/{slug}/index.html', page(p, 'products', h1, f'{h1} آبادیس: ' + lead, main, lightbox=True, fa_path=f'products/{slug}/'))
    # hub
    p = '../'
    cards = []
    for slug, path, title, im, fb in FAMILIES:
        r = best_img(im, 640) if im else None
        src = (p + r['src']) if r else (p + fb if fb else None)
        ph = f'<div class="ph"><img src="{src}" alt="{esc(title)} آبادیس" loading="lazy" decoding="async"></div>' if src else '<div class="ph txt">آبادیس</div>'
        sub = '، '.join(summaries[slug])
        cards.append(f'<a class="pcard reveal" href="{slug}/">{ph}<strong>{esc(title)}</strong><span>{esc(sub)}</span><span class="go">مشاهده ←</span></a>')
    main = (mosaic_hero(p, [('محصولات', None)], 'کنترل عفونت · مدیریت سیالات بیمارستانی', 'محصولات <em>آبادیس</em>',
                        'کیسه ساکشن یکبار مصرف، فیلترها، مخزن، پایه و نگهدارنده ها، اتصالات، ساکشن تیوب و سایر محصولات.', label='محصولات آبادیس')
            + f'\n  <section class="section"><div class="wrap"><div class="grid g-3">{"".join(cards)}</div></div></section>\n'
            + f'  <section class="section" style="padding-top:0"><div class="wrap"><div class="doc-links"><a href="../downloads/">مرکز دانلود کاتالوگ‌ها</a><a href="../install-guide/">راهنمای نصب</a><a href="../calculator/">محاسبه‌گر صرفه‌جویی</a></div></div></section>')
    write('products/index.html', page(p, 'products', 'محصولات', 'محصولات مخازن طبی آبادیس: کیسه ساکشن یکبار مصرف، فیلترها، مخزن، پایه و نگهدارنده ها، اتصالات، ساکشن تیوب و سایر محصولات.', main, fa_path='products/'))
