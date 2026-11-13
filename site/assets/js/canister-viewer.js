/**
 * On-tap solid 3D viewer for one P05 canister or canister set. Genuine CAD,
 * official print, approved clear-PC material; photo-derived hose set on the
 * 0402102 / 0402103 sets. Orbit after load; theme-aware studio.
 */
import * as THREE from 'three';
import {RoomEnvironment} from 'three/addons/environments/RoomEnvironment.js';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
import {loadCanister, contactShadow} from './p05-canister-core.js?v=20261113a';

const tone = () => (document.documentElement.dataset.theme === 'light' ? 'light' : 'dark');

export function mount(host, {id, capture} = {}) {
  const mob = matchMedia('(max-width:700px),(pointer:coarse)').matches;
  const R = new THREE.WebGLRenderer({antialias: true, alpha: true, preserveDrawingBuffer: !!capture, powerPreference: 'high-performance'});
  R.setPixelRatio(capture ? 1 : Math.min(devicePixelRatio, mob ? 1.6 : 2));
  R.toneMapping = THREE.ACESFilmicToneMapping; R.toneMappingExposure = 1.08; R.outputColorSpace = THREE.SRGBColorSpace;
  host.appendChild(R.domElement);
  Object.assign(R.domElement.style, {position: 'absolute', inset: '0', width: '100%', height: '100%', display: 'block', touchAction: 'none'});
  const S = new THREE.Scene();
  const pm = new THREE.PMREMGenerator(R), env = new RoomEnvironment();
  S.environment = pm.fromScene(env, .04).texture; env.dispose(); pm.dispose();
  const lights = [[-260,340,320,0xfff4e9,3.0],[220,100,150,0xe8f6ff,1.9],[40,250,-310,0xc0e8f7,2.6]].map(([x, y, z, c, i]) => { const l = new THREE.DirectionalLight(c, i); l.position.set(x, y, z); S.add(l); return l; });
  const hemi = new THREE.HemisphereLight(0xf2f8ff, 0x27303a, .8); S.add(hemi);
  const shadow = contactShadow(300); S.add(shadow);
  const cam = new THREE.PerspectiveCamera(28, 1, 1, 4000);
  const ctl = new OrbitControls(cam, R.domElement);
  ctl.enableDamping = true; ctl.enablePan = false;
  const it = {host, R, S, cam, ctl, dead: false, group: null, id: null};
  const stop = ev => ev.stopPropagation();
  R.domElement.addEventListener('pointerdown', stop);
  R.domElement.addEventListener('touchstart', stop, {passive: true});
  R.domElement.addEventListener('wheel', stop, {passive: true});
  function applyTone() {
    const light = tone() === 'light';
    S.environmentIntensity = light ? .7 : 1.1;
    R.toneMappingExposure = light ? .86 : 1.08;
    hemi.groundColor.setHex(light ? 0x8aa3a6 : 0x27303a);
    shadow.material.opacity = light ? .55 : 1;
  }
  applyTone();
  function frameTo(b) {
    const c = b.getCenter(new THREE.Vector3()), sz = b.getSize(new THREE.Vector3());
    const asp = Math.max(.4, host.clientWidth / Math.max(1, host.clientHeight));
    const vfov = THREE.MathUtils.degToRad(cam.fov), hfov = 2 * Math.atan(Math.tan(vfov / 2) * asp);
    // Fit the box height and its widest plan extent, with a margin for the orbit start pose.
    const plan = Math.hypot(sz.x, sz.z) * .5, depth = Math.max(sz.x, sz.z) * .5;
    const d = Math.max(sz.y * .5 * 1.3 / Math.tan(vfov / 2), plan * 1.12 / Math.tan(hfov / 2)) + depth;
    const az = THREE.MathUtils.degToRad(-18), el = THREE.MathUtils.degToRad(14);
    ctl.target.copy(c);
    cam.position.set(c.x + d * Math.sin(az) * Math.cos(el), c.y + d * Math.sin(el), c.z + d * Math.cos(az) * Math.cos(el));
    cam.near = Math.max(1, d / 100); cam.far = d * 6; cam.updateProjectionMatrix();
    ctl.minDistance = d * .35; ctl.maxDistance = d * 1.8; ctl.update();
  }
  function load(nid) {
    it.id = nid;
    host.classList.add('is-loading');
    return loadCanister(R, nid, {tone: tone()}).then(r => {
      if (it.dead || it.id !== nid) return;
      if (it.group) S.remove(it.group);
      it.group = r.group; it.bounds = r.bounds; S.add(r.group);
      shadow.position.y = r.bounds.min.y - .7;
      shadow.position.x = (r.bounds.min.x + r.bounds.max.x) / 2; shadow.position.z = (r.bounds.min.z + r.bounds.max.z) / 2;
      shadow.scale.setScalar(Math.max(r.bounds.max.x - r.bounds.min.x, r.bounds.max.z - r.bounds.min.z) / 300 * 1.25 + .2);
      frameTo(r.bounds);
      host.classList.remove('is-loading'); host.classList.add('is-live');
      host.dataset.solidReady = nid;
    }).catch(() => { host.classList.remove('is-loading'); host.classList.add('is-still-only'); });
  }
  function resize() { const w = host.clientWidth, h = host.clientHeight; R.setSize(w, h, false); cam.aspect = w / Math.max(1, h); cam.updateProjectionMatrix(); if (it.bounds && !it.touched) frameTo(it.bounds); }
  ctl.addEventListener('start', () => { it.touched = true; });
  it.ro = new ResizeObserver(resize); it.ro.observe(host); resize();
  // Theme change: rebuild materials for the new tone (light / dark).
  it.themeObs = new MutationObserver(() => { applyTone(); if (it.id) load(it.id); });
  it.themeObs.observe(document.documentElement, {attributes: true, attributeFilter: ['data-theme']});
  (function loop() { if (it.dead) return; requestAnimationFrame(loop); ctl.update(); R.render(S, cam); })();
  load(id);
  it.setModel = nid => load(nid);
  it.dispose = () => { it.dead = true; it.ro.disconnect(); it.themeObs.disconnect(); ctl.dispose(); R.dispose(); R.domElement.remove(); };
  return it;
}
