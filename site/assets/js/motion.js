/* Subtle autoplay clips: muted loop, no controls; paused for prefers-reduced-motion. */
(function () {
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.querySelectorAll('video.team-clip, video.about-hero-video, video[data-motion]').forEach(function (v) {
    v.muted = true; v.removeAttribute('controls');
    if (reduce) { v.removeAttribute('autoplay'); v.pause(); return; }
    var p = v.play(); if (p && p.catch) p.catch(function () {});
  });
})();
