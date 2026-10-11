/* Hero option 2 — savings dial: auto 0→5000, drag to 15000, real Abadis formulas. */
(() => {
  'use strict';
  const MAX = 15000, TARGET = 5000, STEP = 100, ARC = 300;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const NS = 'http://www.w3.org/2000/svg';
  const FA = '۰۱۲۳۴۵۶۷۸۹';
  const fa = (n) => {
    const s = String(Math.max(0, Math.round(n)));
    let out = '';
    for (let i = 0; i < s.length; i++) {
      if (i && (s.length - i) % 3 === 0) out += '\u066C';
      out += FA[+s.charAt(i)];
    }
    return out;
  };
  const clamp = (v, a, b) => (v < a ? a : v > b ? b : v);
  const F = {
    water: (n) => n * 1.6 * 9.3,
    cost: (n) => n * 2.5 * 85000,
    hours: (n) => n * 1.7 / 60 * 2.2 * 7.1,
  };

  const wrap = document.getElementById('dhKnob');
  const disk = document.getElementById('dhKnobDisk');
  const arc = document.getElementById('dhArc');
  const numEl = document.getElementById('dhNum');
  const waterEl = document.getElementById('dhWater');
  const costEl = document.getElementById('dhCost');
  const hoursEl = document.getElementById('dhHours');
  const noteEl = document.querySelector('.dh-note');
  if (!wrap || !disk || !arc) return;

  // ticks
  const g = wrap.querySelector('.ticks');
  if (g && !g.childElementCount) {
    for (let i = 0; i <= 40; i++) {
      const ang = (-150 + i * 7.5) * Math.PI / 180, major = i % 5 === 0;
      const r1 = 99, r2 = major ? 107 : 104;
      const l = document.createElementNS(NS, 'line');
      l.setAttribute('class', 'tick' + (major ? ' major' : ''));
      l.setAttribute('x1', 100 + r1 * Math.sin(ang));
      l.setAttribute('y1', 100 - r1 * Math.cos(ang));
      l.setAttribute('x2', 100 + r2 * Math.sin(ang));
      l.setAttribute('y2', 100 - r2 * Math.cos(ang));
      g.appendChild(l);
    }
  }

  let value = 0, animating = false, userTouched = false;

  function paint(n) {
    value = clamp(Math.round(n / STEP) * STEP, 0, MAX);
    const t = value / MAX;
    const deg = -150 + t * ARC;
    disk.style.transform = 'rotate(' + deg + 'deg)';
    arc.style.strokeDasharray = (t * ARC) + ' 360';
    numEl.textContent = fa(value);
    waterEl.textContent = fa(F.water(value));
    costEl.textContent = fa(F.cost(value));
    hoursEl.textContent = fa(F.hours(value));
    wrap.setAttribute('aria-valuenow', String(value));
    if (noteEl) {
      noteEl.textContent = value === TARGET
        ? 'برای ۵٬۰۰۰ عمل در سال'
        : ('برای ' + fa(value) + ' عمل در سال');
    }
  }

  function easeOutCubic(t) { return 1 - Math.pow(1 - t, 3); }

  function animateTo(to, ms) {
    if (reduce) { paint(to); return Promise.resolve(); }
    animating = true;
    const from = value, t0 = performance.now();
    return new Promise((resolve) => {
      function frame(now) {
        if (userTouched && to === TARGET) { animating = false; resolve(); return; }
        const p = clamp((now - t0) / ms, 0, 1);
        paint(from + (to - from) * easeOutCubic(p));
        if (p < 1) requestAnimationFrame(frame);
        else { animating = false; resolve(); }
      }
      requestAnimationFrame(frame);
    });
  }

  // Drag (same idea as dial-practical)
  const drag = { on: false, ang0: 0, raw: 0 };
  function angleAt(x, y) {
    const r = wrap.getBoundingClientRect();
    const cx = r.left + r.width / 2, cy = r.top + r.height / 2;
    let a = Math.atan2(x - cx, cy - y) * 180 / Math.PI; // 0 = up
    return a;
  }
  function onDown(e) {
    userTouched = true;
    drag.on = true;
    wrap.classList.add('dragging');
    const pt = e.touches ? e.touches[0] : e;
    drag.ang0 = angleAt(pt.clientX, pt.clientY);
    drag.raw = value;
    if (e.pointerId != null) try { wrap.setPointerCapture(e.pointerId); } catch (_) {}
  }
  function onMove(e) {
    if (!drag.on) return;
    const pt = e.touches ? e.touches[0] : e;
    let a = angleAt(pt.clientX, pt.clientY);
    let d = a - drag.ang0;
    if (d > 180) d -= 360;
    if (d < -180) d += 360;
    drag.ang0 = a;
    drag.raw = clamp(drag.raw + d / ARC * MAX, 0, MAX);
    paint(drag.raw);
    if (e.cancelable) e.preventDefault();
  }
  function onUp() {
    if (!drag.on) return;
    drag.on = false;
    wrap.classList.remove('dragging');
    paint(value);
  }
  wrap.addEventListener('pointerdown', onDown);
  wrap.addEventListener('pointermove', onMove);
  wrap.addEventListener('pointerup', onUp);
  wrap.addEventListener('pointercancel', onUp);
  wrap.addEventListener('keydown', (e) => {
    userTouched = true;
    let nv = value;
    if (e.key === 'ArrowLeft' || e.key === 'ArrowDown') nv -= STEP;
    else if (e.key === 'ArrowRight' || e.key === 'ArrowUp') nv += STEP;
    else if (e.key === 'Home') nv = 0;
    else if (e.key === 'End') nv = MAX;
    else if (e.key === 'PageUp') nv += STEP * 10;
    else if (e.key === 'PageDown') nv -= STEP * 10;
    else return;
    e.preventDefault();
    paint(nv);
  });

  // Boot: paint 0, then ease to 5000 (or show final if reduced-motion)
  paint(0);
  const start = () => {
    if (userTouched) return;
    if (reduce) paint(TARGET);
    else animateTo(TARGET, 2500);
  };
  if (document.readyState === 'complete') setTimeout(start, 120);
  else window.addEventListener('load', () => setTimeout(start, 120));
})();
