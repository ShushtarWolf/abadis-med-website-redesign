# P17 — Wall suction VR-A1 (2 L, 0402202)

## Official product
- FA name: ساکشن دیواری دو لیتری مدل VR-A1
- EN name: 2-litre wall suction, model VR-A1
- Official code for this 2 L set: **0402202**. Family also includes 0402201 (1 L) and 0402203 (3 L).
- Official EN catalog weight for 0402202: **377 g** (Grok listed 371 g; the official figure is used).
- Official 12.2 × 27 cm values are the **individual package dimensions** of the 2 L canister (0402012), not a measured body claim for the set. Same honesty rule as P05.
- Official composition photograph: abadis-med.com cutout `site/assets/img/c/d981ab7fae6e-1600.webp` (also the cover of `wall-suction-catalog-Fa.pdf`). Canister + teal lid + green hoses + regulator on a teal ground. No hospital console.
- Official catalog PDF, page 2: three close-up photographs of the regulator (3/4 left with REG, front with yellow VAC nut and gauge, 3/4 right with the black knob) and the official feature list. **No official dimensioned drawing of the regulator or the set was supplied.** The CAD-line sketch uses the official catalog/photo viewpoint and states this honestly.
- Hospital bed-head console and the O₂ terminal visible in the uncut studio photograph are not Abadis parts and are omitted from the product GLB and the sketch.

## Geometry, labelled honestly
- **Canister (vessel + collar/rear bracket):** genuine 2 L CAD from `2L pit.partlens`, unchanged, same mesh as approved P05 (`p05-2l-canister-cad.glb`). Official 2 L print from AMR_4901 (middle vessel) is applied in the cinematic with the approved P05 mapping — front exterior only, no invented artwork.
- **Liner (lid, collar, bag):** genuine approved 2 L suction-bag CAD (`p02-2l-cad.glb`). The original port cap is omitted because the official assembled photograph shows hose fittings on the ports, not the cap. Yaw only (photo-estimated, so the two genuine lid barbs sit left and right on the front of the lid).
- **Regulator, gauge face, VAC-nut lettering, knob markings, REG button, elbows and hoses:** reconstructed from the official catalog close-ups and the official product cutout, following the layout of Hamid's Grok design (https://winter-rose-lunar-pepper.grok.me). Grok geometry was extracted (no build-mode export prompt was needed) and then corrected to the official photographs. Sizes of the regulator and hoses are **photo estimates** (270 mm genuine vessel height and 123 mm OD used as the scale; perspective makes horizontal and vertical px/mm differ). Not factory CAD.
- No invented fluid, no carved filter lattice, no hospital furniture. The fluid-blocking filter described in the official copy is not visible as separate geometry in the official photograph and is not invented here.

## Colour and finish
- Lid teal sampled from official 2 L lid photographs (p2-main / p2-g1); rendered darker than the raw mid so ACES tone-mapping does not lift it to baby-blue.
- Hose green sampled from the official wall-suction cutout (mid ≈ 117, 151, 81).
- VAC-nut gold sampled from the official catalog close-up (median ≈ 196, 153, 31).
- Gauge scales (BAR / mmHg), VAC / “see no Oil”, LO / H / “vacuum regulator”, and REG are copied from the official catalog close-ups. No brand name is invented where the photo lettering is not reliably readable.
- Chrome, black knob knurling and a faint longitudinal hose bump are surface finishes of reconstructed parts, not new geometry.

## Presentation
- 1800vh track, `exp(-dt*3.2)` damping, no idle drift or sway. Opening camera is the official catalog-cutout viewpoint, with titles kept clear of the hose loop and the canister.
- Package dimensions and the official 377 g weight are identified separately from model extents.
