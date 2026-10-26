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
      title: 'آبادیس',
      subSales: 'مشاور فروش و انتخاب محصول',
      subAcademy: 'پرسش و پاسخ آکادمی',
      tabSales: 'مشاور فروش',
      tabAcademy: 'آکادمی',
      placeholder: 'سؤال یا نیاز بخش درمانی را بنویسید…',
      send: 'ارسال',
      close: 'بستن',
      welcomeSales: 'سلام. می‌توانید از راهکار بالینی شروع کنید یا از حجم کیسه. محاسبه صرفه‌جویی تا ۱۵٬۰۰۰ عمل است و CO₂ ندارد.',
      welcomeAcademy: 'سلام. درباره مصرف بالینی، سیستم بسته، گواهی‌ها، نجات زاگرس یا آبادیس بپرسید. پاسخ از دانش‌نامه همین سایت است.',
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
      empty: 'در دانش‌نامه موردی برای این عبارت پیدا نشد. یکی از پرسش‌های آماده را بزنید یا دقیق‌تر بپرسید.',
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
      welcomeSales: 'Start from a clinical solution or from a liner volume. Savings run up to 15,000 surgeries and do not include CO₂.',
      welcomeAcademy: 'Ask about clinical use, closed-system suction, certificates, Save Zagros, or Abadis. Answers come from the on-page knowledge base.',
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
      empty: 'Nothing in the knowledge base matched that. Try one of the sample prompts.',
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
      academy: ['فیلتر قطع‌کننده چه می‌کند؟', 'ISO و IMED', 'نجات زاگرس چیست؟', 'آبادیس چه سالی تأسیس شد؟']
    },
    en: {
      sales: ['Fluid management solution', '2 litre liner for ICU', 'Savings for 5000 surgeries'],
      academy: ['What does the shutoff filter do?', 'ISO and IMED', 'What is Save Zagros?', 'When was Abadis established?']
    },
    ar: {
      sales: ['حل إدارة السوائل', 'كيس ٢ لتر لـ ICU', 'توفير ٥٠٠٠ عملية'],
      academy: ['ماذا يفعل فلتر قطع التدفق؟', 'ISO و IMED', 'ما إنقاذ زاغروس؟', 'متى تأسست آباديس؟']
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
    launcher.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M4 4h16a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H9l-5 4v-4H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z"/></svg><span></span>';
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
    badgeEl.innerHTML = '<strong></strong><span dir="ltr"></span>';
    head.appendChild(badgeEl);
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
    آبادیس: 1, ابادیس: 1, شرکت: 1, مورد: 1, درباره: 1, کار: 1,
    the: 1, and: 1, what: 1, does: 1, do: 1, did: 1, is: 1, are: 1, was: 1, were: 1, of: 1, an: 1, a: 1,
    to: 1, for: 1, on: 1, in: 1, at: 1, by: 1, with: 1, from: 1, how: 1, many: 1, much: 1, why: 1,
    which: 1, where: 1, when: 1, who: 1, can: 1, if: 1, use: 1, used: 1, using: 1, offer: 1, have: 1,
    has: 1, you: 1, your: 1, we: 1, our: 1, they: 1, it: 1, that: 1, this: 1, there: 1, be: 1, abadis: 1,
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
    ['کارتن', 'بستهبندی', 'تعداد', 'carton', 'pack', 'box', 'کرتون', 'عدد']
  ];

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
    var faSuf = ['هایمان', 'هایتان', 'هایشان', 'هایی', 'های', 'ها', 'مان', 'تان', 'شان', 'ایه', 'ای'];
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

  function synthesize(hit) {
    var body = textOf(hit.text);
    var shown = body;
    if (shown.length > 720) {
      shown = shown.slice(0, 720);
      var cut = Math.max(shown.lastIndexOf('.'), shown.lastIndexOf('؟'), shown.lastIndexOf('?'));
      if (cut > 400) shown = shown.slice(0, cut + 1);
      else shown = shown.replace(/\s+\S*$/, '') + '…';
    }
    var url = urlOf(hit.url);
    return '<p class="abadis-chat-engine-tag">' + esc(t().coreTag) + '</p>'
      + esc(shown).replace(/\n/g, '<br>') + linkLine(url, url);
  }

  function answerSearch(query) {
    var hit = search(query);
    if (!hit) {
      addMsg('bot', esc(t().empty));
      return;
    }
    var body = textOf(hit.text);
    addMsg('bot', synthesize(hit));
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
    if (/صرف|saving|توفير|عمل|surger/.test(q) && surg && !/سال\s*13|سال\s*20|1396|1397|2017|13485/.test(n)) {
      return { type: 'savings', n: surg[1] };
    }
    if (WIZARD_SHORTCUTS[q]) return WIZARD_SHORTCUTS[q];
    return null;
  }

  function ask(query) {
    open();
    addMsg('user', esc(query));
    if (!state.kb) {
      addMsg('bot', esc(t().empty));
      return;
    }
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

  function applyKb(data, source) {
    if (!data || !data.chunks) return false;
    state.kb = data;
    state.kbSource = source;
    buildIndex();
    resetThread();
    paintChrome();
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
  fetch(kbUrl, { credentials: 'omit' }).then(function (r) {
    if (!r.ok) throw new Error('kb');
    return r.json();
  }).then(function (data) {
    if (!applyKb(data, 'site-json')) throw new Error('kb');
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
