/* One Bag, One Oak. Savings come only from savings.json (the dial-practical formula). */
(function () {
  'use strict';

  var STORE = 'abadis-oak-v1';
  var THEMES = ['light', 'dark', 'noir'];
  var SPOTS = [
    { u: 0.18, v: 0.80, s: 1.05 }, { u: 0.33, v: 0.73, s: 0.9 },
    { u: 0.47, v: 0.82, s: 1.08 }, { u: 0.60, v: 0.70, s: 0.84 },
    { u: 0.72, v: 0.78, s: 0.94 }, { u: 0.84, v: 0.67, s: 0.78 },
    { u: 0.27, v: 0.88, s: 1.12 }, { u: 0.66, v: 0.88, s: 1.06 }
  ];
  var STAGE_H = [0.30, 0.40, 0.50, 0.62];
  var SRC = {
    dry: '../zagros-names/shared/img/hero/bg-dry-1280.webp',
    mid: '../zagros-names/shared/img/hero/bg-mid-1280.webp',
    green: '../zagros-names/shared/img/hero/bg-green-1280.webp',
    sprout: '../zagros-names/shared/img/hero/sprout.webp',
    sapling: '../zagros-names/shared/img/hero/sapling.webp',
    young: '../zagros-names/shared/img/hero/young-oak.webp',
    grown: '../zagros-names/shared/img/hero/grown-oak.webp'
  };

  var i18n, cfg, per, state, lang = 'fa';
  var cases = [null, null];
  var caseSeq = 0;
  var shown = { water: 0, cost: 0, hours: 0, seeds: 0 };
  var events = [];
  var msQueue = [];
  var lockUntil = 0;
  var hint = { key: 'hintIdle', vars: {} };
  var tutStep = 0;
  var tutReplay = false;
  var soundOn = false;
  var resetArm = false;
  var pops = {};
  var ghostK = 0;
  var staffX = null;
  var inFlight = 0;
  var currentLayout = null;
  var landCanvas = null;
  var landKey = '';
  var img = {};
  var raf = 0;
  var last = 0;
  var frames = 0;
  var fps = 0;
  var fpsStamp = 0;
  var drag = null;
  var suppressClick = false;
  var lastCoin = -1;
  var reduceMQ = window.matchMedia('(prefers-reduced-motion: reduce)');

  var app = document.getElementById('app');
  var stage = document.getElementById('stage');
  var canvas = document.getElementById('view');
  var ctx = canvas.getContext('2d', { alpha: false });
  var holdEls = [document.getElementById('hold0'), document.getElementById('hold1')];
  var titleCard = document.getElementById('titleCard');
  var tutorial = document.getElementById('tutorial');
  var milestone = document.getElementById('milestone');
  var shop = document.getElementById('shop');
  var hintEl = document.getElementById('hint');
  var caseChip = document.getElementById('caseChip');
  var live = document.getElementById('live');
  var toastEl = document.getElementById('toast');
  var bagBtns = Array.prototype.slice.call(document.querySelectorAll('.bag'));
  var binBtns = Array.prototype.slice.call(document.querySelectorAll('.bin'));

  var mist = [];
  for (var mi = 0; mi < 14; mi++) mist.push({ u: Math.random(), v: 0.42 + Math.random() * 0.36, r: 18 + Math.random() * 46, sp: 4 + Math.random() * 10, a: 0.04 + Math.random() * 0.07 });
  var pollen = [];
  for (var pi = 0; pi < 10; pi++) pollen.push({ u: Math.random(), v: 0.2 + Math.random() * 0.7, sp: 6 + Math.random() * 12, r: 1.2 + Math.random() * 1.6 });
  var drips = [];
  for (var di = 0; di < 5; di++) drips.push({ t: Math.random() });

  var ghostEl = document.createElement('img');
  ghostEl.className = 'ghost-drag';
  ghostEl.alt = '';
  ghostEl.draggable = false;
  ghostEl.src = '../zagros-names/shared/img/hero/canister.webp';
  ghostEl.hidden = true;
  document.body.appendChild(ghostEl);

  function reduced() { return reduceMQ.matches; }
  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }
  function smooth(a, b, x) {
    var t = clamp((x - a) / (b - a || 1), 0, 1);
    return t * t * (3 - 2 * t);
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
      seen: [], tutorialDone: false, started: false, lastSeen: 0
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
  function grantSwaps(n) {
    state.water += per.water * n;
    state.cost += per.cost * n;
    state.hours += per.hours * n;
    state.seeds += cfg.gameRules.seedsPerCleanSwap * n;
    state.trees += n;
    state.swaps += n;
    save();
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
    track('swap', { size: c.size, bonus: !!c.clean, litres: litres, swaps: state.swaps });
    live.textContent = t('liveSwap', { litres: formatNum(litres, 0) });
  }

  function slots() { return state.upgrades.second ? 2 : 1; }
  function makeCase() {
    var types = cfg.gameRules.surgeryTypes;
    var type = types[state.cursor % types.length];
    state.cursor += 1;
    save();
    return { id: ++caseSeq, type: type.id, size: type.sizeL, phase: 'pick', clean: true, t0: 0, reward: null };
  }
  function ensureCases() {
    if (!state.upgrades.second) cases[1] = null;
    var n = slots();
    for (var i = 0; i < n; i++) if (!cases[i]) cases[i] = makeCase();
  }
  function primary() {
    return cases.filter(function (c) { return c && c.phase === 'pick'; })[0]
      || cases.filter(function (c) { return c && c.phase === 'bin'; })[0]
      || cases.filter(function (c) { return c && (c.phase === 'seal' || c.phase === 'sprout'); })[0]
      || null;
  }
  function busy() {
    return !titleCard.hidden || !tutorial.hidden || !milestone.hidden || !shop.hidden;
  }
  function setHint(key, vars) {
    hint = { key: key, vars: vars || {} };
    hintEl.textContent = t(key, hint.vars);
  }
  function syncHint() {
    if (performance.now() < lockUntil) return;
    var p = primary();
    if (!titleCard.hidden) { hintEl.textContent = ''; return; }
    if (!p) setHint('hintIdle');
    else if (p.phase === 'pick') setHint('hintPick', { n: formatNum(p.size, 0) });
    else if (p.phase === 'bin') setHint('hintBin');
    else if (p.phase === 'seal') setHint('hintSeal');
    else setHint('hintSprout');
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
    btn.textContent = soundOn ? '♪' : '◌';
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
    landKey = '';
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
    document.getElementById('shareBtn').textContent = '↗';
    document.getElementById('helpBtn').setAttribute('aria-label', t('help'));
    bagBtns.forEach(function (b) {
      var label = t('bag', { n: formatNum(+b.dataset.size, 0) });
      b.querySelector('span').textContent = label;
      b.setAttribute('aria-label', label);
    });
    document.getElementById('binInf').textContent = t('binInfectious');
    document.getElementById('binGen').textContent = t('binGeneral');
    document.getElementById('labWater').textContent = t('water');
    document.getElementById('labStaff').textContent = t('staff');
    document.getElementById('labChem').textContent = t('chemicals');
    document.getElementById('chemBadge').textContent = t('chemicalsMark');
    document.getElementById('pillChem').title = t('chemicalsNote');
    document.getElementById('pillChem').setAttribute('aria-label', t('chemicalsNote'));
    document.getElementById('labMoney').textContent = t('money');
    document.getElementById('shopTitle').textContent = t('shopTitle');
    document.getElementById('upSecond').textContent = t('upSecond');
    document.getElementById('upSealer').textContent = t('upSealer');
    document.getElementById('upLamp').textContent = t('upLamp');
    document.getElementById('upWild').textContent = t('upWild');
    document.getElementById('shopClose').textContent = t('close');
    document.getElementById('resetBtn').textContent = resetArm ? t('resetArmed') : t('reset');
    document.getElementById('tutSkip').textContent = t('skip');
    document.getElementById('msKicker').textContent = t('msKicker');
    document.getElementById('msLitreLabel').textContent = t('msLitre');
    document.getElementById('msChem').textContent = t('msChem');
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
    hintEl.textContent = hint.key ? t(hint.key, hint.vars) : '';
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
    if (!tutorial.hidden) paintTut();
  }

  function renderChrome() {
    var p = primary();
    app.dataset.phase = titleCard.hidden ? (p ? p.phase : 'idle') : 'title';
    app.dataset.size = p && p.phase === 'pick' ? String(p.size) : '';
    var picking = !!(p && p.phase === 'pick' && !busy());
    var binning = !!(p && p.phase === 'bin' && !busy());
    bagBtns.forEach(function (b) { b.disabled = !picking; });
    binBtns.forEach(function (b) { b.disabled = !binning; });
    if (p) caseChip.textContent = t('caseChip', { name: t(typeKey(p.type)), n: formatNum(p.size, 0) });
    else caseChip.textContent = '';
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
    var minutes = shown.hours * 60;
    if (minutes < 60) {
      document.getElementById('numStaff').textContent = formatNum(minutes, 1);
      document.getElementById('unitStaff').textContent = t('minUnit');
    } else {
      document.getElementById('numStaff').textContent = formatNum(shown.hours, 1);
      document.getElementById('unitStaff').textContent = t('hourUnit');
    }
    document.getElementById('numMoney').textContent = formatNum(cost, 0);
    document.getElementById('subMoney').textContent = cost >= 1e6 ? moneyText(cost) : t('toman');
    if (cost !== lastCoin) {
      if (lastCoin >= 0) {
        var coin = document.getElementById('coin');
        coin.classList.remove('pop'); void coin.offsetWidth; coin.classList.add('pop');
      }
      lastCoin = cost;
    }
    document.getElementById('shopBtn').textContent = t('shop') + ' · ' + formatNum(Math.floor(shown.seeds), 0);
  }

  function paintTut() {
    var keys = [['tut1t', 'tut1b'], ['tut2t', 'tut2b'], ['tut3t', 'tut3b']];
    document.getElementById('tutTitle').textContent = t(keys[tutStep][0]);
    document.getElementById('tutBody').textContent = t(keys[tutStep][1]);
    document.getElementById('tutNext').textContent = tutStep === 2 ? t('lets') : t('next');
    Array.prototype.forEach.call(document.querySelectorAll('#dots i'), function (d, i) {
      d.classList.toggle('on', i === tutStep);
    });
  }
  function openTutorial(replay) {
    tutReplay = !!replay;
    tutStep = 0;
    tutorial.hidden = false;
    paintTut();
    ensureCases();
    renderChrome();
    document.getElementById('tutNext').focus();
  }
  function finishTut() {
    tutorial.hidden = true;
    if (!tutReplay) {
      state.tutorialDone = true;
      state.started = true;
      save();
      beginPlay();
    } else {
      renderChrome();
      pumpMilestone();
    }
  }
  function beginPlay() {
    ensureCases();
    renderChrome();
    pumpMilestone();
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
    if (!titleCard.hidden || !tutorial.hidden || !milestone.hidden) return;
    openMilestone(msQueue.shift());
  }
  function openMilestone(mark) {
    milestone.dataset.mark = String(mark);
    document.getElementById('msLitres').textContent = formatNum(Math.round(state.water), 0);
    document.getElementById('msAlso').textContent = t('msAlso', {
      hours: staffText(state.hours),
      money: moneyText(state.cost)
    });
    var box = document.getElementById('msTags');
    box.textContent = '';
    spotInfo(state.trees).forEach(function (s) {
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
      live.textContent = t('liveWrong');
      var bad = document.querySelector('.bag[data-size="' + picked + '"]');
      var good = document.querySelector('.bag[data-size="' + wanted + '"]');
      if (bad) { bad.classList.add('shake'); setTimeout(function () { bad.classList.remove('shake'); }, 450); }
      if (good) { good.classList.add('need'); setTimeout(function () { good.classList.remove('need'); }, 1300); }
    } else setHint('hintWrongBin');
    audio.softNo();
  }
  function tryPlace(size, i) {
    if (busy() || performance.now() < lockUntil) return;
    var idx = i;
    if (idx == null || !cases[idx] || cases[idx].phase !== 'pick') idx = cases.findIndex(function (c) { return c && c.phase === 'pick'; });
    if (idx < 0) return;
    var c = cases[idx];
    if (size !== c.size) { mistake('size', c.size, size); return; }
    beginSeal(c, idx);
  }
  function beginSeal(c, i) {
    c.phase = 'seal';
    c.t0 = performance.now();
    c.clean = true;
    c.reward = {
      water: per.water, cost: per.cost, hours: per.hours,
      seeds: cfg.gameRules.seedsPerCleanSwap, trees: 1, committed: false
    };
    audio.click();
    if (!reduced() && navigator.vibrate) { try { navigator.vibrate(12); } catch (e) {} }
    flyMotes(holdEls[i]);
    renderChrome();
  }
  function tryBin(i, kind) {
    var c = cases[i];
    if (busy() || performance.now() < lockUntil || !c || c.phase !== 'bin') return;
    if (kind !== cfg.gameRules.correctBin) {
      c.clean = false;
      mistake('bin');
      return;
    }
    if (c.clean) c.reward.seeds += cfg.gameRules.bonusSeedsForCorrectBin;
    c.phase = 'sprout';
    c.t0 = performance.now();
    renderChrome();
    var spotIndex = (state.trees + inFlight) % SPOTS.length;
    inFlight += 1;
    launchSeed(holdEls[i], spotIndex, function () {
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
  }
  function sealMs() {
    return Math.max(280, cfg.gameRules.sealMs - state.upgrades.sealer * cfg.gameRules.sealMsSavedPerLevel);
  }

  function flyMotes(fromEl) {
    if (reduced()) return;
    var targets = [
      [document.getElementById('pillWater'), ''],
      [document.getElementById('pillStaff'), 'staff'],
      [document.getElementById('pillChem'), 'chem'],
      [document.getElementById('pillMoney'), 'money']
    ];
    var a = fromEl.getBoundingClientRect();
    var sx = a.left + a.width / 2;
    var sy = a.top + a.height / 2;
    targets.forEach(function (pair, i) {
      var dot = document.createElement('i');
      dot.className = 'mote ' + pair[1];
      dot.style.left = sx + 'px';
      dot.style.top = sy + 'px';
      document.body.appendChild(dot);
      var b = pair[0].getBoundingClientRect();
      setTimeout(function () {
        dot.style.transform = 'translate(' + (b.left + b.width / 2 - sx) + 'px,' + (b.top + b.height / 2 - sy) + 'px) scale(.4)';
        dot.style.opacity = '0.1';
      }, 40 + i * 80);
      setTimeout(function () { dot.remove(); }, 980);
    });
  }
  function spotClient(spotIndex) {
    var rect = canvas.getBoundingClientRect();
    var sp = SPOTS[spotIndex];
    if (!currentLayout) return { x: rect.left + rect.width * 0.5, y: rect.top + rect.height * 0.4 };
    return {
      x: rect.left + currentLayout.win.x + currentLayout.win.w * sp.u,
      y: rect.top + currentLayout.win.y + currentLayout.win.h * sp.v
    };
  }
  function launchSeed(fromEl, spotIndex, done) {
    if (reduced()) { done(); return; }
    var dot = document.createElement('i');
    dot.className = 'seed';
    var a = fromEl.getBoundingClientRect();
    var sx = a.left + a.width / 2;
    var sy = a.top + a.height / 2;
    var dest = spotClient(spotIndex);
    dot.style.left = sx + 'px';
    dot.style.top = sy + 'px';
    document.body.appendChild(dot);
    requestAnimationFrame(function () {
      dot.style.transform = 'translate(' + (dest.x - sx) + 'px,' + (dest.y - sy) + 'px) scale(.35)';
      dot.style.opacity = '0.15';
    });
    setTimeout(function () { dot.remove(); done(); }, cfg.gameRules.seedFlightMs);
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

  function startDrag(e, kind, payload) {
    if (e.button != null && e.button !== 0) return;
    drag = { kind: kind, payload: payload, x: e.clientX, y: e.clientY, pid: e.pointerId, moved: false };
    try { e.currentTarget.setPointerCapture(e.pointerId); } catch (err) {}
  }
  function onMove(e) {
    if (!drag || e.pointerId !== drag.pid) return;
    if (Math.hypot(e.clientX - drag.x, e.clientY - drag.y) > 8) {
      drag.moved = true;
      ghostEl.hidden = false;
      ghostEl.style.left = e.clientX + 'px';
      ghostEl.style.top = e.clientY + 'px';
      holdEls.forEach(function (el) { el.classList.remove('hot'); });
      binBtns.forEach(function (el) { el.classList.remove('hot'); });
      if (drag.kind === 'bag') {
        var h = holdAt(e.clientX, e.clientY);
        if (h) h.classList.add('hot');
      } else {
        var b = binAt(e.clientX, e.clientY);
        if (b) b.classList.add('hot');
      }
    }
  }
  function onUp(e) {
    if (!drag || e.pointerId !== drag.pid) return;
    var d = drag;
    drag = null;
    ghostEl.hidden = true;
    holdEls.forEach(function (el) { el.classList.remove('hot'); });
    binBtns.forEach(function (el) { el.classList.remove('hot'); });
    if (!d.moved) return;
    suppressClick = true;
    setTimeout(function () { suppressClick = false; }, 0);
    if (d.kind === 'bag') {
      var h = holdAt(e.clientX, e.clientY);
      if (h) tryPlace(d.payload, +h.dataset.i);
    } else {
      var b = binAt(e.clientX, e.clientY);
      if (b) tryBin(d.payload, b.dataset.bin);
    }
  }
  function holdAt(x, y) {
    for (var i = 0; i < holdEls.length; i++) {
      var el = holdEls[i];
      if (el.hidden) continue;
      var r = el.getBoundingClientRect();
      if (x >= r.left && x <= r.right && y >= r.top && y <= r.bottom) return el;
    }
    return null;
  }
  function binAt(x, y) {
    for (var i = 0; i < binBtns.length; i++) {
      var r = binBtns[i].getBoundingClientRect();
      if (x >= r.left && x <= r.right && y >= r.top && y <= r.bottom) return binBtns[i];
    }
    return null;
  }

  function palette() {
    var th = document.documentElement.dataset.theme;
    if (th === 'noir') return {
      w0: '#16122a', w1: '#0c0a16', grid: 'rgba(196,181,253,.07)', glow: 'rgba(167,139,250,.2)',
      cloth: '#2a2144', frame: '#ebe6f8', glass: 'rgba(241,240,255,.28)', fluid: 'rgba(186,176,214,.5)',
      person: 'rgba(236,230,255,.9)', metal: '#d4c8f5', tag: '#6d28d9'
    };
    if (th === 'dark') return {
      w0: '#0a2c30', w1: '#051618', grid: 'rgba(232,243,243,.05)', glow: 'rgba(95,208,209,.16)',
      cloth: '#10383c', frame: '#d5e6e2', glass: 'rgba(232,243,243,.22)', fluid: 'rgba(150,186,190,.42)',
      person: 'rgba(220,236,236,.88)', metal: '#b7dedc', tag: '#087673'
    };
    return {
      w0: '#0e474b', w1: '#083236', grid: 'rgba(255,255,255,.05)', glow: 'rgba(95,208,209,.22)',
      cloth: '#166066', frame: '#eef6f4', glass: 'rgba(236,246,246,.4)', fluid: 'rgba(176,204,206,.55)',
      person: 'rgba(240,248,248,.94)', metal: '#e4f2f0', tag: '#066163'
    };
  }
  function roundRect(c, x, y, w, h, r) {
    var rr = Math.min(r, w / 2, h / 2);
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
    if (img.dry) drawCover(c, img.dry, 0, 0, w, h, 0.5, 0.58);
    else { c.fillStyle = '#c9bfb2'; c.fillRect(0, 0, w, h); }
    if (img.mid && mix.mid > 0.01) { c.globalAlpha = mix.mid; drawCover(c, img.mid, 0, 0, w, h, 0.5, 0.58); }
    if (img.green && mix.green > 0.01) { c.globalAlpha = mix.green; drawCover(c, img.green, 0, 0, w, h, 0.5, 0.58); }
    c.globalAlpha = 1;
  }
  function spotInfo(total) {
    var n = SPOTS.length;
    var out = [];
    var shown = Math.min(total, n);
    for (var i = 0; i < shown; i++) {
      var layers = 1 + Math.floor(Math.max(0, total - 1 - i) / n);
      out.push({ i: i, stage: Math.min(3, layers - 1), label: i + 1 + (layers - 1) * n });
    }
    return out;
  }
  function popScale(t0, now) {
    if (!t0 || reduced()) return { x: 1, y: 1 };
    var t = (now - t0) / 720;
    if (t >= 1) return { x: 1, y: 1 };
    if (t < 0.35) { var k = t / 0.35; return { x: 1 - 0.16 * k, y: 1 + 0.24 * k }; }
    if (t < 0.7) { var k2 = (t - 0.35) / 0.35; return { x: 0.84 + 0.24 * k2, y: 1.24 - 0.36 * k2 }; }
    var k3 = (t - 0.7) / 0.3;
    return { x: 1.08 - 0.08 * k3, y: 0.88 + 0.12 * k3 };
  }
  function wildOn(name) {
    var need = cfg.gameRules.wildlifeAtTrees[name];
    if (need == null) return false;
    var earlier = (state.upgrades.wildlife || 0) * cfg.gameRules.upgrades.wildlife.treesEarlier;
    return state.trees + earlier >= need;
  }
  function drawPerson(c, x, y, s, color, lean) {
    c.save();
    c.translate(x, y);
    c.rotate(lean || 0);
    c.scale(s, s);
    c.fillStyle = color;
    c.beginPath(); c.arc(0, -52, 7.2, 0, Math.PI * 2); c.fill();
    roundRect(c, -10, -42, 20, 28, 7); c.fill();
    roundRect(c, -9, -14, 7, 16, 3); c.fill();
    roundRect(c, 2, -14, 7, 16, 3); c.fill();
    c.restore();
  }
  function drawJar(c, r, alpha, pal) {
    if (alpha < 0.02) return;
    var x = r.x + r.w * 0.28;
    var y = r.y + r.h * 0.18;
    var w = r.w * 0.44;
    var h = r.h * 0.62;
    c.save();
    c.globalAlpha = alpha;
    c.fillStyle = pal.glass;
    roundRect(c, x, y, w, h, 8); c.fill();
    c.strokeStyle = 'rgba(255,255,255,.55)';
    c.lineWidth = 1.5;
    c.stroke();
    c.fillStyle = pal.fluid;
    roundRect(c, x + 3, y + h * 0.38, w - 6, h * 0.58, 6); c.fill();
    c.beginPath();
    c.strokeStyle = pal.metal;
    c.lineWidth = 2;
    c.arc(x + w + 2, y + h * 0.35, 8, -1.2, 1.2);
    c.stroke();
    c.restore();
  }
  function drawWildlife(c, win, now) {
    if (wildOn('birds')) {
      for (var i = 0; i < 3; i++) {
        var u = ((now / 9000) + i * 0.33) % 1;
        var x = win.x + win.w * (0.12 + u * 0.7);
        var y = win.y + win.h * (0.18 + i * 0.06);
        var flap = 0.4 + Math.sin(now / 280 + i) * 0.6;
        c.strokeStyle = 'rgba(36, 44, 40, .72)';
        c.lineWidth = 1.3;
        c.beginPath();
        c.moveTo(x - 8, y);
        c.quadraticCurveTo(x - 3, y - 5 * flap, x, y);
        c.quadraticCurveTo(x + 3, y - 5 * flap, x + 8, y);
        c.stroke();
      }
    }
    if (wildOn('squirrel')) {
      var sx = win.x + win.w * 0.62;
      var sy = win.y + win.h * 0.74;
      c.fillStyle = 'rgba(62, 42, 28, .8)';
      c.beginPath(); c.ellipse(sx, sy, 5, 3.2, 0, 0, Math.PI * 2); c.fill();
      c.beginPath(); c.arc(sx + 4, sy - 2, 2.1, 0, Math.PI * 2); c.fill();
      c.beginPath();
      c.strokeStyle = 'rgba(62, 42, 28, .8)';
      c.lineWidth = 1.4;
      c.moveTo(sx - 4, sy);
      c.quadraticCurveTo(sx - 8, sy - 8, sx - 3, sy - 7);
      c.stroke();
    }
    if (wildOn('goat')) {
      var gx = win.x + win.w * 0.8;
      var gy = win.y + win.h * 0.64;
      c.fillStyle = 'rgba(48, 44, 38, .78)';
      c.beginPath(); c.ellipse(gx, gy, 9, 4.5, 0, 0, Math.PI * 2); c.fill();
      c.beginPath(); c.ellipse(gx + 8, gy - 3, 3.2, 2.6, 0, 0, Math.PI * 2); c.fill();
      c.strokeStyle = 'rgba(48, 44, 38, .78)';
      c.lineWidth = 1.2;
      c.beginPath();
      c.moveTo(gx + 9, gy - 5); c.quadraticCurveTo(gx + 12, gy - 12, gx + 8, gy - 8);
      c.moveTo(gx + 7, gy - 5); c.quadraticCurveTo(gx + 6, gy - 12, gx + 4, gy - 7);
      c.moveTo(gx - 4, gy + 3); c.lineTo(gx - 4, gy + 9);
      c.moveTo(gx + 2, gy + 3); c.lineTo(gx + 2, gy + 9);
      c.stroke();
    }
    if (wildOn('leopard')) {
      var lx = win.x + win.w * 0.88;
      var ly = win.y + win.h * 0.58;
      c.fillStyle = 'rgba(42, 36, 28, .84)';
      c.beginPath(); c.ellipse(lx, ly, 16, 5.5, -0.1, 0, Math.PI * 2); c.fill();
      c.beginPath(); c.ellipse(lx + 14, ly - 3, 5, 3.6, 0.2, 0, Math.PI * 2); c.fill();
      c.strokeStyle = 'rgba(42, 36, 28, .84)';
      c.lineWidth = 1.5;
      c.beginPath();
      c.moveTo(lx - 14, ly);
      c.quadraticCurveTo(lx - 24, ly - 8, lx - 28, ly - 1);
      c.stroke();
      c.fillStyle = 'rgba(232, 220, 196, .35)';
      [[-4, -1], [2, 1], [8, -1]].forEach(function (p) {
        c.beginPath(); c.arc(lx + p[0], ly + p[1], 1.1, 0, Math.PI * 2); c.fill();
      });
    }
  }

  function computeLayout(w, h) {
    var wide = w / h > 1.05;
    var two = !!(state && state.upgrades && state.upgrades.second);
    var win, table, wash, holds;
    if (!wide) {
      win = { x: w * 0.035, y: h * 0.01, w: w * 0.93, h: h * 0.58 };
      table = { x: w * 0.22, y: win.y + win.h - 4, w: w * 0.56, h: Math.max(10, h * 0.045) };
      wash = { x: w * 0.02, y: h * 0.68, w: w * 0.2, h: h * 0.28 };
      var hw = two ? w * 0.26 : w * 0.3;
      var hh = h * 0.3;
      var hy = h * 0.60;
      holds = two
        ? [{ x: w * 0.24, y: hy, w: hw, h: hh }, { x: w * 0.56, y: hy, w: hw, h: hh }]
        : [{ x: w * 0.4, y: hy, w: hw, h: hh }, { x: 0, y: 0, w: 0, h: 0 }];
    } else {
      win = { x: w * 0.035, y: h * 0.03, w: w * 0.93, h: h * 0.58 };
      table = { x: w * 0.18, y: win.y + win.h - 6, w: w * 0.5, h: h * 0.07 };
      wash = { x: w * 0.025, y: h * 0.68, w: w * 0.18, h: h * 0.26 };
      var hw2 = two ? w * 0.2 : w * 0.22;
      var hh2 = h * 0.32;
      holds = two
        ? [{ x: w * 0.28, y: h * 0.64, w: hw2, h: hh2 }, { x: w * 0.52, y: h * 0.64, w: hw2, h: hh2 }]
        : [{ x: w * 0.4, y: h * 0.63, w: hw2, h: hh2 }, { x: 0, y: 0, w: 0, h: 0 }];
    }
    return { wide: wide, win: win, table: table, wash: wash, holds: holds };
  }

  function draw(now) {
    var w = stage.clientWidth;
    var h = stage.clientHeight;
    if (w < 2 || h < 2) return;
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    var bw = Math.round(w * dpr);
    var bh = Math.round(h * dpr);
    if (canvas.width !== bw || canvas.height !== bh) { canvas.width = bw; canvas.height = bh; landKey = ''; }
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    var L = computeLayout(w, h);
    currentLayout = L;
    var pal = palette();
    var retire = clamp(state.trees / cfg.gameRules.washRetireTrees, 0, 1);
    var mix = greenMix(state.trees);

    var g = ctx.createLinearGradient(0, 0, 0, h);
    g.addColorStop(0, pal.w0); g.addColorStop(1, pal.w1);
    ctx.fillStyle = g; ctx.fillRect(0, 0, w, h);
    ctx.strokeStyle = pal.grid; ctx.lineWidth = 1;
    for (var gx = 0; gx < w; gx += 28) { ctx.beginPath(); ctx.moveTo(gx, 0); ctx.lineTo(gx, h); ctx.stroke(); }
    for (var gy = 0; gy < h; gy += 28) { ctx.beginPath(); ctx.moveTo(0, gy); ctx.lineTo(w, gy); ctx.stroke(); }
    var glow = ctx.createRadialGradient(w * 0.5, L.win.y + L.win.h, 20, w * 0.5, L.win.y, L.win.h);
    glow.addColorStop(0, pal.glow); glow.addColorStop(1, 'rgba(0,0,0,0)');
    ctx.fillStyle = glow; ctx.fillRect(0, 0, w, h);

    var lamp = 0.22 + (state.upgrades.lamp || 0) * 0.16;
    var lx = w * 0.55, ly = 8;
    var cone = ctx.createRadialGradient(lx, ly, 8, lx, h * 0.45, w * 0.55);
    cone.addColorStop(0, 'rgba(255,255,255,' + lamp + ')');
    cone.addColorStop(1, 'rgba(255,255,255,0)');
    ctx.fillStyle = cone; ctx.fillRect(0, 0, w, h);

    var win = L.win;
    paintLand(win.w, win.h, dpr, mix);
    ctx.save();
    roundRect(ctx, win.x, win.y, win.w, win.h, 18);
    ctx.clip();
    if (landCanvas) ctx.drawImage(landCanvas, win.x, win.y, win.w, win.h);

    var stream = clamp(shown.water / (per.water * cfg.gameRules.streamSwaps), 0, 1);
    if (stream > 0.02) {
      ctx.save();
      ctx.globalAlpha = 0.35 + stream * 0.5;
      ctx.strokeStyle = 'rgba(210, 236, 236, .95)';
      ctx.lineWidth = 1.4 + stream * 6;
      ctx.lineCap = 'round';
      ctx.setLineDash([7, 12]);
      ctx.lineDashOffset = -now / 45;
      ctx.beginPath();
      var x0 = win.x + win.w * 0.47;
      var y0 = win.y + win.h * 0.56;
      ctx.moveTo(x0, y0);
      ctx.bezierCurveTo(x0 + win.w * 0.06, y0 + win.h * 0.14, x0 - win.w * 0.1, y0 + win.h * 0.24, x0 + win.w * 0.03, win.y + win.h);
      ctx.stroke();
      ctx.restore();
    }

    var trees = spotInfo(state.trees);
    trees.forEach(function (tr) {
      var sp = SPOTS[tr.i];
      var names = ['sprout', 'sapling', 'young', 'grown'];
      var im = img[names[tr.stage]];
      var x = win.x + win.w * sp.u;
      var y = win.y + win.h * sp.v;
      var th = win.h * STAGE_H[tr.stage] * sp.s;
      var sc = popScale(pops[tr.i], now);
      ctx.save();
      ctx.translate(x, y);
      ctx.scale(sc.x, sc.y);
      ctx.fillStyle = 'rgba(40, 36, 24, .28)';
      ctx.beginPath(); ctx.ellipse(0, 0, th * 0.16, th * 0.035, 0, 0, Math.PI * 2); ctx.fill();
      if (im) {
        var dw = th * (im.width / im.height);
        ctx.drawImage(im, -dw / 2, -th, dw, th);
      }
      ctx.restore();
      ctx.save();
      ctx.font = '700 11px Kalameh, Tahoma';
      var label = formatNum(tr.label, 0);
      var tw = Math.max(16, ctx.measureText(label).width + 8);
      ctx.fillStyle = 'rgba(74, 56, 32, .8)';
      ctx.fillRect(x - 0.6, y - 18, 1.4, 16);
      roundRect(ctx, x - tw / 2, y - 34, tw, 16, 4);
      ctx.fillStyle = 'rgba(243,250,250,.92)';
      ctx.fill();
      ctx.fillStyle = pal.tag;
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.direction = 'ltr';
      ctx.fillText(label, x, y - 26);
      ctx.restore();
    });

    drawWildlife(ctx, win, now);

    var mistA = 0.9 * (1 - mix.green);
    if (!reduced() && mistA > 0.05) {
      mist.forEach(function (m) {
        m.u += m.sp * 0.000012;
        if (m.u > 1.15) m.u = -0.1;
        ctx.fillStyle = 'rgba(255,255,255,' + (m.a * mistA) + ')';
        ctx.beginPath();
        ctx.ellipse(win.x + win.w * m.u, win.y + win.h * m.v, m.r, m.r * 0.45, 0, 0, Math.PI * 2);
        ctx.fill();
      });
    }
    if (!reduced() && mix.green > 0.35) {
      pollen.forEach(function (p) {
        p.v -= p.sp * 0.00002;
        if (p.v < 0) { p.v = 1; p.u = Math.random(); }
        ctx.fillStyle = 'rgba(255,255,255,.55)';
        ctx.beginPath();
        ctx.arc(win.x + win.w * p.u, win.y + win.h * p.v, p.r, 0, Math.PI * 2);
        ctx.fill();
      });
    }

    var tod = reduced() ? 0.35 : (now / 1000 / 56) % 1;
    var warm = tod < 0.22 ? 0.16 : tod > 0.62 && tod < 0.8 ? 0.18 : 0.03;
    var night = tod > 0.78 ? 0.34 : tod > 0.62 ? 0.12 : tod < 0.12 ? 0.16 : 0;
    if (warm > 0.02) {
      var wg = ctx.createLinearGradient(0, win.y, 0, win.y + win.h);
      wg.addColorStop(0, 'rgba(255, 214, 196,' + warm + ')');
      wg.addColorStop(1, 'rgba(255, 214, 196,0)');
      ctx.fillStyle = wg; ctx.fillRect(win.x, win.y, win.w, win.h);
    }
    if (night > 0.02) {
      ctx.fillStyle = 'rgba(8, 22, 40,' + night + ')';
      ctx.fillRect(win.x, win.y, win.w, win.h);
    }
    var vig = ctx.createRadialGradient(win.x + win.w / 2, win.y + win.h / 2, win.w * 0.2, win.x + win.w / 2, win.y + win.h / 2, win.w * 0.65);
    vig.addColorStop(0, 'rgba(0,0,0,0)');
    vig.addColorStop(1, 'rgba(0,0,0,.18)');
    ctx.fillStyle = vig; ctx.fillRect(win.x, win.y, win.w, win.h);
    ctx.restore();

    ctx.lineWidth = 10; ctx.strokeStyle = pal.frame;
    roundRect(ctx, win.x, win.y, win.w, win.h, 18); ctx.stroke();
    ctx.lineWidth = 2; ctx.strokeStyle = 'rgba(255,255,255,.35)';
    roundRect(ctx, win.x + 6, win.y + 6, win.w - 12, win.h - 12, 12); ctx.stroke();

    var spill = ctx.createLinearGradient(0, win.y + win.h, 0, win.y + win.h + h * 0.18);
    spill.addColorStop(0, 'rgba(255,255,255,.1)');
    spill.addColorStop(1, 'rgba(255,255,255,0)');
    ctx.fillStyle = spill;
    ctx.fillRect(win.x, win.y + win.h, win.w, h * 0.18);

    roundRect(ctx, L.table.x, L.table.y, L.table.w, L.table.h, 12);
    ctx.fillStyle = pal.cloth; ctx.fill();

    var wash = L.wash;
    ctx.save();
    ctx.globalAlpha = 1 - retire * 0.45;
    roundRect(ctx, wash.x, wash.y + wash.h * 0.35, wash.w, wash.h * 0.45, 8);
    ctx.fillStyle = 'rgba(255,255,255,.08)'; ctx.fill();
    ctx.strokeStyle = 'rgba(255,255,255,.3)'; ctx.lineWidth = 1.5; ctx.stroke();
    ctx.strokeStyle = pal.metal; ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(wash.x + wash.w * 0.35, wash.y + wash.h * 0.15);
    ctx.lineTo(wash.x + wash.w * 0.35, wash.y + wash.h * 0.38);
    ctx.lineTo(wash.x + wash.w * 0.55, wash.y + wash.h * 0.38);
    ctx.stroke();
    for (var b = 0; b < 4; b++) {
      ctx.globalAlpha = (1 - retire) * 0.85;
      roundRect(ctx, wash.x + 6 + b * (wash.w * 0.2), wash.y + wash.h * 0.08, wash.w * 0.12, wash.h * 0.22, 3);
      ctx.fillStyle = 'rgba(220,232,230,.55)'; ctx.fill();
    }
    ctx.restore();
    if (retire < 0.85 && !reduced()) {
      drips.forEach(function (d) {
        d.t += 0.008 * (1 - retire);
        var fall = d.t % 1;
        ctx.globalAlpha = (1 - fall) * (1 - retire);
        ctx.fillStyle = 'rgba(200,230,232,.8)';
        ctx.fillRect(wash.x + wash.w * 0.55, wash.y + wash.h * 0.4 + fall * wash.h * 0.35, 1.5, 5);
        ctx.globalAlpha = 1;
      });
    }
    if (retire > 0.92) {
      ctx.font = '700 11px Kalameh, Tahoma';
      ctx.fillStyle = pal.metal;
      ctx.textAlign = 'center';
      ctx.fillText(t('retired'), wash.x + wash.w / 2, wash.y + wash.h * 0.22);
    }

    var from = wash.x + wash.w * 0.7;
    var to = L.table.x + L.table.w * 0.18;
    var target = from + (to - from) * smooth(0.45, 1, retire);
    if (staffX == null) staffX = target;
    staffX += (target - staffX) * (reduced() ? 1 : 0.04);
    var lean = (1 - retire) * -0.08;
    drawPerson(ctx, staffX, wash.y + wash.h * 0.78, Math.min(w, h) / 520, pal.person, lean);

    var wantGhost = cases.some(function (c) { return c && c.phase === 'pick'; }) ? 1 : 0;
    ghostK += (wantGhost - ghostK) * (reduced() ? 1 : 0.08);
    if (ghostK > 0.03) {
      ctx.save();
      ctx.globalAlpha = ghostK * 0.55;
      var gx0 = wash.x + wash.w + 8;
      var gy0 = wash.y + 6;
      drawPerson(ctx, gx0, gy0 + 36, Math.min(w, h) / 640, pal.person, 0.05);
      ctx.strokeStyle = pal.metal;
      ctx.lineWidth = 1.4;
      ctx.beginPath();
      ctx.arc(gx0 + 28, gy0 + 8, 10, 0, Math.PI * 2);
      ctx.moveTo(gx0 + 28, gy0 + 2); ctx.lineTo(gx0 + 28, gy0 + 10);
      ctx.moveTo(gx0 + 28, gy0 + 8); ctx.lineTo(gx0 + 33, gy0 + 8);
      ctx.stroke();
      roundRect(ctx, gx0 + 46, gy0 + 10, 26, 14, 3);
      ctx.fillStyle = 'rgba(255,255,255,.35)'; ctx.fill();
      ctx.restore();
    }

    for (var hi = 0; hi < slots(); hi++) {
      var hr = L.holds[hi];
      var ccase = cases[hi];
      ctx.strokeStyle = 'rgba(232,243,243,.35)';
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.moveTo(hr.x + hr.w * 0.5, hr.y + hr.h * 0.72);
      ctx.lineTo(hr.x + hr.w * 0.5, hr.y + hr.h);
      ctx.stroke();
      if (ccase && (ccase.phase === 'pick' || ccase.phase === 'seal')) {
        var a = ccase.phase === 'seal' ? 1 - clamp((now - ccase.t0) / sealMs(), 0, 1) : 1;
        drawJar(ctx, hr, a, pal);
      }
    }

    var seasonI = reduced() ? 0 : Math.floor((now / 1000 / 72) % 4);
    var seasonName = [t('seasonSpring'), t('seasonSummer'), t('seasonAutumn'), t('seasonWinter')][seasonI];
    var todName = tod < 0.2 ? t('todDawn') : tod < 0.62 ? t('todDay') : tod < 0.8 ? t('todDusk') : t('todNight');
    var seasonEl = document.getElementById('season');
    var seasonText = todName + ' · ' + seasonName;
    if (seasonEl.textContent !== seasonText) seasonEl.textContent = seasonText;

    for (var si = 0; si < 2; si++) {
      var el = holdEls[si];
      var r = L.holds[si];
      var on = si < slots() && titleCard.hidden;
      el.hidden = !on;
      if (!on) continue;
      el.style.left = r.x + 'px';
      el.style.top = r.y + 'px';
      el.style.width = r.w + 'px';
      el.style.height = r.h + 'px';
      var phase = cases[si] ? cases[si].phase : '';
      el.classList.toggle('phase-pick', phase === 'pick');
      el.classList.toggle('phase-seal', phase === 'seal');
      el.classList.toggle('phase-bin', phase === 'bin');
      el.classList.toggle('phase-sprout', phase === 'sprout');
    }
  }

  function tickCases(now) {
    var changed = false;
    cases.forEach(function (c) {
      if (c && c.phase === 'seal' && now - c.t0 >= sealMs()) {
        c.phase = 'bin';
        changed = true;
        audio.seal();
      }
    });
    if (lockUntil && now > lockUntil) { lockUntil = 0; changed = true; }
    if (changed) renderChrome();
  }
  function frame(now) {
    var dt = Math.min(40, Math.max(0, now - last || 16));
    last = now;
    if (cfg && state) {
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
        if (Math.abs(target[key] - shown[key]) < 0.015) shown[key] = target[key];
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
      state.lastSeen = Date.now();
      save();
      titleCard.hidden = true;
      track('game_start', { trees: state.trees });
      if (!state.tutorialDone) openTutorial(false);
      else beginPlay();
    });
    document.getElementById('tutNext').addEventListener('click', function () {
      if (tutStep < 2) { tutStep += 1; paintTut(); }
      else finishTut();
    });
    document.getElementById('tutSkip').addEventListener('click', finishTut);
    document.getElementById('helpBtn').addEventListener('click', function () {
      if (!titleCard.hidden) return;
      openTutorial(true);
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

    bagBtns.forEach(function (b) {
      b.addEventListener('pointerdown', function (e) { if (!b.disabled) startDrag(e, 'bag', +b.dataset.size); });
      b.addEventListener('click', function () {
        if (suppressClick) { suppressClick = false; return; }
        tryPlace(+b.dataset.size, null);
      });
    });
    binBtns.forEach(function (b) {
      b.addEventListener('click', function () {
        if (suppressClick) { suppressClick = false; return; }
        var idx = cases.findIndex(function (c) { return c && c.phase === 'bin'; });
        if (idx >= 0) tryBin(idx, b.dataset.bin);
      });
    });
    holdEls.forEach(function (el) {
      el.addEventListener('pointerdown', function (e) {
        var i = +el.dataset.i;
        if (!cases[i] || cases[i].phase !== 'bin') return;
        startDrag(e, 'used', i);
      });
    });
    window.addEventListener('pointermove', onMove);
    window.addEventListener('pointerup', onUp);
    window.addEventListener('pointercancel', onUp);
    window.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        if (!shop.hidden) { shop.hidden = true; renderChrome(); }
        else if (!milestone.hidden) closeMilestone();
        return;
      }
      if (busy()) return;
      if (e.key === '1' || e.key === '2' || e.key === '3') tryPlace(+e.key, null);
    });
    document.addEventListener('visibilitychange', function () {
      if (document.hidden) {
        if (raf) cancelAnimationFrame(raf);
        raf = 0;
        audio.suspend();
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
      }).catch(function (e) {
        if (e && e.name === 'AbortError') { track('share', { method: 'abort' }); return; }
        copyText(url).then(function (ok) { finish(ok ? 'copy' : 'failed'); });
      });
    } else {
      copyText(url).then(function (ok) { finish(ok ? 'copy' : 'failed'); });
    }
  }
  function copyText(url) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      return navigator.clipboard.writeText(url).then(function () { return true; }, function () { return fallbackCopy(url); });
    }
    return Promise.resolve(fallbackCopy(url));
  }
  function fallbackCopy(url) {
    var ta = document.createElement('textarea');
    ta.value = url; ta.setAttribute('readonly', '');
    ta.style.position = 'fixed'; ta.style.left = '-999px';
    document.body.appendChild(ta); ta.select();
    var ok = false;
    try { ok = document.execCommand('copy'); } catch (e) {}
    ta.remove();
    return ok;
  }

  function loadImages() {
    Object.keys(SRC).forEach(function (k) {
      var im = new Image();
      im.onload = function () { img[k] = im; landKey = ''; };
      im.src = SRC[k];
    });
  }

  window.__OAK = {
    get fps() { return fps; },
    get state() { return state; },
    get events() { return events; },
    get per() { return per; },
    applyNight: function () { return applyNight(); }
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
