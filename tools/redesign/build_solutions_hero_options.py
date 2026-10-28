#!/usr/bin/env python3
"""Build 3 interactive Hero redesign proposals (H1, H2, H3) for «راهکارها» (solutions/)
at site/solutions-hero-options/ per [t281u]."""
import sys
from pathlib import Path

ROOT = Path('/workspace/abadis-med-website-redesign')
sys.path.insert(0, str(ROOT / 'tools/redesign'))

import solutions_arch as SA
import solutions_philosophy as PHIL
from layout import page
from pages_company import about_motion_tags

OUT = ROOT / 'site/solutions-hero-options'
OUT.mkdir(parents=True, exist_ok=True)

EXTRA_CSS = """<style>
.sho-bar {
  position: sticky; top: 0; z-index: 260;
  background: rgba(4, 32, 35, 0.95); backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(94, 234, 212, 0.28);
  padding: 10px 18px; color: #ecfeff;
}
.sho-bar-inner {
  max-width: 1220px; margin: 0 auto;
  display: flex; align-items: center; justify-content: space-between; gap: 12px; flex-wrap: wrap;
}
.sho-pills { display: flex; flex-wrap: wrap; gap: 8px; }
.sho-pill {
  padding: 6px 14px; border-radius: 999px; font-size: .82rem; font-weight: 800;
  color: #d7f4f4; text-decoration: none; border: 1px solid rgba(255,255,255,0.18);
  background: rgba(255,255,255,0.06);
}
.sho-pill.is-active {
  background: linear-gradient(135deg, #0d9488 0%, #05686b 100%);
  color: #fff; border-color: #5eead4;
}
.sho-rec {
  background: #5eead4; color: #042f2e; padding: 1px 7px; border-radius: 999px;
  font-size: .7rem; font-weight: 900; margin-inline-start: 4px;
}

/* Option H2: Split Interactive Clinical Command Center Hero */
.sho-h2-grid {
  display: grid; grid-template-columns: 1.15fr 1fr; gap: 28px; align-items: center;
}
.sho-cmd-panel {
  background: rgba(6, 36, 40, 0.82); backdrop-filter: blur(14px);
  border: 1.5px solid rgba(94, 234, 212, 0.42); border-radius: 24px;
  padding: 20px; color: #ecfeff; box-shadow: 0 22px 48px rgba(0,0,0,0.34);
}
.sho-cmd-tabs { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-bottom: 14px; }
.sho-cmd-tab {
  padding: 10px 8px; border-radius: 13px; border: 1px solid rgba(94,234,212,0.25);
  background: rgba(255,255,255,0.06); color: #ecfeff; font: inherit; font-size: .8rem; font-weight: 800;
  cursor: pointer; text-align: center; transition: all .2s ease;
}
.sho-cmd-tab.is-on {
  background: #5eead4; color: #042f2e; border-color: #5eead4;
}
.sho-cmd-stage {
  background: rgba(255,255,255,0.06); border: 1px solid rgba(94,234,212,0.2);
  border-radius: 18px; padding: 16px;
}
.sho-cmd-wards { display: flex; flex-wrap: wrap; gap: 6px; margin: 10px 0; }
.sho-ward-pill {
  padding: 4px 10px; border-radius: 999px; font-size: .76rem; font-weight: 800;
  background: rgba(94,234,212,0.18); color: #5eead4; border: 1px solid rgba(94,234,212,0.35);
}

/* Option H3: Executive 4-Questions Matrix Hero */
.sho-q4-grid {
  display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px; margin-top: 22px;
}
.sho-q4-btn {
  text-align: start; padding: 16px; border-radius: 18px;
  background: rgba(255,255,255,0.10); backdrop-filter: blur(10px);
  border: 1.5px solid rgba(94,234,212,0.3); color: #fff; font: inherit;
  cursor: pointer; transition: all .2s ease;
}
.sho-q4-btn.is-on, .sho-q4-btn:hover {
  background: rgba(255,255,255,0.95); color: #07282b; border-color: #5eead4;
  transform: translateY(-3px);
}
.sho-q4-num {
  display: inline-block; font-size: .78rem; font-weight: 900; padding: 2px 9px;
  border-radius: 999px; background: rgba(94,234,212,0.22); color: #5eead4; margin-bottom: 8px;
}
.sho-q4-btn.is-on .sho-q4-num, .sho-q4-btn:hover .sho-q4-num {
  background: #05686b; color: #fff;
}
.sho-q4-btn strong { display: block; font-size: 1rem; font-weight: 900; margin-bottom: 4px; }
.sho-q4-btn span { display: block; font-size: .82rem; opacity: .88; line-height: 1.55; }
.sho-q4-preview {
  margin-top: 14px; padding: 16px 20px; border-radius: 18px;
  background: rgba(6, 36, 40, 0.86); border: 1px solid rgba(94,234,212,0.38);
  display: flex; align-items: center; justify-content: space-between; gap: 16px; flex-wrap: wrap;
}
@media (max-width: 960px) {
  .sho-h2-grid { grid-template-columns: 1fr; }
  .sho-q4-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 560px) {
  .sho-q4-grid, .sho-cmd-tabs { grid-template-columns: 1fr; }
}
</style>"""


def topbar(active):
    return f'''<div class="sho-bar">
  <div class="sho-bar-inner">
    <strong>پیشنهادهای طراحی هیروی صفحه «راهکارها» (Solutions Hero Proposals)</strong>
    <div class="sho-pills">
      <a class="sho-pill{" is-active" if active == "h1" else ""}" href="option-1.html">گزینه H1: ویدیو + ۳ کارت راهکار <span class="sho-rec">پیشنهادی PDF</span></a>
      <a class="sho-pill{" is-active" if active == "h2" else ""}" href="option-2.html">گزینه H2: فرماندهی بالینی دوگانه</a>
      <a class="sho-pill{" is-active" if active == "h3" else ""}" href="option-3.html">گزینه H3: ماتریس ۴ پرسش کلیدی</a>
      <a class="sho-pill{" is-active" if active == "hub" else ""}" href="index.html">مقایسه هر ۳ گزینه</a>
    </div>
  </div>
</div>'''


def build_h1(p='../'):
    return topbar('h1') + '\n' + SA.hub_main(p, 'fa', opening='solution')


def build_h2(p='../'):
    hero = f'''{topbar("h2")}
  <section class="page-hero about-hero solutions-hero has-playing-video">
    <video class="about-hero-video solutions-hero-video is-playing" autoplay muted loop playsinline webkit-playsinline disablepictureinpicture disableremoteplayback preload="metadata" tabindex="-1" aria-hidden="true" poster="{p}assets/media/hero-or-zagros-poster.jpg?v=20261028p">
      <source src="{p}assets/media/hero-or-zagros.mp4?v=20261028p" type="video/mp4">
    </video>
    <div class="wrap sho-h2-grid">
      <div>
        <p class="crumbs"><a href="{p}">خانه</a> › راهکارها (گزینه H2)</p>
        <h1>{SA.SOL_HERO_H1["fa"]}</h1>
        {SA._sol_slogan_html(SA.SOL_SLOGAN_I18N["fa"])}
        <p class="sol-hero-lead">{SA.SOL_HERO_LEAD["fa"]}</p>
        <div class="ps-actions" style="margin-top:18px">
          <a class="sol-btn-calc" href="{p}calculator/">{SA._SVG_CALC}<span>محاسبه صرفه‌جویی بیمارستان</span></a>
          <a class="sol-btn-consult" href="{p}contact/">{SA._SVG_CHAT}<span>دریافت مشاوره تخصصی</span></a>
        </div>
      </div>
      <aside class="sho-cmd-panel" id="h2Cmd">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px">
          <strong style="font-size:.92rem;color:#5eead4">دیاگرام تعاملی سیستم‌های بیمارستانی آبادیس</strong>
          <span class="sol-hcard-badge" id="h2Badge">فعال · آماده عرضه</span>
        </div>
        <div class="sho-cmd-tabs">
          <button type="button" class="sho-cmd-tab is-on" data-h2="0">۰۱ مدیریت مایعات</button>
          <button type="button" class="sho-cmd-tab" data-h2="1">۰۲ مراقبت راه هوایی</button>
          <button type="button" class="sho-cmd-tab" data-h2="2">۰۳ مدیریت پسماند PVA</button>
        </div>
        <div class="sho-cmd-stage">
          <h3 id="h2Title" style="margin:0 0 6px;font-size:1.1rem;color:#fff">۱. مدیریت مایعات و ترشحات بیمارستانی</h3>
          <p id="h2Sub" style="margin:0 0 10px;font-size:.85rem;color:#cbe7e8;line-height:1.65">سیستم مدار بسته ساکشن از جمع‌آوری ایمن مایعات عفونی تا حفاظت از شبکه وکیوم مرکزی و حذف شست‌وشوی مخازن.</p>
          <div style="font-size:.78rem;font-weight:800;color:#8fe3e4">بخش‌های بیمارستانی هدف:</div>
          <div class="sho-cmd-wards" id="h2Wards">
            <span class="sho-ward-pill">اتاق عمل (OR)</span>
            <span class="sho-ward-pill">مراقبت‌های ویژه (ICU/CCU)</span>
            <span class="sho-ward-pill">اورژانس (ER)</span>
            <span class="sho-ward-pill">بخش‌های بستری</span>
          </div>
          <div style="font-size:.78rem;font-weight:800;color:#8fe3e4;margin-top:8px">اجزای کلیدی راهکار:</div>
          <p id="h2Parts" style="margin:4px 0 12px;font-size:.83rem;color:#ecfeff">کیسه ساکشن ۱/۲/۳ لیتری · مخزن پلی‌کربنات · فیلتر قطع‌کننده جریان · ساکشن تیوب · رگولاتور · پایه و ترولی</p>
          <a id="h2Link" class="sol-btn-calc" href="{p}solutions/fluid-management/" style="width:100%;justify-content:center">مشاهده صفحه تخصصی راهکار</a>
        </div>
      </aside>
    </div>
  </section>
  <script>(function(){{
    var data = [
      {{t:"۱. مدیریت مایعات و ترشحات بیمارستانی", s:"سیستم مدار بسته ساکشن از جمع‌آوری ایمن مایعات عفونی تا حفاظت از شبکه وکیوم مرکزی و حذف شست‌وشوی مخازن.", b:"فعال · آماده عرضه", w:["اتاق عمل (OR)","مراقبت‌های ویژه (ICU/CCU)","اورژانس (ER)","بخش‌های بستری"], p:"کیسه ساکشن ۱/۲/۳ لیتری · مخزن پلی‌کربنات · فیلتر قطع‌کننده جریان · ساکشن تیوب · رگولاتور · پایه و ترولی", u:"{p}solutions/fluid-management/"}},
      {{t:"۲. ایمنی و مراقبت از راه هوایی", s:"محصولات مکمل بهداشت دهان و تثبیت ایمن لوله تراشه برای کاهش ریسک پنومونی مرتبط با ونتیلاتور (VAP) در ICU.", b:"فعال · در حال توسعه", w:["مراقبت‌های ویژه (ICU)","بیماران اینتوبه","بیهوشی و ریکاوری"], p:"مسواک ساکشن · فیکسر لوله تراشه · سواب دهانی", u:"{p}solutions/airway-care/"}},
      {{t:"۳. کنترل آلودگی و مدیریت پسماند (PVA)", s:"نسل آینده فیلم‌ها و کیسه‌های پلیمری محلول در آب مبتنی بر PVA و رسیورهای یکبارمصرف برای کنترل پسماند بیمارستانی.", b:"مسیر توسعه · آینده", w:["واحد CSR و لاندری","اتاق عمل و پانسمان","مدیریت پسماند بیمارستانی"], p:"کیسه و فیلم محلول در آب PVA · رسیور یکبارمصرف ۶۰۰ میلی‌لیتری", u:"{p}solutions/waste-management-pva/"}}
    ];
    var box = document.getElementById("h2Cmd");
    if(!box) return;
    box.querySelectorAll("[data-h2]").forEach(function(btn){{
      btn.addEventListener("click", function(){{
        var d = data[+btn.getAttribute("data-h2")];
        box.querySelectorAll("[data-h2]").forEach(function(x){{ x.classList.toggle("is-on", x===btn); }});
        document.getElementById("h2Title").textContent = d.t;
        document.getElementById("h2Sub").textContent = d.s;
        document.getElementById("h2Badge").textContent = d.b;
        document.getElementById("h2Parts").textContent = d.p;
        document.getElementById("h2Link").href = d.u;
        document.getElementById("h2Wards").innerHTML = d.w.map(function(w){{ return '<span class="sho-ward-pill">'+w+'</span>'; }}).join("");
      }});
    }});
  }})();</script>'''
    showcase = '\n' + SA.interactive_showcase_section(p, 'fa')
    philosophy = '\n' + PHIL.hub_html('fa', lambda h: SA.href(p, 'fa', h))
    return hero + showcase + philosophy


def build_h3(p='../'):
    hero = f'''{topbar("h3")}
  <section class="page-hero about-hero solutions-hero has-playing-video">
    <video class="about-hero-video solutions-hero-video is-playing" autoplay muted loop playsinline webkit-playsinline disablepictureinpicture disableremoteplayback preload="metadata" tabindex="-1" aria-hidden="true" poster="{p}assets/media/hero-sdgs-poster.jpg?v=20261028p">
      <source src="{p}assets/media/hero-sdgs.mp4?v=20261028p" type="video/mp4">
    </video>
    <div class="wrap about-hero-grid">
      <div>
        <p class="crumbs"><a href="{p}">خانه</a> › راهکارها (گزینه H3)</p>
        <h1>{SA.SOL_HERO_H1["fa"]}</h1>
        {SA._sol_slogan_html(SA.SOL_SLOGAN_I18N["fa"])}
        <p class="sol-hero-lead">{SA.SOL_HERO_LEAD["fa"]}</p>
        <div class="sho-q4-grid" id="h3Matrix">
          <button type="button" class="sho-q4-btn is-on" data-q4="0">
            <span class="sho-q4-num">پرسش ۰۱ · محصولات</span>
            <strong>ما چه چیزی تولید و عرضه می‌کنیم؟</strong>
            <span>۸ خانواده محصول تخصصی ساکشن، فیلتراسیون، بهداشت دهان و کنترل آلودگی</span>
          </button>
          <button type="button" class="sho-q4-btn" data-q4="1">
            <span class="sho-q4-num">پرسش ۰۲ · راهکارها</span>
            <strong>این محصولات کنار هم چه مسئله‌ای را حل می‌کنند؟</strong>
            <span>۳ راهکار یکپارچه برای مدیریت مایعات، ایمنی راه هوایی و مدیریت پسماند</span>
          </button>
          <button type="button" class="sho-q4-btn" data-q4="2">
            <span class="sho-q4-num">پرسش ۰۳ · کاربردها</span>
            <strong>در کدام بخش‌های بیمارستان استفاده می‌شوند؟</strong>
            <span>اتاق عمل (OR)، مراقبت‌های ویژه (ICU/CCU)، اورژانس و بخش‌های بستری</span>
          </button>
          <button type="button" class="sho-q4-btn" data-q4="3">
            <span class="sho-q4-num">پرسش ۰۴ · نوآوری</span>
            <strong>برای حل مسئله آینده روی چه فناوری‌هایی کار می‌کنیم؟</strong>
            <span>فیلم‌ها و کیسه‌های زیست‌تخریب‌پذیر و محلول در آب PVA، هوش تجاری و پایداری</span>
          </button>
        </div>
        <div class="sho-q4-preview" id="h3Preview">
          <div>
            <strong id="h3PrevTitle" style="display:block;font-size:1.05rem;color:#5eead4;margin-bottom:4px">محور ۰۱: از قطعه و محصول تا سیستم هماهنگ بیمارستانی</strong>
            <span id="h3PrevDesc" style="font-size:.88rem;color:#ecfeff">مشاهده مستقیم ۸ گروه محصول یا ۳ راهکار تخصصی بیمارستانی آبادیس در داشبورد پایین</span>
          </div>
          <a id="h3PrevBtn" class="sol-btn-calc" href="#sol-showcase">کاوش در ۳ راهکار تخصصی</a>
        </div>
      </div>
    </div>
  </section>'''
    showcase = '\n' + SA.interactive_showcase_section(p, 'fa')
    philosophy = '\n' + PHIL.hub_html('fa', lambda h: SA.href(p, 'fa', h))
    return hero + showcase + philosophy


def build_index(p='../'):
    body = f'''{topbar("hub")}
  <section class="section"><div class="wrap">
    <div class="section-head">
      <h1>مقایسه ۳ گزینه طراحی هیروی صفحه «راهکارها» (Solutions Hero Options)</h1>
      <p>هر سه گزینه از ویدیوی پس‌زمینه اختصاصی آبادیس، تایپوگرافی چرخشی ۴ خطی با فونت KalamehWeb-FaNum-Black و تمام محتوای مصوب فایل PDF صفحه ۱ تا ۷ پشتیبانی می‌کنند.</p>
    </div>
    <div class="sol-hero-trio" style="margin-top:18px">
      <article class="sol-hcard">
        <div>
          <div class="sol-hcard-top"><span class="sol-hcard-num">H1</span><span class="sol-hcard-badge">پیشنهاد اصلی (مطابق PDF)</span></div>
          <h2 style="margin:10px 0 6px">گزینه H1: هیروی ویدیویی + ۳ کارت تعاملی راهکارها</h2>
          <p>ترکیب هیروی ویدیویی فیروزه‌ای آبادیس، شعار چرخشی ۴ خطی و ۳ کارت تعاملی راهکارها (۰۱ مدیریت مایعات، ۰۲ ایمنی راه هوایی، ۰۳ مدیریت پسماند PVA) دقیقاً مطابق وایرفریم صفحه ۷ فایل PDF.</p>
        </div>
        <div class="sol-hcard-foot"><a class="btn btn-primary" href="option-1.html" style="width:100%;text-align:center">مشاهده زنده گزینه H1</a></div>
      </article>
      <article class="sol-hcard">
        <div>
          <div class="sol-hcard-top"><span class="sol-hcard-num">H2</span><span class="sol-hcard-badge">فرماندهی بالینی</span></div>
          <h2 style="margin:10px 0 6px">گزینه H2: هیروی دوگانه فرماندهی بالینی (Split System Diagram)</h2>
          <p>چیدمان دوستونه شامل تایپوگرافی چرخشی ۴ خطی در سمت راست و پنل تعاملی انتخاب ۳ راهکار به تفکیک بخش‌های بیمارستانی (OR، ICU، ER) و اجزای کلیدی در سمت چپ.</p>
        </div>
        <div class="sol-hcard-foot"><a class="btn btn-primary" href="option-2.html" style="width:100%;text-align:center">مشاهده زنده گزینه H2</a></div>
      </article>
      <article class="sol-hcard">
        <div>
          <div class="sol-hcard-top"><span class="sol-hcard-num">H3</span><span class="sol-hcard-badge">ماتریس ۴ پرسش</span></div>
          <h2 style="margin:10px 0 6px">گزینه H3: هیروی معماری ۴ پرسش کلیدی (Executive Matrix)</h2>
          <p>نمایش چهار پرسش کلیدی PDF (محصولات، راهکارها، کاربردها، نوآوری) به‌صورت ۴ کارت شیشه‌ای تعاملی در دل هیروی ویدیویی به همراه پیش‌نمایش زنده.</p>
        </div>
        <div class="sol-hcard-foot"><a class="btn btn-primary" href="option-3.html" style="width:100%;text-align:center">مشاهده زنده گزینه H3</a></div>
      </article>
    </div>
  </div></section>'''
    return body


def main():
    p = '../'
    h_css, m_js = about_motion_tags(p)
    extra = h_css + '\n' + EXTRA_CSS
    for fname, title, builder in (
        ('option-1.html', 'گزینه H1 هیروی راهکارها', build_h1),
        ('option-2.html', 'گزینه H2 هیروی راهکارها', build_h2),
        ('option-3.html', 'گزینه H3 هیروی راهکارها', build_h3),
        ('index.html', 'مقایسه ۳ گزینه هیروی راهکارها', build_index),
    ):
        html = page(p, 'solutions', title, 'پیشنهاد طراحی هیروی صفحه راهکارهای آبادیس', builder(p),
                    lang='fa', fa_path='solutions/', extra_head=extra, scripts=m_js, html_attrs='data-slogan="t1"')
        (OUT / fname).write_text(html, encoding='utf-8')
        print('Wrote', OUT / fname)


if __name__ == '__main__':
    main()
