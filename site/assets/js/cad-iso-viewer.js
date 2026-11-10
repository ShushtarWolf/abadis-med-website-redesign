/* Iso-only CAD line sketch. Same crease + silhouette style as cad-line-sketches.
   Loads on demand. No front/side/top/scale buttons. */
import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';

const ISO = [38, 24];
const META = {
  'p01-1l-liner': {accent:['lid','collar','cap'], dim:'Ø 11 cm × H 15.5 cm'},
  'p02-2l-liner': {accent:['lid','collar','cap'], dim:'Ø 11 cm × H 24.5 cm'},
  'p03-3l-liner': {accent:['lid','collar','cap'], dim:'Ø 11 cm × H 39 cm', pouches:true},
  'p12-inline-filter': {accent:['cartridge'], dim:'Ø 3.0 cm × L 7.2 cm', inline:true}
};

function pal() {
  const t = document.documentElement.dataset.theme;
  if (t === 'noir') return {bg:0x141222, ink:0xf1f0ff, teal:0xa78bfa, fill:0x1c1730, ring:0x2a2540, hid:.22};
  if (t === 'dark') return {bg:0x0a2425, ink:0xd7eeee, teal:0x5eead4, fill:0x0b3b3b, ring:0x1d4a4b, hid:.22};
  return {bg:0xffffff, ink:0x10292b, teal:0x04756f, fill:0xd7f4f4, ring:0xd5e7e7, hid:.24};
}

function edgeData(geo) {
  const pos = geo.attributes.position, idx = geo.index ? geo.index.array : [...Array(pos.count).keys()];
  const key = i => `${pos.getX(i).toFixed(3)},${pos.getY(i).toFixed(3)},${pos.getZ(i).toFixed(3)}`;
  const vid = new Map(), V = [], F = [];
  for (let i = 0; i < idx.length; i++) {
    const k = key(idx[i]);
    if (!vid.has(k)) { vid.set(k, V.length); V.push(new THREE.Vector3().fromBufferAttribute(pos, idx[i])); }
    F.push(vid.get(k));
  }
  const N = [], E = new Map();
  for (let f = 0; f < F.length / 3; f++) {
    const a = V[F[3 * f]], b = V[F[3 * f + 1]], c = V[F[3 * f + 2]];
    const n = new THREE.Vector3().subVectors(b, a).cross(new THREE.Vector3().subVectors(c, a));
    if (n.lengthSq() < 1e-12) { N.push(null); continue; }
    N.push(n.normalize());
    for (const [u, v] of [[0, 1], [1, 2], [2, 0]]) {
      const p = F[3 * f + u], q = F[3 * f + v], k = p < q ? p + '_' + q : q + '_' + p;
      (E.get(k) || E.set(k, []).get(k)).push(f);
    }
  }
  const crease = [], cand = [];
  for (const [k, fs] of E) {
    const [p, q] = k.split('_').map(Number);
    const ns = fs.map(f => N[f]).filter(Boolean);
    if (ns.length !== 2) { crease.push(p, q); continue; }
    if (ns[0].dot(ns[1]) < Math.cos(THREE.MathUtils.degToRad(28))) crease.push(p, q);
    else cand.push(p, q, ns[0], ns[1]);
  }
  return {V, cand, cg: new THREE.BufferGeometry().setFromPoints(crease.map(i => V[i]))};
}

function silhouette(ed, dir) {
  const pts = [];
  for (let i = 0; i < ed.cand.length; i += 4) {
    if (Math.sign(ed.cand[i + 2].dot(dir)) !== Math.sign(ed.cand[i + 3].dot(dir)))
      pts.push(ed.V[ed.cand[i]], ed.V[ed.cand[i + 1]]);
  }
  return pts;
}

function label(txt, col, bg) {
  const c = document.createElement('canvas'), x = c.getContext('2d');
  const f = '600 44px Inter, "Segoe UI", Roboto, Arial, sans-serif';
  x.font = f;
  const w = Math.ceil(x.measureText(txt).width) + 28;
  c.width = w; c.height = 64; x.font = f;
  x.fillStyle = bg; x.fillRect(0, 0, w, 64);
  x.fillStyle = col; x.textBaseline = 'middle'; x.textAlign = 'center'; x.fillText(txt, w / 2, 34);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace;
  const s = new THREE.Sprite(new THREE.SpriteMaterial({map: t, depthTest: false, transparent: true}));
  s.renderOrder = 9; s.userData.asp = w / 64; return s;
}

function addPouches(it) {
  const material = new THREE.LineDashedMaterial({color: pal().teal, dashSize: 2, gapSize: 1.2, transparent: true, opacity: .95, depthTest: false});
  it.illustrativeMaterial = material;
  const geo = new THREE.BoxGeometry(34, 7, 46, 10, 2, 12), p = geo.attributes.position;
  for (let i = 0; i < p.count; i++) {
    const x = p.getX(i) / 17, z = p.getZ(i) / 23;
    p.setY(i, p.getY(i) * Math.max(.12, (1 - x * x) * (1 - Math.pow(Math.max(0, z), 6))));
  }
  geo.computeVertexNormals();
  for (let i = 0; i < 3; i++) {
    const pouch = new THREE.Group();
    const body = new THREE.LineSegments(new THREE.EdgesGeometry(geo, 25), material);
    body.computeLineDistances(); body.renderOrder = 7; pouch.add(body);
    const seal = new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.BoxGeometry(34, 1, 6)), material);
    seal.computeLineDistances(); seal.position.z = 25.5; seal.renderOrder = 7; pouch.add(seal);
    pouch.rotation.y = i === 2 ? 1.57 : .6;
    const offset = i === 2 ? new THREE.Vector3(0, 7, -20) : new THREE.Vector3((i === 0 ? -1 : 1) * 19, 0, 0).applyEuler(pouch.rotation);
    pouch.position.copy(offset); pouch.position.y -= 409;
    it.scene.add(pouch);
  }
}

function buildDims(it) {
  const g = it.dimG, box = it.dimBox, meta = it.meta;
  while (g.children.length) g.remove(g.children[0]);
  const c = pal(), col = '#' + c.ink.toString(16).padStart(6, '0'), bg = '#' + c.bg.toString(16).padStart(6, '0');
  let vb = box;
  it.scene.traverse(o => { if (o.isMesh && (o.userData.part === 'vessel' || o.userData.part === 'bag' || o.userData.part === 'barrel')) vb = new THREE.Box3().setFromObject(o); });
  const cx = (vb.min.x + vb.max.x) / 2, cz = (vb.min.z + vb.max.z) / 2;
  const y0 = vb.min.y, y1 = it.id === 'p03-3l-liner' ? -24 : box.max.y;
  const parts = (meta.dim || '').split('×').map(s => s.trim());
  const dTxt = parts[0] || '', hTxt = parts[1] || '';
  const m = new THREE.LineBasicMaterial({color: c.ink, depthTest: false, transparent: true, opacity: .75});
  const L = (a, b) => { const l = new THREE.Line(new THREE.BufferGeometry().setFromPoints([a, b]), m); l.renderOrder = 8; g.add(l); };
  const V = (x, y, z) => new THREE.Vector3(x, y, z), ar = 4;
  if (meta.inline) {
    const xl = vb.min.x - 16, yt = box.max.y + 14;
    L(V(vb.min.x, yt, cz), V(vb.max.x, yt, cz));
    L(V(vb.min.x, vb.max.y + 3, cz), V(vb.min.x, yt + 6, cz));
    L(V(vb.max.x, vb.max.y + 3, cz), V(vb.max.x, yt + 6, cz));
    L(V(vb.min.x, yt, cz), V(vb.min.x + ar * 1.6, yt + ar * .6, cz));
    L(V(vb.min.x, yt, cz), V(vb.min.x + ar * 1.6, yt - ar * .6, cz));
    L(V(vb.max.x, yt, cz), V(vb.max.x - ar * 1.6, yt + ar * .6, cz));
    L(V(vb.max.x, yt, cz), V(vb.max.x - ar * 1.6, yt - ar * .6, cz));
    L(V(xl, vb.min.y, cz), V(xl, vb.max.y, cz));
    L(V(vb.min.x - 3, vb.min.y, cz), V(xl - 6, vb.min.y, cz));
    L(V(vb.min.x - 3, vb.max.y, cz), V(xl - 6, vb.max.y, cz));
    L(V(xl, vb.min.y, cz), V(xl - ar * .6, vb.min.y + ar * 1.6, cz));
    L(V(xl, vb.min.y, cz), V(xl + ar * .6, vb.min.y + ar * 1.6, cz));
    L(V(xl, vb.max.y, cz), V(xl - ar * .6, vb.max.y - ar * 1.6, cz));
    L(V(xl, vb.max.y, cz), V(xl + ar * .6, vb.max.y - ar * 1.6, cz));
    const s1 = label(hTxt || dTxt, col, bg), s2 = label(dTxt, col, bg), k = it.rad * .075;
    for (const s of [s1, s2]) s.scale.set(k * s.userData.asp, k, 1);
    s1.position.set(cx, yt + k * .8, cz);
    s2.position.set(xl - 6 - k * s2.userData.asp * .5, (vb.min.y + vb.max.y) / 2, cz);
    g.add(s1, s2);
    return;
  }
  const xl = vb.min.x - 24, yt = box.max.y + 18;
  L(V(xl, y0, cz), V(xl, y1, cz));
  L(V(vb.min.x - 3, y0, cz), V(xl - 6, y0, cz));
  L(V(vb.min.x - 3, y1, cz), V(xl - 6, y1, cz));
  L(V(xl, y0, cz), V(xl - ar * .6, y0 + ar * 1.6, cz));
  L(V(xl, y0, cz), V(xl + ar * .6, y0 + ar * 1.6, cz));
  L(V(xl, y1, cz), V(xl - ar * .6, y1 - ar * 1.6, cz));
  L(V(xl, y1, cz), V(xl + ar * .6, y1 - ar * 1.6, cz));
  L(V(vb.min.x, yt, cz), V(vb.max.x, yt, cz));
  L(V(vb.min.x, vb.max.y + 3, cz), V(vb.min.x, yt + 6, cz));
  L(V(vb.max.x, vb.max.y + 3, cz), V(vb.max.x, yt + 6, cz));
  L(V(vb.min.x, yt, cz), V(vb.min.x + ar * 1.6, yt + ar * .6, cz));
  L(V(vb.min.x, yt, cz), V(vb.min.x + ar * 1.6, yt - ar * .6, cz));
  L(V(vb.max.x, yt, cz), V(vb.max.x - ar * 1.6, yt + ar * .6, cz));
  L(V(vb.max.x, yt, cz), V(vb.max.x - ar * 1.6, yt - ar * .6, cz));
  const s1 = label(hTxt, col, bg), s2 = label(dTxt, col, bg), k = it.rad * .075;
  for (const s of [s1, s2]) s.scale.set(k * s.userData.asp, k, 1);
  s1.position.set(xl - 6 - k * s1.userData.asp * .5, (y0 + y1) / 2, cz);
  s2.position.set(cx, yt + k * .8, cz);
  g.add(s1, s2);
}

function applyTheme(it) {
  const c = pal(), M = it.mats;
  if (!M.fill) return;
  M.fill.color.set(c.bg); M.fillA.color.set(c.fill);
  M.ink.color.set(c.ink); M.teal.color.set(c.teal);
  M.inkH.color.set(c.ink); M.tealH.color.set(c.teal);
  M.inkH.opacity = M.tealH.opacity = c.hid;
  M.ring.color.set(c.ring);
  if (it.illustrativeMaterial) it.illustrativeMaterial.color.set(c.teal);
  if (it.dimG) buildDims(it);
  it.R.setClearColor(c.bg, 1);
  it.dirty = true;
}

function setIso(it) {
  const [az, el] = ISO;
  const a = THREE.MathUtils.degToRad(az), e = THREE.MathUtils.degToRad(el), d = it.rad * 4;
  it.cam.position.set(
    it.center.x + d * Math.sin(a) * Math.cos(e),
    it.center.y + d * Math.sin(e),
    it.center.z + d * Math.cos(a) * Math.cos(e)
  );
  it.cam.up.set(0, 1, 0);
  it.cam.zoom = 1;
  it.ctl.target.copy(it.center);
  resize(it);
  it.ctl.update();
  it.dirty = true;
}

function resize(it) {
  const w = it.host.clientWidth, h = it.host.clientHeight;
  if (!w || !h) return;
  it.R.setSize(w, h, false);
  const asp = w / h, r = (it.rad || 100) * 1.35;
  const hh = asp > 1 ? r : r / asp;
  it.cam.left = -hh * asp; it.cam.right = hh * asp; it.cam.top = hh; it.cam.bottom = -hh;
  it.cam.updateProjectionMatrix();
  it.dirty = true;
}

function frame(it) {
  if (it.dead) return;
  requestAnimationFrame(() => frame(it));
  if (!it.ready) return;
  it.ctl.update();
  if (!it.dirty) return;
  const dir = new THREE.Vector3();
  it.cam.getWorldDirection(dir);
  for (const pt of it.parts) {
    const ng = new THREE.BufferGeometry().setFromPoints(silhouette(pt.ed, dir));
    pt.sl.geometry.dispose();
    pt.sl.geometry = pt.slH.geometry = ng;
    pt.crH.visible = pt.slH.visible = true;
  }
  it.R.render(it.scene, it.cam);
  it.dirty = false;
}

function dispose(it) {
  it.dead = true;
  if (it.ro) it.ro.disconnect();
  if (it.onTheme) it.themeObs && it.themeObs.disconnect();
  it.ctl && it.ctl.dispose();
  it.R && it.R.dispose();
  if (it.R && it.R.domElement && it.R.domElement.parentNode)
    it.R.domElement.parentNode.removeChild(it.R.domElement);
}

function loadModel(it, id, url) {
  it.ready = false;
  it.id = id;
  it.meta = META[id] || {accent: [], dim: ''};
  it.parts = [];
  while (it.scene.children.length) it.scene.remove(it.scene.children[0]);
  new GLTFLoader().load(url, g => {
    if (it.dead || it.id !== id) return;
    g.scene.updateMatrixWorld(true);
    const box = new THREE.Box3().setFromObject(g.scene);
    it.box = box;
    const c = box.getCenter(new THREE.Vector3());
    it.center = c;
    it.rad = box.getBoundingSphere(new THREE.Sphere()).radius;
    const M = it.mats = {
      fill: new THREE.MeshBasicMaterial({polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1, side: THREE.DoubleSide}),
      fillA: new THREE.MeshBasicMaterial({polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1, side: THREE.DoubleSide}),
      ink: new THREE.LineBasicMaterial(),
      teal: new THREE.LineBasicMaterial(),
      inkH: new THREE.LineBasicMaterial({transparent: true, depthFunc: THREE.GreaterDepth, depthWrite: false}),
      tealH: new THREE.LineBasicMaterial({transparent: true, depthFunc: THREE.GreaterDepth, depthWrite: false}),
      ring: new THREE.LineBasicMaterial({transparent: true})
    };
    g.scene.traverse(o => {
      if (!o.isMesh) return;
      const geo = o.geometry.clone().applyMatrix4(o.matrixWorld);
      const acc = it.meta.accent.includes(o.name);
      const fm = new THREE.Mesh(geo, acc ? M.fillA : M.fill);
      fm.userData.part = o.name;
      it.scene.add(fm);
      const ed = edgeData(geo);
      const lm = acc ? M.teal : M.ink, hm = acc ? M.tealH : M.inkH;
      const cr = new THREE.LineSegments(ed.cg, lm), crH = new THREE.LineSegments(ed.cg, hm);
      const sg = new THREE.BufferGeometry();
      const sl = new THREE.LineSegments(sg, lm), slH = new THREE.LineSegments(sg, hm);
      [cr, crH, sl, slH].forEach(l => { l.frustumCulled = false; it.scene.add(l); });
      cr.renderOrder = sl.renderOrder = 2;
      crH.renderOrder = slH.renderOrder = 3;
      it.parts.push({ed, sl, crH, slH});
    });
    if (it.meta.pouches) addPouches(it);
    const sz = box.getSize(new THREE.Vector3());
    const rg = new THREE.Group();
    for (const r of [1.05, 1.45, 1.9]) {
      const pts = [];
      const R0 = Math.max(sz.x, sz.z) * .5 * r;
      for (let a = 0; a <= 96; a++) {
        const t = a / 96 * Math.PI * 2;
        pts.push(new THREE.Vector3(c.x + Math.cos(t) * R0, box.min.y, c.z + Math.sin(t) * R0));
      }
      rg.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts), M.ring));
    }
    it.scene.add(rg);
    it.dimG = new THREE.Group();
    it.scene.add(it.dimG);
    it.dimBox = box;
    applyTheme(it);
    setIso(it);
    it.ready = true;
    it.host.classList.add('is-live');
    it.dirty = true;
  }, undefined, () => {
    it.host.classList.remove('is-loading');
    it.host.classList.add('is-still-only');
  });
}

export function mount(host, {id, url}) {
  const R = new THREE.WebGLRenderer({antialias: true, alpha: false});
  R.setPixelRatio(Math.min(devicePixelRatio, 2));
  host.appendChild(R.domElement);
  R.domElement.style.width = '100%';
  R.domElement.style.height = '100%';
  R.domElement.style.touchAction = 'none';
  R.domElement.style.display = 'block';
  const scene = new THREE.Scene();
  const cam = new THREE.OrthographicCamera(-1, 1, 1, -1, -5000, 5000);
  const ctl = new OrbitControls(cam, R.domElement);
  ctl.enableDamping = true;
  ctl.enablePan = false;
  ctl.minZoom = .6;
  ctl.maxZoom = 6;
  const it = {host, R, scene, cam, ctl, parts: [], mats: {}, dirty: true, dead: false, ready: false};
  ctl.addEventListener('change', () => { it.dirty = true; });
  const stop = ev => ev.stopPropagation();
  R.domElement.addEventListener('pointerdown', stop);
  R.domElement.addEventListener('touchstart', stop, {passive: true});
  R.domElement.addEventListener('touchmove', ev => { ev.stopPropagation(); }, {passive: true});
  R.domElement.addEventListener('wheel', ev => ev.stopPropagation(), {passive: true});
  it.ro = new ResizeObserver(() => resize(it));
  it.ro.observe(host);
  it.themeObs = new MutationObserver(() => applyTheme(it));
  it.themeObs.observe(document.documentElement, {attributes: true, attributeFilter: ['data-theme']});
  loadModel(it, id, url);
  frame(it);
  it.setModel = (nid, nurl) => loadModel(it, nid, nurl);
  it.dispose = () => dispose(it);
  return it;
}

export function webglOk() {
  try {
    const c = document.createElement('canvas');
    return !!(window.WebGLRenderingContext && (c.getContext('webgl2') || c.getContext('webgl')));
  } catch (e) { return false; }
}
