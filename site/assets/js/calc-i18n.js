/* EN/AR savings calculator: same coefficients as dial-practical abadis-common.js
   (Alireza, فرمول محاسبه گر). Surgery staff factor is 1.6; beds staff factor stays 1.7.
   Currency picker: hide cost, IRT (TGJU toman per USD), or a custom unit cost.
   IRT uses live price_dollar_rl (rial/10), then localStorage abadis-usd-toman, then LAST_KNOWN_USD_TOMAN. */
(function () {
  var root = document.querySelector('[data-calc-i18n]');
  if (!root) return;
  var lang = document.documentElement.lang || 'en';
  var nf = new Intl.NumberFormat(lang === 'ar' ? 'ar' : 'en', { maximumFractionDigits: 0 });
  var $ = function (s) { return root.querySelector(s); };
  function units(mode) {
    if (mode === 'surgery') { var n = +$('#ci-n').value || 0; return { w: n, c: n, staff: 1.6 }; }
    var a = +$('#ci-a').value || 0, b = +$('#ci-b').value || 0;
    return { w: a * 254 + b * 67, c: a * 254 + b * 65, staff: 1.7 };
  }
  var LAST_KNOWN_USD_TOMAN = 269500;
  var USD_RATE_KEY = 'abadis-usd-toman';
  var USD_RATE_URL = 'https://api.tgju.org/v1/market/indicator/today-table-data/price_dollar_rl?lang=fa&start=0&length=1';
  var usdToman = LAST_KNOWN_USD_TOMAN;
  try {
    var saved = JSON.parse(localStorage.getItem(USD_RATE_KEY) || '');
    if (saved && isFinite(+saved.toman) && +saved.toman > 0) usdToman = +saved.toman;
  } catch (e) {}
  function rialFromTgju(data) {
    var row = data && data.data && data.data[0];
    if (!row) return null;
    var s = String(row[0]).replace(/<[^>]*>/g, '');
    s = s.replace(/[۰-۹]/g, function (ch) { return String('۰۱۲۳۴۵۶۷۸۹'.indexOf(ch)); });
    s = s.replace(/[,،٬\s]/g, '');
    var n = Number(s);
    return isFinite(n) && n >= 10000 && n <= 1e12 ? n : null;
  }
  function loadUsdRate() {
    if (typeof fetch !== 'function') return;
    var ctrl = typeof AbortController === 'function' ? new AbortController() : null;
    var timer = setTimeout(function () { if (ctrl) ctrl.abort(); }, 8000);
    var opts = { cache: 'no-store' };
    if (ctrl) opts.signal = ctrl.signal;
    fetch(USD_RATE_URL, opts).then(function (r) {
      if (!r.ok) throw new Error('usd');
      return r.json();
    }).then(function (data) {
      var rial = rialFromTgju(data);
      if (rial == null) throw new Error('usd');
      usdToman = rial / 10;
      try {
        localStorage.setItem(USD_RATE_KEY, JSON.stringify({
          toman: usdToman, rial: rial, updatedAt: new Date().toISOString(), source: USD_RATE_URL
        }));
      } catch (e) {}
      run();
    }).catch(function () {}).then(function () { clearTimeout(timer); });
  }
  function run() {
    var mode = root.querySelector('[name=ci-mode]:checked').value;
    root.querySelectorAll('[data-mode]').forEach(function (el) { el.hidden = el.dataset.mode !== mode; });
    var u = units(mode), cur = $('#ci-cur').value;
    var unitCost = cur === 'IRT' ? usdToman : (+$('#ci-unit').value || 0);
    $('#ci-unit-row').hidden = cur !== 'custom';
    $('#ci-water').textContent = nf.format(u.w * 1.6 * 9.971);
    $('#ci-hours').textContent = nf.format(u.w * u.staff * 2.2 * 7.1 / 60);
    var costRow = $('#ci-cost-row');
    costRow.hidden = cur === 'none';
    var code = cur === 'IRT' ? 'IRT' : ($('#ci-code').value || '').toUpperCase().slice(0, 3);
    $('#ci-cost').textContent = nf.format(u.c * 2.5 * unitCost) + (code ? ' ' + code : '');
  }
  root.addEventListener('input', run);
  root.addEventListener('change', run);
  run();
  loadUsdRate();
})();
