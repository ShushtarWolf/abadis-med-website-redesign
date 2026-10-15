/* Home impact counter: odometer count-up on view, then a live rolling tick. */
(function () {
  var root = document.querySelector('[data-impact-counter]');
  if (!root) return;
  var num = root.querySelector('.impact-num');
  if (!num) return;
  var start = Date.parse(root.dataset.start);
  var perYear = +root.dataset.perYear;
  if (!isFinite(start) || !isFinite(perYear) || perYear < 0) return;
  var perMs = perYear / (365.25 * 864e5);
  var locale = root.dataset.locale || 'fa-IR';
  var nf = new Intl.NumberFormat(locale, { maximumFractionDigits: 0 });
  var plain = new Intl.NumberFormat(locale, { useGrouping: false, maximumFractionDigits: 0 });
  var glyphs = [];
  var glyphIndex = Object.create(null);
  for (var d = 0; d < 10; d++) {
    glyphs.push(plain.format(d));
    glyphIndex[glyphs[d]] = d;
  }
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function litres() { return Math.max(0, (Date.now() - start) * perMs); }
  function format(n) { return nf.format(Math.max(0, Math.floor(n))); }

  if (reduce) {
    function paintStatic() { num.textContent = format(litres()); }
    paintStatic();
    setInterval(paintStatic, 5000);
    return;
  }

  var readout = document.createElement('span');
  readout.className = 'sr-only';
  var odo = document.createElement('span');
  odo.className = 'odo';
  odo.dir = 'ltr';
  odo.setAttribute('aria-hidden', 'true');
  var cols = [];
  var h = 0;
  var digitW = 0;
  var raf = 0;
  var phase = 'wait';
  var lastInt = 0;
  var lastT = 0;

  function tokens(n) {
    var s = format(n);
    var digitCount = 0;
    var i;
    for (i = 0; i < s.length; i++) if (glyphIndex[s[i]] != null) digitCount++;
    var out = [];
    var seen = 0;
    for (i = 0; i < s.length; i++) {
      var ch = s[i];
      var gi = glyphIndex[ch];
      if (gi == null) out.push({ sep: ch });
      else out.push({ gi: gi, place: digitCount - ++seen });
    }
    return out;
  }

  function build(n) {
    cols = [];
    odo.textContent = '';
    tokens(n).forEach(function (tok) {
      if (tok.sep != null) {
        var sep = document.createElement('span');
        sep.className = 'odo-sep';
        sep.textContent = tok.sep;
        odo.appendChild(sep);
        return;
      }
      var col = document.createElement('span');
      col.className = 'odo-col';
      var strip = document.createElement('span');
      strip.className = 'odo-strip';
      var i;
      for (i = 0; i <= 10; i++) {
        var cell = document.createElement('span');
        cell.className = 'odo-cell';
        cell.textContent = glyphs[i % 10];
        strip.appendChild(cell);
      }
      col.appendChild(strip);
      odo.appendChild(col);
      cols.push({ el: col, strip: strip, place: tok.place, gi: tok.gi, pos: 0, dest: 0 });
    });
  }

  function measure() {
    var probe = document.createElement('span');
    probe.className = 'odo-cell';
    probe.style.cssText = 'position:absolute;visibility:hidden;white-space:pre';
    probe.textContent = glyphs.join('');
    num.appendChild(probe);
    var box = probe.getBoundingClientRect();
    digitW = box.width / 10;
    h = box.height;
    num.removeChild(probe);
    if (!(h > 0)) h = 0;
    if (!(digitW > 0)) digitW = h * 0.62;
    cols.forEach(function (c) {
      c.el.style.width = digitW + 'px';
      c.el.style.height = h + 'px';
      Array.prototype.forEach.call(c.strip.children, function (cell) {
        cell.style.height = h + 'px';
      });
    });
    odo.style.height = h + 'px';
  }

  function paint(c) {
    if (!(h > 0)) return;
    var m = ((c.pos % 10) + 10) % 10;
    c.strip.style.transform = 'translateY(' + (-m * h) + 'px)';
  }

  function paintAll() { cols.forEach(paint); }

  function label(n) { readout.textContent = format(n); }

  function digitAt(n, place) {
    return Math.floor(Math.floor(n) / Math.pow(10, place)) % 10;
  }

  function snap(v) {
    var iv = Math.floor(v);
    cols.forEach(function (c) {
      var d = digitAt(iv, c.place);
      if (c.place === 0) c.pos = c.dest = v % 10;
      else {
        var mod = ((c.pos % 10) + 10) % 10;
        c.pos = c.dest = (c.pos - mod) + d;
      }
      paint(c);
    });
    lastInt = iv;
    label(iv);
  }

  function countUp() {
    phase = 'count';
    var target = Math.floor(litres());
    var travel = cols.map(function (c) {
      var extra = c.place <= 1 ? 1 : 0;
      return extra * 10 + digitAt(target, c.place);
    });
    var t0 = performance.now();
    var DUR = 1700;
    function frame(now) {
      var t = Math.min(1, (now - t0) / DUR);
      var e = 1 - Math.pow(1 - t, 3);
      cols.forEach(function (c, i) {
        c.pos = travel[i] * e;
        paint(c);
      });
      if (t < 1) raf = requestAnimationFrame(frame);
      else beginLive();
    }
    raf = requestAnimationFrame(frame);
  }

  function beginLive() {
    phase = 'live';
    var v = litres();
    var iv = Math.floor(v);
    cols.forEach(function (c) {
      var mod = ((c.pos % 10) + 10) % 10;
      var base = c.pos - mod;
      var d = c.place === 0 ? (v % 10) : digitAt(iv, c.place);
      var step = d - mod;
      if (step < -1e-6) step += 10;
      c.dest = base + mod + step;
    });
    lastInt = iv;
    label(iv);
    lastT = performance.now();
    raf = requestAnimationFrame(live);
  }

  function live(now) {
    var dt = Math.min(48, Math.max(0, now - lastT));
    lastT = now;
    var v = litres();
    var iv = Math.floor(v);
    if (iv !== lastInt) {
      cols.forEach(function (c) {
        if (c.place === 0) return;
        var from = digitAt(lastInt, c.place);
        var to = digitAt(iv, c.place);
        c.dest += (to - from + 10) % 10;
      });
      lastInt = iv;
      label(iv);
    }
    var ones = null;
    cols.forEach(function (c) { if (c.place === 0) ones = c; });
    if (ones) {
      var raw = v % 10;
      var cur = ((ones.dest % 10) + 10) % 10;
      var delta = raw - cur;
      if (delta < -1) delta += 10;
      ones.dest += delta;
      var kOnes = 1 - Math.exp(-dt / 45);
      ones.pos += (ones.dest - ones.pos) * kOnes;
      paint(ones);
    }
    var k = 1 - Math.exp(-dt / 220);
    cols.forEach(function (c) {
      if (c.place === 0) return;
      c.pos += (c.dest - c.pos) * k;
      if (Math.abs(c.dest - c.pos) < 0.003) c.pos = c.dest;
      paint(c);
    });
    if (!document.hidden) raf = requestAnimationFrame(live);
  }

  document.addEventListener('visibilitychange', function () {
    if (phase !== 'live') return;
    if (document.hidden) {
      cancelAnimationFrame(raf);
      return;
    }
    snap(litres());
    lastT = performance.now();
    raf = requestAnimationFrame(live);
  });

  window.addEventListener('resize', function () {
    measure();
    paintAll();
  }, { passive: true });

  function mount() {
    var sample = Math.max(litres(), 1);
    build(sample);
    num.textContent = '';
    num.appendChild(readout);
    num.appendChild(odo);
    label(sample);
    measure();
    cols.forEach(function (c) { c.pos = 0; paint(c); });
    if (!('IntersectionObserver' in window)) { countUp(); return; }
    var io = new IntersectionObserver(function (ents) {
      if (!ents.some(function (e) { return e.isIntersecting; })) return;
      io.disconnect();
      countUp();
    }, { threshold: 0.35 });
    io.observe(root);
  }

  if (document.fonts && document.fonts.ready) document.fonts.ready.then(mount);
  else mount();
})();
