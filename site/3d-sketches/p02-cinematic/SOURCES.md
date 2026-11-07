# P02 — 2 L cinematic provenance

Based on the approved P01 cinematic at d3c5851d. P01 files are unchanged.

## Actual geometry
- Input: `2L suction bag.partlens`, exact HIGH mesh chunk 0, source fingerprint `0e9d41922be6e5e82431349c084ded6a3243c429dd0fb31f599becf2c1df3bab`.
- Cross-check: `complete 2L.partlens`, exact HIGH mesh chunk 1 contains the same liner assembly. Chunk 0 is the outer canister and is deliberately excluded.
- Original assembly: 4,912 triangles, connected lid / collar / liner / original cap. Coordinate conversion is CATIA (x,y,z) to Three.js (x,z,-y), millimetres, no overall scale distortion.
- Actual liner body spans y=-268 to -24 mm (244 mm), maximum width approximately 113.29 mm. Original cap is retained; no new peg/tether.
- Lid: real 2L mesh, hanging flap below -30 mm omitted as in approved P01; linear subdivision plus gentle non-shrinking smoothing. Filter pocket polygon clipping removes intersections only.
- Same approved P01 opaque internal backing / seating treatment, retargeted pocket aperture. No canister.

## Manufacturer imagery / specifications
- `site/assets/img/p/p2-main.webp`: actual 2L photo inspected for silhouette and teal/frosted material.
- `site/assets/img/p/p2-g4.webp`: manufacturer dimension diagram, diameter 11 cm, height 24.5 cm. These nominal dimensions also appear in `site/products/suction-bag/index.html`, section s2. CAD mesh extents differ slightly; nominal specifications are not asserted to be exact mesh bounds.
- Porous white filter and its seat use the approved P01 photo-guided exception, not a claimed 2L tear-down measurement. Plastic, film and sachet textures are reused from P01 reference photography.

## Presentation
- Camera independently retargeted for the taller 2L body; no blind 1L hero framing.
- Same 1800vh track and exp(-dt*3.2) scrub response. No idle camera drift or bag sway.
- Fill volume, bottom plane, sachet destination, gel propagation and floor retargeted to 2L CAD.
- Blood/gel and sachet are explanatory visualizations, not validated fluid simulation or calibrated capacity animation.
- QA images and scripts are outside the repository at `/workspace/_qa_p02/v1/`.

## Owner correction — two absorbent sachets
The 2 L product contains **two sealed absorbent mesh sachets inside one liner**, confirmed by the owner. The existing pouch geometry/material is reused twice, side-by-side with a 4 mm local gap; no second liner or loose powder. Both share the same eased rotation and descent. Their final settling is completed at progress .535, before the existing liquid becomes visible, so the approved camera can show both introduction and landing without changing any camera keyframes, damping, lid motion, film material, filter or fill/gel code. At rest the pair's conservative maximum radial envelope is approximately 46 mm, inside the real lower liner radius of approximately 49 mm. Sachet captions are plural in Persian and English. Correction QA: `/workspace/_qa_p02/two-sachets/`.
