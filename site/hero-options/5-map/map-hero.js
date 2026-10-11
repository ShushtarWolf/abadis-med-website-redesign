// Hero option 5: when the hero is in view, play the one-time entrance (dots by region, count-up, export tint). No loop.
(function () {
  var hero = document.getElementById('hero');
  if (!hero || !hero.classList.contains('m5-armed')) return;
  var num = hero.querySelector('.m5-num');
  var fa = function (n) { return n.toLocaleString('en-US').replace(/\d/g, function (d) { return '۰۱۲۳۴۵۶۷۸۹'[d]; }).replace(/,/g, '٬'); };
  var done = false;
  function count() {
    if (!num) return;
    var to = +num.dataset.to, pre = num.dataset.prefix || '', t0 = null, dur = 2200;
    function step(t) {
      if (!t0) t0 = t;
      var p = Math.min(1, (t - t0) / dur), e = p * p * (3 - 2 * p);
      num.textContent = pre + fa(Math.round(to * e));
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  function play() {
    if (done) return; done = true;
    hero.classList.add('m5-play');
    setTimeout(count, 250);
  }
  // safety net: the inline fallback adds m5-play after 4s; make sure the number ends correct too
  setTimeout(function () { if (!done) play(); }, 3900);
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) { if (es[0].isIntersecting) { io.disconnect(); play(); } }, { threshold: 0.25 });
    io.observe(hero);
  } else play();
})();
