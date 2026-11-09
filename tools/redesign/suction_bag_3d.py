"""Interactive 3D wireframe 1L Suction Bag scrollytelling showcase (FA / EN / AR).

Matches the exact visual & interactive architecture of factory_hero.py:
- Option 1: Engineering-drawing callouts (glowing dot + angled SVG leader line + floating text, no boxes)
- Option 2: Unified Top Interactive Station Dock (collapsed by default on mobile <768px)
- Option 3: Clickable 3D sub-component nodes synced with top dock chips + coral (#ff7a59) shader highlight
- Bonus: Exploded View toggle (.f3d-exp) separating all 6 vertical engineering layers along the Y axis
"""
import html as _h
import json

V = '20261109d'
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
                n='بخش ۲ — پورت بیمار، پورت تاندم و پورت وکیوم',
                t='سه پورت روی درب: لوله باریک بیمار در شیار لبه، میله تاندم در چاهک مرکزی و پورت ضخیم وکیوم در چاهک گرد فرورفته.',
                subs=[
                    dict(
                        id=21,
                        code='۲.۱',
                        pin='۲.۱ پورت بیمار (PATIENT)',
                        chip='۲.۱ پورت بیمار — لوله باریک افقی کنار لبه',
                        spec='لوله اتصال باریک و بلند که به\u200cصورت افقی در شیار کنار لبه درب قرار دارد و با حک «PATIENT» مشخص شده است؛ دریچه یک\u200cطرفه زیر آن از برگشت ترشحات به سمت بیمار جلوگیری می\u200cکند.',
                        pos=[-5.0, 20.4, 6.6],
                        exp=[0.0, 13.5, 0.0],
                    ),
                    dict(
                        id=22,
                        code='۲.۲',
                        pin='۲.۲ پورت تاندم',
                        chip='۲.۲ پورت تاندم — میله باریک ایستاده در چاهک',
                        spec='میله باریک ایستاده درون چاهک گرد برای اتصال سری چند کیسه و افزایش ظرفیت جمع\u200cآوری.',
                        pos=[2.0, 23.6, -8.8],
                        exp=[0.0, 13.5, 0.0],
                    ),
                    dict(
                        id=23,
                        code='۲.۳',
                        pin='۲.۳ پورت وکیوم (VACUUM)',
                        chip='۲.۳ پورت وکیوم — لوله ضخیم زاویه\u200cدار در چاهک گرد',
                        spec='لوله ضخیم زاویه\u200cدار با سر مورب که درون چاهک گرد فرورفته درب نشسته و با حک «VACUUM» مشخص شده است؛ مکش از طریق فیلتر هیدروفوبیک به این پورت منتقل می\u200cشود.',
                        pos=[6.5, 20.6, -6.4],
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
                n='Section 2 — Patient, Tandem & Vacuum Ports',
                t='Three ports on the lid: a slim patient tube in the rim slot, a tandem rod in the round well, and a thick vacuum port in the recessed well.',
                subs=[
                    dict(
                        id=21,
                        code='2.1',
                        pin='2.1 PATIENT port',
                        chip='2.1 Patient port — long slim horizontal tube near the rim',
                        spec='Long slim connector tube lying horizontally in a slot near the lid rim, embossed "PATIENT"; a one-way valve beneath it stops secretions flowing back toward the patient.',
                        pos=[-5.0, 20.4, 6.6],
                        exp=[0.0, 13.5, 0.0],
                    ),
                    dict(
                        id=22,
                        code='2.2',
                        pin='2.2 Tandem port',
                        chip='2.2 Tandem port — slim upright rod in the well',
                        spec='Slim upright rod rising from the round well, used to link several bags in series for more collection capacity.',
                        pos=[2.0, 23.6, -8.8],
                        exp=[0.0, 13.5, 0.0],
                    ),
                    dict(
                        id=23,
                        code='2.3',
                        pin='2.3 VACUUM port',
                        chip='2.3 Vacuum port — thick angled tube in the recessed well',
                        spec='Thick angled tube with a bevel-cut end seated in the round recessed well, embossed "VACUUM"; suction is drawn through the hydrophobic filter to this port.',
                        pos=[6.5, 20.6, -6.4],
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
                n='القسم ٢ — منفذ المريض ومنفذ التوصيل المتسلسل ومنفذ الشفط',
                t='ثلاثة منافذ على الغطاء: أنبوب المريض الرفيع في شق الحافة، وقضيب التوصيل المتسلسل في البئر الدائرية، ومنفذ الشفط السميك في البئر الغائرة.',
                subs=[
                    dict(
                        id=21,
                        code='٢.١',
                        pin='٢.١ منفذ المريض (PATIENT)',
                        chip='٢.١ منفذ المريض — أنبوب رفيع أفقي قرب الحافة',
                        spec='أنبوب توصيل رفيع وطويل يقع أفقياً في شق قرب حافة الغطاء ومحفور عليه «PATIENT»؛ يمنع الصمام أحادي الاتجاه أسفله ارتداد الإفرازات نحو المريض.',
                        pos=[-5.0, 20.4, 6.6],
                        exp=[0.0, 13.5, 0.0],
                    ),
                    dict(
                        id=22,
                        code='٢.٢',
                        pin='٢.٢ منفذ التوصيل المتسلسل',
                        chip='٢.٢ منفذ التوصيل المتسلسل — قضيب رفيع قائم في البئر',
                        spec='قضيب رفيع قائم داخل البئر الدائرية لتوصيل عدة أكياس على التوالي وزيادة سعة التجميع.',
                        pos=[2.0, 23.6, -8.8],
                        exp=[0.0, 13.5, 0.0],
                    ),
                    dict(
                        id=23,
                        code='٢.٣',
                        pin='٢.٣ منفذ الشفط (VACUUM)',
                        chip='٢.٣ منفذ الشفط — أنبوب سميك مائل في البئر الغائرة',
                        spec='أنبوب سميك مائل بطرف مشطوف مثبت في البئر الدائرية الغائرة ومحفور عليه «VACUUM»؛ ينتقل الشفط عبر الفلتر الكاره للماء إلى هذا المنفذ.',
                        pos=[6.5, 20.6, -6.4],
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


GATE = {
    'fa': dict(
        btn='نمایش سه‌بعدی',
        note='طرح مهندسی ثابت همین حالا دیده می‌شود. با زدن دکمه، مدل سه‌بعدی فقط در صورت نیاز بارگذاری می‌شود.',
        alt='طرح سه‌بعدی کیسه ساکشن یک‌بارمصرف ۱ لیتری آبادیس',
    ),
    'en': dict(
        btn='View in 3D',
        note='A still engineering sketch is shown first. The interactive 3D model downloads only after you tap the button.',
        alt='3D sketch of the Abadis 1L disposable suction liner',
    ),
    'ar': dict(
        btn='عرض ثلاثي الأبعاد',
        note='تظهر رسمة هندسية ثابتة أولاً. يُحمَّل النموذج التفاعلي ثلاثي الأبعاد فقط بعد الضغط على الزر.',
        alt='رسمة ثلاثية الأبعاد لكيس الشفط أحادي الاستعمال سعة ١ لتر من آباديس',
    ),
}

ICO_CUBE = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2 3 7v10l9 5 9-5V7l-9-5z"/><path d="M12 22V12"/><path d="m3 7 9 5 9-5"/></svg>'


ICO_ORBIT = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="9" ry="3.8"/><path d="M12 3a15 15 0 0 1 0 18"/></svg>'
ICO_EXPLODE = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v6m0 8v6M4.93 4.93l4.24 4.24m5.66 5.66 4.24 4.24M2 12h6m8 0h6M4.93 19.07l4.24-4.24m5.66-5.66 4.24-4.24"/></svg>'
ICO_SKIP = '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 10l5 5 5-5"/><path d="M5 19h14"/></svg>'
ICO_CHEV = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m6 15 6-6 6 6"/></svg>'


def head(p):
    return (
        f'<link rel="stylesheet" href="{p}assets/css/factory-3d.css?v={V}">'
        f'\n<link rel="stylesheet" href="{p}assets/css/product-3d-pilot.css?v={V}">'
    )


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
    g = GATE[lang]
    sketch = (
        f'<span class="theme-sketch f3d-gate-fallback" aria-hidden="true">'
        f'<img class="ts-light" src="{p}assets/img/products/3d/p01-1l-liner-light.webp" width="1200" height="771" alt="" loading="lazy" decoding="async">'
        f'<img class="ts-dark" src="{p}assets/img/products/3d/p01-1l-liner-dark.webp" width="1200" height="771" alt="" loading="lazy" decoding="async">'
        f'</span>'
    )
    gate = (
        f'<div class="f3d-gate">'
        f'{sketch}'
        f'<button type="button" class="f3d-gate-btn" data-f3d-start>{ICO_CUBE}<span>{esc(g["btn"])}</span></button>'
        f'<p class="f3d-gate-note">{esc(g["note"])}</p>'
        f'</div>'
    )
    return f'''  <section class="f3d f3d--bag is-gated" id="{esc(sec_id)}" aria-label="{esc(t['h1a'] + t['h1b'] + t['h1c'])}" data-f3d-src="{p}assets/js/suction-bag-1l-3d.js?v={V}">
    <script type="application/json" class="f3d-cfg">{json.dumps(cfg, ensure_ascii=False)}</script>
    <div class="f3d-stage">
      {gate}
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


def theme_sketch(p, light, dark, alt, w=1200, h=771, loading='lazy', cls=''):
    """Theme-aware light/dark sketch pair (noir uses dark)."""
    extra = (' ' + cls) if cls else ''
    return (
        f'<span class="theme-sketch{extra}">'
        f'<img class="ts-light" src="{p}{light}" width="{w}" height="{h}" alt="{esc(alt)}" loading="{loading}" decoding="async">'
        f'<img class="ts-dark" src="{p}{dark}" width="{w}" height="{h}" alt="" loading="{loading}" decoding="async" aria-hidden="true">'
        f'</span>'
    )


CAD_UI = {
    'fa': dict(
        h='مشخصات فنی',
        lead='نقشه‌های خطی CAD کیسه ساکشن ۱ لیتری — ابعاد اسمی سازنده: قطر ۱۱ سانتی‌متر × ارتفاع ۱۵٫۵ سانتی‌متر.',
        dl='دانلود برگه فنی (PDF)',
        dim='ابعاد اسمی سازنده: ⌀۱۱ cm × H۱۵٫۵ cm',
        views=[('iso', 'ایزومتریک'), ('front', 'نما از جلو'), ('top', 'نما از بالا')],
        zoom='نمایش بزرگ‌تر',
        alt='طرح سه‌بعدی کیسه ساکشن یک‌بارمصرف ۱ لیتری آبادیس',
    ),
    'en': dict(
        h='Technical specs',
        lead='CAD line drawings for the 1L suction liner — manufacturer nominal dimensions: Ø11 cm × H15.5 cm.',
        dl='Download technical sheet (PDF)',
        dim='Manufacturer nominal dimensions: Ø11 cm × H15.5 cm',
        views=[('iso', 'Isometric'), ('front', 'Front'), ('top', 'Top')],
        zoom='Larger view',
        alt='3D sketch of the Abadis 1L disposable suction liner',
    ),
    'ar': dict(
        h='المواصفات الفنية',
        lead='رسومات CAD الخطية لكيس الشفط سعة ١ لتر — الأبعاد الاسمية للشركة المصنعة: ⌀١١ سم × ارتفاع ١٥٫٥ سم.',
        dl='تنزيل الورقة الفنية (PDF)',
        dim='الأبعاد الاسمية للشركة المصنعة: ⌀١١ سم × ارتفاع ١٥٫٥ سم',
        views=[('iso', 'منظور متساوي القياس'), ('front', 'الواجهة'), ('top', 'من الأعلى')],
        zoom='عرض أكبر',
        alt='رسمة ثلاثية الأبعاد لكيس الشفط أحادي الاستعمال سعة ١ لتر من آباديس',
    ),
}

ICO_DL = (
    '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" '
    'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    '<path d="M12 3v12"/><path d="m7 10 5 5 5-5"/><path d="M5 21h14"/></svg>'
)


def cad_tech_section(p, lang='fa'):
    """CAD plates + self-hosted PDF beside the product specs."""
    ui = CAD_UI[lang]
    plates = []
    for view, label in ui['views']:
        light = f'assets/img/products/3d/p01-1l-liner-{view}-light.webp'
        dark = f'assets/img/products/3d/p01-1l-liner-{view}-dark.webp'
        wh = (662, 662) if view != 'front' else (675, 570)
        alt = ui['alt'] + ' — ' + label
        plates.append(
            '<a class="cad-plate" href="' + p + light + '" data-gallery="cad-1l" data-w="' + str(wh[0]) +
            '" data-h="' + str(wh[1]) + '" aria-label="' + esc(ui['zoom']) + ': ' + esc(label) + '">'
            '<figure>' + theme_sketch(p, light, dark, alt, w=wh[0], h=wh[1]) +
            '<figcaption><strong>' + esc(label) + '</strong><span>' + esc(ui['dim']) +
            '</span></figcaption></figure></a>'
        )
    pdf = p + 'assets/docs/abadis-1l-suction-liner-technical-drawing.pdf'
    return (
        '  <section class="section cad-tech" id="tech-drawings">\n'
        '    <div class="wrap">\n'
        '      <div class="cad-tech-head">\n'
        '        <div>\n'
        '          <h2>' + esc(ui['h']) + '</h2>\n'
        '          <p>' + esc(ui['lead']) + '</p>\n'
        '        </div>\n'
        '        <div class="cad-tech-actions">\n'
        '          <a class="cad-dl" href="' + pdf + '" download target="_blank" rel="noopener" '
        'data-track="tech_drawing_download">' + ICO_DL + '<span>' + esc(ui['dl']) + '</span></a>\n'
        '        </div>\n'
        '      </div>\n'
        '      <div class="cad-grid">' + ''.join(plates) + '</div>\n'
        '      <p class="cad-dim">' + esc(ui['dim']) + '</p>\n'
        '    </div>\n'
        '  </section>\n'
    )


def s1_photo_main(p, lang, gallery='s1'):
    """Original product photo as #s1 main (content parity — additions only)."""
    ui = CAD_UI[lang]
    labels = {
        'fa': 'عکس محصول کیسه ساکشن ۱ لیتری',
        'en': '1-litre suction bag product photo',
        'ar': 'صورة منتج كيس الشفط سعة ١ لتر',
    }
    alt = labels[lang]
    return (
        '<a class="gal-main" href="' + p + 'assets/img/p/p1-main.webp" data-gallery="' + gallery +
        '" data-w="900" data-h="900" aria-label="' + esc(ui['zoom']) + ': ' + esc(alt) + '">'
        '<img src="' + p + 'assets/img/p/p1-main.webp" width="900" height="900" alt="' + esc(alt) +
        '" loading="eager" decoding="async"></a>'
    )


def s1_sketch_thumb(p, lang, gallery='s1'):
    """Theme-aware sketch as an extra gallery thumb (does not replace the photo)."""
    ui = CAD_UI[lang]
    light = 'assets/img/products/3d/p01-1l-liner-light.webp'
    dark = 'assets/img/products/3d/p01-1l-liner-dark.webp'
    return (
        '<a class="gal-thumb gal-thumb--sketch" href="' + p + light + '" data-gallery="' + gallery +
        '" data-w="1200" data-h="771" aria-label="' + esc(ui['zoom']) + ': ' + esc(ui['alt']) + '">'
        + theme_sketch(p, light, dark, ui['alt'], w=240, h=154, loading='lazy', cls='gal-thumb-sketch')
        + '</a>'
    )


# Back-compat alias used by older call sites — now returns photo main (parity).
def s1_sketch_main(p, lang, gallery='s1'):
    return s1_photo_main(p, lang, gallery)


SKETCH_GAL = {
    'fa': dict(
        h='گالری طرح سه‌بعدی',
        lead='زاویه‌ها و سبک‌های طرح مهندسی کیسه ساکشن ۱ لیتری — افزوده‌شده در کنار عکس‌های محصول.',
        zoom='نمایش بزرگ‌تر',
        items=[
            ('p01-1l-liner-light.webp', 'p01-1l-liner-dark.webp', 'استودیو سه‌بعدی', 1067, 1200),
            ('p01-sketch-wire-light.webp', 'p01-sketch-wire-dark.webp', 'خطی CAD', 889, 1000),
            ('p01-gal-wire-light.webp', 'p01-gal-wire-dark.webp', 'وایر فریم', 1000, 656),
            ('p01-gal-studio-light.webp', 'p01-gal-studio-dark.webp', 'چندزاویه استودیو', 1000, 656),
            ('p01-gal-explode-light.webp', 'p01-gal-explode-dark.webp', 'انفجاری / برش', 1000, 656),
            ('p01-gal-side.webp', 'p01-gal-side.webp', 'نمای جانبی', 750, 1000),
            ('p01-gal-threeq.webp', 'p01-gal-threeq.webp', 'سه‌ربع', 750, 1000),
            ('p01-gal-top.webp', 'p01-gal-top.webp', 'از بالا', 750, 1000),
            ('p01-1l-liner-iso-light.webp', 'p01-1l-liner-iso-dark.webp', 'ایزومتریک فنی', 662, 662),
        ],
    ),
    'en': dict(
        h='3D sketch gallery',
        lead='Angles and engineering sketch styles for the 1L suction liner — added alongside the product photos.',
        zoom='Larger view',
        items=[
            ('p01-1l-liner-light.webp', 'p01-1l-liner-dark.webp', 'Studio 3D', 1067, 1200),
            ('p01-sketch-wire-light.webp', 'p01-sketch-wire-dark.webp', 'CAD line', 889, 1000),
            ('p01-gal-wire-light.webp', 'p01-gal-wire-dark.webp', 'Wireframe', 1000, 656),
            ('p01-gal-studio-light.webp', 'p01-gal-studio-dark.webp', 'Multi-angle studio', 1000, 656),
            ('p01-gal-explode-light.webp', 'p01-gal-explode-dark.webp', 'Exploded / cutaway', 1000, 656),
            ('p01-gal-side.webp', 'p01-gal-side.webp', 'Side', 750, 1000),
            ('p01-gal-threeq.webp', 'p01-gal-threeq.webp', 'Three-quarter', 750, 1000),
            ('p01-gal-top.webp', 'p01-gal-top.webp', 'Top-down', 750, 1000),
            ('p01-1l-liner-iso-light.webp', 'p01-1l-liner-iso-dark.webp', 'Technical isometric', 662, 662),
        ],
    ),
    'ar': dict(
        h='معرض الرسمات ثلاثية الأبعاد',
        lead='زوايا وأنماط الرسم الهندسي لكيس الشفط سعة ١ لتر — مضافة إلى جانب صور المنتج.',
        zoom='عرض أكبر',
        items=[
            ('p01-1l-liner-light.webp', 'p01-1l-liner-dark.webp', 'استوديو ثلاثي الأبعاد', 1067, 1200),
            ('p01-sketch-wire-light.webp', 'p01-sketch-wire-dark.webp', 'خط CAD', 889, 1000),
            ('p01-gal-wire-light.webp', 'p01-gal-wire-dark.webp', 'إطار سلكي', 1000, 656),
            ('p01-gal-studio-light.webp', 'p01-gal-studio-dark.webp', 'زوايا متعددة', 1000, 656),
            ('p01-gal-explode-light.webp', 'p01-gal-explode-dark.webp', 'تفجير / مقطع', 1000, 656),
            ('p01-gal-side.webp', 'p01-gal-side.webp', 'جانبي', 750, 1000),
            ('p01-gal-threeq.webp', 'p01-gal-threeq.webp', 'ثلاثة أرباع', 750, 1000),
            ('p01-gal-top.webp', 'p01-gal-top.webp', 'من الأعلى', 750, 1000),
            ('p01-1l-liner-iso-light.webp', 'p01-1l-liner-iso-dark.webp', 'منظور فني', 662, 662),
        ],
    ),
}


def sketch_gallery_section(p, lang='fa'):
    """Multi-angle sketch gallery with lightbox (additions only)."""
    ui = SKETCH_GAL[lang]
    cards = []
    for light, dark, label, w, h in ui['items']:
        lp = 'assets/img/products/3d/' + light
        dp = 'assets/img/products/3d/' + dark
        alt = ui['h'] + ' — ' + label
        cards.append(
            '<a class="skg-card" href="' + p + lp + '" data-gallery="skg-1l" data-w="' + str(w) +
            '" data-h="' + str(h) + '" aria-label="' + esc(ui['zoom']) + ': ' + esc(label) + '">'
            '<figure>' + theme_sketch(p, lp, dp, alt, w=w, h=h) +
            '<figcaption>' + esc(label) + '</figcaption></figure></a>'
        )
    return (
        '  <section class="section skg" id="sketch-gallery">\n'
        '    <div class="wrap">\n'
        '      <div class="skg-head"><h2>' + esc(ui['h']) + '</h2>'
        '<p>' + esc(ui['lead']) + '</p></div>\n'
        '      <div class="skg-grid">' + ''.join(cards) + '</div>\n'
        '    </div>\n'
        '  </section>\n'
    )


CIN_UI = {
    'fa': dict(
        h='نمای سینمایی',
        lead='مدار آرام دور کیسه ۱ لیتری با نورپردازی مهندسی و باز شدن جزئی درب برای نمایش رینگ و لاینر.',
        play='پخش نمای سینمایی',
        pause='توقف',
        resume='ادامه',
        note='مدل فقط پس از کلیک یا ورود به نما بارگذاری می‌شود. در صورت نبود WebGL، تصویر ثابت نمایش داده می‌شود.',
        reduced='حرکت کاهش‌یافته فعال است — تصویر ثابت نمایش داده می‌شود.',
        alt='نمای سینمایی کیسه ساکشن ۱ لیتری آبادیس',
        nogl='موتور سه‌بعدی در این مرورگر در دسترس نیست. تصویر ثابت را ببینید.',
    ),
    'en': dict(
        h='Cinematic view',
        lead='A slow orbit around the 1L liner with engineering lighting and a gentle lid lift that reveals the collar and bag.',
        play='Play cinematic view',
        pause='Pause',
        resume='Resume',
        note='The 3D model loads only after you click or the section enters view. If WebGL is unavailable, a still image is shown.',
        reduced='Reduced motion is on — showing a still frame.',
        alt='Cinematic view of the Abadis 1L suction liner',
        nogl='3D is not available in this browser. Showing a still image.',
    ),
    'ar': dict(
        h='عرض سينمائي',
        lead='مدار بطيء حول كيس ١ لتر بإضاءة هندسية ورفع خفيف للغطاء لإظهار الطوق والبطانة.',
        play='تشغيل العرض السينمائي',
        pause='إيقاف مؤقت',
        resume='متابعة',
        note='يُحمَّل النموذج فقط بعد النقر أو دخول القسم إلى الشاشة. عند غياب WebGL تُعرض صورة ثابتة.',
        reduced='تقليل الحركة مفعّل — تُعرض إطار ثابت.',
        alt='عرض سينمائي لكيس الشفط سعة ١ لتر من آباديس',
        nogl='العرض ثلاثي الأبعاد غير متاح في هذا المتصفح. تُعرض صورة ثابتة.',
    ),
}

ICO_PLAY = (
    '<svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor" aria-hidden="true">'
    '<path d="M8 5.14v13.72L19 12 8 5.14z"/></svg>'
)
ICO_PAUSE = (
    '<svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor" aria-hidden="true">'
    '<rect x="6" y="5" width="4" height="14" rx="1"/><rect x="14" y="5" width="4" height="14" rx="1"/></svg>'
)


def cinematic_section(p, lang='fa'):
    """Full-width cinematic orbit gate — loads Three.js only on demand."""
    ui = CIN_UI[lang]
    poster = p + 'assets/img/products/3d/p01-cinematic-poster.webp'
    return (
        '  <section class="section cin-sec" id="cinematic" aria-label="' + esc(ui['h']) + '">\n'
        '    <div class="wrap cin-wrap">\n'
        '      <div class="cin-head"><h2>' + esc(ui['h']) + '</h2>'
        '<p>' + esc(ui['lead']) + '</p></div>\n'
        '      <div class="cin-stage is-gated" data-cin-root'
        ' data-cin-module="' + p + 'assets/js/suction-bag-1l-cinematic.js?v=' + V + '"'
        ' data-cin-base="' + p + '3d-sketches/p01-cinematic/"'
        ' data-cin-play="' + esc(ui['play']) + '"'
        ' data-cin-pause="' + esc(ui['pause']) + '"'
        ' data-cin-resume="' + esc(ui['resume']) + '"'
        ' data-cin-reduced="' + esc(ui['reduced']) + '"'
        ' data-cin-nogl="' + esc(ui['nogl']) + '">\n'
        '        <div class="cin-gate">\n'
        '          <img class="cin-poster" src="' + poster + '" width="1440" height="810" alt="' + esc(ui['alt']) +
        '" loading="lazy" decoding="async">\n'
        '          <button type="button" class="cin-start" data-cin-start>' + ICO_PLAY +
        '<span>' + esc(ui['play']) + '</span></button>\n'
        '          <p class="cin-note">' + esc(ui['note']) + '</p>\n'
        '        </div>\n'
        '        <canvas class="cin-gl" aria-hidden="true"></canvas>\n'
        '        <div class="cin-bar" aria-hidden="true"></div>\n'
        '        <button type="button" class="cin-toggle" data-cin-toggle hidden>' + ICO_PAUSE +
        '<span>' + esc(ui['pause']) + '</span></button>\n'
        '        <p class="cin-status" data-cin-status hidden></p>\n'
        '      </div>\n'
        '    </div>\n'
        '  </section>\n'
    )


def scripts(p):
    # Gate for interactive cutaway + cinematic loader (both deferred).
    return (
        f'<script type="module" src="{p}assets/js/suction-bag-1l-3d-gate.js?v={V}" '
        f'data-f3d-module="{p}assets/js/suction-bag-1l-3d.js?v={V}"></script>\n'
        f'<script type="module" src="{p}assets/js/suction-bag-1l-cinematic-gate.js?v={V}"></script>\n'
    )
