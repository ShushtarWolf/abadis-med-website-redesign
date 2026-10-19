/* Fallback for browsers without CSS scroll-driven animations (see footer-motion.css).
   Same motion: progress 0 when the footer's top touches the bottom of the screen,
   1 just before the footer has fully entered (or fills the screen). ?fm=js forces it for testing. */
(function () {
  var f = document.querySelector('.site-footer');
  if (!f) return;
  var force = /[?&]fm=js\b/.test(location.search);
  var native = window.CSS && CSS.supports && CSS.supports('animation-timeline: view()');
  if (native && !force) return;
  var mq = window.matchMedia('(prefers-reduced-motion: reduce)');
  document.documentElement.classList.add('fm-js');
  var ticking = false;
  function num(name, dflt) {
    var v = parseFloat(getComputedStyle(f).getPropertyValue(name));
    return isNaN(v) ? dflt : v;
  }
  function update() {
    ticking = false;
    if (mq.matches) { f.style.transform = ''; return; }
    var vh = window.innerHeight;
    var y = 0, el = f; while (el) { y += el.offsetTop; el = el.offsetParent; }
    var top = y - window.pageYOffset;                         // layout position, ignores the transform
    var range = (Math.min(f.offsetHeight, vh) * 0.92) || 1;   // matches 'entry 0% entry 92%' in the CSS
    var p = Math.max(0, Math.min(1, (vh - top) / range));
    if (p >= 1) { f.style.transform = ''; return; }
    var k = 1 - p;
    var tilt = num('--fm-tilt', -22), scale = num('--fm-scale', .94);
    f.style.transform = 'perspective(1000px) rotateX(' + (tilt * k).toFixed(3) + 'deg) scale(' + (1 - (1 - scale) * k).toFixed(4) + ')';
  }
  function req() { if (!ticking) { ticking = true; requestAnimationFrame(update); } }
  window.addEventListener('scroll', req, { passive: true });
  window.addEventListener('resize', req);
  if (mq.addEventListener) mq.addEventListener('change', req);
  update();
})();
