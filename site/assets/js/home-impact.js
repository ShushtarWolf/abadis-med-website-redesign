/* Home impact counter: keeps ticking (estimated water saved since a start date at a yearly rate). */
(function () {
  var el = document.querySelector('[data-impact-counter]');
  if (!el) return;
  var num = el.querySelector('.impact-num');
  var start = Date.parse(el.dataset.start), perMs = (+el.dataset.perYear) / (365.25 * 864e5);
  var nf = new Intl.NumberFormat(el.dataset.locale || 'fa-IR', { maximumFractionDigits: 0 });
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  function tick() { num.textContent = nf.format(Math.max(0, (Date.now() - start) * perMs)); }
  tick();
  setInterval(tick, reduce ? 5000 : 120);
})();
