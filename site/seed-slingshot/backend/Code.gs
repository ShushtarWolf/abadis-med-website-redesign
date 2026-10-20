/**
 * Angry Bags — leaderboard backend (Google Apps Script + Google Sheet).
 * Free, no server. Deploy as a Web App (Execute as: Me, Access: Anyone).
 * See README.md in this folder for exact setup steps.
 *
 * GET  ?action=board            → { ok, month, rows:[{name, score}] }  (masked names, NEVER phones)
 * POST text/plain JSON {action:'submit', name, phone, consent, level, win,
 *      jars, nurses, oaks, stars, bagsLeft, bagsUsed, ms, score, lang}
 *                               → { ok, best }  or { ok:false, error }
 *
 * Anti-abuse: per-phone and global rate limits (CacheService), server-side
 * score recomputation with per-level caps, minimum play time, one row per
 * phone per month keeping only the best score. A determined cheater can still
 * forge a plausible request (the game runs in the browser) — winners should be
 * reviewed by a person before any prize is given.
 */

var SHEET_NAME = 'entries';
var TZ = 'Asia/Tehran';
var SCORE = { perJar: 1000, perNurse: 1500, perOak: 50, perBagLeftOnWin: 500, perStar: 1000 }; // must match config.json "score"
// per level id: jars (dirty reusable jars), nurses, bags. Must match config.json levels.
var LEVELS = { 1: { jars: 3, nurses: 1, bags: 5 }, 2: { jars: 4, nurses: 1, bags: 5 }, 3: { jars: 3, nurses: 1, bags: 5 }, 4: { jars: 4, nurses: 1, bags: 5 }, 5: { jars: 5, nurses: 2, bags: 6 } };
var MAX_OAKS = 40;          // generous cap on oaks planted in one level
var MIN_MS_PER_BAG = 1500;  // a bag cannot be aimed + fly + settle faster than this
var PHONE_COOLDOWN_S = 20;  // one submission per phone per 20 s
var GLOBAL_PER_MIN = 120;   // whole-app ceiling per minute
var BOARD_SIZE = 10;

function doGet(e) {
  var action = (e && e.parameter && e.parameter.action) || 'board';
  if (action !== 'board') return json_({ ok: false, error: 'bad_action' });
  var month = month_();
  var cache = CacheService.getScriptCache(), ck = 'board:' + month, hit = cache.get(ck);
  if (hit) return json_(JSON.parse(hit));
  var rows = rows_().filter(function (r) { return r.month === month; })
    .sort(function (a, b) { return b.score - a.score || a.updated - b.updated; })
    .slice(0, BOARD_SIZE).map(function (r) { return { name: mask_(r.name), score: r.score }; });
  var out = { ok: true, month: month, rows: rows };
  cache.put(ck, JSON.stringify(out), 60);
  return json_(out);
}

function doPost(e) {
  var d;
  try { d = JSON.parse(e.postData.contents); } catch (err) { return json_({ ok: false, error: 'bad_json' }); }
  if (!d || d.action !== 'submit') return json_({ ok: false, error: 'bad_action' });

  var phone = normPhone_(d.phone), name = cleanName_(d.name);
  if (!phone) return json_({ ok: false, error: 'phone' });
  if (!name) return json_({ ok: false, error: 'name' });
  if (d.consent !== true) return json_({ ok: false, error: 'consent' });

  var cache = CacheService.getScriptCache(), pk = 'rl:' + hash_(phone);
  if (cache.get(pk)) return json_({ ok: false, error: 'rate' });
  var gk = 'rl:g:' + Utilities.formatDate(new Date(), TZ, 'yyyyMMddHHmm');
  var g = +(cache.get(gk) || 0);
  if (g >= GLOBAL_PER_MIN) return json_({ ok: false, error: 'rate' });
  cache.put(gk, String(g + 1), 120);
  cache.put(pk, '1', PHONE_COOLDOWN_S);

  var score = check_(d);
  if (score < 0) return json_({ ok: false, error: 'invalid' });

  var lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    var sh = sheet_(), month = month_(), vals = sh.getDataRange().getValues(), now = new Date();
    for (var i = 1; i < vals.length; i++) {
      if (vals[i][0] === month && String(vals[i][1]) === phone) {
        var best = +vals[i][3];
        sh.getRange(i + 1, 9).setValue((+vals[i][8] || 1) + 1); // attempts
        if (score > best) {
          sh.getRange(i + 1, 3, 1, 6).setValues([[name, score, +d.level, now, 'yes', String(d.lang || '').slice(0, 2)]]);
          best = score;
        }
        cache.remove('board:' + month);
        return json_({ ok: true, best: best });
      }
    }
    // phone stored as text ('...) so Sheets keeps the leading 0
    sh.appendRow([month, "'" + phone, name, score, +d.level, now, 'yes', String(d.lang || '').slice(0, 2), 1]);
    cache.remove('board:' + month);
    return json_({ ok: true, best: score });
  } finally { lock.releaseLock(); }
}

/* Recompute the score from its parts and reject anything impossible. Returns score or -1. */
function check_(d) {
  var L = LEVELS[+d.level]; if (!L) return -1;
  var jars = int_(d.jars), nurses = int_(d.nurses), oaks = int_(d.oaks), stars = int_(d.stars), left = int_(d.bagsLeft), used = int_(d.bagsUsed), ms = int_(d.ms), win = d.win === true;
  if ([jars, nurses, oaks, stars, left, used, ms].some(function (v) { return v < 0; })) return -1;
  if (jars > L.jars || nurses > L.nurses || oaks > MAX_OAKS || stars > 3 || used < 1 || used + left > L.bags) return -1;
  if (win && jars !== L.jars) return -1;          // a win means every jar was cleared
  if (!win && stars !== 0) return -1;
  if (win && stars < 1) return -1;
  if (ms < used * MIN_MS_PER_BAG || ms > 3600000) return -1;
  var s = jars * SCORE.perJar + nurses * SCORE.perNurse + oaks * SCORE.perOak + stars * SCORE.perStar + (win ? left * SCORE.perBagLeftOnWin : 0);
  if (int_(d.score) !== s) return -1;              // client and server formulas must agree
  return s;
}

function normPhone_(s) {
  var p = String(s || '').replace(/[۰-۹]/g, function (c) { return '۰۱۲۳۴۵۶۷۸۹'.indexOf(c); })
    .replace(/[٠-٩]/g, function (c) { return '٠١٢٣٤٥٦٧٨٩'.indexOf(c); }).replace(/[\s\-().]/g, '');
  if (/^\+98/.test(p)) p = '0' + p.slice(3); else if (/^0098/.test(p)) p = '0' + p.slice(4); else if (/^9\d{9}$/.test(p)) p = '0' + p;
  return /^09\d{9}$/.test(p) ? p : null;
}
function cleanName_(s) { return String(s || '').replace(/[<>=\u0000-\u001f]/g, '').replace(/^[+\-@']+/, '').replace(/\s+/g, ' ').trim().slice(0, 24); }
/* Public board shows only a masked name: first 2 letters + … + last letter. */
function mask_(n) { n = String(n || ''); var a = Array.from ? Array.from(n) : n.split(''); if (a.length <= 2) return a[0] + '…'; return a.slice(0, 2).join('') + '…' + a[a.length - 1]; }
function int_(v) { v = Number(v); return isFinite(v) && Math.floor(v) === v ? v : -1; }
function month_() { return Utilities.formatDate(new Date(), TZ, 'yyyy-MM'); }
function hash_(s) { return Utilities.base64EncodeWebSafe(Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256, s)).slice(0, 22); }
function sheet_() {
  var ss = SpreadsheetApp.getActiveSpreadsheet(), sh = ss.getSheetByName(SHEET_NAME);
  if (!sh) { sh = ss.insertSheet(SHEET_NAME); sh.appendRow(['month', 'phone', 'name', 'score', 'level', 'updated', 'consent', 'lang', 'attempts']); sh.setFrozenRows(1); }
  return sh;
}
function rows_() {
  var v = sheet_().getDataRange().getValues(), out = [];
  for (var i = 1; i < v.length; i++) out.push({ month: v[i][0], name: v[i][2], score: +v[i][3], updated: +new Date(v[i][5]) });
  return out;
}
function json_(o) { return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON); }

/* Run once from the editor to create the sheet header and test the checks. */
function setup() { sheet_(); Logger.log(check_({ level: 1, win: true, jars: 3, nurses: 1, oaks: 6, stars: 3, bagsLeft: 3, bagsUsed: 2, ms: 20000, score: 3000 + 1500 + 300 + 3000 + 1500 })); }
