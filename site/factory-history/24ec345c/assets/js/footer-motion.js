/* Footer scroll motion driver (see footer-motion.css).
   Desktop: fallback only for browsers without CSS scroll-driven animations
     (progress 0 when the footer's top touches the screen bottom, 1 just before it has fully entered).
   Phones (<=760px): always JS, in every browser, so iOS Safari behaves the same:
     progress runs while the footer's top edge moves from the screen bottom to ~30% from the top
     (finishing early, never later than just before the page bottom), with light smoothing.
   ?fm=js forces the JS path on desktop too (for testing). */
(function () {
  var f = document.querySelector('.site-footer');
  if (!f) return;
  var root = document.documentElement;
  var force = /[?&]fm=js\b/.test(location.search);
  var native = !!(window.CSS && CSS.supports && CSS.supports('animation-timeline: view()'));
  var rm = window.matchMedia('(prefers-reduced-motion: reduce)');
  var phoneMq = window.matchMedia('(max-width: 760px)');
  var PHONE_END = 0.30;       // footer top at 30% of the screen height = flat
  var SMOOTH = 0.2;           // phones: share of the remaining distance covered per frame
  var vh = 0, vw = 0, cur = -1, raf = 0, active = false;

  function num(name, dflt) {
    var v = parseFloat(getComputedStyle(f).getPropertyValue(name));
    return isNaN(v) ? dflt : v;
  }
  function measureViewport() {
    // Keep the height stable while the iOS URL bar shows/hides; re-measure only when the width changes (rotation).
    var w = root.clientWidth;
    if (w !== vw || !vh) { vw = w; vh = window.innerHeight; }
  }
  function target() {
    var y = 0, el = f; while (el) { y += el.offsetTop; el = el.offsetParent; }
    var top = y - window.pageYOffset;          // layout position (ignores the transform); rubber-band is clamped below
    var range;
    if (phoneMq.matches) {
      var maxScroll = root.scrollHeight - vh;
      var endTop = Math.max(vh * PHONE_END, y - maxScroll + 8); // must be reachable before the page ends
      range = vh - endTop;
    } else {
      range = Math.min(f.offsetHeight, vh) * 0.92; // matches 'entry 0% entry 92%' in the CSS
    }
    return Math.max(0, Math.min(1, (vh - top) / (range || 1)));
  }
  function apply(p) {
    if (p >= 0.999) { f.style.transform = ''; return; }
    var k = 1 - p;
    var tilt = num('--fm-tilt', -22), scale = num('--fm-scale', .94);
    f.style.transform = 'perspective(1000px) rotateX(' + (tilt * k).toFixed(3) + 'deg) scale(' + (1 - (1 - scale) * k).toFixed(4) + ')';
  }
  function frame() {
    raf = 0;
    if (!active) return;
    if (rm.matches) { f.style.transform = ''; cur = -1; return; }
    var t = target();
    if (cur < 0 || !phoneMq.matches) cur = t;
    else cur += (t - cur) * SMOOTH;
    if (Math.abs(t - cur) < 0.002) cur = t;
    apply(cur);
    if (cur !== t) raf = requestAnimationFrame(frame);
  }
  function req() { if (!raf) raf = requestAnimationFrame(frame); }
  function setup() {
    var want = force || !native || phoneMq.matches;
    if (want !== active) {
      active = want;
      root.classList.toggle('fm-js', want);
      if (!want) { f.style.transform = ''; cur = -1; }
    }
    measureViewport();
    if (active) { cur = -1; req(); }
  }
  window.addEventListener('scroll', req, { passive: true });
  window.addEventListener('resize', function () { measureViewport(); req(); });
  window.addEventListener('orientationchange', function () { vh = 0; setTimeout(setup, 250); });
  [rm, phoneMq].forEach(function (m) {
    if (m.addEventListener) m.addEventListener('change', setup); else if (m.addListener) m.addListener(setup);
  });
  setup();
})();
