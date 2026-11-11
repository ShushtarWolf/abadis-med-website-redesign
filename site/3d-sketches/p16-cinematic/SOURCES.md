# P16 — Porous filter (فیلتر متخلخل)

## Geometry source — not original factory CAD
Hamid supplied a Grok-built reconstruction at https://cloud-zenith-spruce-lark.grok.me. The page lathes a hollow UHMW-PE tube from a filleted 2-D profile (`routes-CUudxthE.js`: `Xf` profile, `$f` `LatheGeometry` with 80 segments; this site mesh uses 128 segments of the same profile so the rims stay smooth at close range, default `height: 29.5, outerD: 20, innerD: 12`). Fine surface porosity is appearance only — Grok does not carve a lattice of holes, and this model does not invent one.

This cinematic uses that published geometry, corrected to the official Abadis photograph and dimensioned drawing. Only materials, lights and cameras are presentation choices. No invented parts.

## Official product
- FA: فیلتر متخلخل. EN: Porous filter.
- Product code 011103. Inventory P16.
- Official pages: `site/products/filters/index.html` `#mot`, EN `site/en/products/filters/index.html` `#mot`.
- Material (official copy): heavy polyethylene / UHMW-PE. Pores swell when wetted and close, stopping liquid. Bacterial filtration 99.999%.
- Official catalog table prints only the name and code — no official printed OD or ID, and no printed weight, on the product page.
- Official website photograph: `assets/img/c/3f3b9e7efaa7-1600.webp` (a group of white sintered tubes). This is the same photograph as Grok `/refs/product.jpg`.
- Official-style drawing (Grok `/refs/drawing.jpg`): 3/4 isometric of the hollow tube, printed height «ارتفاع: ۲۹٫۵ میلی‌متر» (29.5 mm). A width/OD dimension sits at the top of the sheet but is cropped in the supplied scan, so its number is not used.

## Shown dimensions
- Height 29.5 mm — official drawing.
- Outer Ø 20 mm and inner Ø 12 mm (wall 4.0 mm) — Grok estimates from the official product photograph, kept after an independent measurement of that same photo using the official 29.5 mm height as the scale (apparent OD ≈ 20.1–20.5 mm, ID/OD ≈ 0.56–0.60). These are estimates, not official catalog numbers.
- Rim fillet 0.5 mm — Grok profile (`min(0.5, wall×0.28, height×0.055)`).
- Grok's cream/teal preview (`og.jpg`) is not an official photo and is not used for colour. Official parts are matte, slightly warm off-white sintered PE.

## Units and parts
The site file `p16-porous-filter.glb` is in millimetres. Single part: `body` (revolved outer wall, through-bore, 0.5 mm rim fillets). Model extents: 20 × 20 × 29.5 mm (W × D × H).

## Presentation
Approved cinematic typography, vendor Three.js, 1800vh scroll track, cubic pose easing, exp(-dt*3.2) damping, no idle drift or sway. Polar camera interpolation. Matte off-white UHMW-PE is an approximate real-time material matched to the official photograph. A fine sintered grain — procedural object-space albedo speckle and bump, no UV seams — is applied to the outer wall, the bore and the rims; it is presentation only and does not carve holes or change the mesh. Soft studio backdrop and contact shadow are presentation only. A mid-story clip plane reveals the wall and bore using the source solid; it does not add geometry.
