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
- **Regulator, gauge face, VAC-nut lettering, knob markings, REG button, green patient connector and hoses:** reconstructed from the official catalog close-ups and the official product cutout, following the layout of Hamid's Grok design (https://winter-rose-lunar-pepper.grok.me). Grok geometry was extracted (no build-mode export prompt was needed) and then corrected to the official photographs. Regulator size is a **photo estimate** matched to official-photo ratios versus the 123 mm vessel OD (gauge width / canister width ≈ 0.327). The gauge housing is the official short black ring, not a long can. Hose OD (13 mm) is a photo estimate. Perspective makes horizontal and vertical px/mm differ. Not factory CAD.
- No invented fluid, no carved filter lattice, no hospital furniture. The fluid-blocking filter described in the official copy is not visible as separate geometry in the official photograph and is not invented here.

## Colour and finish
- Lid teal sampled from the official wall-suction catalog cutout (mid ≈ RGB 20, 117, 145). The cinematic uses a deeper base (0x013e56) with low sheen, clearcoat and environment so ACES tone-mapping reads as that official deep teal rather than a washed cyan.
- Hose green sampled from the official wall-suction cutout (mid ≈ 117, 151, 81). The cinematic base colour is darkened so ACES tone-mapping lands on that mid (the raw mid lifted to a pale mint). Hose OD is a photo estimate of 13 mm, measured against the genuine 123 mm vessel OD in the official cutout.
- The silver circular socket labelled O₂ in the official catalog photograph is a hospital bed-head oxygen terminal, not an Abadis part. Official components are a metal regulator, a fluid-blocking filter, a suction canister with connectors, and a wall clamp. The O₂ terminal is omitted.
- VAC-nut gold sampled from the official catalog close-up (median ≈ 196, 153, 31).
- Gauge scales (BAR / mmHg), VAC / “see no Oil”, LO / H / “vacuum regulator”, and REG are copied from the official catalog close-ups. No brand name is invented where the photo lettering is not reliably readable.
- Chrome, black knob knurling and a faint longitudinal hose bump are surface finishes of reconstructed parts, not new geometry.

## Presentation
- 1800vh track, `exp(-dt*3.2)` damping, no idle drift or sway. Opening camera is the official catalog-cutout viewpoint, with titles kept clear of the hose loop and the canister.
- Package dimensions and the official 377 g weight are identified separately from model extents.

## v4 — lid-port hose seating
- Hoses now sleeve onto the genuine P02 2 L lid spigots (CAD port positions unchanged; only hose start, a short open hose cuff, and the reconstructed green connector are added).
- A green knurled patient connector, reconstructed from the official wall-suction catalog photograph (not factory CAD), sleeves over the genuine left (patient) spigot; a short length of the blue stem remains visible. The patient hose sleeves over that connector and leaves up-left into a wide left loop; the free end sits beside the left of the lid and does not cross it (the thin blue loops on the official lid are cap tethers already in the genuine lid mesh).
- The vacuum hose sleeves directly over the genuine right (shallow, rim-pointing) lid spigot. No extra coloured vacuum connector is added — none is visible as a separate fitting in the official photograph. The hose then clears the toothed rim and follows the official U down the right of the vessel to the regulator barb (bottom just above the vessel floor).
- v3 regulator scale, short gauge housing, deep teal lid under ACES, and mobile layout are unchanged.

## v5 — hose exits matched to the official catalog photograph
- The patient hose no longer climbs the ~60° genuine spigot and then kinks. After a short seat on the reconstructed green connector it flattens left in one continuous curve, stays near lid height, and opens into a wide oval loop; the free end still sits beside the left of the lid.
- The separate vacuum sleeve cuff (which read as a curl or ring on the right port in v4) is removed. The vacuum hose tube now starts on the genuine shallow right spigot, leaves at the right lid edge, and drops down the canister into the official U, without an arch over the lid.
- The genuine P02 spigot geometry is unchanged. The patient spigot's CAD elevation is about 60°, so the green connector still sits more steeply than the official front-view 30–40° apparent angle; only the hose path is flattened to match the photograph. v3 regulator scale, short gauge housing, deep teal lid under ACES, and mobile layout are unchanged.
