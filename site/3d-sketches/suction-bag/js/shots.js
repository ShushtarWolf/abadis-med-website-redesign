import * as THREE from "three";
import { CALLOUTS } from "./product.js";
import { createStage, PRESETS } from "./stage.js";

const params = new URLSearchParams(location.search);
const shot = params.get("shot") || "1";
const theme = params.get("theme") === "dark" ? "dark" : "light";
const canvas = document.getElementById("view");
const hud = document.getElementById("hud");
const stage = createStage(canvas, { controls: false });

document.documentElement.dataset.theme = theme;
stage.setTheme(theme);
stage.resize(window.innerWidth, window.innerHeight);

const v = new THREE.Vector3();

function project(obj, cam, w, h) {
  obj.getWorldPosition(v);
  v.project(cam);
  return {
    x: (v.x * 0.5 + 0.5) * w,
    y: (-v.y * 0.5 + 0.5) * h,
    z: v.z,
  };
}

function persp(preset, aspect, fov = 30) {
  const cam = new THREE.PerspectiveCamera(fov, aspect, 0.5, 6000);
  cam.position.set(preset.pos[0], preset.pos[1], preset.pos[2]);
  cam.lookAt(preset.target[0], preset.target[1], preset.target[2]);
  cam.userData.target = preset.target;
  return cam;
}

function ortho(aspect) {
  const half = 198;
  const cam = new THREE.OrthographicCamera(-half * aspect, half * aspect, half, -half, 0.5, 6000);
  cam.position.set(250, 190, 300);
  cam.lookAt(-16, 88, 0);
  cam.zoom = 1.02;
  cam.updateProjectionMatrix();
  return cam;
}

function dimSvg(cam) {
  const w = window.innerWidth;
  const h = window.innerHeight;
  const a = stage.product.anchors;
  const L = project(a.dimL, cam, w, h);
  const R = project(a.dimR, cam, w, h);
  const B = project(a.dimBot, cam, w, h);
  const T = project(a.dimTop, cam, w, h);
  const mx = (L.x + R.x) / 2;
  const my = (L.y + R.y) / 2 - 18;
  const hx = (B.x + T.x) / 2 + 16;
  const hy = (B.y + T.y) / 2;
  return `
    <svg class="overlay" viewBox="0 0 ${w} ${h}" width="${w}" height="${h}">
      <defs>
        <marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
          <path d="M0,0 L7,3 L0,6 Z" fill="currentColor"/>
        </marker>
      </defs>
      <line x1="${L.x}" y1="${L.y}" x2="${L.x}" y2="${L.y - 28}" />
      <line x1="${R.x}" y1="${R.y}" x2="${R.x}" y2="${R.y - 28}" />
      <line x1="${L.x}" y1="${L.y - 22}" x2="${R.x}" y2="${R.y - 22}" marker-start="url(#arr)" marker-end="url(#arr)" />
      <line x1="${B.x}" y1="${B.y}" x2="${B.x + 36}" y2="${B.y}" />
      <line x1="${T.x}" y1="${T.y}" x2="${T.x + 36}" y2="${T.y}" />
      <line x1="${B.x + 28}" y1="${B.y}" x2="${T.x + 28}" y2="${T.y}" marker-start="url(#arr)" marker-end="url(#arr)" />
    </svg>
    <div class="dim dim-d" style="left:${mx}px;top:${my}px">قطر ۱۱ سانتی‌متر<span dir="ltr">Ø 11 cm</span></div>
    <div class="dim dim-h" style="left:${hx}px;top:${hy}px">ارتفاع ۱۵٫۵ سانتی‌متر<span dir="ltr">15.5 cm</span></div>
    <div class="plate">
      <b>آبادیس مد</b>
      <strong>کیسه ساکشن یکبار مصرف ۱ لیتری</strong>
      <span>اسکچ فنی · خط و سایه</span>
      <span dir="ltr">CAD wireframe + shade</span>
    </div>
  `;
}

function calloutSvg(cam) {
  const w = window.innerWidth;
  const h = window.innerHeight;
  const place = {
    cap: { x: 36, y: 78 },
    lid: { x: 36, y: 168 },
    patient: { x: 36, y: 258 },
    vacuum: { x: 36, y: 348 },
    aux: { x: w - 250, y: 78 },
    filter: { x: w - 250, y: 188 },
    body: { x: w - 250, y: 298 },
    pouch: { x: w - 250, y: 408 },
  };
  const cards = [];
  const lines = [];
  for (const item of CALLOUTS) {
    const obj = stage.product.anchors[item.id];
    const p = project(obj, cam, w, h);
    const box = place[item.id];
    const x2 = box.x < w / 2 ? box.x + 200 : box.x;
    const y2 = box.y + 22;
    lines.push(`<line x1="${p.x}" y1="${p.y}" x2="${x2}" y2="${y2}" />`);
    lines.push(`<circle cx="${p.x}" cy="${p.y}" r="3.5" />`);
    cards.push(
      `<div class="call" style="left:${box.x}px;top:${box.y}px"><span class="fa">${item.fa}</span><span class="en" dir="ltr">${item.en}</span></div>`
    );
  }
  return `
    <svg class="overlay" viewBox="0 0 ${w} ${h}" width="${w}" height="${h}">${lines.join("")}</svg>
    ${cards.join("")}
    <div class="plate">
      <b>آبادیس مد</b>
      <strong>نمای انفجاری و برش</strong>
      <span>درب · فیلتر هیدروفوبیک · بدنه · پودر ژل‌کننده</span>
      <span dir="ltr">Exploded cutaway</span>
    </div>
  `;
}

function triptychCaptions() {
  return `
    <div class="caps">
      <div><span>نمای جانبی</span><span dir="ltr">Side</span></div>
      <div><span>سه‌ربع</span><span dir="ltr">Three-quarter</span></div>
      <div><span>نمای بالا</span><span dir="ltr">Top</span></div>
    </div>
    <div class="plate plate-top">
      <b>آبادیس مد</b>
      <strong>کیسه ساکشن یکبار مصرف ۱ لیتری</strong>
      <span dir="ltr">Studio views · frosted liner</span>
    </div>
  `;
}

let draw = () => {};
const w = window.innerWidth;
const h = window.innerHeight;

if (shot === "1") {
  stage.setLook("cad");
  stage.product.setWireframe(true);
  stage.product.setExplode(0);
  stage.product.setCutaway(0);
  const cam = ortho(w / h);
  draw = () => {
    stage.render(cam);
    hud.innerHTML = dimSvg(cam);
  };
} else if (shot === "2") {
  stage.setLook("studio");
  stage.product.setWireframe(false);
  stage.product.setExplode(0);
  stage.product.setCutaway(0);
  const aspect = w / 3 / h;
  const cams = [
    persp({ pos: [0, 140, 620], target: [-22, 90, 0] }, aspect, 24),
    persp({ pos: [280, 170, 360], target: [-18, 84, 0] }, aspect, 26),
    persp({ pos: [8, 560, 48], target: [-20, 148, 0] }, aspect, 24),
  ];
  draw = () => {
    const rw = stage.renderer.domElement.width;
    const rh = stage.renderer.domElement.height;
    const slice = Math.floor(rw / 3);
    stage.renderer.setScissorTest(true);
    stage.renderer.autoClear = false;
    cams.forEach((cam, i) => {
      const x = i * slice;
      const width = i === 2 ? rw - x : slice;
      stage.renderer.setViewport(x, 0, width, rh);
      stage.renderer.setScissor(x, 0, width, rh);
      stage.renderer.clear();
      stage.renderer.render(stage.scene, cam);
    });
    stage.renderer.setScissorTest(false);
    stage.renderer.autoClear = true;
    hud.innerHTML = triptychCaptions();
  };
} else {
  stage.setLook("studio");
  stage.product.setWireframe(true);
  stage.product.setExplode(1);
  stage.product.setCutaway(1);
  const cam = persp(PRESETS.exploded, w / h, 34);
  draw = () => {
    stage.render(cam);
    hud.innerHTML = calloutSvg(cam);
  };
}

let n = 0;
function frame() {
  draw();
  n += 1;
  if (n < 4) {
    requestAnimationFrame(frame);
    return;
  }
  document.fonts.ready.then(() => {
    draw();
    requestAnimationFrame(() => {
      window.__READY = true;
    });
  });
}
frame();
