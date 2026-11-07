# P05 — actual 1 L reusable suction canister

## Geometry, no substitutes
Source: `/workspace/boss-orders/partlens/extracted/Abadis/1L pit.partlens`.
Source archive SHA256: `aadfde16e0bdf26db94ff6bcd80a9dbf3be496cdce938aca020c5850edca33e6`.
Exact HIGH mesh fingerprint: `423c00c3e4a32abcb09f98e22c418f9409ab448e25f61c3748956489c8704c98`.

All 1,094 original CAD triangles are retained: vessel 542; upper collar/rear mounting structure 552. Coordinate conversion (x,y,z) -> (x,z,-y), millimetres. No scaling, vertex smoothing, shape deformation, subdivision, clipping or invented rigid parts. Crease-aware normals change shading only.

Full assembly mesh bounds: 129 × 183 × 150.2338 mm in Three.js x/y/z, including mounting structure; vessel body approximately 123 mm wide. These are approximate tessellated CAD extents, not manufacturer nominal dimensions. No dimensions appear in the cinematic.

The open top is intentional and is the actual CAD. No lid, mouth ports, bag liner, filter, sachet, fluid or additional hose barb is added. The mounting piece remains attached in its original pose throughout. No exploded assembly or invented moving mechanism.

## Verified manufacturer reference
https://www.abadis-med.com/en/products/canisters/
Opened during this work: reusable transparent polycarbonate 1 L canister, product code 0402011. The page's 12.2 × 18 cm figures are explicitly individual package dimensions; not product dimensions and not used as such.

Manufacturer print correction: official full-resolution photograph https://www.abadis-med.com/en/wp-content/uploads/2021/07/AMR_4901-scaled-1.jpg (2560 × 2081), linked through the manufacturer page image family. The 1 L canister is the LEFT vessel, explicitly marked “1 ltr”; no 2 L/3 L print is borrowed. Original is retained in `/workspace/_qa_p05/branding/AMR_4901-scaled-1.jpg`, inspected 1 L crop in `official-1l-crop.png`. Local older site asset `site/assets/img/c/49d95f95cd78-1600.webp` is only 1024 × 832 and was not used as the print source.

`tex/official-1l-print.png` is an alpha extraction of genuine teal photo ink, cylindrically inverse-projected; no glyph, number, graduation tick, logo or symbol is redrawn or synthesized. The original sampled ink median was RGB (18,120,114). Refined print uses a deeper, saturated display teal RGB (4,120,110), close to the source ink, composited after output color conversion to avoid nonlinear tone-mapping halos. This is surface print, not an emissive material or added light. The actual circular printed Abadis emblem is retained rather than replacing it with a different contemporary logo asset. Positions and scale are estimated from the original vessel/photo; this is not a certified volumetric calibration.

Verified readable print: paired 0.1–0.9 litre graduations and “1 ltr” tops; circular Abadis mark; “MAKHAZEN TEBI ABADIS”; “WWW.ABADIS-MED.COM”; phone +98 (21) 22671845; Poly carbonate; AUTOCLAVABLE 121° stamp; MADE IN IRAN and ساخت ایران. CE/ISO marks and small symbol lettering remain genuine raster photo pixels, not newly asserted certification claims. The tiny accreditor lettering within/beneath the ISO emblem and the smallest symbol captions cannot be reliably transcribed at this resolution: only genuine photo pixels are retained, with no guessed replacement letters. Fine tick marks are copied as photographed, not asserted to be independently calibrated millilitre increments.

Printing is a shader/material texture on the unchanged outward CAD wall triangles only. No decal mesh, replacement vessel or other rigid geometry. Inner wall, rim, base and rear mount are unprinted. A geometric eye-to-exterior-facing gate suppresses the otherwise mirrored far-side print produced by transparent DoubleSide rendering; no mirrored or duplicate inner/rear label. Only the existing front printed region is reproduced; a possible unphotographed rear-side print is not invented. Clear PC remains the existing approximate real-time material. All camera keys, scroll and animation remain unchanged.

## Presentation
Approved P02 typography, vendor dependencies, antialiasing, 1800vh scroll track and exp(-dt*3.2) camera damping. New canister-specific story: full product, open rim, rear mount, transparent wall, base, final hero. No autonomous product/camera drift. Soft studio environment and contact shadow are presentation assets, not product geometry. Optical appearance uses edge-weighted alpha for readable clear walls and the original rear mounting geometry. This is approximate real-time rendering, not physically calibrated refraction or laboratory-validated material optics.

QA scripts/screenshots/report live outside repository: `/workspace/_qa_p05/v1/`. P01 and P02 are unchanged. No other sizes or products are included.

Branding-correction screenshots, source crop, mapping manifest and QA report: `/workspace/_qa_p05/branding/`.

## Print refinement — photo alignment and legibility
The original photo crop remains the only source for all print silhouettes. Local official logo SVG/PNG assets were inspected but have different outer-ring wording (“ABADIS MED … INFECTION CONTROL”), whereas the canister photo says “ABADIS DISPOSABLE SUCTION BAG”; those assets were NOT substituted.

The photo vessel/rim/body axis is approximately x=259.5 in the 520-pixel crop (previous extraction assumed x=248). Recentring the inverse-cylinder projection corrects the paired-ruler/logo alignment. The source rear mount lies approximately 16 pixels left of the body axis; an estimated -0.05 rad source view azimuth keeps the print facing opposite the actual negative-Z rear mount, rather than rotating it arbitrarily to face the hero camera. Source top/bottom axis is approximately y=37/750, with a 14-pixel front-surface vertical offset measured from rim ellipse depth, correcting logo baseline, ruler height and front-wall curvature. These are photo-based estimates, not factory artwork registration. Both ruler columns and their relative logo/text spacing remain extracted together; no independently moved numbers, invented ticks or replacement typography.

Ink extraction now uses a 0.30-native-pixel chroma denoise and smooth coverage from chroma 11–34, preserving photographed minor ticks and letter counters. The inverse-projected atlas is sampled at 4096×2048, with up to 16x supported anisotropy; this improves filtering, NOT the source photograph's intrinsic detail. Correct output-space alpha compositing removes the pale edge/halo caused by mixing ink coverage before nonlinear ACES conversion. All geometry, original clear PC parameters, lighting, camera keyframes, scroll and damping remain unchanged. Existing exterior/facing masks prevent printing on the inside, rear wall, rim, base or bracket. With a three-quarter camera, an outer front label can naturally project over a transparent rear bracket; this is depth overlap, not printing on that bracket.

Refinement source measurements, extraction script, actual desktop/mobile forward/reverse screenshots and QA: `/workspace/_qa_p05/print-refinement/`. Small captions and fine ticks remain limited by the actual photograph; no perfect factory-print fidelity or graduation calibration is claimed.

## Approved camera-only refinement after a9cdff14
The approved print/material revision is retained byte-for-byte. This later camera-only refinement changes the authored viewing path: readable front three-quarter opening (both scale columns/logo), gentle raised rim, brief rear mounting view, low base with the camera still above the physical vessel floor, and return to the full product. Polar position interpolation maintains camera stand-off during the restrained out-and-back arc instead of interpolating a chord through the vessel. No new product motion or idle sway.

Portrait framing accounts for the true rear bracket's asymmetric silhouette, gently widening stand-off on side views and centring the bracket-inclusive original assembly. Original 1800vh track, cubic pose easing and exp(-dt*3.2) scroll damping remain. Only existing caption timing and bottom clearance are adjusted; copy and product claims are unchanged. No new CAD/print/material/light assets. Historical “camera unchanged” statements above describe the earlier print-only revision, not this expressly approved camera revision.

Camera QA: `/workspace/_qa_p05/camera-refinement/` — actual desktop/mobile/compact-mobile renders at key and intermediate poses, dense original-vertex frustum checks, actual forward/reverse/repeat camera checks and fixed-scroll idle screenshots. Real-time PC/photographic microprint limitations remain unchanged.
