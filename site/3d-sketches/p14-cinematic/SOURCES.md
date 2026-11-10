# P14 — Portable suction base (trolley)

## Provenance
stand from Hamid's supplied design; canisters = genuine Abadis 2L CAD with official print; liners = approved 2L suction bag with two sachets.

پایه از طرح تهیه‌شده توسط حمید مدل‌سازی شده؛ مخازن = CAD اصلی ۲ لیتری آبادیس با چاپ رسمی؛ لاینرها = کیسه ساکشن ۲ لیتری تأییدشده با دو ساشه.

## Stand geometry — not original factory CAD
Hamid supplied a Grok-built reconstruction at https://zinc-cliff-horizon-solar.grok.me (DuoVac 80). Base, square upright, vacuum regulator, and yellow / green / grey tubing are used as-is from that design. No invented stand parts. Materials, lights and cameras are presentation choices. The explode is a presentation pose of the existing parts (lid and bag lift out of each canister, jars part sideways, regulator lifts), using the source offsets. Collected-volume fluid, selection rings and the on-page 80 cm sprite remain omitted.

## Canisters — genuine P05 2 L CAD with official print
Hamid chose to replace the two illustrative Grok jars with the approved genuine 2 L reusable canister CAD, the same mesh and photo-derived print texture as `p05-2l-cinematic` (commit `1ce00c11`).

- Source mesh: `site/3d-sketches/p05-2l-cinematic/p05-2l-canister-cad.glb` (SHA256 `96086aeb53390d8bc85387c8bd98ba64dbeec072535e8b368256cbe27feb87f3`), identical to commit `1ce00c11`.
- Official print: `site/3d-sketches/p05-2l-cinematic/tex/official-2l-print.png` (SHA256 `495ab3cd53661b9273f053e79a7d66e1559e7f87ba0469f7ced4e32be13c5e3c`), extracted from official photograph AMR_4901, same mapping as the approved 2 L cinematic (front exterior only; no mirrored inner/back print).
- Official canister code **0402012**. CAD extents Ø 12.9 × H 27.0 cm including the rear collar-mount (vessel body is an open tall 2 L polycarbonate jar). All 1,194 source triangles per canister are retained (vessel 534; collar-mount 660). No scaled, smoothed, clipped or invented canister triangles.
- Both canisters sit on the stand at the same axis positions as the Grok jars (x = ±102 mm, z = 0) and the same seat (bottom y = 235 mm), upright, at true CAD scale. Print faces +Z (forward), matching the official trolley photograph and the P05 2 L cinematic. No spacing or seat-height shift was required.

## Liners — approved P02 2 L suction bag with two sachets
Hamid's answer on the open-canister / tube gap was to place the matching suction bag inside the lid / canister. Each genuine 2 L canister now holds the approved P02 2 L liner, reused as-is from `p02-cinematic` (commit `f54d8451` for the two-sachet correction; mesh from `p02-2l-cad.glb`, SHA256 `ccf6517709c90d79b83c62d681acea35c90bb9041ca319a29179653b09ebdbc4`).

- Parts seated in each canister, in the approved P02 local frame: lid, liner collar, bag, tethered cap. The lid seating face at local y = 0 rests on the P05 rim (local y = 0, inner r = 60.00, outer r = 61.50). The bag hangs inside (bottom y = −268, 2 mm above the vessel floor at y = −270). The liner collar (r max 59.07) fits inside the mouth. Approved P02 orientation is kept: PATIENT port (tethered cap) at +Z, world tops L (−101.74, 514.84, 33.10) and R (102.26, 514.84, 33.10); VACUUM port (recessed flow-stopper filter underneath, as in official photos and the approved P02 lid) at local ≈ (33.41, −30.41), world tops L (−68.59, 516.42, −30.41) and R (135.41, 516.42, −30.41).
- Two sealed absorbent sachets and the recessed filter disc are the same approved P02 presentation geometry (no sachet or filter CAD). They are built in the cinematic with the approved P02 materials, textures, solid-deck underside and photo-exception disc at (30, −16, −28). They are not baked into the site GLB / CAD-line plate.
- Genuine CAD is not altered. The lid skirt at y ≈ −23 has r ≈ 60.33 mm versus the vessel inner mouth r = 60.00 mm (0.33 mm overlap). This is reported, not patched.

## Official product identity

Hamid’s photograph is the official Abadis product photograph `assets/img/c/227665fb9960.webp` on `/products/stand/` and `/en/products/base-and-holder/`.

- FA: پایه ساکشن پرتابل (ترولی)
- EN: Portable suction base (trolley)
- Inventory: P14
- Catalog codes: 060401 short / 060402 long

Official listed specifications: holds up to four 3-litre canisters (12 litres); the regulator and the ON/OFF valve can be fitted; light and easy to move. The official catalog does not print a height or a base span. This is not P06 and not P15 / 060503 / 060504.

## Fit notes — nothing invented
- No intersection with the upright, base or regulator. At jar height the main post is 40 × 40 mm; clearance from the genuine vessel wall to the post face is 20.5 mm, and from the collar-mount to the post face 17.5 mm. (The upright AABB looks tighter, 7.5 mm, only because a 60 mm square collar sits higher on the post, above the jar rim.)
- Closest approach of tubing to the vessel wall remains about 14.7 mm (mesh-to-mesh); tubes do not intersect the vessel or the seated liner.
- After the approved lids were seated, jar-side line endpoints were compared with the genuine PATIENT and VACUUM port mouths. A snap was allowed only if an endpoint already lay within 5 mm of a port. None did, so no endpoint was moved and no hoses or fittings were invented.
  - Yellow `lines_1` (left outward) → left PATIENT: 12.67 mm (Δ +12.16, −2.75, +2.24).
  - Green `lines_5` (right outward) → right PATIENT: 13.40 mm (Δ −13.30, −0.43, +1.57).
  - Yellow `lines_3` (back circuit) → left VACUUM: 18.94 mm; right VACUUM: 50.20 mm (the unrotated P02 lid places the right VACUUM outboard at x = 135.41, while that tube ends inboard at x ≈ 85.8).
  - Yellow `lines_2` (mid circuit) is about 24 mm from the nearest PATIENT on each side and does not meet VACUUM either.
  - Grey `lines_6` / `lines_7` are the regulator wand and do not approach a lid port.
- The supplied stand has three jar-side endpoints per canister (front / mid / back) versus two genuine lid ports. Tube height already nearly matches the port tops (a few millimetres in Y); the miss is in XZ.
- The genuine rear collar-mount is kept in its original assembled pose, facing −Z (opposite the official print). The supplied stand has no hook, clamp or bracket that engages this collar. The collar sits in open air behind each vessel and does not contact the upright, base, regulator or lines.

## Shown stand defaults versus official catalog
- Labelled height 80 cm; model crown 80.5 cm (hose / tube radius past the 80 cm line). Official catalog prints no height, so the model is not assigned to short vs long.
- Labelled base “about 48 cm”; five-caster footprint about 50.7 × 47.3 cm.
- Official text: up to four 3 L jars. Official photograph and this model show two jars. Those jars are now genuine 2 L CAD, not the earlier illustrative Grok cylinders.
- Overall stand extents, including side tubing: 76.7 × 46.8 × 80.5 cm (W × D × H).

## Units and parts
Site file `p14-suction-stand.glb` is in millimetres. Parts: `base`, `upright`, `canister-l` (genuine vessel + collar-mount + seated P02 liner: lid, collar, bag, cap), `canister-r` (same), `regulator`, `lines`.

SHA256 of the millimetre GLB: `e5da7888a7ba75edd7eda269f43520057bd55f93ad54496713fa8ea37e812855`.
Model extents: 767 × 468 × 805 mm (W × D × H). 44,182 triangles (stand 11,754 + two liners 15,020 CAD triangles each, including the 1,194 canister triangles).

## Presentation
Approved cinematic typography, vendor Three.js, 1800vh scroll track, cubic pose easing, exp(-dt*3.2) damping, no idle drift or sway. Polar camera interpolation. Canister materials and official-print shader match the approved p05-2l-cinematic. Liner materials, recessed filter and two sealed sachets match the approved p02-cinematic. Soft studio backdrop and contact shadow are presentation only. Close-up hooks: `?look=print-l`, `print-r`, `print-l-tight`, `print-r-tight`, `collar`, `ports-l`, `ports-r`, `tubes-l`, `tubes-r`, `ports-l-top`, `ports-r-top`.
