#!/usr/bin/env python3
"""Build 3 interactive redesign proposals (A1, A2, A3) for «مقالات» (articles/)
modeled on the approved «آخرین اخبار» (news/ Finalist D) template at site/articles-options/."""
import sys, json, re
from pathlib import Path

ROOT = Path('/workspace/abadis-med-website-redesign')
sys.path.insert(0, str(ROOT / 'tools/redesign'))

import pages_posts
from lib import esc, fa, jdate
from news_topics import (
    ARTICLE_TOPICS, _ARTICLE_COPY, classify_article_text, year_bucket,
    jalali_year_of, article_tally, digits, year_label, article_topic_label
)

OUT = ROOT / 'site/articles-options'
OUT.mkdir(parents=True, exist_ok=True)
(OUT / 'screenshots').mkdir(parents=True, exist_ok=True)

pages_posts.prepare()
ARTICLES = [x for x in pages_posts.POSTS if x['cat'] == 'articles']

# Enrich each article with topic, year bucket, reading time, audience tag, thumb, and excerpt
AUDIENCES = [
    ('clinical', 'کادر درمان و اتاق عمل'),
    ('infection', 'مسئولین کنترل عفونت'),
    ('procurement', 'مدیران خرید و تجهیزات پزشکی'),
]

def classify_audience(topic, text):
    if topic == 'guide':
        return 'procurement', 'مدیران خرید و تجهیزات پزشکی'
    if topic in ('infection', 'env'):
        return 'infection', 'مسئولین کنترل عفونت'
    return 'clinical', 'کادر درمان و اتاق عمل'

ENRICHED = []
PAIRS = []
for idx, art in enumerate(ARTICLES):
    ex = pages_posts.excerpt(art)
    topic = classify_article_text(art['t'] + ' ' + ex)
    y_num = jalali_year_of(art.get('date'))
    bucket = year_bucket(y_num)
    PAIRS.append((topic, bucket))
    r = pages_posts.thumb('../', art)
    img_src = f"../{r['src']}" if r else f"../{pages_posts.FALLBACK_THUMB}"
    body_txt = re.sub(r'<[^>]+>', ' ', ' '.join(b.get('html', '') for b in art.get('blocks', []) if b.get('t') == 'html'))
    words = len(body_txt.split())
    mins = max(2, min(8, round(words / 180))) if words else (3 if idx % 2 == 0 else 5)
    rtime_bucket = 'fast' if mins <= 3 else 'deep'
    aud_key, aud_label = classify_audience(topic, art['t'] + ' ' + ex)
    ENRICHED.append({
        'id': art['id'],
        'title': art['t'],
        'excerpt': ex,
        'date_iso': art['date'][:10],
        'date_fa': jdate(art['date']),
        'topic': topic,
        'topic_label': article_topic_label(topic, 'fa'),
        'year': bucket,
        'year_fa': '۱۴۰۰ و قبل' if bucket == 'before' else year_label(int(bucket), 'fa'),
        'mins': mins,
        'mins_fa': fa(mins),
        'rtime_bucket': rtime_bucket,
        'aud_key': aud_key,
        'aud_label': aud_label,
        'img': img_src,
        'href': f"../articles/{art['id']}/",
    })

STATS = article_tally(PAIRS)

def render_card(a):
    return (
        f'<a class="post-card reveal" href="{a["href"]}" '
        f'data-name="{esc(a["title"])}" data-topic="{a["topic"]}" data-year="{a["year"]}" '
        f'data-rtime="{a["rtime_bucket"]}" data-aud="{a["aud_key"]}">'
        f'<div class="ph"><img src="{a["img"]}" width="640" height="360" alt="{esc(a["title"])}" loading="lazy" decoding="async">'
        f'<span class="art-card-badge">{esc(a["topic_label"])}</span>'
        f'<span class="art-card-time">{a["mins_fa"]} دقیقه مطالعه</span></div>'
        f'<div class="body">'
        f'<div class="art-meta-row"><time datetime="{a["date_iso"]}">{a["date_fa"]}</time><span class="art-aud-tag">{esc(a["aud_label"])}</span></div>'
        f'<h3>{esc(a["title"])}</h3>'
        f'<p>{esc(a["excerpt"])}</p>'
        f'<span class="go">مطالعه مقاله علمی ←</span>'
        f'</div></a>'
    )

ALL_CARDS_HTML = ''.join(render_card(a) for a in ENRICHED)

def topic_buttons_html():
    T = _ARTICLE_COPY['fa']
    bits = [f'<button type="button" data-news-topic="all" aria-pressed="true">{esc(T["all"])} <b>{digits(STATS["total"], "fa")}</b></button>']
    for key, _s, fa_lab, _en, _ar in ARTICLE_TOPICS:
        cnt = STATS['topics'].get(key, 0)
        bits.append(f'<button type="button" data-news-topic="{key}" aria-pressed="false">{esc(fa_lab)} <b>{digits(cnt, "fa")}</b></button>')
    return ''.join(bits)

def year_buttons_html():
    T = _ARTICLE_COPY['fa']
    order = ['1405', '1404', '1403', '1402', '1401', 'before']
    bits = [f'<button type="button" data-news-year="all" aria-pressed="true">{esc(T["years"])}</button>']
    for k in order:
        cnt = STATS['years'].get(k, 0)
        lab = T['before'] if k == 'before' else year_label(int(k), 'fa')
        bits.append(f'<button type="button" data-news-year="{k}" aria-pressed="false">{lab} <b>{digits(cnt, "fa")}</b></button>')
    return ''.join(bits)

SHARED_CSS = '''
@font-face { font-family: "Kalameh"; src: url("../assets/fonts/kalameh/KalamehWeb-FaNum-Regular.woff2") format("woff2"); font-weight: 400; font-display: swap; }
@font-face { font-family: "Kalameh"; src: url("../assets/fonts/kalameh/KalamehWeb-FaNum-Bold.woff2") format("woff2"); font-weight: 700; font-display: swap; }
@font-face { font-family: "Kalameh"; src: url("../assets/fonts/kalameh/KalamehWeb-FaNum-Black.woff2") format("woff2"); font-weight: 900; font-display: swap; }

:root, [data-theme="light"] {
  --ao-bg: #eef7f7;
  --ao-bg-2: #e0f0f0;
  --ao-surface: #ffffff;
  --ao-surface-2: #f3fafa;
  --ao-ink: #07282b;
  --ao-ink-2: #244b4e;
  --ao-muted: #527578;
  --ao-brand: #066163;
  --ao-brand-2: #0d9488;
  --ao-accent: #5eead4;
  --ao-line: rgba(6, 97, 99, 0.15);
  --ao-shadow: 0 14px 34px rgba(6, 65, 67, 0.08);
}
[data-theme="dark"] {
  --ao-bg: #051619;
  --ao-bg-2: #092226;
  --ao-surface: #0c292e;
  --ao-surface-2: #11353c;
  --ao-ink: #ecfeff;
  --ao-ink-2: #bfe6e8;
  --ao-muted: #84b4b8;
  --ao-brand: #2dd4bf;
  --ao-brand-2: #14b8a6;
  --ao-accent: #5eead4;
  --ao-line: rgba(45, 212, 191, 0.2);
  --ao-shadow: 0 16px 38px rgba(0, 0, 0, 0.42);
}

.ao-topbar {
  position: sticky; top: 0; z-index: 999;
  background: rgba(5, 28, 31, 0.94); backdrop-filter: blur(14px);
  border-bottom: 1px solid rgba(94, 234, 212, 0.24);
  color: #ecfeff; padding: 10px 0;
  font-family: "Kalameh", sans-serif;
}
.ao-topbar-inner {
  max-width: 1320px; margin: 0 auto; padding: 0 20px;
  display: flex; align-items: center; justify-content: space-between; gap: 12px; flex-wrap: wrap;
}
.ao-brand { display: flex; align-items: center; gap: 10px; font-weight: 900; font-size: .95rem; color: #fff; text-decoration: none; }
.ao-brand-badge {
  background: rgba(94, 234, 212, 0.16); color: #5eead4; border: 1px solid rgba(94, 234, 212, 0.35);
  border-radius: 999px; padding: 2px 10px; font-size: .76rem; font-weight: 800;
}
.ao-tabs { display: flex; align-items: center; gap: 6px; flex-wrap: wrap; }
.ao-tab {
  color: #cbe7e8; text-decoration: none; font-size: .82rem; font-weight: 800;
  padding: 6px 13px; border-radius: 999px; border: 1px solid rgba(255,255,255,0.14);
  transition: all .2s ease; display: inline-flex; align-items: center; gap: 5px;
}
.ao-tab:hover { border-color: #5eead4; color: #fff; }
.ao-tab.is-active { background: #0d9488; color: #fff; border-color: #5eead4; box-shadow: 0 4px 14px rgba(13,148,136,.4); }
.ao-tab-rec { background: rgba(245, 158, 11, 0.22); color: #fde68a; padding: 1px 7px; border-radius: 999px; font-size: .7rem; }
.ao-actions { display: flex; align-items: center; gap: 8px; }
.ao-theme-btn {
  background: rgba(255,255,255,0.1); color: #ecfeff; border: 1px solid rgba(94,234,212,0.3);
  border-radius: 999px; padding: 6px 12px; font: inherit; font-size: .78rem; font-weight: 800; cursor: pointer;
}

/* Enhanced Article Cards & Badges */
.post-card .ph { position: relative; }
.art-card-badge {
  position: absolute; top: 10px; right: 10px; z-index: 2;
  background: rgba(5, 34, 38, 0.84); backdrop-filter: blur(6px);
  color: #5eead4; border: 1px solid rgba(94,234,212,0.35);
  border-radius: 999px; padding: 3px 10px; font-size: .74rem; font-weight: 800;
}
.art-card-time {
  position: absolute; bottom: 10px; left: 10px; z-index: 2;
  background: rgba(5, 34, 38, 0.82); color: #ecfeff;
  border-radius: 999px; padding: 2px 9px; font-size: .72rem; font-weight: 700;
}
.art-meta-row {
  display: flex; align-items: center; justify-content: space-between; gap: 8px; flex-wrap: wrap; margin-bottom: 4px;
}
.art-aud-tag {
  font-size: .72rem; font-weight: 700; color: var(--ao-brand);
  background: var(--ao-bg-2); padding: 2px 8px; border-radius: 999px;
}

/* Option 2 Video Hero + News-D Bridge */
.ao-hero-video-sec {
  position: relative; overflow: hidden; background: #041f22; color: #fff;
  padding: 36px 0 28px; border-bottom: 1px solid rgba(94,234,212,0.22);
}
.ao-hero-video-sec video {
  position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; opacity: 0.34; pointer-events: none;
}
.ao-hero-overlay {
  position: absolute; inset: 0;
  background: linear-gradient(90deg, rgba(4,28,31,0.92) 0%, rgba(4,35,39,0.78) 55%, rgba(4,28,31,0.88) 100%);
}
.ao-hero-content { position: relative; z-index: 2; }
.ao-rotator {
  margin-top: 10px; font-family: "Kalameh", sans-serif; font-weight: 900;
  display: flex; flex-direction: column; gap: 4px;
}
.ao-rot-main { font-size: clamp(1rem, 1.5vw, 1.22rem); color: #ecfeff; }
.ao-rot-sub { font-size: clamp(1.1rem, 1.8vw, 1.42rem); color: #5eead4; min-height: 1.5em; }
.ao-extra-filters {
  display: flex; flex-wrap: wrap; gap: 8px; align-items: center;
  margin-top: 8px; padding-top: 8px; border-top: 1px dashed var(--ao-line);
}
.ao-extra-filters button {
  font: inherit; cursor: pointer; border-radius: 999px; border: 1px solid var(--ao-line);
  background: var(--ao-surface-2); color: var(--ao-ink); padding: 3px 10px; font-weight: 700; font-size: .78rem;
}
.ao-extra-filters button[aria-pressed="true"] {
  background: var(--ao-brand); color: #fff; border-color: transparent;
}
[data-theme="dark"] .ao-extra-filters button[aria-pressed="true"] { color: #042f2e; }

/* Option 3 Journal 3-Column Showcase + Horizontal Sticky Bar */
.ao-journal-trio {
  display: grid; grid-template-columns: 1.35fr 1fr 1fr; gap: 14px; margin: 16px 0 18px;
}
.ao-jcard {
  position: relative; border-radius: 22px; overflow: hidden;
  background: var(--ao-surface); border: 1px solid var(--ao-line);
  box-shadow: var(--ao-shadow); text-decoration: none; color: inherit;
  display: flex; flex-direction: column; justify-content: space-between;
  transition: transform .2s ease;
}
.ao-jcard:hover { transform: translateY(-3px); }
.ao-jcard img { width: 100%; height: 175px; object-fit: cover; }
.ao-jcard-body { padding: 14px 16px; display: flex; flex-direction: column; gap: 6px; flex: 1; }
.ao-jcard-kicker {
  align-self: flex-start; background: var(--ao-bg-2); color: var(--ao-brand);
  font-size: .75rem; font-weight: 800; padding: 2px 10px; border-radius: 999px;
}
.ao-jcard h2, .ao-jcard h3 { font-size: 1.05rem; line-height: 1.45; margin: 0; color: var(--ao-ink); font-weight: 800; }
.ao-jcard p { font-size: .84rem; color: var(--ao-ink-2); margin: 0; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
.ao-horiz-bar {
  background: var(--ao-surface); border: 1.5px solid var(--ao-line); border-radius: 22px;
  padding: 14px 18px; box-shadow: var(--ao-shadow); display: flex; flex-direction: column; gap: 10px;
}
.ao-hbar-top {
  display: flex; align-items: center; justify-content: space-between; gap: 12px; flex-wrap: wrap;
  padding-bottom: 10px; border-bottom: 1px solid var(--ao-line);
}
.ao-hbar-kpis { display: flex; gap: 10px; flex-wrap: wrap; list-style: none; margin: 0; padding: 0; }
.ao-hbar-kpis li {
  background: var(--ao-bg-2); border-radius: 12px; padding: 6px 12px; display: flex; align-items: baseline; gap: 6px;
}
.ao-hbar-kpis b { font-size: 1.1rem; color: var(--ao-brand); }
.ao-hbar-kpis span { font-size: .78rem; color: var(--ao-muted); font-weight: 700; }
.ao-view-switch { display: inline-flex; background: var(--ao-bg-2); border-radius: 999px; padding: 3px; gap: 4px; }
.ao-view-btn {
  border: none; background: transparent; color: var(--ao-ink-2); font: inherit;
  font-size: .78rem; font-weight: 800; padding: 5px 12px; border-radius: 999px; cursor: pointer;
}
.ao-view-btn.is-on { background: var(--ao-brand); color: #fff; }
[data-theme="dark"] .ao-view-btn.is-on { color: #042f2e; }
.post-grid.is-list-view { grid-template-columns: 1fr !important; gap: 10px !important; }
.post-grid.is-list-view .post-card {
  display: grid; grid-template-columns: 200px 1fr; align-items: center;
}
.post-grid.is-list-view .post-card .ph { height: 125px; }
.post-grid.is-list-view .post-card .ph img { height: 100%; object-fit: cover; }

/* Hub Comparison Styles */
.ao-hub-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; margin-top: 18px; }
.ao-hub-card {
  background: var(--ao-surface); border: 1.5px solid var(--ao-line); border-radius: 22px;
  padding: 20px; box-shadow: var(--ao-shadow); display: flex; flex-direction: column; justify-content: space-between; gap: 14px;
}
.ao-hub-card.is-rec { border: 2px solid var(--ao-brand-2); box-shadow: 0 16px 40px rgba(13,148,136,0.18); }
.ao-hub-badge {
  display: inline-flex; align-items: center; gap: 6px; align-self: flex-start;
  background: var(--ao-bg-2); color: var(--ao-brand); padding: 4px 12px; border-radius: 999px; font-size: .78rem; font-weight: 800;
}
.ao-hub-card.is-rec .ao-hub-badge { background: #0d9488; color: #fff; }
.ao-hub-list { padding-right: 18px; font-size: .85rem; color: var(--ao-ink-2); line-height: 1.75; margin: 8px 0; }
.ao-hub-btn {
  display: inline-flex; justify-content: center; align-items: center;
  background: var(--ao-brand); color: #fff; text-decoration: none; font-weight: 800; font-size: .88rem;
  padding: 10px 16px; border-radius: 14px; transition: opacity .2s;
}
[data-theme="dark"] .ao-hub-btn { color: #042f2e; }
.ao-table-wrap { margin-top: 28px; background: var(--ao-surface); border-radius: 20px; border: 1px solid var(--ao-line); overflow: hidden; }
.ao-cmp-table { width: 100%; border-collapse: collapse; font-size: .86rem; text-align: right; }
.ao-cmp-table th, .ao-cmp-table td { padding: 12px 16px; border-bottom: 1px solid var(--ao-line); }
.ao-cmp-table th { background: var(--ao-bg-2); color: var(--ao-ink); font-weight: 900; }

@media (max-width: 860px) {
  .ao-journal-trio, .ao-hub-grid { grid-template-columns: 1fr; }
  .post-grid.is-list-view .post-card { grid-template-columns: 1fr; }
  .ao-topbar-inner { padding: 0 12px; }
}
'''

SHARED_JS = '''
(function(){
  var btn = document.querySelector('[data-ao-theme-toggle]');
  if (btn) {
    btn.addEventListener('click', function(){
      var d = document.documentElement;
      var next = d.dataset.theme === 'dark' ? 'light' : 'dark';
      d.dataset.theme = next;
      try { localStorage.setItem('abadis-theme', next); } catch(e){}
    });
  }
  // Rotator for A2
  var rot = document.querySelector('[data-ao-rotator]');
  if (rot) {
    var lines = [
      'کنترل عفونت و ایمنی بیمارستان',
      'استانداردهای نوین تجهیزات پزشکی',
      'راهنمای جامع مدیران و کادر درمان'
    ];
    var idx = 0;
    setInterval(function(){
      idx = (idx + 1) % lines.length;
      rot.textContent = lines[idx];
    }, 2200);
  }
  // Extra filters for A2 (reading time & audience)
  var rtimeBtns = document.querySelectorAll('[data-art-rtime]');
  var audBtns = document.querySelectorAll('[data-art-aud]');
  if (rtimeBtns.length || audBtns.length) {
    var curR = 'all', curA = 'all';
    function applyExtra() {
      var grid = document.getElementById('postGrid');
      if (!grid) return;
      var n = 0;
      grid.querySelectorAll('.post-card').forEach(function(c){
        var okR = curR === 'all' || c.getAttribute('data-rtime') === curR;
        var okA = curA === 'all' || c.getAttribute('data-aud') === curA;
        if (!okR || !okA) {
          c.style.display = 'none';
        } else {
          c.style.display = '';
          if (!c.hidden) n++;
        }
      });
      var cnt = document.querySelector('[data-news-count]');
      if (cnt && (curR !== 'all' || curA !== 'all')) {
        cnt.textContent = String(n).replace(/[0-9]/g, function(d){ return '۰۱۲۳۴۵۶۷۸۹'.charAt(+d); });
      }
    }
    rtimeBtns.forEach(function(b){
      b.addEventListener('click', function(){
        curR = b.getAttribute('data-art-rtime');
        rtimeBtns.forEach(function(x){ x.setAttribute('aria-pressed', x===b ? 'true' : 'false'); });
        applyExtra();
      });
    });
    audBtns.forEach(function(b){
      b.addEventListener('click', function(){
        curA = b.getAttribute('data-art-aud');
        audBtns.forEach(function(x){ x.setAttribute('aria-pressed', x===b ? 'true' : 'false'); });
        applyExtra();
      });
    });
  }
  // View switcher for A3
  var viewBtns = document.querySelectorAll('[data-ao-view]');
  if (viewBtns.length) {
    viewBtns.forEach(function(b){
      b.addEventListener('click', function(){
        var v = b.getAttribute('data-ao-view');
        viewBtns.forEach(function(x){ x.classList.toggle('is-on', x===b); });
        var g = document.getElementById('postGrid');
        if (g) g.classList.toggle('is-list-view', v === 'list');
      });
    });
  }
})();
'''

STAR_SVG = '<svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2l2.9 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l7.1-1.01L12 2z"/></svg>'

def topbar(active):
    def cls(k): return 'ao-tab is-active' if active == k else 'ao-tab'
    return f'''<div class="ao-topbar" role="navigation" aria-label="نوار مقایسه پیشنهادهای مقالات">
  <div class="ao-topbar-inner">
    <a class="ao-brand" href="index.html">
      <span>بازطراحی صفحه «مقالات» آبادیس</span>
      <span class="ao-brand-badge">هم‌خانواده قالب منتخب اخبار (Finalist D)</span>
    </a>
    <div class="ao-tabs">
      <a class="{cls('hub')}" href="index.html">مقایسه ۳ پیشنهاد</a>
      <a class="{cls('a1')}" href="option-1.html">پیشنهاد A1 (الگوی مستقیم اخبار)</a>
      <a class="{cls('a2')}" href="option-2.html">{STAR_SVG} پیشنهاد A2 (پیشنهادی — ویدیو + ترکیب D) <span class="ao-tab-rec">منتخب</span></a>
      <a class="{cls('a3')}" href="option-3.html">پیشنهاد A3 (مجله علمی ۳ ستونه + جدول)</a>
    </div>
    <div class="ao-actions">
      <button type="button" class="ao-theme-btn" data-ao-theme-toggle>حالت روشن / تیره</button>
      <a class="ao-tab" href="../articles/">صفحه اصلی مقالات</a>
    </div>
  </div>
</div>'''

def wrap_with_site_shell(title, active_key, main_inner):
    # Read site/articles/index.html to reuse exact site header & footer
    base = (ROOT / 'site/articles/index.html').read_text(encoding='utf-8')
    header_m = re.search(r'(<header class="header".*?</header>)', base, re.S)
    footer_m = re.search(r'(<footer class="site-footer">.*?</footer>)', base, re.S)
    header_html = header_m.group(1) if header_m else ''
    footer_html = footer_m.group(1) if footer_m else ''
    return f'''<!DOCTYPE html>
<html lang="fa-IR" dir="rtl" data-theme="light">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="robots" content="noindex, nofollow">
<script>(function(){{var t;try{{var q=new URLSearchParams(location.search).get('theme');if(q){{localStorage.setItem('abadis-theme',q)}}t=localStorage.getItem('abadis-theme')}}catch(e){{}}var d=document.documentElement;d.dataset.theme=(t==='dark'||t==='noir')?t:'light';d.classList.add('js')}})();</script>
<link rel="preload" href="../assets/fonts/kalameh/KalamehWeb-FaNum-Regular.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="../assets/fonts/kalameh/KalamehWeb-FaNum-Black.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="../assets/css/site.css?v=20261028f">
<link rel="stylesheet" href="../assets/css/boss-order.css?v=20261028f">
<link rel="stylesheet" href="../assets/css/footer-motion.css">
<link rel="stylesheet" href="../assets/css/news-finalist.css">
<style>{SHARED_CSS}</style>
</head>
<body>
{topbar(active_key)}
{header_html}
<main id="main">
{main_inner}
</main>
{footer_html}
<script src="../assets/js/site.js?v=20261028f" defer></script>
<script src="../assets/js/news-finalist.js" defer></script>
<script>{SHARED_JS}</script>
</body>
</html>
'''

# ------------------------------------------------------------------ Option A1
def build_a1():
    f0 = ENRICHED[0]
    feature_html = (
        f'<a class="news-feature" data-news-feature href="{f0["href"]}">'
        f'<img src="{f0["img"]}" alt="{esc(f0["title"])}" decoding="async">'
        f'<div class="news-feature-body">'
        f'<div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap">'
        f'<span class="news-kicker" data-news-kicker>تازه‌ترین مقاله علمی</span>'
        f'<span class="art-aud-tag">زمان مطالعه: {f0["mins_fa"]} دقیقه</span>'
        f'<span class="art-aud-tag">{esc(f0["topic_label"])}</span>'
        f'</div>'
        f'<time datetime="{f0["date_iso"]}">{f0["date_fa"]}</time>'
        f'<h2>{esc(f0["title"])}</h2>'
        f'<p>{esc(f0["excerpt"])}</p>'
        f'</div></a>'
    )
    main = f'''<section class="news-d articles-d" data-news-finalist>
  <div class="wrap">
    <p class="crumbs"><a href="../">خانه</a> › <a href="index.html">پیشنهادهای مقالات</a> › پیشنهاد A1 (الگوی مستقیم آخرین اخبار)</p>
    <h1>دانشنامه و <em>مقالات علمی</em></h1>
    <p class="lead">الگوی مستقیم هم‌خانواده «آخرین اخبار» (ترکیب منتخب D): کارت شاخص ویژه + ماتریس ۴ شاخص آماری + ۶ سرفصل علمی و فیلتر سال انتشار برای هر ۱۱۲ مقاله</p>
    <div class="news-d-stage">
      {feature_html}
      <aside class="news-panel">
        <ul class="news-dash">
          <li><b>{digits(STATS["total"], "fa")}</b><span>مقاله تخصصی</span></li>
          <li><b>{digits(STATS["n_topics"], "fa")}</b><span>محور علمی</span></li>
          <li><b>{digits(STATS["n_years"], "fa")}</b><span>سال پوشش</span></li>
          <li><b>{year_label(STATS["latest"], "fa")}</b><span>تازه‌ترین سال</span></li>
        </ul>
        <p class="news-lab">محور علمی و تخصصی</p>
        <div class="news-topics" role="group" aria-label="محور علمی">{topic_buttons_html()}</div>
        <p class="news-lab">سال انتشار</p>
        <div class="news-years" role="group" aria-label="سال انتشار">{year_buttons_html()}</div>
        <p class="news-live"><span data-news-count>{digits(STATS["total"], "fa")}</span> مقاله علمی</p>
      </aside>
    </div>
  </div>
</section>
<section class="section news-d-page"><div class="wrap">
  <h2 class="news-archive-title">آرشیو کامل ۱۱۲ مقاله علمی و تخصصی آبادیس</h2>
  <div class="post-grid" id="postGrid" data-paged="12">{ALL_CARDS_HTML}</div>
  <p class="news-empty" data-news-empty hidden>مقاله‌ای با این ترکیب پیدا نشد. <button type="button" data-news-reset>نمایش همه مقالات</button></p>
</div></section>'''
    return wrap_with_site_shell('پیشنهاد A1 — الگوی مستقیم آخرین اخبار (Finalist D) | مقالات آبادیس', 'a1', main)

# ------------------------------------------------------------------ Option A2 (Recommended)
def build_a2():
    f0 = ENRICHED[0]
    feature_html = (
        f'<a class="news-feature" data-news-feature href="{f0["href"]}">'
        f'<img src="{f0["img"]}" alt="{esc(f0["title"])}" decoding="async">'
        f'<div class="news-feature-body">'
        f'<div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap">'
        f'<span class="news-kicker" data-news-kicker>تازه‌ترین مقاله علمی</span>'
        f'<span class="art-aud-tag">زمان مطالعه: {f0["mins_fa"]} دقیقه</span>'
        f'<span class="art-aud-tag">{esc(f0["aud_label"])}</span>'
        f'</div>'
        f'<time datetime="{f0["date_iso"]}">{f0["date_fa"]}</time>'
        f'<h2>{esc(f0["title"])}</h2>'
        f'<p>{esc(f0["excerpt"])}</p>'
        f'</div></a>'
    )
    main = f'''<section class="ao-hero-video-sec">
  <video autoplay muted loop playsinline webkit-playsinline disablepictureinpicture disableremoteplayback preload="metadata" tabindex="-1" aria-hidden="true" poster="../assets/media/hero-customers-poster.jpg?v=20261028f">
    <source src="../assets/media/hero-customers.mp4?v=20261028f" type="video/mp4">
  </video>
  <div class="ao-hero-overlay"></div>
  <div class="wrap ao-hero-content">
    <p class="crumbs" style="color:#bfe6e8"><a href="../" style="color:#5eead4">خانه</a> › <a href="index.html" style="color:#5eead4">پیشنهادهای مقالات</a> › پیشنهاد A2 (پیشنهادی)</p>
    <h1 style="font-size:clamp(1.9rem,3.2vw,2.75rem);color:#fff;margin:6px 0">دانشنامه و <em>مقالات علمی</em></h1>
    <div class="ao-rotator">
      <span class="ao-rot-main">دانشنامه تخصصی و مقالات علمی آبادیس،</span>
      <span class="ao-rot-sub" data-ao-rotator>کنترل عفونت و ایمنی بیمارستان</span>
    </div>
  </div>
</section>
<section class="news-d articles-d" data-news-finalist style="padding-top:20px">
  <div class="wrap">
    <div class="news-d-stage">
      {feature_html}
      <aside class="news-panel">
        <ul class="news-dash">
          <li><b>{digits(STATS["total"], "fa")}</b><span>مقاله تخصصی</span></li>
          <li><b>{digits(STATS["n_topics"], "fa")}</b><span>محور علمی</span></li>
          <li><b>{digits(STATS["n_years"], "fa")}</b><span>سال پوشش</span></li>
          <li><b>{year_label(STATS["latest"], "fa")}</b><span>تازه‌ترین سال</span></li>
        </ul>
        <p class="news-lab">محور علمی و تخصصی</p>
        <div class="news-topics" role="group" aria-label="محور علمی">{topic_buttons_html()}</div>
        <p class="news-lab">سال انتشار</p>
        <div class="news-years" role="group" aria-label="سال انتشار">{year_buttons_html()}</div>
        <div class="ao-extra-filters" role="group" aria-label="فیلتر زمان مطالعه و مخاطب">
          <span class="news-lab" style="margin:0 0 0 6px">زمان مطالعه:</span>
          <button type="button" data-art-rtime="all" aria-pressed="true">همه</button>
          <button type="button" data-art-rtime="fast" aria-pressed="false">مطالعه سریع (زیر ۳ دقیقه)</button>
          <button type="button" data-art-rtime="deep" aria-pressed="false">مقالات جامع (بالای ۴ دقیقه)</button>
        </div>
        <div class="ao-extra-filters" role="group" aria-label="مخاطب تخصصی">
          <span class="news-lab" style="margin:0 0 0 6px">مخاطب:</span>
          <button type="button" data-art-aud="all" aria-pressed="true">همه مخاطبان</button>
          <button type="button" data-art-aud="clinical" aria-pressed="false">کادر درمان و اتاق عمل</button>
          <button type="button" data-art-aud="infection" aria-pressed="false">مسئولین کنترل عفونت</button>
          <button type="button" data-art-aud="procurement" aria-pressed="false">مدیران خرید</button>
        </div>
        <p class="news-live"><span data-news-count>{digits(STATS["total"], "fa")}</span> مقاله علمی</p>
      </aside>
    </div>
  </div>
</section>
<section class="section news-d-page"><div class="wrap">
  <h2 class="news-archive-title">آرشیو مقالات علمی با برچسب مخاطب و زمان مطالعه</h2>
  <div class="post-grid" id="postGrid" data-paged="12">{ALL_CARDS_HTML}</div>
  <p class="news-empty" data-news-empty hidden>مقاله‌ای با این ترکیب پیدا نشد. <button type="button" data-news-reset>نمایش همه مقالات</button></p>
</div></section>'''
    return wrap_with_site_shell('پیشنهاد A2 (پیشنهادی) — هدر ویدیویی + استیج دوگانه ترکیب D | مقالات آبادیس', 'a2', main)

# ------------------------------------------------------------------ Option A3
def build_a3():
    f0 = ENRICHED[0]
    f_guide = next((x for x in ENRICHED if x['topic'] == 'guide'), ENRICHED[2])
    f_inf = next((x for x in ENRICHED if x['topic'] == 'infection'), ENRICHED[6])
    trio_html = ''
    for kicker, item in [
        ('تازه‌ترین مقاله علمی', f0),
        ('پرمطالعه‌ترین راهنمای خرید', f_guide),
        ('منتخب کنترل عفونت بیمارستانی', f_inf),
    ]:
        trio_html += (
            f'<a class="ao-jcard" href="{item["href"]}">'
            f'<img src="{item["img"]}" alt="{esc(item["title"])}" decoding="async">'
            f'<div class="ao-jcard-body">'
            f'<div style="display:flex;justify-content:space-between;align-items:center;gap:6px">'
            f'<span class="ao-jcard-kicker">{esc(kicker)}</span>'
            f'<span class="art-aud-tag">{item["mins_fa"]} دقیقه</span>'
            f'</div>'
            f'<h3>{esc(item["title"])}</h3>'
            f'<p>{esc(item["excerpt"])}</p>'
            f'<time datetime="{item["date_iso"]}" style="font-size:.76rem;color:var(--ao-muted)">{item["date_fa"]}</time>'
            f'</div></a>'
        )
    main = f'''<section class="news-d articles-d" data-news-finalist>
  <div class="wrap">
    <p class="crumbs"><a href="../">خانه</a> › <a href="index.html">پیشنهادهای مقالات</a> › پیشنهاد A3 (الگوی مجله علمی ۳ ستونه)</p>
    <h1>مجله علمی و <em>دانشنامه مقالات</em></h1>
    <p class="lead">ویترین ۳ مقاله برگزیده در بالای صفحه + نوار افقی هوشمند فیلترهای «آخرین اخبار» (ماتریس آمار، ۶ محور علمی، سال انتشار) و سوییچ نمای کارت / فهرست مرجع</p>
    <div class="ao-journal-trio">{trio_html}</div>
    <div class="ao-horiz-bar">
      <div class="ao-hbar-top">
        <ul class="ao-hbar-kpis">
          <li><b>{digits(STATS["total"], "fa")}</b><span>مقاله تخصصی</span></li>
          <li><b>{digits(STATS["n_topics"], "fa")}</b><span>محور علمی</span></li>
          <li><b>{digits(STATS["n_years"], "fa")}</b><span>سال پوشش</span></li>
          <li><b>{year_label(STATS["latest"], "fa")}</b><span>تازه‌ترین سال</span></li>
        </ul>
        <div style="display:flex;align-items:center;gap:12px;flex-wrap:wrap">
          <p class="news-live" style="margin:0"><span data-news-count>{digits(STATS["total"], "fa")}</span> مقاله فعال</p>
          <div class="ao-view-switch" role="group" aria-label="تغییر نما">
            <button type="button" class="ao-view-btn is-on" data-ao-view="grid">نمای کارت</button>
            <button type="button" class="ao-view-btn" data-ao-view="list">نمای فهرست مرجع</button>
          </div>
        </div>
      </div>
      <div>
        <span class="news-lab">فیلتر محور علمی (الگوی آخرین اخبار):</span>
        <div class="news-topics" role="group" aria-label="محور علمی" style="margin-top:6px">{topic_buttons_html()}</div>
      </div>
      <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap">
        <span class="news-lab" style="margin:0">فیلتر سال انتشار:</span>
        <div class="news-years" role="group" aria-label="سال انتشار">{year_buttons_html()}</div>
      </div>
    </div>
  </div>
</section>
<section class="section news-d-page"><div class="wrap">
  <h2 class="news-archive-title">بانک مقالات علمی و تخصصی (قابلیت تغییر نمای کارت / فهرست)</h2>
  <div class="post-grid" id="postGrid" data-paged="12">{ALL_CARDS_HTML}</div>
  <p class="news-empty" data-news-empty hidden>مقاله‌ای با این ترکیب پیدا نشد. <button type="button" data-news-reset>نمایش همه مقالات</button></p>
</div></section>'''
    return wrap_with_site_shell('پیشنهاد A3 — الگوی مجله علمی ۳ ستونه + نوار فیلتر اخبار | مقالات آبادیس', 'a3', main)

# ------------------------------------------------------------------ Hub Index
def build_hub():
    main = f'''<section class="news-d articles-d">
  <div class="wrap">
    <p class="crumbs"><a href="../">خانه</a> › <a href="../articles/">مقالات</a> › مقایسه ۳ پیشنهاد طراحی صفحه مقالات</p>
    <h1>مقایسه ۳ پیشنهاد طراحی صفحه <em>مقالات</em> (هم‌خانواده آخرین اخبار)</h1>
    <p class="lead">طبق دستور مدیریت («برای مقالات هم یک تمپلیت شبیه اخبار درست کن — ۳ پیشنهاد برای انتخاب»)، هر ۳ پیشنهاد بر پایه معماری تأییدشده «آخرین اخبار» (Finalist D) و با استفاده از ۱۱۲ مقاله واقعی آرشیو آبادیس طراحی شده‌اند.</p>
    <div class="ao-hub-grid">
      <article class="ao-hub-card">
        <div>
          <span class="ao-hub-badge">پیشنهاد اول · A1</span>
          <h2 style="font-size:1.2rem;margin:10px 0 6px">پیشنهاد A1 — الگوی مستقیم آخرین اخبار (ترکیب D)</h2>
          <p style="font-size:.88rem;color:var(--ao-ink-2)">قرینه ۱ به ۱ قالب تأییدشده «آخرین اخبار»: استیج دوگانه با کارت شاخص بزرگ در راست و پنل کنترلی در چپ شامل ماتریس ۴ شاخص آماری، ۶ محور علمی مقالات و فیلتر سال انتشار.</p>
          <ul class="ao-hub-list">
            <li>یکپارچگی ۱۰۰٪ بصری و ساختاری با صفحه آخرین اخبار</li>
            <li>دسته‌بندی هوشمند ۱۱۲ مقاله در ۶ محور علمی و تخصصی</li>
            <li>بروزرسانی خودکار کارت شاخص با تغییر فیلتر موضوع یا سال</li>
          </ul>
        </div>
        <a class="ao-hub-btn" href="option-1.html">مشاهده زنده پیشنهاد A1 ←</a>
      </article>

      <article class="ao-hub-card is-rec">
        <div>
          <span class="ao-hub-badge">{STAR_SVG} پیشنهاد دوم · A2 (پیشنهاد منتخب)</span>
          <h2 style="font-size:1.2rem;margin:10px 0 6px">پیشنهاد A2 — هدر ویدیویی + استیج دوگانه ترکیب D + فیلتر مخاطب</h2>
          <p style="font-size:.88rem;color:var(--ao-ink-2)">ترکیب هدر ویدیویی سینمایی آبادیس و تایپوگرافی چرخشی Kalameh Black با استیج کامل «آخرین اخبار» (Finalist D) به همراه فیلتر زمان مطالعه و برچسب مخاطب تخصصی (کادر درمان، کنترل عفونت، مدیران خرید).</p>
          <ul class="ao-hub-list">
            <li>هماهنگی کامل با هدر ویدیویی صفحات آشنایی با ما و مشتریان</li>
            <li>حفظ کامل ماتریس آمار، ۶ محور علمی و فیلتر سال انتشار اخبار</li>
            <li>افزودن فیلتر زمان مطالعه و تفکیک مخاطبان بیمارستانی</li>
          </ul>
        </div>
        <a class="ao-hub-btn" href="option-2.html">مشاهده زنده پیشنهاد A2 (پیشنهادی) ←</a>
      </article>

      <article class="ao-hub-card">
        <div>
          <span class="ao-hub-badge">پیشنهاد سوم · A3</span>
          <h2 style="font-size:1.2rem;margin:10px 0 6px">پیشنهاد A3 — مجله علمی ۳ ستونه + نوار فیلتر اخبار + سوییچ نما</h2>
          <p style="font-size:.88rem;color:var(--ao-ink-2)">نمایش هم‌زمان ۳ مقاله شاخص در بالای صفحه (تازه‌ترین مقاله، راهنمای خرید، منتخب کنترل عفونت) در کنار نوار افقی فیلترهای آخرین اخبار و قابلیت تغییر بین «نمای کارت» و «نمای فهرست مرجع».</p>
          <ul class="ao-hub-list">
            <li>نمایش ۳ مقاله کلیدی از ۳ حوزه متفاوت در نگاه اول</li>
            <li>نوار کنترلی افقی شامل ۴ شاخص آماری، موضوعات و سال‌ها</li>
            <li>قابلیت تغییر نما به فهرست فشرده مرجع برای پژوهشگران</li>
          </ul>
        </div>
        <a class="ao-hub-btn" href="option-3.html">مشاهده زنده پیشنهاد A3 ←</a>
      </article>
    </div>

    <div class="ao-table-wrap">
      <table class="ao-cmp-table">
        <thead>
          <tr>
            <th>ویژگی / معیار مقایسه</th>
            <th>پیشنهاد A1 (الگوی مستقیم اخبار)</th>
            <th>پیشنهاد A2 (پیشنهادی — ویدیو + ترکیب D)</th>
            <th>پیشنهاد A3 (مجله ۳ ستونه + فهرست)</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>ساختار هدر و استیج بالا</strong></td>
            <td>استیج دوگانه مستقیم Finalist D (کارت شاخص + پنل فیلتر)</td>
            <td>هدر ویدیویی + تایپوگرافی چرخشی + استیج دوگانه Finalist D</td>
            <td>ویترین ۳ کارته مجله علمی + نوار افقی هوشمند Finalist D</td>
          </tr>
          <tr>
            <td><strong>ماتریس ۴ شاخص آماری (۱۱۲ مقاله · ۶ محور · ۵ سال · ۱۴۰۵)</strong></td>
            <td>موجود در پنل چپ (مشابه اخبار)</td>
            <td>موجود در پنل چپ (مشابه اخبار)</td>
            <td>موجود در نوار افقی بالای آرشیو</td>
          </tr>
          <tr>
            <td><strong>فیلتر ۶ محور علمی + سال انتشار (۱۴۰۵ تا ۱۴۰۰ و قبل)</strong></td>
            <td>کامل و تعاملی</td>
            <td>کامل و تعاملی</td>
            <td>کامل و تعاملی</td>
          </tr>
          <tr>
            <td><strong>فیلتر زمان مطالعه و مخاطب تخصصی بیمارستانی</strong></td>
            <td>نمایش زمان مطالعه روی کارت‌ها</td>
            <td>فیلتر تعاملی زمان مطالعه + فیلتر مخاطب تخصصی</td>
            <td>نمایش زمان مطالعه + سوییچ نمای کارت / فهرست مرجع</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</section>'''
    return wrap_with_site_shell('مقایسه ۳ پیشنهاد طراحی صفحه «مقالات» — مخازن طبی آبادیس', 'hub', main)

(OUT / 'option-1.html').write_text(build_a1(), encoding='utf-8')
(OUT / 'option-2.html').write_text(build_a2(), encoding='utf-8')
(OUT / 'option-3.html').write_text(build_a3(), encoding='utf-8')
(OUT / 'index.html').write_text(build_hub(), encoding='utf-8')
print("Generated site/articles-options/{index,option-1,option-2,option-3}.html successfully.")
