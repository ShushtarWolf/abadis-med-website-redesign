/* hero-test/birds v2
   Intro (time, plays once): ~110 painterly birds rise from behind the Zagros ridge into the painted sky
   and settle on points of the Abadis mark, then hand over to the real mark.
   Exit (scroll-scrubbed, reversible): scrolling toward Zagros, the mark dissolves back into birds that
   lift off and dive down behind the mountains; the ridge occluder layer (.bt-ridge, above the canvas)
   hides them. One viewport-sized canvas, vanilla JS, no pointer interaction.
   prefers-reduced-motion: static mark, no birds. */
(function () {
  'use strict';
  var scene = document.getElementById('hero');
  var canvas = document.getElementById('btCanvas');
  var mark = document.getElementById('btMark');
  var MARK = window.ABADIS_MARK, RIDGE = window.ZAGROS_RIDGE;
  if (!scene || !canvas || !mark || !MARK || !RIDGE) return;

  var reduced = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduced || !canvas.getContext) { mark.classList.add('is-static'); canvas.style.display = 'none'; return; }

  var ctx = canvas.getContext('2d');
  var IMG_W = 1920, IMG_H = 1080, POS_Y = 0.6;
  var UMBER = [[86, 72, 58], [98, 83, 66], [76, 64, 52], [108, 92, 74]];   // painting's shadow tones
  var TEAL = [14, 84, 85];
  var MARK_OP = 0.8;
  var INTRO_DELAY = 0.35, FLIGHT_END = 3.55, FADE_START = 3.15, FADE_END = 4.05;

  // geometry (scene px)
  var W = 0, VH = 0, H = 0, skyH = 0, sceneTop = 0, sceneH = 0, dpr = 1, span = 10;
  var birds = [];
  // time / scroll state
  var t0 = 0, frozenT = -1, pTarget = 0, pCur = 0, raf = 0, lastNow = 0;

  function mulberry(a) { return function () { a |= 0; a = a + 0x6D2B79F5 | 0; var t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
  function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }
  function lerp(a, b, k) { return a + (b - a) * k; }
  function ease(t) { return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; }
  function bez(a, b, c, d, t) { var u = 1 - t; return u * u * u * a + 3 * u * u * t * b + 3 * u * t * t * c + t * t * t * d; }
  function ridgeAt(ix) {
    var i = clamp(Math.floor(ix / 32), 0, RIDGE.length - 2), a = RIDGE[i], b = RIDGE[i + 1];
    return a[1] + (b[1] - a[1]) * clamp((ix - a[0]) / (b[0] - a[0]), 0, 1);
  }

  function setup() {
    W = scene.clientWidth;
    VH = canvas.parentNode.clientHeight;
    var stage = scene.querySelector('.bt-stage');
    H = stage.clientHeight; skyH = stage.offsetTop; sceneH = scene.offsetHeight;
    sceneTop = scene.getBoundingClientRect().top + (window.pageYOffset || document.documentElement.scrollTop);
    dpr = Math.min(2, window.devicePixelRatio || 1);
    canvas.width = Math.round(W * dpr); canvas.height = Math.round(VH * dpr);

    // backdrop cover mapping -> scene coords
    var s = Math.max(W / IMG_W, H / IMG_H), ox = (W - IMG_W * s) / 2, oy = skyH + (H - IMG_H * s) * POS_Y;
    function toScene(ix, iy) { return [ox + ix * s, oy + iy * s]; }
    var mw = mark.offsetWidth, mh = mark.offsetHeight;
    var mx = mark.offsetLeft - mw / 2, my = mark.offsetTop - mh / 2;     // translate(-50%,-50%)
    span = clamp(mw * 0.075, 8, 14);

    var ix0 = Math.max(60, (-ox) / s + 40), ix1 = Math.min(IMG_W - 60, (W - ox) / s - 40);
    var rnd = mulberry(20261011);
    var n = MARK.pts.length, starts = [], ends = [];
    for (var i = 0; i < n; i++) {
      var u = (rnd() + rnd()) / 2, ix = lerp(ix0, ix1, u);
      starts.push(toScene(ix, ridgeAt(ix) + 30 + rnd() * 90));          // just behind the ridge
      var ex = lerp(ix0, ix1, (rnd() + rnd() + rnd()) / 3);
      ends.push(toScene(ex, ridgeAt(ex) + 40 + rnd() * 120));           // dive back behind it
    }
    var targets = MARK.pts.map(function (p) { return [mx + p[0] * mw, my + p[1] * mh]; });
    // loose left-to-right pairing so the flock converges without a tangle
    var order = targets.map(function (p, i) { return { i: i, k: p[0] + (rnd() - 0.5) * 0.5 * mw }; }).sort(function (a, b) { return a.k - b.k; });
    starts.sort(function (a, b) { return a[0] - b[0]; });
    ends.sort(function (a, b) { return a[0] - b[0]; });

    birds = order.map(function (o, j) {
      var tg = targets[o.i], st = starts[j], en = ends[j];
      var side = rnd() < 0.5 ? -1 : 1;
      var delay = Math.pow(rnd(), 1.4) * 0.85;
      return {
        // intro: behind ridge -> mark
        ix0: st[0], iy0: st[1],
        ix1: st[0] + (rnd() - 0.5) * 0.24 * W, iy1: st[1] - (0.3 + rnd() * 0.25) * H,
        ix2: tg[0] + side * (0.06 + rnd() * 0.14) * Math.min(W, 900), iy2: tg[1] - (0.02 + rnd() * 0.12) * H,
        tx: tg[0], ty: tg[1],
        delay: delay, dur: 2.25 + rnd() * (FLIGHT_END - delay - 2.25),
        // exit: mark -> behind ridge (scroll-scrubbed)
        ed: rnd() * 0.38, edur: 0.5 + rnd() * 0.12,
        ex1: (rnd() - 0.5) * 0.16 * W, ey1: -(0.03 + rnd() * 0.1) * H,
        ex2: en[0] + (rnd() - 0.5) * 0.2 * W, ey2: en[1] - (0.28 + rnd() * 0.2) * H,
        ex: en[0], ey: en[1],
        wob: 5 + rnd() * 11, wf: 1.2 + rnd() * 1.2, wph: rnd() * 6.28,
        flap: 10 + rnd() * 4, fph: rnd() * 6.28,
        size: span * (0.85 + rnd() * 0.35),
        col: UMBER[j % UMBER.length], alpha: 0.78 + rnd() * 0.14,
        lx: st[0]
      };
    });
  }

  function readScroll() {
    var y = (window.pageYOffset || document.documentElement.scrollTop) - sceneTop;
    pTarget = clamp(y / (skyH * 0.95), 0, 1);
  }

  function drawBird(x, y, S, f, tilt, col, a) {
    var tipY = -f * S * 0.34, elb = -f * S * 0.1 - S * 0.07;
    ctx.save();
    ctx.translate(x, y); ctx.rotate(tilt);
    ctx.fillStyle = 'rgba(' + col[0] + ',' + col[1] + ',' + col[2] + ',' + a.toFixed(3) + ')';
    ctx.beginPath();
    ctx.moveTo(0, S * 0.02);
    ctx.quadraticCurveTo(-S * 0.24, elb - S * 0.1, -S * 0.52, tipY);
    ctx.quadraticCurveTo(-S * 0.24, elb + S * 0.05, -S * 0.03, S * 0.16);
    ctx.quadraticCurveTo(0, S * 0.24, S * 0.03, S * 0.16);
    ctx.quadraticCurveTo(S * 0.24, elb + S * 0.05, S * 0.52, tipY);
    ctx.quadraticCurveTo(S * 0.24, elb - S * 0.1, 0, S * 0.02);
    ctx.fill();
    ctx.restore();
  }
  function mix(c1, c2, k) { return [lerp(c1[0], c2[0], k) | 0, lerp(c1[1], c2[1], k) | 0, lerp(c1[2], c2[2], k) | 0]; }

  function render(t, p) {
    var scrollY = window.pageYOffset || document.documentElement.scrollTop;
    var camY = clamp(scrollY - sceneTop, 0, Math.max(0, sceneH - VH));     // sticky canvas top, scene px
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, W, VH);
    ctx.shadowColor = 'rgba(60,50,40,.25)';
    ctx.shadowBlur = 1.6 * dpr;

    var it = t - INTRO_DELAY;
    var introMark = MARK_OP * clamp((it - FADE_START) / 0.9, 0, 1);
    var introBirds = 1 - clamp((it - (FADE_END - 0.6)) / 0.6, 0, 1);
    var k = clamp(p / 0.05, 0, 1);                       // first bit of scroll: mark dissolves into birds
    mark.style.opacity = (introMark * (1 - k)).toFixed(3);
    var birdVis = Math.max(introBirds, k);
    if (birdVis <= 0.001 || it < 0) return;

    for (var i = 0; i < birds.length; i++) {
      var b = birds[i];
      var lt = clamp((it - b.delay) / b.dur, 0, 1);
      if (it < b.delay) continue;
      var e = ease(lt);
      var x = bez(b.ix0, b.ix1, b.ix2, b.tx, e), y = bez(b.iy0, b.iy1, b.iy2, b.ty, e);
      var damp = Math.sin(Math.PI * Math.min(1, lt * 1.15));
      x += Math.sin(t * b.wf * 6.28 + b.wph) * b.wob * damp;
      y += Math.cos(t * b.wf * 4.4 + b.wph) * b.wob * 0.5 * damp;

      // scroll exit from wherever the intro has the bird
      var lp = clamp((p - b.ed) / b.edur, 0, 1), ee = ease(lp);
      if (lp > 0) {
        var x0 = x, y0 = y;
        x = bez(x0, x0 + b.ex1, b.ex2, b.ex, ee);
        y = bez(y0, y0 + b.ey1, b.ey2, b.ey, ee);
        var dw = Math.sin(Math.PI * lp);
        x += Math.sin(t * b.wf * 6.28 + b.wph) * b.wob * 0.6 * dw;
      }
      var air = Math.max(Math.pow(Math.sin(Math.PI * lt), 1.3), Math.sin(Math.PI * Math.min(1, lp * 1.4)));
      var grow = (0.85 + 0.15 * e) * (1 - 0.25 * ee) + 1.1 * air;          // nearer = bigger mid-flight
      var settled = lt >= 1 && lp <= 0;
      var glide = settled ? 0 : 1 - clamp((lt - 0.82) / 0.18, 0, 1) * (lp > 0 ? 0 : 1);
      var f = Math.sin(t * b.flap + b.fph) * (0.25 + 0.75 * glide) + (1 - glide) * 0.15;
      var vx = x - b.lx; b.lx = x;
      var tilt = clamp(vx * 0.06, -0.45, 0.45) * glide;
      var col = lp > 0 ? mix(TEAL, b.col, clamp(lp / 0.45, 0, 1))
                       : (lt < 0.55 ? b.col : mix(b.col, TEAL, clamp((lt - 0.55) / 0.45, 0, 1)));
      var appear = clamp((it - b.delay) / 0.25, 0, 1);
      var a = b.alpha * appear * birdVis;
      var sy = y - camY;
      if (sy < -40 || sy > VH + 40) continue;
      drawBird(x, sy, b.size * grow, f, tilt, col, a);
    }
  }

  function now() { return frozenT >= 0 ? frozenT : (performance.now() - t0) / 1000; }
  function tick(ms) {
    raf = 0;
    var dt = lastNow ? Math.min(64, ms - lastNow) : 16.7; lastNow = ms;
    if (frozenT >= 0) pCur = pTarget;
    else { pCur += (pTarget - pCur) * (1 - Math.pow(1 - 0.16, dt / 16.7)); if (Math.abs(pTarget - pCur) < 0.0005) pCur = pTarget; }
    var t = now();
    render(t, pCur);
    var introRunning = t - INTRO_DELAY < FADE_END;
    var airborne = pCur > 0.001 && pCur < 0.999;          // keep wings beating while birds hang in the air
    if (frozenT < 0 && (introRunning || pCur !== pTarget || airborne)) kick();
    else lastNow = 0;
  }
  function kick() { if (!raf) raf = requestAnimationFrame(tick); }

  function begin() {
    setup(); readScroll(); pCur = pTarget;
    t0 = performance.now();
    kick();
  }
  window.addEventListener('scroll', function () { readScroll(); kick(); }, { passive: true });
  var rz = 0;
  window.addEventListener('resize', function () {
    if (rz) return;
    rz = requestAnimationFrame(function () { rz = 0; setup(); readScroll(); kick(); });
  }, { passive: true });

  var go = function () { if (mark.complete) begin(); else mark.addEventListener('load', begin); };
  if (document.readyState === 'complete') go(); else window.addEventListener('load', go);

  // test hook for frame captures: freeze the intro clock at t seconds (scroll still drives the exit)
  window.__birds = {
    at: function (t) { frozenT = t; if (!birds.length) setup(); readScroll(); pCur = pTarget; render(t, pCur); },
    refresh: function () { readScroll(); pCur = pTarget; render(now(), pCur); }
  };
})();
