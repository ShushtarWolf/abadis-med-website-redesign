/* Round-2 finalists: topic + year filters drive the hero slots and the archive. */
(function () {
  var digits = '۰۱۲۳۴۵۶۷۸۹';
  function fa(n) {
    return String(n).replace(/\d/g, function (d) { return digits[d]; });
  }
  function catsOf(el) {
    return (el.getAttribute('data-cat') || '').split(/\s+/).filter(Boolean);
  }

  document.querySelectorAll('[data-fin]').forEach(function (root) {
    var cards = [].slice.call(root.querySelectorAll('[data-fin-card]'));
    var slots = [].slice.call(root.querySelectorAll('[data-fin-slot]'));
    var state = { cat: 'all', year: 'all', index: 0, n: cards.length };

    function match(el) {
      var okYear = state.year === 'all' || el.getAttribute('data-year') === state.year;
      var okCat = state.cat === 'all' || catsOf(el).indexOf(state.cat) !== -1;
      return okYear && okCat;
    }

    function paintSlot(slot, card) {
      if (!card) {
        slot.hidden = true;
        return;
      }
      slot.hidden = false;
      if (slot.tagName === 'A') slot.href = card.getAttribute('href');
      var img = slot.querySelector('img');
      if (img) {
        img.src = card.getAttribute('data-img');
        img.alt = card.getAttribute('data-title') || '';
      }
      var time = slot.querySelector('time');
      if (time) {
        time.textContent = card.getAttribute('data-date') || '';
        time.setAttribute('datetime', card.getAttribute('data-iso') || '');
      }
      var heading = slot.querySelector('h2, h3');
      if (heading) heading.textContent = card.getAttribute('data-title') || '';
      var copy = slot.querySelector('p');
      if (copy) copy.textContent = card.getAttribute('data-excerpt') || '';
      var list = catsOf(card);
      slot.querySelectorAll('[data-fin-kicker]').forEach(function (kicker) {
        kicker.textContent = list.length ? list[0] : 'خبر شرکت';
      });
    }

    function paint() {
      var found = cards.filter(match);
      state.n = found.length;
      if (state.index >= state.n) state.index = 0;
      cards.forEach(function (card) { card.hidden = !match(card); });
      var count = root.querySelector('[data-fin-count]');
      if (count) count.textContent = fa(found.length) + ' خبر';
      var empty = root.querySelector('[data-fin-empty]');
      if (empty) empty.hidden = found.length !== 0;
      var heroEmpty = root.querySelector('[data-fin-hero-empty]');
      if (heroEmpty) heroEmpty.hidden = found.length !== 0;

      slots.forEach(function (slot) {
        var at = parseInt(slot.getAttribute('data-fin-slot'), 10);
        if (root.querySelector('[data-fin-deck]')) at += state.index;
        paintSlot(slot, found[at] || null);
      });

      var wall = root.querySelector('[data-fin-wall]');
      if (wall) wall.setAttribute('data-shown', String(Math.min(3, found.length)));

      root.querySelectorAll('[data-fin-cat]').forEach(function (button) {
        button.setAttribute('aria-pressed', button.getAttribute('data-fin-cat') === state.cat ? 'true' : 'false');
      });
      root.querySelectorAll('[data-fin-year]').forEach(function (button) {
        button.setAttribute('aria-pressed', button.getAttribute('data-fin-year') === state.year ? 'true' : 'false');
      });

      var pos = root.querySelector('[data-fin-pos]');
      if (pos) pos.textContent = found.length ? fa(state.index + 1) + ' از ' + fa(found.length) : '۰ از ۰';
      var dots = root.querySelector('[data-fin-dots]');
      if (dots) {
        dots.replaceChildren();
        var n = Math.min(found.length, 6);
        for (var k = 0; k < n; k++) {
          var dot = document.createElement('button');
          dot.type = 'button';
          dot.setAttribute('aria-label', 'خبر ' + fa(k + 1));
          if (k === state.index) dot.className = 'is-on';
          dot.addEventListener('click', function (i) {
            return function () { state.index = i; paint(); };
          }(k));
          dots.appendChild(dot);
        }
      }
    }

    root.addEventListener('click', function (event) {
      var button = event.target.closest('button');
      if (!button || !root.contains(button)) return;
      if (button.hasAttribute('data-fin-cat')) {
        var nextCat = button.getAttribute('data-fin-cat');
        state.cat = state.cat === nextCat && nextCat !== 'all' ? 'all' : nextCat;
        state.index = 0;
        paint();
      } else if (button.hasAttribute('data-fin-year')) {
        var nextYear = button.getAttribute('data-fin-year');
        state.year = state.year === nextYear && nextYear !== 'all' ? 'all' : nextYear;
        state.index = 0;
        paint();
      } else if (button.hasAttribute('data-fin-next')) {
        if (!state.n) return;
        state.index = (state.index + 1) % state.n;
        paint();
      } else if (button.hasAttribute('data-fin-prev')) {
        if (!state.n) return;
        state.index = (state.index - 1 + state.n) % state.n;
        paint();
      }
    });

    paint();
  });
})();
