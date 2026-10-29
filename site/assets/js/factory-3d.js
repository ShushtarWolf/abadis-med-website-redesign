/* Abadis 3D factory scrollytelling hero — Option 2 (Unified Top Interactive Dock) + Option 3 (3D Machine Sub-Nodes).
 * Units: 1 = 1 m. Self-hosted three.js (no CDN).
 */
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

  /* ---------- geometry: every edge in one buffer, with aSub for machine highlighting ---------- */
  const P = [], O = [], TN = [], SUB = [];
  function edges(geo, x, y, z, tone = 0, ordBias = 0, subId = 0) {
    const e = new THREE.EdgesGeometry(geo, 20), p = e.attributes.position;
    for (let i = 0; i < p.count; i++) {
      const wx = p.getX(i) + x, wy = p.getY(i) + y, wz = p.getZ(i) + z;
      P.push(wx, wy, wz);
      O.push(Math.min(1, Math.max(0, 0.04 + 0.5 * (25 - wz) / 50 + 0.36 * (wy / 14) + 0.08 * ((wx + 20) / 40) + ordBias)));
      TN.push(tone);
      SUB.push(subId);
    }
    geo.dispose(); e.dispose();
  }
  const B = (w, h, d) => new THREE.BoxGeometry(w, h, d);
  const box = (x0, y0, z0, x1, y1, z1, tone = 0, bias = 0, subId = 0) =>
    edges(B(x1 - x0, y1 - y0, z1 - z0), (x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2, tone, bias, subId);
  const cyl = (r, h, x, y, z, rotZ, tone = 0, seg = 14, subId = 0) => {
    const g = new THREE.CylinderGeometry(r, r, h, seg);
    if (rotZ) g.rotateZ(Math.PI / 2);
    edges(g, x, y, z, tone, 0, subId);
  };

  // Lot 40 x 50 = 2,000 m². South wall is Golshan 19; gates sit in the side yards.
  // Shell from abadis-factory.dwg (AC1032, Mohsen). Drawing units are metres;
  // dimension text is centimetres. One connected shed, not three separated halls:
  //   13.00 | 10.00 | 8.50  = 31.50 m wide (dims 1300 / 1000 / 850)
  //   36.00 m deep on every bay (dim 3600), grid from the north:
  //   5.80, 6.00, 6.05, 6.05, 6.05, 6.05
  // Twin column lines sit 0.80 m apart on the two party walls (grid bubbles E/D and C/B).
  const xW = -15.75, xA = -2.75, xB = 7.25, xE = 15.75;
  const zN = -22, zS = 14;
  const ZG = [0, 5.8, 11.8, 17.85, 23.9, 29.95, 36].map((d) => +(zN + d).toFixed(2));
  const zCut = zN + 18; // hall 2 partition, dim 1800: north extruder, south filter
  const zWip = zN + 20; // hall 1 upper WIP is exactly 13 x 20; interior stays closed
  box(-20, -0.3, -25, 20, 0, 25, 0, -0.2, 0);
  box(-20, 0, 24.8, -18, 2.4, 25.2); box(-14, 0, 24.8, 14, 2.4, 25.2); box(18, 0, 24.8, 20, 2.4, 25.2);
  [-18, -14, 14, 18].forEach((x) => cyl(0.35, 3, x, 1.5, 25, false, 1, 8));
  box(-20, 0, -25.2, 20, 2.4, -24.8); box(-20.2, 0, -25, -19.8, 2.4, 25); box(19.8, 0, -25, 20.2, 2.4, 25);
  // Golshan 19 Alley: two-lane street along the south wall (as in the sample), dashed centre line, kerbs, sidewalk
  box(-34, -0.32, 26.2, 34, -0.02, 34.2, 0, -0.25, 0);
  box(-34, 0, 25.4, 34, 0.15, 26.2, 0, -0.22, 0); box(-34, 0, 34.2, 34, 0.15, 35.0, 0, -0.22, 0);
  for (let x = -33; x < 33; x += 4) box(x, -0.02, 30.1, x + 2.2, 0.0, 30.3, 1, -0.2, 0);
  [-24, 24].forEach((x) => { cyl(0.08, 5, x, 2.5, 25.8, false, 1, 6); box(x - 0.1, 4.9, 25.8, x + 0.1, 5, 27.2, 1); });
  // Central 2-floor office, 11 x 5 m footprint, 110 m² total, in front of the sheds
  box(-5.5, 0, 15, 5.5, 3.4, 20); box(-5.5, 3.4, 15, 5.5, 6.8, 20);
  for (let i = 0; i < 5; i++) { box(-4.6 + i * 2, 1.2, 19.95, -3.4 + i * 2, 2.6, 20.05, 1); box(-4.6 + i * 2, 4.6, 19.95, -3.4 + i * 2, 6, 20.05, 1); }
  box(-12.2, 0, 15.3, -6.2, 0.45, 20.4, 1); box(6.2, 0, 15.3, 12.2, 0.45, 20.4, 1);
  [[-10.6, 16.2], [-7.4, 19.2], [7.4, 16.2], [10.6, 19.2]].forEach(([x, z]) => { cyl(0.12, 1.4, x, 1.2, z, false, 1, 6); edges(new THREE.IcosahedronGeometry(0.9, 0), x, 2.4, z, 1); });

  const roof = (x0, x1, y, z, h) => box(x0, y, z - 0.12, x1, y + h, z + 0.12, 0, 0.08);
  const colH = (x) => (x < xA - 0.1 ? 10.6 : x < xB - 0.1 ? 10.5 : 8.6);
  [xW, xA - 0.4, xA + 0.4, xB - 0.4, xB + 0.4, xE].forEach((x) => {
    ZG.forEach((z) => box(x - 0.16, 0, z - 0.16, x + 0.16, colH(x), z + 0.16, 0, -0.02));
  });

  // HALL 1 (Injection) 13 x 36, xW..xA. Mezzanine stops 3 m short of the south lobby.
  box(xW, 0, zN, xA, 10.6, zS);
  box(xW, 5.15, zN, xA, 5.4, zS - 3, 0, 0.04);
  ZG.forEach((z) => roof(xW, xA, 10.6, z, 0.55));
  // South doors, one per bay, on the street side
  [[(xW + xA) / 2, 10.6], [(xA + xB) / 2, 10.5], [(xB + xE) / 2, 8.6]].forEach(([cx, h]) => {
    box(cx - 1.7, 0, zS - 0.06, cx - 1.45, Math.min(3.4, h * 0.42), zS + 0.08, 1);
    box(cx + 1.45, 0, zS - 0.06, cx + 1.7, Math.min(3.4, h * 0.42), zS + 0.08, 1);
  });
  // Ground-floor locker rooms at the south of hall 1 (DWG plan B: 4.50 + 2.50 + 6.00 m, 2.00 m deep)
  box(-15.55, 0, 6.05, -11.35, 2.7, 7.95, 1);
  box(-11.15, 0, 6.05, -8.85, 2.7, 7.95, 1);
  box(-8.65, 0, 6.05, -2.95, 2.7, 7.95, 1);
  box(-15.65, 0, -21.85, -14.6, 5.2, -20.55, 1);

  // Machine builders: wireframe silhouettes after the Chen Hsong presses and PBM line in the factory videos.
  const lineY = (x0, z0, x1, z1) => box(x0, 0.005, z0, x1, 0.03, z1, 0, -0.1, 0); // yellow floor safety line
  const person = (x, z, rot = 0, sub = 0, s = 1) => {
    const c = Math.cos(rot), sn = Math.sin(rot), o = (dx, dz) => [x + dx * c - dz * sn, z + dx * sn + dz * c];
    [-0.11, 0.11].forEach((d) => { const [px, pz] = o(d, 0); box(px - 0.07 * s, 0, pz - 0.08 * s, px + 0.07 * s, 0.85 * s, pz + 0.08 * s, 1, 0.05, sub); });
    box(x - 0.2 * s, 0.85 * s, z - 0.2 * s, x + 0.2 * s, 1.45 * s, z + 0.2 * s, 1, 0.05, sub);
    [-0.27, 0.27].forEach((d) => { const [px, pz] = o(d, 0.12); box(px - 0.05 * s, 0.95 * s, pz - 0.05 * s, px + 0.05 * s, 1.4 * s, pz + 0.05 * s, 1, 0.05, sub); });
    edges(new THREE.IcosahedronGeometry(0.13 * s, 1), x, 1.62 * s, z, 1, 0.05, sub);
  };
  const crate = (x, z, w = 0.6, d = 0.45, h = 0.4, n = 2, sub = 0) => {
    for (let k = 0; k < n; k++) box(x - w / 2, k * h, z - d / 2, x + w / 2, (k + 1) * h - 0.03, z + d / 2, 1, 0.02, sub);
  };
  // Injection press along +z: injection unit (north) -> clamp unit (south)
  const press = (x, z0, z1, w, hb, sub) => {
    const L = z1 - z0, zc = z0 + L * 0.42; // boundary between injection and clamp units
    box(x - w / 2, 0, z0, x + w / 2, hb * 0.45, z1, 1, 0, sub); // machine base
    // injection unit: carriage, barrel, nozzle, hopper + dryer tube
    box(x - w * 0.3, hb * 0.45, z0 + 0.15, x + w * 0.3, hb * 0.7, zc - 0.1, 1, 0, sub);
    const br = new THREE.CylinderGeometry(w * 0.11, w * 0.11, (zc - z0) * 0.9, 10); br.rotateX(Math.PI / 2);
    edges(br, x, hb * 0.82, z0 + (zc - z0) * 0.5, 1, 0, sub);
    const hz = z0 + (zc - z0) * 0.3;
    edges(new THREE.CylinderGeometry(w * 0.28, w * 0.1, hb * 0.35, 10), x, hb * 1.15, hz, 1, 0, sub);
    cyl(w * 0.2, hb * 0.35, x, hb * 1.5, hz, false, 1, 10, sub);
    cyl(0.05, hb * 0.6, x + w * 0.3, hb * 1.25, hz, false, 1, 6, sub); // dryer feed tube
    // clamp unit: fixed + moving platen, rear platen, 4 tie bars, safety guard with window frames
    const pH = hb * 1.05;
    [zc + 0.05, zc + (z1 - zc) * 0.45, z1 - 0.25].forEach((pz) => box(x - w * 0.42, hb * 0.45, pz - 0.12, x + w * 0.42, hb * 0.45 + pH, pz + 0.12, 1, 0, sub));
    [-1, 1].forEach((sx) => [-1, 1].forEach((sy) => {
      const g = new THREE.CylinderGeometry(0.045, 0.045, z1 - zc - 0.3, 6); g.rotateX(Math.PI / 2);
      edges(g, x + sx * w * 0.32, hb * 0.45 + pH * (0.5 + sy * 0.38), (zc + z1) / 2 - 0.1, 1, 0, sub);
    }));
    box(x - w / 2 - 0.02, hb * 0.45, zc + 0.3, x + w / 2 + 0.02, hb * 0.45 + pH * 0.95, z1 - 0.5, 0, 0.02, sub);
    // control cabinet + operator screen on the walkway side, stack light on top
    box(x + w / 2, 0.6, zc - 0.3, x + w / 2 + 0.12, 1.5, zc + 0.35, 1, 0, sub);
    box(x + w / 2 + 0.12, 1.1, zc - 0.15, x + w / 2 + 0.16, 1.45, zc + 0.2, 1, 0, sub);
    [0, 1, 2].forEach((k) => cyl(0.07, 0.12, x + w * 0.35, hb * 0.45 + pH + 0.1 + k * 0.13, zc + 0.05, false, 1, 8, sub));
    lineY(x - w / 2 - 0.5, z0 - 0.4, x - w / 2 - 0.45, z1 + 0.4);
    lineY(x + w / 2 + 0.75, z0 - 0.4, x + w / 2 + 0.8, z1 + 0.4);
  };
  // Subnode 11: 4 x 220t injection presses (EM220-V proportions) across the north of the ground hall
  [-14.15, -11.15, -8.15, -5.15].forEach((x) => {
    press(x, -20.35, -13.6, 1.75, 2.3, 11);
    crate(x - 0.3, -12.9, 0.7, 0.5, 0.42, 2, 11); crate(x + 0.5, -12.9, 0.5, 0.5, 0.42, 1, 11);
  });
  // Subnode 12: 6 x 120t presses (EM120 proportions), two rows of three filling the middle of the hall
  [-9.7, -4.2].forEach((z) => [-14.05, -9.25, -4.45].forEach((x) => {
    press(x, z - 2.2, z + 1.9, 1.5, 1.85, 12);
    crate(x - 1.2, z + 1.6, 0.5, 0.45, 0.38, 2, 12);
  }));
  person(-10.2, -16.0, Math.PI / 2, 11); person(-4.1, -17.2, Math.PI / 2, 11);
  person(-13.0, -9.0, Math.PI / 2, 12); person(-3.4, -3.5, -Math.PI / 2, 12);

  // Subnode 21: upper 10 x 10 PU assembly, the 10 m zone south of the WIP (DWG plan C)
  box(-14.25, 5.4, -2, -4.25, 9.9, 8, 1, 0.05, 21);
  [-0.2, 2.6, 5.4].forEach((z) => box(-13.4, 5.4, z - 0.45, -5.1, 6.25, z + 0.45, 1, 0, 21));
  // Subnode 22: 10 x 3 cartoning corridor + lift against the hall 2 party wall
  box(-14.2, 5.4, 8, -4.3, 9.9, 11, 1, 0.05, 22);
  box(-13.2, 5.4, 8.55, -6.4, 6.2, 10.45, 1, 0, 22);
  box(-4.25, 0, 8.15, -2.9, 10.6, 10.85, 1, 0, 22);
  // WIP 13 x 20 closed shell on the upper floor. No racks, no aisles, door shut.
  box(xW + 0.2, 5.4, zN + 0.2, xA - 0.2, 9.85, zWip, 0, 0.05, 0);
  box(xW + 1.3, 5.4, zWip - 0.08, xW + 3.3, 7.9, zWip + 0.08, 1, 0, 0);

  // HALL 2: 10 x 36. North 18 m is extruder below / cleanroom above. South bay is the filter room.
  box(xA, 0, zN, xB, 10.5, zS);
  box(xA, 5.15, zN, xB, 5.4, zCut, 0, 0.04);
  ZG.forEach((z) => roof(xA, xB, 10.5, z, 0.5));
  box(xA, 0, zCut - 0.1, xB, 10.5, zCut + 0.1, 0, 0.02);

  // Subnode 41: 4 extrusion lines (PBM-style) side by side, flow north -> south
  [-1.7, 0.7, 3.1, 5.5].forEach((x, i) => {
    box(x - 0.45, 0, -21.4, x + 0.45, 1.0, -19.6, 1, 0, 41); // drive motor + gearbox
    const g = new THREE.CylinderGeometry(0.2, 0.2, 3.2, 10); g.rotateX(Math.PI / 2);
    edges(g, x, 1.2, -17.9, 1, 0, 41); // barrel with heater bands
    for (let k = 0; k < 5; k++) cyl(0.26, 0.18, x, 1.2, -19.2 + k * 0.65, false, 0, 8, 0);
    box(x - 0.35, 0, -19.5, x + 0.35, 1.0, -16.3, 1, 0, 41);
    edges(new THREE.ConeGeometry(0.45, 0.8, 8).rotateX(Math.PI), x, 1.9, -19.2, 1, 0, 41); // hopper
    box(x - 0.3, 0.3, -15.9, x + 0.3, 1.25, -12.9, 1, 0, 41); // vacuum / cooling tank
    box(x - 0.3, 0, -12.6, x + 0.3, 1.45, -11.5, 1, 0, 41); // haul-off
    [0.95, 1.2].forEach((y) => { const b2 = new THREE.CylinderGeometry(0.1, 0.1, 0.62, 8); b2.rotateZ(Math.PI / 2); edges(b2, x, y, -12.05, 1, 0, 41); });
    box(x - 0.25, 0, -11.2, x + 0.25, 1.2, -10.6, 1, 0, 41); // cutter
    // V-shaped stainless tilt trough
    box(x - 0.2, 0, -10.4, x + 0.2, 0.75, -10.2, 0, 0, 41); box(x - 0.2, 0, -8.0, x + 0.2, 0.75, -7.8, 0, 0, 41);
    [-1, 1].forEach((sx) => { const t = new THREE.BoxGeometry(0.03, 0.3, 2.6); t.rotateZ(sx * 0.6); edges(t, x + sx * 0.11, 0.9, -9.1, 1, 0, 41); });
    // control panel on a swivel arm
    cyl(0.04, 1.6, x + 0.55, 0.8, -14.4, false, 0, 6, 41);
    box(x + 0.4, 1.6, -14.65, x + 0.75, 2.05, -14.25, 1, 0, 41);
    crate(x + (i % 2 ? -0.55 : 0.55), -8.6, 0.42, 0.55, 0.36, 2, 41); // yellow crates for coiled tubing
    lineY(x - 0.62, -21.6, x - 0.58, -7.6);
  });
  person(-0.5, -9.4, Math.PI / 2, 41); person(4.3, -12.0, -Math.PI / 2, 41);
  // Subnode 42: cleanroom pass-box + dedicated lift at the 18 m wall
  box(-2.35, 0, -7.3, 0.7, 3, -4.35, 1, 0, 42);
  box(4.55, 0, -7.45, 7.05, 10.5, -4.55, 1, 0, 42);
  // Subnode 43: upper Class 100,000 cleanroom with 2 assembly lines
  box(-2.35, 5.4, -21.5, 6.85, 9.55, -4.35, 1, 0.05, 43);
  [0.3, 4.2].forEach((x) => {
    box(x - 0.55, 5.4, -19.6, x + 0.55, 6.25, -7.4, 1, 0, 43);
    for (let k = 0; k < 4; k++) box(x - 0.28, 6.25, -18.4 + k * 2.7, x + 0.28, 6.75, -17.75 + k * 2.7, 1, 0, 43);
  });

  // Porous filter room: south of the 18 m wall, 9 m clear of the 10 m bay. Demolding only.
  box(-2.25, 0, zCut + 0.25, 6.75, 5.6, zS - 0.35, 0, 0.03, 0);
  // Subnode 31: mold press bed & columns
  box(0.85, 0, 2.6, 3.65, 1.55, 5.4, 1, 0, 31);
  [0.95, 3.55].forEach((x) => [2.75, 5.25].forEach((z) => cyl(0.1, 3.5, x, 3.3, z, false, 1, 6, 31)));
  box(0.85, 4.85, 2.6, 3.65, 5.25, 5.4, 1, 0, 31);
  // Subnode 32: finished filter QC tray
  box(4.35, 0, 7.2, 6.5, 1, 10.2, 1, 0, 32);
  // Demold sorters only: one at the press, one at the QC tray
  person(2.25, 6.3, 0, 31); person(5.4, 10.9, Math.PI, 32);

  // HALL 3: finished goods, full 8.50 x 36 m bay (not the old 7 x 18 stub)
  box(xB, 0, zN, xE, 8.6, zS);
  ZG.forEach((z) => roof(xB, xE, 8.6, z, 0.45));
  // Subnode 51: 45-count carton pallet racks along both long walls, aisle on centerline
  [8.55, 14.45].forEach((x) => {
    for (let z = -20.4; z < 9.5; z += 3.2) {
      box(x - 0.7, 0, z, x + 0.7, 5.1, z + 2.45, 1, 0, 51);
      [1.7, 3.4].forEach((y) => box(x - 0.7, y, z, x + 0.7, y + 0.08, z + 2.45, 1, 0, 51));
      box(x - 0.5, 0.2, z + 0.35, x + 0.15, 1.15, z + 2.1, 1, 0, 51);
    }
  });
  // Subnode 52: forklift aisle and the south dispatch door
  box(10.15, 0, zS - 0.16, 12.85, 3.8, zS + 0.08, 1, 0, 52);
  box(10.7, 0, 10.15, 12.3, 1.45, 12.55, 1, 0, 52);
  box(11.05, 1.45, 10.3, 11.95, 3.2, 10.65, 1, 0, 52);

  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.Float32BufferAttribute(P, 3));
  geo.setAttribute('aOrd', new THREE.Float32BufferAttribute(O, 1));
  geo.setAttribute('aTone', new THREE.Float32BufferAttribute(TN, 1));
  geo.setAttribute('aSub', new THREE.Float32BufferAttribute(SUB, 1));

  const uniforms = {
    uProg: { value: 0 },
    uBase: { value: new THREE.Color() },
    uHi: { value: new THREE.Color() },
    uCoral: { value: new THREE.Color('#ff7a59') },
    uActiveSub: { value: 0 },
    uInStation: { value: 0 },
  };
  const mat = new THREE.ShaderMaterial({
    uniforms, transparent: true,
    vertexShader: `
      attribute float aOrd;
      attribute float aTone;
      attribute float aSub;
      varying float vO;
      varying float vT;
      varying float vSub;
      void main(){
        vO = aOrd;
        vT = aTone;
        vSub = aSub;
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.);
      }
    `,
    fragmentShader: `
      uniform float uProg;
      uniform vec3 uBase;
      uniform vec3 uHi;
      uniform vec3 uCoral;
      uniform float uActiveSub;
      uniform float uInStation;
      varying float vO;
      varying float vT;
      varying float vSub;
      void main(){
        if (vO > uProg) discard;
        float fr = 1. - smoothstep(0., .06, uProg - vO);
        float isSub = (uActiveSub > 0.5 && abs(vSub - uActiveSub) < 0.25) ? 1.0 : 0.0;
        vec3 c = mix(uBase, uHi, vT);
        c = mix(c, uCoral, max(fr, isSub));
        float alpha = mix(1.0, vT > 0.5 ? 0.88 : 0.38, uInStation * (1.0 - isSub));
        gl_FragColor = vec4(c, alpha);
      }
    `,
  });
  scene.add(new THREE.LineSegments(geo, mat));

  // Animated filter demolding (Subnode 31)
  function partLines(build, subId = 31) {
    const g = build(), e = new THREE.EdgesGeometry(g, 20), n = e.attributes.position.count;
    e.setAttribute('aOrd', new THREE.Float32BufferAttribute(new Array(n).fill(0.55), 1));
    e.setAttribute('aTone', new THREE.Float32BufferAttribute(new Array(n).fill(1), 1));
    e.setAttribute('aSub', new THREE.Float32BufferAttribute(new Array(n).fill(subId), 1));
    g.dispose(); return new THREE.LineSegments(e, mat);
  }
  const moldTop = partLines(() => B(2.8, 0.9, 2.8), 31); scene.add(moldTop);
  const filter = partLines(() => new THREE.CylinderGeometry(0.75, 0.75, 0.22, 20), 31); scene.add(filter);

  // 3D Target Beacon Ring at the active machine sub-node
  const beaconGroup = new THREE.Group();
  const beaconMat = new THREE.LineBasicMaterial({ color: 0xff7a59, transparent: true, opacity: 0.95 });
  const bPts1 = [], bPts2 = [];
  for (let k = 0; k <= 64; k++) {
    const a = (k / 64) * Math.PI * 2;
    bPts1.push(new THREE.Vector3(Math.cos(a) * 2.2, 0, Math.sin(a) * 2.2));
    bPts2.push(new THREE.Vector3(Math.cos(a) * 1.1, 0, Math.sin(a) * 1.1));
  }
  const beaconOuter = new THREE.Line(new THREE.BufferGeometry().setFromPoints(bPts1), beaconMat);
  const beaconInner = new THREE.Line(new THREE.BufferGeometry().setFromPoints(bPts2), beaconMat);
  beaconGroup.add(beaconOuter, beaconInner);
  beaconGroup.visible = false;
  scene.add(beaconGroup);

  // Fingerprint ground rings
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

  /* ---------- stations & sub-nodes ---------- */
  const V3 = (x, y, z) => new THREE.Vector3(x, y, z);
  const VIEWS = [
    { p: V3(-40, 18, 2), t: V3(-9.4, 1.6, -10) },
    { p: V3(-36, 18, 14), t: V3(-9.25, 7.2, 4) },
    { p: V3(20, 11, 24), t: V3(2.25, 2.2, 4) },
    { p: V3(28, 16, 0), t: V3(1.9, 4.2, -15) },
    { p: V3(34, 13, 18), t: V3(11.5, 2.4, -4) },
  ];
  const LBL = [V3(-9.4, 6, -12), V3(-9.25, 11.4, 3), V3(2.25, 8, 5), V3(1.9, 11.2, -15), V3(11.5, 8.4, -4), V3(0, 8.2, 17.6), V3(16, 0.2, 30.2)];
  const smooth = (x) => { x = Math.min(1, Math.max(0, x)); return x * x * (3 - 2 * x); };
  const fmtStep = (i) => cfg.step.replace('{n}', cfg.nums[i]).replace('{t}', cfg.total);

  const controls = new OrbitControls(camera, canvas);
  controls.enabled = false; controls.enableDamping = true; controls.dampingFactor = 0.08;
  controls.maxDistance = 170; controls.minDistance = 6; controls.maxPolarAngle = Math.PI * 0.495;

  const intro = $('.f3d-intro'), dock = $('.f3d-dock'), dockToggle = $('.f3d-dock-toggle'), dockToggleLbl = $('.f3d-dock-toggle-lbl');
  const pStep = $('.f3d-step'), pTitle = $('.f3d-title'), subChipsEl = $('.f3d-subchips'), pSpec = $('.f3d-subspec');
  const dots = [...sec.querySelectorAll('.f3d-dots i')], bar = $('.f3d-prog i');
  const pills = [...sec.querySelectorAll('.f3d-pill')], exBtn = $('.f3d-ex'), exLabel = exBtn.querySelector('span');
  const labelsEl = $('.f3d-labels'), subPinsEl = $('.f3d-subpins');
  // Engineering-drawing callouts: one SVG holds every leader line
  const SVGNS = 'http://www.w3.org/2000/svg';
  const leadSvg = document.createElementNS(SVGNS, 'svg'); leadSvg.setAttribute('class', 'f3d-leads'); leadSvg.setAttribute('aria-hidden', 'true');
  labelsEl.parentNode.insertBefore(leadSvg, labelsEl);
  function makeCallout(cls, text, host, onClick) {
    const el = document.createElement('button'); el.type = 'button'; el.className = 'f3d-co ' + cls;
    el.innerHTML = '<span></span>'; el.firstChild.textContent = text;
    const dot = document.createElement('i'); dot.className = 'f3d-co-dot ' + cls;
    const path = document.createElementNS(SVGNS, 'path'); path.setAttribute('class', 'f3d-co-ln');
    leadSvg.appendChild(path); host.appendChild(dot); host.appendChild(el);
    el.addEventListener('click', onClick); dot.addEventListener('click', onClick);
    return { el, dot, path, side: 0 };
  }
  function removeCallout(c) { c.el.remove(); c.dot.remove(); c.path.remove(); }

  let sT = 0, sS = 0, explore = false, tween = null, lastIdx = -2, activeStation = 0, activeSubIdx = 0, visible = true;
  const subFocusOffset = new THREE.Vector3();
  const targetSubFocus = new THREE.Vector3();

  // Mobile: dock starts collapsed so the 3D machines stay visible
  const isNarrow = () => stage.clientWidth < 768;
  function setCollapsed(v) {
    dock.classList.toggle('is-collapsed', v);
    dockToggle.setAttribute('aria-expanded', String(!v));
    dockToggle.title = v ? cfg.expand : cfg.collapse;
    if (dockToggleLbl) dockToggleLbl.textContent = v ? cfg.expand : cfg.collapse;
  }
  if (isNarrow()) setCollapsed(true);
  // Dock collapse / expand toggle
  dockToggle.addEventListener('click', () => {
    const collapsed = dock.classList.toggle('is-collapsed');
    dockToggle.setAttribute('aria-expanded', String(!collapsed));
    dockToggle.title = collapsed ? cfg.expand : cfg.collapse;
    if (dockToggleLbl) dockToggleLbl.textContent = collapsed ? cfg.expand : cfg.collapse;
  });

  // Hall labels
  const lbls = cfg.labels.map((txt, i) => makeCallout('f3d-lbl', txt, labelsEl, () => {
    if (i < 5) {
      if (explore) flyTo(i, 0);
      else scrollTo({ top: stationScroll(i), behavior: reduce ? 'auto' : 'smooth' });
    }
  }));

  // Build 3D floating sub-node pins for active station
  let currentPinEls = [];
  function selectSubNode(stIdx, subIdx, userClicked = false) {
    const st = cfg.stations[stIdx];
    if (!st || !st.subs || !st.subs[subIdx]) return;
    activeStation = stIdx;
    activeSubIdx = subIdx;
    const sub = st.subs[subIdx];
    uniforms.uActiveSub.value = sub.id;
    pSpec.textContent = sub.spec;

    // Update top dock chips active state
    [...subChipsEl.querySelectorAll('.f3d-subchip')].forEach((c, k) => {
      c.classList.toggle('act', k === subIdx);
      c.setAttribute('aria-selected', String(k === subIdx));
    });
    // Update 3D floating pins active state
    currentPinEls.forEach((p, k) => { p.el.classList.toggle('act', k === subIdx); p.dot.classList.toggle('act', k === subIdx); p.path.classList.toggle('act', k === subIdx); });

    // Position 3D beacon ring at machine coordinates
    beaconGroup.position.set(sub.pos[0], sub.pos[1] - 0.8, sub.pos[2]);
    beaconGroup.visible = true;

    // Gentle camera focus shift toward the selected machine
    const baseT = VIEWS[stIdx].t;
    targetSubFocus.set(
      (sub.pos[0] - baseT.x) * 0.42,
      (sub.pos[1] - baseT.y) * 0.35,
      (sub.pos[2] - baseT.z) * 0.42
    );

    if (userClicked) {
      if (!isNarrow()) setCollapsed(false);
      if (explore) {
        tween = {
          t: 0,
          fp: camera.position.clone(),
          tp: VIEWS[stIdx].p.clone(),
          ft: controls.target.clone(),
          tt: V3(sub.pos[0], sub.pos[1], sub.pos[2]),
          i: stIdx
        };
      }
    }
  }

  function renderStationUI(stIdx) {
    if (stIdx < 0 || stIdx >= cfg.stations.length) {
      uniforms.uActiveSub.value = 0;
      beaconGroup.visible = false;
      targetSubFocus.set(0, 0, 0);
      currentPinEls.forEach(removeCallout);
      currentPinEls = [];
      return;
    }
    const st = cfg.stations[stIdx];
    const drawer = $('.f3d-dock-drawer');
    if (drawer && !reduce) { drawer.classList.remove('f3d-swap'); void drawer.offsetWidth; drawer.classList.add('f3d-swap'); }
    pStep.textContent = fmtStep(stIdx);
    pTitle.textContent = st.n;
    dots.forEach((d, k) => (d.className = k <= stIdx ? 'a' : ''));
    pills.forEach((p, k) => {
      const act = k === stIdx; p.classList.toggle('act', act);
      if (act) { const nav = p.parentElement; if (nav) nav.scrollTo({ left: p.offsetLeft - nav.clientWidth / 2 + p.offsetWidth / 2, behavior: reduce ? 'auto' : 'smooth' }); }
    });

    // Render top dock machine chips
    subChipsEl.innerHTML = '';
    currentPinEls.forEach(removeCallout);
    currentPinEls = [];

    st.subs.forEach((sub, k) => {
      const chip = document.createElement('button');
      chip.type = 'button';
      chip.className = 'f3d-subchip' + (k === 0 ? ' act' : '');
      chip.setAttribute('role', 'tab');
      chip.innerHTML = `<i></i><span>${sub.chip}</span>`;
      chip.addEventListener('click', () => selectSubNode(stIdx, k, true));
      subChipsEl.appendChild(chip);

      const co = makeCallout('f3d-subpin', sub.pin, subPinsEl, () => selectSubNode(stIdx, k, true));
      co.pos = V3(sub.pos[0], sub.pos[1], sub.pos[2]);
      currentPinEls.push(co);
    });

    selectSubNode(stIdx, 0, false);
  }

  function readScroll() {
    const r = sec.getBoundingClientRect(), m = r.height - innerHeight;
    sT = m > 0 ? Math.min(1, Math.max(0, -r.top / m)) : 0;
  }
  addEventListener('scroll', readScroll, { passive: true }); readScroll(); sS = sT;
  const stationScroll = (i) => { const m = sec.offsetHeight - innerHeight; return sec.getBoundingClientRect().top + scrollY + m * (0.25 + 0.15 * i + 0.08); };

  // Lock page scroll during free explore. iOS Safari ignores overflow:hidden on <html>,
  // so touches on the 3D view would scroll the page instead of orbiting the model.
  stage.addEventListener('touchmove', (e) => {
    if (explore && !e.target.closest('.f3d-dock,.f3d-tools')) e.preventDefault();
  }, { passive: false });
  function setExplore(on) {
    explore = on;
    tween = null;
    sec.classList.toggle('is-ex', on);
    resize();
    controls.enabled = on; exLabel.textContent = on ? cfg.back : cfg.explore;
    if (on) {
      const stI = lastIdx >= 0 ? lastIdx : 0;
      if (lastIdx < 0) { lastIdx = 0; renderStationUI(0); }
      // Visible feedback: glide from the current camera to an orbit view of the active hall
      activeStation = stI;
      const tgt = VIEWS[stI].t.clone().add(subFocusOffset);
      controls.target.copy(look);
      const dir = tmp.copy(camera.position).sub(look).normalize();
      tween = { t: 0, fp: camera.position.clone(), tp: tgt.clone().add(dir.multiplyScalar(camera.aspect < 1 ? 46 : 34)).setY(Math.max(14, camera.position.y)), ft: look.clone(), tt: tgt, i: stI };
    } else {
      readScroll();
    }
  }
  let lastExToggle = 0;
  function toggleExplore(e) {
    if (performance.now() - lastExToggle < 280) return;
    lastExToggle = performance.now();
    e.preventDefault(); e.stopPropagation(); setExplore(!explore);
  }
  exBtn.addEventListener('pointerup', (e) => { if (e.pointerType === 'touch' || e.pointerType === 'pen') toggleExplore(e); });
  exBtn.addEventListener('click', toggleExplore);
  $('.f3d-skip').addEventListener('click', () => { if (explore) setExplore(false); });
  pills.forEach((b) => b.addEventListener('click', () => {
    const i = +b.dataset.i;
    if (!isNarrow()) setCollapsed(false);
    if (explore) flyTo(i, 0);
    else scrollTo({ top: stationScroll(i), behavior: reduce ? 'auto' : 'smooth' });
  }));
  function flyTo(i, subIdx = 0) {
    lastIdx = i;
    renderStationUI(i);
    if (subIdx > 0) selectSubNode(i, subIdx, false);
    tween = { t: 0, fp: camera.position.clone(), tp: VIEWS[i].p.clone(), ft: controls.target.clone(), tt: VIEWS[i].t.clone(), i };
  }

  function resize() {
    const w = stage.clientWidth, h = stage.clientHeight; renderer.setSize(w, h, false);
    camera.aspect = w / h; camera.fov = w / h < 1 ? 60 : 40; camera.updateProjectionMatrix();
  }
  resize(); addEventListener('resize', resize);
  new IntersectionObserver((en) => { visible = en[0].isIntersecting; }).observe(sec);

  const pos = new THREE.Vector3(), look = new THREE.Vector3(), tmp = new THREE.Vector3(), fromP = new THREE.Vector3(), fromT = new THREE.Vector3();
  const clock = new THREE.Clock();
  function aerial(s, out, tgt) {
    const k = Math.min(1, s / 0.25), a = -0.75 + 0.9 * k, R = (camera.aspect < 1 ? 118 : 82) - 10 * k;
    out.set(Math.sin(a) * R, 54 - 8 * k, Math.cos(a) * R - 4); tgt.set(0, camera.aspect < 1 ? 14 - 6 * k : 16 - 4 * k, -4);
  }
  function frame() {
    requestAnimationFrame(frame);
    if (!visible) return;
    const dt = Math.min(0.1, clock.getDelta());
    const time = clock.elapsedTime;
    // Framerate-independent damping, time constant ~0.6 s
    const kS = reduce ? 1 : 1 - Math.exp(-dt / 0.6);
    const kF = reduce ? 1 : 1 - Math.exp(-dt / 0.45);
    sS += (sT - sS) * kS;
    if (Math.abs(sT - sS) < 1e-5) sS = sT;
    const s = sS;
    const autoProg = Math.min(1.1, (time / 1.4) * 1.1);
    const prog = (explore || reduce) ? 1.1 : Math.max(autoProg, Math.min(1.1, (s / 0.17) * 1.1));
    uniforms.uProg.value = prog;
    ringMats.forEach((m, i) => { m.opacity = 0.03 + 0.14 * Math.min(1, Math.max(0, prog - i * 0.06)); });

    // Pulse the 3D beacon ring
    if (beaconGroup.visible) {
      const pulse = reduce ? 1 : 1 + 0.12 * Math.sin(time * 4.0);
      beaconOuter.scale.set(pulse, 1, pulse);
    }

    // Filter demolding loop (6 s)
    const c = reduce ? 0.8 : (time % 6) / 6, lift = smooth(c / 0.25) - smooth((c - 0.85) / 0.15);
    moldTop.position.set(2.25, 2.0 + lift * 1.6, 4.0);
    const out = smooth((c - 0.3) / 0.35), place = smooth((c - 0.65) / 0.15);
    filter.position.set(2.25 + out * 2.5, 1.7 + Math.sin(out * Math.PI) * 1.6 * (1 - place) + lift * 0.2 * (1 - out) - place * 0.45, 4.0 + out * 3.5);
    filter.visible = c < 0.95 && c > 0.05;

    subFocusOffset.lerp(targetSubFocus, kF);

    let idx = -1;
    if (!explore) {
      const t = (s - 0.25) / 0.15;
      if (t < 0) {
        aerial(s, pos, look);
        uniforms.uInStation.value = 0;
      } else {
        idx = Math.min(4, Math.floor(t));
        uniforms.uInStation.value = 1;
        // Keyframes: aerial at t=0, station i centred at t=i+0.5; ease across the whole gap
        const u = t - 0.5;
        if (u < 0) {
          aerial(0.25, fromP, fromT); const f = smooth(t / 0.5);
          pos.lerpVectors(fromP, VIEWS[0].p, f); look.lerpVectors(fromT, VIEWS[0].t, f);
        } else {
          const a = Math.min(4, Math.floor(u)), b = Math.min(4, a + 1), f = smooth(u - a);
          pos.lerpVectors(VIEWS[a].p, VIEWS[b].p, f); look.lerpVectors(VIEWS[a].t, VIEWS[b].t, f);
        }
        look.add(subFocusOffset);
        if (camera.aspect < 1) { pos.add(tmp.copy(pos).sub(look).multiplyScalar(0.95)); pos.y += 6; }
      }
      camera.position.copy(pos); camera.lookAt(look);
      intro.style.opacity = String(Math.max(0, 1 - Math.max(0, s - 0.19) / 0.045));
      intro.style.visibility = s > 0.235 ? 'hidden' : 'visible';
      bar.style.height = (s * 100) + '%';
      dock.classList.toggle('on', idx >= 0);
      if (idx !== lastIdx) {
        lastIdx = idx;
        renderStationUI(idx);
      }
    } else {
      uniforms.uInStation.value = 1;
      if (tween) {
        tween.t = reduce ? 1 : Math.min(1, tween.t + dt / 1.1); const e = smooth(tween.t);
        camera.position.lerpVectors(tween.fp, tween.tp, e); controls.target.lerpVectors(tween.ft, tween.tt, e);
        if (tween.t >= 1) tween = null;
      }
      controls.update();
      dock.classList.add('on');
      idx = activeStation;
    }

    const w = stage.clientWidth, h = stage.clientHeight;
    const narrow = w < 768;
    const sr = stage.getBoundingClientRect();
    const dockBot = dock.classList.contains('on') ? dock.getBoundingClientRect().bottom - sr.top + 4 : (narrow ? 110 : 130);
    const introBot = (idx < 0 && s < 0.22 && !explore) ? intro.getBoundingClientRect().bottom - sr.top + 8 : 0;
    const topSafe = Math.max(dockBot, introBot, narrow ? 64 : 80), botSafe = h - (narrow ? 84 : 90);
    const showHallLabels = (explore || idx < 0) && prog > 0.75;
    const items = [];
    lbls.forEach((c, i) => {
      const act = i === idx;
      c.el.classList.toggle('act', act); c.dot.classList.toggle('act', act); c.path.classList.toggle('act', act);
      items.push({ c, p: LBL[i], on: showHallLabels && (explore || i < 5 || i === 6), pri: act ? 3 : 1 });
    });
    currentPinEls.forEach((c, k) => items.push({ c, p: c.pos, on: idx >= 0, pri: k === activeSubIdx ? 4 : 2 }));
    items.sort((x, y) => y.pri - x.pri);
    const placed = [];
    const hit = (r) => placed.some((q) => r.x < q.x + q.w && r.x + r.w > q.x && r.y < q.y + q.h && r.y + r.h > q.y);
    const LX = narrow ? 18 : 26, LY = narrow ? 26 : 34, LH = narrow ? 10 : 14;
    items.forEach(({ c, p, on }) => {
      let vis = false;
      if (on) {
        tmp.copy(p).project(camera);
        const ax = (tmp.x * 0.5 + 0.5) * w, ay = (-tmp.y * 0.5 + 0.5) * h;
        if (tmp.z < 1 && ax > 8 && ax < w - 8 && ay > topSafe && ay < botSafe) {
          const tw = c.el.offsetWidth, th = c.el.offsetHeight;
          const pref = ax > w / 2 ? -1 : 1;
          const tries = [[pref, 1], [-pref, 1], [pref, 1.9], [-pref, 1.9], [pref, -0.9], [-pref, -0.9]];
          for (const [sd, up] of tries) {
            const ex = ax + sd * LX, ey = ay - LY * up, tx = sd > 0 ? ex + LH : ex - LH - tw;
            const r = { x: tx - 4, y: ey - th / 2 - 2, w: tw + 8, h: th + 4 };
            if (r.x < 4 || r.x + r.w > w - 4 || r.y < topSafe - 6 || r.y + r.h > botSafe + 30 || hit(r)) continue;
            placed.push(r, { x: ax - 7, y: ay - 7, w: 14, h: 14 });
            c.el.style.transform = `translate(${tx}px,${ey - th / 2}px)`;
            c.dot.style.transform = `translate(${ax}px,${ay}px)`;
            c.path.setAttribute('d', `M${ax.toFixed(1)} ${ay.toFixed(1)}L${ex.toFixed(1)} ${ey.toFixed(1)}H${(ex + sd * (LH - 3)).toFixed(1)}`);
            vis = true; break;
          }
        }
      }
      c.el.classList.toggle('show', vis); c.dot.classList.toggle('show', vis); c.path.classList.toggle('show', vis);
    });

    renderer.render(scene, camera);
  }
  frame();
}
