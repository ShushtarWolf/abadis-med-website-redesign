/* Gallery, size tabs, sub-nav, iso gate, and cinematic gate. Does not load Three.js on its own. */
(function () {
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var root = document.querySelector('[data-cin-root]');
  function webgl() {
    try {
      var c = document.createElement('canvas');
      return !!(window.WebGL2RenderingContext && (c.getContext('webgl2') || c.getContext('webgl')));
    } catch (e) { return false; }
  }
  if (root && !reduced && webgl()) {
    var src = root.getAttribute('data-cin-module');
    import(src).then(function (m) { return m.mount(root); }).catch(function () {
      root.classList.add('is-still');
    });
  } else if (root) {
    root.classList.add('is-still');
  }

  var film = document.getElementById('film');
  var header = document.querySelector('.header');
  var sub = document.querySelector('.bag-sub');
  function setStickyOffset() {
    var h = header ? Math.round(header.getBoundingClientRect().height) : 64;
    var sh = sub ? Math.round(sub.getBoundingClientRect().height) : 52;
    var rootEl = document.documentElement;
    rootEl.style.setProperty('--bag-sticky-top', h + 'px');
    rootEl.style.setProperty('--bag-anchor-pad', (h + sh + 10) + 'px');
  }
  if (film && header) {
    var heroObs = new IntersectionObserver(function (entries) {
      header.classList.toggle('past-hero', !entries[0].isIntersecting);
    }, { threshold: 0, rootMargin: '-1px 0px 0px 0px' });
    heroObs.observe(film);
  }
  setStickyOffset();
  window.addEventListener('resize', setStickyOffset);

  function initGallery(gal) {
    var rail = gal.querySelector('.gal-rail');
    var cards = gal.querySelectorAll('.gal-card');
    var dots = gal.querySelector('.gal-dots');
    if (!rail || !cards.length || !dots) return;
    dots.replaceChildren();
    function scrollToCard(i) {
      var card = cards[i];
      if (!card) return;
      var railBox = rail.getBoundingClientRect();
      var cardBox = card.getBoundingClientRect();
      var delta = (cardBox.left + cardBox.width / 2) - (railBox.left + railBox.width / 2);
      rail.scrollBy({ left: delta, behavior: reduced ? 'auto' : 'smooth' });
    }
    cards.forEach(function (_, i) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'gal-dot';
      b.setAttribute('aria-label', String(i + 1));
      b.addEventListener('click', function () { scrollToCard(i); });
      dots.appendChild(b);
    });
    function current() {
      var r = rail.getBoundingClientRect();
      var mid = r.left + r.width / 2;
      var best = 0, dist = Infinity;
      cards.forEach(function (card, i) {
        var c = card.getBoundingClientRect();
        var d = Math.abs(c.left + c.width / 2 - mid);
        if (d < dist) { dist = d; best = i; }
      });
      return best;
    }
    function paint(i) {
      if (i == null) i = current();
      dots.querySelectorAll('.gal-dot').forEach(function (d, n) {
        if (n === i) d.setAttribute('aria-current', 'true');
        else d.removeAttribute('aria-current');
      });
    }
    rail.addEventListener('scroll', function () { requestAnimationFrame(function () { paint(); }); }, { passive: true });
    paint();
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (entries) {
        var best = null, ratio = 0;
        entries.forEach(function (e) {
          if (e.intersectionRatio > ratio) { ratio = e.intersectionRatio; best = e.target; }
        });
        if (!best || ratio < 0.45) return;
        var i = Array.prototype.indexOf.call(cards, best);
        if (i >= 0) paint(i);
      }, { root: rail, threshold: [0.45, 0.6, 0.75, 0.9] });
      cards.forEach(function (card) { io.observe(card); });
    }
    function go(dir) {
      var i = Math.min(cards.length - 1, Math.max(0, current() + dir));
      scrollToCard(i);
    }
    var prev = gal.querySelector('.gal-prev');
    var next = gal.querySelector('.gal-next');
    if (prev) prev.addEventListener('click', function () { go(-1); });
    if (next) next.addEventListener('click', function () { go(1); });
  }
  document.querySelectorAll('[data-gal]').forEach(initGallery);

  var scroller = document.querySelector('.bag-sub-scroller');
  var hint = document.querySelector('.bag-sub-hint');
  if (scroller && hint) {
    function overflow() { return scroller.scrollWidth - scroller.clientWidth > 8; }
    function atEnd() {
      var rtl = getComputedStyle(scroller).direction === 'rtl';
      var max = scroller.scrollWidth - scroller.clientWidth;
      var x = Math.abs(scroller.scrollLeft);
      return x >= max - 4;
    }
    function sync() { hint.hidden = !overflow() || atEnd(); }
    hint.addEventListener('click', function () {
      var rtl = getComputedStyle(scroller).direction === 'rtl';
      scroller.scrollBy({ left: (rtl ? -1 : 1) * Math.round(scroller.clientWidth * 0.7), behavior: reduced ? 'auto' : 'smooth' });
    });
    scroller.addEventListener('scroll', sync, { passive: true });
    window.addEventListener('resize', sync);
    sync();
  }

  var heroCopy = document.querySelector('.cin-copy');
  function placeChat() {
    if (!heroCopy) return;
    var r = heroCopy.getBoundingClientRect();
    var on = r.bottom > 80 && r.top < window.innerHeight - 8;
    document.body.classList.toggle('bag-hero-cta', on);
  }
  if (heroCopy) {
    placeChat();
    window.addEventListener('scroll', function () { requestAnimationFrame(placeChat); }, { passive: true });
    window.addEventListener('resize', placeChat);
  }

  function activePanel() {
    return document.querySelector('.bag-panel:not([hidden])') || document.querySelector('.bag-panel');
  }
  function sectionEl(name, panel) {
    panel = panel || activePanel();
    if (!panel) return document.getElementById(name);
    if (name === 'gallery' || name === 'specs' || name === 'uses' || name === 'codes' || name === 'size' || name === 'packaging' || name === 'catalog') {
      return panel.querySelector('[data-sec="' + name + '"]') || document.getElementById(name);
    }
    return document.getElementById(name);
  }
  function anchorPad() {
    var v = getComputedStyle(document.documentElement).getPropertyValue('--bag-anchor-pad');
    return parseFloat(v) || 140;
  }
  function scrollToEl(el, behavior) {
    if (!el) return;
    var top = el.getBoundingClientRect().top + window.scrollY - anchorPad();
    window.scrollTo({ top: Math.max(0, top), behavior: behavior || (reduced ? 'auto' : 'smooth') });
  }

  var links = document.querySelectorAll('.bag-sub-scroller a[href^="#"]');
  function revealCurrent(link) {
    if (!scroller || !link) return;
    var s = scroller.getBoundingClientRect();
    var r = link.getBoundingClientRect();
    if (r.left >= s.left + 10 && r.right <= s.right - 10) return;
    /* Scroll only the horizontal subnav. link.scrollIntoView() also moves the
       document (sticky item + block:nearest) and was snapping iPhone scroll
       back to intro / the quote CTA. */
    var left = scroller.scrollLeft + (r.left + r.right) / 2 - (s.left + s.right) / 2;
    if (typeof scroller.scrollTo === 'function') {
      scroller.scrollTo({ left: left, behavior: reduced ? 'auto' : 'smooth' });
    } else {
      scroller.scrollLeft = left;
    }
  }
  function spy() {
    var y = anchorPad() + 8;
    var current = '';
    links.forEach(function (a) {
      var id = a.getAttribute('href').slice(1);
      var el = sectionEl(id);
      if (!el) return;
      if (el.getBoundingClientRect().top <= y) current = id;
    });
    links.forEach(function (a) {
      var on = a.getAttribute('href') === '#' + current;
      if (on) {
        a.setAttribute('aria-current', 'true');
        revealCurrent(a);
      } else {
        a.removeAttribute('aria-current');
      }
    });
  }
  /* Ignore click if a vertical swipe ended on sticky chrome (otherwise a flick
     up the page jumps back to معرفی / اعداد and feels stuck). */
  var ptr = {x: 0, y: 0, dragged: false};
  function markDown(x, y) { ptr = {x: x, y: y, dragged: false}; }
  function markMove(x, y) {
    if (Math.abs(y - ptr.y) > 12 || Math.abs(x - ptr.x) > 12) ptr.dragged = true;
  }
  document.addEventListener('pointerdown', function (e) { markDown(e.clientX, e.clientY); }, {passive: true});
  document.addEventListener('pointermove', function (e) { markMove(e.clientX, e.clientY); }, {passive: true});
  document.addEventListener('touchstart', function (e) {
    var t = e.changedTouches[0];
    if (t) markDown(t.clientX, t.clientY);
  }, {passive: true});
  document.addEventListener('touchmove', function (e) {
    var t = e.changedTouches[0];
    if (t) markMove(t.clientX, t.clientY);
  }, {passive: true});
  document.addEventListener('click', function (e) {
    if (!ptr.dragged) return;
    if (!e.target.closest('.bag-sub a, .bag-sub button, .site-header a, .site-header button, .size-pick-btn, .gal-dots button, .gal-prev, .gal-next, .bag-close a, .cin-cta a')) return;
    e.preventDefault();
    e.stopPropagation();
  }, true);
  if (links.length) {
    links.forEach(function (a) {
      a.addEventListener('click', function (e) {
        if (ptr && ptr.dragged) { e.preventDefault(); return; }
        var id = a.getAttribute('href').slice(1);
        var el = sectionEl(id);
        if (!el) return;
        e.preventDefault();
        scrollToEl(el);
      });
    });
    window.addEventListener('scroll', function () { requestAnimationFrame(spy); }, { passive: true });
    spy();
  }

  function isoModuleUrl() {
    var s = document.querySelector('script[src*="suction-bag-ui.js"]');
    if (!s) return '';
    return s.src.replace(/suction-bag-ui\.js[^/]*$/, 'cad-iso-viewer.js?v=20261110w');
  }
  document.querySelectorAll('[data-iso]').forEach(function (frame) {
    var btn = frame.querySelector('.iso-load');
    if (!btn) return;
    if (reduced || !webgl()) {
      frame.classList.add('is-still-only');
      btn.hidden = true;
      return;
    }
    btn.addEventListener('click', function () {
      if (frame._iso || frame.classList.contains('is-loading')) return;
      frame.classList.add('is-loading');
      import(isoModuleUrl()).then(function (mod) {
        frame._iso = mod.mount(frame, {
          id: frame.getAttribute('data-iso-id'),
          url: frame.getAttribute('data-iso-src')
        });
        frame.classList.remove('is-loading');
      }).catch(function () {
        frame.classList.remove('is-loading');
        frame.classList.add('is-still-only');
      });
    });
  });

  /* Align an RTL table so the sticky code column is on-screen at first paint.
     iOS Safari starts overflow:auto at the physical left, which hides the start
     (right) edge and leaves position:sticky unpainted until the first touch. */
  function alignTableStart(wrap) {
    if (!wrap) return;
    var first = wrap.querySelector('thead th:first-child') || wrap.querySelector('th:first-child, td:first-child');
    if (!first) return;
    var rtl = getComputedStyle(wrap).direction === 'rtl';
    function delta() {
      var wr = wrap.getBoundingClientRect();
      var fr = first.getBoundingClientRect();
      return rtl ? (fr.right - wr.right) : (fr.left - wr.left);
    }
    var d = delta();
    if (Math.abs(d) > 1) wrap.scrollLeft += d;
    var d2 = delta();
    if (Math.abs(d2) > Math.abs(d) && Math.abs(d) > 1) {
      wrap.scrollLeft -= d * 2;
    }
    /* Nudge so WebKit composites sticky cells before the first finger scroll. */
    var sl = wrap.scrollLeft;
    wrap.scrollLeft = sl + (rtl ? -1 : 1);
    wrap.scrollLeft = sl;
  }
  function updateTableFade(shell) {
    var wrap = shell.querySelector('.code-table-wrap');
    if (!wrap) return;
    var last = wrap.querySelector('thead th:last-child') || wrap.querySelector('th:last-child');
    var wr = wrap.getBoundingClientRect();
    var endVisible = wrap.scrollWidth <= wrap.clientWidth + 2;
    if (!endVisible && last) {
      var lr = last.getBoundingClientRect();
      endVisible = lr.left >= wr.left - 2 && lr.right <= wr.right + 2;
    }
    shell.classList.toggle('is-at-end', endVisible);
  }
  function initTable(shell) {
    var wrap = shell.querySelector('.code-table-wrap');
    if (!wrap) return;
    alignTableStart(wrap);
    updateTableFade(shell);
    wrap.addEventListener('scroll', function () { updateTableFade(shell); }, { passive: true });
  }
  function initVisibleTables() {
    document.querySelectorAll('.bag-panel:not([hidden]) [data-table-scroll], body > .code-table-shell').forEach(initTable);
    document.querySelectorAll('.bag-panel:not([hidden]) [data-table-scroll]').forEach(initTable);
  }

  function currentSize() {
    var p = activePanel();
    return (p && p.getAttribute('data-size')) || '1';
  }
  function setBagSize(size, opts) {
    opts = opts || {};
    var panel = document.getElementById('s' + size);
    if (!panel) return;
    document.querySelectorAll('.size-pick-btn').forEach(function (b) {
      var on = b.getAttribute('data-size') === size;
      b.setAttribute('aria-selected', on ? 'true' : 'false');
      b.tabIndex = on ? 0 : -1;
    });
    document.querySelectorAll('.bag-panel').forEach(function (p) {
      if (p.getAttribute('data-size') === size) p.removeAttribute('hidden');
      else p.setAttribute('hidden', '');
    });
    if (opts.scrollSec) {
      scrollToEl(sectionEl(opts.scrollSec, panel), 'auto');
    }
    requestAnimationFrame(function () {
      initVisibleTables();
      setStickyOffset();
      spy();
    });
    if (opts.hash !== false) {
      var hash = '#s' + size + (opts.scrollSec && opts.scrollSec !== 'gallery' ? '-' + opts.scrollSec : '');
      if (opts.scrollSec === 'gallery') hash = '#s' + size;
      try { history.replaceState(null, '', hash); } catch (e) {}
    }
  }
  document.querySelectorAll('.size-pick-btn').forEach(function (b) {
    b.addEventListener('click', function () {
      setBagSize(b.getAttribute('data-size'), { hash: true });
    });
    b.addEventListener('keydown', function (e) {
      var keys = { ArrowRight: 1, ArrowLeft: -1, ArrowDown: 1, ArrowUp: -1 };
      if (!(e.key in keys)) return;
      var rtl = getComputedStyle(b).direction === 'rtl';
      var dir = keys[e.key] * (rtl ? -1 : 1);
      var sizes = ['1', '2', '3'];
      var i = sizes.indexOf(currentSize()) + dir;
      if (i < 0 || i > 2) return;
      e.preventDefault();
      setBagSize(sizes[i], { hash: true });
      var next = document.querySelector('.size-pick-btn[data-size="' + sizes[i] + '"]');
      if (next) next.focus();
    });
  });

  function applyHash() {
    var h = (location.hash || '').replace(/^#/, '');
    if (!h) {
      initVisibleTables();
      return;
    }
    var m = h.match(/^s([123])(?:-(gallery|specs|uses|codes|size|packaging|catalog))?$/);
    if (m) {
      setBagSize(m[1], { hash: false, scrollSec: m[2] || null });
      return;
    }
    if (h === 'sizes') {
      scrollToEl(document.getElementById('sizes'));
      initVisibleTables();
      return;
    }
    var el = sectionEl(h);
    if (el) scrollToEl(el, 'auto');
    initVisibleTables();
  }
  applyHash();
  window.addEventListener('hashchange', applyHash);
  window.addEventListener('resize', function () { initVisibleTables(); });
  window.addEventListener('load', function () { initVisibleTables(); setStickyOffset(); });

  var pick = document.querySelector('.size-pick-vert');
  var stage = document.getElementById('sizes');
  if (pick && stage && 'IntersectionObserver' in window) {
    new IntersectionObserver(function (ents) {
      pick.classList.toggle('is-docked', ents.some(function (e) { return e.isIntersecting; }));
    }, { root: null, threshold: 0, rootMargin: '-15% 0px -15% 0px' }).observe(stage);
  }
})();
