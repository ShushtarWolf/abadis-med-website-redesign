/* Sample-only behaviour for the news-hero previews. */
(function () {
  var digits = '۰۱۲۳۴۵۶۷۸۹';
  function fa(n) { return String(n).replace(/\d/g, function (d) { return digits[d]; }); }
  function norm(s) {
    return String(s || '').replace(/\u200c/g, '').replace(/ي/g, 'ی').replace(/ك/g, 'ک').toLowerCase();
  }

  document.querySelectorAll('[data-nho-tabs]').forEach(function (root) {
    var tabs = root.querySelectorAll('[role="tab"]');
    var panels = root.querySelectorAll('[data-panel]');
    function show(id) {
      tabs.forEach(function (tab) {
        var on = tab.getAttribute('data-panel-id') === id;
        tab.setAttribute('aria-selected', on ? 'true' : 'false');
      });
      panels.forEach(function (panel) {
        panel.classList.toggle('is-on', panel.getAttribute('data-panel') === id);
      });
    }
    tabs.forEach(function (tab) {
      tab.addEventListener('click', function () { show(tab.getAttribute('data-panel-id')); });
    });
  });

  document.querySelectorAll('[data-nho-slider]').forEach(function (root) {
    var slides = [].slice.call(root.querySelectorAll('[data-slide]'));
    var dots = [].slice.call(root.querySelectorAll('[data-dot]'));
    var i = 0;
    var timer = 0;
    function show(n) {
      i = (n + slides.length) % slides.length;
      slides.forEach(function (slide, k) { slide.classList.toggle('is-on', k === i); });
      dots.forEach(function (dot, k) {
        var on = k === i;
        dot.setAttribute('aria-current', on ? 'true' : 'false');
        if (on) {
          dot.style.animation = 'none';
          void dot.offsetWidth;
          dot.style.animation = '';
        }
      });
    }
    function stop() { if (timer) clearInterval(timer); timer = 0; }
    function play() {
      stop();
      if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
      timer = setInterval(function () { show(i + 1); }, 7000);
    }
    var next = root.querySelector('[data-next]');
    var prev = root.querySelector('[data-prev]');
    if (next) next.addEventListener('click', function () { show(i + 1); });
    if (prev) prev.addEventListener('click', function () { show(i - 1); });
    dots.forEach(function (dot, k) { dot.addEventListener('click', function () { show(k); }); });
    root.addEventListener('mouseenter', stop);
    root.addEventListener('mouseleave', play);
    root.addEventListener('focusin', stop);
    root.addEventListener('focusout', function (e) { if (!root.contains(e.relatedTarget)) play(); });
    show(0);
    play();
  });

  document.querySelectorAll('[data-nho-quiet]').forEach(function (root) {
    var pills = root.querySelectorAll('[data-quiet]');
    var rows = root.querySelectorAll('[data-quiet-row]');
    pills.forEach(function (pill) {
      pill.addEventListener('click', function () {
        var key = pill.getAttribute('data-quiet');
        pills.forEach(function (p) { p.setAttribute('aria-pressed', p === pill ? 'true' : 'false'); });
        var shown = 0;
        rows.forEach(function (row) {
          var topics = (row.getAttribute('data-topics') || '').split(/\s+/);
          var hide = key === 'all' ? row.getAttribute('data-primary') === '0' : topics.indexOf(key) === -1;
          row.hidden = hide;
          if (!hide) shown += 1;
        });
        var wall = root.querySelector('[data-quiet-wall]');
        if (wall) wall.classList.toggle('is-solo', shown === 1);
      });
    });
  });

  var hub = document.querySelector('[data-nho-hub]');
  if (hub) {
    var raw = document.getElementById('nho9-data');
    var items = raw ? JSON.parse(raw.textContent) : [];
    var input = hub.querySelector('input');
    var chips = hub.querySelectorAll('[data-chip]');
    var list = hub.querySelector('[data-hub-list]');
    var feature = hub.querySelector('[data-hub-feature]');
    var empty = hub.querySelector('[data-hub-empty]');
    var chip = 'all';
    function topicsOf(item) { return item.topics || []; }
    function match(item, q) {
      var okChip = chip === 'all' || topicsOf(item).indexOf(chip) !== -1;
      if (!okChip) return false;
      if (!q) return true;
      return norm(item.title).indexOf(norm(q)) !== -1;
    }
    function paint() {
      var q = input ? input.value.trim() : '';
      var found = items.filter(function (item) { return match(item, q); });
      if (feature && found[0]) {
        feature.hidden = false;
        feature.href = '../../news/' + found[0].id + '/';
        feature.querySelector('img').src = found[0].img;
        feature.querySelector('img').alt = found[0].title;
        feature.querySelector('time').textContent = found[0].date;
        feature.querySelector('time').setAttribute('datetime', found[0].iso);
        feature.querySelector('h2').textContent = found[0].title;
        feature.querySelector('p').textContent = found[0].excerpt;
      }
      var showList = q || chip !== 'all';
      if (list) {
        list.hidden = !showList;
        list.innerHTML = '';
        found.slice(0, 5).forEach(function (item) {
          var li = document.createElement('li');
          var a = document.createElement('a');
          a.href = '../../news/' + item.id + '/';
          var strong = document.createElement('strong');
          strong.textContent = item.title;
          var time = document.createElement('time');
          time.textContent = item.date;
          time.setAttribute('datetime', item.iso);
          a.appendChild(strong);
          a.appendChild(time);
          li.appendChild(a);
          list.appendChild(li);
        });
      }
      if (empty) empty.hidden = found.length !== 0;
      var live = hub.querySelector('[data-hub-count]');
      if (live) live.textContent = fa(found.length) + ' خبر';
    }
    chips.forEach(function (button) {
      button.addEventListener('click', function () {
        chip = button.getAttribute('data-chip');
        chips.forEach(function (b) { b.setAttribute('aria-pressed', b === button ? 'true' : 'false'); });
        paint();
      });
    });
    if (input) input.addEventListener('input', paint);
    var form = hub.querySelector('form');
    if (form) form.addEventListener('submit', function (e) { e.preventDefault(); paint(); });
  }
})();

/* Bento filters for option 2. */
(function () {
  var root = document.querySelector('[data-nho-filter]');
  if (!root) return;
  var pills = root.querySelectorAll('[data-nho-pill]');
  var cards = root.querySelectorAll('[data-nho-card]');
  var empty = root.querySelector('[data-nho-empty]');
  var count = root.querySelector('[data-nho-count]');
  var digits = '۰۱۲۳۴۵۶۷۸۹';
  function fa(n) {
    return String(n).replace(/\d/g, function (d) { return digits[d]; });
  }
  function apply(key) {
    var n = 0;
    cards.forEach(function (card) {
      var topics = (card.getAttribute('data-topics') || '').split(/\s+/);
      var year = card.getAttribute('data-year') || '';
      var show = key === 'all' || topics.indexOf(key) !== -1 || year === key;
      card.hidden = !show;
      if (show) n += 1;
    });
    if (empty) empty.hidden = n !== 0;
    if (count) count.textContent = fa(n) + ' خبر';
    pills.forEach(function (pill) {
      pill.setAttribute('aria-pressed', pill.getAttribute('data-nho-pill') === key ? 'true' : 'false');
    });
  }
  pills.forEach(function (pill) {
    pill.addEventListener('click', function () {
      apply(pill.getAttribute('data-nho-pill'));
    });
  });
})();
