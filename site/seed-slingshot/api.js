/* Angry Bags — leaderboard API client + replay gate helpers.
   Pluggable: set config.json → leaderboard.endpoint to a deployed backend URL
   (see backend/README.md). Empty endpoint = feature shows "coming soon" and
   NOTHING is sent or stored. The phone number is only ever sent once in the
   POST body; it is never written to localStorage, never logged, and the
   backend never returns it. */
(function () {
  'use strict';
  var GATE_KEY = 'abadis-angrybags-gate';

  function toLatinDigits(s) {
    return String(s || '').replace(/[۰-۹]/g, function (d) { return '۰۱۲۳۴۵۶۷۸۹'.indexOf(d); })
      .replace(/[٠-٩]/g, function (d) { return '٠١٢٣٤٥٦٧٨٩'.indexOf(d); });
  }
  /* Iranian mobile → canonical 09xxxxxxxxx, or null. Accepts Persian/Arabic
     digits, spaces/dashes, and +98 / 0098 / 98 / 9xxxxxxxxx forms. */
  function normPhone(s) {
    var d = toLatinDigits(s).replace(/[\s\-().]/g, '');
    if (/^\+98/.test(d)) d = '0' + d.slice(3);
    else if (/^0098/.test(d)) d = '0' + d.slice(4);
    else if (/^98(9\d{9})$/.test(d)) d = '0' + d.slice(2);
    else if (/^9\d{9}$/.test(d)) d = '0' + d;
    return /^09\d{9}$/.test(d) ? d : null;
  }
  function cleanName(s) { return String(s || '').replace(/[<>\u0000-\u001f]/g, '').replace(/\s+/g, ' ').trim().slice(0, 24); }

  function Api(cfg) { this.url = (cfg && cfg.endpoint || '').trim(); this.timeout = (cfg && cfg.timeoutMs) || 9000; }
  Api.prototype.enabled = function () { return /^https:\/\//.test(this.url); };
  /* text/plain body keeps it a "simple" CORS request (no preflight), which
     both Google Apps Script and Cloudflare Workers accept. */
  Api.prototype.submit = function (entry) {
    if (!this.enabled()) return Promise.reject(new Error('disabled'));
    var ctl = typeof AbortController !== 'undefined' ? new AbortController() : null, ms = this.timeout;
    var tm = ctl && setTimeout(function () { ctl.abort(); }, ms);
    return fetch(this.url, { method: 'POST', headers: { 'Content-Type': 'text/plain;charset=utf-8' }, body: JSON.stringify(Object.assign({ action: 'submit' }, entry)), signal: ctl ? ctl.signal : undefined, redirect: 'follow' })
      .then(function (r) { clearTimeout(tm); return r.json(); });
  };
  Api.prototype.board = function () {
    if (!this.enabled()) return Promise.reject(new Error('disabled'));
    var ctl = typeof AbortController !== 'undefined' ? new AbortController() : null, ms = this.timeout;
    var tm = ctl && setTimeout(function () { ctl.abort(); }, ms);
    return fetch(this.url + (this.url.indexOf('?') < 0 ? '?' : '&') + 'action=board', { signal: ctl ? ctl.signal : undefined, redirect: 'follow' })
      .then(function (r) { clearTimeout(tm); return r.json(); });
  };

  /* ---- replay gate (shared with site.js, same localStorage key) ---- */
  function readGate() { try { return JSON.parse(localStorage.getItem(GATE_KEY) || 'null'); } catch (e) { return null; } }
  function writeGate(g) { try { if (g) localStorage.setItem(GATE_KEY, JSON.stringify(g)); else localStorage.removeItem(GATE_KEY); } catch (e) {} }
  function gateStatus(rules) {
    var g = readGate(); if (!g || !g.lockedAt) return { locked: false };
    var waitMs = rules.waitMinutes * 60000, browseNeed = rules.browseSeconds * 1000, now = Date.now();
    var leftWait = Math.max(0, g.lockedAt + waitMs - now), leftBrowse = Math.max(0, browseNeed - (g.browseMs || 0));
    if (leftWait === 0 || leftBrowse === 0 || now < g.lockedAt - 60000) { writeGate(null); return { locked: false }; }
    return { locked: true, leftWait: leftWait, leftBrowse: leftBrowse, browseNeed: browseNeed, browsed: g.browseMs || 0 };
  }
  function lockGate() { if (!readGate()) writeGate({ lockedAt: Date.now(), browseMs: 0 }); }

  window.AngryBagsApi = { Api: Api, normPhone: normPhone, cleanName: cleanName, toLatinDigits: toLatinDigits, gateStatus: gateStatus, lockGate: lockGate, GATE_KEY: GATE_KEY };
})();
