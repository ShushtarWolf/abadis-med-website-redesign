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
    cards.forEach(function (_, i) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'gal-dot';
      b.setAttribute('aria-label', String(i + 1));
      b.addEventListener('click', function () {
        cards[i].scrollIntoView({ inline: 'center', block: 'nearest', behavior: reduced ? 'auto' : 'smooth' });
      });
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
    function paint() {
      var i = current();
      dots.querySelectorAll('.gal-dot').forEach(function (d, n) {
        if (n === i) d.setAttribute('aria-current', 'true');
        else d.removeAttribute('aria-current');
      });
    }
    rail.addEventListener('scroll', function () { requestAnimationFrame(paint); }, { passive: true });
    paint();
    function go(dir) {
      var i = Math.min(cards.length - 1, Math.max(0, current() + dir));
      cards[i].scrollIntoView({ inline: 'center', block: 'nearest', behavior: reduced ? 'auto' : 'smooth' });
    }
    var prev = gal.querySelector('.gal-prev');
    var next = gal.querySelector('.gal-next');
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
})();
