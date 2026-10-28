#!/usr/bin/env python3
"""Build 3 distinct graphical/video Hero proposals (C-H1, C-H2, C-H3) for «ارتباط با ما» (/contact/)
at site/contact-hero-options/ per [t285u]."""
import re
import sys
from pathlib import Path

ROOT = Path('/workspace/abadis-med-website-redesign')
sys.path.insert(0, str(ROOT / 'tools/redesign'))

import pages_company as PC
from layout import page

OUT = ROOT / 'site/contact-hero-options'
OUT.mkdir(parents=True, exist_ok=True)

EXTRA_CSS = """<style>
.cho-bar {
  position: sticky; top: 0; z-index: 260;
  background: rgba(4, 32, 35, 0.95); backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(94, 234, 212, 0.28);
  padding: 10px 18px; color: #ecfeff;
}
.cho-bar-inner {
  max-width: 1220px; margin: 0 auto;
  display: flex; align-items: center; justify-content: space-between; gap: 12px; flex-wrap: wrap;
}
.cho-pills { display: flex; flex-wrap: wrap; gap: 8px; }
.cho-pill {
  padding: 6px 14px; border-radius: 999px; font-size: .82rem; font-weight: 800;
  color: #d7f4f4; text-decoration: none; border: 1px solid rgba(255,255,255,0.18);
  background: rgba(255,255,255,0.06);
}
.cho-pill.is-active {
  background: linear-gradient(135deg, #0d9488 0%, #05686b 100%);
  color: #fff; border-color: #5eead4;
}
.cho-rec {
  background: #5eead4; color: #042f2e; padding: 1px 7px; border-radius: 999px;
  font-size: .7rem; font-weight: 900; margin-inline-start: 4px;
}

/* Option C-H2: Split Interactive B2B Command Hero */
.cho-h2-grid {
  display: grid; grid-template-columns: 1.15fr 1fr; gap: 28px; align-items: center;
}
.cho-b2b-card {
  background: rgba(6, 36, 40, 0.84); backdrop-filter: blur(14px);
  border: 1.5px solid rgba(94, 234, 212, 0.45); border-radius: 24px;
  padding: 20px; color: #ecfeff; box-shadow: 0 22px 48px rgba(0,0,0,0.34);
}
.cho-b2b-tabs { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-bottom: 14px; }
.cho-b2b-tab {
  padding: 10px 8px; border-radius: 12px; border: 1px solid rgba(94,234,212,0.28);
  background: rgba(255,255,255,0.06); color: #ecfeff; font: inherit; font-size: .8rem; font-weight: 800;
  cursor: pointer; text-align: center; transition: all .2s ease;
}
.cho-b2b-tab.is-on {
  background: #5eead4; color: #042f2e; border-color: #5eead4;
}
.cho-b2b-stage {
  background: rgba(255,255,255,0.06); border: 1px solid rgba(94,234,212,0.22);
  border-radius: 18px; padding: 16px;
}

/* Option C-H3: Architectural Radar & Global Reach Hero */
.cho-h3-center {
  text-align: center; max-width: 820px; margin: 0 auto; position: relative; z-index: 2;
}
.cho-h3-center .lead {
  margin-inline: auto; border-inline-start: 0; padding-inline-start: 0; text-align: center;
}
.cho-h3-center .contact-hero-ctas {
  justify-content: center;
}
.cho-radar-wrap {
  margin: 22px auto 0; max-width: 780px; padding: 16px 20px; border-radius: 22px;
  background: rgba(5, 34, 38, 0.78); backdrop-filter: blur(12px);
  border: 1px solid rgba(94, 234, 212, 0.36);
  display: grid; grid-template-columns: 1.2fr 1fr; gap: 18px; align-items: center; text-align: start;
}
.cho-sla-pills { display: grid; gap: 8px; }
.cho-sla-pill {
  display: flex; align-items: center; justify-content: space-between; gap: 10px;
  padding: 9px 14px; border-radius: 12px; background: rgba(255,255,255,0.08);
  border: 1px solid rgba(94,234,212,0.25); font-size: .84rem;
}
.cho-sla-pill b { color: #5eead4; font-weight: 900; }
@media (max-width: 900px) {
  .cho-h2-grid, .cho-radar-wrap { grid-template-columns: 1fr; }
}
@media (max-width: 600px) {
  .cho-b2b-tabs { grid-template-columns: 1fr; }
}
</style>"""


def topbar(active):
    return f'''<div class="cho-bar">
  <div class="cho-bar-inner">
    <strong>پیشنهادهای طراحی هیروی صفحه «ارتباط با ما» (Contact Hero Proposals)</strong>
    <div class="cho-pills">
      <a class="cho-pill{" is-active" if active == "h1" else ""}" href="option-1.html">گزینه C-H1: ویدیو + ۳ کارت شیشه‌ای دسترسی سریع <span class="cho-rec">پیشنهادی</span></a>
      <a class="cho-pill{" is-active" if active == "h2" else ""}" href="option-2.html">گزینه C-H2: فرماندهی دوگانه واحدهای سازمانی</a>
      <a class="cho-pill{" is-active" if active == "h3" else ""}" href="option-3.html">گزینه C-H3: رادار ارتباطی تهران–شمس‌آباد</a>
      <a class="cho-pill{" is-active" if active == "hub" else ""}" href="index.html">مقایسه هر ۳ گزینه</a>
    </div>
  </div>
</div>'''


def contact_body_below_hero():
    raw = (ROOT / 'site/contact/index.html').read_text(encoding='utf-8')
    m = re.search(r'<main id="main">.*?</section>\s*(<section class="section">.*)</main>', raw, flags=re.S)
    return m.group(1) if m else ''


def build_h1(p='../'):
    return topbar('h1') + '\n' + PC.contact_video_hero(p, 'fa') + '\n  ' + contact_body_below_hero()


def build_h2(p='../'):
    hero = f'''{topbar("h2")}
  <section class="page-hero about-hero contact-hero has-playing-video">
    <video class="about-hero-video contact-hero-video is-playing" autoplay muted loop playsinline webkit-playsinline disablepictureinpicture disableremoteplayback preload="metadata" tabindex="-1" aria-hidden="true" poster="{p}assets/media/hero-customers-poster.jpg?v=20261028p">
      <source src="{p}assets/media/hero-customers.mp4?v=20261028p" type="video/mp4">
    </video>
    <div class="wrap cho-h2-grid">
      <div>
        <p class="crumbs"><a href="{p}">خانه</a> › ارتباط با ما (گزینه C-H2)</p>
        <h1>با ما در ارتباط <em>باشید…</em></h1>
        <p class="lead">برای استعلام قیمت، دریافت نمونه، خدمات نصب و پشتیبانی یا همکاری تجاری، با ما در تماس باشید.</p>
        <div class="contact-hero-ctas">
          <a class="ch-btn-call" href="tel:02192001017">{PC._SVG_PHONE_HERO}<span>تماس با آبادیس</span></a>
          <a class="ch-btn-wa" href="https://wa.me/989100145809" target="_blank" rel="noopener">{PC._SVG_WA_HERO}<span>پیام در واتس‌اپ</span></a>
        </div>
      </div>
      <aside class="cho-b2b-card" id="cH2Cmd">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px">
          <strong style="font-size:.92rem;color:#5eead4">مسیریابی مستقیم واحدهای تخصصی آبادیس</strong>
          <span class="sol-hcard-badge">پاسخگویی سریع</span>
        </div>
        <div class="cho-b2b-tabs">
          <button type="button" class="cho-b2b-tab is-on" data-ch2="0">فروش و پیش‌فاکتور</button>
          <button type="button" class="cho-b2b-tab" data-ch2="1">نصب و پشتیبانی فنی</button>
          <button type="button" class="cho-b2b-tab" data-ch2="2">همکاری تجاری و صادرات</button>
        </div>
        <div class="cho-b2b-stage">
          <h3 id="ch2Title" style="margin:0 0 6px;font-size:1.08rem;color:#fff">واحد فروش، استعلام قیمت و ارسال نمونه</h3>
          <p id="ch2Desc" style="margin:0 0 12px;font-size:.85rem;color:#cbe7e8;line-height:1.65">صدور پیش‌فاکتور رسمی بیمارستانی، استعلام قیمت روز کیسه‌ها و مخازن ساکشن و هماهنگی ارسال نمونه برای مراکز درمانی.</p>
          <div style="display:flex;flex-wrap:wrap;gap:8px;align-items:center;justify-content:space-between;padding-top:10px;border-top:1px solid rgba(94,234,212,0.2)">
            <span id="ch2Ext" style="font-size:.84rem;font-weight:800;color:#5eead4" dir="ltr">021-92001017 (Ext. 11)</span>
            <a id="ch2Btn" class="ch-btn-call" href="tel:02192001017" style="padding:8px 14px;font-size:.82rem">اتصال مستقیم به واحد</a>
          </div>
        </div>
      </aside>
    </div>
  </section>
  <script>(function(){{
    var d=[
      {{t:"واحد فروش، استعلام قیمت و ارسال نمونه",p:"صدور پیش‌فاکتور رسمی بیمارستانی، استعلام قیمت روز کیسه‌ها و مخازن ساکشن و هماهنگی ارسال نمونه برای مراکز درمانی.",e:"021-92001017 (Ext. 11)",h:"tel:02192001017"}},
      {{t:"واحد خدمات نصب، راه‌اندازی و پشتیبانی فنی",p:"مشاوره انتخاب سیستم ساکشن مرکزی یا پرتابل، نصب مخازن و رگولاتورها در اتاق عمل و ICU و خدمات گارانتی.",e:"021-22218910 · WhatsApp",h:"https://wa.me/989100145809"}},
      {{t:"واحد بازرگانی، نمایندگان و همکاری صادراتی",p:"همکاری با شرکت‌های پخش استانی، مناقصات دانشگاه‌های علوم پزشکی و صادرات به عراق، عمان و ازبکستان.",e:"info@abadis-med.com · Ext. 12",h:"#leadForm"}}
    ];
    var box=document.getElementById("cH2Cmd");
    if(!box)return;
    box.querySelectorAll("[data-ch2]").forEach(function(b){{
      b.addEventListener("click",function(){{
        var x=d[+b.getAttribute("data-ch2")];
        box.querySelectorAll("[data-ch2]").forEach(function(t){{t.classList.toggle("is-on",t===b);}});
        document.getElementById("ch2Title").textContent=x.t;
        document.getElementById("ch2Desc").textContent=x.p;
        document.getElementById("ch2Ext").textContent=x.e;
        document.getElementById("ch2Btn").href=x.h;
      }});
    }});
  }})();</script>'''
    return hero + '\n  ' + contact_body_below_hero()


def build_h3(p='../'):
    radar_svg = (
        '<svg viewBox="0 0 360 150" width="100%" height="135" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
        '<rect width="360" height="150" rx="16" fill="#06282c"/>'
        '<circle cx="95" cy="75" r="46" stroke="#14b8a6" stroke-opacity="0.28" stroke-dasharray="4 4"/>'
        '<circle cx="95" cy="75" r="26" stroke="#5eead4" stroke-opacity="0.45"/>'
        '<path d="M95 75 Q180 25 265 75" stroke="#5eead4" stroke-width="2.2" stroke-dasharray="5 4"/>'
        '<circle cx="95" cy="75" r="6" fill="#5eead4"/>'
        '<circle cx="265" cy="75" r="6" fill="#2dd4bf"/>'
        '<text x="95" y="108" fill="#ecfeff" font-size="11" font-weight="800" text-anchor="middle" font-family="Kalameh,Tahoma">دفتر مرکزی (قیطریه)</text>'
        '<text x="265" y="108" fill="#ecfeff" font-size="11" font-weight="800" text-anchor="middle" font-family="Kalameh,Tahoma">کارخانه (شمس‌آباد)</text>'
        '<text x="180" y="42" fill="#5eead4" font-size="10" font-weight="800" text-anchor="middle" font-family="Kalameh,Tahoma">پوشش ۳۱ استان · ۱٬۲۸۴ مرکز</text>'
        '</svg>'
    )
    hero = f'''{topbar("h3")}
  <section class="page-hero about-hero contact-hero has-playing-video">
    <video class="about-hero-video contact-hero-video is-playing" autoplay muted loop playsinline webkit-playsinline disablepictureinpicture disableremoteplayback preload="metadata" tabindex="-1" aria-hidden="true" poster="{p}assets/media/hero-or-zagros-poster.jpg?v=20261028p">
      <source src="{p}assets/media/hero-or-zagros.mp4?v=20261028p" type="video/mp4">
    </video>
    <div class="wrap cho-h3-center">
      <p class="crumbs"><a href="{p}">خانه</a> › ارتباط با ما (گزینه C-H3)</p>
      <h1>با ما در ارتباط <em>باشید…</em></h1>
      <p class="lead">برای استعلام قیمت، دریافت نمونه، خدمات نصب و پشتیبانی یا همکاری تجاری، با ما در تماس باشید.</p>
      <div class="contact-hero-ctas">
        <a class="ch-btn-call" href="tel:02192001017">{PC._SVG_PHONE_HERO}<span>تماس با آبادیس</span></a>
        <a class="ch-btn-wa" href="https://wa.me/989100145809" target="_blank" rel="noopener">{PC._SVG_WA_HERO}<span>پیام در واتس‌اپ</span></a>
      </div>
      <div class="cho-radar-wrap">
        <div>{radar_svg}</div>
        <div class="cho-sla-pills">
          <div class="cho-sla-pill"><span>مرکز تماس و فروش</span><b dir="ltr">021-92001017</b></div>
          <div class="cho-sla-pill"><span>پشتیبانی مستقیم واتس‌اپ</span><b dir="ltr">+98 910 014 5809</b></div>
          <div class="cho-sla-pill"><span>پست الکترونیک رسمی</span><b dir="ltr">info@abadis-med.com</b></div>
        </div>
      </div>
    </div>
  </section>'''
    return hero + '\n  ' + contact_body_below_hero()


def build_index(p='../'):
    return f'''{topbar("hub")}
  <section class="section"><div class="wrap">
    <div class="section-head">
      <h1>مقایسه ۳ گزینه طراحی هیروی صفحه «ارتباط با ما» (/contact/)</h1>
      <p>هر سه گزینه شامل متن مصوب مدیریت («با ما در ارتباط باشید… / برای استعلام قیمت، دریافت نمونه، خدمات نصب و پشتیبانی یا همکاری تجاری، با ما در تماس باشید.») و دو دکمه «تماس با آبادیس» و «پیام در واتس‌اپ» با آیکون‌های برداری اختصاصی هستند.</p>
    </div>
    <div class="sol-hero-trio" style="margin-top:18px">
      <article class="sol-hcard">
        <div>
          <div class="sol-hcard-top"><span class="sol-hcard-num">C-H1</span><span class="sol-hcard-badge">پیشنهاد اصلی</span></div>
          <h2 style="margin:10px 0 6px">گزینه C-H1: هیروی ویدیویی + ۳ کارت شیشه‌ای دسترسی سریع</h2>
          <p>پس‌زمینه ویدیویی فیروزه‌ای آبادیس با تیتر Kalameh Black، دو دکمه اصلی «تماس با آبادیس» و «پیام در واتس‌اپ» و ۳ کارت شیشه‌ای دسترسی مستقیم به مرکز تماس، واتس‌اپ و نقشه.</p>
        </div>
        <div class="sol-hcard-foot"><a class="btn btn-primary" href="option-1.html" style="width:100%;text-align:center">مشاهده زنده گزینه C-H1</a></div>
      </article>
      <article class="sol-hcard">
        <div>
          <div class="sol-hcard-top"><span class="sol-hcard-num">C-H2</span><span class="sol-hcard-badge">مسیریاب سازمانی</span></div>
          <h2 style="margin:10px 0 6px">گزینه C-H2: هیروی دوگانه فرماندهی واحدهای سازمانی</h2>
          <p>چیدمان دوستونه شامل تیتر و دو دکمه تماس/واتس‌اپ در سمت راست و پنل تعاملی انتخاب مستقیم واحد فروش، واحد نصب و پشتیبانی فنی یا واحد صادرات در سمت چپ.</p>
        </div>
        <div class="sol-hcard-foot"><a class="btn btn-primary" href="option-2.html" style="width:100%;text-align:center">مشاهده زنده گزینه C-H2</a></div>
      </article>
      <article class="sol-hcard">
        <div>
          <div class="sol-hcard-top"><span class="sol-hcard-num">C-H3</span><span class="sol-hcard-badge">رادار ارتباطی</span></div>
          <h2 style="margin:10px 0 6px">گزینه C-H3: هیروی معماری و گرافیک ارتباطی تهران–شمس‌آباد</h2>
          <p>چیدمان مرکزی با ویدیوی پس‌زمینه، دو دکمه تماس و واتس‌اپ و دیاگرام برداری ارتباط دفتر مرکزی قیطریه، کارخانه شمس‌آباد و ۳۱ استان کشور.</p>
        </div>
        <div class="sol-hcard-foot"><a class="btn btn-primary" href="option-3.html" style="width:100%;text-align:center">مشاهده زنده گزینه C-H3</a></div>
      </article>
    </div>
  </div></section>'''


def main():
    p = '../'
    for fname, title, builder in (
        ('option-1.html', 'گزینه C-H1 هیروی ارتباط با ما', build_h1),
        ('option-2.html', 'گزینه C-H2 هیروی ارتباط با ما', build_h2),
        ('option-3.html', 'گزینه C-H3 هیروی ارتباط با ما', build_h3),
        ('index.html', 'مقایسه ۳ گزینه هیروی ارتباط با ما', build_index),
    ):
        html = page(p, 'contact', title, 'پیشنهاد طراحی هیروی صفحه ارتباط با ما', builder(p),
                    lang='fa', fa_path='contact/', extra_head=EXTRA_CSS)
        (OUT / fname).write_text(html, encoding='utf-8')
        print('Wrote', OUT / fname)


if __name__ == '__main__':
    main()
