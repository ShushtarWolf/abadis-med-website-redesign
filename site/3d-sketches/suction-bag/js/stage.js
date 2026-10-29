import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";
import { createProduct } from "./product.js";

export const THEMES = {
  light: {
    clear: 0xf3fafa,
    ground: 0xe7f3f3,
    hemiSky: 0xf7fffe,
    hemiGround: 0xb7ccc8,
    shadow: 0.22,
  },
  dark: {
    clear: 0x071416,
    ground: 0x071416,
    hemiSky: 0x2a4448,
    hemiGround: 0x041012,
    shadow: 0.45,
  },
};

export function createStage(canvas, { controls = true } = {}) {
  const renderer = new THREE.WebGLRenderer({
    canvas,
    antialias: true,
    alpha: false,
    preserveDrawingBuffer: true,
    powerPreference: "high-performance",
  });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.setSize(canvas.clientWidth || window.innerWidth, canvas.clientHeight || window.innerHeight, false);
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.05;
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.localClippingEnabled = true;
  renderer.setClearColor(THEMES.light.clear, 1);

  const scene = new THREE.Scene();
  scene.background = new THREE.Color(THEMES.light.clear);
  const pmrem = new THREE.PMREMGenerator(renderer);
  scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
  if ("environmentIntensity" in scene) scene.environmentIntensity = 0.72;

  const camera = new THREE.PerspectiveCamera(30, 1, 0.5, 6000);
  camera.position.set(188, 132, 236);

  let orbit = null;
  if (controls) {
    orbit = new OrbitControls(camera, canvas);
    orbit.enableDamping = true;
    orbit.dampingFactor = 0.08;
    orbit.target.set(0, 74, 0);
    orbit.minDistance = 90;
    orbit.maxDistance = 700;
    orbit.maxPolarAngle = Math.PI * 0.92;
    orbit.update();
  }

  const hemi = new THREE.HemisphereLight(THEMES.light.hemiSky, THEMES.light.hemiGround, 0.72);
  scene.add(hemi);
  const key = new THREE.DirectionalLight(0xfffaf4, 2.35);
  key.position.set(-90, 240, 150);
  key.castShadow = true;
  key.shadow.mapSize.set(2048, 2048);
  key.shadow.camera.near = 20;
  key.shadow.camera.far = 640;
  key.shadow.camera.left = -160;
  key.shadow.camera.right = 160;
  key.shadow.camera.top = 180;
  key.shadow.camera.bottom = -140;
  key.shadow.bias = -0.0008;
  key.shadow.normalBias = 0.8;
  scene.add(key);
  const fill = new THREE.DirectionalLight(0xd5ecee, 0.85);
  fill.position.set(160, 90, 70);
  scene.add(fill);
  const rim = new THREE.DirectionalLight(0xffffff, 1.25);
  rim.position.set(30, 80, -200);
  scene.add(rim);
  const interior = new THREE.PointLight(0xf4fffe, 6.5, 260, 2);
  interior.position.set(0, 78, 8);
  scene.add(interior);

  const product = createProduct();
  scene.add(product.root);

  const ground = new THREE.Mesh(
    new THREE.CircleGeometry(210, 80),
    new THREE.ShadowMaterial({ opacity: THEMES.light.shadow })
  );
  ground.rotation.x = -Math.PI / 2;
  ground.position.y = -0.15;
  ground.receiveShadow = true;
  scene.add(ground);

  const grid = new THREE.GridHelper(280, 28, 0x9bb8b6, 0xc5d9d7);
  grid.position.y = -0.05;
  grid.visible = false;
  scene.add(grid);

  function resize(w, h) {
    const width = w || canvas.clientWidth || window.innerWidth;
    const height = h || canvas.clientHeight || window.innerHeight;
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    renderer.setSize(width, height, false);
    camera.aspect = width / Math.max(1, height);
    camera.updateProjectionMatrix();
  }

  function setTheme(name) {
    const theme = THEMES[name] || THEMES.light;
    renderer.setClearColor(theme.clear, 1);
    scene.background = new THREE.Color(theme.clear);
    hemi.color.setHex(theme.hemiSky);
    hemi.groundColor.setHex(theme.hemiGround);
    ground.material.opacity = theme.shadow;
    const gridMats = Array.isArray(grid.material) ? grid.material : [grid.material];
    for (const mat of gridMats) {
      if (mat.color) mat.color.setHex(name === "dark" ? 0x245255 : 0xb7ccc8);
      mat.opacity = name === "dark" ? 0.55 : 0.85;
      mat.transparent = true;
    }
    product.setTheme(name === "dark" ? "dark" : "light");
    if ("environmentIntensity" in scene) scene.environmentIntensity = name === "dark" ? 0.55 : 0.72;
    renderer.toneMappingExposure = name === "dark" ? 0.98 : 1.05;
  }

  function setLook(look) {
    product.setLook(look);
    grid.visible = look === "cad";
  }

  function render(cam) {
    renderer.setScissorTest(false);
    renderer.render(scene, cam || camera);
  }

  return {
    THREE,
    renderer,
    scene,
    camera,
    orbit,
    product,
    ground,
    grid,
    resize,
    setTheme,
    setLook,
    render,
  };
}

export const PRESETS = {
  side: { pos: [0, 112, 430], target: [-18, 84, 0] },
  three: { pos: [210, 142, 268], target: [-14, 80, 0] },
  top: { pos: [42, 400, 108], target: [-12, 136, 0] },
  cad: { pos: [240, 180, 290], target: [-12, 84, 0] },
  exploded: { pos: [460, 340, 540], target: [-16, 188, 0] },
};

export function applyPreset(stage, name) {
  const p = PRESETS[name] || PRESETS.three;
  stage.camera.position.set(p.pos[0], p.pos[1], p.pos[2]);
  if (stage.orbit) {
    stage.orbit.target.set(p.target[0], p.target[1], p.target[2]);
    stage.orbit.update();
  } else {
    stage.camera.lookAt(p.target[0], p.target[1], p.target[2]);
  }
}
