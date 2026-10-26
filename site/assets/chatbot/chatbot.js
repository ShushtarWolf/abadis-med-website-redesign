/* Abadis Sales & Academy chatbot.
   Embed: <script src="/assets/chatbot/chatbot.js" defer data-kb="/assets/data/abadis-knowledge-base.json"></script>
   Tier 1 answers from same-origin files only (JSON, then kb-fallback.js). No CDN and no foreign API
   unless a person explicitly selects Tier 3 and international access is not cut off. */
(function () {
  'use strict';

  var script = document.currentScript;
  if (!script) {
    var nodes = document.querySelectorAll('script[src*="chatbot.js"]');
    script = nodes[nodes.length - 1] || null;
  }
  var kbUrl = (script && script.getAttribute('data-kb')) || '/assets/data/abadis-knowledge-base.json';
  var demo = !!(script && script.getAttribute('data-demo') === 'true');

  var I18N = {
    fa: {
      launcher: 'دستیار هوشمند آبادیس',
      title: 'دستیار هوشمند آبادیس',
      subSales: 'پاسخگوی فروش و راهکارهای بالینی',
      subAcademy: 'پرسش‌وپاسخ و آموزش آکادمی آبادیس',
      tabSales: 'مشاور فروش',
      tabAcademy: 'آکادمی',
      placeholder: 'سؤال یا نیاز بخش درمانی را بنویسید…',
      send: 'ارسال',
      close: 'بستن',
      welcomeSales: 'سلام و وقت بخیر! 👋 من دستیار هوشمند آبادیس هستم. درباره کیسه‌های ساکشن یکبارمصرف (۱، ۲ و ۳ لیتری)، راهکارهای بالینی، شرایط خرید و پیش‌فاکتور، یا محاسبه صرفه‌جویی بیمارستانتان هر سؤالی دارید به زبان طبیعی بپرسید.',
      welcomeAcademy: 'سلام و وقت بخیر! 👋 به بخش آکادمی آبادیس خوش آمدید. می‌توانید درباره مزایای علمی ساکشن مدار بسته نسبت به شیشه‌های سنتی، عملکرد فیلتر هیدروفوبیک و پودر جاذب بپرسید یا «مصاحبه بالینی آکادمی» را شروع کنید.',
      bySolution: 'بر اساس راهکار',
      byProduct: 'بر اساس محصول',
      pickSolution: 'کدام راهکار؟',
      pickProduct: 'کدام گروه محصول؟',
      pickVolume: 'کدام حجم کیسه؟',
      pickSurgeries: 'چند عمل جراحی در سال؟ سقف ۱۵٬۰۰۰.',
      surgeries: 'محاسبه صرفه‌جویی',
      quote: 'درخواست پیش‌فاکتور',
      catalogue: 'کاتالوگ',
      phone: 'تماس با فروش',
      whatsapp: 'واتس‌اپ',
      source: 'منبع',
      empty: 'در حال حاضر پاسخ دقیقی برای این عبارت در دانش‌نامه ثبت نشده است؛ اما می‌توانید یکی از موضوعات پرتکرار زیر را انتخاب کنید یا مستقیماً با کارشناسان فروش آبادیس (۰۲۱-۹۲۰۰۱۰۱۷ داخلی ۱۱) در ارتباط باشید:',
      tierSummary: 'لایه‌های پاسخ — پیش‌فرض موتور داخلی، بدون اینترنت بین‌الملل',
      tier1: 'لایه ۱ — موتور بومی داخل هسته سایت (همیشه)',
      tier2: 'لایه ۲ — مدل داخلی / خودمیزبان، مثلاً /api/chat',
      tier3: 'لایه ۳ — API بین‌المللی، مهلت ۲٫۵ ثانیه، بازگشت خودکار',
      domesticPh: 'نشانی مدل داخلی، مثلاً /api/chat',
      intlPh: 'نشانی API بین‌المللی، فقط اگر این لایه روشن باشد',
      llmKey: 'کلید لایه ۲ یا ۳، فقط در همین نشست',
      coreTag: 'موتور داخلی هسته سایت',
      cutoffNote: 'شبیه‌سازی قطع اینترنت بین‌الملل: درخواست خارجی ارسال نشد. پاسخ بالا از موتور داخلی است.',
      intlFallback: 'اینترنت بین‌الملل در دسترس نبود. پاسخ بالا از موتور داخلی هسته سایت است.',
      tierFail: 'لایه بالاتر پاسخ نداد. پاسخ بالا از موتور داخلی هسته سایت است.',
      tier1short: 'لایه فعال: موتور بومی داخل هسته سایت',
      tier2short: 'لایه فعال: مدل داخلی، با بازگشت به موتور هسته',
      tier3short: 'لایه فعال: API بین‌المللی، با بازگشت به موتور هسته',
      cutoffShort: 'قطع بین‌الملل شبیه‌سازی شده',
      embeddedSrc: 'دانش‌نامه از نسخه جاسازی‌شده',
      estimate: function (r) {
        return 'با ' + fmt(r.n, 'fa') + ' عمل در سال: حدود ' + fmt(r.water, 'fa') + ' لیتر آب، ' + fmt(r.cost, 'fa') + ' تومان هزینه شست‌وشو و ضدعفونی، و ' + fmt(r.hours, 'fa') + ' ساعت از زمان کادر درمان. CO₂ و کیلوگرم پلاستیک در این فرمول نیست.';
      }
    },
    en: {
      launcher: 'Talk to Abadis',
      title: 'Abadis',
      subSales: 'Sales and product configurator',
      subAcademy: 'Academy questions',
      tabSales: 'Sales',
      tabAcademy: 'Academy',
      placeholder: 'Ask about a department, a volume, or a certificate…',
      send: 'Send',
      close: 'Close',
      welcomeSales: 'Hello and welcome! 👋 I am the Abadis Medical AI Assistant. Ask me anything about our 1L/2L/3L disposable suction liners, clinical solutions, proforma quotes, or hospital savings calculations.',
      welcomeAcademy: 'Hello and welcome to Abadis Academy! 👋 Ask about closed-system infection control vs. traditional glass bottles, shutoff filters, gelling powder, or start the interactive Clinical Interview.',
      bySolution: 'By solution',
      byProduct: 'By product',
      pickSolution: 'Which solution?',
      pickProduct: 'Which product group?',
      pickVolume: 'Which liner volume?',
      pickSurgeries: 'How many surgeries a year? Cap 15,000.',
      surgeries: 'Estimate savings',
      quote: 'Request a quote',
      catalogue: 'Catalogue',
      phone: 'Call sales',
      whatsapp: 'WhatsApp',
      source: 'Source',
      empty: 'I did not find an exact match for that phrase in the knowledge base, but you can pick one of the core Abadis topics below or reach our team directly:',
      tierSummary: 'Answer tiers — default is the on-site engine, with no international network',
      tier1: 'Tier 1 — on-site core engine (always available)',
      tier2: 'Tier 2 — domestic / self-hosted model, for example /api/chat',
      tier3: 'Tier 3 — international API, 2.5s timeout, automatic fallback',
      domesticPh: 'Domestic model URL, for example /api/chat',
      intlPh: 'International API URL, only if this tier is selected',
      llmKey: 'Tier 2 or 3 key, this session only',
      coreTag: 'On-site core engine',
      cutoffNote: 'International cut-off simulated: the foreign request was not sent. The answer above is from the on-site engine.',
      intlFallback: 'International access did not answer. The reply above is from the on-site core engine.',
      tierFail: 'The higher tier did not answer. The reply above is from the on-site core engine.',
      tier1short: 'Active tier: on-site core engine',
      tier2short: 'Active tier: domestic model, falling back to the core engine',
      tier3short: 'Active tier: international API, falling back to the core engine',
      cutoffShort: 'international cut-off simulated',
      embeddedSrc: 'knowledge base loaded from the embedded copy',
      estimate: function (r) {
        return 'At ' + fmt(r.n, 'en') + ' surgeries a year: about ' + fmt(r.water, 'en') + ' litres of water, ' + fmt(r.cost, 'en') + ' toman in wash and disinfectant, and ' + fmt(r.hours, 'en') + ' staff hours. This formula has no CO₂ and no plastic kilograms.';
      }
    },
    ar: {
      launcher: 'تحدث مع آباديس',
      title: 'آباديس',
      subSales: 'مستشار المبيعات واختيار المنتج',
      subAcademy: 'أسئلة الأكاديمية',
      tabSales: 'المبيعات',
      tabAcademy: 'الأكاديمية',
      placeholder: 'اكتب سؤالًا عن القسم أو السعة أو الشهادة…',
      send: 'إرسال',
      close: 'إغلاق',
      welcomeSales: 'ابدأ من حل سريري أو من سعة الكيس. حساب التوفير حتى ١٥٬٠٠٠ عملية ومن دون CO₂.',
      welcomeAcademy: 'اسأل عن الاستخدام السريري أو النظام المغلق أو الشهادات أو إنقاذ زاغروس أو آباديس. الجواب من قاعدة المعرفة.',
      bySolution: 'حسب الحل',
      byProduct: 'حسب المنتج',
      pickSolution: 'أي حل؟',
      pickProduct: 'أي مجموعة؟',
      pickVolume: 'أي سعة للكيس؟',
      pickSurgeries: 'كم عملية في السنة؟ السقف ١٥٬٠٠٠.',
      surgeries: 'حساب التوفير',
      quote: 'طلب عرض سعر',
      catalogue: 'الكتالوج',
      phone: 'اتصال بالمبيعات',
      whatsapp: 'واتساب',
      source: 'المصدر',
      empty: 'لا نتيجة في قاعدة المعرفة. جرّب أحد الأسئلة الجاهزة.',
      tierSummary: 'طبقات الإجابة — الافتراضي محرك الموقع بلا إنترنت دولي',
      tier1: 'الطبقة ١ — المحرك المحلي داخل نواة الموقع (دائمًا)',
      tier2: 'الطبقة ٢ — نموذج داخلي / مستضاف ذاتيًا، مثل /api/chat',
      tier3: 'الطبقة ٣ — واجهة دولية، مهلة ٢٫٥ ث، رجوع تلقائي',
      domesticPh: 'عنوان النموذج الداخلي، مثل /api/chat',
      intlPh: 'عنوان الواجهة الدولية، فقط إذا اختيرت هذه الطبقة',
      llmKey: 'مفتاح الطبقة ٢ أو ٣ لهذه الجلسة فقط',
      coreTag: 'المحرك المحلي لنواة الموقع',
      cutoffNote: 'محاكاة قطع الإنترنت الدولي: لم يُرسل الطلب الخارجي. الإجابة أعلاه من المحرك المحلي.',
      intlFallback: 'الوصول الدولي لم يجب. الرد أعلاه من المحرك المحلي.',
      tierFail: 'الطبقة الأعلى لم تجب. الرد أعلاه من المحرك المحلي.',
      tier1short: 'الطبقة النشطة: المحرك المحلي',
      tier2short: 'الطبقة النشطة: نموذج داخلي مع الرجوع للمحرك',
      tier3short: 'الطبقة النشطة: واجهة دولية مع الرجوع للمحرك',
      cutoffShort: 'قطع دولي مُحاكى',
      embeddedSrc: 'قاعدة المعرفة من النسخة المضمّنة',
      estimate: function (r) {
        return 'مع ' + fmt(r.n, 'ar') + ' عملية في السنة: نحو ' + fmt(r.water, 'ar') + ' لتر ماء، و' + fmt(r.cost, 'ar') + ' تومان لكلفة الغسل والتعقيم، و' + fmt(r.hours, 'ar') + ' ساعة من وقت الطاقم. بلا CO₂ وبلا كيلوغرامات بلاستيك.';
      }
    }
  };

  var CHIPS = {
    fa: {
      sales: ['راهکار مدیریت مایعات', 'کیسه ۲ لیتری برای ICU', 'صرفه‌جویی ۵۰۰۰ عمل'],
      academy: ['شروع مصاحبه بالینی آکادمی', 'فیلتر قطع‌کننده چه می‌کند؟', 'چرا ساکشن مدار بسته بهتر از شیشه‌ایه؟', 'ISO و IMED', 'نجات زاگرس چیست؟']
    },
    en: {
      sales: ['Fluid management solution', '2 litre liner for ICU', 'Savings for 5000 surgeries'],
      academy: ['Start Academy clinical interview', 'Why are closed-system disposable liners better than traditional glass bottles?', 'What does the shutoff filter do?', 'ISO and IMED']
    },
    ar: {
      sales: ['حل إدارة السوائل', 'كيس ٢ لتر لـ ICU', 'توفير ٥٠٠٠ عملية'],
      academy: ['ابدأ مقابلة الأكاديمية', 'ماذا يفعل فلتر قطع التدفق؟', 'ISO و IMED', 'ما إنقاذ زاغروس؟']
    }
  };

  var SOLUTIONS = [
    { id: 'fluid', fa: 'مدیریت مایعات', en: 'Fluid management', ar: 'إدارة السوائل' },
    { id: 'airway', fa: 'راه هوایی', en: 'Airway safety', ar: 'الطريق الهوائي' },
    { id: 'infection-waste', fa: 'کنترل آلودگی', en: 'Infection control', ar: 'السيطرة على التلوث' },
    { id: 'or-efficiency', fa: 'اتاق عمل', en: 'Operating room', ar: 'غرفة العمليات' },
    { id: 'icu-care', fa: 'مراقبت ICU', en: 'ICU care', ar: 'رعاية ICU' }
  ];
  var PRODUCTS = [
    { id: 'canisters-liners', fa: 'کیسه و مخزن', en: 'Liners & canisters', ar: 'الأكياس والخزانات' },
    { id: 'suction-instruments', fa: 'تیوب ساکشن', en: 'Suction tubes', ar: 'أنبوب الشفط' },
    { id: 'airway', fa: 'راه هوایی', en: 'Airway care', ar: 'الطريق الهوائي' },
    { id: 'anesthesia-icu', fa: 'بیهوشی و ICU', en: 'Anesthesia & ICU', ar: 'التخدير وICU' },
    { id: 'general-consumables', fa: 'ملزومات عمومی', en: 'General consumables', ar: 'مستهلكات عامة' }
  ];

  function fmt(n, lang) {
    var loc = lang === 'fa' ? 'fa-IR' : lang === 'ar' ? 'ar' : 'en-US';
    try { return Math.round(n).toLocaleString(loc); } catch (e) { return String(Math.round(n)); }
  }

  function estimate(n) {
    n = Math.max(0, Math.min(15000, Math.round(Number(n) / 100) * 100));
    var usd = 269500;
    return {
      n: n,
      water: Math.round(n * 1.6 * 9.971),
      cost: Math.round(n * 2.5 * usd),
      hours: Math.round(n * 1.6 * 2.2 * 7.1 / 60)
    };
  }

  var NIN_FA = 'موتور داخلی هسته سایت (فعال در شبکه ملی اطلاعات / بدون نیاز به اینترنت بین‌الملل)';
  var NIN_EN = 'Core On-Site Engine — 100% Iran Intranet Resilient';
  var TIER_MS = 2500;
  var state = {
    lang: 'fa', mode: 'sales', open: false, kb: null, kbSource: '',
    choice: null, volume: null, tier: 'core', cutoff: false
  };
  var root, panel, logEl, chipEl, choiceEl, input, subEl, keyEl, domesticEl, intlEl, badgeEl;
  var index = null;

  function t() { return I18N[state.lang] || I18N.fa; }
  function textOf(node) {
    if (!node) return '';
    if (typeof node === 'string') return node;
    return node[state.lang] || node.fa || node.en || '';
  }
  function urlOf(node) {
    if (!node) return '';
    if (typeof node === 'string') return node;
    return node[state.lang] || node.fa || '';
  }

  function el(tag, cls, html) {
    var node = document.createElement(tag);
    if (cls) node.className = cls;
    if (html != null) node.innerHTML = html;
    return node;
  }

  function build() {
    root = el('div', 'abadis-chat');
    root.dataset.mode = 'sales';
    var launcher = el('button', 'abadis-chat-launcher');
    launcher.type = 'button';
    launcher.setAttribute('aria-expanded', 'false');
    launcher.innerHTML = '<span class="abadis-chat-dot" aria-hidden="true"></span><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M4 4h16a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H9l-5 4v-4H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z"/></svg><span></span>';
    launcher.addEventListener('click', function () { state.open ? close() : open(); });

    panel = el('section', 'abadis-chat-panel');
    panel.hidden = true;
    panel.setAttribute('role', 'dialog');
    panel.setAttribute('aria-modal', 'false');

    var head = el('div', 'abadis-chat-head');
    var titles = el('div');
    titles.appendChild(el('h2', null, ''));
    subEl = el('p');
    titles.appendChild(subEl);
    head.appendChild(titles);
    var langs = el('div', 'abadis-chat-langs');
    ['fa', 'en', 'ar'].forEach(function (code) {
      var b = el('button');
      b.type = 'button';
      b.textContent = code.toUpperCase();
      b.dataset.lang = code;
      b.addEventListener('click', function () { setLang(code); });
      langs.appendChild(b);
    });
    head.appendChild(langs);
    var closer = el('button', 'abadis-chat-iconbtn');
    closer.type = 'button';
    closer.dataset.close = '1';
    closer.textContent = '×';
    closer.addEventListener('click', close);
    head.appendChild(closer);
    badgeEl = el('p', 'abadis-chat-nin');
    badgeEl.hidden = true;
    badgeEl.innerHTML = '<strong></strong><span dir="ltr"></span>';
    panel.appendChild(head);

    var tabs = el('div', 'abadis-chat-tabs');
    tabs.setAttribute('role', 'tablist');
    ['sales', 'academy'].forEach(function (mode) {
      var b = el('button');
      b.type = 'button';
      b.dataset.mode = mode;
      b.setAttribute('role', 'tab');
      b.addEventListener('click', function () { setMode(mode); });
      tabs.appendChild(b);
    });
    panel.appendChild(tabs);

    logEl = el('div', 'abadis-chat-log');
    logEl.setAttribute('aria-live', 'polite');
    panel.appendChild(logEl);
    choiceEl = el('div', 'abadis-chat-choices');
    panel.appendChild(choiceEl);
    chipEl = el('div', 'abadis-chat-chips');
    panel.appendChild(chipEl);

    var llm = el('details', 'abadis-chat-llm');
    llm.hidden = true;
    var sum = el('summary');
    llm.appendChild(sum);
    var tiers = el('div', 'abadis-chat-tiers');
    tiers.setAttribute('role', 'radiogroup');
    ['core', 'domestic', 'intl'].forEach(function (tier) {
      var label = el('label');
      var radio = document.createElement('input');
      radio.type = 'radio';
      radio.name = 'abadis-chat-tier';
      radio.value = tier;
      if (tier === 'core') radio.checked = true;
      radio.addEventListener('change', function () { if (radio.checked) setTier(tier); });
      label.appendChild(radio);
      label.appendChild(document.createTextNode(''));
      tiers.appendChild(label);
    });
    llm.appendChild(tiers);
    domesticEl = document.createElement('input');
    domesticEl.type = 'text';
    domesticEl.autocomplete = 'off';
    domesticEl.spellcheck = false;
    intlEl = document.createElement('input');
    intlEl.type = 'text';
    intlEl.autocomplete = 'off';
    intlEl.spellcheck = false;
    keyEl = document.createElement('input');
    keyEl.type = 'password';
    keyEl.autocomplete = 'off';
    llm.appendChild(domesticEl);
    llm.appendChild(intlEl);
    llm.appendChild(keyEl);
    panel.appendChild(llm);

    var form = el('form', 'abadis-chat-form');
    input = document.createElement('input');
    input.type = 'text';
    input.required = true;
    var send = el('button', 'abadis-chat-send');
    send.type = 'submit';
    form.appendChild(input);
    form.appendChild(send);
    form.addEventListener('submit', function (ev) {
      ev.preventDefault();
      var q = input.value.trim();
      if (!q) return;
      input.value = '';
      ask(q);
    });
    panel.appendChild(form);

    root.appendChild(launcher);
    root.appendChild(panel);
    document.body.appendChild(root);
    var docLang = (document.documentElement.lang || '').toLowerCase();
    if (docLang.indexOf('en') === 0) state.lang = 'en';
    else if (docLang.indexOf('ar') === 0) state.lang = 'ar';
    setLang(state.lang);
    setMode('sales');
  }

  function paintChrome() {
    var L = t();
    root.lang = state.lang === 'en' ? 'en' : state.lang === 'ar' ? 'ar' : 'fa';
    root.dir = state.lang === 'en' ? 'ltr' : 'rtl';
    root.querySelector('.abadis-chat-launcher span').textContent = L.launcher;
    root.querySelector('.abadis-chat-launcher').setAttribute('aria-label', L.launcher);
    root.querySelector('.abadis-chat-head h2').textContent = L.title;
    subEl.textContent = state.mode === 'academy' ? L.subAcademy : L.subSales;
    root.querySelector('[data-close]').setAttribute('aria-label', L.close);
    root.querySelectorAll('.abadis-chat-langs button').forEach(function (b) {
      b.setAttribute('aria-pressed', b.dataset.lang === state.lang ? 'true' : 'false');
    });
    root.querySelectorAll('.abadis-chat-tabs button').forEach(function (b) {
      var on = b.dataset.mode === state.mode;
      b.setAttribute('aria-selected', on ? 'true' : 'false');
      b.textContent = b.dataset.mode === 'sales' ? L.tabSales : L.tabAcademy;
    });
    input.placeholder = L.placeholder;
    input.setAttribute('aria-label', L.placeholder);
    root.querySelector('.abadis-chat-send').textContent = L.send;
    root.querySelector('.abadis-chat-llm summary').textContent = L.tierSummary;
    var tierLabels = [L.tier1, L.tier2, L.tier3];
    root.querySelectorAll('.abadis-chat-tiers label').forEach(function (label, i) {
      label.lastChild.textContent = tierLabels[i];
      var radio = label.querySelector('input');
      radio.checked = radio.value === state.tier;
    });
    domesticEl.placeholder = L.domesticPh;
    intlEl.placeholder = L.intlPh;
    keyEl.placeholder = L.llmKey;
    badgeEl.querySelector('strong').textContent = NIN_FA;
    badgeEl.querySelector('span').textContent = NIN_EN;
    panel.setAttribute('aria-label', L.title);
    root.dataset.tier = state.tier;
    root.dataset.cutoff = state.cutoff ? 'on' : 'off';
    root.dataset.kbSource = state.kbSource || '';
    paintChips();
    emitEngine();
  }

  function paintChips() {
    chipEl.textContent = '';
    var list = (CHIPS[state.lang] || CHIPS.fa)[state.mode] || [];
    list.forEach(function (label) {
      var b = el('button', 'abadis-chat-chip');
      b.type = 'button';
      b.textContent = label;
      b.addEventListener('click', function () { ask(label); });
      chipEl.appendChild(b);
    });
  }

  function addMsg(role, html) {
    var row = el('div', 'abadis-chat-msg abadis-chat-msg--' + role);
    row.innerHTML = html;
    logEl.appendChild(row);
    logEl.scrollTop = logEl.scrollHeight;
    return row;
  }

  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  function linkLine(url, label) {
    if (!url) return '';
    return '<span class="abadis-chat-src">' + esc(t().source) + ': <a href="' + esc(url) + '">' + esc(label || url) + '</a></span>';
  }

  function ctaLine() {
    var L = t();
    var c = state.kb && state.kb.support && state.kb.support.ctas;
    if (!c) return '';
    return '<span class="abadis-chat-src">'
      + '<a href="' + esc(urlOf(c.quote)) + '">' + esc(L.quote) + '</a> · '
      + '<a href="' + esc(urlOf(c.catalogue)) + '">' + esc(L.catalogue) + '</a> · '
      + '<a href="' + esc(c.phone) + '">' + esc(L.phone) + '</a> · '
      + '<a href="' + esc(c.whatsapp) + '" target="_blank" rel="noopener">' + esc(L.whatsapp) + '</a>'
      + '</span>';
  }

  function showChoices(items, kind) {
    choiceEl.textContent = '';
    items.forEach(function (item) {
      var b = el('button', 'abadis-chat-choice');
      b.type = 'button';
      b.textContent = item[state.lang] || item.fa;
      b.addEventListener('click', function () {
        addMsg('user', esc(item[state.lang] || item.fa));
        onChoice(kind, item);
      });
      choiceEl.appendChild(b);
    });
  }

  function findChunk(id) {
    var list = (state.kb && state.kb.chunks) || [];
    for (var i = 0; i < list.length; i++) if (list[i].id === id) return list[i];
    return null;
  }

  function findCatalog(id) {
    var list = (state.kb && state.kb.catalog) || [];
    for (var i = 0; i < list.length; i++) if (list[i].id === id) return list[i];
    return null;
  }

  function onChoice(kind, item) {
    if (kind === 'path') {
      if (item.id === 'solution') {
        addMsg('bot', esc(t().pickSolution));
        showChoices(SOLUTIONS, 'solution');
      } else {
        addMsg('bot', esc(t().pickProduct));
        showChoices(PRODUCTS, 'product');
      }
      return;
    }
    if (kind === 'solution') {
      state.choice = item.id;
      var chunk = findChunk('sol-' + (item.id === 'or-efficiency' || item.id === 'icu-care' ? 'fluid' : item.id));
      var cat = item.id === 'airway' ? findCatalog('airway') : findCatalog('canisters-liners');
      var body = chunk ? textOf(chunk.text) : textOf(cat && cat.summary);
      var url = chunk ? urlOf(chunk.url) : (cat && cat.links && cat.links[0] && urlOf(cat.links[0]));
      addMsg('bot', esc(body).replace(/\n/g, '<br>') + linkLine(url, url) + '<br>' + esc(t().pickVolume));
      showChoices([
        { id: '1', fa: '۱ لیتر', en: '1 litre', ar: '١ لتر' },
        { id: '2', fa: '۲ لیتر', en: '2 litres', ar: '٢ لتر' },
        { id: '3', fa: '۳ لیتر', en: '3 litres', ar: '٣ لتر' }
      ], 'volume');
      return;
    }
    if (kind === 'product') {
      state.choice = item.id;
      var product = findCatalog(item.id);
      var summary = product ? textOf(product.summary) + '\n' + textOf(product.applications) : '';
      var href = product && product.links && product.links[0] ? urlOf(product.links[0]) : '/products/';
      addMsg('bot', esc(summary).replace(/\n/g, '<br>') + linkLine(href, href) + (item.id === 'canisters-liners' || item.id === 'anesthesia-icu' || item.id === 'gastroenterology' || item.id === 'gynecology' ? '<br>' + esc(t().pickVolume) : '<br>' + ctaLine()));
      if (item.id === 'canisters-liners' || item.id === 'anesthesia-icu') {
        showChoices([
          { id: '1', fa: '۱ لیتر', en: '1 litre', ar: '١ لتر' },
          { id: '2', fa: '۲ لیتر', en: '2 litres', ar: '٢ لتر' },
          { id: '3', fa: '۳ لیتر', en: '3 litres', ar: '٣ لتر' }
        ], 'volume');
      } else {
        showChoices([
          { id: '1000', fa: '۱۰۰۰ عمل', en: '1000 surgeries', ar: '١٠٠٠ عملية' },
          { id: '5000', fa: '۵۰۰۰ عمل', en: '5000 surgeries', ar: '٥٠٠٠ عملية' },
          { id: '15000', fa: '۱۵۰۰۰ عمل', en: '15000 surgeries', ar: '١٥٠٠٠ عملية' }
        ], 'savings');
      }
      return;
    }
    if (kind === 'volume') {
      state.volume = item.id;
      addMsg('bot', esc(t().pickSurgeries));
      showChoices([
        { id: '1000', fa: '۱۰۰۰ عمل', en: '1000 surgeries', ar: '١٠٠٠ عملية' },
        { id: '5000', fa: '۵۰۰۰ عمل', en: '5000 surgeries', ar: '٥٠٠٠ عملية' },
        { id: '10000', fa: '۱۰۰۰۰ عمل', en: '10000 surgeries', ar: '١٠٠٠٠ عملية' },
        { id: '15000', fa: '۱۵۰۰۰ عمل', en: '15000 surgeries', ar: '١٥٠٠٠ عملية' }
      ], 'savings');
      return;
    }
    if (kind === 'savings') {
      var row = estimate(item.id);
      var calc = state.kb && state.kb.calculator && urlOf(state.kb.calculator.url);
      addMsg('bot', esc(t().estimate(row)) + linkLine(calc || '/dial-practical/', calc || '/dial-practical/') + ctaLine());
      choiceEl.textContent = '';
    }
  }

  var STOP = {
    چه: 1, که: 1, از: 1, در: 1, به: 1, را: 1, با: 1, این: 1, آن: 1, است: 1, هست: 1, بود: 1, شد: 1,
    برای: 1, یا: 1, و: 1, می: 1, کند: 1, شود: 1, آیا: 1, ایا: 1, چند: 1, چنده: 1, چقدر: 1, چقدره: 1,
    چطور: 1, چگونه: 1, چرا: 1, چیه: 1, چیست: 1, کجا: 1, کجاست: 1, کدام: 1, کی: 1, اگر: 1, بشه: 1,
    میشه: 1, دارد: 1, دارند: 1, میشود: 1, میکند: 1, های: 1, ها: 1, یک: 1, هم: 1, بر: 1, تا: 1, هر: 1,
    آبادیس: 1, ابادیس: 1, شرکت: 1, مورد: 1, درباره: 1, کار: 1, بگید: 1, بگو: 1, لطفا: 1, میخواستم: 1, میخوام: 1,
    the: 1, and: 1, what: 1, does: 1, do: 1, did: 1, is: 1, are: 1, was: 1, were: 1, of: 1, an: 1, a: 1,
    to: 1, for: 1, on: 1, in: 1, at: 1, by: 1, with: 1, from: 1, how: 1, many: 1, much: 1, why: 1,
    which: 1, where: 1, when: 1, who: 1, can: 1, if: 1, use: 1, used: 1, using: 1, offer: 1, have: 1,
    has: 1, you: 1, your: 1, we: 1, our: 1, they: 1, it: 1, that: 1, this: 1, there: 1, be: 1, abadis: 1,
    tell: 1, me: 1, about: 1, please: 1,
    ما: 1, ماذا: 1, هل: 1, من: 1, في: 1, على: 1, الى: 1, إلى: 1, عن: 1, مع: 1, هذا: 1, هذه: 1,
    التي: 1, الذي: 1, كم: 1, كيف: 1, لماذا: 1, اين: 1, أين: 1, متى: 1, هي: 1, هو: 1, او: 1, أو: 1,
    كل: 1, عند: 1, اباديس: 1, آباديس: 1
  };
  var SYN = [
    ['فیلتر', 'filter', 'فلتر'],
    ['قطع', 'shutoff', 'هیدروفوبیک', 'hydrophobic', 'مسدود'],
    ['سرریز', 'overflow', 'طفح'],
    ['کیسه', 'liner', 'کیس', 'bag'],
    ['مخزن', 'canister', 'خزان'],
    ['زاگرس', 'zagros', 'زاغروس', 'بلوط', 'oak'],
    ['گواهی', 'گواهینامه', 'مجوز', 'پروانه', 'استاندارد', 'ایزو', 'iso', 'imed', 'ce', 'gmp', 'certificate', 'license', 'patent', 'اختراع', 'شهاده', 'شهادات', 'تراخیص'],
    ['تاسیس', 'founded', 'established', '2017', '1396'],
    ['عفونت', 'infection', 'تلوث', 'الودگی'],
    ['هوا', 'هوایی', 'airway', 'هوايي'],
    ['تیوب', 'tube', 'انبوب'],
    ['صرفه', 'صرفهجویی', 'saving', 'توفیر', 'calculator', 'محاسبهگر'],
    ['پودر', 'powder', 'جاذب', 'absorbent', 'ژله', 'جامدکننده', 'ماص'],
    ['امار', 'رضایت', 'مراکز', 'مرکز', 'بیمارستان', 'کاربر', 'خرابی', 'ظرفیت', 'سهم', 'stats', 'satisfaction', 'center', 'hospital', 'user', 'failure', 'rate', '1232', '11112', '98', 'احصاییات', 'رضا', 'مراکز'],
    ['فلسفه', 'ستون', 'رویکرد', 'معماری', 'راهکار', 'philosophy', 'pillar', 'solution', 'فلسفه', 'ارکان', 'حلول'],
    ['شیشه', 'سنتی', 'چندبارمصرف', 'مداربسته', 'بسته', 'بهتر', 'برتری', 'مقایسه', 'glass', 'bottle', 'reusable', 'traditional', 'closed', 'better', 'beat', 'advantage', 'زجاج', 'زجاجیه', 'تقلیدیه', 'مغلق', 'افضل'],
    ['قیمت', 'خرید', 'هزینه', 'تعرفه', 'پیشفاکتور', 'فاکتور', 'سفارش', 'حجم', 'سایز', 'لیتر', 'price', 'pricing', 'cost', 'quote', 'proforma', 'order', 'volume', 'سعر', 'اسعار', 'شراء', 'سعه', 'سعات'],
    ['اینترنت', 'فیلترینگ', 'ملی', 'افلاین', 'چتبات', 'intranet', 'internet', 'filtering', 'offline', 'national', 'network', 'انترنت', 'انقطاع', 'حجب', 'وطنیه'],
    ['تماس', 'تلفن', 'شماره', 'ادرس', 'نشانی', 'کارخانه', 'دفتر', 'واتساپ', 'contact', 'phone', 'address', 'factory', 'office', 'whatsapp', 'اتصال', 'عنوان', 'مصنع'],
    ['کارتن', 'بستهبندی', 'تعداد', 'carton', 'pack', 'box', 'کرتون', 'عدد'],
    ['کاتالوگ', 'دانلود', 'فایل', 'بروشور', 'catalog', 'catalogue', 'download', 'brochure', 'کتالوج', 'تنزیل'],
    ['نماینده', 'نمایندگی', 'استان', 'پخش', 'توزیع', 'dealer', 'distributor', 'agent', 'representative', 'ممثل', 'وکیل'],
    ['نصب', 'راهاندازی', 'سری', 'اتصال', 'نشتی', 'install', 'installation', 'series', 'leak', 'ترکیب', 'تسلسل'],
    ['گارانتی', 'وارانتی', 'ضمانت', 'تعمیر', 'تعویض', 'warranty', 'guarantee', 'replacement', 'ضمان', 'استبدال'],
    ['نمونه', 'دمو', 'تست', 'sample', 'trial', 'عینه']
  ];

  var ACADEMY_QUIZ = [
    {
      q: {
        fa: 'سؤال ۱ از ۳ (مصاحبه بالینی آکادمی آبادیس):\nدر بخش ICU یا اتاق عمل، مهم‌ترین خطر استفاده از شیشه‌های ساکشن سنتی (چندبارمصرف) هنگام تخلیه و شست‌وشو چیست؟',
        en: 'Question 1 of 3 (Abadis Academy Clinical Interview):\nIn the ICU or Operating Room, what is the primary clinical hazard of manually emptying and washing traditional reusable glass suction bottles?',
        ar: 'السؤال ١ من ٣ (المقابلة السريرية لأكاديمية آباديس):\nفي قسم العناية المركزة أو غرفة العمليات، ما هو الخطر الرئيسي لتفريغ وغسل قوارير الشفط الزجاجية التقليدية يدويًا؟'
      },
      options: [
        { id: 'q1_a', fa: 'انتشار آئروسل و تماس مستقیم پرستار با ترشحات عفونی', en: 'Aerosol splash & direct nurse exposure to infectious fluids', ar: 'انتشار الرذاذ والتعرض المباشر للسوائل المعدية' },
        { id: 'q1_b', fa: 'فقط سنگینی شیشه', en: 'Only the weight of the glass bottle', ar: 'ثقل وزن القارورة الزجاجية فقط' }
      ],
      feedback: {
        fa: 'دقیقاً درست است! تخلیه دستی شیشه‌های سنتی باعث پخش آئروسل‌های عفونی (مانند هانتاویروس و پاتوژن‌های تنفسی/خونی) و آلودگی محیط می‌شود. سیستم ساکشن مدار بسته یکبارمصرف آبادیس با پودر جاذب (ژله‌ای‌کننده) این تماس را به صفر می‌رساند.',
        en: 'Spot on! Manual emptying of open glass canisters releases infectious aerosols and exposes nursing staff to bloodborne and respiratory pathogens. Abadis closed-system disposable liners with solidifying powder eliminate this exposure completely.',
        ar: 'إجابة صحيحة تمامًا! التفريغ اليدوي للقوارير التقليدية ينشر الرذاذ المعدي ويعرض الكادر التمريضي للعدوى. نظام الشفط المغلق من آباديس مع المسحوق الماص يمنع هذا التماس كليًا.'
      }
    },
    {
      q: {
        fa: 'سؤال ۲ از ۳ (مصاحبه بالینی آکادمی آبادیس):\nوظیفه «فیلتر قطع‌کننده جریان (هیدروفوبیک)» در درب کیسه ساکشن آبادیس چیست؟',
        en: 'Question 2 of 3 (Abadis Academy Clinical Interview):\nWhat is the role of the hydrophobic shutoff filter integrated into the Abadis suction liner lid?',
        ar: 'السؤال ٢ من ٣ (المقابلة السريرية لأكاديمية آباديس):\nما هي وظيفة فلتر قطع التدفق (الهيدروفوبيك) في غطاء كيس الشفط من آباديس؟'
      },
      options: [
        { id: 'q2_a', fa: 'جلوگیری از سرریز مایع و محافظت از سیستم وکیوم مرکزی/دستگاه', en: 'Prevents fluid overflow & protects central vacuum/suction pump', ar: 'منع طفح السوائل وحماية منظومة الشفط المركزية' },
        { id: 'q2_b', fa: 'افزایش حجم مخزن ساکشن', en: 'Increases the volume of the canister', ar: 'زيادة سعة خزان الشفط' }
      ],
      feedback: {
        fa: 'عالی! آبادیس اولین تولیدکننده فیلترهای قطع‌کننده جریان در ایران است. به محض پر شدن کیسه یا رسیدن مایع به فیلتر، مسیر وکیوم به شکل خودکار مسدود می‌شود تا مایعات عفونی وارد شلنگ وکیوم مرکزی یا موتور دستگاه ساکشن نشوند.',
        en: 'Excellent! Abadis is the first manufacturer of shutoff filters in Iran. When fluid reaches the filter, it automatically seals the vacuum path so infectious liquid never enters the central vacuum line or portable suction unit.',
        ar: 'ممتاز! آباديس هي أول مصنّع لفلاتر قطع التدفق في إيران. عند وصول السائل إلى الفلتر، يُغلق مسار الفراغ تلقائيًا لحماية جهاز الشفط والشبكة المركزية.'
      }
    },
    {
      q: {
        fa: 'سؤال ۳ از ۳ (مصاحبه بالینی آکادمی آبادیس):\nدر جراحی‌های سنگین اتاق عمل با حجم مایعات بالا، کدام سایز کیسه ساکشن آبادیس و چه آرایشی پیشنهاد می‌شود؟',
        en: 'Question 3 of 3 (Abadis Academy Clinical Interview):\nFor high-fluid-volume operating room surgeries, which Abadis liner size and configuration is recommended?',
        ar: 'السؤال ٣ من ٣ (المقابلة السريرية لأكاديمية آباديس):\nفي العمليات الجراحية ذات الحجم العالي من السوائل، أي سعة وترتيب لأكياس آباديس يُنصح به؟'
      },
      options: [
        { id: 'q3_a', fa: 'کیسه ۳ لیتری با قابلیت اتصال سری تا ۴ مخزن (۱۲ لیتر) روی ترولی', en: '3 L liners connected in series up to 4 canisters (12 L) on a trolley', ar: 'كيس ٣ لتر مع الربط المتسلسل حتى ٤ خزانات (١٢ لترًا) على ترولي' },
        { id: 'q3_b', fa: 'کیسه ۱ لیتری تکی (مخصوص آمبولانس و دندانپزشکی)', en: 'Single 1 L liner (meant for ambulance & dental)', ar: 'كيس ١ لتر مفرد (للإسعاف والأسنان)' }
      ],
      feedback: {
        fa: 'تبریک! شما مصاحبه بالینی آکادمی آبادیس را با موفقیت کامل کردید. کیسه ۱ لیتری برای آمبولانس و دندانپزشکی، ۲ لیتری برای ICU/CCU و آندوسکوپی، و ۳ لیتری (با قابلیت اتصال سری تا ۴ مخزن / ۱۲ لیتر) برای اتاق عمل طراحی شده است.',
        en: 'Congratulations! You completed the Abadis Academy Clinical Assessment. 1 L is built for ambulance/dental/pediatrics, 2 L for ICU/CCU & endoscopy, and 3 L (connectable in series up to 4 canisters / 12 L) for the Operating Room.',
        ar: 'تهانينا! لقد أتممت التقييم السريري لأكاديمية آباديس بنجاح. سعة ١ لتر للإسعاف والأسنان، و٢ لتر للعناية المركزة والتنظير، و٣ لتر (قابلة للربط المتسلسل حتى ٤ خزانات / ١٢ لترًا) لغرف العمليات.'
      }
    }
  ];

  function estimateBeds(orBeds, icuBeds) {
    var a = Math.max(0, Math.min(700, Math.round(Number(orBeds) || 0)));
    var b = Math.max(0, Math.min(700, Math.round(Number(icuBeds) || 0)));
    var usd = 269500;
    return {
      a: a,
      b: b,
      water: Math.round(((a * 254) + (b * 67)) * 1.6 * 9.971),
      cost: Math.round(((a * 254) + (b * 65)) * 2.5 * usd),
      hours: Math.round(((a * 254) + (b * 67)) * 1.7 * 2.2 * 7.1 / 60)
    };
  }

  function normWord(w) {
    if (!w) return '';
    w = w.replace(/\u200c/g, ' ')
      .replace(/[يئ]/g, 'ی')
      .replace(/ك/g, 'ک')
      .replace(/ة/g, 'ه')
      .replace(/[أإآ]/g, 'ا')
      .replace(/ؤ/g, 'و')
      .replace(/\u0640/g, '');
    if (w === 'centres' || w === 'centers') return 'center';
    if (w === 'surgeries') return 'surgery';
    if (w === 'licences' || w === 'licenses' || w === 'licence') return 'license';
    if (/^[a-z]+$/.test(w) && w.length > 4) {
      if (w.slice(-3) === 'ies') w = w.slice(0, -3) + 'y';
      else if (w.slice(-2) === 'es' && !/(ses|xes|zes|ches|shes)$/.test(w)) w = w.slice(0, -1);
      else if (w.slice(-1) === 's' && w.slice(-2) !== 'ss') w = w.slice(0, -1);
    }
    var faSuf = ['هایمان', 'هایتان', 'هایشان', 'هایی', 'های', 'ها', 'مان', 'تان', 'شان', 'ایه', 'ای', 'اش', 'ات', 'ام'];
    if (/^(قیمت|تفاوت|سایز|حجم|کاربرد|گارانتی|وارانتی|نصب|عمر|جنس|مدل|کد|ابعاد|تعداد|وزن|ظرفیت)ش$/.test(w)) {
      w = w.slice(0, -1);
    }
    for (var i = 0; i < faSuf.length; i++) {
      var s = faSuf[i];
      if (w.length - s.length >= 3 && w.slice(-s.length) === s) {
        w = w.slice(0, -s.length);
        break;
      }
    }
    return w;
  }

  function tokens(s, keepStop) {
    var raw = String(s || '').toLowerCase()
      .replace(/\u200c/g, ' ')
      .replace(/[^\p{L}\p{N}]+/gu, ' ')
      .split(/\s+/);
    var out = [];
    raw.forEach(function (w) {
      if (w.length <= 1) return;
      var nw = normWord(w);
      if (nw.length <= 1) return;
      if (!keepStop && (STOP[w] || STOP[nw])) return;
      out.push(nw);
    });
    if (!out.length && !keepStop) return tokens(s, true);
    return out;
  }

  function expand(words) {
    var extra = [];
    var seen = {};
    words.forEach(function (w) { seen[w] = 1; });
    words.forEach(function (w) {
      SYN.forEach(function (group) {
        var normGroup = group.map(normWord);
        if (normGroup.indexOf(w) === -1) return;
        normGroup.forEach(function (alt) {
          if (!seen[alt]) { seen[alt] = 1; extra.push(alt); }
        });
      });
    });
    return extra;
  }

  function buildIndex() {
    var chunks = (state.kb && state.kb.chunks) || [];
    var docs = [];
    var df = {};
    var total = 0;
    chunks.forEach(function (chunk) {
      var text = chunk.text || {};
      var toks = tokens([text.fa, text.en, text.ar, chunk.keywords].join('\n'));
      var kwToks = tokens(chunk.keywords || '');
      var kwSet = {};
      kwToks.forEach(function (w) { kwSet[w] = 1; });
      var tf = {};
      toks.forEach(function (w) { tf[w] = (tf[w] || 0) + 1; });
      kwToks.forEach(function (w) { tf[w] = (tf[w] || 0) + 2; });
      Object.keys(tf).forEach(function (w) { df[w] = (df[w] || 0) + 1; });
      var len = toks.length || 1;
      total += len;
      docs.push({ chunk: chunk, tf: tf, kwSet: kwSet, len: len });
    });
    index = { docs: docs, df: df, n: docs.length, avg: total / (docs.length || 1) };
  }

  function idf(term) {
    var n = index.df[term] || 0;
    return Math.log(1 + (index.n - n + 0.5) / (n + 0.5));
  }

  function bm25(doc, terms, weight) {
    var k1 = 1.2;
    var b = 0.75;
    var score = 0;
    terms.forEach(function (term) {
      var f = doc.tf[term] || 0;
      if (!f) return;
      var denom = f + k1 * (1 - b + b * doc.len / index.avg);
      score += idf(term) * (f * (k1 + 1) / denom) * weight;
    });
    return score;
  }

  function search(query) {
    if (!index) return null;
    var q = tokens(query);
    if (!q.length) return null;
    var extra = expand(q);
    var best = null;
    var bestScore = 0;
    index.docs.forEach(function (doc) {
      var text = doc.chunk.text || {};
      var langText = text[state.lang] || '';
      var fa = text.fa || '';
      var headToks = tokens((langText.split('\n')[0] || '') + ' ' + (fa.split('\n')[0] || ''));
      var headSet = {};
      headToks.forEach(function (w) { headSet[w] = 1; });
      var score = bm25(doc, q, 2.5) + bm25(doc, extra, 0.9);
      var headHits = 0;
      var docHits = 0;
      q.forEach(function (word) {
        if (doc.tf[word]) docHits += 1;
        if (doc.kwSet && doc.kwSet[word]) score += 5;
        if (headSet[word]) {
          headHits += 1;
          score += 4;
        }
      });
      if (q.length >= 2 && docHits === q.length) score += 8;
      if (q.length >= 2 && headHits === q.length) {
        score += 8;
        if (doc.chunk.section === 'faq') score += 4;
      }
      if (score > bestScore) { bestScore = score; best = doc.chunk; }
    });
    return bestScore > 0 ? best : null;
  }

  function fmtMd(s) {
    return esc(s)
      .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
      .replace(/\n/g, '<br>');
  }

  function composeWarmLead(hit) {
    if (state.lang === 'en') {
      if (hit.section === 'faq') return 'Here is the exact answer based on Abadis Medical’s technical guide:\n';
      if (hit.section === 'catalog') return 'Here are the details on this Abadis product group:\n';
      if (hit.section === 'solutions') return 'Regarding this Abadis clinical solution:\n';
      if (hit.section === 'calculator') return 'Here is how our hospital savings calculator works:\n';
      return '';
    }
    if (state.lang === 'ar') {
      if (hit.section === 'faq') return 'إليك الإجابة الدقيقة وفق الدليل الفني لآباديس:\n';
      return '';
    }
    if (hit.section === 'faq') {
      var lines = (hit.text && hit.text.fa || '').split('\n');
      if (lines.length > 1) {
        return '**' + lines[0].trim() + '**\n' + lines.slice(1).join('\n').trim() + '\n\nاگر درباره جزئیات فنی یا نحوه سفارش سؤال دیگری دارید، در خدمتم.';
      }
    }
    if (hit.section === 'catalog') return 'خوشبختانه این محصول در سبد تولیدات دانش‌بنیان آبادیس قرار دارد:\n';
    if (hit.section === 'solutions') return 'در رویکرد راهکارمحور آبادیس، این حوزه به شکل زیر طراحی شده است:\n';
    return '';
  }

  function synthesize(hit) {
    state.lastHit = hit;
    var body = textOf(hit.text);
    if (state.lang === 'fa' && hit.section === 'faq') {
      var customFaq = composeWarmLead(hit);
      if (customFaq) {
        var u1 = urlOf(hit.url);
        return fmtMd(customFaq) + linkLine(u1, u1) + ctaLine();
      }
    }
    var lead = composeWarmLead(hit);
    var shown = body;
    if (shown.length > 820) {
      shown = shown.slice(0, 820);
      var cut = Math.max(shown.lastIndexOf('.'), shown.lastIndexOf('؟'), shown.lastIndexOf('?'));
      if (cut > 400) shown = shown.slice(0, cut + 1);
      else shown = shown.replace(/\s+\S*$/, '') + '…';
    }
    var tail = state.lang === 'en'
      ? '\n\nWould you like me to calculate your hospital’s annual savings or connect you with sales for a proforma invoice?'
      : state.lang === 'ar'
      ? '\n\nهل ترغب في حساب التوفير السنوي لمستشفاك أو طلب فاتورة أولية؟'
      : '\n\nاگر مایل باشید می‌توانم صرفه‌جویی سالانه مرکز درمانی شما را هم محاسبه کنم یا راهنمای دریافت پیش‌فاکتور را برایتان بفرستم.';
    var url = urlOf(hit.url);
    return fmtMd(lead + shown + tail) + linkLine(url, url) + ctaLine();
  }

  function showQuickPrompts() {
    var prompts = state.lang === 'en' ? [
      { id: 'What products does Abadis manufacture?', en: 'All Products' },
      { id: 'How do we get a price quote and proforma?', en: 'Pricing & Quote' },
      { id: 'Why are closed-system disposable liners better than traditional glass bottles?', en: 'Closed vs Glass' },
      { id: 'Start Academy clinical interview', en: 'Academy Interview' }
    ] : state.lang === 'ar' ? [
      { id: 'ما هي منتجات آباديس؟', ar: 'جميع المنتجات' },
      { id: 'أسعار وسعات أكياس الشفط', ar: 'الأسعار والسعات' },
      { id: 'لماذا يتفوق نظام الشفط المغلق على القوارير الزجاجية؟', ar: 'المغلق مقابل الزجاجي' },
      { id: 'ابدأ مقابلة الأكاديمية', ar: 'مقابلة الأكاديمية' }
    ] : [
      { id: 'محصولات آبادیس چیست؟', fa: 'معرفی همه محصولات' },
      { id: 'قیمت و حجم‌های کیسه ساکشن چنده؟', fa: 'قیمت و پیش‌فاکتور' },
      { id: 'چرا ساکشن مدار بسته بهتر از شیشه‌ایه؟', fa: 'مقایسه با شیشه سنتی' },
      { id: 'شروع مصاحبه بالینی آکادمی', fa: 'مصاحبه بالینی آکادمی' }
    ];
    choiceEl.textContent = '';
    prompts.forEach(function (item) {
      var b = el('button', 'abadis-chat-choice');
      b.type = 'button';
      b.textContent = item[state.lang] || item.fa || item.en;
      b.addEventListener('click', function () { ask(item.id); });
      choiceEl.appendChild(b);
    });
  }

  function startQuiz(stepIndex) {
    state.quizStep = stepIndex;
    var step = ACADEMY_QUIZ[stepIndex];
    if (!step) {
      state.quizStep = null;
      return;
    }
    var msg = esc(textOf(step.q)).replace(/\n/g, '<br>');
    addMsg('bot', msg);
    choiceEl.textContent = '';
    step.options.forEach(function (opt) {
      var b = el('button', 'abadis-chat-choice');
      b.type = 'button';
      b.textContent = opt[state.lang] || opt.fa;
      b.addEventListener('click', function () {
        addMsg('user', esc(opt[state.lang] || opt.fa));
        var fb = esc(textOf(step.feedback)).replace(/\n/g, '<br>');
        addMsg('bot', fb);
        if (stepIndex + 1 < ACADEMY_QUIZ.length) {
          startQuiz(stepIndex + 1);
        } else {
          state.quizStep = null;
          showQuickPrompts();
        }
      });
      choiceEl.appendChild(b);
    });
  }

  function conversationalReply(query) {
    var raw = String(query || '').trim();
    var q = raw.toLowerCase()
      .replace(/\u200c/g, ' ')
      .replace(/[يئ]/g, 'ی')
      .replace(/ك/g, 'ک')
      .replace(/ة/g, 'ه')
      .replace(/[أإآ]/g, 'ا')
      .replace(/[؟?!.,،؛]+/g, ' ')
      .replace(/\s+/g, ' ')
      .trim();

    var numNorm = q.replace(/[۰-۹]/g, function (d) { return '۰۱۲۳۴۵۶۷۸۹'.indexOf(d); })
      .replace(/[٠-٩]/g, function (d) { return '٠١٢٣٤٥٦٧٨٩'.indexOf(d); });

    // 0. Multi-turn conversational follow-ups
    if (/^(بیشتر توضیح بده|بیشتر بگو|جزئیات بیشتر|توضیح بیشتر|ادامه بده|tell me more|more details|explain more)$/.test(q) && state.lastHit) {
      var fullBody = textOf(state.lastHit.text);
      var fUrl = urlOf(state.lastHit.url);
      addMsg('bot', fmtMd(fullBody) + linkLine(fUrl, fUrl) + ctaLine());
      return true;
    }
    if (/^(چطور سفارش بدم|چگونه سفارش دهم|نحوه سفارش|نحوه خرید|چطور بخرم|شرایط خرید|سفارش خرید|how to order|how do i buy|how to buy)$/.test(q)) {
      var ordHit = findChunk('pricing-and-ordering') || findChunk('flow-tender');
      if (ordHit) { addMsg('bot', synthesize(ordHit)); return true; }
    }

    if (/کارتن|بسته بندی|بستهبندی|carton|per box|how many in a box/.test(q) && !/وسیله نقلیه|خاور|وانت|نیسان|کامیون/.test(q)) {
      var cartTxt = state.lang === 'en'
        ? '**Abadis Carton Packaging & Dimensions:**\n• **Disposable Suction Liners (1 L, 2 L, 3 L):** **45 liners per carton** (liners with a mechanical filter: **30 per carton**).\n• **Suction Tubes (CH25, CH30, CH35):** **100 tubes per carton**.\n• **Carton Dimensions:** 1 L & 2 L: 57.5 × 42.5 × 44 cm | 3 L: 49 × 49 × 49 cm | Suction tube: 59 × 44.5 × 43.5 cm.'
        : state.lang === 'ar'
        ? '**تعبئة وأبعاد كراتين منتجات آباديس:**\n• **أكياس الشفط ذات الاستعمال الواحد (١، ٢، ٣ لتر):** **٤٥ كيسًا في كل كرتون** (الكيس بفلتر ميكانيكي: ٣٠ في الكرتون).\n• **أنابيب الشفط (CH25، CH30، CH35):** **١٠٠ أنبوب في الكرتون**.'
        : '**تعداد در کارتن و ابعاد بسته‌بندی محصولات آبادیس:**\n• **کیسه ساکشن یکبارمصرف (۱، ۲ و ۳ لیتری):** در هر کارتن **۴۵ عدد** قرار دارد (مدل دارای فیلتر مکانیکی: **۳۰ عدد** در کارتن).\n• **ساکشن تیوب (CH25، CH30، CH35):** در هر کارتن **۱۰۰ عدد** قرار دارد.\n• **ابعاد کارتن‌ها:** کیسه ۱ و ۲ لیتری: ۴۴×۴۲٫۵×۵۷٫۵ سانتی‌متر | کیسه ۳ لیتری: ۴۹×۴۹×۴۹ سانتی‌متر | ساکشن تیوب: ۴۳٫۵×۴۴٫۵×۵۹ سانتی‌متر.';
      addMsg('bot', fmtMd(cartTxt) + linkLine('/faq/', '/faq/') + ctaLine());
      return true;
    }

    // 1. Academy interactive interview / quiz trigger
    if (/^(شروع مصاحبه|مصاحبه بالینی|مصاحبه اکادمی|ازمون بالینی|کوییز|تست بالینی|امتحان|start academy|clinical interview|academy interview|start quiz|quiz|مقابله الاکادیمیه|ابدا مقابله)/.test(q) || /مصاحبه.*اکادمی|اکادمی.*مصاحبه|interview.*academy|academy.*interview/.test(q)) {
      startQuiz(0);
      return true;
    }

    // 2. Bed-count savings calculation in chat (e.g. "بیمارستان ۲۰۰ تخت", "10 تخت اتاق عمل و 20 تخت ICU")
    if (/تخت|bed|سریر|سرير/.test(numNorm)) {
      var nums = numNorm.match(/\d+/g);
      if (nums && nums.length >= 1) {
        var n1 = parseInt(nums[0], 10);
        var n2 = nums.length >= 2 ? parseInt(nums[1], 10) : 0;
        var orB = n1, icuB = n2;
        if (nums.length === 1 && n1 > 30) {
          orB = Math.max(2, Math.round(n1 * 0.08));
          icuB = Math.max(4, Math.round(n1 * 0.15));
        }
        var br = estimateBeds(orB, icuB);
        var calcUrl = (state.kb && state.kb.calculator && urlOf(state.kb.calculator.url)) || '/dial-practical/';
        var bedTxt = state.lang === 'en'
          ? ('For ' + fmt(br.a, 'en') + ' OR beds and ' + fmt(br.b, 'en') + ' ICU beds per year: switching to Abadis closed-system suction liners saves approximately ' + fmt(br.water, 'en') + ' litres of water, ' + fmt(br.cost, 'en') + ' toman in washing & disinfectant costs, and ' + fmt(br.hours, 'en') + ' nursing/staff hours per year (cap: 15,000 surgeries; no CO₂ metric).')
          : state.lang === 'ar'
          ? ('لمركز يضم ' + fmt(br.a, 'ar') + ' سرير عمليات و' + fmt(br.b, 'ar') + ' سرير عناية مركزة سنويًا: يحقق نظام الشفط المغلق من آباديس توفيرًا يقارب ' + fmt(br.water, 'ar') + ' لتر ماء، و' + fmt(br.cost, 'ar') + ' تومان من تكاليف الغسل والتعقيم، و' + fmt(br.hours, 'ar') + ' ساعة من وقت الكادر الطبي سنويًا.')
          : ('برآورد صرفه‌جویی سالانه برای ' + fmt(br.a, 'fa') + ' تخت اتاق عمل و ' + fmt(br.b, 'fa') + ' تخت ویژه (ICU/CCU):\n• صرفه‌جویی در مصرف آب: حدود ' + fmt(br.water, 'fa') + ' لیتر در سال\n• کاهش هزینه شست‌وشو و مواد ضدعفونی: حدود ' + fmt(br.cost, 'fa') + ' تومان در سال\n• آزادسازی زمان کادر درمان: حدود ' + fmt(br.hours, 'fa') + ' ساعت در سال\n(طبق فرمول محاسبه‌گر عملی آبادیس؛ بدون لحاظ CO₂ و کیلوگرم پلاستیک).');
        addMsg('bot', fmtMd(bedTxt) + linkLine(calcUrl, calcUrl) + ctaLine());
        return true;
      }
    }

    // 3. Broad "What products does Abadis have?" overview
    if (/^(محصولات|محصولات ابادیس|محصولات شرکت|لیست محصولات|سبد محصولات|چه محصولاتی دارید|چه تولید میکنید|تولیدات ابادیس|all products|what products|product list|your products|ما هي منتجات|منتجات اباديس)$/.test(q) || (/محصولات/.test(q) && q.split(' ').length <= 4 && !/کد|قیمت|گارانتی|کارتن/.test(q))) {
      var prodText = state.lang === 'en'
        ? 'Abadis Medical manufactures a complete closed-system hospital fluid & airway management portfolio:\n1. Disposable Suction Liners (1 L, 2 L, 3 L — with hydrophobic shutoff filter & optional solidifying powder) and unbreakable Polycarbonate Canisters\n2. Suction Tubes (CH25, CH30, CH35 — clear & ribbed, with or without fingertip control)\n3. Respiratory & Airway Care (disposable suction toothbrush, endotracheal-tube holder)\n4. Vacuum & ICU Accessories (VR-A1 adult & VR-B1 pediatric vacuum regulators, antibacterial & shutoff filters)\n5. Connectors & Stands (600 ml polypropylene receiver, T-connector, silicone tubing, ON/OFF valve, wall/portable clamps, cascade trolley for up to 4 canisters / 12 L).'
        : state.lang === 'ar'
        ? 'تنتج شركة خزانات آباديس الطبية منظومة متكاملة لإدارة السوائل والطريق الهوائي في المستشفيات:\n١. أكياس الشفط ذات الاستعمال الواحد (١ و٢ و٣ لتر مع فلتر قطع التدفق ومسحوق التصلب) وخزانات البولي كربونات\n٢. أنابيب الشفط (CH25، CH30، CH35)\n٣. منتجات العناية بالطريق الهوائي (فرشاة الشفط وحامل أنبوب القصبة)\n٤. منظمات الفراغ للكبار والأطفال (VR-A1 / VR-B1) والفلاتر المضادة للبكتيريا\n٥. الملحقات والوصلات وحوامل الترولي (حتى ٤ خزانات على التسلسل).'
        : 'سبد محصولات تخصصی شرکت دانش‌بنیان مخازن طبی آبادیس شامل ۵ گروه اصلی است:\n۱. کیسه‌های ساکشن یکبارمصرف (در سه سایز ۱، ۲ و ۳ لیتری مجهز به فیلتر قطع‌کننده جریان و پودر جاذب) و مخازن ثابت پلی‌کربنات نشکن\n۲. ابزار ساکشن (ساکشن تیوب شفاف و شیاردار در سایزهای CH25، CH30 و CH35 با و بدون فینگرتیپ)\n۳. مراقبت تنفسی و راه هوایی (مسواک ساکشن یکبارمصرف و نگهدارنده لوله تراشه)\n۴. ملزومات بیهوشی، ICU و مدار وکیوم (رگولاتور ساکشن بزرگسال VR-A1 و اطفال VR-B1، فیلتر آنتی‌باکتریال و فیلتر هیدروفوبیک)\n۵. ملزومات عمومی، اتصالات و پایه‌ها (رسیور ۶۰۰ میلی‌لیتر، اتصال T، کانکتور، شلنگ سیلیکونی، شیر ON/OFF، گیره دیواری و ترولی سری تا ۴ مخزن / ۱۲ لیتر).';
      addMsg('bot', fmtMd(prodText) + linkLine('/products/', '/products/') + ctaLine());
      showQuickPrompts();
      return true;
    }

    // 4. Greetings & Salutations (only when the message is primarily a greeting/small-talk, not a domain question starting with سلام)
    var domainWords = /کیسه|مخزن|ساکشن|فیلتر|تیوب|رگولاتور|پودر|قیمت|خرید|فاکتور|کارتن|گارانتی|وارانتی|نصب|زاگرس|بلوط|مراکز|رضایت|امار|تاسیس|گواهی|مجوز|ایزو|imed|iso|فلسفه|راهکار|شیشه|تخت|عمل|جراحی|اینترنت|فیلترینگ|تلفن|شماره|ادرس|کارخانه|نمایند|کاتالوگ|اورولوژی|گوارش|زنان|بیهوشی|مسواک|تراشه|liner|canister|suction|filter|tube|price|quote|zagros|certificate|solution|glass|surgery|hospital|intranet|contact|address|catalog|dealer|شهاده|كيس|خزان|سعر|زاغروس|مستشفي/;
    if (!domainWords.test(q)) {
      if (/^(سلام|درود|وقت بخیر|صبح بخیر|عصر بخیر|شب بخیر|خسته نباشید|قوت اله|سلام علیکم|علیکم السلام|های|هلو|salam|salaam|hi|hello|hey|good morning|good afternoon|good evening|greetings|مرحبا|اهلا|أهلا|السلام علیکم|صباح الخیر|مساء الخیر)(\s|$)/.test(q)) {
        var greetTxt = state.lang === 'en'
          ? (state.mode === 'academy'
            ? 'Hello and welcome to the Abadis Academy Assistant! 👋\nI run 100% on the website’s core engine (resilient on Iran’s National Information Network) and can help you with:\n• Clinical evidence for closed-system suction vs. traditional glass bottles\n• Interactive 3-step Clinical Assessment / Interview\n• Shutoff & antibacterial filter specifications and installation\n• Certificates (IMED, Patents, ISO 13485 / GMP) & Save Zagros CSR.\n\nAsk any question below or click one of the topics:'
            : 'Hello and welcome to Abadis Medical! 👋\nI am your Sales & Clinical Solutions Assistant (running 100% on the on-site core engine with zero foreign internet dependency). I can help you right now with:\n• Choosing the right suction liner volume (1 L, 2 L, 3 L) and accessories for your ward\n• Pricing, carton counts (45 pcs), and instant Proforma Invoice (پیش‌فاکتور) guidance\n• Calculating your hospital’s annual water, cost, and nursing-hour savings (up to 15,000 surgeries)\n• Exploring our 5 Clinical Solutions & 1,232+ active healthcare centers.\n\nType your question or choose a quick action below:')
          : state.lang === 'ar'
          ? 'أهلاً ومرحباً بكم في شركة خزانات آباديس الطبية! 👋\nأنا المساعد الذكي للمبيعات والأكاديمية (يعمل بالكامل داخل نواة الموقع وبدون حاجة للإنترنت الدولي). يمكنني مساعدتكم في:\n• اختيار سعة أكياس الشفط (١، ٢، ٣ لتر) وملحقاتها حسب القسم السريري\n• الأسعار، الفاتورة الأولية، وحساب التوفير السنوي للمستشفى (حتى ١٥٬٠٠٠ عملية)\n• الشهادات المعتمدة (IMED، براءات الاختراع، ISO 13485) ومبادرة إنقاذ زاغروس.\n\nاكتب سؤالك أو اختر أحد المواضيع أدناه:'
          : (state.mode === 'academy'
            ? 'سلام و وقت بخیر! به دستیار هوشمند آکادمی آبادیس خوش آمدید 👋\nمن روی موتور بومی هسته سایت (۱۰۰٪ پایدار در شبکه ملی اطلاعات) اجرا می‌شوم و در این بخش می‌توانم در موارد زیر کمکتان کنم:\n• مقایسه علمی سیستم ساکشن مدار بسته یکبارمصرف با شیشه‌های سنتی و کنترل عفونت بیمارستانی\n• اجرای «مصاحبه و ارزیابی بالینی تعاملی آکادمی» (۳ مرحله‌ای)\n• عملکرد فیلتر قطع‌کننده جریان (هیدروفوبیک)، فیلتر آنتی‌باکتریال و پودر جاذب\n• گواهینامه‌ها (IMED، ثبت اختراع، ISO 13485 / GMP)، مقالات علمی و پویش نجات زاگرس.\n\nهر سؤالی دارید بپرسید یا یکی از گزینه‌های زیر را انتخاب کنید:'
            : 'سلام و وقت بخیر! به دستیار هوشمند فروش و راهکارهای بالینی آبادیس خوش آمدید 👋\nمن روی موتور بومی هسته سایت (فعال در شبکه ملی اطلاعات و بدون نیاز به اینترنت بین‌الملل) کار می‌کنم و آماده راهنمایی شما هستم:\n• انتخاب حجم مناسب کیسه ساکشن (۱، ۲ و ۳ لیتر)، مخازن پلی‌کربنات، تیوب و رگولاتور بر اساس بخش بیمارستانی\n• اطلاع از شرایط خرید، تعداد در کارتن (۴۵ عدد) و دریافت پیش‌فاکتور رسمی\n• محاسبه آنی صرفه‌جویی سالانه بیمارستان شما در مصرف آب، هزینه ضدعفونی و زمان پرستاران (تا سقف ۱۵٬۰۰۰ عمل)\n• معرفی ۵ راهکار بالینی، گواهینامه‌ها و آمار ۱٬۲۳۲ مرکز درمانی فعال.\n\nسؤال خود را بنویسید یا یکی از گزینه‌های زیر را بزنید:');
        addMsg('bot', fmtMd(greetTxt) + ctaLine());
        showQuickPrompts();
        return true;
      }

      if (/^(چطوری|حالت چطوره|خوبی|احوالت چطوره|چه خبر|خوب هستی|چطورین|how are you|how is it going|how are things|whats up|کیف حالک|كيف حالك|اخبارک)/.test(q)) {
        var howTxt = state.lang === 'en'
          ? 'I am doing great and ready to help! 😊 As Abadis Medical’s on-site assistant, I have the full product catalog, clinical solutions, calculator formulas, and FAQ loaded right here. What ward or product can I help you with today?'
          : state.lang === 'ar'
          ? 'بخير والحمد لله، وجاهز لخدمتكم! 😊 قاعدة معرفة آباديس الكاملة متوفرة لدي هنا. كيف يمكنني مساعدتكم اليوم؟'
          : 'ممنون از لطف شما، عالی هستم و آماده پاسخگویی! 😊 تمام اطلاعات محصولات، ۵ راهکار بالینی، محاسبه‌گر صرفه‌جویی و دانش‌نامه فنی آبادیس در هسته سایت آماده است. درباره کدام محصول یا بخش بیمارستانی سؤال دارید؟';
        addMsg('bot', fmtMd(howTxt));
        showQuickPrompts();
        return true;
      }

      if (/کی هستی|معرفی کن|چیکار میکنی|چه کاری بلدی|چه کمکی|هوش مصنوعی|ربات|بات|مدل تو چیه|who are you|what are you|what can you do|help|راهنمایی|کمک|من انت|ما دورک|مساعده/.test(q)) {
        var whoTxt = state.lang === 'en'
          ? 'I am the **Abadis Medical Core AI Assistant** (Sales Advisor & Academy Assistant).\n• **Architecture:** 3-Tier Engine with a 100% self-contained On-Site Core (Tier 1) that runs inside the website without needing international internet or foreign CDNs, plus optional Domestic Iran LLM (Tier 2) and International API (Tier 3) hooks.\n• **Capabilities:** Product configuration (1L/2L/3L liners, canisters, tubes, filters, airway care), hospital savings calculations (water, cost, staff hours), clinical solution guidance, Academy interactive interviews, and technical FAQ support.'
          : state.lang === 'ar'
          ? 'أنا المساعد الذكي الأساسي لشركة خزانات آباديس الطبية (مستشار المبيعات والأكاديمية). أعمل عبر محرك محلي مدمج في نواة الموقع (الطبقة ١) يعمل ١٠٠٪ على الشبكة الوطنية دون حاجة لإنترنت دولي، وأقدم استشارات المنتجات، الحلول السريرية، حساب التوفير، والمقابلة التفاعلية للأكاديمية.'
          : 'من «دستیار هوشمند مشاور فروش و آکادمی آبادیس» هستم.\n• معماری پایدار در شبکه ملی اطلاعات: موتور اصلی من (لایه ۱) ۱۰۰٪ در هسته خود وب‌سایت آبادیس روی دانش‌نامه رسمی شرکت اجرا می‌شود و حتی در صورت قطع کامل اینترنت بین‌الملل بدون وقفه کار می‌کند (به همراه پشتیبانی از لایه ۲ مدل داخلی ایران و لایه ۳ بین‌المللی).\n• قابلیت‌ها: مشاوره انتخاب محصول و راهکار بالینی، محاسبه آنی صرفه‌جویی آب/هزینه/ساعت پرستاری برای بیمارستان شما، برگزاری مصاحبه تعاملی آکادمی، و پاسخ به ۲۹ پرسش فنی و بازرگانی.';
        addMsg('bot', fmtMd(whoTxt) + ctaLine());
        showQuickPrompts();
        return true;
      }

      if (/^(ممنون|مرسی|دمت گرم|تشکر|سپاس|سپاسگزارم|عالی|خسته نباشی|خداحافظ|فعلا|بدرود|thanks|thank you|thx|great|awesome|bye|goodbye|شکرا|شكرا|مع السلامه|جزاك)/.test(q)) {
        var thxTxt = state.lang === 'en'
          ? 'You’re very welcome! 🙏 Whenever you need a proforma invoice, sample request, or technical support, our team is available at 021-92001017 (Ext. 11) or on WhatsApp (+989100145809).'
          : state.lang === 'ar'
          ? 'على الرحب والسعة! 🙏 يسعدنا تواصلكم مع قسم المبيعات على الرقم 02192001017 (تحويلة 11) أو عبر واتساب +989100145809.'
          : 'خواهش می‌کنم، خوشحالم که توانستم کمکتان کنم! 🙏 هر زمان برای دریافت پیش‌فاکتور، درخواست نمونه یا مشاوره فنی نیاز به همراهی داشتید، کارشناسان فروش آبادیس با شماره ۰۲۱-۹۲۰۰۱۰۱۷ (داخلی ۱۱) و واتس‌اپ +۹۸۹۱۰۰۱۴۵۸۰۹ در کنار شما هستند.';
        addMsg('bot', fmtMd(thxTxt) + ctaLine());
        return true;
      }
    }

    return false;
  }

  function tryLiveAiFallback(query, fallbackHtml) {
    var bubble = addMsg('bot', '<span class="abadis-chat-typing">' + (state.lang === 'en' ? 'Typing…' : state.lang === 'ar' ? 'جاري الكتابة…' : 'در حال نوشتن…') + '</span>');
    var ctrl = typeof AbortController === 'function' ? new AbortController() : null;
    var timer = setTimeout(function () { if (ctrl) ctrl.abort(); }, 3500);
    var sys = 'تو دستیار هوشمند شرکت دانش‌بنیان مخازن طبی آبادیس هستی. طبیعی، گرم، کوتاه و دقیق به فارسی پاسخ بده. اطلاعات مرجع: کیسه ساکشن یکبارمصرف آبادیس در ۳ سایز ۱، ۲ و ۳ لیتر (هر کارتن ۴۵ عدد) با فیلتر هیدروفوبیک قطع‌کننده جریان و پودر جاذب، مخازن پلی‌کربنات، تیوب ساکشن CH25/CH30/CH35، مسواک ساکشن، نگهدارنده لوله تراشه، رگولاتور وکیوم، ۱٬۲۳۲ مرکز درمانی فعال (۱٬۲۹۴ بیمارستان و مرکز جراحی در نقشه خانواده سبز)، ۹۸.۹۹٪ رضایت، ۰.۰۰۱۸٪ خرابی، سال تأسیس ۱۳۹۶/2017، تلفن فروش ۰۲۱-۹۲۰۰۱۰۱۷ داخلی ۱۱، واتس‌اپ +۹۸۹۱۰۰۱۴۵۸۰۹.';
    var url = 'https://text.pollinations.ai/' + encodeURIComponent(query) + '?model=openai&system=' + encodeURIComponent(sys);
    var opts = { method: 'GET' };
    if (ctrl) opts.signal = ctrl.signal;
    fetch(url, opts).then(function (r) {
      if (!r.ok) throw new Error('http');
      return r.text();
    }).then(function (txt) {
      clearTimeout(timer);
      var clean = String(txt || '').trim();
      if (clean && clean.length > 10 && clean.indexOf('<!DOCTYPE') === -1) {
        bubble.innerHTML = fmtMd(clean) + ctaLine();
      } else {
        bubble.innerHTML = fallbackHtml;
      }
      showQuickPrompts();
    }).catch(function () {
      clearTimeout(timer);
      bubble.innerHTML = fallbackHtml;
      showQuickPrompts();
    });
  }

  function answerSearch(query) {
    var hit = search(query);
    if (!hit) {
      var fallbackHtml = fmtMd(t().empty) + '<br>' + ctaLine();
      if (!state.cutoff) {
        tryLiveAiFallback(query, fallbackHtml);
      } else {
        addMsg('bot', fallbackHtml);
        showQuickPrompts();
      }
      return;
    }
    var body = textOf(hit.text);
    addMsg('bot', synthesize(hit));
    showQuickPrompts();
    maybeEnrich(query, body);
  }

  function maybeEnrich(query, context) {
    if (state.tier === 'core') return;
    if (state.tier === 'intl' && state.cutoff) {
      addMsg('bot', esc(t().cutoffNote));
      return;
    }
    var url = state.tier === 'domestic' ? domesticEl.value.trim() : intlEl.value.trim();
    var key = keyEl.value.trim();
    if (!url || (state.tier === 'intl' && !key)) {
      addMsg('bot', esc(t().tierFail));
      return;
    }
    var ctrl = typeof AbortController === 'function' ? new AbortController() : null;
    var timer = setTimeout(function () { if (ctrl) ctrl.abort(); }, TIER_MS);
    var headers = { 'Content-Type': 'application/json' };
    if (key) headers.Authorization = 'Bearer ' + key;
    var payload = {
      model: 'local',
      messages: [
        { role: 'system', content: 'Answer only from the Abadis context. If the context is silent, say so. Do not invent certificates, prices, or founding years.' },
        { role: 'user', content: 'Context:\n' + context + '\n\nQuestion:\n' + query }
      ]
    };
    var opts = { method: 'POST', headers: headers, body: JSON.stringify(payload) };
    if (ctrl) opts.signal = ctrl.signal;
    fetch(url, opts).then(function (r) {
      if (!r.ok) throw new Error('http');
      return r.json();
    }).then(function (data) {
      var msg = data && data.choices && data.choices[0] && data.choices[0].message && data.choices[0].message.content;
      if (msg) addMsg('bot', esc(msg).replace(/\n/g, '<br>'));
      else addMsg('bot', esc(state.tier === 'intl' ? t().intlFallback : t().tierFail));
    }).catch(function () {
      addMsg('bot', esc(state.tier === 'intl' ? t().intlFallback : t().tierFail));
    }).then(function () { clearTimeout(timer); });
  }

  var WIZARD_SHORTCUTS = {
    'راهکار مدیریت مایعات': { type: 'solution', id: 'fluid' },
    'کیسه ۲ لیتری برای icu': { type: 'volume', id: '2' },
    'fluid management solution': { type: 'solution', id: 'fluid' },
    '2 litre liner for icu': { type: 'volume', id: '2' },
    'حل إدارة السوائل': { type: 'solution', id: 'fluid' },
    'كيس ٢ لتر لـ icu': { type: 'volume', id: '2' }
  };

  function intent(query) {
    var q = query.trim().toLowerCase();
    var n = query.replace(/[۰-۹]/g, function (d) { return '۰۱۲۳۴۵۶۷۸۹'.indexOf(d); })
      .replace(/[٠-٩]/g, function (d) { return '٠١٢٣٤٥٦٧٨٩'.indexOf(d); });
    var surg = n.match(/(\d{3,5})/);
    if (/صرف|saving|توفير|عمل|جراحی|surger/.test(q) && surg && !/سال\s*13|سال\s*20|1396|1397|2017|13485/.test(n)) {
      return { type: 'savings', n: surg[1] };
    }
    if (WIZARD_SHORTCUTS[q]) return WIZARD_SHORTCUTS[q];
    return null;
  }

  function runQuery(query) {
    if (conversationalReply(query)) return;
    var hit = intent(query);
    if (hit && hit.type === 'savings') {
      onChoice('savings', { id: hit.n, fa: hit.n, en: hit.n, ar: hit.n });
      return;
    }
    if (state.mode === 'sales' && hit) {
      if (hit.type === 'volume') {
        onChoice('volume', { id: hit.id, fa: hit.id + ' L', en: hit.id + ' L', ar: hit.id + ' L' });
        return;
      }
      if (hit.type === 'solution') {
        var sol = null;
        SOLUTIONS.forEach(function (s) { if (s.id === hit.id) sol = s; });
        if (sol) { onChoice('solution', sol); return; }
      }
    }
    answerSearch(query);
  }

  function ask(query) {
    open();
    addMsg('user', esc(query));
    if (!state.kb) {
      if (window.ABADIS_KB && applyKb(window.ABADIS_KB, 'embedded', true)) {
        runQuery(query);
        return;
      }
      state.pending = state.pending || [];
      state.pending.push(query);
      return;
    }
    runQuery(query);
  }

  function resetThread() {
    logEl.textContent = '';
    choiceEl.textContent = '';
    addMsg('bot', esc(state.mode === 'academy' ? t().welcomeAcademy : t().welcomeSales));
    if (state.mode === 'sales') {
      showChoices([
        { id: 'solution', fa: t().bySolution, en: t().bySolution, ar: t().bySolution },
        { id: 'product', fa: t().byProduct, en: t().byProduct, ar: t().byProduct }
      ], 'path');
    }
  }

  function setLang(lang) {
    if (!I18N[lang]) lang = 'fa';
    state.lang = lang;
    try { sessionStorage.setItem('abadis-chat-lang', lang); } catch (e) {}
    paintChrome();
    resetThread();
    if (demo) {
      document.documentElement.lang = root.lang;
      document.documentElement.dir = root.dir;
      document.dispatchEvent(new CustomEvent('abadis-chat-lang', { detail: lang }));
    }
  }

  function setMode(mode) {
    state.mode = mode === 'academy' ? 'academy' : 'sales';
    root.dataset.mode = state.mode;
    paintChrome();
    resetThread();
  }

  function open() {
    state.open = true;
    panel.hidden = false;
    root.querySelector('.abadis-chat-launcher').setAttribute('aria-expanded', 'true');
  }
  function close() {
    if (root.classList.contains('is-docked')) return;
    state.open = false;
    panel.hidden = true;
    root.querySelector('.abadis-chat-launcher').setAttribute('aria-expanded', 'false');
  }

  function dock(host) {
    if (!host) return;
    host.appendChild(root);
    root.classList.add('is-docked');
    open();
  }
  function float() {
    document.body.appendChild(root);
    root.classList.remove('is-docked');
  }

  function engineState() {
    var L = t();
    var tierName = state.tier === 'domestic' ? L.tier2short : state.tier === 'intl' ? L.tier3short : L.tier1short;
    var bits = [tierName];
    if (state.cutoff) bits.push(L.cutoffShort);
    if (state.kbSource === 'embedded') bits.push(L.embeddedSrc);
    return { tier: state.tier, cutoff: state.cutoff, kbSource: state.kbSource, status: bits.join(' · ') };
  }

  function emitEngine() {
    document.dispatchEvent(new CustomEvent('abadis-chat-engine', { detail: engineState() }));
  }

  function setTier(tier) {
    state.tier = tier === 'domestic' || tier === 'intl' ? tier : 'core';
    paintChrome();
  }

  function setCutoff(on) {
    state.cutoff = !!on;
    paintChrome();
  }

  function applyKb(data, source, keepLog) {
    if (!data || !data.chunks) return false;
    var hadKb = !!state.kb;
    state.kb = data;
    state.kbSource = source;
    buildIndex();
    if (!keepLog && !hadKb && (!state.pending || !state.pending.length)) {
      resetThread();
    }
    paintChrome();
    if (state.pending && state.pending.length) {
      var qList = state.pending.slice();
      state.pending = [];
      qList.forEach(function (q) { runQuery(q); });
    }
    return true;
  }

  function fallbackSrc() {
    if (script && script.src) return script.src.replace(/chatbot\.js(?:\?.*)?$/, 'kb-fallback.js');
    return '/assets/chatbot/kb-fallback.js';
  }

  function loadEmbedded() {
    if (applyKb(window.ABADIS_KB, 'embedded')) return;
    var node = document.createElement('script');
    node.src = fallbackSrc();
    node.onload = function () {
      if (!applyKb(window.ABADIS_KB, 'embedded')) addMsg('bot', esc(t().empty));
    };
    node.onerror = function () { addMsg('bot', esc(t().empty)); };
    document.head.appendChild(node);
  }

  build();
  if (window.ABADIS_KB) {
    applyKb(window.ABADIS_KB, 'embedded');
  }
  fetch(kbUrl, { credentials: 'omit' }).then(function (r) {
    if (!r.ok) throw new Error('kb');
    return r.json();
  }).then(function (data) {
    if (!applyKb(data, 'site-json', true)) throw new Error('kb');
  }).catch(loadEmbedded);

  window.AbadisChat = {
    open: open,
    close: close,
    setLang: setLang,
    setMode: setMode,
    ask: ask,
    dock: dock,
    float: float,
    setTier: setTier,
    setCutoff: setCutoff,
    engine: engineState
  };
})();
