# جدول جامع ریدایرکت‌های ۳۰۱ (301 Redirect Map) — انتقال بدون افت سئو از سایت فعلی به سایت جدید

- **تعداد کل قوانین ریدایرکت ۳۰۱:** `198` مسیر یکتا (شامل تمامی صفحات اصلی، ۲۳ محصول، مقالات علمی، اخبار، دسته‌بندی‌های وردپرس و صفحات انگلیسی و عربی)
- **فایل کانفیگ Nginx:** [`site/redirects-nginx.conf`](../site/redirects-nginx.conf) و [`tools/redesign/redirects-301.conf`](../tools/redesign/redirects-301.conf)
- **فایل استاندارد `_redirects` (مناسب Cloudflare / Netlify):** [`site/_redirects`](../site/_redirects)
- **فلسفه معماری URL جدید:** در سایت وردپرسی فعلی، تمامی محصولات (`/suction-bag/`, `/paye/`, ...) و تمامی مقالات و اخبار (`/<post-slug>/`) مستقیماً در ریشه دامنه (`/`) قرار داشتند. در سایت جدید، محصولات در `/products/<slug>/`، مقالات در `/articles/<slug>/` و اخبار در `/news/<slug>/` ساختاردهی شده‌اند و تمام URLهای قدیمی همگی با کد `301 Moved Permanently` به آدرس جدید هدایت می‌شوند.

| ردیف | آدرس قدیم در `abadis-med.com` | آدرس جدید در سایت بازطراحی‌شده | دسته‌بندی | توضیح / عنوان |
|---|---|---|---|---|
| 1 | `/home/` | `/` | صفحات اصلی و محصولات (FA) | صفحه اصلی (وردپرس قدیمی) |
| 2 | `/about-us/` | `/about/` | صفحات اصلی و محصولات (FA) | درباره ما |
| 3 | `/contact-us/` | `/contact/` | صفحات اصلی و محصولات (FA) | ارتباط با ما |
| 4 | `/blog/` | `/articles/` | صفحات اصلی و محصولات (FA) | مقالات علمی و تخصصی |
| 5 | `/save-zagros/` | `/csr/` | صفحات اصلی و محصولات (FA) | پویش نجات زاگرس / مسئولیت اجتماعی |
| 6 | `/sustainable-development/` | `/sdgs/` | صفحات اصلی و محصولات (FA) | توسعه پایدار (SDGs) |
| 7 | `/sustainability/` | `/sdgs/` | صفحات اصلی و محصولات (FA) | توسعه پایدار (مسیر جایگزین) |
| 8 | `/collaboration-opportunities/` | `/careers/` | صفحات اصلی و محصولات (FA) | فرصت‌های شغلی و همکاری |
| 9 | `/center-download/` | `/downloads/` | صفحات اصلی و محصولات (FA) | مرکز دانلود کاتالوگ و راهنما |
| 10 | `/installation-manual/` | `/guide/` | صفحات اصلی و محصولات (FA) | راهنمای مصرف‌کننده نهایی و نصب |
| 11 | `/rahnama-nasb-va-estefade/` | `/guide/` | صفحات اصلی و محصولات (FA) | راهنمای نصب و استفاده قدیمی |
| 12 | `/after-sales-service/` | `/services/` | صفحات اصلی و محصولات (FA) | خدمات پس از فروش |
| 13 | `/exhibitions/` | `/events/` | صفحات اصلی و محصولات (FA) | نمایشگاه‌ها، کنگره‌ها و رویدادها |
| 14 | `/congress/` | `/events/` | صفحات اصلی و محصولات (FA) | کنگره‌ها و سمپوزیوم‌ها |
| 15 | `/workshops/` | `/events/` | صفحات اصلی و محصولات (FA) | کارگاه‌های آموزشی |
| 16 | `/feedback/` | `/contact/#feedback` | صفحات اصلی و محصولات (FA) | فرم ثبت نظرات و شکایات |
| 17 | `/sales-inquiry/` | `/contact/#inquiry` | صفحات اصلی و محصولات (FA) | فرم استعلام قیمت و خرید |
| 18 | `/product/` | `/products/` | صفحات اصلی و محصولات (FA) | فهرست محصولات |
| 19 | `/suction-bag/` | `/products/suction-bag/` | صفحات اصلی و محصولات (FA) | کیسه ساکشن یکبار مصرف |
| 20 | `/filter/` | `/products/filters/` | صفحات اصلی و محصولات (FA) | فیلترهای ساکشن |
| 21 | `/filters/` | `/products/filters/` | صفحات اصلی و محصولات (FA) | فیلترهای ساکشن |
| 22 | `/anti/` | `/products/anti/` | صفحات اصلی و محصولات (FA) | فیلتر آنتی‌باکتریال |
| 23 | `/ght/` | `/products/ght/` | صفحات اصلی و محصولات (FA) | فیلتر قطع‌کننده جریان |
| 24 | `/mot/` | `/products/mot/` | صفحات اصلی و محصولات (FA) | فیلتر متخلخل |
| 25 | `/paye/` | `/products/paye/` | صفحات اصلی و محصولات (FA) | پایه ساکشن پرتابل (ترولی) |
| 26 | `/wallg/` | `/products/wallg/` | صفحات اصلی و محصولات (FA) | گیره مخزن دیواری |
| 27 | `/wallp/` | `/products/wallp/` | صفحات اصلی و محصولات (FA) | پشت گیره مخزن پرتابل |
| 28 | `/tube/` | `/products/Tube/` | صفحات اصلی و محصولات (FA) | ساکشن تیوب استریل |
| 29 | `/Tube/` | `/products/Tube/` | صفحات اصلی و محصولات (FA) | ساکشن تیوب استریل |
| 30 | `/fingertip/` | `/products/Fingertip/` | صفحات اصلی و محصولات (FA) | فینگرتیپ (رابط ساکشن) |
| 31 | `/Fingertip/` | `/products/Fingertip/` | صفحات اصلی و محصولات (FA) | فینگرتیپ (رابط ساکشن) |
| 32 | `/msk/` | `/products/msk/` | صفحات اصلی و محصولات (FA) | مخازن ساکشن پلی‌کربنات |
| 33 | `/sdv/` | `/products/sdv/` | صفحات اصلی و محصولات (FA) | ساکشن دیواری |
| 34 | `/collectioncup/` | `/products/collectioncup/` | صفحات اصلی و محصولات (FA) | محفظه نمونه‌گیری (Collection Cup) |
| 35 | `/lipo/` | `/products/lipo/` | صفحات اصلی و محصولات (FA) | مخزن جمع‌آوری چربی (لیپوساکشن) |
| 36 | `/tsh/` | `/products/tsh/` | صفحات اصلی و محصولات (FA) | اتصال T شکل |
| 37 | `/cnt/` | `/products/cnt/` | صفحات اصلی و محصولات (FA) | کانکتور |
| 38 | `/shl/` | `/products/shl/` | صفحات اصلی و محصولات (FA) | شلنگ سیلیکونی |
| 39 | `/rgl/` | `/products/rgl/` | صفحات اصلی و محصولات (FA) | رگولاتور وکیوم |
| 40 | `/shr/` | `/products/shr/` | صفحات اصلی و محصولات (FA) | شیر ON/OFF |
| 41 | `/sri/` | `/products/sri/` | صفحات اصلی و محصولات (FA) | سری شلنگ و اتصالات |
| 42 | `/swab/` | `/products/swab/` | صفحات اصلی و محصولات (FA) | سوآب دهانی |
| 43 | `/mesvak/` | `/products/mesvak/` | صفحات اصلی و محصولات (FA) | مسواک ساکشن یکبار مصرف |
| 44 | `/negahdarande/` | `/products/negahdarande/` | صفحات اصلی و محصولات (FA) | نگهدارنده لوله تراشه (فیکسر) |
| 45 | `/receiver/` | `/products/receiver/` | صفحات اصلی و محصولات (FA) | رسیور یکبار مصرف (Kidney Dish) |
| 46 | `/splashvac/` | `/products/splashvac/` | صفحات اصلی و محصولات (FA) | ساکشن زمینی چندمنظوره (Splash-Vac) |
| 47 | `/en/home/` | `/en/` | صفحات انگلیسی (EN) | English Home (WP legacy) |
| 48 | `/en/blog/` | `/en/articles/` | صفحات انگلیسی (EN) | English Scientific Articles (alias also served directly) |
| 49 | `/en/news/` | `/en/latest-news/` | صفحات انگلیسی (EN) | English Latest News |
| 50 | `/en/collaboration-opportunities/` | `/en/careers/` | صفحات انگلیسی (EN) | English Careers (both paths served with full C1 dashboard) |
| 51 | `/en/sustainable-development/` | `/en/sdgs/` | صفحات انگلیسی (EN) | English Sustainable Development |
| 52 | `/en/sustainability/` | `/en/sdgs/` | صفحات انگلیسی (EN) | English Sustainability |
| 53 | `/en/save-zagros/` | `/en/csr/` | صفحات انگلیسی (EN) | English Save Zagros / CSR |
| 54 | `/en/customers/` | `/en/our-customers/` | صفحات انگلیسی (EN) | English Customers |
| 55 | `/en/contact/` | `/en/contact-us/` | صفحات انگلیسی (EN) | English Contact Us |
| 56 | `/en/about/` | `/en/about-us/` | صفحات انگلیسی (EN) | English About Us |
| 57 | `/en/downloads/` | `/en/center-download/` | صفحات انگلیسی (EN) | English Download Center |
| 58 | `/en/guide/` | `/en/installation-manual/` | صفحات انگلیسی (EN) | English Installation Manual |
| 59 | `/en/services/` | `/en/after-sales-service/` | صفحات انگلیسی (EN) | English After-Sales Service |
| 60 | `/en/events/` | `/en/exhibitions/` | صفحات انگلیسی (EN) | English Exhibitions & Events |
| 61 | `/en/suction-bag/` | `/en/products/suction-bag/` | صفحات انگلیسی (EN) | English Suction Bag |
| 62 | `/en/filter/` | `/en/products/filters/` | صفحات انگلیسی (EN) | English Filters |
| 63 | `/arabic/home/` | `/arabic/` | صفحات عربی (AR) | Arabic Home (WP legacy) |
| 64 | `/arabic/about-us/` | `/arabic/من-نحن/` | صفحات عربی (AR) | Arabic About Us |
| 65 | `/arabic/contact-us/` | `/arabic/اتصل-بنا/` | صفحات عربی (AR) | Arabic Contact Us |
| 66 | `/arabic/solutions/` | `/arabic/الحلول/` | صفحات عربی (AR) | Arabic Solutions |
| 67 | `/arabic/news/` | `/arabic/الاخبار/` | صفحات عربی (AR) | Arabic Latest News |
| 68 | `/arabic/blog/` | `/arabic/articles/` | صفحات عربی (AR) | Arabic Articles |
| 69 | `/arabic/sustainable-development/` | `/arabic/sdgs/` | صفحات عربی (AR) | Arabic Sustainable Development |
| 70 | `/arabic/save-zagros/` | `/arabic/csr/` | صفحات عربی (AR) | Arabic CSR / Save Zagros |
| 71 | `/arabic/collaboration-opportunities/` | `/arabic/careers/` | صفحات عربی (AR) | Arabic Careers |
| 72 | `/arabic/our-customers/` | `/arabic/customers/` | صفحات عربی (AR) | Arabic Customers |
| 73 | `/arabic/center-download/` | `/arabic/مركز-التنزيل/` | صفحات عربی (AR) | Arabic Download Center |
| 74 | `/arabic/installation-manual/` | `/arabic/دليل-التركيب/` | صفحات عربی (AR) | Arabic Installation Guide |
| 75 | `/arabic/after-sales-service/` | `/arabic/خدمات-ما-بعد-البيع/` | صفحات عربی (AR) | Arabic After-Sales Service |
| 76 | `/en/the-future-of-medical-devices-with-artificial-intelligence-technologies-transforming-healthcare/` | `/en/latest-news/the-future-of-medical-devices-with-artificial-intelligence-technologies-transforming-healthcare/` | پست انگلیسی (EN Post) | The Future of Medical Devices with Artificial Intelligence:  |
| 77 | `/en/reusable-suction-canisters-an-economical-choice-or-a-hidden-cost-for-hospitals/` | `/en/latest-news/reusable-suction-canisters-an-economical-choice-or-a-hidden-cost-for-hospitals/` | پست انگلیسی (EN Post) | Reusable Suction Canisters: An Economical Choice or a Hidden |
| 78 | `/en/urine-bag-buying-guide-types-features-and-selection-tips/` | `/en/latest-news/urine-bag-buying-guide-types-features-and-selection-tips/` | پست انگلیسی (EN Post) | Urine Bag Buying Guide: Types, Features, and Selection Tips |
| 79 | `/en/what-are-pva-film-bags-applications-benefits-and-their-role-in-infection-control/` | `/en/latest-news/what-are-pva-film-bags-applications-benefits-and-their-role-in-infection-control/` | پست انگلیسی (EN Post) | What Are PVA FILM Bags? Applications, Benefits, and Their Ro |
| 80 | `/en/a-guide-to-purchasing-disposable-suction-liner-bags-for-healthcare-facilities/` | `/en/latest-news/a-guide-to-purchasing-disposable-suction-liner-bags-for-healthcare-facilities/` | پست انگلیسی (EN Post) | A Guide to Purchasing Disposable Suction Liner Bags for Heal |
| 81 | `/en/what-is-an-oropharyngeal-airway-opa/` | `/en/latest-news/what-is-an-oropharyngeal-airway-opa/` | پست انگلیسی (EN Post) | What Is an Oropharyngeal Airway (OPA)? |
| 82 | `/en/what-is-a-nelaton-catheter/` | `/en/latest-news/what-is-a-nelaton-catheter/` | پست انگلیسی (EN Post) | What Is a Nelaton Catheter? |
| 83 | `/en/what-is-an-extension-tube/` | `/en/latest-news/what-is-an-extension-tube/` | پست انگلیسی (EN Post) | What Is an Extension Tube? |
| 84 | `/en/what-are-antibacterial-filters-and-hydrophobic-filters/` | `/en/latest-news/what-are-antibacterial-filters-and-hydrophobic-filters/` | پست انگلیسی (EN Post) | What Are Antibacterial Filters and Hydrophobic Filters? |
| 85 | `/en/what-is-a-chest-tube/` | `/en/latest-news/what-is-a-chest-tube/` | پست انگلیسی (EN Post) | What Is a Chest Tube? |
| 86 | `/en/the-role-of-disposable-suction-liners-in-hospital-infectious-waste-management/` | `/en/latest-news/the-role-of-disposable-suction-liners-in-hospital-infectious-waste-management/` | پست انگلیسی (EN Post) | The Role of Disposable Suction Liners in Hospital Infectious |
| 87 | `/en/what-is-a-wall-suction-system/` | `/en/latest-news/what-is-a-wall-suction-system/` | پست انگلیسی (EN Post) | What Is a Wall Suction System? |
| 88 | `/en/the-role-of-disposable-suction-bags-in-reducing-the-risk-of-hantavirus-transmission-in-hospitals/` | `/en/latest-news/the-role-of-disposable-suction-bags-in-reducing-the-risk-of-hantavirus-transmission-in-hospitals/` | پست انگلیسی (EN Post) | The Role of Disposable Suction Bags in Reducing the Risk of  |
| 89 | `/en/what-is-hantavirus/` | `/en/latest-news/what-is-hantavirus/` | پست انگلیسی (EN Post) | What is hantavirus? |
| 90 | `/en/20-leading-scientific-journals-in-the-medical-device-industry/` | `/en/latest-news/20-leading-scientific-journals-in-the-medical-device-industry/` | پست انگلیسی (EN Post) | 20 Leading Scientific Journals in the Medical Device Industr |
| 91 | `/en/endotracheal-tube-fixation-enhancing-patient-safety-comfort-and-infection-control/` | `/en/latest-news/endotracheal-tube-fixation-enhancing-patient-safety-comfort-and-infection-control/` | پست انگلیسی (EN Post) | Endotracheal Tube Fixation: Enhancing Patient Safety, Comfor |
| 92 | `/en/abadis-medical-filters-maximum-safety-in-hospital-infection-control/` | `/en/latest-news/abadis-medical-filters-maximum-safety-in-hospital-infection-control/` | پست انگلیسی (EN Post) | Abadis Medical Filters: Maximum Safety in Hospital Infection |
| 93 | `/en/the-role-of-knowledge-based-industries-in-achieving-green-governance/` | `/en/latest-news/the-role-of-knowledge-based-industries-in-achieving-green-governance/` | پست انگلیسی (EN Post) | The Role of Knowledge-Based Industries in Achieving Green Go |
| 94 | `/en/human-capital-development-at-abadis-med-co/` | `/en/latest-news/human-capital-development-at-abadis-med-co/` | پست انگلیسی (EN Post) | Human Capital Development at Abadis med Co. |
| 95 | `/en/abadis-international-negotiations-at-iran-health-2025/` | `/en/latest-news/abadis-international-negotiations-at-iran-health-2025/` | پست انگلیسی (EN Post) | Abadis’ International Negotiations at Iran Health 2025 |
| 96 | `/en/full-interview-with-the-ceo-of-abadis-on-radio-salamats-program-ta-soraya/` | `/en/latest-news/full-interview-with-the-ceo-of-abadis-on-radio-salamats-program-ta-soraya/` | پست انگلیسی (EN Post) | Full interview with the CEO of Abadis on Radio Salamat’s pro |
| 97 | `/en/abadis-bridges-cooperation-between-iranmed-exhibition-and-baloot-e-dalahoo-association/` | `/en/latest-news/abadis-bridges-cooperation-between-iranmed-exhibition-and-baloot-e-dalahoo-association/` | پست انگلیسی (EN Post) | Abadis Bridges Cooperation Between IranMed Exhibition and Ba |
| 98 | `/en/what-is-a-sterile-disposable-suction-bag/` | `/en/latest-news/what-is-a-sterile-disposable-suction-bag/` | پست انگلیسی (EN Post) | What Is a Sterile Disposable Suction Bag? |
| 99 | `/en/existing-standards-in-the-production-of-medical-suction-tubes/` | `/en/latest-news/existing-standards-in-the-production-of-medical-suction-tubes/` | پست انگلیسی (EN Post) | Existing Standards in the Production of Medical Suction Tube |
| 100 | `/en/existing-standards-for-the-production-of-disposable-suction-liner-bags/` | `/en/latest-news/existing-standards-for-the-production-of-disposable-suction-liner-bags/` | پست انگلیسی (EN Post) | Existing Standards for the Production of Disposable Suction  |
| 101 | `/en/abadis-med-publishes-article-on-medium/` | `/en/latest-news/abadis-med-publishes-article-on-medium/` | پست انگلیسی (EN Post) | Abadis Med Publishes Article on Medium |
| 102 | `/en/the-critical-role-of-medical-grade-pvc-in-suction-tube-products/` | `/en/latest-news/the-critical-role-of-medical-grade-pvc-in-suction-tube-products/` | پست انگلیسی (EN Post) | The Critical Role of Medical-Grade PVC in Suction Tube Produ |
| 103 | `/en/standardized-cleaning-procedures-for-reusable-suction-canisters-and-safe-handling-of-disposable-suction-liners-in-clinical-settings/` | `/en/latest-news/standardized-cleaning-procedures-for-reusable-suction-canisters-and-safe-handling-of-disposable-suction-liners-in-clinical-settings/` | پست انگلیسی (EN Post) | Standardized Cleaning Procedures for Reusable Suction Canist |
| 104 | `/en/why-disposable-suction-liner-bags-can-save-patients-lives/` | `/en/latest-news/why-disposable-suction-liner-bags-can-save-patients-lives/` | پست انگلیسی (EN Post) | Why Disposable Suction liner bags Can Save Patients’ Lives |
| 105 | `/en/abadis-medical-publishes-its-first-comprehensive-sustainability-report-up-to-march-2025/` | `/en/latest-news/abadis-medical-publishes-its-first-comprehensive-sustainability-report-up-to-march-2025/` | پست انگلیسی (EN Post) |  Abadis Medical Publishes Its First Comprehensive Sustainabi |
| 106 | `/en/the-first-sustainability-report-of-abadis-medical-knowledge-based-company-up-to-the-end-of-2024/` | `/en/latest-news/the-first-sustainability-report-of-abadis-medical-knowledge-based-company-up-to-the-end-of-2024/` | پست انگلیسی (EN Post) | The First Sustainability Report of Abadis Medical Knowledge- |
| 107 | `/en/top-5-features-to-look-for-in-a-medical-suction-tube/` | `/en/latest-news/top-5-features-to-look-for-in-a-medical-suction-tube/` | پست انگلیسی (EN Post) | Top 5 Features to Look for in a Medical Suction Tube |
| 108 | `/en/achievements-of-abadis-med-company-in-developing-disposable-suction-bags/` | `/en/latest-news/achievements-of-abadis-med-company-in-developing-disposable-suction-bags/` | پست انگلیسی (EN Post) | Achievements of Abadis Med Company in Developing Disposable  |
| 109 | `/en/water-conservation-through-abadis-disposable-suction-bags/` | `/en/latest-news/water-conservation-through-abadis-disposable-suction-bags/` | پست انگلیسی (EN Post) | Water Conservation through Abadis Disposable Suction Bags |
| 110 | `/en/disposable-suction-liner-bags-vs-reusable-ones/` | `/en/latest-news/disposable-suction-liner-bags-vs-reusable-ones/` | پست انگلیسی (EN Post) | Why Hospitals Prefer Disposable Suction Liner Bags Over Reus |
| 111 | `/en/pva-film-in-the-medical-equipment-industry/` | `/en/latest-news/pva-film-in-the-medical-equipment-industry/` | پست انگلیسی (EN Post) | PVA Film in the Medical Equipment Industry |
| 112 | `/en/super-absorbent-powder-in-the-medical-equipment-industry/` | `/en/latest-news/super-absorbent-powder-in-the-medical-equipment-industry/` | پست انگلیسی (EN Post) | Super Absorbent Powder in the Medical Equipment Industry |
| 113 | `/en/porous-filters-in-the-medical-industry/` | `/en/latest-news/porous-filters-in-the-medical-industry/` | پست انگلیسی (EN Post) | Porous Filters in the Medical Industry |
| 114 | `/en/what-is-a-suction-tube/` | `/en/latest-news/what-is-a-suction-tube/` | پست انگلیسی (EN Post) | What Is a Suction Tube? |
| 115 | `/en/what-is-suction-tube/` | `/en/latest-news/what-is-suction-tube/` | پست انگلیسی (EN Post) | What Is Suction Tube? |
| 116 | `/en/introduction-of-disposable-suction-liner-bags-a-key-solution-by-abadis-for-preventing-nosocomial-infections/` | `/en/latest-news/introduction-of-disposable-suction-liner-bags-a-key-solution-by-abadis-for-preventing-nosocomial-infections/` | پست انگلیسی (EN Post) | Introduction of Disposable Suction Liner Bags: A Key Solutio |
| 117 | `/en/the-report-of-the-second-salamat-bonyan-basic-health-exhibition/` | `/en/latest-news/the-report-of-the-second-salamat-bonyan-basic-health-exhibition/` | پست انگلیسی (EN Post) | The Report Of The Second Salamat Bonyan (The Health Based) E |
| 118 | `/en/mangement-of-hospital-infectious-waste/` | `/en/latest-news/mangement-of-hospital-infectious-waste/` | پست انگلیسی (EN Post) | Mangement Of Hospital Infectious Waste |
| 119 | `/en/assessment-of-hand-hygiene-compliance-among-healthcare-workers-in-zahedan-social-security-hospital-in-2023/` | `/en/latest-news/assessment-of-hand-hygiene-compliance-among-healthcare-workers-in-zahedan-social-security-hospital-in-2023/` | پست انگلیسی (EN Post) | Assessment of Hand Hygiene Compliance among Healthcare Worke |
| 120 | `/en/disposable-suction-bottle-is-cost-effective-in-iran-or-not/` | `/en/latest-news/disposable-suction-bottle-is-cost-effective-in-iran-or-not/` | پست انگلیسی (EN Post) | Disposable suction bottle: Is cost-effective in Iran or not? |
| 121 | `/en/infection-control-congress-report-2023/` | `/en/latest-news/infection-control-congress-report-2023/` | پست انگلیسی (EN Post) | Infection Control Congress Report 2023 |
| 122 | `/en/honoring-ceremony-for-professor-valiollah-mehrabi/` | `/en/latest-news/honoring-ceremony-for-professor-valiollah-mehrabi/` | پست انگلیسی (EN Post) | Honoring Ceremony for Professor Valiollah Mehrabi |
| 123 | `/en/publication-of-the-article-entitled-improving-the-environmental-effects-of-nosocomial-infectious-effluents-by-using-disposable-suction-liner-bags-in-the-journal-of-biomedical-and-allied-research/` | `/en/latest-news/publication-of-the-article-entitled-improving-the-environmental-effects-of-nosocomial-infectious-effluents-by-using-disposable-suction-liner-bags-in-the-journal-of-biomedical-and-allied-research/` | پست انگلیسی (EN Post) | Publication of an article by Abadis in ISI journal |
| 124 | `/en/report-of-the-international-medical-equipment-exhibition-of-uzbekistan-2023/` | `/en/latest-news/report-of-the-international-medical-equipment-exhibition-of-uzbekistan-2023/` | پست انگلیسی (EN Post) | Report of the International Medical Equipment Exhibition of  |
| 125 | `/en/improving-the-environmental-effects-of-nosocomial-infectious-effluents-by-using-disposable-suction-liner-bags/` | `/en/latest-news/improving-the-environmental-effects-of-nosocomial-infectious-effluents-by-using-disposable-suction-liner-bags/` | پست انگلیسی (EN Post) | Improving The Environmental Effects Of Nosocomial Infectious |
| 126 | `/en/the-presence-of-abadis-at-uzmedexpo/` | `/en/latest-news/the-presence-of-abadis-at-uzmedexpo/` | پست انگلیسی (EN Post) | The Presence Of Abadis At Uzmedexpo |
| 127 | `/en/hospital-infection-surveillance-system-and-prevention-and-control-of-infection-associated-with-health-care-services/` | `/en/latest-news/hospital-infection-surveillance-system-and-prevention-and-control-of-infection-associated-with-health-care-services/` | پست انگلیسی (EN Post) | Hospital Infection Surveillance System And Prevention And Co |
| 128 | `/en/executive-guideline-for-the-disinfection-of-medical-tools-and-equipment/` | `/en/latest-news/executive-guideline-for-the-disinfection-of-medical-tools-and-equipment/` | پست انگلیسی (EN Post) | Executive Guideline for the Disinfection of Medical Tools an |
| 129 | `/en/report-on-the-10th-infection-control-congress/` | `/en/latest-news/report-on-the-10th-infection-control-congress/` | پست انگلیسی (EN Post) | Report on the 10th Infection Control Congress |
| 130 | `/en/abadis-unveils-its-new-product-for-filtration/` | `/en/latest-news/abadis-unveils-its-new-product-for-filtration/` | پست انگلیسی (EN Post) | Abadis Unveils its New Product for Filtration |
| 131 | `/en/the-presence-of-makhazen-tebi-abadis-at-the-tabriz-medical-equipment-exhibition/` | `/en/latest-news/the-presence-of-makhazen-tebi-abadis-at-the-tabriz-medical-equipment-exhibition/` | پست انگلیسی (EN Post) | The Presence of Abadis Med at the Tabriz Medical Equipment E |
| 132 | `/en/the-presence-of-mkhazen-tebi-abadis-at-the-mashhad-medical-equipment-exhibition/` | `/en/latest-news/the-presence-of-mkhazen-tebi-abadis-at-the-mashhad-medical-equipment-exhibition/` | پست انگلیسی (EN Post) | The Presence of Abadis Med at the Mashhad Medical Equipment  |
| 133 | `/en/report-of-the-23rd-iran-health-international-exhibition/` | `/en/latest-news/report-of-the-23rd-iran-health-international-exhibition/` | پست انگلیسی (EN Post) | Report of the 23rd Iran Health International Exhibition |
| 134 | `/en/interview-of-managers-of-makhazen-tebi-abadis-with-medirence/` | `/en/latest-news/interview-of-managers-of-makhazen-tebi-abadis-with-medirence/` | پست انگلیسی (EN Post) | Interview of Managers of Abadis Med With Medirence |
| 135 | `/en/new-products-makhazen-tebi-abadis/` | `/en/latest-news/new-products-makhazen-tebi-abadis/` | پست انگلیسی (EN Post) | New products of Abadis Med |
| 136 | `/en/obtaining-europe-ce-certification/` | `/en/latest-news/obtaining-europe-ce-certification/` | پست انگلیسی (EN Post) | Obtaining  Europe CE certification |
| 137 | `/en/abadis-activities-during-the-corona-2/` | `/en/latest-news/abadis-activities-during-the-corona-2/` | پست انگلیسی (EN Post) | Abadis Activities During the Corona |
| 138 | `/en/control-of-corona-virus/` | `/en/latest-news/control-of-corona-virus/` | پست انگلیسی (EN Post) | Important Health Tips in the Prevention and Control of Coron |
| 139 | `/en/how-to-distinguish-corona-from-colds-and-flu/` | `/en/latest-news/how-to-distinguish-corona-from-colds-and-flu/` | پست انگلیسی (EN Post) | How to Distinguish Corona from Colds and Flu? |
| 140 | `/en/abadis-medical-reservoirs-in-the-14th-isfahan-medical-equipment-exhibition/` | `/en/latest-news/abadis-medical-reservoirs-in-the-14th-isfahan-medical-equipment-exhibition/` | پست انگلیسی (EN Post) | Abadis in the 14th Isfahan Medical Equipment Exhibition |
| 141 | `/en/participation-of-abadis-medical-reservoirs-in-the-fourth-shiraz-medical-equipment-exhibition/` | `/en/latest-news/participation-of-abadis-medical-reservoirs-in-the-fourth-shiraz-medical-equipment-exhibition/` | پست انگلیسی (EN Post) | Participation of Abadis Med in the Fourth Shiraz Medical Equ |
| 142 | `/en/medical-engineering-monthly-interview-with-abadis-medical-reservoirs-strategic-consultant/` | `/en/latest-news/medical-engineering-monthly-interview-with-abadis-medical-reservoirs-strategic-consultant/` | پست انگلیسی (EN Post) | Medical Engineering Monthly Interview with Abadis Med Strate |
| 143 | `/en/types-of-suction-devices/` | `/en/latest-news/types-of-suction-devices/` | پست انگلیسی (EN Post) | Types of Suction Devices |
| 144 | `/en/what-is-a-suctioning-device/` | `/en/latest-news/what-is-a-suctioning-device/` | پست انگلیسی (EN Post) | What is a Suction Device? |
| 145 | `/en/abadis-medical-reservoirs-in-iran-health-exhibition-on-medirence-website/` | `/en/latest-news/abadis-medical-reservoirs-in-iran-health-exhibition-on-medirence-website/` | پست انگلیسی (EN Post) | Abadis Medical Co.  in Iran Health Exhibition on Medirence W |
| 146 | `/en/iran-radio-interview-with-abadis-medical/` | `/en/latest-news/iran-radio-interview-with-abadis-medical/` | پست انگلیسی (EN Post) | Radio Iran Interview with Abadis Medical in Iran Health 98 E |
| 147 | `/en/interview-with-colleagues-and-managers-of-abadis-medical-reservoirs-in-iran-health-98-exhibition/` | `/en/latest-news/interview-with-colleagues-and-managers-of-abadis-medical-reservoirs-in-iran-health-98-exhibition/` | پست انگلیسی (EN Post) | Interview with Colleagues and Managers of Abadis Medical in  |
| 148 | `/en/photo-story-from-the-22nd-iran-health-international-exhibition-first-day/` | `/en/latest-news/photo-story-from-the-22nd-iran-health-international-exhibition-first-day/` | پست انگلیسی (EN Post) | Photo Report from the 22nd Iran Health International Exhibit |
| 149 | `/en/evolvement-of-abadis-ideas-investment-fund-project-at-iran-health-international-exhibition/` | `/en/latest-news/evolvement-of-abadis-ideas-investment-fund-project-at-iran-health-international-exhibition/` | پست انگلیسی (EN Post) | Evolvement of Abadis Ideas Investment Fund Project at Iran H |
| 150 | `/en/unveiling-of-abadis-fixture-product/` | `/en/latest-news/unveiling-of-abadis-fixture-product/` | پست انگلیسی (EN Post) | Unveiling of Abadis Endotracheal Tube Holder |
| 151 | `/en/disposable-suction-bags/` | `/en/latest-news/disposable-suction-bags/` | پست انگلیسی (EN Post) | Strategy and Necessity of Using Disposable Suction Bags – Pa |
| 152 | `/en/fixture/` | `/en/latest-news/fixture/` | پست انگلیسی (EN Post) | فیکسر &#8211; نگهدارنده لوله تراشه |
| 153 | `/en/disposable-suction-cups/` | `/en/latest-news/disposable-suction-cups/` | پست انگلیسی (EN Post) | Strategy and Necessity of Using Disposable Suction Liner Bag |
| 154 | `/en/introduction-of-single-dose-suction-bag/` | `/en/latest-news/introduction-of-single-dose-suction-bag/` | پست انگلیسی (EN Post) | Introduction of Disposable Suction Liner Bag |
| 155 | `/en/definition-of-hospital-infections/` | `/en/latest-news/definition-of-hospital-infections/` | پست انگلیسی (EN Post) | Definition of Nosocomial Infections and Their Types |
| 156 | `/en/the-most-common-pathogens/` | `/en/latest-news/the-most-common-pathogens/` | پست انگلیسی (EN Post) | Introducing The Most Common Pathogens |
| 157 | `/en/types-of-hospital-infections/` | `/en/latest-news/types-of-hospital-infections/` | پست انگلیسی (EN Post) | Types of Nosocomial Infections |
| 158 | `/en/hospital-equipment/` | `/en/latest-news/hospital-equipment/` | پست انگلیسی (EN Post) | High Quality Hospital Equipment and Products |
| 159 | `/en/report-on-the-2018-infection-control-congress/` | `/en/latest-news/report-on-the-2018-infection-control-congress/` | پست انگلیسی (EN Post) | Report on the 2018 Infection Control Congress |
| 160 | `/en/photo-story-of-abadis-participation-in-iran-health-international-exhibition-part-3/` | `/en/latest-news/photo-story-of-abadis-participation-in-iran-health-international-exhibition-part-3/` | پست انگلیسی (EN Post) | Photo  Story of Abadis Participation in Iran Health Internat |
| 161 | `/en/گیره-t-شکل/` | `/en/latest-news/گیره-t-شکل/` | پست انگلیسی (EN Post) | گیره T شکل |
| 162 | `/en/incidence-of-nosocomial-infections/` | `/en/latest-news/incidence-of-nosocomial-infections/` | پست انگلیسی (EN Post) | Nosocomial Infections |
| 163 | `/en/prevention-and-control-of-hospital-infections/` | `/en/latest-news/prevention-and-control-of-hospital-infections/` | پست انگلیسی (EN Post) | Prevention and Control of Nosocomial Infections |
| 164 | `/arabic/تقرير-مصور-عن-حضور-آباديس-في-معرض-إيران/` | `/arabic/الاخبار/تقرير-مصور-عن-حضور-آباديس-في-معرض-إيران/` | پست عربی (AR Post) | تقرير مصور عن حضور آباديس في معرض إيران هلث الدولي عام 2018 |
| 165 | `/arabic/الكشف-عن-منتج-حامل-أداة-تثبيت-آباديس/` | `/arabic/الاخبار/الكشف-عن-منتج-حامل-أداة-تثبيت-آباديس/` | پست عربی (AR Post) | الكشف عن منتج حامل (أداة تثبيت) آباديس |
| 166 | `/arabic/افتتاح-صندوق-استثمار-مشاريع-آباديس-ال/` | `/arabic/الاخبار/افتتاح-صندوق-استثمار-مشاريع-آباديس-ال/` | پست عربی (AR Post) | افتتاح صندوق استثمار مشاريع آباديس الإبداعية في معرض إيران ه |
| 167 | `/arabic/تقرير-مصور-لمعرض-إيران-هلث-الدولي-الثا/` | `/arabic/الاخبار/تقرير-مصور-لمعرض-إيران-هلث-الدولي-الثا/` | پست عربی (AR Post) | تقرير مصور لمعرض إيران هلث الدولي الثاني والعشرين 2019 |
| 168 | `/arabic/مقابلة-مع-زملاء-ورؤساء-آباديس-للخزانا/` | `/arabic/الاخبار/مقابلة-مع-زملاء-ورؤساء-آباديس-للخزانا/` | پست عربی (AR Post) | مقابلة مع زملاء ورؤساء آباديس للخزانات الطبية في معرض إيران  |
| 169 | `/arabic/مقابلة-إذاعة-إيران-مع-آباديس-في-معرض-إي/` | `/arabic/الاخبار/مقابلة-إذاعة-إيران-مع-آباديس-في-معرض-إي/` | پست عربی (AR Post) | مقابلة إذاعة إيران مع آباديس في معرض إيران هلث 2019 |
| 170 | `/arabic/التغطية-الإخبارية-لحضور-آباديس-في-معر/` | `/arabic/الاخبار/التغطية-الإخبارية-لحضور-آباديس-في-معر/` | پست عربی (AR Post) | التغطية الإخبارية لحضور آباديس في معرض إيران هلث على موقع Me |
| 171 | `/arabic/مقابلة-مجلة-الهندسة-الطبية-مع-المستش/` | `/arabic/الاخبار/مقابلة-مجلة-الهندسة-الطبية-مع-المستش/` | پست عربی (AR Post) | مقابلة مجلة &#8220;الهندسة الطبية&#8221; مع المستشار الاسترا |
| 172 | `/arabic/جريدة-غذا-ودارو-العدد-40/` | `/arabic/الاخبار/جريدة-غذا-ودارو-العدد-40/` | پست عربی (AR Post) | جريدة &#8220;غذا ودارو&#8221; العدد 40 |
| 173 | `/arabic/اليانصيب-الكبير-لشركة-آباديس/` | `/arabic/الاخبار/اليانصيب-الكبير-لشركة-آباديس/` | پست عربی (AR Post) | اليانصيب الكبير لشركة آباديس |
| 174 | `/arabic/حضور-آباديس-في-معرض-شيراز-الرابع-للأجه/` | `/arabic/الاخبار/حضور-آباديس-في-معرض-شيراز-الرابع-للأجه/` | پست عربی (AR Post) | حضور آباديس في معرض شيراز الرابع للأجهزة الطبية |
| 175 | `/arabic/أخبار-أكثر-عن-مسابقة-آباديس-الكبيرة/` | `/arabic/الاخبار/أخبار-أكثر-عن-مسابقة-آباديس-الكبيرة/` | پست عربی (AR Post) | أخبار أكثر عن مسابقة آباديس الكبيرة |
| 176 | `/arabic/الخبر-العاجل-لآباديس/` | `/arabic/الاخبار/الخبر-العاجل-لآباديس/` | پست عربی (AR Post) | الخبر العاجل لآباديس |
| 177 | `/arabic/يانصيب-آباديس-الكبير-2020-بمناسبة-عيد-الت/` | `/arabic/الاخبار/يانصيب-آباديس-الكبير-2020-بمناسبة-عيد-الت/` | پست عربی (AR Post) | يانصيب آباديس الكبير 2020 بمناسبة عيد التمريض |
| 178 | `/arabic/حضور-شركة-آباديس-في-معرض-المعدات-الطبي/` | `/arabic/الاخبار/حضور-شركة-آباديس-في-معرض-المعدات-الطبي/` | پست عربی (AR Post) | حضور شركة آباديس في معرض المعدات الطبية الرابع عشر في أصفهان |
| 179 | `/arabic/أنشطة-آباديس-خلال-أزمة-كورونا/` | `/arabic/الاخبار/أنشطة-آباديس-خلال-أزمة-كورونا/` | پست عربی (AR Post) | أنشطة آباديس خلال أزمة كورونا |
| 180 | `/arabic/الحصول-على-شهادة-ce-من-الاتحاد-الأوروبي/` | `/arabic/الاخبار/الحصول-على-شهادة-ce-من-الاتحاد-الأوروبي/` | پست عربی (AR Post) | الحصول على شهادة CE من الاتحاد الأوروبي |
| 181 | `/arabic/الكشف-عن-المنتجات-الجديدة-لشركة-آبادي/` | `/arabic/الاخبار/الكشف-عن-المنتجات-الجديدة-لشركة-آبادي/` | پست عربی (AR Post) | الكشف عن المنتجات الجديدة لشركة آباديس |
| 182 | `/arabic/عرض-منتجات-آباديس-الجديدة-في-مجال-التر/` | `/arabic/الاخبار/عرض-منتجات-آباديس-الجديدة-في-مجال-التر/` | پست عربی (AR Post) | عرض منتجات آباديس الجديدة في مجال الترشيح والتصفية |
| 183 | `/arabic/أسماء-الفائزين-في-مسابقة-يوم-التمريض-ع/` | `/arabic/الاخبار/أسماء-الفائزين-في-مسابقة-يوم-التمريض-ع/` | پست عربی (AR Post) | أسماء الفائزين في مسابقة يوم التمريض عام 2022 |
| 184 | `/arabic/مقابلة-مديرنس-مع-رؤساء-آباديس/` | `/arabic/الاخبار/مقابلة-مديرنس-مع-رؤساء-آباديس/` | پست عربی (AR Post) | مقابلة مديرنس مع رؤساء آباديس |
| 185 | `/arabic/صفحاتنا-الافتراضية/` | `/arabic/الاخبار/صفحاتنا-الافتراضية/` | پست عربی (AR Post) | صفحاتنا الافتراضية |
| 186 | `/arabic/مقابلة-وكالة-أنباء-فارس-مع-رؤساء-آبادي/` | `/arabic/الاخبار/مقابلة-وكالة-أنباء-فارس-مع-رؤساء-آبادي/` | پست عربی (AR Post) | مقابلة وكالة أنباء فارس مع رؤساء آباديس |
| 187 | `/arabic/صورة-تقديم-الدعوة-لمعرض-إيران-هلث-2022-من-ق/` | `/arabic/الاخبار/صورة-تقديم-الدعوة-لمعرض-إيران-هلث-2022-من-ق/` | پست عربی (AR Post) | صورة تقديم الدعوة لمعرض إيران هلث 2022 من قبل رؤساء آباديس |
| 188 | `/arabic/مقابلة-وكالة-أنباء-اخبار-رسمي-مع-مديري/` | `/arabic/الاخبار/مقابلة-وكالة-أنباء-اخبار-رسمي-مع-مديري/` | پست عربی (AR Post) | مقابلة وكالة أنباء اخبار رسمي مع مديري آباديس |
| 189 | `/arabic/تقرير-معرض-إيران-هلث-الدولي-الثالث-وال/` | `/arabic/الاخبار/تقرير-معرض-إيران-هلث-الدولي-الثالث-وال/` | پست عربی (AR Post) | تقرير معرض إيران هلث الدولي الثالث والعشرون |
| 190 | `/arabic/شركة-آباديس-أصبحت-شركة-قائمة-على-المعر/` | `/arabic/الاخبار/شركة-آباديس-أصبحت-شركة-قائمة-على-المعر/` | پست عربی (AR Post) | شركة آباديس أصبحت شركة قائمة على المعرفة |
| 191 | `/arabic/مشاركة-آباديس-الطبية-في-معرض-تبريز-للم/` | `/arabic/الاخبار/مشاركة-آباديس-الطبية-في-معرض-تبريز-للم/` | پست عربی (AR Post) | مشاركة آباديس الطبية في معرض تبريز للمعدات الطبية |
| 192 | `/category/news/` | `/news/` | دسته‌بندی وردپرس | آرشیو دسته‌بندی اخبار |
| 193 | `/category/blog/` | `/articles/` | دسته‌بندی وردپرس | آرشیو دسته‌بندی مقالات |
| 194 | `/category/articles/` | `/articles/` | دسته‌بندی وردپرس | آرشیو دسته‌بندی مقالات |
| 195 | `/category/exhibitions/` | `/events/` | دسته‌بندی وردپرس | آرشیو نمایشگاه‌ها |
| 196 | `/category/congress/` | `/events/` | دسته‌بندی وردپرس | آرشیو کنگره‌ها |
| 197 | `/category/workshops/` | `/events/` | دسته‌بندی وردپرس | آرشیو کارگاه‌ها |
| 198 | `/feed/` | `/news/` | فید RSS قدیمی | هدایت فید به اخبار |
