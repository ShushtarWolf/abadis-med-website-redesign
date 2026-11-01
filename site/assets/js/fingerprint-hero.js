/* Home fingerprint hero — living ridge lines (scoped to .fp-hero). */
(function () {
  'use strict';
  var root = document.querySelector('.fp-hero');
  if (!root) return;

  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var cv = root.querySelector('.fp-canvas');
  var ecv = root.querySelector('.fp-ecg');
  if (!cv || !ecv) return;
  var ctx = cv.getContext('2d');
  var ectx = ecv.getContext('2d');
  var stage = root.querySelector('.fp-stage');
  var capEl = root.querySelector('.fp-cap');
  var hintEl = root.querySelector('.fp-hint');
  var chips = Array.prototype.slice.call(root.querySelectorAll('.fp-chip'));
  var ltr = document.documentElement.getAttribute('dir') === 'ltr';
  var digits = root.getAttribute('data-digits') || 'fa';
  var countTpl = root.getAttribute('data-count-tpl') || '{n}';
  var CAPS = (root.getAttribute('data-caps') || '').split('|');
  if (CAPS.length < 3) {
    CAPS = [
      'خطوط اثر انگشت، هویت یک انسان',
      'همین خطوط، در خطوط تراز کوه و حلقه‌های تنهٔ درخت',
      'ردِ یک اثر، در هر نقطه از جهان'
    ];
  }

  var TAU = Math.PI * 2, N = 54, BEAT = 1.7;
  var W = 0, H = 0, dpr = 1, cx = 0, cy = 0, fpR = 200, coverR = 800, sp = 6, spanR = 300, desktop = true;
  var originX = 0, originY = 0;

  function hash(i, j) {
    var h = Math.imul(i, 374761393) ^ Math.imul(j, 668265263);
    h = Math.imul(h ^ (h >>> 13), 1274126177);
    h ^= h >>> 16;
    return (h >>> 0) / 4294967296;
  }
  function vn(x, y) {
    var xi = Math.floor(x), yi = Math.floor(y), xf = x - xi, yf = y - yi;
    var u = xf * xf * (3 - 2 * xf), v = yf * yf * (3 - 2 * yf);
    var a = hash(xi, yi), b = hash(xi + 1, yi), c = hash(xi, yi + 1), d = hash(xi + 1, yi + 1);
    return a + (b - a) * u + (c - a) * v + (a - b - c + d) * u * v;
  }
  function fbm(x, y) { return vn(x, y) * 0.65 + vn(x * 2.1 + 5.2, y * 2.1 + 1.3) * 0.35; }

  var MODES = [
    { topo: 0, A: 0.75, f: 1.7,  ax: 0.84, thr: 0.66 },
    { topo: 1, A: 4.6,  f: 0.95, ax: 1.0,  thr: 2 },
    { topo: 1, A: 8.5,  f: 0.42, ax: 1.22, thr: 2 }
  ];
  var P = { topo: 0, A: 0.75, f: 1.7, ax: 0.84, thr: 0.66 };
  var mode = 0, modeT = 0, autoplay = !reduce;

  function setMode(m, fromUser) {
    mode = m;
    if (fromUser) modeT = 0;
    chips.forEach(function (c, i) { c.setAttribute('aria-pressed', i === m ? 'true' : 'false'); });
    if (capEl) capEl.textContent = CAPS[m] || '';
  }
  chips.forEach(function (c) {
    c.addEventListener('click', function () { setMode(+c.dataset.mode, true); });
  });

  function resize() {
    var rect = root.getBoundingClientRect();
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    W = Math.max(1, Math.round(rect.width));
    H = Math.max(1, Math.round(rect.height));
    originX = rect.left;
    originY = rect.top;
    cv.width = Math.round(W * dpr);
    cv.height = Math.round(H * dpr);
    cv.style.width = W + 'px';
    cv.style.height = H + 'px';
    ecv.width = Math.round(132 * dpr);
    ecv.height = Math.round(34 * dpr);
    desktop = W >= 860;
    cx = desktop ? (ltr ? W * 0.69 : W * 0.31) : W * 0.5;
    cy = desktop ? H * 0.5 : H * 0.31;
    fpR = desktop ? Math.min(H * 0.4, W * 0.25) : Math.min(W * 0.4, H * 0.21);
    coverR = Math.hypot(Math.max(cx, W - cx), Math.max(cy, H - cy)) * 1.04;
    if (stage) {
      stage.style.background = 'radial-gradient(circle at ' + cx + 'px ' + cy + 'px, rgba(34,150,140,.20), rgba(4,16,15,0) ' + Math.round(coverR * 0.7) + 'px)';
    }
  }
  window.addEventListener('resize', resize);
  window.addEventListener('scroll', function () {
    var rect = root.getBoundingClientRect();
    originX = rect.left;
    originY = rect.top;
  }, { passive: true });
  resize();

  var ptr = { x: -999, y: -999, tx: -999, ty: -999, a: 0, str: 0, press: 0, seen: false };
  var ripples = [], imprints = [], count = 0;

  function fmt(n) {
    var loc = digits === 'fa' ? 'fa-IR' : (digits === 'ar' ? 'ar-EG' : 'en-US');
    try { return n.toLocaleString(loc); } catch (e) { return String(n); }
  }
  function localXY(e) {
    return { x: e.clientX - originX, y: e.clientY - originY };
  }
  function overHero(e) {
    var r = root.getBoundingClientRect();
    return e.clientX >= r.left && e.clientX <= r.right && e.clientY >= r.top && e.clientY <= r.bottom;
  }

  window.addEventListener('pointermove', function (e) {
    if (!overHero(e)) { ptr.a = 0; return; }
    var p = localXY(e);
    ptr.tx = p.x; ptr.ty = p.y;
    if (!ptr.seen) { ptr.x = ptr.tx; ptr.y = ptr.ty; ptr.seen = true; }
    ptr.a = 1;
  }, { passive: true });

  root.addEventListener('pointerdown', function (e) {
    if (e.target.closest('a, button')) return;
    var p = localXY(e);
    ptr.tx = ptr.x = p.x; ptr.ty = ptr.y = p.y; ptr.seen = true;
    ptr.a = 1; ptr.press = 1;
    if (!reduce) {
      ripples.push({ x: p.x, y: p.y, t0: clock });
      if (ripples.length > 3) ripples.shift();
    }
    imprints.push({ x: p.x, y: p.y, t0: clock, seed: Math.random() * 100, rot: (Math.random() - 0.5) * 1.2 });
    if (imprints.length > 6) imprints.shift();
    count++;
    if (hintEl) hintEl.textContent = countTpl.replace('{n}', fmt(count));
  }, { passive: true });

  function release(e) {
    if (!e || e.pointerType === 'touch' || e.type === 'pointerleave') ptr.a = 0;
  }
  window.addEventListener('pointerup', release, { passive: true });
  window.addEventListener('pointercancel', release, { passive: true });
  root.addEventListener('pointerleave', function () { ptr.a = 0; });

  var o = { x: 0, y: 0 };
  function pt(k, th, pkk, out) {
    var c = Math.cos(th), s = Math.sin(th), u = k / N, rb = k * sp;
    var n = fbm(c * P.f + k * 0.11 + 7.3, s * P.f + T * 0.045 + 2.1);
    var d = (n - 0.5) * 2 * P.A * sp * Math.min(1, k / 8);
    var r = rb + d + pkk;
    var core = (1 - P.topo) * (1 - u) * (1 - u);
    out.x = cx + c * r * P.ax + Math.sin(k * 0.21) * core * sp * 5;
    out.y = cy + s * r - core * sp * N * 0.1;
    return out;
  }
  function gapNoise(k, th) {
    return vn(Math.cos(th) * 3.1 + k * 0.37 + 11, Math.sin(th) * 3.1 + k * 0.23 + 7.9);
  }

  function gs(x, m, s) { var d = (x - m) / s; return Math.exp(-d * d); }
  function ecg(ph) {
    return 0.14 * gs(ph, 0.14, 0.03) - 0.14 * gs(ph, 0.275, 0.010) + gs(ph, 0.30, 0.011) - 0.3 * gs(ph, 0.323, 0.011) + 0.26 * gs(ph, 0.52, 0.05);
  }
  function drawEcg() {
    var w = 132, h = 34, speed = 46, y0 = h * 0.72, amp = h * 0.62;
    ectx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ectx.clearRect(0, 0, w, h);
    var gr = ectx.createLinearGradient(0, 0, w, 0);
    gr.addColorStop(0, 'rgba(111,240,214,0)');
    gr.addColorStop(1, 'rgba(111,240,214,1)');
    ectx.strokeStyle = gr;
    ectx.lineWidth = 1.4;
    ectx.lineJoin = 'round';
    ectx.beginPath();
    var ly = y0;
    for (var x = 0; x <= w; x++) {
      var tt = T - (w - x) / speed;
      var y = y0;
      if (tt > 0.7) {
        var ph = ((((tt - 1.0) / BEAT) + 0.30) % 1 + 1) % 1;
        y = y0 - ecg(ph) * amp;
      }
      if (x === 0) ectx.moveTo(x, y); else ectx.lineTo(x, y);
      ly = y;
    }
    ectx.stroke();
    ectx.fillStyle = '#ff6a57';
    ectx.beginPath();
    ectx.arc(w - 1, ly, 2.3, 0, TAU);
    ectx.fill();
  }

  var parts = [];
  for (var i = 0; i < 64; i++) {
    parts.push({
      k: 4 + Math.floor(Math.random() * (N - 5)),
      th: Math.random() * TAU,
      v: (0.04 + Math.random() * 0.14) * (Math.random() < 0.5 ? -1 : 1),
      s: 1.1 + Math.random() * 1.2
    });
  }

  var T = reduce ? 6 : 0, clock = 0, last = performance.now();
  var pkArr = new Array(N + 2), paArr = new Array(N + 2);
  var timeScale = reduce ? 0 : 1;
  var running = true;

  function ease3(x) { x = Math.max(0, Math.min(1, x)); return 1 - Math.pow(1 - x, 3); }
  function clamp01(x) { return x < 0 ? 0 : x > 1 ? 1 : x; }

  function frame(now) {
    if (!running) return;
    var dt = Math.min(0.05, (now - last) / 1000 || 0.016);
    last = now;
    clock += dt;
    T += dt * timeScale;

    if (autoplay && T > 5.5) {
      modeT += dt;
      if (modeT > 6.8) setMode((mode + 1) % 3, true);
    }

    var tg = MODES[mode], kk = 1 - Math.exp(-dt * (reduce ? 6 : 2.2));
    P.topo += (tg.topo - P.topo) * kk;
    P.A += (tg.A - P.A) * kk;
    P.f += (tg.f - P.f) * kk;
    P.ax += (tg.ax - P.ax) * kk;
    P.thr += (tg.thr - P.thr) * kk;

    spanR = fpR + (coverR - fpR) * P.topo;
    sp = spanR / N;

    ptr.x += (ptr.tx - ptr.x) * (1 - Math.exp(-dt * 14));
    ptr.y += (ptr.ty - ptr.y) * (1 - Math.exp(-dt * 14));
    ptr.str += (ptr.a - ptr.str) * (1 - Math.exp(-dt * 6));
    ptr.press *= Math.exp(-dt * 3);
    var Rm = Math.min(W, H) * 0.16 * (1 + ptr.press * 0.5);
    var Rm2 = Rm * Rm;
    var ms = ptr.str * (1 + ptr.press * 1.2);
    ripples = ripples.filter(function (r) { return clock - r.t0 < 3.6; });
    imprints = imprints.filter(function (r) { return clock - r.t0 < 3.4; });

    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, W, H);

    var vel = spanR / 1.6, w = sp * 3.2, pamp = sp * 1.3 * (1 + (1 - P.topo) * 0.5), beatAge = 99, k;
    for (k = 0; k <= N; k++) { pkArr[k] = 0; paArr[k] = 0; }
    if (T >= 1.0) {
      var bi = Math.floor((T - 1.0) / BEAT);
      for (var j = bi; j >= bi - 1; j--) {
        if (j < 0) continue;
        var age = T - (1.0 + j * BEAT);
        if (j === bi) beatAge = age;
        var front = age * vel, decay = Math.exp(-age * 0.9);
        for (k = 1; k <= N; k++) {
          var e = (k * sp - front) / w, gg = Math.exp(-e * e) * decay;
          pkArr[k] += pamp * gg;
          paArr[k] += gg;
        }
      }
    }

    if (T < 1.9) {
      var la = 1 - clamp01((T - 1.0) / 0.8);
      var hx;
      if (ltr) {
        hx = cx - cx * (1 - ease3(Math.min(1, T / 1.0)));
        if (T >= 1.0) hx = cx;
        ctx.strokeStyle = 'rgba(111,240,214,' + (0.75 * la) + ')';
        ctx.lineWidth = 1.4;
        ctx.beginPath();
        ctx.moveTo(0, cy);
        for (var xL = 0; xL <= hx; xL += 3) {
          var phL = 0.30 - (hx - xL) / 260, yyL = 0;
          if (phL >= 0) yyL = ecg(phL) * 96;
          ctx.lineTo(xL, cy - yyL);
        }
        ctx.stroke();
      } else {
        hx = cx + (W - cx) * (1 - ease3(Math.min(1, T / 1.0)));
        if (T >= 1.0) hx = cx;
        ctx.strokeStyle = 'rgba(111,240,214,' + (0.75 * la) + ')';
        ctx.lineWidth = 1.4;
        ctx.beginPath();
        ctx.moveTo(W, cy);
        for (var x = W; x >= hx; x -= 3) {
          var ph = 0.30 - (x - hx) / 260, yy = 0;
          if (ph >= 0) yy = ecg(ph) * 96;
          ctx.lineTo(x, cy - yy);
        }
        ctx.stroke();
      }
    }

    var introCount = N * ease3((T - 0.9) / 3.4);
    ctx.lineJoin = 'round';
    ctx.lineCap = 'round';
    for (k = 1; k <= N; k++) {
      var vis = clamp01(introCount - (k - 1));
      if (vis <= 0) break;
      var u = k / N, rb = k * sp, M = Math.min(320, Math.max(40, (TAU * rb * P.ax / 7) | 0));
      var isIdx = (k % 5 === 0);
      var edge = 1 - (1 - P.topo) * clamp01((u - 0.8) / 0.2) * clamp01((u - 0.8) / 0.2);
      var a = (1 - P.topo) * (0.92 - 0.5 * u) + P.topo * (isIdx ? 0.62 : 0.26);
      a = (a + paArr[k] * 0.45) * vis * edge;
      var h = 170 - 14 * P.topo + 18 * u;
      var l = isIdx && P.topo > 0.5 ? 74 : 62 + 12 * (1 - u) * (1 - P.topo);
      ctx.strokeStyle = 'hsla(' + h.toFixed(0) + ',72%,' + l.toFixed(0) + '%,' + Math.min(1, a).toFixed(3) + ')';
      ctx.lineWidth = isIdx && P.topo > 0.5 ? 1.7 : 1.1;
      ctx.beginPath();
      var pen = false, useGap = P.thr < 1.5;
      for (var m = 0; m <= M; m++) {
        var th = m / M * TAU;
        if (useGap && gapNoise(k, th) > P.thr) { pen = false; continue; }
        pt(k, th, pkArr[k], o);
        if (ms > 0.01) {
          var dx = o.x - ptr.x, dy = o.y - ptr.y, d2 = dx * dx + dy * dy;
          if (d2 < Rm2 * 4) {
            var dd = Math.sqrt(d2) + 0.001;
            var f = Math.exp(-d2 / (Rm2 * 0.5));
            var push = ms * f * Rm * 0.34;
            o.x += dx / dd * push;
            o.y += dy / dd * push;
          }
        }
        for (var q = 0; q < ripples.length; q++) {
          var rp = ripples[q], ra = clock - rp.t0;
          var rx = o.x - rp.x, ry = o.y - rp.y;
          var rd = Math.sqrt(rx * rx + ry * ry) + 0.001;
          var ee = rd - ra * 460;
          if (ee > -140 && ee < 140) {
            var wv = Math.exp(-(ee * ee) / (2 * 34 * 34)) * Math.sin(ee * 0.12) * 14 * Math.exp(-ra * 0.9);
            o.x += rx / rd * wv;
            o.y += ry / rd * wv;
          }
        }
        if (pen) ctx.lineTo(o.x, o.y); else { ctx.moveTo(o.x, o.y); pen = true; }
      }
      ctx.stroke();
    }

    ctx.globalCompositeOperation = 'lighter';
    var visK = Math.floor(introCount);
    for (var pi = 0; pi < parts.length; pi++) {
      var pr = parts[pi];
      if (pr.k > visK) continue;
      pr.th += pr.v * dt * timeScale * (0.6 + P.topo * 0.8);
      pt(pr.k, pr.th, pkArr[pr.k], o);
      var halo = 5 + pr.s * 3;
      var grd = ctx.createRadialGradient(o.x, o.y, 0, o.x, o.y, halo);
      grd.addColorStop(0, 'rgba(184,247,198,.55)');
      grd.addColorStop(1, 'rgba(184,247,198,0)');
      ctx.fillStyle = grd;
      ctx.beginPath();
      ctx.arc(o.x, o.y, halo, 0, TAU);
      ctx.fill();
      ctx.fillStyle = 'rgba(232,246,243,.95)';
      ctx.beginPath();
      ctx.arc(o.x, o.y, pr.s * 0.8, 0, TAU);
      ctx.fill();
    }

    if (ptr.str > 0.02) {
      var pg = ctx.createRadialGradient(ptr.x, ptr.y, 0, ptr.x, ptr.y, Rm * 1.1);
      pg.addColorStop(0, 'rgba(111,240,214,' + (0.16 * ptr.str) + ')');
      pg.addColorStop(1, 'rgba(111,240,214,0)');
      ctx.fillStyle = pg;
      ctx.beginPath();
      ctx.arc(ptr.x, ptr.y, Rm * 1.1, 0, TAU);
      ctx.fill();
    }
    ctx.globalCompositeOperation = 'source-over';

    for (var ii = 0; ii < imprints.length; ii++) {
      var im = imprints[ii], ia = clock - im.t0;
      var life = Math.pow(1 - ia / 3.4, 1.5), sc = 1 + ia * 0.06;
      ctx.strokeStyle = 'rgba(184,247,198,' + (0.85 * life).toFixed(3) + ')';
      ctx.lineWidth = 1.1;
      for (var rr = 1; rr <= 9; rr++) {
        ctx.beginPath();
        for (var s2 = 0; s2 <= 40; s2++) {
          var t2 = s2 / 40 * TAU;
          var nn = (vn(Math.cos(t2) * 1.4 + rr * 0.3 + im.seed, Math.sin(t2) * 1.4 + im.seed) - 0.5) * 3.2;
          var rad = (rr * 3.6 + nn) * sc;
          var ex = Math.cos(t2) * rad * 0.82, ey = Math.sin(t2) * rad;
          var rx2 = ex * Math.cos(im.rot) - ey * Math.sin(im.rot);
          var ry2 = ex * Math.sin(im.rot) + ey * Math.cos(im.rot);
          if (s2 === 0) ctx.moveTo(im.x + rx2, im.y + ry2);
          else ctx.lineTo(im.x + rx2, im.y + ry2);
        }
        ctx.stroke();
      }
    }

    if (T >= 1.0) {
      var bp = Math.exp(-beatAge * 5), rad0 = 2.6 + 7 * bp;
      var cg = ctx.createRadialGradient(cx, cy, 0, cx, cy, rad0 * 3.2);
      cg.addColorStop(0, 'rgba(255,106,87,' + (0.5 + 0.4 * bp) + ')');
      cg.addColorStop(1, 'rgba(255,106,87,0)');
      ctx.fillStyle = cg;
      ctx.beginPath();
      ctx.arc(cx, cy, rad0 * 3.2, 0, TAU);
      ctx.fill();
      ctx.fillStyle = '#ff6a57';
      ctx.beginPath();
      ctx.arc(cx, cy, 2.6 + 2 * bp, 0, TAU);
      ctx.fill();
    }

    drawEcg();
    requestAnimationFrame(frame);
  }

  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        running = en.isIntersecting;
        if (running) {
          last = performance.now();
          requestAnimationFrame(frame);
        }
      });
    }, { threshold: 0.05 });
    io.observe(root);
  }
  requestAnimationFrame(frame);
})();
