/* News & Articles Finalist D — multi-category + year + format/content-type + multi-audience filters, live featured card */
(function () {
  var root = document.querySelector('[data-news-finalist]');
  var grid = document.getElementById('postGrid');
  if (!root || !grid) return;

  var cards = Array.prototype.slice.call(grid.querySelectorAll('.post-card'));
  var topicBtns = Array.prototype.slice.call(root.querySelectorAll('[data-news-topic]'));
  var yearBtns = Array.prototype.slice.call(root.querySelectorAll('[data-news-year]'));
  var fmtBtns = Array.prototype.slice.call(root.querySelectorAll('[data-news-format]'));
  var ctypeBtns = Array.prototype.slice.call(root.querySelectorAll('[data-art-ctype]'));
  var rtimeBtns = Array.prototype.slice.call(root.querySelectorAll('[data-art-rtime]'));
  var audBtns = Array.prototype.slice.call(root.querySelectorAll('[data-art-aud]'));
  var countEl = root.querySelector('[data-news-count]');
  var feat = root.querySelector('[data-news-feature]');
  var empty = document.querySelector('[data-news-empty]');
  var lang = (document.documentElement.getAttribute('lang') || 'fa').toLowerCase();
  var fmt = new Intl.NumberFormat(lang.indexOf('fa') === 0 ? 'fa-IR' : lang.indexOf('ar') === 0 ? 'ar-EG' : 'en-US');

  var state = { topic: 'all', year: 'all', format: 'all', ctype: 'all', rtime: 'all', aud: 'all' };

  function splitCsv(val) {
    if (!val) return [];
    return val.split(',').map(function (s) { return s.trim(); }).filter(Boolean);
  }

  function match(card) {
    var cats = splitCsv(card.getAttribute('data-cats') || card.getAttribute('data-topic') || '');
    var y = card.getAttribute('data-year') || '';
    var fmts = splitCsv(card.getAttribute('data-formats') || card.getAttribute('data-format') || '');
    var ct = card.getAttribute('data-ctype') || '';
    var rt = card.getAttribute('data-rtime') || '';
    var auds = splitCsv(card.getAttribute('data-audiences') || card.getAttribute('data-aud') || '');
    if (state.topic !== 'all' && cats.indexOf(state.topic) < 0) return false;
    if (state.year !== 'all' && y !== state.year) return false;
    if (state.format !== 'all' && fmts.indexOf(state.format) < 0) return false;
    if (state.ctype !== 'all' && ct !== state.ctype) return false;
    if (state.rtime !== 'all' && rt !== state.rtime) return false;
    if (state.aud !== 'all' && auds.indexOf(state.aud) < 0) return false;
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
    var fCtype = feat.querySelector('[data-news-feat-ctype]');
    var cCtype = card.querySelector('.art-ctype-badge');
    if (fCtype && cCtype) fCtype.textContent = cCtype.textContent;
    var fCat = feat.querySelector('[data-news-feat-cat]');
    var cCat = card.querySelector('.art-card-badge');
    if (fCat && cCat) fCat.textContent = cCat.textContent;
    var fFmt = feat.querySelector('[data-news-feat-fmt]');
    var cFmt = card.querySelector('.news-fmt-badge');
    if (fFmt && cFmt) fFmt.textContent = cFmt.textContent;
    var kick = feat.querySelector('[data-news-kicker]');
    if (kick) {
      var activeBtn = root.querySelector('[data-news-topic="' + state.topic + '"] span') || root.querySelector('[data-news-topic="' + state.topic + '"]');
      kick.textContent = (state.topic === 'all' || !activeBtn)
        ? kick.getAttribute('data-default') || kick.textContent
        : activeBtn.textContent.replace(/\s+\d+$/, '');
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
    fmtBtns.forEach(function (b) {
      b.setAttribute('aria-pressed', b.getAttribute('data-news-format') === state.format ? 'true' : 'false');
    });
    ctypeBtns.forEach(function (b) {
      b.setAttribute('aria-pressed', b.getAttribute('data-art-ctype') === state.ctype ? 'true' : 'false');
    });
    rtimeBtns.forEach(function (b) {
      b.setAttribute('aria-pressed', b.getAttribute('data-art-rtime') === state.rtime ? 'true' : 'false');
    });
    audBtns.forEach(function (b) {
      b.setAttribute('aria-pressed', b.getAttribute('data-art-aud') === state.aud ? 'true' : 'false');
    });
  }

  function bindGroup(btns, attr, key) {
    btns.forEach(function (b) {
      b.addEventListener('click', function () {
        var v = b.getAttribute(attr);
        state[key] = (state[key] === v && v !== 'all') ? 'all' : v;
        paint();
      });
    });
  }

  bindGroup(topicBtns, 'data-news-topic', 'topic');
  bindGroup(yearBtns, 'data-news-year', 'year');
  bindGroup(fmtBtns, 'data-news-format', 'format');
  bindGroup(ctypeBtns, 'data-art-ctype', 'ctype');
  bindGroup(rtimeBtns, 'data-art-rtime', 'rtime');
  bindGroup(audBtns, 'data-art-aud', 'aud');

  var reset = document.querySelector('[data-news-reset]');
  if (reset) {
    reset.addEventListener('click', function () {
      state.topic = 'all';
      state.year = 'all';
      state.format = 'all';
      state.ctype = 'all';
      state.rtime = 'all';
      state.aud = 'all';
      paint();
    });
  }
})();
