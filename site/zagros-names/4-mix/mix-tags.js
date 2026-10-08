/* Sample 4 — «درخت‌ها و دیوار افتخار»
   Scene part: one wooden tag per oak, rotating through a calm selection of names (not the whole list):
   each tree shows ~C names over the scroll, ≥ ~240px of scroll per name (≈170px fully readable), with a soft crossfade/drift.
   The selection is spread evenly through names.json. When the canister rises, the counter «+۱٬۲۵۳ مرکز درمانی»
   counts in and the visible tags drift down out of the scene (scroll-scrubbed, reversible) toward the wall below,
   where every name sits in the columns. The counter hands off to the wall's counter as the scene scrolls away.
   Same placement rules as sample 1 (hero copy, canister, counter, each other). Transform/opacity only. */
(function () {
  'use strict';
  var ZH = window.__zagrosHero, ZN = window.ZN;
  if (!ZH || !ZN) return;
  var clamp = ZN.clamp, seg = ZN.seg, smooth = ZN.smooth;
  var stage = ZH.stage, layer = document.getElementById('ttTags');
  var bg = stage.querySelector('.zh-bg'), spotsEl = document.getElementById('zhSpots');
  var copyEl = stage.querySelector('.csr-hero > div');
  var countEl = document.getElementById('mxCount'), numEl = document.getElementById('mxNum');

  var Q0 = 0.14, Q1 = 0.78;          // rotation part of the scroll (acorns land ~0.12, canister rises 0.80–0.95)
  var PERIOD = 240;                  // px of scroll per name on each tree (calm, readable)
  var C_IN = 0.80, C_FULL = 0.92;    // counter counts in with the canister
  var F0 = 0.83, F1 = 1.0;           // tags drift down out of the scene
  var PAN = 0.03, ZOOM = 1.07;
  var NAMES = [], N = 0, meas = [], fontKey = '';
  var slots = [], S = 0, C = 2, T = 0, obst = [], cRect = null, W = 0, H = 0, visBottom = 0, countTop = 0, canG = null;
  var ctx = document.createElement('canvas').getContext('2d');

  function cfg() {
    var desk = W >= 900;
    return { desk: desk, fs: desk ? 12.5 : 10.5, padX: desk ? 10 : 6, maxW: desk ? 210 : Math.min(104, W * 0.27), lh: desk ? 18.2 : 15.2, padY: 5, stick: desk ? 24 : 18, lift: desk ? 22 : 16 };
  }
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
      return { w: Math.ceil(widest + 2 * c.padX + 4), h: Math.ceil(lines * c.lh + c.padY + 2) };
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
    slots = spots.map(function (sp, k) { return { sp: sp, k: k, phase: 0.2 + 0.55 * (k / S), tags: [makeTag(), makeTag()] }; });
  }
  // name for tree k at rotation step m: an even spread through the whole list
  function nameIdx(k, m) { return Math.min(N - 1, Math.floor((k + m * S) * N / T)); }

  function rect(el, pad) {
    var r = el.getBoundingClientRect(), s = stage.getBoundingClientRect();
    return { l: r.left - s.left - pad, r: r.right - s.left + pad, t: r.top - s.top - pad, b: r.bottom - s.top + pad };
  }
  function onLayout() {
    W = ZH.W; H = ZH.H;
    if (!N) return;
    buildSlots();
    measureAll();
    C = Math.max(2, Math.floor((Q1 - Q0) * ZH.track / PERIOD) + 1);
    T = S * C;
    var can = ZH.canister, cw = can.offsetWidth;
    canG = { l: can.offsetLeft - cw / 2, r: can.offsetLeft + cw / 2, t: can.offsetTop, h: can.offsetHeight };
    visBottom = H;
    var probe = document.createElement('div');                         // Safari: part of the stage under the bottom bar
    probe.style.cssText = 'position:absolute;height:var(--zh-vis-bottom);width:0;visibility:hidden';
    stage.appendChild(probe); visBottom = H - probe.offsetHeight; stage.removeChild(probe);
    var cr = rect(copyEl, 0);
    // counter sits centred under the hero copy, above the canister; measured with its final text
    var keep = numEl.textContent; numEl.textContent = ZN.fa(N);
    var ch = countEl.offsetHeight, cwid = countEl.offsetWidth;
    numEl.textContent = keep;
    countTop = Math.min(cr.b + (W >= 900 ? 18 : 14), can.offsetTop - ch - 10);
    cRect = { l: W / 2 - cwid / 2 - 8, r: W / 2 + cwid / 2 + 8, t: countTop - 6, b: countTop + ch + 6 };
    obst = [
      { l: cr.l - 10, r: cr.r + 10, t: cr.t - 10, b: cr.b + 10 },
      { l: can.offsetLeft - cw / 2 - 5, r: can.offsetLeft + cw / 2 + 5, t: can.offsetTop - 8, b: can.offsetTop + can.offsetHeight + 20 }
    ];
  }
  function hit(a, list) {
    for (var i = 0; i < list.length; i++) { var b = list[i]; if (a.l < b.r && a.r > b.l && a.t < b.b && a.b > b.t) return true; }
    return false;
  }

  var exitK = 0;                     // 0 while pinned, → 1 as the scene scrolls away (counter hand-off)
  function counter(p) {
    var co = ZH.reduced ? 0 : smooth(seg(p, C_IN, C_FULL - 0.03)) * (1 - exitK);
    var n = p >= C_FULL ? N : Math.min(N - 1, Math.floor(N * smooth(seg(p, C_IN, C_FULL))));
    var t = ZN.fa(n);
    if (t !== countEl._n) { numEl.textContent = t; countEl._n = t; }
    var tf = 'translate3d(-50%,' + (countTop + (1 - smooth(seg(p, C_IN, C_FULL))) * 16 - exitK * 24).toFixed(1) + 'px,0)';
    if (tf !== countEl._tf) { countEl.style.transform = tf; countEl._tf = tf; }
    var o = co.toFixed(3);
    if (o !== countEl._o) { countEl.style.opacity = o; countEl._o = o; }
    return co;
  }

  function onRender(p) {
    if (!N || !slots.length) return;
    var c = cfg(), reduced = ZH.reduced;
    var pan = (1 - 2 * smooth(seg(p, 0.04, 0.80))) * PAN * W;
    var tf = 'translate3d(' + pan.toFixed(1) + 'px,0,0) scale(' + ZOOM + ')';
    if (tf !== bg._tf) { bg.style.transform = spotsEl.style.transform = tf; bg._tf = tf; }

    var co = counter(p);
    var fall = reduced ? 0 : smooth(seg(p, F0, F1));
    var q = seg(p, Q0, Q1);
    var maxH = 0, placed = obst.slice();
    for (var i = 0; i < S; i++) if (slots[i].sp.H > maxH) maxH = slots[i].sp.H;
    var items = [];
    slots.slice().sort(function (a, b) { return b.sp.gy - a.sp.gy; }).forEach(function (sl) {
      var sp = sl.sp;
      var gate = smooth(clamp((sp.fall - 0.85) / 0.15, 0, 1));
      var pos = q * (C - 1) + sl.phase, m = Math.floor(pos);
      for (var j = 0; j < 2; j++) {
        var mm = m - j, tag = sl.tags[((mm % 2) + 2) % 2];
        if (mm < 0 || mm >= C) { items.push({ tag: tag, hide: true }); continue; }
        var t = pos - mm;
        var a = smooth(seg(t, 0, 0.12)), d = smooth(seg(t, 0.84, 1.12));
        if (mm === C - 1) d = 0;                                       // last name of each tree stays until the drift
        items.push({ tag: tag, sl: sl, idx: nameIdx(sl.k, mm), a: a * gate, d: d, leaving: j === 1 });
      }
    });
    items.sort(function (x, y) { return (x.hide ? 2 : x.leaving ? 1 : 0) - (y.hide ? 2 : y.leaving ? 1 : 0); });
    var cx = W / 2;
    items.forEach(function (it) {
      var tag = it.tag;
      if (it.hide || it.a * (1 - it.d) < 0.01 || fall >= 0.999) { setO(tag, 0); return; }
      if (tag.idx !== it.idx) {
        tag.idx = it.idx; tag.cand = 0;
        tag.plate.textContent = NAMES[it.idx];
        tag.plate.style.width = meas[it.idx].w + 'px';
      }
      var sp = it.sl.sp, mz = meas[it.idx];
      var ds = clamp(0.82 + 0.18 * (sp.H / maxH), 0.82, 1) * (1 - 0.32 * it.d);
      var bx = cx + (sp.gx - cx) * ZOOM + pan, by = H + (sp.gy - H) * ZOOM;
      bx += (cx - bx) * 0.12 * it.d;
      by -= 16 * it.d;
      var w = mz.w * ds, h = mz.h * ds, side = sp.gx < cx ? 1 : -1;
      var lean = side * Math.min(w / 2 - 12, sp.H * 0.12 + 8);
      var cands = [[0, 0], [lean, 0], [-lean, 0], [0, 1], [lean, 1], [-lean, 1]];
      var best = -1, r;
      for (var n = 0; n < cands.length; n++) {
        var ci = (n + tag.cand) % cands.length;
        var raise = cands[ci][1] ? h + 6 : 0;
        var px = clamp(bx + cands[ci][0], w / 2 + 6, W - w / 2 - 6);
        var bottom = by - c.lift * ds - raise;
        r = { l: px - w / 2 - 3, r: px + w / 2 + 3, t: bottom - h - 3, b: bottom + 3 };
        if (r.b > visBottom - 4 || r.t < 0) continue;
        if (cRect && raise && hit(r, [cRect])) continue;               // never raise a tag into the counter's spot
        if (!hit(r, placed)) { best = ci; break; }
      }
      if (best < 0) { setO(tag, 0); return; }
      tag.cand = best;
      placed.push(r);
      // a tag under the counter's spot gives way while the counter fades in (no overlap at any moment)
      var give = cRect && hit(r, [cRect]) ? 1 - Math.min(1, co * 4) : 1;
      var raise2 = cands[best][1] ? h + 6 : 0;
      var off = clamp(bx + cands[best][0], w / 2 + 6, W - w / 2 - 6) - bx;
      var ptf = 'translate3d(calc(-50% + ' + (off / ds).toFixed(1) + 'px),' + (-raise2 / ds).toFixed(1) + 'px,0) rotate(' + (side * -1.5) + 'deg)';
      if (ptf !== tag._p) { tag.plate.style.transform = ptf; tag._p = ptf; }
      var stf = 'scaleY(' + ((c.stick + raise2 / ds) / c.stick).toFixed(3) + ')';
      if (stf !== tag._s) { tag.stick.style.transform = stf; tag._s = stf; }
      // drift down past the bottom edge, easing outward (away from the canister, never across it), fading out
      var fy = fall * (H - by + h + 60 + (it.sl.k % 3) * 30);
      var fr = fall * side * (8 + (it.sl.k % 4) * 3);
      var fs = 1 - 0.12 * fall;
      var fx = bx - side * (14 + (it.sl.k % 3) * 6) * fall;
      if (fall > 0 && canG) {
        // keep falling tags clear of the rising canister: if a tag would pass its height, ease it out sideways first
        var cc = smooth(seg(p, 0.80, 0.95)), canTop = canG.t + (1 - cc) * 0.26 * canG.h;
        var cxT = fx + off * fs, half = w * fs / 2 + 4;
        var tb = by + 2 + fy - (c.lift * ds + raise2) * fs;
        var near = clamp((tb - canTop + 40) / 40, 0, 1);
        var push = cxT < cx ? Math.min(0, canG.l - 8 - (cxT + half)) : Math.max(0, canG.r + 8 - (cxT - half));
        fx += push * near;
      }
      var etf = 'translate3d(' + fx.toFixed(1) + 'px,' + (by + 2 + fy).toFixed(1) + 'px,0) rotate(' + fr.toFixed(2) + 'deg) scale(' + (ds * fs).toFixed(3) + ')';
      if (etf !== tag._t) { tag.el.style.transform = etf; tag._t = etf; }
      setO(tag, it.a * (1 - it.d) * give * (1 - smooth(seg(fall, 0.45, 1))));
    });
  }
  function setO(tag, o) { var s = o.toFixed(3); if (s !== tag._o) { tag.el.style.opacity = s; tag._o = s; } }

  // hand-off: as the pinned scene scrolls away, the scene counter fades and the wall's counter takes over
  function onScroll() {
    var y = window.pageYOffset || document.documentElement.scrollTop;
    var k = ZH.reduced ? 1 : clamp((y - ZH.heroTop - ZH.track) / (ZH.H * 0.3), 0, 1);
    k = Math.round(k * 100) / 100;
    if (k !== exitK) { exitK = k; counter(ZH.p); }
  }
  window.addEventListener('scroll', onScroll, { passive: true });

  ZH.onLayout(onLayout);
  ZH.onRender(onRender);
  Promise.all([ZN.loadNames(), ZN.fontsReady(['700 10.5px Kalameh', '700 12.5px Kalameh', '900 40px Kalameh'])]).then(function (res) {
    NAMES = res[0]; N = NAMES.length;
    fontKey = '';
    ZH.refresh(); onScroll();
  }).catch(function (e) { console.error('[mix-tags]', e); });
})();
