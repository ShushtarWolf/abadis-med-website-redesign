// Hero option 6: savings figures from the approved calculator's formulas (site/dial-practical/common/abadis-common.js,
// A.F.surgery, "exactly as on the live abadis-med.com calculator"), for 5,000 surgeries a year.
// Final values are already in the HTML; this recomputes them and, on desktop with motion allowed, counts up once. No loop.
(function () {
  var hero = document.getElementById('hero');
  if (!hero) return;
  var n = 5000;
  var LAST_KNOWN_USD_TOMAN = 269500;
  var USD_RATE_KEY = 'abadis-usd-toman';
  var USD_RATE_URL = 'https://api.tgju.org/v1/market/indicator/today-table-data/price_dollar_rl?lang=fa&start=0&length=1';
  var usdToman = LAST_KNOWN_USD_TOMAN;
  try {
    var saved = JSON.parse(localStorage.getItem(USD_RATE_KEY) || '');
    if (saved && isFinite(+saved.toman) && +saved.toman > 0) usdToman = +saved.toman;
  } catch (e) {}
  function costs() { return { water: n * 1.6 * 9.971, cost: n * 2.5 * usdToman, hours: n * 1.6 * 2.2 * 7.1 / 60 }; }
  var fa = function (v) { return Math.round(v).toLocaleString('en-US').replace(/\d/g, function (d) { return '۰۱۲۳۴۵۶۷۸۹'[d]; }).replace(/,/g, '٬'); };
  var els = [].slice.call(hero.querySelectorAll('[data-k]'));
  var num = hero.querySelector('.s6-num');
  function set(e) {
    var out = costs();
    els.forEach(function (el) { el.textContent = fa(out[el.dataset.k] * e); });
    if (num) num.textContent = '+' + fa(1000 * e);
  }
  if (!hero.classList.contains('s6-armed')) { set(1); return; }
  var done = false;
  function play() {
    if (done) return; done = true;
    hero.classList.add('s6-play');
    var t0 = null, dur = 2000;
    setTimeout(function () {
      requestAnimationFrame(function step(t) {
        if (!t0) t0 = t;
        var p = Math.min(1, (t - t0) / dur), e = p * p * (3 - 2 * p);
        set(p < 1 ? e : 1);
        if (p < 1) requestAnimationFrame(step);
      });
    }, 250);
  }
  setTimeout(function () { if (!done) play(); }, 3900);
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) { if (es[0].isIntersecting) { io.disconnect(); play(); } }, { threshold: 0.25 });
    io.observe(hero);
  } else play();
  if (typeof fetch === 'function') {
    var ctrl = typeof AbortController === 'function' ? new AbortController() : null;
    var timer = setTimeout(function () { if (ctrl) ctrl.abort(); }, 8000);
    var opts = { cache: 'no-store' };
    if (ctrl) opts.signal = ctrl.signal;
    fetch(USD_RATE_URL, opts).then(function (r) {
      if (!r.ok) throw new Error('usd');
      return r.json();
    }).then(function (data) {
      var row = data && data.data && data.data[0];
      var rial = Number(String(row && row[0] || '').replace(/<[^>]*>/g, '').replace(/[,،٬\s]/g, ''));
      if (!isFinite(rial) || rial < 10000) throw new Error('usd');
      usdToman = rial / 10;
      try {
        localStorage.setItem(USD_RATE_KEY, JSON.stringify({ toman: usdToman, rial: rial, updatedAt: new Date().toISOString(), source: USD_RATE_URL }));
      } catch (e2) {}
      if (!hero.classList.contains('s6-armed') || done) set(1);
    }).catch(function () {}).then(function () { clearTimeout(timer); });
  }
})();
