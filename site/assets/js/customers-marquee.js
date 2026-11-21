/* Homepage customers strip: CSS owns the loop. This only pauses while a finger is down. */
(function () {
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
  document.querySelectorAll('[data-cust-marquee]').forEach(function (root) {
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
  });
})();
