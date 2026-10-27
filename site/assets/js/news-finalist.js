/* Finalist D: topic tags and year pills filter the news grid and the lead card. */
(function () {
  'use strict';
  function digitsOf(lang) {
    if (lang === 'en') return null;
    return lang === 'ar' ? '٠١٢٣٤٥٦٧٨٩' : '۰۱۲۳۴۵۶۷۸۹';
  }
  function fmt(n, lang) {
    var s = String(n);
    var map = digitsOf(lang);
    if (!map) return s.replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    var out = '';
    for (var i = 0; i < s.length; i++) {
      if (i && (s.length - i) % 3 === 0) out += '٬';
      out += map.charAt(+s.charAt(i));
    }
    return out;
  }
  function langOf() {
    var l = document.documentElement.lang || 'fa';
    if (l.indexOf('en') === 0) return 'en';
    if (l.indexOf('ar') === 0) return 'ar';
    return 'fa';
  }

  document.querySelectorAll('[data-news-finalist]').forEach(function (root) {
    var lang = langOf();
    var topic = 'all';
    var year = 'all';
    var grid = document.getElementById('postGrid');
    if (!grid) return;
    var cards = [].slice.call(grid.querySelectorAll('.post-card'));
    var feature = root.querySelector('[data-news-feature]');
    var kicker = root.querySelector('[data-news-kicker]');
    var countEl = root.querySelector('[data-news-count]');
    var empty = document.querySelector('[data-news-empty]');
    var labels = {};
    root.querySelectorAll('[data-news-topic]').forEach(function (btn) {
      var key = btn.getAttribute('data-news-topic');
      var text = btn.childNodes[0] ? btn.childNodes[0].textContent : btn.textContent;
      labels[key] = (text || '').trim();
    });

    function match(card) {
      var okT = topic === 'all' || card.getAttribute('data-topic') === topic;
      var okY = year === 'all' || card.getAttribute('data-year') === year;
      return okT && okY;
    }
    function fillFeature(card) {
      if (!feature) return;
      if (!card) {
        feature.hidden = true;
        return;
      }
      feature.hidden = false;
      feature.href = card.getAttribute('href');
      var img = feature.querySelector('img');
      var src = card.querySelector('img');
      if (img && src) {
        img.src = src.getAttribute('src');
        img.alt = src.getAttribute('alt') || '';
      }
      var heading = feature.querySelector('h2');
      var h3 = card.querySelector('h3');
      if (heading && h3) heading.textContent = h3.textContent;
      var copy = feature.querySelector('p');
      var p = card.querySelector('.body p, p');
      if (copy && p) copy.textContent = p.textContent;
      var time = feature.querySelector('time');
      var srcTime = card.querySelector('time');
      if (time && srcTime) {
        time.textContent = srcTime.textContent;
        time.setAttribute('datetime', srcTime.getAttribute('datetime') || '');
      }
      if (kicker) kicker.textContent = labels[card.getAttribute('data-topic')] || labels.all || kicker.textContent;
    }
    function paint() {
      var n = 0;
      var first = null;
      cards.forEach(function (card) {
        var on = match(card);
        card.hidden = !on;
        if (on) {
          n++;
          if (!first) first = card;
        }
      });
      if (countEl) countEl.textContent = fmt(n, lang);
      if (empty) empty.hidden = n !== 0;
      fillFeature(first);
      root.querySelectorAll('[data-news-topic]').forEach(function (btn) {
        btn.setAttribute('aria-pressed', btn.getAttribute('data-news-topic') === topic ? 'true' : 'false');
      });
      root.querySelectorAll('[data-news-year]').forEach(function (btn) {
        btn.setAttribute('aria-pressed', btn.getAttribute('data-news-year') === year ? 'true' : 'false');
      });
    }
    root.addEventListener('click', function (e) {
      var topicBtn = e.target.closest('[data-news-topic]');
      var yearBtn = e.target.closest('[data-news-year]');
      if (topicBtn && root.contains(topicBtn)) {
        var next = topicBtn.getAttribute('data-news-topic');
        topic = topic === next && next !== 'all' ? 'all' : next;
        paint();
      } else if (yearBtn && root.contains(yearBtn)) {
        var nextY = yearBtn.getAttribute('data-news-year');
        year = year === nextY && nextY !== 'all' ? 'all' : nextY;
        paint();
      }
    });
    document.addEventListener('click', function (e) {
      var reset = e.target.closest('[data-news-reset]');
      if (!reset) return;
      topic = 'all';
      year = 'all';
      paint();
    });
    paint();
  });
})();
