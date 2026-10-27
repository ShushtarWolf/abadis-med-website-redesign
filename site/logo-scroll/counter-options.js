/* Home impact counter — formula + three motion samples (M1 odometer, M2 water, M3 pulse+rate).
   Mode is data-counter on the card (c2 wires m2); <html data-counter> still works. */
(function () {
  function formatStat(n, lang, decimals) {
    var neg = n < 0;
    n = Math.abs(n);
    var parts = n.toFixed(decimals).split('.');
    var whole = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    var frac = parts[1] || '';
    var map = lang === 'fa' ? '۰۱۲۳۴۵۶۷۸۹' : (lang === 'ar' ? '٠١٢٣٤٥٦٧٨٩' : '');
    if (map) {
      var sep = '\u066c';
      whole = whole.replace(/,/g, sep).replace(/\d/g, function (d) { return map[d]; });
      frac = frac.replace(/\d/g, function (d) { return map[d]; });
    }
    return (neg ? '-' : '') + whole + (decimals ? '.' + frac : '');
  }
  /* Four published impact figures. Final text is already in the markup. */
  document.querySelectorAll('[data-impact-stat]').forEach(function (el) {
    var to = parseFloat(el.getAttribute('data-impact-stat'));
    var decimals = parseInt(el.getAttribute('data-decimals') || '0', 10);
    var lang = el.getAttribute('data-lang') || 'fa';
    if (!isFinite(to)) return;
    var finalText = formatStat(to, lang, decimals);
    var reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (reduceMotion || !('IntersectionObserver' in window)) { el.textContent = finalText; return; }
    el.textContent = formatStat(0, lang, decimals);
    var dur = 1100, started = false;
    function run(t0) {
      function frame(now) {
        var p = Math.min(1, (now - t0) / dur);
        var e = 1 - Math.pow(1 - p, 3);
        el.textContent = p < 1 ? formatStat(to * e, lang, decimals) : finalText;
        if (p < 1) requestAnimationFrame(frame);
      }
      requestAnimationFrame(frame);
    }
    var io = new IntersectionObserver(function (ents) {
      if (started || !ents.some(function (x) { return x.isIntersecting; })) return;
      started = true;
      io.disconnect();
      requestAnimationFrame(function (now) { run(now); });
    }, { threshold: 0.35 });
    io.observe(el.closest('.impact-stat') || el);
  });

  /* ⓘ note beside the impact title. Hover, focus, and click/tap; Escape and outside press close. */
  (function initImpactInfo() {
    var wrap = document.querySelector('.impact-title-wrap');
    var btn = wrap && wrap.querySelector('.impact-info-btn');
    var tip = document.getElementById('impact-info-tip');
    if (!wrap || !btn || !tip) return;
    var pinned = false, hover = false, focus = false, suppress = false, openedAt = 0;
    function shown() { return btn.getAttribute('aria-expanded') === 'true'; }
    function place() {
      tip.hidden = false;
      tip.style.top = 'calc(100% + 10px)';
      tip.style.bottom = 'auto';
      tip.classList.remove('is-above');
      tip.style.transform = 'none';
      var pad = 12;
      var vw = document.documentElement.clientWidth;
      var r = tip.getBoundingClientRect();
      var dx = 0;
      if (r.left < pad) dx = pad - r.left;
      else if (r.right > vw - pad) dx = (vw - pad) - r.right;
      if (dx) tip.style.transform = 'translateX(' + dx + 'px)';
      r = tip.getBoundingClientRect();
      if (r.bottom > window.innerHeight - pad && r.top > r.height + pad) {
        tip.style.top = 'auto';
        tip.style.bottom = 'calc(100% + 10px)';
        tip.classList.add('is-above');
        r = tip.getBoundingClientRect();
      }
      var br = btn.getBoundingClientRect();
      var cx = br.left + br.width / 2 - r.left - 6;
      cx = Math.max(10, Math.min(Math.max(10, r.width - 22), cx));
      tip.style.setProperty('--caret', cx + 'px');
    }
    function open() {
      var was = shown();
      tip.hidden = false;
      btn.setAttribute('aria-expanded', 'true');
      btn.setAttribute('aria-describedby', 'impact-info-tip');
      if (!was) openedAt = Date.now();
      place();
    }
    function close() {
      pinned = false;
      btn.setAttribute('aria-expanded', 'false');
      btn.removeAttribute('aria-describedby');
      tip.hidden = true;
      tip.classList.remove('is-above');
      tip.style.transform = 'none';
    }
    function sync() {
      if (pinned || ((hover || focus) && !suppress)) open();
      else close();
    }
    wrap.addEventListener('pointerenter', function () { hover = true; if (!suppress) sync(); });
    wrap.addEventListener('pointerleave', function () { hover = false; suppress = false; sync(); });
    btn.addEventListener('focus', function () { focus = true; suppress = false; sync(); });
    btn.addEventListener('blur', function () { focus = false; sync(); });
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();
      if (shown() && (Date.now() - openedAt > 400)) {
        pinned = false;
        suppress = true;
        close();
      } else {
        suppress = false;
        pinned = true;
        open();
      }
    });
    document.addEventListener('keydown', function (e) {
      if (e.key !== 'Escape' || !shown()) return;
      pinned = false;
      suppress = true;
      close();
      btn.blur();
    });
    document.addEventListener('pointerdown', function (e) {
      if (!shown() || wrap.contains(e.target)) return;
      pinned = false;
      suppress = true;
      close();
    });
    window.addEventListener('resize', function () { if (shown()) place(); });
  })();

  // PLACEHOLDER: day the counter read exactly 56,500,000 L (1 Farvardin 1405, Tehran). Change here only.
  var COUNTER_BASE_DATE = '2026-03-21T00:00:00+03:30';

  function calculateWaterSaved(baseDate, now) {
    if (now === undefined) now = Date.now();
    const baseLiters = 56_500_000;
    const annualBags = 1_200_000;
    const litersPerBag = 10;
    const annualGrowth = 0.17;
    const secondsPerYear = 365 * 24 * 60 * 60;
    const baseTime = new Date(baseDate).getTime();
    if (!Number.isFinite(baseTime)) throw new Error('Invalid base date');
    const elapsedSeconds = Math.max(0, (now - baseTime) / 1000);
    const elapsedYears = elapsedSeconds / secondsPerYear;
    const annualLiters = annualBags * litersPerBag;
    return baseLiters + (annualLiters / annualGrowth) * Math.expm1(Math.log1p(annualGrowth) * elapsedYears);
  }
  // litres per second at `now` (derivative of the formula)
  function rateNow(now) {
    var y = Math.max(0, (now - Date.parse(COUNTER_BASE_DATE)) / 1000) / 31536000;
    return (12e6 / 0.17) * Math.log1p(0.17) * Math.pow(1.17, y) / 31536000;
  }
  window.calculateWaterSaved = calculateWaterSaved;
  function L(now) { return calculateWaterSaved(COUNTER_BASE_DATE, now); }

  var root = document.querySelector('[data-impact-counter]');
  if (!root) return;
  var num = root.querySelector('.impact-num');
  var mode = root.dataset.counter || document.documentElement.dataset.counter || 'm1';
  root.classList.add('cnt-' + mode);
  var locale = root.dataset.locale || 'fa-IR';
  var nf = new Intl.NumberFormat(locale, { maximumFractionDigits: 0 });
  var nf2 = new Intl.NumberFormat(locale, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  function fmt(n) { return nf.format(Math.floor(n)); }
  var sr = document.createElement('span'); sr.className = 'sr-only';
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  window.__counterLog = function () { var t = Date.now(); return { t: new Date(t).toISOString(), value: L(t), shown: num.textContent }; };

  if (reduce) {
    var p = function () { num.textContent = fmt(L(Date.now())); };
    p(); setInterval(p, 60000); return;
  }
  function onView(cb) {
    if (!('IntersectionObserver' in window)) return cb();
    var io = new IntersectionObserver(function (e) { if (e.some(function (x) { return x.isIntersecting; })) { io.disconnect(); cb(); } }, { threshold: 0.35 });
    io.observe(root);
  }
  var ease = function (t) { return 1 - Math.pow(1 - t, 3); };

  /* ---------- M1 odometer ---------- */
  if (mode === 'm1') {
    var glyph = '۰۱۲۳۴۵۶۷۸۹';
    var odo = document.createElement('span'); odo.className = 'odo'; odo.dir = 'ltr'; odo.setAttribute('aria-hidden', 'true');
    var s = fmt(L(Date.now())), cols = [], nd = s.replace(/[^۰-۹]/g, '').length, seen = 0;
    for (var i = 0; i < s.length; i++) {
      var ch = s[i];
      if (glyph.indexOf(ch) < 0) { var sp = document.createElement('span'); sp.className = 'odo-sep'; sp.textContent = ch; odo.appendChild(sp); continue; }
      var col = document.createElement('span'); col.className = 'odo-col';
      var st = document.createElement('span'); st.className = 'odo-strip';
      for (var k = 0; k <= 10; k++) { var c = document.createElement('span'); c.className = 'odo-cell'; c.textContent = glyph[k % 10]; st.appendChild(c); }
      col.appendChild(st); odo.appendChild(col);
      cols.push({ st: st, place: nd - ++seen, pos: 0 });
    }
    num.textContent = ''; num.appendChild(sr); num.appendChild(odo);
    // continuous digit position: place p shows value/10^p mod 10, with carry rolling only in last 10% of lower digit
    function posFor(v, p) {
      var q = v / Math.pow(10, p), d = Math.floor(q) % 10;
      if (p === 0) { var f = v % 1; return d + (f > 0.8 ? (f - 0.8) / 0.2 : 0); }
      var lower = posFor(v, p - 1); // carry rolls in with the lower digit
      return d + (lower > 9 ? (lower - 9) : 0);
    }
    function paint(v) { cols.forEach(function (c) { c.st.style.transform = 'translateY(' + (-(posFor(v, c.place) % 10) * 1.2) + 'em)'; }); sr.textContent = fmt(v); }
    var base = 56500000;
    paint(base);
    onView(function () {
      var t0 = performance.now(), D = 2200;
      (function f(now) {
        var t = Math.min(1, (now - t0) / D), target = L(Date.now());
        paint(base + (target - base) * ease(t));
        requestAnimationFrame(t < 1 ? f : function g() { paint(L(Date.now())); requestAnimationFrame(g); });
      })(t0);
    });
    return;
  }

  /* ---------- M2 flowing water ---------- */
  if (mode === 'm2') {
    var clip = document.createElement('div'); clip.className = 'cnt-water-clip'; clip.setAttribute('aria-hidden', 'true');
    var water = document.createElement('div'); water.className = 'cnt-water';
    water.innerHTML = '<svg viewBox="0 0 400 20" preserveAspectRatio="none"><path d="M0 10 Q50 0 100 10 T200 10 T300 10 T400 10 V20 H0Z"/></svg><svg viewBox="0 0 400 20" preserveAspectRatio="none"><path d="M0 10 Q50 20 100 10 T200 10 T300 10 T400 10 V20 H0Z"/></svg>';
    clip.appendChild(water);
    var drop = document.createElement('span'); drop.className = 'cnt-drop'; drop.setAttribute('aria-hidden', 'true');
    root.insertBefore(clip, root.firstChild); root.appendChild(drop);
    // fraction of the current Persian year (from base date, one 365-day year)
    function frac() { return Math.min(1, Math.max(0, (Date.now() - Date.parse(COUNTER_BASE_DATE)) / 31536e6)); }
    num.textContent = fmt(56500000);
    onView(function () {
      root.style.setProperty('--fill', (frac() * 100).toFixed(2) + '%');
      var t0 = performance.now(), D = 2000, last = -1;
      (function f(now) {
        var t = Math.min(1, (now - t0) / D), v = t < 1 ? 56500000 + (L(Date.now()) - 56500000) * ease(t) : L(Date.now());
        var iv = Math.floor(v);
        if (iv !== last) { if (t >= 1 && last > 0) { drop.classList.remove('go'); void drop.offsetWidth; drop.classList.add('go'); } num.textContent = fmt(iv); last = iv; }
        requestAnimationFrame(f);
      })(t0);
    });
    return;
  }

  /* ---------- M3 pulse + rate ---------- */
  var rate = document.createElement('p'); rate.className = 'cnt-rate';
  var bar = document.createElement('div'); bar.className = 'cnt-bar'; bar.innerHTML = '<i></i>';
  var barLbl = document.createElement('p'); barLbl.className = 'cnt-barlbl';
  root.appendChild(rate); root.appendChild(bar); root.appendChild(barLbl);
  num.textContent = fmt(56500000);
  function render(iv, prev) {
    var a = fmt(iv), b = prev == null ? '' : fmt(prev), h = '';
    for (var i = 0; i < a.length; i++) h += (b.length === a.length && b[i] !== a[i]) ? '<span class="chg">' + a[i] + '</span>' : a[i];
    num.innerHTML = '<span dir="ltr" aria-hidden="true">' + h + '</span>';
    num.appendChild(sr); sr.textContent = a;
  }
  onView(function () {
    var t0 = performance.now(), D = 1800, last = null;
    (function f(now) {
      var t = Math.min(1, (now - t0) / D), real = L(Date.now()), v = t < 1 ? 56500000 + (real - 56500000) * ease(t) : real;
      var iv = Math.floor(v);
      if (iv !== last) { render(iv, t >= 1 ? last : null); last = iv; }
      var r = rateNow(Date.now());
      rate.innerHTML = '<bdi dir="ltr">+' + nf2.format(r) + '</bdi> لیتر در هر ثانیه';
      var rem = real % 1000;
      bar.firstChild.style.width = (rem / 10).toFixed(2) + '%';
      barLbl.textContent = '≈ ' + nf.format(Math.ceil((1000 - rem) / r)) + ' ثانیه تا هزار لیتر بعدی';
      requestAnimationFrame(f);
    })(t0);
  });
})();
