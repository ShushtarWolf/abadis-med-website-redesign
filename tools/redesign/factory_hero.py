"""Interactive 3D factory scrollytelling hero (Abadis Shams-Abad plant, 1 unit = 1 m).

Shared by the live FA/EN/AR home #intro and the standalone option page.
Implements the Option 2 + Option 3 Hybrid:
- Option 2: Unified Top Interactive Station Dock under the 1-5 stepper bar (no bottom-right corner box!)
- Option 3: Clickable 3D Machine Sub-Nodes on the wireframe equipment with coral (#ff7a59) highlighting & two-way sync.
three.js r170 + OrbitControls are self-hosted in assets/js/ (no CDN).
"""
import json
from html import escape as esc

V = '20261101a'

T = {
  'fa': dict(
    root='', quote_href='export/#quote',
    kicker='شرکت دانش‌بنیان مخازن طبی آبادیس',
    h1a='آبادیس؛ ', h1b='مهندسی دقیق', h1c='، برای مراقبتی ایمن‌تر',
    sub='پیشرو در کنترل عفونت و مدیریت مایعات بیمارستانی — اسکرول کنید یا روی ایستگاه‌ها بزنید تا وارد خط تولید شوید.',
    skip='رد کردن و ادامه صفحه', explore='حالت کاوش آزاد', back='بازگشت به مسیر اسکرول',
    collapse='بستن جزئیات', expand='نمایش جزئیات',
    hint='بکشید تا بچرخد • دو انگشت یا چرخ موس برای زوم • روی دستگاه‌ها یا دکمه‌های بالا بزنید',
    step='ایستگاه {n} از {t}', aerial='نمای هوایی کارخانه',
    stations=[
      dict(
        n='سوله ۱ (همکف) — سالن تزریق پلاستیک و قالب‌گیری',
        t='ورود از دهانه ۱۴ متری و رختکن‌ها به سالن تزریق با سقف ۵ متر؛ تولید بدنه، درب و قطعات کیسه ساکشن.',
        subs=[
          dict(id=11, code='۱.۱', pin='۱.۱ ردیف شمالی تزریق', chip='۱.۱ سالن تزریق — ردیف شمالی',
               spec='قالب‌گیری دقیق بدنه کیسه‌های ساکشن یک‌بارمصرف با ۴ دستگاه تزریق ۲۲۰ تن در ردیف شمالی سالن همکف (سقف ۵ متر).',
               pos=[-9.65, 2.8, -16.8]),
          dict(id=12, code='۱.۲', pin='۱.۲ ردیف میانی تزریق', chip='۱.۲ سالن تزریق — ردیف میانی',
               spec='تزریق درب، اتصالات و قطعات ظریف کیسه ساکشن با ۶ دستگاه تزریق ۱۲۰ تن در میانه سالن همکف.',
               pos=[-9.25, 2.2, -6.95]),
        ]
      ),
      dict(
        n='سوله ۱ (طبقه دوم) — مونتاژ کیسه ساکشن و کارتنینگ',
        t='سالن ایزوله ساندویچ‌پنل پلی‌اورتان ۱۰×۱۰ متر با ۳ خط مونتاژ و راهروی کارتنینگ ۱۰×۳ متر متصل به بالابر.',
        subs=[
          dict(id=21, code='۲.۱', pin='۲.۱ سالن مونتاژ', chip='۲.۱ سالن مونتاژ پلی‌اورتان',
               spec='۳ خط موازی مونتاژ و تست نشتی کیسه ساکشن در اتاق ایزوله با دیوار و سقف پلی‌اورتان.',
               pos=[-9.25, 7.2, 3.0]),
          dict(id=22, code='۲.۲', pin='۲.۲ کارتنینگ و بالابر', chip='۲.۲ راهروی کارتنینگ و بالابر',
               spec='بسته‌بندی در راهروی ۱۰×۳ متری و انتقال مستقیم به همکف با بالابر اختصاصی (انبار میانی بسته).',
               pos=[-8.5, 7.2, 9.5]),
          dict(id=23, code='۲.۳', pin='۲.۳ بالابر انبار در جریان ساخت', chip='۲.۳ بالابر شمال‌غربی و انبار در جریان ساخت',
               spec='بالابر گوشه شمال‌غربی سوله، قطعات تزریقی را به انبار در جریان ساخت بالای سالن تزریق می‌برد (فضای داخلی محرمانه است).',
               pos=[-15.0, 9.0, -21.2]),
        ]
      ),
      dict(
        n='سوله ۲ — سالن تولید فیلتر متخلخل (خروج از قالب)',
        t='نمایش صرفاً مرحله خروج فیلتر متخلخل نهایی از قالب در بخش جنوبی سوله ۲، بعد از دیوار ۱۸ متری، با حفظ کامل محرمانگی دانش فنی.',
        subs=[
          dict(id=31, code='۳.۱', pin='۳.۱ خروج فیلتر از قالب', chip='۳.۱ خروج فیلتر متخلخل از قالب',
               spec='جداسازی فیلتر متخلخل نهایی از قالب پرس؛ سایر مراحل تولید به دلیل محرمانگی دانش فنی نمایش داده نمی‌شود.',
               pos=[2.25, 3.2, 4.0]),
          dict(id=32, code='۳.۲', pin='۳.۲ سینی کنترل کیفیت فیلتر', chip='۳.۲ سینی کنترل کیفیت فیلتر قطع جریان',
               spec='آماده‌سازی فیلترهای هیدروفوبیک، دوئال و مکانیکی با راندمان ۹۹.۹۹۹٪ جهت نصب در درب کیسه.',
               pos=[5.4, 1.6, 8.7]),
        ]
      ),
      dict(
        n='سوله ۲ (همکف) — سالن اکسترودر تیوب',
        t='۴ دستگاه اکسترودر تیوب پزشکی در همکف؛ کلاف‌ها با باکس کلین‌رومی و بالابر مخصوص به طبقه بالا می‌روند.',
        subs=[
          dict(id=41, code='۴.۱', pin='۴.۱ ۴ دستگاه اکسترودر', chip='۴.۱ ۴ دستگاه اکسترودر',
               spec='تولید پیوسته تیوب‌های ساکشن پزشکی ضدپیچ‌خوردگی با ۴ دستگاه اکسترودر در سالن ۱۰×۱۸ متری طبقه همکف سوله ۲.',
               pos=[1.9, 2.2, -16.2]),
          dict(id=42, code='۴.۲', pin='۴.۲ باکس کلین‌رومی و بالابر', chip='۴.۲ باکس کلین‌رومی و بالابر مخصوص',
               spec='انتقال ایزوله کلاف‌های تیوب از سالن اکسترودر به طبقه بالا بدون تماس با هوای محیط.',
               pos=[2.2, 4.5, -5.8]),
        ]
      ),
      dict(
        n='سوله ۲ (طبقه دوم) — کلین‌روم کلاس ۱۰۰٬۰۰۰',
        t='اتاق تمیز مستقل بالای سالن اکسترودر با ۲ خط مونتاژ کانکتور و بسته‌بندی تیوب، فیلترهای HEPA سقفی و فشار مثبت.',
        subs=[
          dict(id=43, code='۵.۱', pin='۵.۱ کلین‌روم ۱۰۰٬۰۰۰ (طبقه دوم)', chip='۵.۱ کلین‌روم کلاس ۱۰۰٬۰۰۰ (طبقه دوم)',
               spec='مونتاژ کانکتور و بسته‌بندی ساکشن تیوب در ۲ خط مجزا تحت فشار مثبت اتاق تمیز کلاس ۱۰۰٬۰۰۰.',
               pos=[2.25, 7.4, -13.0]),
        ]
      ),
      dict(
        n='سوله ۳ — انبار محصول نهایی و ارسال سراسری',
        t='نگهداری پالت‌های کارتن ۴۵ عددی در سوله ۸٫۵×۳۶ متر و ارسال مستقیم به ۱٬۲۸۴ مرکز درمانی در ۳۱ استان.',
        subs=[
          dict(id=51, code='۶.۱', pin='۶.۱ پالت‌های کارتن ۴۵ عددی', chip='۶.۱ پالت‌های کارتن ۴۵ عددی (ظرفیت ۵ میلیون)',
               spec='چیدمان استاندارد کارتن‌های ۴۵ عددی در قفسه‌های سوله ۳ با ظرفیت تولید سالانه ۵ میلیون کیسه ساکشن.',
               pos=[11.5, 3.4, -6.0]),
          dict(id=52, code='۶.۲', pin='۶.۲ لیفتراک و درب ارسال', chip='۶.۲ راهروی لیفتراک و ارسال به ۱٬۲۸۴ مرکز',
               spec='بارگیری از درب پارکینگ راست و ارسال رایگان به ۱٬۲۸۴ بیمارستان و مرکز جراحی در سراسر کشور.',
               pos=[11.5, 2.2, 11.4]),
        ]
      ),
    ],
    labels=['تزریق','مونتاژ و کارتن','فیلتر','اکسترودر','کلین‌روم','انبار و ارسال','ساختمان اداری','کوچه گلشن ۱۹'],
    digits='fa'),
  'en': dict(
    root='en/', quote_href='export/#quote',
    kicker='Abadis Medical Canisters Knowledge-Based Co.',
    h1a='Abadis: ', h1b='Precision Engineering', h1c=' for Safer Care',
    sub='Pioneer in Hospital Infection Control & Fluid Management — Scroll or tap any station to inspect the plant.',
    skip='Skip & Continue', explore='Free Exploration Mode', back='Back to scroll tour',
    collapse='Hide details', expand='Show details',
    hint='Drag to rotate • Pinch or wheel to zoom • Tap 3D machine nodes or top chips to inspect',
    step='Station {n} of {t}', aerial='Aerial view of the plant',
    stations=[
      dict(
        n='Hall 1 (Ground) — Plastic Injection Molding',
        t='Entering past the 14m front bay and locker rooms into the 5m ground hall, filled with four 220-ton and six 120-ton injection presses.',
        subs=[
          dict(id=11, code='1.1', pin='1.1 North injection row', chip='1.1 Injection hall — north row',
               spec='Precision molding of disposable suction canister bodies on four 220-ton presses along the north row of the 5m ground hall.',
               pos=[-9.65, 2.8, -16.8]),
          dict(id=12, code='1.2', pin='1.2 Middle injection row', chip='1.2 Injection hall — middle row',
               spec='Injection of lids, ports, and fine canister fittings on six 120-ton presses filling the middle of the ground hall.',
               pos=[-9.25, 2.2, -6.95]),
        ]
      ),
      dict(
        n='Hall 1 (Upper Floor) — Canister Assembly & Cartoning',
        t='10×10m isolated polyurethane panel room with 3 assembly lines and a 10×3m cartoning corridor linked to the lift.',
        subs=[
          dict(id=21, code='2.1', pin='2.1 PU Assembly', chip='2.1 Polyurethane Assembly',
               spec='3 parallel suction canister assembly & leak-testing lines inside an isolated polyurethane panel room.',
               pos=[-9.25, 7.2, 3.0]),
          dict(id=22, code='2.2', pin='2.2 Cartoning & Lift', chip='2.2 Cartoning Corridor & Lift',
               spec='Cartoning in the 10×3m corridor with direct vertical lift transfer to the ground floor (WIP room closed).',
               pos=[-8.5, 7.2, 9.5]),
          dict(id=23, code='2.3', pin='2.3 WIP Storage Lift', chip='2.3 North-West Lift & WIP Storage',
               spec='The north-west corner lift carries molded parts up to the closed WIP storage above the injection hall (interior kept private).',
               pos=[-15.0, 9.0, -21.2]),
        ]
      ),
      dict(
        n='Hall 2 — Porous Filter Demolding (IP Protected)',
        t='Exclusively showing finished porous filter demolding in the south bay of hall 2, beyond the 18m partition, to protect proprietary manufacturing IP.',
        subs=[
          dict(id=31, code='3.1', pin='3.1 Filter Demolding', chip='3.1 Porous Filter Demolding',
               spec='Finished porous filter exiting the mold press; upstream process is hidden to protect trade secrets.',
               pos=[2.25, 3.2, 4.0]),
          dict(id=32, code='3.2', pin='3.2 Shut-Off Filter QC', chip='3.2 Shut-Off Filter QC Tray',
               spec='Inspection of 99.999% efficiency hydrophobic, dual, and mechanical shut-off filters for lid integration.',
               pos=[5.4, 1.6, 8.7]),
        ]
      ),
      dict(
        n='Hall 2 (Ground) — Medical Tube Extrusion',
        t='Four medical tube extruders on the ground floor; coils rise to the upper floor via a sealed pass-box and dedicated lift.',
        subs=[
          dict(id=41, code='4.1', pin='4.1 4× Tube Extruders', chip='4.1 4× Tube Extruders',
               spec='Continuous extrusion of kink-resistant medical suction tubing on four extruders in the 10×18m ground-floor hall.',
               pos=[1.9, 2.2, -16.2]),
          dict(id=42, code='4.2', pin='4.2 Pass-Box & Lift', chip='4.2 Cleanroom Pass-Box & Lift',
               spec='Sealed vertical transfer of extruded tubing coils from ground floor into the upstairs cleanroom.',
               pos=[2.2, 4.5, -5.8]),
        ]
      ),
      dict(
        n='Hall 2 (Upper Floor) — Class 100,000 Cleanroom',
        t='A dedicated cleanroom above the extrusion hall: 2 connector-assembly & tube-packing lines under ceiling HEPA and positive pressure.',
        subs=[
          dict(id=43, code='5.1', pin='5.1 Class 100k Cleanroom', chip='5.1 Class 100,000 Cleanroom (Upper)',
               spec='Suction tube connector assembly and sterile-grade packaging across 2 lines under positive pressure.',
               pos=[2.25, 7.4, -13.0]),
        ]
      ),
      dict(
        n='Hall 3 — Finished Goods Warehouse & Nationwide Dispatch',
        t='Organized 45-count carton pallet racks in the 8.5×36m hall dispatching to 1,284 medical centers across 31 provinces.',
        subs=[
          dict(id=51, code='6.1', pin='6.1 45-Count Pallets', chip='6.1 45-Count Carton Pallets (5M/yr)',
               spec='Standardized pallet racks of 45-unit cartons supporting a 5-million-unit annual production capacity.',
               pos=[11.5, 3.4, -6.0]),
          dict(id=52, code='6.2', pin='6.2 Forklift & Dispatch', chip='6.2 Forklift Aisle & Dispatch (1,284 Centers)',
               spec='Loading via the east dispatch gate for free delivery to 1,284 hospitals and surgical centers nationwide.',
               pos=[11.5, 2.2, 11.4]),
        ]
      ),
    ],
    labels=['Injection','Assembly & cartoning','Filter','Extrusion','Cleanroom','Warehouse & dispatch','Administrative Building','Golshan 19 Alley'],
    digits='en'),
  'ar': dict(
    root='arabic/', quote_href='export/#quote',
    kicker='شركة أباديس المعرفية للخزانات الطبية',
    h1a='أباديس؛ ', h1b='هندسة دقيقة', h1c=' لرعاية أكثر أماناً',
    sub='الرائدة في مكافحة العدوى وإدارة السوائل بالمستشفيات — مرّر أو اضغط على المحطات لاستكشاف خط الإنتاج.',
    skip='تخطي والمتابعة', explore='وضع الاستكشاف الحر', back='العودة إلى جولة التمرير',
    collapse='إخفاء التفاصيل', expand='عرض التفاصيل',
    hint='اسحب للتدوير • قرّب للتكبير • اضغط على نقاط الماكينات ثلاثية الأبعاد أو الأزرار العلوية',
    step='المحطة {n} من {t}', aerial='منظر جوي للمصنع',
    stations=[
      dict(
        n='القاعة ١ (الأرضي) — حقن البلاستيك وتشكيل القوالب',
        t='الدخول عبر البهو الأمامي بارتفاع ١٤ م وغرف تبديل الملابس إلى قاعة الحقن بارتفاع ٥ م لتشكيل أجسام وأغطية الأكياس.',
        subs=[
          dict(id=11, code='١.١', pin='١.١ صف الحقن الشمالي', chip='١.١ قاعة الحقن — الصف الشمالي',
               spec='قولبة دقيقة لأجسام عبوات الشفط أحادية الاستخدام على ٤ ماكينات حقن ٢٢٠ طن في الصف الشمالي من القاعة الأرضية (٥ م).',
               pos=[-9.65, 2.8, -16.8]),
          dict(id=12, code='١.٢', pin='١.٢ صف الحقن الأوسط', chip='١.٢ قاعة الحقن — الصف الأوسط',
               spec='حقن الأغطية والوصلات والأجزاء الدقيقة على ٦ ماكينات حقن ١٢٠ طن في وسط القاعة الأرضية.',
               pos=[-9.25, 2.2, -6.95]),
        ]
      ),
      dict(
        n='القاعة ١ (الطابق الثاني) — تجميع أكياس الشفط والكرتنة',
        t='قاعة معزولة بألواح البولي يوريثان ١٠×١٠ م بـ ٣ خطوط تجميع وممر كرتنة ١٠×٣ م متصل بالمصعد.',
        subs=[
          dict(id=21, code='٢.١', pin='٢.١ قاعة التجميع', chip='٢.١ قاعة التجميع المعزولة',
               spec='٣ خطوط متوازية لتجميع واختبار عدم التسرب داخل غرفة معزولة بألواح البولي يوريثان.',
               pos=[-9.25, 7.2, 3.0]),
          dict(id=22, code='٢.٢', pin='٢.٢ الكرتنة والمصعد', chip='٢.٢ ممر الكرتنة والمصعد',
               spec='التعبئة في ممر ١٠×٣ م والنقل المباشر إلى الطابق الأرضي عبر المصعد المخصص (المخزن الوسيط مغلق).',
               pos=[-8.5, 7.2, 9.5]),
          dict(id=23, code='٢.٣', pin='٢.٣ مصعد مخزن قيد التصنيع', chip='٢.٣ المصعد الشمالي الغربي ومخزن قيد التصنيع',
               spec='ينقل مصعد الزاوية الشمالية الغربية القطع المحقونة إلى مخزن قيد التصنيع المغلق فوق قاعة الحقن (الداخل سري).',
               pos=[-15.0, 9.0, -21.2]),
        ]
      ),
      dict(
        n='القاعة ٢ — فصل الفلتر المسامي من القالب',
        t='عرض مرحلة إخراج الفلتر المسامي النهائي من القالب فقط في الجناح الجنوبي للقاعة ٢ بعد الفاصل البالغ ١٨ م، حفاظاً على سرية تقنية التصنيع.',
        subs=[
          dict(id=31, code='٣.١', pin='٣.١ إخراج الفلتر من القالب', chip='٣.١ إخراج الفلتر المسامي من القالب',
               spec='فصل الفلتر المسامي النهائي عن القالب؛ لا تُعرض المراحل السابقة حفاظاً على الملكية الفكرية.',
               pos=[2.25, 3.2, 4.0]),
          dict(id=32, code='٣.٢', pin='٣.٢ فحص فلاتر الإيقاف', chip='٣.٢ صينية فحص فلاتر إيقاف التدفق',
               spec='تجهيز وفحص الفلاتر الهيدروفوبية والمزدوجة والميكانيكية بكفاءة ٩٩.٩۹٩٪ للتركيب في الأغطية.',
               pos=[5.4, 1.6, 8.7]),
        ]
      ),
      dict(
        n='القاعة ٢ (الأرضي) — بثق الأنابيب الطبية',
        t='أربع آلات بثق للأنابيب الطبية في الطابق الأرضي؛ ترتفع اللفائف إلى الطابق الثاني عبر صندوق تمرير محكم ومصعد مخصص.',
        subs=[
          dict(id=41, code='٤.١', pin='٤.١ ٤ ماكينات بثق', chip='٤.١ ٤ ماكينات بثق',
               spec='إنتاج مستمر لأنابيب الشفط الطبية المقاومة للالتواء على ٤ ماكينات بثق في قاعة ١٠×١٨ م بالطابق الأرضي.',
               pos=[1.9, 2.2, -16.2]),
          dict(id=42, code='٤.٢', pin='٤.٢ صندوق التمرير والمصعد', chip='٤.٢ صندوق التمرير والمصعد المعقم',
               spec='نقل معقم لملفات الأنابيب من قاعة البثق إلى الطابق الثاني دون تلامس مع الهواء الخارجي.',
               pos=[2.2, 4.5, -5.8]),
        ]
      ),
      dict(
        n='القاعة ٢ (الطابق الثاني) — غرفة نظيفة فئة ١٠٠٬٠٠٠',
        t='غرفة نظيفة مستقلة فوق قاعة البثق: خطّان لتجميع الموصلات وتعبئة الأنابيب تحت فلاتر HEPA سقفية وضغط إيجابي.',
        subs=[
          dict(id=43, code='٥.١', pin='٥.١ الغرفة النظيفة ١٠٠٬٠٠٠', chip='٥.١ الغرفة النظيفة فئة ١٠٠٬٠٠٠ (الطابق الثاني)',
               spec='تجميع وصلات أنابيب الشفط وتغليفها في خطين مستقلين تحت ضغط إيجابي داخل الغرفة النظيفة.',
               pos=[2.25, 7.4, -13.0]),
        ]
      ),
      dict(
        n='القاعة ٣ — مستودع المنتجات النهائية والشحن',
        t='تخزين منصات الكراتين (٤٥ عبوة) في القاعة ٣ والشحن المباشر إلى ١٬٢٨٤ مركزاً علاجياً.',
        subs=[
          dict(id=51, code='٦.١', pin='٦.١ منصات الكراتين (٤٥ عبوة)', chip='٦.١ منصات الكراتين (٥ ملايين سنوياً)',
               spec='تخزين منظم لكراتين سعة ٤٥ عبوة بطاقة إنتاجية سنوية تبلغ ٥ ملايين كيس شفط.',
               pos=[11.5, 3.4, -6.0]),
          dict(id=52, code='٦.٢', pin='٦.٢ الرافعة الشوكية والشحن', chip='٦.٢ ممر الرافعة الشوكية والشحن (١٬٢٨٤ مركزاً)',
               spec='التحميل عبر البوابة الشرقية للشحن المجاني إلى ١٬٢٨٤ مستشفى ومركزاً جراحياً في ٣١ محافظة.',
               pos=[11.5, 2.2, 11.4]),
        ]
      ),
    ],
    labels=['الحقن','التجميع والتعبئة','الفلتر','البثق','الغرفة النظيفة','المستودع والشحن','المبنى الإداري','زقاق گلشن ۱۹'],
    digits='ar'),
}

_SVG = 'viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"'
ICO_SKIP = f'<svg {_SVG}><path d="M12 5v14"/><path d="m6 13 6 6 6-6"/></svg>'
ICO_ORBIT = f'<svg {_SVG}><circle cx="12" cy="12" r="3"/><ellipse cx="12" cy="12" rx="10" ry="4.5"/></svg>'
ICO_CHEV = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m6 15 6-6 6 6"/></svg>'


def num(n, lang):
    s = str(n)
    if lang == 'fa':
        return s.translate(str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹'))
    if lang == 'ar':
        return s.translate(str.maketrans('0123456789', '٠١٢٣٤٥٦٧٨٩'))
    return s


def head(p):
    return f'<link rel="stylesheet" href="{p}assets/css/factory-3d.css?v={V}">'


def scripts(p):
    # No import map: factory-3d.js imports ./three.module.js and ./OrbitControls.js (self-hosted, no CDN).
    return f'<script type="module" src="{p}assets/js/factory-3d.js?v={V}"></script>\n'


def hero(p, lang='fa', quote_href=None, skip_to='#about'):
    t = T[lang]
    cfg = {
        'lang': lang,
        'step': t['step'], 'total': num(len(t['stations']), lang),
        'nums': [num(i, lang) for i in range(1, len(t['stations']) + 1)],
        'stations': t['stations'],
        'labels': t['labels'],
        'explore': t['explore'], 'back': t['back'],
        'collapse': t['collapse'], 'expand': t['expand'],
    }
    pills = ''.join(
        f'<button type="button" class="f3d-pill" data-i="{i}"><b>{num(i + 1, lang)}</b><span>{esc(lb)}</span></button>'
        for i, lb in enumerate(t['labels'][:len(t['stations'])]))
    return f'''  <section class="f3d" id="intro" aria-label="{esc(t['h1a'] + t['h1b'] + t['h1c'])}">
    <script type="application/json" class="f3d-cfg">{json.dumps(cfg, ensure_ascii=False)}</script>
    <div class="f3d-stage">
      <canvas class="f3d-gl" aria-hidden="true"></canvas>
      <div class="f3d-labels"></div>
      <div class="f3d-subpins"></div>
      <div class="f3d-intro">
        <p class="f3d-kicker">{esc(t['kicker'])}</p>
        <h1>{esc(t['h1a'])}<b>{esc(t['h1b'])}</b>{esc(t['h1c'])}</h1>
        <p class="f3d-sub">{esc(t['sub'])}</p>
      </div>
      <div class="f3d-dock f3d-glass" aria-live="polite">
        <div class="f3d-dock-top">
          <nav class="f3d-pills" aria-label="{esc(t['aerial'])}">{pills}</nav>
          <button type="button" class="f3d-dock-toggle" aria-expanded="true" title="{esc(t['collapse'])}">{ICO_CHEV}<span class="f3d-dock-toggle-lbl">{esc(t['collapse'])}</span></button>
        </div>
        <div class="f3d-dock-drawer">
          <div class="f3d-dock-head">
            <span class="f3d-step"></span>
            <h2 class="f3d-title"></h2>
          </div>
          <div class="f3d-subchips" role="tablist"></div>
          <p class="f3d-subspec"></p>
          <div class="f3d-dots">{''.join('<i></i>' for _ in t['stations'])}</div>
        </div>
      </div>
      <div class="f3d-prog" aria-hidden="true"><i></i></div>
      <div class="f3d-tools">
        <button type="button" class="f3d-btn f3d-ex">{ICO_ORBIT}<span>{esc(t['explore'])}</span></button>
        <a class="f3d-btn f3d-skip" href="{skip_to}">{ICO_SKIP}<span>{esc(t['skip'])}</span></a>
      </div>
      <div class="f3d-hint f3d-glass">{esc(t['hint'])}</div>
    </div>
  </section>'''
