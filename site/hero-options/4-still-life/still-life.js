/* Hero option 4 — still life: product rise + count +۱٬۰۰۰ once. */
(() => {
  'use strict';
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const phone = matchMedia('(max-width: 900px)').matches;
  const FA = '۰۱۲۳۴۵۶۷۸۹';
  const SEP = '\u066C'; // Arabic thousands separator ٬
  const fa = (n) => {
    const s = String(Math.max(0, Math.round(n)));
    let out = '';
    for (let i = 0; i < s.length; i++) {
      if (i && (s.length - i) % 3 === 0) out += SEP;
      out += FA[+s.charAt(i)];
    }
    return out;
  };

  const root = document.querySelector('.sl-hero');
  const numEl = document.getElementById('slNum');
  if (!root || !numEl) return;

  const TARGET = 1000;

  function paint(n) {
    numEl.textContent = '+' + fa(n);
  }

  function easeOutCubic(t) { return 1 - Math.pow(1 - t, 3); }

  function countUp() {
    if (reduce || phone) { paint(TARGET); return; }
    const t0 = performance.now();
    const dur = 900;
    function frame(now) {
      const p = Math.min(1, (now - t0) / dur);
      paint(TARGET * easeOutCubic(p));
      if (p < 1) requestAnimationFrame(frame);
      else paint(TARGET);
    }
    requestAnimationFrame(frame);
  }

  function boot() {
    if (reduce || phone) {
      root.classList.add('is-in');
      paint(TARGET);
      return;
    }
    paint(0);
    // next frame: trigger CSS rise
    requestAnimationFrame(() => {
      root.classList.add('is-in');
      countUp();
    });
  }

  if (document.readyState === 'complete') setTimeout(boot, 80);
  else window.addEventListener('load', () => setTimeout(boot, 80));
})();
