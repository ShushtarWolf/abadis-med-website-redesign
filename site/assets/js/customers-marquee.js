/* Homepage customers strip. CSS owns the loop and the pause.
   Duration follows the real width of one logo set so the speed stays calm
   when the row is long: 28px/s on desktop, 20px/s at 768px and below. */
(function () {
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
  var mobile = window.matchMedia('(max-width: 768px)');
  var DESKTOP_PX_PER_S = 28;
  var MOBILE_PX_PER_S = 20;

  document.querySelectorAll('[data-cust-marquee]').forEach(function (root) {
    var track = root.querySelector('.cust-marquee-track');
    var set = root.querySelector('.cust-marquee-set:not([aria-hidden="true"])');
    if (!track || !set) return;

    function pause() {
      if (reduce.matches) return;
      root.classList.add('is-paused');
    }
    function resume() {
      root.classList.remove('is-paused');
    }
    root.addEventListener('pointerdown', pause);
    root.addEventListener('pointerup', resume);
    root.addEventListener('pointercancel', resume);
    root.addEventListener('pointerleave', resume);

    var timer = 0;
    var lastWidth = 0;
    function apply() {
      if (reduce.matches) {
        track.style.animationDuration = '';
        lastWidth = 0;
        return;
      }
      var width = set.getBoundingClientRect().width;
      if (!(width > 1)) return;
      if (Math.abs(width - lastWidth) < 0.5) return;
      lastWidth = width;
      var speed = mobile.matches ? MOBILE_PX_PER_S : DESKTOP_PX_PER_S;
      track.style.animationDuration = (width / speed) + 's';
    }
    function schedule() {
      if (timer) window.clearTimeout(timer);
      timer = window.setTimeout(function () {
        timer = 0;
        apply();
      }, 150);
    }

    apply();
    window.addEventListener('resize', schedule);
    window.addEventListener('load', schedule);
    if (mobile.addEventListener) mobile.addEventListener('change', schedule);
    else if (mobile.addListener) mobile.addListener(schedule);
    if (reduce.addEventListener) reduce.addEventListener('change', apply);
    else if (reduce.addListener) reduce.addListener(apply);

    set.querySelectorAll('img').forEach(function (img) {
      if (img.complete) return;
      img.addEventListener('load', schedule);
      img.addEventListener('error', schedule);
    });
  });
})();
