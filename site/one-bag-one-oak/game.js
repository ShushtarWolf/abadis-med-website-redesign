/* One Bag, One Oak. Savings come only from savings.json (the dial-practical formula). */
(function () {
  'use strict';

  var STORE = 'abadis-oak-v1';
  var THEMES = ['light', 'dark', 'noir'];
  var SIZE_SCALE = { 1: 0.78, 2: 1, 3: 1.22 };
  var SPOTS = makeSpots();
  var STAGE_KEY = ['young', 'young', 'grown', 'grown'];
  var STAGE_H = [0.30, 0.42, 0.56, 0.70];
  var SRC = {};

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
  var img = {};
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
      softNo: function () { blip(170, 0.12, 'triangle', 0.05); },
      milestone: function () { [523.25, 659.25, 783.99, 1046.5].forEach(function (f, i) { setTimeout(function () { blip(f, 0.5, 'sine', 0.05); }, i * 120); }); }
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
    var tl = document.getElementById('themeLabel');
    if (tl) tl.textContent = t(names[nxt]);
    R.roomKey = '';
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
    document.getElementById('helpLabel').textContent = t('help');
    document.getElementById('shareLabel').textContent = t('share');
    document.getElementById('menuBtn').setAttribute('aria-label', lang === 'en' ? 'Menu' : lang === 'ar' ? 'القائمة' : 'منو');
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
    celebrate(performance.now());
    audio.milestone();
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

  /* ===== Renderer: one illustrated style, vector only, static layers cached ===== */
  var R = { room: null, roomKey: '', land: null, landKey: '', frame: null, sprites: {}, grain: null, ripples: [], bursts: [], leaves: [], msGlow: 0, retireT: 0, wasRetired: null };
  var BAG_H = { 1: 0.70, 2: 0.86, 3: 1.0 };
  var BAG_AR = { 1: 0.86, 2: 0.78, 3: 0.74 };
  function lerp(a, b, k) { return a + (b - a) * k; }
  function hexRgb(h) { var n = parseInt(h.slice(1), 16); return [n >> 16 & 255, n >> 8 & 255, n & 255]; }
  function mixC(a, b, k, al) {
    var A = hexRgb(a), B = hexRgb(b);
    var r = Math.round(lerp(A[0], B[0], k)), g = Math.round(lerp(A[1], B[1], k)), bl = Math.round(lerp(A[2], B[2], k));
    return al == null ? 'rgb(' + r + ',' + g + ',' + bl + ')' : 'rgba(' + r + ',' + g + ',' + bl + ',' + al + ')';
  }
  function rng(seed) { var s = seed % 2147483647; if (s <= 0) s += 2147483646; return function () { s = s * 16807 % 2147483647; return (s - 1) / 2147483646; }; }
  function mk(w, h, dpr) {
    var cv = document.createElement('canvas');
    cv.width = Math.max(1, Math.ceil(w * dpr)); cv.height = Math.max(1, Math.ceil(h * dpr));
    var x = cv.getContext('2d'); x.setTransform(dpr, 0, 0, dpr, 0, 0);
    return { c: cv, x: x, w: w, h: h };
  }
  function roundRect(c, x, y, w, h, r) {
    var rr = Math.min(r, Math.abs(w) / 2, Math.abs(h) / 2);
    c.beginPath(); c.moveTo(x + rr, y);
    c.arcTo(x + w, y, x + w, y + h, rr); c.arcTo(x + w, y + h, x, y + h, rr);
    c.arcTo(x, y + h, x, y, rr); c.arcTo(x, y, x + w, y, rr); c.closePath();
  }
  function lg(c, x0, y0, x1, y1, stops) { var g = c.createLinearGradient(x0, y0, x1, y1); stops.forEach(function (s) { g.addColorStop(s[0], s[1]); }); return g; }
  function rg(c, x, y, r0, r1, stops) { var g = c.createRadialGradient(x, y, r0, x, y, r1); stops.forEach(function (s) { g.addColorStop(s[0], s[1]); }); return g; }
  function FF() { return lang === 'en' ? '"KalamehLatinDigits", Kalameh, Tahoma, sans-serif' : 'Kalameh, Tahoma, sans-serif'; }
  var shadowBlob = null;
  function softShadow(c, x, y, rx, ry, a) {
    if (rx <= 0 || ry <= 0) return;
    if (!shadowBlob) {
      shadowBlob = document.createElement('canvas'); shadowBlob.width = shadowBlob.height = 64;
      var sx = shadowBlob.getContext('2d');
      var gg = sx.createRadialGradient(32, 32, 0, 32, 32, 32); gg.addColorStop(0, 'rgba(8,36,40,1)'); gg.addColorStop(1, 'rgba(8,36,40,0)');
      sx.fillStyle = gg; sx.fillRect(0, 0, 64, 64);
    }
    var ga = c.globalAlpha; c.globalAlpha = ga * a;
    c.drawImage(shadowBlob, x - rx, y - ry, rx * 2, ry * 2);
    c.globalAlpha = ga;
  }
  function grain() {
    if (R.grain) return R.grain;
    var g = document.createElement('canvas'); g.width = g.height = 128;
    var x = g.getContext('2d'); var d = x.createImageData(128, 128); var r = rng(7);
    for (var i = 0; i < d.data.length; i += 4) { var v = r() * 255; d.data[i] = d.data[i + 1] = d.data[i + 2] = v; d.data[i + 3] = 22; }
    x.putImageData(d, 0, 0); R.grain = g; return g;
  }
  function addGrain(c, w, h) { c.save(); c.globalCompositeOperation = 'overlay'; c.fillStyle = c.createPattern(grain(), 'repeat'); c.fillRect(0, 0, w, h); c.restore(); }
  function palette() {
    var th = document.documentElement.dataset.theme;
    if (th === 'dark' || th === 'noir') return {
      dark: true, wallT: '#16393c', wallB: '#0e2a2d', seam: 'rgba(160,220,220,.05)', dado: '#0b4d54', ceil: '#1c4245',
      floorF: '#0f3134', floorN: '#071a1c', steel: '#9fb3b4', steelD: '#5d7476', steelL: '#d3e2e2', drape: '#1f7c78', drapeD: '#0f4e4c', drapeL: '#3d9a95',
      frame: '#d9e6e5', frameD: '#93a9a8', reveal: '#0b2326', shaft: 'rgba(255,240,215,.05)'
    };
    return {
      dark: false, wallT: '#eef7f6', wallB: '#d8eae8', seam: 'rgba(6,97,99,.07)', dado: '#0d5962', ceil: '#f6fbfb',
      floorF: '#a9c7c5', floorN: '#6f9c9a', steel: '#c9d7d7', steelD: '#8aa0a1', steelL: '#f1f7f7', drape: '#2e8c86', drapeD: '#1b615d', drapeL: '#5aaba5',
      frame: '#fbfdfd', frameD: '#b7c8c7', reveal: '#c4dad8', shaft: 'rgba(255,246,226,.16)'
    };
  }
  /* ---------- layout ---------- */
  function computeLayout(w, h) {
    var wide = w >= 820 && w > h;
    var L = { w: w, h: h, wide: wide };
    var flip = rtl();
    var top = 56;
    if (wide) {
      var ww = Math.min(w * 0.5, (h * 0.5) * 1.75);
      L.win = { x: (w - ww) / 2, y: top + 10, w: ww, h: h * 0.5 };
      L.floorY = h * 0.67;
      L.table = { cx: w * 0.57, top: L.floorY - 20, w: Math.min(460, w * 0.32) };
      L.lamp = { x: L.win.x + L.win.w * 0.1, y: L.win.y + L.win.h * 0.16, r: Math.min(92, h * 0.11) };
      L.monitor = { x: w * 0.87 - Math.min(150, w * 0.11) / 2, y: top + 14, w: Math.min(150, w * 0.11), h: Math.min(96, w * 0.07) };
      L.cabinet = { x: w * 0.035, y: top + 22, w: w * 0.17, h: h * 0.3 };
      L.sink = { x: w * 0.035, top: L.floorY - h * 0.15, w: w * 0.17, bottom: L.floorY + 12 };
      L.unitBase = { x: w * 0.87, regY: top + 14 + Math.min(96, w * 0.07) + 130, footY: L.floorY + 10, itemH: 0 };
      L.trayBox = { x: w * 0.15, foot: h - 130, w: Math.min(380, w * 0.27) };
      L.binBox = { x: w * 0.6, foot: h - 64, bw: Math.min(112, w * 0.08), bh: Math.min(146, w * 0.105), gap: 26 };
      L.washerHome = { x: L.sink.x + L.sink.w * 0.62, y: L.floorY + 26, s: h * 0.3 };
      L.nurse = { x: L.table.cx - L.table.w * 0.6, y: L.floorY + 44, s: h * 0.28 };
    } else {
      L.win = { x: w * 0.06, y: top + 6, w: w * 0.88, h: Math.min(h * 0.37, w * 0.95) };
      L.floorY = L.win.y + L.win.h + h * 0.24;
      L.table = { cx: w * 0.44, top: L.win.y + L.win.h + h * 0.12, w: w * 0.5 };
      L.lamp = { x: w * 0.36, y: L.win.y + L.win.h + 10, r: Math.min(46, w * 0.12) };
      L.monitor = { x: w * 0.2, y: L.win.y + L.win.h + 22, w: w * 0.21, h: w * 0.14, stand: true };
      L.cabinet = null;
      L.sink = { x: -4, top: L.floorY - h * 0.105, w: w * 0.24, bottom: L.floorY + 8 };
      L.unitBase = { x: w * 0.83, regY: L.win.y + L.win.h + 40, footY: L.floorY + 6, itemH: 0 };
      L.trayBox = { x: w * 0.03, foot: h - 120, w: w * 0.5 };
      L.binBox = { x: w * 0.6, foot: h - 66, bw: w * 0.165, bh: w * 0.215, gap: w * 0.04 };
      L.washerHome = { x: L.sink.x + L.sink.w * 0.6, y: L.floorY + 14, s: h * 0.2 };
      L.nurse = { x: L.table.cx + L.table.w * 0.42, y: L.floorY + 26, s: h * 0.21 };
    }
    var n = titleCard.hidden ? slots() : 1;
    var maxBag0 = wide ? Math.min(176, h * 0.21) : Math.min(98, h * 0.112);
    var itemH = maxBag0 * 1.06, itemW = itemH * 0.72;
    var units = [];
    for (var i = 0; i < n; i++) {
      var fx = L.unitBase.x - (n - 1 - i) * (itemW + 22) * 1.12;
      units.push({ footX: fx, footY: L.unitBase.footY, itemW: itemW, itemH: itemH, regY: L.unitBase.regY, i: i });
    }
    var tb = L.trayBox, maxBag = maxBag0;
    var bags = {}, totalW = 0, gap = wide ? 18 : 10;
    [1, 2, 3].forEach(function (s) { totalW += maxBag * BAG_H[s] * BAG_AR[s]; });
    totalW += gap * 2;
    var bx = tb.x + (tb.w - totalW) / 2;
    [1, 2, 3].forEach(function (s) {
      var bh = maxBag * BAG_H[s], bw = bh * BAG_AR[s];
      bags[s] = { x: bx, y: tb.foot - bh, w: bw, h: bh };
      bx += bw + gap;
    });
    var bb = L.binBox;
    var bins = {
      infectious: { x: bb.x, y: bb.foot - bb.bh, w: bb.bw, h: bb.bh },
      general: { x: bb.x + bb.bw + bb.gap, y: bb.foot - bb.bh, w: bb.bw, h: bb.bh }
    };
    var used = [null, null];
    units.forEach(function (u, i) {
      var c = titleCard.hidden ? cases[i] : null;
      var kind = 'empty', size = 2, lift = false;
      if (!titleCard.hidden) { kind = state.trees > 0 ? 'sealed' : 'jar'; size = lastSize || 2; }
      else if (c && (c.phase === 'lift' || c.phase === 'bin')) { kind = c.used === 'jar' ? 'jar' : 'sealed'; size = c.usedSize || 2; lift = c.phase === 'bin'; }
      else if (c && (c.phase === 'seal' || c.phase === 'sprout')) { kind = 'fresh'; size = c.size; }
      var bh = kind === 'jar' ? u.itemH : maxBag0 * BAG_H[size];
      var bw = kind === 'jar' ? bh * 0.72 : bh * BAG_AR[size];
      var footY = u.footY - (lift ? Math.min(30, bh * 0.2) : 0);
      var dragging = drag && drag.moved && drag.kind === 'used' && drag.index === i;
      used[i] = { x: u.footX - bw / 2, y: footY - bh, w: bw, h: bh, kind: kind, size: size, lift: lift, hide: dragging };
    });
    L.units = units; L.used = used; L.bags = bags; L.bins = bins; L.foot = tb.foot;
    if (flip) {
      var fx2 = function (r) { if (r) r.x = w - r.x - (r.w || 0); };
      [L.win, L.monitor, L.cabinet, L.trayBox].forEach(fx2);
      L.sink.x = w - L.sink.x - L.sink.w;
      L.table.cx = w - L.table.cx; L.lamp.x = w - L.lamp.x;
      L.washerHome.x = w - L.washerHome.x; L.nurse.x = w - L.nurse.x;
      units.forEach(function (u) { u.footX = w - u.footX; });
      used.forEach(fx2);
      [1, 2, 3].forEach(function (s) { fx2(bags[s]); });
      fx2(bins.infectious); fx2(bins.general);
    }
    L.flip = flip;
    return L;
  }

  /* ---------- landscape (window view) ---------- */
  function ridgeY(x, w, h) {
    var u = x / w;
    var peak = Math.exp(-Math.pow((u - 0.52) / 0.2, 2)) * 0.2 + Math.exp(-Math.pow((u - 0.3) / 0.16, 2)) * 0.1 + Math.exp(-Math.pow((u - 0.78) / 0.14, 2)) * 0.11;
    var j = Math.sin(u * 37) * 0.008 + Math.sin(u * 91 + 1.3) * 0.005 + Math.sin(u * 13 + 2) * 0.01;
    return h * (0.5 - peak - j);
  }
  function paintLandscape(c, w, h, g) {
    c.fillStyle = lg(c, 0, 0, 0, h * 0.6, [[0, mixC('#e9e1d3', '#bcd9e4', g)], [0.7, mixC('#efe8dc', '#e3efee', g)], [1, mixC('#ece2cf', '#eef3e6', g)]]);
    c.fillRect(0, 0, w, h);
    c.fillStyle = rg(c, w * 0.74, h * 0.16, 0, h * 0.5, [[0, 'rgba(255,250,236,' + (0.5 + g * 0.3) + ')'], [1, 'rgba(255,250,236,0)']]);
    c.fillRect(0, 0, w, h);
    var r = rng(11), x, i;
    for (var k = 0; k < 7; k++) {
      var cx = r() * w, cy = h * (0.06 + r() * 0.2), cr = w * (0.08 + r() * 0.12);
      c.save(); c.translate(cx, cy); c.scale(1, 0.32);
      c.fillStyle = rg(c, 0, 0, 0, cr, [[0, 'rgba(255,255,255,' + (0.35 + g * 0.15) + ')'], [1, 'rgba(255,255,255,0)']]);
      c.beginPath(); c.arc(0, 0, cr, 0, 7); c.fill(); c.restore();
    }
    c.beginPath(); c.moveTo(0, h * 0.6);
    for (x = 0; x <= w; x += 4) c.lineTo(x, h * (0.47 + Math.sin(x / w * 9 + 1) * 0.015 + Math.sin(x / w * 23) * 0.006));
    c.lineTo(w, h * 0.6); c.closePath();
    c.fillStyle = mixC('#ddd3c3', '#a9bcc0', g); c.fill();
    c.beginPath(); c.moveTo(0, h * 0.6);
    for (x = 0; x <= w; x += 3) c.lineTo(x, ridgeY(x, w, h));
    c.lineTo(w, h * 0.6); c.closePath();
    c.fillStyle = lg(c, 0, h * 0.25, 0, h * 0.6, [[0, mixC('#efe6d8', '#c9d3cf', g)], [1, mixC('#d3c3aa', '#8ea08f', g)]]);
    c.fill();
    c.save(); c.clip();
    for (var fxp = 0; fxp < w; fxp += 2) {
      var sl = (ridgeY(fxp + 3, w, h) - ridgeY(fxp - 3, w, h)) / 6;
      if (sl < 0) continue;
      c.fillStyle = mixC('#b8a68c', '#7d917f', g, Math.min(0.28, sl * 0.5));
      c.fillRect(fxp, ridgeY(fxp, w, h), 2, h * 0.6 - ridgeY(fxp, w, h));
    }
    var rr = rng(23);
    for (i = 0; i < 300; i++) {
      var sx = rr() * w, top = ridgeY(sx, w, h);
      var len = (h * 0.6 - top) * (0.3 + rr() * 0.7);
      var slope = (ridgeY(sx + 6, w, h) - ridgeY(sx - 6, w, h)) / 12;
      var lean = clamp(-slope * 2.2, -1.6, 1.6) + (rr() - 0.5) * 0.25;
      var lit = slope > 0;
      len *= 0.55;
      c.strokeStyle = lit ? mixC('#fbf6ee', '#e6eee9', g, 0.28 + rr() * 0.25) : mixC('#a8957a', '#677b68', g, 0.18 + rr() * 0.18);
      c.lineWidth = 0.6 + rr() * 1.4;
      c.beginPath(); c.moveTo(sx, top + 1);
      c.quadraticCurveTo(sx + lean * len * 0.25, top + len * 0.5, sx + lean * len * 0.6, top + len);
      c.stroke();
    }
    if (g > 0.02) {
      var rv = rng(41);
      for (var t2 = 0; t2 < Math.floor(g * 260); t2++) {
        var px = rv() * w, py0 = ridgeY(px, w, h);
        var py = lerp(h * 0.59, py0 + 6, Math.pow(rv(), 1.6) * (0.35 + g * 0.5));
        var pr = 1 + rv() * 1.8;
        c.fillStyle = 'rgba(' + (60 + rv() * 30 | 0) + ',' + (92 + rv() * 30 | 0) + ',58,' + (0.5 * g + 0.2) + ')';
        c.beginPath(); c.ellipse(px, py, pr * 1.4, pr, 0, 0, 7); c.fill();
      }
    }
    c.restore();
    c.fillStyle = lg(c, 0, h * 0.42, 0, h * 0.64, [[0, 'rgba(250,246,238,0)'], [0.7, 'rgba(250,246,238,' + (0.75 - g * 0.45) + ')'], [1, 'rgba(250,246,238,' + (0.4 - g * 0.25) + ')']]);
    c.fillRect(0, h * 0.42, w, h * 0.22);
    [[0.585, '#d9c09a', '#9db27a', 0.012], [0.62, '#ceb185', '#86a065', 0.016]].forEach(function (hl, hi) {
      c.beginPath(); c.moveTo(0, h);
      for (var x2 = 0; x2 <= w; x2 += 4) c.lineTo(x2, h * (hl[0] + Math.sin(x2 / w * (5 + hi * 3) + hi) * hl[3] + Math.sin(x2 / w * 17 + hi * 2) * 0.004));
      c.lineTo(w, h); c.closePath();
      c.fillStyle = mixC(hl[1], hl[2], g); c.fill();
    });
    c.beginPath(); c.moveTo(0, h);
    for (x = 0; x <= w; x += 4) c.lineTo(x, h * (0.645 + Math.sin(x / w * 6 + 2) * 0.008));
    c.lineTo(w, h); c.closePath();
    c.fillStyle = lg(c, 0, h * 0.62, 0, h, [[0, mixC('#cfb084', '#93ad67', g)], [1, mixC('#b8925e', '#6f8f4a', g)]]); c.fill();
    var rs = rng(57);
    for (i = 0; i < 1100; i++) {
      var gy = h * (0.65 + Math.pow(rs(), 1.4) * 0.35), d = (gy / h - 0.64) / 0.36;
      var gx = rs() * w, gl = 1.5 + d * 6;
      c.strokeStyle = rs() < 0.5 ? mixC('#e2c999', '#b3c97e', g, 0.55) : mixC('#9c7a4c', '#55753a', g, 0.45);
      c.lineWidth = 0.5 + d * 0.7;
      c.beginPath(); c.moveTo(gx, gy); c.lineTo(gx + (rs() - 0.5) * gl * 0.6, gy - gl); c.stroke();
    }
    for (i = 0; i < 24; i++) {
      var sy = h * (0.68 + rs() * 0.3), dd = (sy / h - 0.64) / 0.36, sxx = rs() * w, sr = 1.5 + dd * 7 * (0.5 + rs());
      softShadow(c, sxx - sr * 0.3, sy + sr * 0.1, sr * 1.3, sr * 0.4, 0.25);
      c.fillStyle = lg(c, sxx, sy - sr, sxx, sy, [[0, '#ece6dc'], [1, '#a59b8c']]);
      c.beginPath(); c.ellipse(sxx, sy - sr * 0.1, sr, sr * 0.6, 0, Math.PI, 0); c.closePath(); c.fill();
    }
    if (g > 0.5) {
      for (i = 0; i < 160 * (g - 0.5); i++) {
        var fy = h * (0.67 + rs() * 0.32), fx = rs() * w;
        c.fillStyle = ['#f2e6a8', '#f4f1ea', '#e9b9c0'][i % 3];
        c.beginPath(); c.arc(fx, fy, 0.8 + (fy / h - 0.64) * 3, 0, 7); c.fill();
      }
    }
    c.fillStyle = 'rgba(244,238,226,' + (0.28 * (1 - g)) + ')'; c.fillRect(0, 0, w, h);
    addGrain(c, w, h);
  }
  /* ---------- oaks ---------- */
  function makeSpots() {
    var r = rng(2026), out = [], tries = 0;
    [[0.3, 0.8], [0.7, 0.86], [0.5, 0.74], [0.14, 0.9], [0.86, 0.76]].forEach(function (p) { out.push({ u: p[0], v: p[1], s: 0.9 + r() * 0.2, k: out.length % 4 }); });
    while (out.length < 44 && tries < 5000) {
      tries++;
      var u = 0.04 + r() * 0.92, v = 0.67 + Math.pow(r(), 0.8) * 0.3;
      var d = (v - 0.64) / 0.36, ok = true;
      for (var i = 0; i < out.length; i++) {
        var o = out[i], dd = (o.v - 0.64) / 0.36, m = Math.min(d, dd);
        if (Math.abs(o.u - u) < 0.04 + 0.12 * m && Math.abs(o.v - v) < 0.02 + 0.06 * m) { ok = false; break; }
      }
      if (ok) out.push({ u: u, v: v, s: 0.82 + r() * 0.36, k: out.length % 4 });
    }
    return out;
  }
  function oakSprite(k, H, dpr) {
    var key = 'oak' + k + '_' + H + '_' + dpr;
    if (R.sprites[key]) return R.sprites[key];
    var W = H * 1.6, s = mk(W, H, dpr), c = s.x, r = rng(100 + k * 17);
    var cx = W / 2, base = H, trunkH = H * (0.3 + k * 0.02);
    c.fillStyle = lg(c, cx - H * 0.05, 0, cx + H * 0.05, 0, [[0, '#7a6656'], [0.5, '#5e4c3e'], [1, '#3e3128']]);
    c.beginPath(); c.moveTo(cx - H * 0.055, base); c.quadraticCurveTo(cx - H * 0.03, base - trunkH * 0.6, cx - H * 0.035, base - trunkH);
    c.lineTo(cx + H * 0.035, base - trunkH); c.quadraticCurveTo(cx + H * 0.03, base - trunkH * 0.6, cx + H * 0.06, base); c.closePath(); c.fill();
    c.strokeStyle = '#4f3f33'; c.lineCap = 'round'; c.lineWidth = Math.max(1, H * 0.03);
    [[-0.22, 0.5], [0.22, 0.54], [0.02, 0.6]].forEach(function (b) {
      c.beginPath(); c.moveTo(cx, base - trunkH * 0.9); c.quadraticCurveTo(cx + b[0] * H * 0.5, base - trunkH * 1.2, cx + b[0] * H, base - H * b[1]); c.stroke();
    });
    var crW = H * (0.7 + k * 0.04), crTop = H * 0.06, crBot = base - trunkH * 0.85;
    var crC = (crTop + crBot) / 2, crH = (crBot - crTop) / 2;
    var blobs = [], i;
    for (i = 0; i < 26; i++) {
      var a = r() * Math.PI * 2, rad = Math.sqrt(r());
      blobs.push([cx + Math.cos(a) * crW * 0.6 * rad, crC + Math.sin(a) * crH * 0.55 * rad, H * (0.12 + r() * 0.07)]);
    }
    for (i = 0; i < 12; i++) { var aa = Math.PI + (i / 11) * Math.PI; blobs.push([cx + Math.cos(aa) * crW * 0.7, crC + Math.sin(aa) * crH * 0.72 + H * 0.02, H * (0.1 + r() * 0.05)]); }
    blobs.sort(function (p, q) { return p[1] - q[1]; });
    c.fillStyle = '#33472a';
    blobs.forEach(function (b) { c.beginPath(); c.arc(b[0], b[1] + b[2] * 0.15, b[2], 0, 7); c.fill(); });
    blobs.forEach(function (b) {
      c.fillStyle = rg(c, b[0] + b[2] * 0.35, b[1] - b[2] * 0.45, b[2] * 0.1, b[2] * 1.15, [[0, '#97ab63'], [0.55, '#5f7b3b'], [1, 'rgba(70,96,44,0)']]);
      c.beginPath(); c.arc(b[0], b[1], b[2] * 0.92, 0, 7); c.fill();
    });
    c.save(); c.globalCompositeOperation = 'source-atop';
    c.fillStyle = lg(c, 0, crC, 0, crBot + H * 0.08, [[0, 'rgba(30,44,24,0)'], [1, 'rgba(30,44,24,.5)']]);
    c.fillRect(0, crC, W, H * 0.4); c.restore();
    c.fillStyle = 'rgba(200,212,146,.6)';
    for (i = 0; i < 70; i++) {
      var sa = r() * Math.PI * 2, sr = Math.sqrt(r()) * 0.9;
      var sx2 = cx + Math.cos(sa) * crW * 0.62 * sr, sy2 = crC + Math.sin(sa) * crH * 0.6 * sr;
      if (sx2 - cx > -crW * 0.15 && sy2 < crC) { c.beginPath(); c.arc(sx2, sy2, Math.max(0.6, H * 0.012), 0, 7); c.fill(); }
    }
    R.sprites[key] = s; return s;
  }
  function spotInfo(total) {
    var n = SPOTS.length, shownN = Math.min(total, n), out = [];
    for (var i = 0; i < shownN; i++) {
      var layers = 1 + Math.floor(Math.max(0, total - 1 - i) / n);
      out.push({ i: i, stage: Math.min(3, Math.max(1, Math.floor((total - i + 2) / 2))), label: i + 1 + (layers - 1) * n });
    }
    return out;
  }
  function popScale(t0, now) {
    if (!t0 || reduced()) return { x: 1, y: 1 };
    var u = (now - t0) / 900;
    if (u >= 1) return { x: 1, y: 1 };
    var grow = 1 - Math.pow(1 - Math.min(1, u / 0.55), 3);
    var wob = u > 0.55 ? Math.sin((u - 0.55) / 0.45 * Math.PI * 2) * 0.06 * (1 - u) : 0;
    return { x: Math.max(0.01, grow * (1 - wob)), y: Math.max(0.01, grow * (1 + wob)) };
  }
  function greenMix(trees) { var g = cfg.gameRules.green; return { mid: smooth(g.midFrom, g.midTo, trees), green: smooth(g.greenFrom, g.greenTo, trees) }; }
  function wildOn(name) {
    var need = cfg.gameRules.wildlifeAtTrees[name]; if (need == null) return false;
    var earlier = (state.upgrades.wildlife || 0) * cfg.gameRules.upgrades.wildlife.treesEarlier;
    return state.trees + earlier >= need;
  }
  function ghostAlpha() { return clamp((1 - smooth(0, 12, state.trees)) * (1 - (ghostBurst || 0) * 0.7), 0, 1); }
  function bakeBag() {}
  function treeHeight(win, sp, stage) {
    var d = (sp.v - 0.64) / 0.36;
    return Math.min(win.h, win.w * 0.55) * (0.07 + d * 0.2) * sp.s * [0, 0.45, 0.72, 1][stage];
  }
  function drawOaks(c, win, now, dpr) {
    var list = spotInfo(state.trees).slice().sort(function (a, b) { return SPOTS[a.i].v - SPOTS[b.i].v; });
    list.forEach(function (s) {
      var sp = SPOTS[s.i];
      var H = treeHeight(win, sp, s.stage);
      var spr = oakSprite(sp.k, Math.max(8, Math.round(H / 4) * 4), dpr);
      var fx = win.x + win.w * sp.u, fy = win.y + win.h * sp.v;
      var pop = popScale(pops[s.i], now);
      softShadow(c, fx - H * 0.2, fy, H * 0.6 * pop.x, H * 0.08, 0.3);
      c.save(); c.translate(fx, fy); c.scale(pop.x, pop.y);
      var sw = spr.w * (H / spr.h);
      c.drawImage(spr.c, -sw / 2, -H, sw, H);
      c.restore();
    });
  }

  /* ---------- animals ---------- */
  function drawBirds(c, win, now) {
    var n = 4 + (wildOn('leopard') ? 2 : 0);
    for (var i = 0; i < n; i++) {
      var tt = (now / 1000 + i * 7.3) / (26 + i * 3);
      var u = tt % 1, x = win.x + win.w * (u * 1.2 - 0.1), y = win.y + win.h * (0.12 + 0.05 * Math.sin(i * 2 + tt * 6) + i * 0.025);
      var s = win.h * (0.016 + (i % 3) * 0.004), f = reduced() ? 0.3 : Math.sin(now / 140 + i * 1.7);
      c.strokeStyle = 'rgba(40,52,56,.85)'; c.lineWidth = Math.max(1, s * 0.22); c.lineCap = 'round';
      c.beginPath(); c.moveTo(x - s * 1.6, y - f * s * 0.7);
      c.quadraticCurveTo(x - s * 0.6, y - s * 0.5 - f * s * 0.3, x, y);
      c.quadraticCurveTo(x + s * 0.6, y - s * 0.5 - f * s * 0.3, x + s * 1.6, y - f * s * 0.7); c.stroke();
    }
  }
  function rock(c, x, y, w2, h2) {
    softShadow(c, x, y, w2 * 0.62, h2 * 0.16, 0.3);
    c.fillStyle = lg(c, x - w2 * 0.3, y - h2, x + w2 * 0.2, y, [[0, '#e9e2d6'], [0.6, '#b9ad9a'], [1, '#857a6a']]);
    c.beginPath(); c.moveTo(x - w2 / 2, y); c.quadraticCurveTo(x - w2 * 0.48, y - h2 * 0.7, x - w2 * 0.2, y - h2 * 0.95);
    c.quadraticCurveTo(x + w2 * 0.15, y - h2 * 1.08, x + w2 * 0.4, y - h2 * 0.7); c.quadraticCurveTo(x + w2 * 0.55, y - h2 * 0.3, x + w2 / 2, y); c.closePath(); c.fill();
    c.strokeStyle = 'rgba(255,255,255,.35)'; c.lineWidth = 1; c.beginPath(); c.moveTo(x - w2 * 0.25, y - h2 * 0.9); c.quadraticCurveTo(x + w2 * 0.1, y - h2 * 1.02, x + w2 * 0.35, y - h2 * 0.72); c.stroke();
  }
  function drawGoat(c, x, y, s, now) {
    var head = reduced() ? 0 : Math.sin(now / 1600) * 0.06;
    c.save(); c.translate(x, y); c.lineCap = 'round';
    c.strokeStyle = '#4a3a2c'; c.lineWidth = s * 0.05;
    [[-0.32, 0.02], [-0.22, -0.02], [0.24, 0.03], [0.34, -0.01]].forEach(function (l) { c.beginPath(); c.moveTo(s * l[0], -s * 0.36); c.lineTo(s * (l[0] + l[1]), 0); c.stroke(); });
    c.fillStyle = lg(c, 0, -s * 0.62, 0, -s * 0.28, [[0, '#b89a78'], [1, '#86694d']]);
    c.beginPath(); c.ellipse(0, -s * 0.47, s * 0.4, s * 0.17, -0.05, 0, 7); c.fill();
    c.fillStyle = 'rgba(58,42,30,.6)'; c.beginPath(); c.ellipse(s * 0.22, -s * 0.46, s * 0.06, s * 0.15, 0.3, 0, 7); c.fill();
    c.fillStyle = '#efe3cf'; c.beginPath(); c.ellipse(-s * 0.02, -s * 0.35, s * 0.28, s * 0.045, 0, 0, 7); c.fill();
    c.strokeStyle = '#6b5440'; c.lineWidth = s * 0.05; c.beginPath(); c.moveTo(-s * 0.4, -s * 0.5); c.lineTo(-s * 0.48, -s * 0.56); c.stroke();
    c.translate(s * 0.36, -s * 0.54); c.rotate(head);
    c.fillStyle = '#9c7f61'; c.beginPath(); c.moveTo(-s * 0.08, s * 0.1); c.lineTo(s * 0.04, -s * 0.18); c.lineTo(s * 0.15, -s * 0.12); c.lineTo(s * 0.06, s * 0.12); c.closePath(); c.fill();
    c.fillStyle = '#8a6d52'; c.beginPath(); c.ellipse(s * 0.16, -s * 0.1, s * 0.12, s * 0.055, 0.55, 0, 7); c.fill();
    c.fillStyle = '#3a2c20'; c.beginPath(); c.moveTo(s * 0.18, -s * 0.05); c.lineTo(s * 0.17, s * 0.09); c.lineTo(s * 0.23, -s * 0.03); c.closePath(); c.fill();
    c.strokeStyle = '#6e5f4c'; c.lineWidth = s * 0.055;
    c.beginPath(); c.moveTo(s * 0.08, -s * 0.18); c.bezierCurveTo(s * 0.0, -s * 0.55, -s * 0.26, -s * 0.6, -s * 0.36, -s * 0.36); c.stroke();
    c.strokeStyle = 'rgba(240,230,210,.7)'; c.lineWidth = Math.max(0.6, s * 0.014);
    for (var i = 1; i < 6; i++) { var k = i / 6; var px = lerp(s * 0.06, -s * 0.32, k), py = -s * 0.2 - Math.sin(k * Math.PI) * s * 0.32; c.beginPath(); c.moveTo(px - s * 0.025, py - s * 0.015); c.lineTo(px + s * 0.025, py + s * 0.015); c.stroke(); }
    c.fillStyle = '#2b2018'; c.beginPath(); c.arc(s * 0.12, -s * 0.13, Math.max(0.6, s * 0.014), 0, 7); c.fill();
    c.restore();
  }
  function drawLeopard(c, x, y, s, now) {
    var sway = reduced() ? 0 : Math.sin(now / 1100) * 0.1;
    c.save(); c.translate(x, y); c.lineCap = 'round';
    c.strokeStyle = '#c9a676'; c.lineWidth = s * 0.065;
    c.beginPath(); c.moveTo(s * 0.4, -s * 0.1); c.bezierCurveTo(s * 0.58, -s * 0.04, s * (0.56 + sway * 0.3), s * 0.22, s * (0.46 + sway), s * 0.3); c.stroke();
    c.strokeStyle = '#3b2a1a'; c.lineWidth = s * 0.07; c.beginPath(); c.moveTo(s * (0.465 + sway), s * 0.28); c.lineTo(s * (0.45 + sway), s * 0.33); c.stroke();
    c.fillStyle = lg(c, 0, -s * 0.28, 0, 0, [[0, '#e1c18f'], [0.7, '#cfa874'], [1, '#f1e4cc']]);
    c.beginPath(); c.moveTo(-s * 0.3, 0); c.bezierCurveTo(-s * 0.34, -s * 0.2, -s * 0.1, -s * 0.25, s * 0.2, -s * 0.21);
    c.bezierCurveTo(s * 0.42, -s * 0.19, s * 0.5, -s * 0.05, s * 0.42, 0); c.closePath(); c.fill();
    c.fillStyle = '#d7b583';
    roundRect(c, -s * 0.52, -s * 0.055, s * 0.32, s * 0.06, s * 0.03); c.fill();
    roundRect(c, -s * 0.46, -s * 0.025, s * 0.3, s * 0.05, s * 0.025); c.fill();
    var r = rng(77);
    c.strokeStyle = 'rgba(48,32,18,.85)'; c.lineWidth = Math.max(0.7, s * 0.009);
    for (var i = 0; i < 40; i++) {
      var px = -s * 0.24 + r() * s * 0.62, py = -s * 0.2 + r() * s * 0.17;
      if (py > -s * 0.03) continue;
      c.beginPath(); c.arc(px, py, s * (0.012 + r() * 0.01), r() * 3, r() * 3 + 4.4); c.stroke();
    }
    c.fillStyle = 'rgba(48,32,18,.85)';
    for (i = 0; i < 6; i++) { c.beginPath(); c.arc(s * (0.45 + i * 0.012), -s * 0.06 + i * s * 0.05, s * 0.01, 0, 7); c.fill(); }
    var bre = reduced() ? 0 : Math.sin(now / 900) * s * 0.004;
    c.translate(-s * 0.36, -s * 0.2 + bre);
    c.fillStyle = '#ddbd8c'; c.beginPath(); c.ellipse(0, 0, s * 0.1, s * 0.085, 0, 0, 7); c.fill();
    c.beginPath(); c.ellipse(-s * 0.075, s * 0.03, s * 0.05, s * 0.04, 0, 0, 7); c.fill();
    c.fillStyle = '#b48e5e'; c.beginPath(); c.arc(s * 0.035, -s * 0.075, s * 0.028, 0, 7); c.fill(); c.beginPath(); c.arc(-s * 0.045, -s * 0.085, s * 0.026, 0, 7); c.fill();
    c.fillStyle = '#f4ead8'; c.beginPath(); c.ellipse(-s * 0.08, s * 0.045, s * 0.035, s * 0.022, 0, 0, 7); c.fill();
    c.fillStyle = '#2a1d12'; c.beginPath(); c.arc(-s * 0.118, s * 0.028, s * 0.012, 0, 7); c.fill();
    c.beginPath(); c.ellipse(-s * 0.045, -s * 0.012, s * 0.014, s * 0.008, 0, 0, 7); c.fill();
    for (var j = 0; j < 7; j++) { c.beginPath(); c.arc(-s * 0.01 + (j % 3) * s * 0.03, -s * 0.05 + Math.floor(j / 3) * s * 0.03, s * 0.006, 0, 7); c.fill(); }
    c.restore();
  }
  function drawSquirrel(c, x, y, s, now) {
    var tw = reduced() ? 0 : Math.sin(now / 300) * 0.08;
    c.save(); c.translate(x, y);
    c.save(); c.rotate(tw); c.fillStyle = '#a5643a';
    c.beginPath(); c.moveTo(s * 0.2, -s * 0.1); c.bezierCurveTo(s * 0.75, -s * 0.2, s * 0.6, -s * 1.1, s * 0.25, -s * 0.95);
    c.bezierCurveTo(s * 0.5, -s * 0.75, s * 0.45, -s * 0.35, s * 0.05, -s * 0.25); c.closePath(); c.fill(); c.restore();
    c.fillStyle = lg(c, 0, -s * 0.6, 0, 0, [[0, '#b8744a'], [1, '#8c512d']]);
    c.beginPath(); c.ellipse(0, -s * 0.28, s * 0.2, s * 0.3, -0.2, 0, 7); c.fill();
    c.fillStyle = '#e8c9a2'; c.beginPath(); c.ellipse(-s * 0.08, -s * 0.26, s * 0.09, s * 0.2, -0.2, 0, 7); c.fill();
    c.fillStyle = '#ad6a40'; c.beginPath(); c.ellipse(-s * 0.1, -s * 0.62, s * 0.14, s * 0.12, 0, 0, 7); c.fill();
    c.beginPath(); c.moveTo(-s * 0.06, -s * 0.7); c.lineTo(-s * 0.02, -s * 0.86); c.lineTo(s * 0.03, -s * 0.68); c.closePath(); c.fill();
    c.fillStyle = '#1f140c'; c.beginPath(); c.arc(-s * 0.15, -s * 0.64, Math.max(0.7, s * 0.03), 0, 7); c.fill();
    c.restore();
  }
  function drawStream(c, win, k, now) {
    if (k <= 0.01) return;
    var pts = [[0.58, 0.645], [0.53, 0.7], [0.6, 0.78], [0.68, 0.88], [0.63, 1.02]];
    var wid = function (v, pass) { return (0.003 + (v - 0.64) * 0.1) * win.w * (pass ? 0.6 : 1); };
    c.save(); c.globalAlpha = k;
    for (var pass = 0; pass < 2; pass++) {
      c.beginPath();
      var i;
      for (i = 0; i < pts.length; i++) { var p = pts[i]; var X = win.x + win.w * p[0] - wid(p[1], pass), Y = win.y + win.h * p[1]; if (i === 0) c.moveTo(X, Y); else c.lineTo(X, Y); }
      for (i = pts.length - 1; i >= 0; i--) { var q = pts[i]; c.lineTo(win.x + win.w * q[0] + wid(q[1], pass), win.y + win.h * q[1]); }
      c.closePath();
      c.fillStyle = pass ? lg(c, 0, win.y + win.h * 0.64, 0, win.y + win.h, [[0, '#d4eaee'], [1, '#86bfcc']]) : 'rgba(88,128,72,.85)';
      c.fill();
    }
    c.strokeStyle = 'rgba(255,255,255,.75)'; c.lineWidth = 1;
    for (var j = 0; j < 9; j++) {
      var u = reduced() ? j / 9 : ((now / 4000 + j / 9) % 1), seg = Math.min(pts.length - 2, Math.floor(u * (pts.length - 1))), f = u * (pts.length - 1) - seg;
      var ax = lerp(pts[seg][0], pts[seg + 1][0], f), ay = lerp(pts[seg][1], pts[seg + 1][1], f), ww = (ay - 0.64) * 0.04 * win.w;
      c.beginPath(); c.moveTo(win.x + win.w * ax - ww, win.y + win.h * ay); c.lineTo(win.x + win.w * ax + ww * 0.5, win.y + win.h * ay); c.stroke();
    }
    c.restore();
  }
  /* ---------- room (static, prerendered) ---------- */
  function drawRoom(c, L, pal) {
    var w = L.w, h = L.h, win = L.win, i;
    c.fillStyle = lg(c, 0, 0, 0, L.floorY, [[0, pal.wallT], [1, pal.wallB]]); c.fillRect(0, 0, w, L.floorY);
    var ceilH = 30;
    c.fillStyle = pal.ceil; c.fillRect(0, 0, w, ceilH);
    c.fillStyle = 'rgba(6,60,64,.07)'; c.fillRect(0, ceilH, w, 3);
    c.strokeStyle = pal.seam; c.lineWidth = 1;
    for (var x = w / 7; x < w; x += w / 7) { c.beginPath(); c.moveTo(x, ceilH); c.lineTo(x, L.floorY); c.stroke(); }
    var dy = L.floorY - (L.wide ? 120 : 64);
    c.fillStyle = pal.dado; c.fillRect(0, dy, w, 7);
    c.fillStyle = 'rgba(255,255,255,.25)'; c.fillRect(0, dy, w, 1.5);
    c.fillStyle = 'rgba(0,0,0,.08)'; c.fillRect(0, dy + 7, w, 4);
    c.fillStyle = rg(c, win.x + win.w / 2, win.y + win.h / 2, win.w * 0.3, win.w * 0.95, [[0, 'rgba(255,250,238,.35)'], [1, 'rgba(255,250,238,0)']]);
    c.fillRect(0, 0, w, L.floorY);
    var vpX = w / 2, vpY = L.floorY - h * 0.9;
    c.fillStyle = lg(c, 0, L.floorY, 0, h, [[0, pal.floorF], [1, pal.floorN]]); c.fillRect(0, L.floorY, w, h - L.floorY);
    c.save(); c.beginPath(); c.rect(0, L.floorY, w, h - L.floorY); c.clip();
    c.strokeStyle = 'rgba(255,255,255,.08)'; c.lineWidth = 1;
    for (i = -14; i <= 14; i++) { var bx = vpX + i * w * 0.14; c.beginPath(); c.moveTo(vpX + (bx - vpX) * ((L.floorY - vpY) / (h - vpY)), L.floorY); c.lineTo(bx, h); c.stroke(); }
    for (var j = 1; j < 9; j++) { var yy = L.floorY + (h - L.floorY) * Math.pow(j / 9, 1.7); c.beginPath(); c.moveTo(0, yy); c.lineTo(w, yy); c.stroke(); }
    c.fillStyle = pal.shaft;
    c.beginPath(); c.moveTo(win.x + win.w * 0.1, L.floorY); c.lineTo(win.x + win.w * 0.9, L.floorY);
    c.lineTo(win.x + win.w * 1.15, h); c.lineTo(win.x - win.w * 0.15, h); c.closePath(); c.fill();
    c.fillStyle = lg(c, 0, L.floorY, 0, L.floorY + 26, [[0, 'rgba(0,0,0,.14)'], [1, 'rgba(0,0,0,0)']]); c.fillRect(0, L.floorY, w, 26);
    c.restore();
    c.fillStyle = pal.dark ? '#0c3336' : '#c7dcda'; c.fillRect(0, L.floorY - 8, w, 8);
    c.fillStyle = 'rgba(255,255,255,.3)'; c.fillRect(0, L.floorY - 8, w, 1);
    var rv = L.wide ? 20 : 12;
    c.fillStyle = 'rgba(8,50,54,.10)'; roundRect(c, win.x - rv - 6, win.y - rv - 6, win.w + 2 * rv + 12, win.h + 2 * rv + 12, 8); c.fill();
    c.fillStyle = pal.reveal; c.fillRect(win.x - rv, win.y - rv, win.w + 2 * rv, win.h + 2 * rv);
    c.fillStyle = 'rgba(0,0,0,.10)'; c.beginPath(); c.moveTo(win.x - rv, win.y - rv); c.lineTo(win.x + win.w + rv, win.y - rv); c.lineTo(win.x + win.w, win.y); c.lineTo(win.x, win.y); c.closePath(); c.fill();
    c.fillStyle = 'rgba(0,0,0,.05)'; c.beginPath(); c.moveTo(win.x - rv, win.y - rv); c.lineTo(win.x, win.y); c.lineTo(win.x, win.y + win.h); c.lineTo(win.x - rv, win.y + win.h + rv); c.closePath(); c.fill();
    if (L.cabinet) drawCabinet(c, L.cabinet, pal);
    drawSinkStatic(c, L, pal);
    L.units.forEach(function (u) { drawUnitStatic(c, u, pal); });
    drawTable(c, L, pal);
    drawTrolley(c, L, pal);
    addGrain(c, w, h);
  }
  function drawCabinet(c, r, pal) {
    softShadow(c, r.x + r.w / 2, r.y + r.h + 6, r.w * 0.6, 8, 0.15);
    c.fillStyle = lg(c, r.x, 0, r.x + r.w, 0, [[0, pal.steelL], [1, pal.steel]]); roundRect(c, r.x, r.y, r.w, r.h, 6); c.fill();
    var pad = 8, dw = (r.w - pad * 3) / 2;
    for (var d = 0; d < 2; d++) {
      var dx = r.x + pad + d * (dw + pad), dy = r.y + pad, dh = r.h - pad * 2;
      c.fillStyle = pal.dark ? 'rgba(20,60,64,.9)' : 'rgba(208,230,230,.95)'; c.fillRect(dx, dy, dw, dh);
      for (var s = 1; s < 4; s++) {
        var sy = dy + dh * s / 4;
        c.fillStyle = 'rgba(80,110,112,.35)'; c.fillRect(dx, sy, dw, 2);
        var r2 = rng(d * 10 + s + 3), bx = dx + 4;
        while (bx < dx + dw - 12) {
          var bw = 6 + r2() * 12, bh = dh / 4 * (0.35 + r2() * 0.45);
          c.fillStyle = ['#ffffff', '#5aa9a6', '#e9f0f0', '#0d5962', '#b9d3d3'][Math.floor(r2() * 5)];
          roundRect(c, bx, sy - bh, bw, bh, 1.5); c.fill(); bx += bw + 3;
        }
      }
      c.fillStyle = 'rgba(255,255,255,.3)'; c.beginPath(); c.moveTo(dx, dy + dh * 0.7); c.lineTo(dx + dw * 0.6, dy); c.lineTo(dx + dw, dy); c.lineTo(dx, dy + dh); c.closePath(); c.fill();
      c.strokeStyle = pal.steelD; c.lineWidth = 1.5; c.strokeRect(dx, dy, dw, dh);
      c.fillStyle = pal.steelD; c.fillRect(d ? dx + 4 : dx + dw - 7, dy + dh * 0.45, 3, dh * 0.12);
    }
  }
  function drawSinkStatic(c, L, pal) {
    var s = L.sink, top = s.top, w2 = s.w, x = s.x, bot = s.bottom, sbH = L.wide ? 90 : 56;
    c.fillStyle = pal.dark ? '#1b4245' : '#e6f1f0'; c.fillRect(x, top - sbH, w2, sbH);
    c.strokeStyle = 'rgba(6,97,99,.09)'; c.lineWidth = 1;
    for (var ty = top - sbH; ty < top; ty += 14) { c.beginPath(); c.moveTo(x, ty); c.lineTo(x + w2, ty); c.stroke(); }
    for (var tx = x; tx < x + w2; tx += 14) { c.beginPath(); c.moveTo(tx, top - sbH); c.lineTo(tx, top); c.stroke(); }
    softShadow(c, x + w2 / 2, bot, w2 * 0.6, 8, 0.25);
    c.fillStyle = lg(c, x, 0, x + w2, 0, [[0, pal.steel], [0.5, pal.steelL], [1, pal.steelD]]); c.fillRect(x, top + 8, w2, bot - top - 8);
    c.strokeStyle = 'rgba(60,90,92,.35)'; c.beginPath(); c.moveTo(x + w2 / 2, top + 12); c.lineTo(x + w2 / 2, bot - 6); c.stroke();
    c.fillStyle = pal.steelD; c.fillRect(x + w2 / 2 - 10, top + 20, 6, 3); c.fillRect(x + w2 / 2 + 4, top + 20, 6, 3);
    c.fillStyle = lg(c, 0, top, 0, top + 10, [[0, pal.steelL], [1, pal.steel]]); roundRect(c, x - 4, top, w2 + 8, 10, 3); c.fill();
    c.fillStyle = 'rgba(30,60,62,.45)'; roundRect(c, x + w2 * 0.25, top + 1, w2 * 0.55, 5, 3); c.fill();
    var fx = x + w2 * 0.5, fh = L.wide ? 56 : 34;
    c.strokeStyle = pal.steelD; c.lineWidth = L.wide ? 5 : 3.5; c.lineCap = 'round';
    c.beginPath(); c.moveTo(fx, top); c.lineTo(fx, top - fh); c.quadraticCurveTo(fx, top - fh - 14, fx + 14, top - fh - 8); c.lineTo(fx + 16, top - fh + 6); c.stroke();
    c.strokeStyle = pal.steelL; c.lineWidth = 1.2; c.beginPath(); c.moveTo(fx - 1, top); c.lineTo(fx - 1, top - fh); c.stroke();
    var bs = L.wide ? 1 : 0.65;
    [['#f3f6f2', '#d0453d'], ['#e8f1f0', '#2c7fb8'], ['#f0f0e6', '#e0a526']].forEach(function (b, i) {
      var bx = x + w2 * 0.72 + i * 13 * bs, bh = 30 * bs;
      if (bx + 11 * bs > x + w2) return;
      c.fillStyle = b[0]; roundRect(c, bx, top - bh, 11 * bs, bh, 3); c.fill();
      c.fillStyle = b[1]; c.fillRect(bx, top - bh * 0.6, 11 * bs, bh * 0.25); c.fillRect(bx + 3 * bs, top - bh - 5 * bs, 5 * bs, 5 * bs);
    });
  }
  function drawUnitStatic(c, u, pal) {
    var x = u.footX, ry = u.regY, s = u.itemW;
    c.fillStyle = lg(c, x - s * 0.08, 0, x + s * 0.08, 0, [[0, pal.steelD], [0.5, pal.steelL], [1, pal.steelD]]);
    var by = u.footY - u.itemH * 0.62;
    c.fillRect(x - s * 0.05, ry - s * 0.3, s * 0.1, u.footY - ry + s * 0.3);
    softShadow(c, x, u.footY + 6, s * 0.6, 6, 0.25);
    c.fillStyle = lg(c, 0, u.footY, 0, u.footY + 9, [[0, pal.steelL], [1, pal.steelD]]); roundRect(c, x - s * 0.58, u.footY, s * 1.16, 8, 3); c.fill();
    c.fillStyle = pal.steelD; c.beginPath(); c.moveTo(x - s * 0.05, u.footY + 8); c.lineTo(x + s * 0.05, u.footY + 8); c.lineTo(x + s * 0.05, u.footY + 26); c.closePath(); c.fill();
    c.fillStyle = 'rgba(0,0,0,.08)'; roundRect(c, x - s * 0.36 + 2, ry - s * 0.66 + 3, s * 0.72, s * 0.4, 6); c.fill();
    c.fillStyle = lg(c, 0, ry - s * 0.66, 0, ry - s * 0.26, [[0, '#ffffff'], [1, '#dfe9e9']]); roundRect(c, x - s * 0.36, ry - s * 0.66, s * 0.72, s * 0.4, 6); c.fill();
    c.fillStyle = '#f2c94c'; roundRect(c, x - s * 0.3, ry - s * 0.6, s * 0.18, s * 0.08, 2); c.fill();
    c.fillStyle = '#0d5962'; c.beginPath(); c.arc(x + s * 0.14, ry - s * 0.46, s * 0.08, 0, 7); c.fill();
    c.fillStyle = '#e6eeee'; c.beginPath(); c.arc(x + s * 0.14, ry - s * 0.46, s * 0.035, 0, 7); c.fill();
    var gr = s * 0.26;
    softShadow(c, x + 3, ry + gr * 0.9, gr * 1.1, gr * 0.3, 0.2);
    c.fillStyle = lg(c, x - gr, ry - gr, x + gr, ry + gr, [[0, pal.steelL], [1, pal.steelD]]); c.beginPath(); c.arc(x, ry, gr * 1.12, 0, 7); c.fill();
    c.fillStyle = '#fbfdfd'; c.beginPath(); c.arc(x, ry, gr * 0.92, 0, 7); c.fill();
    c.lineWidth = gr * 0.12;
    c.strokeStyle = '#3aa070'; c.beginPath(); c.arc(x, ry, gr * 0.72, Math.PI * 0.8, Math.PI * 1.45); c.stroke();
    c.strokeStyle = '#d9534f'; c.beginPath(); c.arc(x, ry, gr * 0.72, Math.PI * 1.9, Math.PI * 2.2); c.stroke();
    c.strokeStyle = '#2f4e51'; c.lineWidth = 1;
    for (var t3 = 0; t3 <= 10; t3++) { var a = Math.PI * 0.75 + t3 / 10 * Math.PI * 1.5; c.beginPath(); c.moveTo(x + Math.cos(a) * gr * 0.84, ry + Math.sin(a) * gr * 0.84); c.lineTo(x + Math.cos(a) * gr * (t3 % 5 ? 0.72 : 0.62), ry + Math.sin(a) * gr * (t3 % 5 ? 0.72 : 0.62)); c.stroke(); }
    c.fillStyle = '#2a8a64'; roundRect(c, x - gr * 0.3, ry + gr * 1.08, gr * 0.6, gr * 0.42, 4); c.fill();
    c.fillStyle = 'rgba(255,255,255,.3)'; c.fillRect(x - gr * 0.2, ry + gr * 1.13, gr * 0.4, 2);
    c.fillStyle = pal.steelD; roundRect(c, x - s * 0.08, by - 4, s * 0.16, 12, 3); c.fill();
    c.strokeStyle = pal.steelD; c.lineWidth = 4;
    c.beginPath(); c.ellipse(x, by + 6, s * 0.56, s * 0.12, 0, Math.PI, 0); c.stroke();
  }
  function drawUnitFront(c, u, pal) {
    var x = u.footX, s = u.itemW, by = u.footY - u.itemH * 0.62;
    c.strokeStyle = pal.steel; c.lineWidth = 4.5; c.lineCap = 'round';
    c.beginPath(); c.ellipse(x, by + 6, s * 0.56, s * 0.12, 0, 0, Math.PI); c.stroke();
    c.strokeStyle = 'rgba(255,255,255,.75)'; c.lineWidth = 1.2;
    c.beginPath(); c.ellipse(x, by + 5, s * 0.54, s * 0.11, 0, 0.3, Math.PI - 0.3); c.stroke();
  }
  function drawTable(c, L, pal) {
    var t = L.table, cx = t.cx, tw = t.w, top = t.top, fl = L.floorY + (L.wide ? 60 : 36), dir = L.flip ? -1 : 1, i;
    softShadow(c, cx, fl, tw * 0.55, tw * 0.07, 0.35);
    c.fillStyle = '#4f6466'; c.beginPath(); c.moveTo(cx - tw * 0.22, fl); c.lineTo(cx + tw * 0.22, fl); c.lineTo(cx + tw * 0.16, fl - 14); c.lineTo(cx - tw * 0.16, fl - 14); c.closePath(); c.fill();
    c.fillStyle = lg(c, cx - tw * 0.06, 0, cx + tw * 0.06, 0, [[0, pal.steelD], [0.4, pal.steelL], [1, pal.steelD]]); c.fillRect(cx - tw * 0.06, top + 18, tw * 0.12, fl - top - 30);
    var dh = (fl - top) * 0.52;
    c.fillStyle = lg(c, 0, top, 0, top + dh, [[0, pal.drape], [1, pal.drapeD]]);
    c.beginPath(); c.moveTo(cx - tw / 2, top + 6); c.lineTo(cx + tw / 2, top + 6);
    c.quadraticCurveTo(cx + tw * 0.53, top + dh * 0.6, cx + tw * 0.5, top + dh);
    for (i = 0; i < 8; i++) { var fx = cx + tw * 0.5 - tw * i / 8; c.quadraticCurveTo(fx - tw / 16, top + dh + (i % 2 ? 7 : -1), fx - tw / 8, top + dh); }
    c.quadraticCurveTo(cx - tw * 0.53, top + dh * 0.6, cx - tw / 2, top + 6); c.closePath(); c.fill();
    c.strokeStyle = 'rgba(0,0,0,.12)'; c.lineWidth = 1.2;
    for (i = 1; i < 8; i++) { var px = cx - tw / 2 + tw * i / 8; c.beginPath(); c.moveTo(px, top + 14); c.quadraticCurveTo(px + 3, top + dh * 0.6, px + (i % 2 ? 4 : -2), top + dh); c.stroke(); }
    var hx = cx - dir * tw * 0.38;
    c.fillStyle = '#f4f8f8'; roundRect(c, hx - tw * 0.1, top - 8, tw * 0.2, 14, 7); c.fill();
    c.fillStyle = '#d6a27f'; c.beginPath(); c.ellipse(hx, top - 11, tw * 0.05, tw * 0.042, 0, 0, 7); c.fill();
    c.fillStyle = '#7fc1c0'; c.beginPath(); c.ellipse(hx, top - 14, tw * 0.053, tw * 0.03, 0, Math.PI, 0); c.closePath(); c.fill();
    c.fillStyle = lg(c, 0, top - 18, 0, top + 8, [[0, pal.drapeL], [1, pal.drape]]);
    c.beginPath(); c.moveTo(hx + dir * tw * 0.06, top + 7);
    c.bezierCurveTo(hx + dir * tw * 0.1, top - 16, cx + dir * tw * 0.3, top - 14, cx + dir * tw * 0.47, top + 7); c.closePath(); c.fill();
    c.fillStyle = 'rgba(255,255,255,.2)'; c.fillRect(cx - tw / 2, top + 5, tw, 2.5);
    // anaesthesia screen bar
    c.strokeStyle = pal.steelD; c.lineWidth = 2.5; c.beginPath(); c.moveTo(hx + dir * tw * 0.1, top + 6); c.lineTo(hx + dir * tw * 0.1, top - tw * 0.16); c.stroke();
  }
  function drawTrolley(c, L, pal) {
    var tb = L.trayBox, x = tb.x, w2 = tb.w, y = tb.foot, legH = L.wide ? 90 : 62;
    softShadow(c, x + w2 / 2, y + legH + 6, w2 * 0.55, 9, 0.3);
    c.strokeStyle = pal.steelD; c.lineWidth = 3;
    [x + 8, x + w2 - 8].forEach(function (lx) { c.beginPath(); c.moveTo(lx, y); c.lineTo(lx, y + legH); c.stroke(); });
    c.fillStyle = lg(c, 0, y + legH * 0.55, 0, y + legH * 0.55 + 8, [[0, pal.steelL], [1, pal.steel]]); c.fillRect(x + 4, y + legH * 0.55, w2 - 8, 6);
    c.fillStyle = '#2f3f41'; [x + 8, x + w2 - 8].forEach(function (lx) { c.beginPath(); c.arc(lx, y + legH + 2, 5, 0, 7); c.fill(); });
    c.fillStyle = lg(c, 0, y - 4, 0, y + 10, [[0, pal.steelL], [1, pal.steelD]]); roundRect(c, x, y - 2, w2, 11, 4); c.fill();
    c.fillStyle = 'rgba(255,255,255,.6)'; c.fillRect(x + 4, y - 1, w2 - 8, 1.5);
  }
  function drawWindowFrame(c, L, pal) {
    var win = L.win, ft = L.wide ? 12 : 8;
    c.save(); c.beginPath(); c.rect(win.x, win.y, win.w, win.h); c.clip();
    c.fillStyle = 'rgba(255,255,255,.10)';
    c.beginPath(); c.moveTo(win.x + win.w * 0.05, win.y + win.h); c.lineTo(win.x + win.w * 0.32, win.y); c.lineTo(win.x + win.w * 0.42, win.y); c.lineTo(win.x + win.w * 0.15, win.y + win.h); c.closePath(); c.fill();
    c.fillStyle = 'rgba(255,255,255,.06)';
    c.beginPath(); c.moveTo(win.x + win.w * 0.55, win.y + win.h); c.lineTo(win.x + win.w * 0.78, win.y); c.lineTo(win.x + win.w * 0.82, win.y); c.lineTo(win.x + win.w * 0.59, win.y + win.h); c.closePath(); c.fill();
    c.fillStyle = lg(c, 0, win.y, 0, win.y + 22, [[0, 'rgba(8,40,44,.22)'], [1, 'rgba(8,40,44,0)']]); c.fillRect(win.x, win.y, win.w, 22);
    c.restore();
    var fr = lg(c, 0, win.y, 0, win.y + win.h, [[0, pal.frame], [1, pal.frameD]]);
    c.strokeStyle = 'rgba(0,0,0,.12)'; c.lineWidth = ft + 4; c.strokeRect(win.x - ft / 2 + 1, win.y - ft / 2 + 2, win.w + ft, win.h + ft);
    c.strokeStyle = fr; c.lineWidth = ft; c.strokeRect(win.x - ft / 2, win.y - ft / 2, win.w + ft, win.h + ft);
    c.strokeStyle = 'rgba(255,255,255,.7)'; c.lineWidth = 1; c.strokeRect(win.x - ft + 0.5, win.y - ft + 0.5, win.w + 2 * ft - 1, win.h + 2 * ft - 1);
    var mw = Math.max(4, ft * 0.6), tY = win.y + win.h * 0.24;
    c.fillStyle = fr;
    c.fillRect(win.x + win.w / 2 - mw / 2, win.y, mw, win.h);
    c.fillRect(win.x, tY - mw / 2, win.w, mw);
    c.fillStyle = 'rgba(0,0,0,.1)'; c.fillRect(win.x + win.w / 2 + mw / 2, win.y, 2, win.h); c.fillRect(win.x, tY + mw / 2, win.w, 2);
    c.fillStyle = pal.steelD; roundRect(c, win.x + win.w / 2 + mw, win.y + win.h * 0.55, 4, 22, 2); c.fill();
    var sy = win.y + win.h + ft;
    c.fillStyle = lg(c, 0, sy - 2, 0, sy + 12, [[0, '#ffffff'], [1, pal.frameD]]); roundRect(c, win.x - ft * 2.2, sy - 3, win.w + ft * 4.4, 12, 3); c.fill();
    c.fillStyle = 'rgba(0,0,0,.12)'; c.fillRect(win.x - ft * 2, sy + 9, win.w + ft * 4, 4);
  }
  /* ---------- items ---------- */
  function bagSprite(size, H, fill, dpr) {
    var key = 'bag' + size + '_' + H + '_' + fill + '_' + dpr;
    if (R.sprites[key]) return R.sprites[key];
    var W = H * BAG_AR[size], pad = Math.ceil(H * 0.16), s = mk(W + pad * 2, H + pad, dpr), c = s.x;
    c.translate(pad, pad);
    var lh = H * 0.17, bt = lh * 0.92, tw = W * 0.9, bw = W * 0.8, cx = W / 2, r = H * 0.05, i;
    var body = function () {
      c.beginPath(); c.moveTo(cx - tw / 2, bt); c.lineTo(cx + tw / 2, bt);
      c.lineTo(cx + bw / 2, H - r); c.quadraticCurveTo(cx + bw / 2, H, cx + bw / 2 - r, H);
      c.lineTo(cx - bw / 2 + r, H); c.quadraticCurveTo(cx - bw / 2, H, cx - bw / 2, H - r); c.closePath();
    };
    body();
    c.fillStyle = lg(c, cx - tw / 2, 0, cx + tw / 2, 0, [[0, 'rgba(210,225,228,.97)'], [0.28, 'rgba(252,254,254,.99)'], [0.62, 'rgba(236,244,245,.98)'], [1, 'rgba(178,198,202,.98)']]);
    c.fill();
    c.save(); body(); c.clip();
    c.fillStyle = 'rgba(40,130,150,.2)'; roundRect(c, cx - W * 0.07, bt + H * 0.05, W * 0.14, H * 0.34, W * 0.07); c.fill();
    if (fill) {
      var fy = bt + (H - bt) * 0.3;
      c.fillStyle = lg(c, 0, fy, 0, H, [[0, 'rgba(160,62,48,.62)'], [1, 'rgba(96,28,24,.8)']]); c.fillRect(0, fy, W, H);
      c.fillStyle = 'rgba(210,120,100,.5)'; c.beginPath(); c.ellipse(cx, fy, tw * 0.46, H * 0.014, 0, 0, 7); c.fill();
    }
    var rr = rng(size * 31 + 5);
    c.fillStyle = 'rgba(255,255,255,.4)';
    for (i = 0; i < 160; i++) c.fillRect(rr() * W, bt + rr() * (H - bt), 1, 1);
    c.fillStyle = 'rgba(120,150,155,.12)';
    for (i = 0; i < 90; i++) c.fillRect(rr() * W, bt + rr() * (H - bt), 1, 1);
    c.fillStyle = lg(c, cx - tw * 0.38, 0, cx - tw * 0.18, 0, [[0, 'rgba(255,255,255,0)'], [0.5, 'rgba(255,255,255,.85)'], [1, 'rgba(255,255,255,0)']]);
    c.fillRect(cx - tw * 0.38, bt, tw * 0.2, H);
    c.fillStyle = lg(c, cx + tw * 0.25, 0, cx + tw * 0.5, 0, [[0, 'rgba(90,120,124,0)'], [1, 'rgba(90,120,124,.22)']]); c.fillRect(cx + tw * 0.2, bt, tw * 0.3, H);
    c.fillStyle = lg(c, 0, H * 0.8, 0, H, [[0, 'rgba(90,120,124,0)'], [1, 'rgba(90,120,124,.22)']]); c.fillRect(0, H * 0.8, W, H * 0.2);
    c.fillStyle = 'rgba(150,178,184,.5)'; c.fillRect(0, bt + H * 0.04, W, 1.4); c.fillRect(0, bt + H * 0.075, W, 1);
    c.restore();
    c.strokeStyle = 'rgba(80,110,115,.4)'; c.lineWidth = 1; body(); c.stroke();
    var lw = W * 1.0, ly = H * 0.05;
    c.fillStyle = lg(c, 0, ly, 0, lh, [[0, '#2aa2ad'], [1, '#0d6470']]);
    roundRect(c, cx - lw / 2, ly + lh * 0.25, lw, lh * 0.72, lh * 0.2); c.fill();
    c.fillStyle = lg(c, cx - lw / 2, 0, cx + lw / 2, 0, [[0, '#1c8e9b'], [0.4, '#40b6c1'], [1, '#14707c']]);
    c.beginPath(); c.ellipse(cx, ly + lh * 0.28, lw / 2, lh * 0.26, 0, 0, 7); c.fill();
    c.fillStyle = 'rgba(255,255,255,.28)'; c.beginPath(); c.ellipse(cx - lw * 0.12, ly + lh * 0.22, lw * 0.25, lh * 0.08, 0, 0, 7); c.fill();
    c.fillStyle = 'rgba(0,0,0,.15)'; c.fillRect(cx - lw / 2 + 2, ly + lh * 0.72, lw - 4, 1.2);
    c.fillStyle = '#146f7b'; roundRect(c, cx + lw / 2 - 2, ly + lh * 0.45, W * 0.14, lh * 0.22, 3); c.fill();
    c.fillStyle = lg(c, 0, -H * 0.06, 0, ly + lh * 0.3, [[0, '#33aab5'], [1, '#0f6874']]);
    c.save(); c.translate(cx - W * 0.16, ly + lh * 0.25); c.rotate(-0.55); roundRect(c, -W * 0.055, -H * 0.12, W * 0.11, H * 0.13, W * 0.04); c.fill(); c.restore();
    roundRect(c, cx + W * 0.12, ly - H * 0.04, W * 0.13, H * 0.075, W * 0.04); c.fill();
    c.fillStyle = '#0f3f46'; c.beginPath(); c.ellipse(cx + W * 0.185, ly - H * 0.04, W * 0.05, H * 0.012, 0, 0, 7); c.fill();
    c.strokeStyle = '#1c8a96'; c.lineWidth = 1.4; c.beginPath(); c.moveTo(cx + W * 0.18, ly); c.quadraticCurveTo(cx + W * 0.42, ly + lh * 0.1, cx + lw / 2, ly + lh * 0.4); c.stroke();
    if (fill) { c.fillStyle = '#0b525c'; c.beginPath(); c.arc(cx - W * 0.25, ly - H * 0.02, W * 0.055, 0, 7); c.fill(); }
    s.ox = pad; s.oy = pad;
    R.sprites[key] = s; return s;
  }
  function drawBag(c, rect, size, fill, dpr, alpha) {
    var spr = bagSprite(size, Math.round(rect.h), fill ? 1 : 0, dpr);
    softShadow(c, rect.x + rect.w / 2, rect.y + rect.h, rect.w * 0.58, rect.w * 0.12, 0.3);
    if (alpha != null) { c.save(); c.globalAlpha = alpha; }
    c.drawImage(spr.c, rect.x - spr.ox, rect.y - spr.oy, spr.w, spr.h);
    if (alpha != null) c.restore();
  }
  function jarSprite(H, dpr) {
    var key = 'jar_' + H + '_' + dpr;
    if (R.sprites[key]) return R.sprites[key];
    var W = H * 0.72, pad = Math.ceil(H * 0.3), s = mk(W + pad * 2, H + pad, dpr), c = s.x, i;
    c.translate(pad, pad);
    var lt = H * 0.15, cx = W / 2;
    var body = function () { roundRect(c, W * 0.04, lt, W * 0.92, H - lt, W * 0.1); };
    c.strokeStyle = 'rgba(176,150,96,.95)'; c.lineWidth = H * 0.035; c.lineCap = 'round';
    c.beginPath(); c.moveTo(cx + W * 0.2, lt * 0.2); c.bezierCurveTo(cx + W * 0.9, -H * 0.15, W * 1.25, H * 0.3, W * 1.02, H * 0.45);
    c.bezierCurveTo(W * 0.9, H * 0.58, W * 1.2, H * 0.62, W * 1.1, H * 0.72); c.stroke();
    c.strokeStyle = 'rgba(255,240,200,.45)'; c.lineWidth = H * 0.01; c.stroke();
    body();
    c.fillStyle = lg(c, 0, 0, W, 0, [[0, 'rgba(176,168,136,.97)'], [0.3, 'rgba(226,220,190,.97)'], [1, 'rgba(146,138,108,.97)']]); c.fill();
    c.save(); body(); c.clip();
    var fy = lt + (H - lt) * 0.28;
    c.fillStyle = lg(c, 0, fy, 0, H, [[0, 'rgba(128,80,46,.88)'], [0.5, 'rgba(96,54,30,.94)'], [1, 'rgba(52,30,18,.98)']]); c.fillRect(0, fy, W, H);
    var r = rng(91);
    for (i = 0; i < 9; i++) { c.fillStyle = 'rgba(190,150,110,' + (0.08 + r() * 0.14) + ')'; c.beginPath(); c.ellipse(r() * W, fy + r() * (H - fy) * 0.7, W * (0.15 + r() * 0.2), H * 0.03, 0, 0, 7); c.fill(); }
    c.fillStyle = 'rgba(30,16,8,.6)'; for (i = 0; i < 40; i++) { c.beginPath(); c.arc(r() * W, H - r() * H * 0.08, 0.6 + r() * 1.6, 0, 7); c.fill(); }
    c.fillStyle = 'rgba(230,210,170,.6)'; for (i = 0; i < 14; i++) { c.beginPath(); c.arc(W * 0.1 + r() * W * 0.8, fy + r() * 3, 1 + r() * 2.2, 0, 7); c.fill(); }
    for (i = 0; i < 7; i++) { c.fillStyle = 'rgba(110,70,40,' + (0.18 + r() * 0.22) + ')'; c.beginPath(); c.ellipse(r() * W, lt + 4 + r() * (fy - lt - 4), W * 0.06 + r() * W * 0.08, 2 + r() * 4, r(), 0, 7); c.fill(); }
    c.strokeStyle = 'rgba(255,255,245,.55)'; c.lineWidth = 0.7;
    for (i = 0; i < 28; i++) { var sx = r() * W, sy = lt + r() * (H - lt), a = r() * Math.PI, l = 4 + r() * W * 0.25; c.beginPath(); c.moveTo(sx, sy); c.lineTo(sx + Math.cos(a) * l, sy + Math.sin(a) * l * 0.4); c.stroke(); }
    c.strokeStyle = 'rgba(40,40,30,.6)'; c.lineWidth = 1;
    for (i = 1; i < 8; i++) { var gy = H - (H - lt) * i / 8.5; c.beginPath(); c.moveTo(W * 0.1, gy); c.lineTo(W * (i % 2 ? 0.18 : 0.26), gy); c.stroke(); }
    c.fillStyle = lg(c, W * 0.14, 0, W * 0.3, 0, [[0, 'rgba(255,255,255,0)'], [0.5, 'rgba(255,255,250,.45)'], [1, 'rgba(255,255,255,0)']]); c.fillRect(W * 0.12, lt, W * 0.2, H);
    c.restore();
    c.strokeStyle = 'rgba(70,64,48,.85)'; c.lineWidth = 2; body(); c.stroke();
    c.fillStyle = lg(c, 0, 0, 0, lt * 1.2, [[0, '#6b7174'], [1, '#33393b']]); roundRect(c, -W * 0.02, lt * 0.15, W * 1.04, lt * 1.0, 4); c.fill();
    c.fillStyle = 'rgba(255,255,255,.2)'; c.fillRect(W * 0.04, lt * 0.25, W * 0.9, 2);
    c.fillStyle = '#9aa2a5'; c.fillRect(-W * 0.04, lt * 0.9, W * 1.08, lt * 0.3);
    c.fillStyle = '#c3c9cb'; c.fillRect(-W * 0.04, lt * 0.9, W * 1.08, 1.2);
    c.fillStyle = '#3e4446'; roundRect(c, cx - W * 0.28, -H * 0.04, W * 0.14, lt * 0.42, 2); c.fill(); roundRect(c, cx + W * 0.12, -H * 0.05, W * 0.14, lt * 0.44, 2); c.fill();
    s.ox = pad; s.oy = pad;
    R.sprites[key] = s; return s;
  }
  function drawJar(c, rect, dpr, tilt) {
    var spr = jarSprite(Math.round(rect.h), dpr);
    softShadow(c, rect.x + rect.w / 2, rect.y + rect.h, rect.w * 0.62, rect.w * 0.12, 0.34);
    c.save(); c.translate(rect.x + rect.w / 2, rect.y + rect.h); c.rotate(tilt || 0);
    c.drawImage(spr.c, -rect.w / 2 - spr.ox, -rect.h - spr.oy, spr.w, spr.h); c.restore();
  }
  function bioIcon(sz, dpr, col) {
    var key = 'bio' + Math.round(sz) + '_' + dpr;
    if (R.sprites[key]) return R.sprites[key];
    var s = mk(sz, sz, dpr), c = s.x, cx = sz / 2, cy = sz / 2 + sz * 0.03, R1 = sz * 0.21, d = sz * 0.17, k;
    c.fillStyle = col;
    for (k = 0; k < 3; k++) { var a = -Math.PI / 2 + k * Math.PI * 2 / 3; c.beginPath(); c.arc(cx + Math.cos(a) * d, cy + Math.sin(a) * d, R1, 0, 7); c.fill(); }
    c.globalCompositeOperation = 'destination-out';
    for (k = 0; k < 3; k++) { var a2 = -Math.PI / 2 + k * Math.PI * 2 / 3; c.beginPath(); c.arc(cx + Math.cos(a2) * d * 1.42, cy + Math.sin(a2) * d * 1.42, R1 * 0.7, 0, 7); c.fill(); }
    c.beginPath(); c.arc(cx, cy, sz * 0.075, 0, 7); c.fill();
    c.globalCompositeOperation = 'source-over';
    c.strokeStyle = col; c.lineWidth = sz * 0.05; c.beginPath(); c.arc(cx, cy, sz * 0.16, 0, 7); c.stroke();
    c.globalCompositeOperation = 'destination-out';
    c.lineWidth = sz * 0.04;
    for (k = 0; k < 3; k++) { var a3 = Math.PI / 2 + k * Math.PI * 2 / 3; c.beginPath(); c.moveTo(cx, cy); c.lineTo(cx + Math.cos(a3) * sz * 0.22, cy + Math.sin(a3) * sz * 0.22); c.stroke(); }
    c.globalCompositeOperation = 'source-over';
    R.sprites[key] = s; return s;
  }
  function drawBin(c, r, kind, open, hot, dpr, flip) {
    var inf = kind === 'infectious';
    var c0 = inf ? '#a8303f' : '#a9b3b5', c1 = inf ? '#6e1724' : '#717c7f';
    var lidH = r.h * 0.12, bodyT = r.y + lidH * 0.6;
    softShadow(c, r.x + r.w / 2, r.y + r.h, r.w * 0.64, r.w * 0.12, 0.35);
    if (hot) { c.fillStyle = rg(c, r.x + r.w / 2, r.y + r.h * 0.4, 0, r.w * 1.1, [[0, inf ? 'rgba(255,170,160,.45)' : 'rgba(255,255,255,.35)'], [1, 'rgba(255,255,255,0)']]); c.fillRect(r.x - r.w, r.y - r.h, r.w * 3, r.h * 2.5); }
    c.fillStyle = lg(c, r.x, 0, r.x + r.w, 0, [[0, c1], [0.28, c0], [0.7, c0], [1, c1]]);
    c.beginPath(); c.moveTo(r.x, bodyT); c.lineTo(r.x + r.w, bodyT); c.lineTo(r.x + r.w * 0.94, r.y + r.h - 4); c.quadraticCurveTo(r.x + r.w * 0.93, r.y + r.h, r.x + r.w * 0.88, r.y + r.h);
    c.lineTo(r.x + r.w * 0.12, r.y + r.h); c.quadraticCurveTo(r.x + r.w * 0.07, r.y + r.h, r.x + r.w * 0.06, r.y + r.h - 4); c.closePath(); c.fill();
    c.fillStyle = 'rgba(255,255,255,.16)'; c.fillRect(r.x + r.w * 0.16, bodyT + 4, r.w * 0.05, r.h * 0.72);
    c.fillStyle = 'rgba(0,0,0,.18)'; c.fillRect(r.x, bodyT, r.w, 3);
    c.fillStyle = '#2b3335'; roundRect(c, r.x + r.w * 0.32, r.y + r.h - 6, r.w * 0.36, 7, 3); c.fill();
    var ic = r.w * 0.5;
    if (inf) { var b = bioIcon(Math.round(ic), dpr, '#fff1d0'); c.drawImage(b.c, r.x + r.w / 2 - ic / 2, bodyT + r.h * 0.14, ic, ic); }
    else {
      var gx = r.x + r.w / 2, gy = bodyT + r.h * 0.14 + ic * 0.5;
      c.fillStyle = 'rgba(255,255,255,.9)'; c.beginPath(); c.arc(gx, gy, ic * 0.42, 0, 7); c.fill();
      c.strokeStyle = '#5f6a6d'; c.lineWidth = 1.6; c.lineJoin = 'round';
      c.beginPath(); c.moveTo(gx - ic * 0.17, gy - ic * 0.12); c.lineTo(gx + ic * 0.17, gy - ic * 0.12);
      c.moveTo(gx - ic * 0.13, gy - ic * 0.12); c.lineTo(gx - ic * 0.1, gy + ic * 0.2); c.lineTo(gx + ic * 0.1, gy + ic * 0.2); c.lineTo(gx + ic * 0.13, gy - ic * 0.12);
      c.moveTo(gx - ic * 0.05, gy - ic * 0.12); c.lineTo(gx - ic * 0.05, gy - ic * 0.18); c.lineTo(gx + ic * 0.05, gy - ic * 0.18); c.lineTo(gx + ic * 0.05, gy - ic * 0.12); c.stroke();
    }
    c.font = '800 ' + Math.max(10, Math.round(r.w * 0.15)) + 'px ' + FF();
    c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillStyle = inf ? '#fff1d0' : '#ffffff';
    c.fillText(t(inf ? 'binInfShort' : 'binGenShort'), r.x + r.w / 2, r.y + r.h * 0.82);
    var ang = open * (flip ? 1 : -1) * 0.95;
    var hx = flip ? r.x + r.w + r.w * 0.03 : r.x - r.w * 0.03;
    c.save(); c.translate(hx, bodyT); c.rotate(ang);
    var lx = flip ? -r.w * 1.06 : 0;
    c.fillStyle = lg(c, 0, -lidH, 0, 0, [[0, c0], [1, c1]]); roundRect(c, lx, -lidH, r.w * 1.06, lidH, lidH * 0.4); c.fill();
    c.fillStyle = 'rgba(255,255,255,.28)'; c.fillRect(lx + 4, -lidH + 2, r.w * 0.95, 1.5);
    c.restore();
  }

  /* ---------- people ---------- */
  function drawPerson(c, x, foot, H, o, now) {
    var face = o.face || 1, tt = reduced() ? 0 : now / 1000;
    var breathe = Math.sin(tt * 1.6 + (o.seed || 0)) * 0.008;
    var walk = o.walk || 0, ph = tt * 7;
    c.save(); c.translate(x, foot); c.scale(face, 1);
    if (o.alpha != null) c.globalAlpha = o.alpha;
    softShadow(c, 0, 0, H * 0.17, H * 0.03, 0.32);
    var hip = -H * 0.47, sh = -H * 0.8, scrub = o.color || '#3d9c96', scrubD = o.dark || '#2b7671';
    c.lineCap = 'round'; c.lineJoin = 'round';
    var sw = walk ? Math.sin(ph) * H * 0.07 : 0;
    c.strokeStyle = scrubD; c.lineWidth = H * 0.072;
    c.beginPath(); c.moveTo(-H * 0.035, hip); c.lineTo(-H * 0.04 - sw, -H * 0.045); c.stroke();
    c.strokeStyle = scrub;
    c.beginPath(); c.moveTo(H * 0.035, hip); c.lineTo(H * 0.04 + sw, -H * 0.045); c.stroke();
    c.fillStyle = '#eef4f4';
    c.beginPath(); c.ellipse(-H * 0.025 - sw, -H * 0.02, H * 0.05, H * 0.024, 0, 0, 7); c.fill();
    c.beginPath(); c.ellipse(H * 0.055 + sw, -H * 0.02, H * 0.05, H * 0.024, 0, 0, 7); c.fill();
    c.save(); c.translate(0, hip); c.scale(1, 1 + breathe); c.translate(0, -hip);
    c.fillStyle = lg(c, -H * 0.12, 0, H * 0.12, 0, [[0, scrubD], [0.45, scrub], [1, scrub]]);
    c.beginPath(); c.moveTo(-H * 0.1, hip + H * 0.04); c.quadraticCurveTo(-H * 0.125, sh + H * 0.12, -H * 0.11, sh + H * 0.012);
    c.quadraticCurveTo(0, sh - H * 0.025, H * 0.11, sh + H * 0.012); c.quadraticCurveTo(H * 0.125, sh + H * 0.12, H * 0.1, hip + H * 0.04); c.closePath(); c.fill();
    c.fillStyle = '#d5a283'; c.beginPath(); c.moveTo(-H * 0.035, sh); c.lineTo(H * 0.035, sh); c.lineTo(0, sh + H * 0.06); c.closePath(); c.fill();
    c.fillStyle = 'rgba(255,255,255,.85)'; c.fillRect(H * 0.04, sh + H * 0.1, H * 0.035, Math.max(1, H * 0.006));
    c.strokeStyle = 'rgba(0,0,0,.12)'; c.lineWidth = 1; c.beginPath(); c.moveTo(-H * 0.1, hip + H * 0.02); c.lineTo(H * 0.1, hip + H * 0.02); c.stroke();
    [-1, 1].forEach(function (side) {
      var col = side < 0 ? scrubD : scrub;
      var shx = side * H * 0.095, shy = sh + H * 0.035, ex, ey, hx2, hy2;
      if (o.pose === 'scrub' || o.pose === 'reach') {
        var m = o.pose === 'scrub' ? Math.sin(tt * 5 + side) * H * 0.02 : Math.sin(tt * 0.9 + side) * H * 0.01;
        ex = shx + H * 0.05; ey = sh + H * 0.2;
        hx2 = ex + H * 0.15 + m; hy2 = ey - H * 0.01 + (o.pose === 'scrub' ? Math.cos(tt * 5 + side) * H * 0.015 : 0);
      } else {
        var a = walk ? Math.sin(ph + (side > 0 ? Math.PI : 0)) * 0.35 : 0.06 * side;
        ex = shx + Math.sin(a) * H * 0.14; ey = shy + Math.cos(a) * H * 0.15;
        hx2 = ex + Math.sin(a * 1.3) * H * 0.13; hy2 = ey + Math.cos(a) * H * 0.13;
      }
      c.strokeStyle = col; c.lineWidth = H * 0.052;
      c.beginPath(); c.moveTo(shx, shy); c.lineTo(ex, ey); c.stroke();
      c.strokeStyle = '#d29b7a'; c.lineWidth = H * 0.036;
      c.beginPath(); c.moveTo(ex, ey); c.lineTo(hx2, hy2); c.stroke();
      c.fillStyle = '#8fc6e8'; c.beginPath(); c.arc(hx2, hy2, H * 0.024, 0, 7); c.fill();
    });
    c.restore();
    var hy = sh - H * 0.075, hr = H * 0.06;
    c.fillStyle = '#d0a080'; c.fillRect(-H * 0.02, sh - H * 0.035, H * 0.04, H * 0.045);
    c.fillStyle = lg(c, -hr, 0, hr, 0, [[0, '#c38f6f'], [1, '#e4b596']]);
    c.beginPath(); c.ellipse(0, hy, hr * 0.9, hr * 1.05, 0, 0, 7); c.fill();
    c.fillStyle = '#c08a6b'; c.beginPath(); c.ellipse(-hr * 0.68, hy + hr * 0.05, hr * 0.17, hr * 0.25, 0, 0, 7); c.fill();
    c.fillStyle = '#c4e4ee'; c.beginPath(); c.moveTo(-hr * 0.6, hy + hr * 0.02); c.quadraticCurveTo(hr * 1.05, hy - hr * 0.06, hr * 0.96, hy + hr * 0.45); c.quadraticCurveTo(hr * 0.4, hy + hr * 1.12, -hr * 0.55, hy + hr * 0.62); c.closePath(); c.fill();
    c.strokeStyle = 'rgba(120,170,190,.6)'; c.lineWidth = 0.8; c.beginPath(); c.moveTo(-hr * 0.5, hy + hr * 0.3); c.lineTo(hr * 0.9, hy + hr * 0.25); c.moveTo(-hr * 0.5, hy + hr * 0.48); c.lineTo(hr * 0.8, hy + hr * 0.5); c.stroke();
    var blink = (Math.floor(tt * 10 + (o.seed || 0) * 13) % 38) === 0;
    c.fillStyle = '#2a1f1a'; c.beginPath(); c.ellipse(hr * 0.45, hy - hr * 0.15, hr * 0.09, blink ? hr * 0.015 : hr * 0.065, 0, 0, 7); c.fill();
    c.strokeStyle = '#4a3428'; c.lineWidth = Math.max(0.8, hr * 0.07); c.beginPath(); c.moveTo(hr * 0.28, hy - hr * 0.34); c.lineTo(hr * 0.64, hy - hr * 0.3); c.stroke();
    c.fillStyle = o.cap || '#0d5962';
    c.beginPath(); c.ellipse(-hr * 0.05, hy - hr * 0.42, hr * 1.0, hr * 0.64, 0, Math.PI * 0.92, Math.PI * 2.08); c.closePath(); c.fill();
    c.fillRect(-hr * 0.96, hy - hr * 0.5, hr * 1.86, hr * 0.2);
    c.fillStyle = 'rgba(255,255,255,.2)'; c.beginPath(); c.ellipse(hr * 0.2, hy - hr * 0.8, hr * 0.4, hr * 0.14, -0.2, 0, 7); c.fill();
    c.restore();
  }
  /* ---------- dynamic room pieces ---------- */
  function drawLamp(c, L, pal) {
    var lp = L.lamp, r = lp.r, soft = 1 + (state.upgrades.lamp || 0) * 0.3;
    var jx = L.wide ? lp.x + (L.flip ? 1 : -1) * r * 1.3 : lp.x + (L.flip ? -1 : 1) * r * 1.5;
    c.fillStyle = lg(c, 0, L.table.top - 40, 0, L.table.top + 10, [[0, 'rgba(255,252,236,0)'], [1, 'rgba(255,252,236,' + (0.08 * soft) + ')']]);
    c.beginPath(); c.moveTo(lp.x - r * 0.8, lp.y + r * 0.1); c.lineTo(lp.x + r * 0.8, lp.y + r * 0.1); c.lineTo(L.table.cx + L.table.w * 0.5, L.table.top + 6); c.lineTo(L.table.cx - L.table.w * 0.5, L.table.top + 6); c.closePath(); c.fill();
    c.strokeStyle = pal.steelD; c.lineWidth = L.wide ? 7 : 4.5; c.lineCap = 'round';
    c.beginPath(); c.moveTo(jx, 0); c.lineTo(jx, lp.y - r * 1.2); c.quadraticCurveTo(jx, lp.y - r * 0.7, lp.x, lp.y - r * 0.45); c.stroke();
    c.strokeStyle = pal.steelL; c.lineWidth = 1.5; c.beginPath(); c.moveTo(jx - 1.5, 0); c.lineTo(jx - 1.5, lp.y - r * 1.2); c.stroke();
    c.fillStyle = pal.steelD; c.beginPath(); c.arc(jx, lp.y - r * 1.2, L.wide ? 6 : 4, 0, 7); c.fill();
    softShadow(c, lp.x, lp.y + r * 0.35, r * 0.9, r * 0.12, 0.12);
    c.fillStyle = lg(c, 0, lp.y - r * 0.5, 0, lp.y + r * 0.2, [[0, '#ffffff'], [1, pal.steel]]);
    c.beginPath(); c.ellipse(lp.x, lp.y, r, r * 0.42, 0, Math.PI, 0); c.lineTo(lp.x + r, lp.y + r * 0.04); c.ellipse(lp.x, lp.y + r * 0.04, r, r * 0.22, 0, 0, Math.PI); c.closePath(); c.fill();
    c.fillStyle = 'rgba(255,255,255,.6)'; c.beginPath(); c.ellipse(lp.x - r * 0.3, lp.y - r * 0.24, r * 0.4, r * 0.08, -0.15, 0, 7); c.fill();
    c.fillStyle = 'rgba(255,253,240,.97)'; c.beginPath(); c.ellipse(lp.x, lp.y + r * 0.05, r * 0.88, r * 0.17, 0, 0, 7); c.fill();
    c.fillStyle = '#f5e2a6';
    for (var i = 0; i < 7; i++) { var a = i / 7 * Math.PI * 2; c.beginPath(); c.ellipse(lp.x + Math.cos(a) * r * 0.55, lp.y + r * 0.05 + Math.sin(a) * r * 0.1, r * 0.1, r * 0.035, 0, 0, 7); c.fill(); }
    c.beginPath(); c.ellipse(lp.x, lp.y + r * 0.05, r * 0.12, r * 0.04, 0, 0, 7); c.fill();
    c.fillStyle = rg(c, lp.x, lp.y + r * 0.1, 0, r * 1.7 * soft, [[0, 'rgba(255,250,230,.5)'], [1, 'rgba(255,250,230,0)']]);
    c.beginPath(); c.arc(lp.x, lp.y + r * 0.1, r * 1.7 * soft, 0, 7); c.fill();
    c.fillStyle = pal.steelD; roundRect(c, lp.x - r * 0.12, lp.y - r * 0.62, r * 0.24, r * 0.2, 3); c.fill();
  }
  function drawMonitor(c, L, now, pal) {
    var m = L.monitor;
    c.strokeStyle = pal.steelD; c.lineWidth = 5; c.lineCap = 'round';
    if (m.stand) {
      c.beginPath(); c.moveTo(m.x + m.w / 2, m.y + m.h); c.lineTo(m.x + m.w / 2, L.table.top + 8); c.stroke();
    } else {
      c.beginPath(); c.moveTo(m.x + m.w / 2, 0); c.lineTo(m.x + m.w / 2, m.y + 4); c.stroke();
    }
    softShadow(c, m.x + m.w / 2, m.y + m.h + 8, m.w * 0.5, 6, 0.14);
    c.fillStyle = '#26383a'; roundRect(c, m.x, m.y, m.w, m.h, 6); c.fill();
    c.fillStyle = '#071417'; roundRect(c, m.x + 4, m.y + 4, m.w - 8, m.h - 12, 3); c.fill();
    var sx = m.x + 8, sw = m.w * 0.6;
    [['#5fe08f', 0.3], ['#5fd0d1', 0.56], ['#f2d36b', 0.8]].forEach(function (rw, ri) {
      c.strokeStyle = rw[0]; c.lineWidth = 1.2; c.beginPath();
      var y0 = m.y + (m.h - 12) * rw[1] + 4;
      for (var k = 0; k <= 48; k++) {
        var u = k / 48, ph = (u + (reduced() ? 0 : now / 2600)) % 1, v;
        if (ri === 0) { var q = ph % 0.25; v = q > 0.17 && q < 0.19 ? -1 : (q > 0.19 && q < 0.205 ? 0.5 : 0); }
        else v = Math.sin(ph * Math.PI * 8 + ri) * 0.35;
        var px = sx + u * sw, py = y0 + v * m.h * 0.12;
        if (k === 0) c.moveTo(px, py); else c.lineTo(px, py);
      }
      c.stroke();
    });
    c.font = '800 ' + Math.round(m.h * 0.2) + 'px ' + FF(); c.textAlign = 'left'; c.textBaseline = 'middle';
    c.fillStyle = '#5fe08f'; c.fillText(formatNum(72, 0), m.x + m.w * 0.72, m.y + m.h * 0.28);
    c.fillStyle = '#5fd0d1'; c.fillText(formatNum(98, 0), m.x + m.w * 0.72, m.y + m.h * 0.56);
    c.fillStyle = '#3c5254'; c.fillRect(m.x + m.w * 0.4, m.y + m.h - 6, m.w * 0.2, 3);
    c.fillStyle = '#5fe08f'; c.beginPath(); c.arc(m.x + m.w - 9, m.y + m.h - 5, 1.6, 0, 7); c.fill();
  }
  function drawSinkLive(c, L, now, dpr) {
    var s = L.sink, fx = s.x + s.w * 0.5 + 16, top = s.top, fh = L.wide ? 56 : 34;
    if (!state.retired) {
      c.strokeStyle = 'rgba(170,215,230,.8)'; c.lineWidth = 2.2;
      c.beginPath(); c.moveTo(fx, top - fh + 8); c.lineTo(fx + Math.sin(now / 80) * 0.6, top + 2); c.stroke();
      for (var i = 0; i < 3; i++) {
        var u = reduced() ? 0.4 : ((now / 2400) + i / 3) % 1;
        c.fillStyle = rg(c, fx - 10 + Math.sin(u * 6 + i) * 8, top - u * fh * 1.3, 0, 8 + u * 12, [[0, 'rgba(255,255,255,' + (0.35 * (1 - u)) + ')'], [1, 'rgba(255,255,255,0)']]);
        c.beginPath(); c.arc(fx - 10 + Math.sin(u * 6 + i) * 8, top - u * fh * 1.3, 8 + u * 12, 0, 7); c.fill();
      }
    } else {
      var px = s.x + s.w * 0.22, ps = L.wide ? 1 : 0.7;
      c.fillStyle = '#c9805b'; c.beginPath(); c.moveTo(px - 9 * ps, top); c.lineTo(px + 9 * ps, top); c.lineTo(px + 11 * ps, top - 14 * ps); c.lineTo(px - 11 * ps, top - 14 * ps); c.closePath(); c.fill();
      c.fillStyle = '#5e8a46';
      [[-6, -24, 7], [5, -28, 8], [0, -34, 7], [-9, -19, 6], [9, -20, 6]].forEach(function (b) { c.beginPath(); c.arc(px + b[0] * ps, top + b[1] * ps, b[2] * ps, 0, 7); c.fill(); });
      c.fillStyle = '#86b062'; c.beginPath(); c.arc(px + 3 * ps, top - 31 * ps, 3.5 * ps, 0, 7); c.fill();
    }
    var ga = state.retired ? 0 : ghostAlpha();
    if (ga > 0.02) {
      c.save(); c.globalAlpha = 0.25 + ga * 0.5;
      var jh = L.wide ? 50 : 30;
      var jx = s.x + s.w * 0.12;
      drawJar(c, { x: jx, y: top - jh, w: jh * 0.72, h: jh }, dpr, -0.06);
      drawJar(c, { x: jx + jh * 0.62, y: top - jh * 0.88, w: jh * 0.63, h: jh * 0.88 }, dpr, 0.1);
      c.restore();
    }
  }
  function staffPositions(L, now) {
    var home = L.washerHome;
    var dest = L.wide
      ? { x: L.table.cx + (L.flip ? -1 : 1) * L.table.w * 0.6, y: L.floorY + 44 }
      : { x: L.table.cx - (L.flip ? -1 : 1) * L.table.w * 0.32, y: L.floorY + 4 };
    if (R.wasRetired === null) R.wasRetired = !!state.retired;
    if (state.retired && !R.wasRetired) { R.wasRetired = true; R.retireT = now; }
    var k = state.retired ? (R.retireT ? clamp((now - R.retireT) / 4200, 0, 1) : 1) : 0;
    var e = k * k * (3 - 2 * k);
    return { x: lerp(home.x, dest.x, e), y: lerp(home.y, dest.y, e), walking: k > 0 && k < 1, arrived: k >= 1 };
  }
  function ensureLand(win, dpr, g) {
    var q = Math.round(g * 20) / 20;
    var key = [Math.round(win.w), Math.round(win.h), dpr, q].join('|');
    if (key === R.landKey && R.land) return;
    R.landKey = key;
    R.land = mk(win.w, win.h, dpr);
    paintLandscape(R.land.x, win.w, win.h, q);
  }
  function ensureRoom(L, dpr, pal) {
    var key = [L.w, L.h, dpr, pal.dark, L.flip, L.units.length].join('|');
    if (key === R.roomKey && R.room) return;
    R.roomKey = key;
    R.room = mk(L.w, L.h, dpr); drawRoom(R.room.x, L, pal);
    R.frame = mk(L.w, L.h, dpr); drawWindowFrame(R.frame.x, L, pal);
  }
  function drawDropGlow(c, rect, now, color) {
    if (!rect) return;
    var p = reduced() ? 0.5 : (Math.sin(now / 360) + 1) / 2;
    var cx = rect.x + rect.w / 2, cy = rect.y + rect.h / 2, rad = Math.max(rect.w, rect.h) * (0.7 + p * 0.14);
    c.fillStyle = rg(c, cx, cy, rad * 0.15, rad, [[0, color || 'rgba(120,230,225,.42)'], [1, 'rgba(120,230,225,0)']]);
    c.beginPath(); c.arc(cx, cy, rad, 0, 7); c.fill();
  }
  function drawSlotHalo(c, u, now) {
    var p = reduced() ? 0.5 : (Math.sin(now / 360) + 1) / 2;
    var cx = u.footX, cy = u.footY - u.itemH * 0.45;
    c.save();
    c.strokeStyle = 'rgba(95,224,210,' + (0.45 + p * 0.4) + ')'; c.lineWidth = 2.5;
    c.shadowColor = 'rgba(95,224,210,.9)'; c.shadowBlur = 14;
    c.beginPath(); c.ellipse(cx, u.footY - 2, u.itemW * 0.5, u.itemW * 0.12, 0, 0, 7); c.stroke();
    c.restore();
    drawDropGlow(c, { x: cx - u.itemW / 2, y: cy - u.itemH / 2, w: u.itemW, h: u.itemH }, now);
  }

  function draw(now) {
    var dpr = Math.min(2, window.devicePixelRatio || 1);
    var w = canvas.clientWidth, h = canvas.clientHeight;
    if (w < 2 || h < 2) return;
    var bw = Math.round(w * dpr), bh = Math.round(h * dpr);
    if (canvas.width !== bw || canvas.height !== bh) { canvas.width = bw; canvas.height = bh; R.roomKey = ''; }
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    var pal = palette();
    var L = computeLayout(w, h);
    currentLayout = L;
    var win = L.win, mix = greenMix(state.trees), g = clamp(mix.mid * 0.35 + mix.green * 0.65, 0, 1);
    ensureRoom(L, dpr, pal);
    ensureLand(win, dpr, g);
    ctx.drawImage(R.room.c, 0, 0, w, h);
    ctx.save(); ctx.beginPath(); ctx.rect(win.x, win.y, win.w, win.h); ctx.clip();
    ctx.drawImage(R.land.c, win.x, win.y, win.w, win.h);
    if (wildOn('birds')) drawBirds(ctx, win, now);
    drawStream(ctx, win, smooth(cfg.gameRules.streamSwaps - 1, cfg.gameRules.streamSwaps + 3, state.trees), now);
    if (wildOn('goat')) { rock(ctx, win.x + win.w * 0.2, win.y + win.h * 0.75, win.h * 0.13, win.h * 0.05); drawGoat(ctx, win.x + win.w * 0.2, win.y + win.h * 0.712, Math.min(win.h * 0.15, win.w * 0.12), now); }
    drawOaks(ctx, win, now, dpr);
    if (wildOn('squirrel')) drawSquirrel(ctx, win.x + win.w * (SPOTS[1].u - 0.06), win.y + win.h * SPOTS[1].v + 1, win.h * 0.05, now);
    if (wildOn('leopard')) { var ls = Math.min(win.w * 0.19, win.h * 0.32), lx0 = win.x + win.w * 0.44; rock(ctx, lx0, win.y + win.h * 1.01, ls * 1.45, win.h * 0.12); drawLeopard(ctx, lx0, win.y + win.h * 0.895, ls, now); }
    var mistA = (1 - g) * 0.9;
    if (mistA > 0.02) {
      mist.forEach(function (m) {
        var mx = win.x + ((m.u + (reduced() ? 0 : now / 1000 / m.sp / 6)) % 1.2 - 0.1) * win.w;
        var my = win.y + m.v * win.h, rr = m.r * 2.2 * (win.w / 400);
        ctx.fillStyle = rg(ctx, mx, my, 0, rr, [[0, 'rgba(246,242,234,' + (m.a * 2.4 * mistA) + ')'], [1, 'rgba(246,242,234,0)']]);
        ctx.fillRect(mx - rr, my - rr, rr * 2, rr * 2);
      });
    }
    R.ripples = R.ripples.filter(function (rp) { return now - rp.t0 < 1500; });
    R.ripples.forEach(function (rp) {
      var u = (now - rp.t0) / 1500;
      ctx.strokeStyle = 'rgba(190,250,160,' + (0.85 * (1 - u)) + ')'; ctx.lineWidth = 3 * (1 - u) + 0.5;
      ctx.beginPath(); ctx.ellipse(rp.x, rp.y, win.w * 0.2 * u + 2, win.h * 0.045 * u + 1, 0, 0, 7); ctx.stroke();
      ctx.fillStyle = 'rgba(150,220,110,' + (0.28 * (1 - u)) + ')';
      ctx.beginPath(); ctx.ellipse(rp.x, rp.y, win.w * 0.14 * u + 1, win.h * 0.03 * u + 1, 0, 0, 7); ctx.fill();
      ctx.fillStyle = rg(ctx, rp.x, rp.y - 10, 0, 40, [[0, 'rgba(255,255,220,' + (0.6 * (1 - u)) + ')'], [1, 'rgba(255,255,220,0)']]);
      ctx.beginPath(); ctx.arc(rp.x, rp.y - 10, 40, 0, 7); ctx.fill();
    });
    if (R.msGlow && now - R.msGlow < 2600) {
      var mu = (now - R.msGlow) / 2600;
      ctx.fillStyle = 'rgba(255,240,190,' + (0.35 * Math.sin(mu * Math.PI)) + ')'; ctx.fillRect(win.x, win.y, win.w, win.h);
    }
    ctx.restore();
    ctx.drawImage(R.frame.c, 0, 0, w, h);

    drawMonitor(ctx, L, now, pal);
    drawSinkLive(ctx, L, now, dpr);
    var ws = staffPositions(L, now);
    var toTable = L.flip ? -1 : 1;
    var wFace = state.retired ? (ws.walking ? (ws.x < L.table.cx ? 1 : -1) : (ws.x < L.table.cx ? 1 : -1)) : (L.flip ? 1 : -1);
    var wPose = state.retired ? (ws.arrived ? 'reach' : '') : 'scrub';
    var nurseFace = L.nurse.x < L.table.cx ? 1 : -1;
    drawPerson(ctx, ws.x, ws.y, L.nurse.s * 0.97, { face: wFace, pose: wPose, walk: ws.walking ? 1 : 0, seed: 2, color: '#62afa8', dark: '#438c86', cap: '#9fd0cf' }, now);
    drawPerson(ctx, L.nurse.x, L.nurse.y, L.nurse.s, { face: nurseFace, pose: 'reach', seed: 1, cap: '#0d5962' }, now);
    void toTable;
    drawLamp(ctx, L, pal);

    var p = (!busy() && titleCard.hidden) ? primary() : null;
    L.units.forEach(function (u, i) {
      var item = L.used[i];
      if (p && p.phase === 'place' && cases[i] && cases[i].phase === 'place') drawSlotHalo(ctx, u, now);
      var hasItem = item && item.kind !== 'empty' && !item.hide;
      var topY = hasItem ? item.y + 2 : u.footY - u.itemH * 0.75;
      var tipX = u.footX + (hasItem ? (item.kind === 'jar' ? item.w * 0.12 : -item.w * 0.16) : 0);
      ctx.strokeStyle = 'rgba(205,228,230,.95)'; ctx.lineWidth = 3.5; ctx.lineCap = 'round';
      ctx.beginPath(); ctx.moveTo(u.footX + u.itemW * 0.1, u.regY + u.itemW * 0.38);
      ctx.bezierCurveTo(u.footX + u.itemW * 0.75, u.regY + u.itemW * 0.7, u.footX + u.itemW * 0.6, topY - 30, tipX, topY); ctx.stroke();
      ctx.strokeStyle = 'rgba(255,255,255,.7)'; ctx.lineWidth = 1; ctx.stroke();
      if (hasItem) {
        if (item.kind === 'jar') drawJar(ctx, item, dpr, item.lift ? 0.1 : 0);
        else if (item.kind === 'fresh') {
          var cz = cases[i], k = 1;
          if (cz && cz.phase === 'seal') k = clamp((now - cz.t0) / sealMs(), 0, 1);
          var dk = Math.min(1, k * 2.2), drop = 1 - (1 - dk) * (1 - dk);
          drawBag(ctx, { x: item.x, y: item.y - (1 - drop) * 26, w: item.w, h: item.h }, item.size, false, dpr);
          if (cz && cz.phase === 'seal' && k > 0.45) {
            var kk = (k - 0.45) / 0.55;
            ctx.strokeStyle = 'rgba(120,240,215,' + (1 - kk) + ')'; ctx.lineWidth = 3;
            ctx.beginPath(); ctx.ellipse(item.x + item.w / 2, item.y + item.h * 0.1, item.w * (0.5 + kk * 0.5), item.h * 0.06 * (1 + kk * 2), 0, 0, 7); ctx.stroke();
          }
        } else drawBag(ctx, item, item.size, true, dpr);
      }
      drawUnitFront(ctx, u, pal);
      if (p && p.phase === 'lift' && cases[i] === p && hasItem && (state.swaps < 3 || now < coachUntil)) {
        drawDropGlow(ctx, item, now, 'rgba(255,230,150,.16)');
      }
    });

    var placing = p && p.phase === 'place';
    [1, 2, 3].forEach(function (sz) {
      var r = Object.assign({}, L.bags[sz]);
      var sh = shakes[sz];
      if (sh && now - sh < 420) r.x += Math.sin((now - sh) / 40) * 5;
      var lifted = drag && drag.moved && drag.kind === 'bag' && drag.size === sz;
      if (placing && p.size === sz && (state.swaps < 3 || now < coachUntil)) drawDropGlow(ctx, r, now, 'rgba(255,236,170,.4)');
      drawBag(ctx, r, sz, false, dpr, lifted ? 0.28 : 1);
      var lab = formatNum(sz, 0) + ' ' + (lang === 'en' ? 'L' : lang === 'ar' ? 'لتر' : 'لیتر');
      ctx.font = '800 ' + (L.wide ? 13 : 11) + 'px ' + FF(); ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
      var tw = ctx.measureText(lab).width + 14, lx = r.x + r.w / 2, ly = r.y + r.h * 0.62;
      roundRect(ctx, lx - tw / 2, ly - 10, tw, 20, 10); ctx.fillStyle = 'rgba(13,89,98,.92)'; ctx.fill();
      ctx.fillStyle = '#f3fafa'; ctx.fillText(lab, lx, ly + 1);
    });

    var binning = p && p.phase === 'bin';
    var dragUsed = drag && drag.moved && drag.kind === 'used';
    var over = dragUsed ? binAt(drag.px, drag.py) : null;
    ['infectious', 'general'].forEach(function (k2) {
      var key = 'lid_' + k2, target = over === k2 ? 1 : (dragUsed ? 0.3 : (binning ? 0.15 : 0));
      R[key] = (R[key] || 0) + (target - (R[key] || 0)) * 0.22;
      if (binning && k2 === 'infectious' && (state.swaps < 3 || now < coachUntil)) drawDropGlow(ctx, L.bins[k2], now, 'rgba(255,190,170,.38)');
      drawBin(ctx, L.bins[k2], k2, R[key], over === k2, dpr, L.flip);
    });

    if (drag && drag.moved && !busy()) {
      if (drag.kind === 'bag') {
        var src = L.bags[drag.size], sc = 1.1;
        drawBag(ctx, { x: drag.px - src.w * sc / 2, y: drag.py - src.h * sc * 0.7, w: src.w * sc, h: src.h * sc }, drag.size, false, dpr);
      } else if (drag.kind === 'used' && L.used[drag.index]) {
        var su = L.used[drag.index];
        var rr2 = { x: drag.px - su.w / 2, y: drag.py - su.h * 0.7, w: su.w, h: su.h };
        if (su.kind === 'jar') drawJar(ctx, rr2, dpr, 0.08); else drawBag(ctx, rr2, su.size, true, dpr);
      }
    }

    R.bursts = R.bursts.filter(function (b) { return now - b.t0 < 900; });
    R.bursts.forEach(function (b) {
      var u = (now - b.t0) / 900, rad = 90 * (0.4 + u);
      ctx.fillStyle = rg(ctx, b.x, b.y, 0, rad, [[0, 'rgba(210,255,240,' + (0.6 * (1 - u)) + ')'], [1, 'rgba(210,255,240,0)']]);
      ctx.beginPath(); ctx.arc(b.x, b.y, rad, 0, 7); ctx.fill();
      for (var q = 0; q < 12; q++) {
        var a = q / 12 * Math.PI * 2 + b.t0, d = 18 + u * 64;
        ctx.fillStyle = 'rgba(235,255,245,' + (1 - u) + ')'; ctx.beginPath(); ctx.arc(b.x + Math.cos(a) * d, b.y + Math.sin(a) * d * 0.7 - u * 20, 2.4 * (1 - u) + 0.5, 0, 7); ctx.fill();
      }
    });
    seedsFly.forEach(function (s) {
      var u = clamp((now - s.t0) / cfg.gameRules.seedFlightMs, 0, 1);
      for (var tr = 7; tr >= 0; tr--) {
        var uu = Math.max(0, u - tr * 0.022), e = uu * uu * (3 - 2 * uu);
        var x = s.x + (s.tx - s.x) * e, y = s.y + (s.ty - s.y) * e - Math.sin(uu * Math.PI) * 80;
        if (tr === 0) {
          ctx.fillStyle = rg(ctx, x, y, 0, 22, [[0, 'rgba(255,255,240,1)'], [0.25, 'rgba(220,255,200,.85)'], [1, 'rgba(160,240,170,0)']]);
          ctx.beginPath(); ctx.arc(x, y, 22, 0, 7); ctx.fill();
        } else {
          ctx.fillStyle = 'rgba(220,255,215,' + (0.55 - tr * 0.06) + ')';
          ctx.beginPath(); ctx.arc(x, y, Math.max(1, 5 - tr * 0.55), 0, 7); ctx.fill();
        }
      }
    });
    R.leaves = R.leaves.filter(function (lf) { return now - lf.t0 < lf.life; });
    R.leaves.forEach(function (lf) {
      if (now < lf.t0) return;
      var u = (now - lf.t0) / lf.life;
      var x = lf.x + Math.sin(u * 6 + lf.ph) * 30, y = lf.y + u * h * 1.15;
      ctx.save(); ctx.translate(x, y); ctx.rotate(u * 8 + lf.ph); ctx.globalAlpha = Math.min(1, (1 - u) * 3);
      ctx.fillStyle = lf.col; ctx.beginPath(); ctx.ellipse(0, 0, lf.s, lf.s * 0.45, 0, 0, 7); ctx.fill();
      ctx.strokeStyle = 'rgba(0,0,0,.18)'; ctx.lineWidth = 0.8; ctx.beginPath(); ctx.moveTo(-lf.s, 0); ctx.lineTo(lf.s, 0); ctx.stroke();
      ctx.restore();
    });
    placeChrome(L, now);
  }
  function celebrate(now) {
    if (reduced()) return;
    R.msGlow = now;
    var w = canvas.clientWidth;
    for (var i = 0; i < 46; i++) R.leaves.push({ x: Math.random() * w, y: -20 - Math.random() * 200, s: 5 + Math.random() * 6, ph: Math.random() * 6, t0: now + Math.random() * 600, life: 3200 + Math.random() * 1600, col: ['#6f9a45', '#8fb55a', '#4f7a34', '#b6cf7a'][i % 4] });
  }
  function popCounters() {
    ['pillWater', 'pillStaff', 'pillMoney'].forEach(function (id, i) {
      var el = document.getElementById(id); if (!el) return;
      setTimeout(function () { el.classList.remove('bump'); void el.offsetWidth; el.classList.add('bump'); }, i * 90);
    });
  }
  function placeChrome(L, now) {
    var show = titleCard.hidden && !busy();
    var p = primary();
    var teach = state.swaps < 2 || now < coachUntil;
    var target = null;
    if (show && p) {
      var idx = cases.indexOf(p);
      if (p.phase === 'lift' && L.used[idx]) { var r = L.used[idx]; target = { x: r.x + r.w / 2, y: r.y + r.h * 0.45 }; }
      else if (p.phase === 'bin') { var b2 = L.bins.infectious; target = { x: b2.x + b2.w / 2, y: b2.y + b2.h * 0.35 }; }
      else if (p.phase === 'place' && L.bags[p.size]) { var b = L.bags[p.size]; target = { x: b.x + b.w / 2, y: b.y + b.h * 0.35 }; }
    }
    if (target && teach && !drag) { handEl.hidden = false; handEl.style.left = target.x + 'px'; handEl.style.top = target.y + 'px'; }
    else handEl.hidden = true;
    var guide = document.getElementById('guide');
    if (guide) {
      var gt = Math.round(L.win.y + 12) + "px";
      if (guide.style.top !== gt) guide.style.top = gt;
    }
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
        if (currentLayout && currentLayout.units[i]) R.bursts.push({ x: currentLayout.units[i].footX, y: currentLayout.units[i].footY - currentLayout.units[i].itemH * 0.5, t0: now });
        var spotIndex = (state.trees + inFlight) % SPOTS.length;
        inFlight += 1;
        var from = currentLayout && currentLayout.units[i]
          ? { x: currentLayout.units[i].footX, y: currentLayout.units[i].footY - 40 }
          : { x: 0, y: 0 };
        launchSeed(from, spotIndex, function () {
          inFlight -= 1;
          commitCase(c);
          pops[spotIndex] = performance.now();
          if (currentLayout) { var sp0 = SPOTS[spotIndex], w0 = currentLayout.win; R.ripples.push({ x: w0.x + w0.w * sp0.u, y: w0.y + w0.h * sp0.v, t0: performance.now() }); }
          popCounters();
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
    var menuBtn = document.getElementById('menuBtn'), menuEl = document.getElementById('menu');
    var setMenu = function (on) { menuEl.hidden = !on; menuBtn.setAttribute('aria-expanded', on ? 'true' : 'false'); };
    menuBtn.addEventListener('click', function (e) { e.stopPropagation(); setMenu(menuEl.hidden); });
    menuEl.addEventListener('click', function (e) { if (e.target.closest('.menu-item') && e.target.closest('.menu-item').id !== 'themeBtn') setMenu(false); });
    document.addEventListener('pointerdown', function (e) { if (!menuEl.hidden && !e.target.closest('.menu-wrap')) setMenu(false); });
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
