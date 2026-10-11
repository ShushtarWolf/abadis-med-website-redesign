// Hero option 1: calm scroll-scrub product reveal (no libraries).
// Without JS, with reduced motion, data saver or a slow connection, the CSS shows the finished still composition.
(function () {
  var track = document.getElementById('hero');
  if (!track) return;
  var mm = window.matchMedia ? function (q) { return matchMedia(q).matches; } : function () { return false; };
  var conn = navigator.connection || {};
  var still = mm('(prefers-reduced-motion: reduce)') || conn.saveData || /(^|-)2g$/.test(conn.effectiveType || '') ||
    /[?&]still=1/.test(location.search);

  // ---- count-up numbers (only figures already on the approved home page) ----
  var nums = [].slice.call(track.querySelectorAll('[data-count]'));
  var fa = function (n) { return String(n).replace(/\d/g, function (d) { return '۰۱۲۳۴۵۶۷۸۹'[d]; }); };
  function countUp() {
    if (still) return;
    var t0 = performance.now(), dur = 1600;
    nums.forEach(function (el) { el.dataset.final = el.textContent; });
    (function step(t) {
      var k = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - k, 3);
      nums.forEach(function (el) {
        var to = +el.dataset.count;
        el.textContent = (el.dataset.pre || '') + fa(Math.round(to * e)) + (el.dataset.post || '');
      });
      if (k < 1) requestAnimationFrame(step); else nums.forEach(function (el) { el.textContent = el.dataset.final; });
    })(t0);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', countUp); else countUp();

  if (still) return;

  // ---- scroll scrub ----
  var q = function (s) { return track.querySelector(s); };
  var b1 = q('.ph-b1'), b2 = q('.ph-b2'), b3 = q('.ph-b3'), lid = q('.ph-lid'), mouth = q('.ph-open');
  var f1 = q('.ph-f1'), f2 = q('.ph-f2'), hint = q('.ph-hint');
  var caps = [].slice.call(track.querySelectorAll('.ph-bag figcaption'));
  var fcaps = [].slice.call(track.querySelectorAll('.ph-filter figcaption'));
  track.classList.add('ph-live');

  var clamp = function (v) { return v < 0 ? 0 : v > 1 ? 1 : v; };
  var seg = function (p, a, b) { var t = clamp((p - a) / (b - a)); return t * t * (3 - 2 * t); }; // smoothstep
  var lerp = function (a, b, t) { return a + (b - a) * t; };
  var s0 = 1.2, dx1 = 0, dx3 = 0, cur = -1, target = 0, raf = 0;

  function measure() {
    var c2 = b2.offsetLeft; // offsetLeft ignores transforms; b2 is translated -50%, so its centre sits at offsetLeft
    dx1 = c2 - (b1.offsetLeft + b1.offsetWidth / 2);
    dx3 = c2 - (b3.offsetLeft + b3.offsetWidth / 2);
    s0 = window.innerWidth <= 860 ? 1.3 : 1.18;
  }
  function progress() {
    var r = track.getBoundingClientRect();
    var span = r.height - window.innerHeight;
    return span > 0 ? clamp(-r.top / span) : 1;
  }
  function render(p) {
    // 1) the 2 L bag turns gently toward the viewer
    var a = seg(p, 0, 0.34);
    b2.style.transform = 'translateX(-50%) perspective(900px) rotateY(' + lerp(-16, 0, a).toFixed(2) + 'deg) scale(' + lerp(s0, 1, a).toFixed(4) + ')';
    // 2) the lid lifts and tilts open
    var o = seg(p, 0.22, 0.56);
    lid.style.transform = 'translateY(' + lerp(0, -34, o).toFixed(2) + '%) rotate(' + lerp(0, -4, o).toFixed(2) + 'deg)';
    mouth.style.opacity = o.toFixed(3);
    // 3) the 1 L and 3 L bags slide out from behind it
    var s = seg(p, 0.38, 0.8);
    b1.style.transform = 'translateX(' + (dx1 * (1 - s)).toFixed(1) + 'px) scale(' + lerp(0.82, 1, s).toFixed(4) + ')';
    b3.style.transform = 'translateX(' + (dx3 * (1 - s)).toFixed(1) + 'px) scale(' + lerp(0.82, 1, s).toFixed(4) + ')';
    b1.style.opacity = b3.style.opacity = clamp(s * 1.6).toFixed(3);
    var c = seg(p, 0.6, 0.86).toFixed(3);
    caps.forEach(function (el) { el.style.opacity = c; });
    // 4) the filters rise out of the open bag
    [f1, f2].forEach(function (f, i) {
      var t = seg(p, 0.62 + i * 0.06, 0.94 + i * 0.03);
      f.style.transform = 'translateY(' + lerp(70, 0, t).toFixed(1) + '%) scale(' + lerp(0.6, 1, t).toFixed(4) + ')';
      f.style.opacity = clamp(t * 1.4).toFixed(3);
    });
    var fc = seg(p, 0.85, 1).toFixed(3);
    fcaps.forEach(function (el) { el.style.opacity = fc; });
    if (hint) hint.style.opacity = (0.7 * (1 - seg(p, 0, 0.12))).toFixed(3);
  }
  function tick() {
    raf = 0;
    // light smoothing so touch scrolling on iPhone stays calm, never laggy
    cur = cur < 0 ? target : cur + (target - cur) * 0.22;
    if (Math.abs(target - cur) < 0.0008) cur = target;
    render(cur);
    if (cur !== target) raf = requestAnimationFrame(tick);
  }
  function onScroll() { target = progress(); if (!raf) raf = requestAnimationFrame(tick); }
  function onResize() { measure(); cur = -1; onScroll(); }
  measure();
  target = progress(); cur = -1; tick();
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onResize);
  window.addEventListener('load', onResize);
})();
