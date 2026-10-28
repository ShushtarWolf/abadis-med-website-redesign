/* News & Articles Finalist D — topic + year + reading-time + audience filters, live featured card */
(function () {
  var root = document.querySelector('[data-news-finalist]');
  var grid = document.getElementById('postGrid');
  if (!root || !grid) return;

  var cards = Array.prototype.slice.call(grid.querySelectorAll('.post-card'));
  var topicBtns = Array.prototype.slice.call(root.querySelectorAll('[data-news-topic]'));
  var yearBtns = Array.prototype.slice.call(root.querySelectorAll('[data-news-year]'));
  var rtimeBtns = Array.prototype.slice.call(root.querySelectorAll('[data-art-rtime]'));
  var audBtns = Array.prototype.slice.call(root.querySelectorAll('[data-art-aud]'));
  var countEl = root.querySelector('[data-news-count]');
  var feat = root.querySelector('[data-news-feature]');
  var empty = document.querySelector('[data-news-empty]');
  var lang = (document.documentElement.getAttribute('lang') || 'fa').toLowerCase();
  var fmt = new Intl.NumberFormat(lang.indexOf('fa') === 0 ? 'fa-IR' : lang.indexOf('ar') === 0 ? 'ar-EG' : 'en-US');

  var state = { topic: 'all', year: 'all', rtime: 'all', aud: 'all' };

  function match(card) {
    var t = card.getAttribute('data-topic') || 'corp';
    var y = card.getAttribute('data-year') || '';
    var rt = card.getAttribute('data-rtime') || '';
    var au = card.getAttribute('data-aud') || '';
    if (state.topic !== 'all' && t !== state.topic) return false;
    if (state.year !== 'all' && y !== state.year) return false;
    if (state.rtime !== 'all' && rt !== state.rtime) return false;
    if (state.aud !== 'all' && au !== state.aud) return false;
    return true;
  }

  function fillFeature(card) {
    if (!feat || !card) return;
    var img = card.querySelector('img');
    var fImg = feat.querySelector('img');
    var h3 = card.querySelector('h3');
    var p = card.querySelector('p');
    var tm = card.querySelector('time');
    var fH = feat.querySelector('h2');
    var fP = feat.querySelector('p');
    var fT = feat.querySelector('time');
    feat.setAttribute('href', card.getAttribute('href') || '#');
    if (img && fImg) {
      fImg.setAttribute('src', img.getAttribute('src') || '');
      fImg.setAttribute('alt', img.getAttribute('alt') || '');
    }
    if (h3 && fH) fH.textContent = h3.textContent;
    if (p && fP) fP.textContent = p.textContent;
    if (fT) {
      if (tm) {
        fT.textContent = tm.textContent;
        fT.setAttribute('datetime', tm.getAttribute('datetime') || '');
        fT.hidden = false;
      } else {
        fT.hidden = true;
      }
    }
    var fRtime = feat.querySelector('[data-news-feat-rtime]');
    var cRtime = card.querySelector('.art-card-time');
    if (fRtime && cRtime) fRtime.textContent = cRtime.textContent;
    var fAud = feat.querySelector('[data-news-feat-aud]');
    var cAud = card.querySelector('.art-aud-tag');
    if (fAud && cAud) fAud.textContent = cAud.textContent;
    var kick = feat.querySelector('[data-news-kicker]');
    if (kick) {
      var activeBtn = root.querySelector('[data-news-topic="' + state.topic + '"] span');
      kick.textContent = (state.topic === 'all' || !activeBtn)
        ? kick.getAttribute('data-default') || kick.textContent
        : activeBtn.textContent;
    }
  }

  function paint() {
    var shown = 0;
    var first = null;
    cards.forEach(function (c) {
      var on = match(c);
      c.hidden = !on;
      if (on) {
        shown++;
        if (!first) first = c;
      }
    });
    if (countEl) countEl.textContent = fmt.format(shown);
    if (empty) empty.hidden = shown > 0;
    if (first) fillFeature(first);
    topicBtns.forEach(function (b) {
      b.setAttribute('aria-pressed', b.getAttribute('data-news-topic') === state.topic ? 'true' : 'false');
    });
    yearBtns.forEach(function (b) {
      b.setAttribute('aria-pressed', b.getAttribute('data-news-year') === state.year ? 'true' : 'false');
    });
    rtimeBtns.forEach(function (b) {
      b.setAttribute('aria-pressed', b.getAttribute('data-art-rtime') === state.rtime ? 'true' : 'false');
    });
    audBtns.forEach(function (b) {
      b.setAttribute('aria-pressed', b.getAttribute('data-art-aud') === state.aud ? 'true' : 'false');
    });
  }

  topicBtns.forEach(function (b) {
    b.addEventListener('click', function () {
      var v = b.getAttribute('data-news-topic');
      state.topic = (state.topic === v && v !== 'all') ? 'all' : v;
      paint();
    });
  });

  yearBtns.forEach(function (b) {
    b.addEventListener('click', function () {
      var v = b.getAttribute('data-news-year');
      state.year = (state.year === v && v !== 'all') ? 'all' : v;
      paint();
    });
  });

  rtimeBtns.forEach(function (b) {
    b.addEventListener('click', function () {
      var v = b.getAttribute('data-art-rtime');
      state.rtime = (state.rtime === v && v !== 'all') ? 'all' : v;
      paint();
    });
  });

  audBtns.forEach(function (b) {
    b.addEventListener('click', function () {
      var v = b.getAttribute('data-art-aud');
      state.aud = (state.aud === v && v !== 'all') ? 'all' : v;
      paint();
    });
  });

  var reset = document.querySelector('[data-news-reset]');
  if (reset) {
    reset.addEventListener('click', function () {
      state.topic = 'all';
      state.year = 'all';
      state.rtime = 'all';
      state.aud = 'all';
      paint();
    });
  }
})();
