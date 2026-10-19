/* Approved logo animation B ("growth"), driven by scroll.
   Leaves -> stem -> branches + nodes light up -> arcs sweep -> arc dots.
   Reduced motion or no GSAP: the complete static logo stays as is. */
(function () {
  if (!window.gsap || !window.ScrollTrigger) return;
  if (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  gsap.registerPlugin(ScrollTrigger);
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
    ScrollTrigger.create({
      trigger: svg, start: 'top 85%', end: 'center 50%',
      scrub: 0.4, animation: tl, invalidateOnRefresh: true
    });
  });
})();
