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
  // Solid 3D machine shells (injection presses 11/12, extrusion lines 41); edges stay as a thin overlay
  const SP = [], SN = [], SO = [], SS = [], SOLID_SUBS = new Set([29, 49, 11, 12, 21, 22, 23, 31, 43, 44, 32, 41, 42, 51, 52]);
  function edges(geo, x, y, z, tone = 0, ordBias = 0, subId = 0) {
    const e = new THREE.EdgesGeometry(geo, 20), p = e.attributes.position;
    for (let i = 0; i < p.count; i++) {
      const wx = p.getX(i) + x, wy = p.getY(i) + y, wz = p.getZ(i) + z;
      P.push(wx, wy, wz);
      O.push(Math.min(1, Math.max(0, 0.04 + 0.5 * (25 - wz) / 50 + 0.36 * (wy / 14) + 0.08 * ((wx + 20) / 40) + ordBias)));
      TN.push(tone);
      SUB.push(subId);
    }
    if (tone === 1 && SOLID_SUBS.has(subId)) {
      const g2 = geo.index ? geo.toNonIndexed() : geo; g2.computeVertexNormals();
      const q = g2.attributes.position, nn = g2.attributes.normal;
      for (let i = 0; i < q.count; i++) {
        const wx = q.getX(i) + x, wy = q.getY(i) + y, wz = q.getZ(i) + z;
        SP.push(wx, wy, wz); SN.push(nn.getX(i), nn.getY(i), nn.getZ(i));
        SO.push(Math.min(1, Math.max(0, 0.04 + 0.5 * (25 - wz) / 50 + 0.36 * (wy / 14) + 0.08 * ((wx + 20) / 40) + ordBias)));
        SS.push(subId);
      }
      if (g2 !== geo) g2.dispose();
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
  box(xW, 5.15, zN, xA, 5.4, zS - 3, 1, 0.04, 29); // solid mezzanine slab (2nd floor)
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
  const PEOPLE = []; // built later as animated wireframe groups (work-cycle micro-motion)
  const person = (x, z, rot = 0, sub = 0, s = 1, kind = null) => { PEOPLE.push({ x, z, rot, sub, s, kind }); };
  const MOV = { hop: [], light: [], roll: [], trough: [] }; // active-station machine motion anchors
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
    MOV.hop.push({ x, y: hb * 1.15, z: hz, r0: w * 0.28, r1: w * 0.1, h: hb * 0.35, sub, st: 0 });
    MOV.light.push({ x: x + w * 0.35, y: hb * 0.45 + pH + 0.1 + 2 * 0.13, z: zc + 0.05, sub, st: 0 });
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
  box(-14.25, 5.4, -2, -4.25, 9.9, 8, 0, 0.05, 21); // PU room shell: outline only so the lines inside stay visible
  [-0.2, 2.6, 5.4].forEach((z) => {
    box(-13.4, 5.4, z - 0.45, -5.1, 6.25, z + 0.45, 1, 0, 21); // assembly bench
    for (let k = 0; k < 4; k++) box(-12.6 + k * 2, 6.25, z - 0.3, -11.6 + k * 2, 6.75, z + 0.3, 1, 0, 21); // leak-test / sealing stations
    box(-13.4, 6.25, z - 0.06, -5.1, 6.35, z + 0.06, 1, 0, 21); // conveyor belt strip
  });
  // Subnode 22: 10 x 3 cartoning corridor + lift against the hall 2 party wall
  box(-14.2, 5.4, 8, -4.3, 9.9, 11, 0, 0.05, 22);
  box(-13.2, 5.4, 8.55, -6.4, 6.2, 10.45, 1, 0, 22);
  box(-4.25, 0, 8.15, -2.9, 10.6, 10.85, 1, 0, 22);
  // WIP 13 x 20 closed shell on the upper floor. No racks, no aisles, door shut.
  box(xW + 0.2, 5.4, zN + 0.2, xA - 0.2, 9.85, zWip, 0, 0.05, 0);
  box(xW + 1.3, 5.4, zWip - 0.08, xW + 3.3, 7.9, zWip + 0.08, 1, 0, 0);
  // Subnode 23: NW-corner goods lift feeding the closed WIP store above injection (shaft + car + landing door only)
  box(xW + 0.35, 0, zN + 0.35, xW + 2.55, 10.4, zN + 2.55, 1, 0, 23);
  box(xW + 0.6, 5.45, zN + 0.6, xW + 2.3, 7.6, zN + 2.3, 1, 0, 23); // lift car parked at the WIP level
  box(xW + 2.55, 5.4, zN + 0.8, xW + 2.65, 7.8, zN + 2.1, 1, 0, 23); // landing door into the WIP shell (shut)

  // HALL 2: 10 x 36. North 18 m is extruder below / cleanroom above. South bay is the filter room.
  box(xA, 0, zN, xB, 10.5, zS);
  box(xA, 5.15, zN, xB, 5.4, zCut, 1, 0.04, 49); // solid cleanroom floor slab
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
    MOV.hop.push({ x, y: 1.9, z: -19.2, cone: true, sub: 41, st: 3 });
    [0.95, 1.2].forEach((y) => MOV.roll.push({ x, y, z: -12.05, sub: 41, st: 3 }));
    MOV.trough.push({ x, z: -9.1, sub: 41, st: 3 });
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
  // Extra crew (+6): QC at the yellow lines, crate stackers, extrusion QC, dispatch, street-side walker. None in WIP / cleanroom.
  person(-6.9, -12.2, 0, 11, 1, 'qc'); person(-11.0, -2.0, Math.PI, 12, 1, 'stack');
  person(2.0, -8.2, Math.PI / 2, 41, 1, 'qc'); person(9.8, 4.0, Math.PI / 2, 51, 1, 'stack');
  person(11.5, 13.0, 0, 52, 1, 'qc'); person(-20, 24.2, Math.PI / 2, 0, 1, 'walk');
  // Subnode 42: cleanroom pass-box + dedicated lift at the 18 m wall
  box(-2.35, 0, -7.3, 0.7, 3, -4.35, 1, 0, 42);
  box(4.55, 0, -7.45, 7.05, 10.5, -4.55, 1, 0, 42);
  // Subnode 43: upper Class 100,000 cleanroom with 2 assembly lines
  box(-2.35, 5.4, -21.5, 6.85, 9.55, -4.35, 0, 0.05, 43); // cleanroom envelope: outline only
  [0.3, 4.2].forEach((x) => {
    box(x - 0.55, 5.4, -19.6, x + 0.55, 6.25, -7.4, 1, 0, 43);
    for (let k = 0; k < 4; k++) box(x - 0.28, 6.25, -18.4 + k * 2.7, x + 0.28, 6.75, -17.75 + k * 2.7, 1, 0, 43);
  });

  // Porous filter room: south of the 18 m wall, 9 m clear of the 10 m bay. Demolding only.
  box(-2.25, 0, zCut + 0.25, 6.75, 5.6, zS - 0.35, 0, 0.03, 0);
  // Subnode 31: mold press bed & columns
  // 6 filter mold presses: 2 columns x 3 rows, west of the QC tray
  const PRESSES = [];
  [-0.35, 3.05].forEach((cx) => [-1.4, 2.6, 6.6].forEach((cz) => PRESSES.push([cx, cz])));
  PRESSES.forEach(([cx, cz]) => {
    box(cx - 1.4, 0, cz - 1.4, cx + 1.4, 1.55, cz + 1.4, 1, 0, 31);
    [cx - 1.3, cx + 1.3].forEach((x) => [cz - 1.25, cz + 1.25].forEach((z) => cyl(0.1, 3.5, x, 3.3, z, false, 1, 6, 31)));
    box(cx - 1.4, 4.85, cz - 1.4, cx + 1.4, 5.25, cz + 1.4, 1, 0, 31);
  });
  // Subnode 32: finished filter QC tray
  box(5.0, 0, 7.2, 6.6, 1, 10.2, 1, 0, 32);
  // Demold sorters only: at the presses and one at the QC tray
  person(1.35, 3.0, Math.PI / 2, 31); person(1.35, -1.0, -Math.PI / 2, 31); person(1.35, 7.0, Math.PI / 2, 31);
  person(5.8, 10.9, Math.PI, 32);

  // HALL 3: finished goods, full 8.50 x 36 m bay (not the old 7 x 18 stub)
  box(xB, 0, zN, xE, 8.6, zS);
  ZG.forEach((z) => roof(xB, xE, 8.6, z, 0.45));
  // Subnode 51: 45-count carton pallet racks along both long walls, aisle on centerline
  [8.55, 14.45].forEach((x) => {
    for (let z = -20.4; z < 9.5; z += 3.2) {
      // solid rack: 4 uprights, 3 shelf decks, pallet + carton stacks on every level
      [[x - 0.7, z], [x + 0.62, z], [x - 0.7, z + 2.37], [x + 0.62, z + 2.37]].forEach(([px, pz]) => box(px, 0, pz, px + 0.08, 5.1, pz + 0.08, 1, 0, 51));
      [0.12, 1.7, 3.4].forEach((y, li) => {
        box(x - 0.7, y, z, x + 0.7, y + 0.08, z + 2.45, 1, 0, 51);
        box(x - 0.55, y + 0.08, z + 0.2, x + 0.55, y + 0.2, z + 2.25, 1, 0, 51); // pallet
        for (let c = 0; c < 3; c++) {
          const cz = z + 0.3 + c * 0.66, h = 0.5 + ((li + c) % 2) * 0.35;
          box(x - 0.5, y + 0.2, cz, x - 0.02, y + 0.2 + h, cz + 0.6, 1, 0, 51);
          box(x + 0.02, y + 0.2, cz, x + 0.5, y + 0.2 + 0.85 - h * 0.4, cz + 0.6, 1, 0, 51);
        }
      });
    }
  });
  // Subnode 52: forklift (solid) in the aisle + south dispatch door
  box(10.15, 0, zS - 0.16, 12.85, 3.8, zS + 0.08, 1, 0, 52);
  box(10.75, 0.3, 9.6, 12.25, 1.25, 11.9, 1, 0, 52); // chassis
  box(10.8, 1.25, 11.2, 12.2, 1.75, 11.9, 1, 0, 52); // counterweight
  box(11.1, 1.25, 10.4, 11.9, 1.6, 11.0, 1, 0, 52); // seat
  [[10.8, 9.75], [12.2, 9.75], [10.8, 11.75], [12.2, 11.75]].forEach(([px, pz]) => box(px - 0.04, 1.25, pz - 0.04, px + 0.04, 3.0, pz + 0.04, 1, 0, 52));
  box(10.75, 2.95, 9.7, 12.25, 3.05, 11.85, 1, 0, 52); // overhead guard
  box(10.95, 0.1, 9.3, 11.1, 3.3, 9.45, 1, 0, 52); box(11.9, 0.1, 9.3, 12.05, 3.3, 9.45, 1, 0, 52); // mast
  box(11.0, 0.75, 9.25, 12.0, 0.85, 9.35, 1, 0, 52); // carriage
  box(11.1, 0.7, 8.1, 11.25, 0.78, 9.3, 1, 0, 52); box(11.75, 0.7, 8.1, 11.9, 0.78, 9.3, 1, 0, 52); // forks
  box(11.0, 0.78, 8.1, 12.0, 0.9, 9.25, 1, 0, 52); box(11.1, 0.9, 8.2, 11.9, 1.6, 9.15, 1, 0, 52); // pallet + carton load
  [[10.75, 10.0], [12.25, 10.0], [10.75, 11.5], [12.25, 11.5]].forEach(([px, pz]) => cyl(0.3, 0.22, px, 0.3, pz, true, 1, 14, 52));

  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.Float32BufferAttribute(P, 3));
  geo.setAttribute('aOrd', new THREE.Float32BufferAttribute(O, 1));
  geo.setAttribute('aTone', new THREE.Float32BufferAttribute(TN, 1));
  geo.setAttribute('aSub', new THREE.Float32BufferAttribute(SUB, 1));

  const uniforms = {
    uProg: { value: 0 },
    uBase: { value: new THREE.Color() },
    uHi: { value: new THREE.Color() },
    uCoral: { value: new THREE.Color('#ffb300') },
    uActiveSub: { value: 0 },
    uInStation: { value: 0 },
    uRoof: { value: 0 },
    uPulse: { value: 0 },
    uFill: { value: new THREE.Color('#08333d') }, uFillMix: { value: 0.35 },
    uUpper: { value: 0 }, // 0..1: upper-floor focus (assembly / cleanroom): shells + other floors recede
    uHideSt: { value: 0 }, // 0..1: hide occluding hall-3 racks while on the extruder station
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
      varying vec3 vW;
      void main(){
        vW = position;
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
      varying vec3 vW;
      uniform float uRoof;
      uniform float uPulse;
      uniform float uHideSt;
      uniform float uUpper;
      void main(){
        if (vO > uProg) discard;
        float fr = 1. - smoothstep(0., .06, uProg - vO);
        float isSub = (uActiveSub > 0.5 && abs(vSub - uActiveSub) < 0.25) ? smoothstep(0.3, 0.7, uInStation) : 0.0;
        vec3 c = mix(uBase, uHi, vT);
        c = mix(c, uCoral, max(fr, isSub));
        float alpha = mix(1.0, vT > 0.5 ? 0.88 : 0.38, uInStation * (1.0 - isSub));
        // Roof fade: upper shell (roof trusses + wall tops over the sheds) dims while inside a station
        float up = smoothstep(7.6, 8.4, vW.y) * step(vW.z, 14.3) * step(abs(vW.x), 16.0);
        alpha *= mix(1.0, 0.05, uRoof * up);
        // Non-active machines recede a bit so the active one pops
        alpha *= mix(1.0, 0.7, uRoof * (1.0 - isSub) * vT * (1.0 - up));
        c = mix(c, vec3(1.0, 0.82, 0.35), isSub * (0.25 + 0.2 * uPulse));
        // Extruder station: hall-3 racks nearly vanish, hall shell wireframe recedes hard
        float occ = step(49.5, vSub) * step(vSub, 59.5);
        alpha *= mix(1.0, 0.04, uHideSt * occ);
        alpha *= mix(1.0, 0.35, uHideSt * (1.0 - vT));
        alpha *= mix(1.0, 0.45, uHideSt * vT * (1.0 - isSub) * (1.0 - step(39.5, vSub) * step(vSub, 49.5)));
        // Upper-floor focus: hall walls / WIP shell / ground machines fade, mezzanine machines stay crisp
        float slab = step(28.5, vSub) * step(vSub, 29.5) + step(48.5, vSub) * step(vSub, 49.5);
        float upSub = (step(20.5, vSub) * step(vSub, 23.5) + step(42.5, vSub) * step(vSub, 44.5)) + slab;
        alpha *= mix(1.0, mix(0.1, 0.3, step(0.5, upSub)), uUpper * (1.0 - vT) * (1.0 - isSub));
        alpha *= mix(1.0, 0.3, uUpper * vT * (1.0 - upSub));
        alpha = max(alpha, uUpper * upSub * vT);
        c = mix(c, uHi, uUpper * upSub * vT * (1.0 - isSub) * 0.6);
        c = mix(c, uHi, slab * 0.5);
        alpha *= mix(1.0, mix(0.25, 1.0, uUpper), slab * uRoof);
        gl_FragColor = vec4(c, alpha);
      }
    `,
  });
  scene.add(new THREE.LineSegments(geo, mat));

  const sgeo = new THREE.BufferGeometry();
  sgeo.setAttribute('position', new THREE.Float32BufferAttribute(SP, 3));
  sgeo.setAttribute('normal', new THREE.Float32BufferAttribute(SN, 3));
  sgeo.setAttribute('aOrd', new THREE.Float32BufferAttribute(SO, 1));
  sgeo.setAttribute('aSub', new THREE.Float32BufferAttribute(SS, 1));
  const smat = new THREE.ShaderMaterial({
    uniforms, transparent: true, side: THREE.DoubleSide, depthWrite: true,
    polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1,
    vertexShader: `
      attribute float aOrd; attribute float aSub;
      varying float vO; varying float vSub; varying vec3 vN;
      void main(){ vO = aOrd; vSub = aSub; vN = normalize(normal);
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.); }
    `,
    fragmentShader: `
      uniform float uProg; uniform vec3 uBase; uniform vec3 uHi; uniform vec3 uCoral;
      uniform float uActiveSub; uniform float uInStation; uniform float uPulse; uniform float uRoof; uniform float uHideSt; uniform float uUpper; uniform vec3 uFill; uniform float uFillMix;
      varying float vO; varying float vSub; varying vec3 vN;
      void main(){
        if (uHideSt > 0.5 && vSub > 49.5 && vSub < 59.5) discard;
        float grow = smoothstep(vO, vO + .08, uProg);
        if (grow <= 0.) discard;
        vec3 L = normalize(vec3(.45, .85, .35));
        float d = .45 + .55 * max(dot(normalize(vN), L), 0.) + .12 * abs(vN.z);
        float isSub = (uActiveSub > 0.5 && abs(vSub - uActiveSub) < 0.25) ? smoothstep(0.3, 0.7, uInStation) : 0.0;
        // Active machine: full coral + key light / rim glow; others dim slightly
        vec3 c = mix(mix(uFill, uHi * 0.55, uFillMix) * d * mix(1.0, 0.78, uRoof), uCoral * (0.75 + 0.6 * d), isSub * .95);
        float rim = pow(1. - abs(normalize(vN).y), 2.0);
        c += isSub * (vec3(1.0, 0.7, 0.1) * (0.18 + 0.14 * uPulse) + vec3(1.0, 0.9, 0.6) * rim * 0.12);
        float ext = step(39.5, vSub) * step(vSub, 49.5);
        c *= 1.0 + uHideSt * ext * 0.25 * (1.0 - isSub);
        c += uHideSt * isSub * vec3(0.12, 0.08, 0.0);
        float upS = step(20.5, vSub) * step(vSub, 23.5) + step(42.5, vSub) * step(vSub, 44.5);
        c *= mix(1.0, mix(1.0, 1.35, upS), uUpper * (1.0 - isSub)); // key light on the mezzanine, ground dims
        c += uUpper * upS * vec3(0.05, 0.09, 0.1);
        // Floor slabs: a clear 2nd-floor deck. Aerial = translucent, upper station = near-opaque, ground station = ghosted
        float slab = step(28.5, vSub) * step(vSub, 29.5) + step(48.5, vSub) * step(vSub, 49.5);
        vec3 deck = mix(uHi, vec3(1.0), 0.35) * (0.8 + 0.2 * d);
        c = mix(c, deck, slab);
        float a = grow * mix(mix(.82, .97, isSub), mix(.22, 1.0, upS), uUpper);
        float aSlab = grow * mix(mix(0.55, 0.12, uRoof), 0.92, uUpper);
        gl_FragColor = vec4(c, mix(a, aSlab, slab));
      }
    `,
  });
  const solids = new THREE.Mesh(sgeo, smat); solids.renderOrder = -1; scene.add(solids);

  // Animated filter demolding (Subnode 31)
  function partLines(build, subId = 31) {
    const g = build(), e = new THREE.EdgesGeometry(g, 20), n = e.attributes.position.count;
    e.setAttribute('aOrd', new THREE.Float32BufferAttribute(new Array(n).fill(0.55), 1));
    e.setAttribute('aTone', new THREE.Float32BufferAttribute(new Array(n).fill(1), 1));
    e.setAttribute('aSub', new THREE.Float32BufferAttribute(new Array(n).fill(subId), 1));
    g.dispose(); return new THREE.LineSegments(e, mat);
  }
  function solidPart(build, subId = 31) {
    const l = partLines(build, subId), g = build(), n = g.attributes.position.count;
    g.setAttribute('aOrd', new THREE.Float32BufferAttribute(new Array(n).fill(0.55), 1));
    g.setAttribute('aSub', new THREE.Float32BufferAttribute(new Array(n).fill(subId), 1));
    g.computeVertexNormals();
    const m = new THREE.Mesh(g, smat); m.renderOrder = -1; l.add(m); return l;
  }
  const moldTops = PRESSES.map(() => { const m = solidPart(() => B(2.8, 0.9, 2.8), 31); scene.add(m); return m; });
  const filters = PRESSES.map(() => { const m = solidPart(() => new THREE.CylinderGeometry(0.75, 0.75, 0.22, 20), 31); scene.add(m); return m; });

  // Operators: block/stick figures with looping work cycles (no faces). Kind from station sub-id.
  const PART = (geo, sub, x, y, z) => { const l = partLines(() => geo, sub); l.position.set(x, y, z); return l; };
  const workers = PEOPLE.map((d, n) => {
    const { s, sub } = d, g = new THREE.Group(); g.position.set(d.x, 0, d.z); g.rotation.y = -d.rot;
    [-0.11, 0.11].forEach((dx) => g.add(PART(B(0.14 * s, 0.85 * s, 0.16 * s), sub, dx, 0.425 * s, 0)));
    const up = new THREE.Group(); up.position.y = 0.85 * s; g.add(up); // hip pivot
    up.add(PART(B(0.4 * s, 0.6 * s, 0.4 * s), sub, 0, 0.3 * s, 0));
    const head = PART(new THREE.IcosahedronGeometry(0.13 * s, 1), sub, 0, 0.77 * s, 0); up.add(head);
    const arms = [-0.27, 0.27].map((dx) => {
      const sh = new THREE.Group(); sh.position.set(dx * s, 0.55 * s, 0.12 * s); up.add(sh); // shoulder pivot
      sh.add(PART(B(0.1 * s, 0.45 * s, 0.1 * s), sub, 0, -0.225 * s, 0)); return sh;
    });
    scene.add(g);
    const kind = d.kind || (sub >= 51 ? 'stack' : sub >= 41 ? 'coil' : sub >= 31 ? 'demold' : sub === 12 ? 'sort' : 'pendant');
    return { g, up, head, arms, kind, s, ph: n * 0.37, per: 2.2 + (n % 4) * 0.25, legs: g.children.slice(0, 2) };
  });
  function animateWorkers(time) {
    workers.forEach((w) => {
      const [L, R] = w.arms;
      if (reduce) { w.up.rotation.set(0.06, 0, 0); w.up.position.y = 0.85 * w.s; L.rotation.set(-0.5, 0, 0); R.rotation.set(-0.5, 0, 0); return; }
      const c = ((time + w.ph) % w.per) / w.per, sw = Math.sin(c * Math.PI * 2), hump = Math.sin(c * Math.PI);
      w.up.position.y = 0.85 * w.s + 0.025 * w.s * Math.sin(c * Math.PI * 4); // breathing / weight shift bob
      if (w.kind === 'pendant') { // reach up to the control pendant, tap, return
        R.rotation.set(-0.4 - 1.1 * hump, 0, -0.15 * hump); L.rotation.set(-0.15, 0, 0); w.up.rotation.set(0.04, 0.2 * hump, 0); w.head.rotation.x = -0.2 * hump;
      } else if (w.kind === 'sort') { // bend, pick part, turn and drop into crate
        const bend = smooth(c / 0.3) - smooth((c - 0.55) / 0.3);
        w.up.rotation.set(0.45 * bend, 0.6 * smooth((c - 0.35) / 0.3) * (1 - smooth((c - 0.8) / 0.2)), 0);
        L.rotation.set(-0.3 - 0.9 * bend, 0, 0); R.rotation.set(-0.3 - 0.9 * bend, 0, 0);
      } else if (w.kind === 'qc') { // QC: hold clipboard, look down / scan along the line
        L.rotation.set(-1.1, 0, 0.3); R.rotation.set(-1.0 - 0.15 * sw, 0, -0.3); w.head.rotation.set(0.35 + 0.1 * sw, 0.45 * Math.sin(c * Math.PI * 2), 0); w.up.rotation.set(0.08, 0, 0);
      } else if (w.kind === 'stack') { // crate stacker: squat-lift, raise, place on stack
        const lift = smooth(c / 0.35) - smooth((c - 0.6) / 0.3);
        w.up.rotation.set(0.55 * (1 - lift) * hump, 0, 0); L.rotation.set(-0.6 - 1.4 * lift, 0, 0); R.rotation.set(-0.6 - 1.4 * lift, 0, 0);
      } else if (w.kind === 'walk') { // street-side walker: gate path along the sidewalk, ping-pong
        const T = 24, q = ((time + w.ph) % T) / T, dir = q < 0.5 ? 1 : -1, ph = q < 0.5 ? q * 2 : 2 - q * 2;
        w.g.position.x = -20 + 40 * smooth(ph); w.g.rotation.y = dir > 0 ? Math.PI / 2 : -Math.PI / 2;
        const st = Math.sin(time * 7); w.legs[0].rotation.x = 0.4 * st; w.legs[1].rotation.x = -0.4 * st;
        L.rotation.set(-0.35 * st, 0, 0); R.rotation.set(0.35 * st, 0, 0); w.up.rotation.set(0.05, 0, 0);
      } else if (w.kind === 'coil') { // hand-over-hand coiling of tube at the haul-off
        L.rotation.set(-0.9 + 0.5 * sw, 0, 0.2 * sw); R.rotation.set(-0.9 - 0.5 * sw, 0, -0.2 * sw); w.up.rotation.set(0.15, 0.12 * sw, 0);
      } else { // demold sorter: reach into opened mold, lift filter, set down
        const reach = smooth((c - 0.2) / 0.25) - smooth((c - 0.6) / 0.25);
        w.up.rotation.set(0.1 + 0.35 * reach, 0, 0); L.rotation.set(-0.4 - 1.0 * reach, 0, 0); R.rotation.set(-0.4 - 1.0 * reach, 0, 0); w.head.rotation.x = 0.25 * reach;
      }
    });
  }

  // Active-station machine motion overlays (Y): only the station in view animates; others sit still.
  const movers = [];
  const ovl = (geo, sub, x, y, z, st, kind, extra = {}) => { const l = partLines(() => geo, sub); l.position.set(x, y, z); scene.add(l); movers.push({ l, st, kind, ...extra }); return l; };
  MOV.hop.forEach((h, i) => ovl(h.cone ? new THREE.ConeGeometry(0.5, 0.15, 8) : new THREE.CylinderGeometry(h.r0 * 1.08, h.r0 * 1.08, 0.06, 10), h.sub, h.x, h.cone ? 2.25 : h.y + h.h * 0.5, h.z, h.st, 'hop', { i, y0: h.cone ? 2.25 : h.y + h.h * 0.5 }));
  MOV.light.forEach((h, i) => ovl(new THREE.IcosahedronGeometry(0.11, 1), h.sub, h.x, h.y + 0.02, h.z, h.st, 'light', { i }));
  MOV.roll.forEach((h, i) => { const g2 = new THREE.CylinderGeometry(0.13, 0.13, 0.5, 6); g2.rotateZ(Math.PI / 2); ovl(g2, h.sub, h.x, h.y, h.z, h.st, 'roll', { i }); });
  MOV.trough.forEach((h, i) => ovl(new THREE.BoxGeometry(0.34, 0.02, 2.3), h.sub, h.x, 1.1, h.z, h.st, 'trough', { i }));
  // BIG Abadis Med flag in the front yard by Golshan 19 (boss request): tall pole + waving teal flag with wordmark
  const FLAG = { x: -10, z: 23, h: 17, w: 8, fh: 4.6 };
  {
    const pm = new THREE.LineBasicMaterial({ color: 0x0e8c8c, transparent: true, opacity: 0.9 });
    const pole = new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.CylinderGeometry(0.12, 0.16, FLAG.h, 8)), pm);
    pole.position.set(FLAG.x, FLAG.h / 2, FLAG.z); scene.add(pole);
    const base = new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.CylinderGeometry(0.9, 1.1, 0.5, 8)), pm);
    base.position.set(FLAG.x, 0.25, FLAG.z); scene.add(base);
    const fin = new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.SphereGeometry(0.28, 8, 6)), pm);
    fin.position.set(FLAG.x, FLAG.h + 0.25, FLAG.z); scene.add(fin);
  }
  const flagCv = document.createElement('canvas'); flagCv.width = 1024; flagCv.height = 590;
  {
    const c = flagCv.getContext('2d');
    c.fillStyle = 'rgba(14,140,140,0.82)'; c.fillRect(0, 0, 1024, 590);
    c.strokeStyle = 'rgba(255,255,255,0.9)'; c.lineWidth = 10; c.strokeRect(18, 18, 988, 554);
    // real site logo (same asset as header), drawn once loaded
    const img = new Image();
    img.onload = () => { const w = 860, h = w * 79.16 / 165.57; c.drawImage(img, 512 - w / 2, 295 - h / 2, w, h); flagTex.needsUpdate = true; };
    img.src = new URL('../img/abadis-logo-white.svg', import.meta.url).href;
  }
  const flagTex = new THREE.CanvasTexture(flagCv);
  const flagGeo = new THREE.PlaneGeometry(FLAG.w, FLAG.fh, 24, 8); flagGeo.translate(FLAG.w / 2, 0, 0);
  const flag0 = flagGeo.attributes.position.array.slice();
  const flagMesh = new THREE.Mesh(flagGeo, new THREE.MeshBasicMaterial({ map: flagTex, transparent: true, side: THREE.DoubleSide, depthWrite: false }));
  const flagWire = new THREE.LineSegments(new THREE.WireframeGeometry(flagGeo), new THREE.LineBasicMaterial({ color: 0x7fe3e3, transparent: true, opacity: 0.25 }));
  const flagG = new THREE.Group(); flagG.add(flagMesh, flagWire);
  flagG.position.set(FLAG.x + 0.15, FLAG.h - FLAG.fh / 2 - 0.2, FLAG.z); scene.add(flagG);
  function animateFlag(time) {
    const a = flagGeo.attributes.position;
    for (let i = 0; i < a.count; i++) {
      const x = flag0[i * 3], k = x / FLAG.w;
      a.array[i * 3 + 2] = reduce ? 0.25 * k : k * (0.55 * Math.sin(x * 0.9 - time * 2.6) + 0.15 * Math.sin(flag0[i * 3 + 1] * 1.3 - time * 1.7));
    }
    a.needsUpdate = true;
    flagWire.geometry.dispose(); flagWire.geometry = new THREE.WireframeGeometry(flagGeo);
  }
  animateFlag(0);

  function animateMachines(time, st) {
    movers.forEach((m) => {
      const on = !reduce && m.st === st, l = m.l;
      if (m.kind === 'hop') { const k = on ? Math.sin(time * 3 + m.i * 0.7) : 0; l.scale.set(1 + 0.12 * k, 1, 1 + 0.12 * k); l.position.y = m.y0 + (on ? 0.06 * k : 0); }
      else if (m.kind === 'light') l.visible = on ? ((time * 1.6 + m.i * 0.31) % 1) < 0.55 : false;
      else if (m.kind === 'roll') l.rotation.x = on ? (m.i % 2 ? -1 : 1) * time * 4 : 0;
      else if (m.kind === 'trough') { const c = ((time + m.i * 1.3) % 5) / 5; l.rotation.z = on ? 0.35 * (smooth((c - 0.6) / 0.15) - smooth((c - 0.85) / 0.15)) : 0; }
    });
  }

  // 3D Target Beacon Ring at the active machine sub-node
  const beaconGroup = new THREE.Group();
  const beaconMat = new THREE.LineBasicMaterial({ color: 0xffb300, transparent: true, opacity: 0.95 });
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

  // Product journey: glowing dot + simple tube-set silhouette on a dotted floor path
  // injection -> mold demold -> extruder -> hall 3 racks -> forklift -> south gate -> Golshan 19
  const PATH = [V0(-9.4, -11), V0(-9.4, -2), V0(1.35, -2), V0(1.35, 4), V0(-2, 4), V0(-2, -15), V0(2.2, -15), V0(8, -15), V0(8, -4), V0(11.5, -4), V0(11.5, 8), V0(11.5, 13.5), V0(11.5, 27)];
  function V0(x, z) { return new THREE.Vector3(x, 0.14, z); }
  const pathCurve = new THREE.CatmullRomCurve3(PATH, false, 'catmullrom', 0.05);
  const pathLen = pathCurve.getLength();
  const pathPts = pathCurve.getSpacedPoints(Math.round(pathLen * 2));
  const pathGeo = new THREE.BufferGeometry().setFromPoints(pathPts);
  const pathMat = new THREE.PointsMaterial({ color: 0x7ff6ff, size: 0.22, transparent: true, opacity: 0.0, depthWrite: false });
  const pathDots = new THREE.Points(pathGeo, pathMat); scene.add(pathDots);
  const trailGeo = new THREE.BufferGeometry().setFromPoints(pathPts);
  const trailMat = new THREE.PointsMaterial({ color: 0xffffff, size: 0.36, transparent: true, opacity: 0.95, depthWrite: false });
  const trail = new THREE.Points(trailGeo, trailMat); trail.geometry.setDrawRange(0, 0); scene.add(trail);
  const glowTex = (() => { const cv = document.createElement('canvas'); cv.width = cv.height = 64; const x = cv.getContext('2d');
    const g = x.createRadialGradient(32, 32, 0, 32, 32, 32); g.addColorStop(0, 'rgba(255,255,255,1)'); g.addColorStop(0.25, 'rgba(160,250,255,.9)'); g.addColorStop(1, 'rgba(0,229,255,0)');
    x.fillStyle = g; x.fillRect(0, 0, 64, 64); return new THREE.CanvasTexture(cv); })();
  const product = new THREE.Group(); scene.add(product);
  const glow = new THREE.Sprite(new THREE.SpriteMaterial({ map: glowTex, color: 0xffffff, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending }));
  glow.scale.set(3.6, 3.6, 1); glow.position.y = 0.9; product.add(glow);
  const pMat = new THREE.MeshBasicMaterial({ color: 0xe9fdff, transparent: true, opacity: 0.95 });
  const pEdge = new THREE.LineBasicMaterial({ color: 0x00e5ff });
  // simple silhouette: small chamber + tube loop (generic medical tubing set)
  const chamber = new THREE.Mesh(new THREE.CylinderGeometry(0.16, 0.16, 0.5, 14), pMat); chamber.position.y = 0.9; product.add(chamber);
  const loop = new THREE.Mesh(new THREE.TorusGeometry(0.32, 0.045, 8, 24), pMat); loop.position.set(0, 0.9, 0); loop.rotation.y = Math.PI / 2; product.add(loop);
  product.add(new THREE.LineSegments(new THREE.EdgesGeometry(chamber.geometry), pEdge)).position.y = 0.9;
  // scroll t (station i centred at i+0.5) -> path fraction; 0 inj, ~.23 mold, ~.5 extruder, ~.7 racks, 1 street
  const PKEY = [[0.5, 0], [2.5, 0.24], [3.5, 0.5], [4.5, 0.7], [5.2, 1]];
  function pathFrac(t) {
    if (t <= PKEY[0][0]) return 0;
    for (let k = 1; k < PKEY.length; k++) if (t <= PKEY[k][0]) { const [a, fa] = PKEY[k - 1], [b, fb] = PKEY[k]; return fa + (fb - fa) * smooth((t - a) / (b - a)); }
    return 1;
  }
  let prodF = 0;
  function animateProduct(time, s, dt) {
    const tgt = explore ? (reduce ? 0.5 : (time * 0.04) % 1) : pathFrac((s - 0.25) / 0.15);
    prodF += (tgt - prodF) * (reduce || explore ? 1 : 1 - Math.exp(-dt / 0.35));
    const vis = explore ? 1 : smooth((s - 0.2) / 0.05);
    pathMat.opacity = 0.55 * vis; trailMat.opacity = 0.95 * vis; product.visible = vis > 0.02;
    const p = pathCurve.getPointAt(Math.min(1, Math.max(0, prodF)));
    product.position.set(p.x, 0, p.z);
    const bob = reduce ? 0 : Math.sin(time * 3) * 0.08;
    chamber.position.y = loop.position.y = 0.9 + bob; product.children[3].position.y = 0.9 + bob;
    if (!reduce) loop.rotation.z = time * 1.2;
    glow.material.opacity = vis * (0.8 + (reduce ? 0 : 0.2 * Math.sin(time * 5)));
    trail.geometry.setDrawRange(0, Math.round(prodF * pathPts.length));
  }

  /* ---------- theme sync ---------- */
  function applyTheme() {
    const t = document.documentElement.dataset.theme || 'light';
    const dark = t !== 'light';
    // light: pale ground + brand teal wire; dark/noir: deep-teal night (#0A1518) cyan wire. Amber active in all.
    uniforms.uBase.value.set(dark ? '#4dd0e1' : '#0a666b');
    uniforms.uHi.value.set(dark ? '#00e5ff' : '#0e8c8c');
    uniforms.uCoral.value.set(dark ? '#ffb300' : '#f29a00');
    uniforms.uFill.value.set(dark ? '#08333d' : '#b9e2e2');
    uniforms.uFillMix.value = dark ? 0.35 : 0.12;
    ringMats.forEach((m) => { m.color.set(dark ? '#162e35' : '#0e8c8c'); });
    pathMat.color.set(dark ? '#7ff6ff' : '#0e8c8c');
    trailMat.color.set(dark ? '#ffffff' : '#e08a00');
    pMat.color.set(dark ? '#e9fdff' : '#ffffff');
    pEdge.color.set(dark ? '#00e5ff' : '#066565');
    glow.material.color.set(dark ? '#ffffff' : '#ffb300');
    glow.material.blending = dark ? THREE.AdditiveBlending : THREE.NormalBlending;
    glow.material.needsUpdate = true;
  }
  applyTheme();
  try { // system mode: follow OS when user hasn't picked a theme
    const mq = matchMedia('(prefers-color-scheme: dark)');
    mq.addEventListener('change', (e) => { let saved = null; try { saved = localStorage.getItem('abadis-theme'); } catch (_) {}
      if (!saved) document.documentElement.dataset.theme = e.matches ? 'dark' : 'light'; });
  } catch (_) {}
  document.addEventListener('themechange', applyTheme);
  new MutationObserver(applyTheme).observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });

  /* ---------- stations & sub-nodes ---------- */
  const V3 = (x, y, z) => new THREE.Vector3(x, y, z);
  const VIEWS = [
    { p: V3(-31, 12, 6), t: V3(-9.4, 1.8, -11) },
    { p: V3(-24, 14.5, 8.5), t: V3(-9.8, 6.6, -2.5) }, // close 3/4 onto the PU assembly mezzanine
    { p: V3(20, 8, 11), t: V3(2.5, 2, 5) },
    { p: V3(17, 5.2, -7), t: V3(2.2, 0.9, -15) }, // low 3/4 onto the extruder lines, under the cleanroom deck
    { p: V3(19, 13.5, -2), t: V3(2.2, 6.9, -13.2) }, // own station: high 3/4 into the upstairs Class 100k cleanroom
    { p: V3(27, 9.5, 13), t: V3(11.5, 2.4, -4) },
  ];
  const STREET_M = V3(-12, 0.2, 30.2); // street callout anchor on phones
  const LBL = [V3(-9.4, 6, -12), V3(-9.25, 11.4, 3), V3(2.25, 8, 5), V3(1.9, 4.6, -18.5), V3(2.25, 11.4, -11), V3(11.5, 8.4, -4), V3(0, 8.2, 17.6), V3(12, 4.5, 28)];
  // Close camera for a sub-node on the upper floor (cleanroom), blended in during that station's hold
  const SUBCAM = { 23: { p: V3(-34, 17, 6), t: V3(-11, 6.4, -15.5) } };
  const NST = VIEWS.length, LAST = NST - 1, STEP = 0.75 / (NST + 0.5); // scroll span per station
  let subCamK = 0, autoSub = -1;
  const HOLD = 0.3; // each station dwells ~60% of its scroll span before the camera moves on
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

  let outroF = 0, sT = 0, sS = 0, explore = false, tween = null, lastIdx = -2, activeStation = 0, activeSubIdx = 0, visible = true;
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
    if (i < NST) {
      if (explore) flyTo(i, 0);
      else goStation(i);
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
  const stationScroll = (i) => { const m = sec.offsetHeight - innerHeight; return sec.getBoundingClientRect().top + scrollY + m * (0.25 + STEP * (i + 0.5)); };
  const goStation = (i) => { sT = Math.min(1, Math.max(0, 0.25 + STEP * (i + 0.5))); const y = stationScroll(i); (document.scrollingElement || document.documentElement).scrollTo({ top: y, behavior: reduce ? 'auto' : 'smooth' }); };

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
    else goStation(i);
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
  let introK = reduce ? 1 : 0; // 0 -> 1 over the first ~3.2 s: soft auto-glide into the opening view
  function aerial(s, out, tgt) {
    const k = Math.min(1, s / 0.25), g = 1 - introK, a = -0.75 + 0.9 * k - 0.35 * g, R = ((camera.aspect < 1 ? 118 : 82) - 10 * k) * (1 + 0.28 * g);
    out.set(Math.sin(a) * R, 40 - 6 * k + 22 * g, Math.cos(a) * R + 4); tgt.set(0, camera.aspect < 1 ? 14 - 6 * k : 16 - 4 * k, -4);
  }
  function frame() {
    requestAnimationFrame(frame);
    if (!visible) return;
    const dt = Math.min(0.1, clock.getDelta());
    const time = clock.elapsedTime;
    // Framerate-independent damping; heavier time constant (~1.0 s) for a smoother, less snappy glide between stations
    if (!reduce) { const it = Math.min(1, time / 3.2); introK = it * it * it * (it * (it * 6 - 15) + 10); }
    // Heavier damping during the opening seconds so early scroll never snaps
    const kS = reduce ? 1 : 1 - Math.exp(-dt / (1.0 + 0.9 * (1 - introK)));
    const kF = reduce ? 1 : 1 - Math.exp(-dt / 0.75);
    sS += (sT - sS) * kS;
    if (Math.abs(sT - sS) < 1e-5) sS = sT;
    const s = sS;
    const autoProg = Math.min(1.1, (time / 2.6) * 1.1);
    const prog = (explore || reduce) ? 1.1 : Math.max(autoProg, Math.min(1.1, (s / 0.17) * 1.1));
    uniforms.uProg.value = prog;
    ringMats.forEach((m, i) => { m.opacity = 0.25 + 0.55 * Math.min(1, Math.max(0, prog - i * 0.06)); });

    // Pulse the 3D beacon ring
    beaconGroup.scale.setScalar(Math.max(0.001, 1 - outroF));
    if (beaconGroup.visible) {
      const pulse = reduce ? 1 : 1 + 0.12 * Math.sin(time * 4.0);
      beaconOuter.scale.set(pulse, 1, pulse);
    }

    animateWorkers(time);
    animateProduct(time, s, dt);
    if (!reduce) animateFlag(time);
    animateMachines(time, explore ? activeStation : lastIdx);

    // Filter demolding loop (6 s)
    PRESSES.forEach(([px, pz], k) => {
      const c = reduce ? 0.8 : ((time + k * 1.0) % 6) / 6, lift = smooth(c / 0.25) - smooth((c - 0.85) / 0.15);
      moldTops[k].position.set(px, 2.0 + lift * 1.6, pz);
      const out = smooth((c - 0.3) / 0.35), place = smooth((c - 0.65) / 0.15);
      // lift filter out of the opened mold and set it on the bed edge toward the aisle (x ~ 1.35)
      const dir = px < 1.35 ? 1 : -1;
      filters[k].position.set(px + dir * out * 0.9, 1.7 + Math.sin(out * Math.PI) * 1.6 * (1 - place) + lift * 0.2 * (1 - out) - place * 0.1, pz);
      filters[k].visible = c < 0.95 && c > 0.05;
    });

    subFocusOffset.lerp(targetSubFocus, kF);

    let idx = -1;
    outroF = 0;
    if (!explore) {
      const t = (s - 0.25) / STEP;
      if (t < 0) {
        aerial(s, pos, look);
        uniforms.uInStation.value = 0;
      } else {
        idx = Math.min(LAST, Math.floor(t));
        uniforms.uInStation.value = 1;
        // Keyframes: aerial at t=0, station i centred at t=i+0.5; ease across the whole gap
        const u = t - 0.5;
        if (u < 0) {
          aerial(0.25, fromP, fromT); const f = smooth(t / (0.5 - HOLD));
          pos.lerpVectors(fromP, VIEWS[0].p, f); look.lerpVectors(fromT, VIEWS[0].t, f);
        } else {
          const a = Math.min(LAST, Math.floor(u)), b = Math.min(LAST, a + 1), f = smooth((u - a - HOLD) / (1 - 2 * HOLD));
          pos.lerpVectors(VIEWS[a].p, VIEWS[b].p, f); look.lerpVectors(VIEWS[a].t, VIEWS[b].t, f);
        }
        look.add(subFocusOffset);
        // Extruder station: second half of the hold auto-switches to the Class 100k cleanroom upstairs
        const sc = SUBCAM[uniforms.uActiveSub.value];
        const inHold = 1 - smooth((Math.abs(u - idx) - 0.3) / 0.25);
        subCamK += (((sc && idx === activeStation) ? inHold : 0) - subCamK) * kF;
        if (sc && subCamK > 1e-3) { pos.lerp(sc.p, subCamK); look.lerp(sc.t, subCamK); }
        if (camera.aspect < 1) { pos.add(tmp.copy(pos).sub(look).multiplyScalar(0.95 - 0.55 * subCamK)); pos.y += 6 - 3 * subCamK; }
        // Outro: after the last station, rise and pull back to the whole plant + Golshan 19 street, then hold
        outroF = smooth((u - LAST - 0.05) / 0.4);
        if (outroF > 0) {
          const ph = camera.aspect < 1;
          fromP.set(ph ? -6 : -16, ph ? 70 : 34, ph ? 112 : 70); fromT.set(0, ph ? 2 : 4, ph ? 10 : 12);
          // gentle arc: lift first, then glide out
          const fy = smooth(outroF * 1.4), fx = outroF;
          pos.set(pos.x + (fromP.x - pos.x) * fx, pos.y + (fromP.y - pos.y) * fy, pos.z + (fromP.z - pos.z) * fx);
          look.lerp(fromT, outroF);
          uniforms.uInStation.value = 1 - outroF;
        }
      }
      camera.position.copy(pos); camera.lookAt(look);
      intro.style.opacity = String(Math.max(0, 1 - Math.max(0, s - 0.19) / 0.045));
      intro.style.visibility = s > 0.235 ? 'hidden' : 'visible';
      bar.style.height = (s * 100) + '%';
      dock.classList.toggle('on', idx >= 0);
      sec.classList.toggle('is-outro', outroF > 0.6);
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
    const introBot = (innerWidth <= 760 && idx < 0 && s < 0.22 && !explore) ? intro.getBoundingClientRect().bottom - sr.top + 8 : 0;
    const topSafe = Math.max(dockBot, introBot, narrow ? 64 : 80), botSafe = h - (narrow ? 84 : 90);
    const showHallLabels = (explore || idx < 0 || outroF > 0.6) && prog > 0.75;
    const items = [];
    lbls.forEach((c, i) => {
      const act = i === idx && outroF < 0.6;
      c.el.classList.toggle('act', act); c.dot.classList.toggle('act', act); c.path.classList.toggle('act', act);
      items.push({ c, p: (i === NST + 1 && narrow) ? STREET_M : LBL[i], on: showHallLabels && (explore || i < NST || i === NST + 1), pri: act ? 3 : 1 });
    });
    currentPinEls.forEach((c, k) => items.push({ c, p: c.pos, on: idx >= 0 && outroF < 0.4, pri: k === activeSubIdx ? 4 : 2 }));
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

    // Roof fade target: on inside a station / explore, off on aerial + outro
    const roofT = (explore || idx >= 0) ? (explore ? 1 : 1 - outroF) : 0;
    uniforms.uRoof.value += (roofT - uniforms.uRoof.value) * (reduce ? 1 : 1 - Math.exp(-dt / 0.45));
    const upT = ((idx === 1 || idx === 4) && outroF < 0.5) ? 1 : 0;
    uniforms.uUpper.value += (upT - uniforms.uUpper.value) * (reduce ? 1 : 1 - Math.exp(-dt / 0.4));
    const hideT = ((idx >= 2 && idx <= 4) && outroF < 0.5) ? 1 : 0;
    uniforms.uHideSt.value += (hideT - uniforms.uHideSt.value) * (reduce ? 1 : 1 - Math.exp(-dt / 0.35));
    uniforms.uPulse.value = reduce ? 0.5 : 0.5 + 0.5 * Math.sin(time * 3.2);
    renderer.render(scene, camera);
  }
  frame();
}
