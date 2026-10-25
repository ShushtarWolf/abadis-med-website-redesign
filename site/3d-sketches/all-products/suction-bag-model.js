import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

/**
 * Procedural stipple / frosted bump & roughness map for the 1L translucent liner body
 * plus subtle molded volume graduation markings (200 - 1000 ml).
 */
export function createFrostedTextures() {
  const size = 512;
  const bumpCanvas = document.createElement('canvas');
  bumpCanvas.width = bumpCanvas.height = size;
  const bctx = bumpCanvas.getContext('2d');
  const imgData = bctx.createImageData(size, size);
  const d = imgData.data;
  let seed = 1337;
  const rand = () => {
    seed = (seed * 16807) % 2147483647;
    return (seed - 1) / 2147483646;
  };
  for (let i = 0; i < d.length; i += 4) {
    const v = Math.floor(110 + rand() * 85);
    d[i] = d[i + 1] = d[i + 2] = v;
    d[i + 3] = 255;
  }
  bctx.putImageData(imgData, 0, 0);
  const bumpTex = new THREE.CanvasTexture(bumpCanvas);
  bumpTex.wrapS = bumpTex.wrapT = THREE.RepeatWrapping;
  bumpTex.repeat.set(6, 4);

  // Graduation scale texture (subtle embossed ticks on side of liner)
  const gradCanvas = document.createElement('canvas');
  gradCanvas.width = 1024;
  gradCanvas.height = 512;
  const gctx = gradCanvas.getContext('2d');
  gctx.clearRect(0, 0, 1024, 512);

  const gx = 240;
  gctx.strokeStyle = 'rgba(255, 255, 255, 0.45)';
  gctx.fillStyle = 'rgba(255, 255, 255, 0.50)';
  gctx.lineWidth = 2.4;
  gctx.font = '700 18px Arial, sans-serif';
  gctx.textAlign = 'left';

  gctx.beginPath();
  gctx.moveTo(gx, 75);
  gctx.lineTo(gx, 445);
  gctx.stroke();

  const levels = [
    { y: 90, label: '1000 ml', major: true },
    { y: 132, label: '900', major: false },
    { y: 174, label: '800 ml', major: true },
    { y: 216, label: '700', major: false },
    { y: 258, label: '600 ml', major: true },
    { y: 300, label: '500', major: false },
    { y: 342, label: '400 ml', major: true },
    { y: 384, label: '300', major: false },
    { y: 426, label: '200 ml', major: true },
  ];
  for (const lv of levels) {
    const tickW = lv.major ? 28 : 15;
    gctx.beginPath();
    gctx.moveTo(gx - tickW / 2, lv.y);
    gctx.lineTo(gx + tickW / 2, lv.y);
    gctx.stroke();
    if (lv.major) {
      gctx.fillText(lv.label, gx + 18, lv.y + 6);
    }
  }

  const gradTex = new THREE.CanvasTexture(gradCanvas);
  gradTex.colorSpace = THREE.SRGBColorSpace;
  return { bumpTex, gradTex };
}

/**
 * Creates a soft radial contact shadow plane under the 1L suction bag
 */
export function createContactShadow(radius = 0.085, dark = false) {
  const c = document.createElement('canvas');
  c.width = c.height = 256;
  const g = c.getContext('2d');
  const grd = g.createRadialGradient(128, 128, 8, 128, 128, 120);
  if (dark) {
    grd.addColorStop(0, 'rgba(0, 0, 0, 0.62)');
    grd.addColorStop(0.55, 'rgba(0, 15, 18, 0.25)');
    grd.addColorStop(1, 'rgba(0, 0, 0, 0)');
  } else {
    grd.addColorStop(0, 'rgba(5, 55, 58, 0.24)');
    grd.addColorStop(0.55, 'rgba(5, 55, 58, 0.09)');
    grd.addColorStop(1, 'rgba(5, 55, 58, 0)');
  }
  g.fillStyle = grd;
  g.fillRect(0, 0, 256, 256);
  const tex = new THREE.CanvasTexture(c);
  tex.colorSpace = THREE.SRGBColorSpace;
  const mesh = new THREE.Mesh(
    new THREE.PlaneGeometry(radius * 2.2, radius * 2.2),
    new THREE.MeshBasicMaterial({
      map: tex,
      transparent: true,
      depthWrite: false,
    })
  );
  mesh.rotation.x = -Math.PI / 2;
  mesh.position.y = -0.109;
  mesh.renderOrder = -1;
  return mesh;
}

/**
 * Builds the complete Abadis 1L Disposable Suction Liner 3D Assembly.
 */
export async function loadSuctionBag1L(glbUrl = '/viewer/assets/abadis-scrub-parts.glb') {
  const gltf = await new GLTFLoader().loadAsync(glbUrl);
  const rawRoot = gltf.scene;
  const rawLid = rawRoot.getObjectByName('lid');

  const { bumpTex, gradTex } = createFrostedTextures();

  const root = new THREE.Group();
  root.name = 'AbadisSuctionBag1L';

  // Materials
  const lidTealMat = new THREE.MeshPhysicalMaterial({
    color: 0x006e6d,
    roughness: 0.35,
    metalness: 0.04,
    clearcoat: 0.28,
    clearcoatRoughness: 0.30,
    reflectivity: 0.65,
    side: THREE.DoubleSide,
  });

  const tetherTealMat = new THREE.MeshPhysicalMaterial({
    color: 0x007876,
    roughness: 0.34,
    metalness: 0.03,
    clearcoat: 0.25,
    side: THREE.DoubleSide,
  });

  const filterCageMat = new THREE.MeshPhysicalMaterial({
    color: 0x054043,
    roughness: 0.42,
    metalness: 0.05,
    clearcoat: 0.15,
    side: THREE.DoubleSide,
  });

  const filterElementMat = new THREE.MeshStandardMaterial({
    color: 0xe2f4f4,
    roughness: 0.65,
    metalness: 0.0,
  });

  const frostedLinerMat = new THREE.MeshPhysicalMaterial({
    color: 0xebf3f3,
    roughness: 0.44,
    metalness: 0.0,
    transmission: 0.32,
    transparent: true,
    opacity: 0.54,
    ior: 1.46,
    thickness: 0.008,
    clearcoat: 0.16,
    clearcoatRoughness: 0.48,
    bumpMap: bumpTex,
    bumpScale: 0.0006,
    roughnessMap: bumpTex,
    side: THREE.DoubleSide,
    depthWrite: false,
  });

  const linerCollarMat = new THREE.MeshPhysicalMaterial({
    color: 0xdceaea,
    roughness: 0.38,
    metalness: 0.0,
    transparent: true,
    opacity: 0.74,
    clearcoat: 0.2,
    side: THREE.DoubleSide,
    depthWrite: false,
  });

  const absorbentPadMat = new THREE.MeshPhysicalMaterial({
    color: 0xf7fbfb,
    roughness: 0.60,
    metalness: 0.0,
    sheen: 0.35,
    sheenColor: new THREE.Color(0xffffff),
    side: THREE.DoubleSide,
  });

  // CAD Wireframe overlay materials
  const cadEdgeTealMat = new THREE.LineBasicMaterial({
    color: 0x008c8e,
    transparent: true,
    opacity: 0.78,
  });
  const cadEdgeLinerMat = new THREE.LineBasicMaterial({
    color: 0x157a7c,
    transparent: true,
    opacity: 0.52,
  });
  const cadHiddenMat = new THREE.LineDashedMaterial({
    color: 0x006668,
    dashSize: 0.004,
    gapSize: 0.0025,
    transparent: true,
    opacity: 0.65,
  });

  // -------------------------------------------------------------------------
  // 1. LID ASSEMBLY GROUP (Rotated 180° around Y so Tether/U-clip is on -X Left)
  // -------------------------------------------------------------------------
  const lidGroup = new THREE.Group();
  lidGroup.name = 'lidGroup';

  const lidOrient = new THREE.Group();
  lidOrient.rotation.y = Math.PI;
  lidGroup.add(lidOrient);

  const cadOverlays = [];

  if (rawLid) {
    const lidClone = rawLid.clone(true);
    lidClone.traverse((o) => {
      if (o.isMesh) {
        o.geometry = o.geometry.clone();
        o.geometry.computeVertexNormals();
        o.material = lidTealMat;
        o.renderOrder = 2;

        const edgesGeo = new THREE.EdgesGeometry(o.geometry, 22);
        const edgeLines = new THREE.LineSegments(edgesGeo, cadEdgeTealMat);
        edgeLines.visible = false;
        edgeLines.name = 'cadEdge';
        o.add(edgeLines);
        cadOverlays.push(edgeLines);
      }
    });
    lidOrient.add(lidClone);
  }

  // Second angled tubular nozzle (Patient port emerging from crescent recess)
  const nozzle2Group = new THREE.Group();
  nozzle2Group.position.set(0.016, 0.001, 0.028);
  nozzle2Group.rotation.z = -Math.PI * 0.27;
  const nozOuterGeo = new THREE.CylinderGeometry(0.0052, 0.0064, 0.028, 32, 1, false);
  nozOuterGeo.translate(0, 0.014, 0);
  const nozOuterMesh = new THREE.Mesh(nozOuterGeo, lidTealMat);
  const nozRimGeo = new THREE.TorusGeometry(0.0049, 0.0007, 12, 32);
  nozRimGeo.rotateX(Math.PI / 2);
  nozRimGeo.translate(0, 0.028, 0);
  const nozRimMesh = new THREE.Mesh(nozRimGeo, lidTealMat);
  const boreMat = new THREE.MeshBasicMaterial({ color: 0x022224 });
  const boreGeo = new THREE.CylinderGeometry(0.0038, 0.0038, 0.006, 24);
  boreGeo.translate(0, 0.0255, 0);
  const boreMesh = new THREE.Mesh(boreGeo, boreMat);
  nozzle2Group.add(nozOuterMesh, nozRimMesh, boreMesh);

  const noz2Edges = new THREE.LineSegments(new THREE.EdgesGeometry(nozOuterGeo, 15), cadEdgeTealMat);
  noz2Edges.visible = false;
  nozzle2Group.add(noz2Edges);
  cadOverlays.push(noz2Edges);
  lidOrient.add(nozzle2Group);

  // Auxiliary circular port rim on right side of top surface
  const auxPortGroup = new THREE.Group();
  auxPortGroup.position.set(-0.026, 0.0002, -0.030);
  const auxCollarGeo = new THREE.TorusGeometry(0.0068, 0.0012, 14, 32);
  auxCollarGeo.rotateX(Math.PI / 2);
  const auxCollarMesh = new THREE.Mesh(auxCollarGeo, lidTealMat);
  const auxRecessGeo = new THREE.CylinderGeometry(0.0062, 0.0062, 0.004, 28);
  auxRecessGeo.translate(0, -0.0015, 0);
  const auxRecessMesh = new THREE.Mesh(auxRecessGeo, new THREE.MeshStandardMaterial({ color: 0x03383a, roughness: 0.5 }));
  auxPortGroup.add(auxCollarMesh, auxRecessMesh);
  lidOrient.add(auxPortGroup);

  root.add(lidGroup);

  // -------------------------------------------------------------------------
  // 2. TETHERED PORT CAP & FLEXIBLE LOOP GROUP (Left Side: -X in world space)
  // -------------------------------------------------------------------------
  const tetherGroup = new THREE.Group();
  tetherGroup.name = 'tetherGroup';

  const loopCurve = new THREE.CatmullRomCurve3([
    new THREE.Vector3(-0.0705, 0.0022, 0.0285),
    new THREE.Vector3(-0.088, 0.0020, 0.0335),
    new THREE.Vector3(-0.108, 0.0012, 0.0255),
    new THREE.Vector3(-0.113, 0.0008, 0.0135),
    new THREE.Vector3(-0.104, 0.0006, 0.0030),
    new THREE.Vector3(-0.085, 0.0008, 0.0095),
    new THREE.Vector3(-0.0685, 0.0015, 0.0245),
  ], false);
  const loopGeo = new THREE.TubeGeometry(loopCurve, 64, 0.00115, 12, false);
  const loopMesh = new THREE.Mesh(loopGeo, tetherTealMat);
  loopMesh.renderOrder = 3;
  tetherGroup.add(loopMesh);

  const capRingGeo = new THREE.CylinderGeometry(0.0042, 0.0042, 0.0025, 24);
  capRingGeo.translate(-0.0708, 0.0025, 0.0285);
  const capRingMesh = new THREE.Mesh(capRingGeo, tetherTealMat);
  tetherGroup.add(capRingMesh);

  // Also include a standalone plug + U-clip representation when exploded so Tethered Cap & U-Clip shows as a full unit
  const uClipTabGeo = new THREE.BoxGeometry(0.012, 0.0028, 0.014);
  uClipTabGeo.translate(-0.072, -0.0015, -0.019);
  const uClipTabMesh = new THREE.Mesh(uClipTabGeo, tetherTealMat);
  tetherGroup.add(uClipTabMesh);

  const loopEdges = new THREE.LineSegments(new THREE.EdgesGeometry(loopGeo, 25), cadEdgeTealMat);
  loopEdges.visible = false;
  tetherGroup.add(loopEdges);
  cadOverlays.push(loopEdges);

  root.add(tetherGroup);

  // -------------------------------------------------------------------------
  // 3. INTERNAL SHUT-OFF VALVE / FILTER CAGE GROUP (Center Underside of Lid)
  // -------------------------------------------------------------------------
  const filterCageGroup = new THREE.Group();
  filterCageGroup.name = 'filterCageGroup';

  const upperBossGeo = new THREE.CylinderGeometry(0.0195, 0.0180, 0.018, 36);
  upperBossGeo.translate(0, -0.029, 0);
  const upperBossMesh = new THREE.Mesh(upperBossGeo, filterCageMat);
  filterCageGroup.add(upperBossMesh);

  const cageBodyGeo = new THREE.CylinderGeometry(0.0162, 0.0188, 0.060, 36);
  cageBodyGeo.translate(0, -0.066, 0);
  const cageBodyMesh = new THREE.Mesh(cageBodyGeo, filterCageMat);
  filterCageGroup.add(cageBodyMesh);

  const cageCapGeo = new THREE.CylinderGeometry(0.0198, 0.0192, 0.0045, 36);
  cageCapGeo.translate(0, -0.0975, 0);
  const cageCapMesh = new THREE.Mesh(cageCapGeo, filterCageMat);
  filterCageGroup.add(cageCapMesh);

  const innerFilterGeo = new THREE.CylinderGeometry(0.0135, 0.0150, 0.046, 28);
  innerFilterGeo.translate(0, -0.066, 0);
  const innerFilterMesh = new THREE.Mesh(innerFilterGeo, filterElementMat);
  filterCageGroup.add(innerFilterMesh);

  for (let i = 0; i < 8; i++) {
    const ang = (i / 8) * Math.PI * 2;
    const ribGeo = new THREE.BoxGeometry(0.0024, 0.056, 0.0035);
    ribGeo.translate(0, -0.066, 0.0172);
    ribGeo.rotateY(ang);
    const ribMesh = new THREE.Mesh(ribGeo, filterCageMat);
    filterCageGroup.add(ribMesh);
  }

  const cageEdgeGeo = new THREE.EdgesGeometry(cageBodyGeo, 12);
  const cageLines = new THREE.LineSegments(cageEdgeGeo, cadHiddenMat);
  cageLines.computeLineDistances();
  cageLines.visible = false;
  filterCageGroup.add(cageLines);
  cadOverlays.push(cageLines);

  root.add(filterCageGroup);

  // -------------------------------------------------------------------------
  // 4. WHITE COAGULANT / ABSORBENT PACKET AT BOTTOM OF LINER
  // -------------------------------------------------------------------------
  const absorbentPadGroup = new THREE.Group();
  absorbentPadGroup.name = 'absorbentPadGroup';

  const padGeo = new THREE.BoxGeometry(0.052, 0.015, 0.042, 16, 8, 16);
  const posAttr = padGeo.attributes.position;
  const pv = new THREE.Vector3();
  for (let i = 0; i < posAttr.count; i++) {
    pv.fromBufferAttribute(posAttr, i);
    const nx = pv.x / 0.026;
    const ny = pv.y / 0.0075;
    const nz = pv.z / 0.021;
    const dome = Math.cos(Math.min(1, Math.abs(nx)) * Math.PI * 0.48) *
                 Math.cos(Math.min(1, Math.abs(nz)) * Math.PI * 0.48);
    pv.y = ny * 0.0085 * (0.18 + 0.82 * dome);
    posAttr.setXYZ(i, pv.x, pv.y, pv.z);
  }
  padGeo.computeVertexNormals();
  const padMesh = new THREE.Mesh(padGeo, absorbentPadMat);

  const flangeGeo = new THREE.BoxGeometry(0.057, 0.0012, 0.047, 8, 1, 8);
  const flangeMesh = new THREE.Mesh(flangeGeo, absorbentPadMat);
  padMesh.add(flangeMesh);

  padMesh.position.set(0.004, -0.165, 0.003);
  padMesh.rotation.set(0.18, 0.35, -0.22);
  absorbentPadGroup.add(padMesh);

  const padEdgeGeo = new THREE.EdgesGeometry(padGeo, 10);
  const padLines = new THREE.LineSegments(padEdgeGeo, cadHiddenMat);
  padLines.computeLineDistances();
  padLines.visible = false;
  padMesh.add(padLines);
  cadOverlays.push(padLines);

  root.add(absorbentPadGroup);

  // -------------------------------------------------------------------------
  // 5. 1L TAPERED FROSTED TRANSLUCENT LINER BODY (y = -0.016 to -0.184)
  // -------------------------------------------------------------------------
  const linerBodyGroup = new THREE.Group();
  linerBodyGroup.name = 'linerBodyGroup';

  const collarProfile = [
    new THREE.Vector2(0.0545, -0.038),
    new THREE.Vector2(0.0564, -0.036),
    new THREE.Vector2(0.0564, -0.024),
    new THREE.Vector2(0.0578, -0.022),
    new THREE.Vector2(0.0578, -0.017),
    new THREE.Vector2(0.0552, -0.017),
  ];
  const collarGeo = new THREE.LatheGeometry(collarProfile, 64);
  const collarMesh = new THREE.Mesh(collarGeo, linerCollarMat);
  collarMesh.renderOrder = 3;
  linerBodyGroup.add(collarMesh);

  const bodyProfile = [];
  bodyProfile.push(new THREE.Vector2(0.000, -0.184));
  bodyProfile.push(new THREE.Vector2(0.0425, -0.184));
  bodyProfile.push(new THREE.Vector2(0.0452, -0.183));
  bodyProfile.push(new THREE.Vector2(0.0462, -0.180));
  const steps = 18;
  for (let i = 1; i <= steps; i++) {
    const t = i / steps;
    const y = -0.180 + t * (-0.038 - -0.180);
    const r = 0.0462 + t * (0.0554 - 0.0462);
    bodyProfile.push(new THREE.Vector2(r, y));
  }
  const linerGeo = new THREE.LatheGeometry(bodyProfile, 64);
  const linerMesh = new THREE.Mesh(linerGeo, frostedLinerMat);
  linerMesh.renderOrder = 4;
  linerBodyGroup.add(linerMesh);

  // Cutaway version of liner body (260° arc leaving a 100° open cutaway window in front!)
  const cutawayCollarGeo = new THREE.LatheGeometry(collarProfile, 48, Math.PI * 0.35, Math.PI * 1.45);
  const cutawayCollarMesh = new THREE.Mesh(cutawayCollarGeo, linerCollarMat);
  cutawayCollarMesh.visible = false;
  cutawayCollarMesh.renderOrder = 3;
  linerBodyGroup.add(cutawayCollarMesh);

  const cutawayLinerGeo = new THREE.LatheGeometry(bodyProfile, 48, Math.PI * 0.35, Math.PI * 1.45);
  const cutawayLinerMesh = new THREE.Mesh(cutawayLinerGeo, frostedLinerMat);
  cutawayLinerMesh.visible = false;
  cutawayLinerMesh.renderOrder = 4;
  linerBodyGroup.add(cutawayLinerMesh);

  // Cutaway section edge highlight lines (bright teal cross-section wall edges where sliced)
  const cutSectionGroup = new THREE.Group();
  cutSectionGroup.visible = false;
  const cutEdgeMat = new THREE.LineBasicMaterial({ color: 0x00b8ba, linewidth: 2 });
  for (const ang of [Math.PI * 0.35, Math.PI * 1.80]) {
    const pts = bodyProfile.map((v2) => new THREE.Vector3(Math.sin(ang) * v2.x, v2.y, Math.cos(ang) * v2.x));
    const lGeo = new THREE.BufferGeometry().setFromPoints(pts);
    cutSectionGroup.add(new THREE.Line(lGeo, cutEdgeMat));
  }
  linerBodyGroup.add(cutSectionGroup);

  const gradGeo = new THREE.CylinderGeometry(0.0550, 0.0466, 0.136, 64, 1, true);
  gradGeo.translate(0, -0.109, 0);
  const gradMat = new THREE.MeshBasicMaterial({
    map: gradTex,
    transparent: true,
    opacity: 0.72,
    depthWrite: false,
    side: THREE.FrontSide,
  });
  const gradMesh = new THREE.Mesh(gradGeo, gradMat);
  gradMesh.renderOrder = 5;
  linerBodyGroup.add(gradMesh);

  // Clean engineering CAD wireframe grid for the 1L liner body
  const cadGridGroup = new THREE.Group();
  cadGridGroup.visible = false;
  const ringHeights = [-0.038, -0.055, -0.073, -0.091, -0.109, -0.127, -0.145, -0.163, -0.180, -0.184];
  for (const ry of ringHeights) {
    const t = THREE.MathUtils.clamp((ry - -0.180) / (-0.038 - -0.180), 0, 1);
    const rr = ry < -0.180 ? 0.043 : 0.0462 + t * (0.0554 - 0.0462);
    const pts = [];
    for (let s = 0; s <= 64; s++) {
      const a = (s / 64) * Math.PI * 2;
      pts.push(new THREE.Vector3(Math.cos(a) * rr, ry, Math.sin(a) * rr));
    }
    const lineGeo = new THREE.BufferGeometry().setFromPoints(pts);
    cadGridGroup.add(new THREE.Line(lineGeo, cadEdgeLinerMat));
  }
  for (let m = 0; m < 24; m++) {
    const a = (m / 24) * Math.PI * 2;
    const pts = [
      new THREE.Vector3(Math.cos(a) * 0.0564, -0.022, Math.sin(a) * 0.0564),
      new THREE.Vector3(Math.cos(a) * 0.0554, -0.038, Math.sin(a) * 0.0554),
      new THREE.Vector3(Math.cos(a) * 0.0462, -0.180, Math.sin(a) * 0.0462),
      new THREE.Vector3(Math.cos(a) * 0.0425, -0.184, Math.sin(a) * 0.0425),
    ];
    const lineGeo = new THREE.BufferGeometry().setFromPoints(pts);
    cadGridGroup.add(new THREE.Line(lineGeo, cadEdgeLinerMat));
  }
  linerBodyGroup.add(cadGridGroup);
  cadOverlays.push(cadGridGroup);

  root.add(linerBodyGroup);

  // Center the entire assembly vertically around y = 0
  const centerOffset = new THREE.Vector3(0, 0.078, 0);
  lidGroup.position.add(centerOffset);
  tetherGroup.position.add(centerOffset);
  filterCageGroup.position.add(centerOffset);
  absorbentPadGroup.position.add(centerOffset);
  linerBodyGroup.position.add(centerOffset);

  const basePos = {
    lid: lidGroup.position.clone(),
    tether: tetherGroup.position.clone(),
    filterCage: filterCageGroup.position.clone(),
    linerBody: linerBodyGroup.position.clone(),
    absorbentPad: absorbentPadGroup.position.clone(),
  };

  function setExploded(t) {
    const k = THREE.MathUtils.clamp(t, 0, 1);
    lidGroup.position.copy(basePos.lid).add(new THREE.Vector3(0, 0.118 * k, 0));
    tetherGroup.position.copy(basePos.tether).add(new THREE.Vector3(-0.038 * k, 0.088 * k, 0));
    filterCageGroup.position.copy(basePos.filterCage).add(new THREE.Vector3(0, 0.042 * k, 0));
    linerBodyGroup.position.copy(basePos.linerBody).add(new THREE.Vector3(0, -0.032 * k, 0));
    absorbentPadGroup.position.copy(basePos.absorbentPad).add(new THREE.Vector3(0, -0.108 * k, 0));
  }

  function setCutaway(enabled) {
    collarMesh.visible = !enabled;
    linerMesh.visible = !enabled;
    cutawayCollarMesh.visible = enabled;
    cutawayLinerMesh.visible = enabled;
    cutSectionGroup.visible = enabled;
  }

  function setCadMode(enabled, dark = false) {
    for (const ov of cadOverlays) {
      ov.visible = enabled;
    }
    if (enabled) {
      cadEdgeTealMat.color.setHex(dark ? 0x35e0e2 : 0x006d70);
      cadEdgeTealMat.opacity = dark ? 0.62 : 0.55;
      cadEdgeLinerMat.color.setHex(dark ? 0x2ec4c6 : 0x05686b);
      cadEdgeLinerMat.opacity = dark ? 0.58 : 0.52;
      cadHiddenMat.color.setHex(dark ? 0x7ef4f6 : 0x004d4f);
      cadHiddenMat.opacity = dark ? 0.82 : 0.72;

      lidTealMat.transparent = true;
      lidTealMat.opacity = dark ? 0.34 : 0.28;
      lidTealMat.roughness = 0.25;

      tetherTealMat.transparent = true;
      tetherTealMat.opacity = dark ? 0.45 : 0.38;

      frostedLinerMat.opacity = dark ? 0.18 : 0.16;
      linerCollarMat.opacity = dark ? 0.24 : 0.22;

      filterCageMat.color.setHex(dark ? 0x16989a : 0x005c5e);
    } else {
      lidTealMat.transparent = false;
      lidTealMat.opacity = 1.0;
      lidTealMat.roughness = 0.35;

      tetherTealMat.transparent = false;
      tetherTealMat.opacity = 1.0;

      frostedLinerMat.opacity = dark ? 0.50 : 0.54;
      linerCollarMat.opacity = dark ? 0.68 : 0.74;

      filterCageMat.color.setHex(0x054043);
    }
  }

  return {
    root,
    parts: {
      lidGroup,
      tetherGroup,
      filterCageGroup,
      linerBodyGroup,
      absorbentPadGroup,
    },
    materials: {
      lidTealMat,
      tetherTealMat,
      filterCageMat,
      frostedLinerMat,
      linerCollarMat,
      absorbentPadMat,
    },
    setExploded,
    setCutaway,
    setCadMode,
  };
}
