# P05 3 L reusable rigid suction canister — NOT the missing P03 liner

## Exact genuine 3 L geometry
Source: `/workspace/boss-orders/partlens/extracted/Abadis/3L pit.partlens`.
Archive SHA256: `d5e9bdd4d8185e79f55db293100c2828a5b4ee96affd6580b2f951c9f596df93`.
HIGH exact mesh fingerprint: `6fc5fcdc3805cfce85aef1b6893fd064f8c0eb2837ba6700bd7528655fd21df8`.

All 1,194 original triangles retained: vessel 534; original collar/rear mounting structure 660. Exported triangle multiset verified against the entire original HIGH exact vertex stream. Coordinate permutation only, CATIA `(x,y,z)` → Three.js `(x,z,-y)`, millimetres. No scaling of 1 L/2 L geometry, no deformation, position smoothing, subdivision, clipping, added/removed triangles or invented rigid parts. Crease-aware normals affect shading only; inherited normal-welding processing was numerically checked and changes ZERO vertex positions.

Approximate tessellated full bounds including bracket: 129 × 150.2338 × 420 mm in original x/y/z (129 × 420 × 150.2338 mm in Three.js x/y/z). These are CAD extents, not packaging dimensions or certified nominal product dimensions; they do not appear as claims in the page.

Actual open vessel, collar and attached rear bracket only. No bag liner, lid, cap, mouth ports, filter, sachet or fluid. Nothing is added to compensate for P03's missing soft-liner CAD. The bracket remains in its genuine assembled pose.

## Manufacturer verification
Opened during this build: https://www.abadis-med.com/en/products/canisters/

Verified 3 L transparent polycarbonate canister, code **0402013**. Do not confuse with **0402103**, the separate canister-with-accessories item. The manufacturer's 12.2 × 42 cm values are explicitly individual package dimensions, not product dimensions. Persian/English page copy identifies the 3 L reusable rigid polycarbonate canister and verified code, without new clinical claims.

## Actual right-hand 3 L photo print
Official original source used:
https://www.abadis-med.com/en/wp-content/uploads/2021/07/AMR_4901-scaled-1.jpg

Native photograph 2560 × 2081, local `/workspace/_qa_p05/branding/AMR_4901-scaled-1.jpg`. The **right-hand tallest vessel explicitly reads “3 ltr”**. Only this genuine 3 L print is used. Crop `(1650,185,2200,1910)`, native 550 × 1725 pixels, saved as `/workspace/_qa_p05_3l/v1/official-3l-crop.png`. No 1 L/2 L artwork or numeric scale is stretched, reused, redrawn or synthesized.

`tex/official-3l-print.png` is an alpha extraction and cylindrical inverse projection of that right-hand 3 L vessel's real ink. Verified photographed silhouettes: paired 0.1–2.9 graduations; “1 litr”, “2 litr” intermediate headers and “3 ltr” tops; circular Abadis emblem; MAKHAZEN TEBI ABADIS; WWW.ABADIS-MED.COM; social glyphs/ABADIS.MED lettering; +98 (21) 22671845; Poly carbonate; AUTOCLAVABLE 121° stamp; MADE IN IRAN and ساخت ایران. CE/ISO symbols remain genuine source pixels, not newly asserted certification claims. Tiny accreditor lettering and smallest symbol captions cannot be reliably transcribed and have no guessed replacement text. All fine ticks are copied as photographed, not asserted to be independently calibrated millilitre increments.

This 3 L photograph's measured cylinder axis is approximately x=270→265, radius=235→200, rim/base axis y=30→1670 within the crop. About 12 px front ellipse offset and -0.10 rad source viewing azimuth reproduce the photographed relationship of front print and the slightly leftward rear bracket. Original print groups remain together, opposite the genuine negative-Z rear mount. Registration is an estimate from this actual 3 L photo, not factory artwork or metrological calibration. No unseen rear print is invented.

Native chroma denoise 0.30 px, smooth coverage from chroma 11–34, 4096 × 4096 atlas, supported anisotropy up to 16x. Bottom ROI retains all genuine MADE IN IRAN / ساخت ایران strokes. The source's bluer teal ink is normalized to the approved saturated display teal RGB (4,120,110), without altering photographed glyph silhouettes; this is not colorimetric ink matching. Output-space coverage compositing preserves clean alpha without nonlinear ACES halos. Atlas upsampling improves filtering, not native photographic detail. Ink is surface shader compositing, not emissive lighting or new geometry.

Existing outward-wall and geometric eye-facing masks restrict print to original outward near-vertical vessel triangles: no inner-wall, mirrored far-side/back, rim, base or bracket texture. No decal mesh or replacement shell. In front-oblique views original transparent rear-bracket geometry can project over front ink; that is depth overlap, not printing on the bracket.

## Approved presentation, proportion-adapted cameras
Approved P05 1 L final `8be8523e` and P05 2 L `1ce00c11` are the style/implementation baseline. Clear-PC material definitions, lights, backdrop, typography, 1800vh track and `exp(-dt*3.2)` damping are retained. Only copy, genuine geometry/3 L texture, correct base-shadow height and tall-proportion camera stand-off/focus are adapted. Smooth polar camera sequence: front three-quarter, gently raised rim, brief rear mount, low base, full product return. No idle drift, shape animation or new design direction. Clear PC remains the approved approximate real-time material, not physically calibrated laboratory refraction.

## Evidence and scope
All source crops, mapping manifest/extraction helper, exact-CAD checks, desktop/mobile/compact-mobile actual local/live PNGs, dense camera envelope, scroll/reverse/repeat/idle checks, live-byte and screenshot parity records: `/workspace/_qa_p05_3l/v1/`. See `QA-REPORT.md` there.

Only this new P05 3 L page/assets are introduced. P01, P02, approved P05 1 L/2 L and workflow configuration remain unchanged. No further product is started; no additional CAD-backed products are established.
