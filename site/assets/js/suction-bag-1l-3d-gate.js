/* Deferred loader for the 1L suction-bag 3D scrollytelling.
 * Does not download Three.js / the heavy module until the user taps "View in 3D".
 * Still sketch stays visible if WebGL is unavailable (same pattern as factory-3d fallback).
 */
(function () {
  const V = '20261109a';
  const BTN_BUSY = { fa: 'در حال بارگذاری…', en: 'Loading…', ar: 'جارٍ التحميل…' };
  const NO_GL = {
    fa: 'مرورگر شما نمایش سه‌بعدی را پشتیبانی نمی‌کند؛ طرح ثابت نمایش داده می‌شود.',
    en: 'Your browser cannot run the 3D view; the still sketch stays on screen.',
    ar: 'متصفحك لا يدعم العرض ثلاثي الأبعاد؛ ستبقى الرسمة الثابتة ظاهرة.',
  };

  function langOf(sec) {
    try {
      const cfg = JSON.parse(sec.querySelector('.f3d-cfg').textContent);
      return (cfg.lang || document.documentElement.lang || 'fa').slice(0, 2);
    } catch (e) {
      return (document.documentElement.lang || 'fa').slice(0, 2);
    }
  }

  function webglOk() {
    try {
      const c = document.createElement('canvas');
      return !!(c.getContext('webgl') || c.getContext('experimental-webgl'));
    } catch (e) {
      return false;
    }
  }

  function moduleUrl() {
    return new URL('./suction-bag-1l-3d.js?v=' + V, import.meta.url).href;
  }

  function markNoGl(sec, lang) {
    sec.classList.add('no-gl');
    sec.classList.remove('is-gated', 'gl-on');
    const note = document.createElement('p');
    note.className = 'f3d-gate-note';
    note.style.cssText = 'position:absolute;inset-inline:16px;bottom:16px;z-index:5;margin:0;text-align:center';
    note.textContent = NO_GL[lang] || NO_GL.en;
    sec.querySelector('.f3d-stage')?.appendChild(note);
  }

  async function load3d(sec, btn) {
    const lang = langOf(sec);
    if (!webglOk()) {
      const gate = sec.querySelector('.f3d-gate');
      if (gate) gate.remove();
      markNoGl(sec, lang);
      return;
    }
    btn.disabled = true;
    btn.setAttribute('aria-busy', 'true');
    const label = btn.querySelector('span');
    if (label) label.textContent = BTN_BUSY[lang] || BTN_BUSY.en;
    try {
      await import(moduleUrl());
      sec.classList.remove('is-gated');
      const gate = sec.querySelector('.f3d-gate');
      if (gate) gate.remove();
      // If WebGLRenderer silently fails, keep the CSS still-sketch fallback.
      setTimeout(() => {
        if (!sec.classList.contains('gl-on')) markNoGl(sec, lang);
      }, 1200);
    } catch (err) {
      console.error('suction-bag 3D load failed', err);
      const gate = sec.querySelector('.f3d-gate');
      if (gate) gate.remove();
      markNoGl(sec, lang);
    }
  }

  document.querySelectorAll('.f3d--bag').forEach((sec) => {
    sec.classList.add('is-gated');
    const btn = sec.querySelector('[data-f3d-start]');
    if (!btn) return;
    btn.addEventListener('click', () => load3d(sec, btn));
  });
})();
