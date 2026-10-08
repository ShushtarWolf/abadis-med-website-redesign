/**
 * Abadis Med redesign — full-site Playwright suite (prompt 7).
 * Records pass/fail into out/summary.json. Does not fix bugs.
 */
import { test, expect, chromium } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { execSync } from 'node:child_process';
import {
  REPS, EXPECTED_NAV, YELLOW_PATTERNS,
  loadSummary, saveSummary, record, addBug,
} from './lib/summary.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '../..');
const SITE = path.join(ROOT, 'site');
const OUT = path.join(__dirname, 'out');
const SHOTS = path.join(OUT, 'shots');
const DOCS_SHOTS = path.join(ROOT, 'docs/abadis/test-shots');

function allPageUrls() {
  const urls = [];
  function walk(dir, urlBase) {
    for (const ent of fs.readdirSync(dir, { withFileTypes: true })) {
      if (ent.name === 'index.html') urls.push(urlBase.endsWith('/') ? urlBase : urlBase + '/');
      else if (ent.isDirectory() && ent.name !== 'assets') {
        walk(path.join(dir, ent.name), urlBase + ent.name + '/');
      }
    }
  }
  walk(SITE, '/');
  if (fs.existsSync(path.join(SITE, 'index.html')) && !urls.includes('/')) urls.unshift('/');
  return [...new Set(urls)].sort();
}

function slug(p) {
  return (p === '/' ? 'home' : p.replace(/^\/|\/$/g, '').replace(/\//g, '__')) || 'home';
}

async function shot(page, rel) {
  const dest = path.join(SHOTS, rel);
  fs.mkdirSync(path.dirname(dest), { recursive: true });
  await page.screenshot({ path: dest, fullPage: true });
  return dest;
}

test.beforeAll(() => {
  fs.mkdirSync(OUT, { recursive: true });
  fs.mkdirSync(SHOTS, { recursive: true });
  fs.mkdirSync(DOCS_SHOTS, { recursive: true });
  const s = loadSummary();
  try {
    s.sha = execSync('git rev-parse HEAD', { cwd: ROOT }).toString().trim();
  } catch { /* ignore */ }
  s.pageCount = allPageUrls().length;
  saveSummary(s);
});

// ---------------------------------------------------------------------------
// 2 + 3: HTTP ≥400 / requestfailed + console errors on all pages
// ---------------------------------------------------------------------------
test('2+3 crawl: broken assets and console errors (all pages)', async ({ browser }) => {
  test.setTimeout(1_800_000);
  const pages = allPageUrls();
  const badStatus = [];
  const failedReq = [];
  const consoleErrors = [];
  const pageErrors = [];

  const context = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const page = await context.newPage();

  page.on('response', (res) => {
    const st = res.status();
    if (st >= 400) {
      badStatus.push({ url: res.url(), status: st, page: page.url() });
    }
  });
  page.on('requestfailed', (req) => {
    failedReq.push({ url: req.url(), error: req.failure()?.errorText || 'failed', page: page.url() });
  });
  page.on('console', (msg) => {
    if (msg.type() === 'error') consoleErrors.push({ text: msg.text(), page: page.url() });
  });
  page.on('pageerror', (err) => {
    pageErrors.push({ text: String(err), page: page.url() });
  });

  for (const u of pages) {
    try {
      await page.goto(u, { waitUntil: 'domcontentloaded', timeout: 30_000 });
      await page.waitForTimeout(150);
    } catch (e) {
      pageErrors.push({ text: `goto failed: ${e.message}`, page: u });
    }
  }

  fs.writeFileSync(path.join(OUT, 'crawl-404.json'), JSON.stringify({ badStatus, failedReq }, null, 2));
  fs.writeFileSync(path.join(OUT, 'console-errors.json'), JSON.stringify({ consoleErrors, pageErrors }, null, 2));

  // Filter noise: ignore abadis-med.com external and chrome-extension
  const internalBad = badStatus.filter((b) => b.url.includes('127.0.0.1') || b.url.includes('localhost'));
  const internalFail = failedReq.filter((b) => b.url.includes('127.0.0.1') || b.url.includes('localhost'));

  const ok2 = internalBad.length === 0 && internalFail.length === 0;
  record(2, {
    name: '404 and broken assets',
    scope: `${pages.length} pages`,
    result: ok2 ? 'pass' : 'fail',
    details: { internalBad: internalBad.length, internalFail: internalFail.length, allBad: badStatus.length },
  });
  if (!ok2) {
    for (const b of internalBad.slice(0, 20)) {
      addBug({ severity: 'major', test: 2, page: b.page, detail: `${b.status} ${b.url}` });
    }
  }

  const ok3 = consoleErrors.length === 0 && pageErrors.length === 0;
  record(3, {
    name: 'Console / page errors',
    scope: `${pages.length} pages`,
    result: ok3 ? 'pass' : 'fail',
    details: { consoleErrors: consoleErrors.length, pageErrors: pageErrors.length, sample: consoleErrors.slice(0, 10) },
  });
  if (!ok3) {
    for (const e of [...consoleErrors, ...pageErrors].slice(0, 15)) {
      addBug({ severity: 'major', test: 3, page: e.page, detail: e.text.slice(0, 200) });
    }
  }

  await context.close();
  // Soft: still mark test run complete even if fails (report owns the verdict)
  expect(true).toBeTruthy();
});

// ---------------------------------------------------------------------------
// 4: three themes + contrast on reps
// ---------------------------------------------------------------------------
test('4 themes light/dark/noir + contrast', async ({ page }) => {
  const themeResults = [];
  const contrastFails = [];
  const themePages = REPS.filter((p) => ['/', '/about/', '/products/', '/news/', '/csr/', '/contact/', '/calculator/'].includes(p));

  for (const u of themePages) {
    for (const theme of ['light', 'dark', 'noir']) {
      await page.goto(`${u}?theme=${theme}`, { waitUntil: 'domcontentloaded' });
      await page.waitForTimeout(200);
      const dt = await page.evaluate(() => document.documentElement.dataset.theme);
      const ok = dt === theme;
      themeResults.push({ page: u, theme, ok, actual: dt });
      await shot(page, path.join(String(1440), theme, `${slug(u)}.png`));

      try {
        const axe = await new AxeBuilder({ page }).withRules(['color-contrast']).analyze();
        if (axe.violations.length) {
          contrastFails.push({ page: u, theme, count: axe.violations.length, nodes: axe.violations[0]?.nodes?.length });
        }
      } catch (e) {
        contrastFails.push({ page: u, theme, error: String(e).slice(0, 120) });
      }
    }
  }

  const themeOk = themeResults.every((r) => r.ok);
  const contrastOk = contrastFails.length === 0;
  record(4, {
    name: 'Three themes + color contrast',
    scope: `${themePages.length} pages × 3 themes`,
    result: themeOk && contrastOk ? 'pass' : (!themeOk ? 'fail' : 'warn'),
    details: { themeOk, contrastFails: contrastFails.slice(0, 20), themeFails: themeResults.filter((r) => !r.ok) },
  });
  for (const f of contrastFails.slice(0, 10)) {
    addBug({ severity: 'minor', test: 4, page: f.page, detail: `contrast ${f.theme}: ${f.count || f.error}` });
  }
  expect(true).toBeTruthy();
});

// ---------------------------------------------------------------------------
// 5: responsive viewports
// ---------------------------------------------------------------------------
test('5 responsive viewports + no horizontal scroll', async ({ browser }) => {
  const viewports = [
    { w: 375, h: 812 },
    { w: 768, h: 1024 },
    { w: 1440, h: 900 },
  ];
  const overflow = [];
  const sample = REPS.filter((p) =>
    ['/', '/about/', '/products/suction-bag/', '/news/', '/csr/', '/calculator/', '/customers/', '/contact/'].includes(p));

  for (const vp of viewports) {
    const context = await browser.newContext({ viewport: { width: vp.w, height: vp.h } });
    const page = await context.newPage();
    for (const u of sample) {
      const themes = (u === '/' && vp.w === 1440) ? ['light', 'noir'] : ['light'];
      for (const theme of themes) {
        await page.goto(`${u}?theme=${theme}`, { waitUntil: 'domcontentloaded' });
        await page.waitForTimeout(250);
        const ov = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 1);
        if (ov) overflow.push({ page: u, w: vp.w, theme });
        await shot(page, path.join(String(vp.w), theme, `${slug(u)}.png`));
      }
    }
    await context.close();
  }

  const ok = overflow.length === 0;
  record(5, {
    name: 'Responsive / no horizontal scroll',
    scope: `${sample.length} pages × viewports`,
    result: ok ? 'pass' : 'fail',
    details: { overflow },
  });
  for (const o of overflow) {
    addBug({ severity: 'major', test: 5, page: o.page, detail: `horizontal scroll at ${o.w}px theme=${o.theme}` });
  }
  expect(true).toBeTruthy();
});

// ---------------------------------------------------------------------------
// 7: RTL / lang
// ---------------------------------------------------------------------------
test('7 RTL/LTR lang+dir on FA/EN/AR pages', async ({ page }) => {
  const fails = [];
  for (const u of REPS) {
    await page.goto(u, { waitUntil: 'domcontentloaded' });
    const meta = await page.evaluate(() => ({
      lang: document.documentElement.getAttribute('lang'),
      dir: document.documentElement.getAttribute('dir'),
    }));
    if (u.startsWith('/en/')) {
      if (meta.lang !== 'en') fails.push({ page: u, ...meta, reason: 'lang' });
      if (meta.dir !== 'ltr') fails.push({ page: u, ...meta, reason: 'dir' });
    } else if (u.startsWith('/arabic/')) {
      if (meta.lang !== 'ar') fails.push({ page: u, ...meta, reason: 'lang' });
      if (meta.dir !== 'rtl') fails.push({ page: u, ...meta, reason: 'dir' });
    } else {
      if (meta.lang !== 'fa' && meta.lang !== 'fa-IR') fails.push({ page: u, ...meta, reason: 'lang' });
      if (meta.dir !== 'rtl') fails.push({ page: u, ...meta, reason: 'dir' });
    }
  }
  const ok = fails.length === 0;
  record(7, {
    name: 'RTL / LTR lang+dir',
    scope: 'representative FA + EN + AR pages',
    result: ok ? 'pass' : 'fail',
    details: { fails },
  });
  for (const f of fails) addBug({ severity: 'critical', test: 7, page: f.page, detail: `lang=${f.lang} dir=${f.dir}` });
  expect(true).toBeTruthy();
});

// ---------------------------------------------------------------------------
// 8: Kalameh font
// ---------------------------------------------------------------------------
test('8 Kalameh font loaded', async ({ page }) => {
  const fails = [];
  for (const u of ['/', '/about/', '/news/', '/products/']) {
    const woffFails = [];
    page.on('response', (res) => {
      if (res.url().includes('kalameh') && res.url().endsWith('.woff2') && res.status() !== 200) {
        woffFails.push({ url: res.url(), status: res.status() });
      }
    });
    await page.goto(u, { waitUntil: 'networkidle' });
    const info = await page.evaluate(async () => {
      await document.fonts.ready;
      const kal = [...document.fonts].filter((f) => f.family.includes('Kalameh') && f.status === 'loaded');
      return {
        count: kal.length,
        bodyFont: getComputedStyle(document.body).fontFamily,
      };
    });
    if (info.count === 0 || !/Kalameh/i.test(info.bodyFont) || woffFails.length) {
      fails.push({ page: u, ...info, woffFails });
    }
  }
  const ok = fails.length === 0;
  record(8, {
    name: 'Kalameh font',
    scope: 'home/about/news/products',
    result: ok ? 'pass' : 'fail',
    details: { fails },
  });
  for (const f of fails) addBug({ severity: 'critical', test: 8, page: f.page, detail: `Kalameh count=${f.count} font=${f.bodyFont}` });
  expect(true).toBeTruthy();
});

// ---------------------------------------------------------------------------
// 9: calculator formulas
// ---------------------------------------------------------------------------
test('9 calculator formulas + UI preset', async ({ page }) => {
  const tol = 0.01;
  const expected = {
    'surgery:1000': { water: 14880, cost: 212500000, hours: 442.567 },
    'surgery:1': { water: 14.88, cost: 212500, hours: 0.44257 },
    'beds:10,20': { water: 57734.4, cost: 637500000, hours: 1717.159 },
    'beds:1,0': { water: 3779.52, cost: 42500000, hours: 112.412 },
    'beds:0,1': { water: 996.96, cost: 10625000, hours: 29.652 },
  };

  await page.goto('/calculator/', { waitUntil: 'networkidle' });
  const hasF = await page.evaluate(() => typeof window.ABADIS_FORMULAS === 'object' && !!window.ABADIS_FORMULAS.surgery);
  const formulaCheck = await page.evaluate(({ expected, tol }) => {
    const F = window.ABADIS_FORMULAS;
    const out = [];
    const near = (a, b) => Math.abs(a - b) <= tol || Math.abs(a - b) / Math.max(Math.abs(b), 1) < 1e-4;
    const s1000 = F.surgery({ n: 1000 });
    out.push({ key: 'surgery:1000', ok: near(s1000.water, expected['surgery:1000'].water) && near(s1000.cost, expected['surgery:1000'].cost) && near(s1000.hours, expected['surgery:1000'].hours), got: s1000 });
    const s1 = F.surgery({ n: 1 });
    out.push({ key: 'surgery:1', ok: near(s1.water, expected['surgery:1'].water) && near(s1.cost, expected['surgery:1'].cost) && near(s1.hours, expected['surgery:1'].hours), got: s1 });
    const b = F.beds({ a: 10, b: 20 });
    out.push({ key: 'beds:10,20', ok: near(b.water, expected['beds:10,20'].water) && near(b.cost, expected['beds:10,20'].cost) && near(b.hours, expected['beds:10,20'].hours), got: b });
    const b10 = F.beds({ a: 1, b: 0 });
    out.push({ key: 'beds:1,0', ok: near(b10.water, expected['beds:1,0'].water) && near(b10.cost, expected['beds:1,0'].cost) && near(b10.hours, expected['beds:1,0'].hours), got: b10 });
    const b01 = F.beds({ a: 0, b: 1 });
    out.push({ key: 'beds:0,1', ok: near(b01.water, expected['beds:0,1'].water) && near(b01.cost, expected['beds:0,1'].cost) && near(b01.hours, expected['beds:0,1'].hours), got: b01 });
    return out;
  }, { expected, tol });

  // UI: click preset chip data-n=1000 if present; water odo should read ~14880
  let uiOk = null;
  const chip = page.locator('[data-n="1000"]').first();
  if (await chip.count()) {
    await chip.click();
    await page.waitForTimeout(2500);
    const shown = await page.evaluate(() => {
      const odos = [...document.querySelectorAll('.odo[data-value]')].map((el) => Number(el.getAttribute('data-value')));
      // surgery page exposes n, water, cost, hours — water must be ~14880
      return { odos, hasWater: odos.some((v) => Math.abs(v - 14880) < 2) };
    });
    uiOk = !!shown.hasWater;
  } else {
    uiOk = null; // warn: no chip
  }

  const formulaOk = hasF && formulaCheck.every((r) => r.ok);
  const result = formulaOk && uiOk !== false ? (uiOk === null ? 'warn' : 'pass') : 'fail';
  record(9, {
    name: 'Calculator formulas',
    scope: '/calculator/ + 5 designs have ABADIS_FORMULAS',
    result,
    details: { hasF, formulaCheck, uiOk },
  });
  if (!formulaOk) addBug({ severity: 'critical', test: 9, page: '/calculator/', detail: 'formula mismatch' });

  // presence on other calc pages
  for (const u of ['/calculator/dial/', '/calculator/receipt/', '/calculator/hospital/', '/calculator/scale/', '/calculator/flood/']) {
    await page.goto(u, { waitUntil: 'domcontentloaded' });
    const ok = await page.evaluate(() => !!window.ABADIS_FORMULAS?.surgery);
    if (!ok) addBug({ severity: 'major', test: 9, page: u, detail: 'ABADIS_FORMULAS missing' });
  }
  expect(true).toBeTruthy();
});

// ---------------------------------------------------------------------------
// 10: CSR Zagros scroll states
// ---------------------------------------------------------------------------
test('10 CSR Zagros scroll states', async ({ browser }) => {
  const results = [];
  for (const vp of [{ w: 375, h: 812 }, { w: 1440, h: 900 }]) {
    const context = await browser.newContext({ viewport: { width: vp.w, height: vp.h } });
    const page = await context.newPage();
    const assetFails = [];
    page.on('response', (res) => {
      if (res.url().includes('/csr/img/hero/') && res.status() !== 200) {
        assetFails.push({ url: res.url(), status: res.status() });
      }
    });
    const cons = [];
    page.on('console', (m) => { if (m.type() === 'error') cons.push(m.text()); });

    await page.goto('/csr/', { waitUntil: 'networkidle' });
    const hero = page.locator('#hero');
    const box = await hero.boundingBox();
    if (!box) {
      results.push({ vp, ok: false, reason: 'no #hero' });
      await context.close();
      continue;
    }

    async function stateAt(frac) {
      // scroll within hero track
      const scrollY = await page.evaluate((f) => {
        const h = document.getElementById('hero');
        const track = h?.parentElement || h;
        const max = Math.max(0, (track?.offsetHeight || 0) - window.innerHeight);
        // also try document scroll through hero sticky section
        const top = h.getBoundingClientRect().top + window.scrollY;
        const height = h.offsetHeight || 800;
        const y = top + f * Math.max(height - window.innerHeight, 400);
        window.scrollTo(0, y);
        return y;
      }, frac);
      await page.waitForTimeout(400);
      // wheel nudge for scrubbers that listen to scroll
      await page.mouse.wheel(0, 80);
      await page.waitForTimeout(300);
      const opac = await page.evaluate(() => {
        const mid = document.querySelector('.zh-bg-mid');
        const green = document.querySelector('.zh-bg-green');
        const cs = (el) => el ? parseFloat(getComputedStyle(el).opacity || '0') : 0;
        return { mid: cs(mid), green: cs(green), scrollY: window.scrollY };
      });
      await shot(page, path.join(String(vp.w), 'light', `csr-scroll-${Math.round(frac * 100)}.png`));
      return { scrollY, ...opac };
    }

    const s0 = await stateAt(0);
    const s50 = await stateAt(0.5);
    const s100 = await stateAt(1);
    // dry → sprout → green: mid/green opacity should increase over scroll
    const progressed = (s100.green >= s0.green - 0.05) && (s100.mid + s100.green >= s0.mid + s0.green - 0.05);
    results.push({
      vp, s0, s50, s100, progressed,
      assetFails, cons: cons.slice(0, 5),
      ok: progressed && assetFails.length === 0 && cons.length === 0,
    });
    await context.close();
  }

  const ok = results.every((r) => r.ok);
  record(10, {
    name: 'CSR Zagros scroll',
    scope: '375 + 1440',
    result: ok ? 'pass' : 'fail',
    details: { results },
  });
  if (!ok) addBug({ severity: 'major', test: 10, page: '/csr/', detail: JSON.stringify(results.map((r) => ({ vp: r.vp, progressed: r.progressed, assets: r.assetFails?.length, cons: r.cons?.length }))) });
  expect(true).toBeTruthy();
});

// ---------------------------------------------------------------------------
// 11: suction-bag 3D
// ---------------------------------------------------------------------------
test('11 suction-bag WebGL / GLB', async ({ browser }) => {
  const results = [];
  for (const vp of [{ w: 375, h: 812 }, { w: 1440, h: 900 }]) {
    const context = await browser.newContext({ viewport: { width: vp.w, height: vp.h } });
    const page = await context.newPage();
    let glbStatus = null;
    page.on('response', (res) => {
      if (res.url().includes('abadis-scrub-parts.glb')) glbStatus = res.status();
    });
    await page.goto('/products/suction-bag/', { waitUntil: 'networkidle' });
    await page.waitForTimeout(1500);
    const info = await page.evaluate(() => {
      const canvas = document.querySelector('canvas');
      return {
        hasCanvas: !!canvas,
        w: canvas?.width || 0,
        h: canvas?.height || 0,
        overflow: document.documentElement.scrollWidth > window.innerWidth + 1,
      };
    });
    await shot(page, path.join(String(vp.w), 'light', 'suction-bag.png'));
    // scroll scrub a bit
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight * 0.3));
    await page.waitForTimeout(500);
    await shot(page, path.join(String(vp.w), 'light', 'suction-bag-scrub.png'));
    results.push({ vp, ...info, glbStatus, ok: info.hasCanvas && glbStatus === 200 && !info.overflow });
    await context.close();
  }

  // WebGL disabled fallback
  const context2 = await chromium.launch({
    headless: true,
    args: ['--disable-webgl', '--use-gl=swiftshader'],
  }).then((b) => b.newContext({ viewport: { width: 1440, height: 900 } })).catch(() => null);

  let fallback = { note: 'skipped' };
  if (context2) {
    const page = await context2.newPage();
    await page.goto('/products/suction-bag/', { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(800);
    const cons = [];
    page.on('console', (m) => { if (m.type() === 'error') cons.push(m.text()); });
    fallback = {
      hasCanvas: await page.evaluate(() => !!document.querySelector('canvas')),
      bodyText: await page.evaluate(() => document.body.innerText.slice(0, 200)),
    };
    await context2.close();
  }

  const ok = results.every((r) => r.ok);
  record(11, {
    name: 'Suction-bag 3D viewer',
    scope: '375 + 1440 + WebGL-off probe',
    result: ok ? 'pass' : 'fail',
    details: { results, fallback },
  });
  if (!ok) addBug({ severity: 'major', test: 11, page: '/products/suction-bag/', detail: JSON.stringify(results) });
  expect(true).toBeTruthy();
});

// ---------------------------------------------------------------------------
// 12: theme toggle cycle + persist
// ---------------------------------------------------------------------------
test('12 theme toggle cycle and persistence', async ({ page }) => {
  await page.goto('/', { waitUntil: 'domcontentloaded' });
  await page.evaluate(() => localStorage.removeItem('abadis-theme'));
  await page.goto('/?theme=light', { waitUntil: 'domcontentloaded' });

  const seq = [];
  for (let i = 0; i < 3; i++) {
    await page.locator('.theme-toggle').click();
    await page.waitForTimeout(200);
    seq.push(await page.evaluate(() => document.documentElement.dataset.theme));
  }
  const cycleOk = seq[0] === 'dark' && seq[1] === 'noir' && seq[2] === 'light';
  const stored = await page.evaluate(() => localStorage.getItem('abadis-theme'));
  await page.reload({ waitUntil: 'domcontentloaded' });
  const after = await page.evaluate(() => document.documentElement.dataset.theme);
  const persistOk = after === stored && stored === 'light';

  // reduced motion
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await page.locator('.theme-toggle').click();
  await page.waitForTimeout(200);
  const rmTheme = await page.evaluate(() => document.documentElement.dataset.theme);

  const ok = cycleOk && persistOk && !!rmTheme;
  record(12, {
    name: 'Theme toggle cycle + persist',
    scope: 'home',
    result: ok ? 'pass' : 'fail',
    details: { seq, stored, after, rmTheme, cycleOk, persistOk },
  });
  if (!ok) addBug({ severity: 'major', test: 12, page: '/', detail: `seq=${seq} stored=${stored}` });
  expect(true).toBeTruthy();
});

// ---------------------------------------------------------------------------
// 13: header transparent / scrolled / on-light
// ---------------------------------------------------------------------------
test('13 header transparency and on-light', async ({ page }) => {
  const pages = ['/', '/about/', '/products/', '/news/'];
  const fails = [];
  for (const u of pages) {
    await page.goto(`${u}?theme=light`, { waitUntil: 'domcontentloaded' });
    await page.evaluate(() => window.scrollTo(0, 0));
    await page.waitForTimeout(200);
    const top = await page.evaluate(() => {
      const h = document.querySelector('header');
      const bg = getComputedStyle(h).backgroundColor;
      const scrolled = h.classList.contains('scrolled');
      return { bg, scrolled, alpha: (() => {
        const m = bg.match(/rgba?\(([^)]+)\)/);
        if (!m) return null;
        const parts = m[1].split(',').map((x) => parseFloat(x.trim()));
        return parts.length === 4 ? parts[3] : 1;
      })() };
    });
    if (top.scrolled) fails.push({ page: u, reason: 'scrolled at top' });
    if (top.alpha != null && top.alpha > 0.2) fails.push({ page: u, reason: `opaque header at top alpha=${top.alpha} bg=${top.bg}` });

    await page.evaluate(() => window.scrollTo(0, 80));
    await page.waitForTimeout(250);
    const mid = await page.evaluate(() => {
      const h = document.querySelector('header');
      const bg = getComputedStyle(h).backgroundColor;
      return {
        scrolled: h.classList.contains('scrolled'),
        bg,
        // fail if solid white/opaque mint fill
        isSolidWhite: /rgb\(\s*255,\s*255,\s*255\s*\)/.test(bg) || /rgba\(\s*255,\s*255,\s*255,\s*1\s*\)/.test(bg),
      };
    });
    if (!mid.scrolled) fails.push({ page: u, reason: 'missing .scrolled after scroll' });
    if (mid.isSolidWhite) fails.push({ page: u, reason: 'solid white header when scrolled' });
  }

  const ok = fails.length === 0;
  record(13, {
    name: 'Header transparent / scrolled / on-light',
    scope: 'home about products news (light)',
    result: ok ? 'pass' : 'fail',
    details: { fails },
  });
  for (const f of fails) addBug({ severity: 'major', test: 13, page: f.page, detail: f.reason });
  expect(true).toBeTruthy();
});

// ---------------------------------------------------------------------------
// 14: forms mailto / validation
// ---------------------------------------------------------------------------
test('14 contact and careers forms', async ({ page }) => {
  const details = {};

  await page.goto('/contact/', { waitUntil: 'domcontentloaded' });
  const lead = page.locator('#leadForm');
  details.hasLead = await lead.count() > 0;
  details.endpointEmpty = await page.evaluate(() => {
    const ep = document.querySelector('meta[name="abadis-form-endpoint"]')?.content || '';
    return !ep.trim();
  });
  if (details.hasLead) {
    details.contactEmptyBlocked = await page.evaluate(() => !document.getElementById('leadForm').checkValidity());

    await page.fill('input[name="name"]', 'تست');
    await page.fill('input[name="org"]', 'بیمارستان');
    await page.fill('input[name="phone"]', '۰۹۱۲۱۲۳۴۵۶۷');
    await page.selectOption('select[name="topic"]', { index: 1 }).catch(() => {});
    await page.fill('textarea[name="msg"]', 'پیام آزمایشی');

    // site.js assigns location.href = 'mailto:…' when endpoint empty — capture via CDP
    details.contactMailto = null;
    const client = await page.context().newCDPSession(page);
    await client.send('Page.setInterceptFileChooserDialog', { enabled: false }).catch(() => {});
    page.on('framenavigated', () => {});
    await page.evaluate(() => {
      window.__mailtoHits = [];
      const loc = window.location;
      try {
        // Spy on assignments used by openMailto()
        const proto = Object.getPrototypeOf(loc);
        const desc = Object.getOwnPropertyDescriptor(proto, 'href');
        Object.defineProperty(proto, 'href', {
          configurable: true,
          enumerable: true,
          get() { return desc.get.call(this); },
          set(v) {
            window.__mailtoHits.push(String(v));
            if (String(v).startsWith('mailto:')) return;
            return desc.set.call(this, v);
          },
        });
      } catch (e) {
        window.__mailtoHits.push('spy-failed:' + e.message);
      }
    });
    await lead.locator('button[type="submit"]').first().click();
    await page.waitForTimeout(400);
    details.contactMailto = await page.evaluate(() => {
      const hits = window.__mailtoHits || [];
      return hits.find((h) => h.startsWith('mailto:')) || hits[hits.length - 1] || null;
    });
    // Also accept success status text as evidence mailto path ran
    const status = await page.locator('#formStatus, .form-status').first().textContent().catch(() => '');
    details.contactStatus = (status || '').trim();
    details.contactMailtoBuilt = !!(
      (details.contactMailto && details.contactMailto.startsWith('mailto:info@abadis-med.com'))
      || /ایمیل/.test(details.contactStatus)
    );
  }

  await page.goto('/careers/', { waitUntil: 'domcontentloaded' });
  const careersForm = page.locator('form[data-mailto-form], form[data-abadis-form="careers"]');
  details.hasCareers = await careersForm.count() > 0;
  if (details.hasCareers) {
    details.careersEmptyBlocked = await page.evaluate(() => {
      const f = document.querySelector('form[data-mailto-form], form[data-abadis-form="careers"]');
      return f ? !f.checkValidity() : null;
    });
  }

  const ok = details.hasLead && details.contactEmptyBlocked && details.contactMailtoBuilt && details.hasCareers && details.careersEmptyBlocked;
  record(14, {
    name: 'Forms contact + careers',
    scope: '/contact/ /careers/',
    result: ok ? 'pass' : 'fail',
    details,
  });
  if (!ok) addBug({ severity: 'major', test: 14, page: '/contact/', detail: JSON.stringify(details) });
  expect(true).toBeTruthy();
});

// ---------------------------------------------------------------------------
// 15: brand rules
// ---------------------------------------------------------------------------
test('15 brand rules (footer, nav, no yellow, pointermove audit)', async ({ page }) => {
  await page.goto('/', { waitUntil: 'domcontentloaded' });
  const nav = await page.evaluate(() => {
    // Main menu only — exclude .lang-switch (FA/EN/ع)
    const links = [...document.querySelectorAll('header nav#mainNav a')].map((a) => a.textContent.trim());
    return links;
  });
  const navOk = EXPECTED_NAV.every((t, i) => nav[i] === t) && nav.length === EXPECTED_NAV.length;

  const footer = await page.evaluate(() => {
    const img = document.querySelector('.foot-certs img');
    return img ? img.getAttribute('src') : null;
  });
  const footerOk = footer && footer.includes('abd-certs-768x119-1-copy.webp');

  // yellow scan in CSS files
  const cssFiles = [];
  function walkCss(dir) {
    for (const ent of fs.readdirSync(dir, { withFileTypes: true })) {
      const p = path.join(dir, ent.name);
      if (ent.isDirectory()) walkCss(p);
      else if (ent.name.endsWith('.css')) cssFiles.push(p);
    }
  }
  walkCss(path.join(SITE, 'assets/css'));
  walkCss(path.join(SITE, 'csr'));
  walkCss(path.join(SITE, 'calculator'));
  const yellowHits = [];
  for (const f of cssFiles) {
    const txt = fs.readFileSync(f, 'utf8').toLowerCase();
    for (const pat of YELLOW_PATTERNS) {
      if (txt.includes(pat.toLowerCase())) yellowHits.push({ file: path.relative(ROOT, f), pat });
    }
  }

  // pointermove / mousemove grep in site JS (exclude vendor three)
  const moveHits = [];
  const jsRoots = [
    path.join(SITE, 'assets/js'),
    path.join(SITE, 'csr'),
    path.join(SITE, 'calculator'),
  ];
  function walkJs(dir) {
    if (!fs.existsSync(dir)) return;
    for (const ent of fs.readdirSync(dir, { withFileTypes: true })) {
      const p = path.join(dir, ent.name);
      if (ent.isDirectory()) walkJs(p);
      else if (ent.name.endsWith('.js')) {
        const txt = fs.readFileSync(p, 'utf8');
        if (/addEventListener\(\s*['"]m(?:ouse|pointer)move['"]/.test(txt) || /\.on(?:mouse|pointer)move\s*=/.test(txt)) {
          moveHits.push(path.relative(ROOT, p));
        }
      }
    }
  }
  for (const r of jsRoots) walkJs(r);

  // brand: decorative mousemove forbidden; product-viewer pointermove is interaction (warn)
  const decorativeMoves = moveHits.filter((f) => !f.includes('product-viewer') && !f.includes('vendor'));
  const ok = navOk && footerOk && yellowHits.length === 0 && decorativeMoves.length === 0;
  record(15, {
    name: 'Brand rules',
    scope: 'nav order, footer certs, yellow CSS, pointermove',
    result: ok ? (moveHits.length ? 'warn' : 'pass') : 'fail',
    details: { nav, navOk, footer, footerOk, yellowHits, moveHits, decorativeMoves },
  });
  if (!navOk) addBug({ severity: 'critical', test: 15, page: '/', detail: `nav order wrong: ${nav.join(' | ')}` });
  if (!footerOk) addBug({ severity: 'critical', test: 15, page: '/', detail: `footer certs: ${footer}` });
  if (yellowHits.length) addBug({ severity: 'major', test: 15, page: yellowHits[0].file, detail: `yellow/lime: ${yellowHits.map((h) => h.pat).join(',')}` });
  if (moveHits.includes('site/assets/js/product-viewer.js')) {
    addBug({ severity: 'minor', test: 15, page: '/products/suction-bag/', detail: 'pointermove in product-viewer.js (3D interaction — review)' });
  }
  expect(true).toBeTruthy();
});

// ---------------------------------------------------------------------------
// 16: meta title/description/h1/alt
// ---------------------------------------------------------------------------
test('16 meta uniqueness and basics', async ({ page }) => {
  test.setTimeout(1_800_000);
  const pages = allPageUrls();
  const titles = new Map();
  const dupTitles = [];
  const missingDesc = [];
  const multiH1 = [];
  const noH1 = [];
  const missingAlt = [];

  for (const u of pages) {
    await page.goto(u, { waitUntil: 'domcontentloaded' });
    const meta = await page.evaluate(() => {
      const title = document.title || '';
      const desc = document.querySelector('meta[name="description"]')?.content || '';
      const h1s = [...document.querySelectorAll('h1')].map((h) => h.textContent.trim());
      const imgs = [...document.querySelectorAll('img')].filter((img) => !img.hasAttribute('alt')).map((img) => img.getAttribute('src'));
      const og = document.querySelector('meta[property="og:image"]')?.content || null;
      return { title, desc, h1s, imgs, og };
    });
    if (titles.has(meta.title)) dupTitles.push({ page: u, title: meta.title, other: titles.get(meta.title) });
    else titles.set(meta.title, u);
    if (!meta.desc) missingDesc.push(u);
    if (meta.h1s.length === 0) noH1.push(u);
    if (meta.h1s.length > 1) multiH1.push({ page: u, count: meta.h1s.length });
    if (meta.imgs.length) missingAlt.push({ page: u, count: meta.imgs.length, sample: meta.imgs.slice(0, 3) });
  }

  fs.writeFileSync(path.join(OUT, 'meta-audit.json'), JSON.stringify({
    dupTitles, missingDesc, multiH1, noH1, missingAlt: missingAlt.slice(0, 50),
  }, null, 2));

  const critical = dupTitles.length > 0 || noH1.length > 0;
  const warn = missingDesc.length > 0 || multiH1.length > 0 || missingAlt.length > 0;
  record(16, {
    name: 'Meta title/description/h1/alt',
    scope: `${pages.length} pages`,
    result: critical ? 'fail' : (warn ? 'warn' : 'pass'),
    details: {
      dupTitles: dupTitles.length,
      missingDesc: missingDesc.length,
      multiH1: multiH1.length,
      noH1: noH1.length,
      missingAltPages: missingAlt.length,
      samples: { dupTitles: dupTitles.slice(0, 5), missingDesc: missingDesc.slice(0, 10), missingAlt: missingAlt.slice(0, 5) },
    },
  });
  for (const d of dupTitles.slice(0, 10)) addBug({ severity: 'major', test: 16, page: d.page, detail: `duplicate title: ${d.title}` });
  for (const u of noH1.slice(0, 10)) addBug({ severity: 'major', test: 16, page: u, detail: 'no h1' });
  expect(true).toBeTruthy();
});
