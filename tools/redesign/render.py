"""Render extracted crawl blocks into redesign markup."""
import re
from lib import esc, best_img, img, rewrite_html, href, strip_tags, fa

def picture(p, url, alt='', maxw=1000, cls='', fallback=None, lazy=True):
    r = best_img(url, maxw)
    if not r:
        if fallback: return f'<img{f" class={cls!r}" if cls else ""} src="{p}{fallback}" alt="{esc(alt)}" loading="lazy" decoding="async">'
        return ''
    c = f' class="{cls}"' if cls else ''
    lz = ' loading="lazy"' if lazy else ''
    return f'<img{c} src="{p}{r["src"]}" width="{r["w"]}" height="{r["h"]}"{lz} decoding="async" alt="{esc(alt)}">'

def gallery_link(p, url, group, alt='', thumbw=480, fullw=1600, cls=''):
    t = best_img(url, thumbw); f = best_img(url, fullw)
    if not t: return ''
    c = f' class="{cls}"' if cls else ''
    return (f'<a{c} href="{p}{f["src"]}" data-gallery="{group}" data-w="{f["w"]}" data-h="{f["h"]}" aria-label="نمایش بزرگ‌تر{": " + esc(alt) if alt else ""}">'
            f'<img src="{p}{t["src"]}" width="{t["w"]}" height="{t["h"]}" loading="lazy" decoding="async" alt="{esc(alt)}"></a>')

def table(rows):
    if not rows: return ''
    head, *body = rows
    th = ''.join(f'<th>{esc(c)}</th>' for c in head)
    tb = ''.join('<tr>' + ''.join(f'<td>{esc(c)}</td>' for c in r) + '</tr>' for r in body)
    return f'<div class="table-wrap"><table><thead><tr>{th}</tr></thead><tbody>{tb}</tbody></table></div>'

def aparat(code, title):
    return (f'<div class="video-frame"><iframe src="https://www.aparat.com/video/video/embed/videohash/{code}/vt/frame" '
            f'title="{esc(title)}" loading="lazy" allowfullscreen referrerpolicy="no-referrer-when-downgrade"></iframe></div>')

def blocks_to_prose(bl, p, skip_title=None, gid='g'):
    """Generic renderer for article-like content (posts, experiences ...)."""
    out = []; gi = 0
    for b in bl:
        t = b['t']
        if t == 'h':
            if skip_title and strip_tags(b['text']) == strip_tags(skip_title): continue
            lvl = min(max(int(b.get('lvl') or 2), 2), 4)
            txt = esc(b['text'])
            if b.get('href'):
                h, ext = href(b['href'], p)
                txt = f'<a href="{esc(h, quote=True)}"{" target=_blank rel=noopener" if ext else ""}>{txt}</a>'
            out.append(f'<h{lvl}>{txt}</h{lvl}>')
        elif t == 'html' and b.get('html'):
            out.append(rewrite_html(b['html'], p))
        elif t == 'img':
            pic = picture(p, b['src'], b.get('alt', ''), 1000)
            if pic: out.append(f'<figure>{pic}{f"<figcaption>{esc(b["cap"])}</figcaption>" if b.get("cap") else ""}</figure>')
        elif t == 'gallery':
            gi += 1
            items = ''.join(gallery_link(p, i['src'] if isinstance(i, dict) else i, f'{gid}{gi}', (i.get('alt') if isinstance(i, dict) else '') or '') for i in b['imgs'])
            if items: out.append(f'<div class="photo-grid">{items}</div>')
        elif t == 'btn' and b.get('href'):
            h, ext = href(b['href'], p)
            out.append(f'<p><a class="btn btn-ghost" href="{esc(h, quote=True)}"{" target=_blank rel=noopener" if ext else ""}>{esc(b["text"])}</a></p>')
        elif t == 'list':
            out.append('<ul>' + ''.join(f'<li>{esc(x)}</li>' for x in b.get('items', [])) + '</ul>')
        elif t == 'table':
            out.append(table(b['rows']))
        elif t == 'faq':
            out.append(faq_list(b['items'], p))
        elif t == 'tabs':
            for tb in b['tabs']:
                out.append(f'<h3>{esc(tb["title"])}</h3>' + rewrite_html(tb.get('html', ''), p))
                for x in tb.get('imgs', []):
                    pic = picture(p, x, '', 900)
                    if pic: out.append(f'<figure>{pic}</figure>')
        elif t == 'box':
            out.append(f'<p><strong>{esc(b.get("title",""))}</strong> {esc(b.get("desc",""))}</p>')
    return '\n'.join(out)

def faq_list(items, p):
    return '<div class="faq">' + ''.join(
        f'<details class="faq-item"><summary>{esc(it["q"])}</summary><div class="faq-a">{rewrite_html(it["a"], p)}</div></details>'
        for it in items) + '</div>'

def secs(bl):
    out = []
    for b in bl:
        if not out or out[-1][0] != b.get('sec'): out.append([b.get('sec'), []])
        out[-1][1].append(b)
    return out
