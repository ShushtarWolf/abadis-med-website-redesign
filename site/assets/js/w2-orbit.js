/* W2-2 live orbit: scroll-in draw, node / pill detail, auto-cycle, replay. */
(function () {
  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function fit(root) {
    var fitEl = root.querySelector('.w2-stage-fit');
    var stage = root.querySelector('.orb-stage--w2');
    if (!fitEl || !stage) return;
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
      panel.querySelector('[data-role="stem-pill"]').textContent = stems[activeStem] || stems.long || '';
      panel.querySelector('[data-role="h3"]').textContent = info.h3;
      panel.querySelector('[data-role="p"]').textContent = info.p;
      panel.querySelector('[data-role="kpis"]').innerHTML = (info.kpis || []).map(function (k) {
        return '<div class="w2-kpi"><b>' + esc(k[0]) + '</b><span>' + esc(k[1]) + '</span></div>';
      }).join('');
      panel.querySelector('[data-role="bar-a-label"]').textContent = info.bar_a_label;
      panel.querySelector('[data-role="bar-a-val"]').textContent = info.bar_a_val;
      panel.querySelector('[data-role="bar-a-fill"]').style.width = info.bar_a_pct + '%';
      panel.querySelector('[data-role="bar-b-label"]').textContent = info.bar_b_label;
      panel.querySelector('[data-role="bar-b-val"]').textContent = info.bar_b_val;
      panel.querySelector('[data-role="bar-b-fill"]').style.width = info.bar_b_pct + '%';
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

    function fitLabels() {
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

    fit(root);
    fitLabels();
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(fitLabels);
    window.addEventListener('resize', function () { fit(root); fitLabels(); });
    root._w2Stop = function () { if (timer) clearInterval(timer); };
  }

  function init() {
    document.querySelectorAll('.w2-live').forEach(boot);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
