/* generated from site/dial-practical/index.html inline script (ShushtarWolf) */


    /* Practical dial: no scroll-scrub. The dial turns by touch/mouse drag (or arrow keys), the LCD value is typed directly,
       presets are one-tap shortcuts. Formulas, odometers, formatting and ranges all come from abadis-common.js (Abadis.F / Abadis.IN). */
    (() => {
      const A = Abadis, fa = A.fa, clamp = A.clamp;
      const NS = 'http://www.w3.org/2000/svg';
      function ticksKnob(g) {
        for (let i = 0; i <= 40; i++) {
          const ang = (-150 + i * 7.5) * Math.PI / 180, major = i % 5 === 0;
          const r1 = 99, r2 = major ? 107 : 104;
          const l = document.createElementNS(NS, 'line');
          l.setAttribute('x1', 100 + r1 * Math.sin(ang)); l.setAttribute('y1', 100 - r1 * Math.cos(ang));
          l.setAttribute('x2', 100 + r2 * Math.sin(ang)); l.setAttribute('y2', 100 - r2 * Math.cos(ang));
          l.setAttribute('class', 'tick' + (major ? ' major' : '')); g.appendChild(l);
        }
      }
      function ticksGauge(g) {
        for (let i = 0; i <= 10; i++) {
          const ang = (-90 + i * 18) * Math.PI / 180, r1 = 60, r2 = i % 5 === 0 ? 66 : 63.5;
          const l = document.createElementNS(NS, 'line');
          l.setAttribute('x1', 66 + r1 * Math.sin(ang)); l.setAttribute('y1', 76 - r1 * Math.cos(ang));
          l.setAttribute('x2', 66 + r2 * Math.sin(ang)); l.setAttribute('y2', 76 - r2 * Math.cos(ang));
          l.setAttribute('class', 'g-tick'); g.appendChild(l);
        }
      }
      /* Persian (۰-۹), Arabic-Indic (٠-٩) and English digits; any separators / other characters are ignored */
      const DIGIT_RE = /[0-9\u06F0-\u06F9\u0660-\u0669]/;
      function parseNum(str) {
        const t = String(str || '')
          .replace(/[\u06F0-\u06F9]/g, (c) => String(c.charCodeAt(0) - 0x06F0))
          .replace(/[\u0660-\u0669]/g, (c) => String(c.charCodeAt(0) - 0x0660))
          .replace(/[^0-9]/g, '');
        return t ? Number(t.length > 9 ? '999999999' : t) : null;
      }

      const calcs = [];
      let raf = 0, last = performance.now();
      function tick(now) {
        raf = 0;
        const dt = Math.min(64, Math.max(0, now - last)); last = now;
        let busy = false;
        calcs.forEach((c) => { busy = c.update(dt) || busy; });
        if (busy) kick();
      }
      function kick() { if (!raf) { last = performance.now(); raf = requestAnimationFrame(tick); } }

      function setup(root, kind, render) {
        ticksKnob(root.querySelector('.knob-scale .ticks'));
        const keys = kind === 'surgery' ? ['n'] : ['a', 'b'];
        const odoList = [];
        root.querySelectorAll('[data-odo]').forEach((el) => odoList.push([el.dataset.odo, new A.Odo(el, +el.dataset.digits || 6)]));
        const chips = [...root.querySelectorAll('.chip')];
        const confirmBtn = root.querySelector('[data-confirm]');
        const wrap = root.querySelector('.knob-wrap'), knob = root.querySelector('.knob');
        const ins = {}; root.querySelectorAll('[data-in]').forEach((el) => { ins[el.dataset.in] = el; el.parentElement.classList.add('has-in'); });
        const val = {}, shown = {}, disp = {};
        keys.forEach((k) => { val[k] = 0; shown[k] = 0; disp[k] = -1; });
        const st = { phase: kind === 'surgery' ? 'n' : 'a', mode: '' };
        const active = () => (kind === 'surgery' ? 'n' : st.phase);
        let dirty = true, swingT = 0;

        function setVal(k, v, smooth) {
          val[k] = clamp(Math.round(v), 0, A.IN[k].max);
          if (!smooth) shown[k] = val[k];
          kick();
        }
        function setPhase(ph) {
          if (kind === 'surgery' || ph === st.phase) return;
          st.phase = ph; dirty = true;
          knob.classList.add('swing'); clearTimeout(swingT); swingT = setTimeout(() => knob.classList.remove('swing'), 380);
          kick();
        }

        const api = {
          root, kind, val, disp, st, setVal, setPhase,
          update(dt, force) {
            const k = A.reduced || force ? 1 : 1 - Math.exp(-dt / 110);
            let busy = false, changed = !!force || dirty; dirty = false;
            keys.forEach((key) => {
              const inp = A.IN[key];
              let s = shown[key] + (val[key] - shown[key]) * k;
              if (Math.abs(val[key] - s) < inp.step * 0.5) s = val[key]; else busy = true;
              shown[key] = s;
              /* while easing, show the original step grid; at rest show the exact (typed) value */
              const d = s === val[key] ? val[key] : clamp(Math.round(s / inp.step) * inp.step, 0, inp.max);
              if (d !== disp[key]) { disp[key] = d; changed = true; }
            });
            if (!changed) return busy;
            const out = kind === 'surgery' ? A.F.surgery(disp) : A.F.beds(disp);
            const W = Math.round(out.water), C = Math.round(out.cost), H = Math.round(out.hours);
            const vals = { n: disp.n, a: disp.a, b: disp.b, water: W, cost: C, hours: H };
            odoList.forEach(([key, o]) => { if (vals[key] != null) o.set(vals[key]); });
            const fr = kind === 'surgery'
              ? { water: disp.n / 15000, cost: disp.n / 15000, hours: disp.n / 15000, input: disp.n / 15000 }
              : { water: (disp.a * 254 + disp.b * 67) / (321 * 700), cost: (disp.a * 200 + disp.b * 50) / (250 * 700), hours: (disp.a * 254 + disp.b * 67) / (321 * 700), a: disp.a / 700, b: disp.b / 700 };
            chips.forEach((c) => c.classList.toggle('on', c.dataset.n != null ? +c.dataset.n === disp.n : (+c.dataset.a === disp.a && +c.dataset.b === disp.b)));
            if (confirmBtn) {
              st.mode = st.phase === 'a' ? (disp.a > 0 ? 'confirm' : '') : 'edit';
              confirmBtn.hidden = !st.mode; confirmBtn.dataset.mode = st.mode;
              if (st.mode === 'confirm') confirmBtn.textContent = 'ثبت ' + fa(disp.a) + ' تخت اتاق عمل و رفتن به مرحله ۲ ←';
              else if (st.mode === 'edit') confirmBtn.textContent = '↑ تغییر تعداد تخت اتاق عمل';
            }
            /* slider semantics for the knob */
            const ak = active(), ai = A.IN[ak];
            wrap.setAttribute('aria-valuemin', '0'); wrap.setAttribute('aria-valuemax', String(ai.max));
            wrap.setAttribute('aria-valuenow', String(val[ak])); wrap.setAttribute('aria-valuetext', fa(val[ak]));
            wrap.setAttribute('aria-label', kind === 'surgery' ? 'دایال تعداد عمل در سال' : (ak === 'a' ? 'دایال تعداد تخت اتاق عمل' : 'دایال تعداد تخت ICU|CCU'));
            keys.forEach((key) => { const el = ins[key]; if (el && document.activeElement !== el) el.value = fa(val[key]); });
            render({ disp, W, C, H, fr, phase: st.phase, api });
            return busy;
          },
        };

        /* drag to turn: rotate around the knob centre; 300° sweep = full range (same as the drawn scale) */
        let drag = null;
        function polar(e) {
          const r = wrap.getBoundingClientRect();
          const dx = e.clientX - (r.left + r.width / 2), dy = e.clientY - (r.top + r.height / 2);
          return { deg: Math.atan2(dx, -dy) * 180 / Math.PI, dist: Math.hypot(dx, dy), size: r.width };
        }
        function endDrag(e) {
          if (!drag || (e && e.pointerId !== drag.id)) return;
          try { wrap.releasePointerCapture(drag.id); } catch (err) {}
          drag = null; wrap.classList.remove('dragging');
        }
        wrap.addEventListener('pointerdown', (e) => {
          if (e.pointerType === 'mouse' && e.button !== 0) return;
          e.preventDefault();
          wrap.focus({ preventScroll: true });
          const p = polar(e), key = active();
          drag = { id: e.pointerId, last: p.deg, raw: val[key], key };
          try { wrap.setPointerCapture(e.pointerId); } catch (err) {}
          wrap.classList.add('dragging');
        });
        wrap.addEventListener('pointermove', (e) => {
          if (!drag || e.pointerId !== drag.id) return;
          e.preventDefault();
          const p = polar(e);
          if (p.dist < p.size * 0.08) { drag.last = p.deg; return; } /* too close to the centre: angle is unstable */
          let d = p.deg - drag.last;
          if (d > 180) d -= 360; else if (d < -180) d += 360;
          drag.last = p.deg;
          const inp = A.IN[drag.key];
          drag.raw = clamp(drag.raw + d / 300 * inp.max, 0, inp.max);
          const v = clamp(Math.round(drag.raw / inp.step) * inp.step, 0, inp.max);
          if (v !== val[drag.key]) setVal(drag.key, v, false);
        });
        ['pointerup', 'pointercancel', 'lostpointercapture'].forEach((ev) => wrap.addEventListener(ev, endDrag));
        wrap.addEventListener('touchmove', (e) => { if (drag) e.preventDefault(); }, { passive: false });
        /* keyboard on the focused knob */
        wrap.addEventListener('keydown', (e) => {
          const key = active(), inp = A.IN[key], v = val[key];
          let nv = null;
          if (e.key === 'ArrowUp' || e.key === 'ArrowRight') nv = Math.floor(v / inp.step) * inp.step + inp.step;
          else if (e.key === 'ArrowDown' || e.key === 'ArrowLeft') nv = Math.ceil(v / inp.step) * inp.step - inp.step;
          else if (e.key === 'PageUp') nv = Math.floor(v / inp.step) * inp.step + inp.step * 10;
          else if (e.key === 'PageDown') nv = Math.ceil(v / inp.step) * inp.step - inp.step * 10;
          else if (e.key === 'Home') nv = 0;
          else if (e.key === 'End') nv = inp.max;
          if (nv == null) return;
          e.preventDefault(); setVal(key, nv, true);
        });

        /* typed values: exact numbers, clamped to the original range */
        Object.keys(ins).forEach((key) => {
          const el = ins[key], cell = el.parentElement, max = A.IN[key].max;
          let before = 0;
          el.addEventListener('focus', () => {
            cell.classList.add('editing'); setPhase(key);
            before = val[key]; el.value = fa(val[key]);
            setTimeout(() => { if (document.activeElement === el) { try { el.select(); } catch (err) {} } }, 0);
          });
          el.addEventListener('input', () => {
            const raw = el.value;
            const caret = el.selectionStart == null ? raw.length : el.selectionStart;
            let digitsBefore = 0; for (const ch of raw.slice(0, caret)) if (DIGIT_RE.test(ch)) digitsBefore++;
            const n = parseNum(raw);
            if (n == null) { el.value = ''; return; } /* empty: keep the last value until something is typed */
            const v = clamp(n, 0, max);
            setVal(key, v, false);
            const txt = fa(v); el.value = txt;
            let pos = txt.length;
            if (v === n && String(n).length === raw.replace(/[^0-9\u06F0-\u06F9\u0660-\u0669]/g, '').length) {
              let cnt = 0; pos = 0;
              while (pos < txt.length && cnt < digitsBefore) { if (DIGIT_RE.test(txt[pos])) cnt++; pos++; }
            }
            try { el.setSelectionRange(pos, pos); } catch (err) {}
          });
          el.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') { e.preventDefault(); el.blur(); }
            else if (e.key === 'Escape') { setVal(key, before, false); el.value = fa(before); el.blur(); }
          });
          el.addEventListener('blur', () => {
            cell.classList.remove('editing');
            const n = parseNum(el.value);
            if (n != null) setVal(key, clamp(n, 0, max), false);
            el.value = fa(val[key]); dirty = true; kick();
          });
        });

        /* presets: one-tap shortcuts */
        chips.forEach((c) => c.addEventListener('click', () => {
          if (c.dataset.n != null) setVal('n', +c.dataset.n, true);
          else { setVal('a', +c.dataset.a, true); setVal('b', +c.dataset.b, true); setPhase('b'); }
        }));
        if (confirmBtn) confirmBtn.addEventListener('click', () => {
          if (confirmBtn.dataset.mode === 'confirm') setPhase('b');
          else if (confirmBtn.dataset.mode === 'edit') setPhase('a');
        });
        calcs.push(api);
        return api;
      }

      function view(root, kind) {
        const arc = root.querySelector('.knob-arc'), knob = root.querySelector('.knob');
        const gauges = {};
        root.querySelectorAll('[data-gauge]').forEach((m) => { ticksGauge(m.querySelector('.g-ticks')); gauges[m.dataset.gauge] = { arc: m.querySelector('.g-arc'), needle: m.querySelector('.g-needle') }; });
        const sub = {}; root.querySelectorAll('[data-sub]').forEach((e) => { sub[e.dataset.sub] = e; });
        const sum = root.querySelector('[data-sum]'), hint = root.querySelector('[data-hint]');
        const chA = root.querySelector('[data-ch="a"]'), chB = root.querySelector('[data-ch="b"]');
        return (s) => {
          const f = kind === 'surgery' ? s.fr.input : (s.phase === 'a' ? s.fr.a : s.fr.b);
          const ang = -150 + f * 300;
          knob.style.transform = 'rotate(' + ang.toFixed(2) + 'deg)';
          arc.setAttribute('stroke-dasharray', (f * 300).toFixed(2) + ' 360');
          ['water', 'cost', 'hours'].forEach((k) => {
            const g = gauges[k], v = Math.min(1, s.fr[k]);
            g.arc.setAttribute('stroke-dasharray', (v * 100).toFixed(2) + ' 100');
            g.needle.setAttribute('transform', 'rotate(' + (-90 + v * 180).toFixed(2) + ' 66 76)');
          });
          sub.tubs.innerHTML = s.W > 0 ? '≈ <b>' + fa(s.W / 200) + '</b> وان حمام ۲۰۰ لیتری (تقریبی)' : 'معادل وان حمام ۲۰۰ لیتری (تقریبی)';
          sub.read.innerHTML = s.C >= 1e6 ? '≈ <b>' + A.readableToman(s.C) + '</b>' : '&nbsp;';
          sub.shifts.innerHTML = s.H > 0 ? '≈ <b>' + fa(s.H / 8) + '</b> شیفت کاری ۸ ساعته' : 'معادل شیفت کاری ۸ ساعته';
          if (kind === 'surgery') {
            sum.innerHTML = s.disp.n > 0
              ? 'با <b>' + fa(s.disp.n) + '</b> عمل جراحی در سال: حدود <b>' + fa(s.W) + '</b> لیتر آب، <b>' + fa(s.C) + '</b> تومان هزینه شست‌وشو و ضدعفونی و <b>' + fa(s.H) + '</b> ساعت از زمان کادر درمان.<span class="sum-note">* محاسبات بر اساس فرمول‌های محاسبه‌گر فعلی آبادیس</span>'
              : 'دایال را با لمس یا ماوس بچرخانید یا تعداد عمل جراحی در سال را تایپ کنید.';
          } else {
            chA.classList.toggle('active', s.phase === 'a'); chB.classList.toggle('active', s.phase === 'b');
            chA.classList.toggle('held', s.phase === 'b'); chB.classList.toggle('idle', s.phase === 'a');
            hint.textContent = s.phase === 'a' ? 'مرحله ۱: تعداد تخت اتاق عمل را با چرخاندن دایال یا تایپ عدد تنظیم کنید' : 'مرحله ۲: تعداد تخت ICU|CCU را با چرخاندن دایال یا تایپ عدد تنظیم کنید';
            sum.innerHTML = (s.disp.a + s.disp.b) > 0
              ? 'با <b>' + fa(s.disp.a) + '</b> تخت اتاق عمل و <b>' + fa(s.disp.b) + '</b> تخت ICU|CCU: حدود <b>' + fa(s.W) + '</b> لیتر آب، <b>' + fa(s.C) + '</b> تومان هزینه شست‌وشو و ضدعفونی و <b>' + fa(s.H) + '</b> ساعت از زمان کادر درمان.<span class="sum-note">* محاسبات بر اساس فرمول‌های محاسبه‌گر فعلی آبادیس</span>'
              : 'دایال را با لمس یا ماوس بچرخانید یا تعداد تخت را تایپ کنید.';
          }
        };
      }

      const c1 = document.getElementById('calc1'), c2 = document.getElementById('calc2');
      setup(c1, 'surgery', view(c1, 'surgery'));
      setup(c2, 'beds', view(c2, 'beds'));
      window.DIAL_PRACTICAL = { calc1: calcs[0], calc2: calcs[1] };
      document.documentElement.classList.add('no-anim');
      calcs.forEach((c) => c.update(0, true));
      A.start();
    })();


  