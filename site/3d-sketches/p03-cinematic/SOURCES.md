# P03 3 L liner — SIZE-ADAPTED RECONSTRUCTION, not original 3 L CAD

## New owner authorization and scope
The owner explicitly confirmed that the 3 L liner has the same construction as the real 2 L liner, is taller, and contains THREE sealed absorbent powder sachets, then authorized supported missing bigger/smaller variants. This overrides the earlier original-CAD-only restriction for this supported size variant only. The original `3L complete.partlens` is canister-only and was NOT used as a bag. No new nominal product sizes or unrelated constructions are inferred.

## Genuine parent and careful adaptation
Parent: approved `site/3d-sketches/p02-cinematic/p02-2l-cad.glb`, derived from genuine `/workspace/boss-orders/partlens/extracted/Abadis/2L suction bag.partlens` (source fingerprint `0e9d41922be6e5e82431349c084ded6a3243c429dd0fb31f599becf2c1df3bab`), PartLens file SHA256 `fd025fd161c758d7f07f05739ca8e350721e8419b4f6cc9eac4e93b6c5aa07d1`; checked previously against `complete 2L.partlens` liner chunk1. The canister chunk is excluded.

The approved detailed P02 rigid lid, small original cap/strap and collar vertex arrays and index buffers remain unchanged. Their existing approved rendering treatments (lid finish, cavity clipping, underside backing, collar seating and photo-guided recessed white filter/seat exception) are inherited, not new pegs, housings or invented cap hardware. No lid lettering is added. The cinematic is not claimed to be an untouched raw CAD assembly; those approved parent treatments were already present.

Only the soft bag's long middle wall is elongated. The attachment/neck above y=-38 mm stays fixed; the rounded sealed bottom below about y=-265.119 mm is translated downward by145 mm without changing its shape. Intermediate wall heights are remapped between those fixed/translated boundaries; x/z and all cross-sections remain unchanged. Rigid components are never stretched or globally scaled.

Actual parent soft-body y=-24…-268 =244 mm. Official nominal parent height245 mm and 3 L height390 mm differ by145 mm. This adds145 mm to the real244 mm body, yielding an adapted389 mm body at y=-24…-413 while preserving the parent's1 mm nominal-versus-tessellation offset. The unchanged parent bag is about113.29 mm across; Ø110 mm is the manufacturer's nominal dimension, not a false assertion of exact mesh width. The whole assembly including unscaled lid/ports/cap is taller than the nominal bag-body height. These source conventions are explicitly separated rather than stretching every component to a nominal bounding box.

`p03-3l-size-adapted.glb` carries machine-readable adapted provenance. `/workspace/_qa_p03/adapted-v1/geometry-adaptation.json` records parent/output SHA256, rigid-array identity, bounds and the height mapping. This is a size-adapted reconstruction based on2L CAD and manufacturer dimensions; original3L liner CAD remains unavailable.

## Manufacturer evidence opened and actually inspected
https://www.abadis-med.com/en/products/suction-bag/
- 2 L: Ø11 cm, H24.5 cm.
- 3 L: Ø11 cm, H39 cm; gel powder, same suction-liner/filter family.
- Manufacturer diagrams read: `site/assets/img/p/p2-g4.webp` and `site/assets/img/p/p3-g5.webp`, with those exact Persian diameter/height callouts. They are product dimensions, not package dimensions. No pixel-scaling of the stylized diagrams is used as a new CAD measurement.
- The owner's three-sachet confirmation supplies the count; no manufacturer sachet dose, dimensions or powder mass is invented.
- Official photos show printing on the rigid canisters, not on the liner film. No logo, graduation, invented number or lettering is added to this bag.

## Three sealed illustrative sachets and explanatory fluid/gel
The approved P02 sealed mesh pouch is reused three times, without loose powder particles. Two lie side-by-side at the real adapted bottom, with the third as a shallow top layer; the floor/radial fit and visible introduction/descent/landing are checked on desktop/mobile/compact mobile. Pouches, filter, fluid and gel are explanatory non-CAD illustrations, not original3L component CAD, certified powder dose, calibrated capacity animation or validated physical simulation. The larger liner's bottom, fill height, pour range, gel centre/range and cameras follow the adapted body. All visual motion is scrub-driven, including liquid detail, so holding scroll has no autonomous drift.

## Presentation and provenance visibility
Approved P02 PE/PP/filter/sachet materials, lighting, soft studio feel, PATIENT original cap, recessed filter, blood-to-gel story, 1800vh track and exp(-dt*3.2) damping retained. Cameras are adapted for the taller body and three-pouch focal range. Close-ups intentionally frame the active detail (cap/filter/sachets/fluid), not the entire long bag; full hero/final product and essential focal envelopes are verified. A persistent Persian/English provenance caption explicitly says size-adapted reconstruction / not original3L CAD.

## Matching sixth sketch and static sheets
`../cad-line-sketches/#p03-3l-liner` loads the SAME adapted GLB, not a canister proxy. Its three dashed pouches are explicitly illustrative/non-CAD; the filter remains omitted in this sketch. Manufacturer nominal Ø11×H39 cm annotation is distinguished from adapted model extents. The five approved original geometries, original source records and canister print textures remain byte-identical and retain their strict non-CAD omissions.

Light/Dark sheets now cover six designs in three consistently styled pages per theme: original1/2 L liners; clearly labelled adapted3 L liner; original1/2/3 L canisters. Static PNGs and combined PDFs are generated using the existing sheet tooling at `/workspace/3d-product-sketches/cad-line-final/` and linked as downloads from the sketch page.

## Audit, QA and limits
Complete P01–P25 audit: `/workspace/_qa_p03/adapted-v1/SIZE-VARIANT-AUDIT.md`. P03 is the only newly eligible missing size-only product with a genuine supported parent. Tubing25/30/35, fingertip small/large and short/long trolleys are real size families, but have no own genuine CAD parent; they are not built. No filter/connector/regulator/cup/brush/trolley is fabricated from canister geometry.

Actual local/live screenshots, focal camera envelopes, forward/reverse/repeat/idle checks, sketch/sheet typography review, committed/live byte and screenshot comparisons: `/workspace/_qa_p03/adapted-v1/`. See QA-REPORT.md there. All prior cinematics are untouched. Stop after P03; no uncertain additional product is started.
