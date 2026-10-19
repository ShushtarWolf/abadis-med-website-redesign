/* One Bag, One Oak. Savings come only from savings.json (the dial-practical formula). */
(function () {
  'use strict';

  var STORE = 'abadis-oak-v1';
  var THEMES = ['light', 'dark', 'noir'];
  var SIZE_SCALE = { 1: 0.78, 2: 1, 3: 1.22 };
  var SPOTS = [
    { u: 0.10, v: 0.80, s: 1.05 }, { u: 0.72, v: 0.78, s: 1.02 },
    { u: 0.28, v: 0.86, s: 1.08 }, { u: 0.52, v: 0.74, s: 0.96 },
    { u: 0.88, v: 0.84, s: 1.0 }, { u: 0.40, v: 0.90, s: 1.1 },
    { u: 0.18, v: 0.70, s: 0.9 }, { u: 0.62, v: 0.88, s: 1.06 },
    { u: 0.34, v: 0.66, s: 0.84 }, { u: 0.80, v: 0.68, s: 0.88 },
    { u: 0.06, v: 0.92, s: 1.12 }, { u: 0.48, v: 0.84, s: 1.0 },
    { u: 0.66, v: 0.64, s: 0.8 }, { u: 0.22, v: 0.78, s: 0.94 }
  ];
  var STAGE_KEY = ['young', 'young', 'grown', 'grown'];
  var STAGE_H = [0.30, 0.42, 0.56, 0.70];
  var SRC = {
    dry: '../zagros-names/shared/img/hero/bg-dry-1280.webp',
    mid: '../zagros-names/shared/img/hero/bg-mid-1280.webp',
    green: '../zagros-names/shared/img/hero/bg-green-1280.webp',
    young: '../zagros-names/shared/img/hero/young-oak.webp',
    grown: '../zagros-names/shared/img/hero/grown-oak.webp',
    bag: 'assets/abadis-bag.webp'
  };
  var SCRATCHES = [
    [0.22, 0.28, 0.46, 0.33], [0.58, 0.36, 0.74, 0.30], [0.30, 0.48, 0.52, 0.62],
    [0.18, 0.58, 0.28, 0.72], [0.62, 0.55, 0.80, 0.68], [0.36, 0.70, 0.55, 0.78],
    [0.24, 0.40, 0.34, 0.52], [0.68, 0.44, 0.78, 0.58]
  ];

  var i18n, cfg, per, state, lang = 'fa';
  var cases = [null, null];
  var caseSeq = 0;
  var lastSize = 2;
  var shown = { water: 0, cost: 0, hours: 0, seeds: 0 };
  var events = [];
  var msQueue = [];
  var lockUntil = 0;
  var hint = { key: '', vars: {} };
  var soundOn = false;
  var resetArm = false;
  var pops = {};
  var shakes = {};
  var ghostBurst = 0;
  var coachUntil = 0;
  var inFlight = 0;
  var currentLayout = null;
  var landCanvas = null;
  var landKey = '';
  var img = {};
  var bagSprite = null;
  var bagFull = null;
  var bagAspect = 644 / 860;
  var raf = 0;
  var last = 0;
  var frames = 0;
  var fps = 0;
  var fpsStamp = 0;
  var drag = null;
  var lastCoin = -1;
  var seedsFly = [];
  var reduceMQ = window.matchMedia('(prefers-reduced-motion: reduce)');

  var app = document.getElementById('app');
  var canvas = document.getElementById('view');
  var ctx = canvas.getContext('2d', { alpha: false });
  var titleCard = document.getElementById('titleCard');
  var milestone = document.getElementById('milestone');
  var shop = document.getElementById('shop');
  var hintEl = document.getElementById('hint');
  var caseChip = document.getElementById('caseChip');
  var caseText = document.getElementById('caseText');
  var handEl = document.getElementById('hand');
  var live = document.getElementById('live');
  var toastEl = document.getElementById('toast');

  var mist = [];
  for (var mi = 0; mi < 16; mi++) {
    mist.push({
      u: (mi * 0.17) % 1,
      v: 0.36 + ((mi * 37) % 50) / 140,
      r: 28 + (mi % 5) * 16,
      sp: 6 + (mi % 4) * 3,
      a: 0.05 + (mi % 3) * 0.025
    });
  }

  function reduced() { return reduceMQ.matches; }
  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }
  function smooth(a, b, x) {
    var u = clamp((x - a) / (b - a || 1), 0, 1);
    return u * u * (3 - 2 * u);
  }
  function t(key, vars) {
    var pack = (i18n && i18n[lang]) || {};
    var s = pack[key] != null ? pack[key] : key;
    if (vars) Object.keys(vars).forEach(function (k) { s = s.split('{' + k + '}').join(String(vars[k])); });
    return s;
  }
  function formatNum(n, digits) {
    var loc = lang === 'fa' ? 'fa-IR' : lang === 'ar' ? 'ar-EG' : 'en-US';
    return Number(n).toLocaleString(loc, { minimumFractionDigits: digits, maximumFractionDigits: digits });
  }
  function typeKey(id) { return id === 'short' ? 'typeShort' : id === 'long' ? 'typeLong' : 'typeStandard'; }
  function rtl() { return document.documentElement.dir === 'rtl'; }

  function track(name, extra) {
    var detail = Object.assign({ event: name, t: Date.now() }, extra || {});
    events.push(detail);
    try { window.dispatchEvent(new CustomEvent('abadis-oak', { detail: detail })); } catch (e) {}
    if (typeof window.abadisAnalytics === 'function') {
      try { window.abadisAnalytics(name, detail); } catch (e2) {}
    }
  }
  window.abadisOakTrack = track;

  function fresh() {
    return {
      v: 1, trees: 0, seeds: 0, water: 0, cost: 0, hours: 0, swaps: 0, cursor: 0,
      upgrades: { second: false, sealer: 0, lamp: 0, wildlife: 0 },
      seen: [], tutorialDone: false, started: false, lastSeen: 0, retired: false
    };
  }
  function loadState() {
    var base = fresh();
    try {
      var raw = JSON.parse(localStorage.getItem(STORE) || 'null');
      if (!raw || raw.v !== 1) return base;
      var s = Object.assign(base, raw);
      s.upgrades = Object.assign(fresh().upgrades, raw.upgrades || {});
      s.seen = Array.isArray(raw.seen) ? raw.seen : [];
      ['trees', 'seeds', 'water', 'cost', 'hours', 'swaps', 'cursor'].forEach(function (k) {
        if (!isFinite(s[k]) || s[k] < 0) s[k] = 0;
      });
      return s;
    } catch (e) { return fresh(); }
  }
  function save() {
    try { localStorage.setItem(STORE, JSON.stringify(state)); } catch (e) {}
  }
  function derive(c) {
    var f = c.formula;
    return {
      water: f.waterLitres.factors.reduce(function (a, b) { return a * b; }, 1),
      cost: f.costToman.factors.reduce(function (a, b) { return a * b; }, 1),
      hours: f.staffHours.minutes / 60 * f.staffHours.k1 * f.staffHours.k2
    };
  }
  function staffText(hours) {
    var minutes = hours * 60;
    if (minutes < 60) return formatNum(minutes, 1) + ' ' + t('minUnit');
    return formatNum(hours, 1) + ' ' + t('hourUnit');
  }
  function moneyText(cost) {
    var rounded = Math.round(cost);
    var abs = Math.abs(rounded);
    if (abs >= 1e12) return formatNum(rounded / 1e12, 1) + ' ' + t('moneyT12');
    if (abs >= 1e9) return formatNum(rounded / 1e9, 1) + ' ' + t('moneyT9');
    if (abs >= 1e6) return formatNum(rounded / 1e6, 1) + ' ' + t('moneyT6');
    return formatNum(rounded, 0) + ' ' + t('toman');
  }
  function showChem() {
    return !!(cfg && cfg.chemicals && cfg.chemicals.showCounter === true && cfg.chemicals.amount != null);
  }
  function pendingSum() {
    var p = { water: 0, cost: 0, hours: 0, seeds: 0 };
    cases.forEach(function (c) {
      if (c && c.reward && !c.reward.committed) {
        p.water += c.reward.water; p.cost += c.reward.cost;
        p.hours += c.reward.hours; p.seeds += c.reward.seeds;
      }
    });
    return p;
  }
  function noteRetired() {
    if (state.trees >= cfg.gameRules.washRetireTrees && !state.retired) {
      state.retired = true;
      save();
      toast(t('retired'));
    }
  }
  function grantSwaps(n) {
    state.water += per.water * n;
    state.cost += per.cost * n;
    state.hours += per.hours * n;
    state.seeds += cfg.gameRules.seedsPerCleanSwap * n;
    state.trees += n;
    state.swaps += n;
    save();
    noteRetired();
    checkMilestones();
  }
  function applyNight() {
    if (!state.started) return 0;
    if (!state.lastSeen) { state.lastSeen = Date.now(); save(); return 0; }
    var away = Date.now() - state.lastSeen;
    state.lastSeen = Date.now();
    var rule = cfg.gameRules.nightShift;
    if (away < rule.minAwayMs) { save(); return 0; }
    var elapsed = Math.min(away, rule.capHours * 3600000);
    var n = Math.floor(elapsed / rule.msPerTree);
    if (n > 0) grantSwaps(n);
    else save();
    return n;
  }
  function commitCase(c) {
    if (!c.reward || c.reward.committed) return;
    c.reward.committed = true;
    state.water += c.reward.water;
    state.cost += c.reward.cost;
    state.hours += c.reward.hours;
    state.seeds += c.reward.seeds;
    state.trees += c.reward.trees;
    state.swaps += 1;
    save();
    var litres = Math.round(state.water);
    track('swap', { size: c.size, bonus: !!c.bonus, litres: litres, swaps: state.swaps });
    live.textContent = t('liveSwap', { litres: formatNum(litres, 0) });
    noteRetired();
  }

  function slots() { return state.upgrades.second ? 2 : 1; }
  function makeCase() {
    var types = cfg.gameRules.surgeryTypes;
    var type = types[state.cursor % types.length];
    state.cursor += 1;
    save();
    return {
      id: ++caseSeq, type: type.id, size: type.sizeL, phase: 'lift',
      clean: true, bonus: false, t0: 0, reward: null, flying: false,
      used: state.swaps === 0 ? 'jar' : 'bag', usedSize: lastSize
    };
  }
  function ensureCases() {
    if (!state.upgrades.second) cases[1] = null;
    var n = slots();
    for (var i = 0; i < n; i++) if (!cases[i]) cases[i] = makeCase();
  }
  function primary() {
    var order = ['lift', 'bin', 'place', 'seal', 'sprout'];
    for (var p = 0; p < order.length; p++) {
      for (var i = 0; i < cases.length; i++) {
        if (cases[i] && cases[i].phase === order[p]) return cases[i];
      }
    }
    return null;
  }
  function busy() {
    return !titleCard.hidden || !milestone.hidden || !shop.hidden;
  }
  function setHint(key, vars) {
    hint = { key: key, vars: vars || {} };
    hintEl.textContent = t(key, hint.vars);
    hintEl.hidden = !titleCard.hidden;
  }
  function syncHint() {
    if (performance.now() < lockUntil) return;
    if (!titleCard.hidden) { hintEl.hidden = true; return; }
    var p = primary();
    if (!p) setHint('hintIdle');
    else if (p.phase === 'lift') setHint('hintLift');
    else if (p.phase === 'bin') setHint('hintBin');
    else if (p.phase === 'place') setHint('hintPlace', { n: formatNum(p.size, 0) });
    else if (p.phase === 'seal') setHint('hintSeal');
    else setHint('hintSprout');
  }
  function sealMs() {
    return Math.max(280, cfg.gameRules.sealMs - state.upgrades.sealer * cfg.gameRules.sealMsSavedPerLevel);
  }

  var audio = (function () {
    var actx, master, started = false;
    function ensure() {
      if (actx) return;
      var AC = window.AudioContext || window.webkitAudioContext;
      if (!AC) return;
      actx = new AC();
      master = actx.createGain();
      master.gain.value = 0;
      master.connect(actx.destination);
    }
    function ambience() {
      if (!actx || started) return;
      started = true;
      var len = actx.sampleRate * 2;
      var buf = actx.createBuffer(1, len, actx.sampleRate);
      var d = buf.getChannelData(0);
      var s = 0;
      for (var i = 0; i < len; i++) { s = (s + Math.random() * 2 - 1) * 0.35; d[i] = s * 0.25; }
      var src = actx.createBufferSource();
      src.buffer = buf; src.loop = true;
      var filter = actx.createBiquadFilter();
      filter.type = 'lowpass'; filter.frequency.value = 380;
      var ng = actx.createGain(); ng.gain.value = 0.09;
      src.connect(filter); filter.connect(ng); ng.connect(master); src.start();
      [174.61, 220].forEach(function (freq, idx) {
        var o = actx.createOscillator();
        var g = actx.createGain();
        o.type = 'sine'; o.frequency.value = freq; g.gain.value = idx ? 0.018 : 0.028;
        o.connect(g); g.connect(master); o.start();
      });
    }
    function blip(freq, dur, type, peak) {
      if (!actx || !master || master.gain.value < 0.01) return;
      var o = actx.createOscillator();
      var g = actx.createGain();
      o.type = type || 'sine';
      o.frequency.setValueAtTime(freq, actx.currentTime);
      g.gain.setValueAtTime(0.0001, actx.currentTime);
      g.gain.exponentialRampToValueAtTime(peak || 0.07, actx.currentTime + 0.015);
      g.gain.exponentialRampToValueAtTime(0.0001, actx.currentTime + dur);
      o.connect(g); g.connect(master);
      o.start(); o.stop(actx.currentTime + dur + 0.02);
    }
    return {
      set: function (on) {
        ensure();
        if (!actx) return;
        actx.resume();
        ambience();
        master.gain.setTargetAtTime(on ? 0.9 : 0, actx.currentTime, 0.06);
      },
      suspend: function () { if (actx) actx.suspend(); },
      resume: function () { if (actx && soundOn) actx.resume(); },
      click: function () { blip(760, 0.06); setTimeout(function () { blip(480, 0.05); }, 36); },
      seal: function () { blip(910, 0.05, 'sine', 0.06); },
      sprout: function () {
        if (!actx || !master || master.gain.value < 0.01) return;
        var o = actx.createOscillator();
        var g = actx.createGain();
        o.type = 'sine';
        o.frequency.setValueAtTime(420, actx.currentTime);
        o.frequency.linearRampToValueAtTime(680, actx.currentTime + 0.26);
        g.gain.setValueAtTime(0.0001, actx.currentTime);
        g.gain.exponentialRampToValueAtTime(0.06, actx.currentTime + 0.03);
        g.gain.exponentialRampToValueAtTime(0.0001, actx.currentTime + 0.34);
        o.connect(g); g.connect(master); o.start(); o.stop(actx.currentTime + 0.38);
      },
      softNo: function () { blip(170, 0.12, 'triangle', 0.05); }
    };
  })();

  function paintSound() {
    var btn = document.getElementById('soundBtn');
    btn.setAttribute('aria-pressed', soundOn ? 'true' : 'false');
    btn.setAttribute('aria-label', t(soundOn ? 'soundOn' : 'soundOff'));
  }
  function setSound(on, persist) {
    soundOn = !!on;
    if (persist) { try { localStorage.setItem('abadis-oak-mute', soundOn ? '0' : '1'); } catch (e) {} }
    audio.set(soundOn);
    paintSound();
  }
  function applyTheme(next, persist) {
    if (THEMES.indexOf(next) < 0) next = 'light';
    document.documentElement.dataset.theme = next;
    if (persist) { try { localStorage.setItem('abadis-theme', next); } catch (e) {} }
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.content = next === 'light' ? '#e8f3f3' : next === 'dark' ? '#061719' : '#0a0a12';
    var names = { light: 'themeLight', dark: 'themeDark', noir: 'themeNoir' };
    var nxt = THEMES[(THEMES.indexOf(next) + 1) % 3];
    var btn = document.getElementById('themeBtn');
    var label = t('themeLabel', { now: t(names[next]), next: t(names[nxt]) });
    btn.setAttribute('aria-label', label);
    btn.title = label;
  }
  function paintTitle() {
    document.title = t('metaTitle');
    var desc = document.querySelector('meta[name="description"]');
    if (desc) desc.content = t('metaDescription');
    document.getElementById('tagline').textContent = t('tagline');
    document.getElementById('heroTitle').textContent = t('title');
    document.getElementById('lead').textContent = t('lead');
    document.getElementById('wordmark').textContent = t('title');
    document.getElementById('logoLink').setAttribute('aria-label', t('brand'));
    var light = document.querySelector('.logo .lg-light');
    if (light) light.alt = t('brand');
    var returning = state.started || state.trees > 0;
    document.getElementById('start').textContent = returning ? t('resume') : t('start');
    var have = document.getElementById('haveTrees');
    if (state.trees > 0) {
      have.hidden = false;
      have.textContent = t('haveTrees', { n: formatNum(state.trees, 0) });
    } else have.hidden = true;
  }
  function applyStatic() {
    paintTitle();
    paintSound();
    applyTheme(document.documentElement.dataset.theme || 'light', false);
    document.querySelector('.skip').textContent = lang === 'en' ? 'Skip to the game' : lang === 'ar' ? 'إلى اللعبة' : 'پرش به بازی';
    document.getElementById('shareBtn').setAttribute('aria-label', t('share'));
    document.getElementById('helpBtn').setAttribute('aria-label', t('help'));
    document.getElementById('labWater').textContent = t('water');
    document.getElementById('labStaff').textContent = t('staff');
    document.getElementById('labMoney').textContent = t('money');
    var labChem = document.getElementById('labChem');
    if (labChem) labChem.textContent = t('chemicals');
    document.getElementById('shopTitle').textContent = t('shopTitle');
    document.getElementById('upSecond').textContent = t('upSecond');
    document.getElementById('upSealer').textContent = t('upSealer');
    document.getElementById('upLamp').textContent = t('upLamp');
    document.getElementById('upWild').textContent = t('upWild');
    document.getElementById('shopClose').textContent = t('close');
    document.getElementById('resetBtn').textContent = resetArm ? t('resetArmed') : t('reset');
    document.getElementById('msKicker').textContent = t('msKicker');
    document.getElementById('msLitreLabel').textContent = t('msLitre');
    document.getElementById('msStaffK').textContent = t('staff');
    document.getElementById('msMoneyK').textContent = t('money');
    var msChem = document.getElementById('msChem');
    msChem.textContent = t('msChem');
    msChem.hidden = !showChem();
    document.getElementById('pillChem').hidden = !showChem();
    document.getElementById('msCalc').textContent = t('msCalc');
    document.getElementById('msZagros').textContent = t('msZagros');
    document.getElementById('msClose').textContent = t('msClose');
    document.getElementById('msNote').textContent = t('msNote');
    if (cfg && cfg.links) {
      document.getElementById('msCalc').href = cfg.links.calculator;
      document.getElementById('msZagros').href = cfg.links.zagros;
    }
    document.querySelectorAll('.lang-link').forEach(function (b) {
      var code = b.dataset.lang;
      var name = code === 'en' ? 'langEn' : code === 'ar' ? 'langAr' : 'langFa';
      b.setAttribute('aria-label', t(name));
      b.setAttribute('aria-current', code === lang ? 'true' : 'false');
    });
    if (hint.key) hintEl.textContent = t(hint.key, hint.vars);
    renderChrome();
    paintNumbers();
  }
  function setLang(code) {
    if (code !== 'fa' && code !== 'en' && code !== 'ar') code = 'fa';
    lang = code;
    try { localStorage.setItem('abadis-oak-lang', code); } catch (e) {}
    var map = { fa: ['fa-IR', 'rtl'], en: ['en', 'ltr'], ar: ['ar', 'rtl'] };
    document.documentElement.lang = map[code][0];
    document.documentElement.dir = map[code][1];
    applyStatic();
  }
  function renderChrome() {
    var p = primary();
    app.dataset.phase = titleCard.hidden ? (p ? p.phase : 'idle') : 'title';
    if (p && titleCard.hidden) {
      caseChip.hidden = false;
      caseText.textContent = t('caseChip', { name: t(typeKey(p.type)), n: formatNum(p.size, 0) });
    } else caseChip.hidden = true;
    syncHint();
    paintShop();
  }
  function paintShop() {
    var seeds = state ? state.seeds : 0;
    document.getElementById('shopSeeds').textContent = formatNum(seeds, 0) + ' ' + t('seeds');
    document.getElementById('shopBtn').textContent = t('shop') + ' · ' + formatNum(Math.floor(shown.seeds || seeds), 0);
    [['second', 'costSecond'], ['sealer', 'costSealer'], ['lamp', 'costLamp'], ['wildlife', 'costWild']].forEach(function (pair) {
      var id = pair[0];
      var spec = cfg.gameRules.upgrades[id];
      var owned = id === 'second' ? (state.upgrades.second ? 1 : 0) : state.upgrades[id];
      var max = id === 'second' ? 1 : spec.max;
      var btn = document.querySelector('[data-up="' + id + '"]');
      var costEl = document.getElementById(pair[1]);
      costEl.textContent = owned >= max ? t('upHave') : t('upCost', { n: formatNum(spec.seeds, 0) });
      btn.disabled = owned >= max || seeds < spec.seeds;
    });
  }
  function paintNumbers() {
    var w = Math.round(shown.water);
    var cost = Math.round(shown.cost);
    document.getElementById('numWater').textContent = formatNum(w, 0);
    document.getElementById('pillWater').setAttribute('aria-label', t('water') + ' ' + formatNum(w, 0));
    var cap = per.water * cfg.gameRules.tankSwaps;
    document.getElementById('tankFill').style.height = clamp(shown.water / cap, 0, 1) * 100 + '%';
    document.getElementById('numStaff').textContent = staffText(shown.hours);
    document.getElementById('pillStaff').setAttribute('aria-label', t('staff') + ' ' + staffText(shown.hours));
    document.getElementById('numMoney').textContent = moneyText(shown.cost);
    document.getElementById('pillMoney').setAttribute('aria-label', t('money') + ' ' + moneyText(shown.cost));
    if (showChem()) {
      document.getElementById('numChem').textContent = formatNum(cfg.chemicals.amount, 0);
    }
    if (cost !== lastCoin) {
      if (lastCoin >= 0) {
        var coin = document.getElementById('numMoney');
        coin.classList.remove('pop'); void coin.offsetWidth; coin.classList.add('pop');
      }
      lastCoin = cost;
    }
    document.getElementById('shopBtn').textContent = t('shop') + ' · ' + formatNum(Math.floor(shown.seeds), 0);
  }

  function checkMilestones() {
    var open = milestone.hidden ? null : +milestone.dataset.mark;
    cfg.gameRules.milestones.forEach(function (m) {
      if (state.trees >= m && state.seen.indexOf(m) < 0 && msQueue.indexOf(m) < 0 && m !== open) msQueue.push(m);
    });
    pumpMilestone();
  }
  function pumpMilestone() {
    if (!msQueue.length) return;
    if (!titleCard.hidden || !milestone.hidden) return;
    openMilestone(msQueue.shift());
  }
  function clearDrag() { drag = null; }
  function openMilestone(mark) {
    clearDrag();
    milestone.dataset.mark = String(mark);
    document.getElementById('msLitres').textContent = formatNum(Math.round(state.water), 0);
    document.getElementById('msStaff').textContent = t('msStaffLine', { hours: staffText(state.hours) });
    document.getElementById('msMoney').textContent = t('msMoneyLine', { money: moneyText(state.cost) });
    var box = document.getElementById('msTags');
    box.textContent = '';
    var info = spotInfo(state.trees);
    info.slice(Math.max(0, info.length - 4)).forEach(function (s) {
      var d = document.createElement('span');
      d.className = 'tag-plate';
      d.textContent = formatNum(s.label, 0);
      box.appendChild(d);
    });
    milestone.hidden = false;
    document.getElementById('msClose').focus();
    track('milestone', { trees: mark, litres: Math.round(state.water) });
    renderChrome();
  }
  function closeMilestone() {
    var mark = +milestone.dataset.mark;
    if (mark && state.seen.indexOf(mark) < 0) state.seen.push(mark);
    milestone.hidden = true;
    save();
    renderChrome();
    pumpMilestone();
  }
  function mistake(kind, wanted, picked) {
    lockUntil = performance.now() + cfg.gameRules.mistakeDelayMs;
    if (kind === 'size') {
      setHint('hintWrongSize', { n: formatNum(wanted, 0) });
      shakes[picked] = performance.now();
      live.textContent = t('liveWrong');
    } else setHint('hintWrongBin');
    audio.softNo();
    renderChrome();
  }
  function tryLift(i) {
    var c = cases[i];
    if (busy() || performance.now() < lockUntil || !c || c.phase !== 'lift') return;
    c.phase = 'bin';
    audio.click();
    renderChrome();
  }
  function tryPlace(size, i) {
    if (busy() || performance.now() < lockUntil) return;
    var idx = i;
    if (idx == null || !cases[idx] || cases[idx].phase !== 'place') {
      idx = -1;
      for (var k = 0; k < cases.length; k++) {
        if (cases[k] && cases[k].phase === 'place' && cases[k].size === size) { idx = k; break; }
      }
      if (idx < 0) {
        for (var k2 = 0; k2 < cases.length; k2++) {
          if (cases[k2] && cases[k2].phase === 'place') { idx = k2; break; }
        }
      }
    }
    if (idx < 0) return;
    var c = cases[idx];
    if (size !== c.size) { mistake('size', c.size, size); return; }
    beginSeal(c, idx);
  }
  function beginSeal(c) {
    c.phase = 'seal';
    c.t0 = performance.now();
    var seeds = cfg.gameRules.seedsPerCleanSwap + (c.bonus ? cfg.gameRules.bonusSeedsForCorrectBin : 0);
    c.reward = {
      water: per.water, cost: per.cost, hours: per.hours,
      seeds: seeds, trees: 1, committed: false
    };
    lastSize = c.size;
    audio.click();
    if (!reduced() && navigator.vibrate) { try { navigator.vibrate(12); } catch (e) {} }
    flyMotes();
    renderChrome();
  }
  function tryBin(i, kind) {
    var c = cases[i];
    if (busy() || performance.now() < lockUntil || !c || c.phase !== 'bin') return;
    if (kind !== cfg.gameRules.correctBin) {
      c.clean = false;
      c.bonus = false;
      mistake('bin');
      return;
    }
    c.bonus = !!c.clean;
    c.phase = 'place';
    audio.click();
    renderChrome();
  }
  function flyMotes() {
    if (reduced() || !currentLayout) return;
    var targets = [
      document.getElementById('pillWater'),
      document.getElementById('pillStaff'),
      document.getElementById('pillMoney')
    ];
    var rect = canvas.getBoundingClientRect();
    var u = currentLayout.units[0];
    var sx = rect.left + u.footX;
    var sy = rect.top + u.footY - u.itemH * 0.5;
    targets.forEach(function (el, i) {
      if (!el || el.hidden) return;
      var dot = document.createElement('i');
      dot.className = 'mote';
      dot.style.left = sx + 'px';
      dot.style.top = sy + 'px';
      document.body.appendChild(dot);
      var b = el.getBoundingClientRect();
      setTimeout(function () {
        dot.style.transform = 'translate(' + (b.left + b.width / 2 - sx) + 'px,' + (b.top + b.height / 2 - sy) + 'px) scale(.4)';
        dot.style.opacity = '0.1';
      }, 40 + i * 70);
      setTimeout(function () { dot.remove(); }, 980);
    });
  }
  function launchSeed(from, spotIndex, done) {
    if (reduced() || !currentLayout) { done(); return; }
    var sp = SPOTS[spotIndex];
    var win = currentLayout.win;
    seedsFly.push({
      x: from.x, y: from.y,
      tx: win.x + win.w * sp.u,
      ty: win.y + win.h * sp.v,
      t0: performance.now(),
      done: done,
      fired: false
    });
  }
  function toast(msg) {
    toastEl.textContent = msg;
    toastEl.classList.add('on');
    setTimeout(function () { toastEl.classList.remove('on'); }, 3200);
  }
  function buy(id) {
    var spec = cfg.gameRules.upgrades[id];
    var owned = id === 'second' ? (state.upgrades.second ? 1 : 0) : state.upgrades[id];
    var max = id === 'second' ? 1 : spec.max;
    if (owned >= max || state.seeds < spec.seeds) return;
    state.seeds -= spec.seeds;
    if (id === 'second') state.upgrades.second = true;
    else state.upgrades[id] += 1;
    shown.seeds = state.seeds;
    save();
    if (titleCard.hidden) ensureCases();
    renderChrome();
  }

  function rectHit(r, x, y, min) {
    if (!r) return false;
    var w = Math.max(r.w, min || 44);
    var h = Math.max(r.h, min || 44);
    var cx = r.x + r.w / 2;
    var cy = r.y + r.h / 2;
    return Math.abs(x - cx) <= w / 2 && Math.abs(y - cy) <= h / 2;
  }
  function localPoint(e) {
    var r = canvas.getBoundingClientRect();
    return { x: e.clientX - r.left, y: e.clientY - r.top };
  }
  function hitTest(x, y) {
    var L = currentLayout;
    if (!L || busy()) return null;
    for (var i = 0; i < L.used.length; i++) {
      var u = L.used[i];
      if (u && cases[i] && (cases[i].phase === 'lift' || cases[i].phase === 'bin') && rectHit(u, x, y, 48)) {
        return { kind: 'used', index: i };
      }
    }
    var placing = cases.some(function (c) { return c && c.phase === 'place'; });
    if (placing) {
      var sizes = [1, 2, 3];
      for (var s = 0; s < sizes.length; s++) {
        if (rectHit(L.bags[sizes[s]], x, y, 48)) return { kind: 'bag', size: sizes[s] };
      }
    }
    var binning = cases.some(function (c) { return c && c.phase === 'bin'; });
    if (binning) {
      if (rectHit(L.bins.infectious, x, y, 52)) return { kind: 'bin', bin: 'infectious' };
      if (rectHit(L.bins.general, x, y, 52)) return { kind: 'bin', bin: 'general' };
    }
    return null;
  }
  function binAt(x, y) {
    var L = currentLayout;
    if (!L) return null;
    if (rectHit(L.bins.infectious, x, y, 56)) return 'infectious';
    if (rectHit(L.bins.general, x, y, 56)) return 'general';
    return null;
  }
  function unitAt(x, y) {
    var L = currentLayout;
    if (!L) return -1;
    for (var i = 0; i < L.units.length; i++) {
      var u = L.units[i];
      var r = { x: u.footX - u.itemW / 2, y: u.footY - u.itemH, w: u.itemW, h: u.itemH };
      if (rectHit(r, x, y, 64) && cases[i] && cases[i].phase === 'place') return i;
    }
    for (var j = 0; j < L.units.length; j++) {
      if (cases[j] && cases[j].phase === 'place') {
        var u2 = L.units[j];
        var r2 = { x: u2.footX - u2.itemW / 2, y: u2.footY - u2.itemH, w: u2.itemW, h: u2.itemH };
        if (rectHit(r2, x, y, 80)) return j;
      }
    }
    return -1;
  }
  function onDown(e) {
    if (e.button != null && e.button !== 0) return;
    if (busy()) return;
    var p = localPoint(e);
    var hit = hitTest(p.x, p.y);
    if (!hit) return;
    drag = {
      kind: hit.kind, index: hit.index, size: hit.size, bin: hit.bin,
      sx: e.clientX, sy: e.clientY, px: p.x, py: p.y,
      pid: e.pointerId, moved: false
    };
    try { canvas.setPointerCapture(e.pointerId); } catch (err) {}
  }
  function onMove(e) {
    if (!drag || e.pointerId !== drag.pid) return;
    var p = localPoint(e);
    drag.px = p.x; drag.py = p.y;
    if (Math.hypot(e.clientX - drag.sx, e.clientY - drag.sy) > 8) drag.moved = true;
  }
  function onUp(e) {
    if (!drag || (e.pointerId != null && e.pointerId !== drag.pid)) return;
    var d = drag;
    drag = null;
    if (busy()) return;
    if (d.kind === 'used') {
      var c = cases[d.index];
      if (!c) return;
      if (!d.moved) {
        if (c.phase === 'lift') tryLift(d.index);
        else if (c.phase === 'bin') tryBin(d.index, cfg.gameRules.correctBin);
        return;
      }
      if (c.phase === 'lift') c.phase = 'bin';
      var b = binAt(d.px, d.py);
      if (b) tryBin(d.index, b);
      else renderChrome();
    } else if (d.kind === 'bag') {
      if (!d.moved) { tryPlace(d.size, null); return; }
      var ui = unitAt(d.px, d.py);
      if (ui >= 0) tryPlace(d.size, ui);
    } else if (d.kind === 'bin' && !d.moved) {
      var idx = -1;
      for (var i = 0; i < cases.length; i++) if (cases[i] && cases[i].phase === 'bin') { idx = i; break; }
      if (idx >= 0) tryBin(idx, d.bin);
    }
  }

  function palette() {
    var th = document.documentElement.dataset.theme;
    if (th === 'noir') return {
      w0: '#221838', w1: '#100c1c', floor: '#140e22', frame: '#ebe6f8', sill: '#2a2344',
      cloth: '#d9d4ea', metal: '#c8c0dc', glow: 'rgba(220,210,245,.2)'
    };
    if (th === 'dark') return {
      w0: '#0c3034', w1: '#041416', floor: '#071c1e', frame: '#d5e6e2', sill: '#0e3336',
      cloth: '#d5e4e2', metal: '#b7c9c6', glow: 'rgba(210,236,234,.18)'
    };
    return {
      w0: '#11555a', w1: '#07282c', floor: '#0a3034', frame: '#e7f3f1', sill: '#0d3e42',
      cloth: '#e7f2f0', metal: '#d5e2e0', glow: 'rgba(220,244,242,.22)'
    };
  }
  function roundRect(c, x, y, w, h, r) {
    var rr = Math.min(r, Math.abs(w) / 2, Math.abs(h) / 2);
    c.beginPath();
    c.moveTo(x + rr, y);
    c.arcTo(x + w, y, x + w, y + h, rr);
    c.arcTo(x + w, y + h, x, y + h, rr);
    c.arcTo(x, y + h, x, y, rr);
    c.arcTo(x, y, x + w, y, rr);
    c.closePath();
  }
  function drawCover(c, image, x, y, w, h, ax, ay) {
    var s = Math.max(w / image.width, h / image.height);
    var sw = w / s, sh = h / s;
    var sx = (image.width - sw) * ax;
    var sy = (image.height - sh) * ay;
    c.drawImage(image, sx, sy, sw, sh, x, y, w, h);
  }
  function greenMix(trees) {
    var g = cfg.gameRules.green;
    return { mid: smooth(g.midFrom, g.midTo, trees), green: smooth(g.greenFrom, g.greenTo, trees) };
  }
  function paintLand(w, h, dpr, mix) {
    var key = [Math.round(w), Math.round(h), dpr, mix.mid.toFixed(2), mix.green.toFixed(2)].join('|');
    if (key === landKey && landCanvas) return;
    landKey = key;
    if (!landCanvas) landCanvas = document.createElement('canvas');
    landCanvas.width = Math.max(1, Math.round(w * dpr));
    landCanvas.height = Math.max(1, Math.round(h * dpr));
    var c = landCanvas.getContext('2d');
    c.setTransform(dpr, 0, 0, dpr, 0, 0);
    if (img.dry) drawCover(c, img.dry, 0, 0, w, h, 0.5, 0.62);
    else { c.fillStyle = '#c4b8a4'; c.fillRect(0, 0, w, h); }
    if (img.mid && mix.mid > 0.01) { c.globalAlpha = mix.mid; drawCover(c, img.mid, 0, 0, w, h, 0.5, 0.62); }
    if (img.green && mix.green > 0.01) { c.globalAlpha = mix.green; drawCover(c, img.green, 0, 0, w, h, 0.5, 0.62); }
    c.globalAlpha = 1;
  }
  function spotInfo(total) {
    var n = SPOTS.length;
    var shownN = Math.min(total, n);
    var out = [];
    for (var i = 0; i < shownN; i++) {
      var layers = 1 + Math.floor(Math.max(0, total - 1 - i) / n);
      out.push({
        i: i,
        stage: Math.min(3, Math.max(1, Math.floor((total - i + 2) / 2))),
        label: i + 1 + (layers - 1) * n
      });
    }
    return out;
  }
  function popScale(t0, now) {
    if (!t0 || reduced()) return { x: 1, y: 1 };
    var u = (now - t0) / 720;
    if (u >= 1) return { x: 1, y: 1 };
    if (u < 0.35) { var k = u / 0.35; return { x: 1 - 0.12 * k, y: 1 + 0.18 * k }; }
    if (u < 0.7) { var k2 = (u - 0.35) / 0.35; return { x: 0.88 + 0.18 * k2, y: 1.18 - 0.28 * k2 }; }
    var k3 = (u - 0.7) / 0.3;
    return { x: 1.06 - 0.06 * k3, y: 0.9 + 0.1 * k3 };
  }
  function wildOn(name) {
    var need = cfg.gameRules.wildlifeAtTrees[name];
    if (need == null) return false;
    var earlier = (state.upgrades.wildlife || 0) * cfg.gameRules.upgrades.wildlife.treesEarlier;
    return state.trees + earlier >= need;
  }
  function ghostAlpha() {
    var base = 1 - smooth(0, 8, state.trees);
    return clamp(base * 0.96 * (1 - (ghostBurst || 0) * 0.62), 0, 1);
  }

  function jarBody(c, cx, top, bw, bh, ry) {
    c.beginPath();
    c.ellipse(cx, top, bw / 2, ry, 0, Math.PI, 0, true);
    c.lineTo(cx + bw / 2, top + bh);
    c.ellipse(cx, top + bh, bw / 2, ry * 0.85, 0, 0, Math.PI, false);
    c.closePath();
  }
  function drawOldJar(c, x, y, w, h, tilt) {
    c.save();
    c.translate(x + w / 2, y + h * 0.94);
    c.rotate(tilt || 0);
    c.translate(-(x + w / 2), -(y + h * 0.94));
    var cx = x + w * 0.48;
    var top = y + h * 0.2;
    var bw = w * 0.78;
    var bh = h * 0.68;
    var ry = Math.max(7, bw * 0.14);
    c.fillStyle = 'rgba(10,18,20,.34)';
    c.beginPath();
    c.ellipse(cx, y + h * 0.95, bw * 0.48, Math.max(4, h * 0.04), 0, 0, Math.PI * 2);
    c.fill();
    c.strokeStyle = '#8e9694';
    c.lineWidth = Math.max(3, w * 0.045);
    c.beginPath();
    c.moveTo(cx - bw * 0.52, top + bh * 0.35);
    c.quadraticCurveTo(cx - bw * 0.78, top + bh * 0.15, cx - bw * 0.5, top + bh * 0.02);
    c.stroke();
    jarBody(c, cx, top, bw, bh, ry);
    var glass = c.createLinearGradient(cx - bw / 2, 0, cx + bw / 2, 0);
    glass.addColorStop(0, 'rgba(70,80,78,.78)');
    glass.addColorStop(0.16, 'rgba(226,230,228,.5)');
    glass.addColorStop(0.4, 'rgba(150,158,154,.36)');
    glass.addColorStop(0.72, 'rgba(196,202,198,.4)');
    glass.addColorStop(1, 'rgba(58,66,64,.8)');
    c.fillStyle = glass;
    c.fill();
    c.save();
    jarBody(c, cx, top, bw, bh, ry);
    c.clip();
    var fluid = c.createLinearGradient(0, top + bh * 0.28, 0, top + bh);
    fluid.addColorStop(0, 'rgba(120,112,90,0)');
    fluid.addColorStop(0.12, 'rgba(110,102,78,.5)');
    fluid.addColorStop(1, 'rgba(54,52,40,.78)');
    c.fillStyle = fluid;
    c.fillRect(cx - bw, top + bh * 0.32, bw * 2, bh);
    c.strokeStyle = 'rgba(62,56,40,.7)';
    c.lineWidth = 2;
    c.beginPath();
    c.moveTo(cx - bw * 0.4, top + bh * 0.36);
    c.bezierCurveTo(cx - bw * 0.1, top + bh * 0.28, cx + bw * 0.15, top + bh * 0.44, cx + bw * 0.42, top + bh * 0.34);
    c.stroke();
    SCRATCHES.forEach(function (s, i) {
      c.strokeStyle = i % 2 ? 'rgba(36,32,24,.55)' : 'rgba(255,255,255,.45)';
      c.lineWidth = i % 3 === 0 ? 1.6 : 1;
      c.beginPath();
      c.moveTo(cx - bw / 2 + bw * s[0], top + bh * s[1]);
      c.lineTo(cx - bw / 2 + bw * s[2], top + bh * s[3]);
      c.stroke();
    });
    c.fillStyle = 'rgba(48,42,32,.4)';
    [[0.3, 0.72], [0.55, 0.8], [0.42, 0.6], [0.68, 0.7]].forEach(function (p) {
      c.beginPath();
      c.ellipse(cx - bw / 2 + bw * p[0], top + bh * p[1], bw * 0.06, bh * 0.025, 0.5, 0, 7);
      c.fill();
    });
    var shine = c.createLinearGradient(cx - bw * 0.36, 0, cx - bw * 0.12, 0);
    shine.addColorStop(0, 'rgba(255,255,255,0)');
    shine.addColorStop(0.5, 'rgba(255,255,255,.32)');
    shine.addColorStop(1, 'rgba(255,255,255,0)');
    c.fillStyle = shine;
    c.fillRect(cx - bw * 0.4, top + 6, bw * 0.16, bh);
    c.restore();
    var bandY = top + bh * 0.42;
    var metal = c.createLinearGradient(0, bandY, 0, bandY + h * 0.08);
    metal.addColorStop(0, '#f4f6f8');
    metal.addColorStop(0.45, '#7e868e');
    metal.addColorStop(1, '#d8dce0');
    c.fillStyle = metal;
    roundRect(c, cx - bw * 0.54, bandY, bw * 1.08, h * 0.07, 3);
    c.fill();
    c.fillStyle = '#4e555c';
    [-0.28, 0.28].forEach(function (p) {
      c.beginPath();
      c.arc(cx + bw * p, bandY + h * 0.035, Math.max(1.6, w * 0.02), 0, 7);
      c.fill();
    });
    var lidY = top - h * 0.02;
    var lid = c.createLinearGradient(0, lidY - h * 0.1, 0, lidY + ry);
    lid.addColorStop(0, '#f7f8fa');
    lid.addColorStop(0.35, '#a0a7ae');
    lid.addColorStop(1, '#dedfe3');
    c.fillStyle = lid;
    c.beginPath();
    c.ellipse(cx, lidY, bw * 0.46, ry * 0.85, 0, 0, Math.PI * 2);
    c.fill();
    c.strokeStyle = '#6c737a';
    c.lineWidth = 1.5;
    c.stroke();
    c.fillStyle = '#5c646c';
    c.beginPath();
    c.ellipse(cx, lidY - ry * 0.2, bw * 0.08, ry * 0.35, 0, 0, 7);
    c.fill();
    c.strokeStyle = '#4e5854';
    c.lineWidth = Math.max(4.5, w * 0.065);
    c.lineCap = 'round';
    c.beginPath();
    c.moveTo(cx, lidY - ry * 0.15);
    c.bezierCurveTo(cx, y + h * 0.02, x + w * 1.05, y + h * 0.08, x + w * 1.08, y + h * 0.28);
    c.stroke();
    c.strokeStyle = 'rgba(86,74,56,.65)';
    c.lineWidth = Math.max(2, w * 0.02);
    c.beginPath();
    c.moveTo(cx + bw * 0.1, lidY);
    c.bezierCurveTo(cx + bw * 0.4, top + bh * 0.15, x + w * 0.95, top + bh * 0.05, x + w * 1.02, y + h * 0.26);
    c.stroke();
    c.restore();
  }

  function bakeBag() {
    if (!img.bag) return;
    bagAspect = img.bag.width / img.bag.height;
    function make(full) {
      var s = document.createElement('canvas');
      s.width = img.bag.width;
      s.height = img.bag.height;
      var c = s.getContext('2d');
      c.drawImage(img.bag, 0, 0);
      c.globalCompositeOperation = 'source-atop';
      var g = c.createLinearGradient(s.width * 0.08, 0, s.width * 0.4, s.height);
      g.addColorStop(0, 'rgba(255,255,255,.34)');
      g.addColorStop(0.22, 'rgba(255,255,255,.08)');
      g.addColorStop(0.55, 'rgba(255,255,255,0)');
      c.fillStyle = g;
      c.fillRect(0, 0, s.width * 0.45, s.height);
      if (full) {
        var f = c.createLinearGradient(0, s.height * 0.42, 0, s.height * 0.92);
        f.addColorStop(0, 'rgba(176,198,204,0)');
        f.addColorStop(0.25, 'rgba(168,196,204,.22)');
        f.addColorStop(1, 'rgba(150,178,186,.34)');
        c.fillStyle = f;
        c.fillRect(0, s.height * 0.4, s.width, s.height * 0.55);
      }
      return s;
    }
    bagSprite = make(false);
    bagFull = make(true);
  }
  function drawBag(c, rect, mode, seal) {
    var sprite = mode === 'sealed' ? (bagFull || bagSprite) : bagSprite;
    c.save();
    c.fillStyle = 'rgba(8,24,28,.24)';
    c.beginPath();
    c.ellipse(rect.x + rect.w / 2, rect.y + rect.h - 1, rect.w * 0.32, Math.max(3, rect.h * 0.03), 0, 0, Math.PI * 2);
    c.fill();
    if (sprite) c.drawImage(sprite, rect.x, rect.y, rect.w, rect.h);
    else {
      roundRect(c, rect.x + rect.w * 0.18, rect.y + rect.h * 0.16, rect.w * 0.64, rect.h * 0.78, rect.w * 0.12);
      c.fillStyle = 'rgba(236,242,242,.92)';
      c.fill();
      roundRect(c, rect.x + rect.w * 0.16, rect.y + rect.h * 0.02, rect.w * 0.68, rect.h * 0.2, 6);
      c.fillStyle = '#0e7475';
      c.fill();
    }
    if (seal > 0.02) {
      var y = rect.y + rect.h * 0.2;
      var bh = Math.max(5, rect.h * 0.04);
      c.globalAlpha = 0.45 + 0.55 * seal;
      roundRect(c, rect.x + rect.w * 0.22, y, rect.w * 0.56, bh, bh / 2);
      c.fillStyle = '#066163';
      c.fill();
      c.fillStyle = '#f3fafa';
      c.beginPath();
      c.arc(rect.x + rect.w * 0.5, y + bh / 2, bh * 0.32, 0, Math.PI * 2);
      c.fill();
      c.globalAlpha = 1;
    }
    c.restore();
  }
  function drawSealProgress(c, rect, k) {
    drawBag(c, rect, 'sealed', k);
  }

  function drawStaff(c, x, y, scale, role, carry) {
    c.save();
    c.translate(x, y);
    c.scale(scale, scale);
    var skin = '#e6c4ae';
    var scrub = role === 'porter' ? '#083e44' : '#0e7475';
    var scrub2 = role === 'porter' ? '#062e32' : '#066163';
    c.fillStyle = 'rgba(0,0,0,.18)';
    c.beginPath();
    c.ellipse(0, 2, 22, 5, 0, 0, 7);
    c.fill();
    c.fillStyle = '#1c2c30';
    roundRect(c, -16, -8, 12, 8, 2); c.fill();
    roundRect(c, 4, -8, 12, 8, 2); c.fill();
    c.fillStyle = scrub2;
    roundRect(c, -13, -52, 11, 46, 4); c.fill();
    roundRect(c, 2, -52, 11, 46, 4); c.fill();
    var torso = c.createLinearGradient(-20, -100, 20, -40);
    torso.addColorStop(0, scrub);
    torso.addColorStop(1, scrub2);
    c.fillStyle = torso;
    roundRect(c, -22, -108, 44, 62, 12);
    c.fill();
    c.fillStyle = 'rgba(243,250,250,.85)';
    roundRect(c, -8, -104, 16, 10, 3); c.fill();
    c.fillStyle = scrub;
    if (carry) {
      roundRect(c, -34, -96, 14, 36, 6); c.fill();
      roundRect(c, 18, -78, 14, 28, 6); c.fill();
    } else {
      roundRect(c, -36, -100, 14, 42, 6); c.fill();
      roundRect(c, 22, -100, 14, 42, 6); c.fill();
    }
    c.fillStyle = skin;
    roundRect(c, -32, -64, 12, 12, 4); c.fill();
    roundRect(c, 20, -64, 12, 12, 4); c.fill();
    c.fillStyle = skin;
    roundRect(c, -7, -122, 14, 12, 4); c.fill();
    c.beginPath();
    c.ellipse(0, -132, 15, 17, 0, 0, 7);
    c.fill();
    c.fillStyle = role === 'porter' ? '#2a2420' : '#f3fafa';
    if (role === 'porter') {
      c.beginPath();
      c.ellipse(0, -140, 15, 10, 0, Math.PI, 0);
      c.fill();
    } else {
      roundRect(c, -16, -152, 32, 14, 6); c.fill();
      c.fillStyle = '#e7f3f1';
      c.fillRect(-16, -142, 32, 4);
    }
    c.fillStyle = '#2c2420';
    c.beginPath();
    c.ellipse(-5, -134, 1.5, 1.8, 0, 0, 7);
    c.ellipse(5, -134, 1.5, 1.8, 0, 0, 7);
    c.fill();
    c.strokeStyle = 'rgba(90,60,50,.7)';
    c.lineWidth = 1.2;
    c.beginPath();
    c.arc(0, -128, 4, 0.15, Math.PI - 0.15);
    c.stroke();
    if (carry) {
      c.save();
      c.translate(18, -70);
      c.rotate(-0.35);
      drawOldJar(c, -28, -48, 58, 78, 0);
      c.restore();
    }
    c.restore();
  }

  function drawVignette(c, win, alpha, now) {
    if (alpha < 0.03) return;
    var vw = win.w * (0.42 + 0.26 * alpha);
    var vh = win.h * (0.36 + 0.2 * alpha);
    var vx = win.x + (win.w - vw) / 2;
    var vy = win.y + win.h * 0.07;
    c.save();
    c.beginPath();
    c.rect(win.x, win.y, win.w, win.h);
    c.clip();
    c.globalAlpha = alpha;
    roundRect(c, vx, vy, vw, vh, 18);
    c.fillStyle = 'rgba(243,250,250,.72)';
    c.fill();
    c.strokeStyle = 'rgba(6,97,99,.35)';
    c.lineWidth = 2;
    c.stroke();
    var wash = (1 - alpha) + (ghostBurst || 0) * 0.35;
    c.save();
    roundRect(c, vx, vy, vw, vh, 18);
    c.clip();
    c.globalAlpha = alpha * Math.min(1, wash + 0.15);
    c.fillStyle = 'rgba(150,196,198,.45)';
    var wave = reduced() ? 0 : Math.sin(now / 500) * 4;
    for (var i = 0; i < 4; i++) {
      c.globalAlpha = alpha * (0.12 + wash * 0.2);
      c.fillRect(vx, vy + vh * (0.55 + i * 0.1) + wave, vw, 3 + i);
    }
    c.restore();
    c.globalAlpha = alpha;
    var sinkX = vx + vw * 0.06;
    var sinkY = vy + vh * 0.42;
    var sinkW = vw * 0.24;
    c.fillStyle = '#d5e0de';
    roundRect(c, sinkX, sinkY, sinkW, vh * 0.28, 8);
    c.fill();
    c.fillStyle = '#b7c8c6';
    c.beginPath();
    c.ellipse(sinkX + sinkW / 2, sinkY + vh * 0.12, sinkW * 0.32, vh * 0.07, 0, 0, 7);
    c.fill();
    c.strokeStyle = '#8aa09e';
    c.lineWidth = 3;
    c.beginPath();
    c.moveTo(sinkX + sinkW * 0.5, sinkY);
    c.lineTo(sinkX + sinkW * 0.5, sinkY - vh * 0.12);
    c.lineTo(sinkX + sinkW * 0.78, sinkY - vh * 0.12);
    c.stroke();
    drawStaff(c, vx + vw * 0.5, vy + vh * 0.86, Math.min(0.72, vh / 230), 'nurse', true);
    var bx = vx + vw * 0.72;
    var baseY = vy + vh * 0.62;
    [[0, 28, '#e7f1f0'], [16, 40, 'rgba(180,210,208,.85)'], [34, 22, '#c5d0ce']].forEach(function (b) {
      roundRect(c, bx + b[0], baseY - b[1], 12, b[1], 3);
      c.fillStyle = b[2];
      c.fill();
      c.fillStyle = '#9aa8a6';
      c.fillRect(bx + b[0] - 1, baseY - b[1] - 4, 14, 5);
    });
    var clockX = vx + vw * 0.84;
    var clockY = vy + vh * 0.22;
    c.beginPath();
    c.arc(clockX, clockY, Math.min(18, vw * 0.06), 0, 7);
    c.fillStyle = '#f7fbfb';
    c.fill();
    c.strokeStyle = '#066163';
    c.lineWidth = 2;
    c.stroke();
    c.beginPath();
    c.moveTo(clockX, clockY);
    c.lineTo(clockX, clockY - 10);
    c.moveTo(clockX, clockY);
    c.lineTo(clockX + 7, clockY + 2);
    c.stroke();
    c.restore();
  }

  function drawBin(c, r, kind, hot) {
    var inf = kind === 'infectious';
    var body = inf ? '#6e2430' : '#5c6765';
    var lid = inf ? '#8a3140' : '#7d8785';
    c.save();
    c.fillStyle = 'rgba(0,0,0,.2)';
    c.beginPath();
    c.ellipse(r.x + r.w / 2, r.y + r.h - 2, r.w * 0.4, 4, 0, 0, 7);
    c.fill();
    roundRect(c, r.x, r.y + r.h * 0.16, r.w, r.h * 0.82, 8);
    c.fillStyle = body;
    c.fill();
    c.fillStyle = lid;
    c.beginPath();
    c.ellipse(r.x + r.w / 2, r.y + r.h * 0.18, r.w * 0.46, r.h * 0.09, 0, 0, 7);
    c.fill();
    c.fillStyle = 'rgba(0,0,0,.25)';
    c.beginPath();
    c.ellipse(r.x + r.w / 2, r.y + r.h * 0.2, r.w * 0.3, r.h * 0.05, 0, 0, 7);
    c.fill();
    if (hot) {
      c.strokeStyle = 'rgba(243,250,250,.9)';
      c.lineWidth = 3;
      roundRect(c, r.x - 3, r.y + r.h * 0.12, r.w + 6, r.h * 0.86, 10);
      c.stroke();
    }
    c.fillStyle = '#f3fafa';
    c.font = '700 12px Kalameh, Tahoma, sans-serif';
    c.textAlign = 'center';
    c.textBaseline = 'middle';
    var label = t(inf ? 'binInfShort' : 'binGenShort');
    c.fillText(label, r.x + r.w / 2, r.y + r.h * 0.62);
    c.restore();
  }

  function drawRing(c, r, now) {
    if (!r) return;
    var k = reduced() ? 0.7 : (0.45 + 0.55 * Math.sin(now / 260));
    c.save();
    c.strokeStyle = 'rgba(4,16,18,' + (0.35 + 0.2 * k) + ')';
    c.lineWidth = 5;
    roundRect(c, r.x - 5, r.y - 5, r.w + 10, r.h + 10, 14);
    c.stroke();
    c.strokeStyle = 'rgba(244,251,251,' + (0.55 + 0.4 * k) + ')';
    c.lineWidth = 2.4;
    c.setLineDash([7, 5]);
    roundRect(c, r.x - 5, r.y - 5, r.w + 10, r.h + 10, 14);
    c.stroke();
    c.restore();
  }

  function computeLayout(w, h) {
    var wide = w >= 820;
    var hud = 62;
    var margin = 10;
    var win = wide
      ? { x: 12, y: 8, w: w - 24, h: Math.max(220, h * 0.62) }
      : { x: 8, y: 6, w: w - 16, h: Math.max(200, h * 0.56) };
    var foot = h - hud - 16;
    var base = wide ? Math.min(156, h * 0.22) : Math.min(86, h * 0.105);
    var bags = {};
    var sizes = [1, 2, 3];
    var gap = wide ? 14 : 8;
    var cursorX = rtl() ? (w - margin) : margin;
    var tall = base * SIZE_SCALE[3];
    sizes.forEach(function (sz) {
      var bh = base * SIZE_SCALE[sz];
      var bw = bh * bagAspect;
      var left = rtl() ? cursorX - bw : cursorX;
      bags[sz] = { x: left, y: foot - bh, w: bw, h: bh };
      cursorX = rtl() ? left - gap : left + bw + gap;
    });
    var binW = wide ? 86 : 64;
    var binH = wide ? 100 : 76;
    var binGap = 8;
    var binsRight = !rtl();
    var binStart = binsRight ? (w - margin - binW * 2 - binGap) : margin;
    var bins = {
      infectious: { x: binStart, y: foot - binH, w: binW, h: binH },
      general: { x: binStart + binW + binGap, w: binW, h: binH, y: foot - binH }
    };
    var bagLeft = Math.min(bags[1].x, bags[2].x, bags[3].x);
    var bagRight = Math.max(bags[1].x + bags[1].w, bags[2].x + bags[2].w, bags[3].x + bags[3].w);
    var binLeft = Math.min(bins.infectious.x, bins.general.x);
    var binRight = Math.max(bins.infectious.x + bins.infectious.w, bins.general.x + bins.general.w);
    var nudge = 0;
    if (bagLeft >= binRight && bagLeft - binRight < 14) nudge = 14 - (bagLeft - binRight);
    else if (bagRight <= binLeft && binLeft - bagRight < 14) nudge = -(14 - (binLeft - bagRight));
    if (nudge && bagLeft + nudge > 6 && bagRight + nudge < w - 6) {
      bags[1].x += nudge; bags[2].x += nudge; bags[3].x += nudge;
    }
    var n = titleCard.hidden ? slots() : 1;
    var itemH = wide ? Math.min(230, h * 0.32) : Math.min(176, h * 0.2);
    var itemW = itemH * 0.78;
    var total = n * itemW + (n - 1) * 18;
    var anchor = wide ? w * (rtl() ? 0.56 : 0.4) : w * 0.5;
    var left0 = anchor - total / 2;
    var unitFoot = wide ? foot - 4 : (foot - tall - 18);
    if (!wide && unitFoot - itemH < win.y + win.h - 36) {
      itemH = Math.max(120, unitFoot - (win.y + win.h - 30));
      itemW = itemH * 0.78;
    }
    var units = [];
    for (var i = 0; i < n; i++) {
      var fx = left0 + i * (itemW + 18) + itemW / 2;
      units.push({ footX: fx, footY: unitFoot, itemW: itemW, itemH: itemH, i: i });
    }
    var used = [null, null];
    units.forEach(function (u, i) {
      var c = titleCard.hidden ? cases[i] : null;
      var kind = 'empty';
      var size = 2;
      var lift = false;
      if (!titleCard.hidden) {
        kind = state.trees > 0 ? 'sealed' : 'jar';
        size = lastSize || 2;
      } else if (c && (c.phase === 'lift' || c.phase === 'bin')) {
        kind = c.used === 'jar' ? 'jar' : 'sealed';
        size = c.usedSize || 2;
        lift = c.phase === 'bin';
      } else if (c && (c.phase === 'seal' || c.phase === 'sprout')) {
        kind = 'fresh';
        size = c.size;
      }
      var bh = kind === 'jar' ? u.itemH : u.itemH * (SIZE_SCALE[size] || 1) * 0.92;
      var bw = kind === 'jar' ? bh * 0.8 : bh * bagAspect;
      var footY = u.footY - (lift ? Math.min(36, bh * 0.22) : 0);
      var footX = u.footX + (lift ? (rtl() ? -16 : 16) : 0);
      var dragging = drag && drag.moved && drag.kind === 'used' && drag.index === i;
      used[i] = {
        x: footX - bw / 2, y: footY - bh, w: bw, h: bh,
        kind: kind, size: size, lift: lift, hide: dragging, seal: 0
      };
    });
    return {
      win: win, wide: wide, foot: foot, bags: bags, bins: bins, units: units, used: used,
      table: wide
        ? { x: rtl() ? w * 0.62 : margin + 8, y: foot - 86, w: Math.min(300, w * 0.22), h: 78 }
        : { x: margin, y: win.y + win.h + 8, w: Math.max(70, units[0].footX - units[0].itemW / 2 - margin - 12), h: 58 }
    };
  }

  function drawOaks(c, win, now) {
    var list = spotInfo(state.trees).slice().sort(function (a, b) { return SPOTS[a.i].v - SPOTS[b.i].v; });
    c.save();
    c.beginPath();
    c.rect(win.x + 6, win.y + 6, win.w - 12, win.h - 12);
    c.clip();
    list.forEach(function (s) {
      var sp = SPOTS[s.i];
      var key = STAGE_KEY[s.stage];
      var im = img[key];
      if (!im) return;
      var persp = 0.62 + sp.v * 0.55;
      var hh = win.h * STAGE_H[s.stage] * sp.s * persp;
      var ww = hh * (im.width / im.height);
      var footX = win.x + win.w * sp.u;
      var footY = win.y + win.h * (sp.v + 0.02);
      var pop = popScale(pops[s.i], now);
      c.save();
      c.translate(footX, footY);
      c.scale(pop.x, pop.y);
      c.fillStyle = 'rgba(20,28,16,.32)';
      c.beginPath();
      c.ellipse(0, 3, ww * 0.22, Math.max(3, hh * 0.025), 0, 0, 7);
      c.fill();
      c.drawImage(im, -ww / 2, -hh, ww, hh);
      c.restore();
    });
    c.restore();
  }

  function drawWildlife(c, win, now) {
    c.save();
    c.beginPath();
    c.rect(win.x, win.y, win.w, win.h);
    c.clip();
    if (wildOn('birds')) {
      for (var i = 0; i < 3; i++) {
        var bx = win.x + ((now / 40 + i * 180) % (win.w + 40)) - 20;
        var by = win.y + win.h * (0.16 + i * 0.07);
        var flap = reduced() ? 0.4 : Math.sin(now / 180 + i) ;
        c.strokeStyle = 'rgba(30,28,26,.8)';
        c.lineWidth = 1.6;
        c.beginPath();
        c.moveTo(bx - 8, by);
        c.quadraticCurveTo(bx - 4, by - 6 * flap, bx, by);
        c.quadraticCurveTo(bx + 4, by - 6 * flap, bx + 8, by);
        c.stroke();
      }
    }
    if (wildOn('squirrel')) {
      var sx = win.x + win.w * 0.3;
      var sy = win.y + win.h * 0.62;
      c.fillStyle = '#6a4a32';
      c.beginPath();
      c.ellipse(sx, sy, 7, 4, 0, 0, 7);
      c.fill();
      c.beginPath();
      c.ellipse(sx + 6, sy - 3, 3.2, 3, 0, 0, 7);
      c.fill();
      c.strokeStyle = '#6a4a32';
      c.lineWidth = 2;
      c.beginPath();
      c.arc(sx - 2, sy - 6, 7, 0.4, 2.4);
      c.stroke();
    }
    if (wildOn('goat')) {
      var gx = win.x + win.w * 0.7;
      var gy = win.y + win.h * 0.8;
      c.fillStyle = '#d9d3c8';
      c.beginPath();
      c.ellipse(gx, gy, 16, 8, 0, 0, 7);
      c.fill();
      c.beginPath();
      c.ellipse(gx + 14, gy - 8, 6, 5, 0.4, 0, 7);
      c.fill();
      c.strokeStyle = '#6b645c';
      c.lineWidth = 1.5;
      c.beginPath();
      c.moveTo(gx + 16, gy - 12); c.lineTo(gx + 12, gy - 18);
      c.moveTo(gx + 18, gy - 11); c.lineTo(gx + 22, gy - 17);
      c.moveTo(gx - 8, gy + 6); c.lineTo(gx - 8, gy + 14);
      c.moveTo(gx + 6, gy + 6); c.lineTo(gx + 6, gy + 14);
      c.stroke();
    }
    if (wildOn('leopard')) {
      var lx = win.x + win.w * 0.9;
      var ly = win.y + win.h * 0.6;
      c.fillStyle = 'rgba(40,36,30,.35)';
      c.beginPath();
      c.ellipse(lx, ly + 18, 36, 9, 0, 0, 7);
      c.fill();
      c.fillStyle = '#c4a36a';
      c.beginPath();
      c.ellipse(lx, ly, 34, 12, -0.08, 0, 7);
      c.fill();
      c.beginPath();
      c.ellipse(lx + 28, ly - 8, 10, 8, 0.3, 0, 7);
      c.fill();
      c.strokeStyle = '#c4a36a';
      c.lineWidth = 4;
      c.beginPath();
      c.moveTo(lx - 30, ly);
      c.quadraticCurveTo(lx - 46, ly - 10, lx - 40, ly + 8);
      c.stroke();
      c.fillStyle = '#5a4630';
      [[-10, -2], [0, 3], [10, -1], [18, 4], [-20, 2], [6, -4]].forEach(function (p) {
        c.beginPath();
        c.ellipse(lx + p[0], ly + p[1], 2.4, 1.7, 0.4, 0, 7);
        c.fill();
      });
    }
    c.restore();
  }

  function drawStream(c, win, k) {
    if (k < 0.02) return;
    c.save();
    c.beginPath();
    c.rect(win.x, win.y, win.w, win.h);
    c.clip();
    c.globalAlpha = 0.45 * k;
    c.strokeStyle = 'rgba(214,236,232,.85)';
    c.lineWidth = Math.max(4, win.w * 0.012);
    c.lineCap = 'round';
    c.beginPath();
    var y = win.y + win.h * 0.74;
    c.moveTo(win.x - 10, y + 8);
    c.bezierCurveTo(win.x + win.w * 0.28, y - win.h * 0.05, win.x + win.w * 0.58, y + win.h * 0.06, win.x + win.w + 10, y);
    c.stroke();
    c.globalAlpha = 0.25 * k;
    c.lineWidth = Math.max(2, win.w * 0.005);
    c.beginPath();
    c.moveTo(win.x - 10, y + 14);
    c.bezierCurveTo(win.x + win.w * 0.3, y, win.x + win.w * 0.6, y + win.h * 0.05, win.x + win.w + 10, y + 6);
    c.stroke();
    c.restore();
  }

  function draw(now) {
    var dpr = Math.min(2, window.devicePixelRatio || 1);
    var w = canvas.clientWidth;
    var h = canvas.clientHeight;
    if (w < 2 || h < 2) return;
    var bw = Math.round(w * dpr);
    var bh = Math.round(h * dpr);
    if (canvas.width !== bw || canvas.height !== bh) {
      canvas.width = bw; canvas.height = bh;
      landKey = '';
    }
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    var pal = palette();
    var L = computeLayout(w, h);
    currentLayout = L;
    var mix = greenMix(state.trees);
    ctx.fillStyle = pal.w1;
    ctx.fillRect(0, 0, w, h);
    var wall = ctx.createLinearGradient(0, 0, 0, h);
    wall.addColorStop(0, pal.w0);
    wall.addColorStop(1, pal.w1);
    ctx.fillStyle = wall;
    ctx.fillRect(0, 0, w, h);

    var win = L.win;
    paintLand(win.w, win.h, dpr, mix);
    if (landCanvas) ctx.drawImage(landCanvas, win.x, win.y, win.w, win.h);
    drawStream(ctx, win, smooth(cfg.gameRules.streamSwaps - 1, cfg.gameRules.streamSwaps + 4, state.trees));
    var mistA = (1 - mix.green) * (1 - mix.mid * 0.45);
    if (mistA > 0.02) {
      ctx.save();
      ctx.beginPath();
      ctx.rect(win.x, win.y, win.w, win.h);
      ctx.clip();
      mist.forEach(function (m) {
        var mx = win.x + ((m.u + (reduced() ? 0 : now / 1000 / m.sp)) % 1) * win.w;
        var my = win.y + m.v * win.h;
        ctx.globalAlpha = m.a * mistA;
        ctx.fillStyle = '#f4f7f4';
        ctx.beginPath();
        ctx.ellipse(mx, my, m.r, m.r * 0.45, 0, 0, 7);
        ctx.fill();
      });
      ctx.restore();
    }
    drawOaks(ctx, win, now);
    drawWildlife(ctx, win, now);
    drawVignette(ctx, win, ghostAlpha(), now);

    ctx.save();
    roundRect(ctx, win.x - 8, win.y - 8, win.w + 16, win.h + 16, 16);
    ctx.strokeStyle = pal.frame;
    ctx.lineWidth = 12;
    ctx.stroke();
    ctx.restore();
    ctx.fillStyle = pal.sill;
    ctx.fillRect(win.x - 16, win.y + win.h - 4, win.w + 32, 16);

    ctx.fillStyle = pal.floor;
    ctx.fillRect(0, win.y + win.h + 6, w, h);
    var floorG = ctx.createLinearGradient(0, win.y + win.h, 0, h);
    floorG.addColorStop(0, 'rgba(255,255,255,.05)');
    floorG.addColorStop(1, 'rgba(0,0,0,.18)');
    ctx.fillStyle = floorG;
    ctx.fillRect(0, win.y + win.h + 6, w, h);

    var table = L.table;
    if (table.w > 40) {
      ctx.fillStyle = pal.metal;
      roundRect(ctx, table.x, table.y, table.w, table.h * 0.45, 8);
      ctx.fill();
      ctx.fillStyle = pal.cloth;
      roundRect(ctx, table.x + 6, table.y - 8, table.w - 12, table.h * 0.42, 10);
      ctx.fill();
      ctx.fillStyle = 'rgba(6,40,44,.15)';
      ctx.fillRect(table.x + table.w * 0.2, table.y + table.h * 0.45, 8, table.h * 0.5);
      ctx.fillRect(table.x + table.w * 0.75, table.y + table.h * 0.45, 8, table.h * 0.5);
      var monX = table.x + table.w * 0.55;
      var monY = table.y - 58;
      ctx.fillStyle = '#1a2426';
      roundRect(ctx, monX, monY, Math.min(92, table.w * 0.4), 52, 6);
      ctx.fill();
      ctx.fillStyle = '#0e7475';
      ctx.fillRect(monX + 6, monY + 8, Math.min(80, table.w * 0.34), 30);
      ctx.strokeStyle = '#d7f3f1';
      ctx.lineWidth = 1.4;
      ctx.beginPath();
      var pulse = reduced() ? 0 : Math.sin(now / 400);
      ctx.moveTo(monX + 10, monY + 24);
      ctx.lineTo(monX + 22, monY + 24);
      ctx.lineTo(monX + 28, monY + 16 - pulse * 2);
      ctx.lineTo(monX + 36, monY + 28);
      ctx.lineTo(monX + 48, monY + 22);
      ctx.stroke();
      ctx.fillStyle = pal.metal;
      ctx.fillRect(monX + 28, table.y - 10, 6, 12);
    }

    var lampSoft = 1 + (state.upgrades.lamp || 0) * 0.35;
    L.units.forEach(function (u) {
      var gx = u.footX;
      var gy = u.footY - u.itemH * 0.55;
      var rad = Math.max(u.itemH, 120) * lampSoft;
      var g = ctx.createRadialGradient(gx, gy, 8, gx, gy, rad);
      g.addColorStop(0, pal.glow);
      g.addColorStop(1, 'rgba(255,255,255,0)');
      ctx.fillStyle = g;
      ctx.beginPath();
      ctx.arc(gx, gy, rad, 0, 7);
      ctx.fill();
      ctx.strokeStyle = pal.metal;
      ctx.lineWidth = 4;
      ctx.beginPath();
      ctx.moveTo(gx, win.y + win.h + 10);
      ctx.lineTo(gx, gy - 20);
      ctx.stroke();
      ctx.fillStyle = '#e7f1ef';
      ctx.beginPath();
      ctx.ellipse(gx, gy - 18, 28, 8, 0, 0, 7);
      ctx.fill();
      ctx.fillStyle = 'rgba(232,248,246,.55)';
      ctx.beginPath();
      ctx.ellipse(gx, gy - 16, 16, 4, 0, 0, 7);
      ctx.fill();
    });

    var nurseX = L.units[0].footX - L.units[0].itemW * 0.95;
    if (nurseX < 36) nurseX = L.units[0].footX + L.units[0].itemW * 0.95;
    drawStaff(ctx, nurseX, L.units[0].footY + 4, L.wide ? 0.95 : 0.72, 'nurse', false);
    if (L.wide) {
      var porterX = L.bins.infectious.x - 48;
      if (porterX > L.units[0].footX + 80) drawStaff(ctx, porterX, L.foot + 4, 0.78, 'porter', false);
    }

    L.units.forEach(function (u, i) {
      ctx.fillStyle = pal.metal;
      roundRect(ctx, u.footX - 16, win.y + win.h + 18, 32, 46, 4);
      ctx.fill();
      ctx.strokeStyle = '#9aa8a6';
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.arc(u.footX, win.y + win.h + 36, 10, 0, 7);
      ctx.stroke();
      ctx.strokeStyle = pal.metal;
      ctx.lineWidth = 6;
      ctx.beginPath();
      ctx.moveTo(u.footX - u.itemW * 0.45, u.footY - 8);
      ctx.lineTo(u.footX + u.itemW * 0.45, u.footY - 8);
      ctx.moveTo(u.footX - u.itemW * 0.38, u.footY - 8);
      ctx.lineTo(u.footX - u.itemW * 0.2, u.footY - u.itemH * 0.35);
      ctx.moveTo(u.footX + u.itemW * 0.38, u.footY - 8);
      ctx.lineTo(u.footX + u.itemW * 0.2, u.footY - u.itemH * 0.35);
      ctx.stroke();
      var item = L.used[i];
      if (!item || item.hide || item.kind === 'empty') return;
      var shake = 0;
      if (item.kind === 'jar') {
        var tilt = item.lift ? 0.18 : 0;
        drawOldJar(ctx, item.x, item.y, item.w, item.h, tilt);
      } else if (item.kind === 'fresh') {
        var caze = cases[i];
        var k = 1;
        if (caze && caze.phase === 'seal') k = clamp((now - caze.t0) / sealMs(), 0, 1);
        drawSealProgress(ctx, item, k);
      } else {
        drawBag(ctx, item, 'sealed', 1);
      }
      if (shake) { /* reserved */ }
    });

    ctx.fillStyle = 'rgba(214,224,222,.9)';
    var trayLeft = Math.min(L.bags[1].x, L.bags[3].x) - 8;
    var trayRight = Math.max(L.bags[1].x + L.bags[1].w, L.bags[3].x + L.bags[3].w) + 8;
    var trayTop = L.foot - 10;
    roundRect(ctx, trayLeft, trayTop, trayRight - trayLeft, 12, 6);
    ctx.fill();
    [1, 2, 3].forEach(function (sz) {
      var r = Object.assign({}, L.bags[sz]);
      var sh = shakes[sz];
      if (sh && now - sh < 420) r.x += Math.sin((now - sh) / 40) * 5;
      var faded = drag && drag.moved && drag.kind === 'bag' && drag.size === sz;
      ctx.save();
      ctx.globalAlpha = faded ? 0.35 : 1;
      drawBag(ctx, r, 'fresh', 0);
      ctx.restore();
      var lab = formatNum(sz, 0);
      ctx.font = '800 13px Kalameh, Tahoma, sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      var lx = r.x + r.w / 2;
      var ly = r.y + r.h - 12;
      roundRect(ctx, lx - 13, ly - 9, 26, 18, 9);
      ctx.fillStyle = 'rgba(6,28,32,.78)';
      ctx.fill();
      ctx.fillStyle = '#f3fafa';
      ctx.fillText(lab, lx, ly);
    });

    var overInf = drag && drag.moved && drag.kind === 'used' && binAt(drag.px, drag.py) === 'infectious';
    var overGen = drag && drag.moved && drag.kind === 'used' && binAt(drag.px, drag.py) === 'general';
    drawBin(ctx, L.bins.infectious, 'infectious', overInf);
    drawBin(ctx, L.bins.general, 'general', overGen);

    if (!busy() && titleCard.hidden) {
      var p = primary();
      if (p && (p.phase === 'lift' || p.phase === 'bin' || p.phase === 'place')) {
        var idx = cases.indexOf(p);
        if (p.phase === 'lift' || p.phase === 'bin') drawRing(ctx, L.used[idx], now);
        if (p.phase === 'bin') drawRing(ctx, L.bins.infectious, now);
        if (p.phase === 'place') {
          drawRing(ctx, L.bags[p.size], now);
          var u = L.units[idx];
          drawRing(ctx, { x: u.footX - u.itemW / 2, y: u.footY - u.itemH, w: u.itemW, h: u.itemH }, now);
        }
      }
    }

    if (drag && drag.moved && !busy()) {
      if (drag.kind === 'bag') {
        var bh2 = (L.wide ? 148 : 90) * SIZE_SCALE[drag.size];
        var bw2 = bh2 * bagAspect;
        drawBag(ctx, { x: drag.px - bw2 / 2, y: drag.py - bh2 * 0.75, w: bw2, h: bh2 }, 'fresh', 0);
      } else if (drag.kind === 'used' && L.used[drag.index]) {
        var src = L.used[drag.index];
        var rr = { x: drag.px - src.w / 2, y: drag.py - src.h * 0.75, w: src.w, h: src.h };
        if (src.kind === 'jar') drawOldJar(ctx, rr.x, rr.y, rr.w, rr.h, 0.12);
        else drawBag(ctx, rr, 'sealed', 1);
      }
    }

    seedsFly.forEach(function (s) {
      var u = clamp((now - s.t0) / cfg.gameRules.seedFlightMs, 0, 1);
      var e = u * u * (3 - 2 * u);
      var x = s.x + (s.tx - s.x) * e;
      var y = s.y + (s.ty - s.y) * e - Math.sin(u * Math.PI) * 30;
      ctx.fillStyle = '#f3fafa';
      ctx.beginPath();
      ctx.arc(x, y, 4, 0, 7);
      ctx.fill();
    });

    placeChrome(L, now);
  }

  function placeChrome(L, now) {
    var show = titleCard.hidden && !busy();
    var p = primary();
    var teach = state.swaps < 2 || now < coachUntil;
    if (caseChip.hidden === false && L.units[0]) {
      var u = L.units[0];
      caseChip.style.left = u.footX + 'px';
      caseChip.style.top = (u.footY - u.itemH - 8) + 'px';
      caseChip.style.transform = 'translate(-50%, -100%)';
    }
    var target = null;
    if (show && p) {
      var idx = cases.indexOf(p);
      if ((p.phase === 'lift' || p.phase === 'bin') && L.used[idx]) {
        var r = p.phase === 'bin' ? L.bins.infectious : L.used[idx];
        if (p.phase === 'lift') r = L.used[idx];
        target = { x: r.x + r.w / 2, y: r.y + r.h * 0.15 };
      } else if (p.phase === 'place' && L.bags[p.size]) {
        var b = L.bags[p.size];
        target = { x: b.x + b.w / 2, y: b.y + 8 };
      }
    }
    if (target && teach && !drag) {
      handEl.hidden = false;
      handEl.style.left = target.x + 'px';
      handEl.style.top = (target.y + 18) + 'px';
    } else handEl.hidden = true;
    if (!hintEl.hidden) {
      if (target) {
        hintEl.style.left = clamp(target.x, 100, canvas.clientWidth - 100) + 'px';
        hintEl.style.top = clamp(target.y - 28, 64, canvas.clientHeight - 96) + 'px';
        hintEl.style.transform = 'translate(-50%, -100%)';
      } else {
        hintEl.style.left = (canvas.clientWidth / 2) + 'px';
        hintEl.style.top = '72px';
        hintEl.style.transform = 'translate(-50%, 0)';
      }
    }
    var seasonI = reduced() ? 0 : Math.floor((now / 1000 / 72) % 4);
    var seasonName = [t('seasonSpring'), t('seasonSummer'), t('seasonAutumn'), t('seasonWinter')][seasonI];
    var tod = (now / 1000 / 50) % 1;
    var todName = tod < 0.2 ? t('todDawn') : tod < 0.62 ? t('todDay') : tod < 0.8 ? t('todDusk') : t('todNight');
    var seasonEl = document.getElementById('season');
    var seasonText = todName + ' · ' + seasonName;
    if (seasonEl.textContent !== seasonText) seasonEl.textContent = seasonText;
  }

  function tickCases(now) {
    var changed = false;
    cases.forEach(function (c, i) {
      if (c && c.phase === 'seal' && !c.flying && now - c.t0 >= sealMs()) {
        c.flying = true;
        c.phase = 'sprout';
        c.t0 = now;
        audio.seal();
        ghostBurst = 1;
        var spotIndex = (state.trees + inFlight) % SPOTS.length;
        inFlight += 1;
        var from = currentLayout && currentLayout.units[i]
          ? { x: currentLayout.units[i].footX, y: currentLayout.units[i].footY - 40 }
          : { x: 0, y: 0 };
        launchSeed(from, spotIndex, function () {
          inFlight -= 1;
          commitCase(c);
          pops[spotIndex] = performance.now();
          audio.sprout();
          var idx = cases.indexOf(c);
          if (idx >= 0) cases[idx] = null;
          ensureCases();
          renderChrome();
          checkMilestones();
        });
        changed = true;
      }
    });
    for (var s = seedsFly.length - 1; s >= 0; s--) {
      if (!seedsFly[s].fired && now - seedsFly[s].t0 >= cfg.gameRules.seedFlightMs) {
        seedsFly[s].fired = true;
        var done = seedsFly[s].done;
        seedsFly.splice(s, 1);
        done();
      }
    }
    if (lockUntil && now > lockUntil) { lockUntil = 0; changed = true; }
    if (changed) renderChrome();
  }

  function frame(now) {
    var dt = Math.min(40, Math.max(0, now - last || 16));
    last = now;
    if (cfg && state) {
      if (ghostBurst > 0) ghostBurst = Math.max(0, ghostBurst - dt / 700);
      tickCases(now);
      var pnd = pendingSum();
      var target = {
        water: state.water + pnd.water,
        cost: state.cost + pnd.cost,
        hours: state.hours + pnd.hours,
        seeds: state.seeds + pnd.seeds
      };
      var k = reduced() ? 1 : 1 - Math.exp(-dt / 170);
      Object.keys(target).forEach(function (key) {
        shown[key] += (target[key] - shown[key]) * k;
        if (Math.abs(target[key] - shown[key]) < 0.02) shown[key] = target[key];
      });
      paintNumbers();
      draw(now);
    }
    frames++;
    if (now - fpsStamp > 1000) {
      fps = frames * 1000 / (now - fpsStamp);
      frames = 0;
      fpsStamp = now;
    }
    if (!document.hidden) raf = requestAnimationFrame(frame);
  }
  function startLoop() {
    if (document.hidden) return;
    last = performance.now();
    fpsStamp = last;
    if (!raf) raf = requestAnimationFrame(frame);
  }

  function bind() {
    document.getElementById('start').addEventListener('click', function () {
      var prefMute = false;
      try { prefMute = localStorage.getItem('abadis-oak-mute') === '1'; } catch (e) {}
      setSound(!prefMute, false);
      state.started = true;
      state.tutorialDone = true;
      state.lastSeen = Date.now();
      save();
      titleCard.hidden = true;
      track('game_start', { trees: state.trees });
      ensureCases();
      renderChrome();
      pumpMilestone();
    });
    document.getElementById('helpBtn').addEventListener('click', function () {
      if (!titleCard.hidden) return;
      coachUntil = performance.now() + 14000;
    });
    document.getElementById('themeBtn').addEventListener('click', function () {
      var cur = document.documentElement.dataset.theme || 'light';
      var next = THEMES[(THEMES.indexOf(cur) + 1) % 3];
      var btn = document.getElementById('themeBtn');
      btn.classList.remove('spin'); void btn.offsetWidth; btn.classList.add('spin');
      var apply = function () { applyTheme(next, true); };
      if (reduced() || !document.startViewTransition) { apply(); return; }
      var r = btn.getBoundingClientRect();
      var x = r.left + r.width / 2, y = r.top + r.height / 2;
      var end = Math.hypot(Math.max(x, innerWidth - x), Math.max(y, innerHeight - y));
      var vt = document.startViewTransition(apply);
      vt.ready.then(function () {
        document.documentElement.animate(
          { clipPath: ['circle(0px at ' + x + 'px ' + y + 'px)', 'circle(' + end + 'px at ' + x + 'px ' + y + 'px)'] },
          { duration: 750, easing: 'cubic-bezier(.65,0,.35,1)', pseudoElement: '::view-transition-new(root)' }
        );
      }).catch(function () {});
    });
    document.querySelectorAll('.lang-link').forEach(function (b) {
      b.addEventListener('click', function () { setLang(b.dataset.lang); });
    });
    document.getElementById('soundBtn').addEventListener('click', function () { setSound(!soundOn, true); });
    document.getElementById('shareBtn').addEventListener('click', doShare);
    document.getElementById('shopBtn').addEventListener('click', function () {
      clearDrag();
      shop.hidden = false;
      resetArm = false;
      paintShop();
      document.getElementById('resetBtn').textContent = t('reset');
      renderChrome();
    });
    document.getElementById('shopClose').addEventListener('click', function () { shop.hidden = true; renderChrome(); });
    shop.addEventListener('click', function (e) { if (e.target === shop) { shop.hidden = true; renderChrome(); } });
    document.querySelectorAll('[data-up]').forEach(function (b) {
      b.addEventListener('click', function () { buy(b.dataset.up); });
    });
    document.getElementById('resetBtn').addEventListener('click', function () {
      if (!resetArm) {
        resetArm = true;
        document.getElementById('resetBtn').textContent = t('resetArmed');
        return;
      }
      try { localStorage.removeItem(STORE); } catch (e) {}
      location.reload();
    });
    document.getElementById('msClose').addEventListener('click', closeMilestone);
    document.getElementById('msCalc').addEventListener('click', function () { track('cta_calculator_click'); });
    document.getElementById('msZagros').addEventListener('click', function () { track('cta_zagros_click'); });
    canvas.addEventListener('pointerdown', onDown);
    window.addEventListener('pointermove', onMove);
    window.addEventListener('pointerup', onUp);
    window.addEventListener('pointercancel', function (e) {
      if (drag && e.pointerId === drag.pid) drag = null;
    });
    window.addEventListener('blur', clearDrag);
    window.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        if (!shop.hidden) { shop.hidden = true; renderChrome(); }
        else if (!milestone.hidden) closeMilestone();
        clearDrag();
        return;
      }
      if (busy()) return;
      if (e.code === 'Digit1' || e.code === 'Digit2' || e.code === 'Digit3') {
        tryPlace(+e.code.slice(-1), null);
      } else if (e.code === 'KeyI' || e.code === 'KeyG') {
        var idx = -1;
        for (var i = 0; i < cases.length; i++) if (cases[i] && cases[i].phase === 'bin') { idx = i; break; }
        if (idx >= 0) tryBin(idx, e.code === 'KeyI' ? 'infectious' : 'general');
      } else if (e.code === 'Enter' || e.code === 'Space') {
        var p = primary();
        if (p && p.phase === 'lift') {
          e.preventDefault();
          tryLift(cases.indexOf(p));
        }
      }
    });
    document.addEventListener('visibilitychange', function () {
      if (document.hidden) {
        if (raf) cancelAnimationFrame(raf);
        raf = 0;
        audio.suspend();
        clearDrag();
        if (state && state.started) { state.lastSeen = Date.now(); save(); }
      } else {
        var n = state && state.started ? applyNight() : 0;
        if (n) toast(t('night', { n: formatNum(n, 0) }));
        audio.resume();
        startLoop();
      }
    });
    window.addEventListener('pagehide', function () {
      if (state && state.started) { state.lastSeen = Date.now(); save(); }
    });
    setInterval(function () {
      if (!state || !state.started || document.hidden) return;
      state.lastSeen = Date.now();
      save();
    }, 20000);
  }

  function doShare() {
    var url = new URL('./', location.href).href;
    var litres = formatNum(Math.round(state.water + pendingSum().water), 0);
    var text = t('shareText', { litres: litres });
    var finish = function (method) {
      if (method === 'copy') toast(t('copied'));
      track('share', { method: method });
    };
    if (navigator.share) {
      navigator.share({ title: t('title'), text: text, url: url }).then(function () {
        finish('web-share');
      }).catch(function (err) {
        if (err && err.name === 'AbortError') { track('share', { method: 'abort' }); return; }
        copyText(url).then(function (ok) { finish(ok ? 'copy' : 'failed'); });
      });
    } else copyText(url).then(function (ok) { finish(ok ? 'copy' : 'failed'); });
  }
  function copyText(url) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      return navigator.clipboard.writeText(url).then(function () { return true; }, function () { return fallbackCopy(url); });
    }
    return Promise.resolve(fallbackCopy(url));
  }
  function fallbackCopy(url) {
    var ta = document.createElement('textarea');
    ta.value = url;
    ta.setAttribute('readonly', '');
    ta.style.position = 'fixed';
    ta.style.left = '-999px';
    document.body.appendChild(ta);
    ta.select();
    var ok = false;
    try { ok = document.execCommand('copy'); } catch (e) {}
    ta.remove();
    return ok;
  }

  function loadImages() {
    Object.keys(SRC).forEach(function (k) {
      var im = new Image();
      im.onload = function () {
        img[k] = im;
        landKey = '';
        if (k === 'bag') bakeBag();
      };
      im.src = SRC[k];
    });
  }

  window.__OAK = {
    get fps() { return fps; },
    get state() { return state; },
    get events() { return events; },
    get per() { return per; },
    applyNight: function () { return applyNight(); },
    layout: function () { return currentLayout; },
    phase: function () { var p = primary(); return p ? p.phase : ''; },
    wanted: function () { var p = primary(); return p ? p.size : 0; }
  };

  function boot() {
    Promise.all([fetch('i18n.json'), fetch('savings.json')]).then(function (res) {
      if (!res[0].ok || !res[1].ok) throw new Error('load');
      return Promise.all([res[0].json(), res[1].json()]);
    }).then(function (pair) {
      i18n = pair[0];
      cfg = pair[1];
      per = derive(cfg);
      if (!isFinite(per.water) || !isFinite(per.cost) || !isFinite(per.hours)) throw new Error('formula');
      state = loadState();
      var nightN = applyNight();
      shown.water = state.water;
      shown.cost = state.cost;
      shown.hours = state.hours;
      shown.seeds = state.seeds;
      var stored = 'fa';
      try { stored = localStorage.getItem('abadis-oak-lang') || 'fa'; } catch (e) {}
      var fromHtml = document.documentElement.lang.indexOf('en') === 0 ? 'en' : document.documentElement.lang.indexOf('ar') === 0 ? 'ar' : 'fa';
      setLang(stored || fromHtml);
      if (nightN) {
        var line = document.getElementById('nightLine');
        line.hidden = false;
        line.textContent = t('night', { n: formatNum(nightN, 0) });
      }
      checkMilestones();
      loadImages();
      bind();
      startLoop();
    }).catch(function () {
      document.getElementById('lead').textContent = 'Config failed to load.';
      document.getElementById('start').hidden = true;
    });
  }
  boot();
})();
