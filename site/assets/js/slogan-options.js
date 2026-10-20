/* Slogan text animation T1, scrubbed with the emblem growth.
   The main line wipes in along the reading direction (right to left in
   Persian and Arabic, left to right in English). The three short lines
   then rise one after another. Persian is never split inside a word.
   Reduced motion / no GSAP: slogan stays static (fully visible). */
(function () {
  var mode = document.documentElement.getAttribute('data-slogan');
  var p = document.querySelector('.impact .slogan');
  if (!p || !mode) return;
  var lines = p.querySelectorAll('.slogan-line');
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!window.gsap || !window.ScrollTrigger || reduce) { p.classList.add('slogan-static'); return; }
  if (mode !== 't1' || lines.length < 4) { p.classList.add('slogan-static'); return; }
  gsap.registerPlugin(ScrollTrigger);
  p.classList.add('slogan-anim');
  var rtl = document.documentElement.getAttribute('dir') !== 'ltr';
  var main = lines[0], rest = [lines[1], lines[2], lines[3]];
  var tl = gsap.timeline({ defaults: { ease: 'power2.out' } });
  main.innerHTML = '<span class="sl-mask">' + main.innerHTML + '</span>';
  var m = main.firstChild;
  /* inset is top / right / bottom / left. Hide the trailing edge so the wipe
     follows the reading direction. */
  var hidden = rtl ? 'inset(-20% 0% -20% 100%)' : 'inset(-20% 100% -20% 0%)';
  gsap.set(m, { clipPath: hidden });
  gsap.set(rest, { opacity: 0, y: 26 });
  tl.to(m, { clipPath: 'inset(-20% 0% -20% 0%)', duration: 1.2, ease: 'none' }, 0.3)
    .to(rest, { opacity: 1, y: 0, duration: 0.6, stagger: 0.3 }, 1.4);
  ScrollTrigger.create({ trigger: p, start: 'top 85%', end: 'bottom 75%', scrub: 0.5, animation: tl, invalidateOnRefresh: true });
})();
