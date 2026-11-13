# P05 2 L suction canister with hose and fittings (0402102) — genuine canister CAD + photo-derived hose and fittings

Label used on the page: **Genuine canister CAD + photo-derived hose and fittings (est.)**.

## Product facts (official)
Opened: https://abadis-med.com/محصولات/مخزن/ (tab «مخازن ساکشن») and https://www.abadis-med.com/en/products/canisters/

- 0402102: 2 L canister with accessories, official weight 370 g, package 12.2 × 27 cm (package size, not a product dimension).
- Bare canister 0402012: 346 g. Difference 24 g.
- Hose and fittings set 050103 (connections page, «سری شلنگ و اتصالات مربوطه»): silicone hose 13×7, T connector, connector; hose 30 cm, 37 cm with fittings; 25 g.
  - T connector 030402: polyacetal, 5.6 cm, 3.5 g.
  - Connector 030403: polyethylene, 6 cm, 4 g.
  - Silicone hose 13×7: 050101.

**Inference, not an official statement:** no official photo of the exact 0402102 pack exists on the site. The pairing of the canister with set 050103 is inferred from the official weights (set minus bare canister ≈ hose set 25 g). The 2 L and 3 L sets use the same hose set.

## Genuine geometry (canister)
- Source GLB: `../p05-2l-cinematic/p05-2l-canister-cad.glb` (2L pit.partlens; see that folder's SOURCES.md).
- Meshes `vessel` and `collar-mount` copied verbatim: identity transform, no edit. Position-buffer SHA256 round-trip check after export:
  - vessel `330a26b9c5cb21310af366aafb97ff6b1e85231b01e85e960d83536ce8076b7c` — exact: True
  - collar-mount `5d167f000c6753312049e10ab8bd96a20db8aa7a278232c03d5af53cf8e19dd7` — exact: True
- The official 2 L print texture is reused from `../p05-2l-cinematic/tex/` with the same mapping as the approved bare canister page.
- No liner, lid, filter, cap or fluid is added (none is part of 0402102).

## Photo-derived hose set 050103 (estimated, not factory CAD)
Official sources:
- Kit photo: https://abadis-med.com/wp-content/uploads/2022/12/23.jpg (green hose with a white T on one end and a yellow connector on the other).
- Kit photo EN: https://www.abadis-med.com/en/wp-content/uploads/2021/07/AMR_4789-scaled-1.jpg (T barbs inside the hose end).
- T connector photo: https://abadis-med.com/wp-content/uploads/2022/12/18.jpg and drawing …/2026/11/Teal-Stippled-T-Barbed-Hose-Fitting.png.
- Connector photo: https://abadis-med.com/wp-content/uploads/2022/12/20.jpg and drawing …/2026/11/Teal-Connector-Pipe-Diagram.png (6 cm).
- Hose drawing: https://abadis-med.com/wp-content/uploads/2026/11/Hose-Dimensions-With-Connectors.png (30 cm; 37 cm with fittings).

Modelled (mm):
- Hose: OD 13 / ID 7 (official 13×7), arc length exactly 300.0 (official 300). Lies on the floor in a gentle arc in front of the canister (presentation pose, est.).
- T connector: run 56 overall (official 5.6 cm); hub Ø9.3, collars Ø10, barbed arms Ø6.6 with Ø8.4 barbs (2 per run arm, 3 on the stem), stem ≈ 26 below the run axis, bore Ø4 — proportions measured from 18.jpg (est.). The hose sleeves over one run arm up to the collar, as in 23.jpg / AMR_4789. The stem lies flat, to the side.
- Connector: 60 overall (official 6 cm): 24 insert inside the hose (Ø8.6, hidden), knurled collar Ø15.6 × 11 (24 ribs), taper Ø12.4 → Ø8.8 × 25, bore Ø5 — proportions from 20.jpg and the diagram (est.).
- Overall along the hose path: 373.4 (official 370; difference from estimated fitting proportions).
- Colours sampled from 23.jpg / 20.jpg / 18.jpg (est.): hose green, connector yellow, T white. Real-time materials, not calibrated.

## Model
- `p05-2l-set.glb` SHA256 `44c25756f24a6c1d8c9a6a35c89dda5f84e61cb54e9d8783edc7a6ac8fdfb10b`, 1,243,156 bytes, 13,578 triangles. Extents ≈ 352 × 261 × 270 mm (W × D × H), including the hose set on the floor. Not product dimensions.
- Same file as `../cad-line-sketches/models/p05-2l-set.glb` (sketch sheet 10).
- Builder: `/workspace/_qa_canister_sets/build_sets.mjs` (outside the repo). Coordinates snapped to 1e-6 mm, zero-area triangles dropped (hose set only).

## Presentation
Same style as the approved P05 cinematics: 1800vh track, `exp(-dt*3.2)` damping, same backdrop, lights and clear-PC material. Film: full set, genuine canister rim and print, T connector, hose, connector, full set. `?look=photo|kit|t|ttop|kittop|connector|cside|front|side|top|threeq` for QA stills. Portrait stand-off widens so the whole hose set stays in frame. Studio contact shadows are not product parts.

## Evidence outside the repository
`/workspace/_qa_canister_sets/`: official source images, side-by-side compares (`compare-*.png`), film stills (desktop 1440×900, mobile 390×844), build metadata (`exports/`).

Not yet approved by Hamid (2 L and 3 L are on preview for review).
