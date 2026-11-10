/* Gallery, sub-nav hint, and cinematic gate. Does not load Three.js. */
(function () {
  var root = document.querySelector('[data-cin-root]');
  function webgl() {
    try {
      var c = document.createElement('canvas');
      return !!(window.WebGL2RenderingContext && (c.getContext('webgl2') || c.getContext('webgl')));
    } catch (e) { return false; }
  }
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
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
  if (film && header) {
    var heroObs = new IntersectionObserver(function (entries) {
      header.classList.toggle('past-hero', !entries[0].isIntersecting);
    }, { threshold: 0, rootMargin: '-1px 0px 0px 0px' });
    heroObs.observe(film);
  }

  document.querySelectorAll('[data-gal]').forEach(function (gal) {
    var rail = gal.querySelector('.gal-rail');
    var cards = gal.querySelectorAll('.gal-card');
    var dots = gal.querySelector('.gal-dots');
    if (!rail || !cards.length || !dots) return;
    // Rebuild dots so a warm cache or a second init cannot leave a single stale pip.
    dots.replaceChildren();
    function scrollToCard(i) {
      var card = cards[i];
      if (!card) return;
      // Visual midpoint, so RTL and LTR both land on the same slide.
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
    // dir is in DOM order, so قبلی / Previous always steps to the prior slide in RTL and LTR.
    if (prev) prev.addEventListener('click', function () { go(-1); });
    if (next) next.addEventListener('click', function () { go(1); });
  });

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

  var links = document.querySelectorAll('.bag-sub-scroller a[href^="#"]');
  function spy() {
    var y = 160;
    var current = '';
    links.forEach(function (a) {
      var id = a.getAttribute('href').slice(1);
      var el = document.getElementById(id);
      if (!el) return;
      if (el.getBoundingClientRect().top <= y) current = id;
    });
    links.forEach(function (a) {
      var on = a.getAttribute('href') === '#' + current;
      if (on) a.setAttribute('aria-current', 'true');
      else a.removeAttribute('aria-current');
    });
  }
  if (links.length) {
    window.addEventListener('scroll', function () { requestAnimationFrame(spy); }, { passive: true });
    spy();
  }

  function isoModuleUrl() {
    var s = document.querySelector('script[src*="suction-bag-ui.js"]');
    if (!s) return '';
    return s.src.replace(/suction-bag-ui\.js[^/]*$/, 'cad-iso-viewer.js?v=20261110s');
  }
  function themeKey() {
    var t = document.documentElement.getAttribute('data-theme');
    return (t === 'dark' || t === 'noir') ? 'dark' : 'light';
  }
  function applyIsoStill(frame, size) {
    if (frame.getAttribute('data-iso-kind') !== 'liner' || !size) return;
    var light = frame.getAttribute('data-iso-still-' + size + '-light');
    var dark = frame.getAttribute('data-iso-still-' + size + '-dark');
    var imgL = frame.querySelector('.iso-still-light');
    var imgD = frame.querySelector('.iso-still-dark');
    if (light && imgL) imgL.src = light;
    if (dark && imgD) imgD.src = dark;
    frame.setAttribute('data-iso-size', size);
  }
  function currentIsoId(frame) {
    if (frame.getAttribute('data-iso-kind') === 'filter') return frame.getAttribute('data-iso-id');
    var size = frame.getAttribute('data-iso-size') || '1';
    return frame.getAttribute('data-iso-id-' + size);
  }
  function currentIsoSrc(frame) {
    if (frame.getAttribute('data-iso-kind') === 'filter') return frame.getAttribute('data-iso-src');
    var size = frame.getAttribute('data-iso-size') || '1';
    return frame.getAttribute('data-iso-src-' + size);
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
      var url = isoModuleUrl();
      import(url).then(function (mod) {
        frame._iso = mod.mount(frame, { id: currentIsoId(frame), url: currentIsoSrc(frame) });
        frame.classList.remove('is-loading');
      }).catch(function () {
        frame.classList.remove('is-loading');
        frame.classList.add('is-still-only');
      });
    });
  });
  function setBagSize(size, scroll) {
    document.querySelectorAll('.size-pick-btn').forEach(function (b) {
      if (b.getAttribute('data-size') === size) b.setAttribute('aria-selected', 'true');
      else b.setAttribute('aria-selected', 'false');
    });
    document.querySelectorAll('[data-iso-kind="liner"]').forEach(function (frame) {
      applyIsoStill(frame, size);
      if (frame._iso) {
        frame._iso.setModel(currentIsoId(frame), currentIsoSrc(frame));
      }
    });
    if (scroll) {
      var el = document.getElementById('s' + size);
      if (el) el.scrollIntoView({ behavior: reduced ? 'auto' : 'smooth', block: 'start' });
    }
  }
  document.querySelectorAll('.size-pick-btn').forEach(function (b) {
    b.addEventListener('click', function () { setBagSize(b.getAttribute('data-size'), true); });
  });
  /* Keep the iso size in step if the reader scrolls the sections by hand. */
  var sizeSecs = ['1', '2', '3'].map(function (s) { return document.getElementById('s' + s); }).filter(Boolean);
  if (sizeSecs.length && 'IntersectionObserver' in window) {
    var sizeIo = new IntersectionObserver(function (entries) {
      var best = null, ratio = 0;
      entries.forEach(function (e) {
        if (e.isIntersecting && e.intersectionRatio > ratio) { ratio = e.intersectionRatio; best = e.target; }
      });
      if (!best) return;
      var id = best.id || '';
      if (id.charAt(0) === 's') setBagSize(id.slice(1), false);
    }, { rootMargin: '-30% 0px -45% 0px', threshold: [0.2, 0.4, 0.6] });
    sizeSecs.forEach(function (el) { sizeIo.observe(el); });
  }

})();
