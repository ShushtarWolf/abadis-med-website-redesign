/* Deferred loader for the 1L suction-bag 3D scrollytelling (approved teal-lid model).
 * Apple mode: no overlay gate — loads when the section enters view.
 * Classic mode: still sketch + button until the user taps.
 */
(function () {
  const V = '20261109e';
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

  function moduleUrl(sec) {
    const fromData = sec?.getAttribute('data-f3d-src');
    const fromScript = document.querySelector('script[data-f3d-module]')?.getAttribute('data-f3d-module');
    if (fromData) return fromData.includes('?') ? fromData : fromData + '?v=' + V;
    if (fromScript) return fromScript;
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
    if (sec.dataset.f3dLoaded === '1') return;
    sec.dataset.f3dLoaded = '1';
    const lang = langOf(sec);
    const gate = sec.querySelector('.f3d-gate');
    if (!webglOk()) {
      if (gate) gate.remove();
      markNoGl(sec, lang);
      return;
    }
    if (btn) {
      btn.disabled = true;
      btn.setAttribute('aria-busy', 'true');
      const label = btn.querySelector('span');
      if (label) label.textContent = BTN_BUSY[lang] || BTN_BUSY.en;
    }
    try {
      await import(moduleUrl(sec));
      sec.classList.remove('is-gated');
      if (gate) gate.remove();
      setTimeout(() => {
        if (!sec.classList.contains('gl-on')) markNoGl(sec, lang);
      }, 1200);
    } catch (err) {
      console.error('suction-bag 3D load failed', err);
      if (gate) gate.remove();
      markNoGl(sec, lang);
    }
  }

  document.querySelectorAll('.f3d--bag').forEach((sec) => {
    const apple = sec.classList.contains('apple-mode');
    if (apple) {
      sec.classList.remove('is-gated');
      const gate = sec.querySelector('.f3d-gate');
      if (gate) gate.remove();
      if ('IntersectionObserver' in window) {
        const io = new IntersectionObserver(
          (entries) => {
            for (const e of entries) {
              if (e.isIntersecting) {
                load3d(sec, null);
                io.disconnect();
              }
            }
          },
          { threshold: 0.2 },
        );
        io.observe(sec);
      } else {
        setTimeout(() => load3d(sec, null), 600);
      }
      return;
    }

    const btn = sec.querySelector('[data-f3d-start]');
    if (!btn) return;
    if (!webglOk()) {
      markNoGl(sec, langOf(sec));
      return;
    }
    btn.addEventListener('click', () => load3d(sec, btn));
  });
})();
