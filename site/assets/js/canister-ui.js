/* Canister page: hero size switch, solid 3D viewer gate, canister / set toggle,
   tech-specs tabs. Works with suction-bag-ui.js (gallery, size tabs, iso gate).
   Three.js loads only when the visitor taps a 3D button. */
(function () {
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function webgl() {
    try {
      var c = document.createElement('canvas');
      return !!(window.WebGL2RenderingContext && (c.getContext('webgl2') || c.getContext('webgl')));
    } catch (e) { return false; }
  }
  var self = document.querySelector('script[src*="canister-ui.js"]');
  var ver = self ? (self.src.split('?')[1] || '') : '';
  function moduleUrl() {
    return self ? self.src.replace(/canister-ui\.js[^/]*$/, 'canister-viewer.js' + (ver ? '?' + ver : '')) : '';
  }

  /* Hero switch mirrors the size picker (one source of truth: .size-pick-btn). */
  var heroBtns = document.querySelectorAll('.cin-size-btn');
  function syncHero() {
    var sel = document.querySelector('.size-pick-btn[aria-selected="true"]');
    var size = sel ? sel.getAttribute('data-size') : '1';
    heroBtns.forEach(function (b) { b.setAttribute('aria-pressed', b.getAttribute('data-size') === size ? 'true' : 'false'); });
    return size;
  }
  heroBtns.forEach(function (b) {
    b.addEventListener('click', function () {
      var t = document.querySelector('.size-pick-btn[data-size="' + b.getAttribute('data-size') + '"]');
      if (t) t.click();
    });
  });
  var pick = document.querySelector('.size-pick');
  if (pick && 'MutationObserver' in window) {
    new MutationObserver(function () { syncHero(); releaseHidden(); })
      .observe(pick, {subtree: true, attributes: true, attributeFilter: ['aria-selected']});
  }
  syncHero();

  /* Solid viewers */
  var gl = !reduced && webgl();
  function release(frame) {
    if (frame._v) { try { frame._v.dispose(); } catch (e) {} frame._v = null; }
    frame.classList.remove('is-live', 'is-loading');
    delete frame.dataset.solidReady;
  }
  function releaseHidden() {
    document.querySelectorAll('[data-solid]').forEach(function (f) {
      if (f._v && (f.hidden || f.closest('[hidden]'))) release(f);
    });
  }
  document.querySelectorAll('[data-solid]').forEach(function (frame) {
    var btn = frame.querySelector('.solid-load');
    if (!btn) return;
    if (!gl) { frame.classList.add('is-still-only'); btn.hidden = true; return; }
    btn.addEventListener('click', function () {
      if (frame._v || frame.classList.contains('is-loading')) return;
      frame.classList.add('is-loading');
      import(moduleUrl()).then(function (m) {
        frame._v = m.mount(frame, {id: frame.getAttribute('data-solid-id')});
      }).catch(function () {
        frame.classList.remove('is-loading');
        frame.classList.add('is-still-only');
      });
    });
  });
  document.querySelectorAll('[data-solid-show]').forEach(function (b) {
    b.addEventListener('click', function () {
      var box = b.closest('.size-solid');
      var id = b.getAttribute('data-solid-show');
      box.querySelectorAll('[data-solid-show]').forEach(function (o) { o.setAttribute('aria-pressed', o === b ? 'true' : 'false'); });
      box.querySelectorAll('[data-solid]').forEach(function (f) {
        var on = f.getAttribute('data-solid-id') === id;
        f.hidden = !on;
        if (!on) release(f);
      });
    });
  });

  /* Tech-specs tabs */
  document.querySelectorAll('.spec-tabs').forEach(function (list) {
    var tabs = Array.prototype.slice.call(list.querySelectorAll('[role="tab"]'));
    function select(t) {
      tabs.forEach(function (o) {
        var on = o === t;
        o.setAttribute('aria-selected', on ? 'true' : 'false');
        o.tabIndex = on ? 0 : -1;
        var p = document.getElementById(o.getAttribute('aria-controls'));
        if (p) p.hidden = !on;
      });
    }
    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { select(t); });
      t.addEventListener('keydown', function (e) {
        var k = {ArrowRight: 1, ArrowLeft: -1, ArrowDown: 1, ArrowUp: -1}[e.key];
        if (!k) return;
        if (getComputedStyle(t).direction === 'rtl' && (e.key === 'ArrowRight' || e.key === 'ArrowLeft')) k = -k;
        var n = tabs[(i + k + tabs.length) % tabs.length];
        e.preventDefault(); select(n); n.focus();
      });
    });
  });
})();
