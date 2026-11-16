# Live-identical URLs (Hamid, 2026-11-15)

Every redesign page now lives at exactly the URL it has on https://abadis-med.com: Persian slugs for FA
(`/درباره-ما/`, `/محصولات/مخزن/`, posts at `/<slug>/`), `/en/...` for English and `/arabic/...` for Arabic.
Tool: `tools/redesign/url_migrate.py` (idempotent; `build.py` runs it last). Inventory of live URLs:
`tools/redesign/data/live_urls.csv` (Yoast sitemaps for FA and EN, WordPress core sitemap for AR, plus links
found in the menus of all 82 live pages). Farsi checklist for the team: `docs/url-audit/url-checklist-fa.md` (+ .csv, .xlsx).

## Counts (live inventory, liara-test)

- live URLs: 818
- matched (already identical): 157
- moved to the live URL: 248 (+13 posts the live site merged into another post, kept at their own old slug with canonical to the post that replaced them)
- missing (no redesign page, redirect stub + 301 to the nearest page): the archives below are now real pages
  - content not built yet: the article and manual URLs still listed under "Live pages with no redesign page"
  - live duplicates / test pages: kept as 301s (canonical is another URL, or the WordPress test post `/تست/`)
  - WordPress archives (tags, authors, categories, `_customers`, `_franchise`, `_citynmg`, `_downloadcenter`, jet-menu, `_joboffers`) and the old job-ad posts: real pages, including `/page/N/` and `/مقالات/N/` pagination
- live 404 (ignored): 1
- redesign-only pages (kept at their path): 109
- archive and special pages added by `tools/redesign/pages_archives.py` on this branch keep liara-test's header and footer (496 pages; 301 rules after this pass: 322)

## Archives that are real pages

`python3 tools/redesign/pages_archives.py` writes a page at each live archive URL plus the eight old job-ad posts. Pagination follows the live site. Each new page has `noindex, nofollow`, a self canonical, and a self hreflang. FA/EN/AR alternates are added only for author slugs that exist in more than one language.

These three URLs are real pages as well:

- `/محصولات/کیسه-های-تخصصی-و-مدیریت-پسماند/` lists کیسه زباله PVA and رسیور یکبار مصرف
- `/en/catalogue/` lists the English catalogue PDFs
- `/en/reservoir-calculator/` serves the English calculator, with its own canonical

301s that stay, because the live canonical is a different URL:

- `/راهنمای-استفاده-کاربر-نهایی/`, `/ساکشن-تیوب/`
- `/en/base-and-holder/`, `/en/canisters/`, `/en/connections/`, `/en/filters/`, `/en/suction-bag/`
- `/تست/` (WordPress test post)
- duplicate or test leaves: `/en/a1-2/`, `/en/representatives-3/`, `/en/دیگر-محصولات-2/`, `/en/فوتر/`, `/arabic/الحاسبة/`
- `/محصولات/کیسه-های-تخصصی-و-مدیریت-پسماند-2/` (second copy of the waste-bag category)

## Old redesign path -> live URL

| old | new |
|---|---|
| `/about/` | `/درباره-ما/` |
| `/articles/` | `/مقالات/` |
| `/articles/1041/` | `/دستگاه-ساکشن-چیست/` |
| `/articles/1050/` | `/انواع-دستگاه-ساکشن/` |
| `/articles/1133/` | `/کرونا،سرماخوردگی،آنفلونزا/` |
| `/articles/1140/` | `/کنترل-ویروس-کرونا/` |
| `/articles/11455/` | `/مخزن-ساکشن-چیست؟/` |
| `/articles/14956/` | `/improving-the-environmental-effects-of-nosocomial-infectious-effluents-by-using-disposable-suction-liner-bagsfa/` |
| `/articles/15088/` | `/affordability-of-disposable-suction-bags/` |
| `/articles/15731/` | `/مقایسهی-نانو-واکسن-ها-و-واکسن-های-بر/` |
| `/articles/15748/` | `/بررسی-آلودگی-های-قارچی-به-ويژه-عوامل-مو/` |
| `/articles/15757/` | `/دستورالعمل-اجرایی-نحوه-ضدعفونی-ابزار/` |
| `/articles/15766/` | `/بررسی-علل-ایجاد-پریتونیت-در-بخش-دیالیز/` |
| `/articles/15774/` | `/نظام-مراقبت-عفونت-های-بیمارستانی-و-پیش/` |
| `/articles/15884/` | `/suctiontube/` |
| `/articles/15898/` | `/پروتکل-جامع-فرآیند-ضد-عفونی-با-نور-فراب/` |
| `/articles/16051/` | `/سیستم-شستشوی-بیمار-و-ضدعفونی-کننده-تجھ/` |
| `/articles/16135/` | `/آشنایی-با-اتحادیه-ها-و-تشکل-های-تجهیزات/` |
| `/articles/16170/` | `/الگوی-مقاومت-آنتی-بیوتیکی-باکتریهای/` |
| `/articles/16173/` | `/اجرا-و-رعایت-توصیه-نامه-های-بهداشتی-ارا/` |
| `/articles/16208/` | `/فیلتر-های-متخلخل-در-صنعت-پزشکی/` |
| `/articles/16244/` | `/بررسی-مشكلات-استفاده-از-وسايل-حفاظت-فر/` |
| `/articles/16273/` | `/ارزيابي-و-تحليل-مواجهات-شغلی-کادر-درما/` |
| `/articles/16317/` | `/رسیور-پزشکی-چیست؟/` |
| `/articles/16340/` | `/حذف-آنتیبیوتیک-ونکومایسین-با-استفاد/` |
| `/articles/16394/` | `/کلاس-خطر-تجهیزات-پزشکی-چیست-؟/` |
| `/articles/16419/` | `/بررسی-فراوانی-پنومونی-ناشی-از-ونتیلات/` |
| `/articles/16427/` | `/میزان-دانش-مراقبت-در-پیشگیری-و-کنترل-پ/` |
| `/articles/16430/` | `/رسانه-ها-در-صنعت-سلامت،-دارو-و-تجهیزات-پ/` |
| `/articles/16437/` | `/پودر-جاذب-در-صنعت-تجهیزات-پزشکی/` |
| `/articles/16445/` | `/مديريت-پسماند-هاى-عفونی-بيمارستان/` |
| `/articles/16452/` | `/طراحی-و-اجرای-دستورالعمل-مدیریت-مصرف-و/` |
| `/articles/16714/` | `/فیلم-pva-در-صنعت-تجهیزات-پزشکی/` |
| `/articles/16727/` | `/بررسی-شاخصهای-میکروبی-و-شیمیایی-آب-و/` |
| `/articles/16744/` | `/بررسی-میزان-رعایت-بهداشت-دست-کارکنان-د/` |
| `/articles/16752/` | `/معرفی-سایت-های-اینترنتی-خرید-آنلاین-تج/` |
| `/articles/16765/` | `/ایزو-در-صنعت-تجهیزات-پزشکی/` |
| `/articles/16786/` | `/ارزیابی-مقایسهای-مدیریت-مصرف-آنتی-بی/` |
| `/articles/16791/` | `/وسایل-یکبار-مصرف-پزشکی-و-استاندارد/` |
| `/articles/16798/` | `/برترین-شرکتهای-تجهیزات-پزشکی-در-سال/` |
| `/articles/16804/` | `/منسوجات-پزشکی-چیست؟/` |
| `/articles/16849/` | `/تبعیت-از-دستورالعمل-های-پیشگیری-کننده/` |
| `/articles/16856/` | `/ارتقا-فرايند-بیولوژيک-تصفیه-خانه-فاضل/` |
| `/articles/16870/` | `/فیلتر-متخلخل-و-انواع-آن-فلزی-،پلیمری،ptfe/` |
| `/articles/16927/` | `/کنترل-عفونت-در-دندانپزشکی/` |
| `/articles/17000/` | `/تجهیزات-و-ملزومات-پزشکی/` |
| `/articles/17226/` | `/hospital-infection-control-indicators/` |
| `/articles/17269/` | `/شرکت-دانشبنیان-صنعت-تجهیزات-پزشکی/` |
| `/articles/17305/` | `/اثرات-کیسههای-ساکشن-یکبار-مصرف-آبادی/` |
| `/articles/17402/` | `/تجهیزات-پزشکی-مصرفی-و-ملزومات-پزشکی-مص/` |
| `/articles/17425/` | `/فینگرتیپ-رابط-ساکشن-چیست؟/` |
| `/articles/17431/` | `/دستاوردهای-شرکت-مخازن-طبی-آبادیس-در-تو/` |
| `/articles/17488/` | `/معرفی-رشته-مهندسی-پزشکی/` |
| `/articles/17496/` | `/توسعه-پایدار-در-تجهیزات-پزشکی/` |
| `/articles/17551/` | `/معرفی-رشته-پرستاری-بازار-کار،-دانشگاه/` |
| `/articles/17561/` | `/محصولات-و-تجهیزات-پزشکی-پلیمری/` |
| `/articles/17588/` | `/چرا-کیسه-ساکشن-یکبار-مصرف-میتواند-جا/` |
| `/articles/17605/` | `/اهداف-توسعه-پایدار-آبادیس/` |
| `/articles/17748/` | `/طبقه-بندی-تجهیزات-پزشکی-t1-تا-t4-و-فرصتها/` |
| `/articles/17756/` | `/لیبل-اصالت-در-تجهیزات-پزشکی/` |
| `/articles/17781/` | `/کاربرد-pvc-مدیکال-گرید-در-تولید-لوله-ساکش/` |
| `/articles/17796/` | `/نحوه-شست-و-شوی-مخازن-ساکشن-ثابت-و-مدیریت/` |
| `/articles/17936/` | `/استانداردهای-موجود-در-تولید-کیسه-ساکش/` |
| `/articles/17949/` | `/استانداردهای-موجود-در-تولید-ساکشن-تیو/` |
| `/articles/17992/` | `/کیسه-ساکشن-یکبار-مصرف-استریل-چیست؟/` |
| `/articles/18409/` | `/فیلترهای-آبادیس؛-حداکثر-ایمنی-در-کنتر/` |
| `/articles/18410/` | `/نقش-صنایع-دانشبنیان-در-تحقق-حکمرانی/` |
| `/articles/18499/` | `/نمایشگاههای-تجهیزات-پزشکی-ایران/` |
| `/articles/18529/` | `/فیکسر-لوله-تراشه؛-ایمنی-بیشتر،-مراقبت/` |
| `/articles/18540/` | `/ساکشن-پرتابل-آمبولانسی-و-اهمیت-استفاد/` |
| `/articles/18568/` | `/نمایشگاههای-تجهیزات-پزشکی-جهان/` |
| `/articles/18578/` | `/طراحی-و-پیادهسازی-سیستم-هوش-تجاری-بر/` |
| `/articles/18597/` | `/ویروس-هانتا-چیست؟/` |
| `/articles/18609/` | `/نقش-کیسه-ساکشن-یکبارمصرف-در-کاهش-خطر/` |
| `/articles/18681/` | `/ساکشن-دیواری-چیست؟/` |
| `/articles/18699/` | `/20-ژورنال-معتبر-تجهیزات-پزشکی/` |
| `/articles/18736/` | `/ساکشن-مرکزی-یا-ساکشن-پرتابل؟-راهنمای-ج/` |
| `/articles/18758/` | `/نقش-کیسه-ساکشن-یکبار-مصرف-در-مدیریت-پسم/` |
| `/articles/18761/` | `/چست-تیوب-چیست؟/` |
| `/articles/18768/` | `/فیلتر-آنتیباکتریال-و-فیلتر-هیدروفوب/` |
| `/articles/18772/` | `/اکستنشن-تیوب-چیست؟/` |
| `/articles/18786/` | `/قیمت-کیسه-ساکشن-یکبار-مصرف؛-هر-آنچه-مدی/` |
| `/articles/18793/` | `/سوند-نلاتون-چیست؟/` |
| `/articles/18814/` | `/راهنمای-خرید-کیسه-ساکشن-یکبار-مصرف-برا/` |
| `/articles/18824/` | `/لوله-هوا-ایروی-چیست؟/` |
| `/articles/18883/` | `/دستگاه-تزریق-چربی-چیست؟/` |
| `/articles/19391/` | `/آشنایی-با-دستگاه-ساکشن-دامپزشکی/` |
| `/articles/19689/` | `/کیسه-pva-چیست؟-کاربردها،-مزایا-و-نقش-آن-در/` |
| `/articles/19696/` | `/راهنمای-خرید-کیسه-ادرار-یورین-بگ/` |
| `/articles/19701/` | `/مخزن-ساکشن-دائمی؛-انتخابی-اقتصادی-یا-ه/` |
| `/articles/19716/` | `/آینده-تجهیزات-پزشکی-با-هوش-مصنوعی؛-فنا/` |
| `/articles/19761/` | `/چست-باتل-چیست؟-آشنایی-با-انواع،-کاربرد/` |
| `/articles/19793/` | `/بهداشت-دهان-در-بیمارستان؛-از-اهمیت-مرا/` |
| `/articles/2615/` | `/نحوه-نصب-مخازن/` |
| `/articles/3341/` | `/کنترل-عفونت-بیمارستانی-کرونا/` |
| `/articles/3404/` | `/استفاده-مخزن-های-ساکشن-دائم/` |
| `/articles/3489/` | `/اصول-و-مبانی-کنترل-عفونت-های-بیمارستان/` |
| `/articles/3691/` | `/اصول-و-مبانی-کنترل-عفونت-های-بیمارستان-2/` |
| `/articles/382/` | `/کنترل-عفونت-های-بیمارستانی/` |
| `/articles/393/` | `/کیسه-ساکشن-یکبار-مصرف/` |
| `/articles/452/` | `/بررسی-میزان-بروز-عفونت-بیمارستانی/` |
| `/articles/467/` | `/بروز-عفونت-بیمارستانی/` |
| `/articles/516/` | `/گیره-t-شکل/` |
| `/articles/6370/` | `/زباله-های-بیمارستانی/` |
| `/articles/709/` | `/تجهیزات-و-محصولات-بیمارستانی/` |
| `/articles/713/` | `/انواع-عفونتهای-بیمارستانی/` |
| `/articles/716/` | `/پاتوژن/` |
| `/articles/719/` | `/عفونت/` |
| `/articles/738/` | `/معرفی-کیسه-ساکشن/` |
| `/articles/7439/` | `/کنترل-عفونت-پسماند-مایعات/` |
| `/articles/7451/` | `/زباله-های-پلاستیکی/` |
| `/articles/7643/` | `/کیسه-ساکشن-چیست/` |
| `/articles/773/` | `/introducing-medical-engineering-sites/` |
| `/articles/7890/` | `/رگولاتور-ساکشن-چیست/` |
| `/articles/7930/` | `/انواع-فیلترهای-کیسه-ساکشن/` |
| `/articles/910/` | `/fixture/` |
| `/articles/945/` | `/strategicity-and-necessity-of-using-disposable-suction-bags-part-ii/` |
| `/articles/9724/` | `/کنترل-عفونت-در-بیمارستان/` |
| `/articles/9920/` | `/پسماندهای_-عفونی_-بیمارستانی/` |
| `/articles/9939/` | `/تصفیه-فاضلاب-بیمارستانی/` |
| `/articles/9953/` | `/امحا-زباله-های-بیمارستانی/` |
| `/calculator/` | `/محاسبه-گر/` |
| `/calculator/dial/` | `/محاسبه-گر/dial/` |
| `/calculator/flood/` | `/محاسبه-گر/flood/` |
| `/calculator/hospital/` | `/محاسبه-گر/hospital/` |
| `/calculator/receipt/` | `/محاسبه-گر/receipt/` |
| `/calculator/scale/` | `/محاسبه-گر/scale/` |
| `/careers/` | `/فرصت-های-همکاری/` |
| `/careers/jobs/accountant/` | `/_joboffers/کارشناس-حسابداری/` |
| `/careers/jobs/collections-officer/` | `/_joboffers/کارمند-وصول-مطالبات/` |
| `/careers/jobs/export-specialist/` | `/_joboffers/کارشناس-صادرات/` |
| `/careers/jobs/market-research/` | `/_joboffers/کارشناس-تحقیقات-بازار/` |
| `/careers/jobs/quality-assurance/` | `/_joboffers/کارشناس-تضمین-کیفیت/` |
| `/careers/jobs/rnd-specialist/` | `/_joboffers/کارشناس-تحقیق-و-توسعه/` |
| `/careers/jobs/sales-manager/` | `/_joboffers/مدیر-فروش/` |
| `/careers/jobs/sales-specialist/` | `/_joboffers/کارشناس-فروش/` |
| `/careers/jobs/secretary/` | `/_joboffers/منشی/` |
| `/contact/` | `/ارتباط-با-ما/` |
| `/csr/` | `/مسئولیت-اجتماعی/` |
| `/customers/` | `/مشتریان-ما/` |
| `/dealers/` | `/لیست-نمایندگان/` |
| `/downloads/` | `/کاتالوگ/` |
| `/en/products/oral-hygiene/` | `/en/products/oral-swabs-tube-holders/` |
| `/experiences/` | `/تجارب-ما/` |
| `/faq/` | `/پرسش-های-متداول/` |
| `/install-guide/` | `/راهنمای-نصب/` |
| `/install-guide/end-user/` | `/راهنمای-نصب/راهنمای-استفاده-کاربر-نهایی/` |
| `/install-guide/tanks/` | `/راهنمای-نصب/راهنمای-نصب-مخازن/` |
| `/jobs/` | `/موقعیت-های-شغلی/` |
| `/news/` | `/آخرین-اخبار/` |
| `/news/1001/` | `/صورة-للمعرض-الدولي-الثاني-والعشرون-في/` |
| `/news/10182/` | `/شرکت-مخازن-طبی-آبادیس-دانش-بنیان-شد/` |
| `/news/10187/` | `/حضور-مخازن-طبی-آبادیس-در-نمایشگاه-تجهی/` |
| `/news/1022/` | `/مصاحبه-با-همکاران-و-مدیران-مخازن-طبی-آب/` |
| `/news/1029/` | `/iran-radio-interview-with-abadis-medical/` |
| `/news/1036/` | `/بازتاب-خبری-از-حضور-مخازن-طبی-آبادیس-د/` |
| `/news/1056/` | `/مصاحبه-ماهنامه-مهندسی-پزشکی-با-مشاور-ا/` |
| `/news/10707/` | `/رو-نمایی-از-محصول-جدید-آبادیس-در-حوزه-کن/` |
| `/news/10719/` | `/حضور-مخازن-طبی-آبادیس-در-نمایشگاه-تجهی-2/` |
| `/news/1122/` | `/قرعه-کشی-بزرگ-روز-پرستار-۹۸-آبادیس/` |
| `/news/1124/` | `/اهدا-جوایز-قرعه-کشی-روز-پرستار-سال-۹۸/` |
| `/news/11453/` | `/حضور-مخازن-طبی-آبادیس-در-نمایشگاه-تجهی-3/` |
| `/news/11467/` | `/رونمایی-از-محصول-جدید-آبادیس-در-حوزه-فی/` |
| `/news/11498/` | `/طراحی-جدیدی-از-اکسسوری-های-آبادیس/` |
| `/news/1162/` | `/فعالیت-های-مخازن-طبی-آبادیس-در-بحران-کر/` |
| `/news/12626/` | `/رونمایی-کیسه-ساکشن-یکبار-مصرف-با-فیلتر/` |
| `/news/13234/` | `/دعوت-نامه-حضور-در-کنگره-کنترل-عفونت-1401/` |
| `/news/13840/` | `/گزارش-کنگره-کنترل-عفونت-1401/` |
| `/news/14506/` | `/انتخاب-آبادیس-به-عنوان-فعالترین-شرکت-ت/` |
| `/news/14748/` | `/بیانیه-مدیران-مخازن-طبی-آبادیس-در-مورد/` |
| `/news/14844/` | `/دیدار-راهبردی-معاونت-بازرگانی-آبادیس/` |
| `/news/14895/` | `/حضور-شرکت-مخازن-طبی-آبادیس-در-چهاردهمی/` |
| `/news/14923/` | `/abadismed-in-uzmedexpo/` |
| `/news/15009/` | `/the-beginning-of-the-school-year-in-abadis/` |
| `/news/15027/` | `/uzmedexpo2023reports/` |
| `/news/15101/` | `/the-need-to-use-a-disposable-suction-bag/` |
| `/news/15123/` | `/the-environmental-effects-publication-of-article-of-improving/` |
| `/news/15300/` | `/dr-mehrabi/` |
| `/news/15358/` | `/invitation-to-the-11th-congress-of-infection-control/` |
| `/news/15479/` | `/nurse-day-1402/` |
| `/news/15495/` | `/گزارش-کنگره-کنترل-عفونت-۱۴۰۲/` |
| `/news/15799/` | `/abadis-med-in-salamatbonyan-exhibition/` |
| `/news/15833/` | `/salamat-bonyan-exhibition-report/` |
| `/news/16094/` | `/نجات-زاگرس،مسئولیت-اجتماعی-آبادیس/` |
| `/news/16121/` | `/مصاحبه-شرکت-پیام-گستر-با-مدیران-آبادیس/` |
| `/news/16162/` | `/گزارش-کنگره-کنترل-عفونت-۱۳۹۷/` |
| `/news/16198/` | `/نظرسنجی-آبادیس-از-ایران-هلث-1403/` |
| `/news/16300/` | `/مجمع-عمومی-عادی-سالیانه-انجمن-آمدال/` |
| `/news/16311/` | `/مجمع-فوق-العاده-اتحادیه-تولیدکنندگا/` |
| `/news/16638/` | `/جلسات-مدیران-آبادیس-با-رؤسای-بیمارستا/` |
| `/news/16880/` | `/نظرسنجی-آبادیس-از-ایران-مد-۱۴۰۳/` |
| `/news/16906/` | `/روز-پرستار-سال-1403-آبادیس/` |
| `/news/16916/` | `/دعوت-نامه-آبادیس-در-دوازدهمین-کنگره-کن/` |
| `/news/16921/` | `/گزارش-کنگره-بین-المللی-ایران-کلین-۱۴۰۳/` |
| `/news/17014/` | `/جلسه-همفکری-جهت-بهبود-کنگره-کنترل-عفون/` |
| `/news/17024/` | `/گفتوگوی-تیترکوتاه-با-مدیرعامل-شرکت-م/` |
| `/news/17068/` | `/حمایت-آبادیس-از-کارزار-مطالبات-معوق/` |
| `/news/17077/` | `/گزارش-حضور-آبادیس-در-کنگره-کنترل-عفونت/` |
| `/news/17128/` | `/گفتوگوی-سرکار-خانم-دکتر-محرز-درباره/` |
| `/news/17173/` | `/گزارش-حضور-شرکت-مخازن-طبی-آبادیس-در-ایر/` |
| `/news/17194/` | `/مجمع-و-انتخابات-انجمن-آمدال/` |
| `/news/17214/` | `/مصاحبه-مدیران-آبادیس-با-گروه-تمپا/` |
| `/news/17277/` | `/نظرات-دکتر-رئیسی-معاون-وزارت-بهداشت-در/` |
| `/news/17283/` | `/حفاظت-از-محیط-زیست-و-کنترل-عفونت؛-دستاو/` |
| `/news/17291/` | `/چالشهای-مالی-در-صنعت-تجهیزات-پزشکی؛/` |
| `/news/17297/` | `/انتخابات-اتحادیه-بازرگانان-تجهیزات-پ/` |
| `/news/17302/` | `/تجهیزات-پزشکی-یکبار-مصرف،-کنترل-عفونت/` |
| `/news/17448/` | `/هزار-درخت-بلوط،-هزار-امید-برای-نجات-زاگ/` |
| `/news/17663/` | `/معرفی-کدینگ-محصولات-آبادیس/` |
| `/news/17688/` | `/iranhealth-iranmed/` |
| `/news/17738/` | `/برای-زندگی-ایستادهایم؛-ارسال-۸-خاور/` |
| `/news/17760/` | `/مذاکرات-بین-المللی-آبادیس-در-ایران-هلث-1/` |
| `/news/17912/` | `/صرفه-جویی-۴۰-میلیون-لیتر-آب-با-کیسه-های/` |
| `/news/17929/` | `/انتشار-مقاله-مخازن-طبی-آبادیس-در-medium/` |
| `/news/17970/` | `/بازخورد-کار-آماری-آبادیس-درباره-نمایش/` |
| `/news/18088/` | `/آبادیس-واسط-همکاری-نمایشگاه-ایرانمد/` |
| `/news/18108/` | `/گفتوگوی-مدیرعامل-شرکت-دانشبنیان-آ/` |
| `/news/18112/` | `/گفتوگوی-کامل-رادیو-سلامت-با-مدیرعامل/` |
| `/news/18140/` | `/بررسی-منابع-انسانی-در-آبادیس/` |
| `/news/18169/` | `/دعوت-به-نشست-تخصصی-تولید-پایدار-در-شرای/` |
| `/news/18195/` | `/اولین-گزارش-اقدامات-توسعه-پایدار-آباد/` |
| `/news/18205/` | `/سومین-دوره-نمایشگاه-ایرانمد-۲۰۲۵/` |
| `/news/18210/` | `/برگزاری-مجمع-عمومی-عادی-انجمن-شرکتها/` |
| `/news/18213/` | `/مجمع-عمومی-سالیانه-انجمن-تولیدکنندگا/` |
| `/news/18217/` | `/مجمع-عمومی-عادی-بهطور-فوقا/` |
| `/news/18235/` | `/nurse1404/` |
| `/news/18415/` | `/مقاله-مدیرعامل-مخازن-طبی-آبادیس-در-کنف/` |
| `/news/18446/` | `/وبینار-آموزشی-نقش-هوش-مصنوعی-و-هوش-تج/` |
| `/news/18474/` | `/چرا-مخازن-طبی-آبادیس-در-هیچیک-از-نم/` |
| `/news/18478/` | `/انتشار-کتاب-تاریخ-شفاهی-صنعت-تجهیزات/` |
| `/news/18537/` | `/مصاحبه-رئیس-هیئتمدیره-آبادیس-در-برنا/` |
| `/news/18554/` | `/پروانه-بهره-برداری-جدید-آبادیس-صادر-گر/` |
| `/news/18586/` | `/انتشار-مقاله-مدیرعامل-مخازن-طبی-آبادی/` |
| `/news/18693/` | `/آبادیس-در-روزهای-جنگ-رمضان؛-تداوم-خدمت/` |
| `/news/18779/` | `/اعلام-عدم-تمدید-عضویت-و-انتشار-نامه-سرگ/` |
| `/news/18804/` | `/آغاز-فوری-عملیات-بازسازی-کارخانه-آباد/` |
| `/news/18810/` | `/۱۷-مرداد؛-روز-خبرنگار-گرامی-باد/` |
| `/news/19204/` | `/آبادیس-پیشنهادهای-جامع-خود-برای-اصلاح/` |
| `/news/19271/` | `/استخدام-کارشناس-فروش-در-شرکت-دانشبنی/` |
| `/news/19280/` | `/آبادیس،-نخستین-شرکت-صنعت-تجهیزات-پزشک/` |
| `/news/19284/` | `/آبادیس-اجرای-بازاریابی-نسل-چهارم-و-پنج/` |
| `/news/3524/` | `/اخذ-گواهی-ce-اتحادیه-اروپا/` |
| `/news/3704/` | `/محصولات-جدید-مخازن-طبی-آبادیس-رونمایی/` |
| `/news/4968/` | `/رو-نمایی-از-محصولات-جدید-آبادیس-در-حوزه/` |
| `/news/535/` | `/گزارش-تصویری-از-حضور-آبادیس-در-نمایشگا-3/` |
| `/news/5985/` | `/اسامی-برندگان-مسابقه-روز-پرستار-سال-1400/` |
| `/news/6708/` | `/مصاحبه-مدیران-مخازن-طبی-آبادیس-با-مدیر/` |
| `/news/8/` | `/ایرانمد-۱۴۰۵؛-گردهمایی-فعالان-صنعت-ت/` |
| `/news/8008/` | `/مصاحبه-مدیران-آبادیس-با-خبرگزاری-فارس/` |
| `/news/9013/` | `/ایران-هلث-1401/` |
| `/news/9036/` | `/مصاحبه-مدیران-آبادیس-با-خبرگزاری-اخبا/` |
| `/news/9354/` | `/گزارش-بیست-و-سومین-نمایشگاه-بین-المللی/` |
| `/news/994/` | `/رونمایی-از-محصول-فیکسر-آبادیس/` |
| `/products/` | `/محصولات/` |
| `/products/canister/` | `/محصولات/مخزن/` |
| `/products/connectors/` | `/محصولات/اتصالات/` |
| `/products/filters/` | `/محصولات/فیلترها/` |
| `/products/oral-hygiene/` | `/محصولات/سواب-های-دهانی-و-نگهدارنده/` |
| `/products/other/` | `/محصولات/سایر-محصولات/` |

Product category labels and order follow the live products-page cards. These slugs are unchanged, and no new category 301 was added.
| `/products/stand/` | `/محصولات/پایه/` |
| `/products/suction-bag/` | `/محصولات/کیسه-ساکشن/` |
| `/products/suction-tube/` | `/محصولات/ساکشن-تیوب/` |
| `/sdgs/` | `/توسعه-پایدار/` |
| `/en/careers/` | `/en/collaboration-opportunities/` (duplicate copy replaced by a redirect) |

## Live pages with no redesign page (content to build)

| live URL | temporary 301 target |
|---|---|
| `/en/canister-installation/` | `/en/installation-manual/` |
| `/en/products/specialized-bags-waste-management/` | `/en/solutions/waste-management-pva/` |
| `/en/user-manuals/` | `/en/installation-manual/` |
| `/en/business-intelligence-bi-transforming-the-medical-device-industry/` | `/en/blog/` |
| `/en/from-the-operating-room-to-infection-control-the-role-of-suction-liners-in-veterinary-medicine/` | `/en/blog/` |
| `/en/oral-hygiene-in-hospitals-from-essential-patient-care-to-specialized-medical-equipment/` | `/en/blog/` |
| `/en/un-sdgs-and-infection-control/` | `/en/blog/` |
| `/en/what-is-a-chest-bottle-types-applications-and-how-chest-drainage-systems-work/` | `/en/blog/` |
| `/en/what-is-a-microdrip-set-uses-components-differences-from-macrodrip-sets/` | `/en/blog/` |
| `/en/what-is-an-iv-infusion-set-a-comprehensive-guide-to-types-components-applications-and-safety-standards/` | `/en/blog/` |
| `/محصولات/کیسه-های-تخصصی-و-مدیریت-پسماند-2/` | `/solutions/waste-management-pva/` |
| `/از-اتاق-عمل-تا-کنترل-عفونت؛-نقش-کیسه-ساک/` | `/مقالات/` |
| `/رنگبندی-کیسههای-زباله-بیمارستانی/` | `/مقالات/` |
| `/۴-برند-تولیدکننده-کیسه-ساکشن-در-جهان-که/` | `/مقالات/` |

## Redesign-only pages (no live equivalent, kept)

- `/3d-sketches/all-products/`
- `/3d-sketches/cad-line-sketches/`
- `/3d-sketches/p05-2l-cinematic/`
- `/3d-sketches/p05-2l-set-cinematic/`
- `/3d-sketches/p05-3l-cinematic/`
- `/3d-sketches/p05-3l-set-cinematic/`
- `/3d-sketches/p05-cinematic/`
- `/academy/`
- `/academy/_full/`
- `/academy/login/`
- `/arabic/academy/`
- `/arabic/academy/_full/`
- `/arabic/academy/login/`
- `/arabic/articles/`
- `/arabic/careers/`
- `/arabic/csr/`
- `/arabic/customers/`
- `/arabic/export/`
- `/arabic/green-family-map/`
- `/arabic/sdgs/`
- `/arabic/seed-slingshot/`
- `/arabic/sustainability/`
- `/arabic/الحلول/`
- `/arabic/الحلول/airway-care/`
- `/arabic/الحلول/contamination-control/`
- `/arabic/الحلول/fluid-management/`
- `/arabic/الحلول/hospital-suction-systems/`
- `/arabic/الحلول/icu-anesthesia/`
- `/arabic/الحلول/or-efficiency/`
- `/arabic/الحلول/waste-management-pva/`
- `/arabic/نظافة-الفم/`
- `/articles-options/`
- `/brand/section-logos/`
- `/careers-options/`
- `/chatbot-demo/`
- `/contact-hero-options/`
- `/dial-designs/1-light-neumorphic/`
- `/dial-designs/2-abadis-plus/`
- `/dial-designs/3-cost-time-h2o/`
- `/dial-practical/`
- `/dial-steppers/`
- `/en/academy/`
- `/en/academy/_full/`
- `/en/academy/login/`
- `/en/export/`
- `/en/green-family-map/`
- `/en/seed-slingshot/`
- `/en/solutions/`
- `/en/solutions/airway-care/`
- `/en/solutions/contamination-control/`
- `/en/solutions/fluid-management/`
- `/en/solutions/hospital-suction-systems/`
- `/en/solutions/icu-anesthesia/`
- `/en/solutions/or-efficiency/`
- `/en/solutions/waste-management-pva/`
- `/en/sustainability/`
- `/export/`
- `/green-family-map/`
- `/hero-options/`
- `/hero-options/1-product/`
- `/hero-options/2-dial/`
- `/hero-options/3-numbers/`
- `/hero-options/4-still-life/`
- `/hero-options/5-map/`
- `/hero-options/6-savings/`
- `/hero-options/7-oak/`
- `/hero-options/8-quality/`
- `/hero-test/birds/`
- `/home-hero-options/`
- `/news-hero-options/`
- `/news-hero-options/1-editorial-split/`
- `/news-hero-options/2-bento-magazine/`
- `/news-hero-options/3-press-timeline/`
- `/news-hero-options/4-serres-calm-minimal/`
- `/news-hero-options/5-interactive-category-showcase/`
- `/news-hero-options/6-cinematic-spotlight-slider/`
- `/news-hero-options/7-newspaper-broadsheet-grid/`
- `/news-hero-options/8-impact-media-wall/`
- `/news-hero-options/9-search-command-hub/`
- `/news-hero-options/finalist-a-bento/`
- `/news-hero-options/finalist-b-media-wall/`
- `/news-hero-options/finalist-c-d3/`
- `/news-hero-options/finalist-d-hybrid/`
- `/seed-slingshot/`
- `/seed-slingshot/_full/`
- `/solutions-hero-options/`
- `/solutions/`
- `/solutions/airway-care/`
- `/solutions/contamination-control/`
- `/solutions/fluid-management/`
- `/solutions/hospital-suction-systems/`
- `/solutions/icu-anesthesia/`
- `/solutions/or-efficiency/`
- `/solutions/waste-management-pva/`
- `/sustainability/`
- `/template-dials/1-neumorphic/`
- `/template-dials/2-abadis-plus/`
- `/template-dials/3-cost-time-h2o/`
- `/why-abadis-options/`
- `/zagros-names/`
- `/zagros-names/1-tree-tags/`
- `/zagros-names/2-sky-ribbons/`
- `/zagros-names/3-wall-of-honor/`
- `/zagros-names/4-mix/`
- `/محاسبه-گر/dial/`
- `/محاسبه-گر/flood/`
- `/محاسبه-گر/hospital/`
- `/محاسبه-گر/receipt/`
- `/محاسبه-گر/scale/`

## How redirects work

- Every old path keeps a stub `index.html` (meta refresh + JS redirect, canonical = new URL, noindex), so GitHub Pages works.
- `site/liara_nginx.conf` (Liara static platform, included in the server block) and `site/redirects-nginx.conf` carry real 301s
  to `https://$host/<percent-encoded live path>`; `site/_redirects` has the same map for Netlify/Cloudflare.
- `docs/redirect-map-301.md`, `docs/redirects-301.csv` and `tools/redesign/redirects-301.conf` describe the previous `/products/<x>/`
  architecture and are superseded by this file.
