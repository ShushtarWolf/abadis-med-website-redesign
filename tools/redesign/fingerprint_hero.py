"""Home fingerprint hero — living ridge lines (اثر یک سرانگشت).

Adapted from the approved standalone HTML into the site shell:
Kalameh only, shared header/nav, products CTA, FA/EN/AR strings.
"""
from html import escape as esc

V = '20261101a'

T = {
    'fa': dict(
        aria='اثر یک سرانگشت',
        h1_before='ما به اندازهٔ یک ',
        h1_em='سرانگشت',
        h1_after=' اثر می‌گذاریم',
        to_prefix='به',
        chips=('شما', 'طبیعت', 'جهان'),
        caps=(
            'خطوط اثر انگشت، هویت یک انسان',
            'همین خطوط، در خطوط تراز کوه و حلقه‌های تنهٔ درخت',
            'ردِ یک اثر، در هر نقطه از جهان',
        ),
        cta='مشاهدهٔ محصولات',
        products='products/',
        hint='انگشت یا ماوس را روی صفحه بگذارید',
        count='{n} اثر از شما ثبت شد',
        digits='fa',
    ),
    'en': dict(
        aria='A fingertip mark',
        h1_before='We leave a mark as light as a ',
        h1_em='fingertip',
        h1_after='',
        to_prefix='to',
        chips=('you', 'nature', 'the world'),
        caps=(
            'Fingerprint lines, a human identity',
            'The same lines in mountain contours and tree rings',
            'One mark, felt anywhere in the world',
        ),
        cta='View products',
        products='products/',
        hint='Place your finger or mouse on the page',
        count='{n} marks recorded from you',
        digits='en',
    ),
    'ar': dict(
        aria='أثر بصمة إصبع',
        h1_before='نترك أثراً بقدر ',
        h1_em='أنملة',
        h1_after='',
        to_prefix='إلى',
        chips=('أنتم', 'الطبيعة', 'العالم'),
        caps=(
            'خطوط البصمة، هوية إنسان',
            'الخطوط نفسها في خطوط الجبال وحلقات جذوع الأشجار',
            'أثر واحد يُحسّ في أي نقطة من العالم',
        ),
        cta='عرض المنتجات',
        products='منتجات/',
        hint='ضع إصبعك أو المؤشر على الصفحة',
        count='{n} أثر سُجّل منكم',
        digits='ar',
    ),
}


def head(p):
    return f'<link rel="stylesheet" href="{p}assets/css/fingerprint-hero.css?v={V}">'


def scripts(p):
    return f'<script src="{p}assets/js/fingerprint-hero.js?v={V}" defer></script>\n'


def hero(p, lang='fa'):
    t = T[lang]
    sep = '،' if lang == 'fa' else ','
    chips = ''.join(
        f'<span>{esc(t["to_prefix"])}</span>'
        f'<button class="fp-chip" type="button" data-mode="{i}" '
        f'aria-pressed="{"true" if i == 0 else "false"}">{esc(label)}</button>'
        + ('' if i == len(t['chips']) - 1 else f'<span>{sep}</span>')
        for i, label in enumerate(t['chips'])
    )
    caps_json = esc('|'.join(t['caps']))
    return f'''  <section class="fp-hero" id="intro" data-tone="dark" data-lang="{esc(lang)}" data-digits="{esc(t['digits'])}" data-count-tpl="{esc(t['count'])}" data-caps="{caps_json}" aria-label="{esc(t['aria'])}">
    <div class="fp-stage" aria-hidden="true"><canvas class="fp-canvas"></canvas></div>
    <div class="fp-shade" aria-hidden="true"></div>
    <div class="fp-ui">
      <div class="fp-main">
        <h1 class="fp-rise" style="--d:1.4s">{esc(t['h1_before'])}<em>{esc(t['h1_em'])}</em>{esc(t['h1_after'])}</h1>
        <div class="fp-to fp-rise" style="--d:1.8s" role="group" aria-label="{esc(t['aria'])}">{chips}</div>
        <p class="fp-cap fp-rise" style="--d:2s" aria-live="polite">{esc(t['caps'][0])}</p>
        <a class="fp-cta fp-rise" style="--d:2.2s" href="{p}{esc(t['products'])}" data-track="products_click" data-track-label="home_fp_hero">
          {esc(t['cta'])}
          <svg width="18" height="12" viewBox="0 0 18 12" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M17 6H1M6 1 1 6l5 5"/></svg>
        </a>
      </div>
      <div class="fp-foot fp-rise" style="--d:2.6s">
        <canvas class="fp-ecg" width="132" height="34" aria-hidden="true"></canvas>
        <span class="fp-hint">{esc(t['hint'])}</span>
      </div>
    </div>
  </section>'''
