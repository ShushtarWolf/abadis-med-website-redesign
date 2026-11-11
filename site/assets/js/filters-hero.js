/**
 * Filters preview cinematic: hose → antibacterial disc → bag with
 * flow-stop filter → porous filter revealed from the flow-stop core.
 * Scroll-scoped, damped, no idle drift. Canvas keeps touch-action: pan-y
 * so iOS page scroll is never trapped. No OrbitControls on the hero.
 */
import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {RoomEnvironment} from 'three/addons/environments/RoomEnvironment.js';
import {mergeVertices} from 'three/addons/utils/BufferGeometryUtils.js';
import {applySinteredGrain} from '../../3d-sketches/p16-cinematic/sintered-grain.js';

const SK = (file) => new URL('../../3d-sketches/' + file, import.meta.url).href;

export function mount(root){
  const stillCapture = root.getAttribute('data-cin-capture') === 'still';
  const mob = stillCapture ? false : matchMedia('(max-width:700px),(pointer:coarse)').matches;
  const cv = root.querySelector('canvas');
  const stage = cv.parentElement;
  cv.style.touchAction = 'pan-y';

  const R = new THREE.WebGLRenderer({
    canvas: cv, antialias: true, alpha: true,
    preserveDrawingBuffer: stillCapture,
    powerPreference: 'high-performance'
  });
  R.setClearColor(0x05090b, 1);
  R.setPixelRatio(Math.min(devicePixelRatio, mob ? 1.6 : 2));
  R.toneMapping = THREE.ACESFilmicToneMapping;
  R.toneMappingExposure = 1.05;
  R.shadowMap.enabled = !mob;
  R.shadowMap.type = THREE.PCFSoftShadowMap;

  const S = new THREE.Scene();
  const pm = new THREE.PMREMGenerator(R);
  S.environment = pm.fromScene(new RoomEnvironment(), .05).texture;
  S.environmentIntensity = .46;
  pm.dispose();
  R.setRenderTarget(null);
  R.setScissorTest(false);
  const C = new THREE.PerspectiveCamera(mob ? 36 : 28, 1, 2, 4000);

  const key = new THREE.DirectionalLight(0xfff2ea, 1.32);
  key.position.set(-180, 420, 260);
  key.castShadow = !mob;
  if (!mob) {
    key.shadow.mapSize.set(2048, 2048);
    Object.assign(key.shadow.camera, {left: -400, right: 400, top: 400, bottom: -400, near: 40, far: 1600});
    key.shadow.radius = 16;
    key.shadow.bias = -.00035;
  }
  S.add(key);
  const fillA = new THREE.DirectionalLight(0xe8f4f8, 1.1); fillA.position.set(160, 220, 200); S.add(fillA);
  const fillB = new THREE.DirectionalLight(0x7ecad4, .7); fillB.position.set(240, 140, -320); S.add(fillB);
  const hemi = new THREE.HemisphereLight(0xf0f6f7, 0x1a1814, .85);
  S.add(hemi);

  function radTex(stops){
    const c = document.createElement('canvas'); c.width = c.height = 256;
    const x = c.getContext('2d');
    const g = x.createRadialGradient(128, 128, 0, 128, 128, 128);
    stops.forEach(s => g.addColorStop(...s));
    x.fillStyle = g; x.fillRect(0, 0, 256, 256);
    return new THREE.CanvasTexture(c);
  }
  const floor = new THREE.Mesh(
    new THREE.PlaneGeometry(1600, 1600),
    new THREE.MeshBasicMaterial({map: radTex([
      [0, 'rgba(46,127,150,.28)'], [.5, 'rgba(46,127,150,.08)'], [1, 'rgba(46,127,150,0)']
    ]), transparent: true, depthWrite: false})
  );
  floor.rotation.x = -Math.PI / 2;
  floor.position.y = -2;
  S.add(floor);
  if (!mob) {
    const sr = new THREE.Mesh(new THREE.PlaneGeometry(900, 900), new THREE.ShadowMaterial({opacity: .32}));
    sr.rotation.x = -Math.PI / 2; sr.position.y = -1.6; sr.receiveShadow = true; S.add(sr);
  }

  const glass = new THREE.MeshPhysicalMaterial({
    color: 0xe7f1f8, roughness: .08, metalness: 0, transparent: true, opacity: .38,
    depthWrite: false, thickness: 2.2, ior: 1.49,
    attenuationColor: 0xd9eef0, attenuationDistance: 80, side: THREE.DoubleSide
  });
  const ribMat = new THREE.MeshPhysicalMaterial({
    color: 0x6f97b8, roughness: .28, metalness: 0, transparent: true, opacity: .85,
    depthWrite: false, side: THREE.DoubleSide
  });
  const p12Glass = new THREE.MeshPhysicalMaterial({
    color: 0xf4f8f7, roughness: .06, metalness: 0, transparent: true, opacity: .36,
    depthWrite: false, thickness: 2.4, ior: 1.49, side: THREE.DoubleSide
  });
  const cartMat = new THREE.MeshStandardMaterial({
    color: 0xf4f0e6, roughness: .9, metalness: 0, envMapIntensity: .28, side: THREE.DoubleSide
  });
  const hoseMat = new THREE.MeshPhysicalMaterial({
    color: 0xc5d5d8, roughness: .42, metalness: 0, transparent: true, opacity: .72,
    thickness: 3, ior: 1.4, side: THREE.DoubleSide
  });
  const bagMat = new THREE.MeshPhysicalMaterial({
    color: 0xd8e4e2, roughness: .55, metalness: 0, transparent: true, opacity: .55,
    thickness: 1.4, ior: 1.45, side: THREE.DoubleSide
  });
  const lidMat = new THREE.MeshPhysicalMaterial({
    color: 0x0a6176, roughness: .28, metalness: .08, clearcoat: .4, clearcoatRoughness: .35
  });

  const porousMat = applySinteredGrain(new THREE.MeshPhysicalMaterial({
    color: 0xf1f1f1, roughness: .90, metalness: 0, envMapIntensity: 0.14,
    clearcoat: 0, side: THREE.DoubleSide
  }), {mobile: mob});

  const world = new THREE.Group();
  S.add(world);
  const p11G = new THREE.Group(); p11G.name = 'antibacterial';
  const p12G = new THREE.Group(); p12G.name = 'flowstop';
  const p16G = new THREE.Group(); p16G.name = 'porous';
  const bagG = new THREE.Group(); bagG.name = 'bag';
  const hoseG = new THREE.Group(); hoseG.name = 'hose';
  const p12Parts = {};
  world.add(hoseG, p11G, bagG, p12G, p16G);

  const loader = new GLTFLoader();
  function prep(src, assign, after){
    return new Promise((resolve, reject) => {
      loader.load(src, (g) => {
        g.scene.updateMatrixWorld(true);
        g.scene.traverse((o) => {
          if (!o.isMesh) return;
          let geo = o.geometry.clone().applyMatrix4(o.matrixWorld);
          geo = mergeVertices(geo, 1e-5);
          geo.computeVertexNormals();
          const mesh = new THREE.Mesh(geo, assign(o.name || ''));
          mesh.name = o.name || 'part';
          mesh.castShadow = mesh.receiveShadow = !mob;
          after && after(mesh);
        });
        resolve();
      }, undefined, reject);
    });
  }
  function centerOnFloor(group){
    const box = new THREE.Box3().setFromObject(group);
    const c = box.getCenter(new THREE.Vector3());
    group.children.forEach((ch) => { ch.position.x -= c.x; ch.position.z -= c.z; ch.position.y -= box.min.y; });
  }
  function longestAxis(group){
    const box = new THREE.Box3().setFromObject(group);
    const s = box.getSize(new THREE.Vector3());
    if (s.x >= s.y && s.x >= s.z) return 'x';
    if (s.y >= s.x && s.y >= s.z) return 'y';
    return 'z';
  }
  function axisToX(group){
    const a = longestAxis(group);
    if (a === 'y') group.rotation.z = -Math.PI / 2;
    else if (a === 'z') group.rotation.y = Math.PI / 2;
  }

  function makeHose(path){
    const curve = new THREE.CatmullRomCurve3(path, false, 'catmullrom', .35);
    const geo = new THREE.TubeGeometry(curve, 180, 3.2, 16, false);
    const mesh = new THREE.Mesh(geo, hoseMat);
    mesh.castShadow = !mob;
    hoseG.clear();
    hoseG.add(mesh);
  }

  let hoseY = 180;
  const P12_REST = {inlet: 0, inletCap: 0, barrel: 0, outletCap: 0, outlet: 0, cartridge: 0};
  const P12_EXPLODE = {inlet: -16, inletCap: -7, barrel: 0, outletCap: 7, outlet: 16, cartridge: 0};

  Promise.all([
    prep(SK('p11-cinematic/p11-disc-filter.glb'), (n) => n === 'ribs' ? ribMat : glass, (m) => p11G.add(m)),
    prep(SK('p12-cinematic/p12-inline-filter.glb'), (n) => n.includes('cartridge') ? cartMat : p12Glass, (m) => { p12G.add(m); p12Parts[m.name] = m; }),
    prep(SK('p16-cinematic/p16-porous-filter.glb'), () => porousMat, (m) => p16G.add(m)),
    prep(SK('p02-cinematic/p02-2l-cad.glb'), (n) => (n === 'bag' ? bagMat : lidMat), (m) => bagG.add(m))
  ]).then(() => {
    function bakeOrigin(group, stand){
      group.updateMatrixWorld(true);
      const box = new THREE.Box3().setFromObject(group);
      const c = box.getCenter(new THREE.Vector3());
      const y0 = stand ? box.min.y : c.y;
      group.children.forEach((m) => {
        if (m.isMesh) m.geometry.translate(-c.x, -y0, -c.z);
      });
      group.position.set(0, 0, 0);
      group.rotation.set(0, 0, 0);
      group.updateMatrixWorld(true);
    }
    function sizeOf(group){
      group.updateMatrixWorld(true);
      return new THREE.Box3().setFromObject(group).getSize(new THREE.Vector3());
    }
    function centerOf(group){
      group.updateMatrixWorld(true);
      return new THREE.Box3().setFromObject(group).getCenter(new THREE.Vector3());
    }
    function rotateAxisToX(group){
      const s = sizeOf(group);
      const axes = [['x', s.x], ['y', s.y], ['z', s.z]].sort((a, b) => a[1] - b[1]);
      // A disc has two equal long axes; the unique short axis is the bore / nozzles.
      // Otherwise use the longest axis (inline filter, bag parts).
      let axis = axes[2][0];
      if (Math.abs(axes[1][1] - axes[2][1]) < 1 && Math.abs(axes[2][1] - axes[0][1]) > 2) {
        axis = axes[0][0];
      }
      group.children.forEach((m) => {
        if (!m.isMesh) return;
        if (axis === 'y') m.geometry.rotateZ(-Math.PI / 2);
        else if (axis === 'z') m.geometry.rotateY(Math.PI / 2);
      });
      bakeOrigin(group, false);
    }

    bakeOrigin(bagG, true);
    bakeOrigin(p11G, false); rotateAxisToX(p11G);
    bakeOrigin(p12G, false); rotateAxisToX(p12G);
    bakeOrigin(p16G, true);

    const bagH = sizeOf(bagG).y;
    bagG.position.set(240, 0, 0);

    hoseY = Math.max(90, bagH * 0.90);
    const s11 = sizeOf(p11G);
    p11G.position.set(-90, hoseY, 0);

    p12G.position.set(240, hoseY + 22, 36);
    Object.keys(p12Parts).forEach((k) => {
      const m = p12Parts[k];
      m.userData.rest = m.position.clone();
    });

    p16G.rotation.set(0, 0, Math.PI / 2);
    p16G.position.copy(p12G.position);
    p16G.scale.setScalar(.01);
    p16G.visible = false;

    const b11 = new THREE.Box3().setFromObject(p11G);
    makeHose([
      new THREE.Vector3(b11.min.x - 240, hoseY + 8, -10),
      new THREE.Vector3(b11.min.x - 120, hoseY + 3, 0),
      new THREE.Vector3(b11.min.x - 6, hoseY, 0),
      new THREE.Vector3(b11.max.x + 6, hoseY, 0),
      new THREE.Vector3(b11.max.x + 90, hoseY + 6, 12),
      new THREE.Vector3(160, hoseY + 10, 24),
      new THREE.Vector3(230, hoseY + 8, 32)
    ]);

    const c11 = centerOf(p11G), c12 = centerOf(p12G), cBag = centerOf(bagG);
    // Rebuild camera path from real object centers.
    const midX = (c11.x + cBag.x) / 2;
    KF.splice(0, KF.length,
      [0,    c11.clone().add(V(-180, 50, 160)), c11.clone().add(V(-50, 0, 0))],
      [.10,  c11.clone().add(V(-100, 28, 110)), c11.clone()],
      [.20,  c11.clone().add(V(36, 18, 78)),    c11.clone()],
      [.30,  c11.clone().add(V(20, 50, 90)),    c11.clone().add(V(20, 0, 0))],
      [.40,  V(midX - 40, hoseY + 220, 720),    V(midX, hoseY * .4, 0)],
      [.52,  cBag.clone().add(V(260, 200, 520)), V(cBag.x, bagH * .55, cBag.z)],
      [.62,  c12.clone().add(V(120, 40, 160)),  c12.clone()],
      [.70,  c12.clone().add(V(90, 30, 110)),   c12.clone()],
      [.80,  c12.clone().add(V(110, 70, 170)),  c12.clone().add(V(0, 24, 0))],
      [.90,  c12.clone().add(V(80, 110, 200)),  c12.clone().add(V(0, 60, 0))],
      [1,    c12.clone().add(V(60, 130, 210)),  c12.clone().add(V(0, 80, 0))]
    );

    window.__ready = true;
    window.__hero_debug = {
      bagH, hoseY,
      c11: c11.toArray(), c12: c12.toArray(), cBag: cBag.toArray(),
      s11: s11.toArray(), s12: sizeOf(p12G).toArray(), sBag: sizeOf(bagG).toArray()
    };
    if (stillCapture) {
      const t0 = parseFloat(new URLSearchParams(location.search).get('cin') || root.getAttribute('data-cin-t') || '0.20') || 0.20;
      T = t0;
      requestAnimationFrame((now) => {
        frame(now, true);
        requestAnimationFrame(() => {
          frame(performance.now(), true);
          window.__still_capture = true;
          root.dispatchEvent(new CustomEvent('cin-still-ready', {bubbles: true}));
        });
      });
    }
  }).catch((e) => { console.error(e); window.__ready = 'error'; });

  function size(){
    const w = stage.clientWidth, h = stage.clientHeight;
    if (!w || !h) return;
    R.setSize(w, h, false);
    cv.style.width = w + 'px';
    cv.style.height = h + 'px';
    C.aspect = w / h;
    C.updateProjectionMatrix();
  }
  new ResizeObserver(size).observe(stage);
  size();

  const cl = (x) => Math.min(1, Math.max(0, x));
  const ease = (x) => { x = cl(x); return x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; };
  const seg = (t, a, b) => ease((t - a) / (b - a));
  const V = (x, y, z) => new THREE.Vector3(x, y, z);
  const beats = [...root.querySelectorAll('.beat')].map((e) => ({e, a: +e.dataset.a, b: +e.dataset.b}));
  const bar = root.querySelector('.cin-bar');
  const qp = new URLSearchParams(location.search);

  // Camera path tells the suction-path story. Units in mm.
  const KF = [
    [0,    V(-260, 210, 140), V(-140, 180, 0)],
    [.08,  V(-220, 200, 130), V(-100, 175, 0)],
    [.16,  V(-40,  195, 150), V(-70,  180, 0)],
    [.24,  V(20,   200, 120), V(-70,  185, 0)],
    [.32,  V(-30,  230, 90),  V(-70,  185, 0)],
    [.40,  V(80,   250, 280), V(80,   160, 0)],
    [.50,  V(280,  220, 260), V(210,  140, 10)],
    [.58,  V(250,  210, 90),  V(210,  200, 20)],
    [.66,  V(250,  230, 70),  V(210,  215, 28)],
    [.76,  V(270,  250, 110), V(210,  250, 28)],
    [.86,  V(250,  280, 90),  V(210,  280, 28)],
    [.94,  V(230,  300, 120), V(210,  300, 20)],
    [1,    V(220,  310, 130), V(210,  305, 16)]
  ];

  let T = 0, lastN = 0;
  const cp = new THREE.Vector3(), ct = new THREE.Vector3();
  let trackH = 1, trackTop = 0, onScreen = true, rafId = 0, looping = false, measureQueued = false;
  const cinStage = root.querySelector('.cin-stage') || stage;

  function measureTrack(){
    const stageH = (cinStage && cinStage.offsetHeight) || innerHeight || 1;
    trackH = Math.max(1, root.offsetHeight - stageH);
    trackTop = root.getBoundingClientRect().top + scrollY;
  }
  function requestMeasure(){
    if (measureQueued) return;
    measureQueued = true;
    requestAnimationFrame(() => { measureQueued = false; measureTrack(); });
  }
  measureTrack();
  addEventListener('resize', requestMeasure, {passive: true});
  if (window.visualViewport) visualViewport.addEventListener('resize', requestMeasure, {passive: true});
  if ('IntersectionObserver' in window) {
    new IntersectionObserver((ents) => {
      onScreen = ents.some((e) => e.isIntersecting);
      if (onScreen) ensureLoop();
    }, {root: null, threshold: 0, rootMargin: '80px 0px'}).observe(root);
  }
  document.addEventListener('visibilitychange', () => { if (!document.hidden) ensureLoop(); });

  function prog(){
    measureTrack();
    const scrolled = Math.min(trackH, Math.max(0, scrollY - trackTop));
    return cl(scrolled / trackH);
  }
  function sampleKF(t, outP, outT){
    let i = 0;
    while (i < KF.length - 2 && KF[i + 1][0] < t) i++;
    const a = KF[i], b = KF[i + 1];
    const u = b[0] === a[0] ? 0 : ease((t - a[0]) / (b[0] - a[0]));
    outP.copy(a[1]).lerp(b[1], u);
    outT.copy(a[2]).lerp(b[2], u);
  }

  function applyStory(t){
    const open = seg(t, .70, .82);
    const rise = seg(t, .78, .92);
    p12G.position.y = hoseY + 22 + 36 * open;
    // Explode the flow-stop so the finished porous core can come out.
    Object.keys(p12Parts).forEach((name) => {
      const m = p12Parts[name];
      if (!m || !m.userData.rest) return;
      const rest = m.userData.rest;
      const dx = (P12_EXPLODE[name] || 0) * open;
      m.position.set(rest.x + dx, rest.y, rest.z);
      if (name === 'cartridge') {
        m.position.y = rest.y + 10 * open;
        m.material.opacity = 1 - open * .85;
        m.material.transparent = open > .05;
        m.visible = open < .98;
      }
    });
    if (p16G.children.length) {
      const show = open > .08;
      p16G.visible = show;
      const sc = show ? (.15 + .85 * rise) : .01;
      p16G.scale.setScalar(sc);
      p16G.position.set(
        p12G.position.x,
        p12G.position.y + 8 + 46 * rise,
        p12G.position.z
      );
      // Stand the finished part upright as it leaves the housing.
      p16G.rotation.z = (Math.PI / 2) * (1 - rise);
    }
    // Softly dim the bag once we are close on the reveal.
    const bagFade = 1 - seg(t, .72, .88) * .35;
    bagG.traverse((o) => {
      if (o.isMesh && o.material && 'opacity' in o.material && o.parent === bagG) {
        /* bag already transparent; leave lid solid */
      }
    });
    bagG.visible = t < .96;
    if (bar) bar.style.width = (t * 100) + '%';
    beats.forEach((b) => {
      const on = t >= b.a && t <= b.b;
      b.e.style.opacity = on ? 1 : 0;
    });
  }

  function frame(now, once){
    const dt = Math.min(.1, (now - (lastN || now)) / 1000);
    lastN = now;
    const target = (qp.has('t') && !stillCapture) ? cl(parseFloat(qp.get('t'))) : (stillCapture ? T : prog());
    if (!stillCapture) T += (target - T) * (qp.has('t') ? 1 : 1 - Math.exp(-dt * 3.2));
    const t = stillCapture ? T : T;
    sampleKF(t, cp, ct);
    let fit = mob ? 1.35 : 1.18;
    if (t > .14 && t < .36) fit = Math.max(fit, mob ? 1.15 : 1.05);
    if (t > .62) fit = Math.max(fit, mob ? 1.25 : 1.12);
    cp.sub(ct).multiplyScalar(fit).add(ct);
    applyStory(t);
    C.position.copy(cp);
    C.lookAt(ct);
    const d = cp.distanceTo(ct);
    C.near = Math.max(1, d * .05);
    C.far = d + 2000;
    C.updateProjectionMatrix();
    R.render(S, C);
    if (!window.__cin_frame) {
      window.__cin_frame = true;
      root.dispatchEvent(new CustomEvent('cin-frame', {bubbles: true}));
    }
    if (!once && looping) rafId = requestAnimationFrame(frame);
  }
  function ensureLoop(){
    if (stillCapture || looping) return;
    if (!onScreen && document.hidden) return;
    looping = true;
    rafId = requestAnimationFrame(frame);
  }

  if (stillCapture) {
    root.classList.add('is-still');
  } else {
    root.classList.remove('is-still');
    root.classList.add('is-playing');
    ensureLoop();
    addEventListener('scroll', () => { if (onScreen) ensureLoop(); }, {passive: true});
  }
}
