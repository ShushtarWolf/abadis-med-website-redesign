#!/usr/bin/env bash
# Full Abadis site test suite (prompt 7). Run from repo root or tools/test.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
TEST_DIR="$ROOT/tools/test"
OUT="$TEST_DIR/out"
BASE="${BASE:-http://127.0.0.1:8080}"
PORT="${PORT:-8080}"
export BASE TEST_SHA
TEST_SHA="$(git -C "$ROOT" rev-parse HEAD)"

mkdir -p "$OUT/shots" "$OUT/lh"
cd "$TEST_DIR"

# Fresh summary shell
node --input-type=module -e "
import { saveSummary } from './lib/summary.mjs';
saveSummary({
  startedAt: new Date().toISOString(),
  sha: process.env.TEST_SHA,
  base: process.env.BASE,
  tests: {},
  bugs: [],
});
"

# Start static server if nothing listens on PORT
SERVER_PID=""
if ! curl -sf -o /dev/null "$BASE/"; then
  python3 -m http.server "$PORT" --directory "$ROOT/site" >"$OUT/http-server.log" 2>&1 &
  SERVER_PID=$!
  for i in $(seq 1 30); do
    curl -sf -o /dev/null "$BASE/" && break
    sleep 0.2
  done
  echo "Started http.server pid=$SERVER_PID"
fi

cleanup() {
  if [[ -n "${SERVER_PID}" ]]; then
    kill "$SERVER_PID" 2>/dev/null || true
  fi
}
trap cleanup EXIT

# ---- 1. Linkinator (internal links only) ----
echo "==> 1 linkinator"
set +e
npx linkinator "$BASE/" --recurse --skip '^https?://(?!127\\.0\\.0\\.1|localhost)' --format json >"$OUT/links.json" 2>"$OUT/links.err"
LINK_EC=$?
set -e
node --input-type=module <<'NODE'
import fs from 'node:fs';
import { record, addBug } from './lib/summary.mjs';
const raw = fs.readFileSync('out/links.json', 'utf8');
let data;
try { data = JSON.parse(raw); } catch { data = { links: [] }; }
const links = data.links || [];
const broken = links.filter((l) => l.state === 'BROKEN' || (l.status != null && l.status >= 400));
const externalAbadis = links.filter((l) => /abadis-med\.com/i.test(l.url || ''));
const postExt = externalAbadis.filter((l) => !/wp-content/i.test(l.url || ''));
const ok = broken.length === 0;
record(1, {
  name: 'Internal links (linkinator)',
  scope: 'full recurse',
  result: ok ? (postExt.length ? 'warn' : 'pass') : 'fail',
  details: {
    total: links.length,
    broken: broken.length,
    brokenSample: broken.slice(0, 20),
    externalAbadis: externalAbadis.length,
    nonWpContentExternal: postExt.length,
    postExtSample: postExt.slice(0, 15).map((l) => l.url),
  },
});
for (const b of broken.slice(0, 25)) {
  addBug({ severity: 'critical', test: 1, page: b.parent || '', detail: `${b.status} ${b.url}` });
}
if (postExt.length) {
  addBug({ severity: 'minor', test: 1, page: '/', detail: `${postExt.length} external links to abadis-med.com (non wp-content)` });
}
console.log('linkinator broken=', broken.length, 'external posts=', postExt.length);
NODE

# ---- 6. Lighthouse (mobile) on key pages ----
echo "==> 6 lighthouse"
run_lh() {
  local path="$1" name="$2"
  local out="$OUT/lh/lh-${name}.json"
  echo "  lighthouse $path -> $out"
  set +e
  npx lighthouse "${BASE}${path}" \
    --only-categories=performance,accessibility,seo,best-practices \
    --form-factor=mobile \
    --quiet \
    --chrome-flags="--headless --no-sandbox --disable-gpu" \
    --output=json \
    --output-path="$out"
  set -e
}
run_lh "/" "home"
run_lh "/products/suction-bag/" "suction"
run_lh "/csr/" "csr"
run_lh "/news/" "news"
run_lh "/calculator/" "calc"

node --input-type=module <<'NODE'
import fs from 'node:fs';
import path from 'node:path';
import { record, addBug } from './lib/summary.mjs';
const dir = 'out/lh';
const files = fs.existsSync(dir) ? fs.readdirSync(dir).filter((f) => f.endsWith('.json')) : [];
const rows = [];
let worst = 'pass';
for (const f of files) {
  const j = JSON.parse(fs.readFileSync(path.join(dir, f), 'utf8'));
  const cats = j.categories || {};
  const scores = {
    file: f,
    url: j.finalRequestedUrl || j.requestedUrl,
    performance: Math.round((cats.performance?.score || 0) * 100),
    accessibility: Math.round((cats.accessibility?.score || 0) * 100),
    bestPractices: Math.round((cats['best-practices']?.score || 0) * 100),
    seo: Math.round((cats.seo?.score || 0) * 100),
  };
  let r = 'pass';
  if (scores.accessibility < 90 || scores.bestPractices < 90) r = 'fail';
  else if (scores.performance < 70) r = 'fail';
  // SEO low expected due to noindex → warn
  if (scores.seo < 90 && r === 'pass') r = 'warn';
  scores.result = r;
  rows.push(scores);
  if (r === 'fail') worst = 'fail';
  else if (r === 'warn' && worst === 'pass') worst = 'warn';
  if (r === 'fail') {
    addBug({
      severity: scores.accessibility < 90 ? 'major' : 'major',
      test: 6,
      page: scores.url,
      detail: `LH a11y=${scores.accessibility} bp=${scores.bestPractices} perf=${scores.performance} seo=${scores.seo}`,
    });
  }
}
record(6, {
  name: 'Lighthouse mobile',
  scope: '5 key pages',
  result: files.length ? worst : 'fail',
  details: { rows, note: 'SEO may be low due to noindex (warn, not fail alone)' },
});
console.log('lighthouse', JSON.stringify(rows, null, 2));
NODE

# ---- 2–5, 7–16 Playwright ----
echo "==> Playwright site.spec.mjs"
set +e
npx playwright test site.spec.mjs --reporter=list
PW_EC=$?
set -e
echo "playwright exit=$PW_EC"

# ---- Build TEST-REPORT.md ----
echo "==> report"
node "$TEST_DIR/write-report.mjs"

echo "Done. Summary: $OUT/summary.json"
echo "Report: $ROOT/docs/abadis/TEST-REPORT.md"
