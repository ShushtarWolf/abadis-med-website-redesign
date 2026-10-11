// Hero option 6: savings figures from the approved calculator's formulas (site/dial-practical/common/abadis-common.js,
// A.F.surgery, "exactly as on the live abadis-med.com calculator"), for 5,000 surgeries a year.
// Final values are already in the HTML; this recomputes them and, on desktop with motion allowed, counts up once. No loop.
(function () {
  var hero = document.getElementById('hero');
  if (!hero) return;
  var n = 5000;
  var out = { water: n * 1.6 * 9.3, cost: n * 2.5 * 85000, hours: n * 1.7 / 60 * 2.2 * 7.1 };
  var fa = function (v) { return Math.round(v).toLocaleString('en-US').replace(/\d/g, function (d) { return '۰۱۲۳۴۵۶۷۸۹'[d]; }).replace(/,/g, '٬'); };
  var els = [].slice.call(hero.querySelectorAll('[data-k]'));
  var num = hero.querySelector('.s6-num');
  function set(e) {
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
})();
