"""Interactive 3D wireframe 1L Suction Bag scrollytelling showcase (FA / EN / AR).

Matches the exact visual & interactive architecture of factory_hero.py:
- Option 1: Engineering-drawing callouts (glowing dot + angled SVG leader line + floating text, no boxes)
- Option 2: Unified Top Interactive Station Dock (collapsed by default on mobile <768px)
- Option 3: Clickable 3D sub-component nodes synced with top dock chips + coral (#ff7a59) shader highlight
- Bonus: Exploded View toggle (.f3d-exp) separating all 6 vertical engineering layers along the Y axis
"""
import html as _h
import json

V = '20261029k'
FA_DIGITS = str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')
AR_DIGITS = str.maketrans('0123456789', '٠١٢٣٤٥٦٧٨٩')


def esc(s):
    return _h.escape(str(s), quote=True)


def num(n, lang):
    s = str(n)
    return s.translate(FA_DIGITS if lang == 'fa' else (AR_DIGITS if lang == 'ar' else {}))


T = {
    'fa': dict(
        kicker='کالبدشکافی مهندسی سه‌بعدی • کیسه ساکشن یک‌بارمصرف ۱ لیتری آبادیس (کد ۰۴۰۱۱۱۱)',
        h1a='کیسه ساکشن ',
        h1b='۱ لیتری آبادیس',
        h1c='؛ دقت میکرونی در کنترل عفونت',
        sub='قطر ۱۱ سانتی‌متر • ارتفاع ۱۵.۵ سانتی‌متر • فیلتر هیدروفوبیک ۹۹.۹۹۹٪ و پودر سوپرجاذب — اسکرول کنید، روی قطعات بزنید یا نمای انفجاری را فعال کنید.',
        aerial='بخش‌های مهندسی کیسه ساکشن ۱ لیتری',
        step='بخش {n} از {t}',
        explore='حالت کاوش آزاد',
        back='بازگشت به مسیر اسکرول',
        explode='نمای انفجاری قطعات',
        assemble='بستن نمای انفجاری',
        skip='رد کردن و ادامه صفحه',
        collapse='بستن جزئیات',
        expand='نمایش جزئیات',
        hint='بکشید تا ۳۶۰ درجه بچرخد • دو انگشت یا چرخ موس برای زوم • روی نقاط مهندسی یا دکمه‌های بالا بزنید',
        labels=[
            'درب و آب‌بندی',
            'پورت‌ها و اتصالات',
            'فیلتر آنتی‌باکتریال',
            'کیسه ۱ لیتری و جاذب',
            'مخزن و نصب بیمارستانی',
        ],
        stations=[
            dict(
                n='بخش ۱ — درب یکپارچه HDPE و سیستم قفل رینگ آب‌بند',
                t='درب فیروزه‌ای تزریق‌شده از پلی‌اتیلن سنگین پزشکی با قفل رینگ ۳۶۰ درجه، گودی مرکزی تقویت‌شده و زبانه ارگونومیک جداسازی ایمن.',
                subs=[
                    dict(
                        id=11,
                        code='۱.۱',
                        pin='۱.۱ رینگ قفل‌شونده ۳۶۰ درجه',
                        chip='۱.۱ رینگ قفل‌شونده و شیار آب‌بند ۳۶۰ درجه',
                        spec='دامنه محیطی دوجداره با ۳۶ شیار عمودی ضدلغزش که روی لبه کیسه و دهانه مخزن پلی‌کربنات قفل شده و آب‌بندی کامل وکیوم را تضمین می‌کند.',
                        pos=[12.4, 15.4, 5.4],
                        exp=[0.0, 7.5, 0.0],
                    ),
                    dict(
                        id=12,
                        code='۱.۲',
                        pin='۱.۲ گودی مرکزی درب (CAD Pit)',
                        chip='۱.۲ گودی مرکزی تقویت‌شده و نشان برجسته آبادیس',
                        spec='حفره مرکزی پله‌ای مطابق مدل مهندسی 1L pit.CATPart با ریب‌های شعاعی ضددفورمگی تحت خلأ بالا و حک برجسته نشان آبادیس.',
                        pos=[-0.8, 18.6, -6.4],
                        exp=[0.0, 7.5, 0.0],
                    ),
                    dict(
                        id=13,
                        code='۱.۳',
                        pin='۱.۳ زبانه جداسازی ایمن',
                        chip='۱.۳ دستگیره و زبانه جداسازی ایمن بدون تماس',
                        spec='زبانه ارگونومیک کناری با آج‌های ضدلغزش برای باز کردن و خروج ایمن کیسه پرشده از داخل مخزن بدون تماس دست پرستار با مسیر ترشحات.',
                        pos=[15.4, 17.0, 2.2],
                        exp=[0.0, 7.5, 0.0],
                    ),
                ],
            ),
            dict(
                n='بخش ۲ — پورت‌های ورودی، تاندم و دریچه یک‌طرفه ضدبرگشت',
                t='چیدمان مهندسی ۴ پورت استاندارد روی درب به همراه دریچه یک‌طرفه ضدبرگشت بیمار و درپوش‌های متصل آب‌بند برای امحای بهداشتی.',
                subs=[
                    dict(
                        id=21,
                        code='۲.۱',
                        pin='۲.۱ پورت بیمار و دریچه یک‌طرفه',
                        chip='۲.۱ پورت بیمار زاویه‌دار + دریچه یک‌طرفه ضدبرگشت',
                        spec='نازل مخروطی زاویه‌دار ۴۵ درجه (مناسب انواع ساکشن تیوب) مجهز به دریچه یک‌طرفه داخلی جهت جلوگیری کامل از برگشت ترشحات به سمت بیمار.',
                        pos=[7.0, 20.6, -6.4],
                        exp=[0.0, 13.5, 0.0],
                    ),
                    dict(
                        id=22,
                        code='۲.۲',
                        pin='۲.۲ پورت تاندم (اتصال سری)',
                        chip='۲.۲ پورت تاندم (اتصال سری کیسه‌ها) + کپ متصل',
                        spec='پورت اختصاصی اتصال سری برای افزایش ظرفیت جمع‌آوری با اتصال زنجیره‌ای چند کیسه به یکدیگر، همراه با بند انعطاف‌پذیر و درپوش قفل‌شونده.',
                        pos=[1.8, 20.9, 4.1],
                        exp=[0.0, 13.5, 0.0],
                    ),
                    dict(
                        id=23,
                        code='۲.۳',
                        pin='۲.۳ پورت نمونه‌گیری و کپ متصل',
                        chip='۲.۳ پورت نمونه‌گیری و درپوش‌های آب‌بند متصل',
                        spec='پورت جانبی نمونه‌گیری و تخلیه با درپوش‌های متصل یکپارچه که پس از اتمام عمل، تمامی منافذ کیسه را پیش از انتقال به زباله عفونی پلمب می‌کند.',
                        pos=[2.0, 23.6, -8.8],
                        exp=[0.0, 13.5, 0.0],
                    ),
                ],
            ),
            dict(
                n='بخش ۳ — فیلتر متخلخل هیدروفوبیک و سیستم قطع‌کن سرریز',
                t='حفاظت دوگانه از پمپ و شبکه ساکشن سانترال بیمارستان با فیلتر متخلخل آنتی‌باکتریال و مکانیسم قطع خودکار جریان در زمان پر شدن کیسه.',
                subs=[
                    dict(
                        id=31,
                        code='۳.۱',
                        pin='۳.۱ فیلتر متخلخل هیدروفوبیک',
                        chip='۳.۱ فیلتر متخلخل هیدروفوبیک (۹۹.۹۹۹٪ بازدارندگی)',
                        spec='استوانه متخلخل هیدروفوبیک و آنتی‌باکتریال در زیر پورت وکیوم با راندمان فیلتراسیون ۹۹.۹۹۹٪ که مانع عبور ذرات، باکتری‌ها و آئروسل‌های عفونی می‌شود.',
                        pos=[-6.2, 9.2, 0.8],
                        exp=[0.0, 2.0, 0.0],
                    ),
                    dict(
                        id=32,
                        code='۳.۲',
                        pin='۳.۲ قطع‌کن خودکار سرریز',
                        chip='۳.۲ محفظه شیاردار و قطع‌کن خودکار سرریز',
                        spec='با رسیدن سطح مایع به تراز ۱۰۰۰ میلی‌لیتر، فیلتر آب‌گریز و سوپاپ شناور مسیر مکش را به‌طور خودکار مسدود کرده و از ورود مایع به ساکشن مرکزی جلوگیری می‌کنند.',
                        pos=[-6.2, 1.2, 3.6],
                        exp=[0.0, 2.0, 0.0],
                    ),
                ],
            ),
            dict(
                n='بخش ۴ — کیسه چندلایه ۱ لیتری، درجه‌بندی حجمی و پودر سوپرجاذب',
                t='بدنه انعطاف‌پذیر و شفاف از فیلم پلیمری چندلایه پزشکی با جوش اولتراسونیک، مقیاس مدرج ۱۰۰ تا ۱۰۰۰ میلی‌لیتر و ساشه پودر ژل‌کننده.',
                subs=[
                    dict(
                        id=41,
                        code='۴.۱',
                        pin='۴.۱ فیلم پلیمری چندلایه',
                        chip='۴.۱ فیلم چندلایه پزشکی با جوش اولتراسونیک',
                        spec='فیلم پلیمری چندلایه انعطاف‌پذیر (قطر ۱۱ و ارتفاع ۱۵.۵ سانتی‌متر) با جوش حرارتی و اولتراسونیک دوبل به یقه درب، مقاوم در برابر فشار منفی و ضربه.',
                        pos=[-9.8, -3.5, 4.2],
                        exp=[0.0, -3.5, 0.0],
                    ),
                    dict(
                        id=42,
                        code='۴.۲',
                        pin='۴.۲ درجه‌بندی ۱۰۰ تا ۱۰۰۰ml',
                        chip='۴.۲ مقیاس مدرج ۱۰۰ تا ۱۰۰۰ میلی‌لیتر (۱L)',
                        spec='نوار درجه‌بندی دقیق از ۱۰۰ تا ۱۰۰۰ میلی‌لیتر روی دیواره شفاف کیسه جهت پایش لحظه‌ای حجم خون و مایعات جمع‌آوری‌شده در اورژانس، دندانپزشکی و اطفال.',
                        pos=[7.8, -5.5, 7.2],
                        exp=[0.0, -3.5, 0.0],
                    ),
                    dict(
                        id=43,
                        code='۴.۳',
                        pin='۴.۳ ساشه پودر جاذب (PVA/SAP)',
                        chip='۴.۳ ساشه پودر ژل‌کننده سوپرجاذب (کد ۰۴۰۱۱۱۱)',
                        spec='ساشه فیلم محلول در آب PVA حاوی پودر سوپرجاذب (SAP) در کف کیسه که به محض ورود مایع باز شده و ۱ لیتر ترشحات عفونی را به ژل نیمه‌جامد بدون نشت تبدیل می‌کند.',
                        pos=[1.2, -15.2, 2.5],
                        exp=[0.0, -9.5, 0.0],
                    ),
                ],
            ),
            dict(
                n='بخش ۵ — استقرار در مخزن پلی‌کربنات ۱ لیتری و براکت بیمارستانی',
                t='نشستن دقیق کیسه ۱ لیتری درون مخزن بیرونی پلی‌کربنات نشکن و اتصال استاندارد به پایه دیواری، ترولی و ساکشن پرتابل.',
                subs=[
                    dict(
                        id=51,
                        code='۵.۱',
                        pin='۵.۱ مخزن پلی‌کربنات ۱ لیتری',
                        chip='۵.۱ مخزن پلی‌کربنات شفاف و نشکن ۱ لیتری',
                        spec='پوسته بیرونی پلی‌کربنات شفاف، مدرج و قابل اتوکلاو که فشار خلأ را تحمل کرده و کیسه یک‌بارمصرف ۱ لیتری به‌صورت کاملاً کیپ درون آن قرار می‌گیرد.',
                        pos=[-11.5, -10.5, 4.5],
                        exp=[0.0, -15.5, 0.0],
                    ),
                    dict(
                        id=52,
                        code='۵.۲',
                        pin='۵.۲ براکت نصب دیواری و ترولی',
                        chip='۵.۲ براکت کشویی نصب روی پایه دیواری و ترولی',
                        spec='زبانه استاندارد پشت مخزن (مطابق قطعه مهندسی 1L pit.CATPart) جهت نصب سریع تکی یا سری روی براکت دیواری، کنسول بالای تخت و پایه پرتابل ۵ چرخ.',
                        pos=[0.0, 0.5, -15.8],
                        exp=[0.0, -15.5, -5.5],
                    ),
                ],
            ),
        ],
    ),
    'en': dict(
        kicker='3D Engineering Cutaway • Abadis 1L Disposable Suction Liner Bag (SKU 0401111)',
        h1a='Abadis ',
        h1b='1L Suction Liner Bag',
        h1c=' — Precision Infection Control',
        sub='11 cm diameter • 15.5 cm height • 99.999% hydrophobic filter & SAP solidifier — scroll, click 3D callouts, or toggle Exploded View.',
        aerial='1L Suction Bag Engineering Zones',
        step='Zone {n} of {t}',
        explore='Free 3D Explore',
        back='Back to Scroll Tour',
        explode='Exploded View',
        assemble='Assemble View',
        skip='Skip to Details',
        collapse='Hide details',
        expand='Show details',
        hint='Drag to rotate 360° • Pinch or scroll wheel to zoom • Click 3D callouts or top chips',
        labels=[
            'Lid & Sealing',
            'Ports & Valves',
            'Hydrophobic Filter',
            '1L Liner & SAP',
            'Canister & Mount',
        ],
        stations=[
            dict(
                n='Zone 1 — Rigid HDPE Teal Lid & 360° Snap-Lock Sealing System',
                t='Medical-grade high-density polyethylene lid featuring a 360° vacuum-tight snap-lock skirt, reinforced central CAD pit, and non-contact removal tab.',
                subs=[
                    dict(
                        id=11,
                        code='1.1',
                        pin='1.1 360° Snap-Lock Rim',
                        chip='1.1 360° Snap-Lock Rim & Grip Skirt',
                        spec='Dual-lip perimeter sealing channel with 36 vertical knurled grip ribs that locks onto the 1L polycarbonate canister mouth for leak-free vacuum integrity.',
                        pos=[12.4, 15.4, 5.4],
                        exp=[0.0, 7.5, 0.0],
                    ),
                    dict(
                        id=12,
                        code='1.2',
                        pin='1.2 Central CAD Pit',
                        chip='1.2 Reinforced Central Pit & Abadis Emblem',
                        spec='Stepped central recess derived from the 1L pit.CATPart CAD model with radial anti-collapse ribs under high vacuum and raised Abadis Med embossing.',
                        pos=[-0.8, 18.6, -6.4],
                        exp=[0.0, 7.5, 0.0],
                    ),
                    dict(
                        id=13,
                        code='1.3',
                        pin='1.3 Safe Removal Tab',
                        chip='1.3 Ergonomic Non-Contact Removal Tab',
                        spec='Textured perimeter thumb tab allowing clinical staff to unseat and seal the filled 1L liner cleanly without touching fluid-exposed surfaces.',
                        pos=[15.4, 17.0, 2.2],
                        exp=[0.0, 7.5, 0.0],
                    ),
                ],
            ),
            dict(
                n='Zone 2 — Angled Patient Port, Tandem Port & One-Way Anti-Reflux Valve',
                t='Four precision-molded top ports with an integrated one-way patient check valve and tethered sealing caps for closed-system disposal.',
                subs=[
                    dict(
                        id=21,
                        code='2.1',
                        pin='2.1 Patient Port & Valve',
                        chip='2.1 45° Patient Port & One-Way Check Valve',
                        spec='45° stepped conical hose connector fitted with an internal one-way anti-reflux valve that prevents backflow toward the patient tubing.',
                        pos=[7.0, 20.6, -6.4],
                        exp=[0.0, 13.5, 0.0],
                    ),
                    dict(
                        id=22,
                        code='2.2',
                        pin='2.2 Tandem Series Port',
                        chip='2.2 Tandem Series Port & Tethered Plug',
                        spec='Dedicated tandem port with flexible retention loop and snap plug, enabling multiple suction bags to be linked in series for higher fluid volumes.',
                        pos=[1.8, 20.9, 4.1],
                        exp=[0.0, 13.5, 0.0],
                    ),
                    dict(
                        id=23,
                        code='2.3',
                        pin='2.3 Sampling Port & Cap',
                        chip='2.3 Sampling Port & Integrated Seal Caps',
                        spec='Auxiliary sampling and access port with captive tethered plugs that hermetically seal all openings prior to infectious-waste transport.',
                        pos=[2.0, 23.6, -8.8],
                        exp=[0.0, 13.5, 0.0],
                    ),
                ],
            ),
            dict(
                n='Zone 3 — Hydrophobic Antibacterial Filter & Overflow Shut-Off Valve',
                t='Dual protection for central hospital vacuum lines combining a 99.999% porous hydrophobic barrier with automatic overflow shut-off.',
                subs=[
                    dict(
                        id=31,
                        code='3.1',
                        pin='3.1 Hydrophobic Filter',
                        chip='3.1 Sintered Hydrophobic Filter (99.999%)',
                        spec='Sintered porous hydrophobic & antibacterial filter cartridge suspended beneath the vacuum port, blocking 99.999% of bacteria, viruses, and aerosols.',
                        pos=[-6.2, 9.2, 0.8],
                        exp=[0.0, 2.0, 0.0],
                    ),
                    dict(
                        id=32,
                        code='3.2',
                        pin='3.2 Overflow Shut-Off',
                        chip='3.2 Slotted Cage & Overflow Shut-Off Valve',
                        spec='When fluid reaches 1000 ml, the hydrophobic barrier and float shut-off mechanism immediately seal the vacuum path to protect central hospital pumps.',
                        pos=[-6.2, 1.2, 3.6],
                        exp=[0.0, 2.0, 0.0],
                    ),
                ],
            ),
            dict(
                n='Zone 4 — 1L Multi-Layer Medical Liner, Graduations & SAP Solidifier',
                t='Tear-resistant co-extruded medical film bag (Ø 11 × 15.5 cm) with ultrasonic welds, 100–1000 ml volume scale, and PVA/SAP gelling packet.',
                subs=[
                    dict(
                        id=41,
                        code='4.1',
                        pin='4.1 Multi-Layer Liner',
                        chip='4.1 Multi-Layer Film & Ultrasonic Welds',
                        spec='Flexible co-extruded polymer liner thermally and ultrasonically welded 360° to the lid collar, engineered to resist puncture and negative pressure.',
                        pos=[-9.8, -3.5, 4.2],
                        exp=[0.0, -3.5, 0.0],
                    ),
                    dict(
                        id=42,
                        code='4.2',
                        pin='4.2 100–1000 ml Scale',
                        chip='4.2 100–1000 ml (1L) Graduation Scale',
                        spec='Clear 100 to 1000 ml graduation ladder along the translucent liner wall for accurate fluid monitoring in ambulance, dental, pediatric, and ER care.',
                        pos=[7.8, -5.5, 7.2],
                        exp=[0.0, -3.5, 0.0],
                    ),
                    dict(
                        id=43,
                        code='4.3',
                        pin='4.3 PVA/SAP Solidifier',
                        chip='4.3 Water-Soluble PVA / SAP Solidifier Pouch',
                        spec='Pre-measured super-absorbent polymer (SAP) in a water-soluble PVA film sachet (SKU 0401111) that rapidly solidifies 1L of infectious fluid into spill-proof gel.',
                        pos=[1.2, -15.2, 2.5],
                        exp=[0.0, -9.5, 0.0],
                    ),
                ],
            ),
            dict(
                n='Zone 5 — 1L Polycarbonate Outer Canister & Universal Hospital Mount',
                t='Precision seating inside the shatterproof graduated 1L polycarbonate canister with universal slide bracket for wall rails and mobile stands.',
                subs=[
                    dict(
                        id=51,
                        code='5.1',
                        pin='5.1 1L PC Outer Canister',
                        chip='5.1 1L Graduated Polycarbonate Outer Shell',
                        spec='Autoclavable, shatter-resistant outer polycarbonate canister (from 1L pit.CATPart) that sustains vacuum pressure while supporting the disposable liner.',
                        pos=[-11.5, -10.5, 4.5],
                        exp=[0.0, -15.5, 0.0],
                    ),
                    dict(
                        id=52,
                        code='5.2',
                        pin='5.2 Wall & Trolley Bracket',
                        chip='5.2 Integrated Slide Bracket for Stand & Wall',
                        spec='Rear dovetail mounting tongue (1L pit.CATPart) compatible with hospital wall brackets, headwall consoles, and 5-caster mobile trolley stands.',
                        pos=[0.0, 0.5, -15.8],
                        exp=[0.0, -15.5, -5.5],
                    ),
                ],
            ),
        ],
    ),
    'ar': dict(
        kicker='التشريح الهندسي ثلاثي الأبعاد • كيس الشفط الطبي ١ لتر من آباديس (رمز ٠٤٠١١١١)',
        h1a='كيس الشفط ',
        h1b='١ لتر من آباديس',
        h1c='؛ هندسة دقيقة لمكافحة العدوى',
        sub='قطر ١١ سم • ارتفاع ١٥.٥ سم • فلتر كاره للماء ٩٩.٩٩٩٪ ومسحوق مُهلِّم فائق الامتصاص — مرّر أو اضغط على الأجزاء أو فعّل العرض التفصيلي.',
        aerial='المناطق الهندسية لكيس الشفط ١ لتر',
        step='المنطقة {n} من {t}',
        explore='الاستكشاف الحر ٣٦٠°',
        back='العودة إلى مسار التمرير',
        explode='العرض التفصيلي للأجزاء',
        assemble='تجميع الأجزاء',
        skip='تخطّي ومتابعة الصفحة',
        collapse='إخفاء التفاصيل',
        expand='عرض التفاصيل',
        hint='اسحب للتدوير ٣٦٠° • قرّب للتكبير • اضغط على النقاط الهندسية أو الأزرار العلوية',
        labels=[
            'الغطاء والإحكام',
            'المنافذ والوصلات',
            'الفلتر المضاد للبكتيريا',
            'كيس ١ لتر والمادة الماصة',
            'الخزان والتثبيت',
        ],
        stations=[
            dict(
                n='المنطقة ١ — غطاء HDPE الموحّد ونظام الإغلاق المحكم ٣٦٠°',
                t='غطاء فيروزي مصنّع من البولي إيثيلين الطبي عالي الكثافة مع حافة قفل محكمة ٣٦٠° وتجويف مركزي مقوّى ولسان فصل آمن.',
                subs=[
                    dict(
                        id=11,
                        code='١.١',
                        pin='١.١ حلقة الإغلاق ٣٦٠°',
                        chip='١.١ حلقة الإغلاق المحكم وأخدود العزل ٣٦٠°',
                        spec='حافة محيطية مزدوجة الشفة مع ٣٦ ضلعاً عمودياً مانعاً للانزلاق تُحكم الإغلاق على فوهة الخزان البولي كربونات لضمان ثبات التفريغ.',
                        pos=[12.4, 15.4, 5.4],
                        exp=[0.0, 7.5, 0.0],
                    ),
                    dict(
                        id=12,
                        code='١.٢',
                        pin='١.٢ التجويف المركزي (CAD)',
                        chip='١.٢ التجويف المركزي المقوّى وشعار آباديس البارز',
                        spec='تجويف مركزي متدرّج مطابق للنموذج الهندسي 1L pit.CATPart مع أضلاع تقوية شعاعية مقاومة للانبعاج تحت الضغط السلبي العالي.',
                        pos=[-0.8, 18.6, -6.4],
                        exp=[0.0, 7.5, 0.0],
                    ),
                    dict(
                        id=13,
                        code='١.٣',
                        pin='١.٣ لسان الفصل الآمن',
                        chip='١.٣ مقبض ولسان الفصل الآمن دون تلامس',
                        spec='لسان جانبي مريح محزّز يتيح للطاقم التمريضي فك وإغلاق الكيس الممتلئ بأمان دون ملامسة مسار السوائل الملوّثة.',
                        pos=[15.4, 17.0, 2.2],
                        exp=[0.0, 7.5, 0.0],
                    ),
                ],
            ),
            dict(
                n='المنطقة ٢ — منافذ الإدخال والتوصيل المتسلسل والصمام أحادي الاتجاه',
                t='أربعة منافذ قياسية على الغطاء مزوّدة بصمام أحادي الاتجاه لمنع الرجوع إلى المريض وأغطية متصلة للإغلاق المحكم.',
                subs=[
                    dict(
                        id=21,
                        code='٢.١',
                        pin='٢.١ منفذ المريض والصمام',
                        chip='٢.١ منفذ المريض بزاوية ٤٥° + صمام مانع للرجوع',
                        spec='فوهة مخروطية بزاوية ٤٥ درجة متوافقة مع أنابيب الشفط الطبية ومزوّدة بصمام داخلي أحادي الاتجاه يمنع ارتداد السوائل نحو المريض.',
                        pos=[7.0, 20.6, -6.4],
                        exp=[0.0, 13.5, 0.0],
                    ),
                    dict(
                        id=22,
                        code='٢.٢',
                        pin='٢.٢ منفذ التوصيل المتسلسل',
                        chip='٢.٢ منفذ التوصيل المتسلسل (تاندم) مع غطاء متصل',
                        spec='منفذ مخصّص لربط عدة أكياس على التسلسل لزيادة السعة الاستيعابية، مزوّد بحلقة مرنة وسدادة إغلاق محكمة.',
                        pos=[1.8, 20.9, 4.1],
                        exp=[0.0, 13.5, 0.0],
                    ),
                    dict(
                        id=23,
                        code='٢.٣',
                        pin='٢.٣ منفذ العينات والغطاء',
                        chip='٢.٣ منفذ أخذ العينات وسدادات الإحكام المتصلة',
                        spec='منفذ إضافي لأخذ العينات والتفريغ مع أغطية متصلة تغلق جميع الفتحات بإحكام تام قبل نقل الكيس إلى النفايات الطبية.',
                        pos=[2.0, 23.6, -8.8],
                        exp=[0.0, 13.5, 0.0],
                    ),
                ],
            ),
            dict(
                n='المنطقة ٣ — الفلتر المسامي الكاره للماء وآلية إيقاف الطفح التلقائي',
                t='حماية مزدوجة لشبكة الشفط المركزي في المستشفى عبر فلتر مضاد للبكتيريا بنسبة ٩٩.٩٩٩٪ وصمام إغلاق تلقائي عند الامتلاء.',
                subs=[
                    dict(
                        id=31,
                        code='٣.١',
                        pin='٣.١ الفلتر الكاره للماء',
                        chip='٣.١ الفلتر المسامي الكاره للماء (كفاءة ٩٩.٩٩٩٪)',
                        spec='أسطوانة مسامية كارهة للماء ومضادة للبكتيريا أسفل منفذ التفريغ تمنع مرور ٩٩.٩٩٩٪ من البكتيريا والفيروسات والرذاذ الملوّث.',
                        pos=[-6.2, 9.2, 0.8],
                        exp=[0.0, 2.0, 0.0],
                    ),
                    dict(
                        id=32,
                        code='٣.٢',
                        pin='٣.٢ صمام إيقاف الطفح',
                        chip='٣.٢ القفص المشقوق وصمام إيقاف الطفح التلقائي',
                        spec='عند وصول السائل إلى مستوى ١٠٠٠ مل، يغلق الفلتر الكاره للماء والصمام العائم مسار الشفط تلقائياً لحماية مضخات الشفط المركزي.',
                        pos=[-6.2, 1.2, 3.6],
                        exp=[0.0, 2.0, 0.0],
                    ),
                ],
            ),
            dict(
                n='المنطقة ٤ — الكيس متعدد الطبقات ١ لتر والتدريج الحجمي والمسحوق الماص',
                t='جسم مرن وشفاف من فيلم بوليمري طبي متعدد الطبقات بلحام فوق صوتي، وتدريج ١٠٠–١٠٠٠ مل، وكيس مسحوق مُهلِّم.',
                subs=[
                    dict(
                        id=41,
                        code='٤.١',
                        pin='٤.١ فيلم طبي متعدد الطبقات',
                        chip='٤.١ فيلم طبي متعدد الطبقات بلحام فوق صوتي',
                        spec='فيلم بوليمري مرن عالي المتانة (قطر ١١ وارتفاع ١٥.٥ سم) ملحوم حرارياً وبالأمواج فوق الصوتية بعنق الغطاء لمقاومة الضغط السلبي والتمزق.',
                        pos=[-9.8, -3.5, 4.2],
                        exp=[0.0, -3.5, 0.0],
                    ),
                    dict(
                        id=42,
                        code='٤.٢',
                        pin='٤.٢ تدريج ١٠٠–١٠٠٠ مل',
                        chip='٤.٢ مقياس متدرّج ١٠٠ إلى ١٠٠٠ مل (١ لتر)',
                        spec='مقياس تدريج واضح من ١٠٠ إلى ١٠٠٠ مل على جدار الكيس الشفاف لمراقبة حجم السوائل بدقة في الطوارئ والإسعاف وطب الأسنان والأطفال.',
                        pos=[7.8, -5.5, 7.2],
                        exp=[0.0, -3.5, 0.0],
                    ),
                    dict(
                        id=43,
                        code='٤.٣',
                        pin='٤.٣ كيس المسحوق الماص SAP',
                        chip='٤.٣ كيس مسحوق مُهلِّم فائق الامتصاص (رمز ٠٤٠١١١١)',
                        spec='كيس من فيلم PVA القابل للذوبان في الماء يحتوي على مسحوق فائق الامتصاص (SAP) في قاع الكيس يحوّل ١ لتر من السوائل فوراً إلى هلام آمن غير قابل للانسكاب.',
                        pos=[1.2, -15.2, 2.5],
                        exp=[0.0, -9.5, 0.0],
                    ),
                ],
            ),
            dict(
                n='المنطقة ٥ — الاستقرار داخل الخزان البولي كربونات ١ لتر وحامل التثبيت',
                t='تموضع محكم للكيس داخل الخزان الخارجي البولي كربونات غير القابل للكسر مع حامل تثبيت قياسي للجدار والترولي.',
                subs=[
                    dict(
                        id=51,
                        code='٥.١',
                        pin='٥.١ خزان البولي كربونات ١ لتر',
                        chip='٥.١ خزان بولي كربونات شفاف ومدرّج ١ لتر',
                        spec='خزان خارجي شفاف من البولي كربونات القابل للتعقيم بالأتوكلاف يتحمّل ضغط التفريغ ويحتضن الكيس ذو الاستخدام الواحد بإحكام تام.',
                        pos=[-11.5, -10.5, 4.5],
                        exp=[0.0, -15.5, 0.0],
                    ),
                    dict(
                        id=52,
                        code='٥.٢',
                        pin='٥.٢ حامل التثبيت الجداري',
                        chip='٥.٢ لسان تثبيت منزلق للحائط والترولي',
                        spec='لسان تثبيت خلفي قياسي (مطابق لملف 1L pit.CATPart) للتركيب السريع الفردي أو المتسلسل على الحامل الجداري أو قاعدة الترولي المتحركة.',
                        pos=[0.0, 0.5, -15.8],
                        exp=[0.0, -15.5, -5.5],
                    ),
                ],
            ),
        ],
    ),
}

ICO_ORBIT = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="9" ry="3.8"/><path d="M12 3a15 15 0 0 1 0 18"/></svg>'
ICO_EXPLODE = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v6m0 8v6M4.93 4.93l4.24 4.24m5.66 5.66 4.24 4.24M2 12h6m8 0h6M4.93 19.07l4.24-4.24m5.66-5.66 4.24-4.24"/></svg>'
ICO_SKIP = '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 10l5 5 5-5"/><path d="M5 19h14"/></svg>'
ICO_CHEV = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m6 15 6-6 6 6"/></svg>'


def head(p):
    return f'<link rel="stylesheet" href="{p}assets/css/factory-3d.css?v={V}">'


def scripts(p):
    return f'<script type="module" src="{p}assets/js/suction-bag-1l-3d.js?v={V}"></script>\n'


def section(p, lang='fa', skip_to='#s1', sec_id='bag-3d', tag_h='h2'):
    t = T[lang]
    cfg = {
        'lang': lang,
        'step': t['step'],
        'total': num(5, lang),
        'nums': [num(i, lang) for i in range(1, 6)],
        'stations': t['stations'],
        'labels': t['labels'],
        'explore': t['explore'],
        'back': t['back'],
        'explode': t['explode'],
        'assemble': t['assemble'],
        'collapse': t['collapse'],
        'expand': t['expand'],
    }
    pills = ''.join(
        f'<button type="button" class="f3d-pill" data-i="{i}"><b>{num(i + 1, lang)}</b><span>{esc(lb)}</span></button>'
        for i, lb in enumerate(t['labels'][:5])
    )
    return f'''  <section class="f3d f3d--bag" id="{esc(sec_id)}" aria-label="{esc(t['h1a'] + t['h1b'] + t['h1c'])}">
    <script type="application/json" class="f3d-cfg">{json.dumps(cfg, ensure_ascii=False)}</script>
    <div class="f3d-stage">
      <canvas class="f3d-gl" aria-hidden="true"></canvas>
      <div class="f3d-labels"></div>
      <div class="f3d-subpins"></div>
      <div class="f3d-intro">
        <p class="f3d-kicker">{esc(t['kicker'])}</p>
        <{tag_h} class="f3d-h">{esc(t['h1a'])}<b>{esc(t['h1b'])}</b>{esc(t['h1c'])}</{tag_h}>
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
          <div class="f3d-dots"><i></i><i></i><i></i><i></i><i></i></div>
        </div>
      </div>
      <div class="f3d-prog" aria-hidden="true"><i></i></div>
      <div class="f3d-tools">
        <button type="button" class="f3d-btn f3d-ex">{ICO_ORBIT}<span>{esc(t['explore'])}</span></button>
        <button type="button" class="f3d-btn f3d-exp" aria-pressed="false">{ICO_EXPLODE}<span>{esc(t['explode'])}</span></button>
        <a class="f3d-btn f3d-skip" href="{esc(skip_to)}">{ICO_SKIP}<span>{esc(t['skip'])}</span></a>
      </div>
      <div class="f3d-hint f3d-glass">{esc(t['hint'])}</div>
    </div>
  </section>'''
