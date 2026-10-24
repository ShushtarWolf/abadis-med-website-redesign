/* Sample-only filters for the newsroom bento hero. */
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
