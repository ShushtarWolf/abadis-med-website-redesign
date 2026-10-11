"""Test pages that are not linked from the site (noindex): hero-test/birds/.

A painted sky (the Zagros painting continued upward) above the Zagros scene. Birds rise from
behind the ridge and flock into the Abadis mark in the sky; scrolling down sends them back
behind the mountains (scrubbed, reversible). Assets: make_birds_mark.py, make_birds_scene.py.
"""
from layout import page
from lib import esc
import pages_home

P = '../../'


def birds(write):
    b = P + 'csr/img/hero/'
    main = f'''  <section class="bt-scene" id="hero" aria-label="نجات زاگرس">
    <div class="bt-sky" aria-hidden="true">
      <img src="sky.webp" srcset="sky-1280.webp 1280w, sky.webp 1920w" sizes="(max-aspect-ratio: 16/9) 177.78vh, 100vw" alt="" width="1920" height="1080" decoding="async" fetchpriority="high">
      <div class="bt-sky-veil"></div>
    </div>
    <div class="bt-stage" aria-hidden="true">
      <picture>
        <source type="image/webp" srcset="{b}bg-dry-1280.webp 1280w, {b}bg-dry.webp 1920w" sizes="(max-aspect-ratio: 16/9) 177.78vh, 100vw">
        <img src="{b}bg-dry.jpg" srcset="{b}bg-dry-1280.jpg 1280w, {b}bg-dry.jpg 1920w" sizes="(max-aspect-ratio: 16/9) 177.78vh, 100vw" alt="" width="1920" height="1080" decoding="async">
      </picture>
    </div>
    <img class="bt-mark" id="btMark" src="mark.png" alt="" aria-hidden="true" width="298" height="309">
    <div class="bt-canvas-wrap" aria-hidden="true"><canvas class="bt-canvas" id="btCanvas"></canvas></div>
    <div class="bt-ridge" aria-hidden="true">
      <img src="ridge.webp" alt="" width="1920" height="1080" decoding="async">
      <div class="zh-veil"></div>
    </div>
    <div class="bt-copy csr-hero home-zagros-hero">
      <div>
        <span class="chip">پویش نجات زاگرس · کاشت نهال بلوط</span>
        <h1>نجات زاگرس،‌مسئولیت اجتماعی آبادیس</h1>
        <p class="lead">{esc(pages_home.ZAGROS_LEAD)}</p>
        <div class="hero-actions" style="justify-content:center">
          <a class="btn btn-primary" href="{P}csr/">ادامه در توسعه پایدار</a>
        </div>
      </div>
    </div>
  </section>'''
    extra_head = f'''<meta name="robots" content="noindex,nofollow">
<link rel="preload" as="image" href="sky.webp" type="image/webp">
<link rel="stylesheet" href="{P}csr/zagros-hero.css">
<link rel="stylesheet" href="{P}assets/css/home.css">
<link rel="stylesheet" href="birds.css">'''
    scripts = '<script src="mark-points.js" defer></script>\n<script src="ridge.js" defer></script>\n<script src="birds.js" defer></script>\n'
    html = page(P, None, 'آزمایش هیرو: پرندگان زاگرس — مخازن طبی آبادیس', pages_home.HOME_DESC, main,
                fa_path='hero-test/birds/', canonical_path='hero-test/birds/',
                extra_head=extra_head, scripts=scripts, main_class='home-page bt-page', body_class='home')
    write('hero-test/birds/index.html', html)


GROUPS = {'herotest': birds}
