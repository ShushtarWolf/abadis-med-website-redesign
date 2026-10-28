"""News + articles lists and one page per archived post."""
import html, json, re, urllib.parse as u
from lib import load, esc, strip_tags, best_img, jdate, fa, POST_MAP, ROOT, SITE
from layout import page, page_hero
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

FALLBACK_THUMB = 'assets/img/post-thumb-fallback.webp'

def thumb(p, post, w=640):
    r = best_img(post.get('image'), w) if post.get('image') else None
    if not r:   # first inline image as fallback
        for b in post['blocks']:
            srcs = [b['src']] if b['t'] == 'img' else [html.unescape(m) for m in re.findall(r'<img [^>]*src="([^"]+)"', b.get('html') or '')]
            for s in srcs:
                r = best_img(s, w)
                if r: break
            if r: break
    return r

def excerpt(post):
    d = strip_tags(post.get('desc') or '')
    d = re.sub(r'[\xa0\s]+', ' ', d).strip(' \t\n\r\u200c·-|')
    if len(d) < 12:
        d = strip_tags(' '.join(b.get('html', '') for b in post['blocks'] if b['t'] == 'html'))
        d = re.sub(r'[\xa0\s]+', ' ', d).strip()
    if len(d) < 12:
        d = strip_tags(post.get('t') or post.get('title') or '')
    return d[:190] + ('…' if len(d) > 190 else '')

def card(p, post, from_list=True, tag='', topic='', year=''):
    r = thumb(p, post)
    alt = esc(post['t'])
    ph = (f'<div class="ph"><img src="{p}{r["src"]}" width="{r["w"]}" height="{r["h"]}" alt="{alt}" loading="lazy" decoding="async"></div>' if r
          else f'<div class="ph txt"><img src="{p}{FALLBACK_THUMB}" width="1280" height="720" alt="{alt}" loading="lazy"></div>')
    href = (post['rel'].split('/', 1)[1] if from_list else p + post['rel'])
    tag_html = f'<span class="tag">{esc(tag)}</span>' if tag else ''
    attrs = ''
    if topic:
        attrs += f' data-topic="{esc(topic)}"'
    if year:
        attrs += f' data-year="{esc(year)}"'
    return (f'<a class="post-card reveal" href="{href}" data-name="{esc(post["t"])}"{attrs}>{ph}<div class="body">{tag_html}<time datetime="{post["date"][:10]}">{jdate(post["date"])}</time>'
            f'<h3>{esc(post["t"])}</h3><p>{esc(excerpt(post))}</p><span class="go">ادامه مطلب ←</span></div></a>')

def missing_card(p, m):
    return (f'<a class="post-card ext reveal" href="{esc(m["url"])}" target="_blank" rel="noopener" data-name="{esc(m["t"])}"><div class="ph txt"><img src="{p}{FALLBACK_THUMB}" width="1280" height="720" alt="{esc(m["t"])}" loading="lazy"></div>'
            f'<div class="body"><span class="date">متن در نسخهٔ آرشیوشده موجود نیست</span><h3>{esc(m["t"])}</h3><span class="go">مطالعه در سایت فعلی</span></div></a>')

def build(write):
    prepare()
    for cat in ('news', 'articles'):
        p = '../'
        items = [x for x in POSTS if x['cat'] == cat]
        miss = [m for m in MISSING if m['cat'] == cat]
        n = len(items) + len(miss)
        lead = ('اخبار، گزارش‌ها، مصاحبه‌ها و رویدادهای شرکت دانش‌بنیان مخازن طبی آبادیس' if cat == 'news'
                else 'اگر به دنبال مطلب خاصی می گردید، از موتور جستجوگر زیر استفاده نمایید.')
        h1 = 'آخرین <em>اخبار</em>' if cat == 'news' else '<em>مقالات</em>'
        if cat == 'news':
            from news_topics import classify_text, year_bucket, jalali_year_of, news_shell, empty_html, tally, feature_from_card
            from layout import crumbs
            bits = []
            pairs = []
            for x in items:
                topic = classify_text(x['t'] + ' ' + excerpt(x))
                bucket = year_bucket(jalali_year_of(x.get('date')))
                pairs.append((topic, bucket))
                bits.append(card(p, x, topic=topic, year=bucket))
            cards = ''.join(missing_card(p, m) for m in miss) + ''.join(bits)
            stats = tally(pairs)
            shell = news_shell('fa', p, crumbs(p, [(LABEL[cat], None)]), stats, feature_from_card(bits[0] if bits else '', 'fa'))
            main = shell + f'\n    <div class="post-grid" id="postGrid" data-paged="12">{cards}</div>\n    {empty_html("fa")}\n  </div></section>'
            extra = f'<link rel="stylesheet" href="{p}assets/css/news-finalist.css">\n'
            scripts = f'<script src="{p}assets/js/news-finalist.js" defer></script>\n'
            write(f'{cat}/index.html', page(p, cat, LABEL[cat], lead, main, fa_path=f'{cat}/', extra_head=extra, scripts=scripts))
        else:
            from news_topics import classify_article_text, year_bucket, jalali_year_of, article_shell, article_empty_html, article_tally, article_feature_from_card
            from layout import crumbs
            bits = []
            pairs = []
            for x in items:
                topic = classify_article_text(x['t'] + ' ' + excerpt(x))
                bucket = year_bucket(jalali_year_of(x.get('date')))
                pairs.append((topic, bucket))
                bits.append(card(p, x, topic=topic, year=bucket))
            cards = ''.join(missing_card(p, m) for m in miss) + ''.join(bits)
            stats = article_tally(pairs)
            shell = article_shell('fa', p, crumbs(p, [(LABEL[cat], None)]), stats, article_feature_from_card(bits[0] if bits else '', 'fa'))
            main = shell + f'\n    <div class="post-grid" id="postGrid" data-paged="12">{cards}</div>\n    {article_empty_html("fa")}\n  </div></section>'
            extra = f'<link rel="stylesheet" href="{p}assets/css/news-finalist.css">\n'
            scripts = f'<script src="{p}assets/js/news-finalist.js" defer></script>\n'
            write(f'{cat}/index.html', page(p, cat, LABEL[cat], lead, main, fa_path=f'{cat}/', extra_head=extra, scripts=scripts))
        # singles
        p = '../../'
        for i, x in enumerate(items):
            r = thumb(p, x, 1200)
            first_img = next((b for b in x['blocks'] if b['t'] in ('img', 'html')), None)
            dup = bool(first_img and first_img['t'] == 'img' and x.get('image') and re.sub(r'-\d+x\d+', '', first_img['src']).rsplit('.', 1)[0] == re.sub(r'-\d+x\d+', '', x['image']).rsplit('.', 1)[0])
            if r and not dup:
                lead_img = f'<div class="lead-img"><img src="{p}{r["src"]}" width="{r["w"]}" height="{r["h"]}" alt="{esc(x["t"])}" decoding="async"></div>'
            elif not r:
                lead_img = f'<div class="lead-img"><img src="{p}{FALLBACK_THUMB}" width="1280" height="720" alt="{esc(x["t"])}" decoding="async"></div>'
            else:
                lead_img = ''
            body = blocks_to_prose(x['blocks'], p, skip_title=x['t'], gid=f'p{x["id"]}-')
            newer = items[i - 1] if i > 0 else None; older = items[i + 1] if i + 1 < len(items) else None
            nav = ''
            if newer or older:
                nav = '<nav class="post-nav" aria-label="مطالب دیگر">' + \
                      (f'<a href="{p}{newer["rel"]}"><span>مطلب جدیدتر</span>{esc(newer["t"])}</a>' if newer else '<span></span>') + \
                      (f'<a href="{p}{older["rel"]}"><span>مطلب قدیمی‌تر</span>{esc(older["t"])}</a>' if older else '') + '</nav>'
            related = [y for y in items if y is not x][max(0, i - 1):max(0, i - 1) + 3]
            words = len(re.sub(r'<[^>]+>', ' ', body).split()); mins = max(1, round(words / 200))
            meta = f'<div class="meta"><span>{TAG[cat]}</span><span>{jdate(x["date"])}</span><span>زمان مطالعه: {fa(mins)} دقیقه</span></div>'
            from urllib.parse import quote
            url = quote(f'https://abadis-med.com/{cat}/{x["id"]}/', safe=':/'); tt = quote(x['t'])
            share = (f'<div class="share" aria-label="اشتراک‌گذاری"><span>اشتراک‌گذاری:</span>'
                     f'<a href="https://t.me/share/url?url={url}&amp;text={tt}" target="_blank" rel="noopener">تلگرام</a>'
                     f'<a href="https://wa.me/?text={tt}%20{url}" target="_blank" rel="noopener">واتس‌اپ</a>'
                     f'<a href="https://www.linkedin.com/sharing/share-offsite/?url={url}" target="_blank" rel="noopener">لینکدین</a>'
                     f'<button type="button" onclick="navigator.clipboard&&navigator.clipboard.writeText(location.href);this.textContent=\'کپی شد\'">کپی پیوند</button></div>')
            rel_html = (f'<section class="related"><h2>مطالب مرتبط</h2><div class="post-grid">{"".join(card(p, y, False) for y in related)}</div></section>') if related else ''
            main = f'''{page_hero(p, [(LABEL[cat], '../'), (x['t'][:60] + ('…' if len(x['t']) > 60 else ''), None)], esc(x['t']), '', meta)}
  <section class="section"><div class="wrap">
    <article class="article prose post-v2">
      {lead_img}
      {body}
    </article>
    <div class="article-foot post-v2"><span>تاریخ انتشار: {jdate(x['date'])}</span>{share}<a href="../">بازگشت به {LABEL[cat]} ←</a></div>
    {nav}
    {rel_html}
  </div></section>'''
            og = (p + r['src']) if r else (p + FALLBACK_THUMB)
            # Document title includes section so it never collides with same-named pages
            # (e.g. article 2615 «راهنمای نصب مخازن» vs /install-guide/tanks/).
            doc_title = f'{x["t"]} | {LABEL[cat]}'
            write(f'{cat}/{x["id"]}/index.html', page(p, cat, doc_title, excerpt(x), main, og=og, lightbox='data-gallery' in body, fa_path=f'{cat}/'))
    # Home teasers are generated by pages_home (run `build.py home` or full build).
    try:
        import pages_home
        pages_home.build(write)
    except ImportError:
        pass
