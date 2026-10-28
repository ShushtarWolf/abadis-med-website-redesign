"""Interactive 3D factory scrollytelling hero (Abadis Shams-Abad plant, 1 unit = 1 m).

Shared by the live FA/EN/AR home #intro and the standalone option page.
three.js r170 + OrbitControls are self-hosted in assets/vendor/three/ (no CDN).
"""
import json
from html import escape as esc

V = '20261029g'
CATALOGUE = 'https://abadis-med.com/wp-content/uploads/2024/12/کاتالوگ-جامع-آبادیس.pdf'

T = {
  'fa': dict(
    root='', quote_href='export/#quote',
    kicker='پیشرو در کنترل عفونت و مدیریت مایعات بیمارستانی',
    h1a='کارخانه‌ای که ', h1b='ردش', h1c=' را می‌کشیم',
    motto='آبادیس: مهندسی دقیق، برای مراقبتی ایمن‌تر',
    sub='اسکرول کنید تا ساختمان ترسیم شود و وارد خط تولید شوید.',
    badge='طرح سه‌بعدی منطبق بر معماری واقعی کارخانه آبادیس (شمس‌آباد — ۲۰۰۰ متر مربع)',
    cat='دریافت کاتالوگ', quote='درخواست قیمت',
    skip='رد کردن و ادامه صفحه', explore='حالت کاوش آزاد', back='بازگشت به مسیر اسکرول',
    hint='بکشید تا بچرخد، دو انگشت یا چرخ موس برای زوم، روی نام بخش‌ها بزنید',
    step='ایستگاه {n} از {t}', aerial='نمای هوایی کارخانه',
    stations=[
      ('سالن ۱ — تزریق پلاستیک', 'سه دستگاه تزریق ۲۲۰ تن، دو دستگاه بادی و یک تزریق ۱۲۰ تن در سالن ۵ متری همکف؛ بدنه، درب و اجزای کیسه‌ها از همین‌جا شکل می‌گیرند.'),
      ('سالن ۱ طبقه بالا — مونتاژ و کارتن‌گذاری', 'سالن ۱۰ در ۱۰ متری مونتاژ پلی‌اورتان با سه ردیف میز، و راهروی ۱۰ در ۳ متری کارتن‌گذاری متصل به آسانسور بار.'),
      ('سالن ۲ — جداسازی فیلتر از قالب', 'فیلتر نهایی از قالب جدا می‌شود. سایر مراحل این اتاق به دلیل حفظ مالکیت فکری نمایش داده نمی‌شود.'),
      ('سالن ۲ — اکسترودر و کلین‌روم', 'دو اکسترودر در طبقه همکف و کلین‌روم کلاس ۱۰۰٬۰۰۰ با دو خط مونتاژ در طبقه بالا، مطابق الزامات تجهیزات پزشکی.'),
      ('سالن ۳ — انبار محصول و ارسال', 'بسته‌بندی ۴۵ عددی در کارتن، ظرفیت تولید ۵ میلیون کیسه در سال و ارسال رایگان به مراکز درمانی از درب سمت راست.'),
    ],
    labels=['تزریق','مونتاژ و کارتن','فیلتر','اکسترودر و کلین‌روم','انبار و ارسال','دفتر مرکزی'],
    digits='fa'),
  'en': dict(
    root='en/', quote_href='export/#quote',
    kicker='A leader in infection control and hospital fluid management',
    h1a='The factory ', h1b='we draw', h1c=', line by line',
    motto='Abadis: precise engineering for safer care',
    sub='Scroll to draw the building and step inside the production line.',
    badge='3D model matched to the real Abadis plant layout (Shams-Abad, 2,000 m²)',
    cat='Download catalogue', quote='Request a quote',
    skip='Skip & Continue', explore='Free Exploration Mode', back='Back to scroll tour',
    hint='Drag to rotate, pinch or wheel to zoom, tap a section name',
    step='Station {n} of {t}', aerial='Aerial view of the plant',
    stations=[
      ('Hall 1: injection molding', 'Three 220-ton injection machines, two blow-molding machines and one 120-ton machine on a 5 m ground floor. Bag bodies, lids and parts start here.'),
      ('Hall 1 upper floor: assembly and cartoning', 'A 10 x 10 m polyurethane assembly hall with three table rows, plus a 10 x 3 m cartoning corridor linked to the goods lift.'),
      ('Hall 2: filter demolding', 'The finished filter is removed from its mold. Other steps in this room are not shown to protect our intellectual property.'),
      ('Hall 2: extrusion and cleanroom', 'Two extruders on the ground floor and a Class 100,000 cleanroom with two assembly lines upstairs, built for medical-device requirements.'),
      ('Hall 3: finished goods and dispatch', 'Cartons of 45, capacity of 5 million bags a year, and free shipping to healthcare centers through the right-hand gate.'),
    ],
    labels=['Injection','Assembly & cartoning','Filter','Extrusion & cleanroom','Warehouse & dispatch','Head office'],
    digits='en'),
  'ar': dict(
    root='arabic/', quote_href='export/#quote',
    kicker='رائدة في مكافحة العدوى وإدارة السوائل في المستشفيات',
    h1a='المصنع الذي ', h1b='نرسمه', h1c=' خطًا بخط',
    motto='آباديس: هندسة دقيقة من أجل رعاية أكثر أمانًا',
    sub='مرّر للأسفل ليُرسم المبنى وادخل إلى خط الإنتاج.',
    badge='نموذج ثلاثي الأبعاد مطابق للتصميم المعماري الحقيقي لمصنع آباديس (شمس آباد — ٢٠٠٠ متر مربع)',
    cat='تحميل الكتالوج', quote='طلب سعر',
    skip='تخطي والمتابعة', explore='وضع الاستكشاف الحر', back='العودة إلى جولة التمرير',
    hint='اسحب للتدوير، واستخدم إصبعين أو عجلة الفأرة للتكبير، واضغط على اسم القسم',
    step='المحطة {n} من {t}', aerial='منظر جوي للمصنع',
    stations=[
      ('القاعة ١: الحقن البلاستيكي', 'ثلاث آلات حقن بقوة ٢٢٠ طنًا وآلتا نفخ وآلة حقن ١٢٠ طنًا في الطابق الأرضي بارتفاع ٥ أمتار؛ هنا تبدأ أجسام الأكياس وأغطيتها.'),
      ('القاعة ١ الطابق العلوي: التجميع والتعبئة', 'قاعة تجميع البولي يوريثان بمساحة ١٠ × ١٠ م مع ثلاثة صفوف من الطاولات، وممر تعبئة الكراتين ١٠ × ٣ م متصل بمصعد البضائع.'),
      ('القاعة ٢: فصل الفلتر من القالب', 'يُفصل الفلتر النهائي عن القالب. لا تُعرض بقية مراحل هذه الغرفة حفاظًا على الملكية الفكرية.'),
      ('القاعة ٢: البثق والغرفة النظيفة', 'آلتا بثق في الطابق الأرضي وغرفة نظيفة من الفئة ١٠٠٬٠٠٠ مع خطَّي تجميع في الطابق العلوي، وفق متطلبات الأجهزة الطبية.'),
      ('القاعة ٣: مستودع المنتجات والشحن', 'كراتين من ٤٥ وحدة، وطاقة إنتاجية ٥ ملايين كيس سنويًا، وشحن مجاني إلى المراكز الصحية عبر البوابة اليمنى.'),
    ],
    labels=['الحقن','التجميع والتعبئة','الفلتر','البثق والغرفة النظيفة','المستودع والشحن','المكتب الرئيسي'],
    digits='ar'),
}

_SVG = 'viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"'
ICO_DL = f'<svg {_SVG}><path d="M12 3v12"/><path d="m7 10 5 5 5-5"/><path d="M5 21h14"/></svg>'
ICO_TAG = f'<svg {_SVG}><path d="M20.6 13.4 13.4 20.6a2 2 0 0 1-2.8 0L3 13V3h10l7.6 7.6a2 2 0 0 1 0 2.8z"/><circle cx="7.5" cy="7.5" r="1.5"/></svg>'
ICO_SKIP = f'<svg {_SVG}><path d="M12 5v14"/><path d="m6 13 6 6 6-6"/></svg>'
ICO_ORBIT = f'<svg {_SVG}><circle cx="12" cy="12" r="3"/><ellipse cx="12" cy="12" rx="10" ry="4.5"/></svg>'
ICO_PIN = f'<svg {_SVG}><path d="M12 22s7-6.2 7-12a7 7 0 0 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/></svg>'


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
    qh = quote_href or (p + t['root'] + t['quote_href'])
    cfg = {
        'lang': lang,
        'step': t['step'], 'total': num(5, lang),
        'nums': [num(i, lang) for i in range(1, 6)],
        'stations': [{'n': a, 't': b} for a, b in t['stations']],
        'labels': t['labels'], 'explore': t['explore'], 'back': t['back'],
    }
    pills = ''.join(
        f'<button type="button" class="f3d-pill" data-i="{i}"><b>{num(i + 1, lang)}</b><span>{esc(lb)}</span></button>'
        for i, lb in enumerate(t['labels'][:5]))
    return f'''  <section class="f3d" id="intro" data-tone="dark" aria-label="{esc(t['h1a'] + t['h1b'] + t['h1c'])}">
    <script type="application/json" class="f3d-cfg">{json.dumps(cfg, ensure_ascii=False)}</script>
    <div class="f3d-stage">
      <canvas class="f3d-gl" aria-hidden="true"></canvas>
      <div class="f3d-labels" aria-hidden="true"></div>
      <div class="f3d-intro">
        <p class="f3d-kicker">{esc(t['kicker'])}</p>
        <h1>{esc(t['h1a'])}<b>{esc(t['h1b'])}</b>{esc(t['h1c'])}</h1>
        <p class="f3d-motto">{esc(t['motto'])}</p>
        <p class="f3d-sub">{esc(t['sub'])}</p>
        <div class="f3d-cta">
          <a class="btn btn-primary" href="{esc(CATALOGUE)}" target="_blank" rel="noopener" data-track="catalogue_download" data-track-label="home_f3d_catalogue_{lang}">{ICO_DL}<span>{esc(t['cat'])}</span></a>
          <a class="btn btn-ghost f3d-ghost" href="{esc(qh)}" data-track="contact_click" data-track-label="home_f3d_quote_{lang}">{ICO_TAG}<span>{esc(t['quote'])}</span></a>
        </div>
        <span class="f3d-cue" aria-hidden="true"></span>
      </div>
      <div class="f3d-panel f3d-glass" aria-live="polite">
        <small class="f3d-step"></small><h2 class="f3d-title"></h2><p class="f3d-text"></p>
        <div class="f3d-dots"><i></i><i></i><i></i><i></i><i></i></div>
      </div>
      <nav class="f3d-pills f3d-glass" aria-label="{esc(t['aerial'])}">{pills}</nav>
      <div class="f3d-prog" aria-hidden="true"><i></i></div>
      <div class="f3d-tools">
        <button type="button" class="f3d-btn f3d-ex">{ICO_ORBIT}<span>{esc(t['explore'])}</span></button>
        <a class="f3d-btn f3d-skip" href="{skip_to}">{ICO_SKIP}<span>{esc(t['skip'])}</span></a>
      </div>
      <div class="f3d-hint f3d-glass">{esc(t['hint'])}</div>
      <p class="f3d-badge f3d-glass">{ICO_PIN}<span>{esc(t['badge'])}</span></p>
    </div>
  </section>'''
