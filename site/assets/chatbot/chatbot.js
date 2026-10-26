/* Abadis Sales & Academy chatbot.
   Embed: <script src="/assets/chatbot/chatbot.js" defer data-kb="/assets/data/abadis-knowledge-base.json"></script>
   Works offline from the knowledge-base JSON. An API key is optional and never required. */
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
      llmLabel: 'مدل زنده (اختیاری) — بدون کلید، پاسخ فقط از دانش‌نامه است',
      llmKey: 'کلید API، فقط در همین نشست',
      llmUrl: 'نشانی تکمیل گفتگو',
      llmFail: 'مدل زنده پاسخ نداد. پاسخ بالا از دانش‌نامه محلی است.',
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
      llmLabel: 'Optional live model — with no key, answers stay on the knowledge base',
      llmKey: 'API key, this session only',
      llmUrl: 'Chat completions URL',
      llmFail: 'The live model did not answer. The reply above is from the local knowledge base.',
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
      llmLabel: 'نموذج مباشر اختياري — بلا مفتاح تبقى الإجابة من قاعدة المعرفة',
      llmKey: 'مفتاح API لهذه الجلسة فقط',
      llmUrl: 'عنوان إكمال المحادثة',
      llmFail: 'النموذج المباشر لم يجب. الرد أعلاه من قاعدة المعرفة المحلية.',
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

  var state = { lang: 'fa', mode: 'sales', open: false, kb: null, choice: null, volume: null };
  var root, panel, logEl, chipEl, choiceEl, input, subEl, keyEl, urlEl;

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
    keyEl = document.createElement('input');
    keyEl.type = 'password';
    keyEl.autocomplete = 'off';
    urlEl = document.createElement('input');
    urlEl.type = 'url';
    urlEl.value = 'https://api.openai.com/v1/chat/completions';
    llm.appendChild(keyEl);
    llm.appendChild(urlEl);
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
    root.querySelector('.abadis-chat-llm summary').textContent = L.llmLabel;
    keyEl.placeholder = L.llmKey;
    urlEl.placeholder = L.llmUrl;
    panel.setAttribute('aria-label', L.title);
    paintChips();
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

  var STOP = { چه: 1, که: 1, از: 1, در: 1, به: 1, را: 1, با: 1, این: 1, است: 1, برای: 1, یا: 1, و: 1, می: 1, کند: 1, شود: 1, آیا: 1, the: 1, and: 1, what: 1, does: 1, do: 1, is: 1, of: 1, an: 1, a: 1, to: 1, for: 1, on: 1, in: 1, ما: 1, هل: 1, من: 1, في: 1 };

  function tokens(s) {
    return String(s || '').toLowerCase().replace(/[^\p{L}\p{N}]+/gu, ' ').split(/\s+/).filter(function (w) { return w.length > 1 && !STOP[w]; });
  }

  function search(query) {
    var list = (state.kb && state.kb.chunks) || [];
    var q = tokens(query);
    var best = null;
    var bestScore = 0;
    list.forEach(function (chunk) {
      var text = chunk.text || {};
      var langText = text[state.lang] || '';
      var fa = text.fa || '';
      var head = tokens((langText.split('\n')[0] || '') + ' ' + (fa.split('\n')[0] || '')).join(' ');
      var bag = tokens(langText + ' ' + fa + ' ' + (text.en || '') + ' ' + (chunk.keywords || '')).join(' ');
      var score = 0;
      var headHits = 0;
      q.forEach(function (word) {
        var weight = word.length > 3 ? 3 : 1;
        if (head.indexOf(word) !== -1) { score += weight * 4; headHits += 1; }
        else if (bag.indexOf(word) !== -1) score += weight;
      });
      if (q.length && headHits === q.length) {
        score += 8;
        if (chunk.section === 'faq') score += 4;
      }
      if (score > bestScore) { bestScore = score; best = chunk; }
    });
    return bestScore > 0 ? best : null;
  }

  function answerSearch(query) {
    var hit = search(query);
    if (!hit) {
      addMsg('bot', esc(t().empty));
      return;
    }
    var body = textOf(hit.text);
    var url = urlOf(hit.url);
    addMsg('bot', esc(body).replace(/\n/g, '<br>') + linkLine(url, url));
    maybeModel(query, body);
  }

  function maybeModel(query, context) {
    var key = keyEl && keyEl.value.trim();
    if (!key) return;
    var endpoint = (urlEl && urlEl.value.trim()) || 'https://api.openai.com/v1/chat/completions';
    var payload = {
      model: 'gpt-4o-mini',
      messages: [
        { role: 'system', content: 'Answer only from the Abadis context. If the context is silent, say so. Do not invent certificates, prices, or founding years.' },
        { role: 'user', content: 'Context:\n' + context + '\n\nQuestion:\n' + query }
      ]
    };
    fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + key },
      body: JSON.stringify(payload)
    }).then(function (r) {
      if (!r.ok) throw new Error('http');
      return r.json();
    }).then(function (data) {
      var msg = data && data.choices && data.choices[0] && data.choices[0].message && data.choices[0].message.content;
      if (msg) addMsg('bot', esc(msg).replace(/\n/g, '<br>'));
      else addMsg('bot', esc(t().llmFail));
    }).catch(function () {
      addMsg('bot', esc(t().llmFail));
    });
  }

  function intent(query) {
    var q = query.toLowerCase();
    var n = query.replace(/[۰-۹]/g, function (d) { return '۰۱۲۳۴۵۶۷۸۹'.indexOf(d); })
      .replace(/[٠-٩]/g, function (d) { return '٠١٢٣٤٥٦٧٨٩'.indexOf(d); });
    var surg = n.match(/(\d{3,5})/);
    if (/صرف|saving|توفير|عمل|surger/.test(q) && surg) return { type: 'savings', n: surg[1] };
    if (/۲ لیتر|2 لیتر|2 litre|2 liter|٢ لتر|دو لیتر/.test(query) || /\b2\s*l\b/i.test(q)) return { type: 'volume', id: '2' };
    if (/۳ لیتر|3 لیتر|3 litre|٣ لتر|سه لیتر/.test(query) || /\b3\s*l\b/i.test(q)) return { type: 'volume', id: '3' };
    if (/۱ لیتر|1 لیتر|1 litre|١ لتر|یک لیتر/.test(query) || /\b1\s*l\b/i.test(q)) return { type: 'volume', id: '1' };
    if (/icu|سی‌سی‌یو|سی سی یو|عنایة مركزة|العناية/.test(q)) return { type: 'solution', id: 'icu-care' };
    if (/اتاق عمل|operating room|غرفة العمليات/.test(q)) return { type: 'solution', id: 'or-efficiency' };
    if (/راه هوا|airway|هوائ/.test(q)) return { type: 'solution', id: 'airway' };
    if (/آلودگ|infection|تلوث|پسماند|waste/.test(q)) return { type: 'solution', id: 'infection-waste' };
    if (/مایع|fluid|سوائل|ترشح/.test(q)) return { type: 'solution', id: 'fluid' };
    if (/تیوب|tube|أنبوب|فینگ|fingertip/.test(q)) return { type: 'product', id: 'suction-instruments' };
    if (/کیسه|مخزن|liner|canister|كيس|خزان/.test(q)) return { type: 'product', id: 'canisters-liners' };
    return null;
  }

  function ask(query) {
    open();
    addMsg('user', esc(query));
    if (!state.kb) {
      addMsg('bot', esc(t().empty));
      return;
    }
    if (state.mode === 'sales') {
      var hit = intent(query);
      if (hit && hit.type === 'savings') {
        onChoice('savings', { id: hit.n, fa: hit.n, en: hit.n, ar: hit.n });
        return;
      }
      if (hit && hit.type === 'volume') {
        onChoice('volume', { id: hit.id, fa: hit.id + ' L', en: hit.id + ' L', ar: hit.id + ' L' });
        return;
      }
      if (hit && hit.type === 'solution') {
        var sol = null;
        SOLUTIONS.forEach(function (s) { if (s.id === hit.id) sol = s; });
        if (sol) { onChoice('solution', sol); return; }
      }
      if (hit && hit.type === 'product') {
        var prod = null;
        PRODUCTS.forEach(function (s) { if (s.id === hit.id) prod = s; });
        if (prod) { onChoice('product', prod); return; }
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

  build();
  fetch(kbUrl, { credentials: 'omit' }).then(function (r) {
    if (!r.ok) throw new Error('kb');
    return r.json();
  }).then(function (data) {
    state.kb = data;
    resetThread();
  }).catch(function () {
    addMsg('bot', esc(t().empty));
  });

  window.AbadisChat = {
    open: open,
    close: close,
    setLang: setLang,
    setMode: setMode,
    ask: ask,
    dock: dock,
    float: float
  };
})();
