import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(__dirname, '..', 'out');
const SUMMARY_PATH = path.join(OUT, 'summary.json');

export function loadSummary() {
  fs.mkdirSync(OUT, { recursive: true });
  if (!fs.existsSync(SUMMARY_PATH)) {
    return {
      startedAt: new Date().toISOString(),
      sha: process.env.TEST_SHA || '',
      base: process.env.BASE || 'http://127.0.0.1:8080',
      tests: {},
      bugs: [],
    };
  }
  return JSON.parse(fs.readFileSync(SUMMARY_PATH, 'utf8'));
}

export function saveSummary(s) {
  fs.mkdirSync(OUT, { recursive: true });
  s.finishedAt = new Date().toISOString();
  fs.writeFileSync(SUMMARY_PATH, JSON.stringify(s, null, 2));
}

export function record(id, result) {
  const s = loadSummary();
  s.tests[String(id)] = { ...result, at: new Date().toISOString() };
  saveSummary(s);
  return s;
}

export function addBug(bug) {
  const s = loadSummary();
  s.bugs.push(bug);
  saveSummary(s);
}

export const REPS = [
  '/',
  '/about/',
  '/products/',
  '/products/suction-bag/',
  '/products/filters/',
  '/news/',
  '/news/1001/',
  '/articles/',
  '/articles/1041/',
  '/dealers/',
  '/customers/',
  '/experiences/',
  '/downloads/',
  '/install-guide/',
  '/install-guide/tanks/',
  '/faq/',
  '/careers/',
  '/careers/jobs/accountant/',
  '/csr/',
  '/contact/',
  '/calculator/',
  '/calculator/dial/',
  '/calculator/receipt/',
  '/calculator/hospital/',
  '/calculator/scale/',
  '/calculator/flood/',
  // i18n (prompt 3)
  '/en/',
  '/en/about-us/',
  '/en/products/',
  '/en/latest-news/',
  '/en/contact-us/',
  '/arabic/',
  '/arabic/من-نحن/',
  '/arabic/منتجات/',
  '/arabic/الاخبار/',
  '/arabic/اتصل-بنا/',
];

export const EXPECTED_NAV = [
  'آشنایی با ما',
  'محصولات',
  'آخرین اخبار',
  'لیست نمایندگان',
  'توسعه پایدار',
  'مقالات',
  'ارتباط با ما',
  'محاسبه‌گر',
];

export const YELLOW_PATTERNS = [
  '#c6ff00', '#d4ff00', '#ffeb3b', '#cddc39', 'yellow', 'lime',
];
