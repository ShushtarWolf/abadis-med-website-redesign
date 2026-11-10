# P14 — Portable suction trolley — sources

Official identity: پایه ساکشن پرتابل (ترولی) / Portable suction base (trolley). Product codes 060401 (short) and 060402 (long). Official photograph `227665fb9960`. Official catalog drawing prints ارتفاع ۸۰ سانتی‌متر (H 80 cm).

**Provenance:** stand rebuilt to match the official Abadis trolley photo and drawing (H 80 cm); canisters = genuine 2L CAD; liners = approved 2L bag.

The Grok DuoVac 80 geometry (5-arm base, thin faceted tubes, stick-arm regulator) did not match the official product. This rebuild follows the official photo and drawing as the source of truth for the stand. No factory CAD exists for the trolley itself. The two canisters remain genuine Abadis 2 L vessel CAD with the official print; each holds the approved P02 2 L liner (lid seated on the rim, bag hanging inside). Two sealed sachets and the recessed filter are cinematic-only presentation geometry and are not in this GLB or the CAD-line plate.

## Stand (reconstructed from the official photo and drawing)

- Four-arm X base of square white tube, about 40 cm caster-to-caster span (from the official photo’s base-to-jar proportion; the earlier 48 cm figure was the Grok span), with four black twin-wheel casters.
- Square white post. A pale-green collar at lid height and a small front badge, as in the official photo.
- Canisters sit high and close to the pole. Their genuine rear collar-mounts face the upright and engage a simple holder/clamp modelled from the part visible in the official photo (not an invented fitting). Prints face forward/outward: logo on the outer side, volume scale toward the pole, matching the official photo. The left canister is yawed −48° (logo to the outer-front); its collar-mount then points inward and slightly aft rather than straight at the pole — print match was prioritised. The right canister stays at +72° so the mount faces the pole and the print already matches. The right liner is yawed 180° on the vessel so the genuine PATIENT / VACUUM ports follow the official serial circuit.
- Tubes are rebuilt as smooth `TubeGeometry` (24 radial segments, Catmull-Rom paths), not the original 9-sided Grok strings:
  - short yellow patient stub on **left PATIENT**;
  - thick yellow arch, **left VACUUM → right PATIENT** (serial link, left jar then right);
  - yellow loop from the arch up into the underside of the regulator;
  - short green overflow loop on **right VACUUM**;
  - clear/grey supply hose from the top inlet of the regulator, looping down the left side.
  Ends sleeve the genuine P02 nipples. No free dangling tails.
- Regulator on top of the pole: off-white/grey body, round front gauge, large ribbed knob to the right, inlet fitting on top, outlet barb underneath — reconstructed from the official photo and drawing, not factory CAD.
- Official drawing height is 80 cm floor to top. This model is about 812 mm to the top of the inlet/hose (12 mm over, honest). Official catalog lists up to four 3 L jars; this model follows the official photo (two 2 L).

## Canisters and liners (unchanged genuine CAD)

- Canisters: genuine P05 2 L CAD, official print (`official-2l-print.png`), same shader as p05-2l-cinematic.
- Liners: approved P02 2 L bag CAD (lid, collar, bag, cap). The tethered cap is folded down onto the lid deck so it does not stand up beside the patient port (the official trolley photo shows no upright cap).
- SHA256 of the millimetre GLB: `4b1ebbc66e7d69249b3003768ce697ac1b70cfd3e765f3e2e3745aa82c34ed88`.

## Explode

Lid and bag lift out of each canister; tube ends stay with the stand and detach cleanly; jars part sideways; regulator lifts.
