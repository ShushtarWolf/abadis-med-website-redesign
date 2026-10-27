"""Patch live About and News HTML. Does not rebuild posts or i18n."""
import html as html_lib
import json
import re
import sys
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from build import write
from pages_company import about
from about_motion import inject_about_motion
from news_topics import (
    TOPICS, classify_text, year_bucket, jalali_year_of, news_shell, empty_html,
    tally, feature_from_card, digits, topic_label, _COPY,
)
from layout import crumbs


def patch_about():
    about(write)
    jobs = [
        (ROOT / 'site/en/about-us/index.html', 'en', '../../'),
        (ROOT / 'site/arabic/من-نحن/index.html', 'ar', '../../'),
    ]
    for path, lang, prefix in jobs:
        text = path.read_text(encoding='utf-8')
        path.write_text(inject_about_motion(text, lang, prefix), encoding='utf-8')
        print('about', lang, 'ab-orbit' , 'ab-orbit-fit' in path.read_text(encoding='utf-8'))


def _dates(name):
    path = ROOT / 'tools/redesign/data' / name
    if not path.exists():
        return {}
    out = {}
    for wp in json.loads(path.read_text(encoding='utf-8')):
        slug = urllib.parse.unquote(wp.get('slug') or '')
        out[slug] = wp.get('date') or ''
    return out


def annotate(text, lang, dates):
    if 'data-topic=' in text and 'data-news-finalist' in text:
        return text, [], None
    parts = text.split('<a class="post-card reveal"')
    out = [parts[0]]
    pairs = []
    first = None
    for part in parts[1:]:
        end = part.find('</a>')
        card = part[:end] if end >= 0 else part
        rest = part[end:] if end >= 0 else ''
        title = re.search(r'<h3>(.*?)</h3>', card, re.S)
        para = re.search(r'<p>(.*?)</p>', card, re.S)
        blob = html_lib.unescape(((title.group(1) if title else '') + ' ' + (para.group(1) if para else '')))
        blob = re.sub(r'<[^>]+>', ' ', blob)
        topic = classify_text(blob)
        iso = re.search(r'datetime="([^"]+)"', card)
        year = jalali_year_of(iso.group(1)) if iso else 0
        if not year:
            href = re.search(r'href="([^"]+)"', card)
            slug = urllib.parse.unquote(href.group(1)).rstrip('/').rsplit('/', 1)[-1] if href else ''
            year = jalali_year_of(dates.get(slug) or '')
        bucket = year_bucket(year) if year else 'before'
        pairs.append((topic, bucket))
        piece = f'<a class="post-card reveal" data-topic="{topic}" data-year="{bucket}"' + card + rest
        if first is None:
            first = piece[:piece.find('</a>') + 4]
        out.append(piece)
    return ''.join(out), pairs, first


def patch_news(path, lang, prefix, dates):
    text = path.read_text(encoding='utf-8')
    text, pairs, first = annotate(text, lang, dates)
    stats = tally(pairs)
    shell = news_shell(lang, prefix, crumbs(prefix, [(_COPY[lang]['archive'], None)], lang=lang), stats, feature_from_card(first or '', lang))
    text, n = re.subn(
        r'<section class="page-hero">.*?</section>\s*<section class="section"><div class="wrap">\s*<div class="list-tools">.*?</div>',
        shell,
        text,
        count=1,
        flags=re.S,
    )
    if n != 1:
        raise SystemExit(f'hero replace failed for {path} ({n})')
    text = re.sub(r'<p class="empty-msg" hidden>.*?</p>', empty_html(lang), text, count=1)
    css = f'<link rel="stylesheet" href="{prefix}assets/css/news-finalist.css">'
    js = f'<script src="{prefix}assets/js/news-finalist.js" defer></script>'
    if 'news-finalist.css' not in text:
        text = text.replace('</head>', css + '\n</head>', 1)
    if 'news-finalist.js' not in text:
        text = text.replace('</body>', js + '\n</body>', 1)
    path.write_text(text, encoding='utf-8')
    from collections import Counter
    print(path.name, lang, 'total', stats['total'], 'topics', dict(Counter(t for t, _ in pairs)), 'years', stats['years'])


def patch_finalist():
    path = ROOT / 'site/news-hero-options/finalist-d-hybrid/index.html'
    text = path.read_text(encoding='utf-8')
    fa_digits = str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789')
    short = {key: label for key, label, *_rest in TOPICS}

    def card_repl(m):
        tag = m.group(0)
        title = html_lib.unescape(re.search(r'data-title="([^"]*)"', tag).group(1))
        excerpt = html_lib.unescape(re.search(r'data-excerpt="([^"]*)"', tag).group(1)) if 'data-excerpt="' in tag else ''
        topic = classify_text(title + ' ' + excerpt)
        cat = short.get(topic, '')
        yraw = re.search(r'data-year="([^"]*)"', tag).group(1)
        year = int(re.search(r'1[34]\d\d', yraw.translate(fa_digits)).group(0)) if re.search(r'1[34]\d\d', yraw.translate(fa_digits)) else 0
        bucket = yraw if year >= 1401 else '۱۴۰۰ و قبل'
        tag = re.sub(r'data-cat="[^"]*"', f'data-cat="{cat}"', tag, count=1)
        tag = re.sub(r'data-year="[^"]*"', f'data-year="{bucket}"', tag, count=1)
        return tag

    text2, n = re.subn(r'<a class="post-card" data-fin-card\b[^>]*>', card_repl, text)
    print('finalist cards', n)
    counts = {}
    years = {}
    # Count archive cards only. Hero slots repeat the same data-year/data-cat.
    for m in re.finditer(r'<a class="post-card" data-fin-card\b[^>]*>', text2):
        tag = m.group(0)
        y = re.search(r'data-year="([^"]*)"', tag)
        c = re.search(r'data-cat="([^"]*)"', tag)
        if y:
            years[y.group(1)] = years.get(y.group(1), 0) + 1
        if c and c.group(1):
            counts[c.group(1)] = counts.get(c.group(1), 0) + 1
    total = len(re.findall(r'data-fin-card', text2))
    def fa(n):
        return str(n).translate(str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹'))
    topic_btns = f'<button type="button" data-fin-cat="all" aria-pressed="true">همه اخبار <b>{fa(total)}</b></button>'
    for key, label, fa_label, _en, _ar in TOPICS:
        topic_btns += f'<button type="button" data-fin-cat="{label}" aria-pressed="false">{fa_label} <b>{fa(counts.get(label, 0))}</b></button>'
    year_order = ['۱۴۰۵', '۱۴۰۴', '۱۴۰۳', '۱۴۰۲', '۱۴۰۱', '۱۴۰۰ و قبل']
    max_n = max([years.get(y, 0) for y in year_order] or [1])
    year_btns = '<button type="button" class="fin-year" data-fin-year="all" aria-pressed="true"><b>همه سال‌ها</b></button>'
    for label in year_order:
        n = years.get(label, 0)
        w = int(round(100 * n / max_n)) if max_n else 0
        year_btns += f'<button type="button" class="fin-year" data-fin-year="{label}" aria-pressed="false"><b>{label}</b><em>{fa(n)}</em><i style="--w:{w}%"></i></button>'
    text2, n1 = re.subn(r'(<div class="fin-topics"[^>]*>).*?(</div>)', r'\1' + topic_btns + r'\2', text2, count=1, flags=re.S)
    text2, n2 = re.subn(r'(<div class="fin-years"[^>]*>).*?(</div>)', r'\1' + year_btns + r'\2', text2, count=1, flags=re.S)
    text2, n3 = re.subn(r'(<div class="fin-row"[^>]*aria-label="فیلتر تقسیم‌بندی موضوعی"[^>]*>).*?(</div>)',
                        r'\1<span class="fin-lab">موضوع</span>' + topic_btns + r'\2', text2, count=1, flags=re.S)
    plain_years = '<button type="button" data-fin-year="all" aria-pressed="true">همه سال‌ها</button>'
    for label in year_order:
        plain_years += (
            f'<button type="button" data-fin-year="{label}" aria-pressed="false">{label} <b>{fa(years.get(label, 0))}</b></button>'
        )
    text2, n4 = re.subn(r'(<div class="fin-row"[^>]*aria-label="فیلتر سال"[^>]*>).*?(</div>)',
                        r'\1<span class="fin-lab">سال</span>' + plain_years + r'\2', text2, count=1, flags=re.S)
    print('finalist regions', n1, n2, n3, n4, 'counts', counts, 'years', years)
    path.write_text(text2, encoding='utf-8')


if __name__ == '__main__':
    patch_about()
    patch_news(ROOT / 'site/news/index.html', 'fa', '../', {})
    patch_news(ROOT / 'site/en/latest-news/index.html', 'en', '../../', _dates('en_posts.json'))
    patch_news(ROOT / 'site/arabic/الاخبار/index.html', 'ar', '../../', _dates('ar_posts.json'))
    patch_finalist()
