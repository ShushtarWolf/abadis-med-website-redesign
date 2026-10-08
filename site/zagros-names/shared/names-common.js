/* Shared helpers for the hospital-name samples: names list, Persian digits, counter pill. */
(function (global) {
  'use strict';
  var BASE = (document.currentScript && document.currentScript.src) ? document.currentScript.src.replace(/[^\/]*$/, '') : './';
  var FA = '۰۱۲۳۴۵۶۷۸۹';
  function fa(n) {                         // 1253 -> ۱٬۲۵۳ (Persian digits, Arabic thousands separator U+066C)
    var s = String(Math.max(0, Math.round(n))), out = '';
    for (var i = 0; i < s.length; i++) {
      if (i && (s.length - i) % 3 === 0) out += '\u066C';
      out += FA.charAt(+s.charAt(i));
    }
    return out;
  }
  var namesP = null;
  function loadNames() {
    if (!namesP) namesP = fetch(BASE + '../names.json').then(function (r) {
      if (!r.ok) throw new Error('names.json ' + r.status);
      return r.json();
    });
    return namesP;
  }
  function fontsReady(specs) {
    if (!document.fonts || !document.fonts.load) return Promise.resolve();
    var all = specs.map(function (s) { return document.fonts.load(s).catch(function () {}); });
    // never block the scene on a slow font host
    return Promise.race([Promise.all(all), new Promise(function (r) { setTimeout(r, 2500); })]);
  }
  function counter(el) {
    var num = el.querySelector('b'), last = -1;
    return { set: function (n) { n = Math.round(n); if (n !== last) { num.textContent = fa(n); last = n; } } };
  }
  function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }
  function seg(p, a, b) { return clamp((p - a) / (b - a), 0, 1); }
  function smooth(t) { return t * t * (3 - 2 * t); }
  // normalise for search: Arabic yeh/kaf -> Persian, drop ZWNJ/ZWJ/tatweel/diacritics, unify digits, collapse spaces
  function norm(s) {
    return String(s)
      .replace(/[يى]/g, 'ی').replace(/ك/g, 'ک').replace(/[ةه]/g, 'ه').replace(/[أإٱ]/g, 'ا').replace(/ؤ/g, 'و')
      .replace(/[\u064B-\u065F\u0670\u0640]/g, '')
      .replace(/[\u06F0-\u06F9]/g, function (d) { return String(d.charCodeAt(0) - 0x06F0); })
      .replace(/[\u0660-\u0669]/g, function (d) { return String(d.charCodeAt(0) - 0x0660); })
      .replace(/[\u200c\u200d\u200f\u200e]/g, ' ')
      .replace(/\s+/g, ' ').trim().toLowerCase();
  }
  global.ZN = { fa: fa, loadNames: loadNames, fontsReady: fontsReady, counter: counter, clamp: clamp, seg: seg, smooth: smooth, norm: norm };
})(window);
