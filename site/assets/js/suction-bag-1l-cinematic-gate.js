/**
 * Deferred loader for the 1L suction-bag cinematic orbit.
 * Loads Three.js module only on click or when the section enters view (after a short idle).
 */
const roots = [...document.querySelectorAll('[data-cin-root]')];
if (!roots.length) throw new Error('cinematic root missing');

function canWebGL() {
  try {
    const c = document.createElement('canvas');
    return !!(c.getContext('webgl2') || c.getContext('webgl') || c.getContext('experimental-webgl'));
  } catch {
    return false;
  }
}

async function boot(root, { auto = false } = {}) {
  if (root.dataset.cinBooted === '1') return;
  root.dataset.cinBooted = '1';
  const status = root.querySelector('[data-cin-status]');
  const startBtn = root.querySelector('[data-cin-start]');
  if (startBtn) startBtn.disabled = true;

  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduced) {
    root.classList.add('is-reduced');
    if (status) {
      status.hidden = false;
      status.textContent = root.dataset.cinReduced || '';
    }
    return;
  }

  const modUrl = root.dataset.cinModule;
  if (!modUrl) return;
  try {
    const mod = await import(modUrl);
    await mod.mount(root, { auto });
    root.classList.remove('is-gated');
    root.classList.add('is-playing');
  } catch (err) {
    console.error('[cin] load failed', err);
    root.classList.add('no-gl');
    if (status) {
      status.hidden = false;
      status.textContent = root.dataset.cinNogl || '3D failed to load';
    }
  }
}

for (const root of roots) {
  const btn = root.querySelector('[data-cin-start]');
  if (btn) btn.addEventListener('click', () => boot(root, { auto: true }));

  // Lazy: when mostly in view, show still; only start on click unless data-cin-autostart
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(
      (entries) => {
        for (const e of entries) {
          if (e.isIntersecting && e.intersectionRatio >= 0.45 && root.dataset.cinAutostart === '1') {
            boot(root, { auto: true });
            io.disconnect();
          }
        }
      },
      { threshold: [0.45] },
    );
    io.observe(root);
  }
}
