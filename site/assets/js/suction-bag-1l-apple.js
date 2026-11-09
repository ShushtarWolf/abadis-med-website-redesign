/**
 * Apple-style hero orbit + scroll-story for the APPROVED 1L suction bag model
 * (solid Abadis teal HDPE lid — same recipe as suction-bag-1l-3d.js / commits
 * 9182584b, 9e09a22f, 881a968e). Lazy: Three.js loads after first paint / in-view.
 * Poster = real product photo. Reduced-motion / no-WebGL → stills only.
 */
const TEAL = 0x0f9a9c;
const TEAL_EM = 0x0a6f71;

function webglOk() {
  try {
    const c = document.createElement('canvas');
    return !!(c.getContext('webgl') || c.getContext('experimental-webgl'));
  } catch {
    return false;
  }
}

function ease(t) {
  return t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
}
function seg(t, a, b) {
  if (t <= a) return 0;
  if (t >= b) return 1;
  return (t - a) / (b - a);
}

function fitCamera(THREE, camera, object, { fill = 0.6, pad = 1.35, preferY = 2 } = {}) {
  const box = new THREE.Box3().setFromObject(object);
  const size = new THREE.Vector3();
  const center = new THREE.Vector3();
  box.getSize(size);
  box.getCenter(center);
  // Recenter object so geometry sits around origin mid-height
  object.position.sub(center);
  object.position.y += preferY;
  const maxDim = Math.max(size.x, size.y, size.z);
  const fov = (camera.fov * Math.PI) / 180;
  // Distance so the bag occupies ~fill of the shorter view axis
  let dist = Math.abs((maxDim / fill) / 2 / Math.tan(fov / 2));
  dist *= pad;
  return { dist, size, maxDim };
}

async function loadThree() {
  const three = await import('./three.module.js');
  const { OrbitControls } = await import('./OrbitControls.js');
  return { THREE: three, OrbitControls };
}

/** Build the approved 1L bag group (teal solid lid + translucent liner). */
function buildApprovedBag(THREE) {
  const root = new THREE.Group();
  const lidG = new THREE.Group();
  const bagG = new THREE.Group();
  root.add(lidG, bagG);

  const lidMat = new THREE.MeshStandardMaterial({
    color: TEAL,
    emissive: TEAL_EM,
    emissiveIntensity: 0.45,
    roughness: 0.48,
    metalness: 0.02,
  });
  // Frosted translucent liner — matches product photos / Hamid refs (inner tube visible)
  const bagMat = new THREE.MeshPhysicalMaterial({
    color: 0xeef6f7,
    roughness: 0.42,
    metalness: 0,
    transparent: true,
    opacity: 0.42,
    transmission: 0.62,
    thickness: 2.2,
    ior: 1.42,
    attenuationColor: new THREE.Color(0xd8ecee),
    attenuationDistance: 18,
    depthWrite: false,
    side: THREE.DoubleSide,
  });
  const rimMat = new THREE.MeshStandardMaterial({
    color: 0xd5e8ea,
    roughness: 0.28,
    metalness: 0.05,
    transparent: true,
    opacity: 0.22,
    depthWrite: false,
    side: THREE.FrontSide,
  });

  // Pillow-dome lid (Hamid ref / 881a968e + 9182584b)
  const lidProfile = [
    [11.0, 12.0], [11.4, 12.4], [11.4, 14.6], [12.2, 15.2], [12.7, 15.6],
    [13.0, 16.8], [13.0, 17.6], [12.6, 17.8], [11.0, 17.8], [10.7, 18.45],
    [10.2, 19.25], [9.3, 19.8], [7.9, 20.08], [5.6, 20.2], [3.0, 20.22], [0.01, 20.23],
  ].map(([r, y]) => new THREE.Vector2(r, y));
  lidG.add(new THREE.Mesh(new THREE.LatheGeometry(lidProfile, 64), lidMat));

  // VACUUM well (recessed round) + thick angled port
  const well = new THREE.Mesh(new THREE.CylinderGeometry(2.6, 2.6, 0.7, 32), lidMat);
  well.position.set(-6.2, 19.85, 0.8);
  lidG.add(well);
  const vac = new THREE.Mesh(new THREE.CylinderGeometry(1.15, 1.35, 5.2, 20), lidMat);
  vac.rotation.z = 0.55;
  vac.position.set(5.2, 20.2, -4.2);
  lidG.add(vac);

  // PATIENT — long thin horizontal tube in rim slot
  const pat = new THREE.Mesh(new THREE.CylinderGeometry(0.55, 0.55, 7.2, 16), lidMat);
  pat.rotation.z = Math.PI / 2;
  pat.position.set(-5.2, 19.6, 6.2);
  lidG.add(pat);

  // Tandem stem in central pit
  const tan = new THREE.Mesh(new THREE.CylinderGeometry(0.45, 0.45, 4.2, 14), lidMat);
  tan.position.set(1.6, 22.2, -7.2);
  lidG.add(tan);

  // Inner hydrophobic filter tube (visible through frosted liner)
  const filterTube = new THREE.Mesh(
    new THREE.CylinderGeometry(1.55, 1.85, 16, 24),
    new THREE.MeshStandardMaterial({ color: 0x0a7072, roughness: 0.55, metalness: 0.04 }),
  );
  filterTube.position.set(-1.2, 1.5, 0.4);
  bagG.add(filterTube);
  const filterCage = new THREE.Mesh(
    new THREE.CylinderGeometry(2.35, 2.55, 5.5, 10, 1, true),
    new THREE.MeshStandardMaterial({ color: 0x0c8588, roughness: 0.5, metalness: 0.06, transparent: true, opacity: 0.85 }),
  );
  filterCage.position.set(-1.2, 6.2, 0.4);
  bagG.add(filterCage);

  // 1L liner proportions: Ø11 × H15.5 cm (scene units ~ matching suction-bag-1l-3d)
  const liner = new THREE.Mesh(new THREE.CylinderGeometry(10.2, 9.4, 28, 48, 1, true), bagMat);
  liner.position.y = -2;
  bagG.add(liner);
  // Subtle fresnel rim shell (slightly larger, low opacity)
  const rim = new THREE.Mesh(new THREE.CylinderGeometry(10.45, 9.65, 28, 48, 1, true), rimMat);
  rim.position.y = -2;
  bagG.add(rim);
  const bottom = new THREE.Mesh(new THREE.CircleGeometry(9.4, 48), bagMat);
  bottom.rotation.x = Math.PI / 2;
  bottom.position.y = -16;
  bagG.add(bottom);

  // Collar under lid
  const collar = new THREE.Mesh(
    new THREE.TorusGeometry(11.2, 0.55, 10, 48),
    new THREE.MeshStandardMaterial({ color: 0xb8c8ca, roughness: 0.45, metalness: 0.05 }),
  );
  collar.rotation.x = Math.PI / 2;
  collar.position.y = 11.2;
  bagG.add(collar);

  root.userData = { lidG, bagG };
  return root;
}

function setupLights(THREE, scene) {
  scene.add(new THREE.AmbientLight(0xb8d0d2, 0.55));
  const key = new THREE.DirectionalLight(0xfff2ea, 1.35);
  key.position.set(-40, 80, 50);
  scene.add(key);
  const rim = new THREE.DirectionalLight(0x7ecad4, 0.95);
  rim.position.set(60, 30, -50);
  scene.add(rim);
  const fill = new THREE.DirectionalLight(0xfff8f2, 0.7);
  fill.position.set(20, 40, 60);
  scene.add(fill);
  // teal floor glow
  const c = document.createElement('canvas');
  c.width = c.height = 128;
  const x = c.getContext('2d');
  const g = x.createRadialGradient(64, 64, 0, 64, 64, 64);
  g.addColorStop(0, 'rgba(46,127,150,.4)');
  g.addColorStop(1, 'rgba(46,127,150,0)');
  x.fillStyle = g;
  x.fillRect(0, 0, 128, 128);
  const floor = new THREE.Mesh(
    new THREE.PlaneGeometry(120, 120),
    new THREE.MeshBasicMaterial({ map: new THREE.CanvasTexture(c), transparent: true, depthWrite: false }),
  );
  floor.rotation.x = -Math.PI / 2;
  floor.position.y = -17;
  scene.add(floor);
}


async function applyEnv(THREE, renderer, scene) {
  try {
    const { RoomEnvironment } = await import('../vendor/three/examples/jsm/environments/RoomEnvironment.js');
    const pmrem = new THREE.PMREMGenerator(renderer);
    scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
    pmrem.dispose();
  } catch (e) {
    // Fallback: soft gradient cube so transmission is not flat gray
    const c = document.createElement('canvas');
    c.width = c.height = 64;
    const ctx = c.getContext('2d');
    const g = ctx.createLinearGradient(0, 0, 0, 64);
    g.addColorStop(0, '#cfe8ea');
    g.addColorStop(0.55, '#6a9ea4');
    g.addColorStop(1, '#142428');
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, 64, 64);
    const tex = new THREE.CanvasTexture(c);
    tex.mapping = THREE.EquirectangularReflectionMapping;
    scene.environment = tex;
  }
}

async function mountHero(root) {
  const canvas = root.querySelector('canvas');
  const poster = root.querySelector('.bag-hero-poster');
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!webglOk() || reduced) {
    root.classList.add('no-gl');
    return;
  }
  const { THREE } = await loadThree();
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, powerPreference: 'high-performance' });
  renderer.setPixelRatio(Math.min(devicePixelRatio || 1, 1.75));
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.05;
  const scene = new THREE.Scene();
  setupLights(THREE, scene);
  await applyEnv(THREE, renderer, scene);
  const mob = matchMedia('(max-width:700px),(pointer:coarse)').matches;
  const camera = new THREE.PerspectiveCamera(mob ? 34 : 28, 1, 0.5, 600);
  const bag = buildApprovedBag(THREE);
  scene.add(bag);
  // Keep whole bag in the UPPER stage band (CSS clips stage above the copy)
  const fit = fitCamera(THREE, camera, bag, {
    fill: mob ? 0.72 : 0.68,
    pad: mob ? 1.06 : 1.05,
    preferY: mob ? 2 : 1.5,
  });
  let baseDist = fit.dist;

  function resize() {
    const w = root.clientWidth || 1;
    const h = root.clientHeight || 1;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
    const fov = (camera.fov * Math.PI) / 180;
    const fill = mob ? 0.70 : 0.66;
    baseDist = Math.abs((fit.maxDim / fill) / 2 / Math.tan(fov / 2)) * (mob ? 1.08 : 1.05);
  }
  resize();
  new ResizeObserver(resize).observe(root);

  let playing = true;
  let t0 = performance.now();
  const CYCLE = 16000;
  root.classList.add('is-gl');

  function frame(now) {
    requestAnimationFrame(frame);
    if (!playing) return;
    const u = ((now - t0) % CYCLE) / CYCLE;
    const ang = -0.7 + u * Math.PI * 2;
    const elev = 0.18 + 0.04 * Math.sin(u * Math.PI * 2);
    const dist = baseDist * (1.0 + 0.03 * Math.sin(u * Math.PI * 2));
    // Look above origin so the bag sits in the upper hero band, clear of the headline
    const targetY = mob ? 1.2 : 1.0;
    camera.position.set(
      Math.cos(ang) * dist * Math.cos(elev),
      targetY + 2 + Math.sin(elev) * dist * 0.28,
      Math.sin(ang) * dist * Math.cos(elev),
    );
    camera.lookAt(0, targetY, 0);
    const lift = 0.2 * Math.max(0, Math.sin(u * Math.PI * 2));
    bag.userData.lidG.position.y = lift;
    renderer.render(scene, camera);
  }
  requestAnimationFrame(frame);

  const io = new IntersectionObserver((entries) => {
    for (const e of entries) playing = e.isIntersecting;
  }, { threshold: 0.15 });
  io.observe(root);
  if (poster) poster.setAttribute('aria-hidden', 'true');
}

async function mountStory(root) {
  const canvas = root.querySelector('canvas');
  const stills = [...root.querySelectorAll('.bag-story-still')];
  const beats = [...root.querySelectorAll('.bag-story-beat')];
  const bar = root.querySelector('.bag-story-bar');
  const track = root.closest('.bag-story')?.querySelector('.bag-story-track') || root.parentElement;
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;

  function setProgress(u) {
    beats.forEach((b, i) => {
      const a = +b.dataset.a;
      const bb = +b.dataset.b;
      const on = u >= a && u < bb;
      b.classList.toggle('is-on', on);
    });
    if (bar) bar.style.transform = `scaleX(${u})`;
    // stills fallback frames
    if (stills.length) {
      const idx = Math.min(stills.length - 1, Math.floor(u * stills.length));
      stills.forEach((s, i) => {
        s.style.opacity = i === idx ? '1' : '0';
      });
    }
  }

  function progress() {
    const rect = track.getBoundingClientRect();
    const total = track.offsetHeight - innerHeight;
    const scrolled = Math.min(total, Math.max(0, -rect.top));
    return total > 0 ? scrolled / total : 0;
  }

  if (!webglOk() || reduced) {
    root.classList.add('no-gl');
    const onScroll = () => setProgress(progress());
    addEventListener('scroll', onScroll, { passive: true });
    onScroll();
    return;
  }

  const { THREE } = await loadThree();
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, powerPreference: 'high-performance' });
  renderer.setPixelRatio(Math.min(devicePixelRatio || 1, 1.75));
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.05;
  const scene = new THREE.Scene();
  setupLights(THREE, scene);
  await applyEnv(THREE, renderer, scene);
  const mob = matchMedia('(max-width:700px),(pointer:coarse)').matches;
  const camera = new THREE.PerspectiveCamera(mob ? 34 : 28, 1, 0.5, 500);
  const bag = buildApprovedBag(THREE);
  scene.add(bag);
  const fit = fitCamera(THREE, camera, bag, { fill: 0.50, pad: 1.15, preferY: 3 });
  let baseDist = fit.dist;
  root.classList.add('is-gl');
  // Hide stills once live GL is up
  stills.forEach((s) => { s.style.opacity = '0'; s.style.visibility = 'hidden'; });

  function resize() {
    const w = root.clientWidth || 1;
    const h = root.clientHeight || 1;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
    const fov = (camera.fov * Math.PI) / 180;
    baseDist = Math.abs((fit.maxDim / 0.48) / 2 / Math.tan(fov / 2)) * 1.15;
  }
  resize();
  new ResizeObserver(resize).observe(root);

  let u = 0;
  function apply(u) {
    setProgress(u);
    // Camera path: establish → lid lift → ports → seal → gel settle (whole bag always in frame)
    const ang = -0.45 + u * Math.PI * 1.55;
    const elev = 0.2 + 0.12 * Math.sin(u * Math.PI);
    const dist = baseDist * (1.05 - 0.08 * ease(seg(u, 0.1, 0.5)));
    camera.position.set(
      Math.cos(ang) * dist * Math.cos(elev),
      3 + Math.sin(elev) * dist * 0.45,
      Math.sin(ang) * dist * Math.cos(elev),
    );
    camera.lookAt(0, 2, 0);
    const lift = ease(seg(u, 0.12, 0.28)) * (1 - ease(seg(u, 0.55, 0.7)));
    bag.userData.lidG.position.y = lift * 3.8;
    bag.userData.bagG.position.y = -lift * 1.0;
    renderer.render(scene, camera);
  }

  function onScroll() {
    u = progress();
    apply(u);
  }
  addEventListener('scroll', onScroll, { passive: true });
  onScroll();
  requestAnimationFrame(function loop() {
    requestAnimationFrame(loop);
    // keep rendering while pinned for smooth scrub
    if (root.getBoundingClientRect().bottom > 0 && root.getBoundingClientRect().top < innerHeight) {
      apply(u);
    }
  });
}

function bootSticky() {
  const bar = document.querySelector('.bag-sticky');
  const hero = document.querySelector('.bag-hero');
  if (!bar || !hero) return;
  const io = new IntersectionObserver(
    (entries) => {
      for (const e of entries) bar.classList.toggle('is-on', !e.isIntersecting);
    },
    { threshold: 0.2 },
  );
  io.observe(hero);
}

function boot() {
  bootSticky();
  const hero = document.querySelector('[data-bag-apple-hero]');
  const story = document.querySelector('[data-bag-apple-story]');
  // Defer Three until idle / in view
  const start = () => {
    if (hero) mountHero(hero);
    if (story) mountStory(story);
  };
  if ('requestIdleCallback' in window) requestIdleCallback(start, { timeout: 1800 });
  else setTimeout(start, 400);

  // Also boot approved f3d cutaway without gate when present
  document.querySelectorAll('.f3d--bag.apple-mode').forEach((sec) => {
    sec.classList.remove('is-gated');
    const gate = sec.querySelector('.f3d-gate');
    if (gate) gate.remove();
  });
}

if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
else boot();
