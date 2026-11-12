# P16 — Porous filter (فیلتر متخلخل)

## Geometry source — not original factory CAD
Hamid supplied a Grok-built reconstruction at https://cloud-zenith-spruce-lark.grok.me. The page lathes a hollow UHMW-PE tube (Grok's assumption; the real part is solid, see v5) from a filleted 2-D profile (`routes-CUudxthE.js`: `Xf` profile, `$f` `LatheGeometry` with 80 segments; this site mesh uses 128 segments of the same profile so the rims stay smooth at close range, default `height: 29.5, outerD: 20, innerD: 12`). Fine surface porosity is appearance only — Grok does not carve a lattice of holes, and this model does not invent one.

This cinematic uses that published geometry, corrected to the official Abadis photograph and dimensioned drawing. Only materials, lights and cameras are presentation choices. No invented parts.

## Official product
- FA: فیلتر متخلخل. EN: Porous filter.
- Product code 011103. Inventory P16.
- Official pages: `site/products/filters/index.html` `#mot`, EN `site/en/products/filters/index.html` `#mot`.
- Material (official copy): heavy polyethylene / UHMW-PE. Pores swell when wetted and close, stopping liquid. Bacterial filtration 99.999%.
- Official catalog table prints only the name and code — no official printed OD or ID, and no printed weight, on the product page.
- Official website photograph: `assets/img/c/3f3b9e7efaa7-1600.webp` (a group of white sintered tubes). This is the same photograph as Grok `/refs/product.jpg`.
- Official-style drawing (Grok `/refs/drawing.jpg`): 3/4 isometric drawn as a hollow tube (Hamid confirms the real part has no hole), printed height «ارتفاع: ۲۹٫۵ میلی‌متر» (29.5 mm). A width/OD dimension sits at the top of the sheet but is cropped in the supplied scan, so its number is not used.

## Shown dimensions
- Height 29.5 mm — official drawing.
- Outer Ø 20 mm — Grok estimate from the official product photograph, kept after an independent measurement of that same photo using the official 29.5 mm height as the scale (apparent OD ≈ 20.1–20.5 mm). An estimate, not an official catalog number.
- No bore: solid, no bore per Hamid 2026-11-12. (The inner Ø 12 mm used up to v4 is withdrawn.)
- Edge round 0.5 mm on both flat ends — from the Grok profile's rim fillet.
- Grok's cream/teal preview (`og.jpg`) is not an official photo and is not used for colour. Official parts are matte, slightly warm off-white sintered PE.

## Units and parts
The site file `p16-porous-filter.glb` is in millimetres. Single part: `body`, a solid cylinder (revolved profile: flat bottom, 0.5 mm edge round, wall, 0.5 mm edge round, flat top). No bore. Model extents: 20 × 20 × 29.5 mm (W × D × H). 5,120 triangles.

## Presentation
Approved cinematic typography, vendor Three.js, 1800vh scroll track, cubic pose easing, exp(-dt*3.2) damping, no idle drift or sway. Polar camera interpolation. Matte cool-neutral white UHMW-PE is an approximate real-time material matched to the official photograph's midtones and grey shadows, with no yellow cast. A fine sintered grain — procedural object-space albedo speckles and a slight mid-scale bump, no UV seams, with a distance fade so fine pores do not alias — is applied to the wall, both flat end faces and the edge rounds; it is presentation only and does not carve holes or change the mesh. Soft studio backdrop and contact shadow are presentation only. There is no cutaway: the part is solid, and showing an interior would be invented. The mid-story beat holds a flank view of the solid body instead.

## v5 — solid, no bore per Hamid 2026-11-12
Hamid, after v4: «It is still not filled, there is no hole in real product.» The porous filter 011103 is a solid cylinder with no bore at either end.

- History: v1–v3 had a through-bore (Grok's hollow-tube assumption). v4 (same day) made it a blind bore after Hamid said one side has no hole. Both were wrong and are superseded by v5.
- Geometry: one lathe of a solid profile, 128 segments, flat ends with a 0.5 mm edge round, no zero-area triangles, seam coordinates snapped. H 29.5 mm (official), Ø 20 mm (estimate). Builder: `_qa_p16/build_filter_v5.mjs` (QA workspace, not shipped).
- Matches the official photograph's flat, solid ends (the standing tube at the back centre shows one clearly).
- The v3 cool-white sintered grain (`sintered-grain.js`, Hamid-approved, unchanged) is object-space, so it covers the wall and both end faces.
- Cinematic: the half-cut, its cap and the clip plane are removed; the mid-story beat now reads «بدنهٔ توپر و متخلخل» / "Solid sintered body · flat ends · the pores swell shut when wet and stop liquid". The "ID 12" figure is removed from the height beat. `?look=` views: `drawing`, `photo`, `set`, `flank` (was `cut`), `front`, `side`, `threeq`, `end` (bottom end face, was `base`), `top`.
- The same GLB is shared by the filters-page solid viewer, the CAD line sketch (`cad-line-sketches/models/p16-porous-filter.glb`, also the filters-page iso viewer source) and this cinematic. Filters-page stills were re-rendered from the v5 GLB with the page's own viewers.
- CAD line sketch sheet 8: iso, section A–A (fully hatched, solid), top, front, side. No inner diameter or bore depth anywhere.
