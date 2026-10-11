/* hero-test/birds: ~110 painterly birds rise from the Zagros ridge and flock into the Abadis mark,
   then hand over to the real mark (teal, modest opacity). One canvas, vanilla JS, plays once.
   No pointer interaction. prefers-reduced-motion: the mark is shown directly. */
(function () {
  'use strict';
  var stage = document.getElementById('hero');
  var canvas = document.getElementById('btCanvas');
  var mark = document.getElementById('btMark');
  var data = window.ABADIS_MARK;
  if (!stage || !canvas || !mark || !data) return;

  var reduced = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  function showMark(instant) {
    if (instant) mark.classList.add('no-anim');
    mark.classList.add('is-shown');
  }
  if (reduced || !canvas.getContext) { showMark(true); return; }

  var ctx = canvas.getContext('2d');
  var IMG_W = 1920, IMG_H = 1080, POS_Y = 0.6;           // .bt-bg img object-fit: cover; 50% 60%
  // Zagros ridge in painting px (sampled from bg-dry.jpg); birds lift off the slopes just below it
  var RIDGE = [[160, 554], [320, 484], [480, 433], [640, 412], [800, 390], [960, 321],
               [1120, 384], [1280, 424], [1440, 437], [1600, 470], [1760, 527]];
  // palette: the painting's own shadow umbers, cooling into a deep teal as they settle
  var UMBER = [[86, 72, 58], [98, 83, 66], [76, 64, 52], [108, 92, 74]];
  var TEAL = [14, 84, 85];

  var W = 0, H = 0, dpr = 1, birds = [], t0 = 0, raf = 0, done = false, paused = false;
  var FLIGHT_END = 3.55, FADE_START = 3.15, FADE_END = 4.05;

  function rnd(a, b) { return a + Math.random() * (b - a); }
  function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }
  function ridgeY(ix) {
    for (var i = 0; i < RIDGE.length - 1; i++) {
      var a = RIDGE[i], b = RIDGE[i + 1];
      if (ix >= a[0] && ix <= b[0]) return a[1] + (b[1] - a[1]) * (ix - a[0]) / (b[0] - a[0]);
    }
    return RIDGE[ix < RIDGE[0][0] ? 0 : RIDGE.length - 1][1];
  }
  function ease(t) {                                     // soft start, long gentle settle
    return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
  }
  function bez(a, b, c, d, t) {
    var u = 1 - t;
    return u * u * u * a + 3 * u * u * t * b + 3 * u * t * t * c + t * t * t * d;
  }

  function setup() {
    W = stage.clientWidth; H = stage.clientHeight;
    dpr = Math.min(2, window.devicePixelRatio || 1);
    canvas.width = Math.round(W * dpr); canvas.height = Math.round(H * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

    var s = Math.max(W / IMG_W, H / IMG_H);
    var ox = (W - IMG_W * s) / 2, oy = (H - IMG_H * s) * POS_Y;
    var sr = stage.getBoundingClientRect(), mr = mark.getBoundingClientRect();
    var mx = mr.left - sr.left, my = mr.top - sr.top, mw = mr.width, mh = mr.height;
    var span = clamp(mw * 0.085, 7, 13);                 // settled wingspan: neighbours overlap into strokes

    // visible part of the ridge, in painting px
    var ix0 = Math.max(RIDGE[0][0], (-ox) / s + 30), ix1 = Math.min(RIDGE[RIDGE.length - 1][0], (W - ox) / s - 30);
    var starts = [];
    data.pts.forEach(function () {
      // denser near the peak, like a flock lifting off the high slopes
      var u = Math.random(), v = Math.random();
      var ix = ix0 + (ix1 - ix0) * ((u + v) / 2);
      var iy = ridgeY(ix) + rnd(18, 150);
      starts.push([ox + ix * s, oy + iy * s]);
    });
    var targets = data.pts.map(function (p) { return [mx + p[0] * mw, my + p[1] * mh]; });
    // loose spatial pairing (left starts -> left targets) with jitter, so the flock converges without a tangle
    starts.sort(function (a, b) { return a[0] - b[0]; });
    targets = targets.map(function (p) { return { p: p, k: p[0] + rnd(-0.25, 0.25) * mw }; })
      .sort(function (a, b) { return a.k - b.k; }).map(function (o) { return o.p; });

    birds = starts.map(function (st, i) {
      var tg = targets[i];
      var side = Math.random() < 0.5 ? -1 : 1;
      var lift = rnd(0.22, 0.42) * H;
      var delay = Math.pow(Math.random(), 1.4) * 0.85;   // staggered take-off, most leave early
      var dur = rnd(2.25, FLIGHT_END - delay);
      return {
        x0: st[0], y0: st[1],
        x1: st[0] + rnd(-0.12, 0.12) * W, y1: st[1] - lift,
        x2: tg[0] + side * rnd(0.06, 0.2) * Math.min(W, 900), y2: tg[1] - rnd(0.02, 0.14) * H,
        x3: tg[0], y3: tg[1],
        delay: delay, dur: dur,
        wob: rnd(5, 16), wf: rnd(1.2, 2.4), wph: rnd(0, 6.28),
        flap: rnd(10, 14), fph: rnd(0, 6.28),
        size: span * rnd(0.85, 1.2),
        col: UMBER[i % UMBER.length], alpha: rnd(0.78, 0.92),
        px: st[0], py: st[1]
      };
    });
  }

  function drawBird(x, y, S, f, tilt, col, a) {
    var tipY = -f * S * 0.34, elb = -f * S * 0.1 - S * 0.07;
    ctx.save();
    ctx.translate(x, y); ctx.rotate(tilt);
    ctx.fillStyle = 'rgba(' + col[0] + ',' + col[1] + ',' + col[2] + ',' + a.toFixed(3) + ')';
    ctx.beginPath();
    ctx.moveTo(0, S * 0.02);
    ctx.quadraticCurveTo(-S * 0.24, elb - S * 0.1, -S * 0.52, tipY);      // left leading edge
    ctx.quadraticCurveTo(-S * 0.24, elb + S * 0.05, -S * 0.03, S * 0.16);  // left trailing edge
    ctx.quadraticCurveTo(0, S * 0.24, S * 0.03, S * 0.16);                  // body / tail
    ctx.quadraticCurveTo(S * 0.24, elb + S * 0.05, S * 0.52, tipY);
    ctx.quadraticCurveTo(S * 0.24, elb - S * 0.1, 0, S * 0.02);
    ctx.fill();
    ctx.restore();
  }

  function frame(t) {                                    // t: seconds since start
    ctx.clearRect(0, 0, W, H);
    var fade = 1 - clamp((t - (FADE_END - 0.6)) / 0.6, 0, 1);
    if (t >= FADE_START && !mark.classList.contains('is-shown')) showMark(false);
    ctx.shadowColor = 'rgba(60,50,40,.25)';
    ctx.shadowBlur = 1.6 * dpr;
    for (var i = 0; i < birds.length; i++) {
      var b = birds[i];
      var lt = clamp((t - b.delay) / b.dur, 0, 1);
      if (t < b.delay) {
        continue;                                        // still hidden on the slope
      }
      var e = ease(lt);
      var x = bez(b.x0, b.x1, b.x2, b.x3, e), y = bez(b.y0, b.y1, b.y2, b.y3, e);
      // organic wobble, fading out as the bird settles
      var damp = Math.sin(Math.PI * Math.min(1, lt * 1.15));
      x += Math.sin(t * b.wf * 6.28 + b.wph) * b.wob * damp;
      y += Math.cos(t * b.wf * 4.4 + b.wph) * b.wob * 0.5 * damp;
      var vx = x - b.px; b.px = x; b.py = y;
      var grow = 0.85 + 0.15 * e + 1.15 * Math.pow(Math.sin(Math.PI * lt), 1.3);  // nearer (bigger) mid-flight, small on the far slope and once settled
      var glide = 1 - clamp((lt - 0.82) / 0.18, 0, 1);  // wings settle open on arrival
      var f = Math.sin(t * b.flap + b.fph) * (0.25 + 0.75 * glide) + (1 - glide) * 0.15;
      var tilt = clamp(vx * 0.06, -0.45, 0.45) * glide;
      var c = lt < 0.55 ? b.col : (function (k) {
        return [0, 1, 2].map(function (j) { return Math.round(b.col[j] + (TEAL[j] - b.col[j]) * k); });
      })(clamp((lt - 0.55) / 0.45, 0, 1));
      var appear = clamp((t - b.delay) / 0.25, 0, 1);  // emerge from the haze instead of popping in
      drawBird(x, y, b.size * grow, f, tilt, c, b.alpha * appear * fade);
    }
  }

  function loop(now) {
    if (paused) return;
    var t = (now - t0) / 1000;
    frame(t);
    if (t < FADE_END) raf = requestAnimationFrame(loop);
    else finish();
  }
  function finish() {
    if (done) return;
    done = true;
    if (raf) cancelAnimationFrame(raf);
    ctx.clearRect(0, 0, W, H);
    showMark(false);
  }

  function start() {
    setup();
    t0 = performance.now();
    raf = requestAnimationFrame(loop);
  }
  // resizing mid-flight: just land everything
  window.addEventListener('resize', function () { if (!done) finish(); }, { passive: true });

  function ready(fn) {
    var go = function () { setTimeout(fn, 400); };       // let the painting be seen for a beat first
    if (document.readyState === 'complete') go(); else window.addEventListener('load', go);
  }
  ready(function () { if (mark.complete) start(); else mark.addEventListener('load', start); });

  // test hook for frame captures: __birds.at(seconds) renders that moment and freezes
  window.__birds = {
    at: function (t) {
      paused = true; if (raf) cancelAnimationFrame(raf);
      if (!birds.length) setup();
      mark.classList.add('no-anim');
      frame(t);
      mark.style.opacity = (0.8 * clamp((t - FADE_START) / 0.9, 0, 1)).toFixed(3);   // same ramp as the CSS fade
      if (t >= FADE_END) ctx.clearRect(0, 0, W, H);
    }
  };
})();
