# P11 — Antibacterial disc filter

## Geometry source — not original factory CAD
Hamid supplied a Grok-built reconstruction at https://yellow-scarlet-cherry-craft.grok.me (Discform / “Disc nozzle”). He described it as the filter designed for him. The page is a clear disc with two hollow nozzles, matched to his photograph, plus the official dimensioned drawing.

This cinematic uses that published geometry as-is. No invented parts (no membrane, no extra fittings, no resized barbs). Only materials, lights and cameras are presentation choices.

The GLB is not a static file on that host; it is generated in the browser from:

- `assets/routes-CJotr-Lq.js` — `measures()`, outer and bore profiles
- `assets/disc-geometry-Wv9SVXNF.js` — lathe, end caps, 24 radial ribs, half-cut section cap

Cached copies, the photograph, the drawing, `og.jpg` and this export live in `/workspace/_qa_filter/`.

## Shown defaults versus official catalog numbers
The Discform page, as opened, shows:

- disc diameter 5.00 cm
- overall length 4.45 cm (photo proportions locked, L/D = 0.89)
- disc thickness 0.65 cm
- upper nozzle 1.80 cm
- lower nozzle 2.00 cm
- bore Ø 0.45 cm
- nozzle outside Ø 0.72 cm
- 24 radial ribs

Those are the dimensions of this mesh. The same official Abadis drawing used as “Your drawing” on that page (site asset `assets/img/filters/anti-2.webp`, also Hamid’s `refs/drawing.jpg`) prints **Ø 5.8 cm, length 5.8 cm, weight 16.6 g**. The page text said the drawing “doesn’t print numbers”; it does. This model was not silently rescaled to 5.8 × 5.8, because that would change the photo-locked proportions of the supplied design. Sketch labels distinguish model extents from those manufacturer nominal figures.

Official product identity: فیلتر آنتی‌باکتریال دیسکی / Antibacterial Disc Filter, product code 040501, inventory P11. The photograph on the Discform page is the same official product photograph as `assets/img/filters/anti-1.webp`. This is the standalone inline disc filter, not the white porous disc omitted from the P01/P02/P03 liner sketches, and not P12 (shut-off cage) or P13 (sintered PE).

## Units and parts
Source download: GLB in metres (× 0.01 from centimetres), STL in millimetres (× 10). The site file `p11-disc-filter.glb` is the same mesh in millimetres so it matches the other Abadis cinematics. Parts: `housing` (revolved outer wall, through-bore, end rims), `ribs` (24). The half-cut cap is the source section profile, shown only during the mid-story cut; it is not a new part.

SHA256 of the millimetre GLB: `57d4fcaee4618dc9859947e919c07b4e543e73fd28f80ecb201ae5d28e693f74`.
Model extents: 50 × 44.5 × 50 mm (W × H × D).

## Presentation
Approved cinematic typography, vendor Three.js, 1800vh scroll track, cubic pose easing, exp(-dt*3.2) damping, no idle drift or sway. Polar camera interpolation. Clear / transparent plastic is an approximate real-time material matched to the photograph, not a factory optical specification. Soft studio backdrop and contact shadow are presentation only.

The official site mentions a paper / membrane inside the disc; that part is not in the supplied geometry and is not invented here.
