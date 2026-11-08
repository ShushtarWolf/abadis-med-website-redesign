# P05 2 L reusable suction canister — original CAD and actual 2 L photo print

## Genuine geometry, preserved exactly
- Source: `/workspace/boss-orders/partlens/extracted/Abadis/2L pit.partlens`.
- Archive SHA256: `8364fa10207d92c840ff0aade2aa1533ddddcf6dabd4844a1328ecb41b972bf8`.
- Exact HIGH mesh fingerprint: `78ae8d7d690d91738b241d967eab853ffbf5f699e164898213b83a8ce526826b`.
- All 1,194 source triangles retained: vessel 534; original connected collar/rear mounting structure 660. Exported triangle multiset checked against the entire genuine source stream. No removed, added, scaled, smoothed-position, subdivided, clipped or reshaped CAD triangles. Crease-aware normals affect shading only.
- Coordinate permutation only: CATIA `(x,y,z)` → Three.js `(x,z,-y)`, millimetres.
- Approximate tessellated overall extents: 129 × 270 × 150.2338 mm in Three.js x/y/z, including bracket. This is the original tall 2 L vessel, not a scaled 1 L. CAD extents are NOT packaging dimensions and do not appear as a product claim.
- Open vessel, upper collar and rear bracket only. No invented closure, mouth ports, bag, filter, fluid or sachet. The bracket remains in its original assembled pose.

## Manufacturer verification
Opened for this revision: https://www.abadis-med.com/en/products/canisters/

The manufacturer specifies transparent polycarbonate, 2 L volume, product code **0402012** (not 0402102, the separate accessories package). Its 12.2 × 27 cm values are explicitly **individual package dimensions**, not product dimensions. The cinematic says 2 L reusable polycarbonate canister in Persian/English and carries only the verified product code; no new clinical claims.

## Actual 2 L branding, not stretched 1 L markings
Original official source photograph:
https://www.abadis-med.com/en/wp-content/uploads/2021/07/AMR_4901-scaled-1.jpg

Native resolution 2560 × 2081. Original local photo `/workspace/_qa_p05/branding/AMR_4901-scaled-1.jpg`. The **middle canister is explicitly labelled “2 ltr”**; only this vessel's print is used. Native crop `(980,770,1540,1910)` is retained at `/workspace/_qa_p05_2l/v1/official-2l-crop.png`. The separate left 1 L and right 3 L vessels supply no print pixels to this page.

`tex/official-2l-print.png` is a teal-chroma alpha extraction and inverse cylindrical projection of that actual middle 2 L vessel. No number, tick, symbol, logo, line of type or certification artwork is redrawn, synthesized, replaced or borrowed from the 1 L texture. The paired 0.1–1.9 graduations, intermediate “1 litr” labels and “2 ltr” tops, circular Abadis emblem, MAKHAZEN TEBI ABADIS, WWW.ABADIS-MED.COM, +98 (21) 22671845, Poly carbonate, AUTOCLAVABLE 121° stamp, MADE IN IRAN and ساخت ایران are copied as genuine photo silhouettes. CE/ISO symbols remain source photo pixels, not newly made certification claims. Small accreditor lettering and very small symbol captions cannot be reliably transcribed from this photo and have no guessed replacement text. Fine graduation ticks are photographic, not an independently validated volumetric calibration.

Registration uses this 2 L photograph's rim/body axis x≈285→278, radius≈235→210, top/base y≈25→1085 within the crop, and ≈12 px front ellipse offset. Its rear mount lies slightly left of the cylindrical axis, corresponding to an estimated -0.06 rad source azimuth. The retained print is opposite the genuine negative-Z rear bracket. Positions/scale are photo estimates, not factory artwork or metrological registration. No unseen rear artwork is invented.

Antialiased saturated teal RGB (4,120,110), 0.30-native-pixel chroma denoise and smooth coverage from chroma 11–34. Atlas 4096 × 3072 with supported anisotropy up to 16x. Output-space coverage compositing retains clean ink edges without nonlinear ACES halos. Upsampling improves filtering only, not the photograph's intrinsic detail.

Print is shader/material mapping on original outward, near-vertical vessel triangles only. Existing outward-normal and eye-facing masks exclude inner wall, back-facing mirrored ink, rim, floor and collar/bracket. There is no decal mesh or invented rigid geometry. In oblique front views the original transparent rear bracket can project over front ink; this is genuine depth overlap, not printing on the bracket.

## Presentation and limitations
Approved 1 L revision `8be8523e` is the style baseline. Original clear-PC parameters, lights, backdrop, typography, 1800vh track and `exp(-dt*3.2)` damping retained. Polar, eased camera choreography is adapted to the genuine taller 2 L proportions: readable front three-quarter, gentle raised rim, brief rear mount, low base, full-product return. Portrait/compact portrait stand-off is widened gently for the bracket silhouette. No idle motion. Real-time PC transparency is the approved approximate material, not laboratory-calibrated refraction.

## Evidence outside the repository
`/workspace/_qa_p05_2l/v1/`: source crop/grid, extracted alpha/atlas preview, `build.py`, `cad-source-check.json`, `mapping-and-ink.json`, desktop/mobile/compact-mobile key/intermediate PNGs, dense exact-vertex camera-envelope checks, forward/reverse/repeat damping and idle checks, live byte/asset verification and live screenshot parity. See `QA-REPORT.md` there for completed checks.

Only this new page and its assets are introduced. P01, P02 and approved P05 1 L are preserved; no other size/product is started.
