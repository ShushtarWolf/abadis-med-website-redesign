/* Abadis Med redesign — shared behaviour.
   Theme toggle (light/dark/noir, persisted), transparent header, mobile menu,
   mosaic (square-grid) video, lightbox, scroll reveal, CSR background fade.
   Deliberately NO mousemove / hover-driven motion. */
(() => {
  const root = document.documentElement;
  const KEY = 'abadis-theme';
  const THEMES = ['light', 'dark', 'noir'];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- theme ----------
     One compact button (left corner of the header) cycles light → dark → noir.
     The new theme is revealed as a growing circle from the button (View
     Transitions API); browsers without it get a soft crossfade.
     Choice persists in localStorage; ?theme= in the URL still works. */
  const header = document.getElementById('header');
  const toggle = document.querySelector('.theme-toggle');
  const NAMES = { light: 'روشن', dark: 'تیره', noir: 'نوآر' };
  const nextOf = (t) => THEMES[(THEMES.indexOf(t) + 1) % THEMES.length];
  function setTheme(t, save) {
    if (!THEMES.includes(t)) t = 'light';
    root.dataset.theme = t;
    if (save) { try { localStorage.setItem(KEY, t); } catch (_) {} }
    if (toggle) {
      const label = 'حالت نمایش: ' + NAMES[t] + ' — تغییر به ' + NAMES[nextOf(t)];
      toggle.setAttribute('aria-label', label); toggle.title = label;
    }
    const meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.content = t === 'light' ? '#e8f3f3' : t === 'dark' ? '#061719' : '#0a0a12';
    document.dispatchEvent(new CustomEvent('themechange', { detail: t }));
  }
  setTheme(root.dataset.theme || 'light', false);
  if (toggle) toggle.addEventListener('click', () => {
    const next = nextOf(root.dataset.theme || 'light');
    toggle.classList.remove('spin'); void toggle.offsetWidth; toggle.classList.add('spin');
    if (reduce) { setTheme(next, true); return; }
    if (document.startViewTransition) {
      const r = toggle.getBoundingClientRect();
      const x = r.left + r.width / 2, y = r.top + r.height / 2;
      const end = Math.hypot(Math.max(x, innerWidth - x), Math.max(y, innerHeight - y));
      const vt = document.startViewTransition(() => { setTheme(next, true); tone(); });
      vt.ready.then(() => {
        root.animate({ clipPath: ['circle(0px at ' + x + 'px ' + y + 'px)', 'circle(' + end + 'px at ' + x + 'px ' + y + 'px)'] },
          { duration: 750, easing: 'cubic-bezier(.65,0,.35,1)', pseudoElement: '::view-transition-new(root)' });
      }).catch(() => {});
    } else {
      root.classList.add('theme-fade');
      setTheme(next, true);
      setTimeout(() => root.classList.remove('theme-fade'), 550);
    }
  });

  /* ---------- header ----------
     Transparent in every theme. `.scrolled` only fades in an untinted blur;
     `.on-light` (light theme only) switches the ink + logo to teal while the
     bar sits over light content, and back to white over dark bands. */
  const DARK = '.hero, .page-hero, .deep, .site-footer, .cta-band, .media-frame, .product-visual, [data-tone="dark"]';
  const zones = header ? [...header.querySelectorAll('.logo, .nav, .menu-btn, .theme-toggle, .lang-switch')] : [];
  const isLightAt = (x, y) => {
    const el = document.elementsFromPoint(x, y).find((n) => !header.contains(n));
    return !!el && !el.closest(DARK);
  };
  /* Each part of the bar (logo, menu, buttons) picks its own ink from what is
     directly underneath it, so nothing turns white-on-mint or teal-on-teal. */
  function tone() {
    if (!header) return;
    const light = (root.dataset.theme || 'light') === 'light';
    const mobileMenu = menuBtnVisible();
    zones.forEach((z) => {
      let on = false;
      if (light && !(z.classList.contains('nav') && mobileMenu)) {
        const r = z.getBoundingClientRect();
        if (r.width && r.height) {
          const y = r.top + r.height / 2;
          const xs = z.classList.contains('nav') ? [r.left + r.width * .15, r.left + r.width * .5, r.left + r.width * .85] : [r.left + r.width / 2];
          on = xs.filter((x) => isLightAt(x, y)).length * 2 > xs.length;
        }
      }
      z.classList.toggle('on-light', on);
    });
  }
  function menuBtnVisible() {
    const m = header && header.querySelector('.menu-btn');
    return !!m && getComputedStyle(m).display !== 'none';
  }
  if (header) {
    let ticking = false;
    const on = () => {
      if (ticking) return; ticking = true;
      requestAnimationFrame(() => { ticking = false; header.classList.toggle('scrolled', scrollY > 24); tone(); });
    };
    addEventListener('scroll', on, { passive: true });
    addEventListener('resize', on);
    document.addEventListener('themechange', on);
    addEventListener('load', on);
    on();
  }
  const menuBtn = document.querySelector('.menu-btn');
  if (menuBtn && header) {
    const setOpen = (open) => { header.classList.toggle('open', open); menuBtn.setAttribute('aria-expanded', String(open)); };
    menuBtn.addEventListener('click', () => setOpen(!header.classList.contains('open')));
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape') setOpen(false); });
    document.addEventListener('click', (e) => { if (!header.contains(e.target)) setOpen(false); });
  }

  /* ---------- scroll reveal ---------- */
  const rev = document.querySelectorAll('.reveal');
  if (reduce || !('IntersectionObserver' in window)) rev.forEach((e) => e.classList.add('in'));
  else {
    const io = new IntersectionObserver((en) => en.forEach((x) => {
      if (x.isIntersecting) { x.target.classList.add('in'); io.unobserve(x.target); }
    }), { rootMargin: '0px 0px -8% 0px' });
    rev.forEach((e) => io.observe(e));
  }

  /* ---------- mosaic video (مربع مربعی) ----------
     The <video> is decoded off-screen; every frame is sampled down to a
     grid (one pixel per tile) and redrawn as crisp square tiles with a
     thin gap. On load the tiles resolve from coarse to fine; while the
     hero scrolls away they grow coarse again. Scroll-driven only. */
  function mosaic(host) {
    const video = host.querySelector('video');
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d', { alpha: false });
    if (!ctx || !video) { host.classList.add('no-canvas'); return; }
    host.appendChild(canvas);
    const small = document.createElement('canvas');
    const sctx = small.getContext('2d');
    const poster = new Image();
    poster.src = video.getAttribute('poster') || '';
    const fine = Number(host.dataset.tile || 12);
    let W = 0, H = 0, dpr = 1, gap = '#062a2c', visible = true, t0 = performance.now();
    const patterns = new Map();

    function readGap() {
      gap = getComputedStyle(root).getPropertyValue('--mosaic-gap').trim() || '#062a2c';
      patterns.clear();
    }
    function size() {
      dpr = Math.min(devicePixelRatio || 1, 1.5);
      W = Math.round(host.clientWidth * dpr); H = Math.round(host.clientHeight * dpr);
      canvas.width = W; canvas.height = H;
    }
    function pattern(t) {
      const k = t;
      if (patterns.has(k)) return patterns.get(k);
      const p = document.createElement('canvas'); p.width = p.height = t;
      const g = p.getContext('2d');
      const gw = Math.max(1, Math.round(t * 0.1));
      g.fillStyle = gap; g.fillRect(0, 0, t, t); g.clearRect(0, 0, t - gw, t - gw);
      const pat = ctx.createPattern(p, 'repeat'); patterns.set(k, pat); return pat;
    }
    function tileNow() {
      const mobile = host.clientWidth < 700;
      const base = mobile ? Math.max(7, fine - 4) : fine;
      let intro = 1;
      if (!reduce) intro = Math.min(1, (performance.now() - t0) / 1800);
      const ease = 1 - Math.pow(1 - intro, 3);
      let tile = base + (base * 5) * (1 - ease);          // coarse → fine on load
      const r = host.getBoundingClientRect();
      const out = Math.min(1, Math.max(0, -r.top / Math.max(1, r.height)));
      if (!reduce) tile += base * 2.5 * out;                 // coarser as hero scrolls away
      return Math.max(4, Math.round(tile * dpr));
    }
    function draw() {
      const src = video.readyState >= 2 ? video : (poster.complete && poster.naturalWidth ? poster : null);
      if (!src || !W) return;
      const sw = src.videoWidth || src.naturalWidth, sh = src.videoHeight || src.naturalHeight;
      const t = tileNow();
      const cols = Math.ceil(W / t), rows = Math.ceil(H / t);
      // cover-crop source to canvas aspect
      const ca = (cols * t) / (rows * t), sa = sw / sh;
      let cx = 0, cy = 0, cw = sw, ch = sh;
      if (sa > ca) { cw = sh * ca; cx = (sw - cw) / 2; } else { ch = sw / ca; cy = (sh - ch) / 2; }
      if (small.width !== cols || small.height !== rows) { small.width = cols; small.height = rows; }
      sctx.drawImage(src, cx, cy, cw, ch, 0, 0, cols, rows);
      ctx.imageSmoothingEnabled = false;
      ctx.drawImage(small, 0, 0, cols, rows, 0, 0, cols * t, rows * t);
      ctx.fillStyle = pattern(t);
      ctx.fillRect(0, 0, W, H);
    }
    function loop() {
      if (visible) draw();
      requestAnimationFrame(loop);
    }
    readGap(); size();
    poster.addEventListener('load', draw); video.addEventListener('loadeddata', draw);
    addEventListener('resize', size);
    document.addEventListener('themechange', readGap);
    new IntersectionObserver((en) => {
      visible = en[0].isIntersecting;
      if (visible) video.play().catch(() => {}); else video.pause();
    }).observe(host);
    if (reduce) { video.removeAttribute('autoplay'); video.pause(); video.addEventListener('loadeddata', draw); poster.onload = draw; }
    else video.play().catch(() => {});
    loop();
  }
  document.querySelectorAll('.mosaic').forEach(mosaic);

  /* ---------- CSR background: fade in once the painting is decoded ---------- */
  const csr = document.querySelector('.csr-bg');
  if (csr) {
    const img = new Image();
    img.src = csr.dataset.src;
    const show = () => requestAnimationFrame(() => requestAnimationFrame(() => csr.classList.add('shown')));
    (img.decode ? img.decode() : Promise.reject()).then(show, () => { img.onload = show; if (img.complete) show(); });
  }

  /* ---------- lightbox (click / keyboard / swipe) ---------- */
  const lb = document.getElementById('lightbox');
  if (lb) {
    const img = lb.querySelector('img'), cap = lb.querySelector('figcaption'), cnt = lb.querySelector('.lb-count');
    let items = [], idx = 0, last = null;
    const fa = (n) => n.toLocaleString('fa-IR');
    const show = (i) => {
      idx = (i + items.length) % items.length;
      const a = items[idx], alt = (a.querySelector('img') || {}).alt || '';
      img.src = a.getAttribute('href'); img.alt = alt; cap.textContent = alt;
      cnt.textContent = fa(idx + 1) + ' / ' + fa(items.length);
    };
    const open = (a) => {
      items = [...document.querySelectorAll('[data-gallery="' + a.dataset.gallery + '"]')];
      last = document.activeElement; lb.hidden = false; lb.classList.add('open');
      document.body.classList.add('lb-lock'); show(items.indexOf(a)); lb.querySelector('.lb-close').focus();
    };
    const close = () => { lb.classList.remove('open'); lb.hidden = true; document.body.classList.remove('lb-lock'); if (last) last.focus(); };
    document.querySelectorAll('[data-gallery]').forEach((a) => a.addEventListener('click', (e) => { e.preventDefault(); open(a); }));
    lb.querySelector('.lb-close').addEventListener('click', close);
    lb.querySelector('.lb-prev').addEventListener('click', () => show(idx - 1));
    lb.querySelector('.lb-next').addEventListener('click', () => show(idx + 1));
    lb.addEventListener('click', (e) => { if (e.target === lb) close(); });
    document.addEventListener('keydown', (e) => {
      if (!lb.classList.contains('open')) return;
      if (e.key === 'Escape') close(); else if (e.key === 'ArrowRight') show(idx - 1); else if (e.key === 'ArrowLeft') show(idx + 1);
    });
    let sx = null, sy = 0;
    lb.addEventListener('touchstart', (e) => { sx = e.touches[0].clientX; sy = e.touches[0].clientY; }, { passive: true });
    lb.addEventListener('touchend', (e) => {
      if (sx == null) return;
      const dx = e.changedTouches[0].clientX - sx, dy = e.changedTouches[0].clientY - sy; sx = null;
      if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy) * 1.3) show(idx + (dx > 0 ? 1 : -1));
    });
  }

  /* ---------- forms: POST to configurable endpoint, mailto fallback ---------- */
  const formEndpoint = (document.querySelector('meta[name="abadis-form-endpoint"]')?.content || '').trim();
  const formMailtoDefault = (document.querySelector('meta[name="abadis-form-mailto"]')?.content || 'info@abadis-med.com').trim();
  document.querySelectorAll('.form-offline-hint').forEach((el) => { el.hidden = !!formEndpoint; });

  const asciiDigits = (s) => String(s ?? '').replace(/[۰-۹]/g, (d) => '۰۱۲۳۴۵۶۷۸۹'.indexOf(d))
    .replace(/[٠-٩]/g, (d) => '٠١٢٣٤٥٦٧٨٩'.indexOf(d));

  function formBodyLines(fd) {
    const lines = [];
    fd.forEach((v, k) => {
      if (k === '_gotcha' || k === 'form_name') return;
      if (typeof v === 'string' && !v.trim()) return;
      lines.push(k + ': ' + v);
    });
    return lines.join('\n');
  }

  function openMailto(form, fd) {
    const to = form.dataset.mailtoForm || formMailtoDefault;
    let subject = form.dataset.subject || 'درخواست از وب‌سایت';
    if (form.id === 'leadForm' && fd.get('topic')) subject += ' — ' + fd.get('topic');
    const body = form.id === 'leadForm'
      ? ['نام: ' + (fd.get('name') || ''), 'مرکز درمانی / شرکت: ' + (fd.get('org') || ''),
         'تلفن: ' + (fd.get('phone') || ''), 'موضوع: ' + (fd.get('topic') || ''), '', fd.get('msg') || ''].join('\n')
      : formBodyLines(fd);
    location.href = 'mailto:' + to + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
  }

  function setFormStatus(form, text, isError) {
    const s = form.querySelector('.form-status') || document.getElementById('formStatus');
    if (!s) return;
    s.textContent = text;
    s.classList.toggle('is-error', !!isError);
  }

  document.querySelectorAll('form[data-abadis-form], form#leadForm, form[data-mailto-form]').forEach((form) => {
    if (form.dataset.formBound) return;
    form.dataset.formBound = '1';
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      if (!form.reportValidity()) return;
      const btn = form.querySelector('[type="submit"]');
      const fd = new FormData(form);
      // honeypot: pretend success, do nothing
      if ((fd.get('_gotcha') || '').toString().trim()) {
        setFormStatus(form, 'پیام شما ثبت شد. به‌زودی با شما تماس می‌گیریم.', false);
        form.reset();
        return;
      }
      // normalize Persian/Arabic digits in tel-like fields
      ['phone', 'تلفن ثابت', 'تلفن همراه', 'شماره شناسنامه', 'تاریخ تولد'].forEach((k) => {
        if (fd.has(k)) fd.set(k, asciiDigits(fd.get(k)));
      });
      if (!fd.get('form_name')) fd.set('form_name', form.dataset.abadisForm || form.id || 'form');

      if (!formEndpoint) {
        openMailto(form, fd);
        setFormStatus(form, 'برنامهٔ ایمیل شما باز شد؛ پیام بعد از ارسال از همان‌جا به دست ما می‌رسد.', false);
        return;
      }

      if (btn) btn.disabled = true;
      setFormStatus(form, 'در حال ارسال…', false);
      try {
        const res = await fetch(formEndpoint, {
          method: 'POST',
          body: fd,
          headers: { Accept: 'application/json' },
        });
        if (!res.ok) throw new Error('HTTP ' + res.status);
        setFormStatus(form, 'پیام شما ثبت شد. به‌زودی با شما تماس می‌گیریم.', false);
        form.reset();
      } catch (err) {
        setFormStatus(form, 'ارسال از طریق سرور ممکن نشد؛ ایمیل آماده باز می‌شود.', true);
        openMailto(form, fd);
      } finally {
        if (btn) btn.disabled = false;
      }
    });
  });

  /* careers list fields: clone row */
  document.querySelectorAll('[data-list-add]').forEach((btn) => {
    btn.addEventListener('click', () => {
      const root = btn.closest('[data-list-field]');
      const rows = root && root.querySelector('.list-rows');
      const first = rows && rows.querySelector('.list-row');
      if (!first) return;
      const clone = first.cloneNode(true);
      clone.querySelectorAll('input').forEach((inp) => {
        inp.value = '';
        inp.removeAttribute('required');
        const base = inp.getAttribute('name') || '';
        const n = rows.querySelectorAll('.list-row').length + 1;
        inp.setAttribute('name', base.replace(/ \(\d+\)$/, '') + ' (' + n + ')');
      });
      rows.appendChild(clone);
    });
  });

  /* ---------- phase 2: paged lists + live search ---------- */
  const faNum = (n) => new Intl.NumberFormat('fa-IR').format(n);
  document.querySelectorAll('[data-paged]').forEach((grid) => {
    const step = parseInt(grid.dataset.paged, 10) || 12;
    let shown = step;
    const items = Array.from(grid.children);
    const input = document.querySelector('[data-filter="#' + grid.id + '"]');
    const count = document.querySelector('[data-count-for="#' + grid.id + '"]');
    const empty = grid.parentElement.querySelector('.empty-msg');
    const unit = count ? count.textContent.replace(/^[\d۰-۹٬,]+\s*/, '') : '';
    let btn = null;
    if (items.length > step) {
      const wrap = document.createElement('div'); wrap.className = 'more-wrap';
      btn = document.createElement('button'); btn.type = 'button'; btn.className = 'btn btn-ghost'; btn.textContent = 'نمایش بیشتر';
      wrap.appendChild(btn); grid.after(wrap);
      btn.addEventListener('click', () => { shown += step; apply(); });
    }
    const norm = (t) => (t || '').replace(/[\u200c\s]+/g, ' ').replace(/ي/g, 'ی').replace(/ك/g, 'ک').trim();
    function apply() {
      const q = input ? norm(input.value) : '';
      let n = 0, visible = 0;
      items.forEach((el) => {
        const hit = !q || norm(el.dataset.name || el.textContent).includes(q);
        if (!hit) { el.setAttribute('data-filter-hidden', ''); el.classList.remove('is-hidden'); return; }
        el.removeAttribute('data-filter-hidden'); n++;
        const hide = !q && n > shown;
        el.classList.toggle('is-hidden', hide);
        if (!hide) visible++;
      });
      if (btn) btn.parentElement.hidden = !!q || shown >= items.length;
      if (count) count.textContent = faNum(n) + ' ' + unit;
      if (empty) empty.hidden = n > 0;
    }
    if (input) input.addEventListener('input', apply);
    apply();
  });

  /* ---------- phase 2: dealers province filter ---------- */
  const chips = document.getElementById('provChips');
  if (chips) chips.addEventListener('click', (e) => {
    const b = e.target.closest('button[data-prov]');
    if (!b) return;
    const on = b.getAttribute('aria-pressed') !== 'true';
    chips.querySelectorAll('button[data-prov]').forEach((x) => x.setAttribute('aria-pressed', 'false'));
    b.setAttribute('aria-pressed', on ? 'true' : 'false');
    document.querySelectorAll('.prov-group').forEach((g) => { g.hidden = on && g.dataset.prov !== b.dataset.prov; });
    if (on) { const g = document.querySelector('.prov-group[data-prov="' + b.dataset.prov + '"]'); if (g) g.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
  });

  /* ---------- footer: accordions closed on mobile; forced open on desktop ---------- */
  const footMq = window.matchMedia('(max-width: 560px)');
  function syncFootAcc() {
    document.querySelectorAll('.site-footer .foot-acc').forEach((d) => {
      if (footMq.matches) {
        /* compact mobile: start collapsed (contact block stays outside details) */
        if (d.classList.contains('foot-nav') || d.classList.contains('foot-more') || d.classList.contains('foot-address')) {
          d.open = false;
        }
      } else {
        d.open = true;
      }
    });
  }
  syncFootAcc();
  if (footMq.addEventListener) footMq.addEventListener('change', syncFootAcc);
  else if (footMq.addListener) footMq.addListener(syncFootAcc);
  document.querySelectorAll('.site-footer .foot-acc').forEach((d) => {
    d.addEventListener('toggle', () => {
      if (!footMq.matches && !d.open) d.open = true;
    });
  });

  /* ---------- home customers logo carousel (infinite marquee; track-only) ---------- */
  document.querySelectorAll('[data-logo-carousel]').forEach((root) => {
    const track = root.querySelector('.logo-carousel-track');
    const prev = root.querySelector('.logo-carousel-prev');
    const next = root.querySelector('.logo-carousel-next');
    if (!track) return;

    const originals = [...track.querySelectorAll('.home-logo')];
    if (originals.length < 2) return;

    /* Build [clone][original][clone] inside a strip; move via transform (never window). */
    const strip = document.createElement('div');
    strip.className = 'logo-carousel-strip';
    const mkClone = () => originals.map((el) => {
      const c = el.cloneNode(true);
      c.setAttribute('aria-hidden', 'true');
      c.querySelectorAll('[id]').forEach((n) => n.removeAttribute('id'));
      return c;
    });
    mkClone().forEach((c) => strip.appendChild(c));
    originals.forEach((el) => strip.appendChild(el));
    mkClone().forEach((c) => strip.appendChild(c));
    track.replaceChildren(strip);

    const slides = [...strip.querySelectorAll('.home-logo')];
    const n = originals.length;
    const reduceMq = window.matchMedia('(prefers-reduced-motion: reduce)');
    const PX_PER_SEC = 28; /* slow linear marquee */

    /* Logical travel distance (unbounded). Displayed x = baseX + mod(offset, setW). */
    let offset = 0;
    let setW = 0;
    let baseX = 0;
    let inView = false;
    let hoverPaused = false;
    let interactPaused = false;
    let dragging = false;
    let raf = 0;
    let lastTs = 0;
    let resumeTimer = 0;
    let stepAnim = 0;

    function reduce() { return reduceMq.matches; }
    function canAutoplay() {
      return inView && !hoverPaused && !interactPaused && !dragging && !document.hidden && !reduce() && !stepAnim;
    }

    function modOffset() {
      if (!(setW > 0)) return 0;
      let d = offset % setW;
      if (d < 0) d += setW;
      /* Float edge: treat 0 and setW as the same seam */
      if (d < 0.05 || d > setW - 0.05) d = 0;
      return d;
    }
    function apply() {
      strip.style.transform = 'translate3d(' + (baseX + modOffset()) + 'px,0,0)';
    }
    function trackCenterX() {
      const r = track.getBoundingClientRect();
      return (r.left + r.right) / 2;
    }
    function markCenter() {
      const mid = trackCenterX();
      let best = null, bestAbs = Infinity;
      for (let i = 0; i < slides.length; i++) {
        const r = slides[i].getBoundingClientRect();
        const a = Math.abs((r.left + r.right) / 2 - mid);
        if (a < bestAbs) { bestAbs = a; best = slides[i]; }
      }
      for (let i = 0; i < slides.length; i++) {
        slides[i].classList.toggle('is-center', slides[i] === best);
      }
    }
    /** Measure one-set width and center the first logo of the middle set. */
    function layout() {
      const kept = modOffset();
      strip.style.transform = 'translate3d(0,0,0)';
      const a = slides[n].getBoundingClientRect();
      const b = slides[n * 2].getBoundingClientRect();
      setW = Math.abs(b.left - a.left);
      if (setW < 1) setW = 1;
      const mid = trackCenterX();
      const logoMid = (a.left + a.right) / 2;
      baseX = mid - logoMid;
      offset = kept; /* preserve phase across resize */
      apply();
      markCenter();
    }

    function scheduleResume(ms) {
      if (resumeTimer) window.clearTimeout(resumeTimer);
      interactPaused = true;
      resumeTimer = window.setTimeout(() => {
        resumeTimer = 0;
        interactPaused = false;
        lastTs = 0;
      }, ms);
    }

    function stepBy(dir) {
      /* dir +1 = marquee / reading direction (strip +X); -1 = opposite */
      if (!setW || stepAnim) return;
      scheduleResume(2200);
      const from = offset;
      const gap = parseFloat(getComputedStyle(strip).gap) || 28;
      const sample = slides[n];
      const step = (sample ? sample.getBoundingClientRect().width : 110) + gap;
      const to = from + dir * step;
      if (reduce()) {
        offset = to; apply(); markCenter();
        return;
      }
      const t0 = performance.now();
      const dur = 420;
      stepAnim = 1;
      function tickStep(now) {
        const t = Math.min(1, (now - t0) / dur);
        const e = 1 - Math.pow(1 - t, 3);
        offset = from + (to - from) * e;
        apply();
        markCenter();
        if (t < 1) requestAnimationFrame(tickStep);
        else { stepAnim = 0; lastTs = 0; }
      }
      requestAnimationFrame(tickStep);
    }

    function loop(ts) {
      raf = requestAnimationFrame(loop);
      if (!canAutoplay()) { lastTs = 0; markCenter(); return; }
      if (!lastTs) lastTs = ts;
      const dt = Math.min(64, ts - lastTs);
      lastTs = ts;
      /* RTL reading: advance through DOM order → positive translateX */
      offset += (PX_PER_SEC * dt) / 1000;
      apply();
      markCenter();
    }

    if (prev) prev.addEventListener('click', () => stepBy(-1));
    if (next) next.addEventListener('click', () => stepBy(1));

    root.addEventListener('mouseenter', () => { hoverPaused = true; lastTs = 0; });
    root.addEventListener('mouseleave', () => { hoverPaused = false; lastTs = 0; });

    /* Drag / swipe on the track (both directions); loop wraps both ways */
    let dragStartX = 0, dragOrigin = 0, dragPid = 0;
    track.addEventListener('pointerdown', (e) => {
      if (e.button != null && e.button !== 0) return;
      if (e.target.closest && e.target.closest('.logo-carousel-btn')) return;
      dragging = true;
      interactPaused = true;
      if (resumeTimer) { window.clearTimeout(resumeTimer); resumeTimer = 0; }
      dragStartX = e.clientX;
      dragOrigin = offset;
      dragPid = e.pointerId;
      try { track.setPointerCapture(e.pointerId); } catch (_) {}
      lastTs = 0;
    });
    track.addEventListener('pointermove', (e) => {
      if (!dragging || e.pointerId !== dragPid) return;
      offset = dragOrigin + (e.clientX - dragStartX);
      apply();
      markCenter();
    });
    function endDrag(e) {
      if (!dragging || (e && e.pointerId !== dragPid)) return;
      dragging = false;
      dragPid = 0;
      apply();
      markCenter();
      scheduleResume(1800);
    }
    track.addEventListener('pointerup', endDrag);
    track.addEventListener('pointercancel', endDrag);

    if ('IntersectionObserver' in window) {
      const io = new IntersectionObserver((entries) => {
        const e = entries[0];
        inView = !!(e && e.isIntersecting && e.intersectionRatio >= 0.2);
        lastTs = 0;
      }, { threshold: [0, 0.2, 0.5, 0.75] });
      io.observe(root);
    } else {
      inView = true;
    }

    document.addEventListener('visibilitychange', () => { lastTs = 0; });
    if (reduceMq.addEventListener) {
      reduceMq.addEventListener('change', () => { lastTs = 0; markCenter(); });
    }

    let resizeRaf = 0;
    window.addEventListener('resize', () => {
      if (resizeRaf) return;
      resizeRaf = requestAnimationFrame(() => { resizeRaf = 0; layout(); lastTs = 0; });
    }, { passive: true });

    layout();
    /* Second pass after fonts/images settle so the row stays filled both sides */
    requestAnimationFrame(() => {
      layout();
      raf = requestAnimationFrame(loop);
      /* One deferred remeasure; avoid fighting active drag/autoplay later */
      window.setTimeout(() => { if (!dragging) { layout(); lastTs = 0; } }, 400);
    });
  });
})();
