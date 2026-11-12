/* Factory scroll test badge. Listeners are passive so they cannot block scroll. */
(function () {
  const params = new URLSearchParams(location.search);
  let v = (params.get('v') || 'A').toUpperCase();
  if (!/^[ABCD]$/.test(v)) v = 'A';
  const root = document.documentElement;
  root.dataset.f3dTest = v;
  root.classList.add('f3d-test', 'f3d-test-' + v);

  const names = {
    A: 'current main (12f)',
    B: 'no html/body overflow override',
    C: 'no OrbitControls until explore',
    D: 'stage pointer-events:none'
  };

  const badge = document.createElement('div');
  badge.id = 'f3d-debug';
  badge.setAttribute('dir', 'ltr');
  badge.innerHTML = '<div class="vars">' +
    'ABCD'.split('').map((k) => '<a href="?v=' + k + '" class="' + (k === v ? 'is-on' : '') + '">' + k + '</a>').join('') +
    '</div><div id="f3d-debug-body"></div>';
  document.addEventListener('DOMContentLoaded', () => document.body.appendChild(badge));

  const last = { type: 'none', y: 0, t: 0, target: '', dy: 0, moves: 0 };
  let scrollEv = { window: 0, document: 0, element: 0, vv: 0 };
  let lastSY = 0, lastST = 0, maxSY = 0, maxST = 0;

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
  function stationOf(sT) {
    if (sT < 0.19) return 'intro';
    // same STEP as factory-3d.js: 0.75 / (6 + 0.5)
    const STEP = 0.75 / 6.5;
    const idx = Math.round((sT - 0.25) / STEP);
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
    maxSY = Math.max(maxSY, sy, sel);
    maxST = Math.max(maxST, sT);
    const pageMoved = maxSY > 8 || Math.abs(fTop) > 8;
    const animMoved = maxST > 0.02;
    const st = explore ? 'explore' : stationOf(sT);
    const age = last.type === 'none' ? '' : (' ' + Math.round((Date.now() - last.t) / 1000) + 's');
    const ox = (id) => {
      const el = id === 'html' ? document.documentElement : id === 'body' ? document.body : document.getElementById('main');
      return ov(el);
    };
    const ta = stage ? getComputedStyle(stage).touchAction : '-';
    const pe = canvas ? getComputedStyle(canvas).pointerEvents : '-';
    const spe = stage ? getComputedStyle(stage).pointerEvents : '-';
    bodyEl.innerHTML =
      '<div class="row"><b>v=' + v + '</b> ' + names[v] + '</div>' +
      '<div class="row">scrollY ' + Math.round(sy) + '  sel ' + Math.round(sel) + '  html ' + Math.round(htmlTop) + '  body ' + Math.round(bodyTop) + '</div>' +
      '<div class="row">f3d.top ' + fTop + '  sT ' + sT.toFixed(3) + '  station ' + st + (explore ? ' EX' : '') + '</div>' +
      '<div class="row">maxY ' + Math.round(maxSY) + '  max sT ' + maxST.toFixed(3) + '</div>' +
      '<div class="row">page ' + (pageMoved ? '<span class="ok">MOVED</span>' : '<span class="bad">stuck?</span>') +
      '  anim ' + (animMoved ? '<span class="ok">ADVANCED</span>' : '<span class="bad">not yet</span>') + '</div>' +
      '<div class="row">scroll ev w/d/el/vv ' + [scrollEv.window, scrollEv.document, scrollEv.element, scrollEv.vv].join('/') + '</div>' +
      '<div class="row">touch ' + last.type + ' dy=' + Math.round(last.dy) + ' n=' + last.moves + age + '</div>' +
      '<div class="row">on ' + (last.target || 'none') + '</div>' +
      '<div class="row">ov html ' + ox('html') + ' body ' + ox('body') + ' main ' + ox('main') + '</div>' +
      '<div class="row">ta stage ' + ta + '  pe stage/canvas ' + spe + '/' + pe + '</div>';
    lastSY = sy; lastST = sT;
    requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
})();
