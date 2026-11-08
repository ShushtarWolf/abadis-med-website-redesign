# Core Abadis Knowledge Base

Version **2026-10-26**. Machine-readable twin: `site/assets/data/abadis-knowledge-base.json` (same file also at `docs/knowledge-base/abadis-knowledge-base.json`). The chatbot also keeps `site/assets/chatbot/kb-fallback.js`, the same JSON on `window.ABADIS_KB`, for `file://` and a cache that cannot fetch the JSON. Section 8 is the Iran intranet engine.

**Source of truth.** For pages that already exist — About, products, certificates, contact — [abadis-med.com](https://abadis-med.com) wins. New sections use the approved redesign (solutions philosophy, dial-practical calculator, Zagros CSR) and are labelled. Figures below are copied, not improved.

## 1. Company profile and About

- **Name:** شرکت دانش‌بنیان مخازن طبی آبادیس / Abadis Medical (knowledge-based company)
- **Established:** 2017 / 1396. Live About page (about_copy.json, modified 2026-10-20) and the homepage: the company was established in 2017. Factory lead: factory started in 1397.
- **Not used as a founding date:** 1387 / 2008 is not the founding year on the current abadis-med.com About page. This knowledge base does not treat it as a fact.
- **Earlier context on the same About page:** Disposable liners have been used in developed countries since the 1990s. In Iran, culture-building began in 2010 through Abzar Darman Persia.
- **Slogan (live About hero):** ما به اندازه یک سرانگشت اثر می‌گذاریم، به شما، به طبیعت، به جهان
- **EN gloss:** We make a difference as small as a fingertip — for you, for nature, for the world.
- **AR gloss:** نُحدِث أثرًا بقدر رأس إصبع — لك، وللطبيعة، وللعالم.

شرکت دانش‌بنیان مخازن طبی آبادیس با نگاهی علمی، نوآورانه و دغدغه‌مند در صنعت تجهیزات پزشکی فعالیت می‌کند و به‌عنوان مجموعه‌ای پیشگام و پیشرو در تولید محصولات تخصصی کنترل عفونت، گام‌های مؤثری در ارتقای بهداشت، ایمنی و بهره‌وری مراکز درمانی برداشته است.

Abadis Medical is an Iranian knowledge-based company driven by scientific thinking, innovation, and a strong sense of responsibility. As a pioneering and leading manufacturer of specialized infection control products, Abadis has made significant contributions to improving hygiene, safety, and operational efficiency in healthcare facilities.

### Mission, vision, history

The full FA / EN / AR About text approved on 2026-10-20 is embedded in the JSON under `company.about` (mission, vision, three strategic pillars, achievements, three history phases, commitment, goals). It is not shortened here.

### Stats (do not merge these rows)

| Figure | Value | Source |
| --- | --- | --- |
| Active centres on the redesign customers list | 1232 | zagros-names/names.json |
| Homepage impact counter (1405) | 1284 | Homepage impact counter is data-impact-stat="1284". 612 is not the current homepage figure. |
| Users | 11112 | homepage impact row |
| Satisfaction | 98.99% | homepage impact row |
| Product failure | 0.0018% | homepage impact row |
| Annual liner capacity | 5 million | homepage factory lead, factory year 1397 |
| Domestic liner share | about 90 percent | About page 2026-10-20 |
| Provinces | 28 | About page |
| Customers on the About page | more than 1000 | About page |

### Contact

- Phones: 02192001017, 02122671845, 02122205502, 02122215503, 02122218910
- Fax: 02141425555 | داخلی 28544
- Extensions: management 12, sales 11, finance 32
- Email: info@abadis-med.com
- WhatsApp: https://wa.me/989100145809
- Tehran office: ایران، تهران، قیطریه، خیابان اندرزگو، پلاک 104، واحد2 — postal 1935839683
- Neshan: https://neshan.org/maps/places/9399a4513b6974a287127c06bd9269b9
- Google Maps: https://www.google.com/maps/search/?api=1&query=35.79866,51.44826
- Factory: ایران،تهران،شهرک صنعتی شمس آباد، بلوار گلستان، کوچه گلشن ۱۹،پلاک۱۷ — postal 1834165776

## 2. Product categories and catalog

Eight headings for the meeting. A heading is a catalog line only when `status` says so. Urology, gynecology and gastroenterology are published **use sites** of the suction liner, not extra SKUs.

### Suction canisters and liners — مخازن و کیسه‌های ساکشن

- Status: `in_current_catalog`
- Volumes / sizes: 1 L, 2 L, 3 L
- FA: کیسه یکبارمصرف در ۱، ۲ و ۳ لیتر داخل مخزن پلی‌کربنات. ۲ لیتر تا ۸ لیتر تک‌ردیف و ۱۶ لیتر دو ردیف؛ ۳ لیتر تا ۱۲ لیتر سری. کارتن معمولاً ۴۵ عدد (فیلتر مکانیکی ۳۰). ابعاد کیسه از صفحه محصول: ۱ لیتر Ø۱۱×۱۵٫۵، ۲ لیتر Ø۱۱×۲۴٫۵، ۳ لیتر Ø۱۱×۳۹ سانتی‌متر.
- EN: Disposable liner in 1, 2 and 3 L inside a polycarbonate canister. 2 L up to 8 L single-row / 16 L double-row; 3 L up to 12 L in series. Carton usually 45 (mechanical filter 30). Bag size on the product page: 1 L Ø11×15.5, 2 L Ø11×24.5, 3 L Ø11×39 cm.
- AR: كيس استعمال واحد ١ و٢ و٣ لتر داخل خزان بولي كربونات. ٢ لتر حتى ٨ لتر صفًا واحدًا / ١٦ لتر صفين؛ ٣ لتر حتى ١٢ لترًا بالتسلسل. الكرتون عادة ٤٥ (الفلتر الميكانيكي ٣٠).
- Applications: 1 L: ambulance, infectious, dentistry, ophthalmology, paediatrics. 2 L: lung and endoscopy, gastroenterology, CCU/ICU, infectious, men’s and women’s wards, NICU/PICU, emergency, ECT. 3 L: infectious, operating room, cardiology, men’s and women’s wards, liposuction, surgery, gastroenterology, ICU.
- Links (FA): /products/suction-bag/, /products/canister/

### Suction instruments (tube and fingertip) — ابزار ساکشن (تیوب و فینگرتیپ)

- Status: `in_current_catalog`
- Volumes / sizes: CH25, CH30, CH35
- FA: ساکشن تیوب شفاف و شیاردار در CH25 و CH30 و CH35، با یا بدون فینگرتیپ. Yankauer به‌عنوان محصول آبادیس در کاتالوگ زنده نیست؛ در مقاله تاریخی ساکشن به مخترع آن اشاره شده است.
- EN: Clear and ribbed suction tube in CH25, CH30 and CH35, with or without a fingertip. Yankauer is not an Abadis SKU in the live catalog; an article only names Yankauer as the historical inventor of an early suction device.
- AR: أنبوب شفط شفاف ومضلّع بمقاسات CH25 وCH30 وCH35، مع طرف الإصبع أو من دونه. Yankauer ليس رمز منتج لآباديس في الكتالوج الحالي.
- Applications: Connects the patient circuit to the liner and canister in the operating room, intensive care and other departments that need suction.
- Links (FA): /products/suction-tube/

### Respiratory and airway care — مراقبت تنفسی و راه هوایی

- Status: `in_current_catalog`
- FA: مسواک ساکشن یکبارمصرف و نگهدارنده لوله تراشه روی صفحه سایر محصولات. سواب دهانی در متن راهکار آمده و صفحه محصول جدا ندارد.
- EN: Disposable suction toothbrush and endotracheal-tube holder are on the other-products page. An oral swab is named in the solution text and has no separate product page.
- AR: فرشاة الشفط ذات الاستعمال الواحد وحامل أنبوب القصبة في صفحة المنتجات الأخرى. المسحة الفموية مذكورة في نص الحل ومن دون صفحة منتج مستقلة.
- Applications: Oral care and patients with an endotracheal tube, following each product’s instructions.
- Links (FA): /products/other/

### Urology and drainage — اورولوژی و درناژ

- Status: `not_a_separate_catalog_line`
- FA: خط محصول جداگانه‌ای با این نام در abadis-med.com نیست. کیسه ساکشن در بخش مردان استفاده می‌شود و محفظه نمونه‌گیری برای جمع‌آوری ذرات از مایع ساکشن است.
- EN: abadis-med.com has no separate product line under this name. Suction liners are used on the men’s ward, and the collection cup gathers particles from suctioned fluid.
- AR: لا خط منتجات مستقل بهذا الاسم في abadis-med.com. تُستخدم أكياس الشفط في جناح الرجال، وكوب العينة يجمع الجسيمات من سائل الشفط.
- Applications: Men’s ward; sampling suctioned fluid.
- Links (FA): /products/suction-bag/, /products/canister/

### Gastroenterology — گوارش

- Status: `use_site_not_a_separate_catalog_line`
- Volumes / sizes: 2 L, 3 L
- FA: گوارش کاربرد منتشرشده کیسه ۲ و ۳ لیتری است، نه خانواده محصول جدا.
- EN: Gastroenterology is a published use of the 2 L and 3 L liners, not a separate product family.
- AR: الجهاز الهضمي استخدام منشور لكيسي ٢ و٣ لتر، وليس عائلة منتجات مستقلة.
- Applications: Lung, endoscopy and gastroenterology, as on the liner page.
- Links (FA): /products/suction-bag/

### Gynecology — زنان

- Status: `use_site_not_a_separate_catalog_line`
- Volumes / sizes: 2 L, 3 L
- FA: بخش زنان کاربرد منتشرشده کیسه ۲ و ۳ لیتری است. محصول زنان و زایمان جداگانه‌ای در کاتالوگ نیست.
- EN: The women’s ward is a published use of the 2 L and 3 L liners. The catalog has no separate obstetrics and gynecology range.
- AR: جناح النساء استخدام منشور لكيسي ٢ و٣ لتر. لا مجموعة مستقلة لطب النساء في الكتالوج.
- Applications: Women’s ward.
- Links (FA): /products/suction-bag/

### Anesthesia and ICU consumables — ملزومات بیهوشی و ICU

- Status: `in_current_catalog`
- Volumes / sizes: 2 L
- FA: کیسه ۲ لیتری برای CCU/ICU، رگولاتور بزرگسال VR-A1 و کودکان VR-B1، فیلتر آنتی‌باکتریال و قطع‌کننده جریان، نگهدارنده لوله تراشه.
- EN: 2 L liner for CCU/ICU, adult regulator VR-A1 and paediatric VR-B1, antibacterial and flow-stopper filters, endotracheal-tube holder.
- AR: كيس ٢ لتر لـ CCU/ICU، منظّم الكبار VR-A1 والأطفال VR-B1، الفلتر المضاد للبكتيريا وقاطع التدفق، وحامل أنبوب القصبة.
- Applications: CCU/ICU, operating room, vacuum circuit.
- Links (FA): /products/suction-bag/, /products/filters/, /products/other/

### General consumables — ملزومات عمومی

- Status: `in_current_catalog`
- Volumes / sizes: 600 ml
- FA: رسیور یکبارمصرف ۶۰۰ میلی‌لیتر (پلی‌پروپیلن)، اتصال T، کانکتور، شلنگ سیلیکونی، شیر ON/OFF، گیره مخزن. Splash-Vac روی سایر محصولات است.
- EN: 600 ml disposable kidney dish (polypropylene), T connector, connector, silicone hose, ON/OFF valve, canister clamp. Splash-Vac is on the other-products page.
- AR: وعاء كلوي ٦٠٠ مل (بولي بروبيلين)، وصلة T، وصلة، خرطوم سيليكون، صمام تشغيل/إيقاف، مشبك الخزان. Splash-Vac في صفحة المنتجات الأخرى.
- Applications: First collection, suction-circuit connectors, instrument counting.
- Links (FA): /products/connectors/, /products/other/, /products/stand/

Full Persian product-page text (headings, tables, uses) is in JSON `product_pages`, taken from the live page snapshots.

## 3. Clinical solutions

Dual path: **by product** (specs, real photos, enquiry) and **by solution** (problem, technology, advantage, result). Four pillars: Products, Solutions, Applications, Innovation.

- **Products / محصولات.** What do we manufacture and supply?
- **Solutions / راهکارها.** Which problem do these products solve together?
- **Applications / کاربردها.** Which hospital departments use these solutions?
- **Innovation / نوآوری.** Which technologies is Abadis working on to solve the problem of the future?

### 1. Hospital fluid and secretion management

From fluid collection to an integrated suction system

Managing hospital fluids and secretions is one of the sensitive processes in keeping a care centre hygienic, safe and efficient. Contact with contaminated fluids, washing reusable equipment, the use of resources and waste handling are among the challenges of this field.

Abadis, the first and largest manufacturer of disposable suction liner bags in Iran, took a pioneering approach to this product and began its path toward a complete solution for hospital fluid management.

The path continued by completing the suction system and developing filters, canisters, regulators, stands, trolleys and other related equipment, so that the parts of fluid collection are available to care centres as one coordinated system.

FA title: ۱. مدیریت مایعات و ترشحات بیمارستانی. AR title: ١. إدارة السوائل والإفرازات في المستشفى.

### 2. Airway safety and care

Developing specialist solutions for safer patient care

Airway care and secretion management are an important part of looking after patients in intensive units and other care settings. Oral hygiene, securing equipment and reducing the risks tied to care all need specialist products and standard methods.

Using its experience in secretion management and medical-device development, Abadis has opened a new stage of research and development in airway safety and care.

Developing products such as the suction toothbrush, the endotracheal-tube fixer and related equipment is part of this path.

FA title: ۲. ایمنی و مراقبت از راه هوایی. AR title: ٢. سلامة الطريق الهوائي والعناية به.

### 3. Contamination control and waste management

Materials technology; a new horizon for sustainable solutions

Contamination control and hospital-waste management are important challenges for the health system and for protecting the environment. Higher use of disposable equipment, and the need to handle waste safely, make the case for new technologies and solutions clearer than before.

Continuing its innovation path, Abadis has made research and development in materials technology, and in new contamination-control and waste-management solutions, part of its future work.

Studying and developing products based on polyvinyl alcohol (PVA), water-soluble films and related technologies is part of this forward-looking approach.

FA title: ۳. کنترل آلودگی و مدیریت پسماند. AR title: ٣. السيطرة على التلوث وإدارة النفايات.

OR efficiency and ICU care are application contexts of fluid management (see JSON `application_contexts_without_own_page`). They do not have their own solution URL.

## 4. Savings calculator and Save Zagros

The dial-practical calculator caps at 15,000 surgeries a year. Outputs: litres of water, toman of wash and disinfectant cost, staff hours. No CO₂ and no plastic kilograms.

- Surgery cap: **15000**.
- CO₂: **not included.** Alireza: the calculator does not report CO₂.
- Plastic mass and infectious-waste volume are **not** numeric outputs. The homepage teaser mentions infectious-waste savings; dial-practical does not compute them.
- Surgery water (litres): `n * 1.6 * 9.971`
- Surgery cost (toman): `n * 2.5 * usd_toman`
- Surgery staff hours: `n * 1.6 * 2.2 * 7.1 / 60`
- Beds water: `((a * 254) + (b * 67)) * 1.6 * 9.971`
- Beds cost: `((a * 254) + (b * 65)) * 2.5 * usd_toman`
- Beds hours: `((a * 254) + (b * 67)) * 1.7 * 2.2 * 7.1 / 60`
- USD fallback: 269500 toman, then TGJU.
- Page: /dial-practical/

### Save Zagros

In 1395 more than 75 fires destroyed about 950 hectares of Zagros forest. With Dpaper, Abadis planted one oak per member of its family of care centres (then 400+) and aimed at 1,000 saplings by Ordibehesht 1403. The 15 Esfand 1402 conference had about 800 participants. On 30 Tir 1403 Abadis signed the Save Zagros campaign. Hospital wall of honour: /zagros-names/4-mix/. The live page does not name Quercus brantii.

Wall of honour: `/zagros-names/4-mix/`

## 5. Certificates, licences and awards

Approved order:

1. IMED / IMED
2. ثبت اختراع / Patents
3. پروانه بهره‌برداری و ISO 13485 / GMP / Operating licences and ISO 13485 / GMP
4. جوایز و مقالات / Awards and publications

Footer strip only: CE · ISO 13485:2016 · IMED.

Display order on About is IMED, patents, operating licence, awards (pages_company.CERT_GROUPS). The filename router currently files ISO*, CE, export and IMED images into the IMED bucket and operating-licence filenames into operate. ISO 13485 is named on the footer strip. Do not invent certificate numbers.

## 6. Abadis Academy and news

The /academy/ shell is a mock interface and has no live course. Published education is the articles archive, the install guide and the FAQ.

Recent article titles (redesign archive, titles verbatim):

- [آبادیس پیشنهادهای جامع خود برای اصلاح اساسنامه انجمن تولید را ارائه کرد](https://abadis-med.com/آبادیس-پیشنهادهای-جامع-خود-برای-اصلاح)
- [دستگاه تزریق چربی چیست؟](/articles/18883/)
- [لوله هوا (ایروی) چیست؟](/articles/18824/)
- [۱۷ مرداد؛ روز خبرنگار گرامی باد](https://abadis-med.com/۱۷-مرداد؛-روز-خبرنگار-گرامی-باد)
- [آغاز فوری عملیات بازسازی کارخانه آبادیس پس از حادثه شهرک صنعتی شمس‌آباد](https://abadis-med.com/آغاز-فوری-عملیات-بازسازی-کارخانه-آباد)
- [راهنمای خرید کیسه ساکشن یکبار مصرف برای مراکز درمانی](/articles/18814/)
- [سوند نلاتون چیست؟](/articles/18793/)
- [قیمت کیسه ساکشن یکبار مصرف؛ هر آنچه مدیران خرید مراکز درمانی باید بدانند](/articles/18786/)
- [اعلام عدم تمدید عضویت و انتشار نامه سرگشاده مدیرعامل شرکت آبادیس خطاب به انجمن تولیدکنندگان تجهیزات پزشکی](https://abadis-med.com/اعلام-عدم-تمدید-عضویت-و-انتشار-نامه-سرگ)
- [اکستنشن تیوب چیست؟](/articles/18772/)
- [فیلتر آنتی‌باکتریال و فیلتر هیدروفوبیک چیست؟](/articles/18768/)
- [چست تیوب چیست؟](/articles/18761/)
- [نقش کیسه ساکشن یکبار مصرف در مدیریت پسماند عفونی بیمارستانی](/articles/18758/)
- [ساکشن دیواری چیست؟](/articles/18681/)
- [ساکشن مرکزی یا ساکشن پرتابل؟ راهنمای جامع انتخاب سیستم ساکشن برای مراکز درمانی](/articles/18736/)
- [نقش کیسه ساکشن یک‌بارمصرف در کاهش خطر انتقال هانتاویروس در مراکز درمانی](/articles/18609/)
- [ویروس هانتا چیست؟](/articles/18597/)
- [20 ژورنال معتبر تجهیزات پزشکی](/articles/18699/)
- [آبادیس در روزهای جنگ رمضان؛ تداوم خدمت‌رسانی بدون حتی یک روز توقف](https://abadis-med.com/آبادیس-در-روزهای-جنگ-رمضان؛-تداوم-خدمت)
- [انتشار مقاله مدیرعامل مخازن طبی آبادیس در کنفرانس بین‌المللی](https://abadis-med.com/%d8%a7%d9%86%d8%aa%d8%b4%d8%a7%d8%b1-%d9%85%d9%82%d8%a7%d9%84%d9%87-%d9%85%d8%af%db%8c%d8%b1%d8%b9%d8%a7%d9%85%d9%84-%d9%85%d8%ae%d8%a7%d8%b2%d9%86-%d8%b7%d8%a8%db%8c-%d8%a2%d8%a8%d8%a7%d8%af%db%8c/)
- [طراحی و پیاده‌سازی سیستم هوش تجاری برای مدیریت نقدینگی و تصمیم‌گیری تولید در شرکت‌های تجهیزات پزشکی: مطالعه موردی آبادیس](/articles/18578/)
- [نمایشگاه‌های تجهیزات پزشکی جهان](/articles/18568/)
- [آبادیس اجرای بازاریابی نسل چهارم و پنجم را تکمیل کرد](https://abadis-med.com/آبادیس-اجرای-بازاریابی-نسل-چهارم-و-پنج)
- [پروانه بهره برداری جدید آبادیس صادر گردید](https://abadis-med.com/%d9%be%d8%b1%d9%88%d8%a7%d9%86%d9%87-%d8%a8%d9%87%d8%b1%d9%87-%d8%a8%d8%b1%d8%af%d8%a7%d8%b1%db%8c-%d8%ac%d8%af%db%8c%d8%af-%d8%a2%d8%a8%d8%a7%d8%af%db%8c%d8%b3-%d8%b5%d8%a7%d8%af%d8%b1-%da%af%d8%b1/)

## 7. FAQ, sales configurator and support

Live FAQ: **29** pairs from the Persian FAQ page. EN/AR on the short answers are translations of that Persian text (`translation: translated-from-fa-faq`). The vehicle-load table and the product-code table stay verbatim in Persian.

### آیا باید بعد از هر بار مصرف مخازن ساکشن آبادیس را عوض کرد ؟

خیر، مخازن ثابت نیاز به تعویض بعد از هر بار مصرف را ندارند.

**EN.** Do Abadis suction canisters have to be replaced after every use? No. The rigid canisters do not need to be replaced after every use.

**AR.** هل يجب استبدال خزانات الشفط من آباديس بعد كل استخدام؟ لا. الخزانات الثابتة لا تحتاج إلى استبدال بعد كل استخدام.

### کیسه های ساکشن یکبار مصرف از چه موادی ساخته شده اند؟

کیسه ساکشن از مواد پلی اتیلن (PE) و مخازن ثابت از پلی کربنات ساخته شده است.

**EN.** What are the disposable suction liners made of? The liner is polyethylene (PE). The rigid canister is polycarbonate.

**AR.** ممّ تُصنع أكياس الشفط ذات الاستعمال الواحد؟ الكيس من البولي إيثيلين (PE) والخزان الثابت من البولي كربونات.

### فیلتر قطع کننده کیسه ساکشن آبادیس چه وظیفه ای دارد؟

این فیلتر ها سبب جلوگیری از سرریز شدن مایعات ساکشن شده به محیط اطراف می گردد.

**EN.** What does the shutoff filter on the Abadis suction liner do? It stops suctioned fluid from overflowing into the surroundings.

**AR.** ما وظيفة فلتر قطع التدفق في كيس الشفط؟ يمنع طفح السوائل المسحوبة إلى المحيط.

### آیا فیلترهای قطع کننده تولید داخل ایران می باشند؟

شرکت مخازن طبی آبادیس به عنوان اولین تولید کننده این فیلتر ها در ایران می باشد.

**EN.** Are the shutoff filters made in Iran? Abadis Medical is the first manufacturer of these filters in Iran.

**AR.** هل فلاتر قطع التدفق مصنّعة في إيران؟ شركة خزانات آباديس الطبية هي أول منتج لهذه الفلاتر في إيران.

### پودر جاذب (جامدکننده) در کیسه های ساکشن آبادیس چیست؟

پودر جاذب موجود درکیسه های ساکشن آبادیس سبب ژله ای شدن مواد مایع درون کیسه ها می شود که این امر موجب حمل آسان و همچنین در صورت سرریز شدن یا پاره شدن کیسه باعث جمع آوری بهتر مایعات درون کیسه می گردد.طبق گزارش منابع بین المللی استفاده از پودر جاذب تا ۳ برابر هزینه های امحا زباله های بیمارستانی را کاهش می دهد.

**EN.** What is the absorbent (solidifying) powder in Abadis liners? It gels the liquid inside the liner so the bag is easier to carry, and if the liner overflows or tears the fluid is contained better. International sources report that absorbent powder can cut hospital-waste disposal costs by up to three times.

**AR.** ما هو المسحوق الماص (المُصلِّب) في أكياس آباديس؟ يحوّل السائل داخل الكيس إلى هلام فيسهل الحمل، وإذا طفح الكيس أو تمزق يُجمع السائل بصورة أفضل. تفيد مصادر دولية أن المسحوق الماص يخفض كلفة التخلص من نفايات المستشفى حتى ثلاثة أضعاف.

### زمانی که کیسه های ساکشن شروع به استفاده می گردد، بعد از چه مدتی باید آن ها را تعویض کرد؟

کیسه های ساکشن را پس از پر شدن کامل می توان تعویض کرد و حتما برای کنترل عفونت بهتر کیسه های ساکشن بیماران مختلف با یکدیگر جا به جا نشوند.

**EN.** Once a liner is in use, when should it be changed? Change it when it is full. Do not move one patient’s liner to another patient.

**AR.** متى يُستبدل كيس الشفط بعد بدء الاستخدام؟ يمكن استبداله بعد امتلائه. لا يُنقل كيس مريض إلى مريض آخر.

### در چه صورتی کیسه ساکشن آبادیس از گارانتی خارج می گردد؟

۱) از کیسه متناسب با سایز مخزن استفاده نشود.
۲) حداقل هر ۲۴ ساعت یکبار کیسه ها در صورت استفاده تعویض نگردد.
۳) از کیسه ها بیش تر از یکبار استفاده شود.
در صورتی که از کیسه ساکشن های آبادیس به شیوه صحیح که در مواردبالا ذکر شده است استفاده نگردد این محصول از وارانتی خارج می شود.

**EN.** When does an Abadis suction liner leave warranty? 1) The liner does not match the canister size. 2) A liner in use is not changed at least every 24 hours. 3) A liner is used more than once. Use outside these rules voids the warranty.

**AR.** متى يخرج كيس الشفط من الضمان؟ ١) عدم استخدام كيس يناسب حجم الخزان. ٢) عدم استبدال الكيس المستخدم مرة كل ٢٤ ساعة على الأقل. ٣) استخدام الكيس أكثر من مرة. خلاف ذلك يُسقط الضمان.

### شیوه صحیح شست و شوی مخازن ساکشن آبادیس چگونه است ؟

۱) برای شست و شوی مخازن ساکشن به نسبت ۱ به ۱۰ از مواد ضدعفونی کننده و آب استفاده گردد.
۲) مخازن ساکشن را به مدت ۱۰ دقیقه در محلول ذکر شده در بالا بغلتانید؛ دقت شود بیش تر از زمان ذکر شده نباید مخزن ها را در محلول قرار داد زیرا سبب آسیب رسیدن به مخازن می گردد.
۳) سپس مخزن را روی یک حوله تمیز و خشک قرار دهید و اجازه دهید مخازن کاملا خشک شوند.
۴) مخازن ساکشن آبادیس تا دمای ۱۲۰ درجه قابلیت شست و شو در اتوکلاو را دارند.
۵) در صورت وجود هر گونه ترک یا شکستگی مخزن باید تعویض گردد.
نحوه شست و شوی مخازن تنها به صورت بالا مورد قبول می باشد و در صورتی که شست و شو بدین صورت انجام نگردد از وارانتی خارج می شود.
*این نکته را در نظر داشته باشید مخازن ساکشن آبادیس تنها در صورت وجود آلودگی نیاز به شست و شو دارند.

**EN.** How should Abadis suction canisters be washed? 1) Disinfectant to water, 1:10. 2) Roll the canister in that solution for 10 minutes — not longer, or the canister can be damaged. 3) Dry it on a clean towel. 4) Autoclave washing is possible up to 120°C. 5) Replace a cracked or broken canister. Any other wash voids the warranty. Wash only when the canister is contaminated.

**AR.** ما الطريقة الصحيحة لغسل خزانات الشفط؟ ١) مطهّر إلى ماء بنسبة ١ إلى ١٠. ٢) دحرجة الخزان في المحلول ١٠ دقائق لا أكثر. ٣) التجفيف على منشفة نظيفة. ٤) يمكن الغسل في الأوتوكلاف حتى ١٢٠ درجة. ٥) يُستبدل الخزان إذا تشقق أو انكسر. أي غسل آخر يُسقط الضمان. الغسل فقط عند وجود تلوث.

### طول عمر فیلتر آنتی باکتریال چقدر است؟

زمانی که کاغذ درون فیلتر آنتی باکتریال تغییر رنگ دهد باید فیلتر تعویض گردد و در صورتی که هر ۶ ماه فیلتر تعویض شود مطلوب ترین عملکرد را خواهیم داشت.

**EN.** How long does the antibacterial filter last? Replace it when the paper inside changes colour. Replacing it every 6 months gives the best performance.

**AR.** ما عمر الفلتر المضاد للبكتيريا؟ يُستبدل عندما يتغير لون الورق داخله. الاستبدال كل ٦ أشهر يعطي أفضل أداء.

### طول عمر فیلتر قطع کننده جریان چقدر است ؟

زمانی که مایعات به سطح فیلتر نفوذ کنند یا افت فشار ساکشن رخ دهد باید فیلتر تعویض گردد و بهتر است برای عملکرد صحیح هر ماه فیلتر قطع کننده جریان تعویض شود

**EN.** How long does the flow-stopper filter last? Replace it when liquid reaches its surface or suction pressure drops. For correct operation, replace it every month.

**AR.** ما عمر فلتر قطع التدفق؟ يُستبدل عندما يصل السائل إلى سطحه أو ينخفض ضغط الشفط. والأفضل استبداله كل شهر.

### آیا گیره مخزن دیواری و پرتابل قابل شست و شو است؟

بله،گیره مخزن دیواری و پرتابل در هر دو نوع فلزی و پلاستیکی قابل شست و شو تا حداکثر دمای ۹۵ درجه می باشند.

**EN.** Can the wall and portable canister clamps be washed? Yes. Both the metal and plastic versions can be washed up to 95°C.

**AR.** هل يمكن غسل مشبك الخزان الجداري والمحمول؟ نعم. النوعان المعدني والبلاستيكي يُغسلان حتى ٩٥ درجة كحد أقصى.

### در چه صورتی پایه ساکشن پرتابل از گارانتی خارج می گردد؟

پایه ساکشن پرتابل آبادیس در صورتی که ضربه شدید به آن وارد شود از گارانتی خارج می شود.

**EN.** When does the portable suction base leave warranty? A heavy impact voids the warranty.

**AR.** متى تخرج قاعدة الشفط المحمولة من الضمان؟ إذا تلقت ضربة شديدة.

### در چه صورتی مخازن ساکشن آبادیس از گارانتی خارج می گردد؟

مخزن ساکشن آبادیس در صورتی که آسیب ببیند و به آن ضربه وارد شود از گارانتی خارج می گردد.

**EN.** When does an Abadis canister leave warranty? If it is damaged or struck.

**AR.** متى يخرج خزان الشفط من الضمان؟ إذا تضرر أو تعرّض لضربة.

### در چه صورتی رگولاتور آبادیس از گارانتی خارج می گردد؟

رگولاتور آبادیس در صورتی که ضربه به آن وارد شود و دستگاه آسیب ببیند از گارانتی خارج می شود.

**EN.** When does an Abadis regulator leave warranty? If it is struck and the device is damaged.

**AR.** متى يخرج المنظّم من الضمان؟ إذا تعرّض لضربة وتضرر الجهاز.

### وارانتی محصولات شرکت مخازن طبی آبادیس به چه صورت می باشد؟

نام محصول
وضعیت وارانتی

کیسه ساکشن
کیسه های ساکشن یکبار مصرف آبادیس تا ۱ سال پس از تاریخ فروش در صورت بروز مشکل امکان تعویض رایگان دارند.

مخزن ساکشن
مخازن ساکشن آبادیس تا ۱ سال پس از تاریخ فروش در صورت بروز مشکل امکان تعویض رایگان  دارند.

پایه ساکشن پرتابل
پایه ساکشن پرتابل آبادیس در صورت بروز مشکل تا ۶ ماه پس از خرید امکان تعویض رایگان دارد و تا ۱ سال پس از آن تعمیرات به صورت رایگان صورت میگیرد و بعد از آن تاریخ تعمیر با هزینه امکان پذیر می باشد.

گیره مخزن دیواری
گیره مخزن دیواری آبادیس در صورت بروز مشکل تا ۳ سال امکان تعویض رایگان دارد.

گیره مخزن پرتابل
گیره مخزن پرتابل آبادیس در صورت بروز مشکل تا ۳ سال امکان تعویض رایگان دارد.

اتصال T شکل
اتصال Tشکل در صورت خرابی دارای وارانتی مادام العمر تعویض به صورت رایگان می باشد.

کانکتور
کانکتور آبادیس در صورت خرابی دارای وارانتی مادام العمر تعویض به صورت رایگان می باشد.

رگولاتور
رگولاتور آبادیس تا ۶ ماه در صورت بروز مشکل امکان تعویض دارد و تا ۱ سال پس از آن تعمیر به صورت رایگان صورت میگیرد؛ و بعد از آن مشمول هزینه می باشد.

ساکشن دیواری
ساکشن دیواری تا ۶ ماه در صورت بروز مشکل امکان تعویض دارد و تا ۱ سال پس از آن تعمیر به صورت رایگان صورت میگیرد؛ و بعد از آن مشمول هزینه می باشد.

**EN.** What is the Abadis product warranty? Suction liner: free replacement up to 1 year after the sale date if there is a fault. Suction canister: the same, 1 year. Portable base: free replacement for 6 months, then free repair up to 1 year, then paid repair. Wall clamp and portable clamp: free replacement for 3 years. T connector and connector: lifetime free replacement. Regulator and wall suction: free replacement for 6 months, free repair up to 1 year, then paid.

**AR.** كيف يكون ضمان منتجات آباديس؟ كيس الشفط والخزان: استبدال مجاني حتى سنة من تاريخ البيع عند وجود عيب. القاعدة المحمولة: استبدال مجاني ٦ أشهر ثم إصلاح مجاني حتى سنة ثم إصلاح مدفوع. مشبك الجدار والمشبك المحمول: استبدال مجاني ٣ سنوات. وصلة T والوصلة: استبدال مجاني مدى الحياة. المنظّم والشفط الجداري: استبدال ٦ أشهر ثم إصلاح مجاني حتى سنة ثم مدفوع.

### ساکشن تیوب آبادیس چند نوع است؟

3 نوع: CH25، CH30،  CH35

**EN.** How many Abadis suction-tube sizes are there? Three: CH25, CH30 and CH35.

**AR.** كم نوعًا لأنبوب الشفط؟ ثلاثة: CH25 وCH30 وCH35.

### تعداد کیسه ساکشن یکبار مصرف آبادیس در هر کارتن چند عدد است؟

در هر کارتن بسته بندی کیسه های ساکشن یکبار مصرف برای هر ۳ سایز 45 عدد می باشد.
کیسه ساکشن یکبار مصرف با فیلتر مکانیکی در هر کارتن 30 عدد قرار دارد.

**EN.** How many liners are in a carton? 45 liners per carton for each of the three sizes. A liner with a mechanical filter is packed 30 per carton.

**AR.** كم كيس شفط في الكرتون؟ ٤٥ كيسًا لكل سعة من السعات الثلاث. الكيس بفلتر ميكانيكي: ٣٠ في الكرتون.

### سایز کیسه ساکشن های یکبار مصرف آبادیس چند لیتر است؟

کیسه های ساکشن یکبار مصرف آبادیس در سه سایز یک، دو و سه لیتری تولید می شود.

**EN.** Which volumes do Abadis disposable liners come in? 1 litre, 2 litres and 3 litres.

**AR.** ما سعات أكياس الشفط؟ ١ لتر و٢ لتر و٣ لترات.

### ابعاد کارتن های محصولات آبادیس چقدر است؟

– ابعاد کارتن ۱ لیتری۵۷/۵*۴۲/۵*۴۴
– ابعاد کارتن ۲ لیتری ۵۷/۵*۴۲/۵*۴۴
– ابعاد کارتن ۳ لیتری ۴۹*۴۹*۴۹
_ ابعاد کارتن ساکشن تیوب 59*44.5*43.5

**EN.** What are the carton dimensions? 1 L and 2 L liners: 57.5 × 42.5 × 44 cm. 3 L: 49 × 49 × 49 cm. Suction tube: 59 × 44.5 × 43.5 cm.

**AR.** ما أبعاد الكراتين؟ ١ و٢ لتر: ٥٧٫٥ × ٤٢٫٥ × ٤٤ سم. ٣ لتر: ٤٩ × ٤٩ × ٤٩ سم. أنبوب الشفط: ٥٩ × ٤٤٫٥ × ٤٣٫٥ سم.

### در هریک از وسایل نقلیه چه تعداد کارتن کیسه ساکشن قرار می گیرد ؟

Long published table — see JSON `faq` and `/faq/`.

### تعداد ساکشن تیوب آبادیس در هر کارتن چند عدد است؟

تعداد 100 عدد ساکشن تیوب در هر کارتن موجود است.

**EN.** How many suction tubes are in a carton? 100 suction tubes per carton.

**AR.** كم أنبوب شفط في الكرتون؟ ١٠٠ أنبوب في الكرتون.

### برای درخواست نمونه از محصولات شرکت مخازن طبی آبادیس چه مراحلی باید طی شود؟

شما می توانید با استفاده از تکمیل فرم ارتباط با ما درخواست خود را مطرح کنید یا با واحد نصب و راه اندازی شرکت مخازن طبی آبادیس تماس حاصل فرمایید.

**EN.** How do I request a product sample? Send the contact form, or call the installation and commissioning unit.

**AR.** كيف أطلب عيّنة من المنتجات؟ عبر نموذج اتصل بنا، أو بالاتصال بوحدة التركيب والتشغيل.

### مراحل خرید محصولات شرکت مخازن طبی آبادیس چگونه است؟

۱- تکمیل فرم ارتباط با ما یا تماس با کارشناسان فروش و ثبت درخواست
۲- تاییدیه پیش فاکتور توسط مشتری
۳- واریز وجه
۴- ارسال کالا

**EN.** What are the steps to buy Abadis products? 1) Contact form or a call to sales, and the request is registered. 2) The customer confirms the proforma. 3) Payment. 4) Dispatch.

**AR.** ما خطوات شراء منتجات آباديس؟ ١) نموذج الاتصال أو الاتصال بمندوبي المبيعات وتسجيل الطلب. ٢) اعتماد الفاتورة الأولية. ٣) الدفع. ٤) الشحن.

### آیا شرکت مخازن طبی آبادیس در دیگر استان های کشور دارای نمایندگی است؟

بله، برای دیدن لیست نمایندگان به صفحه نمایندگان مراجعه شود

**EN.** Does Abadis have distributors in other provinces? Yes. The distributor list is on the representatives page.

**AR.** هل لآباديس ممثلون في المحافظات؟ نعم. قائمة الممثلين في صفحة الممثلين.

### کد محصولات شرکت مخازن طبی آبادیس

Long published table — see JSON `faq` and `/faq/`.

### نحوه نصب کیسه های ساکشن یکبار مصرف آبادیس چگونه است؟

1- مطابق شکل لوله سیلیکونی را از رگولاتور یا دستگاه ساکشن به اتصال T شکل روی مخزن متصل می نماییم .
2- از طرف دیگر اتصال T شکل لوله سیلیکونی را به اتصال کانکشن متصل کرده و کانکشن را روی قسمت وکیوم روی درب متصل می نماییم.
3- ساکشن تیوب ( لوله ساکشن) به قسمت patient ( بیمار) متصل کرده و از ساکشن تیوب ( لوله ساکشن) عملیات ساکشن را انجام می دهد.

**EN.** How is a disposable liner installed? 1) Connect the silicone tube from the regulator or suction unit to the T connector on the canister. 2) From the other side of the T, connect silicone tube to the connector and seat that connector on the vacuum port of the lid. 3) Connect the suction tube to the patient port and suction through that tube.

**AR.** كيف يُركَّب كيس الشفط؟ ١) وصل الخرطوم السيليكوني من المنظّم أو جهاز الشفط إلى وصلة T على الخزان. ٢) من الجهة الأخرى لوصلة T إلى الوصلة ثم إلى منفذ الفراغ على الغطاء. ٣) وصل أنبوب الشفط بمنفذ المريض والشفط عبره.

### در حین نصب کیسه های ساکشن آبادیس به چه نکاتی برای جلوگیری از افت فشار و نشتی باید توجه کرد ؟

از اتصالات زیر اطمینان حاصل فرمایید :
1- از اتصال گیره T شکل روی مخزن
2-اتصال و عدم نشتی در شلنگ های سیلیکونی مربوط به دستگاه ساکشن و گیره T شکل
۳-اتصال لوله ساکشن به بیمار

**EN.** What should be checked during installation to avoid pressure loss and leaks? Check: 1) the T clamp on the canister, 2) the silicone hoses between the suction unit and the T clamp, with no leak, 3) the suction tube connection to the patient.

**AR.** ما الذي يُفحص عند التركيب لتفادي هبوط الضغط والتسرب؟ ١) مشبك T على الخزان. ٢) خراطيم السيليكون بين الجهاز ومشبك T من دون تسرب. ٣) وصل أنبوب الشفط بالمريض.

### آیا کیسه های ساکشن یکبار مصرف آبادیس با یکدیگر سری می شوند؟

بله، باتوجه به تصویر زیر می توان سری کرد:
1- مطابق شکل لوله سیلیکونی را از رگولاتور یا دستگاه ساکشن به اتصال T شکل روی مخزن دارای کیسه ساکشن اولیه (pre) متصل می نماییم .
2- از طرف دیگر اتصال T شکل لوله سیلیکونی را به مخزن بعدی که حاوی کیسه ی Final ( یا نهایی) و دارای فیلتر قطع کننده می باشد متصل می کنیم
3- از طرف دیگر گیره T شکل همین مخزن با لوله سیلیکونی به قسمت وکیوم روی درب متصل میکنیم .
۴- از اتصال بیمار روی درب همین مخزن به قسمت وکیوم مخزن قبلی متصل می نماییم.
5- ساکشن تیوب ( لوله ساکشن) به قسمت patient ( بیمار) متصل کرده و از ساکشن تیوب ( لوله ساکشن) عملیات ساکشن را انجام می دهیم

**EN.** Can Abadis liners be connected in series? Yes. Connect the regulator to the T on the first (pre) canister, then from that T to the next canister which holds the final liner and the shutoff filter, then from that T to the vacuum port on the lid, then from the patient port of that canister back to the vacuum of the previous one, and the suction tube to the patient port.

**AR.** هل يمكن وصل أكياس الشفط على التسلسل؟ نعم. المنظّم إلى وصلة T للخزان الأول (pre)، ثم إلى الخزان التالي الذي فيه الكيس النهائي وفلتر القطع، ثم إلى منفذ الفراغ على الغطاء، ثم من منفذ المريض في هذا الخزان إلى فراغ الخزان السابق، وأنبوب الشفط إلى منفذ المريض.

### چند عدد کیسه ساکشن را با هم می توان سری کرد؟

حداکثر چهار کیسه ساکشن یکبار مصرف را روی پایه ترولی می توان با همدیگر سری کرد.

**EN.** How many liners can be connected in series? Up to four disposable liners can be connected together on the trolley base.

**AR.** كم كيسًا يمكن وصلها معًا؟ أربعة أكياس كحد أقصى على قاعدة الترولي.

### Support flows

- **Where does a hospital tender or purchase start?** 1) Contact form or sales, extension 11, 02192001017. 2) Confirm the proforma. 3) Pay. 4) Dispatch. Catalogues are in Downloads. Product codes are tabulated on the FAQ.
- **How do I find a distributor?** The distributor list is at /en/representatives/. For a province without a distributor, call the company.
- **How do I request a sample?** Use the contact form, or call the installation and commissioning unit. That is the live FAQ wording.
- **Which liner volume should we choose?** 1 L for ambulance, dentistry, eyes and children. 2 L for endoscopy, gastroenterology, ICU and emergency. 3 L for the operating room and higher fluid volumes. The liner must match the canister size or the warranty is void.

CTAs: contact form, downloads (catalogue), `tel:+982192001017`, WhatsApp `https://wa.me/989100145809`.

## 8. Iran intranet engine (شبکه ملی اطلاعات)

Hamid’s requirement: if filtering leaves only Iran’s National Information Network, the sales and academy chatbot must still answer. The engine is part of the site core. It does not load Google Fonts, jsDelivr, unpkg, Cloudflare, or any other foreign script or stylesheet. Kalameh is the set already in `site/assets/fonts/`. Icons in the widget are inline SVG.

Files:

- `site/assets/chatbot/chatbot.js` — widget, BM25 retrieval, synonym expansion, sales intent, and answer synthesis.
- `site/assets/data/abadis-knowledge-base.json` — same-origin knowledge base. This is the copy the widget fetches first.
- `site/assets/chatbot/kb-fallback.js` — that same JSON assigned to `window.ABADIS_KB`. The widget loads this sibling file only when the JSON fetch fails.
- `site/chatbot-demo/index.html` — meeting page, with the badge, the tier switch, and the international-cut-off toggle.

Three tiers. Tier 1 is the default and does not leave the site.

1. **Tier 1 — موتور بومی داخل هسته سایت.** BM25 over the chunks, plus synonym groups (Persian, English, Arabic) and the sales intent rules (solution, product, volume, savings). The answer is synthesized from the winning chunk and cites the on-site page. No API key and no foreign host.
2. **Tier 2 — optional domestic model.** A URL the hospital or Abadis hosts inside Iran, for example `/api/chat` on Liara, on abadis-med.com, or an on-prem Ollama or vLLM. The call uses a 2.5 second timeout. If it fails, the Tier 1 answer stays on screen.
3. **Tier 3 — optional international model.** An OpenAI-style chat-completions URL and a session key. Same 2.5 second timeout. If the request is blocked, times out, or the demo toggle «شبیه‌سازی قطع اینترنت بین‌الملل» is on, the widget does not wait on that host: the Tier 1 answer is already shown, and the foreign request is skipped while the toggle is on.

The widget header and `/chatbot-demo/` show this badge: **موتور داخلی هسته سایت (فعال در شبکه ملی اطلاعات / بدون نیاز به اینترنت بین‌الملل)** — Core On-Site Engine, 100% Iran intranet resilient.

