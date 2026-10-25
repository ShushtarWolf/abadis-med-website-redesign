/* EN/AR savings calculator: same coefficients as dial-practical abadis-common.js
   (Alireza, فرمول محاسبه گر). Surgery staff factor is 1.6; beds staff factor stays 1.7.
   Currency picker: hide cost, IRT (original toman unit cost), or a custom unit cost. */
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
  function run() {
    var mode = root.querySelector('[name=ci-mode]:checked').value;
    root.querySelectorAll('[data-mode]').forEach(function (el) { el.hidden = el.dataset.mode !== mode; });
    var u = units(mode), cur = $('#ci-cur').value;
    var unitCost = cur === 'IRT' ? 85000 : (+$('#ci-unit').value || 0);
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
})();
