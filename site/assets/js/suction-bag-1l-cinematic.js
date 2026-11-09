/**
 * Cinematic view for the 1L bag: smooth image-sequence orbit/dolly with lid-reveal frames.
 * Loaded only via the gate. Respects prefers-reduced-motion. No emojis.
 */
export async function mount(root, { auto = true } = {}) {
  const canvas = root.querySelector('.cin-gl');
  const toggle = root.querySelector('[data-cin-toggle]');
  const bar = root.querySelector('.cin-bar');
  const status = root.querySelector('[data-cin-status]');
  const poster = root.querySelector('.cin-poster');
  const base = new URL('../../assets/img/products/3d/cin/', import.meta.url);

  const manifestUrl = new URL('manifest.json', base);
  const manifest = await fetch(manifestUrl).then((r) => r.json());
  const count = manifest.count | 0;
  const fps = manifest.fps || 12;
  const images = [];

  // Preload frames
  await Promise.all(
    Array.from({ length: count }, (_, i) => {
      const n = String(i).padStart(2, '0');
      const url = new URL(`${manifest.prefix}${n}.${manifest.ext}`, base).href;
      return new Promise((resolve, reject) => {
        const img = new Image();
        img.onload = () => {
          images[i] = img;
          resolve();
        };
        img.onerror = reject;
        img.src = url;
      });
    }),
  );

  const ctx = canvas.getContext('2d', { alpha: false });
  function resize() {
    const w = root.clientWidth || 1;
    const h = Math.max(340, Math.round(w * (matchMedia('(max-width:700px)').matches ? 0.78 : 0.5)));
    root.style.setProperty('--cin-h', h + 'px');
    const dpr = Math.min(devicePixelRatio || 1, 2);
    canvas.width = Math.round(w * dpr);
    canvas.height = Math.round(h * dpr);
    canvas.style.width = w + 'px';
    canvas.style.height = h + 'px';
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    draw(clock.u);
  }

  function draw(u) {
    const w = canvas.clientWidth || root.clientWidth;
    const h = canvas.clientHeight || parseInt(getComputedStyle(root).getPropertyValue('--cin-h')) || 400;
    const idx = Math.min(count - 1, Math.max(0, Math.floor(u * count) % count));
    const img = images[idx];
    if (!img) return;
    ctx.fillStyle = '#05090b';
    ctx.fillRect(0, 0, w, h);
    // cover
    const ir = img.width / img.height;
    const cr = w / h;
    let dw, dh, dx, dy;
    if (ir > cr) {
      dh = h;
      dw = h * ir;
      dx = (w - dw) / 2;
      dy = 0;
    } else {
      dw = w;
      dh = w / ir;
      dx = 0;
      dy = (h - dh) / 2;
    }
    ctx.drawImage(img, dx, dy, dw, dh);
    if (bar) bar.style.transform = `scaleX(${(idx + 1) / count})`;
  }

  let playing = !!auto;
  let t0 = performance.now();
  let pausedAt = 0;
  const CYCLE = (count / fps) * 1000;
  const clock = { u: 0.42 }; // start near mid-orbit for first paint

  function setToggleLabel() {
    if (!toggle) return;
    toggle.hidden = false;
    const span = toggle.querySelector('span');
    const label = playing ? root.dataset.cinPause : root.dataset.cinResume;
    if (span) span.textContent = label || (playing ? 'Pause' : 'Resume');
    toggle.classList.toggle('is-paused', !playing);
  }
  setToggleLabel();
  if (toggle) {
    toggle.addEventListener('click', () => {
      playing = !playing;
      if (playing) t0 = performance.now() - pausedAt;
      else pausedAt = performance.now() - t0;
      setToggleLabel();
    });
  }

  resize();
  const ro = new ResizeObserver(resize);
  ro.observe(root);

  function frame(now) {
    requestAnimationFrame(frame);
    if (playing) clock.u = ((now - t0) % CYCLE) / CYCLE;
    draw(clock.u);
  }
  requestAnimationFrame(frame);

  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(
      (entries) => {
        for (const e of entries) {
          if (!e.isIntersecting && playing) {
            playing = false;
            pausedAt = performance.now() - t0;
            setToggleLabel();
          }
        }
      },
      { threshold: 0.05 },
    );
    io.observe(root);
  }

  if (status) status.hidden = true;
  if (poster) poster.style.display = 'none';
  return { canvas };
}
