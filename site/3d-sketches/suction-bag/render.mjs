/**
 * Regenerates the suction-bag sketch stills and comparison sheets.
 * Needs a static server rooted at site/ and puppeteer-core + system Chrome.
 *
 *   python3 -m http.server 8080 --directory site
 *   NODE_PATH=/tmp/pw/node_modules node site/3d-sketches/suction-bag/render.mjs
 */
import { mkdir } from "node:fs/promises";

const puppeteerMod = await import(process.env.PUPPETEER || "puppeteer-core");
const puppeteer = puppeteerMod.default ?? puppeteerMod;

const browser = await puppeteer.launch({
  executablePath: process.env.CHROME || "/usr/bin/google-chrome",
  headless: "new",
  args: [
    "--use-gl=angle",
    "--use-angle=swiftshader",
    "--enable-webgl",
    "--ignore-gpu-blocklist",
    "--enable-unsafe-swiftshader",
    "--hide-scrollbars",
    "--no-sandbox",
    "--disable-dev-shm-usage",
  ],
});

const base = process.env.SKETCH_ORIGIN || "http://127.0.0.1:8080/3d-sketches/suction-bag/";
const outDir = new URL("./renders/", import.meta.url);

async function shoot(url, path, width, height) {
  const page = await browser.newPage();
  page.on("pageerror", (err) => console.error("PAGEERROR", url, err.message));
  page.on("console", (msg) => {
    if (msg.type() === "error") console.error("CONSOLE", url, msg.text());
  });
  await page.setCacheEnabled(false);
  await page.setViewport({ width, height, deviceScaleFactor: 2 });
  await page.goto(url, { waitUntil: "networkidle0", timeout: 90000 });
  await page.waitForFunction("window.__READY === true", { timeout: 120000 });
  await page.screenshot({ path, type: "png" });
  await page.close();
  console.log(path);
}

await mkdir(outDir, { recursive: true });
const jobs = [
  ["render.html?shot=1&theme=light", "style-1-light.png", 1400, 980],
  ["render.html?shot=1&theme=dark", "style-1-dark.png", 1400, 980],
  ["render.html?shot=2&theme=light", "style-2-light.png", 1680, 780],
  ["render.html?shot=2&theme=dark", "style-2-dark.png", 1680, 780],
  ["render.html?shot=3&theme=light", "style-3-light.png", 1400, 1000],
  ["render.html?shot=3&theme=dark", "style-3-dark.png", 1400, 1000],
  ["index.html?capture=1&theme=light", "style-4-light.png", 1440, 900],
  ["index.html?capture=1&theme=dark", "style-4-dark.png", 1440, 900],
];
for (const [url, name, w, h] of jobs) {
  await shoot(base + url, new URL(name, outDir).pathname, w, h);
}
await shoot(base + "sheet.html?theme=light", new URL("../suction-bag-3d-sketch-candidates.png", outDir).pathname, 2000, 1500);
await shoot(base + "sheet.html?theme=dark", new URL("../suction-bag-3d-sketch-candidates-dark.png", outDir).pathname, 2000, 1500);
await browser.close();
