// Abadis Med Complete 25-Product 3D Parametric CAD & Studio Model Library
export const CATEGORIES = [
  { id: 'cat-1-suction-bags', num: 1, fa: 'کیسه‌های ساکشن', en: 'Disposable Suction Bags & Core', descFa: 'کیسه‌های ساکشن یکبارمصرف ۱، ۲ و ۳ لیتری با فیلتر قطع‌کن هیدروفوبیک و پودر ژل‌کننده', descEn: '1L, 2L & 3L Frosted Liners with Hydrophobic Shut-Off Valve & Coagulant Sachet' },
  { id: 'cat-2-canisters', num: 2, fa: 'مخازن ساکشن و نمونه‌گیری', en: 'Suction Canisters & Collection Jars', descFa: 'مخازن پلی‌کربنات مدرج، ساکشن دیواری، ظرف نمونه و مخزن جمع‌آوری چربی', descEn: 'Reusable Polycarbonate Canisters, Wall Units, Specimen Traps & Lipo Jars' },
  { id: 'cat-3-suction-tubes', num: 3, fa: 'ساکشن تیوب و رابط کنترل', en: 'Medical Suction Tubes & Finger-Tip', descFa: 'لوله رابط ساکشن PVC پزشکی ضد تاخوردگی و رابط کنترل خلا فینگر تیپ', descEn: 'Non-Kinking Medical PVC Connecting Tubes & Finger-Tip Vacuum Control Adapters' },
  { id: 'cat-4-filters', num: 4, fa: 'فیلترهای محافظ و قطع‌کن', en: 'Hydrophobic & Antibacterial Filters', descFa: 'فیلتر آنتی‌باکتریال دیسکی، فیلتر قطع‌کن جریان و فیلتر متخلخل پلی‌اتیلنی', descEn: 'Antibacterial Disc Filters, Overflow Shut-Off Cages & Sintered PE Elements' },
  { id: 'cat-5-stands-holders', num: 5, fa: 'پایه، ترولی و نگهدارنده', en: 'Suction Trolleys, Wall Brackets & Clips', descFa: 'پایه ساکشن پرتابل ۴ مخزنه، گیره دیواری و پشت گیره مخزن', descEn: '4-Canister Mobile Trolleys, Wall Slide Brackets & Rear Mounting Clips' },
  { id: 'cat-6-connectors-regulators', num: 6, fa: 'اتصالات، شلنگ و رگولاتور', en: 'Connectors, Silicone Hoses & Regulators', descFa: 'اتصال T شکل، رابط مستقیم، شلنگ سیلیکونی، رگولاتور خلا و شیر قطع و وصل', descEn: 'Tandem T-Connectors, Straight Unions, Silicone Jumper Hoses, Regulators & Valves' },
  { id: 'cat-7-other-products', num: 7, fa: 'سایر محصولات مراقبتی و جراحی', en: 'Oral Care, Airway & OR Fluid Products', descFa: 'مسواک ساکشن یکبارمصرف، نگهدارنده لوله تراشه، رسیور ۶۰۰cc و مکش سطحی Splash-Vac', descEn: 'Suction Toothbrush, Endotracheal Tube Holder, 600cc Kidney Basin & Splash-Vac Dome' },
];

export const PRODUCTS = [
  {
    id: 'p01', code: 'ABD-SB-1000', catId: 'cat-1-suction-bags',
    faName: 'کیسه ساکشن یکبار مصرف ۱ لیتری آبادیس',
    enName: '1L Disposable Suction Liner Bag',
    dims: 'Ø110 × 155 mm | 1000 mL',
    material: 'Medical PP Copolymer Liner + HDPE Teal Lid (#05686b)',
    specFa: 'مجهز به فیلتر هیدروفوبیک قطع‌کن خودکار، پورت بیمار و وکیوم زاویه‌دار ۴۵ درجه، درپوش متصل و ساشه پودر ژل‌کننده',
    specEn: '45° angled patient & vacuum ports, deep crescent recess, tethered cap with U-clip, internal shut-off filter cage & coagulant pad',
    refImg: './assets/refs/p01-ref.png',
    callouts: [
      { label: 'Patient & Vacuum 45° Ports | پورت بیمار و وکیوم', target: [0.02, 0.088, 0.015], offset: [0.095, 0.115, 0] },
      { label: 'Hydrophobic Shut-Off Cage | فیلتر قطع‌کن داخلی', target: [0.0, 0.015, 0.0], offset: [-0.105, 0.035, 0] },
      { label: '1000 mL Frosted Liner | بدنه مدرج ۱ لیتری', target: [0.048, -0.03, 0.01], offset: [0.105, -0.025, 0] },
      { label: 'Coagulant Sachet | پد پودر ژل‌کننده', target: [0.0, -0.085, 0.0], offset: [-0.095, -0.095, 0] },
    ]
  },
  {
    id: 'p02', code: 'ABD-SB-2000', catId: 'cat-1-suction-bags',
    faName: 'کیسه ساکشن یکبار مصرف ۲ لیتری آبادیس',
    enName: '2L Disposable Suction Liner Bag',
    dims: 'Ø110 × 245 mm | 2000 mL',
    material: 'Medical PP Copolymer Liner + HDPE Teal Lid',
    specFa: 'ظرفیت ۲۰۰۰ میلی‌لیتر با بدنه نیمه‌شفاف مدرج، پورت تاندم، فیلتر قطع‌کن هیدروفوبیک و پودر ژل‌کننده جاذب',
    specEn: 'Tall 2000 mL tapered frosted liner, dual angled ports + tandem port, internal shut-off valve & superabsorbent pouch',
    refImg: './assets/refs/p02-ref.png',
    callouts: [
      { label: 'Stepped Snap Lid & Ports | درب قفل‌شونده و پورت‌ها', target: [0.015, 0.105, 0.01], offset: [0.095, 0.12, 0] },
      { label: 'Internal Filter Cage | محفظه فیلتر قطع‌کن', target: [0.0, 0.045, 0.0], offset: [-0.105, 0.055, 0] },
      { label: '2000 mL Graduated Body | بدنه مدرج ۲ لیتری', target: [0.048, -0.02, 0.0], offset: [0.105, -0.02, 0] },
      { label: 'Bottom Gelling Pad | ساشه پودر ژل‌کننده', target: [0.0, -0.102, 0.0], offset: [-0.095, -0.11, 0] },
    ]
  },
  {
    id: 'p03', code: 'ABD-SB-3000', catId: 'cat-1-suction-bags',
    faName: 'کیسه ساکشن یکبار مصرف ۳ لیتری آبادیس',
    enName: '3L Disposable Suction Liner Bag',
    dims: 'Ø130 × 275 mm | 3000 mL',
    material: 'Heavy-Duty Medical PP Liner + HDPE Teal Lid',
    specFa: 'ظرفیت ۳۰۰۰ میلی‌لیتر مناسب جراحی‌های پرحجم، قابلیت اتصال سری (Tandem)، فیلتر آنتی‌باکتریال و پودر ژل‌کننده',
    specEn: 'Wide-body 3000 mL high-capacity surgical liner, tandem cascade port, hydrophobic overflow valve & coagulant sachet',
    refImg: './assets/refs/p03-ref.png',
    callouts: [
      { label: 'Wide Ø130mm Teal Lid | درب عریض ۱۳۰ میلی‌متری', target: [0.02, 0.108, 0.01], offset: [0.10, 0.12, 0] },
      { label: 'Shut-Off Valve Housing | فیلتر قطع‌کن جریان', target: [0.0, 0.048, 0.0], offset: [-0.11, 0.055, 0] },
      { label: '3000 mL High-Volume Liner | کیسه حجیم ۳ لیتری', target: [0.056, -0.02, 0.0], offset: [0.11, -0.02, 0] },
      { label: 'High-Capacity Gelling Pad | ساشه ژل‌کننده قوی', target: [0.0, -0.105, 0.0], offset: [-0.10, -0.112, 0] },
    ]
  },
  {
    id: 'p04', code: 'ABD-GF-CORE', catId: 'cat-1-suction-bags',
    faName: 'پودر ژل‌کننده و فیلتر هیدروفوبیک کیسه ساکشن',
    enName: 'Superabsorbent Gelling Sachet & Hydrophobic Filter Core',
    dims: 'Filter Ø36 × 68 mm | Sachet 65 × 50 mm',
    material: 'Sintered UHMW-PE Hydrophobic Core + SAP Polymer Granules',
    specFa: 'ترکیب فیلتر هیدروفوبیک مسدودکننده مایعات و ساشه پودر سوپرجاذب جهت تبدیل سریع ترشحات به ژل نیمه‌جامد',
    specEn: 'Dual safety system: microporous hydrophobic filter plug stops backflow while SAP granules solidify up to 3000 mL fluid',
    refImg: './assets/refs/p04-ref.png',
    callouts: [
      { label: 'Slotted Teal Filter Cage | قفسه محافظ فیلتر', target: [-0.038, 0.035, 0.0], offset: [-0.11, 0.075, 0] },
      { label: 'Hydrophobic Sintered Core | مغزی هیدروفوبیک', target: [-0.038, -0.015, 0.0], offset: [-0.11, -0.03, 0] },
      { label: 'Water-Soluble SAP Sachet | ساشه پودر ژل‌کننده', target: [0.035, 0.005, 0.0], offset: [0.105, 0.045, 0] },
      { label: 'Active Gel Crystals | کریستال‌های سوپرجاذب', target: [0.042, -0.045, 0.015], offset: [0.105, -0.065, 0] },
    ]
  },
  {
    id: 'p05', code: 'ABD-CN-1230', catId: 'cat-2-canisters',
    faName: 'مخزن ساکشن پلی‌کربنات مدرج (۱، ۲ و ۳ لیتری)',
    enName: 'Reusable Graduated Polycarbonate Suction Canister',
    dims: 'Ø115–135 × 175–290 mm | 1000 / 2000 / 3000 mL',
    material: 'Autoclavable Optical-Grade Polycarbonate (PC) + Brass/Polymer Barb',
    specFa: 'بدنه شفاف و نشکن از جنس پلی‌کربنات گرید پزشکی با درجه‌بندی دقیق، قابلیت اتوکلاو و براکت نصب ریلی پشت مخزن',
    specEn: 'Shatter-resistant crystal-clear polycarbonate jar with precision mL scale, side vacuum hose barb & rear dovetail mount',
    refImg: './assets/refs/p05-ref.png',
    callouts: [
      { label: 'Top Rim Seal Collar | لبه آب‌بندی کیسه ساکشن', target: [0.052, 0.092, 0.0], offset: [0.105, 0.11, 0] },
      { label: 'Side Vacuum Hose Barb | نازل اتصال وکیوم بدنه', target: [0.062, 0.062, 0.0], offset: [0.11, 0.045, 0] },
      { label: 'Rear Dovetail Mount | شیار نگهدارنده پشت مخزن', target: [-0.058, 0.05, 0.0], offset: [-0.11, 0.06, 0] },
      { label: 'Clear PC Graduated Wall | بدنه شفاف مدرج پلی‌کربنات', target: [0.045, -0.035, 0.02], offset: [0.105, -0.055, 0] },
    ]
  },
  {
    id: 'p06', code: 'ABD-WS-UNIT', catId: 'cat-2-canisters',
    faName: 'پکیج کامل ساکشن دیواری بیمارستانی',
    enName: 'Complete Wall-Mounted Hospital Suction Assembly',
    dims: '280 × 160 × 340 mm | Complete Unit',
    material: 'PC Canister + PP Liner + Anodized Wall Rail Bracket + Regulator',
    specFa: 'مجموعه کامل شامل مخزن پلی‌کربنات، کیسه ساکشن یکبارمصرف، براکت دیواری، رگولاتور خلا، گیج و شلنگ رابط سیلیکونی',
    specEn: 'Integrated bedside suction station: wall bracket, vacuum regulator with gauge, silicone jumper hose, PC canister & liner',
    refImg: './assets/refs/p06-ref.png',
    callouts: [
      { label: 'Vacuum Gauge & Regulator | رگولاتور و گیج خلا', target: [-0.055, 0.075, 0.0], offset: [-0.115, 0.105, 0] },
      { label: 'Silicone Jumper Tube | شلنگ رابط سیلیکونی', target: [-0.015, 0.088, 0.0], offset: [0.095, 0.115, 0] },
      { label: 'Canister + Liner Assembly | مخزن و کیسه ساکشن', target: [0.032, -0.015, 0.02], offset: [0.11, -0.02, 0] },
      { label: 'Wall Slide Bracket | براکت نگهدارنده دیواری', target: [-0.045, -0.01, -0.02], offset: [-0.11, -0.045, 0] },
    ]
  },
  {
    id: 'p07', code: 'ABD-SC-0150', catId: 'cat-2-canisters',
    faName: 'ظرف جمع‌آوری نمونه ترشحات (Specimen Trap)',
    enName: 'Graduated Sputum & Specimen Collection Container',
    dims: 'Ø58 × 115 mm | 100–150 mL',
    material: 'Crystal Clear PS/PP Cup + Medical Teal Dual-Nozzle Cap',
    specFa: 'ظرف مدرج شفاف جهت نمونه‌گیری استریل ترشحات تنفسی و جراحی در مسیر خط ساکشن بدون تماس دست',
    specEn: 'Inline sterile specimen trap with dual angled stepped tubing nozzles, leak-proof screw cap & mL scale markings',
    refImg: './assets/refs/p07-ref.png',
    callouts: [
      { label: 'Dual Angled Tubing Nozzles | دو نازل زاویه‌دار ساکشن', target: [0.015, 0.085, 0.0], offset: [0.10, 0.105, 0] },
      { label: 'Ribbed Screw Cap | درب پیچی آب‌بند', target: [-0.038, 0.048, 0.0], offset: [-0.105, 0.06, 0] },
      { label: 'Internal Baffle Tube | لوله راهنمای داخلی', target: [0.0, 0.01, 0.0], offset: [-0.105, -0.005, 0] },
      { label: 'Graduated Clear Cup | مخزن شفاف مدرج نمونه', target: [0.032, -0.045, 0.01], offset: [0.10, -0.055, 0] },
    ]
  },
  {
    id: 'p08', code: 'ABD-FC-1000', catId: 'cat-2-canisters',
    faName: 'مخزن استریل جمع‌آوری و تزریق چربی (Lipo Collector)',
    enName: 'Sterile Autologous Fat Harvesting & Lipo Canister',
    dims: 'Ø115 × 220 mm | 1000 mL Sterile',
    material: 'Medical Grade PC + Multi-Port Teal Lid + Lower Luer Harvest Port',
    specFa: 'مخزن تخصصی استریل جهت جداسازی، شستشو و برداشت بافت چربی با پورت‌های چندگانه فوقانی و خروجی تحتانی لوئرلاک',
    specEn: 'Closed-system liposuction fat separation canister with internal decanting dip tube, multi-port lid & bottom extraction valve',
    refImg: './assets/refs/p08-ref.png',
    callouts: [
      { label: 'Multi-Port Harvesting Lid | درب چند پورت ورود و خلا', target: [0.02, 0.088, 0.0], offset: [0.105, 0.11, 0] },
      { label: 'Internal Decanting Tube | لوله جداسازی داخلی', target: [-0.015, 0.015, 0.0], offset: [-0.105, 0.03, 0] },
      { label: 'Conical Settling Base | کف مخروطی جداسازی چربی', target: [0.035, -0.055, 0.0], offset: [0.105, -0.05, 0] },
      { label: 'Lower Luer Extraction Port | پورت برداشت تحتانی', target: [0.025, -0.092, 0.02], offset: [-0.105, -0.095, 0] },
    ]
  },
  {
    id: 'p09', code: 'ABD-ST-2100', catId: 'cat-3-suction-tubes',
    faName: 'لوله رابط ساکشن پزشکی (Suction Connecting Tube)',
    enName: 'Medical PVC Suction Connecting Tube with Conical Ends',
    dims: 'ID 6.5 mm / OD 9.5 mm × L 1.8m / 2.1m / 3.0m',
    material: 'DEHP-Free Medical Grade Transparent PVC (Shore A 72)',
    specFa: 'لوله شفاف و انعطاف‌پذیر مقاوم در برابر کولاپس در فشار منفی بالا، مجهز به سرکانکتورهای مخروطی شیاردار استاندارد در دو سر',
    specEn: 'Collapse-resistant striated medical PVC tubing coils with universal ribbed female funnel connectors on both ends',
    refImg: './assets/refs/p09-ref.png',
    callouts: [
      { label: 'Universal Ribbed Funnel End | سرکانکتور مخروطی شیاردار', target: [-0.045, 0.055, 0.02], offset: [-0.11, 0.085, 0] },
      { label: 'Helical Coiled PVC Tubing | کلاف لوله PVC ضد تاخوردگی', target: [0.062, 0.01, 0.0], offset: [0.11, 0.03, 0] },
      { label: 'Thick Collapse-Proof Wall | دیواره مقاوم به خلا بالا', target: [-0.062, -0.025, 0.0], offset: [-0.11, -0.045, 0] },
      { label: 'Distal Conical Connector | کانکتور انتهایی استاندارد', target: [0.048, -0.055, 0.02], offset: [0.105, -0.075, 0] },
    ]
  },
  {
    id: 'p10', code: 'ABD-FT-0010', catId: 'cat-3-suction-tubes',
    faName: 'فینگر تیپ / رابط کنترل خلا ساکشن (Finger-Tip Adapter)',
    enName: 'Ergonomic Finger-Tip Vacuum Control Adapter',
    dims: 'L 72 mm | Stepped Ø5–11 mm Cones',
    material: 'Medical Grade PE/PP Copolymer (Teal / Translucent)',
    specFa: 'رابط ارگونومیک مجهز به دریچه انگشتی جهت کنترل لحظه‌ای و متناوب مکش توسط جراح یا پرستار',
    specEn: 'Inline thumb-vented suction control adapter with stepped barbed male cone & ribbed funnel female end',
    refImg: './assets/refs/p10-ref.png',
    callouts: [
      { label: 'Ergonomic Thumb Vent | دریچه کنترل انگشتی مکش', target: [0.0, 0.032, 0.0], offset: [0.0, 0.095, 0] },
      { label: 'Stepped Male Cone | سر مخروطی پله‌ای اتصال کاتتر', target: [0.058, 0.0, 0.0], offset: [0.11, 0.04, 0] },
      { label: 'Contoured Grip Body | بدنه ارگونومیک ضدلغزش', target: [-0.01, -0.005, 0.0], offset: [-0.105, -0.055, 0] },
      { label: 'Ribbed Tubing Socket | سوکت اتصال به لوله ساکشن', target: [-0.058, 0.0, 0.0], offset: [-0.11, 0.04, 0] },
    ]
  },
  {
    id: 'p11', code: 'ABD-FL-DISC', catId: 'cat-4-filters',
    faName: 'فیلتر آنتی‌باکتریال و هیدروفوبیک دیسکی (Disc Filter)',
    enName: 'Inline Antibacterial & Hydrophobic Disc Filter',
    dims: 'Ø64 mm Housing | Stepped Ø7–11 mm Barbs',
    material: 'Ultrasonic-Welded Clear ABS/PC Housing + 0.22µm PTFE Membrane',
    specFa: 'فیلتر دیسکی با غشای هیدروفوبیک ۰.۲۲ میکرون جهت حفاظت کامل پمپ و سیستم سانترال از ورود باکتری، ویروس و مایعات',
    specEn: '99.99% bacterial/viral retention PTFE hydrophobic membrane in welded transparent disc housing with stepped hose barbs',
    refImg: './assets/refs/p11-ref.png',
    callouts: [
      { label: 'Stepped Inlet Hose Barb | نازل پله‌ای ورودی', target: [-0.068, 0.0, 0.0], offset: [-0.115, 0.065, 0] },
      { label: 'Welded Radial Rib Housing | بدنه دیسکی تقویت‌شده', target: [0.0, 0.048, 0.0], offset: [0.095, 0.085, 0] },
      { label: '0.22µm PTFE Membrane | غشای هیدروفوبیک داخلی', target: [0.0, -0.01, 0.0], offset: [-0.105, -0.065, 0] },
      { label: 'Vacuum Pump Outlet Barb | نازل خروجی به سمت وکیوم', target: [0.068, 0.0, 0.0], offset: [0.115, -0.055, 0] },
    ]
  },
  {
    id: 'p12', code: 'ABD-FL-SHUT', catId: 'cat-4-filters',
    faName: 'فیلتر قطع‌کننده جریان مسدودشونده (Overflow Shut-Off Filter)',
    enName: 'Slotted Cage Overflow Shut-Off Valve & Filter Assembly',
    dims: 'Ø38 × 74 mm',
    material: 'Dark Teal Medical PP Cage + Expanding Hydrophobic Core',
    specFa: 'مجموعه قفسه شیاردار و مغزی حساس به رطوبت که به محض رسیدن سطح مایع به سقف مخزن، مسیر وکیوم را به صورت خودکار مسدود می‌کند',
    specEn: 'Snap-fit under-lid slotted guard cage housing a moisture-activated shut-off core that seals vacuum upon full liner level',
    refImg: './assets/refs/p12-ref.png',
    callouts: [
      { label: 'Snap-Fit Lid Boss | یقه اتصال به زیر درب کیسه', target: [0.0, 0.062, 0.0], offset: [0.10, 0.085, 0] },
      { label: '8-Rib Slotted Guard Cage | قفسه شیاردار محافظ', target: [-0.028, 0.01, 0.0], offset: [-0.105, 0.03, 0] },
      { label: 'Hydrophobic Shut-Off Plug | مغزی قطع‌کننده خودکار', target: [0.0, -0.01, 0.0], offset: [0.105, -0.015, 0] },
      { label: 'Bottom Retention Cap | درپوش نگهدارنده تحتانی', target: [0.0, -0.062, 0.0], offset: [-0.10, -0.075, 0] },
    ]
  },
  {
    id: 'p13', code: 'ABD-FL-SINT', catId: 'cat-4-filters',
    faName: 'فیلتر متخلخل پلی‌اتیلنی (Porous Sintered PE Filter)',
    enName: 'Microporous Sintered Polyethylene Filter Cylinder',
    dims: 'Ø18–26 × 38–52 mm | Pore Size 25–45 µm',
    material: 'Pure Sintered UHMW-PE + Self-Sealing Swell Polymer',
    specFa: 'استوانه متخلخل پلی‌اتیلنی با تخلخل یکنواخت جهت عبور آزاد هوا و انسداد فوری در برابر نفوذ کف، خون و ترشحات',
    specEn: 'Precision sintered microporous UHMW-PE cylinders in solid & tubular configurations for suction lids and regulators',
    refImg: './assets/refs/p13-ref.png',
    callouts: [
      { label: 'Flanged Top Shoulder | لبه پله‌ای آب‌بندی', target: [-0.028, 0.048, 0.0], offset: [-0.105, 0.075, 0] },
      { label: 'Microporous UHMW-PE Matrix | بافت متخلخل پلی‌اتیلنی', target: [-0.028, -0.005, 0.0], offset: [-0.105, -0.025, 0] },
      { label: 'Tubular Core Variant | نمونه استوانه‌ای توخالی', target: [0.032, 0.015, 0.0], offset: [0.105, 0.045, 0] },
      { label: 'High-Airflow Base | مقطع عبوردهنده جریان هوا', target: [0.032, -0.042, 0.0], offset: [0.105, -0.065, 0] },
    ]
  },
  {
    id: 'p14', code: 'ABD-TR-4CAN', catId: 'cat-5-stands-holders',
    faName: 'پایه ساکشن پرتابل ترولی ۴ مخزنه (Suction Trolley)',
    enName: 'Mobile 4-Canister Surgical Suction Stand & Trolley',
    dims: 'Base Ø560 mm × H 880 mm | 4 Canister Mounts',
    material: 'Stainless Steel / Chrome Column + 5-Star Antistatic Caster Base',
    specFa: 'پایه ترولی پرتابل ۵ چرخ ترمزدار با ستون استیل، دسته هدایت ارگونومیک و ۴ براکت نگهدارنده مخزن ساکشن جهت اتاق عمل',
    specEn: 'Heavy-duty 5-caster mobile OR stand with quad radial canister brackets, central manifold ring & 4 graduated canisters',
    refImg: './assets/refs/p14-ref.png',
    callouts: [
      { label: 'Quad Canister Ring Mount | نگهدارنده ۴ مخزن ساکشن', target: [0.035, 0.068, 0.02], offset: [0.105, 0.095, 0] },
      { label: 'Mounted Suction Canisters | مخازن ساکشن نصب‌شده', target: [-0.042, 0.055, 0.02], offset: [-0.11, 0.07, 0] },
      { label: 'Chrome Vertical Column | ستون عمودی استیل کروم', target: [0.0, -0.01, 0.0], offset: [0.105, -0.01, 0] },
      { label: '5-Star Locking Caster Base | پایه ۵ پر چرخ‌دار ترمزدار', target: [-0.055, -0.088, 0.02], offset: [-0.11, -0.095, 0] },
    ]
  },
  {
    id: 'p15', code: 'ABD-BR-WALL', catId: 'cat-5-stands-holders',
    faName: 'گیره و نگهدارنده دیواری مخزن ساکشن (Wall Bracket)',
    enName: 'Wall-Mount Slide Bracket for Suction Canisters',
    dims: '115 × 68 × 42 mm',
    material: 'High-Impact Reinforced Polymer / Anodized Aluminum Channel',
    specFa: 'براکت دیواری مقاوم با شیار استاندارد ذوزنقه‌ای جهت نصب سریع و ایمن مخازن ساکشن ۱، ۲ و ۳ لیتری بر روی دیوار بخش و اتاق عمل',
    specEn: 'Heavy-duty wall plate with precision dovetail slide channel, positive stop latch & countersunk mounting screw holes',
    refImg: './assets/refs/p15-ref.png',
    callouts: [
      { label: 'Dovetail Slide Guide Rails | ریل‌های راهنمای کشویی', target: [0.025, 0.035, 0.012], offset: [0.105, 0.065, 0] },
      { label: 'Countersunk Screw Holes | سوراخ‌های پیچ نصب دیواری', target: [-0.032, 0.042, 0.0], offset: [-0.105, 0.065, 0] },
      { label: 'Reinforced Backplate | صفحه پشتی تقویت‌شده', target: [-0.035, -0.02, 0.0], offset: [-0.105, -0.04, 0] },
      { label: 'Bottom Retention Stop | ضامن نگهدارنده انتهایی', target: [0.0, -0.052, 0.012], offset: [0.105, -0.065, 0] },
    ]
  },
  {
    id: 'p16', code: 'ABD-CL-REAR', catId: 'cat-5-stands-holders',
    faName: 'پشت گیره مخزن ساکشن پرتابل (Canister Rear Clip)',
    enName: 'Contoured Canister Rear Mounting Hanger Clip',
    dims: '88 × 54 × 24 mm',
    material: 'High-Strength Medical ABS / Polycarbonate (Teal / White)',
    specFa: 'قطعه رابط نصب‌شونده بر روی بدنه مخزن جهت آویز بر روی ریل دیواری، ترولی ساکشن یا تخت بیمارستان',
    specEn: 'Curved cradle adapter with tapered slide tongue that locks canisters securely into wall brackets or trolley rings',
    refImg: './assets/refs/p16-ref.png',
    callouts: [
      { label: 'Curved Canister Cradle | انحنای نشیمنگاه بدنه مخزن', target: [0.0, 0.045, -0.01], offset: [0.105, 0.075, 0] },
      { label: 'Tapered Slide Tongue | زبانه کشویی قفل‌شونده', target: [0.018, 0.005, 0.015], offset: [0.105, 0.005, 0] },
      { label: 'Structural Gusset Ribs | دنده‌های تقویتی پشت گیره', target: [-0.022, -0.01, 0.0], offset: [-0.105, 0.02, 0] },
      { label: 'Snap-Lock Release Tab | ضامن قفل و آزادسازی', target: [0.0, -0.048, 0.01], offset: [-0.105, -0.065, 0] },
    ]
  },
  {
    id: 'p17', code: 'ABD-CN-TEE', catId: 'cat-6-connectors-regulators',
    faName: 'اتصال T شکل ساکشن با درپوش (Tandem T-Connector)',
    enName: '3-Way Barbed T-Shape Tandem Suction Connector',
    dims: '68 × 48 mm | Ø8–11 mm Multi-Barb Arms',
    material: 'Medical PP / Nylon Body + Flexible Teal Sealing Cap',
    specFa: 'سه راهی شیاردار جهت اتصال سری (تاندم) چند مخزن ساکشن یا انشعاب خط وکیوم، مجهز به درپوش آب‌بندی پورت سوم',
    specEn: '3-way barbed tee union enabling series tandem canister connection or dual suction lines, with tethered teal seal cap',
    refImg: './assets/refs/p17-ref.png',
    callouts: [
      { label: 'Left Barbed Hose Arm | بازوی شیاردار اتصال شلنگ', target: [-0.052, 0.012, 0.0], offset: [-0.11, 0.055, 0] },
      { label: 'Right Barbed Hose Arm | بازوی خروجی وکیوم', target: [0.052, 0.012, 0.0], offset: [0.11, 0.055, 0] },
      { label: 'Vertical Canister Port | پورت عمودی اتصال مخزن', target: [0.0, -0.038, 0.0], offset: [-0.105, -0.055, 0] },
      { label: 'Tethered Teal Seal Plug | درپوش آب‌بند فیروزه‌ای', target: [0.025, 0.042, 0.0], offset: [0.105, -0.035, 0] },
    ]
  },
  {
    id: 'p18', code: 'ABD-CN-STR', catId: 'cat-6-connectors-regulators',
    faName: 'کانکتور رابط مستقیم دو سر مخروطی (Straight Connector)',
    enName: 'Symmetrical Double-Cone Stepped Straight Tubing Connector',
    dims: 'L 64 mm | Stepped Ø6–12 mm Barbs',
    material: 'Translucent / Teal Medical Polypropylene (PP)',
    specFa: 'رابط مستقیم دو سر پله‌ای (فشنگـی) با حلقه گریپ میانی جهت اتصال مطمئن دو لوله ساکشن با سایزهای مختلف',
    specEn: 'Universal 5-step barbed double-cone union with knurled center flange for joining medical suction tubing of varying IDs',
    refImg: './assets/refs/p18-ref.png',
    callouts: [
      { label: '5-Step Proximal Cone | مخروط ۵ پله‌ای سر اول', target: [-0.048, 0.0, 0.0], offset: [-0.11, 0.055, 0] },
      { label: 'Knurled Center Grip Ring | حلقه گریپ میانی', target: [0.0, 0.018, 0.0], offset: [0.0, 0.085, 0] },
      { label: '5-Step Distal Cone | مخروط ۵ پله‌ای سر دوم', target: [0.048, 0.0, 0.0], offset: [0.11, 0.055, 0] },
      { label: 'Smooth High-Flow Bore | مجرای داخلی بدون مانع', target: [0.02, -0.008, 0.0], offset: [0.105, -0.055, 0] },
    ]
  },
  {
    id: 'p19', code: 'ABD-SH-1307', catId: 'cat-6-connectors-regulators',
    faName: 'شلنگ سیلیکونی رابط ساکشن (Medical Silicone Hose)',
    enName: 'Thick-Walled Medical Platinum-Cured Silicone Jumper Hose',
    dims: 'OD 13 mm × ID 7 mm (Wall 3 mm)',
    material: '100% Platinum-Cured Medical Grade Translucent Silicone (Autoclavable)',
    specFa: 'شلنگ سیلیکونی ضخیم ۱۳×۷ میلی‌متر با تحمل خلا بالا بدون جمع‌شدگی، قابل اتوکلاو مکرر جهت اتصال رگولاتور به مخزن',
    specEn: 'Heavy-wall 13×7 mm autoclavable translucent silicone vacuum hose linking suction regulators and canister ports',
    refImg: './assets/refs/p19-ref.png',
    callouts: [
      { label: '3mm Thick Collapse-Proof Wall | دیواره ضخیم ۳ میلی‌متری', target: [-0.045, 0.042, 0.02], offset: [-0.11, 0.075, 0] },
      { label: 'Platinum-Cured Silicone | سیلیکون گرید پزشکی قابل اتوکلاو', target: [0.052, 0.015, 0.0], offset: [0.11, 0.045, 0] },
      { label: '7mm Smooth Inner Lumen | قطر داخلی ۷ میلی‌متری', target: [0.038, -0.045, 0.02], offset: [0.11, -0.065, 0] },
      { label: 'Flexible Kink-Free Loop | انعطاف‌پذیری بالا بدون شکستگی', target: [-0.048, -0.025, 0.0], offset: [-0.11, -0.055, 0] },
    ]
  },
  {
    id: 'p20', code: 'ABD-RG-VAC', catId: 'cat-6-connectors-regulators',
    faName: 'رگولاتور ساکشن پزشکی با گیج و مخزن محافظ (Vacuum Regulator)',
    enName: 'Medical Vacuum Suction Regulator with Gauge & Safety Trap',
    dims: '165 × 95 × 120 mm | 0 to -100 kPa (-760 mmHg)',
    material: 'Anodized Brass/Aluminum Body + Bourdon Gauge + PC Safety Jar',
    specFa: 'رگولاتور دقیق تنظیم فشار منفی سانترال با گیج عقربه‌ای رنگی، پیچ تنظیم نرم، شیر قطع سریع و مخزن تله ایمنی',
    specEn: 'Precision central vacuum regulator featuring color-coded 0 to -100 kPa dial gauge, control knob, shut-off switch & overflow trap',
    refImg: './assets/refs/p20-ref.png',
    callouts: [
      { label: '0 to -100 kPa Vacuum Gauge | گیج عقربه‌ای فشار منفی', target: [0.0, 0.062, 0.015], offset: [0.105, 0.095, 0] },
      { label: 'Fine Vacuum Control Knob | پیچ تنظیم دقیق مکش', target: [-0.032, 0.005, 0.025], offset: [-0.11, 0.035, 0] },
      { label: 'Safety Overflow Trap Jar | مخزن تله محافظ رگولاتور', target: [0.0, -0.058, 0.0], offset: [-0.105, -0.065, 0] },
      { label: 'Central Wall Probe & Barb | کانکتور سانترال و خروجی شلنگ', target: [0.038, -0.015, 0.0], offset: [0.11, -0.025, 0] },
    ]
  },
  {
    id: 'p21', code: 'ABD-VL-ONOF', catId: 'cat-6-connectors-regulators',
    faName: 'شیر قطع و وصل ساکشن (ON/OFF Vacuum Shut-Off Valve)',
    enName: 'Quarter-Turn Inline Vacuum ON/OFF Shut-Off Valve',
    dims: 'L 78 mm | G1/4" Thread × Ø9 mm Hose Barb',
    material: 'Chrome-Plated Brass Body + Ergonomic Teal Lever + PTFE Seal',
    specFa: 'شیر ربع‌گرد قطع و وصل سریع خط وکیوم بدون تغییر تنظیم فشار، مجهز به بدنه برنجی آبکاری‌شده و نازل شلنگ‌خور',
    specEn: 'Instant quarter-turn vacuum isolation valve with chrome-plated brass body, teal lever handle & barbed hose outlet',
    refImg: './assets/refs/p21-ref.png',
    callouts: [
      { label: 'Quarter-Turn Teal Lever | اهرم ربع‌گرد قطع و وصل', target: [0.008, 0.038, 0.0], offset: [0.095, 0.085, 0] },
      { label: 'Chrome-Plated Brass Body | بدنه برنجی آبکاری کروم', target: [-0.01, 0.0, 0.0], offset: [-0.105, 0.04, 0] },
      { label: 'Hex Thread Adapter | مهره شش‌ضلعی اتصال رگولاتور', target: [-0.048, 0.0, 0.0], offset: [-0.105, -0.05, 0] },
      { label: 'Ribbed Hose Barb | نازل شلنگ‌خور شیاردار', target: [0.052, 0.0, 0.0], offset: [0.105, -0.045, 0] },
    ]
  },
  {
    id: 'p22', code: 'ABD-KT-HOSE', catId: 'cat-6-connectors-regulators',
    faName: 'سری کامل شلنگ سیلیکونی و اتصالات مخزن (Hose & Fittings Kit)',
    enName: 'Complete Silicone Jumper Hose, T-Connector & Elbow Fittings Set',
    dims: 'Hose L 350 mm + T-Union + 90° Elbow Adapter',
    material: 'Medical Silicone Hose + PP/Brass Barbed Fittings',
    specFa: 'پکیج آماده نصب شامل شلنگ سیلیکونی رابط، سه راهی T شکل، زانویی ۹۰ درجه و سرشلنگی جهت اتصال سریع مخازن و رگولاتور',
    specEn: 'Ready-to-connect vacuum plumbing kit combining silicone jumper hose, barbed T-connector, 90° elbow & brass hose barb',
    refImg: './assets/refs/p22-ref.png',
    callouts: [
      { label: 'Silicone Jumper Arch | شلنگ رابط سیلیکونی', target: [0.0, 0.055, 0.0], offset: [0.095, 0.09, 0] },
      { label: 'Barbed T-Connector | سه راهی اتصال تاندم', target: [-0.052, -0.025, 0.0], offset: [-0.11, 0.015, 0] },
      { label: '90° Swivel Elbow Fitting | زانویی ۹۰ درجه مخزن', target: [0.052, -0.02, 0.0], offset: [0.11, 0.01, 0] },
      { label: 'Brass/Polymer Hose Nipples | سرشلنگی‌های آب‌بند', target: [0.01, -0.055, 0.015], offset: [-0.10, -0.075, 0] },
    ]
  },
  {
    id: 'p23', code: 'ABD-TB-SUCT', catId: 'cat-7-other-products',
    faName: 'مسواک ساکشن یکبارمصرف (Disposable Suction Toothbrush)',
    enName: 'Disposable Oral Care Suction Toothbrush with Foam Swab',
    dims: 'L 185 mm | Thumb-Control Hollow Lumen Handle',
    material: 'Medical PP Hollow Handle + Ultra-Soft Nylon Bristles + PU Foam Sponge',
    specFa: 'مسواک ساکشن ICU جهت بهداشت دهان بیماران اینتوبه و پیشگیری از پنومونی وابسته به ونتیلاتور (VAP) با دریچه کنترل مکش',
    specEn: 'ICU VAP-prevention oral care suction toothbrush combining ultra-soft bristles, ridged foam sponge back & thumb suction port',
    refImg: './assets/refs/p23-ref.png',
    callouts: [
      { label: 'Foam Swab & Soft Bristles | اسفنج شیاردار و برس نرم', target: [0.062, 0.015, 0.0], offset: [0.11, 0.065, 0] },
      { label: 'Suction Evacuation Aperture | منفذ مکش ترشحات دهان', target: [0.042, -0.005, 0.0], offset: [0.11, -0.045, 0] },
      { label: 'Thumb Vacuum Control Port | دریچه انگشتی کنترل مکش', target: [-0.018, 0.012, 0.0], offset: [-0.10, 0.065, 0] },
      { label: 'Stepped Suction Tube Barb | سر پله‌ای اتصال به لوله ساکشن', target: [-0.072, 0.0, 0.0], offset: [-0.11, -0.05, 0] },
    ]
  },
  {
    id: 'p24', code: 'ABD-ET-HOLD', catId: 'cat-7-other-products',
    faName: 'نگهدارنده لوله تراشه (Endotracheal Tube Holder)',
    enName: 'Quick-Lock Endotracheal Tube Holder with Bite Block',
    dims: 'Arch W 125 mm | Fits ETT 6.5–10.0 mm',
    material: 'Medical Grade PP Arch + Soft Cheek Pads + Velcro Headband',
    specFa: 'تثبیت‌کننده ایمن لوله تراشه بدون نیاز به چسب، دارای بایت‌بلاک محافظ دندان، پیچ قفل سریع و پورت دسترسی ساکشن دهانی',
    specEn: 'Adhesive-free ergonomic ETT stabilizer featuring integral bite block, quick-turn locking clamp, oral suction port & padded strap',
    refImg: './assets/refs/p24-ref.png',
    callouts: [
      { label: 'Quick-Turn ETT Clamp Screw | پیچ تثبیت سریع لوله تراشه', target: [0.0, 0.032, 0.028], offset: [0.105, 0.075, 0] },
      { label: 'Integral Bite Block Tunnel | کانال بایت‌بلاک محافظ', target: [0.0, -0.008, 0.015], offset: [-0.105, 0.055, 0] },
      { label: 'Anatomical Arch Faceplate | کمان آناتومیک روی صورت', target: [0.048, 0.0, 0.0], offset: [0.11, -0.045, 0] },
      { label: 'Soft Padded Neck Strap | بند نرم دور سر و گردن', target: [-0.052, -0.01, -0.025], offset: [-0.11, -0.055, 0] },
    ]
  },
  {
    id: 'p25', code: 'ABD-OR-RCVR', catId: 'cat-7-other-products',
    faName: 'رسیور پزشکی ۶۰۰ سی‌سی و مکش سطحی (Kidney Basin & Splash-Vac)',
    enName: '600cc Graduated Medical Kidney Basin & Floor Splash-Vac Dome',
    dims: 'Basin 210 × 115 × 48 mm (600cc) | Splash-Vac Ø145 mm',
    material: 'Medical Polypropylene (PP) + Weighted Flexible Elastomer Dome',
    specFa: 'ظرف رسیور لوبیایی ۶۰۰ سی‌سی مدرج به همراه دیسک مکش سطحی Splash-Vac جهت جمع‌آوری سریع مایعات از سطح زمین اتاق عمل',
    specEn: 'Graduated 600cc polypropylene emesis kidney dish paired with weighted multi-nozzle OR floor fluid evacuation dome',
    refImg: './assets/refs/p25-ref.png',
    callouts: [
      { label: '600cc Kidney Receiver Basin | رسیور لوبیایی مدرج ۶۰۰cc', target: [-0.038, 0.018, 0.0], offset: [-0.11, 0.065, 0] },
      { label: 'Rolled Pouring Lip | لبه برگشتی ضدریزش', target: [-0.068, 0.028, 0.02], offset: [-0.11, -0.045, 0] },
      { label: 'Splash-Vac Suction Dome | دیسک مکش سطحی اتاق عمل', target: [0.045, -0.015, 0.01], offset: [0.11, 0.055, 0] },
      { label: 'Perimeter Suction Slots & Barb | منافذ مکش محیطی و نازل', target: [0.045, 0.015, 0.01], offset: [0.11, -0.055, 0] },
    ]
  }
];

let _cachedTex = null;
function getSharedTextures(THREE) {
  if (_cachedTex) return _cachedTex;
  const size = 256;
  const bumpCanvas = document.createElement('canvas');
  bumpCanvas.width = bumpCanvas.height = size;
  const bctx = bumpCanvas.getContext('2d');
  const img = bctx.createImageData(size, size);
  let seed = 4242;
  for (let i = 0; i < img.data.length; i += 4) {
    seed = (seed * 16807) % 2147483647;
    const v = 120 + ((seed & 63));
    img.data[i] = img.data[i+1] = img.data[i+2] = v;
    img.data[i+3] = 255;
  }
  bctx.putImageData(img, 0, 0);
  const bumpTex = new THREE.CanvasTexture(bumpCanvas);
  bumpTex.wrapS = bumpTex.wrapT = THREE.RepeatWrapping;
  bumpTex.repeat.set(5, 4);

  const makeScale = (maxMl, stepsCount, colorStr = 'rgba(15, 95, 98, 0.78)') => {
    const c = document.createElement('canvas');
    c.width = 512; c.height = 512;
    const g = c.getContext('2d');
    g.strokeStyle = colorStr;
    g.fillStyle = colorStr;
    g.lineWidth = 3;
    g.font = 'bold 20px Arial, sans-serif';
    const gx = 150;
    g.beginPath(); g.moveTo(gx, 55); g.lineTo(gx, 455); g.stroke();
    for (let i = 0; i <= stepsCount; i++) {
      const y = 450 - (i / stepsCount) * 390;
      const major = i % 2 === 0;
      const w = major ? 30 : 16;
      g.beginPath(); g.moveTo(gx - w/2, y); g.lineTo(gx + w/2, y); g.stroke();
      if (major && i > 0) {
        const ml = Math.round((i / stepsCount) * maxMl);
        g.fillText(`${ml} ml`, gx + 20, y + 7);
      }
    }
    const t = new THREE.CanvasTexture(c);
    t.colorSpace = THREE.SRGBColorSpace;
    return t;
  };

  // Gauge dial texture for Vacuum Regulator
  const dialCanvas = document.createElement('canvas');
  dialCanvas.width = dialCanvas.height = 256;
  const dctx = dialCanvas.getContext('2d');
  dctx.fillStyle = '#f8fbfb';
  dctx.beginPath(); dctx.arc(128, 128, 118, 0, Math.PI * 2); dctx.fill();
  dctx.lineWidth = 10;
  dctx.strokeStyle = '#18a66b'; dctx.beginPath(); dctx.arc(128, 128, 96, Math.PI*0.75, Math.PI*1.35); dctx.stroke();
  dctx.strokeStyle = '#e5a000'; dctx.beginPath(); dctx.arc(128, 128, 96, Math.PI*1.35, Math.PI*1.85); dctx.stroke();
  dctx.strokeStyle = '#d9383a'; dctx.beginPath(); dctx.arc(128, 128, 96, Math.PI*1.85, Math.PI*2.25); dctx.stroke();
  dctx.strokeStyle = '#0e3538'; dctx.lineWidth = 2.5;
  for (let i = 0; i <= 10; i++) {
    const a = Math.PI * 0.75 + (i / 10) * Math.PI * 1.5;
    dctx.beginPath();
    dctx.moveTo(128 + Math.cos(a)*78, 128 + Math.sin(a)*78);
    dctx.lineTo(128 + Math.cos(a)*104, 128 + Math.sin(a)*104);
    dctx.stroke();
  }
  dctx.fillStyle = '#072a2c'; dctx.font = 'bold 20px Arial'; dctx.textAlign = 'center';
  dctx.fillText('-100 kPa', 128, 178);
  dctx.fillText('VACUUM', 128, 202);
  // Needle
  dctx.strokeStyle = '#d12626'; dctx.lineWidth = 4;
  dctx.beginPath(); dctx.moveTo(128, 128); dctx.lineTo(68, 78); dctx.stroke();
  dctx.fillStyle = '#05686b'; dctx.beginPath(); dctx.arc(128, 128, 10, 0, Math.PI*2); dctx.fill();
  const dialTex = new THREE.CanvasTexture(dialCanvas);
  dialTex.colorSpace = THREE.SRGBColorSpace;

  _cachedTex = {
    bumpTex,
    scale1000: makeScale(1000, 10, 'rgba(235, 252, 252, 0.78)'),
    scale2000: makeScale(2000, 10, 'rgba(235, 252, 252, 0.78)'),
    scale3000: makeScale(3000, 12, 'rgba(235, 252, 252, 0.78)'),
    scalePC: makeScale(2000, 10, 'rgba(5, 95, 100, 0.85)'),
    scale150: makeScale(150, 6, 'rgba(5, 95, 100, 0.85)'),
    dialTex,
  };
  return _cachedTex;
}

function makeMats(THREE, isCad, isDark) {
  const { bumpTex } = getSharedTextures(THREE);
  const edgeColor = isDark ? 0x3ce8ea : 0x046669;
  const edgeSubtle = isDark ? 0x229ea0 : 0x167c80;
  const cadEdgeMat = new THREE.LineBasicMaterial({
    color: edgeColor, transparent: true, opacity: isCad ? 0.88 : 0.24
  });
  const cadGridMat = new THREE.LineBasicMaterial({
    color: edgeSubtle, transparent: true, opacity: isCad ? 0.62 : 0.14
  });

  const tealLid = new THREE.MeshPhysicalMaterial({
    color: 0x05686b, roughness: 0.32, metalness: 0.05, clearcoat: 0.30,
    transparent: isCad, opacity: isCad ? (isDark ? 0.38 : 0.30) : 1.0, side: THREE.DoubleSide
  });
  const darkTeal = new THREE.MeshPhysicalMaterial({
    color: 0x034447, roughness: 0.36, metalness: 0.06, clearcoat: 0.20,
    transparent: isCad, opacity: isCad ? 0.48 : 1.0, side: THREE.DoubleSide
  });
  const lightTeal = new THREE.MeshPhysicalMaterial({
    color: 0x129296, roughness: 0.30, metalness: 0.04, clearcoat: 0.25,
    transparent: isCad, opacity: isCad ? 0.42 : 1.0, side: THREE.DoubleSide
  });
  const frostedBag = new THREE.MeshPhysicalMaterial({
    color: isDark ? 0xd9f2f2 : 0xeef7f7,
    roughness: 0.40, metalness: 0.0, transmission: isCad ? 0.15 : 0.38,
    transparent: true, opacity: isCad ? 0.20 : (isDark ? 0.52 : 0.56),
    bumpMap: bumpTex, bumpScale: 0.0005, clearcoat: 0.18, side: THREE.DoubleSide, depthWrite: false
  });
  const clearPC = new THREE.MeshPhysicalMaterial({
    color: isDark ? 0xd5f4f7 : 0xf0fbfc,
    roughness: 0.14, metalness: 0.02, transmission: isCad ? 0.15 : 0.52,
    transparent: true, opacity: isCad ? 0.22 : (isDark ? 0.44 : 0.46),
    clearcoat: 0.65, side: THREE.DoubleSide, depthWrite: false
  });
  const siliconeMat = new THREE.MeshPhysicalMaterial({
    color: 0xdff6f6, roughness: 0.26, metalness: 0.0,
    transparent: true, opacity: isCad ? 0.30 : 0.72, clearcoat: 0.35, side: THREE.DoubleSide
  });
  const whitePorous = new THREE.MeshStandardMaterial({
    color: 0xf4f9f9, roughness: 0.62, metalness: 0.02,
    transparent: isCad, opacity: isCad ? 0.55 : 1.0, side: THREE.DoubleSide
  });
  const chromeMetal = new THREE.MeshStandardMaterial({
    color: isDark ? 0xd0e2e5 : 0xdce7e9, roughness: 0.22, metalness: 0.78,
    transparent: isCad, opacity: isCad ? 0.45 : 1.0, side: THREE.DoubleSide
  });
  const brassMetal = new THREE.MeshStandardMaterial({
    color: 0xd4a843, roughness: 0.28, metalness: 0.72,
    transparent: isCad, opacity: isCad ? 0.50 : 1.0, side: THREE.DoubleSide
  });
  const darkPolymer = new THREE.MeshStandardMaterial({
    color: 0x1c2b2d, roughness: 0.42, metalness: 0.15,
    transparent: isCad, opacity: isCad ? 0.48 : 1.0
  });
  const foamPink = new THREE.MeshStandardMaterial({
    color: 0x3ec6c9, roughness: 0.68, metalness: 0.0,
    transparent: isCad, opacity: isCad ? 0.45 : 1.0
  });

  return {
    tealLid, darkTeal, lightTeal, frostedBag, clearPC, siliconeMat,
    whitePorous, chromeMetal, brassMetal, darkPolymer, foamPink,
    cadEdgeMat, cadGridMat
  };
}

function addMesh(THREE, parent, geo, mat, edgeMat, threshold = 18) {
  const m = new THREE.Mesh(geo, mat);
  if (edgeMat) {
    const eg = new THREE.EdgesGeometry(geo, threshold);
    const lines = new THREE.LineSegments(eg, edgeMat);
    m.add(lines);
  }
  parent.add(m);
  return m;
}

function buildSteppedLidAndBag(THREE, group, mats, cfg) {
  const { rTop, rBot, hBag, scaleTex, hasTandem } = cfg;
  const yTop = hBag * 0.46;
  const yBot = -hBag * 0.54;

  // Tapered Frosted Liner Body
  const pts = [
    new THREE.Vector2(0, yBot),
    new THREE.Vector2(rBot * 0.92, yBot),
    new THREE.Vector2(rBot, yBot + 0.006),
    new THREE.Vector2(rTop, yTop - 0.012),
    new THREE.Vector2(rTop * 1.03, yTop - 0.008),
    new THREE.Vector2(rTop * 1.03, yTop),
  ];
  const bagGeo = new THREE.LatheGeometry(pts, 48);
  const bagMesh = addMesh(THREE, group, bagGeo, mats.frostedBag, mats.cadGridMat, 12);
  bagMesh.renderOrder = 3;

  // Scale label cylinder
  const scGeo = new THREE.CylinderGeometry(rTop * 0.995, rBot * 1.002, (yTop - yBot) * 0.82, 40, 1, true);
  scGeo.translate(0, (yTop + yBot) * 0.5, 0);
  const scMat = new THREE.MeshBasicMaterial({ map: scaleTex, transparent: true, opacity: 0.82, depthWrite: false });
  const scMesh = new THREE.Mesh(scGeo, scMat);
  scMesh.renderOrder = 4;
  group.add(scMesh);

  // Internal Shut-Off Filter Cage
  const cageG = new THREE.Group();
  cageG.position.set(0, yTop - 0.042, 0);
  addMesh(THREE, cageG, new THREE.CylinderGeometry(0.017, 0.019, 0.056, 28), mats.darkTeal, mats.cadEdgeMat);
  addMesh(THREE, cageG, new THREE.CylinderGeometry(0.0135, 0.0145, 0.046, 24), mats.whitePorous, null);
  for (let i = 0; i < 8; i++) {
    const a = (i / 8) * Math.PI * 2;
    const rib = new THREE.BoxGeometry(0.0024, 0.052, 0.0035);
    rib.translate(0, 0, 0.0175);
    rib.rotateY(a);
    addMesh(THREE, cageG, rib, mats.darkTeal, null);
  }
  group.add(cageG);

  // Bottom Coagulant Pad
  const padGeo = new THREE.BoxGeometry(rBot * 1.05, 0.014, rBot * 0.85, 8, 2, 8);
  padGeo.translate(0, yBot + 0.012, 0);
  addMesh(THREE, group, padGeo, mats.whitePorous, mats.cadEdgeMat);

  // Stepped Teal Lid
  const lidG = new THREE.Group();
  lidG.position.set(0, yTop, 0);
  addMesh(THREE, lidG, new THREE.CylinderGeometry(rTop * 1.06, rTop * 1.06, 0.010, 48), mats.tealLid, mats.cadEdgeMat);
  addMesh(THREE, lidG, new THREE.CylinderGeometry(rTop * 0.96, rTop * 1.01, 0.012, 48).translate(0, 0.009, 0), mats.tealLid, mats.cadEdgeMat);
  // Crescent recess
  addMesh(THREE, lidG, new THREE.CylinderGeometry(rTop * 0.46, rTop * 0.44, 0.008, 32, 1, false, 0, Math.PI * 1.15).translate(0.008, 0.012, 0.006), mats.darkTeal, mats.cadEdgeMat);

  // Two 45° Angled Ports (Patient & Vacuum)
  for (const [px, pz, rz] of [[-0.018, 0.016, 0.62], [0.018, -0.014, -0.62]]) {
    const pG = new THREE.Group();
    pG.position.set(px, 0.012, pz);
    pG.rotation.z = rz;
    addMesh(THREE, pG, new THREE.CylinderGeometry(0.0055, 0.0070, 0.032, 24).translate(0, 0.016, 0), mats.tealLid, mats.cadEdgeMat);
    addMesh(THREE, pG, new THREE.TorusGeometry(0.0056, 0.0011, 10, 24).rotateX(Math.PI/2).translate(0, 0.032, 0), mats.lightTeal, null);
    lidG.add(pG);
  }
  // Auxiliary / Tandem Port
  if (hasTandem) {
    addMesh(THREE, lidG, new THREE.CylinderGeometry(0.007, 0.008, 0.022, 24).translate(-0.022, 0.020, -0.022), mats.lightTeal, mats.cadEdgeMat);
  }
  // Left Tether Loop + Cap
  const loopCurve = new THREE.CatmullRomCurve3([
    new THREE.Vector3(-rTop * 1.04, 0.004, 0.015),
    new THREE.Vector3(-rTop * 1.42, 0.002, 0.022),
    new THREE.Vector3(-rTop * 1.48, 0.001, -0.005),
    new THREE.Vector3(-rTop * 1.04, 0.003, -0.012),
  ]);
  addMesh(THREE, lidG, new THREE.TubeGeometry(loopCurve, 36, 0.0016, 10, false), mats.lightTeal, mats.cadEdgeMat);
  addMesh(THREE, lidG, new THREE.CylinderGeometry(0.0065, 0.0065, 0.008, 20).translate(-rTop * 1.44, 0.003, 0.008), mats.tealLid, mats.cadEdgeMat);

  group.add(lidG);
}

export function buildProductModel(THREE, productId, options = {}) {
  const isCad = !!options.isCad;
  const isDark = !!options.isDark;
  const mats = makeMats(THREE, isCad, isDark);
  const tex = getSharedTextures(THREE);
  const root = new THREE.Group();
  root.name = `Product_${productId}`;

  switch (productId) {
    case 'p01':
      buildSteppedLidAndBag(THREE, root, mats, { rTop: 0.056, rBot: 0.045, hBag: 0.165, scaleTex: tex.scale1000, hasTandem: true });
      break;
    case 'p02':
      buildSteppedLidAndBag(THREE, root, mats, { rTop: 0.054, rBot: 0.043, hBag: 0.205, scaleTex: tex.scale2000, hasTandem: true });
      break;
    case 'p03':
      buildSteppedLidAndBag(THREE, root, mats, { rTop: 0.064, rBot: 0.052, hBag: 0.212, scaleTex: tex.scale3000, hasTandem: true });
      break;

    case 'p04': {
      // Left: Hydrophobic Shut-Off Filter Assembly; Right: Gelling Powder Sachet + Granules
      const fG = new THREE.Group(); fG.position.set(-0.042, 0.01, 0);
      addMesh(THREE, fG, new THREE.CylinderGeometry(0.024, 0.022, 0.016, 32).translate(0, 0.042, 0), mats.darkTeal, mats.cadEdgeMat);
      addMesh(THREE, fG, new THREE.CylinderGeometry(0.019, 0.021, 0.068, 32), mats.tealLid, mats.cadEdgeMat);
      addMesh(THREE, fG, new THREE.CylinderGeometry(0.015, 0.016, 0.058, 28), mats.whitePorous, mats.cadGridMat);
      for (let i = 0; i < 8; i++) {
        const a = (i/8)*Math.PI*2;
        addMesh(THREE, fG, new THREE.BoxGeometry(0.003, 0.062, 0.004).translate(0, 0, 0.020).rotateY(a), mats.darkTeal, null);
      }
      root.add(fG);

      const sG = new THREE.Group(); sG.position.set(0.038, 0.005, 0); sG.rotation.set(0.25, -0.25, 0.12);
      addMesh(THREE, sG, new THREE.BoxGeometry(0.062, 0.020, 0.050, 12, 4, 12), mats.whitePorous, mats.cadEdgeMat);
      addMesh(THREE, sG, new THREE.BoxGeometry(0.070, 0.002, 0.058), mats.siliconeMat, mats.cadEdgeMat);
      root.add(sG);
      // Gel crystals cluster
      for (let i = 0; i < 14; i++) {
        const a = i * 0.9; const r = 0.012 + (i % 4) * 0.008;
        addMesh(THREE, root, new THREE.DodecahedronGeometry(0.0055).translate(0.038 + Math.cos(a)*r, -0.048 + (i%3)*0.006, Math.sin(a)*r), mats.lightTeal, mats.cadEdgeMat);
      }
      break;
    }

    case 'p05': {
      // Reusable Graduated Polycarbonate Canister
      addMesh(THREE, root, new THREE.CylinderGeometry(0.060, 0.050, 0.195, 48, 1, false), mats.clearPC, mats.cadEdgeMat);
      addMesh(THREE, root, new THREE.TorusGeometry(0.060, 0.0035, 14, 48).rotateX(Math.PI/2).translate(0, 0.097, 0), mats.clearPC, mats.cadEdgeMat);
      const sc = new THREE.Mesh(new THREE.CylinderGeometry(0.0605, 0.0505, 0.165, 40, 1, true), new THREE.MeshBasicMaterial({ map: tex.scalePC, transparent: true, depthWrite: false }));
      root.add(sc);
      // Rear dovetail bracket mount
      addMesh(THREE, root, new THREE.BoxGeometry(0.014, 0.058, 0.032).translate(-0.062, 0.045, 0), mats.tealLid, mats.cadEdgeMat);
      // Side brass/polymer vacuum barb
      addMesh(THREE, root, new THREE.CylinderGeometry(0.006, 0.008, 0.028, 20).rotateZ(-Math.PI/2).translate(0.068, 0.062, 0), mats.brassMetal, mats.cadEdgeMat);
      break;
    }

    case 'p06': {
      // Wall Suction Unit (Canister + Liner + Wall Bracket + Regulator + Jumper Tube)
      const cG = new THREE.Group(); cG.position.set(0.032, -0.015, 0);
      buildSteppedLidAndBag(THREE, cG, mats, { rTop: 0.046, rBot: 0.038, hBag: 0.150, scaleTex: tex.scale1000, hasTandem: false });
      addMesh(THREE, cG, new THREE.CylinderGeometry(0.050, 0.042, 0.155, 40).translate(0, -0.008, 0), mats.clearPC, mats.cadEdgeMat);
      root.add(cG);
      // Wall bracket & rail
      addMesh(THREE, root, new THREE.BoxGeometry(0.028, 0.11, 0.018).translate(-0.022, -0.01, -0.028), mats.chromeMetal, mats.cadEdgeMat);
      // Regulator & Gauge on left
      const rG = new THREE.Group(); rG.position.set(-0.055, 0.045, 0);
      addMesh(THREE, rG, new THREE.CylinderGeometry(0.018, 0.018, 0.048, 28), mats.chromeMetal, mats.cadEdgeMat);
      addMesh(THREE, rG, new THREE.CylinderGeometry(0.026, 0.026, 0.012, 32).rotateX(Math.PI/2).translate(0, 0.032, 0.010), mats.darkPolymer, mats.cadEdgeMat);
      const dFace = new THREE.Mesh(new THREE.CircleGeometry(0.023, 32), new THREE.MeshBasicMaterial({ map: tex.dialTex }));
      dFace.position.set(0, 0.032, 0.017); rG.add(dFace);
      addMesh(THREE, rG, new THREE.CylinderGeometry(0.011, 0.011, 0.018, 20).rotateX(Math.PI/2).translate(0, -0.005, 0.020), mats.tealLid, mats.cadEdgeMat);
      root.add(rG);
      // Silicone jumper curve
      const jCurve = new THREE.CatmullRomCurve3([
        new THREE.Vector3(-0.055, 0.020, 0),
        new THREE.Vector3(-0.035, 0.095, 0.015),
        new THREE.Vector3(0.018, 0.095, 0.010),
        new THREE.Vector3(0.032, 0.072, 0.008),
      ]);
      addMesh(THREE, root, new THREE.TubeGeometry(jCurve, 36, 0.0048, 12, false), mats.siliconeMat, mats.cadEdgeMat);
      break;
    }

    case 'p07': {
      // Specimen Collection Container
      addMesh(THREE, root, new THREE.CylinderGeometry(0.042, 0.034, 0.135, 40), mats.clearPC, mats.cadEdgeMat);
      const sc7 = new THREE.Mesh(new THREE.CylinderGeometry(0.0425, 0.0345, 0.11, 36, 1, true), new THREE.MeshBasicMaterial({ map: tex.scale150, transparent: true, depthWrite: false }));
      root.add(sc7);
      // Ribbed Teal Cap
      addMesh(THREE, root, new THREE.CylinderGeometry(0.045, 0.045, 0.024, 36).translate(0, 0.072, 0), mats.tealLid, mats.cadEdgeMat);
      // Internal dip tube
      addMesh(THREE, root, new THREE.CylinderGeometry(0.0045, 0.0045, 0.075, 16).translate(-0.012, 0.030, 0), mats.siliconeMat, mats.cadEdgeMat);
      // Two stepped top nozzles
      for (const [nx, rz] of [[-0.014, 0.35], [0.014, -0.35]]) {
        const nG = new THREE.Group(); nG.position.set(nx, 0.082, 0); nG.rotation.z = rz;
        addMesh(THREE, nG, new THREE.CylinderGeometry(0.004, 0.007, 0.036, 20).translate(0, 0.018, 0), mats.tealLid, mats.cadEdgeMat);
        root.add(nG);
      }
      break;
    }

    case 'p08': {
      // Autologous Fat Collection Canister (Lipo Collector)
      addMesh(THREE, root, new THREE.CylinderGeometry(0.054, 0.050, 0.155, 44).translate(0, 0.012, 0), mats.clearPC, mats.cadEdgeMat);
      // Conical settling bottom
      addMesh(THREE, root, new THREE.CylinderGeometry(0.050, 0.012, 0.038, 44).translate(0, -0.084, 0), mats.clearPC, mats.cadEdgeMat);
      // Multi-port Teal Lid
      addMesh(THREE, root, new THREE.CylinderGeometry(0.057, 0.057, 0.018, 44).translate(0, 0.092, 0), mats.tealLid, mats.cadEdgeMat);
      for (const px of [-0.026, 0.0, 0.026]) {
        addMesh(THREE, root, new THREE.CylinderGeometry(0.005, 0.007, 0.028, 20).translate(px, 0.112, 0), mats.lightTeal, mats.cadEdgeMat);
      }
      // Internal decanting dip tube
      addMesh(THREE, root, new THREE.CylinderGeometry(0.004, 0.004, 0.155, 16).translate(-0.018, 0.005, 0), mats.chromeMetal, mats.cadEdgeMat);
      // Lower Luer extraction port
      addMesh(THREE, root, new THREE.CylinderGeometry(0.005, 0.006, 0.028, 18).rotateZ(Math.PI/2).translate(0.024, -0.092, 0), mats.tealLid, mats.cadEdgeMat);
      break;
    }

    case 'p09': {
      // Medical PVC Suction Connecting Tube (Coiled Helix + 2 Ribbed Funnel Ends)
      const pts = [];
      const turns = 4.2;
      for (let i = 0; i <= 140; i++) {
        const t = i / 140;
        const a = t * turns * Math.PI * 2;
        const r = 0.068 + Math.sin(t * Math.PI) * 0.006;
        const y = (t - 0.5) * 0.075;
        pts.push(new THREE.Vector3(Math.cos(a) * r, y, Math.sin(a) * r));
      }
      const coilCurve = new THREE.CatmullRomCurve3(pts);
      addMesh(THREE, root, new THREE.TubeGeometry(coilCurve, 160, 0.0052, 14, false), mats.clearPC, mats.cadEdgeMat);
      // Ribbed Universal Conical Female Ends
      for (const [ex, ey, ez, rz] of [[-0.055, 0.058, 0.025, 0.5], [0.055, -0.058, -0.025, -0.5]]) {
        const cG = new THREE.Group(); cG.position.set(ex, ey, ez); cG.rotation.z = rz;
        addMesh(THREE, cG, new THREE.CylinderGeometry(0.011, 0.006, 0.038, 24), mats.tealLid, mats.cadEdgeMat);
        for (let r = -1; r <= 1; r++) {
          addMesh(THREE, cG, new THREE.TorusGeometry(0.0085 + r*0.0012, 0.0014, 10, 24).rotateX(Math.PI/2).translate(0, r*0.009, 0), mats.lightTeal, null);
        }
        root.add(cG);
      }
      break;
    }

    case 'p10': {
      // Finger-Tip Vacuum Control Adapter
      const fG = new THREE.Group();
      // Main horizontal body
      addMesh(THREE, fG, new THREE.CylinderGeometry(0.012, 0.012, 0.065, 28).rotateZ(Math.PI/2), mats.tealLid, mats.cadEdgeMat);
      // Stepped male cone on right
      for (let s = 0; s < 4; s++) {
        const r1 = 0.0095 - s * 0.0014;
        const r2 = 0.0082 - s * 0.0014;
        addMesh(THREE, fG, new THREE.CylinderGeometry(r2, r1, 0.014, 24).rotateZ(-Math.PI/2).translate(0.038 + s*0.012, 0, 0), mats.lightTeal, mats.cadEdgeMat);
      }
      // Ribbed female funnel on left
      addMesh(THREE, fG, new THREE.CylinderGeometry(0.015, 0.011, 0.042, 24).rotateZ(Math.PI/2).translate(-0.052, 0, 0), mats.tealLid, mats.cadEdgeMat);
      // Angled ergonomic thumb-vent chimney on top
      const vG = new THREE.Group(); vG.position.set(-0.004, 0.018, 0); vG.rotation.z = -0.22;
      addMesh(THREE, vG, new THREE.CylinderGeometry(0.013, 0.010, 0.028, 24), mats.whitePorous, mats.cadEdgeMat);
      addMesh(THREE, vG, new THREE.TorusGeometry(0.0125, 0.0022, 12, 24).rotateX(Math.PI/2).translate(0, 0.014, 0), mats.tealLid, mats.cadEdgeMat);
      fG.add(vG);
      root.add(fG);
      break;
    }

    case 'p11': {
      // Antibacterial Disc Filter
      const dG = new THREE.Group();
      // Circular disc housing facing camera at slight angle
      dG.rotation.y = 0.35; dG.rotation.x = 0.20;
      addMesh(THREE, dG, new THREE.CylinderGeometry(0.056, 0.056, 0.016, 48).rotateX(Math.PI/2), mats.clearPC, mats.cadEdgeMat);
      addMesh(THREE, dG, new THREE.TorusGeometry(0.056, 0.0035, 14, 48), mats.tealLid, mats.cadEdgeMat);
      // Internal hydrophobic PTFE membrane disc
      addMesh(THREE, dG, new THREE.CylinderGeometry(0.048, 0.048, 0.004, 40).rotateX(Math.PI/2), mats.whitePorous, mats.cadGridMat);
      // Radial support ribs
      for (let i = 0; i < 8; i++) {
        const a = (i / 8) * Math.PI * 2;
        addMesh(THREE, dG, new THREE.BoxGeometry(0.0025, 0.096, 0.018).rotateZ(a), mats.clearPC, null);
      }
      // Left & Right Stepped Hose Barbs
      for (const dir of [-1, 1]) {
        for (let s = 0; s < 3; s++) {
          const r = 0.009 - s * 0.0015;
          addMesh(THREE, dG, new THREE.CylinderGeometry(r*0.88, r, 0.014, 24).rotateZ(-dir * Math.PI/2).translate(dir * (0.062 + s*0.012), 0, 0), mats.tealLid, mats.cadEdgeMat);
        }
      }
      root.add(dG);
      break;
    }

    case 'p12': {
      // Overflow Shut-Off Filter (Slotted Cage + Float Core)
      addMesh(THREE, root, new THREE.CylinderGeometry(0.032, 0.030, 0.022, 36).translate(0, 0.062, 0), mats.darkTeal, mats.cadEdgeMat);
      addMesh(THREE, root, new THREE.CylinderGeometry(0.026, 0.028, 0.095, 36), mats.tealLid, mats.cadEdgeMat);
      addMesh(THREE, root, new THREE.CylinderGeometry(0.021, 0.022, 0.082, 32), mats.whitePorous, mats.cadGridMat);
      for (let i = 0; i < 8; i++) {
        const a = (i / 8) * Math.PI * 2;
        addMesh(THREE, root, new THREE.BoxGeometry(0.004, 0.088, 0.006).translate(0, 0, 0.027).rotateY(a), mats.darkTeal, mats.cadEdgeMat);
      }
      addMesh(THREE, root, new THREE.CylinderGeometry(0.030, 0.028, 0.010, 36).translate(0, -0.052, 0), mats.darkTeal, mats.cadEdgeMat);
      break;
    }

    case 'p13': {
      // Porous Sintered PE Filter (Flanged Solid Plug + Tubular Cylinder)
      const p1 = new THREE.Group(); p1.position.set(-0.032, 0, 0);
      addMesh(THREE, p1, new THREE.CylinderGeometry(0.022, 0.022, 0.092, 36), mats.whitePorous, mats.cadEdgeMat);
      addMesh(THREE, p1, new THREE.CylinderGeometry(0.028, 0.028, 0.014, 36).translate(0, 0.044, 0), mats.whitePorous, mats.cadEdgeMat);
      root.add(p1);

      const p2 = new THREE.Group(); p2.position.set(0.034, -0.008, 0.012);
      addMesh(THREE, p2, new THREE.CylinderGeometry(0.020, 0.020, 0.078, 36), mats.whitePorous, mats.cadEdgeMat);
      addMesh(THREE, p2, new THREE.CylinderGeometry(0.011, 0.011, 0.080, 28), mats.darkTeal, null);
      root.add(p2);
      break;
    }

    case 'p14': {
      // Portable 4-Canister Suction Trolley
      // Central Chrome Column
      addMesh(THREE, root, new THREE.CylinderGeometry(0.007, 0.008, 0.175, 24).translate(0, -0.005, 0), mats.chromeMetal, mats.cadEdgeMat);
      // 5-Star Base + Casters
      for (let i = 0; i < 5; i++) {
        const a = (i / 5) * Math.PI * 2;
        const legG = new THREE.Group(); legG.position.set(0, -0.085, 0); legG.rotation.y = a;
        addMesh(THREE, legG, new THREE.BoxGeometry(0.010, 0.008, 0.068).translate(0, 0, 0.034), mats.chromeMetal, mats.cadEdgeMat);
        addMesh(THREE, legG, new THREE.CylinderGeometry(0.009, 0.009, 0.006, 20).rotateZ(Math.PI/2).translate(0, -0.010, 0.064), mats.darkPolymer, mats.cadEdgeMat);
        root.add(legG);
      }
      // 4 Mounted Suction Canisters around top ring
      for (let i = 0; i < 4; i++) {
        const a = (i / 4) * Math.PI * 2 + Math.PI * 0.25;
        const cG = new THREE.Group();
        cG.position.set(Math.cos(a) * 0.042, 0.042, Math.sin(a) * 0.042);
        addMesh(THREE, cG, new THREE.CylinderGeometry(0.022, 0.018, 0.065, 24), mats.clearPC, mats.cadEdgeMat);
        addMesh(THREE, cG, new THREE.CylinderGeometry(0.023, 0.023, 0.007, 24).translate(0, 0.034, 0), mats.tealLid, mats.cadEdgeMat);
        root.add(cG);
      }
      // Top Push Handle
      addMesh(THREE, root, new THREE.TorusGeometry(0.024, 0.0035, 10, 28).rotateX(Math.PI/2).translate(0, 0.085, 0), mats.tealLid, mats.cadEdgeMat);
      break;
    }

    case 'p15': {
      // Wall Mounting Bracket
      addMesh(THREE, root, new THREE.BoxGeometry(0.072, 0.125, 0.012), mats.whitePorous, mats.cadEdgeMat);
      // Left & Right Dovetail Guide Rails
      for (const sx of [-0.026, 0.026]) {
        addMesh(THREE, root, new THREE.BoxGeometry(0.014, 0.115, 0.022).translate(sx, 0, 0.014), mats.tealLid, mats.cadEdgeMat);
      }
      // Bottom stop latch
      addMesh(THREE, root, new THREE.BoxGeometry(0.048, 0.014, 0.024).translate(0, -0.052, 0.014), mats.darkTeal, mats.cadEdgeMat);
      // Screw holes
      for (const sy of [0.036, -0.022]) {
        addMesh(THREE, root, new THREE.CylinderGeometry(0.006, 0.006, 0.016, 20).rotateX(Math.PI/2).translate(0, sy, 0.002), mats.chromeMetal, mats.cadEdgeMat);
      }
      break;
    }

    case 'p16': {
      // Canister Rear Mounting Clip
      addMesh(THREE, root, new THREE.CylinderGeometry(0.058, 0.058, 0.095, 36, 1, true, -0.55, 1.10).translate(0, 0, -0.042), mats.tealLid, mats.cadEdgeMat);
      addMesh(THREE, root, new THREE.BoxGeometry(0.042, 0.088, 0.014).translate(0, 0, 0.010), mats.tealLid, mats.cadEdgeMat);
      // Tapered dovetail tongue
      addMesh(THREE, root, new THREE.BoxGeometry(0.030, 0.076, 0.012).translate(0, -0.004, 0.022), mats.lightTeal, mats.cadEdgeMat);
      for (const ry of [-0.025, 0, 0.025]) {
        addMesh(THREE, root, new THREE.BoxGeometry(0.038, 0.005, 0.022).translate(0, ry, 0.004), mats.darkTeal, null);
      }
      break;
    }

    case 'p17': {
      // T-Shape Tandem Connector with Teal Cap
      addMesh(THREE, root, new THREE.CylinderGeometry(0.011, 0.011, 0.105, 24).rotateZ(Math.PI/2).translate(0, 0.012, 0), mats.whitePorous, mats.cadEdgeMat);
      addMesh(THREE, root, new THREE.CylinderGeometry(0.011, 0.010, 0.068, 24).translate(0, -0.022, 0), mats.whitePorous, mats.cadEdgeMat);
      // Barbs on arms
      for (const sx of [-0.045, 0.045]) {
        addMesh(THREE, root, new THREE.TorusGeometry(0.0115, 0.0022, 10, 24).rotateY(Math.PI/2).translate(sx, 0.012, 0), mats.whitePorous, mats.cadEdgeMat);
      }
      // Tethered Teal Sealing Cap
      addMesh(THREE, root, new THREE.CylinderGeometry(0.013, 0.013, 0.018, 24).translate(0.028, 0.042, 0), mats.tealLid, mats.cadEdgeMat);
      const tCurve = new THREE.CatmullRomCurve3([
        new THREE.Vector3(0.018, 0.012, 0),
        new THREE.Vector3(0.036, 0.028, 0.012),
        new THREE.Vector3(0.028, 0.042, 0),
      ]);
      addMesh(THREE, root, new THREE.TubeGeometry(tCurve, 24, 0.002, 8, false), mats.lightTeal, null);
      break;
    }

    case 'p18': {
      // Straight Ribbed Double-Cone Connector
      addMesh(THREE, root, new THREE.CylinderGeometry(0.018, 0.018, 0.012, 28).rotateZ(Math.PI/2), mats.tealLid, mats.cadEdgeMat);
      for (const dir of [-1, 1]) {
        for (let s = 0; s < 5; s++) {
          const r1 = 0.0135 - s * 0.0016;
          const r2 = 0.0115 - s * 0.0016;
          addMesh(THREE, root, new THREE.CylinderGeometry(r2, r1, 0.012, 24).rotateZ(-dir * Math.PI/2).translate(dir * (0.012 + s*0.011), 0, 0), mats.lightTeal, mats.cadEdgeMat);
        }
      }
      break;
    }

    case 'p19': {
      // Medical Silicone Jumper Hose (13x7mm Thick-Walled Loop)
      const sPts = [];
      for (let i = 0; i <= 80; i++) {
        const t = i / 80;
        const a = t * Math.PI * 2.6;
        const r = 0.052 + 0.012 * Math.cos(t * Math.PI * 2);
        sPts.push(new THREE.Vector3(Math.cos(a)*r, (t - 0.5)*0.075, Math.sin(a)*r));
      }
      const sCurve = new THREE.CatmullRomCurve3(sPts);
      addMesh(THREE, root, new THREE.TubeGeometry(sCurve, 100, 0.0095, 18, false), mats.siliconeMat, mats.cadEdgeMat);
      addMesh(THREE, root, new THREE.TubeGeometry(sCurve, 80, 0.0050, 12, false), mats.lightTeal, null);
      break;
    }

    case 'p20': {
      // Vacuum Suction Regulator with Analog Gauge & Safety Trap Jar
      // Manifold block
      addMesh(THREE, root, new THREE.BoxGeometry(0.044, 0.048, 0.036).translate(0, 0.008, 0), mats.chromeMetal, mats.cadEdgeMat);
      // Top Bourdon Gauge
      addMesh(THREE, root, new THREE.CylinderGeometry(0.036, 0.036, 0.018, 36).rotateX(Math.PI/2).translate(0, 0.058, 0.006), mats.darkPolymer, mats.cadEdgeMat);
      const gFace = new THREE.Mesh(new THREE.CircleGeometry(0.032, 32), new THREE.MeshBasicMaterial({ map: tex.dialTex }));
      gFace.position.set(0, 0.058, 0.016); root.add(gFace);
      // Front Rotary Adjustment Knob
      addMesh(THREE, root, new THREE.CylinderGeometry(0.016, 0.018, 0.022, 28).rotateX(Math.PI/2).translate(-0.012, 0.008, 0.026), mats.tealLid, mats.cadEdgeMat);
      // Bottom Safety Trap Bottle
      addMesh(THREE, root, new THREE.CylinderGeometry(0.026, 0.022, 0.062, 32).translate(0, -0.052, 0), mats.clearPC, mats.cadEdgeMat);
      addMesh(THREE, root, new THREE.CylinderGeometry(0.010, 0.010, 0.038, 20).translate(0, -0.042, 0), mats.whitePorous, null);
      // Right Hose Barb
      addMesh(THREE, root, new THREE.CylinderGeometry(0.005, 0.007, 0.028, 20).rotateZ(-Math.PI/2).translate(0.035, 0.005, 0), mats.brassMetal, mats.cadEdgeMat);
      break;
    }

    case 'p21': {
      // ON/OFF Vacuum Shut-Off Valve
      addMesh(THREE, root, new THREE.CylinderGeometry(0.014, 0.014, 0.068, 28).rotateZ(Math.PI/2), mats.chromeMetal, mats.cadEdgeMat);
      // Left Hex Nut
      addMesh(THREE, root, new THREE.CylinderGeometry(0.019, 0.019, 0.018, 6).rotateZ(Math.PI/2).translate(-0.038, 0, 0), mats.chromeMetal, mats.cadEdgeMat);
      // Right Hose Barb
      for (let s = 0; s < 3; s++) {
        addMesh(THREE, root, new THREE.CylinderGeometry(0.0065, 0.0085, 0.012, 20).rotateZ(-Math.PI/2).translate(0.038 + s*0.010, 0, 0), mats.brassMetal, mats.cadEdgeMat);
      }
      // Top Quarter-Turn Teal Lever
      addMesh(THREE, root, new THREE.CylinderGeometry(0.008, 0.008, 0.022, 20).translate(0, 0.018, 0), mats.chromeMetal, mats.cadEdgeMat);
      addMesh(THREE, root, new THREE.BoxGeometry(0.052, 0.010, 0.016).translate(0.012, 0.032, 0), mats.tealLid, mats.cadEdgeMat);
      break;
    }

    case 'p22': {
      // Regulator Hose & Fittings Kit
      const archCurve = new THREE.CatmullRomCurve3([
        new THREE.Vector3(-0.055, -0.020, 0),
        new THREE.Vector3(-0.045, 0.055, 0),
        new THREE.Vector3(0.045, 0.055, 0),
        new THREE.Vector3(0.055, -0.020, 0),
      ]);
      addMesh(THREE, root, new THREE.TubeGeometry(archCurve, 64, 0.0075, 16, false), mats.siliconeMat, mats.cadEdgeMat);
      // Left T-Connector
      addMesh(THREE, root, new THREE.CylinderGeometry(0.009, 0.009, 0.048, 20).translate(-0.055, -0.032, 0), mats.tealLid, mats.cadEdgeMat);
      addMesh(THREE, root, new THREE.CylinderGeometry(0.008, 0.008, 0.036, 20).rotateZ(Math.PI/2).translate(-0.038, -0.038, 0), mats.tealLid, mats.cadEdgeMat);
      // Right 90° Elbow + Brass Adapter
      addMesh(THREE, root, new THREE.CylinderGeometry(0.009, 0.009, 0.042, 20).translate(0.055, -0.030, 0), mats.whitePorous, mats.cadEdgeMat);
      addMesh(THREE, root, new THREE.CylinderGeometry(0.008, 0.008, 0.038, 20).rotateZ(Math.PI/2).translate(0.036, -0.045, 0), mats.brassMetal, mats.cadEdgeMat);
      break;
    }

    case 'p23': {
      // Disposable Suction Toothbrush
      const tbG = new THREE.Group(); tbG.rotation.z = 0.18;
      // Hollow ergonomic handle
      addMesh(THREE, tbG, new THREE.CylinderGeometry(0.007, 0.0085, 0.145, 24).rotateZ(Math.PI/2).translate(-0.012, 0, 0), mats.whitePorous, mats.cadEdgeMat);
      // Thumb suction control port
      addMesh(THREE, tbG, new THREE.CylinderGeometry(0.008, 0.006, 0.016, 20).translate(-0.025, 0.010, 0), mats.tealLid, mats.cadEdgeMat);
      // Proximal stepped barb
      addMesh(THREE, tbG, new THREE.CylinderGeometry(0.005, 0.008, 0.026, 20).rotateZ(Math.PI/2).translate(-0.092, 0, 0), mats.tealLid, mats.cadEdgeMat);
      // Brush head + ridged foam sponge + soft bristles
      addMesh(THREE, tbG, new THREE.BoxGeometry(0.038, 0.018, 0.018).translate(0.068, 0.006, 0), mats.foamPink, mats.cadEdgeMat);
      for (let b = 0; b < 5; b++) {
        addMesh(THREE, tbG, new THREE.CylinderGeometry(0.003, 0.003, 0.014, 12).translate(0.054 + b*0.007, -0.008, 0), mats.whitePorous, null);
      }
      root.add(tbG);
      break;
    }

    case 'p24': {
      // Endotracheal Tube Holder
      // Curved anatomical arch faceplate
      const archPts = [];
      for (let i = 0; i <= 32; i++) {
        const a = (i / 32 - 0.5) * Math.PI * 0.85;
        archPts.push(new THREE.Vector3(Math.sin(a) * 0.072, 0, Math.cos(a) * 0.028 - 0.015));
      }
      const archCurve = new THREE.CatmullRomCurve3(archPts);
      addMesh(THREE, root, new THREE.TubeGeometry(archCurve, 40, 0.009, 12, false), mats.tealLid, mats.cadEdgeMat);
      // Central Bite Block + Quick-Turn Clamp Screw
      addMesh(THREE, root, new THREE.CylinderGeometry(0.014, 0.014, 0.048, 24).rotateX(Math.PI/2).translate(0, 0.004, 0.018), mats.whitePorous, mats.cadEdgeMat);
      addMesh(THREE, root, new THREE.CylinderGeometry(0.009, 0.009, 0.032, 20).translate(0, 0.026, 0.022), mats.tealLid, mats.cadEdgeMat);
      addMesh(THREE, root, new THREE.CylinderGeometry(0.016, 0.016, 0.010, 16).translate(0, 0.042, 0.022), mats.lightTeal, mats.cadEdgeMat);
      // Soft padded neck strap loop
      addMesh(THREE, root, new THREE.TorusGeometry(0.058, 0.005, 10, 36, Math.PI * 1.15).rotateX(Math.PI/2).rotateZ(Math.PI*0.92).translate(0, -0.004, -0.012), mats.foamPink, mats.cadEdgeMat);
      break;
    }

    case 'p25': {
      // Medical Receiver Kidney Basin (600cc) + Splash-Vac Floor Suction Dome
      // Left: Kidney-shaped basin
      const bG = new THREE.Group(); bG.position.set(-0.040, 0.012, 0); bG.rotation.x = 0.35;
      addMesh(THREE, bG, new THREE.CylinderGeometry(0.048, 0.036, 0.036, 36).scale(1.25, 1, 0.68), mats.tealLid, mats.cadEdgeMat);
      addMesh(THREE, bG, new THREE.TorusGeometry(0.048, 0.0035, 12, 36).rotateX(Math.PI/2).scale(1.25, 0.68, 1).translate(0, 0.018, 0), mats.lightTeal, mats.cadEdgeMat);
      root.add(bG);

      // Right: Low-profile Splash-Vac Floor Suction Dome
      const sG = new THREE.Group(); sG.position.set(0.045, -0.018, 0.012); sG.rotation.x = 0.25;
      addMesh(THREE, sG, new THREE.CylinderGeometry(0.032, 0.048, 0.018, 36), mats.lightTeal, mats.cadEdgeMat);
      addMesh(THREE, sG, new THREE.CylinderGeometry(0.005, 0.007, 0.028, 20).rotateZ(-0.45).translate(0.008, 0.020, 0), mats.whitePorous, mats.cadEdgeMat);
      root.add(sG);
      break;
    }
  }

  return root;
}
