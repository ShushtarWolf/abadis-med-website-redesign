"""Calm Iran-map home hero — sequential centre dots, shared fa/en/ar."""
import json
from pathlib import Path

from lib import esc

_DATA = Path(__file__).resolve().parent / 'data'

# Same province order as the dealers page (geo west → east feel in animation).
PROVINCES = [
    'آذربایجان شرقی', 'آذربایجان غربی', 'اردبیل', 'اصفهان', 'البرز', 'ایلام', 'بوشهر', 'تهران',
    'چهارمحال و بختیاری', 'خراسان جنوبی', 'خراسان رضوی', 'خراسان شمالی', 'خوزستان', 'زنجان', 'سمنان',
    'سیستان و بلوچستان', 'فارس', 'قزوین', 'قم', 'کردستان', 'کرمان', 'کرمانشاه', 'کهگیلویه و بویراحمد',
    'گلستان', 'گیلان', 'لرستان', 'مازندران', 'مرکزی', 'هرمزگان', 'همدان', 'یزد',
]

MAP_ARIA = {
    'fa': 'نقشه ایران — حضور آبادیس در استان‌ها',
    'en': 'Map of Iran — Abadis presence across provinces',
    'ar': 'خريطة إيران — حضور آباديس في المحافظات',
}


def _iran_geo():
    return json.loads((_DATA / 'iran_provinces.json').read_text(encoding='utf-8'))


def map_figure(prefix='', lang='fa'):
    """SVG Iran outline + one dot per province (no counts in copy)."""
    m = _iran_geo()
    T = MAP_ARIA.get(lang, MAP_ARIA['fa'])
    paths = []
    dots = []
    for i, name in enumerate(PROVINCES):
        v = m['p'].get(name)
        if not v:
            continue
        paths.append(
            f'<path class="home-map-land" d="{v["d"]}" tabindex="-1" aria-hidden="true"></path>'
        )
        cx, cy = v['c']
        dots.append(
            f'<circle class="home-map-dot" cx="{cx}" cy="{cy}" r="5.5" data-seq="{i}" aria-hidden="true"></circle>'
        )
    return (
        f'<figure class="home-map-figure" data-home-map-figure>'
        f'<svg class="home-map-svg" viewBox="0 0 {m["w"]} {m["h"]}" role="img" aria-label="{esc(T)}">'
        f'<g class="home-map-lands">{"".join(paths)}</g>'
        f'<g class="home-map-dots">{"".join(dots)}</g>'
        f'</svg></figure>'
    )


def render(prefix, lang, kicker, h1, sub, catalogue_href, quote_href, catalogue_label, quote_label, track_suffix=''):
    """Full hero section markup."""
    p = prefix or ''
    ts = track_suffix or lang
    fig = map_figure(p, lang)
    return f'''  <section class="home-map" data-tone="dark" data-home-map id="intro" aria-label="{esc(MAP_ARIA.get(lang, MAP_ARIA["fa"]))}">
    <div class="home-map-bg" aria-hidden="true"></div>
    <div class="wrap home-map-inner">
      <div class="home-map-copy">
        <p class="home-map-kicker">{esc(kicker)}</p>
        <h1>{esc(h1)}</h1>
        <p class="home-map-sub">{esc(sub)}</p>
        <div class="hero-actions">
          <a class="btn btn-primary" href="{esc(catalogue_href)}" target="_blank" rel="noopener" data-track="catalogue_download" data-track-label="home_hero_catalogue_{ts}">{esc(catalogue_label)}</a>
          <a class="btn btn-ghost" href="{esc(quote_href)}" data-track="contact_click" data-track-label="home_hero_quote_{ts}">{esc(quote_label)}</a>
        </div>
      </div>
      {fig}
    </div>
  </section>'''


def extra_head(prefix=''):
    p = prefix or ''
    return (
        f'<link rel="stylesheet" href="{p}assets/css/home.css">\n'
        f'<script src="{p}assets/js/home-map-hero.js" defer></script>\n'
    )
