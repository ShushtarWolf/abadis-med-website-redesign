/**
 * Build docs/abadis/TEST-REPORT.md from out/summary.json and copy ~30 key screenshots.
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '../..');
const OUT = path.join(__dirname, 'out');
const REPORT = path.join(ROOT, 'docs/abadis/TEST-REPORT.md');
const DOCS_SHOTS = path.join(ROOT, 'docs/abadis/test-shots');

const NAMES = {
  1: 'Internal links (linkinator)',
  2: '404 / broken assets',
  3: 'Console / page errors',
  4: 'Three themes + contrast',
  5: 'Responsive / horizontal scroll',
  6: 'Lighthouse mobile',
  7: 'RTL / lang=fa',
  8: 'Kalameh font',
  9: 'Calculator formulas',
  10: 'CSR Zagros scroll',
  11: 'Suction-bag 3D',
  12: 'Theme toggle + persist',
  13: 'Header transparent / scrolled',
  14: 'Forms contact + careers',
  15: 'Brand rules',
  16: 'Meta title / description / h1 / alt',
};

const icon = (r) => (r === 'pass' ? '✅ pass' : r === 'warn' ? '⚠️ warn' : r === 'fail' ? '❌ fail' : '❓ n/a');

function ensureSummary() {
  const p = path.join(OUT, 'summary.json');
  if (!fs.existsSync(p)) {
    throw new Error('missing out/summary.json — run the suite first');
  }
  return JSON.parse(fs.readFileSync(p, 'utf8'));
}

function copyKeyShots() {
  fs.mkdirSync(DOCS_SHOTS, { recursive: true });
  const wanted = [
    '1440/light/home.png',
    '1440/dark/home.png',
    '1440/noir/home.png',
    '375/light/home.png',
    '1440/light/about.png',
    '1440/light/products__suction-bag.png',
    '375/light/suction-bag.png',
    '1440/light/csr.png',
    '1440/light/csr-scroll-0.png',
    '1440/light/csr-scroll-50.png',
    '1440/light/csr-scroll-100.png',
    '375/light/csr-scroll-0.png',
    '1440/light/news.png',
    '1440/light/calculator.png',
    '1440/light/customers.png',
    '1440/light/contact.png',
    '768/light/home.png',
    '1440/noir/csr.png',
    '375/light/products__suction-bag.png',
    '1440/light/suction-bag.png',
    '1440/light/suction-bag-scrub.png',
    '375/light/suction-bag-scrub.png',
    '1440/dark/about.png',
    '1440/noir/news.png',
    '375/light/calculator.png',
    '375/light/contact.png',
    '1440/light/dealers.png',
    '1440/light/careers.png',
    '768/light/csr.png',
    '375/light/news.png',
  ];
  const copied = [];
  for (const rel of wanted) {
    const src = path.join(OUT, 'shots', rel);
    if (!fs.existsSync(src)) continue;
    const destName = rel.replace(/\//g, '__');
    const dest = path.join(DOCS_SHOTS, destName);
    fs.copyFileSync(src, dest);
    copied.push(destName);
  }
  return copied;
}

function detailCell(t) {
  if (!t?.details) return '';
  const d = t.details;
  const bits = [];
  if (d.total != null) bits.push(`total=${d.total}`);
  if (d.broken != null) bits.push(`broken=${d.broken}`);
  if (d.nonWpContentExternal != null) bits.push(`livePostHrefs=${d.nonWpContentExternal}`);
  if (d.postCardExt != null) bits.push(`post-card-ext=${d.postCardExt}`);
  if (d.note) bits.push(d.note);
  if (d.internalBad != null) bits.push(`bad=${d.internalBad}`);
  if (d.consoleErrors != null) bits.push(`console=${d.consoleErrors}`);
  if (d.overflow) bits.push(`overflow=${d.overflow.length}`);
  if (d.rows) bits.push(d.rows.map((r) => `${r.file}: a11y ${r.accessibility} / perf ${r.performance} / seo ${r.seo}`).join('; '));
  if (d.fails && Array.isArray(d.fails)) bits.push(`fails=${d.fails.length}`);
  if (d.yellowHits) bits.push(`yellow=${d.yellowHits.length}`);
  if (d.moveHits) bits.push(`pointermove=${d.moveHits.length}`);
  if (d.samples?.dupTitles) bits.push(`dupTitles=${d.dupTitles}`);
  if (d.missingAltPages != null) bits.push(`missingAltPages=${d.missingAltPages}`);
  if (d.formulaCheck) bits.push(`formulas=${d.formulaCheck.every((x) => x.ok) ? 'ok' : 'mismatch'}`);
  if (typeof d === 'object') {
    const s = JSON.stringify(d);
    if (bits.length === 0) return s.length > 180 ? s.slice(0, 177) + '…' : s;
  }
  return bits.join('; ') || '';
}

const s = ensureSummary();
const copied = copyKeyShots();
const tests = s.tests || {};
const counts = { pass: 0, fail: 0, warn: 0, na: 0 };
for (let i = 1; i <= 16; i++) {
  const r = tests[i]?.result || 'n/a';
  if (r === 'pass') counts.pass++;
  else if (r === 'fail') counts.fail++;
  else if (r === 'warn') counts.warn++;
  else counts.na++;
}

const lines = [];
lines.push('# Abadis redesign — TEST REPORT');
lines.push('');
lines.push(`- **Date:** ${s.finishedAt || s.startedAt || new Date().toISOString()}`);
lines.push(`- **SHA:** \`${s.sha || 'unknown'}\``);
lines.push(`- **Base:** ${s.base || 'http://127.0.0.1:8080'}`);
lines.push(`- **Pages:** ${s.pageCount ?? '—'}`);
lines.push(`- **Totals:** ✅ ${counts.pass} · ❌ ${counts.fail} · ⚠️ ${counts.warn} · ❓ ${counts.na}`);
lines.push('');
lines.push('## Results');
lines.push('');
lines.push('| # | Test | Scope | Result | Details / shots |');
lines.push('|---|------|-------|--------|-----------------|');
for (let i = 1; i <= 16; i++) {
  const t = tests[i] || {};
  const name = t.name || NAMES[i];
  const scope = t.scope || '';
  const result = icon(t.result || 'n/a');
  const det = detailCell(t).replace(/\|/g, '\\|');
  lines.push(`| ${i} | ${name} | ${scope} | ${result} | ${det} |`);
}
lines.push('');
lines.push('## Bugs (do not fix in this prompt)');
lines.push('');
const bugs = s.bugs || [];
if (!bugs.length) {
  lines.push('_None recorded._');
} else {
  lines.push('| Severity | Test | Page | Detail |');
  lines.push('|----------|------|------|--------|');
  const order = { critical: 0, major: 1, minor: 2 };
  const sorted = [...bugs].sort((a, b) => (order[a.severity] ?? 9) - (order[b.severity] ?? 9));
  for (const b of sorted) {
    lines.push(`| ${b.severity} | ${b.test} | ${b.page || ''} | ${(b.detail || '').replace(/\|/g, '\\|').slice(0, 240)} |`);
  }
}
lines.push('');
lines.push('## Lighthouse (mobile)');
lines.push('');
const lh = tests[6]?.details?.rows || [];
if (lh.length) {
  lines.push('| Page | Perf | a11y | Best practices | SEO |');
  lines.push('|------|------|------|----------------|-----|');
  for (const r of lh) {
    lines.push(`| ${r.url || r.file} | ${r.performance} | ${r.accessibility} | ${r.bestPractices} | ${r.seo} |`);
  }
} else {
  lines.push('_No Lighthouse rows._');
}
lines.push('');
lines.push('## Screenshots (curated)');
lines.push('');
if (copied.length) {
  for (const f of copied) {
    lines.push(`- \`docs/abadis/test-shots/${f}\``);
  }
} else {
  lines.push('_No screenshots copied (suite may not have produced shots yet)._');
}
lines.push('');
lines.push('## How to re-run');
lines.push('');
lines.push('```bash');
lines.push('cd tools/test && npm i && npx playwright install chromium');
lines.push('# from repo root:');
lines.push('bash tools/test/run-all.sh');
lines.push('# or: cd tools/test && npx playwright test site.spec.mjs --reporter=list');
lines.push('```');
lines.push('');
lines.push('Artifacts under `tools/test/out/` are gitignored. This report and curated shots are committed.');
lines.push('');

fs.mkdirSync(path.dirname(REPORT), { recursive: true });
fs.writeFileSync(REPORT, lines.join('\n'));
console.log('Wrote', REPORT);
console.log('Copied shots:', copied.length);
