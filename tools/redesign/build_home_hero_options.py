#!/usr/bin/env python3
"""Build 3 full-bleed clinical nurse video Hero proposals (M-H1, M-H2, M-H3) for the Main Page
at site/home-hero-options/ per [t301u] & [t302u] (full-bleed edge-to-edge nurse video, NOT in a box)."""
import re
import sys
from pathlib import Path

ROOT = Path('/workspace/abadis-med-website-redesign')
sys.path.insert(0, str(ROOT / 'tools/redesign'))

import pages_home as PH
import w2_orbit
import factory_hero
import suction_bag_3d
from layout import page

OUT = ROOT / 'site/home-hero-options'
OUT.mkdir(parents=True, exist_ok=True)

EXTRA_CSS = """<style>
.mho-bar {
  position: sticky; top: 0; z-index: 260;
  background: rgba(4, 32, 35, 0.95); backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(94, 234, 212, 0.28);
  padding: 10px 18px; color: #ecfeff;
}
.mho-bar-inner {
  max-width: 1220px; margin: 0 auto;
  display: flex; align-items: center; justify-content: space-between; gap: 12px; flex-wrap: wrap;
}
.mho-pills { display: flex; flex-wrap: wrap; gap: 8px; }
.mho-pill {
  padding: 6px 14px; border-radius: 999px; font-size: .82rem; font-weight: 800;
  color: #d7f4f4; text-decoration: none; border: 1px solid rgba(255,255,255,0.18);
  background: rgba(255,255,255,0.06);
}
.mho-pill.is-active {
  background: linear-gradient(135deg, #0d9488 0%, #05686b 100%);
  color: #fff; border-color: #5eead4;
}
.mho-rec {
  background: #5eead4; color: #042f2e; padding: 1px 7px; border-radius: 999px;
  font-size: .7rem; font-weight: 900; margin-inline-start: 4px;
}

/* Option M-H2: Full-Bleed Nurse Video + Interactive Clinical Ward Selector Dock */
.mh2-trust-chips {
  display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 12px;
}
.mh2-chip {
  padding: 4px 12px; border-radius: 999px; font-size: .78rem; font-weight: 800;
  background: rgba(94, 234, 212, 0.16); border: 1px solid rgba(94, 234, 212, 0.42);
  color: #5eead4; backdrop-filter: blur(8px);
}
.mh2-ward-dock {
  background: rgba(5, 34, 40, 0.80); backdrop-filter: blur(14px);
  border: 1.5px solid rgba(94, 234, 212, 0.42); border-radius: 22px;
  padding: 16px 20px; color: #ecfeff; box-shadow: 0 20px 44px rgba(0,0,0,0.32);
}
.mh2-ward-tabs {
  display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-bottom: 12px;
}
.mh2-ward-tab {
  padding: 10px 12px; border-radius: 13px; border: 1px solid rgba(94, 234, 212, 0.28);
  background: rgba(255,255,255,0.07); color: #ecfeff; font: inherit; font-size: .84rem; font-weight: 800;
  cursor: pointer; text-align: center; transition: all .2s ease;
}
.mh2-ward-tab.is-on {
  background: #5eead4; color: #042f2e; border-color: #5eead4;
}
.mh2-ward-stage {
  display: flex; align-items: center; justify-content: space-between; gap: 16px; flex-wrap: wrap;
  padding-top: 8px; border-top: 1px solid rgba(94, 234, 212, 0.22);
}

/* Option M-H3: Serres-Inspired Panoramic Full-Bleed Nurse Video + Full-Width Live Impact Ribbon */
.mh3-sub-highlight {
  display: inline-block; margin: 0 0 12px; padding: 6px 14px; border-radius: 12px;
  background: rgba(6, 46, 52, 0.76); border-inline-start: 4px solid #5eead4;
  color: #99f6e4; font-size: clamp(.95rem, 1.35vw, 1.12rem); font-weight: 800;
  backdrop-filter: blur(8px);
}
.mh3-ribbon {
  display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px;
  padding: 16px 20px; border-radius: 22px;
  background: rgba(4, 30, 36, 0.80); backdrop-filter: blur(14px);
  border: 1.5px solid rgba(94, 234, 212, 0.38);
  box-shadow: 0 18px 42px rgba(0,0,0,0.30);
}
.mh3-stat {
  padding-inline: 10px; border-inline-start: 2px solid rgba(94, 234, 212, 0.35);
}
.mh3-stat strong {
  display: block; font-size: clamp(1.15rem, 1.8vw, 1.45rem); font-weight: 900; color: #5eead4;
}
.mh3-stat span {
  display: block; font-size: .82rem; color: #e2f8f8; margin-top: 2px;
}
@media (max-width: 900px) {
  .mh2-ward-tabs { grid-template-columns: 1fr; }
  .mh3-ribbon { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 560px) {
  .mh3-ribbon { grid-template-columns: 1fr; }
}
</style>"""


def topbar(active):
    return f'''<div class="mho-bar">
  <div class="mho-bar-inner">
    <strong>پیشنهادهای هیروی تمام‌صفحه ویدیوی پرستاران برای صفحه اصلی (Main Page Full-Bleed Nurse Video Proposals)</strong>
    <div class="mho-pills">
      <a class="mho-pill{" is-active" if active == "mh1" else ""}" href="option-1.html">گزینه M-H1: تمام‌صفحه + روتیتور ۴ خطی و ۳ کارت شیشه‌ای <span class="mho-rec">پیشنهادی</span></a>
      <a class="mho-pill{" is-active" if active == "mh2" else ""}" href="option-2.html">گزینه M-H2: تمام‌صفحه + داک تعاملی بخش‌های درمانی</a>
      <a class="mho-pill{" is-active" if active == "mh3" else ""}" href="option-3.html">گزینه M-H3: پانورامیک Serres + نوار آمار سراسری</a>
      <a class="mho-pill{" is-active" if active == "hub" else ""}" href="index.html">مقایسه هر ۳ گزینه</a>
    </div>
  </div>
</div>'''


def home_body_below_hero(p='../'):
    raw = (ROOT / 'site/index.html').read_text(encoding='utf-8')
    m = re.search(r'<main id="main"[^>]*>\s*<section[^>]*id="intro"[^>]*>.*?</section>\s*(.*)</main>', raw, flags=re.S)
    body = m.group(1) if m else ''
    # Prefix relative asset/page paths for subdirectory site/home-hero-options/
    body = re.sub(r'(href|src)="(?!https?:|mailto:|tel:|#|\.\./)([^"]+)"', rf'\1="{p}\2"', body)
    return body


def build_mh1(p='../'):
    return topbar('mh1') + '\n' + PH.hero_v2(p) + '\n' + home_body_below_hero(p)


def build_mh2(p='../'):
    hero = f'''{topbar("mh2")}
  <section class="hx hx--fullbleed" data-tone="dark" id="intro" aria-label="پیشرو در کنترل عفونت و مدیریت مایعات بیمارستانی">
    <div class="mh-bg-media" aria-hidden="true" style="background-image:url('{p}assets/media/hero-nurse-main-2-poster.jpg?v=20261029a')">
      <video class="mh-bg-video is-playing" autoplay muted loop playsinline webkit-playsinline disablepictureinpicture disableremoteplayback preload="auto" tabindex="-1" aria-hidden="true" poster="{p}assets/media/hero-nurse-main-2-poster.jpg?v=20261029a">
        <source src="{p}assets/media/hero-nurse-main-2.mp4?v=20261029a" type="video/mp4">
      </video>
      <div class="mh-bg-veil"></div>
    </div>
    <div class="wrap mh-hero-inner">
      <div class="mh-copy">
        <div class="mh2-trust-chips">
          <span class="mh2-chip">شرکت دانش‌بنیان مخازن طبی آبادیس</span>
          <span class="mh2-chip">CE اروپا · ISO 13485:2016 · IMED</span>
        </div>
        <h1>{PH.HERO_H1}</h1>
        <p class="hx-sub">طراحی‌شده برای آرامش خاطر پرستاران، سرعت عمل تیم جراحی و ایمنی کامل بیمار؛ سیستم مدار بسته ساکشن و فیلترهای قطع‌کننده جریان با راندمان ۹۹.۹۹۹٪ در ۱٬۲۸۴ مرکز درمانی در سراسر ۳۱ استان کشور.</p>
        <div class="hero-actions">
          <a class="btn btn-primary" href="{PH.CATALOGUE}" target="_blank" rel="noopener">دریافت کاتالوگ</a>
          <a class="btn btn-ghost" href="{p}export/#quote">درخواست قیمت / همکاری صادراتی</a>
        </div>
      </div>
      <div class="mh2-ward-dock" id="mh2Dock">
        <div class="mh2-ward-tabs">
          <button type="button" class="mh2-ward-tab is-on" data-mh2="0">۰۱ اتاق عمل و جراحی (OR)</button>
          <button type="button" class="mh2-ward-tab" data-mh2="1">۰۲ بخش‌های مراقبت ویژه (ICU / CCU)</button>
          <button type="button" class="mh2-ward-tab" data-mh2="2">۰۳ ایمنی پرستاران و مدیریت پسماند</button>
        </div>
        <div class="mh2-ward-stage">
          <div>
            <strong id="mh2Title" style="display:block;font-size:1.02rem;color:#5eead4;margin-bottom:3px">راهکار اتاق عمل: جمع‌آوری ایمن مایعات بدون سرریز و بدون شست‌وشوی مخزن</strong>
            <span id="mh2Desc" style="font-size:.85rem;color:#e2f8f8">کیسه‌های ساکشن ۱، ۲ و ۳ لیتری مدار بسته + فیلتر هیدروفوبیک قطع‌کننده جریان + ترولی و پایه استاندارد</span>
          </div>
          <a id="mh2Link" class="ch-btn-call" href="{p}solutions/fluid-management/" style="padding:9px 16px;font-size:.84rem">مشاهده راهکار بالینی</a>
        </div>
      </div>
    </div>
  </section>
  <script>(function(){{
    var d=[
      {{t:"راهکار اتاق عمل: جمع‌آوری ایمن مایعات بدون سرریز و بدون شست‌وشوی مخزن",s:"کیسه‌های ساکشن ۱، ۲ و ۳ لیتری مدار بسته + فیلتر هیدروفوبیک قطع‌کننده جریان + ترولی و پایه استاندارد",u:"{p}solutions/fluid-management/"}},
      {{t:"راهکار بخش ویژه (ICU/CCU): مراقبت ایمن از راه هوایی و پیشگیری از پنومونی VAP",s:"مسواک ساکشن، سواب دهانی، فیکسر لوله تراشه و سیستم ساکشن مدار بسته برای بیماران اینتوبه",u:"{p}solutions/airway-care/"}},
      {{t:"راهکار کنترل آلودگی و ایمنی پرستاران: حذف تماس مستقیم با ترشحات عفونی",s:"صرفه‌جویی سالانه بیش از ۱۲ میلیون لیتر آب و توسعه کیسه‌های محلول در آب PVA برای بیمارستان سبز",u:"{p}solutions/waste-management-pva/"}}
    ];
    var box=document.getElementById("mh2Dock");
    if(!box)return;
    box.querySelectorAll("[data-mh2]").forEach(function(b){{
      b.addEventListener("click",function(){{
        var x=d[+b.getAttribute("data-mh2")];
        box.querySelectorAll("[data-mh2]").forEach(function(t){{t.classList.toggle("is-on",t===b);}});
        document.getElementById("mh2Title").textContent=x.t;
        document.getElementById("mh2Desc").textContent=x.s;
        document.getElementById("mh2Link").href=x.u;
      }});
    }});
  }})();</script>'''
    return hero + '\n' + home_body_below_hero(p)


def build_mh3(p='../'):
    hero = f'''{topbar("mh3")}
  <section class="hx hx--fullbleed" data-tone="dark" id="intro" aria-label="پیشرو در کنترل عفونت و مدیریت مایعات بیمارستانی">
    <div class="mh-bg-media" aria-hidden="true" style="background-image:url('{p}assets/media/hero-nurse-main-3-poster.jpg?v=20261029a')">
      <video class="mh-bg-video is-playing" autoplay muted loop playsinline webkit-playsinline disablepictureinpicture disableremoteplayback preload="auto" tabindex="-1" aria-hidden="true" poster="{p}assets/media/hero-nurse-main-3-poster.jpg?v=20261029a">
        <source src="{p}assets/media/hero-nurse-main-3.mp4?v=20261029a" type="video/mp4">
      </video>
      <div class="mh-bg-veil mh-bg-veil--panoramic"></div>
    </div>
    <div class="wrap mh-hero-inner">
      <div class="mh-copy">
        <p class="mh-eyebrow">شرکت دانش‌بنیان مخازن طبی آبادیس</p>
        <h1>{PH.HERO_H1}</h1>
        <div class="mh3-sub-highlight">نخستین و بزرگ‌ترین تولیدکننده دانش‌بنیان کیسه‌های ساکشن یکبارمصرف مدار بسته در ایران</div>
        <p class="hx-sub">حذف عفونت متقاطع، محافظت از پرستاران و کادر درمان، و حذف کامل شست‌وشوی مخازن سنتی در ۱٬۲۸۴ بیمارستان و مرکز جراحی در سراسر کشور.</p>
        <div class="hero-actions">
          <a class="btn btn-primary" href="{PH.CATALOGUE}" target="_blank" rel="noopener">دریافت کاتالوگ</a>
          <a class="btn btn-ghost" href="{p}export/#quote">درخواست قیمت / همکاری صادراتی</a>
        </div>
      </div>
      <div class="mh3-ribbon">
        <div class="mh3-stat"><strong>۱٬۲۸۴ مرکز درمانی</strong><span>۱٬۲۴۲ بیمارستان + ۴۲ مرکز جراحی فعال</span></div>
        <div class="mh3-stat"><strong>۳۱ استان کشور</strong><span>پوشش سراسری با ۲۹ نماینده انحصاری</span></div>
        <div class="mh3-stat"><strong>۷۸٪ سهم بازار خصوصی</strong><span>و ۶۳٪ سهم بازار بیمارستان‌های دولتی</span></div>
        <div class="mh3-stat"><strong>۹۹.۹۹۹٪ فیلتراسیون</strong><span>حاجز هیدروفوبیک آنتی‌باکتریال و ویروسی</span></div>
      </div>
    </div>
  </section>'''
    return hero + '\n' + home_body_below_hero(p)


def build_index(p='../'):
    return f'''{topbar("hub")}
  <section class="section"><div class="wrap">
    <div class="section-head">
      <h1>مقایسه ۳ پیشنهاد هیروی تمام‌صفحه ویدیوی پرستاران برای صفحه اصلی (Main Page Hero Proposals)</h1>
      <p>در هر سه گزینه، ویدیوی پرستاران و کادر درمان به‌صورت تمام‌صفحه (Full-Bleed لبه به لبه در کل پس‌زمینه هیرو و بدون هیچ کادر یا باکس مستطیلی) اجرا شده است.</p>
    </div>
    <a class="f3d-hubcard" href="suction-bag-1l-3d.html" style="background:linear-gradient(120deg,#054a4d,#0e8c8c 58%,#ff7a59)">
      <span class="f3d-hubcard-tag">SB-1L-3D — کالبدشکافی مهندسی سه‌بعدی محصول</span>
      <h2>کالبدشکافی تعاملی سه‌بعدی کیسه ساکشن ۱ لیتری آبادیس (وایرفریم مهندسی + نمای انفجاری)</h2>
      <p>مدل سه‌بعدی دقیق کیسه ساکشن ۱ لیتری (کد ۰۴۰۱۱۱۱) مبتنی بر فایل مهندسی 1L pit.CATPart با ۵ بخش تعاملی (درب و قفل ۳۶۰ درجه، پورت‌ها و دریچه یک‌طرفه، فیلتر هیدروفوبیک ۹۹.۹۹۹٪، کیسه مدرج ۱ لیتری و پودر سوپرجاذب SAP، مخزن پلی‌کربنات و براکت نصب)، خطوط راهنمای مهندسی بدون باکس، حالت کاوش آزاد ۳۶۰ درجه و دکمه نمای انفجاری قطعات.</p>
      <span class="btn btn-primary">مشاهده زنده کیسه ساکشن ۱ لیتری سه‌بعدی</span>
    </a>
    <a class="f3d-hubcard" href="factory-3d.html">
      <span class="f3d-hubcard-tag">F-3D — پیشنهاد ویژه</span>
      <h2>هیروی تعاملی سه‌بعدی کارخانه آبادیس (اسکرولی‌تلینگ)</h2>
      <p>ترسیم خط‌به‌خط کارخانه واقعی شمس‌آباد (۲۰۰۰ متر مربع) با Three.js: نمای هوایی، ۵ ایستگاه تولید (تزریق، مونتاژ و کارتن، فیلتر، اکسترودر و کلین‌روم، انبار)، حالت کاوش آزاد و برچسب‌های قابل کلیک. نسخه فعال روی صفحه اصلی FA/EN/AR.</p>
      <span class="btn btn-primary">مشاهده زنده هیروی سه‌بعدی</span>
    </a>
    <div class="sol-hero-trio" style="margin-top:18px">
      <article class="sol-hcard">
        <div>
          <div class="sol-hcard-top"><span class="sol-hcard-num">M-H1</span><span class="sol-hcard-badge">پیشنهاد اصلی (فعال روی سایت)</span></div>
          <h2 style="margin:10px 0 6px">گزینه M-H1: ویدیوی تمام‌صفحه پرستاران + روتیتور ۴ خطی و ۳ کارت شیشه‌ای آمار</h2>
          <p>ویدیوی تمام‌صفحه پرستاران در کل پس‌زمینه هیرو (بدون باکس)، تیتر ارزش پیشنهادی با فونت Kalameh Black، روتیتور ۴ خطی، ۲ دکمه CTA و ۳ کارت شیشه‌ای آمار کلیدی در پایین.</p>
        </div>
        <div class="sol-hcard-foot"><a class="btn btn-primary" href="option-1.html" style="width:100%;text-align:center">مشاهده زنده گزینه M-H1</a></div>
      </article>
      <article class="sol-hcard">
        <div>
          <div class="sol-hcard-top"><span class="sol-hcard-num">M-H2</span><span class="sol-hcard-badge">انتخابگر بخش درمانی</span></div>
          <h2 style="margin:10px 0 6px">گزینه M-H2: ویدیوی تمام‌صفحه پرستاران + داک شیشه‌ای انتخاب سریع بخش بالینی</h2>
          <p>ویدیوی تمام‌صفحه پرستاران به همراه بج‌های استاندارد CE/ISO/IMED و نوار شیشه‌ای تعاملی انتخاب راهکار بر اساس بخش بیمارستانی (اتاق عمل OR، بخش ویژه ICU/CCU، و کنترل آلودگی).</p>
        </div>
        <div class="sol-hcard-foot"><a class="btn btn-primary" href="option-2.html" style="width:100%;text-align:center">مشاهده زنده گزینه M-H2</a></div>
      </article>
      <article class="sol-hcard">
        <div>
          <div class="sol-hcard-top"><span class="sol-hcard-num">M-H3</span><span class="sol-hcard-badge">پانورامیک Serres</span></div>
          <h2 style="margin:10px 0 6px">گزینه M-H3: ویدیوی تمام‌صفحه پانورامیک الهام‌گرفته از Serres + نوار آمار سراسری</h2>
          <p>نمای پانورامیک تمام‌صفحه پرستاران در پس‌زمینه با تایپوگرافی ادیتوریال و نوار شیشه‌ای ۴ ستونه شاخص‌های رسمی (۱٬۲۸۴ مرکز، ۳۱ استان، ۷۸٪ سهم بازار، ۹۹.۹۹۹٪ فیلتراسیون).</p>
        </div>
        <div class="sol-hcard-foot"><a class="btn btn-primary" href="option-3.html" style="width:100%;text-align:center">مشاهده زنده گزینه M-H3</a></div>
      </article>
    </div>
  </div></section>'''


def build_factory3d(p='../'):
    about = f'''  <section class="section" id="about"><div class="wrap">
    <div class="section-head">
      <h2>ادامه صفحه اصلی</h2>
      <p>این صفحه نسخه مستقل هیروی سه‌بعدی کارخانه است. همین هیرو اکنون در بالای صفحه اصلی فارسی، انگلیسی و عربی فعال است.</p>
    </div>
    <div class="hero-actions">
      <a class="btn btn-primary" href="{p}">صفحه اصلی فارسی</a>
      <a class="btn btn-ghost" href="{p}en/">English home</a>
      <a class="btn btn-ghost" href="{p}arabic/">الصفحة الرئيسية العربية</a>
      <a class="btn btn-ghost" href="index.html">بازگشت به مقایسه گزینه‌ها</a>
    </div>
  </div></section>'''
    return factory_hero.hero(p, 'fa') + '\n' + about



def build_bag3d(p='../'):
    about = f'''  <section class="section" id="about"><div class="wrap">
    <div class="section-head">
      <h2>مشخصات فنی و صفحه رسمی کیسه ساکشن یک‌بارمصرف ۱ لیتری آبادیس</h2>
      <p>این صفحه نسخه مستقل کالبدشکافی سه‌بعدی کیسه ساکشن ۱ لیتری (کد ۰۴۰۱۱۱۱ با پودر سوپرجاذب و کد ۰۴۰۱۰۱۱ بدون پودر) است. همین بخش تعاملی سه‌بعدی در صفحه رسمی محصول کیسه ساکشن (فارسی، انگلیسی و عربی) نیز فعال است.</p>
    </div>
    <div class="hero-actions">
      <a class="btn btn-primary" href="{p}products/suction-bag/#bag-3d">صفحه محصول کیسه ساکشن (FA)</a>
      <a class="btn btn-ghost" href="{p}en/products/suction-bag/#bag-3d">Suction Bag Page (EN)</a>
      <a class="btn btn-ghost" href="{p}arabic/كيس-الشفط/#bag-3d">صفحة كيس الشفط (AR)</a>
      <a class="btn btn-ghost" href="factory-3d.html">هیروی سه‌بعدی کارخانه</a>
      <a class="btn btn-ghost" href="index.html">بازگشت به فهرست پیش‌نمایش‌ها</a>
    </div>
  </div></section>'''
    return suction_bag_3d.section(p, 'fa', skip_to='#about', sec_id='intro', tag_h='h1') + '\n' + about

def main():
    p = '../'
    extra_head = (
        f'<link rel="stylesheet" href="{p}assets/css/home.css?v=20261028f">\n'
        + PH.logo_scroll_css(p) + '\n'
        + PH.counter_options_css(p) + '\n'
        + w2_orbit.assets(p) + '\n'
        + EXTRA_CSS
    )
    scripts = PH.logo_scroll_scripts(p) + PH.counter_options_script(p)
    extra_head += '\n' + factory_hero.head(p) + '\n<style>.f3d-hubcard{display:block;margin-top:18px;padding:24px 26px;border-radius:22px;text-decoration:none;color:#fff;background:linear-gradient(120deg,#066565,#0e8c8c 60%,#ff7a59);box-shadow:0 24px 60px -30px rgba(6,70,70,.6)}.f3d-hubcard h2{color:#fff;margin:8px 0 6px}.f3d-hubcard p{color:rgba(255,255,255,.9);max-width:820px}.f3d-hubcard-tag{font-weight:700;font-size:13px;background:rgba(255,255,255,.2);padding:4px 12px;border-radius:999px}.f3d-hubcard .btn{margin-top:12px;background:#fff;color:#066565}</style>'
    for fname, title, builder in (
        ('option-1.html', 'گزینه M-H1 هیروی تمام‌صفحه ویدیوی پرستاران (صفحه اصلی)', build_mh1),
        ('option-2.html', 'گزینه M-H2 هیروی تمام‌صفحه ویدیوی پرستاران (صفحه اصلی)', build_mh2),
        ('option-3.html', 'گزینه M-H3 هیروی تمام‌صفحه ویدیوی پرستاران (صفحه اصلی)', build_mh3),
        ('factory-3d.html', 'هیروی تعاملی سه‌بعدی کارخانه آبادیس (اسکرولی‌تلینگ)', build_factory3d),
        ('suction-bag-1l-3d.html', 'کالبدشکافی تعاملی سه‌بعدی کیسه ساکشن ۱ لیتری آبادیس (وایرفریم مهندسی)', build_bag3d),
        ('index.html', 'مقایسه ۳ گزینه هیروی تمام‌صفحه ویدیوی پرستاران (صفحه اصلی)', build_index),
    ):
        html = page(
            p, None, title, PH.HOME_DESC, builder(p),
            lang='fa', fa_path='',
            extra_head=extra_head, scripts=(factory_hero.scripts(p) + scripts) if fname == 'factory-3d.html' else ((suction_bag_3d.scripts(p) + scripts) if fname == 'suction-bag-1l-3d.html' else scripts),
            main_class='home-page', body_class='home', lightbox=True,
            html_attrs='data-slogan="t1"',
        )
        (OUT / fname).write_text(html, encoding='utf-8')
        print('Wrote', OUT / fname)


if __name__ == '__main__':
    main()
