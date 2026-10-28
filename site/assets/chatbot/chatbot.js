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
      launcher: 'گفتگو با آبادیس',
      title: 'پشتیبانی و مشاور آبادیس',
      subSales: 'پاسخگوی فروش و راهکارهای بالینی',
      subAcademy: 'پرسش‌وپاسخ و آموزش آکادمی آبادیس',
      tabSales: 'مشاور فروش',
      tabAcademy: 'آکادمی',
      placeholder: 'سؤال یا نیاز بخش درمانی را بنویسید…',
      send: 'ارسال',
      close: 'بستن',
      welcomeSales: 'سلام و وقت بخیر! خوش آمدید. درباره کیسه‌های ساکشن یکبارمصرف (۱، ۲ و ۳ لیتری)، راهکارهای بالینی هر بخش، دریافت پیش‌فاکتور یا محاسبه صرفه‌جویی بیمارستانتان هر سؤالی دارید بفرمایید.',
      welcomeAcademy: 'سلام و وقت بخیر! به آکادمی آبادیس خوش آمدید. هر سؤالی درباره کنترل عفونت با ساکشن مدار بسته، عملکرد فیلتر هیدروفوبیک و پودر جاذب، یا مقالات علمی دارید بپرسید، یا «مصاحبه بالینی آکادمی» را شروع کنید.',
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
      welcomeSales: 'Hello and welcome! I am the Abadis Medical AI Assistant. Ask me anything about our 1L/2L/3L disposable suction liners, clinical solutions, proforma quotes, or hospital savings calculations.',
      welcomeAcademy: 'Hello and welcome to Abadis Academy! Ask about closed-system infection control vs. traditional glass bottles, shutoff filters, gelling powder, or start the interactive Clinical Interview.',
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
    { id: 'fluid', fa: 'مدیریت مایعات و ترشحات بیمارستانی', en: 'Hospital Fluid & Secretion Management', ar: 'إدارة السوائل والإفرازات في المستشفى' },
    { id: 'airway', fa: 'ایمنی و مراقبت از راه هوایی', en: 'Airway Safety & Care', ar: 'سلامة الطريق الهوائي والعناية به' },
    { id: 'infection-waste', fa: 'کنترل آلودگی و مدیریت پسماند', en: 'Contamination Control & Waste Management', ar: 'السيطرة على التلوث وإدارة النفايات' }
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
    launcher.innerHTML = '<span class="abadis-chat-dot" aria-hidden="true"></span><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg><span class="abadis-chat-launcher-label"></span>';
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
    input = document.createElement('textarea');
    input.className = 'abadis-chat-input';
    input.rows = 1;
    input.required = true;
    input.setAttribute('enterkeyhint', 'send');
    input.setAttribute('dir', 'auto');
    var send = el('button', 'abadis-chat-send');
    send.type = 'submit';
    form.appendChild(input);
    form.appendChild(send);
    function resizeInput() {
      input.style.height = 'auto';
      input.style.height = Math.min(input.scrollHeight || 46, 112) + 'px';
    }
    input.addEventListener('input', resizeInput);
    input.addEventListener('keydown', function (ev) {
      if (ev.key === 'Enter' && !ev.shiftKey) {
        ev.preventDefault();
        if (typeof form.requestSubmit === 'function') form.requestSubmit();
        else form.dispatchEvent(new Event('submit', { cancelable: true }));
      }
    });
    input.addEventListener('focus', function () {
      root.classList.add('is-typing');
      syncViewport();
      setTimeout(syncViewport, 60);
      setTimeout(syncViewport, 180);
      setTimeout(syncViewport, 360);
    });
    input.addEventListener('blur', function () {
      setTimeout(function () {
        root.classList.remove('is-typing');
        syncViewport();
      }, 150);
      setTimeout(syncViewport, 350);
    });
    form.addEventListener('submit', function (ev) {
      ev.preventDefault();
      var q = input.value.trim();
      if (!q) return;
      input.value = '';
      input.style.height = '';
      root.classList.remove('is-typing');
      if (document.activeElement === input) input.blur();
      syncViewport();
      ask(q);
    });
    if (window.visualViewport) {
      window.visualViewport.addEventListener('resize', syncViewport);
      window.visualViewport.addEventListener('scroll', syncViewport);
    }
    window.addEventListener('resize', syncViewport);
    panel.appendChild(form);

    root.appendChild(launcher);
    root.appendChild(panel);
    document.body.appendChild(root);
    var docLang = (document.documentElement.lang || '').toLowerCase();
    if (docLang.indexOf('en') === 0) state.lang = 'en';
    else if (docLang.indexOf('ar') === 0) state.lang = 'ar';
    state.adminUser = loadAdminSession();
    state.adminRules = loadAdminRules();
    setLang(state.lang);
    setMode('sales');
  }

  function paintChrome() {
    var L = t();
    root.lang = state.lang === 'en' ? 'en' : state.lang === 'ar' ? 'ar' : 'fa';
    root.dir = state.lang === 'en' ? 'ltr' : 'rtl';
    root.querySelector('.abadis-chat-launcher-label').textContent = L.launcher;
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
    ['نمونه', 'دمو', 'تست', 'sample', 'trial', 'عینه'],
    ['کارشناس', 'کارشناسان', 'فروشنده', 'فروشندگان', 'تیم', 'اعضا', 'پرسنل', 'همکاران', 'اسامی', 'اسم', 'نام', 'بخش فروش', 'واحد فروش', 'امور مشتریان', 'بازرگانی', 'expert', 'seller', 'team', 'staff', 'executive', 'name'],
    ['مدیر', 'مدیران', 'مدیرعامل', 'هیئت مدیره', 'معاون', 'رییس', 'رئیس', 'سرپرست', 'ceo', 'chairman', 'manager', 'director', 'board'],
    ['شریک', 'شرکا', 'شرکای', 'همکار تجاری', 'انجمن', 'اتحادیه', 'عضویت', 'پارتنر', 'partner', 'membership', 'union', 'association']
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

  var ADMIN_RULES_KEY = 'abadis_chat_admin_rules_v1';
  var ADMIN_SESSION_KEY = 'abadis_chat_admin_session_v1';
  var ADMIN_ACCOUNTS = {
    alireza: {
      id: 'alireza',
      nameFa: 'جناب آقای مهندس علیرضا حسنعلی (مدیرعامل)',
      nameEn: 'Eng. Alireza Hassanali (CEO)',
      hashes: { '1115f0b3': 1, '4ea96397': 1, 'b7d3d642': 1 }
    },
    navid: {
      id: 'navid',
      nameFa: 'جناب آقای مهندس نوید حسنعلی (معاونت بازرگانی و فروش)',
      nameEn: 'Eng. Navid Hassanali (VP Commercial & Sales)',
      hashes: { '410fb81f': 1, '413860af': 1, '00fa80be': 1 }
    }
  };

  function fnv1aHex(str) {
    var h = 0x811c9dc5;
    for (var i = 0; i < str.length; i++) {
      h ^= str.charCodeAt(i);
      h = Math.imul ? Math.imul(h, 0x01000193) >>> 0 : ((h * 0x01000193) >>> 0);
    }
    return ('00000000' + h.toString(16)).slice(-8);
  }

  function normDigits(s) {
    return String(s || '')
      .replace(/[۰-۹]/g, function (d) { return '۰۱۲۳۴۵۶۷۸۹'.indexOf(d); })
      .replace(/[٠-٩]/g, function (d) { return '٠١٢٣٤٥٦٧٨٩'.indexOf(d); });
  }

  function loadAdminSession() {
    try {
      var raw = sessionStorage.getItem(ADMIN_SESSION_KEY);
      if (raw) {
        var parsed = JSON.parse(raw);
        if (parsed && ADMIN_ACCOUNTS[parsed.id]) return ADMIN_ACCOUNTS[parsed.id];
      }
    } catch (e) {}
    return null;
  }

  function saveAdminSession(acc) {
    state.adminUser = acc || null;
    try {
      if (acc) sessionStorage.setItem(ADMIN_SESSION_KEY, JSON.stringify({ id: acc.id }));
      else sessionStorage.removeItem(ADMIN_SESSION_KEY);
    } catch (e) {}
  }

  function loadAdminRules() {
    try {
      var raw = localStorage.getItem(ADMIN_RULES_KEY);
      if (raw) {
        var arr = JSON.parse(raw);
        if (Array.isArray(arr)) return arr;
      }
    } catch (e) {}
    return [];
  }

  function saveAdminRules(rules) {
    state.adminRules = rules || [];
    try {
      localStorage.setItem(ADMIN_RULES_KEY, JSON.stringify(state.adminRules));
    } catch (e) {}
    buildIndex();
  }

  function detectAdminLogin(rawQuery) {
    var clean = normDigits(rawQuery)
      .replace(/\u200c/g, ' ')
      .replace(/[يئ]/g, 'ی')
      .replace(/ك/g, 'ک')
      .replace(/[:|,،؛\-]+/g, ' ')
      .replace(/^(admin|login|ورود|ادمین|کاربر)\s+/i, '')
      .trim();
    var parts = clean.split(/\s+/);
    if (parts.length < 2 || parts.length > 4) return null;
    var uRaw = parts[0].toLowerCase();
    var pRaw = parts.slice(1).join('').toLowerCase();
    var uid = null;
    if (uRaw === 'alireza' || uRaw === 'علیرضا' || uRaw === 'alirezahassanali') uid = 'alireza';
    else if (uRaw === 'navid' || uRaw === 'نوید' || uRaw === 'navidhassanali') uid = 'navid';
    if (!uid) return null;
    var acc = ADMIN_ACCOUNTS[uid];
    var h = fnv1aHex(uid + ':' + pRaw);
    if (acc && acc.hashes[h]) return acc;
    return null;
  }

  function getAdminChunks() {
    var rules = state.adminRules || loadAdminRules();
    state.adminRules = rules;
    return rules.map(function (r, idx) {
      var textFa = 'اصلاحیه و قانون رسمی مدیریت ارشد آبادیس (' + (r.author || 'ادمین') + '): ' + r.fact + (r.topic ? (' | موضوع مرتبط: ' + r.topic) : '');
      return {
        id: 'admin-override-' + (r.id || idx),
        section: 'admin-override',
        url: { fa: '/about/', en: '/en/about/', ar: '/ar/about/' },
        text: { fa: textFa, en: textFa, ar: textFa },
        keywords: (r.topic || '') + ' ' + (r.fact || '')
      };
    });
  }

  function handleAdminCommand(rawQuery) {
    if (!state.adminUser) return false;
    var q = normDigits(rawQuery).replace(/\u200c/g, ' ').replace(/[يئ]/g, 'ی').replace(/ك/g, 'ک').trim();
    var qLow = q.toLowerCase();

    if (/^(خروج ادمین|خروج از ادمین|بستن ادمین|logout|admin logout|exit admin)$/i.test(qLow)) {
      var prevName = state.adminUser.nameFa;
      saveAdminSession(null);
      addMsg('bot', fmtMd(' **خروج از حالت ادمین انجام شد.** (' + prevName + ')\nچت‌بات اکنون در حالت عادی بازدیدکنندگان (فقط‌خواندنی و قفل‌شده روی اطلاعات رسمی) قرار دارد.'));
      return true;
    }

    if (/^(لیست اصلاحات|لیست اموزش ها|لیست آموزش ها|اصلاحات ثبت شده|قوانین ادمین|admin list|list rules)$/i.test(qLow)) {
      var rules = state.adminRules || loadAdminRules();
      if (!rules.length) {
        addMsg('bot', fmtMd(' **هنوز اصلاحیه جدیدی در این مرورگر ثبت نشده است.**\n(اصلاحات پایه سال ۱۴۰۵ شامل ۱۶ سال سابقه مدیریتی مهندس نوید حسنعلی و آمار ۱٬۲۳۲ مرکز درمانی از قبل در هسته اصلی دانش‌نامه قفل شده‌اند.)\nبرای ثبت نکته جدید کافی است بنویسید: `اصلاح: متن صحیح...`'));
      } else {
        var lines = [' **فهرست اصلاحات و نکات ثبت‌شده توسط مدیران ارشد:**'];
        rules.forEach(function (r, i) {
          lines.push((i + 1) + '. **' + r.fact + '** *(ثبت توسط: ' + (r.author || 'ادمین') + (r.topic ? ' — در پاسخ به: «' + r.topic + '»' : '') + ')*');
        });
        lines.push('\nبرای حذف هر مورد بنویسید: `حذف اصلاح ۱` یا `حذف آخرین اصلاح`');
        addMsg('bot', fmtMd(lines.join('\n')));
      }
      return true;
    }

    var delMatch = qLow.match(/^(?:حذف اصلاح|پاک کردن اصلاح|delete rule)\s*(\d+|اخر|آخر)?$/i) || qLow.match(/^(حذف اخرین اصلاح|حذف آخرین اصلاح)$/);
    if (delMatch) {
      var rulesDel = (state.adminRules || loadAdminRules()).slice();
      if (!rulesDel.length) {
        addMsg('bot', fmtMd('موردی برای حذف وجود ندارد.'));
        return true;
      }
      var idxStr = delMatch[1];
      var removed = null;
      if (!idxStr || idxStr === 'اخر' || idxStr === 'آخر' || idxStr.indexOf('آخرین') !== -1 || idxStr.indexOf('اخرین') !== -1) {
        removed = rulesDel.pop();
      } else {
        var rIdx = parseInt(idxStr, 10) - 1;
        if (rIdx >= 0 && rIdx < rulesDel.length) removed = rulesDel.splice(rIdx, 1)[0];
      }
      if (removed) {
        saveAdminRules(rulesDel);
        addMsg('bot', fmtMd(' اصلاحیه زیر حذف شد:\n«' + removed.fact + '»'));
      } else {
        addMsg('bot', fmtMd('شماره اصلاحیه معتبر نیست. برای مشاهده شماره‌ها بنویسید: `لیست اصلاحات`'));
      }
      return true;
    }

    var explicitMatch = q.match(/^(?:اصلاح|اصلاحیه|یاد بگیر|یادبگیر|قانون|نکته|ثبت نکته|ثبت|درستش اینه|درستش|همیشه بگو|teach|correct)\s*[:：\-]?\s*(.+)$/i);
    var isConversationalCorrection = !explicitMatch && (
      /^(نه[،,\s]|خیر[،,\s]|اشتباه|غلط|درست نیست|اینطور نیست|برعکس)/.test(qLow) ||
      /قبلا گفتی|قبلاً گفتی|چرا گفتی|ولی تو گفتی|سابقه.*داره ولی|نگو .* بگو|به جای .* بگو|اطلاعاتت قدیمی|بروز کن|به‌روز کن|تو شرکت ما نیست|در شرکت ما نیست|کارمند ما نیست|پاک کن|حذف کن|اینا کی هستن|این اسامی|از کجا میاری|وجود ندار|غلطه|اشتباهه|نباید بگی|نگو|فقط .* هستن|اصلا تو شرکت|اصلاً تو شرکت/.test(qLow)
    ) && q.length >= 8;

    if (explicitMatch || isConversationalCorrection) {
      var factText = explicitMatch ? explicitMatch[1].trim() : q;
      var topicText = state.lastUserQuery || '';
      var currentRules = (state.adminRules || loadAdminRules()).slice();
      var newRule = {
        id: String(Date.now()),
        author: state.adminUser.nameFa,
        topic: topicText,
        fact: factText,
        ts: new Date().toISOString()
      };
      currentRules.push(newRule);
      saveAdminRules(currentRules);
      addMsg('bot', fmtMd(' **اصلاحیه رسمی شما ثبت و قفل شد** (' + state.adminUser.nameFa + '):\n«' + factText + '»\n\nاز این لحظه این قانون بالاترین اولویت را در پاسخگویی بات دارد. (برای مشاهده همه موارد: `لیست اصلاحات` | برای خروج: `خروج ادمین`)'));
      return true;
    }

    return false;
  }

  function collectDomChunks() {
    var extra = [];
    try {
      var mainEl = document.querySelector('main') || document.body;
      if (!mainEl) return extra;
      var pageUrl = window.location.pathname || '/';
      var members = mainEl.querySelectorAll('.member, .bdt-member-item');
      if (members && members.length) {
        var mLines = [];
        members.forEach(function (m) {
          var t = (m.textContent || '').replace(/\s+/g, ' ').trim();
          if (t && mLines.indexOf(t) === -1) mLines.push('• ' + t);
        });
        if (mLines.length) {
          extra.push({
            id: 'live-dom-team',
            section: 'company',
            url: { fa: pageUrl, en: pageUrl, ar: pageUrl },
            text: { fa: mLines.join('\n'), en: mLines.join('\n'), ar: mLines.join('\n') },
            keywords: 'تیم اجرایی کارشناس فروش مدیر اسامی اسم نام'
          });
        }
      }
      var secs = mainEl.querySelectorAll('section, article, .dealer-card, .prov-panel');
      secs.forEach(function (sec, idx) {
        if (sec.closest('#abadis-chatbot-root')) return;
        var raw = (sec.innerText || sec.textContent || '').replace(/\s+/g, ' ').trim();
        if (raw.length < 60 || raw.length > 3500) return;
        var h = sec.querySelector('h1, h2, h3, h4');
        var hTxt = h ? (h.textContent || '').replace(/\s+/g, ' ').trim() : '';
        var sid = sec.id ? ('#' + sec.id) : '';
        extra.push({
          id: 'live-dom-sec-' + idx,
          section: 'page',
          url: { fa: pageUrl + sid, en: pageUrl + sid, ar: pageUrl + sid },
          text: { fa: raw, en: raw, ar: raw },
          keywords: hTxt
        });
      });
    } catch (e) {}
    return extra;
  }

  function buildIndex() {
    var adminChunks = getAdminChunks();
    var baseChunks = (state.kb && state.kb.chunks) || [];
    var domChunks = collectDomChunks();
    var chunks = adminChunks.concat(baseChunks).concat(domChunks);
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

  function searchRanked(query, limit) {
    if (!index) return [];
    var q = tokens(query);
    if (!q.length) return [];
    var extra = expand(q);
    var qRaw = String(query || '').toLowerCase()
      .replace(/\u200c/g, ' ')
      .replace(/[يئ]/g, 'ی')
      .replace(/ك/g, 'ک')
      .replace(/[أإآ]/g, 'ا');
    var asksPeopleOrNames = /اسم|اسامی|نام|کیه|کیست|چه کسانی|معرفی|کارشناس|کارشناسان|فروشنده|فروشندگان|تیم|اعضا|پرسنل|همکاران|مدیر|مدیران|مدیرعامل|رئیس|هیئت مدیره|معاون|سرپرست|حسابدار|انباردار|حسنعلی|کوکبی|محسن زاده|رعیتی|ناطقی|هاشمیان|تیموری|شرفی|رستمی|مهین دوست|احمدی|اخوان|پورحسن|ناصری|خلیلی|صالحی|قدیمی|تقوی|اسدالهی|فرهنگ|قائم پناه|seller|sales expert|sales team|account executive|who is|team|staff|ceo|manager/.test(qRaw);
    var asksSalesTeam = /فروش|بازرگانی|مشتریان|پیش فاکتور|پیشفاکتور|پشتیبانی|seller|sales|commercial|account executive/.test(qRaw);
    var asksDealers = /نماینده|نمایندگان|نمایندگی|عامل فروش|پخش|توزیع|استان|نیک طب|نیک منش|پردیس طب|کاراطب|قنبریان|جام جم|نائل|پویا طب|مصلحی|بوشهر درمان|محبوسی|رادمان تجهیز|الاسوندی|بهپود|ترابی|جهان درمان|حاج غنی|آبیدر|طبرستان|رضازاده|پاکان طبیب|هگمتان طب|مجیدی|بهسان تجهیز|رفیعی|اصفهان|شیراز|فارس|اهواز|خوزستان|تبریز|آذربایجان|اردبیل|مشهد|خراسان|کرمان|یزد|همدان|مازندران|اراک|مرکزی|بوشهر|گیلان|زنجان|قزوین|کردستان|هرمزگان|سیستان|dealer|distributor|representative|province/.test(qRaw);
    var asksPartners = /شریک|شرکا|شرکای تجاری|عضویت|انجمن|اتحادیه|اتاق بازرگانی|پارک فناوری|آمدال|ویراکام|گوهران|نادین|مهندسین مشاور فیلتر|ابزار درمان پرشیا|gulf innovation|goharan|virakam|تاریخچه|پیشینه|partner|membership/.test(qRaw);
    var asksExplicitNews = /خبر|اخبار|مصاحبه|نمایشگاه|کنگره|ایران هلث|ایران کلین|ایران مد|تا ثریا|عصر خانواده|تمپا|فارس|رادیو|رویداد|وبینار|news|interview|exhibition|congress/.test(qRaw);
    var asksFoundersOrStats = /نوید حسنعلی|علیرضا حسنعلی|ابوالفضل حسنعلی|میلاد پورحسن|سابقه مدیریتی|چند سال سابقه|۱۳ سال|13 سال|۱۶ سال|16 سال|بنیانگذار|هم بنیانگذار|چند بیمارستان|چند مرکز درمانی|تعداد بیمارستان|تعداد مراکز/.test(qRaw);

    var scored = [];
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
        if (doc.chunk.section === 'faq' && !asksPeopleOrNames && !asksDealers) score += 4;
      }
      if ((qRaw.indexOf('اتاق عمل') !== -1 || qRaw.indexOf('مایعات بالا') !== -1 || qRaw.indexOf('حجم مایعات') !== -1 || qRaw.indexOf('جراحی') !== -1) && qRaw.indexOf('قیمت') === -1) {
        if (doc.chunk.id === 'sol-fluid' || doc.chunk.id === 'cat-canisters-liners') score += 28;
      }
      if (asksPeopleOrNames && !asksDealers) {
        if (doc.chunk.id === 'sales-experts-team' && asksSalesTeam) score += 55;
        else if (doc.chunk.id === 'executive-team-full') score += 45;
        else if (doc.chunk.id === 'sales-experts-team') score += 35;
        if (doc.chunk.id === 'faq-17' && !/مراحل خرید|چطور بخرم/.test(qRaw)) score -= 25;
      }
      if (asksDealers) {
        if (doc.chunk.id === 'dealers-directory-all') score += 55;
      }
      if (asksPartners) {
        if (doc.chunk.id === 'partners-and-memberships') score += 48;
      }
      if (/تاریخچه|داستان ابادیس|خط زمانی|تایم لاین|سال تاسیس|1396|1397|1399|1400|1401|1402|1403|1404|1405|۱۳۹۶|۱۳۹۷|۱۳۹۹|۱۴۰۰|۱۴۰۱|۱۴۰۲|۱۴۰۳|۱۴۰۴|۱۴۰۵|عراق|عمان|فیلتر متخلخل/.test(qRaw)) {
        if (doc.chunk.id === 'boss-abadis-timeline-1396-1405') score += 52;
      }
      if (/1410|۱۴۱۰|موتور رشد|سه موتور|برنامه پنج ساله|پنج ساله سوم|۷۰ درصد|70 درصد|افق توسعه/.test(qRaw)) {
        if (doc.chunk.id === 'boss-strategic-vision-1410-and-growth-engines') score += 55;
      }
      if (/برند بوک|هویت بصری|کد رنگی|رنگ سازمانی|فونت|کلمه|ایران سنس|پیام گستر|crm|بازی ده سالگی|کمپین ده سالگی|تجارب ما|mbti/.test(qRaw)) {
        if (doc.chunk.id === 'boss-brand-book-identity-crm-game') score += 55;
      }
      if (/لیست مقالات|همه مقالات|فهرست مقالات|عنوان مقالات|مقالات سایت|چند مقاله/.test(qRaw)) {
        if (doc.chunk.id === 'site-articles-archive') score += 55;
      }
      if (/لیست اخبار|همه اخبار|فهرست اخبار|آخرین اخبار|اخبار سایت|رویدادهای ابادیس/.test(qRaw)) {
        if (doc.chunk.id === 'site-news-archive') score += 55;
      }
      if (/بیمارستان های|مراکز درمانی|مراکز جراحی|کدام بیمارستان/.test(qRaw) && doc.chunk.id.indexOf('hospitals-province-') === 0) {
        score += 35;
      }
      if (doc.chunk.section === 'admin-override' && docHits >= 1) {
        score += 160;
      }
      if (asksFoundersOrStats) {
        if (doc.chunk.id === 'canonical-1405-facts-and-disambiguations') score += 85;
        if (doc.chunk.id === 'executive-team-full') score += 75;
      }
      if (!asksExplicitNews && (doc.chunk.section === 'news' || doc.chunk.id.indexOf('news-item-') === 0)) {
        score -= 18;
      }
      if (score > 0) {
        scored.push({ chunk: doc.chunk, score: score });
      }
    });
    scored.sort(function (a, b) { return b.score - a.score; });
    var out = [];
    var seenIds = {};
    for (var i = 0; i < scored.length && out.length < (limit || 5); i++) {
      var cid = scored[i].chunk.id;
      if (!seenIds[cid]) {
        seenIds[cid] = 1;
        out.push(scored[i].chunk);
      }
    }
    return out;
  }

  function search(query) {
    var top = searchRanked(query, 1);
    return top.length ? top[0] : null;
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
    var maxChars = (hit.id === 'dealers-directory-all' || hit.id === 'executive-team-full' || hit.id === 'sales-experts-team' || hit.id === 'site-news-archive' || hit.id === 'site-articles-archive' || hit.id.indexOf('boss-') === 0 || hit.id.indexOf('hospitals-province-') === 0 || hit.id.indexOf('page-') === 0) ? 2800 : 1600;
    if (shown.length > maxChars) {
      shown = shown.slice(0, maxChars);
      var cut = Math.max(shown.lastIndexOf('.'), shown.lastIndexOf('؟'), shown.lastIndexOf('?'), shown.lastIndexOf('\n'));
      if (cut > 500) shown = shown.slice(0, cut + 1);
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

    // 00. Check Admin Override rules first
    var adminRulesNow = state.adminRules || loadAdminRules();
    if (adminRulesNow && adminRulesNow.length) {
      var qToks = tokens(raw);
      for (var arIdx = adminRulesNow.length - 1; arIdx >= 0; arIdx--) {
        var ar = adminRulesNow[arIdx];
        var arToks = tokens((ar.topic || '') + ' ' + (ar.fact || ''));
        var overlap = 0;
        qToks.forEach(function (wt) { if (arToks.indexOf(wt) !== -1) overlap++; });
        if (overlap >= 2 || (qToks.length === 1 && overlap === 1 && (ar.topic || '').indexOf(qToks[0]) !== -1)) {
          if (state.cutoff) {
            addMsg('bot', fmtMd(ar.fact) + linkLine('/about/', '/about/') + ctaLine());
            showQuickPrompts();
            return true;
          }
        }
      }
    }

    // 0a-person. Direct canonical 1405 biographies for Founders & Senior Executives (prevents outdated 1401 news quotes)
    if (/نوید حسنعلی/.test(q) && !/مقاله|کنگره|عمان|تمپا/.test(q)) {
      var navidBio = state.lang === 'en'
        ? '**Eng. Navid Hassanali — Co-Founder & VP of Commercial and Sales at Abadis Medical Canisters:**\n• **Role:** VP of Commercial & Sales, Board Member, and Co-Founder of the knowledge-based company Abadis Medical Canisters (`abadis-med.com`), leading all sales, marketing, provincial dealer networks, and customer relations.\n• **Education & Experience:** B.Sc. in Biomedical Engineering (Bioelectric) with **over 16 years of continuous management experience in the medical device industry** (since 1389 / 2010).\n• **Key Milestones:** Obtained exclusive representation of Daiken Japan disposable suction liners in 1389 (2010), pioneered the clinical culture of closed-system disposable suction liners across Iranian hospitals, and co-founded **Abadis Medical Canisters** in **1396 (2017)** to launch national production in Iran.\n*(Note on older news archives: the "13 years of management experience" figure appeared in a Khordad 1401 / June 2022 news interview 4 years ago, which corresponds to 16+ years today in 1405/2026.)*'
        : '**مهندس نوید حسنعلی — معاونت بازرگانی و فروش و هم‌بنیان‌گذار شرکت دانش‌بنیان مخازن طبی آبادیس:**\n• **سمت:** معاونت بازرگانی و فروش، عضو هیئت‌مدیره و هم‌بنیان‌گذار شرکت دانش‌بنیان مخازن طبی آبادیس (`abadis-med.com`) و مسئول کل فعالیت‌های فروش، بازاریابی، شبکه نمایندگان و ارتباط با مشتریان.\n• **تحصیلات و سابقه مدیریتی:** کارشناس مهندسی پزشکی (گرایش بیوالکتریک) با **بیش از ۱۶ سال سابقه مدیریتی مستمر در حوزه تجهیزات پزشکی** (از سال ۱۳۸۹ تا ۱۴۰۵).\n• **دستاوردها و پیشینه:** اخذ نمایندگی انحصاری کیسه ساکشن یکبارمصرف از شرکت دایکن ژاپن در سال ۱۳۸۹، فرهنگ‌سازی گسترده استفاده از محصولات کنترل عفونت و کیسه‌های ساکشن یکبارمصرف در بیمارستان‌های کشور، و هم‌بنیان‌گذاری شرکت دانش‌بنیان «مخازن طبی آبادیس» در سال ۱۳۹۶ و راه‌اندازی خط تولید ملی کیسه ساکشن.\n• **توضیح درباره تفاوت عدد ۱۳ سال در آرشیو اخبار با ۱۶ سال فعلی:** عدد «۱۳ سال سابقه مدیریتی» مربوط به مصاحبه خبری خرداد سال ۱۴۰۱ (۴ سال پیش) در آرشیو اخبار سایت است که با گذشت زمان تا سال ۱۴۰۵ به **بیش از ۱۶ سال سابقه مدیریتی در حوزه تجهیزات پزشکی** (و حدود ۱۰ سال از تأسیس شرکت مخازن طبی آبادیس در سال ۱۳۹۶) رسیده است.';
      addMsg('bot', fmtMd(navidBio) + linkLine('/about/#team', '/about/#team') + ctaLine());
      showQuickPrompts();
      return true;
    }
    if (/علیرضا حسنعلی/.test(q) && /کیه|کیست|بیوگرافی|معرفی|سابقه|سمت|مدیرعامل/.test(q)) {
      var alirezaBio = state.lang === 'en'
        ? '**Eng. Alireza Hassanali — CEO & Co-Founder of Abadis Medical Canisters:**\n• **Role:** Chief Executive Officer (CEO), Board Member, and Co-Founder of the knowledge-based company Abadis Medical Canisters (`abadis-med.com`).\n• **Background & Leadership:** Co-founded Abadis Medical Canisters in **1396 (2017)** building on the parent group Persia Medical Instruments (founded in **1385 / 2006**) and exclusive Daiken Japan representation (**1389 / 2010**).\n• **Research & Strategic Focus:** Author of scientific and international conference papers on Business Intelligence (BI) for liquidity and production planning in medical device manufacturing and Green Governance in hospital waste and water reduction; leads Abadis’s 3rd Five-Year Strategic Plan toward 1410.'
        : '**مهندس علیرضا حسنعلی — مدیرعامل و هم‌بنیان‌گذار شرکت دانش‌بنیان مخازن طبی آبادیس:**\n• **سمت:** مدیرعامل، عضو هیئت‌مدیره و هم‌بنیان‌گذار شرکت دانش‌بنیان مخازن طبی آبادیس (`abadis-med.com`).\n• **پیشینه و راهبری:** هم‌بنیان‌گذاری شرکت دانش‌بنیان مخازن طبی آبادیس در سال ۱۳۹۶ (با پشتوانه دو دهه فعالیت مجموعه مادر «ابزار درمان پرشیا» از سال ۱۳۸۵ و فعالیت تخصصی در حوزه کیسه ساکشن از سال ۱۳۸۹) و هدایت شرکت به جایگاه بزرگ‌ترین تولیدکننده کیسه ساکشن یکبارمصرف و اولین تولیدکننده فیلترهای قطع‌کننده جریان در ایران (همراه با ۱٬۲۳۲ مرکز درمانی فعال در سراسر کشور).\n• **فعالیت‌های علمی و راهبردی:** پژوهشگر و نویسنده مقالات علمی و کنفرانسی در زمینه «طراحی سیستم‌های هوش تجاری (BI) برای مدیریت نقدینگی و تصمیم‌گیری تولید در شرکت‌های تجهیزات پزشکی» و «حکمرانی سبز و نوآوری پایدار در کاهش مصرف آب و پسماند بیمارستانی»، و طراح سند چشم‌انداز راهبردی ۱۴۱۰ آبادیس.';
      addMsg('bot', fmtMd(alirezaBio) + linkLine('/about/#team', '/about/#team') + ctaLine());
      showQuickPrompts();
      return true;
    }
    if (/ابوالفضل حسنعلی/.test(q) && /کیه|کیست|بیوگرافی|معرفی|سمت|رئیس/.test(q)) {
      var abolfazlBio = state.lang === 'en'
        ? '**Mr. Abolfazl Hassanali — Chairman of the Board at Abadis Medical Canisters:**\n• **Role:** Chairman of the Board of Directors at the knowledge-based company Abadis Medical Canisters (`abadis-med.com`), overseeing corporate governance, sustainable development, and social responsibility initiatives including the Save Zagros campaign.'
        : '**جناب آقای ابوالفضل حسنعلی — رئیس هیئت‌مدیره شرکت دانش‌بنیان مخازن طبی آبادیس:**\n• **سمت:** رئیس هیئت‌مدیره شرکت دانش‌بنیان مخازن طبی آبادیس (`abadis-med.com`).\n• **محور فعالیت‌ها:** راهبری کلان هیئت‌مدیره، توسعه پایدار، حمایت از تولید دانش‌بنیان و پیشبرد مسئولیت‌های اجتماعی و انسان‌دوستانه آبادیس (از جمله پویش «نجات زاگرس» و کاشت بیش از ۲٬۰۰۰ نهال بلوط به نام مراکز درمانی همراه).';
      addMsg('bot', fmtMd(abolfazlBio) + linkLine('/about/#team', '/about/#team') + ctaLine());
      showQuickPrompts();
      return true;
    }

    // 0a. Direct authoritative answers for Sales Experts, Executive Team & Provincial Dealers
    var hasAdminRules = !!(state.adminRules && state.adminRules.length > 0);
    var isAnalyticalQ = /از کجا|غیر از|چرا|کیست|کیه|لیست پرسنل|کیا رو|چند نفر/.test(q);
    if (!hasAdminRules && (state.cutoff || !isAnalyticalQ)) {
      if (/کارشناس.*فروش|کارشناسان.*فروش|اسامی.*فروش|تیم فروش|نفرات فروش|همکاران فروش|بخش فروش کی|واحد فروش کی|sales expert|sales team|account executive/.test(q)) {
        var salesHit = findChunk('sales-experts-team');
        if (salesHit) { addMsg('bot', synthesize(salesHit)); showQuickPrompts(); return true; }
      }
      if (/اعضای هیئت مدیره|تیم اجرایی|لیست پرسنل|پرسنل شرکت|کیا رو در شرکت|مدیران ابادیس|مدیران شرکت|اسامی مدیران|مدیرعامل کی|رئیس هیئت مدیره|معاون بازرگانی|executive team|board of directors|who is the ceo/.test(q)) {
        var execHit = findChunk('executive-team-full');
        if (execHit) { addMsg('bot', synthesize(execHit)); showQuickPrompts(); return true; }
      }
    }

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
        ? 'Abadis groups its catalogue in eight categories:\n1. Disposable Suction Bag\n2. Suction Canister\n3. Stands & Holders\n4. Connectors\n5. Filter\n6. Suction Tube\n7. Oral Hygiene (suction toothbrush, oral swab, endotracheal-tube fixer)\n8. Other Products (regulator, PVA waste bag, disposable receiver)'
        : state.lang === 'ar'
        ? 'تجمع آباديس كتالوجها في ثماني فئات:\n١. أكياس الشفط ذات الاستخدام الواحد\n٢. علبة الشفط\n٣. الحوامل والمثبتات\n٤. الوصلات\n٥. الفلاتر\n٦. أنبوب الشفط\n٧. نظافة الفم (فرشاة الشفط، المسحة الفموية، مثبّت أنبوب القصبة)\n٨. منتجات أخرى (المنظّم، كيس نفايات PVA، وعاء التجميع)'
        : 'محصولات آبادیس در هشت گروه است:\n۱. کیسه ساکشن یکبار مصرف\n۲. مخزن ساکشن\n۳. پایه و نگهدارنده‌ها\n۴. اتصالات\n۵. فیلتر\n۶. ساکشن تیوب\n۷. بهداشت دهان (مسواک ساکشن، سواب دهانی، فیکسر لوله تراشه)\n۸. سایر محصولات (رگولاتور، کیسه زباله PVA، رسیور یکبار مصرف)';
      addMsg('bot', fmtMd(prodText) + linkLine('/products/', '/products/') + ctaLine());
      showQuickPrompts();
      return true;
    }

    // 4. Greetings & Salutations (only when the message is primarily a greeting/small-talk, not a domain question starting with سلام)
    var domainWords = /اسم|اسامی|نام|کارشناس|فروشنده|تیم|مدیر|اعضا|پرسنل|شریک|شرکا|مقاله|اخبار|کیسه|مخزن|ساکشن|فیلتر|تیوب|رگولاتور|پودر|قیمت|خرید|فاکتور|کارتن|گارانتی|وارانتی|نصب|زاگرس|بلوط|مراکز|رضایت|امار|تاسیس|گواهی|مجوز|ایزو|imed|iso|فلسفه|راهکار|شیشه|تخت|عمل|جراحی|اینترنت|فیلترینگ|تلفن|شماره|ادرس|کارخانه|نمایند|کاتالوگ|اورولوژی|گوارش|زنان|بیهوشی|مسواک|تراشه|liner|canister|suction|filter|tube|price|quote|zagros|certificate|solution|glass|surgery|hospital|intranet|contact|address|catalog|dealer|شهاده|كيس|خزان|سعر|زاغروس|مستشفي/;
    if (!domainWords.test(q)) {
      if (/^(سلام|درود|وقت بخیر|صبح بخیر|عصر بخیر|شب بخیر|خسته نباشید|قوت اله|سلام علیکم|علیکم السلام|های|هلو|salam|salaam|hi|hello|hey|good morning|good afternoon|good evening|greetings|مرحبا|اهلا|أهلا|السلام علیکم|صباح الخیر|مساء الخیر)(\s|$)/.test(q)) {
        var greetTxt = state.lang === 'en'
          ? (state.mode === 'academy'
            ? 'Hello and welcome to Abadis Academy! How can I help you today? You can ask me anything about closed-system suction infection control, hydrophobic filters, gelling powder, or start the 3-step Clinical Interview.'
            : 'Hello and welcome to Abadis Medical! How can I help you today? Feel free to ask about choosing the right suction liner volume (1L, 2L, 3L) for your hospital ward, pricing and proforma invoices, or calculating your annual water and cost savings.')
          : state.lang === 'ar'
          ? 'أهلاً ومرحباً بكم في آباديس الطبية! كيف يمكنني مساعدتكم اليوم؟ اسألوا عن أكياس الشفط (١، ٢، ٣ لتر)، الحلول السريرية، الفاتورة الأولية، أو حساب التوفير السنوي للمستشفى.'
          : (state.mode === 'academy'
            ? 'سلام و وقت بخیر! خیلی خوش آمدید در بخش آکادمی آبادیس چطور می‌توانم کمکتان کنم؟ درباره مقایسه علمی ساکشن مدار بسته با شیشه‌های سنتی، فیلتر هیدروفوبیک و پودر جاذب هر سؤالی دارید بپرسید، یا اگر مایلید «مصاحبه بالینی آکادمی» را شروع کنیم.'
            : 'سلام و وقت بخیر! خیلی خوش آمدید چطور می‌توانم کمکتان کنم؟ اگر درباره انتخاب سایز کیسه ساکشن (۱، ۲ یا ۳ لیتری) و تجهیزات مناسب بخش درمانی‌تان، شرایط خرید و پیش‌فاکتور، یا محاسبه صرفه‌جویی سالانه بیمارستان سؤالی دارید در خدمتم.');
        addMsg('bot', fmtMd(greetTxt) + ctaLine());
        showQuickPrompts();
        return true;
      }

      if (/^(چطوری|حالت چطوره|خوبی|احوالت چطوره|چه خبر|خوب هستی|چطورین|how are you|how is it going|how are things|whats up|کیف حالک|كيف حالك|اخبارک)/.test(q)) {
        var howTxt = state.lang === 'en'
          ? 'I am doing great and ready to help! As Abadis Medical’s on-site assistant, I have the full product catalog, clinical solutions, calculator formulas, and FAQ loaded right here. What ward or product can I help you with today?'
          : state.lang === 'ar'
          ? 'بخير والحمد لله، وجاهز لخدمتكم! قاعدة معرفة آباديس الكاملة متوفرة لدي هنا. كيف يمكنني مساعدتكم اليوم؟'
          : 'ممنون از لطف شما، عالی هستم و آماده پاسخگویی! تمام اطلاعات محصولات، ۵ راهکار بالینی، محاسبه‌گر صرفه‌جویی و دانش‌نامه فنی آبادیس در هسته سایت آماده است. درباره کدام محصول یا بخش بیمارستانی سؤال دارید؟';
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
          ? 'You’re very welcome! Whenever you need a proforma invoice, sample request, or technical support, our team is available at 021-92001017 (Ext. 11) or on WhatsApp (+989100145809).'
          : state.lang === 'ar'
          ? 'على الرحب والسعة! يسعدنا تواصلكم مع قسم المبيعات على الرقم 02192001017 (تحويلة 11) أو عبر واتساب +989100145809.'
          : 'خواهش می‌کنم، خوشحالم که توانستم کمکتان کنم! هر زمان برای دریافت پیش‌فاکتور، درخواست نمونه یا مشاوره فنی نیاز به همراهی داشتید، کارشناسان فروش آبادیس با شماره ۰۲۱-۹۲۰۰۱۰۱۷ (داخلی ۱۱) و واتس‌اپ +۹۸۹۱۰۰۱۴۵۸۰۹ در کنار شما هستند.';
        addMsg('bot', fmtMd(thxTxt) + ctaLine());
        return true;
      }
    }

    return false;
  }

  function topKbContext(query, hit) {
    var parts = [];
    var seen = {};
    var qNorm = String(query || '').toLowerCase().replace(/\u200c/g, ' ').replace(/[يئ]/g, 'ی').replace(/ك/g, 'ک');
    var wantsNews = /خبر|اخبار|مصاحبه|نمایشگاه|کنگره|ایران هلث|ایران کلین|ایران مد|تا ثریا|عصر خانواده|تمپا|فارس|رادیو|رویداد|وبینار|news|interview|exhibition|congress/.test(qNorm);
    var canon = findChunk('canonical-1405-facts-and-disambiguations');
    if (canon && canon.text && /نوید|علیرضا|ابوالفضل|حسنعلی|سابقه|بنیانگذار|چند سال|۱۳ سال|۱۶ سال|13|16|بیمارستان|مرکز درمانی|آمار|رضایت/.test(qNorm)) {
      parts.push(textOf(canon.text));
      seen[canon.id] = 1;
    }
    if (hit && hit.text && !seen[hit.id]) {
      parts.push(textOf(hit.text));
      seen[hit.id] = 1;
    }
    var ranked = searchRanked(query, 7);
    for (var i = 0; i < ranked.length && parts.length < 5; i++) {
      var c = ranked[i];
      if (!wantsNews && (c.section === 'news' || c.id.indexOf('news-item-') === 0) && parts.length >= 1) {
        continue;
      }
      if (!seen[c.id] && c.text) {
        seen[c.id] = 1;
        parts.push(textOf(c.text));
      }
    }
    return parts.join('\n---\n').slice(0, 4400);
  }

  function isRefusalText(txt) {
    return /نمی‌?توانم این اطلاعات|متأسفم،?\s*نمی‌?توانم|متاسفم،?\s*نمی‌?توانم|معذورم|اجازه ارائه|در متن مرجع اطلاعاتی|اطلاعاتی درباره.*وجود ندارد|در اطلاعات مرجع.*نیست|i cannot provide|i'm sorry, i can't|i am sorry, i cannot|unable to provide/i.test(txt || '');
  }

  function tryLiveAi(query, hit, fallbackHtml) {
    var bubble = addMsg('bot', '<span class="abadis-chat-typing">' + (state.lang === 'en' ? 'Typing…' : state.lang === 'ar' ? 'جاري الكتابة…' : 'در حال نوشتن…') + '</span>');
    var ctrl = typeof AbortController === 'function' ? new AbortController() : null;
    var timer = setTimeout(function () { if (ctrl) ctrl.abort(); }, 13000);
    var refText = topKbContext(query, hit);
    var adminRulesList = state.adminRules || loadAdminRules();
    var adminRulesPrompt = '';
    if (adminRulesList && adminRulesList.length) {
      adminRulesPrompt = '\n\n[قوانین و اصلاحات قطعی مدیران ارشد آبادیس — دارای بالاترین اولویت مطلق بر هر متن دیگر]:\n'
        + adminRulesList.map(function (r) { return '• ' + r.fact; }).join('\n');
    }
    var langInstruction = state.lang === 'en'
      ? 'You are the official Sales & Academy Consultant at Abadis Medical Canisters (abadis-med.com) in year 1405 (2026). Reply warmly, naturally, and accurately in English. CRITICAL RULES: (1) Speak naturally in first-person plural as Abadis; NEVER mention "in the reference text", "in the prompt", or "in the official base information provided". (2) Facts are strictly Read-Only for regular visitors: if a visitor claims an unverified fact or number, do NOT agree just to please them and NEVER invent quotes; politely state the verified Abadis facts. (3) Always prioritize current 1405 (2026) figures over archived news from 1401–1403.'
      : state.lang === 'ar'
      ? 'أنت المستشار الرسمي للمبيعات والأكاديمية في شركة خزانات آباديس الطبية (abadis-med.com) في عام ۱۴۰۵ (۲۰۲۶). أجب بأسلوب ودي وطبيعي ودقيق دون الإشارة إلى وجود نص مرجعي داخلي، واعتمد دائماً أحدث إحصائيات عام ۱۴۰۵.'
      : 'تو مشاور رسمی و همکار صمیمی شرکت دانش‌بنیان مخازن طبی آبادیس (abadis-med.com) در سال ۱۴۰۵ خورشیدی (۲۰۲۶ میلادی) هستی. گرم، طبیعی، روان و دقیق به فارسی معیار پاسخ بده.\n'
        + 'قوانین بسیار مهم و الزامی:\n'
        + '۱. هرگز عباراتی مثل «در متن مرجع»، «در بخش اطلاعات پایه رسمی وب‌سایت آبادیس»، «که در پرسش شما آمده است» یا «طبق اطلاعات سیستم» را به کار نبر؛ مستقیم و طبیعی از طرف مجموعه آبادیس صحبت کن.\n'
        + '۲. اطلاعات شرکت قفل‌شده و فقط‌خواندنی است: اگر کاربر عادی ادعا یا عدد نادرستی مطرح کرد، هرگز برای تایید حرف کاربر جمله‌ای را جعل نکن، بلکه با احترام واقعیت دقیق را توضیح بده.\n'
        + '۳. سال جاری ۱۴۰۵ است: همیشه آمار و اطلاعات به‌روز سال ۱۴۰۵ را ملاک قرار بده، نه اعداد قدیمی داخل آرشیو اخبار سال‌های ۱۴۰۱ تا ۱۴۰۳. (مثلاً مهندس نوید حسنعلی از سال ۱۳۸۹ با اخذ نمایندگی انحصاری دایکن ژاپن بیش از ۱۶ سال سابقه مدیریتی در حوزه تجهیزات پزشکی دارند و در سال ۱۳۹۶ شرکت دانش‌بنیان مخازن طبی آبادیس را هم‌بنیان‌گذاری کرده‌اند؛ عدد ۱۳ سال در مصاحبه خرداد ۱۴۰۱ مربوط به ۴ سال پیش بوده است).';
    var sys = langInstruction
      + adminRulesPrompt
      + '\n\n[اطلاعات رسمی و به‌روز سال ۱۴۰۵ شرکت دانش‌بنیان مخازن طبی آبادیس]: '
      + 'هیئت‌مدیره و مدیران ارشد: ابوالفضل حسنعلی (رئیس هیئت مدیره)، مهندس علیرضا حسنعلی (مدیرعامل و هم‌بنیان‌گذار)، مهندس نوید حسنعلی (معاونت بازرگانی و فروش، عضو هیئت‌مدیره و هم‌بنیان‌گذار؛ کارشناس مهندسی پزشکی گرایش بیوالکتریک با بیش از ۱۶ سال سابقه مدیریتی در حوزه تجهیزات پزشکی از سال ۱۳۸۹ و هم‌بنیان‌گذار مخازن طبی آبادیس در سال ۱۳۹۶)، میلاد پورحسن (مشاور عالی مدیرعامل)، مژده مهین‌دوست (مدیر مالی)، محمدمهدی احمدی (مدیر کارخانه)، نازنین اخوان طباطبایی (مدیر حقوقی)، نازنین حسنعلی (مدیر روابط عمومی)، مائده ناصری (مدیر تضمین کیفیت)، علی‌سینا صالحی (مدیر IT). '
      + 'سرپرست تولید: مهران خلیلی. تیم فروش، بازرگانی و امور مشتریان (مطابق صفحه رسمی /about/#team): روژان کوکبی (کارشناس فروش و امور مشتریان)، امیر محسن‌زاده (کارشناس فروش و امور مشتریان)، محبوبه رعیتی (کارشناس فروش و امور مشتریان)، سونا هاشمیان (کارشناس فروش و امور مشتریان)، زهرا ناطقی (کارشناس فروش و امور مشتریان)، هلیا تیموری (کارشناس عملیات فروش)، نیلوفر شرفی (کارشناس ارشد تأمین و بازرگانی)، الهه رستمی (کارشناس بازرگانی). سایر همکاران تیم اجرایی: کیمیا قدیمی (کارشناس حسابداری)، امیرعرشیا تقوی (کارشناس نصب و خدمات فنی)، میثم اسدالهی (انباردار)، پوریا فرهنگ (تحصیلدار)، محمد قائم‌پناه (مسئول تحویل کالا). '
      + 'محصولات: کیسه ساکشن یکبارمصرف در ۳ سایز ۱، ۲ و ۳ لیتر (هر کارتن ۴۵ عدد، فیلتر مکانیکی ۳۰ عدد) با فیلتر هیدروفوبیک قطع‌کننده جریان و پودر جاذب؛ مخازن پلی‌کربنات نشکن؛ ساکشن تیوب CH25/CH30/CH35 (۱۰۰ عدد در کارتن)؛ مسواک ساکشن؛ فیکسر لوله تراشه؛ رگولاتور وکیوم VR-A1 و VR-B1؛ فیلتر آنتی‌باکتریال؛ ترولی سری تا ۴ مخزن (۱۲ لیتر). آمار رسمی سال ۱۴۰۵: ۱٬۲۳۲ مرکز درمانی فعال در سراسر کشور (۱٬۲۸۴ بیمارستان و مرکز جراحی در ۳۱ استان روی نقشه خانواده سبز)، ۱۱٬۱۱۲ کاربر، ۹۸.۹۹٪ رضایت، ۰.۰۰۱۸٪ خرابی، تأسیس شرکت آبادیس ۱۳۹۶ (۲۰۱۷) و پیشینه گروه مادر ابزار درمان پرشیا از ۱۳۸۵ و نمایندگی دایکن ژاپن از ۱۳۸۹. تلفن فروش: ۰۲۱-۲۲۲۱۸۹۱۰ و ۰۲۱-۹۲۰۰۱۰۱۷ داخلی ۱۱، واتس‌اپ +۹۸۹۱۰۰۱۴۵۸۰۹.'
      + (refText ? ('\n\n[جزئیات تکمیلی از صفحات وب‌سایت]:\n' + refText) : '')
      + (adminRulesList && adminRulesList.length ? ('\n\n⚠️ دستور قطعی و لازم‌الاجرای مدیر ارشد (این دستور هر اطلاعات متناقض در متن پایه را باطل می‌کند):\n' + adminRulesList.map(function (r) { return '• ' + r.fact; }).join('\n')) : '');

    var msgs = [{ role: 'system', content: sys }];
    state.history = state.history || [];
    var recent = state.history.slice(-4);
    recent.forEach(function (m) { msgs.push(m); });
    msgs.push({ role: 'user', content: query });

    var customUrl = state.tier === 'domestic' && domesticEl && domesticEl.value.trim()
      ? domesticEl.value.trim()
      : state.tier === 'intl' && intlEl && intlEl.value.trim()
      ? intlEl.value.trim()
      : 'https://text.pollinations.ai/';

    var payload = {
      model: 'openai-fast',
      reasoning_effort: 'low',
      temperature: 0.25,
      messages: msgs
    };
    var headers = { 'Content-Type': 'application/json' };
    if (keyEl && keyEl.value.trim()) headers.Authorization = 'Bearer ' + keyEl.value.trim();

    var opts = { method: 'POST', headers: headers, body: JSON.stringify(payload) };
    if (ctrl) opts.signal = ctrl.signal;

    fetch(customUrl, opts).then(function (r) {
      if (!r.ok) throw new Error('http');
      return r.text();
    }).then(function (raw) {
      clearTimeout(timer);
      var txt = String(raw || '').trim();
      if (txt.charAt(0) === '{') {
        try {
          var j = JSON.parse(txt);
          if (j && j.choices && j.choices[0] && j.choices[0].message && j.choices[0].message.content) {
            txt = String(j.choices[0].message.content).trim();
          }
        } catch (e) {}
      }
      if (txt) {
        txt = txt
          .replace(/در بخش «?اطلاعات پایه رسمی وب‌?سایت آبادیس»?(?: که در پرسش شما آمده است،?)?/g, 'بر اساس اطلاعات رسمی وب‌سایت آبادیس')
          .replace(/که در پرسش شما آمده است،?/g, '')
          .replace(/در متن مرجع(?: مرتبط با سؤال کاربر)?/g, 'در مستندات رسمی آبادیس');
      }
      if (txt && txt.length > 8 && txt.indexOf('<!DOCTYPE') === -1 && txt.indexOf('"error"') === -1 && !isRefusalText(txt)) {
        state.history.push({ role: 'user', content: query });
        state.history.push({ role: 'assistant', content: txt });
        var srcHtml = hit && hit.url ? linkLine(urlOf(hit.url), urlOf(hit.url)) : '';
        bubble.innerHTML = fmtMd(txt) + srcHtml + ctaLine();
      } else {
        bubble.innerHTML = fallbackHtml;
      }
      if (logEl) logEl.scrollTop = logEl.scrollHeight;
      showQuickPrompts();
    }).catch(function () {
      clearTimeout(timer);
      bubble.innerHTML = fallbackHtml;
      if (logEl) logEl.scrollTop = logEl.scrollHeight;
      showQuickPrompts();
    });
  }

  function answerSearch(query) {
    var hit = search(query);
    if (hit) state.lastHit = hit;
    var fallbackHtml = hit ? synthesize(hit) : (fmtMd(t().empty) + '<br>' + ctaLine());
    if (!state.cutoff) {
      tryLiveAi(query, hit, fallbackHtml);
    } else {
      addMsg('bot', fallbackHtml);
      showQuickPrompts();
    }
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
    var loginAcc = detectAdminLogin(query);
    if (loginAcc) {
      saveAdminSession(loginAcc);
      addMsg('user', ' [احراز هویت مدیر ارشد]');
      addMsg('bot', fmtMd(' **خوش آمدید ' + loginAcc.nameFa + ' عزیز — حالت آموزش و اصلاح ادمین فعال شد.**\n'
        + 'از این لحظه هر نکته یا اصلاحیه‌ای که بنویسید، در حافظه رسمی بات ثبت می‌شود و اولویت قطعی بر تمام متون قبلی خواهد داشت:\n'
        + '• **ثبت اصلاحیه یا فکت جدید:** کافی است بنویسید `اصلاح: متن صحیح...` یا `یاد بگیر: ...` (یا مستقیماً به پاسخ قبلی بات اعتراض/اصلاحیه بنویسید).\n'
        + '• **مشاهده قوانین ثبت‌شده:** بنویسید `لیست اصلاحات`\n'
        + '• **حذف آخرین مورد:** بنویسید `حذف آخرین اصلاح`\n'
        + '• **خروج از حالت ادمین:** بنویسید `خروج ادمین`'));
      return;
    }
    addMsg('user', esc(query));
    if (handleAdminCommand(query)) {
      return;
    }
    state.lastUserQuery = query;
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

  function syncViewport() {
    if (!state.open || !root) return;
    var vv = window.visualViewport;
    if (vv) {
      root.style.setProperty('--ac-vvh', Math.round(vv.height) + 'px');
      root.style.setProperty('--ac-vvt', Math.max(0, Math.round(vv.offsetTop)) + 'px');
    } else {
      root.style.setProperty('--ac-vvh', window.innerHeight + 'px');
      root.style.setProperty('--ac-vvt', '0px');
    }
    if (logEl) logEl.scrollTop = logEl.scrollHeight;
  }

  function lockMobileBody() {
    if (root.classList.contains('is-docked') || window.innerWidth > 640) return;
    if (document.body.dataset.acLocked === '1') return;
    state.savedScrollY = window.scrollY || window.pageYOffset || 0;
    document.body.dataset.acLocked = '1';
    document.body.style.position = 'fixed';
    document.body.style.top = (-state.savedScrollY) + 'px';
    document.body.style.left = '0';
    document.body.style.right = '0';
    document.body.style.width = '100%';
    document.body.style.overflow = 'hidden';
    document.documentElement.classList.add('abadis-chat-lock');
  }

  function unlockMobileBody() {
    if (document.body.dataset.acLocked !== '1') return;
    var y = state.savedScrollY || 0;
    delete document.body.dataset.acLocked;
    document.body.style.position = '';
    document.body.style.top = '';
    document.body.style.left = '';
    document.body.style.right = '';
    document.body.style.width = '';
    document.body.style.overflow = '';
    document.documentElement.classList.remove('abadis-chat-lock');
    window.scrollTo(0, y);
  }

  function open() {
    state.open = true;
    panel.hidden = false;
    root.classList.add('is-open');
    lockMobileBody();
    syncViewport();
    root.querySelector('.abadis-chat-launcher').setAttribute('aria-expanded', 'true');
    if (logEl) logEl.scrollTop = logEl.scrollHeight;
  }
  function close() {
    if (root.classList.contains('is-docked')) return;
    state.open = false;
    panel.hidden = true;
    root.classList.remove('is-open', 'is-typing');
    unlockMobileBody();
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
