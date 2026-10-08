/* Sample 1 — «یک درخت، یک نام»
   Each oak spot carries one wooden tag. Scroll progress rotates every spot through its share of the 1,253 names
   (spot k shows names k, k+S, k+2S …), so the whole list passes while only one tag per tree is readable.
   A leaving tag drifts back toward the horizon and fades while the next one appears. The scene pans slowly.
   Tags are placed per frame with collision checks against the hero copy, the risen canister, the counter and
   each other; a tag that cannot be placed cleanly is simply not shown that frame. Transform/opacity only. */
(function () {
  'use strict';
  var ZH = window.__zagrosHero, ZN = window.ZN;
  if (!ZH || !ZN) return;
  var clamp = ZN.clamp, seg = ZN.seg, smooth = ZN.smooth;
  var stage = ZH.stage, layer = document.getElementById('ttTags');
  var bg = stage.querySelector('.zh-bg'), spotsEl = document.getElementById('zhSpots');
  var copyEl = stage.querySelector('.csr-hero > div'), counterEl = document.getElementById('znCounter');
  var cnt = ZN.counter(counterEl);

  var Q0 = 0.12, Q1 = 0.86;          // part of the scroll over which the names rotate (acorns land ~0.12, canister ~0.80–0.95)
  var PAN = 0.03, ZOOM = 1.07;       // slow drift across the forest: ±3% of the width, slight zoom so edges stay covered
  var NAMES = [], N = 0, meas = [], fontKey = '';
  var slots = [], S = 0, obst = [], W = 0, H = 0, visBottom = 0;
  var ctx = document.createElement('canvas').getContext('2d');

  function cfg() {
    var desk = W >= 900;
    return { desk: desk, fs: desk ? 12.5 : 10.5, padX: desk ? 10 : 6, maxW: desk ? 210 : Math.min(104, W * 0.27), lh: desk ? 18.2 : 15.2, padY: 5, stick: desk ? 24 : 18, lift: desk ? 22 : 16 };
  }
  // greedy word wrap with canvas metrics, so plate size is known without touching layout
  function measureAll() {
    var c = cfg(), key = c.fs + '|' + c.maxW;
    if (key === fontKey && meas.length === N) return;
    fontKey = key;
    ctx.font = '700 ' + c.fs + 'px Kalameh, Tahoma, sans-serif';
    var space = ctx.measureText(' ').width;
    meas = NAMES.map(function (name) {
      var words = name.split(' '), lines = 1, line = 0, widest = 0;
      for (var i = 0; i < words.length; i++) {
        var ww = ctx.measureText(words[i]).width;
        if (line && line + space + ww > c.maxW) { widest = Math.max(widest, line); lines++; line = ww; }
        else line = line ? line + space + ww : ww;
      }
      widest = Math.min(c.maxW, Math.max(widest, line));
      var w = Math.ceil(widest + 2 * c.padX + 4);
      return { w: w, h: Math.ceil(lines * c.lh + c.padY + 2), lines: lines };
    });
  }

  function makeTag() {
    var el = document.createElement('div');
    el.className = 'zh-mark tt-tag';
    el.innerHTML = '<i class="zh-mark-foot"></i><i class="zh-mark-stick"></i><span class="zh-mark-plate"></span>';
    layer.appendChild(el);
    return { el: el, stick: el.querySelector('.zh-mark-stick'), plate: el.querySelector('.zh-mark-plate'), idx: -1, cand: 0, _t: '', _o: '', _p: '', _s: '' };
  }

  function buildSlots() {
    var spots = ZH.spots;
    if (slots.length === spots.length && slots[0] && slots[0].sp === spots[0]) return;
    layer.textContent = '';
    S = spots.length;
    slots = spots.map(function (sp, k) {
      var count = Math.max(0, Math.ceil((N - k) / S));             // names k, k+S, k+2S, … (< N)
      return { sp: sp, k: k, count: count, phase: 0.2 + 0.55 * (k / S), tags: [makeTag(), makeTag()] };
    });
  }

  function rect(el, pad) {
    var r = el.getBoundingClientRect(), s = stage.getBoundingClientRect();
    return { l: r.left - s.left - pad, r: r.right - s.left + pad, t: r.top - s.top - pad, b: r.bottom - s.top + pad };
  }
  function onLayout() {
    W = ZH.W; H = ZH.H;
    if (!N) return;
    buildSlots();
    measureAll();
    var can = ZH.canister;                                          // final (risen) canister box, layout position ignores transform
    visBottom = H - (parseFloat(getComputedStyle(stage).getPropertyValue('--zh-vis-bottom')) || 0);
    var cw = can.offsetWidth;
    obst = [
      rect(copyEl, 10),
      { l: can.offsetLeft - cw / 2 - 5, r: can.offsetLeft + cw / 2 + 5, t: can.offsetTop - 8, b: can.offsetTop + can.offsetHeight + 20 },
      rect(counterEl, 8)
    ];
  }
  function hit(a, list) {
    for (var i = 0; i < list.length; i++) { var b = list[i]; if (a.l < b.r && a.r > b.l && a.t < b.b && a.b > b.t) return true; }
    return false;
  }

  function onRender(p) {
    if (!N || !slots.length) return;
    var c = cfg();
    // scroll-scrubbed pan of the painted scene (background + oaks move together)
    var pan = (1 - 2 * smooth(seg(p, 0.04, 0.86))) * PAN * W;
    var tf = 'translate3d(' + pan.toFixed(1) + 'px,0,0) scale(' + ZOOM + ')';
    if (tf !== bg._tf) { bg.style.transform = spotsEl.style.transform = tf; bg._tf = tf; }

    var q = seg(p, Q0, Q1);
    var maxH = 0, shown = 0, placed = obst.slice();
    for (var i = 0; i < S; i++) if (slots[i].sp.H > maxH) maxH = slots[i].sp.H;
    var order = slots.slice().sort(function (a, b) { return b.sp.gy - a.sp.gy; });   // nearest trees first
    var items = [];
    order.forEach(function (sl) {
      var sp = sl.sp;
      if (!sl.count) return;
      var gate = smooth(clamp((sp.fall - 0.85) / 0.15, 0, 1));       // tags appear once the acorn has landed
      var pos = q * (sl.count - 1) + sl.phase, m = Math.floor(pos);
      shown += Math.min(sl.count, m + 1) * (gate > 0.5 ? 1 : 0);
      // current tag (index m) and the one leaving (m-1); element = parity of the name position
      for (var j = 0; j < 2; j++) {
        var mm = m - j, tag = sl.tags[((mm % 2) + 2) % 2];
        if (mm < 0 || mm >= sl.count) { items.push({ tag: tag, hide: true }); continue; }
        var t = pos - mm;
        var a = smooth(seg(t, 0, 0.12)), d = smooth(seg(t, 0.84, 1.18));
        if (mm === sl.count - 1) d = 0;                                // the last name of each tree stays
        items.push({ tag: tag, sl: sl, idx: sl.k + mm * S, a: a * gate, d: d, leaving: j === 1 });
      }
    });
    // current tags get placement priority over leaving ones
    items.sort(function (x, y) { return (x.hide ? 2 : x.leaving ? 1 : 0) - (y.hide ? 2 : y.leaving ? 1 : 0); });
    var cx = W / 2;
    items.forEach(function (it) {
      var tag = it.tag;
      if (it.hide || it.a * (1 - it.d) < 0.01) { setO(tag, 0); return; }
      if (tag.idx !== it.idx) {
        tag.idx = it.idx; tag.cand = 0;
        var mm = meas[it.idx];
        tag.plate.textContent = NAMES[it.idx];
        tag.plate.style.width = mm.w + 'px';
      }
      var sp = it.sl.sp, mz = meas[it.idx];
      var ds = clamp(0.82 + 0.18 * (sp.H / maxH), 0.82, 1) * (1 - 0.32 * it.d);   // farther / leaving = smaller
      // base point in screen space (follows the pan + zoom about the bottom centre)
      var bx = cx + (sp.gx - cx) * ZOOM + pan, by = H + (sp.gy - H) * ZOOM;
      bx += (cx - bx) * 0.12 * it.d;                                 // leaving tags drift toward the vanishing point …
      by -= 16 * it.d;                                               // … and back toward the horizon
      var w = mz.w * ds, h = mz.h * ds, side = sp.gx < cx ? 1 : -1;
      var lean = side * Math.min(w / 2 - 12, sp.H * 0.12 + 8);
      var cands = [[0, 0], [lean, 0], [-lean, 0], [0, 1], [lean, 1], [-lean, 1]];
      var best = -1, r;
      for (var n = 0; n < cands.length; n++) {
        var ci = (n + tag.cand) % cands.length;                     // keep last frame's choice when still valid (no jitter)
        var raise = cands[ci][1] ? h + 6 : 0;
        var px = clamp(bx + cands[ci][0], w / 2 + 6, W - w / 2 - 6);
        var bottom = by - c.lift * ds - raise;
        r = { l: px - w / 2 - 3, r: px + w / 2 + 3, t: bottom - h - 3, b: bottom + 3 };
        if (r.b > visBottom - 4 || r.t < 0) continue;
        if (!hit(r, placed)) { best = ci; break; }
      }
      if (best < 0) { setO(tag, 0); return; }
      tag.cand = best;
      placed.push(r);
      var raise2 = cands[best][1] ? h + 6 : 0;
      var off = clamp(bx + cands[best][0], w / 2 + 6, W - w / 2 - 6) - bx;
      var ptf = 'translate3d(calc(-50% + ' + (off / ds).toFixed(1) + 'px),' + (-raise2 / ds).toFixed(1) + 'px,0) rotate(' + (side * -1.5) + 'deg)';
      if (ptf !== tag._p) { tag.plate.style.transform = ptf; tag._p = ptf; }
      var stf = 'scaleY(' + ((c.stick + raise2 / ds) / c.stick).toFixed(3) + ')';
      if (stf !== tag._s) { tag.stick.style.transform = stf; tag._s = stf; }
      var etf = 'translate3d(' + bx.toFixed(1) + 'px,' + (by + 2).toFixed(1) + 'px,0) scale(' + ds.toFixed(3) + ')';
      if (etf !== tag._t) { tag.el.style.transform = etf; tag._t = etf; }
      setO(tag, it.a * (1 - it.d));
    });
    cnt.set(p >= Q1 ? N : Math.min(N, shown));
  }
  function setO(tag, o) { var s = o.toFixed(3); if (s !== tag._o) { tag.el.style.opacity = s; tag._o = s; } }

  ZH.onLayout(onLayout);
  ZH.onRender(onRender);
  Promise.all([ZN.loadNames(), ZN.fontsReady(['700 10.5px Kalameh', '700 12.5px Kalameh'])]).then(function (res) {
    NAMES = res[0]; N = NAMES.length;
    fontKey = '';
    ZH.refresh();
  }).catch(function (e) { console.error('[tree-tags]', e); });
})();
