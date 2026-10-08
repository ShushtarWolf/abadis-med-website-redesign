/* Sample 2 — «نام‌ها در آسمان»
   Two or three rows of names drift right → left like slow ribbons. The scroll position drives each row's offset
   (scroll back reverses it), each row at its own speed, with a gentle wave. Rows live in the free band between the
   hero copy and the grown treeline / canister, so they never cover the text, the oaks or the jar.
   Only the names currently on screen exist in the DOM (small per-row pool); positions come from canvas metrics. */
(function () {
  'use strict';
  var ZH = window.__zagrosHero, ZN = window.ZN;
  if (!ZH || !ZN) return;
  var clamp = ZN.clamp, seg = ZN.seg, smooth = ZN.smooth;
  var stage = ZH.stage, sky = document.getElementById('srSky');
  var copyEl = stage.querySelector('.csr-hero > div');
  var cnt = ZN.counter(document.getElementById('znCounter'));
  var ctx = document.createElement('canvas').getContext('2d');

  // front → back: size (phone, desktop), weight, opacity, speed (px of drift per px of scroll), wave phase
  var ROWS = [
    { fs: [14, 17.5], wt: 700, op: 0.92, speed: 1.15, ph: 0.0 },
    { fs: [12.5, 15.5], wt: 600, op: 0.74, speed: 1.6, ph: 2.1 },
    { fs: [12, 14.5], wt: 500, op: 0.6, speed: 0.8, ph: 4.2 }
  ];
  var NAMES = [], N = 0, rows = [], W = 0, H = 0, built = '';

  function buildRows(nRows) {
    sky.textContent = '';
    var desk = W >= 900;
    rows = [];
    for (var r = 0; r < nRows; r++) {
      var R = ROWS[r], fs = R.fs[desk ? 1 : 0], gap = Math.round(fs * 2.4);
      var el = document.createElement('div');
      el.className = 'sr-row';
      el.style.height = Math.ceil(fs * 1.6 + 12) + 'px';
      el.style.opacity = R.op;
      el.style.setProperty('--gap', gap + 'px');
      sky.appendChild(el);
      // names are dealt round-robin to the rows, in the list's own order
      var list = [];
      for (var i = r; i < N; i += nRows) list.push(i);
      ctx.font = R.wt + ' ' + fs + 'px Kalameh, Tahoma, sans-serif';
      var X = new Float64Array(list.length + 1), w = new Float32Array(list.length);
      for (var j = 0, x = 0; j < list.length; j++) { X[j] = x; w[j] = Math.ceil(ctx.measureText(NAMES[list[j]]).width) + 2; x += w[j] + gap; }
      X[list.length] = x;
      rows.push({ R: R, el: el, fs: fs, list: list, X: X, w: w, live: new Map(), free: [], y: 0, h: fs * 1.6 + 12 });
    }
  }

  function onLayout() {
    W = ZH.W; H = ZH.H;
    if (!N) return;
    var s = stage.getBoundingClientRect(), cr = copyEl.getBoundingClientRect();
    var top = cr.bottom - s.top + (W >= 900 ? 14 : 10);
    // grown treeline: tops of the oaks that sit in the unmasked middle of the screen, plus the risen canister
    var bottom = ZH.canister.offsetTop - 8;
    ZH.spots.forEach(function (sp) {
      var half = sp.H * 0.55;
      if (sp.gx + half < W * 0.1 || sp.gx - half > W * 0.9) return;
      bottom = Math.min(bottom, sp.gy - sp.H * 1.0 - 6);
    });
    var desk = W >= 900, band = bottom - top, n = 0, need = 0;
    for (var r = 0; r < 3; r++) { var hh = ROWS[r].fs[desk ? 1 : 0] * 1.6 + 4; if (need + hh <= band) { need += hh; n++; } }
    var key = n + '|' + desk + '|' + W;
    if (key !== built) { buildRows(n); built = key; }
    if (!n) return;
    // spread rows evenly through the band (front row lowest = closest to the trees)
    var slack = (band - need) / (n + 1), y = top + slack;
    var order = rows.slice().reverse();
    order.forEach(function (row) {
      var hh = row.fs * 1.6 + 4;
      row.y = y - 6; y += hh + slack;
      row.el.style.transform = 'translate3d(0,' + row.y.toFixed(1) + 'px,0)';
    });
    sky.dataset.band = Math.round(top) + '-' + Math.round(bottom) + ':' + n;
  }

  function firstVisible(row, o) {            // first j with X[j] + w[j] >= o
    var lo = 0, hi = row.list.length - 1;
    while (lo < hi) { var mid = (lo + hi) >> 1; if (row.X[mid] + row.w[mid] < o) lo = mid + 1; else hi = mid; }
    return lo;
  }
  function onRender(p) {
    if (!rows.length) { cnt.set(N && p >= 0.8 ? N : Math.round(N * seg(p, 0.06, 0.8))); return; }
    var track = ZH.track;
    rows.forEach(function (row) {
      var o = p * track * row.R.speed;                             // scroll → offset (reversible)
      var j0 = firstVisible(row, o - 40), seen = {};
      for (var j = j0; j < row.list.length && row.X[j] - o < W + 40; j++) {
        seen[j] = 1;
        var sp = row.live.get(j);
        if (!sp) {
          sp = row.free.pop();
          if (!sp) { sp = document.createElement('span'); sp.className = 'sr-name'; sp.style.fontSize = row.fs + 'px'; sp.style.fontWeight = row.R.wt; row.el.appendChild(sp); }
          sp.textContent = NAMES[row.list[j]];
          sp.style.visibility = '';
          row.live.set(j, sp);
        }
        // screen x of the name's left edge: the ribbon moves right → left as you scroll down, new names enter on the right
        var x = row.X[j] - o;
        var wave = Math.sin((x / W) * 3.2 + row.R.ph + p * 2.4) * (row.fs * 0.28);
        sp.style.transform = 'translate3d(' + x.toFixed(1) + 'px,' + (6 + wave).toFixed(1) + 'px,0)';
      }
      row.live.forEach(function (sp, j) { if (!seen[j]) { sp.style.visibility = 'hidden'; row.live.delete(j); row.free.push(sp); } });
    });
    cnt.set(p >= 0.8 ? N : Math.round(N * smooth(seg(p, 0.06, 0.8))));
  }

  ZH.onLayout(onLayout);
  ZH.onRender(onRender);
  Promise.all([ZN.loadNames(), ZN.fontsReady(['700 14px Kalameh', '600 14px Kalameh', '500 14px Kalameh'])]).then(function (res) {
    NAMES = res[0]; N = NAMES.length; built = '';
    ZH.refresh();
  }).catch(function (e) { console.error('[sky-ribbons]', e); });
})();
