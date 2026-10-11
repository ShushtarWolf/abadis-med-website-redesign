// Hero option 3: each team clip plays once (no loop), staggered, and stops on its last frame.
(function () {
  var hero = document.getElementById('hero');
  if (!hero) return;
  var vids = [].slice.call(hero.querySelectorAll('.team-vid'));
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var saveData = navigator.connection && navigator.connection.saveData;
  function start() {
    hero.classList.add('is-in');
    if (reduce || saveData) return; // posters already show the final frame (eyes open, arms crossed)
    vids.forEach(function (v, i) {
      setTimeout(function () {
        v.currentTime = 0;
        var p = v.play();
        if (p && p.catch) p.catch(function () {});
      }, 350 + i * 700);
    });
  }
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      if (es[0].isIntersecting) { io.disconnect(); start(); }
    }, { threshold: 0.25 });
    io.observe(hero);
  } else start();
})();
