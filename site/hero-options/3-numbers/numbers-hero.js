// Hero option 3: start the silent loop when visible and count the stats up once.
(function () {
  var hero = document.getElementById('hero');
  if (!hero) return;
  var vid = hero.querySelector('.nh-vid');
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var saveData = navigator.connection && navigator.connection.saveData;
  var fa = function (n, plain) {
    var s = plain ? String(n) : n.toLocaleString('en-US');
    return s.replace(/\d/g, function (d) { return '۰۱۲۳۴۵۶۷۸۹'[d]; }).replace(/,/g, '٬');
  };
  function count() {
    if (reduce) return;
    [].forEach.call(hero.querySelectorAll('.nh-num'), function (el) {
      var to = +el.dataset.to, pre = el.dataset.prefix || '', plain = !!el.dataset.plain;
      var from = plain ? to - 30 : 0, t0 = null, dur = 1400;
      function step(t) {
        if (!t0) t0 = t;
        var p = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - p, 3);
        el.textContent = pre + fa(Math.round(from + (to - from) * e), plain);
        if (p < 1) requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
    });
  }
  function start() {
    count();
    if (vid && !reduce && !saveData) { var p = vid.play(); if (p && p.catch) p.catch(function () {}); }
  }
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) { if (es[0].isIntersecting) { io.disconnect(); start(); } }, { threshold: 0.2 });
    io.observe(hero);
  } else start();
})();
