/* Abadis 3D factory scrollytelling hero. Units: 1 = 1 m. Self-hosted three.js (no CDN). */
import * as THREE from './three.module.js';
import { OrbitControls } from './OrbitControls.js';

const root = document.querySelector('.f3d');
if (root) init(root);

function init(sec) {
  const cfg = JSON.parse(sec.querySelector('.f3d-cfg').textContent);
  const stage = sec.querySelector('.f3d-stage');
  const canvas = sec.querySelector('.f3d-gl');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const $ = (s) => sec.querySelector(s);
  let renderer;
  try { renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true }); }
  catch (e) { sec.classList.add('no-gl'); return; }
  renderer.setPixelRatio(Math.min(devicePixelRatio || 1, 1.75));
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(40, 1, 0.5, 900);

  /* ---------- geometry: every edge in one buffer, ordered for the draw-on ---------- */
  const P = [], O = [], TN = [];
  function edges(geo, x, y, z, tone = 0, ordBias = 0) {
    const e = new THREE.EdgesGeometry(geo, 20), p = e.attributes.position;
    for (let i = 0; i < p.count; i++) {
      const wx = p.getX(i) + x, wy = p.getY(i) + y, wz = p.getZ(i) + z;
      P.push(wx, wy, wz);
      O.push(Math.min(1, Math.max(0, 0.04 + 0.5 * (25 - wz) / 50 + 0.36 * (wy / 14) + 0.08 * ((wx + 20) / 40) + ordBias)));
      TN.push(tone);
    }
    geo.dispose(); e.dispose();
  }
  const B = (w, h, d) => new THREE.BoxGeometry(w, h, d);
  // box from min/max corners
  const box = (x0, y0, z0, x1, y1, z1, tone, bias) => edges(B(x1 - x0, y1 - y0, z1 - z0), (x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2, tone, bias);
  const cyl = (r, h, x, y, z, rotZ, tone, seg = 14) => { const g = new THREE.CylinderGeometry(r, r, h, seg); if (rotZ) g.rotateZ(Math.PI / 2); edges(g, x, y, z, tone); };

  // lot (40 x 50 = 2,000 m2) and south front wall on Golshan 19 alley
  box(-20, -0.3, -25, 20, 0, 25, 0, -0.2);
  box(-20, 0, 24.8, -18, 2.4, 25.2); box(-12, 0, 24.8, 12, 2.4, 25.2); box(18, 0, 24.8, 20, 2.4, 25.2);
  [-18, -12, 12, 18].forEach((x) => cyl(0.35, 3, x, 1.5, 25, false, 1, 8));                  // gate posts
  box(-20, 0, -25.2, 20, 2.4, -24.8); box(-20.2, 0, -25, -19.8, 2.4, 25); box(19.8, 0, -25, 20.2, 2.4, 25);
  // central 2-floor office (110 m2) with gardens
  box(-5.5, 0, 18, 5.5, 3.4, 23); box(-5.5, 3.4, 18, 5.5, 6.8, 23);
  for (let i = 0; i < 5; i++) { box(-4.6 + i * 2, 1.2, 22.95, -3.4 + i * 2, 2.6, 23.05, 1); box(-4.6 + i * 2, 4.6, 22.95, -3.4 + i * 2, 6, 23.05, 1); }
  box(-11, 0, 18.5, -6.5, 0.5, 23.5, 1); box(6.5, 0, 18.5, 11, 0.5, 23.5, 1);
  [[-9.8, 20], [-7.6, 22.4], [7.6, 20], [9.8, 22.4]].forEach(([x, z]) => { cyl(0.12, 1.4, x, 1.2, z, false, 1, 6); edges(new THREE.IcosahedronGeometry(0.9, 0), x, 2.4, z, 1); });

  // HALL 1 (injection) 13 x 36, x -19..-6, z -23..13
  box(-19, 0, 7, -6, 14, 13);                                   // entrance bay, 14 m high
  box(-18.6, 0, 9.8, -15.6, 4, 12.6, 1); box(-9.4, 0, 9.8, -6.4, 4, 12.6, 1);   // 2 electrical rooms
  box(-13.5, 0, 12.9, -11.5, 4.2, 13.1, 1);                     // bay door
  box(-19, 0, -23, -6, 10.5, 7);                                // main two-floor shell
  box(-19, 5, -23, -6, 5.3, 7, 0, 0.05);                        // upper floor slab
  box(-18.6, 0, 4.2, -14.6, 3, 7, 1); box(-10.4, 0, 4.2, -6.4, 3, 7, 1);       // locker rooms 1 & 2
  box(-13.5, 0, 6.9, -11.5, 3, 7.1, 1);                         // partition center door
  for (let i = 0; i < 6; i++) box(-19, 10.5, -23 + i * 5, -6, 11.3, -22.6 + i * 5, 0, 0.1);   // roof ribs
  // ground: 3 x 220 t injection (top row), 2 blow molders (bottom-left), 1 x 120 t (bottom-right)
  [-16.5, -12.5, -8.5].forEach((x) => { box(x - 1.1, 0, -21, x + 1.1, 2.2, -13, 1); box(x - 0.7, 2.2, -20.5, x + 0.7, 3.4, -18.6, 1); cyl(0.55, 1, x, 3.9, -19.6, false, 1, 10); box(x - 0.9, 0, -13, x + 0.9, 1.2, -11.6, 1); });
  [-3.5, 1.5].forEach((z) => { box(-18.2, 0, z - 1.6, -14.8, 3.4, z + 1.6, 1); cyl(0.5, 1.4, -16.5, 4.1, z, false, 1, 10); });
  box(-10.6, 0, -3, -7.4, 1.8, 2.6, 1); box(-10, 1.8, -2.4, -8, 2.8, -0.8, 1);
  // upper: 10 x 10 PU assembly with 3 table rows, 10 x 3 cartoning corridor, lift (right), WIP door (left, closed)
  box(-19, 5.3, -3, -9, 9.8, 7, 1, 0.05);
  [-1, 2, 5].forEach((z) => box(-17.8, 5.3, z - 0.5, -10.2, 6.2, z + 0.5, 1));
  box(-19, 5.3, -6, -9, 9.8, -3, 1, 0.05);                      // cartoning corridor
  box(-16.5, 5.3, -5.2, -11.5, 6.1, -3.8, 1);                   // carton conveyor
  box(-9, 0, -6, -6.2, 10.5, -3, 1);                            // goods lift shaft (right)
  box(-9.1, 5.3, -5.4, -8.9, 7.8, -3.6, 1);                     // lift door
  box(-19, 5.3, -23, -9, 9.8, -6, 0, 0.05);                     // WIP storage shell (interior never shown)
  box(-18.4, 5.3, -6.1, -16.4, 7.8, -5.9, 1);                   // WIP door (closed)
  // HALL 2: 10 x 36, x -5..5
  box(-5, 0, -23, 5, 10, 13);
  box(-5, 5, -23, 5, 5.3, -5, 0, 0.05);                         // upper floor over left wing
  for (let i = 0; i < 6; i++) box(-5, 10, -23 + i * 5, 5, 10.8, -22.6 + i * 5, 0, 0.1);
  box(-5, 0, -5, 5, 10, -1, 0, 0.02);                           // central corridor 10 x 4
  for (let s = 0; s < 8; s++) box(1.5, s * 0.62, -4.6 + s * 0.42, 4.6, s * 0.62 + 0.62, -4.18 + s * 0.42, 1);   // stairs
  box(-4, 0, -5.1, -2, 2.4, -4.9, 1); box(-4, 0, -1.1, -2, 2.4, -0.9, 1); box(-1, 0, 12.9, 1, 3, 13.1, 1);
  // left wing ground: 2 extruders + cleanroom box + lift
  [-2.6, 2.6].forEach((x) => { const g = new THREE.CylinderGeometry(0.45, 0.45, 9, 10); g.rotateX(Math.PI / 2); edges(g, x, 1.2, -16, 1); box(x - 0.7, 0, -21.5, x + 0.7, 1, -10.5, 1); edges(new THREE.ConeGeometry(0.9, 1.6, 8), x, 2.6, -20); box(x - 0.6, 0, -9.8, x + 0.6, 1.6, -8, 1); });
  box(-4.4, 0, -8.6, -1.2, 3, -5.6, 1);                         // ground cleanroom box
  box(2.2, 0, -8.4, 4.8, 10, -5.6, 1);                          // lift
  // upper: Class 100,000 cleanroom with 2 assembly lines
  box(-4.5, 5.3, -22.5, 4.5, 9.4, -5.6, 1, 0.05);
  [-2, 2].forEach((x) => { box(x - 0.6, 5.3, -20.5, x + 0.6, 6.2, -8, 1); for (let k = 0; k < 4; k++) box(x - 0.3, 6.2, -19 + k * 3, x + 0.3, 6.7, -18.4 + k * 3, 1); });
  // right wing: filter room (only demolding shown)
  box(-4.4, 0, 0.6, 4.4, 4.2, 12.4, 0, 0.03);
  box(-1.4, 0, 4, 1.4, 1.6, 6.8, 1);                            // mold base / press bed
  [-1.2, 1.2].forEach((x) => [4.2, 6.6].forEach((z) => cyl(0.1, 3.6, x, 1.6 + 1.8, z, false, 1, 6)));
  box(-1.4, 5, 4, 1.4, 5.4, 6.8, 1);                            // press crown
  box(1.8, 0, 7.6, 4, 1, 10.6, 1);                              // finished filter tray
  // HALL 3: finished goods 7 x 18, x 7..14, z -5..13
  box(7, 0, -5, 14, 7, 13);
  [8.2, 12.8].forEach((x) => { for (let z = -3.5; z < 11; z += 2.6) { box(x - 0.8, 0, z, x + 0.8, 4.8, z + 2.2, 1); [1.6, 3.2].forEach((y) => box(x - 0.8, y, z, x + 0.8, y + 0.1, z + 2.2, 1)); box(x - 0.6, 0.2, z + 0.3, x + 0.2, 1.2, z + 1.9, 1); } });
  box(13.9, 0, 9, 14.1, 4, 12.5, 1);                            // dispatch door toward right gate
  box(9.8, 0, 3, 11.2, 1.4, 5.2, 1); box(10.1, 1.4, 3.1, 10.9, 3.4, 3.3, 1);   // forklift
  for (let i = 0; i < 4; i++) box(14.6 + i * 0.1, 0, 14 + i * 2.5, 16.2 + i * 0.1, 0.05, 15.6 + i * 2.5, 1, -0.05);   // dispatch path

  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.Float32BufferAttribute(P, 3));
  geo.setAttribute('aOrd', new THREE.Float32BufferAttribute(O, 1));
  geo.setAttribute('aTone', new THREE.Float32BufferAttribute(TN, 1));
  const uniforms = { uProg: { value: 0 }, uBase: { value: new THREE.Color() }, uHi: { value: new THREE.Color() }, uCoral: { value: new THREE.Color('#ff7a59') } };
  const mat = new THREE.ShaderMaterial({
    uniforms, transparent: true,
    vertexShader: 'attribute float aOrd;attribute float aTone;varying float vO;varying float vT;void main(){vO=aOrd;vT=aTone;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}',
    fragmentShader: 'uniform float uProg;uniform vec3 uBase;uniform vec3 uHi;uniform vec3 uCoral;varying float vO;varying float vT;void main(){if(vO>uProg)discard;float fr=1.-smoothstep(0.,.06,uProg-vO);vec3 c=mix(uBase,uHi,vT);c=mix(c,uCoral,fr);gl_FragColor=vec4(c,1.);}',
  });
  scene.add(new THREE.LineSegments(geo, mat));

  // animated filter demolding: mold top half lifts, finished filter slides to the tray
  function partLines(build) {
    const g = build(), e = new THREE.EdgesGeometry(g, 20), n = e.attributes.position.count;
    e.setAttribute('aOrd', new THREE.Float32BufferAttribute(new Array(n).fill(0.55), 1));
    e.setAttribute('aTone', new THREE.Float32BufferAttribute(new Array(n).fill(1), 1));
    g.dispose(); return new THREE.LineSegments(e, mat);
  }
  const moldTop = partLines(() => B(2.8, 0.9, 2.8)); scene.add(moldTop);
  const filter = partLines(() => new THREE.CylinderGeometry(0.75, 0.75, 0.22, 20)); scene.add(filter);

  // fingerprint rings
  const ringMats = [];
  for (let r = 0; r < 10; r++) {
    const pts = [], R = 34 + r * 7 + (r % 2) * 1.4;
    for (let k = 0; k <= 180; k++) { const an = k / 180 * Math.PI * 2; pts.push(new THREE.Vector3(Math.cos(an) * R * 1.05, -0.35, Math.sin(an) * R * 0.9 + Math.sin(an * 3 + r) * 0.8)); }
    const m = new THREE.LineBasicMaterial({ color: 0x0e8c8c, transparent: true, opacity: 0.1 });
    scene.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts), m)); ringMats.push(m);
  }

  /* ---------- theme sync ---------- */
  function applyTheme() {
    const t = document.documentElement.dataset.theme || 'light';
    const dark = t !== 'light';
    uniforms.uBase.value.set(dark ? '#3fb3b3' : '#0a666b');
    uniforms.uHi.value.set(dark ? '#8ff0e6' : '#0e8c8c');
    ringMats.forEach((m) => m.color.set(dark ? '#4fd1d1' : '#0e8c8c'));
  }
  applyTheme();
  document.addEventListener('themechange', applyTheme);
  new MutationObserver(applyTheme).observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });

  /* ---------- stations ---------- */
  const V3 = (x, y, z) => new THREE.Vector3(x, y, z);
  const VIEWS = [
    { p: V3(-31, 12, 8), t: V3(-12.5, 1.5, -11) },
    { p: V3(-30, 17, 16), t: V3(-14, 6.5, -0.5) },
    { p: V3(13, 9, 21), t: V3(0, 1.5, 6.5) },
    { p: V3(19, 15, -2), t: V3(0, 4, -14) },
    { p: V3(26, 10, 26), t: V3(10.5, 2, 4) },
  ];
  const LBL = [V3(-12.5, 6, -17), V3(-14, 11.6, 2), V3(0, 11.2, 6.5), V3(0, 11.2, -14), V3(10.5, 8.2, 4), V3(0, 8.2, 20.5)];
  const smooth = (x) => { x = Math.min(1, Math.max(0, x)); return x * x * (3 - 2 * x); };
  const fmtStep = (i) => cfg.step.replace('{n}', cfg.nums[i]).replace('{t}', cfg.total);

  const controls = new OrbitControls(camera, canvas);
  controls.enabled = false; controls.enableDamping = true; controls.dampingFactor = 0.08;
  controls.maxDistance = 170; controls.minDistance = 6; controls.maxPolarAngle = Math.PI * 0.495;

  const intro = $('.f3d-intro'), panel = $('.f3d-panel'), pStep = $('.f3d-step'), pTitle = $('.f3d-title'), pText = $('.f3d-text');
  const dots = [...sec.querySelectorAll('.f3d-dots i')], bar = $('.f3d-prog i'), pillsNav = $('.f3d-pills');
  const pills = [...sec.querySelectorAll('.f3d-pill')], exBtn = $('.f3d-ex'), exLabel = exBtn.querySelector('span');
  const labelsEl = $('.f3d-labels');
  const lbls = cfg.labels.map((txt, i) => {
    const d = document.createElement('button'); d.type = 'button'; d.className = 'f3d-lbl'; d.textContent = txt; d.tabIndex = -1;
    d.addEventListener('click', () => { if (explore && i < 5) flyTo(i); }); labelsEl.appendChild(d); return d;
  });

  let sT = 0, sS = 0, explore = false, tween = null, lastIdx = -2, visible = true;
  function readScroll() {
    const r = sec.getBoundingClientRect(), m = r.height - innerHeight;
    sT = m > 0 ? Math.min(1, Math.max(0, -r.top / m)) : 0;
  }
  addEventListener('scroll', readScroll, { passive: true }); readScroll(); sS = sT;
  const stationScroll = (i) => { const m = sec.offsetHeight - innerHeight; return sec.getBoundingClientRect().top + scrollY + m * (0.25 + 0.15 * i + 0.1); };

  function setExplore(on) {
    explore = on;
    sec.classList.toggle('is-ex', on);
    document.documentElement.classList.toggle('f3d-lock', on);
    controls.enabled = on; exLabel.textContent = on ? cfg.back : cfg.explore;
    if (on) { controls.target.set(0, 3, -2); lbls.forEach((l) => (l.tabIndex = 0)); }
    else { lbls.forEach((l) => (l.tabIndex = -1)); readScroll(); }
  }
  exBtn.addEventListener('click', () => setExplore(!explore));
  $('.f3d-skip').addEventListener('click', () => { if (explore) setExplore(false); });
  pills.forEach((b) => b.addEventListener('click', () => {
    const i = +b.dataset.i;
    if (explore) flyTo(i); else scrollTo({ top: stationScroll(i), behavior: reduce ? 'auto' : 'smooth' });
  }));
  function flyTo(i) { tween = { t: 0, fp: camera.position.clone(), tp: VIEWS[i].p.clone(), ft: controls.target.clone(), tt: VIEWS[i].t.clone(), i }; }

  function resize() {
    const w = stage.clientWidth, h = stage.clientHeight; renderer.setSize(w, h, false);
    camera.aspect = w / h; camera.fov = w / h < 1 ? 60 : 40; camera.updateProjectionMatrix();
  }
  resize(); addEventListener('resize', resize);
  new IntersectionObserver((en) => { visible = en[0].isIntersecting; }).observe(sec);

  const pos = new THREE.Vector3(), look = new THREE.Vector3(), tmp = new THREE.Vector3();
  const clock = new THREE.Clock();
  function aerial(s, out, tgt) {
    const k = Math.min(1, s / 0.25), a = -0.75 + 0.9 * k, R = (camera.aspect < 1 ? 118 : 82) - 10 * k;
    out.set(Math.sin(a) * R, 52 - 8 * k, Math.cos(a) * R); tgt.set(0, camera.aspect < 1 ? -4 : 5 - 9 * (1 - k), 0);
  }
  function frame() {
    requestAnimationFrame(frame);
    if (!visible) return;
    const time = clock.getElapsedTime();
    sS += (sT - sS) * (reduce ? 1 : 0.1);
    const s = sS;
    const prog = (explore || reduce) ? 1.1 : Math.min(1.1, (s / 0.17) * 1.1);
    uniforms.uProg.value = prog;
    ringMats.forEach((m, i) => { m.opacity = 0.03 + 0.14 * Math.min(1, Math.max(0, prog - i * 0.06)); });

    // filter demolding loop (6 s)
    const c = reduce ? 0.8 : (time % 6) / 6, lift = smooth(c / 0.25) - smooth((c - 0.85) / 0.15);
    moldTop.position.set(0, 2.05 + lift * 1.6, 5.4);
    const out = smooth((c - 0.3) / 0.35), place = smooth((c - 0.65) / 0.15);
    filter.position.set(out * 2.9, 1.75 + Math.sin(out * Math.PI) * 1.6 * (1 - place) + lift * 0.2 * (1 - out) - place * 0.5, 5.4 + out * 3.7);
    filter.visible = c < 0.95 && c > 0.05;

    let idx = -1;
    if (!explore) {
      const t = (s - 0.25) / 0.15;
      if (t < 0) { aerial(s, pos, look); }
      else {
        idx = Math.min(4, Math.floor(t));
        const f = smooth((t - idx) / 0.45);
        const fromP = new THREE.Vector3(), fromT = new THREE.Vector3();
        if (idx === 0) aerial(0.25, fromP, fromT); else { fromP.copy(VIEWS[idx - 1].p); fromT.copy(VIEWS[idx - 1].t); }
        pos.lerpVectors(fromP, VIEWS[idx].p, f); look.lerpVectors(fromT, VIEWS[idx].t, f);
        if (camera.aspect < 1) pos.add(tmp.copy(pos).sub(look).multiplyScalar(0.45));
      }
      camera.position.copy(pos); camera.lookAt(look);
      intro.style.opacity = String(Math.max(0, 1 - Math.max(0, s - 0.2) / 0.05));
      intro.style.visibility = s > 0.25 ? 'hidden' : 'visible';
      bar.style.height = (s * 100) + '%';
      panel.classList.toggle('on', idx >= 0);
      pillsNav.classList.toggle('on', s > 0.22);
      if (idx !== lastIdx) {
        lastIdx = idx;
        if (idx >= 0) { pStep.textContent = fmtStep(idx); pTitle.textContent = cfg.stations[idx].n; pText.textContent = cfg.stations[idx].t; }
        dots.forEach((d, k) => (d.className = k <= idx ? 'a' : ''));
        pills.forEach((p, k) => p.classList.toggle('act', k === idx));
      }
    } else {
      if (tween) {
        tween.t = reduce ? 1 : Math.min(1, tween.t + 0.022); const e = smooth(tween.t);
        camera.position.lerpVectors(tween.fp, tween.tp, e); controls.target.lerpVectors(tween.ft, tween.tt, e);
        pills.forEach((p, k) => p.classList.toggle('act', k === tween.i));
        if (tween.t >= 1) tween = null;
      }
      controls.update(); pillsNav.classList.add('on');
    }
    const showL = explore || (s > 0.14);
    const w = stage.clientWidth, h = stage.clientHeight;
    lbls.forEach((l, i) => {
      tmp.copy(LBL[i]).project(camera);
      const vis = showL && tmp.z < 1 && Math.abs(tmp.x) < 1.05 && Math.abs(tmp.y) < 1.05 && (explore || idx < 0 || i === idx);
      l.classList.toggle('show', vis); l.classList.toggle('act', !explore && i === idx);
      if (vis) l.style.transform = `translate(${(tmp.x * 0.5 + 0.5) * w - l.offsetWidth / 2}px,${(-tmp.y * 0.5 + 0.5) * h - l.offsetHeight / 2}px)`;
    });
    renderer.render(scene, camera);
  }
  frame();
}
