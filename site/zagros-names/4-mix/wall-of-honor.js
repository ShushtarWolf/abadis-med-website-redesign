/* Sample 4 (wall part) — same as sample 3's «دیوار افتخار», except the counter hand-off (see counter()).
   Sample 3 — «دیوار افتخار»
   All 1,253 names sorted with the Persian collator in tall columns. While the section is pinned, scroll moves the
   columns vertically at slightly different speeds (they start staggered and all finish at the end of their list),
   so every name passes through the window. Search dims the rest, highlights matches, scrolls the page so the
   current match sits in the middle of the wall and lights it up (Enter = next match). Transform-only motion. */
(function () {
  'use strict';
  var ZN = window.ZN; if (!ZN) return;
  var clamp = ZN.clamp, seg = ZN.seg, smooth = ZN.smooth;
  var root = document.documentElement;
  var trackEl = document.getElementById('honor'), stage = document.getElementById('whStage');
  var wall = document.getElementById('whWall'), input = document.getElementById('whQ'), res = document.getElementById('whRes');
  var numEl = document.getElementById('whNum'), countP = numEl.closest('.wh-count');
  var NAMES = [], N = 0, normd = [], nodes = [], cols = [], nCols = 0;
  var trackTop = 0, scrollLen = 1, wallH = 0, vh = 0;
  var target = 0, current = 0, raf = 0, lastT = 0, reduced = root.classList.contains('zh-reduced');
  var lastNum = -1;

  function colCount(w) { return w < 560 ? 2 : w < 900 ? 3 : w < 1200 ? 4 : 5; }
  // section letter = first character; names that start with a number share one «۰–۹» header
  function firstLetter(s) {
    var ch = s.trim().charAt(0);
    if (/[0-9\u06F0-\u06F9\u0660-\u0669]/.test(ch)) return '۰–۹';
    return /[\u0621-\u064A\u067E\u0686\u0698\u06A9\u06AF\u06CC\u0622]/.test(ch) ? ch.replace('آ', 'ا').replace('ي', 'ی').replace('ك', 'ک') : '';
  }

  function build() {
    var n = colCount(window.innerWidth);
    if (n === nCols && cols.length) return;
    nCols = n; wall.textContent = ''; cols = [];
    var per = Math.ceil(N / n);
    for (var c = 0; c < n; c++) {
      var col = document.createElement('div'); col.className = 'wh-col';
      var inner = document.createElement('div'); inner.className = 'wh-inner';
      col.appendChild(inner); wall.appendChild(col);          // RTL flex: first column (آ…) is on the right
      var prev = '';
      for (var i = c * per; i < Math.min(N, (c + 1) * per); i++) {
        var L = firstLetter(NAMES[i]);
        if (L && L !== prev) { var h = document.createElement('span'); h.className = 'wh-letter'; h.setAttribute('aria-hidden', 'true'); h.textContent = L; inner.appendChild(h); prev = L; }
        var el = nodes[i];
        if (!el) { el = nodes[i] = document.createElement('span'); el.className = 'wh-name'; el.setAttribute('role', 'listitem'); el.textContent = NAMES[i]; }
        el._col = c;
        inner.appendChild(el);
      }
      cols.push({ el: col, inner: inner, travel: 0, pad: 0, h: 0 });
    }
  }

  // every column starts filled at the top edge of the wall (y = TOP) and ends with its last name just above the
  // bottom fade; in between each column follows its own easing (p + a·p·(1−p)), so speeds differ only mid-scroll
  var TOP = 14, END_FADE = 52, EASE = [0.32, -0.26, 0.18, -0.34, 0.26];
  function measure() {
    vh = window.innerHeight;
    var cs = getComputedStyle(wall);
    wallH = wall.clientHeight - (parseFloat(cs.paddingBottom) || 0);     // visible window (Safari bottom bar excluded)
    var maxTravel = 0;
    cols.forEach(function (c, i) {
      c.h = c.inner.offsetHeight;
      c.travel = Math.max(0, c.h + TOP - (wallH - END_FADE));
      c.a = EASE[i % EASE.length];
      maxTravel = Math.max(maxTravel, c.travel);
    });
    if (!reduced) {
      // scroll length: names move ~2× (desktop) / ~3× (phone) the scroll distance, bounded to keep the page sane
      var ratio = window.innerWidth >= 900 ? 2 : 3;
      scrollLen = clamp(Math.round(maxTravel / ratio), vh * 2, vh * 9);
      trackEl.style.height = Math.round(stage.offsetHeight + scrollLen) + 'px';
    }
    trackTop = trackEl.getBoundingClientRect().top + window.pageYOffset;
  }

  function ease(c, p) { return p + c.a * p * (1 - p); }                  // monotonic (|a| < 1), 0→0 and 1→1
  function colY(c, p) { return TOP - ease(c, p) * c.travel; }
  function render(p) {
    for (var i = 0; i < cols.length; i++) {
      var c = cols[i], y = colY(c, p).toFixed(1);
      if (y !== c._y) { c.inner.style.transform = 'translate3d(0,' + y + 'px,0)'; c._y = y; }
    }
  }
  function counter() {
    // sample 4: the scene counter has already counted to the total; the wall's counter shows the settled number
    // and fades in as the scene's counter fades out (only one counter on screen at a time)
    var r = trackEl.getBoundingClientRect().top;
    if (lastNum !== N) { numEl.textContent = ZN.fa(N); lastNum = N; }
    var o = reduced ? 1 : smooth(clamp((vh * 0.75 - r) / (vh * 0.4), 0, 1));
    o = (Math.round(o * 100) / 100).toString();
    if (o !== countP.style.opacity) countP.style.opacity = o;
  }
  function readTarget() { target = clamp((window.pageYOffset - trackTop) / scrollLen, 0, 1); }
  function tick(t) {
    var dt = lastT ? Math.min(64, t - lastT) : 16.7; lastT = t;
    current += (target - current) * (1 - Math.pow(1 - 0.12, dt / 16.7));
    if (Math.abs(target - current) < 0.0002) current = target;
    render(current);
    if (current !== target) raf = requestAnimationFrame(tick); else { raf = 0; lastT = 0; }
  }
  function onScroll() { counter(); if (reduced) return; readTarget(); if (!raf) raf = requestAnimationFrame(tick); }
  var rz = 0, lastW = 0;
  function onResize() {
    if (rz) return;
    rz = requestAnimationFrame(function () {
      rz = 0;
      if (window.innerWidth !== lastW) { lastW = window.innerWidth; build(); }
      measure(); readTarget(); current = target; render(current); counter();
    });
  }

  // ---------- search ----------
  var hits = [], at = -1, qT = 0, lastQ = '';
  function clearMarks() { hits.forEach(function (i) { nodes[i].classList.remove('hit', 'focus'); }); }
  function runSearch() {
    var q = ZN.norm(input.value);
    clearMarks(); hits = []; at = -1; lastQ = q;
    if (q.length < 2) { wall.classList.remove('searching'); res.textContent = ''; return; }
    for (var i = 0; i < N; i++) if (normd[i].indexOf(q) !== -1) hits.push(i);
    wall.classList.add('searching');
    if (!hits.length) { res.textContent = 'موردی یافت نشد'; return; }
    hits.forEach(function (i) { nodes[i].classList.add('hit'); });
    at = 0; focusHit();
  }
  function focusHit() {
    var i = hits[at], el = nodes[i];
    el.classList.add('focus');
    res.textContent = ZN.fa(at + 1) + ' از ' + ZN.fa(hits.length);
    var c = cols[el._col], mid = el.offsetTop + el.offsetHeight / 2;
    if (reduced) { wall.scrollTo({ top: Math.max(0, mid - wall.clientHeight / 2), behavior: 'auto' }); return; }
    // progress at which this name sits in the middle of the wall window, then scroll the page there
    var want = c.travel ? clamp((TOP + mid - wallH / 2) / c.travel, 0, 1) : 0, lo = 0, hi = 1;
    for (var k = 0; k < 30; k++) { var m = (lo + hi) / 2; if (ease(c, m) < want) lo = m; else hi = m; }   // invert the easing
    var p = (lo + hi) / 2;
    window.scrollTo({ top: Math.round(trackTop + p * scrollLen), behavior: 'smooth' });
  }
  input.addEventListener('input', function () { clearTimeout(qT); qT = setTimeout(runSearch, 140); });
  input.addEventListener('keydown', function (e) {
    if (e.key !== 'Enter') return;
    e.preventDefault(); clearTimeout(qT);
    if (hits.length && ZN.norm(input.value) === lastQ) {           // Enter again = next match
      nodes[hits[at]].classList.remove('focus'); at = (at + 1) % hits.length; focusHit();
    } else runSearch();
  });

  ZN.loadNames().then(function (names) {
    var coll = new Intl.Collator('fa');
    NAMES = names.slice().sort(coll.compare); N = NAMES.length;
    normd = NAMES.map(ZN.norm);
    lastW = window.innerWidth;
    build(); measure(); readTarget(); current = target; render(current); counter();
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onResize, { passive: true });
    window.addEventListener('load', onResize);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(onResize);
    var mq = matchMedia('(prefers-reduced-motion: reduce)');
    var onMq = function () { reduced = mq.matches; trackEl.style.height = ''; onResize(); };
    if (mq.addEventListener) mq.addEventListener('change', onMq);
    window.__wall = { search: function (s) { input.value = s; runSearch(); return hits.map(function (i) { return NAMES[i]; }); }, get p() { return current; }, get N() { return N; } };
  }).catch(function (e) { console.error('[wall]', e); });
})();
