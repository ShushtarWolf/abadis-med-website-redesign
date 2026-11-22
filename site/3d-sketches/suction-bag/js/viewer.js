import { CALLOUTS } from "./product.js";
import { applyPreset, createStage } from "./stage.js";

const canvas = document.getElementById("view");
const stage = createStage(canvas, { controls: true });
const params = new URLSearchParams(location.search);
const labelLayer = document.getElementById("labels");
const tmp = new stage.THREE.Vector3();

const ui = {
  theme: document.querySelectorAll("[data-theme-set]"),
  wire: document.getElementById("wire"),
  cut: document.getElementById("cut"),
  labels: document.getElementById("labels-toggle"),
  explode: document.getElementById("explode"),
  explodeOut: document.getElementById("explode-out"),
};

let theme = "light";
if (params.get("theme") === "dark" || params.get("theme") === "light") theme = params.get("theme");
let labelsOn = params.get("capture") === "1";

function faNum(value) {
  return String(value).replace(/\d/g, (d) => "۰۱۲۳۴۵۶۷۸۹"[d]);
}

function setTheme(next) {
  theme = next === "dark" ? "dark" : "light";
  document.documentElement.dataset.theme = theme;
  stage.setTheme(theme);
  ui.theme.forEach((btn) => btn.setAttribute("aria-pressed", btn.dataset.themeSet === theme ? "true" : "false"));
}

function syncToggles() {
  ui.wire.setAttribute("aria-pressed", ui.wire.dataset.on === "1" ? "true" : "false");
  ui.cut.setAttribute("aria-pressed", ui.cut.dataset.on === "1" ? "true" : "false");
  ui.labels.setAttribute("aria-pressed", labelsOn ? "true" : "false");
}

function buildLabels() {
  labelLayer.replaceChildren();
  for (const item of CALLOUTS) {
    const el = document.createElement("div");
    el.className = "tag";
    el.innerHTML = `<span class="fa">${item.fa}</span><span class="en" dir="ltr">${item.en}</span>`;
    labelLayer.append(el);
    item.el = el;
  }
}

function updateLabels() {
  const w = canvas.clientWidth;
  const h = canvas.clientHeight;
  const show = labelsOn;
  labelLayer.hidden = !show;
  if (!show) return;
  for (const item of CALLOUTS) {
    const obj = stage.product.anchors[item.id];
    if (!obj || !item.el) continue;
    obj.getWorldPosition(tmp);
    tmp.project(stage.camera);
    const x = (tmp.x * 0.5 + 0.5) * w;
    const y = (-tmp.y * 0.5 + 0.5) * h;
    const behind = tmp.z > 1;
    item.el.hidden = behind || x < -40 || y < -20 || x > w + 40 || y > h + 20;
    item.el.style.transform = `translate(${x}px, ${y}px)`;
  }
}

function resize() {
  stage.resize(canvas.clientWidth, canvas.clientHeight);
}

ui.theme.forEach((btn) => btn.addEventListener("click", () => setTheme(btn.dataset.themeSet)));
document.querySelectorAll("[data-preset]").forEach((btn) => {
  btn.addEventListener("click", () => applyPreset(stage, btn.dataset.preset));
});
ui.wire.addEventListener("click", () => {
  ui.wire.dataset.on = ui.wire.dataset.on === "1" ? "0" : "1";
  stage.product.setWireframe(ui.wire.dataset.on === "1");
  syncToggles();
});
ui.cut.addEventListener("click", () => {
  ui.cut.dataset.on = ui.cut.dataset.on === "1" ? "0" : "1";
  stage.product.setCutaway(ui.cut.dataset.on === "1" ? 1 : 0);
  syncToggles();
});
ui.labels.addEventListener("click", () => {
  labelsOn = !labelsOn;
  syncToggles();
});
ui.explode.addEventListener("input", () => {
  const t = Number(ui.explode.value) / 100;
  stage.product.setExplode(t);
  ui.explodeOut.textContent = faNum(ui.explode.value) + "٪";
});
document.getElementById("reset").addEventListener("click", () => {
  ui.explode.value = "0";
  ui.explodeOut.textContent = faNum(0) + "٪";
  ui.wire.dataset.on = "0";
  ui.cut.dataset.on = "0";
  labelsOn = false;
  stage.product.setExplode(0);
  stage.product.setCutaway(0);
  stage.product.setWireframe(false);
  stage.setLook("studio");
  applyPreset(stage, "three");
  syncToggles();
});

buildLabels();
setTheme(theme);
applyPreset(stage, "three");
syncToggles();
resize();
window.addEventListener("resize", resize);

let frames = 0;
function tick() {
  stage.orbit.update();
  stage.render();
  updateLabels();
  frames += 1;
  if (params.get("capture") === "1" && frames === 6) {
    document.fonts.ready.then(() => {
      window.__READY = true;
    });
  }
  requestAnimationFrame(tick);
}
requestAnimationFrame(tick);
