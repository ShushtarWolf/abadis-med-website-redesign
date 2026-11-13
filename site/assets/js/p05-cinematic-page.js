/**
 * Canister page hero: the approved P05 canister film (same lights, clear PC,
 * official print, polar camera, exp(-dt*3.2) damping), scoped to the hero
 * track. The vertical 1/2/3 L size switch on the page drives which genuine
 * canister plays (1 L 0402011, 2 L 0402012, 3 L 0402013).
 */
import * as THREE from 'three';
import {RoomEnvironment} from 'three/addons/environments/RoomEnvironment.js';
import {loadCanister, contactShadow} from './p05-canister-core.js?v=20261113a';

// Approved per-size film keyframes: [scroll, azimuth deg, elevation deg, distance, vertical focus]
const FILMS = {
  'p05-1l': {kf: [[0,-16,9,660,-68],[.16,-20,9,650,-68],[.30,-20,19,610,-110],[.36,-23,19,610,-110],[.48,-158,10,590,-110],[.54,-165,8,590,-110],[.72,-20,-3,610,-112],[.81,-16,-2,620,-112],[.93,-17,8,660,-70],[1,-16,9,660,-68]], mob: [660, 90]},
  'p05-2l': {kf: [[0,-16,9,1000,-107],[.16,-20,9,990,-107],[.30,-20,19,950,-155],[.36,-23,19,950,-155],[.48,-158,10,930,-145],[.54,-165,8,930,-145],[.72,-20,-3,960,-158],[.81,-16,-2,970,-158],[.93,-17,8,1000,-109],[1,-16,9,1000,-107]], mob: [980, 45]},
  'p05-3l': {kf: [[0,-16,9,1540,-166],[.16,-20,9,1525,-166],[.30,-20,19,1480,-241],[.36,-23,19,1480,-241],[.48,-158,10,1450,-225],[.54,-165,8,1450,-225],[.72,-20,-3,1490,-246],[.81,-16,-2,1505,-246],[.93,-17,8,1540,-169],[1,-16,9,1540,-166]], mob: [1510, 35]}
};
const SIZE_ID = {'1': 'p05-1l', '2': 'p05-2l', '3': 'p05-3l'};

export function mount(root) {
  const stillCapture = root.getAttribute('data-cin-capture') === 'still';
  const mob = stillCapture ? false : matchMedia('(max-width:700px),(pointer:coarse)').matches;
  const cv = root.querySelector('canvas'), stage = cv.parentElement;
  const R = new THREE.WebGLRenderer({canvas: cv, antialias: true, alpha: true, preserveDrawingBuffer: stillCapture, powerPreference: 'high-performance'});
  R.setPixelRatio(Math.min(devicePixelRatio, mob ? 1.75 : 2)); R.toneMapping = THREE.ACESFilmicToneMapping; R.toneMappingExposure = 1.12;
  const S = new THREE.Scene(), C = new THREE.PerspectiveCamera(mob ? 32 : 28, 1, 1, 2500);
  const bg = document.createElement('canvas'); bg.width = bg.height = 1024;
  const bx = bg.getContext('2d'), grad = bx.createRadialGradient(512, 440, 10, 512, 440, 730);
  grad.addColorStop(0, '#35434c'); grad.addColorStop(.55, '#19262f'); grad.addColorStop(1, '#091219');
  bx.fillStyle = grad; bx.fillRect(0, 0, 1024, 1024);
  const backdrop = new THREE.CanvasTexture(bg); backdrop.colorSpace = THREE.SRGBColorSpace; S.background = backdrop;
  const pm = new THREE.PMREMGenerator(R), env = new RoomEnvironment();
  S.environment = pm.fromScene(env, .04).texture; S.environmentIntensity = 1.1; env.dispose(); pm.dispose();
  for (const [x, y, z, color, intensity] of [[-260,340,320,0xfff4e9,3.4],[220,100,150,0xe8f6ff,2.1],[40,250,-310,0xc0e8f7,3.0]]) {
    const l = new THREE.DirectionalLight(color, intensity); l.position.set(x, y, z); S.add(l);
  }
  S.add(new THREE.HemisphereLight(0xf2f8ff, 0x27303a, .8));
  const shadow = contactShadow(270); S.add(shadow);
  const cache = {};
  let cur = null, film = FILMS['p05-1l'], want = 'p05-1l';
  function show(id) {
    want = id;
    const p = cache[id] || (cache[id] = loadCanister(R, id));
    p.then(r => {
      if (want !== id) return;
      if (cur) S.remove(cur);
      cur = r.group; S.add(cur); film = FILMS[id];
      shadow.position.y = -r.cfg.H - .7;
      root.dataset.cinSize = id;
      window.__cinCanister = {id, ready: true};
      if (!stillCapture) { root.classList.remove('is-still'); root.classList.add('is-playing'); }
      ensureLoop();
    }).catch(() => root.classList.add('is-still'));
  }
  const V3 = () => new THREE.Vector3(), cl = x => Math.min(1, Math.max(0, x));
  const ease = x => { x = cl(x); return x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; };
  const cp = V3(), ct = V3();
  function sample(t) {
    const KF = film.kf;
    let a = KF[0], b = KF.at(-1);
    for (let i = 0; i < KF.length - 1; i++) if (t >= KF[i][0] && t <= KF[i + 1][0]) { a = KF[i]; b = KF[i + 1]; break; }
    const k = ease((t - a[0]) / Math.max(.0001, b[0] - a[0])), mix = i => THREE.MathUtils.lerp(a[i], b[i], k);
    const az = THREE.MathUtils.degToRad(mix(1)), el = THREE.MathUtils.degToRad(mix(2));
    // Portrait: the approved mobile stand-off, widened a little so the caption band clears the base.
    const portrait = stage.clientHeight > stage.clientWidth;
    const d = mob ? Math.max(film.mob[0] + film.mob[1] * Math.pow(Math.sin(az), 2), mix(3) * 1.03) * (portrait ? 1.12 : 1) : mix(3);
    const fy = mix(4) - (portrait ? d * .07 : 0);
    ct.set(0, fy, -10 * Math.pow(Math.sin(az), 2));
    cp.set(Math.sin(az) * Math.cos(el), Math.sin(el), Math.cos(az) * Math.cos(el)).multiplyScalar(d).add(ct);
  }
  function resize() { R.setSize(stage.clientWidth, stage.clientHeight, false); C.aspect = stage.clientWidth / Math.max(1, stage.clientHeight); C.updateProjectionMatrix(); }
  new ResizeObserver(resize).observe(stage); resize();
  const qp = new URLSearchParams(location.search);
  const beats = [...root.querySelectorAll('.beat')].map(e => ({e, a: +e.dataset.a, b: +e.dataset.b}));
  const bar = root.querySelector('.cin-bar');
  let trackH = 1, trackTop = 0, onScreen = true, looping = false, T = 0, last = 0;
  const cinStage = root.querySelector('.cin-stage') || stage;
  function measure() { trackH = Math.max(1, root.offsetHeight - ((cinStage && cinStage.offsetHeight) || innerHeight)); trackTop = root.getBoundingClientRect().top + scrollY; }
  measure(); addEventListener('resize', () => requestAnimationFrame(measure), {passive: true});
  if ('IntersectionObserver' in window) new IntersectionObserver(es => { onScreen = es.some(e => e.isIntersecting); if (onScreen) ensureLoop(); }, {rootMargin: '80px 0px'}).observe(root);
  document.addEventListener('visibilitychange', () => { if (!document.hidden) ensureLoop(); });
  const prog = () => qp.has('t') ? cl(+qp.get('t')) : cl(Math.min(trackH, Math.max(0, scrollY - trackTop)) / trackH);
  function ensureLoop() { if (looping) return; looping = true; requestAnimationFrame(frame); }
  function frame(now) {
    if (!stillCapture && (!onScreen || document.hidden)) { looping = false; return; }
    requestAnimationFrame(frame);
    const dt = Math.min(.1, (now - (last || now)) / 1000); last = now;
    T += (prog() - T) * (qp.has('t') || stillCapture ? 1 : 1 - Math.exp(-dt * 3.2));
    beats.forEach(b => { const f = .028, o = Math.min(cl((T - b.a) / f), cl((b.b - T) / f)); b.e.style.opacity = o; b.e.style.transform = `translateY(${(1 - o) * 10}px)`; });
    if (bar) bar.style.width = (T * 100) + '%';
    sample(T);
    C.position.copy(cp); C.lookAt(ct);
    const dist = cp.distanceTo(ct); C.near = Math.max(1, dist * .01); C.far = dist + 1800; C.updateProjectionMatrix();
    R.render(S, C);
    if (cur && !window.__cin_frame) { window.__cin_frame = true; root.dispatchEvent(new CustomEvent('cin-frame', {bubbles: true})); }
  }
  // The page's vertical size switch drives the film.
  function selectedSize() {
    const b = document.querySelector('.size-pick-btn[aria-selected="true"]');
    return (b && b.getAttribute('data-size')) || '1';
  }
  const pick = document.querySelector('.size-pick');
  if (pick && 'MutationObserver' in window) {
    new MutationObserver(() => { const id = SIZE_ID[selectedSize()]; if (id !== want) show(id); }).observe(pick, {subtree: true, attributes: true, attributeFilter: ['aria-selected']});
  }
  show(SIZE_ID[qp.get('size')] || SIZE_ID[selectedSize()] || 'p05-1l');
  if (stillCapture) root.classList.add('is-still');
  ensureLoop();
  return {show};
}
