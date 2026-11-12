/**
 * On-tap solid 3D viewer for a single filter. Studio lighting, orbit after
 * load. Canvas uses touch-action: pan-y until live, then none.
 */
import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {RoomEnvironment} from 'three/addons/environments/RoomEnvironment.js';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
import {mergeVertices} from 'three/addons/utils/BufferGeometryUtils.js';
import {applySinteredGrain} from '../../3d-sketches/p16-cinematic/sintered-grain.js';

function pal(){
  const t = document.documentElement.dataset.theme;
  if (t === 'noir') return {bg: 0x141222, hemi: 0xf1f0ff, ground: 0x1c1730};
  if (t === 'dark') return {bg: 0x0a2425, hemi: 0xd7eeee, ground: 0x061719};
  return {bg: 0xc5d4d6, hemi: 0xf2f8f8, ground: 0x8aa3a6};
}

export function mount(host, {id, url, capture} = {}){
  const mob = matchMedia('(max-width:700px),(pointer:coarse)').matches;
  const R = new THREE.WebGLRenderer({antialias: true, alpha: true, preserveDrawingBuffer: !!capture, powerPreference: 'high-performance'});
  R.setPixelRatio(Math.min(devicePixelRatio, mob ? 1.6 : 2));
  R.toneMapping = THREE.ACESFilmicToneMapping;
  R.toneMappingExposure = 1.08;
  R.outputColorSpace = THREE.SRGBColorSpace;
  host.appendChild(R.domElement);
  Object.assign(R.domElement.style, {position: 'absolute', inset: '0', width: '100%', height: '100%', display: 'block', touchAction: 'none'});

  const S = new THREE.Scene();
  const pm = new THREE.PMREMGenerator(R);
  S.environment = pm.fromScene(new RoomEnvironment(), .05).texture;
  S.environmentIntensity = .42;
  pm.dispose();
  R.setRenderTarget(null);
  R.setScissorTest(false);
  const cam = new THREE.PerspectiveCamera(32, 1, .5, 2000);
  const ctl = new OrbitControls(cam, R.domElement);
  ctl.enableDamping = true;
  ctl.enablePan = false;
  ctl.minDistance = 20;
  ctl.maxDistance = 400;

  const key = new THREE.DirectionalLight(0xfff4ea, 1.35); key.position.set(40, 80, 50); S.add(key);
  const fillA = new THREE.DirectionalLight(0xe8f6ff, .9); fillA.position.set(-50, 30, 40); S.add(fillA);
  const fillB = new THREE.DirectionalLight(0xc0e8f7, .7); fillB.position.set(10, 40, -60); S.add(fillB);
  const hemi = new THREE.HemisphereLight(0xf2f8ff, 0x27303a, .8); S.add(hemi);

  const sc = document.createElement('canvas'); sc.width = sc.height = 256;
  const sx = sc.getContext('2d');
  const sg = sx.createRadialGradient(128, 128, 10, 128, 128, 128);
  sg.addColorStop(0, 'rgba(0,0,0,.45)'); sg.addColorStop(.5, 'rgba(0,0,0,.12)'); sg.addColorStop(1, 'rgba(0,0,0,0)');
  sx.fillStyle = sg; sx.fillRect(0, 0, 256, 256);
  const shadow = new THREE.Mesh(new THREE.PlaneGeometry(80, 80), new THREE.MeshBasicMaterial({map: new THREE.CanvasTexture(sc), transparent: true, depthWrite: false}));
  shadow.rotation.x = -Math.PI / 2; S.add(shadow);

  const glass = new THREE.MeshPhysicalMaterial({
    color: 0xe7f1f8, roughness: .08, metalness: 0, transparent: true, opacity: .38,
    depthWrite: false, thickness: 2.2, ior: 1.49, attenuationColor: 0xd9eef0, attenuationDistance: 80, side: THREE.DoubleSide
  });
  const ribMat = new THREE.MeshPhysicalMaterial({
    color: 0x6f97b8, roughness: .28, metalness: 0, transparent: true, opacity: .85, depthWrite: false, side: THREE.DoubleSide
  });
  const p12Glass = new THREE.MeshPhysicalMaterial({
    color: 0xf4f8f7, roughness: .06, metalness: 0, transparent: true, opacity: .36,
    depthWrite: false, thickness: 2.4, ior: 1.49, side: THREE.DoubleSide
  });
  const cartMat = new THREE.MeshStandardMaterial({color: 0xf4f0e6, roughness: .9, metalness: 0, envMapIntensity: .28, side: THREE.DoubleSide});
  const porousMat = applySinteredGrain(new THREE.MeshPhysicalMaterial({
    color: 0xf1f1f1, roughness: .90, metalness: 0, envMapIntensity: 0.14, side: THREE.DoubleSide
  }), {mobile: mob});

  function matFor(name){
    if (id === 'p16-porous-filter') return porousMat;
    if (id === 'p12-inline-filter') return name.includes('cartridge') ? cartMat : p12Glass;
    return name === 'ribs' ? ribMat : glass;
  }

  const rootG = new THREE.Group(); S.add(rootG);
  let dead = false, ready = false, raf = 0;

  function applyTheme(){
    const p = pal();
    R.setClearColor(p.bg, 1);
    hemi.color.setHex(p.hemi);
    hemi.groundColor.setHex(p.ground);
  }
  applyTheme();
  const themeObs = new MutationObserver(applyTheme);
  themeObs.observe(document.documentElement, {attributes: true, attributeFilter: ['data-theme']});

  function frame(){
    if (dead) return;
    ctl.update();
    R.render(S, cam);
    if (!capture) raf = requestAnimationFrame(frame);
  }

  function resize(){
    const w = host.clientWidth, h = host.clientHeight;
    if (!w || !h) return;
    R.setSize(w, h, false);
    R.domElement.style.width = w + 'px';
    R.domElement.style.height = h + 'px';
    cam.aspect = w / h;
    cam.updateProjectionMatrix();
  }
  const ro = new ResizeObserver(resize);
  ro.observe(host);
  resize();

  new GLTFLoader().load(url, (g) => {
    if (dead) return;
    g.scene.updateMatrixWorld(true);
    g.scene.traverse((o) => {
      if (!o.isMesh) return;
      let geo = o.geometry.clone().applyMatrix4(o.matrixWorld);
      geo = mergeVertices(geo, 1e-5);
      geo.computeVertexNormals();
      const m = new THREE.Mesh(geo, matFor(o.name || ''));
      m.name = o.name || 'part';
      rootG.add(m);
    });
    rootG.updateMatrixWorld(true);
    const box0 = new THREE.Box3().setFromObject(rootG);
    const c0 = box0.getCenter(new THREE.Vector3());
    rootG.children.forEach((m) => {
      if (m.isMesh) m.geometry.translate(-c0.x, -c0.y, -c0.z);
    });
    rootG.position.set(0, 0, 0);
    rootG.updateMatrixWorld(true);
    const box = new THREE.Box3().setFromObject(rootG);
    const c = box.getCenter(new THREE.Vector3());
    const size = box.getSize(new THREE.Vector3());
    const rad = Math.max(box.getBoundingSphere(new THREE.Sphere()).radius, .001);
    shadow.scale.setScalar(Math.max(1, rad / 16));
    shadow.position.set(c.x, box.min.y - rad * 0.02, c.z);
    const dist = rad * 3.4;
    cam.position.set(c.x + dist * 0.85, c.y + dist * 0.45, c.z + dist * 0.95);
    cam.up.set(0, 1, 0);
    cam.lookAt(c);
    cam.updateProjectionMatrix();
    ctl.target.copy(c);
    ctl.minDistance = rad * 1.3;
    ctl.maxDistance = rad * 10;
    ctl.update();
    resize();
    ready = true;
    host.classList.add('is-live');
    host.classList.remove('is-loading');
    window.__viewer_debug = {id, rad, size: size.toArray(), center: c.toArray(), cam: cam.position.toArray()};
    if (capture) {
      cam.lookAt(c);
      R.render(S, cam);
      window.__still_capture = true;
    } else {
      frame();
    }
    }, undefined, () => {
    host.classList.remove('is-loading');
    host.classList.add('is-still-only');
  });

  const it = {
    dispose(){
      dead = true;
      cancelAnimationFrame(raf);
      ro.disconnect();
      themeObs.disconnect();
      ctl.dispose();
      R.dispose();
      if (R.domElement.parentNode) R.domElement.parentNode.removeChild(R.domElement);
    }
  };
  return it;
}
