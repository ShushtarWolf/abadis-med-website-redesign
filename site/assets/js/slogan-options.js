/* Slogan: main line stays; all three short lines («به شما», «به طبیعت», «به جهان») cycle smoothly.
   Reduced motion / no JS: all lines stay visible statically. */
(function () {
  var mode = document.documentElement.getAttribute('data-slogan');
  var p = document.querySelector('.impact .slogan');
  if (!p || !mode) return;

  var lines = Array.prototype.slice.call(p.querySelectorAll('.slogan-line'));
  if (!lines.length) return;

  var main = lines[0];
  var rest = lines.slice(1);
  main.classList.add('slogan-line--main');

  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce || rest.length === 0) {
    p.classList.add('slogan-static');
    return;
  }

  /* Build rotator stage for all three short lines: به شما / به طبیعت / به جهان */
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
})();
