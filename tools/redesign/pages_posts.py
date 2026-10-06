"""News + articles lists and one page per archived post."""
import json, re, urllib.parse as u
from lib import load, esc, strip_tags, best_img, jdate, fa, POST_MAP, ROOT, SITE
from layout import page, mosaic_hero, page_hero
from render import blocks_to_prose
from cats import classify, strip_title

LABEL = {'news': 'آخرین اخبار', 'articles': 'مقالات'}
TAG = {'news': 'خبر', 'articles': 'مقاله'}
POSTS, MISSING = [], []

def prepare():
    if POSTS: return
    kc = {u.unquote(k).rstrip('/'): v for k, v in load('known_cats.json').items()}
    for p in load('posts.json'):
        c = classify(p, kc)
        path = u.unquote(u.urlsplit(p['url']).path)
        if not path.endswith('/') and '.' not in path.rsplit('/', 1)[-1]:
            path += '/'
        if c is None:
            POST_MAP[path] = 'careers/#jobs'
            POST_MAP[path.rstrip('/')] = 'careers/#jobs'
            continue
        p = dict(p, cat=c, t=strip_title(p['title']), rel=f'{c}/{p["id"]}/')
        for key in {path, path.rstrip('/'), (p.get('path') or path)}:
            if not key:
                continue
            k = key if key.endswith('/') or '.' in key.rsplit('/', 1)[-1] else key + '/'
            POST_MAP[k] = p['rel']
            POST_MAP[k.rstrip('/')] = p['rel']
        POSTS.append(p)
    POSTS.sort(key=lambda x: x['date'], reverse=True)
    # posts that exist on the live site but were never archived -> listed, linked to the live URL
    audit = json.load(open(ROOT / 'docs/abadis/ABADIS-AUDIT.json', encoding='utf-8'))
    titles = {u.unquote(i['link']).rstrip('/'): i['title'] for i in audit['wpContent']['items'] if i['type_key'] == 'post'}
    have = {u.unquote(p['url']).rstrip('/') for p in load('posts.json')}
    for x in audit['urlInventory']:
        if x['content_type'] != 'post' or x['language'] != 'fa': continue
        url = u.unquote(x['current_url']).rstrip('/')
        if url in have: continue
        t = titles.get(url) or url.rsplit('/', 1)[-1].replace('-', ' ')
        q = {'url': x['current_url'], 'title': t, 'date': x['lastmod']}
        c = classify(q, {})
        if 'استخدام' in t: c = 'news'
        MISSING.append(dict(q, cat=c, t=t, slug_title=t not in titles.values()))
    MISSING.sort(key=lambda x: x['date'], reverse=True)

def thumb(p, post, w=640):
    r = best_img(post.get('image'), w) if post.get('image') else None
    if not r:   # first inline image as fallback
        for b in post['blocks']:
            if b['t'] == 'img':
                r = best_img(b['src'], w)
                if r: break
    return r

def excerpt(post):
    d = strip_tags(post.get('desc') or '')
    if not d:
        d = strip_tags(' '.join(b.get('html', '') for b in post['blocks'] if b['t'] == 'html'))
    return d[:190] + ('…' if len(d) > 190 else '')

def card(p, post, from_list=True):
    r = thumb(p, post)
    ph = (f'<div class="ph"><img src="{p}{r["src"]}" width="{r["w"]}" height="{r["h"]}" alt="" loading="lazy" decoding="async"></div>' if r
          else f'<div class="ph txt"><img src="{p}assets/img/abadis-logo-teal.png" width="658" height="309" alt="" loading="lazy"></div>')
    href = (post['rel'].split('/', 1)[1] if from_list else p + post['rel'])
    return (f'<a class="post-card reveal" href="{href}" data-name="{esc(post["t"])}">{ph}<div class="body"><time datetime="{post["date"][:10]}">{jdate(post["date"])}</time>'
            f'<h3>{esc(post["t"])}</h3><p>{esc(excerpt(post))}</p><span class="go">ادامه مطلب ←</span></div></a>')

def missing_card(p, m):
    return (f'<a class="post-card ext reveal" href="{esc(m["url"])}" target="_blank" rel="noopener" data-name="{esc(m["t"])}"><div class="ph txt"><img src="{p}assets/img/abadis-logo-teal.png" width="658" height="309" alt="" loading="lazy"></div>'
            f'<div class="body"><span class="date">متن در نسخهٔ آرشیوشده موجود نیست</span><h3>{esc(m["t"])}</h3><span class="go">مطالعه در سایت فعلی</span></div></a>')

def build(write):
    prepare()
    for cat in ('news', 'articles'):
        p = '../'
        items = [x for x in POSTS if x['cat'] == cat]
        miss = [m for m in MISSING if m['cat'] == cat]
        cards = ''.join(missing_card(p, m) for m in miss) + ''.join(card(p, x) for x in items)
        n = len(items) + len(miss)
        lead = ('اخبار، گزارش‌ها، مصاحبه‌ها و رویدادهای شرکت دانش‌بنیان مخازن طبی آبادیس' if cat == 'news'
                else 'اگر به دنبال مطلب خاصی می گردید، از موتور جستجوگر زیر استفاده نمایید.')
        h1 = 'آخرین <em>اخبار</em>' if cat == 'news' else '<em>مقالات</em>'
        main = f'''{mosaic_hero(p, [(LABEL[cat], None)], 'مخازن طبی آبادیس', h1, lead, label=LABEL[cat])}
  <section class="section"><div class="wrap">
    <div class="list-tools"><input class="search" type="search" placeholder="جست و جو" aria-label="جست و جو در {LABEL[cat]}" data-filter="#postGrid"><span class="count" data-count-for="#postGrid">{fa(n)} مطلب</span></div>
    <div class="post-grid" id="postGrid" data-paged="12">{cards}</div>
    <p class="empty-msg" hidden>موردی یافت نشد.</p>
  </div></section>'''
        write(f'{cat}/index.html', page(p, cat, LABEL[cat], lead, main, fa_path=f'{cat}/'))
        # singles
        p = '../../'
        for i, x in enumerate(items):
            r = thumb(p, x, 1200)
            first_img = next((b for b in x['blocks'] if b['t'] in ('img', 'html')), None)
            dup = bool(first_img and first_img['t'] == 'img' and x.get('image') and re.sub(r'-\d+x\d+', '', first_img['src']).rsplit('.', 1)[0] == re.sub(r'-\d+x\d+', '', x['image']).rsplit('.', 1)[0])
            lead_img = f'<div class="lead-img"><img src="{p}{r["src"]}" width="{r["w"]}" height="{r["h"]}" alt="{esc(x["t"])}" decoding="async"></div>' if r and not dup else ''
            body = blocks_to_prose(x['blocks'], p, skip_title=x['t'], gid=f'p{x["id"]}-')
            newer = items[i - 1] if i > 0 else None; older = items[i + 1] if i + 1 < len(items) else None
            nav = ''
            if newer or older:
                nav = '<nav class="post-nav" aria-label="مطالب دیگر">' + \
                      (f'<a href="{p}{newer["rel"]}"><span>مطلب جدیدتر</span>{esc(newer["t"])}</a>' if newer else '<span></span>') + \
                      (f'<a href="{p}{older["rel"]}"><span>مطلب قدیمی‌تر</span>{esc(older["t"])}</a>' if older else '') + '</nav>'
            related = [y for y in items if y is not x][:0]
            meta = f'<div class="meta"><span>{TAG[cat]}</span><span>{jdate(x["date"])}</span></div>'
            main = f'''{page_hero(p, [(LABEL[cat], '../'), (x['t'][:60] + ('…' if len(x['t']) > 60 else ''), None)], esc(x['t']), '', meta)}
  <section class="section"><div class="wrap">
    <article class="article prose">
      {lead_img}
      {body}
    </article>
    <div class="article-foot"><span>تاریخ انتشار: {jdate(x['date'])}</span><a href="../">بازگشت به {LABEL[cat]} ←</a></div>
    {nav}
  </div></section>'''
            og = (p + r['src']) if r else None
            # Document title includes section so it never collides with same-named pages
            # (e.g. article 2615 «راهنمای نصب مخازن» vs /install-guide/tanks/).
            doc_title = f'{x["t"]} | {LABEL[cat]}'
            write(f'{cat}/{x["id"]}/index.html', page(p, cat, doc_title, excerpt(x), main, og=og, lightbox='data-gallery' in body, fa_path=f'{cat}/'))
    home_teasers()

def home_teasers():
    """Point the home page teasers at the real posts (newest titles are only on the live site)."""
    f = SITE / 'index.html'; s = f.read_text(encoding='utf-8')
    by_t = {m['t']: m['url'] for m in MISSING}
    by_t.update({x['t']: x['rel'] for x in POSTS})
    def sub(m):
        t = strip_tags(m.group(2))
        for k, v in by_t.items():
            if k.startswith(t[:40]) or t.startswith(k[:40]):
                ext = v.startswith('http')
                return f'<a class="card teaser reveal" href="{esc(v)}"{" target=\"_blank\" rel=\"noopener\"" if ext else ""}>{m.group(1)}<h3>{m.group(2)}</h3>'
        return m.group(0)
    s = re.sub(r'<a class="card teaser reveal" href="[^"]*"(?: target="_blank" rel="noopener")?>(<span class="tag">[^<]*</span>)<h3>(.*?)</h3>', sub, s)
    f.write_text(s, encoding='utf-8')
