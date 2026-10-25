(function () {
  var root = document.querySelector('[data-home-map]');
  if (!root) return;
  var dots = [].slice.call(root.querySelectorAll('.home-map-dot')).sort(function (a, b) {
    return (+a.getAttribute('data-seq') || 0) - (+b.getAttribute('data-seq') || 0);
  });
  if (!dots.length) return;

  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce) {
    dots.forEach(function (d) {
      d.classList.add('is-lit');
    });
    return;
  }

  var i = 0;
  var delay = 420;

  function lightNext() {
    if (i >= dots.length) return;
    dots[i].classList.add('is-lit');
    i += 1;
    if (i < dots.length) window.setTimeout(lightNext, delay);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      window.setTimeout(lightNext, 320);
    });
  } else {
    window.setTimeout(lightNext, 320);
  }
})();
