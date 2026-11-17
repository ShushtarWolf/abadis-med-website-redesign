#!/usr/bin/env node
import { chromium } from 'playwright';

const base = 'http://127.0.0.1:8765';
const pages = [
  '/%D9%81%DB%8C%D9%84%D8%AA%D8%B1-%D8%A2%D9%86%D8%AA%DB%8C%D8%A8%D8%A7%DA%A9%D8%AA%D8%B1%DB%8C%D8%A7%D9%84-%D9%88-%D9%81%DB%8C%D9%84%D8%AA%D8%B1-%D9%87%DB%8C%D8%AF%D8%B1%D9%88%D9%81%D9%88%D8%A8/',
  '/introducing-medical-engineering-sites/',
  '/%D8%AF%D8%B3%D8%AA%DA%AF%D8%A7%D9%87-%D8%AA%D8%B2%D8%B1%DB%8C%D9%82-%DA%86%D8%B1%D8%A8%DB%8C-%DA%86%DB%8C%D8%B3%D8%AA%D8%9F/',
  '/en/what-are-antibacterial-filters-and-hydrophobic-filters/',
];

const browser = await chromium.launch({ headless: true });
const results = [];

for (const pagePath of pages) {
  for (const width of [1440, 390]) {
    const page = await browser.newPage({ viewport: { width, height: 900 } });
    const url = base + pagePath;
    await page.goto(url, { waitUntil: 'networkidle', timeout: 120000 });
    await page.evaluate(async () => {
      const h = document.body.scrollHeight;
      for (let y = 0; y < h; y += 400) {
        window.scrollTo(0, y);
        await new Promise((r) => setTimeout(r, 50));
      }
      window.scrollTo(0, document.body.scrollHeight);
    });
    await page.waitForTimeout(300);
    const imgs = await page.$$eval('article.prose img', (nodes) =>
      nodes
        .filter((el) => !el.closest('.lead-img'))
        .map((el) => ({
          src: el.getAttribute('src'),
          nw: el.naturalWidth,
          nh: el.naturalHeight,
          vis: el.getClientRects().length > 0,
        })),
    );
    const bad = imgs.filter((i) => i.nw <= 0 || !i.vis);
    results.push({
      page: pagePath,
      width,
      total: imgs.length,
      ok: imgs.length - bad.length,
      bad: bad.length,
      badSrcs: bad.map((b) => b.src),
    });
    await page.close();
  }
}

await browser.close();
console.log(JSON.stringify(results, null, 2));
const failed = results.filter((r) => r.bad > 0);
process.exit(failed.length ? 1 : 0);