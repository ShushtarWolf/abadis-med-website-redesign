/* Approved logo animation B ("growth"), driven by scroll, then a clearly visible
   living loop (light flow, dot glow, arc + leaf sway) once fully grown.
   The loop starts at 100% growth, stops if the visitor scrolls back, and pauses
   while the emblem is off-screen. Reduced motion or no GSAP: static logo. */
(function () {
  if (!window.gsap || !window.ScrollTrigger) return;
  if (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  gsap.registerPlugin(ScrollTrigger);
  var NS = 'http://www.w3.org/2000/svg';
  document.querySelectorAll('svg.logo-grow').forEach(function (svg) {
    var q = function (s) { return svg.querySelectorAll(s); };
    var lines = q('path');
    gsap.set(lines, { strokeDasharray: 1, strokeDashoffset: 1 });
    gsap.set(q('.dot'), { opacity: 0, scale: 0.3, transformOrigin: '50% 50%' });
    var tl = gsap.timeline({ defaults: { ease: 'none' } });
    tl.to(q('.l0,.l1'), { strokeDashoffset: 0, duration: 0.6 }, 0)
      .to(q('.l2,.l3'), { strokeDashoffset: 0, duration: 0.6 }, 0.15)
      .to(q('.stem'), { strokeDashoffset: 0, duration: 0.9 }, 0.35)
      .to(q('.br'), { strokeDashoffset: 0, duration: 0.35, stagger: 0.11 }, 0.45)
      .to(q('.bd'), { opacity: 1, scale: 1, duration: 0.5, stagger: 0.11, ease: 'back.out(2.2)' }, 0.7)
      .to(q('.arc'), { strokeDashoffset: 0, duration: 0.9, stagger: 0.07 }, 1.3)
      .to(q('.ad'), { opacity: 1, scale: 1, duration: 0.35, stagger: 0.03, ease: 'back.out(1.8)' }, 1.85);

    /* ---- living loop after growth: light flow on stem + branches, dot glow, arc sway, leaf sway ---- */
    var layer = document.createElementNS(NS, 'g');
    layer.setAttribute('class', 'pulse-layer');
    layer.setAttribute('fill', 'none'); layer.setAttribute('stroke-linecap', 'round');
    layer.style.opacity = 0; layer.style.pointerEvents = 'none';
    var fid = 'lsglow' + Math.random().toString(36).slice(2, 7);
    var defs = document.createElementNS(NS, 'defs');
    defs.innerHTML = '<filter id="' + fid + '" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="9"/></filter>';
    svg.insertBefore(defs, svg.firstChild);
    svg.appendChild(layer);
    var LIGHT = '#ffffff', GLOW = '#bff6ff';
    var mk = function (src, len) {        /* blurred glow stroke + crisp bright core */
      var g = document.createElementNS(NS, 'g'); g.style.opacity = 0;
      [[GLOW, 30, true], [LIGHT, 13, false]].forEach(function (o) {
        var p = document.createElementNS(NS, 'path');
        p.setAttribute('d', src.getAttribute('d')); p.setAttribute('pathLength', '1');
        p.setAttribute('stroke', o[0]); p.setAttribute('stroke-width', o[1]);
        p.setAttribute('stroke-dasharray', len + ' 3'); p.setAttribute('stroke-dashoffset', len);
        if (o[2]) p.setAttribute('filter', 'url(#' + fid + ')');
        g.appendChild(p);
      });
      layer.appendChild(g); return g;
    };
    var stemG = mk(svg.querySelector('.stem'), 0.22);
    var brs = Array.prototype.slice.call(q('.br')), bds = Array.prototype.slice.call(q('.bd'));
    var halos = bds.map(function (d) {
      var c = document.createElementNS(NS, 'circle');
      c.setAttribute('cx', d.getAttribute('cx')); c.setAttribute('cy', d.getAttribute('cy'));
      c.setAttribute('r', '30'); c.setAttribute('fill', GLOW); c.setAttribute('filter', 'url(#' + fid + ')');
      c.style.opacity = 0; layer.appendChild(c);
      gsap.set(c, { svgOrigin: d.getAttribute('cx') + ' ' + d.getAttribute('cy') }); return c;
    });
    var cores = bds.map(function (d) {      /* white core over each dot */
      var c = document.createElementNS(NS, 'circle');
      c.setAttribute('cx', d.getAttribute('cx')); c.setAttribute('cy', d.getAttribute('cy'));
      c.setAttribute('r', '20'); c.setAttribute('fill', LIGHT);
      c.style.opacity = 0; layer.appendChild(c);
      gsap.set(c, { svgOrigin: d.getAttribute('cx') + ' ' + d.getAttribute('cy') }); return c;
    });
    var STEM = 1.3, CYCLE = 2.5;
    var flow = gsap.timeline({ paused: true, repeat: -1 });
    var segs = function (g) { return g.querySelectorAll('path'); };
    flow.set(stemG, { opacity: 1 }, 0)
        .fromTo(segs(stemG), { strokeDashoffset: 0.22 }, { strokeDashoffset: -1, duration: STEM, ease: 'none' }, 0)
        .to(stemG, { opacity: 0, duration: 0.15 }, STEM - 0.15);
    brs.forEach(function (b, i) {
      var y = +b.getAttribute('d').split(' ')[1];
      var t = STEM * (625 - y) / 550;          /* when the stem light passes this branch */
      var g = mk(b, 0.5);
      flow.set(g, { opacity: 1 }, t)
          .fromTo(segs(g), { strokeDashoffset: 0.5 }, { strokeDashoffset: -1, duration: 0.5, ease: 'none' }, t)
          .to(g, { opacity: 0, duration: 0.12 }, t + 0.38);
      var a = t + 0.3;                          /* light arrives at the dot */
      flow.fromTo(halos[i], { opacity: 0, scale: 0.7 }, { opacity: 0.9, scale: 1.6, duration: 0.25, ease: 'sine.out' }, a)
          .to(halos[i], { opacity: 0, scale: 2, duration: 0.7, ease: 'sine.in' }, a + 0.25)
          .fromTo(cores[i], { opacity: 0, scale: 1 }, { opacity: 0.95, scale: 1.25, duration: 0.22, ease: 'sine.out' }, a)
          .to(cores[i], { opacity: 0, scale: 1, duration: 0.6, ease: 'sine.in' }, a + 0.3)
          .fromTo(bds[i], { scale: 1 }, { scale: 1.25, duration: 0.22, ease: 'sine.out', immediateRender: false }, a)
          .to(bds[i], { scale: 1, duration: 0.5, ease: 'sine.inOut' }, a + 0.25);
    });
    flow.to({}, { duration: 0.001 }, CYCLE - 0.001);

    var arcG = document.createElementNS(NS, 'g'), leafG = document.createElementNS(NS, 'g');
    var strokeG = svg.querySelector('path.arc').parentNode, dotG = svg.querySelector('circle.dot').parentNode;
    arcG.setAttribute('fill', 'none'); arcG.setAttribute('stroke', 'currentColor');
    arcG.setAttribute('stroke-width', '10'); arcG.setAttribute('stroke-linecap', 'round');
    q('.arc').forEach(function (p) { arcG.appendChild(p); });
    q('.ad').forEach(function (c) { var w = document.createElementNS(NS, 'g'); w.setAttribute('fill', 'currentColor'); w.appendChild(c); arcG.appendChild(w); });
    strokeG.parentNode.insertBefore(arcG, dotG.nextSibling);
    q('.leaf').forEach(function (p) { leafG.appendChild(p); });
    strokeG.insertBefore(leafG, strokeG.firstChild);
    var sway = gsap.timeline({ paused: true, repeat: -1 });
    sway.fromTo(arcG, { rotation: -3, svgOrigin: '405 400' }, { rotation: 3, svgOrigin: '405 400', duration: 3, ease: 'sine.inOut', yoyo: true, repeat: 1, immediateRender: false }, 0)
        .fromTo(arcG, { opacity: 1 }, { opacity: 0.6, duration: 3, ease: 'sine.inOut', yoyo: true, repeat: 1, immediateRender: false }, 0)
        .fromTo(leafG, { rotation: -1.5, svgOrigin: '405 625' }, { rotation: 1.5, svgOrigin: '405 625', duration: 1.5, ease: 'sine.inOut', yoyo: true, repeat: 3, immediateRender: false }, 0);

    var grown = false, visible = true, fade;
    var sync = function () {
      var on = grown && visible;
      if (on) { flow.play(); sway.play(); if (fade) fade.kill(); fade = gsap.to(layer, { opacity: 1, duration: 0.5 }); }
      else if (!grown) {
        if (fade) fade.kill();
        fade = gsap.to(layer, { opacity: 0, duration: 0.25, onComplete: function () { if (!grown) flow.pause(0); } });
        sway.pause(0);
        gsap.to(arcG, { rotation: 0, opacity: 1, svgOrigin: '405 400', duration: 0.3 });
        gsap.to(leafG, { rotation: 0, opacity: 1, svgOrigin: '405 625', duration: 0.3 });
        gsap.set(bds, { scale: 1 });
      } else { flow.pause(); sway.pause(); }
    };
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (e) { visible = e[0].isIntersecting; sync(); }).observe(svg);
    }
    ScrollTrigger.create({
      trigger: svg, start: 'top 85%', end: 'center 50%',
      scrub: 0.4, animation: tl, invalidateOnRefresh: true
    });
    /* loop only when the scrubbed growth is actually complete */
    tl.eventCallback('onUpdate', function () {
      var g = tl.progress() >= 0.999;
      if (g !== grown) { grown = g; sync(); }
    });
  });
})();
