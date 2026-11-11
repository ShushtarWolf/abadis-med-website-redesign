/* Product-switcher highlight + on-tap solid 3D viewers for the filters preview. */
(function () {
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function webgl() {
    try {
      var c = document.createElement('canvas');
      return !!(window.WebGLRenderingContext && (c.getContext('webgl2') || c.getContext('webgl')));
    } catch (e) { return false; }
  }

  var picks = document.querySelectorAll('.flt-pick .flt-pick-btn[href^="#"]');
  var sections = [];
  picks.forEach(function (a) {
    var el = document.getElementById((a.getAttribute('href') || '').slice(1));
    if (el) sections.push({a: a, el: el});
  });
  function pad() {
    var cs = getComputedStyle(document.documentElement);
    var v = parseFloat(cs.getPropertyValue('--bag-anchor-pad')) || 140;
    var b = parseFloat(cs.getPropertyValue('--flt-banner-h')) || 0;
    return v + b;
  }
  function spy() {
    var y = pad() + 8, current = null;
    sections.forEach(function (s) {
      if (s.el.getBoundingClientRect().top <= y) current = s;
    });
    picks.forEach(function (a) {
      if (current && a === current.a) a.setAttribute('aria-current', 'true');
      else a.removeAttribute('aria-current');
    });
  }
  if (sections.length) {
    window.addEventListener('scroll', function () { requestAnimationFrame(spy); }, {passive: true});
    window.addEventListener('resize', spy, {passive: true});
    spy();
  }
  picks.forEach(function (a) {
    a.addEventListener('click', function (e) {
      var el = document.getElementById((a.getAttribute('href') || '').slice(1));
      if (!el) return;
      e.preventDefault();
      var top = el.getBoundingClientRect().top + window.scrollY - pad();
      window.scrollTo({top: Math.max(0, top), behavior: reduced ? 'auto' : 'smooth'});
      try { history.replaceState(null, '', a.getAttribute('href')); } catch (err) {}
    });
  });

  function viewerUrl() {
    var s = document.querySelector('script[src*="filters-preview-ui.js"]');
    if (!s) return '../../assets/js/filters-viewer.js';
    return s.src.replace(/filters-preview-ui\.js[^/]*$/, 'filters-viewer.js');
  }
  document.querySelectorAll('[data-solid]').forEach(function (frame) {
    var btn = frame.querySelector('.solid-load');
    if (!btn) return;
    if (reduced || !webgl()) {
      frame.classList.add('is-still-only');
      btn.hidden = true;
      return;
    }
    btn.addEventListener('click', function () {
      if (frame._solid || frame.classList.contains('is-loading')) return;
      frame.classList.add('is-loading');
      import(viewerUrl()).then(function (mod) {
        frame._solid = mod.mount(frame, {
          id: frame.getAttribute('data-solid-id'),
          url: frame.getAttribute('data-solid-src')
        });
      }).catch(function () {
        frame.classList.remove('is-loading');
        frame.classList.add('is-still-only');
      });
    });
  });
})();
