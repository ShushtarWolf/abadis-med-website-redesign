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
The site file `p16-porous-filter.glb` is in millimetres. Single part: `body` (revolved outer wall, blind bore open at the top, closed flat bottom, 0.5 mm rim fillets, 1 mm bore-floor radius). Model extents: 20 × 20 × 29.5 mm (W × D × H). Earlier versions (v1–v3) had a through-bore; see v4 below.

## Presentation
Approved cinematic typography, vendor Three.js, 1800vh scroll track, cubic pose easing, exp(-dt*3.2) damping, no idle drift or sway. Polar camera interpolation. Matte cool-neutral white UHMW-PE is an approximate real-time material matched to the official photograph's midtones and grey shadows, with no yellow cast. A fine sintered grain — procedural object-space albedo speckles and a slight mid-scale bump, no UV seams, with a distance fade so fine pores do not alias — is applied to the outer wall, the bore and the rims; it is presentation only and does not carve holes or change the mesh. Soft studio backdrop and contact shadow are presentation only. A mid-story clip plane reveals the wall, the blind bore and the closed end using the source solid; its cut-face cap is the same section profile as the model (U-shaped, open top, 4 mm closed bottom) and does not add geometry.

## v4 — one end closed (blind bore)
Hamid, from a phone screenshot of the filters-page porous-filter viewer: «یک ور این فیلتر سوراخ نیست، بسته است» ("one side of this filter has no hole, it is closed"). The bore is now blind.

- Open end: top (+Y). The official drawing shows the bore at the top end of its 3/4 view, so that end stays open. The opening beats look into it, as before.
- Closed end: bottom (−Y), flat, with the same 0.5 mm outer edge fillet as the open rim. The official website photograph shows several of the tubes with flat, solid ends (the standing tube at the back centre and the horizontal tube top left), next to others showing open bores, so a flat closed end matches the official photo.
- Closed-end (floor) thickness ≈ 4.0 mm — estimate, set equal to the 4 mm wall. Bore depth ≈ 25.5 mm (29.5 − 4.0) — estimate. Bore floor flat with a ≈ 1 mm corner radius — estimate. None of these is printed on the official drawing or the catalog page, and the official photo does not show a cut part, so they cannot be measured.
- Unchanged: height 29.5 mm (official), Ø 20 / Ø 12 mm (photo estimates), the v3 cool-white sintered grain (`sintered-grain.js`, Hamid-approved, unchanged), materials, lights and the camera path.
- Geometry: one lathe of the blind profile, 128 segments, no zero-area pole triangles, seam coordinates snapped so viewers that weld by position see one closed seam. 7,680 triangles. Builder: `_qa_p16/build_filter_v4.mjs` (QA workspace, not shipped).
- The same GLB is shared by the filters page solid viewer (`data-solid-src`), the CAD line sketch (`cad-line-sketches/models/p16-porous-filter.glb`, also the filters-page iso viewer source) and this cinematic. The filters-page stills (`assets/img/products/3d/p16-porous-filter-still-*.webp`, `assets/img/products/cad-iso/p16-porous-filter-iso-*.webp`) were re-rendered from the v4 GLB with the page's own viewers. The iso viewer's P16 label now reads `Ø 20 mm (est.) × H 29.5 mm` (it said Ø 18.2 mm, an older figure that did not match the model).
- CAD line sketch sheet 8 now shows iso, section A–A (hatched, closed end ≈ 4 mm and bore ≈ 25.5 mm marked as estimates), the closed end from below, front and side. Front and side show the bore as hidden lines that stop at the floor.
