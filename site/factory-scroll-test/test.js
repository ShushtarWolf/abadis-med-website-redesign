/* Factory scroll test badge. Listeners are passive so they cannot block scroll. */
(function () {
  const params = new URLSearchParams(location.search);
  let v = (params.get('v') || window.__F3D_TEST || 'A').toUpperCase();
  const known = { A:1, B:1, C:1, D:1, E:1, G:1, Z:1, OLD1:1, OLD2:1, OLD3:1 };
  if (!known[v]) v = 'A';
  const root = document.documentElement;
  root.dataset.f3dTest = v;
  root.classList.add('f3d-test', 'f3d-test-' + v);

  const names = {
    A: 'current main (12f)',
    B: 'no html/body overflow override',
    C: 'no OrbitControls until explore',
    D: 'stage pointer-events:none',
    E: 'phone auto-tour, no sticky track',
    G: 'render fix: no IO skip, early intro, dt floor, translateZ',
    Z: 'control: site chrome, NO factory',
    OLD1: 'pin Oct 31 24ec345c (900vh, 5 st, homepage era)',
    OLD2: 'pin Nov 5 ce9aaf92 (1060vh, last homepage factory)',
    OLD3: 'pin Nov 11 62990aaa (scroll fix, no 12f overflow)'
  };
  const hrefs = {
    A: 'index.html?v=A', B: 'index.html?v=B', C: 'index.html?v=C', D: 'index.html?v=D',
    E: 'index.html?v=E', G: 'index.html?v=G', Z: 'z.html?v=Z',
    OLD1: 'old1.html?v=OLD1', OLD2: 'old2.html?v=OLD2', OLD3: 'old3.html?v=OLD3'
  };

  // Count every rAF so we can see if the factory loop is alive even on old pins.
  let hookFrames = 0, hookLast = 0, hookFps = 0, hookPrev = 0, hookN = 0;
  const _raf = window.requestAnimationFrame.bind(window);
  window.requestAnimationFrame = function (cb) {
    return _raf(function (t) {
      hookFrames += 1;
      hookN += 1;
      if (t - hookPrev >= 500) {
        hookFps = hookPrev ? Math.round(hookN * 1000 / (t - hookPrev)) : 0;
        hookN = 0; hookPrev = t;
      }
      hookLast = t;
      return cb(t);
    });
  };

  let contextLost = false;
  function armCanvas(cv) {
    if (!cv || cv.__f3dArmed) return;
    cv.__f3dArmed = true;
    cv.addEventListener('webglcontextlost', function (e) { e.preventDefault(); contextLost = true; });
    cv.addEventListener('webglcontextrestored', function () { contextLost = false; });
  }

  const badge = document.createElement('div');
  badge.id = 'f3d-debug';
  badge.setAttribute('dir', 'ltr');
  const keys = ['A','B','C','D','E','G','Z','OLD1','OLD2','OLD3'];
  badge.innerHTML = '<div class="vars">' +
    keys.map((k) => '<a href="' + hrefs[k] + '" class="' + (k === v ? 'is-on' : '') + '">' + k.replace('OLD','o') + '</a>').join('') +
    '</div><div id="f3d-debug-body"></div>';
  document.addEventListener('DOMContentLoaded', () => document.body.appendChild(badge));

  const last = { type: 'none', y: 0, t: 0, target: '', dy: 0, moves: 0 };
  let scrollEv = { window: 0, document: 0, element: 0, vv: 0 };
  let maxSY = 0, maxST = 0, lastIntroOp = null;

  function elName(t) {
    if (!t || !t.tagName) return 'none';
    const c = (t.className && t.className.toString()) || '';
    return (t.tagName.toLowerCase() + (c ? '.' + c.split(/\s+/).slice(0, 2).join('.') : '')).slice(0, 36);
  }
  function onTouch(e) {
    const p = e.changedTouches && e.changedTouches[0] || e.touches && e.touches[0];
    const y = p ? Math.round(p.clientY) : 0;
    if (e.type === 'touchstart') { last.dy = 0; last.y = y; }
    else if (p) last.dy = y - last.y;
    last.type = e.type.replace('touch', '');
    last.t = Date.now();
    last.target = elName(e.target);
    if (e.type === 'touchmove') last.moves += 1;
  }
  ['touchstart', 'touchmove', 'touchend', 'touchcancel'].forEach((ev) => {
    window.addEventListener(ev, onTouch, { passive: true, capture: true });
  });
  window.addEventListener('scroll', () => { scrollEv.window += 1; }, { passive: true });
  document.addEventListener('scroll', () => { scrollEv.document += 1; }, { passive: true });
  if (window.visualViewport) {
    visualViewport.addEventListener('scroll', () => { scrollEv.vv += 1; }, { passive: true });
  }
  document.addEventListener('DOMContentLoaded', () => {
    const se = document.scrollingElement || document.documentElement;
    se.addEventListener('scroll', () => { scrollEv.element += 1; }, { passive: true });
  });

  function ov(el) {
    if (!el) return '-';
    const s = getComputedStyle(el);
    return (s.overflowX + '/' + s.overflowY).replace(/\s+/g, '');
  }
  function stationOf(sT, phone) {
    const start = phone ? 0.10 : 0.25;
    if (sT < start) return 'intro';
    const STEP = 0.75 / 6.5;
    const idx = Math.round((sT - start) / STEP);
    if (sT > 0.92) return 'outro/next';
    if (idx < 0) return 'intro';
    return 'st' + Math.min(5, Math.max(0, idx));
  }

  function tick() {
    const bodyEl = document.getElementById('f3d-debug-body');
    if (!bodyEl) { requestAnimationFrame(tick); return; }
    const sec = document.querySelector('.f3d');
    const stage = document.querySelector('.f3d-stage');
    const canvas = document.querySelector('.f3d-gl');
    const intro = document.querySelector('.f3d-intro');
    armCanvas(canvas);
    const se = document.scrollingElement || document.documentElement;
    const sy = window.scrollY || 0;
    const sel = se.scrollTop || 0;
    const htmlTop = document.documentElement.scrollTop || 0;
    const bodyTop = document.body ? document.body.scrollTop || 0 : 0;
    let fTop = 0, sT = 0, explore = false;
    if (sec) {
      const r = sec.getBoundingClientRect();
      const m = r.height - innerHeight;
      fTop = Math.round(r.top);
      sT = m > 0 ? Math.min(1, Math.max(0, -r.top / m)) : 0;
      explore = sec.classList.contains('is-ex');
    }
    const d = window.__f3dDebug || {};
    if (typeof d.sT === 'number') sT = d.sT; // factory's own sT when present
    maxSY = Math.max(maxSY, sy, sel);
    maxST = Math.max(maxST, sT, d.sS || 0);
    const pageMoved = maxSY > 8 || Math.abs(fTop) > 8;
    const phone = innerWidth <= 820 || (window.matchMedia && matchMedia('(pointer: coarse)').matches);
    const st = explore ? 'explore' : stationOf(sT, v === 'G' || v === 'E' ? phone : false);
    const introCs = intro ? getComputedStyle(intro) : null;
    const introOp = introCs ? introCs.opacity : '-';
    const introVis = introCs ? introCs.visibility : '-';
    if (intro && intro.style.opacity) lastIntroOp = intro.style.opacity;
    const animMoved = v === 'Z' ? pageMoved : (maxST > 0.02 || (d.renders && d.renders > 2) || (lastIntroOp != null && lastIntroOp !== '1' && lastIntroOp !== ''));
    const age = last.type === 'none' ? '' : (' ' + Math.round((Date.now() - last.t) / 1000) + 's');
    const ox = (id) => {
      const el = id === 'html' ? document.documentElement : id === 'body' ? document.body : document.getElementById('main');
      return ov(el);
    };
    const ta = stage ? getComputedStyle(stage).touchAction : '-';
    const pe = canvas ? getComputedStyle(canvas).pointerEvents : '-';
    const spe = stage ? getComputedStyle(stage).pointerEvents : '-';
    const cam = d.cam ? (d.cam.x + ',' + d.cam.y + ',' + d.cam.z) : 'n/a';
    const lost = (d.contextLost || contextLost) ? '<span class="bad">LOST</span>' : 'ok';
    const vis = (d.visible === undefined) ? 'n/a' : String(d.visible);
    const inView = (d.inView === undefined) ? 'n/a' : String(d.inView);
    const thresh = d.thresholds || (phone ? 'current fade 0.19 / hide 0.235 / st0 0.25 (G: 0.05/0.10/0.10)' : 'fade 0.19 / hide 0.235 / st0 0.25');
    const renders = d.renders != null ? d.renders : '-';
    const lastR = d.lastRender ? Math.round((performance.now() - d.lastRender)) + 'ms ago' : 'n/a';
    const dt = d.dt != null ? Number(d.dt).toFixed(4) : 'n/a';
    const sS = d.sS != null ? Number(d.sS).toFixed(3) : 'n/a';
    bodyEl.innerHTML =
      '<div class="row"><b>v=' + v + '</b> ' + names[v] + '</div>' +
      '<div class="row">scrollY ' + Math.round(sy) + '  sel ' + Math.round(sel) + '  html ' + Math.round(htmlTop) + '  body ' + Math.round(bodyTop) + '</div>' +
      '<div class="row">f3d.top ' + fTop + '  sT ' + Number(sT).toFixed(3) + '  sS ' + sS + '  station ' + st + (explore ? ' EX' : '') + '</div>' +
      '<div class="row">maxY ' + Math.round(maxSY) + '  max sT ' + maxST.toFixed(3) + '</div>' +
      '<div class="row">page ' + (pageMoved ? '<span class="ok">MOVED</span>' : '<span class="bad">stuck?</span>') +
      '  anim ' + (v === 'Z' ? (pageMoved ? '<span class="ok">n/a (no factory)</span>' : '<span class="bad">stuck?</span>') : (animMoved ? '<span class="ok">ADVANCED</span>' : '<span class="bad">not yet</span>')) + '</div>' +
      '<div class="row">rAF ' + hookFrames + '  fps ' + hookFps + '  renders ' + renders + '  last ' + lastR + '</div>' +
      '<div class="row">dt ' + dt + '  IO.visible ' + vis + '  inView ' + inView + '  gl ' + lost + '</div>' +
      '<div class="row">cam ' + cam + '  intro op ' + introOp + ' vis ' + introVis + '</div>' +
      '<div class="row">thresholds ' + thresh + '</div>' +
      '<div class="row">scroll ev w/d/el/vv ' + [scrollEv.window, scrollEv.document, scrollEv.element, scrollEv.vv].join('/') + '</div>' +
      '<div class="row">touch ' + last.type + ' dy=' + Math.round(last.dy) + ' n=' + last.moves + age + '</div>' +
      '<div class="row">on ' + (last.target || 'none') + '</div>' +
      '<div class="row">ov html ' + ox('html') + ' body ' + ox('body') + ' main ' + ox('main') + '</div>' +
      '<div class="row">ta stage ' + ta + '  pe stage/canvas ' + spe + '/' + pe + '</div>';
    requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
})();
