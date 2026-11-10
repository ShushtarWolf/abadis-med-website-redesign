# P14 — Portable suction base (trolley)

## Provenance
stand modeled from Hamid's supplied design; canisters = genuine Abadis 2L CAD with official print.

پایه از طرح تهیه‌شده توسط حمید مدل‌سازی شده؛ مخازن = CAD اصلی ۲ لیتری آبادیس با چاپ رسمی.

## Stand geometry — not original factory CAD
Hamid supplied a Grok-built reconstruction at https://zinc-cliff-horizon-solar.grok.me (DuoVac 80). Base, square upright, vacuum regulator, and yellow / green / grey tubing are used as-is from that design. No invented stand parts. Materials, lights and cameras are presentation choices. The explode is a presentation pose of the existing parts (jars part sideways, regulator lifts), using the source offsets. Collected-volume fluid, selection rings and the on-page 80 cm sprite remain omitted.

## Canisters — genuine P05 2 L CAD with official print
Hamid chose to replace the two illustrative Grok jars with the approved genuine 2 L reusable canister CAD, the same mesh and photo-derived print texture as `p05-2l-cinematic` (commit `1ce00c11`).

- Source mesh: `site/3d-sketches/p05-2l-cinematic/p05-2l-canister-cad.glb` (SHA256 `96086aeb53390d8bc85387c8bd98ba64dbeec072535e8b368256cbe27feb87f3`), identical to commit `1ce00c11`.
- Official print: `site/3d-sketches/p05-2l-cinematic/tex/official-2l-print.png` (SHA256 `495ab3cd53661b9273f053e79a7d66e1559e7f87ba0469f7ced4e32be13c5e3c`), extracted from official photograph AMR_4901, same mapping as the approved 2 L cinematic (front exterior only; no mirrored inner/back print).
- Official canister code **0402012**. CAD extents Ø 12.9 × H 27.0 cm including the rear collar-mount (vessel body is an open tall 2 L polycarbonate jar). All 1,194 source triangles per canister are retained (vessel 534; collar-mount 660). No scaled, smoothed, clipped or invented canister triangles.
- Both canisters sit on the stand at the same axis positions as the Grok jars (x = ±102 mm, z = 0) and the same seat (bottom y = 235 mm), upright, at true CAD scale. Print faces +Z (forward), matching the official trolley photograph and the P05 2 L cinematic. No spacing or seat-height shift was required.

## Official product identity
Hamid’s photograph is the official Abadis product photograph `assets/img/c/227665fb9960.webp` on `/products/stand/` and `/en/products/base-and-holder/`.

- FA: پایه ساکشن پرتابل (ترولی)
- EN: Portable suction base (trolley)
- Inventory: P14
- Catalog codes: 060401 short / 060402 long

Official listed specifications: holds up to four 3-litre canisters (12 litres); the regulator and the ON/OFF valve can be fitted; light and easy to move. The official catalog does not print a height or a base span. This is not P06 and not P15 / 060503 / 060504.

## Fit notes — nothing invented
- No intersection with the upright, base or regulator. At jar height the main post is 40 × 40 mm; clearance from the genuine vessel wall to the post face is 20.5 mm, and from the collar-mount to the post face 17.5 mm. (The upright AABB looks tighter, 7.5 mm, only because a 60 mm square collar sits higher on the post, above the jar rim.)
- Closest approach to the supplied tubing is about 14.7 mm (mesh-to-mesh). Some tube vertices hover over the open mouth; they do not intersect the vessel wall.
- Genuine CAD is an open vessel: no lid and no mouth ports. The supplied yellow / green / grey lines still end at the former Grok lid-port locations, about 8 mm above the genuine rim and well inside the mouth (radial about 20–32 mm vs inner rim 60 mm). They no longer meet a port. Lines were not rerouted; no ports, lids or fittings were added.
- The genuine rear collar-mount is kept in its original assembled pose, facing −Z (opposite the official print). The supplied stand has no hook, clamp or bracket that engages this collar. The collar sits in open air behind each vessel and does not contact the upright, base, regulator or lines.

## Shown stand defaults versus official catalog
- Labelled height 80 cm; model crown 80.5 cm (hose / tube radius past the 80 cm line). Official catalog prints no height, so the model is not assigned to short vs long.
- Labelled base “about 48 cm”; five-caster footprint about 50.7 × 47.3 cm.
- Official text: up to four 3 L jars. Official photograph and this model show two jars. Those jars are now genuine 2 L CAD, not the earlier illustrative Grok cylinders.
- Overall stand extents, including side tubing: 76.7 × 46.8 × 80.5 cm (W × D × H).

## Units and parts
Site file `p14-suction-stand.glb` is in millimetres. Parts: `base`, `upright`, `canister-l` (genuine vessel + collar-mount), `canister-r` (same), `regulator`, `lines`.

SHA256 of the millimetre GLB: `9771cf70e5958f9a09de497368be467aedd0777fbd6626307e650a2027b4f9ad`.
Model extents: 767 × 468 × 805 mm (W × D × H). 14,142 triangles.

## Presentation
Approved cinematic typography, vendor Three.js, 1800vh scroll track, cubic pose easing, exp(-dt*3.2) damping, no idle drift or sway. Polar camera interpolation. Canister materials and official-print shader match the approved p05-2l-cinematic. Soft studio backdrop and contact shadow are presentation only.
