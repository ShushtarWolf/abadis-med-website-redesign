/**
 * Abadis 1L disposable suction liner — form study.
 * Envelope from the product drawing: diameter 11 cm, height 15.5 cm
 * (کیسه ساکشن ۱ لیتری، نقشهٔ ابعاد محصول).
 * Lid, tether, filter cage and gelling pouch follow the photographed unit.
 * Units are millimetres. Y is up. Tether is on −X. Front is +Z.
 */
import * as THREE from "three";

export const SPEC = {
  nameFa: "کیسه ساکشن یکبار مصرف ۱ لیتری",
  nameEn: "1L Disposable Suction Liner",
  diameterMm: 110,
  heightMm: 155,
};

const TEAL = 0x0e8490;
const TEAL_DEEP = 0x0b6c76;
const TEAL_DARK = 0x084f58;
const BORE = 0x06282c;

function smoothstep(e0, e1, x) {
  const t = Math.min(1, Math.max(0, (x - e0) / (e1 - e0)));
  return t * t * (3 - 2 * t);
}

function gauss(x, z, cx, cz, s) {
  const dx = x - cx;
  const dz = z - cz;
  return Math.exp(-(dx * dx + dz * dz) / (2 * s * s));
}

function lidHeight(x, z) {
  const r = Math.hypot(x, z);
  let y = 151.15;
  y += smoothstep(43.5, 49.6, r) * 3.85;
  y -= gauss(x, z, 0.5, -1.5, 10.5) * 4.6;
  y += gauss(x, z, -1.5, -17.5, 8.2) * 1.7;
  y += gauss(x, z, 1.2, 16.5, 9) * 1.35;
  y += gauss(x, z, 26, -1, 6.2) * 0.85;
  return y;
}

function makeStipple() {
  const S = 512;
  const height = new Float32Array(S * S);
  let seed = 48271;
  const rand = () => (seed = (seed * 48271) % 2147483647) / 2147483647;
  for (let n = 0; n < 3400; n++) {
    const cx = rand() * S;
    const cy = rand() * S;
    const rad = 1.1 + rand() * 2.15;
    const amp = 0.28 + rand() * 0.72;
    const r = Math.ceil(rad);
    for (let y = -r; y <= r; y++) {
      for (let x = -r; x <= r; x++) {
        const d = Math.hypot(x, y) / rad;
        if (d >= 1) continue;
        const ix = (Math.floor(cx) + x + S) % S;
        const iy = (Math.floor(cy) + y + S) % S;
        const fall = Math.cos(d * Math.PI * 0.5);
        const i = iy * S + ix;
        height[i] = Math.min(1, height[i] + amp * fall * fall);
      }
    }
  }
  const blur = new Float32Array(S * S);
  for (let y = 0; y < S; y++) {
    for (let x = 0; x < S; x++) {
      let a = 0;
      a += height[y * S + x] * 4;
      a += height[y * S + ((x + 1) % S)];
      a += height[y * S + ((x - 1 + S) % S)];
      a += height[((y + 1) % S) * S + x];
      a += height[((y - 1 + S) % S) * S + x];
      blur[y * S + x] = a / 8;
    }
  }
  const ncan = document.createElement("canvas");
  ncan.width = ncan.height = S;
  const nctx = ncan.getContext("2d", { willReadFrequently: true });
  const img = nctx.createImageData(S, S);
  const strength = 4.2;
  for (let y = 0; y < S; y++) {
    for (let x = 0; x < S; x++) {
      const hl = blur[y * S + ((x - 1 + S) % S)];
      const hr = blur[y * S + ((x + 1) % S)];
      const hd = blur[((y + 1) % S) * S + x];
      const hu = blur[((y - 1 + S) % S) * S + x];
      let nx = (hl - hr) * strength;
      let ny = (hd - hu) * strength;
      let nz = 1;
      const len = Math.hypot(nx, ny, nz) || 1;
      nx /= len;
      ny /= len;
      nz /= len;
      const i = (y * S + x) * 4;
      img.data[i] = (nx * 0.5 + 0.5) * 255;
      img.data[i + 1] = (ny * 0.5 + 0.5) * 255;
      img.data[i + 2] = (nz * 0.5 + 0.5) * 255;
      img.data[i + 3] = 255;
    }
  }
  nctx.putImageData(img, 0, 0);
  const normal = new THREE.CanvasTexture(ncan);
  normal.wrapS = normal.wrapT = THREE.RepeatWrapping;
  normal.repeat.set(3.1, 4.0);
  normal.colorSpace = THREE.NoColorSpace;

  const rcan = document.createElement("canvas");
  rcan.width = rcan.height = S;
  const rctx = rcan.getContext("2d");
  const rimg = rctx.createImageData(S, S);
  for (let i = 0; i < S * S; i++) {
    const v = 168 - blur[i] * 70;
    const o = i * 4;
    rimg.data[o] = rimg.data[o + 1] = rimg.data[o + 2] = v;
    rimg.data[o + 3] = 255;
  }
  rctx.putImageData(rimg, 0, 0);
  const roughness = new THREE.CanvasTexture(rcan);
  roughness.wrapS = roughness.wrapT = THREE.RepeatWrapping;
  roughness.repeat.set(3.1, 4.0);
  roughness.colorSpace = THREE.NoColorSpace;

  const acan = document.createElement("canvas");
  acan.width = acan.height = S;
  const actx = acan.getContext("2d");
  const aimg = actx.createImageData(S, S);
  for (let i = 0; i < S * S; i++) {
    const hgt = blur[i];
    const v = 226 + hgt * 28;
    const o = i * 4;
    aimg.data[o] = aimg.data[o + 1] = aimg.data[o + 2] = Math.max(180, Math.min(255, v));
    aimg.data[o + 3] = 255;
  }
  actx.putImageData(aimg, 0, 0);
  const albedo = new THREE.CanvasTexture(acan);
  albedo.wrapS = albedo.wrapT = THREE.RepeatWrapping;
  albedo.repeat.set(3.1, 4.0);
  albedo.colorSpace = THREE.SRGBColorSpace;
  return { normal, roughness, albedo };
}

function lathe(points, segments) {
  const geo = new THREE.LatheGeometry(
    points.map((p) => new THREE.Vector2(p[0], p[1])),
    segments
  );
  geo.computeVertexNormals();
  return geo;
}

function lidDeckGeometry() {
  const nR = 28;
  const nT = 80;
  const R = 49.85;
  const positions = [];
  const indices = [];
  positions.push(0, lidHeight(0, 0), 0);
  const vid = (i, j) => 1 + (i - 1) * nT + ((j % nT) + nT) % nT;
  for (let i = 1; i <= nR; i++) {
    const r = (i / nR) * R;
    for (let j = 0; j < nT; j++) {
      const th = (j / nT) * Math.PI * 2;
      const x = Math.cos(th) * r;
      const z = Math.sin(th) * r;
      positions.push(x, lidHeight(x, z), z);
    }
  }
  for (let j = 0; j < nT; j++) indices.push(0, vid(1, j), vid(1, j + 1));
  for (let i = 1; i < nR; i++) {
    for (let j = 0; j < nT; j++) {
      const a = vid(i, j);
      const b = vid(i, j + 1);
      const d = vid(i + 1, j);
      const c = vid(i + 1, j + 1);
      indices.push(a, d, b, d, c, b);
    }
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute("position", new THREE.Float32BufferAttribute(positions, 3));
  geo.setIndex(indices);
  geo.computeVertexNormals();
  return geo;
}

function arcShell(rIn, rOut, y0, y1, a0, a1, segs) {
  const pos = [];
  const idx = [];
  const v = (x, y, z) => {
    pos.push(x, y, z);
    return pos.length / 3 - 1;
  };
  const ring = [];
  for (let i = 0; i <= segs; i++) {
    const t = a0 + ((a1 - a0) * i) / segs;
    const s = Math.sin(t);
    const c = Math.cos(t);
    ring.push([
      v(rOut * s, y0, rOut * c),
      v(rOut * s, y1, rOut * c),
      v(rIn * s, y1, rIn * c),
      v(rIn * s, y0, rIn * c),
    ]);
  }
  for (let i = 0; i < segs; i++) {
    const A = ring[i];
    const B = ring[i + 1];
    idx.push(A[0], B[0], A[1], A[1], B[0], B[1]);
    idx.push(A[2], A[3], B[2], B[2], A[3], B[3]);
    idx.push(A[1], B[1], A[2], A[2], B[1], B[2]);
    idx.push(A[3], B[3], A[0], A[0], B[3], B[0]);
  }
  const S0 = ring[0];
  const E = ring[ring.length - 1];
  idx.push(S0[0], S0[1], S0[3], S0[1], S0[2], S0[3]);
  idx.push(E[0], E[3], E[1], E[1], E[3], E[2]);
  const geo = new THREE.BufferGeometry();
  geo.setAttribute("position", new THREE.Float32BufferAttribute(pos, 3));
  geo.setIndex(idx);
  geo.computeVertexNormals();
  return geo;
}

function makePort(profile) {
  const geo = lathe(profile, 36);
  return geo;
}

const PATIENT_PROFILE = [
  [0.4, 0.6],
  [11.6, 0],
  [10.4, 2.4],
  [7.6, 9],
  [6.55, 18],
  [6.85, 27.2],
  [5.15, 27.2],
  [4.55, 18],
  [4.15, 6],
  [0.4, 2.2],
];

const VACUUM_PROFILE = [
  [0.35, 0.5],
  [7.5, 0],
  [6.7, 1.8],
  [6.15, 16],
  [6.45, 25.4],
  [4.7, 25.4],
  [4.25, 14],
  [4.05, 2.2],
  [0.35, 1.6],
];

const AUX_PROFILE = [
  [0.25, 0.4],
  [5.15, 0],
  [4.45, 1.4],
  [4.05, 9.5],
  [4.3, 13.2],
  [2.85, 13.2],
  [2.45, 7],
  [0.25, 1.2],
];

function pointPort(group, dir) {
  const q = new THREE.Quaternion().setFromUnitVectors(
    new THREE.Vector3(0, 1, 0),
    dir.clone().normalize()
  );
  group.quaternion.copy(q);
}

export function createProduct() {
  const root = new THREE.Group();
  root.name = "suction-bag-1l";
  const stipple = makeStipple();
  const clipPlane = new THREE.Plane(new THREE.Vector3(-0.86, 0, -0.51).normalize(), 520);

  const bagStudio = new THREE.MeshPhysicalMaterial({
    color: 0xffffff,
    map: stipple.albedo,
    roughness: 0.62,
    metalness: 0,
    transmission: 0.64,
    thickness: 1.8,
    ior: 1.46,
    attenuationColor: new THREE.Color(0xb7cfd2),
    attenuationDistance: 24,
    clearcoat: 0.16,
    clearcoatRoughness: 0.7,
    normalMap: stipple.normal,
    normalScale: new THREE.Vector2(1.65, 1.65),
    roughnessMap: stipple.roughness,
    side: THREE.DoubleSide,
    transparent: true,
    depthWrite: false,
    envMapIntensity: 0.55,
    clippingPlanes: [clipPlane],
    clipShadows: true,
  });
  const bagCad = new THREE.MeshStandardMaterial({
    color: 0xe7f4f4,
    roughness: 0.78,
    metalness: 0,
    transparent: true,
    opacity: 0.4,
    side: THREE.DoubleSide,
    depthWrite: false,
    clippingPlanes: [clipPlane],
    clipShadows: true,
  });
  const lidMat = new THREE.MeshPhysicalMaterial({
    color: TEAL,
    roughness: 0.34,
    metalness: 0.02,
    clearcoat: 0.46,
    clearcoatRoughness: 0.32,
    envMapIntensity: 0.72,
  });
  const lidCad = new THREE.MeshStandardMaterial({
    color: 0x0d7d88,
    roughness: 0.46,
    metalness: 0.02,
  });
  const filterMat = new THREE.MeshPhysicalMaterial({
    color: TEAL_DEEP,
    roughness: 0.4,
    metalness: 0.03,
    clearcoat: 0.2,
    clearcoatRoughness: 0.4,
    transmission: 0.08,
    thickness: 1.2,
    transparent: true,
    envMapIntensity: 0.4,
  });
  const filterCad = new THREE.MeshStandardMaterial({
    color: TEAL_DARK,
    roughness: 0.5,
    metalness: 0.02,
  });
  const mediaMat = new THREE.MeshStandardMaterial({
    color: 0x083f46,
    roughness: 0.72,
    transparent: true,
    opacity: 0.55,
    side: THREE.DoubleSide,
    depthWrite: false,
  });
  const pouchMat = new THREE.MeshStandardMaterial({
    color: 0xf6f5f2,
    roughness: 0.9,
    metalness: 0,
  });
  const pouchCad = new THREE.MeshStandardMaterial({
    color: 0xfbfbfa,
    roughness: 0.92,
  });
  const boreMat = new THREE.MeshStandardMaterial({
    color: BORE,
    roughness: 0.62,
    side: THREE.DoubleSide,
  });
  const inkMat = new THREE.MeshBasicMaterial({
    color: 0x16383c,
    polygonOffset: true,
    polygonOffsetFactor: -2,
    polygonOffsetUnits: -2,
  });

  const bagMeshes = [];
  const lidMeshes = [];
  const filterMeshes = [];
  const pouchMeshes = [];
  const inkMeshes = [];
  const anchors = {};

  function addAnchor(parent, name, x, y, z) {
    const o = new THREE.Object3D();
    o.name = name;
    o.position.set(x, y, z);
    parent.add(o);
    anchors[name] = o;
    return o;
  }

  function addInkMesh(parent, geo, x, y, z) {
    const m = new THREE.Mesh(geo, inkMat);
    m.position.set(x, y, z);
    m.castShadow = false;
    m.receiveShadow = false;
    m.renderOrder = 8;
    m.userData.ink = true;
    parent.add(m);
    inkMeshes.push(m);
    return m;
  }

  const bag = new THREE.Group();
  bag.name = "liner";
  root.add(bag);
  const bagGeo = lathe(
    [
      [0, 1.5],
      [44.8, 1.5],
      [47.4, 0.15],
      [48.7, 3.4],
      [49.6, 18],
      [51.1, 62],
      [52.5, 108],
      [53.55, 130],
      [54.15, 138.5],
      [54.65, 142.2],
      [53.85, 143.35],
      [53.15, 142.15],
    ],
    72
  );
  const bagMesh = new THREE.Mesh(bagGeo, bagStudio);
  bagMesh.castShadow = true;
  bagMesh.receiveShadow = true;
  bagMesh.renderOrder = 3;
  bagMesh.name = "liner-shell";
  bag.add(bagMesh);
  bagMeshes.push(bagMesh);

  const bagRings = [8, 32, 62, 96, 128, 140];
  const bagRadii = [48.2, 49.8, 51.1, 52.4, 53.5, 54.3];
  bagRings.forEach((y, i) => {
    const ring = addInkMesh(bag, new THREE.TorusGeometry(bagRadii[i], 0.42, 6, 72), 0, y, 0);
    ring.rotation.x = Math.PI / 2;
  });
  for (let k = 0; k < 8; k++) {
    const a = (k / 8) * Math.PI * 2;
    const pts = [
      [47.6, 1],
      [49.2, 16],
      [51.0, 60],
      [52.6, 110],
      [54.2, 140],
    ].map(([r, y]) => new THREE.Vector3(Math.cos(a) * r, y, Math.sin(a) * r));
    const curve = new THREE.CatmullRomCurve3(pts);
    addInkMesh(bag, new THREE.TubeGeometry(curve, 16, 0.32, 5, false), 0, 0, 0);
  }
  addAnchor(bag, "body", 0, 78, 54.2);
  addAnchor(bag, "dimL", -55, 136, 0);
  addAnchor(bag, "dimR", 55, 136, 0);
  addAnchor(bag, "dimBot", 64, 0, 0);
  addAnchor(bag, "dimTop", 64, 155, 0);

  const pouch = new THREE.Group();
  pouch.name = "gelling-pouch";
  root.add(pouch);
  const pouchBody = new THREE.Mesh(new THREE.SphereGeometry(1, 28, 18), pouchMat);
  pouchBody.scale.set(17.5, 6.4, 12.2);
  pouchBody.castShadow = true;
  pouchBody.receiveShadow = true;
  pouch.add(pouchBody);
  pouchMeshes.push(pouchBody);
  const pouchFold = new THREE.Mesh(new THREE.SphereGeometry(1, 20, 14), pouchMat);
  pouchFold.scale.set(8.5, 3.6, 6.4);
  pouchFold.position.set(-9.5, 1.6, 2.4);
  pouchFold.rotation.z = 0.35;
  pouch.add(pouchFold);
  pouchMeshes.push(pouchFold);
  const pouchFold2 = new THREE.Mesh(new THREE.SphereGeometry(1, 18, 12), pouchMat);
  pouchFold2.scale.set(6.2, 2.8, 5);
  pouchFold2.position.set(10, 1.1, -3);
  pouch.add(pouchFold2);
  pouchMeshes.push(pouchFold2);
  pouch.position.set(2.5, 8.4, 5.5);
  pouch.rotation.y = 0.45;
  const pouchBaseY = pouch.position.y;
  addAnchor(pouch, "pouch", 0, 4, 10);

  const filter = new THREE.Group();
  filter.name = "filter";
  root.add(filter);
  const cageH = 52;
  const cageR = 12.2;
  const cageBottom = 86;
  function addFilterMesh(geo, mat) {
    const m = new THREE.Mesh(geo, mat);
    m.castShadow = true;
    m.receiveShadow = true;
    filter.add(m);
    filterMeshes.push(m);
    return m;
  }
  const media = addFilterMesh(
    new THREE.CylinderGeometry(9.2, 9.2, cageH - 6, 28, 1, true),
    mediaMat
  );
  media.position.y = cageBottom + cageH / 2;
  for (let i = 0; i < 10; i++) {
    const a = (i / 10) * Math.PI * 2;
    const rib = addFilterMesh(new THREE.BoxGeometry(2.15, cageH - 2, 1.35), filterMat);
    rib.position.set(Math.cos(a) * cageR, cageBottom + cageH / 2, Math.sin(a) * cageR);
    rib.lookAt(0, rib.position.y, 0);
  }
  const topRing = addFilterMesh(new THREE.TorusGeometry(cageR, 1.15, 8, 32), filterMat);
  topRing.rotation.x = Math.PI / 2;
  topRing.position.y = cageBottom + cageH - 1;
  const botRing = addFilterMesh(new THREE.TorusGeometry(cageR, 1.15, 8, 32), filterMat);
  botRing.rotation.x = Math.PI / 2;
  botRing.position.y = cageBottom + 1;
  const seat = addFilterMesh(new THREE.CylinderGeometry(8.4, 10.4, 3.2, 28), filterMat);
  seat.position.y = cageBottom + 3.2;
  const floatBall = addFilterMesh(new THREE.SphereGeometry(6.1, 24, 16), filterMat);
  floatBall.position.y = cageBottom + 16;
  const neck = addFilterMesh(new THREE.CylinderGeometry(6.4, 7.2, 12, 24), filterMat);
  neck.position.y = cageBottom + cageH + 5;
  addInkMesh(filter, new THREE.TorusGeometry(cageR + 0.2, 0.28, 5, 40), 0, cageBottom + cageH - 1, 0).rotation.x =
    Math.PI / 2;
  addInkMesh(filter, new THREE.TorusGeometry(cageR + 0.2, 0.28, 5, 40), 0, cageBottom + 1, 0).rotation.x =
    Math.PI / 2;
  addAnchor(filter, "filter", cageR + 2, cageBottom + cageH * 0.55, 0);

  const lid = new THREE.Group();
  lid.name = "lid";
  root.add(lid);

  const collar = new THREE.Mesh(
    lathe(
      [
        [53.15, 129.2],
        [55.0, 129.2],
        [55.0, 141.7],
        [52.45, 145.5],
        [52.62, 149.15],
        [49.55, 149.15],
        [49.7, 144.8],
        [53.25, 141.2],
        [53.15, 129.35],
      ],
      72
    ),
    lidMat
  );
  collar.castShadow = true;
  collar.receiveShadow = true;
  lid.add(collar);
  lidMeshes.push(collar);

  const slotCenters = [Math.PI / 4, (3 * Math.PI) / 4, (5 * Math.PI) / 4, (7 * Math.PI) / 4];
  const slotW = 0.32;
  for (let i = 0; i < 4; i++) {
    const a1 = slotCenters[i] + slotW / 2;
    const a2 = slotCenters[(i + 1) % 4] + Math.PI * 2 - slotW / 2;
    const start = a1;
    const end = i === 3 ? slotCenters[0] + Math.PI * 2 - slotW / 2 : a2;
    const arc = new THREE.Mesh(arcShell(49.55, 52.62, 149.15, 155, start, end, 18), lidMat);
    arc.castShadow = true;
    arc.receiveShadow = true;
    lid.add(arc);
    lidMeshes.push(arc);
    const mid = (slotCenters[i] + Math.PI * 2) % (Math.PI * 2);
    const slot = new THREE.Mesh(new THREE.BoxGeometry(15.5, 5.4, 3.4), boreMat);
    const sr = 51.3;
    slot.position.set(Math.sin(mid) * sr, 152.05, Math.cos(mid) * sr);
    slot.lookAt(0, 152.05, 0);
    lid.add(slot);
    lidMeshes.push(slot);
    const slotTop = new THREE.Mesh(new THREE.BoxGeometry(14.2, 1.15, 4.2), boreMat);
    slotTop.position.set(Math.sin(mid) * 50.6, 154.55, Math.cos(mid) * 50.6);
    slotTop.lookAt(Math.sin(mid) * 80, 154.55, Math.cos(mid) * 80);
    lid.add(slotTop);
    lidMeshes.push(slotTop);
  }

  const deck = new THREE.Mesh(lidDeckGeometry(), lidMat);
  deck.castShadow = true;
  deck.receiveShadow = true;
  deck.name = "deck";
  lid.add(deck);
  lidMeshes.push(deck);
  addInkMesh(lid, new THREE.TorusGeometry(55, 0.38, 6, 80), 0, 135, 0).rotation.x = Math.PI / 2;
  addInkMesh(lid, new THREE.TorusGeometry(52.5, 0.32, 6, 80), 0, 155, 0).rotation.x = Math.PI / 2;
  for (const rad of [18, 32, 44]) {
    const pts = [];
    for (let j = 0; j <= 72; j++) {
      const th = (j / 72) * Math.PI * 2;
      const x = Math.cos(th) * rad;
      const z = Math.sin(th) * rad;
      pts.push(new THREE.Vector3(x, lidHeight(x, z) + 0.25, z));
    }
    addInkMesh(lid, new THREE.BufferGeometry().setFromPoints(pts), 0, 0, 0);
    inkMeshes[inkMeshes.length - 1].material = new THREE.LineBasicMaterial({ color: 0x16383c });
    // The last call used Mesh with a line geometry — replace with a real line below.
  }

  function placePort(profile, x, z, dir, mat) {
    const g = new THREE.Group();
    const shell = new THREE.Mesh(makePort(profile), mat);
    shell.castShadow = true;
    shell.receiveShadow = true;
    g.add(shell);
    lidMeshes.push(shell);
    const y = lidHeight(x, z) - 0.6;
    g.position.set(x, y, z);
    pointPort(g, dir);
    lid.add(g);
    return g;
  }

  const patient = placePort(
    PATIENT_PROFILE,
    1.2,
    16.2,
    new THREE.Vector3(0.08, 1, 1),
    lidMat
  );
  const vacuum = placePort(
    VACUUM_PROFILE,
    -2.2,
    -17.2,
    new THREE.Vector3(-0.12, 1, -1),
    lidMat
  );
  const aux = placePort(AUX_PROFILE, 26.5, -1.2, new THREE.Vector3(0.42, 1, 0.02), lidMat);
  addAnchor(patient, "patient", 0, 29, 0);
  addAnchor(vacuum, "vacuum", 0, 27, 0);
  addAnchor(aux, "aux", 0, 15, 0);
  addAnchor(lid, "lid", 0, 164, 18);

  const hinge = new THREE.Mesh(new THREE.BoxGeometry(4.4, 6.2, 8.4), lidMat);
  hinge.position.set(-53.4, 149.4, 0);
  hinge.castShadow = true;
  lid.add(hinge);
  lidMeshes.push(hinge);
  const knuckle = new THREE.Mesh(new THREE.CylinderGeometry(1.55, 1.55, 9.2, 14), lidMat);
  knuckle.rotation.x = Math.PI / 2;
  knuckle.position.set(-55.4, 151.1, 0);
  lid.add(knuckle);
  lidMeshes.push(knuckle);

  const clip = new THREE.Group();
  clip.position.set(-66.5, 151.15, 0);
  const clipBack = new THREE.Mesh(new THREE.BoxGeometry(2.3, 1.7, 13.2), lidMat);
  clipBack.position.set(5.4, 0, 0);
  const clipArmA = new THREE.Mesh(new THREE.BoxGeometry(12.4, 1.7, 2.25), lidMat);
  clipArmA.position.set(-0.6, 0, 5.4);
  const clipArmB = new THREE.Mesh(new THREE.BoxGeometry(12.4, 1.7, 2.25), lidMat);
  clipArmB.position.set(-0.6, 0, -5.4);
  clip.add(clipBack, clipArmA, clipArmB);
  lid.add(clip);
  lidMeshes.push(clipBack, clipArmA, clipArmB);

  const linkCurve = new THREE.CatmullRomCurve3([
    new THREE.Vector3(-55.2, 151.2, 0),
    new THREE.Vector3(-62, 151.6, 0),
    new THREE.Vector3(-72.5, 152.4, 0),
  ]);
  const link = new THREE.Mesh(new THREE.TubeGeometry(linkCurve, 18, 0.95, 8, false), lidMat);
  link.castShadow = true;
  lid.add(link);
  lidMeshes.push(link);

  const loopPts = [];
  for (let i = 0; i <= 72; i++) {
    const a = (i / 72) * Math.PI * 2;
    loopPts.push(new THREE.Vector3(-90 + Math.cos(a) * 16.5, 153.1 + Math.sin(a) * 0.7, Math.sin(a) * 6.8));
  }
  const strap = new THREE.Mesh(
    new THREE.TubeGeometry(new THREE.CatmullRomCurve3(loopPts, true), 96, 0.92, 8, true),
    lidMat
  );
  strap.castShadow = true;
  lid.add(strap);
  lidMeshes.push(strap);

  const plug = new THREE.Group();
  const flange = new THREE.Mesh(new THREE.CylinderGeometry(7.1, 7.1, 2.3, 28), lidMat);
  const plugBody = new THREE.Mesh(new THREE.CylinderGeometry(5.35, 5.7, 6.8, 28), lidMat);
  plugBody.position.y = 4.4;
  const nose = new THREE.Mesh(new THREE.CylinderGeometry(3.35, 4.55, 4.2, 24), lidMat);
  nose.position.y = -2.6;
  const ring = new THREE.Mesh(new THREE.TorusGeometry(5.5, 0.7, 8, 24), lidMat);
  ring.rotation.x = Math.PI / 2;
  ring.position.y = 1.5;
  plug.add(flange, plugBody, nose, ring);
  lidMeshes.push(flange, plugBody, nose, ring);
  plug.position.set(-106.5, 153.1, 0);
  lid.add(plug);
  addAnchor(plug, "cap", 0, 8, 0);

  const edgeGeos = [];
  function addEdges(mesh, threshold) {
    const eg = new THREE.EdgesGeometry(mesh.geometry, threshold);
    const lineMat = new THREE.LineBasicMaterial({ color: 0x16383c });
    if (mesh.material && mesh.material.clippingPlanes) lineMat.clippingPlanes = mesh.material.clippingPlanes;
    const ln = new THREE.LineSegments(eg, lineMat);
    ln.renderOrder = 9;
    mesh.add(ln);
    edgeGeos.push(ln);
    return ln;
  }
  addEdges(bagMesh, 18);
  addEdges(collar, 16);
  addEdges(deck, 28);
  lidMeshes.forEach((m) => {
    if (m.geometry && m.geometry.type === "LatheGeometry" && m !== collar) addEdges(m, 22);
  });

  const state = { look: "studio", wireframe: false, explode: 0, cutaway: 0, theme: "light" };

  function applyEdgeColor() {
    const cad = state.look === "cad";
    const dark = state.theme === "dark";
    const hex = cad ? (dark ? 0xd5f4f2 : 0x17383c) : dark ? 0xe7fbfa : 0x12383c;
    inkMat.color.setHex(hex);
    edgeGeos.forEach((ln) => ln.material.color.setHex(hex));
    inkMeshes.forEach((m) => {
      if (m.material && m.material.color) m.material.color.setHex(hex);
    });
  }

  function applyVisibility() {
    const show = state.look === "cad" || state.wireframe;
    inkMeshes.forEach((m) => (m.visible = show));
    edgeGeos.forEach((ln) => (ln.visible = show));
  }

  function applyLook() {
    const cad = state.look === "cad";
    bagMeshes.forEach((m) => (m.material = cad ? bagCad : bagStudio));
    lidMeshes.forEach((m) => {
      if (m.material === boreMat) return;
      m.material = cad ? lidCad : lidMat;
    });
    filterMeshes.forEach((m) => {
      if (m.material === mediaMat) return;
      m.material = cad ? filterCad : filterMat;
    });
    pouchMeshes.forEach((m) => (m.material = cad ? pouchCad : pouchMat));
    applyEdgeColor();
    applyVisibility();
  }

  function setExplode(t) {
    state.explode = t;
    lid.position.y = t * 152;
    filter.position.y = t * 118;
    pouch.position.y = pouchBaseY + t * 164;
  }

  function setCutaway(t) {
    state.cutaway = t;
    clipPlane.constant = THREE.MathUtils.lerp(520, 4, t);
  }

  function setLook(look) {
    state.look = look;
    applyLook();
  }

  function setWireframe(on) {
    state.wireframe = on;
    applyVisibility();
    applyEdgeColor();
  }

  function setTheme(theme) {
    state.theme = theme;
    applyEdgeColor();
  }

  // The deck contour loop above was pushed as a Mesh by mistake if geometry
  // has no faces. Rebuild those three rings as lines and drop empty meshes.
  for (let i = inkMeshes.length - 1; i >= 0; i--) {
    const m = inkMeshes[i];
    if (m.geometry && m.geometry.type === "BufferGeometry" && !m.geometry.getIndex() && m.isMesh) {
      const parent = m.parent;
      parent.remove(m);
      const ln = new THREE.Line(
        m.geometry,
        new THREE.LineBasicMaterial({ color: 0x16383c })
      );
      ln.renderOrder = 8;
      ln.userData.ink = true;
      parent.add(ln);
      inkMeshes[i] = ln;
    }
  }

  applyLook();
  setExplode(0);
  setCutaway(0);

  return {
    root,
    anchors,
    clipPlane,
    bag,
    lid,
    filter,
    pouch,
    setExplode,
    setCutaway,
    setLook,
    setWireframe,
    setTheme,
    state,
  };
}

export const CALLOUTS = [
  { id: "lid", fa: "درب فیروزه‌ای", en: "Teal lid" },
  { id: "patient", fa: "پورت بیمار", en: "Patient port" },
  { id: "vacuum", fa: "پورت وکیوم", en: "Vacuum port" },
  { id: "aux", fa: "پورت کمکی", en: "Auxiliary port" },
  { id: "cap", fa: "درپوش بنددار", en: "Tethered cap" },
  { id: "filter", fa: "فیلتر هیدروفوبیک", en: "Hydrophobic filter" },
  { id: "body", fa: "بدنه کیسه", en: "Liner body" },
  { id: "pouch", fa: "پاکت پودر ژل‌کننده", en: "Gelling-powder pouch" },
];
