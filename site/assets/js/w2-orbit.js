/* W2-2 live orbit: scroll-in draw, node / pill detail, auto-cycle, replay. */
(function () {
  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function phoneMq() {
    return window.matchMedia('(max-width: 480px)').matches;
  }

  function rememberStyle(el) {
    if (!el || el.dataset.w2style != null) return;
    el.dataset.w2style = el.getAttribute('style') || '';
  }

  function restoreStyle(el) {
    if (!el || el.dataset.w2style == null) return;
    el.setAttribute('style', el.dataset.w2style);
  }

  function numFromStyle(style, key) {
    var m = new RegExp(key + ':\\s*([\\d.]+)').exec(style || '');
    return m ? parseFloat(m[1]) : 0;
  }

  /* Phone orbit: same rays and draw, retargeted to a stage that fits the
     viewport. Bubble boxes stay clear of each other and of the hub. */
  function solvePhone(W) {
    var pad = 3;
    var gap = 4;
    var angs = [];
    var i;
    for (i = 0; i < 8; i++) angs.push((-135 + i * 45) * Math.PI / 180);
    var sizes = [108, 104, 100, 96, 92, 88, 84, 80, 76];
    var hubs = [92, 84, 76, 68];
    var si, hi, H, D, hub, r, hr, cx, cy, rx, ry, pts, ok, p, q, j;
    for (si = 0; si < sizes.length; si++) {
      D = sizes[si];
      if (D > W - 36) continue;
      for (hi = 0; hi < hubs.length; hi++) {
        hub = hubs[hi];
        r = D / 2;
        hr = hub / 2;
        for (H = Math.round(W * 1.22); H <= Math.round(W * 2.35); H++) {
          cx = W / 2;
          cy = H / 2;
          rx = W / 2 - r - pad;
          ry = H / 2 - r - pad;
          if (rx < 28 || ry < 28) continue;
          pts = [];
          for (i = 0; i < 8; i++) {
            var c = Math.cos(angs[i]);
            var s = Math.sin(angs[i]);
            var t = 1 / Math.sqrt((c / rx) * (c / rx) + (s / ry) * (s / ry));
            pts.push({ x: cx + t * c, y: cy + t * s, a: angs[i] });
          }
          ok = true;
          for (i = 0; i < 8 && ok; i++) {
            p = pts[i];
            if (p.x - r < pad || p.x + r > W - pad || p.y - r < pad || p.y + r > H - pad) ok = false;
            if (Math.abs(p.x - cx) < hr + r + gap && Math.abs(p.y - cy) < hr + r + gap) ok = false;
            for (j = i + 1; j < 8 && ok; j++) {
              q = pts[j];
              if (Math.abs(p.x - q.x) < D + gap && Math.abs(p.y - q.y) < D + gap) ok = false;
            }
          }
          if (ok) return { W: W, H: H, D: D, hub: hub, cx: cx, cy: cy, rx: rx, ry: ry, pts: pts };
        }
      }
    }
    return null;
  }

  function round1(n) { return Math.round(n * 10) / 10; }

  function layoutPhone(root) {
    var fitEl = root.querySelector('.w2-stage-fit');
    var stage = root.querySelector('.orb-stage--w2');
    var svg = stage && stage.querySelector('.orb-svg');
    var hub = stage && stage.querySelector('.orb-hub');
    if (!fitEl || !stage || !svg || !hub) return;
    rememberStyle(stage);
    rememberStyle(hub);
    stage.querySelectorAll('.orb-node').forEach(rememberStyle);
    if (svg.dataset.w2html == null) {
      svg.dataset.w2html = svg.innerHTML;
      svg.dataset.w2vb = svg.getAttribute('viewBox') || '0 0 640 610';
    }
    var W = Math.max(260, Math.round(fitEl.clientWidth));
    if (W > 480) W = 480;
    var geom = solvePhone(W);
    if (!geom) return;
    var key = geom.W + 'x' + geom.H + 'x' + geom.D;
    root.classList.add('is-phone');
    fitEl.style.overflow = 'hidden';
    fitEl.style.maxWidth = '100%';
    stage.style.zoom = '';
    stage.style.width = geom.W + 'px';
    stage.style.height = geom.H + 'px';
    hub.style.width = geom.hub + 'px';
    hub.style.height = geom.hub + 'px';
    hub.style.left = round1(geom.cx - geom.hub / 2) + 'px';
    hub.style.top = round1(geom.cy - geom.hub / 2) + 'px';

    var hubStyle = hub.dataset.w2style || '';
    var hcx = numFromStyle(hubStyle, 'left') + numFromStyle(hubStyle, 'width') / 2;
    var hcy = numFromStyle(hubStyle, 'top') + numFromStyle(hubStyle, 'height') / 2;
    var buttons = Array.prototype.slice.call(stage.querySelectorAll('.orb-node'));
    buttons.sort(function (a, b) {
      var as = a.dataset.w2style, bs = b.dataset.w2style;
      var aa = Math.atan2(numFromStyle(as, 'top') + numFromStyle(as, 'height') / 2 - hcy, numFromStyle(as, 'left') + numFromStyle(as, 'width') / 2 - hcx);
      var bb = Math.atan2(numFromStyle(bs, 'top') + numFromStyle(bs, 'height') / 2 - hcy, numFromStyle(bs, 'left') + numFromStyle(bs, 'width') / 2 - hcx);
      return aa - bb;
    });
    buttons.forEach(function (btn, i) {
      var p = geom.pts[i];
      btn.style.width = geom.D + 'px';
      btn.style.height = geom.D + 'px';
      btn.style.left = round1(p.x - geom.D / 2) + 'px';
      btn.style.top = round1(p.y - geom.D / 2) + 'px';
    });

    if (root.dataset.w2geom === key) return;
    root.dataset.w2geom = key;
    var defs = svg.querySelector('defs');
    var html = defs ? defs.outerHTML : '';
    function ellipsePt(scale, ang) {
      var c = Math.cos(ang), s = Math.sin(ang);
      var rx = geom.rx * scale, ry = geom.ry * scale;
      var t = 1 / Math.sqrt((c / rx) * (c / rx) + (s / ry) * (s / ry));
      return [geom.cx + t * c, geom.cy + t * s];
    }
    [1, 0.72, 0.46].forEach(function (scale, n) {
      var cls = n === 0 ? 'orbit-long' : n === 1 ? 'orbit-med' : 'orbit-short';
      html += '<ellipse cx="' + round1(geom.cx) + '" cy="' + round1(geom.cy) + '" rx="' + round1(geom.rx * scale) + '" ry="' + round1(geom.ry * scale) + '" class="orbit-guide ' + cls + '" stroke-dasharray="' + (n === 0 ? '10 9' : n === 1 ? '7 8' : '4 7') + '"/>';
    });
    html += '<g class="arc-sweep-group">';
    for (var a = 0; a < 8; a++) {
      var a1 = geom.pts[a].a;
      var a2 = geom.pts[(a + 1) % 8].a;
      if (a2 <= a1) a2 += Math.PI * 2;
      var p1 = ellipsePt(0.84, a1);
      var p2 = ellipsePt(0.84, a2);
      html += '<path d="M ' + round1(p1[0]) + ' ' + round1(p1[1]) + ' A ' + round1(geom.rx * 0.84) + ' ' + round1(geom.ry * 0.84) + ' 0 0 1 ' + round1(p2[0]) + ' ' + round1(p2[1]) + '" pathLength="1" class="grow-arc" style="--ai:' + a + '"/>';
      html += '<circle cx="' + round1(p1[0]) + '" cy="' + round1(p1[1]) + '" r="3.4" class="arc-tip-dot" style="--ai:' + a + '"/>';
    }
    html += '</g>';
    buttons.forEach(function (btn) {
      var idx = btn.getAttribute('data-idx');
      var stem = btn.getAttribute('data-stem') || 'long';
      var order = btn.style.getPropertyValue('--i') || '0';
      var bx = parseFloat(btn.style.left) + geom.D / 2;
      var by = parseFloat(btn.style.top) + geom.D / 2;
      var ang = Math.atan2(by - geom.cy, bx - geom.cx);
      var c = Math.cos(ang), s = Math.sin(ang);
      var x1 = geom.cx + c * (geom.hub / 2 + 2);
      var y1 = geom.cy + s * (geom.hub / 2 + 2);
      var x2 = bx - c * (geom.D / 2 - 2);
      var y2 = by - s * (geom.D / 2 - 2);
      var d = 'M ' + round1(x1) + ' ' + round1(y1) + ' L ' + round1(x2) + ' ' + round1(y2);
      html += '<g class="stem-group stem-' + stem + '" data-idx="' + idx + '" style="--i:' + order + '">'
        + '<path d="' + d + '" pathLength="1" class="stem-base"/>'
        + '<path d="' + d + '" pathLength="1" class="stem-glow" filter="url(#glow-w2)"/>'
        + '<path d="' + d + '" pathLength="1" class="stem-pulse"/>'
        + '<circle cx="' + round1(x1) + '" cy="' + round1(y1) + '" r="3.6" class="stem-root-dot"/>'
        + '<circle cx="' + round1(x2) + '" cy="' + round1(y2) + '" r="4.2" class="stem-tip-dot"/>'
        + '</g>';
    });
    svg.setAttribute('viewBox', '0 0 ' + geom.W + ' ' + geom.H);
    svg.innerHTML = html;
    var active = stage.querySelector('.orb-node.is-active');
    var activeIdx = active ? active.getAttribute('data-idx') : '0';
    stage.querySelectorAll('.stem-group').forEach(function (g) {
      g.classList.toggle('is-active', g.getAttribute('data-idx') === activeIdx);
    });
  }

  function restoreDesktop(root) {
    if (!root.classList.contains('is-phone') && root.dataset.w2geom == null) return;
    root.classList.remove('is-phone');
    root.dataset.w2geom = '';
    var stage = root.querySelector('.orb-stage--w2');
    if (!stage) return;
    restoreStyle(stage);
    stage.style.zoom = '';
    restoreStyle(stage.querySelector('.orb-hub'));
    stage.querySelectorAll('.orb-node').forEach(restoreStyle);
    var svg = stage.querySelector('.orb-svg');
    if (svg && svg.dataset.w2html != null) {
      svg.innerHTML = svg.dataset.w2html;
      svg.setAttribute('viewBox', svg.dataset.w2vb || '0 0 640 610');
    }
    root.querySelectorAll('.orb-node-title, .orb-node-stat').forEach(function (el) {
      el.style.fontSize = '';
    });
  }

  function fit(root) {
    var fitEl = root.querySelector('.w2-stage-fit');
    var stage = root.querySelector('.orb-stage--w2');
    if (!fitEl || !stage) return;
    if (phoneMq()) {
      layoutPhone(root);
      return;
    }
    restoreDesktop(root);
    fitEl.style.overflow = 'hidden';
    fitEl.style.maxWidth = '100%';
    var avail = fitEl.clientWidth;
    if (!avail) return;
    var z = Math.min(1, avail / 640);
    stage.style.zoom = String(z);
  }

  function boot(root) {
    var raw = root.querySelector('.w2-data');
    if (!raw) return;
    var data = JSON.parse(raw.textContent);
    var nodes = data.nodes || [];
    var stems = data.stems || {};
    var idx = 0;
    var paused = false;
    var seen = false;
    var timer = 0;

    function apply(i) {
      var info = nodes[i] || nodes[0];
      if (!info) return;
      idx = i;
      var activeStem = 'long';
      root.querySelectorAll('.orb-node').forEach(function (btn) {
        var on = Number(btn.getAttribute('data-idx')) === i;
        btn.classList.toggle('is-active', on);
        if (on) activeStem = btn.getAttribute('data-stem') || 'long';
      });
      root.querySelectorAll('.stem-group').forEach(function (g) {
        g.classList.toggle('is-active', Number(g.getAttribute('data-idx')) === i);
      });
      root.querySelectorAll('.strip-pill').forEach(function (p) {
        var on = Number(p.getAttribute('data-idx')) === i;
        p.classList.toggle('is-active', on);
        if (on) p.setAttribute('aria-current', 'true');
        else p.removeAttribute('aria-current');
      });
      var panel = root.querySelector('.w2-detail-panel');
      if (!panel) return;
      panel.querySelector('[data-role="tag"]').textContent = info.tag;
      var stemEl = panel.querySelector('[data-role="stem-pill"]'); if (stemEl) stemEl.textContent = stems[activeStem] || stems.long || '';
      panel.querySelector('[data-role="h3"]').textContent = info.h3;
      panel.querySelector('[data-role="p"]').textContent = info.p;
      var kpisEl = panel.querySelector('[data-role="kpis"]');
      var kpisArr = info.kpis || [];
      kpisEl.setAttribute('data-kpi-count', String(kpisArr.length));
      kpisEl.innerHTML = kpisArr.map(function (k) {
        return k[1] ? '<div class="w2-kpi"><b>' + esc(k[0]) + '</b><span>' + esc(k[1]) + '</span></div>' : '<div class="w2-kpi w2-kpi--single"><b>' + esc(k[0]) + '</b></div>';
      }).join('');
      panel.querySelector('[data-role="bar-a-label"]').textContent = info.bar_a_label;
      panel.querySelector('[data-role="bar-a-val"]').textContent = info.bar_a_val;
      panel.querySelector('[data-role="bar-a-fill"]').style.width = info.bar_a_pct + '%';
      panel.querySelector('[data-role="bar-b-label"]').textContent = info.bar_b_label;
      panel.querySelector('[data-role="bar-b-val"]').textContent = info.bar_b_val;
      panel.querySelector('[data-role="bar-b-fill"]').style.width = info.bar_b_pct + '%';
      if (root.classList.contains('is-phone')) {
        var statEl = panel.querySelector('[data-role="stat"]');
        if (!statEl) {
          statEl = document.createElement('p');
          statEl.className = 'w2-node-statline';
          statEl.setAttribute('data-role', 'stat');
          var h3 = panel.querySelector('[data-role="h3"]');
          if (h3) h3.insertAdjacentElement('afterend', statEl);
        }
        statEl.textContent = info.stat || '';
      }
      panel.classList.remove('is-rippling');
      void panel.offsetWidth;
      panel.classList.add('is-rippling');
    }

    function replay() {
      var stage = root.querySelector('.orb-stage--w2');
      if (!stage) return;
      stage.classList.remove('is-animated');
      void stage.offsetWidth;
      stage.classList.add('is-animated');
    }

    root.querySelectorAll('.orb-node, .strip-pill').forEach(function (el) {
      el.addEventListener('click', function () {
        apply(Number(el.getAttribute('data-idx')));
      });
      el.addEventListener('mouseenter', function () {
        apply(Number(el.getAttribute('data-idx')));
      });
    });
    root.addEventListener('mouseenter', function () { paused = true; });
    root.addEventListener('mouseleave', function () { paused = false; });
    root.addEventListener('focusin', function () { paused = true; });
    root.addEventListener('focusout', function (e) {
      if (!root.contains(e.relatedTarget)) paused = false;
    });
    var replayBtn = root.querySelector('[data-w2-replay]');
    if (replayBtn) {
      replayBtn.addEventListener('click', function (e) {
        e.preventDefault();
        replay();
      });
    }

    var stage = root.querySelector('.orb-stage--w2');
    if (stage && 'IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (!en.isIntersecting) return;
          seen = true;
          if (!stage.classList.contains('is-animated')) stage.classList.add('is-animated');
        });
      }, { threshold: 0.28 });
      io.observe(stage);
    } else if (stage) {
      seen = true;
      stage.classList.add('is-animated');
    }

    if (!/[?&]shot=1(?:&|$)/.test(location.search)) {
      timer = setInterval(function () {
        if (paused || !seen) return;
        apply((idx + 1) % nodes.length);
      }, 4600);
    }

    function wordWidth(sample, px, cs) {
      var probe = wordWidth.el;
      if (!probe) {
        probe = document.createElement('span');
        probe.style.cssText = 'position:absolute;visibility:hidden;white-space:nowrap;left:0;top:0;pointer-events:none;letter-spacing:0;';
        document.body.appendChild(probe);
        wordWidth.el = probe;
      }
      probe.style.fontFamily = cs.fontFamily;
      probe.style.fontWeight = cs.fontWeight;
      probe.style.fontSize = px + 'px';
      probe.textContent = sample;
      return probe.getBoundingClientRect().width;
    }

    function textSpills(btn) {
      var b = btn.getBoundingClientRect();
      if (!b.width) return false;
      var cx = b.left + b.width / 2;
      var cy = b.top + b.height / 2;
      var rad = b.width / 2 - 3;
      var parts = btn.querySelectorAll('.orb-node-num, .orb-node-title');
      for (var i = 0; i < parts.length; i++) {
        var r = parts[i].getBoundingClientRect();
        var corners = [[r.left, r.top], [r.right, r.top], [r.left, r.bottom], [r.right, r.bottom]];
        for (var c = 0; c < 4; c++) {
          if (Math.hypot(corners[c][0] - cx, corners[c][1] - cy) > rad + 0.8) return true;
        }
      }
      return false;
    }

    function fitLabels() {
      if (root.classList.contains('is-phone')) {
        var info = nodes[idx] || nodes[0];
        if (info) {
          var panel = root.querySelector('.w2-detail-panel');
          var statEl = panel && panel.querySelector('[data-role="stat"]');
          if (!statEl && panel) {
            statEl = document.createElement('p');
            statEl.className = 'w2-node-statline';
            statEl.setAttribute('data-role', 'stat');
            var h3 = panel.querySelector('[data-role="h3"]');
            if (h3) h3.insertAdjacentElement('afterend', statEl);
          }
          if (statEl) statEl.textContent = info.stat || '';
        }
        root.querySelectorAll('.orb-node').forEach(function (btn) {
          var title = btn.querySelector('.orb-node-title');
          if (!title) return;
          title.style.fontSize = '';
          var cs = getComputedStyle(title);
          var words = (title.textContent || '').trim().split(/\s+/).filter(Boolean);
          var limit = btn.clientWidth * 0.70;
          var size = 13;
          while (size > 10 && words.some(function (w) { return wordWidth(w, size, cs) > limit; })) size -= 0.25;
          title.style.fontSize = size.toFixed(2) + 'px';
          var guard = 0;
          while (textSpills(btn) && size > 9 && guard < 12) {
            size -= 0.25;
            title.style.fontSize = size.toFixed(2) + 'px';
            guard++;
          }
        });
        return;
      }
      root.querySelectorAll('.orb-node').forEach(function (btn) {
        var inner = btn.querySelector('.orb-node-inner');
        var title = btn.querySelector('.orb-node-title');
        var stat = btn.querySelector('.orb-node-stat');
        if (!inner || !title) return;
        title.style.fontSize = '';
        if (stat) stat.style.fontSize = '';
        var limit = btn.clientHeight - 16;
        var size = parseFloat(getComputedStyle(title).fontSize) || 10;
        var guard = 0;
        while (inner.scrollHeight > limit && size > 7 && guard < 10) {
          size -= 0.35;
          title.style.fontSize = size.toFixed(2) + 'px';
          if (stat) stat.style.fontSize = Math.max(6.8, size - 1.2).toFixed(2) + 'px';
          guard++;
        }
      });
    }

    function refit() { fit(root); fitLabels(); }
    refit();
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(fitLabels);
    window.addEventListener('resize', refit);
    if (window.matchMedia) {
      var mq = window.matchMedia('(max-width: 480px)');
      if (mq.addEventListener) mq.addEventListener('change', refit);
    }
    root._w2Stop = function () { if (timer) clearInterval(timer); };
  }

  function init() {
    document.querySelectorAll('.w2-live').forEach(boot);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
