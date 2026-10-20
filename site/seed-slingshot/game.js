/* Angry Bags (Abadis Med). Savings use only config.json (dial-practical surgery formula, n = 1 per jar). */
(function () {
  'use strict';
  var M = Matter, Eng = M.Engine, Bodies = M.Bodies, Body = M.Body, Comp = M.Composite, Events = M.Events;
  var STORE = 'abadis-slingshot-v1', AB = window.AngryBagsApi;
  var canvas = document.getElementById('view'), ctx = canvas.getContext('2d');
  var $ = function (id) { return document.getElementById(id); };
  var cfg, i18n, per, lang = 'fa', W, H, dpr = 1, view = { s: 1, ox: 0, oy: 0 };
  var IMG = {}, engine, level = null, prog, soundOn = false;
  var props = [], parts = [], floats = [], oaks = [], streams = [], actors = [], splashes = [];
  var aim = null, bag = null, flying = null, slow = 0, shake = 0, lastT = 0, acc = 0, fps = 60, frames = 0, fpsT = 0;
  var errors = [];
  var DIM = {
    jar1: [74, 118], jar2: [74, 118], jar3: [64, 136], bucket: [104, 112], can: [70, 120], sink: [146, 128],
    crate: [104, 104], stone: [110, 102], plank: [290, 30], nurse: [150, 225]
  };
  var BREAK = { jar1: 2.6, jar2: 2.6, jar3: 2.4, bucket: 3.4, can: 3.0, sink: 4.4 };
  var WATER_LEN = { jar1: 170, jar2: 170, jar3: 190, bucket: 260, can: 0, sink: 330 };
  var WASTE = { jar1: 1, jar2: 1, jar3: 1, bucket: 1, can: 1, sink: 1 };
  var JAR = { jar1: 1, jar2: 1, jar3: 1 };

  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }
  function lerp(a, b, k) { return a + (b - a) * k; }
  function t(k, v) { var s = (i18n[lang] && i18n[lang][k]) || k; if (v) Object.keys(v).forEach(function (n) { s = s.split('{' + n + '}').join(v[n]); }); return s; }
  function fmt(n, d) { return Number(n).toLocaleString(lang === 'fa' ? 'fa-IR' : lang === 'ar' ? 'ar-EG' : 'en-US', { minimumFractionDigits: d || 0, maximumFractionDigits: d || 0 }); }
  function money(c) { return c >= 1e6 ? fmt(c / 1e6, 2) + ' ' + t('million') : fmt(Math.round(c)) + ' ' + t('toman'); }
  function hours(h) { return fmt(h, 2) + ' ' + t('hour'); }
  function litres(l) { return fmt(l, 1) + ' ' + t('litre'); }

  /* ---------- audio (silent until first tap) ---------- */
  var audio = (function () {
    var ac, master;
    function ensure() { if (ac) return; var A = window.AudioContext || window.webkitAudioContext; if (!A) return; ac = new A(); master = ac.createGain(); master.gain.value = 0; master.connect(ac.destination); }
    function tone(f, d, type, peak, slide) {
      if (!ac || !soundOn) return; var o = ac.createOscillator(), g = ac.createGain(), n = ac.currentTime;
      o.type = type || 'sine'; o.frequency.setValueAtTime(f, n); if (slide) o.frequency.exponentialRampToValueAtTime(slide, n + d);
      g.gain.setValueAtTime(0.0001, n); g.gain.exponentialRampToValueAtTime(peak || 0.08, n + 0.012); g.gain.exponentialRampToValueAtTime(0.0001, n + d);
      o.connect(g); g.connect(master); o.start(n); o.stop(n + d + 0.05);
    }
    function noise(d, f, peak, q) {
      if (!ac || !soundOn) return; var n = ac.currentTime, len = Math.ceil(ac.sampleRate * d), b = ac.createBuffer(1, len, ac.sampleRate), x = b.getChannelData(0);
      for (var i = 0; i < len; i++) x[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / len, 2);
      var s = ac.createBufferSource(), fl = ac.createBiquadFilter(), g = ac.createGain(); s.buffer = b; fl.type = 'bandpass'; fl.frequency.value = f; fl.Q.value = q || 1; g.gain.value = peak || 0.2;
      s.connect(fl); fl.connect(g); g.connect(master); s.start(n);
    }
    return {
      on: function (v) { ensure(); if (!ac) return; ac.resume(); master.gain.setTargetAtTime(v ? 0.8 : 0, ac.currentTime, 0.05); },
      stretch: function (k) { tone(160 + k * 220, 0.06, 'triangle', 0.025); },
      whoosh: function () { noise(0.35, 900, 0.18, 0.7); },
      glass: function () { [1800, 2400, 3100].forEach(function (f, i) { setTimeout(function () { tone(f + Math.random() * 300, 0.25, 'sine', 0.04); }, i * 35); }); noise(0.18, 4000, 0.12, 2); },
      thud: function (v) { tone(90 + Math.random() * 30, 0.14, 'sine', clamp(v * 0.02, 0.02, 0.1), 50); },
      splash: function () { noise(0.6, 700, 0.22, 0.6); },
      pop: function () { tone(520, 0.12, 'sine', 0.06, 900); },
      seed: function () { tone(880 + Math.random() * 300, 0.18, 'sine', 0.03, 1400); },
      free: function () { [523, 659, 784].forEach(function (f, i) { setTimeout(function () { tone(f, 0.3, 'sine', 0.05); }, i * 90); }); },
      win: function () { [523, 659, 784, 1046].forEach(function (f, i) { setTimeout(function () { tone(f, 0.5, 'triangle', 0.05); }, i * 130); }); }
    };
  })();
  function setSound(v) { soundOn = v; audio.on(v); var b = $('soundBtn'); b.textContent = v ? '🔊' : '🔇'; b.setAttribute('aria-pressed', v ? 'true' : 'false'); b.setAttribute('aria-label', t('sound')); try { localStorage.setItem('abadis-slingshot-sound', v ? '1' : '0'); } catch (e) {} }
  var firstTap = false;
  function onFirstTap() { if (firstTap) return; firstTap = true; var p = '1'; try { p = localStorage.getItem('abadis-slingshot-sound') || '1'; } catch (e) {} setSound(p === '1'); }

  /* ---------- progress ---------- */
  function loadProg() { try { var p = JSON.parse(localStorage.getItem(STORE) || 'null'); if (p && p.stars) return p; } catch (e) {} return { stars: {}, unlocked: 1, total: { water: 0, hours: 0, cost: 0, oaks: 0 } }; }
  function saveProg() { try { localStorage.setItem(STORE, JSON.stringify(prog)); } catch (e) {} }

  /* ---------- level ---------- */
  function sprFor(kind) { return { nurse: 'nurse_wash', rock: 'boulder', ledge: 'stone', mover: 'plank' }[kind] || kind; }
  function addBody(b, kind, w, h) { b.kind = kind; b.w = w; b.h = h; b.spr = sprFor(kind); b.home = { x: b.position.x, y: b.position.y }; Comp.add(engine.world, b); return b; }
  function buildLevel(idx) {
    var L = cfg.levels[idx], G = cfg.world.ground;
    if (engine) { Comp.clear(engine.world, false); Eng.clear(engine); }
    engine = Eng.create({ positionIterations: 8, velocityIterations: 6 });
    engine.gravity.y = 1;
    Comp.add(engine.world, [
      Bodies.rectangle(800, G + 60, 6000, 120, { isStatic: true, friction: 0.9, label: 'ground' }),
      Bodies.rectangle(-400, 400, 100, 2000, { isStatic: true, label: 'wall' })
    ]);
    props = []; parts = []; floats = []; oaks = []; streams = []; actors = []; splashes = [];
    level = { idx: idx, def: L, bagsLeft: L.bags, used: 0, waste: 0, wasteTotal: 0, nurses: 0, nursesTotal: 0, freed: 0,
      water: 0, hours: 0, cost: 0, oaks: 0, jars: 0, start: performance.now(), settled: false, over: false, endAt: 0, idleSince: 0, wind: L.wind || 0, movers: [] };
    var tops = [];
    L.items.forEach(function (it, ii) {
      var k = it[0], x = it[1], on = it[2], b;
      var yb = on === 'g' ? G : (typeof on === 'number' && k !== 'mover' ? tops[on] : on);
      tops[ii] = yb - (k === 'rock' ? it[3] * 1.9 : k === 'ledge' ? it[4] : k === 'mover' ? 0 : DIM[k][1]);
      if (k === 'mover') tops[ii] = on;
      if (k === 'rock') { b = Bodies.circle(x, yb - it[3] * 0.9, it[3], { isStatic: true, friction: 0.9 }); addBody(b, 'rock', it[3] * 2, it[3] * 2); return; }
      if (k === 'ledge') { b = Bodies.rectangle(x, yb - it[4] / 2, it[3], it[4], { isStatic: true, friction: 0.9 }); addBody(b, 'ledge', it[3], it[4]); return; }
      if (k === 'mover') { b = Bodies.rectangle(x, yb + 14, it[3], 28, { isStatic: true, friction: 1 }); addBody(b, 'mover', it[3], 28); b.amp = it[4]; b.x0 = x; b.y0 = yb + 14; level.movers.push(b); return; }
      var d = DIM[k], w = d[0], h = d[1];
      var opts = { friction: 0.8, frictionStatic: 1, restitution: 0.05, density: 0.0012, chamfer: { radius: Math.min(6, w * 0.1) } };
      if (k === 'stone') opts.density = 0.004;
      if (k === 'plank') opts.density = 0.0016;
      if (k === 'nurse') { opts.density = 0.003; opts.inertia = Infinity; }
      if (WASTE[k]) opts.density = k === 'sink' ? 0.004 : 0.0015;
      b = Bodies.rectangle(x, yb - h / 2, w, h, opts);
      addBody(b, k, w, h);
      if (WASTE[k]) { level.waste++; level.wasteTotal++; }
      if (k === 'nurse') { level.nurses++; level.nursesTotal++; }
    });
    Events.on(engine, 'collisionStart', onCollide);
    for (var i = 0; i < 90; i++) Eng.update(engine, 1000 / 60);
    Comp.allBodies(engine.world).forEach(function (b) { if (!b.isStatic) { Body.setVelocity(b, { x: 0, y: 0 }); Body.setAngularVelocity(b, 0); b.home = { x: b.position.x, y: b.position.y }; } });
    level.settled = true; level.armedAt = performance.now() + 400;
    loadBag();
    paintHud();
  }
  function slingPt() { return { x: cfg.world.slingX, y: cfg.world.slingY }; }
  function loadBag() {
    if (!level || level.bagsLeft <= 0) { bag = null; return; }
    var p = slingPt();
    bag = { x: p.x, y: p.y, loaded: true, pop: performance.now() };
  }
  function relSpeed(a, b) { var va = a.velocity, vb = b.velocity; return Math.hypot(va.x - vb.x, va.y - vb.y); }
  function onCollide(e) {
    if (!level || !level.settled || performance.now() < level.armedAt) return;
    e.pairs.forEach(function (p) {
      var a = p.bodyA, b = p.bodyB, v = relSpeed(a, b);
      [[a, b], [b, a]].forEach(function (q) {
        var x = q[0], o = q[1];
        if (x.kind === 'bag' && !x.burst && v > 1) { x.burst = performance.now() + 60; }
        if (WASTE[x.kind] && !x.dead) {
          var thr = BREAK[x.kind] * (o.kind === 'bag' ? 0.7 : 1);
          if (v > thr) x.breakAt = performance.now();
          else if (v > 1.5) audio.thud(v);
        }
        if (x.kind === 'nurse' && !x.freed && o.label !== 'ground' && v > (o.kind === 'bag' ? 1.2 : 1.8)) x.freeAt = performance.now();
      });
      if (v > 4 && (a.kind === 'bag' || b.kind === 'bag')) shake = Math.min(14, v * 1.2);
    });
  }
  function destroyWaste(b) {
    if (b.dead) return; b.dead = true; Comp.remove(engine.world, b);
    level.waste--;
    var x = b.position.x, y = b.position.y;
    if (b.kind === 'can') audio.thud(6); else audio.glass();
    if (WATER_LEN[b.kind]) { audio.splash(); splashes.push({ x: x, y: y, t: performance.now(), s: b.kind === 'sink' ? 1.3 : 0.9 }); streams.push({ x: x, len: 0, max: WATER_LEN[b.kind], t: performance.now() }); }
    for (var i = 0; i < 18; i++) parts.push({ x: x, y: y, vx: (Math.random() - 0.5) * 9, vy: -Math.random() * 9, life: 900 + Math.random() * 600, t: performance.now(), c: b.kind === 'can' ? '#c9a37a' : (i % 3 ? 'rgba(160,215,235,.9)' : 'rgba(120,80,40,.8)'), r: 2 + Math.random() * 4, g: 0.35 });
    plantOak(x + (Math.random() - 0.5) * 30, true);
    if (JAR[b.kind]) {
      level.jars++; level.water += per.water; level.hours += per.hours; level.cost += per.cost;
      floats.push({ x: x, y: y - 40, text: '+' + litres(per.water), t: performance.now(), c: '#1f6f9a' });
      bump('cWater'); bump('cStaff'); bump('cMoney');
    }
    paintHud();
    if (level.waste === 0) { slow = performance.now() + 1300; audio.win(); maybeEnd(); if (!level.endAt) { var hn = $('hint'); hn.textContent = t('hintNurse'); hn.hidden = false; } }
  }
  function maybeEnd() {
    if (!level || level.endAt || level.waste > 0) return;
    if (level.freed >= level.nursesTotal || (level.bagsLeft <= 0 && !flying && !bag)) { level.endAt = performance.now() + 2600; $('hint').hidden = true; }
  }
  function freeNurse(b) {
    if (b.freed) return; b.freed = true; Comp.remove(engine.world, b);
    level.freed++; audio.free();
    actors.push({ x: b.position.x + 30, y: cfg.world.ground, t: performance.now(), dir: 1 }); props.push({ x: b.position.x - b.w * 0.18, n: 'sink' });
    floats.push({ x: b.position.x, y: b.position.y - 120, text: t('freed'), t: performance.now(), c: '#0d5962', big: true });
    for (var i = 0; i < 14; i++) parts.push({ x: b.position.x, y: b.position.y - 60, vx: (Math.random() - 0.5) * 6, vy: -2 - Math.random() * 5, life: 1100, t: performance.now(), c: i % 2 ? '#ffe7a0' : '#bff0e6', r: 2 + Math.random() * 3, g: 0.08, glow: true });
    paintHud();
    maybeEnd();
  }
  function plantOak(x, near) {
    var G = cfg.world.ground;
    for (var i = 0; i < oaks.length; i++) if (Math.abs(oaks[i].x - x) < 42) return;
    if (x < cfg.world.slingX + 140 || x > 1700) return;
    oaks.push({ x: x, g: 0, t: performance.now(), s: 0.85 + Math.random() * 0.3, flip: Math.random() < 0.5 });
    level.oaks++;
    audio.seed();
    void G; void near;
  }
  function burstBag(b) {
    if (b.dead) return; b.dead = true; Comp.remove(engine.world, b);
    audio.pop();
    var x = b.position.x, y = b.position.y, vx = b.velocity.x, vy = b.velocity.y;
    for (var i = 0; i < 7; i++) parts.push({ x: x, y: y, vx: vx * 0.3 + (Math.random() - 0.5) * 8, vy: Math.min(vy * 0.3, 0) - 3 - Math.random() * 6, life: 4000, t: performance.now(), acorn: true, r: 14, g: 0.32, plants: i < 2 });
    for (var j = 0; j < 22; j++) parts.push({ x: x, y: y, vx: (Math.random() - 0.5) * 10, vy: (Math.random() - 0.5) * 10, life: 700, t: performance.now(), c: j % 2 ? 'rgba(255,240,180,.95)' : 'rgba(255,255,255,.9)', r: 2 + Math.random() * 3, g: 0.05, glow: true });
    flying = null;
    setTimeout(function () { if (level && !level.over) { loadBag(); paintHud(); } }, 650);
  }
  function fire(dx, dy) {
    var p = slingPt(), k = cfg.world.power;
    var b = Bodies.rectangle(bag.x, bag.y, 50, 100, { density: 0.012, friction: 0.5, restitution: 0.2, frictionAir: 0, chamfer: { radius: 14 } });
    b.kind = 'bag'; b.w = 50; b.h = 100; b.spr = 'bag'; b.launched = performance.now();
    Comp.add(engine.world, b);
    Body.setVelocity(b, { x: (p.x - bag.x) * k, y: (p.y - bag.y) * k });
    Body.setAngularVelocity(b, 0.04);
    flying = b; bag = null; level.bagsLeft--; level.used++;
    audio.whoosh();
    paintHud();
    void dx; void dy;
  }

  /* ---------- simulation ---------- */
  function step(dtMs, now) {
    if (!level) return;
    var ts = now < slow ? 0.28 : 1;
    level.movers.forEach(function (m) {
      var nx = m.x0 + Math.sin((now - level.start) / 1400) * m.amp;
      Body.setVelocity(m, { x: nx - m.position.x, y: 0 }); Body.setPosition(m, { x: nx, y: m.y0 });
    });
    if (flying && level.wind) Body.applyForce(flying, flying.position, { x: level.wind * 0.00012 * flying.mass, y: 0 });
    Eng.update(engine, dtMs * ts);
    var all = Comp.allBodies(engine.world);
    all.forEach(function (b) {
      if (b.dead || b.freed) return;
      if (b.kind === 'bag') {
        if ((b.burst && now >= b.burst) || b.position.y > 1100 || b.position.x > 2000 || (now - b.launched > 6000)) burstBag(b);
      } else if (WASTE[b.kind]) {
        var tilted = Math.abs(Math.sin(b.angle)) > 0.75 && b.speed < 0.3 && b.position.y > cfg.world.ground - 80;
        if (b.breakAt || b.position.y > 1100 || b.position.x > 1900 || tilted) destroyWaste(b);
      } else if (b.kind === 'nurse') {
        var moved = Math.hypot(b.position.x - b.home.x, b.position.y - b.home.y) > 26;
        if (b.freeAt || moved || Math.abs(b.angle) > 0.3) freeNurse(b);
      }
    });
  }
  function updateFx(dt, now) {
    var G = cfg.world.ground, ts = now < slow ? 0.28 : 1, k = dt / 16.67 * ts;
    parts = parts.filter(function (p) {
      p.vy += p.g * k; p.x += p.vx * k; p.y += p.vy * k;
      if (p.acorn && p.y > G - 10) {
        p.y = G - 10; if (!p.landed) { p.landed = true; p.vx *= 0.3; p.vy = 0; p.landT = now; if (p.plants) plantOak(p.x); }
        p.vx *= 0.9; p.vy = 0;
      }
      return now - p.t < p.life && (!p.landed || now - p.landT < 900);
    });
    streams.forEach(function (s) { s.len = Math.min(s.max, s.len + dt * 0.18 * ts); });
    oaks.forEach(function (o) {
      var wet = streams.some(function (s) { return o.x > s.x - 40 && o.x < s.x + s.len + 40; });
      o.wet = wet; o.g = Math.min(1, o.g + dt / 1000 * (wet ? 0.55 : 0.22) * ts);
    });
    actors.forEach(function (a) {
      var age = now - a.t;
      if (age > 1500) { a.x += a.dir * 0.11 * dt * ts; a.walk = true; }
    });
    actors = actors.filter(function (a) { return a.x > -200 && a.x < 2100; });
    floats = floats.filter(function (f) { return now - f.t < 1600; });
    splashes = splashes.filter(function (s) { return now - s.t < 900; });
    if (shake > 0) shake = Math.max(0, shake - dt * 0.03);
    if (level && !level.over) {
      if (level.endAt && now > level.endAt) endLevel(true);
      else if (!level.endAt && level.waste === 0 && level.bagsLeft <= 0 && !flying && !bag) maybeEnd();
      else if (!level.endAt && level.bagsLeft <= 0 && !flying && !bag) {
        var calm = Comp.allBodies(engine.world).every(function (b) { return b.isStatic || b.speed < 0.25; });
        if (calm) { if (!level.idleSince) level.idleSince = now; else if (now - level.idleSince > 1800) endLevel(false); }
        else level.idleSince = 0;
      }
    }
  }

  /* ---------- input ---------- */
  function toWorld(e) { var r = canvas.getBoundingClientRect(); return { x: (e.clientX - r.left - view.ox) / view.s, y: (e.clientY - r.top - view.oy) / view.s }; }
  function onDown(e) {
    onFirstTap();
    if (!level || level.over || !bag || !$('end').hidden) return;
    var p = toWorld(e), s = slingPt();
    if (Math.hypot(p.x - s.x, p.y - s.y) > 170) {
      // forgiving: grabbing anywhere left half of the world also works
      if (p.x > s.x + 260) return;
    }
    aim = { id: e.pointerId, sx: p.x, sy: p.y, lastK: 0 };
    try { canvas.setPointerCapture(e.pointerId); } catch (er) {}
    $('hint').hidden = true;
    onMove(e);
  }
  function onMove(e) {
    if (!aim || e.pointerId !== aim.id || !bag) return;
    var p = toWorld(e), s = slingPt(), mp = cfg.world.maxPull;
    var dx = p.x - aim.sx, dy = p.y - aim.sy, d = Math.hypot(dx, dy);
    if (d > mp) { dx *= mp / d; dy *= mp / d; d = mp; }
    bag.x = s.x + dx; bag.y = s.y + dy;
    var k = Math.round(d / 25); if (k !== aim.lastK) { aim.lastK = k; audio.stretch(d / mp); }
  }
  function onUp(e) {
    if (!aim || e.pointerId !== aim.id) return;
    aim = null;
    if (!bag) return;
    var s = slingPt(), d = Math.hypot(bag.x - s.x, bag.y - s.y);
    if (d < 25) { bag.x = s.x; bag.y = s.y; return; }
    fire();
  }
  function preview() {
    if (!bag || !aim) return [];
    var s = slingPt(), k = cfg.world.power, vx = (s.x - bag.x) * k, vy = (s.y - bag.y) * k, x = bag.x, y = bag.y, g = 1000 / 60 * 1000 / 60 * 0.001, pts = [];
    var wind = level.wind * 0.00012 * (1000 / 60) * (1000 / 60);
    for (var i = 0; i < 70; i++) { vy += g; vx += wind; x += vx; y += vy; if (i % 3 === 2) pts.push([x, y]); if (y > cfg.world.ground) break; }
    return pts.slice(0, 18);
  }

  /* ---------- render ---------- */
  function resize() {
    dpr = Math.min(2, window.devicePixelRatio || 1);
    W = window.innerWidth; H = window.innerHeight;
    canvas.width = Math.round(W * dpr); canvas.height = Math.round(H * dpr);
    var s = Math.min(W / cfg.world.w, H / cfg.world.h);
    view.s = s; view.ox = (W - cfg.world.w * s) / 2; view.oy = (H - cfg.world.h * s) / 2;
    if (W < H) { s = W / 1500; view.s = s; view.ox = -100 * s; view.oy = H * 0.72 - cfg.world.ground * s; }
    $('rotate').hidden = !(W < H && W < 700);
  }
  function img(n) { return IMG[n]; }
  function drawImg(n, x, y, w, h, flip) {
    var im = img(n); if (!im) return;
    if (flip) { ctx.save(); ctx.translate(x + w / 2, 0); ctx.scale(-1, 1); ctx.drawImage(im, -w / 2, y, w, h); ctx.restore(); }
    else ctx.drawImage(im, x, y, w, h);
  }
  function drawBg(now) {
    var bgi = img('bg' + (level ? level.def.bg : 1)); if (!bgi) return;
    var vl = -view.ox / view.s, vt = -view.oy / view.s, vw = W / view.s, vh = H / view.s;
    var bw = Math.max(vw, cfg.world.w), bh = bw * 9 / 16;
    if (bh < vh) { bh = vh; bw = bh * 16 / 9; }
    var bx = vl + (vw - bw) / 2, by = 900 - bh + (bh - 900) * 0;
    if (by > vt) by = vt;
    if (by + bh < vt + vh) by = vt + vh - bh;
    var par = aim ? 0 : Math.sin(now / 9000) * 4;
    ctx.drawImage(bgi, bx + par, by, bw, bh);
    if (vt + vh > by + bh - 2) { ctx.fillStyle = '#6b5232'; ctx.fillRect(vl, by + bh - 2, vw, vt + vh - by - bh + 4); }
    var G = cfg.world.ground;
    var gr = ctx.createLinearGradient(0, G - 20, 0, G + 80);
    gr.addColorStop(0, 'rgba(60,40,20,0)'); gr.addColorStop(0.3, 'rgba(60,40,20,.18)'); gr.addColorStop(1, 'rgba(40,26,12,.35)');
    ctx.fillStyle = gr; ctx.fillRect(vl, G - 20, vw, vt + vh - G + 20);
  }
  function shadow(x, y, w) { ctx.fillStyle = 'rgba(40,25,8,.28)'; ctx.beginPath(); ctx.ellipse(x, y, w, w * 0.16, 0, 0, 7); ctx.fill(); }
  function drawStreams(now) {
    var G = cfg.world.ground;
    streams.forEach(function (s) {
      var x0 = s.x - 30, x1 = s.x + s.len;
      var g = ctx.createLinearGradient(x0, 0, x1 + 40, 0);
      g.addColorStop(0, 'rgba(140,205,230,.0)'); g.addColorStop(0.08, 'rgba(140,205,230,.8)'); g.addColorStop(0.9, 'rgba(120,190,220,.75)'); g.addColorStop(1, 'rgba(120,190,220,0)');
      ctx.fillStyle = g;
      ctx.beginPath(); ctx.moveTo(x0, G - 4);
      for (var x = x0; x <= x1 + 40; x += 16) ctx.lineTo(x, G - 4 - Math.sin(x * 0.05 + s.x) * 2);
      for (var x2 = x1 + 40; x2 >= x0; x2 -= 16) ctx.lineTo(x2, G + 10 + Math.sin(x2 * 0.04) * 3);
      ctx.closePath(); ctx.fill();
      ctx.strokeStyle = 'rgba(255,255,255,.75)'; ctx.lineWidth = 1.6;
      for (var j = 0; j < 5; j++) {
        var u = ((now / 1800 + j / 5) % 1), hx = x0 + 20 + u * (x1 - x0);
        ctx.beginPath(); ctx.moveTo(hx, G + 2); ctx.lineTo(hx + 14, G + 2); ctx.stroke();
      }
    });
  }
  function drawOaks(now) {
    var G = cfg.world.ground;
    oaks.forEach(function (o) {
      var g = o.g, e = 1 - Math.pow(1 - g, 3), n, h;
      if (g < 0.3) { n = 'sprout'; h = 34 + 40 * (g / 0.3); }
      else if (g < 0.65) { n = 'sapling'; h = 80 + 70 * ((g - 0.3) / 0.35); }
      else { n = 'oak'; h = 150 + 70 * ((g - 0.65) / 0.35); }
      h *= o.s; var im = img(n); if (!im) return;
      var w = h * im.width / im.height, sway = Math.sin(now / 900 + o.x) * 0.02;
      shadow(o.x, G + 2, w * 0.35);
      ctx.save(); ctx.translate(o.x, G + 4); ctx.rotate(sway); if (o.flip) ctx.scale(-1, 1);
      var pop = Math.min(1, (now - o.t) / 300); ctx.scale(pop, pop);
      ctx.drawImage(im, -w / 2, -h, w, h); ctx.restore();
      if (o.wet && g < 1) { ctx.fillStyle = 'rgba(200,255,200,' + (0.25 + 0.2 * Math.sin(now / 200)) + ')'; ctx.beginPath(); ctx.arc(o.x, G - h * 0.5, 6, 0, 7); ctx.fill(); }
      void e;
    });
  }
  function drawBody(b, now) {
    var n = b.spr, im = img(n); if (!im) return;
    var w = b.w, h = b.h, dw = w, dh = h;
    if (b.kind === 'rock') { dw = w * 1.08; dh = dw * im.height / im.width; }
    else if (b.kind === 'crate') { dw = w * 1.14; dh = h * 1.02; }
    else if (b.kind === 'stone') { dw = w * 1.12; dh = h * 1.05; }
    else if (b.kind === 'plank' || b.kind === 'mover') { dw = w * 1.04; dh = h * 1.6; }
    else if (b.kind === 'nurse') { dh = h * 1.12; dw = dh * im.width / im.height; }
    else if (b.kind === 'ledge') { ctx.save(); ctx.translate(b.position.x, b.position.y); var pat = ctx.createLinearGradient(0, -h / 2, 0, h / 2); pat.addColorStop(0, '#b9a07a'); pat.addColorStop(1, '#7d6646'); ctx.fillStyle = pat; ctx.beginPath(); ctx.moveTo(-w / 2 - 20, h / 2); ctx.lineTo(-w / 2 + 10, -h / 2 + 6); ctx.quadraticCurveTo(0, -h / 2 - 8, w / 2 - 10, -h / 2 + 4); ctx.lineTo(w / 2 + 24, h / 2); ctx.closePath(); ctx.fill(); ctx.drawImage(im, -w / 2 + 6, -h / 2 - 4, w - 12, 44); ctx.restore(); return; }
    else { dh = h * 1.06; dw = dh * im.width / im.height; }
    ctx.save(); ctx.translate(b.position.x, b.position.y); ctx.rotate(b.angle);
    if (b.kind === 'nurse') { var bob = Math.sin(now / 500) * 1.5; ctx.drawImage(im, -dw / 2 - dw * 0.08, -dh / 2 - (dh - h) + bob * 0, dw, dh); }
    else ctx.drawImage(im, -dw / 2, -dh / 2 - (dh - h) / 2, dw, dh);
    ctx.restore();
  }
  function drawSling(now) {
    var s = slingPt(), fh = 300, fw = fh * 162 / 300, fx = s.x - fw * 0.55, fy = s.y - fh * 0.12;
    var lt = { x: fx + fw * 0.2, y: fy + fh * 0.15 }, rt = { x: fx + fw * 0.88, y: fy + fh * 0.16 };
    var bp = bag ? { x: bag.x, y: bag.y } : { x: s.x, y: s.y + 6 };
    var pull = bag ? Math.hypot(bag.x - s.x, bag.y - s.y) / cfg.world.maxPull : 0;
    shadow(s.x, cfg.world.ground + 4, 60);
    ctx.lineCap = 'round';
    ctx.strokeStyle = '#6b3f1d'; ctx.lineWidth = 7 - pull * 2.5;
    ctx.beginPath(); ctx.moveTo(rt.x, rt.y); ctx.lineTo(bp.x + 14, bp.y + 10); ctx.stroke();
    drawImg('fork', fx, fy, fw, fh);
    if (bag) {
      var bh = 104, bw = bh * 72 / 150, wob = bag.loaded && !aim ? Math.sin(now / 300) * 1.5 : 0;
      var pop = clamp((now - bag.pop) / 250, 0, 1); bh *= pop; bw *= pop;
      ctx.save(); ctx.translate(bag.x, bag.y); ctx.rotate(aim ? Math.atan2(s.y - bag.y, s.x - bag.x) * 0.15 : 0);
      ctx.drawImage(img('bag'), -bw / 2, -bh * 0.62 + wob, bw, bh);
      ctx.restore();
    }
    var pw = 84, ph = pw * 97 / 112;
    drawImg('pouch', bp.x - pw * 0.55, bp.y - ph * 0.15, pw, ph);
    ctx.strokeStyle = '#7a4a22'; ctx.lineWidth = 7 - pull * 2.5;
    ctx.beginPath(); ctx.moveTo(lt.x, lt.y); ctx.lineTo(bp.x - 22, bp.y + 12); ctx.stroke();
    ctx.strokeStyle = 'rgba(255,220,170,.35)'; ctx.lineWidth = 1.5; ctx.stroke();
  }
  function drawActors(now) {
    actors.forEach(function (a) {
      var age = now - a.t, n = age < 1500 ? 'nurse_wave' : 'nurse_walk', im = img(n); if (!im) return;
      var h = 235, w = h * im.width / im.height, bob = a.walk ? Math.abs(Math.sin(age / 160)) * 5 : Math.sin(age / 120) * 2;
      shadow(a.x, cfg.world.ground + 2, 34);
      drawImg(n, a.x - w / 2, cfg.world.ground - h - bob + 4, w, h, n === 'nurse_walk' && a.dir < 0);
    });
  }
  function drawFx(now) {
    splashes.forEach(function (s) {
      var u = (now - s.t) / 900, im = img('splash'); if (!im) return;
      var h = 150 * s.s * (0.5 + u), w = h * im.width / im.height;
      ctx.globalAlpha = 1 - u * u; ctx.drawImage(im, s.x - w / 2, s.y - h * 0.7, w, h); ctx.globalAlpha = 1;
    });
    parts.forEach(function (p) {
      var u = (now - p.t) / p.life;
      if (p.acorn) {
        var im = img('acorn'), r = 26;
        ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.vx * 0.05 + (p.landed ? 0 : now / 200));
        ctx.globalAlpha = p.landed ? clamp(1 - (now - p.landT) / 900, 0, 1) : 1;
        ctx.drawImage(im, -r / 2, -r * 0.6, r, r * im.height / im.width); ctx.restore(); ctx.globalAlpha = 1;
        return;
      }
      ctx.globalAlpha = clamp(1 - u, 0, 1);
      if (p.glow) { var g = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, p.r * 3); g.addColorStop(0, p.c); g.addColorStop(1, 'rgba(255,255,255,0)'); ctx.fillStyle = g; ctx.beginPath(); ctx.arc(p.x, p.y, p.r * 3, 0, 7); ctx.fill(); }
      else { ctx.fillStyle = p.c; ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, 7); ctx.fill(); }
      ctx.globalAlpha = 1;
    });
    floats.forEach(function (f) {
      var u = (now - f.t) / 1600;
      ctx.globalAlpha = clamp(1.4 - u * 1.4, 0, 1);
      ctx.font = '900 ' + (f.big ? 34 : 26) + 'px Kalameh, system-ui, sans-serif'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
      ctx.lineWidth = 6; ctx.strokeStyle = 'rgba(255,250,235,.9)'; ctx.strokeText(f.text, f.x, f.y - u * 50);
      ctx.fillStyle = f.c; ctx.fillText(f.text, f.x, f.y - u * 50);
      ctx.globalAlpha = 1;
    });
  }
  function drawPreview(now) {
    var pts = preview();
    pts.forEach(function (p, i) {
      var r = 7 - i * 0.28, a = 1 - i / pts.length * 0.7;
      var g = ctx.createRadialGradient(p[0], p[1], 0, p[0], p[1], r * 2.4); g.addColorStop(0, 'rgba(255,240,170,' + a + ')'); g.addColorStop(1, 'rgba(255,220,120,0)');
      ctx.fillStyle = g; ctx.beginPath(); ctx.arc(p[0], p[1], r * 2.4, 0, 7); ctx.fill();
      ctx.fillStyle = 'rgba(255,248,215,' + a + ')'; ctx.beginPath(); ctx.arc(p[0], p[1], r * 0.8, 0, 7); ctx.fill();
    });
    void now;
  }
  function drawHand(now) {
    if (!level || level.used > 0 || aim || !bag || level.idx > 0) return;
    var s = slingPt(), u = (now / 1600) % 1, k = u < 0.6 ? u / 0.6 : 1;
    var x = s.x - 120 * k, y = s.y + 50 * k;
    ctx.globalAlpha = u < 0.85 ? 1 : (1 - u) / 0.15;
    ctx.fillStyle = 'rgba(255,255,255,.95)'; ctx.strokeStyle = 'rgba(13,89,98,.9)'; ctx.lineWidth = 4;
    ctx.beginPath(); ctx.arc(x + 10, y + 14, 18, 0, 7); ctx.fill(); ctx.stroke();
    ctx.globalAlpha = 1;
  }
  function render(now) {
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.fillStyle = '#2a2418'; ctx.fillRect(0, 0, W, H);
    var sx = shake ? (Math.random() - 0.5) * shake : 0, sy = shake ? (Math.random() - 0.5) * shake : 0;
    ctx.setTransform(dpr * view.s, 0, 0, dpr * view.s, dpr * (view.ox + sx), dpr * (view.oy + sy));
    drawBg(now);
    if (!level) return;
    drawStreams(now);
    drawOaks(now);
    var bodies = Comp.allBodies(engine.world);
    bodies.forEach(function (b) { if (b.kind && b.kind !== 'bag' && !b.isStatic && b.position.y > cfg.world.ground - b.h) shadow(b.position.x, cfg.world.ground + 2, b.w * 0.55); });
    bodies.forEach(function (b) { if (b.kind && b.kind !== 'bag') drawBody(b, now); });
    props.forEach(function (p) { var im = img(p.n); if (!im) return; var h = 100, w = h * im.width / im.height; shadow(p.x, cfg.world.ground + 2, w * 0.45); ctx.drawImage(im, p.x - w / 2, cfg.world.ground - h + 6, w, h); });
    drawActors(now);
    if (level.def.tint) { ctx.save(); ctx.globalCompositeOperation = 'multiply'; ctx.fillStyle = level.def.tint.replace(/,[.\d]+\)$/, ',1)'); ctx.globalAlpha = parseFloat(level.def.tint.split(',').pop()); ctx.fillRect(-2000, -2000, 6000, 6000); ctx.restore(); }
    drawPreview(now);
    drawSling(now);
    bodies.forEach(function (b) {
      if (b.kind !== 'bag') return;
      var im = img('bag'), bh = 104, bw = bh * im.width / im.height;
      ctx.save(); ctx.translate(b.position.x, b.position.y); ctx.rotate(b.angle); ctx.drawImage(im, -bw / 2, -bh / 2, bw, bh); ctx.restore();
    });
    drawFx(now);
    drawHand(now);
    if (now < slow) { ctx.setTransform(dpr, 0, 0, dpr, 0, 0); var vg = ctx.createRadialGradient(W / 2, H / 2, H * 0.3, W / 2, H / 2, H); vg.addColorStop(0, 'rgba(0,0,0,0)'); vg.addColorStop(1, 'rgba(20,10,0,.35)'); ctx.fillStyle = vg; ctx.fillRect(0, 0, W, H); }
  }

  /* ---------- UI ---------- */
  function bump(id) { var el = $(id); el.classList.remove('pop'); void el.offsetWidth; el.classList.add('pop'); }
  function paintHud() {
    if (!level) return;
    $('lvlName').textContent = t('level', { n: fmt(level.idx + 1) }) + ' · ' + t('l' + level.def.id);
    var bp = $('bagsPill'); bp.innerHTML = '';
    for (var i = 0; i < level.def.bags; i++) { var im = document.createElement('img'); im.src = 'img/bag.webp'; im.alt = ''; if (i >= level.bagsLeft + (bag ? 0 : 0)) im.className = 'used'; bp.appendChild(im); }
    bp.setAttribute('aria-label', t('bags') + ' ' + level.bagsLeft);
    var wp = $('windPill');
    if (level.wind) { wp.hidden = false; var right = level.wind > 0; wp.textContent = t('wind') + ' ' + (right ? '→' : '←') + ' ' + fmt(Math.abs(level.wind) * 10) ; } else wp.hidden = true;
    $('cWater').textContent = litres(level.water);
    $('cStaff').textContent = hours(level.hours);
    $('cMoney').textContent = money(level.cost);
    $('sbTot').textContent = fmt(level.jars) + ' ' + t('jarsWord') + ' · ' + fmt(level.water, 2) + ' ' + t('litre') + ' · ' + mins(level.hours) + ' · ' + money(level.cost);
  }
  function mins(h) { return fmt(h * 60, 1) + ' ' + t('minute'); }
  function paintPer() {
    if (!per) return;
    $('sbPerK').textContent = t('perBag'); $('sbTotK').textContent = t('runTotal');
    $('sbW').textContent = fmt(per.water, 2) + ' ' + t('litre');
    $('sbS').textContent = mins(per.hours);
    $('sbM').textContent = fmt(Math.round(per.cost)) + ' ' + t('toman');
  }
  function show(id) { ['title', 'select', 'end', 'gate'].forEach(function (s) { $(s).hidden = s !== id; }); $('hud').hidden = !!id; $('savebar').hidden = !!id; $('rotate').classList.toggle('off', !!id); if (id !== 'gate') clearInterval(gateTimer); }
  /* ---------- replay gate ---------- */
  var gateTimer = 0, gateReturn = 'title';
  function gate() { return AB.gateStatus(cfg.gate); }
  function clock(ms) { var s = Math.ceil(ms / 1000), m = Math.floor(s / 60), r = s % 60, h = Math.floor(m / 60); m = m % 60; return (h ? fmt(h) + ':' + (m < 10 ? fmt(0) : '') : '') + fmt(m) + ':' + (r < 10 ? fmt(0) : '') + fmt(r); }
  function siteLinks() {
    var L = { fa: [['../about/', 'gAbout'], ['../products/', 'gProducts'], ['../csr/', 'gCsr'], ['../news/', 'gNews']],
      en: [['../en/about-us/', 'gAbout'], ['../en/products/', 'gProducts'], ['../en/csr/', 'gCsr'], ['../en/latest-news/', 'gNews']],
      ar: [['../arabic/%D9%85%D9%86-%D9%86%D8%AD%D9%86/', 'gAbout'], ['../arabic/%D9%85%D9%86%D8%AA%D8%AC%D8%A7%D8%AA/', 'gProducts'], ['../csr/', 'gCsr'], ['../arabic/%D8%A7%D9%84%D8%A7%D8%AE%D8%A8%D8%A7%D8%B1/', 'gNews']] }[lang];
    var box = $('gLinks'); box.innerHTML = '';
    L.forEach(function (x) { var a = document.createElement('a'); a.className = 'btn ghost'; a.href = x[0]; a.textContent = t(x[1]); box.appendChild(a); });
  }
  function paintGate() {
    var g = gate();
    if (!g.locked) { clearInterval(gateTimer); toast(t('unlocked')); show(gateReturn); return; }
    $('gHour').textContent = clock(g.leftWait);
    $('gBrowse').textContent = clock(g.browsed) + ' / ' + clock(g.browseNeed);
    $('gBar').style.width = Math.min(100, g.browsed / g.browseNeed * 100) + '%';
  }
  function openGate(from) {
    gateReturn = from || 'title'; siteLinks(); show('gate'); paintGate();
    clearInterval(gateTimer); gateTimer = setInterval(paintGate, 1000);
    track('gate_shown', {});
  }
  function startLevel(idx) {
    if (gate().locked) { openGate($('end').hidden ? 'title' : 'end'); return; }
    show(null); buildLevel(idx);
    var h = $('hint'); h.textContent = t('hintDrag'); h.hidden = level.idx > 0 && prog.stars[1] != null;
  }
  function endLevel(win) {
    if (level.over) return; level.over = true; aim = null;
    var L = level, stars = 0;
    if (win) { stars = 1; if (L.freed >= L.nursesTotal) stars++; if (L.used <= L.def.par) stars++; }
    if (win) {
      var id = L.def.id; prog.stars[id] = Math.max(prog.stars[id] || 0, stars);
      prog.unlocked = Math.max(prog.unlocked, Math.min(cfg.levels.length, L.idx + 2));
    }
    prog.total.water += L.water; prog.total.hours += L.hours; prog.total.cost += L.cost; prog.total.oaks += L.oaks;
    saveProg();
    var st = $('eStars'); st.innerHTML = '';
    for (var i = 0; i < 3; i++) { var s = document.createElement('span'); s.textContent = '★'; if (i < stars) s.className = 'on'; st.appendChild(s); }
    $('eTitle').textContent = win ? (L.idx === cfg.levels.length - 1 ? t('allDone') : t('win')) : t('lose');
    $('eOaksK').textContent = t('oaks'); $('eOaks').textContent = fmt(L.oaks);
    $('eWaterK').textContent = t('waterSaved'); $('eWater').textContent = litres(L.water);
    $('eStaffK').textContent = t('staffFreed'); $('eStaff').textContent = hours(L.hours);
    $('eMoneyK').textContent = t('moneySaved'); $('eMoney').textContent = money(L.cost);
    $('eNote').textContent = t('unitNote');
    var S = cfg.score;
    L.score = L.jars * S.perJar + L.freed * S.perNurse + L.oaks * S.perOak + stars * S.perStar + (win ? Math.max(0, L.bagsLeft) * S.perBagLeftOnWin : 0);
    L.stars = stars; L.win = win; L.ms = Math.round(performance.now() - L.start);
    $('eScore').textContent = fmt(L.score);
    var gated = !win || L.idx >= cfg.levels.length - 1; if (gated) AB.lockGate(); $('eGate').hidden = !gated; $('eGate').textContent = t('gEnd');
    paintEntry(); loadBoard();
    var nx = $('eNext'); nx.hidden = !win || L.idx >= cfg.levels.length - 1;
    setTimeout(function () { show('end'); $('hud').hidden = false; (nx.hidden ? $('eRetry') : nx).focus(); }, win ? 200 : 0);
    track(win ? 'level_win' : 'level_lose', { level: L.def.id, stars: stars, bags: L.used });
  }
  /* ---------- score entry + leaderboard ---------- */
  var api, submitted = false;
  function paintEntry() {
    submitted = false;
    var on = api.enabled() && level && level.used > 0;
    $('fSoon').hidden = on; $('fFields').hidden = !on; $('fSoon').textContent = t('fSoon');
    $('fMsg').textContent = ''; $('fMsg').className = 'ferr'; $('fSend').disabled = false;
  }
  function loadBoard() {
    var list = $('bList'); list.innerHTML = ''; $('bEmpty').textContent = '';
    if (!api.enabled()) { $('bEmpty').textContent = t('bSoon'); return; }
    api.board().then(function (r) {
      var rows = (r && r.ok && r.rows) || [];
      if (!rows.length) { $('bEmpty').textContent = t('bEmpty'); return; }
      rows.slice(0, 10).forEach(function (x) { var li = document.createElement('li'); var n = document.createElement('span'); n.textContent = String(x.name || '').slice(0, 24); var b = document.createElement('b'); b.textContent = fmt(+x.score || 0); li.appendChild(n); li.appendChild(b); list.appendChild(li); });
    }).catch(function () { $('bEmpty').textContent = t('errNet'); });
  }
  function onSubmit(e) {
    e.preventDefault();
    if (!api.enabled() || submitted || !level || !level.over) return;
    var msg = $('fMsg'), name = AB.cleanName($('fName').value), phone = AB.normPhone($('fPhone').value);
    msg.className = 'ferr';
    if (!name) { msg.textContent = t('errName'); $('fName').focus(); return; }
    if (!phone) { msg.textContent = t('errPhone'); $('fPhone').focus(); return; }
    if (!$('fConsent').checked) { msg.textContent = t('errConsent'); return; }
    var L = level; $('fSend').disabled = true; msg.textContent = t('sending');
    api.submit({ name: name, phone: phone, consent: true, lang: lang, level: L.def.id, win: !!L.win, jars: L.jars, nurses: L.freed, oaks: L.oaks, stars: L.stars, bagsLeft: Math.max(0, L.bagsLeft), bagsUsed: L.used, ms: L.ms, score: L.score })
      .then(function (r) {
        if (r && r.ok) { submitted = true; msg.className = 'fok'; msg.textContent = t('sent', { s: fmt(r.best || L.score) }); $('fPhone').value = ''; loadBoard(); track('score_submit', { level: L.def.id }); }
        else { $('fSend').disabled = false; msg.textContent = t(r && r.error === 'rate' ? 'errRate' : 'errServer'); }
      }).catch(function () { $('fSend').disabled = false; msg.textContent = t('errNet'); });
    $('fPhone').value = '';
  }
  function track(name, d) { try { window.dispatchEvent(new CustomEvent('abadis-slingshot', { detail: Object.assign({ event: name }, d) })); } catch (e) {} }
  function paintSelect() {
    var g = $('lgrid'); g.innerHTML = '';
    cfg.levels.forEach(function (L, i) {
      var b = document.createElement('button'); b.type = 'button'; b.className = 'lcard'; b.style.backgroundImage = 'url(img/bg' + L.bg + '.webp)';
      var lock = i + 1 > prog.unlocked; b.disabled = lock;
      var s = prog.stars[L.id] || 0;
      b.innerHTML = '<em>' + (lock ? '🔒' : '★★★'.slice(0, s) + '<span style="opacity:.35;position:static;background:none;padding:0">' + '★★★'.slice(0, 3 - s) + '</span>') + '</em><span>' + fmt(i + 1) + ' · ' + t('l' + L.id) + '</span>';
      b.setAttribute('aria-label', t('level', { n: i + 1 }) + ' ' + t('l' + L.id) + (lock ? ' ' + t('locked') : ''));
      b.addEventListener('click', function () { onFirstTap(); startLevel(i); });
      g.appendChild(b);
    });
  }
  function paintStatic() {
    document.title = t('title') + ' · ' + t('brand');
    $('tTitle').textContent = t('title'); $('tTag').textContent = t('tagline');
    $('playBtn').textContent = t('play'); $('levelsBtn').textContent = t('levels');
    $('sTitle').textContent = t('levels'); $('selBack').textContent = t('back');
    $('eNext').textContent = t('next'); $('eRetry').textContent = t('retry'); $('eReal').textContent = t('realSavings'); $('eZag').textContent = t('zagros'); $('eShare').textContent = t('share'); $('eLevels').textContent = t('levels');
    $('eReal').href = cfg.links.calculator; $('eZag').href = cfg.links.zagros;
    $('rotate').querySelector('span').textContent = t('rotate');
    $('menuBtn').setAttribute('aria-label', t('menu'));
    var hu = lang === 'en' ? '../en/' : lang === 'ar' ? '../arabic/' : '../';
    ['homeBtn', 'tHome', 'eHome'].forEach(function (id) { var a = $(id); if (a) { a.href = hu; a.setAttribute('aria-label', t('home')); } });
    $('tHome').textContent = '⌂ ' + t('home'); $('eHome').textContent = t('home');
    document.querySelectorAll('.lang[data-lang]').forEach(function (b) { b.setAttribute('aria-current', b.dataset.lang === lang ? 'true' : 'false'); });
    paintHud(); paintSelect(); paintPer();
    $('eScoreK').textContent = t('score'); $('fTitle').textContent = t('fTitle'); $('fName').placeholder = t('fName'); $('fPhone').placeholder = t('fPhone');
    $('fConsentT').textContent = t('fConsent'); $('fSend').textContent = t('fSend'); $('bTitle').textContent = t('bTitle'); $('fSoon').textContent = t('fSoon');
    $('gTitle').textContent = t('gTitle'); $('gBody').textContent = t('gBody'); $('gHourK').textContent = t('gHour'); $('gBrowseK').textContent = t('gBrowse'); $('gNote').textContent = t('gNote'); $('gBack').textContent = t('gBack'); $('eGate').textContent = t('gEnd');
    if (!$('gate').hidden) siteLinks();
  }
  function setLang(c) {
    lang = ['fa', 'en', 'ar'].indexOf(c) >= 0 ? c : 'fa';
    document.documentElement.lang = lang === 'fa' ? 'fa-IR' : lang;
    document.documentElement.dir = lang === 'en' ? 'ltr' : 'rtl';
    try { localStorage.setItem('abadis-slingshot-lang', lang); } catch (e) {}
    paintStatic();
  }
  function toast(m) { var e = $('toast'); e.textContent = m; e.classList.add('on'); setTimeout(function () { e.classList.remove('on'); }, 2200); }
  function share() {
    var url = location.href.split('?')[0], txt = t('shareText', { l: fmt(Math.round(prog.total.water)), o: fmt(prog.total.oaks) });
    if (navigator.share) navigator.share({ title: t('title'), text: txt, url: url }).catch(function () {});
    else if (navigator.clipboard) navigator.clipboard.writeText(txt + ' ' + url).then(function () { toast(t('copied')); }, function () {});
    track('share', {});
  }
  function bind() {
    canvas.addEventListener('pointerdown', onDown);
    window.addEventListener('pointermove', onMove);
    window.addEventListener('pointerup', onUp);
    window.addEventListener('pointercancel', function () { aim = null; if (bag) { var s = slingPt(); bag.x = s.x; bag.y = s.y; } });
    window.addEventListener('resize', resize);
    document.addEventListener('pointerdown', onFirstTap, { once: true });
    $('playBtn').addEventListener('click', function () { onFirstTap(); var n = 0; for (var i = 0; i < cfg.levels.length; i++) if (prog.stars[cfg.levels[i].id] == null) { n = i; break; } else n = i; startLevel(Math.min(n, prog.unlocked - 1)); });
    $('levelsBtn').addEventListener('click', function () { paintSelect(); show('select'); });
    $('selBack').addEventListener('click', function () { show('title'); });
    $('eNext').addEventListener('click', function () { startLevel(level.idx + 1); });
    $('eRetry').addEventListener('click', function () { startLevel(level.idx); });
    $('eLevels').addEventListener('click', function () { paintSelect(); show('select'); });
    $('eShare').addEventListener('click', share);
    $('entry').addEventListener('submit', onSubmit);
    $('gBack').addEventListener('click', function () { show(gateReturn); });
    $('fPhone').addEventListener('input', function () { var v = AB.toLatinDigits(this.value); if (v !== this.value) this.value = v; });
    $('eReal').addEventListener('click', function () { track('cta_calculator', {}); });
    $('eZag').addEventListener('click', function () { track('cta_zagros', {}); });
    $('menuBtn').addEventListener('click', function () { aim = null; paintSelect(); show('select'); });
    $('soundBtn').addEventListener('click', function (e) { e.stopPropagation(); firstTap = true; setSound(!soundOn); });
    document.querySelectorAll('.lang[data-lang]').forEach(function (b) { b.addEventListener('click', function () { setLang(b.dataset.lang); }); });
    document.addEventListener('visibilitychange', function () { lastT = performance.now(); });
  }
  function frame(now) {
    var dt = Math.min(50, now - (lastT || now)); lastT = now;
    if (level && !level.over || (level && level.over)) {
      acc += dt; var n = 0;
      while (acc >= 1000 / 60 && n < 4) { step(1000 / 60, now); acc -= 1000 / 60; n++; }
      if (n === 4) acc = 0;
    }
    updateFx(dt, now);
    render(now);
    frames++; if (now - fpsT > 1000) { fps = frames * 1000 / (now - fpsT); frames = 0; fpsT = now; }
    requestAnimationFrame(frame);
  }
  function loadImages(names) {
    return Promise.all(names.map(function (n) { return new Promise(function (res) { var im = new Image(); im.onload = function () { IMG[n] = im; res(); }; im.onerror = function () { errors.push('img ' + n); res(); }; im.src = 'img/' + n + '.webp'; }); }));
  }
  window.__SS = {
    get fps() { return fps; }, get level() { return level; }, get prog() { return prog; }, get per() { return per; },
    view: function () { return view; }, sling: function () { return slingPt(); }, hasBag: function () { return !!bag; }, flying: function () { return !!flying; },
    bodies: function () { return Comp.allBodies(engine.world).filter(function (b) { return b.kind; }).map(function (b) { return { kind: b.kind, x: b.position.x, y: b.position.y }; }); },
    start: function (i) { startLevel(i); }, end: function (w) { endLevel(!!w); }, gate: function () { return gate(); }
  };
  function boot() {
    Promise.all([fetch('config.json').then(function (r) { return r.json(); }), fetch('i18n.json').then(function (r) { return r.json(); })]).then(function (r) {
      cfg = r[0]; i18n = r[1];
      var f = cfg.formula;
      per = { water: f.waterLitres[0] * f.waterLitres[1], cost: f.costToman[0] * f.costToman[1], hours: f.staffHours.minutes / 60 * f.staffHours.k1 * f.staffHours.k2 };
      prog = loadProg(); api = new AB.Api(cfg.leaderboard);
      var q = new URLSearchParams(location.search).get('lang'), st = null; try { st = localStorage.getItem('abadis-slingshot-lang'); } catch (e) {}
      resize(); bind(); setLang(q || st || 'fa');
      level = null;
      return loadImages(['bg1']).then(function () {
        requestAnimationFrame(frame);
        return loadImages(['bg2', 'bg3', 'bg4', 'bg5', 'fork', 'pouch', 'bag', 'jar1', 'jar2', 'jar3', 'bucket', 'can', 'sink', 'plank', 'crate', 'stone', 'boulder', 'nurse_wash', 'nurse_wave', 'nurse_walk', 'acorn', 'sprout', 'sapling', 'oak', 'splash']);
      });
    }).catch(function (e) { errors.push(String(e)); $('tTag').textContent = 'Failed to load.'; });
  }
  boot();
})();
