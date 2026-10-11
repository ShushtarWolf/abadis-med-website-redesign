"""Test pages that are not linked from the site (noindex): hero-test/birds/.

Birds rise from the Zagros mountains (same painting / haze / copy as the home hero, light mode)
and flock into the Abadis mark. Assets: tools/redesign/make_birds_mark.py.
"""
from layout import page
from lib import esc
import pages_home

P = '../../'


def birds(write):
    b = P + 'csr/img/hero/'
    main = f'''  <section class="bt-stage" id="hero" aria-label="نجات زاگرس">
    <div class="bt-bg" aria-hidden="true">
      <picture>
        <source type="image/webp" srcset="{b}bg-dry-1280.webp 1280w, {b}bg-dry.webp 1920w" sizes="(max-aspect-ratio: 16/9) 177.78vh, 100vw">
        <img src="{b}bg-dry.jpg" srcset="{b}bg-dry-1280.jpg 1280w, {b}bg-dry.jpg 1920w" sizes="(max-aspect-ratio: 16/9) 177.78vh, 100vw" alt="" width="1920" height="1080" decoding="async" fetchpriority="high">
      </picture>
    </div>
    <div class="zh-veil" aria-hidden="true"></div>
    <img class="bt-mark" id="btMark" src="mark.png" alt="" aria-hidden="true" width="298" height="309">
    <canvas class="bt-canvas" id="btCanvas" aria-hidden="true"></canvas>
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
<link rel="preload" as="image" href="{b}bg-dry.webp" type="image/webp">
<link rel="stylesheet" href="{P}csr/zagros-hero.css">
<link rel="stylesheet" href="{P}assets/css/home.css">
<link rel="stylesheet" href="birds.css">'''
    scripts = '<script src="mark-points.js" defer></script>\n<script src="birds.js" defer></script>\n'
    html = page(P, None, 'آزمایش هیرو: پرندگان زاگرس — مخازن طبی آبادیس', pages_home.HOME_DESC, main,
                fa_path='hero-test/birds/', canonical_path='hero-test/birds/',
                extra_head=extra_head, scripts=scripts, main_class='home-page bt-page', body_class='home')
    write('hero-test/birds/index.html', html)


GROUPS = {'herotest': birds}
