# پکیج پرامپت‌های Cursor — بازطراحی سایت آبادیس مد

> ریپو: `ShushtarWolf/abadis-med-website-redesign` · برنچ: **`siamak/redesign`** (head هنگام نوشتن: `1ccbf8f`)
> پیش‌نمایش: https://siaamak-ghodsi.github.io/abadis-med-redesign-live/ (هر ۵ دقیقه از همین برنچ دیپلوی می‌شود)
> این فایل در ریپو هم هست: `docs/cursor/CURSOR-PROMPTS-FA.md`. قوانین ثابت در `.cursor/rules/abadis.mdc` هستند و Cursor خودش آن‌ها را در هر چت می‌خواند.

## طرز استفاده
1. در Cursor ریپو را باز کن، روی برنچ `siamak/redesign` باش (پرامپت ۰ این را چک می‌کند).
2. **برای هر کار یک چت جدید** باز کن (Agent mode)، و متن داخل بلوک کد همان پرامپت را کامل paste کن.
3. ترتیب پیشنهادی پایین صفحه است. **پرامپت ۰ را حتماً اول اجرا کن**؛ بدون آن، اجرای دوبارهٔ ژنراتور روی PC همهٔ عکس‌ها را به placeholder تبدیل می‌کند.
4. ریپو یک rule به اسم `token-warning.mdc` هم دارد که Cursor را وادار می‌کند قبل از کارهای سنگین هشدار بدهد و منتظر OK بماند. اگر هشدار داد، بنویس «OK ادامه بده».
5. بعد از هر پرامپت، Cursor باید SHA کامیت را بدهد. پیش‌نمایش حدود ۵ دقیقه بعد آپدیت می‌شود.

---

## زمینهٔ مشترک (هر پرامپت به این اشاره می‌کند؛ همین در `.cursor/rules/abadis.mdc` هم هست)

**گیت**
- فقط روی `siamak/redesign` کار کن. هیچ‌وقت push به `main` نکن، force-push نکن و تاریخچه را بازنویسی نکن.
- ShushtarWolf و abadismedit هم کامیت می‌زنند، پس قبل از push بزن `git pull --no-rebase` و کامیت دیگران را merge کن، overwrite نکن.
- آخر کار با PR `siamak/redesign → main` می‌رود. خود agent آن را merge نمی‌کند.

**ساختار** (بررسی‌شده روی `1ccbf8f`)
- `site/` شامل ۲۱۹ صفحهٔ HTML استاتیک است و همه فعلاً `noindex,nofollow` دارند.
- ژنراتور در `tools/redesign/` است: `build.py` (گروه‌ها: `products about dealers calculator csr contact customers experiences downloads install faq careers posts`) و `layout.py` (head، هدر، `NAV`، فوتر). باقی ماژول‌ها: `lib.py` (عکس‌ها، لینک‌ها، تاریخ شمسی)، `pages_*.py`، `render.py`، `cats.py` (دسته‌بندی خبر/مقاله) و `apply_shell.py` (هدر/فوتر صفحه‌های دستی).
- داده‌ها در `tools/redesign/data/` هستند: `pages.json` (۲۶ صفحه)، `posts.json` (۱۹۰ پست = ۱۸۱ منتشرشده + ۹ آگهی یا تست)، `jobs.json`، `known_cats.json` (۴۹ مورد)، `imgmap.json` (۵۶۹ URL عکس که فقط ۱۹۲ تا `ok` هستند).
- صفحه‌های دستی: `site/index.html` و `site/products/suction-bag/index.html` (ویوئر سه‌بعدی `site/assets/js/product-viewer.js` + `site/assets/abadis-scrub-parts.glb`).
- `site/csr/index.html` (انیمیشن اسکرول زاگرس: `site/csr/zagros-hero.js`) و `site/contact/index.html` هم دستی‌اند، ولی ژنراتور بلوک‌های `<!-- phase2:… -->` داخلشان را بازنویسی می‌کند.
- `tools/build_site.py` ژنراتور قدیمی فاز ۱ است. **اجرا نشود.**
- منابع داده: `docs/abadis/ABADIS-AUDIT.json`، `docs/abadis/URL-MIGRATION-MAP.csv` (۵۴۲ ردیف، تقریباً همه فارسی، EN و AR فقط ریشه‌اند) و `docs/abadis/ABADIS-MULTILINGUAL-INVENTORY.md` (جفت صفحه‌های FA/EN/AR).

**منبع محتوا**
- https سایت فعلی از بعضی شبکه‌ها کار نمی‌کند، ولی این‌ها روی **http** جواب می‌دهند (تست‌شده در ۶ اکتبر ۲۰۲۶):
  - `http://abadis-med.com/wp-content/uploads/...` برای فایل‌ها و عکس‌ها
  - `http://abadis-med.com/wp-json/wp/v2/posts` با ۲۲۳ پست
  - `/wp-json/wp/v2/media` با ۱۷۳۲ فایل
  - `/wp-json/wp/v2/_franchise` با ۲۶ مورد
  - `/wp-json/wp/v2/_customers` با ۱۵۵ مورد
  - `/wp-json/wp/v2/categories` با ۸ دسته (`newss`=22، `blog`=6، `آگهی-ها`=74، …)
  - `http://abadis-med.com/en/wp-json/wp/v2/pages` با ۳۱ صفحه
  - `http://abadis-med.com/arabic/wp-json/wp/v2/pages` با ۱۹ صفحه
- اگر جواب نداد، از Wayback استفاده کن: `https://web.archive.org/web/2026id_/<url>` (برای عکس `im_`).

**برند**
- فونت فقط Kalameh (`site/assets/fonts/kalameh/`).
- رنگ‌های teal: `#066163 #05686b #015F61 #0e7475 #087673`. پس‌زمینهٔ mint: `#e8f3f3` و `#f3fafa`.
- رنگ زرد یا لیمویی روی teal ممنوع است. تصویر خون ممنوع است. افکت حرکت موس ممنوع است.
- سه تم light، dark و noir باید روی همهٔ صفحه‌ها کار کنند.
- فوتر فقط نوار `CE · ISO 13485:2016 · IMED` را دارد.
- ترتیب منو: آشنایی با ما، محصولات، آخرین اخبار، لیست نمایندگان، توسعه پایدار، مقالات، ارتباط با ما، محاسبه‌گر.
- متن محصولات و صفحه‌ها عیناً از abadis-med.com است و چیزی ساخته یا بازنویسی نمی‌شود.

---

## پرامپت ۰ — آماده‌سازی و قابل‌تکرار کردن ژنراتور روی PC (اجباری، اول)

```
کار: آماده‌سازی محیط و قابل‌تکرار کردن ژنراتور tools/redesign روی این PC، بدون اینکه هیچ عکسی از site/ از بین برود.
قوانین .cursor/rules/abadis.mdc را رعایت کن (فقط برنچ siamak/redesign، بدون push به main، بدون force).

زمینه: tools/redesign/lib.py تابع img() فقط وقتی عکس برمی‌گرداند که فایل خام در RAW وجود داشته باشد
(RAW = env ABADIS_IMG_RAW، پیش‌فرض /workspace/abadis-wb/img-raw که روی این PC وجود ندارد).
خروجی‌های WebP قبلاً ساخته شده‌اند و در site/assets/img/c/ هستند (۲۲۲ فایل؛ نام = sha1(path)[:12]-{maxw}.webp).
پس اجرای build.py روی PC الان همهٔ عکس‌ها را به placeholder تبدیل می‌کند.

مراحل:
1) git fetch origin && git checkout siamak/redesign && git pull --no-rebase origin siamak/redesign
   python --version  (3.10+)،  pip install pillow
2) در tools/redesign/lib.py تابع img() را طوری تغییر بده که اگر فایل خروجی OUT_IMG/name از قبل وجود دارد،
   همان را استفاده کند (w,h را از خود WebP خروجی بخوان) حتی اگر RAW/f وجود نداشته باشد.
   فقط وقتی خروجی نیست و خام هست، تبدیل کند. پیش‌فرض RAW را به tools/redesign/.img-raw (داخل ریپو) تغییر بده
   (env ABADIS_IMG_RAW همچنان override کند) و tools/redesign/.img-raw/ را به .gitignore اضافه کن.
3) tools/redesign/README.md و site/README.md را اصلاح کن: site/README هنوز می‌گوید صفحات با tools/build_site.py ساخته می‌شوند که غلط است.
   بنویس ژنراتور فعلی tools/redesign/build.py است، build_site.py قدیمی است و نباید اجرا شود، و Pillow لازم است.
4) تست: python tools/redesign/build.py و بعد python tools/redesign/apply_shell.py
   سپس git status و git diff --stat site/
   انتظار: هیچ فایل HTML‌ای در site/ تغییر نکرده باشد (یا فقط تغییرات بی‌اهمیت مثل ترتیب).
   اگر جایی src عکس به placeholder ("ph txt" / "lg txt" / letter avatar) تبدیل شد، یعنی fallback کار نمی‌کند: درستش کن، کامیت نکن.
   شمارش مرجع فعلی (باید ثابت بماند):
   grep -o 'class="ph txt"' در کل site → 157 ، 'class="lg txt"' → 126 ، 'class="av" aria-hidden' → 12
5) python -m http.server 8080 --directory site و چند صفحه را باز کن (/ , /about/ , /news/ , /customers/).

معیار پذیرش: build.py روی PC بدون RAW اجرا می‌شود و diff صفحات site/ صفر است. README‌ها درست‌اند.
کامیت: "chore(tools): generator reuses built WebP when raw image cache is absent; fix READMEs"
git pull --no-rebase origin siamak/redesign && git push origin siamak/redesign
در پایان SHA کامیت را گزارش بده.
```

---

## پرامپت ۱ — بازیابی عکس‌های گم‌شده (محصولات، لوگوی مشتریان، تصویر شاخص پست‌ها، آیکون‌های SDG، مجوز ISO صفحهٔ درباره ما)

```
کار: عکس‌هایی را که الان placeholder هستند از سایت فعلی (روی http) یا Wayback بازیابی کن و در ژنراتور جایگزین کن.
قوانین .cursor/rules/abadis.mdc را رعایت کن. پیش‌نیاز: پرامپت ۰ انجام شده باشد.

اول وضعیت فعلی را گزارش کن (این‌ها شمارش‌های روی 1ccbf8f هستند؛ دوباره بشمار و جدول بده):
- tools/redesign/data/imgmap.json: ۵۶۹ URL، فقط ۱۹۲ تا ok:true ⇒ ۳۷۷ عکس بازیابی‌نشده.
- علامت placeholder در HTML:
  * 'class="ph txt"' (کاشی لوگوی آبادیس به‌جای عکس) = 157: news/index.html 69 (۵ تای آن کارت پست خارجی)،
    articles/index.html 77 (۱۳ تا خارجی) ⇒ ۱۲۸ پست آرشیوشده بدون تصویر شاخص؛ downloads 5؛
    products/index.html 1 (سایر محصولات)، products/{stand,canister,filters,connectors,suction-tube}/index.html هرکدام 1.
  * 'class="lg txt"' (حرف اول به‌جای لوگو) در customers/index.html = 126 از 157 مشتری.
  * 'class="av" aria-hidden' (حرف به‌جای عکس تیم) در about/index.html = 12.
  * about/index.html: به‌جای عکس مجوز ISO یک دکمهٔ «مشاهده مجوز ISO» است (pages_company.py حدود خط 20)
    با لینک https://abadis-med.com/wp-content/uploads/2025/01/گواهینامه-ایزو-scaled.jpg
  * csr: 'sdg-icons' = 0 ⇒ آیکون‌های اهداف توسعه پایدار (SDG) رندر نمی‌شوند (pages_company.py حدود خط 161).
  کد placeholderها: pages_posts.py (card/missing_card)، pages_company.py (خطوط ~33-38 تیم، ~229 مشتری، ~263 دانلود)، pages_products.py (~103، ~140).

روش:
1) یک اسکریپت tools/redesign/fetch_images.py بساز:
   - برای هر URL در imgmap.json که ok نیست (و URLهای جدیدی که پیدا می‌کنی) به ترتیب امتحان کن:
     a) http://abadis-med.com/wp-content/uploads/... (همان مسیر، https→http، همچنین نسخهٔ بدون پسوند -WxH)
     b) https://web.archive.org/web/2026im_/<url> و بعد CDX: https://web.archive.org/cdx/search/cdx?url=<url>&output=json&filter=statuscode:200
   - فایل خام را در RAW (tools/redesign/.img-raw) ذخیره کن و imgmap.json را با {"ok": true, "file": "<name>"} آپدیت کن.
   - timeout ۲۰ ثانیه، حداکثر ۴ درخواست همزمان، لاگ موفق/ناموفق در tools/redesign/data/img-fetch-log.json.
2) منابع کمکی برای پیدا کردن URL درست عکس‌ها (روی http):
   - تصویر شاخص پست‌ها: http://abadis-med.com/wp-json/wp/v2/posts?per_page=100&page=N&_fields=id,link,featured_media
     و سپس /wp-json/wp/v2/media?include=<ids>&per_page=100&_fields=id,source_url
     ⇒ فیلد image هر پست در data/posts.json را (بر اساس id یا link) پر/اصلاح کن.
   - لوگوی مشتریان: /wp-json/wp/v2/_customers?per_page=100&page=N&_fields=id,slug,title,featured_media,meta (۱۵۵ مورد)
   - عکس محصولات و تیم و آیکون‌های SDG: محتوای صفحه از /wp-json/wp/v2/pages?slug=<slug>&_fields=content
     (slugها: درباره-ما، توسعه-پایدار، محصولات/* ، کاتالوگ) و src تگ‌های img.
   - مجوز ISO: http://abadis-med.com/wp-content/uploads/2025/01/گواهینامه-ایزو-scaled.jpg
     ⇒ در about به‌صورت عکس (با lightbox) نمایش بده، نه دکمه. (این ISO صفحهٔ «آشنایی با ما» است؛ فوتر دست نخورد و فقط نوار CE·ISO·IMED بماند.)
3) python tools/redesign/build.py و python tools/redesign/apply_shell.py
   اگر home هم کارت‌های بدون عکس دارد، آن بخش را در صفحهٔ دستی فقط داخل بلوک‌های مارک‌شده یا از طریق ژنراتور عوض کن.
4) دوباره بشمار و جدول «قبل / بعد / هنوز ناموجود (با URL)» بده. اگر عکسی هیچ‌جا نبود، placeholder فعلی بماند. عکس ساختگی یا AI ممنوع است.
5) حجم: هر WebP خروجی را چک کن (کارت‌ها ≤ ۸۰KB، عکس بزرگ ≤ ۲۵۰KB)، width/height روی img و loading="lazy" بماند.
6) فایل‌های خام (.img-raw) کامیت نشوند. فقط site/assets/img/c/*.webp، imgmap.json، posts.json، اسکریپت و لاگ.

معیار پذیرش: تعداد placeholderها به‌طور محسوس کم شده؛ ISO درباره ما عکس است؛ SDG آیکون دارد؛ هیچ تصویر خون/نامرتبط نیست؛
سه تم و موبایل در /customers/ ، /news/ ، /about/ ، /csr/ سالم‌اند؛ git diff فقط فایل‌های مرتبط.
کامیت: "feat(site): recover missing images (post thumbnails, customer logos, team, SDG, ISO) from live uploads/Wayback"
git pull --no-rebase origin siamak/redesign && git push origin siamak/redesign  — SHA و جدول قبل/بعد را گزارش بده.
```

---

## پرامپت ۲ — ساخت ۱۸ پست جدید که هنوز به سایت فعلی لینک‌اند + اصلاح دسته‌بندی‌ها

```
کار: پست‌هایی که در سایت جدید صفحه ندارند و به abadis-med.com لینک می‌دهند را از REST API بساز، و دسته‌بندی خبر/مقالهٔ همهٔ پست‌ها را با دستهٔ واقعی وردپرس اصلاح کن.
قوانین .cursor/rules/abadis.mdc را رعایت کن. پیش‌نیاز: پرامپت ۰.

وضعیت فعلی (روی 1ccbf8f):
- pages_posts.py: POSTS=181 پست ساخته‌شده، MISSING=18 پست که فقط کارت «مطالعه در سایت فعلی» دارند (class "post-card ext"):
  2026-09-23 news     استخدام کارشناس فروش در شرکت دانش‌بنیان مخازن طبی آبادیس   /استخدام-کارشناس-فروش-در-شرکت-دانشبنی/
  2026-09-15 articles سوند نلاتون چیست؟                                         /سوند-نلاتون-چیست؟/
  2026-09-15 articles چست تیوب چیست؟                                            /چست-تیوب-چیست؟/
  2026-09-05 articles آبادیس پیشنهادهای جامع خود برای اصلاح اساسنامه انجمن…      /آبادیس-پیشنهادهای-جامع-خود-برای-اصلاح/   (احتمالاً در واقع news)
  2026-08-24 articles ساکشن مرکزی یا ساکشن پرتابل؟ راهنمای جامع…               /ساکشن-مرکزی-یا-ساکشن-پرتابل؟-راهنمای-ج/
  2026-08-23 articles نقش کیسه ساکشن یکبار مصرف در مدیریت پسماند عفونی…          /نقش-کیسه-ساکشن-یکبار-مصرف-در-مدیریت-پسم/
  2026-08-20 articles دستگاه تزریق چربی چیست؟                                   /دستگاه-تزریق-چربی-چیست؟/
  2026-08-19 articles لوله هوا (ایروی) چیست؟                                    /لوله-هوا-ایروی-چیست؟/
  2026-08-19 articles راهنمای خرید کیسه ساکشن یکبار مصرف برای مراکز درمانی       /راهنمای-خرید-کیسه-ساکشن-یکبار-مصرف-برا/
  2026-08-16 articles قیمت کیسه ساکشن یکبار مصرف؛ هر آنچه مدیران خرید…          /قیمت-کیسه-ساکشن-یکبار-مصرف؛-هر-آنچه-مدی/
  2026-08-11 news     آبادیس در روزهای جنگ رمضان؛ تداوم خدمت‌رسانی…             /آبادیس-در-روزهای-جنگ-رمضان؛-تداوم-خدمت/
  2026-08-11 articles اکستنشن تیوب چیست؟                                        /اکستنشن-تیوب-چیست؟/
  2026-08-11 articles فیلتر آنتی‌باکتریال و فیلتر هیدروفوبیک چیست؟              /فیلتر-آنتیباکتریال-و-فیلتر-هیدروفوب/
  2026-08-09 news     آغاز فوری عملیات بازسازی کارخانه آبادیس…                  /آغاز-فوری-عملیات-بازسازی-کارخانه-آباد/
  2026-08-09 news     ۱۷ مرداد؛ روز خبرنگار گرامی باد                           /۱۷-مرداد؛-روز-خبرنگار-گرامی-باد/
  2026-07-22 news     اعلام عدم تمدید عضویت و انتشار نامه سرگشاده مدیرعامل…     /اعلام-عدم-تمدید-عضویت-و-انتشار-نامه-سرگ/
  2026-06-21 articles 20 ژورنال معتبر تجهیزات پزشکی                             /20-ژورنال-معتبر-تجهیزات-پزشکی/
  2026-06-10 articles ساکشن دیواری چیست؟                                        /ساکشن-دیواری-چیست؟/
- علاوه بر این ۶ پست دیگر داخل متن پست‌ها لینک شده‌اند ولی ساخته نشده‌اند (لینک خارجی به سایت فعلی):
  /عفونت/ (id 719)، /کنترل-عفونت-در-بیمارستان/ (id 9724)، /زباله-های-بیمارستانی/ (id 6370)،
  /انواع-عفونتهای-بیمارستانی/، /شرکتهای-دانشبنیان-در-صنعت-تجهیزات/، /کنترل-عفونت-بیمارستانی-کرونا/
  (جمعاً ۲۴ لینک یکتا به پست‌های سایت فعلی در site/ — دستور شمارش:
   grep -rhoE 'href="https?://(www\.)?abadis-med\.com/[^"]*"' site --include=*.html | grep -v wp-content | sort -u)
- دسته‌بندی: فقط 34 از 181 پست دستهٔ واقعی دارند (data/known_cats.json)، 147 تا با حدس عنوانی (tools/redesign/cats.py) دسته گرفته‌اند.
- REST الان 223 پست می‌دهد؛ posts.json 190 دارد.

مراحل:
1) اسکریپت tools/redesign/fetch_posts_rest.py:
   - همه پست‌ها: http://abadis-med.com/wp-json/wp/v2/posts?per_page=100&page=1..3&_fields=id,date,modified,slug,link,title,excerpt,content,featured_media,categories,status
   - همه را با posts.json (کلید: id و unquote(link)) تطبیق بده.
   - known_cats.json را برای همهٔ ۲۲۳ پست از categories کامل کن (map: 22→newss, 6→blog, 74→ads, 20→accessories, 21→products, 69→install, 76→device, 1→uncategorized).
   - برای پست‌های ناموجود در posts.json (منتشرشده و غیر ads) یک رکورد با همان اسکیمای posts.json اضافه کن:
     {url, path, id(str), snapshot:"rest-YYYYMMDD", title, desc(excerpt بدون تگ), image(source_url تصویر شاخص از /wp/v2/media/<id>),
      date(ISO با +00:00 از date_gmt اگر هست), modified, author:"", mode:"rest", blocks:[{"t":"html","html": content.rendered}]}
   - متن عیناً همان content.rendered باشد. فقط wrapperهای Elementor/اسکریپت/استایل inline حذف شوند؛ متن ویرایش نشود.
2) cats.py: اگر دستهٔ واقعی (known_cats) هست، همان ملاک است (newss→news، blog/products/accessories/install/device→articles، ads→careers).
   «uncategorized» (دسته 1) را با همان heuristic فعلی دسته بده و در گزارش لیست کن.
3) عکس‌های داخل متن پست‌های جدید را با روش پرامپت ۱ (fetch_images.py) بگیر و imgmap را آپدیت کن.
4) python tools/redesign/build.py posts و بعد کل build و apply_shell (برای teaserهای صفحهٔ اصلی که home_teasers() لینک می‌کند).
5) بررسی: grep بالا باید 0 لینک پست به سایت فعلی بدهد (به‌جز فایل‌های wp-content که عمداً می‌مانند)؛ "post-card ext" باید 0 باشد.
   تعداد news/articles را قبل و بعد گزارش کن؛ لیست پست‌هایی که دسته‌شان عوض شد (عنوان، قبل→بعد) را در
   docs/abadis/POST-CATEGORY-CHANGES.md بنویس.
6) صفحهٔ چند پست جدید را در سه تم و موبایل ۳۷۵ ببین (تیترها، عکس‌ها، جدول‌ها، RTL، اعداد فارسی در تاریخ).

معیار پذیرش: همهٔ ۱۸ پست + ۶ پست لینک‌شده (و هر پست منتشرشدهٔ دیگری که REST دارد و ما نداریم) صفحهٔ داخلی دارند؛ هیچ لینک پستی به سایت فعلی نمانده؛
دسته‌ها از وردپرس آمده‌اند؛ آگهی‌های استخدام به careers می‌روند؛ صفحهٔ اصلی teaserها را به صفحه‌های داخلی لینک می‌دهد.
کامیت: "feat(site): build remaining posts from WP REST, real WP categories for news/articles"
git pull --no-rebase origin siamak/redesign && git push origin siamak/redesign — SHA + خلاصهٔ اعداد.
```

---

## پرامپت ۳ — نسخهٔ انگلیسی `/en/` و عربی `/arabic/`

> کار بزرگی است؛ پیشنهاد: در سه چت جدا اجرا کن: **۳-الف** زیرساخت و صفحه‌های اصلی EN، **۳-ب** پست‌های EN، **۳-ج** کل AR. همین یک پرامپت را بده و در خط اول بنویس کدام بخش.

```
کار: ساخت نسخه‌های انگلیسی (/en/) و عربی (/arabic/) سایت با همان طراحی، از محتوای واقعی سایت‌های EN/AR فعلی.
بخش این چت: [۳-الف زیرساخت + صفحه‌های اصلی EN | ۳-ب پست‌های EN | ۳-ج همهٔ AR]
قوانین .cursor/rules/abadis.mdc را رعایت کن. پیش‌نیاز: پرامپت ۰. قبل از شروع یک برنامهٔ کوتاه بده و منتظر OK من بمان.

منابع (فقط خواندنی):
- docs/abadis/ABADIS-MULTILINGUAL-INVENTORY.md بخش ۲ (جدول جفت صفحه‌ها FA↔EN↔AR) و بخش ۴-۶ (hreflang، سوییچر، کمبودها).
  docs/abadis/URL-MIGRATION-MAP.csv برای EN/AR فقط ریشه‌ها را دارد (en/ , www.../en/ , arabic/)؛ جدول inventory مرجع ساختار است.
- محتوا از REST روی http:
  EN: http://abadis-med.com/en/wp-json/wp/v2/pages?per_page=100&_fields=id,slug,link,title,content,featured_media,parent  (۳۱ صفحه)
      http://abadis-med.com/en/wp-json/wp/v2/posts?per_page=100&_fields=...  (۸۴ پست طبق inventory)
  AR: http://abadis-med.com/arabic/wp-json/wp/v2/pages?per_page=100&_fields=...  (۱۹ صفحه)، posts (۲۸)
  عکس‌ها: /en/wp-content/uploads/... و /arabic/wp-content/uploads/... روی http، سپس Wayback.
- متن‌ها عیناً از همین سایت‌ها باشند. ترجمهٔ ماشینی یا متن ساختگی ممنوع است. صفحه‌ای که در EN/AR وجود ندارد ساخته نشود
  (مثلاً موقعیت‌های شغلی و تجارب ما در EN/AR نیستند؛ CSR/SDG/مشتریان در AR نیستند). در گزارش لیستشان کن.

ساختار URL پیشنهادی (برای SEO همان slugهای فعلی EN/AR حفظ شود):
  /en/ ، /en/about-us/ ، /en/products/ ، /en/products/suction-bag/ ، /en/products/base-and-holder/ ، /en/products/filters/ ،
  /en/products/canisters/ ، /en/products/connections/ ، /en/products/other-products/ ، /en/suction-tube/ ، /en/calculator/ ،
  /en/contact-us/ ، /en/faqs/ ، /en/installation-manual/ ، /en/representatives/ ، /en/center-download/ ، /en/latest-news/ ،
  /en/blog/ ، /en/csr/ ، /en/sdgs/ ، /en/our-customers/ ، /en/collaboration-opportunities/ ، پست‌ها: /en/<post-slug>/ یا /en/latest-news/<id>/ (یکی را انتخاب و مستند کن).
  /arabic/ ، /arabic/من-نحن/ ، /arabic/منتجات/ ، /arabic/كيس-الشفط/ ، /arabic/تثبیت/ ، /arabic/الفلتر/ ، /arabic/خزانات/ ،
  /arabic/الوصلات/ ، /arabic/منتجات-اخری/ ، /arabic/أنبوب-الشفط/ ، /arabic/الحوسبة/ ، /arabic/اتصل-بنا/ ، /arabic/پرسش-های-متداول/ ،
  /arabic/دليل-التركيب/ ، /arabic/قائمة-الممثلين/ ، /arabic/مركز-التنزيل/ ، /arabic/الاخبار/
  (این مسیرها در site/ به‌صورت پوشه با index.html ساخته شوند. کاراکترهای یونیکد مسیر را در لینک‌ها percent-encode نکن، ولی تست کن روی http.server باز می‌شوند.)

پیاده‌سازی:
1) i18n در ژنراتور: tools/redesign/i18n.py با LANGS = {fa: {lang:"fa-IR", dir:"rtl", root:""}, en: {lang:"en", dir:"ltr", root:"en/"}, ar: {lang:"ar", dir:"rtl", root:"arabic/"}}
   و برچسب‌های منو/فوتر/دکمه‌ها برای هر زبان. برچسب‌ها از منوی واقعی همان سایت باشد (عنوان صفحه‌ها در REST).
   layout.py: head/header/footer پارامتر lang بگیرند (html lang/dir، NAV، متن فوتر، aria-labelها). صفحه‌های فارسی هیچ تغییری نکنند
   (بعد از build باید git diff صفحه‌های فارسی خالی باشد، به‌جز اضافه شدن hreflang و سوییچر).
2) CSS: site/assets/css/site.css را برای [dir="ltr"] درست کن (ترجیحاً با logical properties: margin-inline، inset-inline، text-align:start).
   آیکون‌های جهت‌دار (← →) در LTR برعکس شوند. انیمیشن‌ها و تم‌ها در LTR هم کار کنند.
   فونت: Kalameh حروف لاتین هم دارد. فونت جدید اضافه نکن مگر با تأیید من. در EN اعداد لاتین باشند (فایل‌های FaNum ارقام فارسی دارند
   ⇒ برای EN یک fallback برای ارقام لازم است؛ گزینه‌ها را بگو و منتظر تصمیم من بمان). AR: ارقام همان‌طور که در سایت AR فعلی است.
3) سوییچر زبان در هدر (کنار toggle تم): FA / EN / ع. به صفحهٔ معادل لینک می‌دهد (data/i18n-map.json از جدول inventory)،
   و اگر معادل نیست، به خانهٔ آن زبان. target="_blank" نباشد.
4) hreflang: روی هر صفحه‌ای که معادل دارد <link rel="alternate" hreflang="fa-IR|en|ar" href="..."> و x-default=fa،
   به‌صورت دوطرفه. canonical هر زبان خودش است (دامنهٔ نهایی را از یک ثابت SITE_ORIGIN در lib.py بخوان، پیش‌فرض https://abadis-med.com).
5) صفحه‌های دستی (home، suction-bag، csr) برای EN/AR: اسکلت همان طراحی، ولی متن از صفحهٔ معادل REST. انیمیشن زاگرس فقط اگر /en/csr/ وجود دارد.
   محاسبه‌گر: همان فرمول‌ها (site/calculator/common/abadis-common.js) با برچسب‌های زبان مقصد.
6) build: python tools/redesign/build.py (گروه جدید en و ar) و apply_shell.

معیار پذیرش: همهٔ صفحه‌های جدول بالا که در منبع وجود دارند ساخته شده‌اند؛ EN با dir=ltr درست چیده می‌شود؛ AR با lang="ar" dir="rtl"؛
سوییچر به صفحهٔ معادل می‌رود؛ hreflang دوطرفه است؛ صفحه‌های فارسی تغییری جز hreflang و سوییچر ندارند؛ سه تم و موبایل در هر سه زبان سالم‌اند؛
همه noindex می‌مانند. لیست صفحه‌هایی که منبع نداشتند گزارش شود.
کامیت (برای هر بخش جدا): "feat(site): English /en/ …" / "feat(site): Arabic /arabic/ …" / "feat(site): language switcher + hreflang"
git pull --no-rebase origin siamak/redesign && git push origin siamak/redesign — SHA.
```

---

## پرامپت ۴ — فرم‌ها: تماس + همکاری (بک‌اند واقعی با fallback ایمیل)

> ⚠️ **تصمیم با خودت است:** کدام سرویس و با کدام حساب و ایمیل. Cursor نباید خودش حساب بسازد. گزینه‌ها: **Formspree** (ساده‌ترین؛ آپلود فایل رزومه در پلن پولی)، **Cloudflare Worker** (روی حساب Cloudflare خودت، با ارسال ایمیل از طریق Resend یا Email Routing)، یا **n8n webhook** (در ریپو `docs/abadis/N8N-WORKFLOW.md` هست).

```
کار: فرم تماس و فرم همکاری را به یک endpoint واقعی وصل کن، با fallback ایمیل (mailto) اگر endpoint تنظیم نشده یا خطا داد. فرم همکاری را هم کامل کن.
قوانین .cursor/rules/abadis.mdc را رعایت کن. هیچ حسابی نساز و هیچ کلید یا سکرتی در ریپو کامیت نکن.

وضعیت فعلی:
- تماس: site/contact/index.html → <form class="card form reveal" id="leadForm"> با فیلدهای name, org, phone, topic, msg.
  site/assets/js/site.js خطوط ~246-254 فقط mailto:info@abadis-med.com باز می‌کند.
- همکاری: tools/redesign/pages_company.py تابع careers() → <form class="form" data-mailto-form="info@abadis-med.com" data-subject="ثبت درخواست همکاری">
  فیلدها: عنوان شغلی، نام، نام خانوادگی، نام پدر، نظام وظیفه، تاریخ تولد، محل تولد، شماره شناسنامه، محل صدور، وضعیت تاهل، بیماری خاص.
  یادداشت روی صفحه: «ادامهٔ فیلدهای فرم سایت فعلی (پس از پرسش بیماری خاص) در نسخهٔ آرشیوشده ثبت نشده بود.»
  site.js خطوط ~255+ (form[data-mailto-form]).

مراحل:
1) فیلدهای کامل فرم همکاری سایت فعلی را پیدا کن:
   http://abadis-med.com/wp-json/wp/v2/pages?slug=فرصت-های-همکاری&_fields=content  (HTML فرم معمولاً داخل content.rendered است)
   و اگر نبود، Wayback صفحهٔ https://abadis-med.com/فرصت-های-همکاری/ و موقعیت-های-شغلی/.
   فیلدهای جاافتاده را با همان برچسب و ترتیب و گزینه‌ها به careers() اضافه کن (تحصیلات، سوابق، رزومه و غیره، هرچه واقعاً هست).
   بعد یادداشت «ادامهٔ فیلدها…» را حذف کن. اگر فیلد آپلود فایل دارد، در گزارش بگو که نیاز به بک‌اندِ پشتیبان فایل دارد.
2) یک تنظیم واحد: در layout.py یک <meta name="abadis-form-endpoint" content=""> (یا ثابت FORM_ENDPOINT در lib.py که در head نوشته شود).
   خالی = فقط mailto (رفتار فعلی).
3) site.js: یک handler مشترک برای #leadForm و form[data-mailto-form]:
   - اگر endpoint تنظیم شده: fetch(endpoint, {method:'POST', body: FormData, headers:{Accept:'application/json'}}) با فیلد مخفی form_name و honeypot (_gotcha).
   - موفق: پیام فارسی در .form-status / #formStatus («پیام شما ثبت شد…»)، فرم reset، دکمه موقع ارسال disabled.
   - خطا یا شبکه: پیام خطا + باز کردن mailto با همان متن (fallback).
   - اعتبارسنجی HTML5 حفظ شود؛ شماره تلفن با ارقام فارسی هم پذیرفته شود.
4) مستندات: docs/abadis/FORMS-BACKEND.md با سه گزینه (Formspree / Cloudflare Worker / n8n): مراحل راه‌اندازی، هزینه، محدودیت آپلود، و اینکه
   endpoint را کجا بگذارم. اگر Worker را انتخاب کنم، کد نمونهٔ Worker را در tools/forms-worker/ بگذار (بدون سکرت؛ متغیرها از env).
5) متن یادداشت «پیش‌نمایش: این فرم پس از اتصال…» را شرطی کن: فقط وقتی endpoint خالی است نمایش داده شود.
6) build + apply_shell، تست: با endpoint خالی ⇒ mailto باز می‌شود. با endpoint تستی (مثلاً https://httpbin.org/post) ⇒ پیام موفقیت.
   سه تم و موبایل.

معیار پذیرش: هر دو فرم با endpoint کار می‌کنند و بدون آن mailto؛ فرم همکاری فیلدهای کامل سایت فعلی را دارد؛ هیچ سکرتی در ریپو نیست؛ FORMS-BACKEND.md آماده است.
در پایان از من بپرس کدام گزینه و endpoint را می‌خواهم. خودت چیزی ثبت‌نام نکن.
کامیت: "feat(site): forms post to configurable endpoint with mailto fallback; complete careers form"
git pull --no-rebase origin siamak/redesign && git push origin siamak/redesign — SHA.
```

---

## پرامپت ۵ — نمایندگان: ۲۴ در برابر ۲۶ (و مشتریان ۱۵۷ در برابر ۱۵۵)

```
کار: تعداد و اطلاعات نمایندگان (و مشتریان) سایت جدید را با منبع اصلی تطبیق بده و اختلاف را درست کن.
قوانین .cursor/rules/abadis.mdc را رعایت کن. پیش‌نیاز: پرامپت ۰.

وضعیت فعلی:
- site/dealers/index.html: ۲۴ کارت class="dealer" در ۲۲ استان (legend: «دارای نماینده (۲۲ استان)» و «۲۴ نماینده»).
  کد: tools/redesign/pages_company.py تابع dealers() از data/pages.json کلید '/لیست-نمایندگان/' (نسخهٔ Wayback).
- منبع: CPT _franchise در وردپرس 26 مورد دارد:
  http://abadis-med.com/wp-json/wp/v2/_franchise?per_page=100&_fields=id,slug,title,status,meta,content,_citynmg
  (همچنین docs/abadis/URL-MIGRATION-MAP.csv: ۲۶ ردیف _franchise + آرشیو؛ audit-raw/_franchise-sitemap.xml)
  slugها شامل تکراری‌ها هستند: شرکت-نیک-طب، -2، -3، نیک-طب؛ مخازن-طبی-آبادیس، -2، -3، -4؛ جهان-درمان، -2؛
  دانش-نواندیشان-بهپود و دانش-نو-اندیشان-بهپود ⇒ احتمالاً یک شرکت برای چند استان چند رکورد دارد.
- استان‌ها: taxonomy _citynmg (۲۵ مورد) — http://abadis-med.com/wp-json/wp/v2/_citynmg?per_page=100
- مشتریان: site/customers/index.html = ۱۵۷ مرکز، REST _customers = ۱۵۵ (http://abadis-med.com/wp-json/wp/v2/_customers?per_page=100&page=1..2).

مراحل:
1) هر ۲۶ رکورد _franchise را بگیر (اگر فیلدهای JetEngine در meta نیست، از content یا از صفحهٔ /wp-json/wp/v2/pages?slug=لیست-نمایندگان).
   جدول بساز: slug | نام | استان(ها) | مدیرعامل | تلفن | آدرس | در سایت جدید هست؟
2) علت اختلاف را مشخص کن: رکورد تکراری، استانی که در Wayback نبود، رکورد پیش‌نویس، یا نمایندهٔ جدید.
3) اگر نماینده یا استانی واقعاً جاافتاده، داده را عیناً اضافه کن (data/dealers.json جدید از REST یا تکمیل منطق dealers()).
   تکراری واقعی دوبار نمایش داده نشود؛ نماینده‌ای که چند استان دارد زیر هر استان بیاید. شمارش legend از داده محاسبه شود.
   چیپ استان‌های بدون نماینده درست disabled بماند.
4) مشتریان: همین تطبیق را برای ۱۵۷ و ۱۵۵ انجام بده (تکراری؟ حذف‌شده؟). فقط اگر خطای واقعی بود اصلاح کن.
5) گزارش در docs/abadis/DEALERS-RECONCILIATION.md (جدول کامل + تصمیم برای هر اختلاف).
6) python tools/redesign/build.py dealers customers و بررسی سه تم و موبایل.

معیار پذیرش: تعداد نمایندگان و استان‌ها با منبع یکی است، یا اختلاف مستند و موجه است؛ تلفن‌ها لینک tel: دارند؛ گزارش کامیت شده.
کامیت: "fix(site): dealers reconciled with WP _franchise (26 records); customers check"
git pull --no-rebase origin siamak/redesign && git push origin siamak/redesign — SHA + خلاصهٔ اختلاف.
```

---

## پرامپت ۶ — آماده‌سازی انتشار + باز کردن PR (بدون merge)

> ⚠️ قبل از اجرا تصمیم بگیر: **دامنه و هاست نهایی** (GitHub Pages فعلی روی `main`، یا Cloudflare Pages، یا سرور خود شرکت). ریدایرکت واقعی (301) روی GitHub Pages ممکن نیست و فقط با Cloudflare، Netlify یا nginx می‌شود. فقط وقتی همه چیز تأیید شد noindex را برداریم.

```
کار: آماده‌سازی انتشار (SEO و ریدایرکت‌ها) و باز کردن Pull Request از siamak/redesign به main. PR را merge نکن.
قوانین .cursor/rules/abadis.mdc را رعایت کن. پیش‌نیاز: پرامپت‌های ۰، ۱، ۲، ۵ و ۷ (تست) انجام شده باشند. ۳ و ۴ اختیاری‌اند.
اول از من بپرس: دامنهٔ نهایی (پیش‌فرض https://abadis-med.com) و هاست (GitHub Pages / Cloudflare Pages / nginx). تا جواب ندادم مرحلهٔ ۱ را شروع نکن.

مراحل:
1) noindex: <meta name="robots" content="noindex,nofollow"> در tools/redesign/layout.py (خط ~41) و در صفحه‌های دستی
   (site/index.html، site/products/suction-bag/index.html، site/csr/index.html، site/contact/index.html) و صفحه‌های site/calculator/*/index.html
   (کپی از redesign/calculator از طریق pages_calculator.py) را بردار. یک سوییچ INDEXABLE در lib.py بگذار تا برگرداندن آسان باشد.
   پیش‌نمایش siaamak-ghodsi.github.io نباید ایندکس شود: برای آن robots.txt جدا با Disallow: / یا همان سوییچ در workflow پیش‌نمایش.
2) canonical: روی هر صفحه <link rel="canonical" href="{SITE_ORIGIN}/{path}"> (مسیر نهایی جدید). og:url هم.
3) site/sitemap.xml: اسکریپت tools/redesign/seo.py که همهٔ index.html‌ها را (به‌جز صفحه‌های داخلی محاسبه‌گر calculator/{dial,receipt,hospital,scale,flood}
   مگر بخواهم) با lastmod (از تاریخ پست یا git log) لیست کند. اگر /en/ و /arabic/ هست، xhtml:link alternate هم بگذارد.
   site/robots.txt: Allow همه + Sitemap: {SITE_ORIGIN}/sitemap.xml
4) site/404.html با طراحی سایت (هدر و فوتر از layout.py، سه تم).
5) ریدایرکت از URLهای قدیمی وردپرس به مسیرهای جدید:
   - منبع: docs/abadis/URL-MIGRATION-MAP.csv (۵۴۲ ردیف) + PAGE_MAP و POST_MAP و JOB_MAP در tools/redesign/lib.py (POST_MAP بعد از pages_posts.prepare() پر می‌شود).
   - پست‌ها: /<slug-فارسی>/ → /news/<id>/ یا /articles/<id>/ ؛ صفحه‌ها طبق PAGE_MAP ؛ /_joboffers/* → careers/jobs/<slug>/ ؛
     /category/newss/ → /news/ ، /category/blog/ → /articles/ ؛ tagها (۶۳)، authorها و _citynmg و _franchise و _customers تکی → نزدیک‌ترین صفحه (dealers/ ، customers/) ؛
     /_downloadcenter/* → downloads/ . ردیف‌هایی که مقصد ندارند را در گزارش بیاور.
   - هم نسخهٔ percent-encoded و هم decoded مسیر قدیمی را پوشش بده.
   - خروجی‌ها: site/_redirects (فرمت Cloudflare Pages/Netlify: "/old /new 301")، docs/abadis/redirects-nginx.conf (map)،
     و اگر هاست GitHub Pages است: صفحه‌های stub HTML با meta refresh + canonical در مسیرهای قدیمی (با سوییچ، پیش‌فرض خاموش).
   - docs/abadis/REDIRECTS.csv: old_url,new_url,type,source
6) چک: python tools/redesign/build.py ، apply_shell ، seo.py ؛ همهٔ مقصدهای ریدایرکت در site/ وجود دارند (اسکریپت چک بنویس).
7) PR:
   git fetch origin && git pull --no-rebase origin siamak/redesign && git merge origin/main (اگر main جلو رفته؛ conflict را با حفظ هر دو طرف حل کن، بدون force)
   git push origin siamak/redesign
   gh pr create --base main --head siamak/redesign --title "Abadis redesign — full Persian site (phase 2)" --body-file docs/abadis/PR-BODY.md
   (اگر gh نصب یا لاگین نیست، لینک https://github.com/ShushtarWolf/abadis-med-website-redesign/compare/main...siamak/redesign را بده تا خودم PR را باز کنم.)
   PR-BODY.md: خلاصهٔ صفحه‌ها، تغییرات نسبت به main، لینک پیش‌نمایش https://siaamak-ghodsi.github.io/abadis-med-redesign-live/ ،
   خلاصهٔ docs/abadis/TEST-REPORT.md، موارد باز، و یادآوری که .github/workflows/pages.yml با merge روی main سایت را دیپلوی می‌کند.
   PR را merge نکن و reviewer هم خودت اضافه نکن.

معیار پذیرش: هیچ صفحه‌ای noindex ندارد (grep -rl noindex site → 0، به‌جز موارد عمدی)؛ canonical روی همه هست؛ sitemap.xml معتبر است (xmllint --noout)؛
robots.txt و 404.html هستند؛ فایل‌های ریدایرکت ساخته شده‌اند و مقصدهایشان وجود دارد؛ PR باز است و merge نشده.
کامیت: "feat(site): launch prep — indexable, canonical, sitemap, robots, 404, redirects from WP URLs"
SHA و لینک PR را گزارش بده.
```

---

## پرامپت ۷ — تست کلی سایت (گزارش pass/fail)

```
کار: تست کامل سایت استاتیک site/ و نوشتن گزارش docs/abadis/TEST-REPORT.md با جدول pass/fail. فقط تست و گزارش.
باگ پیدا شد؟ رفع نکن، فقط در گزارش با شدت (critical/major/minor)، صفحه، و اسکرین‌شات ثبت کن. بعد از من بپرس کدام‌ها را رفع کنیم.
قوانین .cursor/rules/abadis.mdc را رعایت کن. ابزارهای تست در tools/test/ بروند (نه در site/). node_modules و خروجی‌های حجیم gitignore شوند.

راه‌اندازی (Node 18+):
  mkdir -p tools/test && cd tools/test && npm init -y
  npm i -D @playwright/test linkinator lighthouse
  npx playwright install chromium
  # سرور محلی (ترمینال جدا، از ریشهٔ ریپو):
  python -m http.server 8080 --directory site
  BASE=http://localhost:8080

لیست صفحه‌ها: همهٔ site/**/index.html (الان ۲۱۹) ⇒ URL. قالب‌های نماینده برای تست‌های سنگین:
  / ، /about/ ، /products/ ، /products/suction-bag/ ، /products/filters/ ، /news/ ، /news/1001/ ، /articles/ ، /articles/1041/ ،
  /dealers/ ، /customers/ ، /experiences/ ، /downloads/ ، /install-guide/ ، /install-guide/tanks/ ، /faq/ ، /careers/ ،
  /careers/jobs/accountant/ ، /csr/ ، /contact/ ، /calculator/ ، /calculator/dial/ ، /calculator/receipt/ ، /calculator/hospital/ ، /calculator/scale/ ، /calculator/flood/
  (+ /en/ و /arabic/ اگر ساخته شده‌اند)

تست‌ها (هرکدام یک ردیف در جدول گزارش):
 1. لینک‌ها: npx linkinator http://localhost:8080/ --recurse --skip "^https?://(?!localhost)" --format json > tools/test/out/links.json
    ⇒ لینک داخلی شکسته = fail. لینک‌های خارجی به abadis-med.com را جدا بشمار (wp-content: با http چک کن؛ لینک پست به سایت فعلی = warn).
 2. ۴۰۴ و asset شکسته: Playwright روی همهٔ ۲۱۹ صفحه (desktop, light): page.on('response') status>=400 و page.on('requestfailed') ⇒ لیست.
 3. خطای کنسول: page.on('console', type==='error') و page.on('pageerror') روی همهٔ صفحه‌ها.
 4. سه تم: برای قالب‌های نماینده × theme ∈ {light, dark, noir} (با ?theme=… و همچنین localStorage['abadis-theme']):
    document.documentElement.dataset.theme درست است؛ کنتراست متن اصلی (axe-core: npm i -D @axe-core/playwright، قانون color-contrast)؛ اسکرین‌شات.
 5. واکنش‌گرا: viewportهای 375x812، 768x1024، 1440x900 × قالب‌های نماینده × light (و noir برای home): اسکرین‌شات fullPage در tools/test/out/shots/<w>/<theme>/<page>.png ؛
    اسکرول افقی: document.documentElement.scrollWidth > innerWidth ⇒ fail.
 6. Lighthouse (موبایل) روی /، /products/suction-bag/، /csr/، /news/، /calculator/:
    npx lighthouse http://localhost:8080/ --only-categories=performance,accessibility,seo,best-practices --form-factor=mobile --output=json --output-path=tools/test/out/lh-home.json --chrome-flags="--headless"
    آستانه: a11y ≥ 90، best-practices ≥ 90، perf ≥ 70 (موبایل)؛ SEO فقط به‌خاطر noindex پایین است (قبل از پرامپت ۶ انتظار می‌رود؛ warn نه fail).
 7. RTL: html[lang="fa"][dir="rtl"] روی همهٔ صفحه‌های فارسی؛ هیچ عنصری از viewport بیرون نزند؛ آیکون‌های جهت‌دار درست باشند؛ اعداد تاریخ و شمارنده‌ها فارسی؛
    در EN (اگر هست) dir="ltr".
 8. فونت Kalameh: await page.evaluate(() => document.fonts.ready.then(() => [...document.fonts].filter(f => f.family.includes('Kalameh') && f.status==='loaded').length)) > 0
    و getComputedStyle(document.body).fontFamily شامل Kalameh؛ درخواست‌های woff2 همه 200.
 9. محاسبه‌گر (/calculator/ و هر ۵ طرح): در صفحه window.ABADIS_FORMULAS وجود دارد. مقادیر مرجع (فرمول‌های سایت فعلی):
    surgery({n:1000}) ⇒ water 14880 ، cost 212,500,000 ، hours ≈ 442.567
    surgery({n:1})    ⇒ water 14.88 ، cost 212,500 ، hours ≈ 0.44257
    beds({a:10,b:20}) ⇒ water 57734.4 ، cost 637,500,000 ، hours ≈ 1717.159
    beds({a:1,b:0})   ⇒ water 3779.52 ، cost 42,500,000 ، hours ≈ 112.412
    beds({a:0,b:1})   ⇒ water 996.96 ، cost 10,625,000 ، hours ≈ 29.652
    (تحمل خطا 0.01). سپس در UI: preset ۱۰۰۰ عمل را بزن (chip با data-n) و صبر کن تا odometer بایستد ⇒ عدد نمایش‌داده با مقدار بالا (گرد شده، ارقام فارسی) بخواند.
    اختیاری: فرمول را با محاسبه‌گر سایت فعلی مقایسه کن: http://abadis-med.com/wp-json/wp/v2/pages?slug=محاسبه-گر&_fields=content (فرمول‌های GFCalc).
10. CSR زاگرس (/csr/) روی 375 و 1440: اسکرول تدریجی (page.mouse.wheel به‌صورت گام‌به‌گام، نه حرکت موس) ⇒ سه حالت خشک → جوانه → سبز؛
    اسکرین‌شات در ۰٪، ۵۰٪، ۱۰۰٪ اسکرول hero؛ بدون خطای کنسول؛ FPS قابل‌قبول (performance trace کوتاه)؛ عکس‌های site/csr/img/hero/* همه 200.
11. صفحهٔ کیسه ساکشن سه‌بعدی (/products/suction-bag/) روی 375 و 1440: canvas/WebGL ساخته می‌شود، site/assets/abadis-scrub-parts.glb لود می‌شود (200)،
    اسکرول‌اسکراب کار می‌کند (اسکرین‌شات در چند نقطه)، روی موبایل بدون لگ شدید یا overflow؛ fallback وقتی WebGL نیست (chromium --disable-webgl).
12. toggle تم: کلیک روی .theme-toggle سه بار ⇒ light → dark → noir → light؛ بعد از reload تم حفظ می‌شود (localStorage['abadis-theme'])؛
    با prefers-reduced-motion هم کار کند (View Transitions یا crossfade fallback).
13. هدر در تم light: بالای صفحه شفاف (header background شفاف / alpha≈0)؛ بعد از scrollY>24 کلاس .scrolled اضافه می‌شود و فقط blur بی‌رنگ دارد (پس‌زمینهٔ سفید مات = fail)؛
    روی بخش‌های روشن کلاس .on-light و لوگو/لینک teal است، روی بخش تیره سفید. روی /، /about/، /products/، /news/ چک کن.
14. فرم‌ها: /contact/ (#leadForm) و /careers/ (form[data-mailto-form]): فیلدهای required بدون مقدار ⇒ ارسال نمی‌شود؛
    با مقدار ⇒ یا mailto ساخته می‌شود (page.on('request') / رهگیری navigation به mailto:) یا اگر endpoint تنظیم شده، POST 2xx و پیام موفقیت.
15. قوانین برند (خودکار تا جای ممکن): فوتر فقط img .foot-certs با abd-certs-768x119-1-copy.webp؛ ترتیب منو دقیقاً:
    آشنایی با ما، محصولات، آخرین اخبار، لیست نمایندگان، توسعه پایدار، مقالات، ارتباط با ما، محاسبه‌گر؛
    هیچ listener روی mousemove/pointermove برای افکت (getEventListeners در CDP یا grep در site/assets/js و site/csr و site/calculator)؛
    رنگ‌های زرد/لیمویی (#c6ff00, #d4ff00, #ffeb3b, #cddc39, yellow, lime …) در CSS کنار teal ⇒ لیست کن.
16. متا: هر صفحه title یکتا، meta description، og:image (اگر هست 200)، فقط یک h1، img بدون alt (لیست).

خروجی:
- اسکریپت‌ها: tools/test/site.spec.mjs (Playwright)، tools/test/run-all.sh (و run-all.ps1 برای ویندوز) که همه را پشت سر هم اجرا کند و tools/test/out/summary.json بسازد.
  اجرا: cd tools/test && npx playwright test site.spec.mjs --reporter=list
- docs/abadis/TEST-REPORT.md: تاریخ، SHA تست‌شده، جدول | # | تست | دامنه | نتیجه (✅ pass / ❌ fail / ⚠️ warn) | جزئیات و لینک به اسکرین‌شات |،
  سپس لیست باگ‌ها با شدت و صفحه و مرحلهٔ بازتولید، و امتیازهای Lighthouse. اسکرین‌شات‌های مهم (حداکثر ~۳۰ عدد، فشرده) در docs/abadis/test-shots/ و بقیه gitignore.
- .gitignore: tools/test/node_modules/ ، tools/test/out/

معیار پذیرش: همهٔ ۱۶ تست اجرا شده و نتیجه دارند؛ گزارش و اسکریپت‌ها کامیت شده‌اند؛ اسکریپت با یک دستور دوباره قابل اجراست.
کامیت: "test(site): full-site Playwright/Lighthouse/link check suite + TEST-REPORT.md"
git pull --no-rebase origin siamak/redesign && git push origin siamak/redesign — SHA + خلاصهٔ تعداد pass/fail/warn + ۵ باگ مهم.
```

---

## ترتیب پیشنهادی
1. **۰ (آماده‌سازی ژنراتور)** — اجباری و اول.
2. **۷ (تست کلی)** — یک بار الان اجرا شود تا وضعیت فعلی معلوم شود (baseline). باگ‌ها را بعداً با پرامپت جدا رفع کن.
3. **۲ (پست‌های جدید + دسته‌ها)**، چون عکس‌های پست‌های جدید را هم پرامپت ۱ پوشش می‌دهد.
4. **۱ (عکس‌ها)**
5. **۵ (نمایندگان و مشتریان)** — کار کوتاهی است.
6. **۴ (فرم‌ها)** — اول تصمیم سرویس.
7. **۳ (انگلیسی و عربی)** — بزرگ‌ترین کار است. اگر قرار است اول فقط سایت فارسی منتشر شود، می‌تواند بعد از انتشار انجام شود.
8. **۷ دوباره** — تست نهایی.
9. **۶ (انتشار + PR)** — آخر، بعد از تأیید دامنه و هاست. PR را خودت (یا ShushtarWolf) merge کن.

### تصمیم‌هایی که با خودت است (Cursor باید بپرسد)
- سرویس فرم: Formspree، Cloudflare Worker یا n8n، و ایمیل مقصد.
- دامنه و هاست نهایی، و روش ریدایرکت (GitHub Pages ریدایرکت 301 ندارد).
- عربی و انگلیسی قبل از انتشار یا بعد از آن.
- ارقام لاتین در نسخهٔ انگلیسی (Kalameh FaNum ارقام فارسی دارد).
