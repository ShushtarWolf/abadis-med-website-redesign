/* Slogan: main line stays; the short lines cycle smoothly.
   Works on the homepage impact block and on About heroes, with or without
   data-slogan on <html>. About waits for the line-by-line fade, then cycles.
   Reduced motion / no JS: every line stays visible.
   site.js carries the same init; dataset.sloganInit keeps a single timer. */
(function () {
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  function arm(p) {
    var lines = Array.prototype.slice.call(p.querySelectorAll('.slogan-line'));
    if (!lines.length) return;
    var main = lines[0];
    var rest = lines.slice(1);
    main.classList.add('slogan-line--main');
    if (reduce || !rest.length) {
      p.classList.add('slogan-static');
      return;
    }
    var stage = document.createElement('span');
    stage.className = 'slogan-rotate';
    stage.setAttribute('aria-hidden', 'true');
    rest.forEach(function (line, i) {
      stage.appendChild(line);
      if (i === 0) line.classList.add('is-on');
    });
    p.appendChild(stage);
    p.classList.add('slogan-rotator', 'slogan-anim');
    var idx = 0;
    var timer = null;
    function tick() {
      rest[idx].classList.remove('is-on');
      idx = (idx + 1) % rest.length;
      rest[idx].classList.add('is-on');
    }
    function start() {
      if (timer || rest.length < 2) return;
      timer = setInterval(tick, 1500);
    }
    function stop() {
      if (!timer) return;
      clearInterval(timer);
      timer = null;
    }
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) start();
          else stop();
        });
      }, { threshold: 0.25 });
      io.observe(p);
    } else {
      start();
    }
    document.addEventListener('visibilitychange', function () {
      if (document.hidden) stop();
      else start();
    });
  }
  document.querySelectorAll('.impact .slogan, .about-hero .slogan, .page-hero .slogan').forEach(function (p) {
    if (p.dataset.sloganInit) return;
    p.dataset.sloganInit = '1';
    var wait = (!reduce && p.closest('.about-hero')) ? 1500 : 0;
    if (wait) setTimeout(function () { arm(p); }, wait);
    else arm(p);
  });
})();
