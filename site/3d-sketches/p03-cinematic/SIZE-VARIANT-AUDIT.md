# P01–P25 size-variant audit — 8 November 2026

## Rule and verified inputs
New owner permission covers size-only reconstructions from a genuine CAD parent of the SAME construction, honestly labelled adapted. It does not create a CAD parent for unrelated products. Known original PartLens inventory consists only of 1L/2L liner assemblies, 1L/2L/3L rigid canisters, duplicates and complete files containing those components. The misleadingly named 3L complete is canister-only, never a 3L bag source.

Sources opened this turn:
- https://www.abadis-med.com/en/products/suction-bag/ — only nominal 1, 2, 3 L liner sizes; Ø11 cm, H15.5/24.5/39 cm; gel powder and filters. The “up to 8 liters” row/base arrangement is NOT an 8 L individual liner size.
- https://www.abadis-med.com/en/products/canisters/ — 1/2/3 L canisters, wall systems, specimen cup and fat-collection system.
- https://www.abadis-med.com/en/suction-tube/ — transparent/ribbed PVC 25/30/35 size names, standard 2 m; small/large fingertip controllers. No CAD parent available.
- https://www.abadis-med.com/en/products/base-and-holder/ — short/long trolleys, separate clamp and rear clamp parts; no genuine trolley/clamp CAD parent.
- https://www.abadis-med.com/en/products/connections/ — T, adapter, silicone hose, regulator, plastic/metal valve and accessories.
- https://www.abadis-med.com/en/products/filters/ — separate antibacterial, flow-stopper and sintered constructions. Read via public HTML fallback after WebFetch timeout; saved filters-official.txt.
- https://www.abadis-med.com/en/products/other-products/ and /en/products/oral-hygiene/ — brush, tube holder, kidney dish, floor suction; saved oral-hygiene-official.txt.
- Existing P01–P25 mapping: /workspace/abadis-cad-inventory/build.py and approved sketch provenance.
- Original manufacturer diagrams read: site/assets/img/p/p2-g4.webp and p3-g5.webp. Both state Ø11 cm; heights24.5 and39 cm respectively. They are product nominal dimensions, not packaging dimensions.

## Result
**One newly eligible missing design: P03 3 L liner.** Parent is the genuine/approved P02 2 L liner, same construction confirmed explicitly by the owner, with THREE sealed absorbent sachets. Build it now as a size-adapted reconstruction, not original 3L CAD. P01/P02 and all P05 canister sizes are already complete; there are no further currently verified eligible missing size-only designs.

| Product | Decision / evidence |
|---|---|
| P01 1 L liner | Already original-CAD-backed and delivered; no missing nominal size here. |
| P02 2 L liner | Already delivered; genuine parent for P03; two sachets remain unchanged. |
| P03 3 L liner | ELIGIBLE NOW: same-construction parent P02 + owner confirmation + nominal Ø11×H39 cm; three illustrative sealed sachets. Original 3L CAD still absent. |
| P04 gel powder / internal filter | Standalone powder/sachet/filter CAD absent. Existing photo-guided illustrative exceptions are not original CAD parents. Filter chemistry/construction variants are not mere sizes. |
| P05 rigid canisters | Genuine 1/2/3 L CAD and all three cinematics/sketches already delivered. No additional nominal canister size established. |
| P06 complete wall suction package | Distinct regulator, gauge, valves, hose, wall bracket and assembly missing. Canister CAD alone is not a complete-system parent; cannot fabricate a bigger/smaller package. |
| P07 specimen collection cup | Different cup/sealing/accessory construction; no genuine parent. Not a resized canister. |
| P08 sterile fat collection/injection canister | Different closed reservoir/connection/pump system; no genuine parent. Not a size-only P05 variant. |
| P09 medical suction tubing | Official 25/30/35 size families and 2 m length are real, but no tubing CAD parent. Transparent versus ribbed is also a construction difference. Size labels carry no unit assumption. Hold pending CAD/drawings. |
| P10 fingertip controller | Official small/large family exists, but no genuine controller CAD parent or dimensional mapping. Bag ports cannot substitute. Hold pending source. |
| P11 antibacterial/hydrophobic disc filter | Different filter housing/membrane construction; no parent CAD. Not a scaled canister or recessed illustration. |
| P12 flow-stopper filter | External protector has a distinct 3 cm×7.2 cm housing; no original CAD. Not the illustrative internal disc. |
| P13 porous PE filter | Distinct porous element 18.2×29.5 mm, no original CAD; no supported size-only CAD parent. |
| P14 four-canister portable trolley | Official short/long models exist, but no trolley CAD parent or verified per-model size mapping. A canister is not a trolley. |
| P15 wall clamp/holder | Separate source product060503; no standalone original CAD. Integrated canister mount is not proof of this geometry. |
| P16 rear clamp component | Separate source product060504; no original CAD. Not a scaled P15 or the canister-integrated bracket. |
| P17 T connector | Specific vacuum-balancing component for2/3 L systems; no CAD. Usage with two sizes does not imply two connector sizes or authorize a bag-port substitute. |
| P18 straight adapter | Separate6 cm connector, no CAD parent. Cannot derive from canister/port appearance. |
| P19 silicone connecting hose | Different material/product from PVC suction tubing; no CAD parent or established missing nominal size. |
| P20 adult/child regulator | Official two models, but calibration/internal/gauge differences unverified and no CAD parent; not safe to assume mere size scaling. |
| P21 on/off valve | Plastic/metal options are material/construction variants, not just sizes; neither has genuine CAD. |
| P22 hose/accessory set | Assembly includes hose, adapter and T. Official30 cm hose /37 cm with connectors are not two new nominal products; no assembly/parts CAD. |
| P23 suction toothbrush | Hair/swab head alternatives are construction changes; no CAD parent. |
| P24 endotracheal tube holder | Separate adjustable holder/strap construction, no CAD parent. |
| P25 600 cc kidney dish / floor suction | Two unrelated constructions; neither is a smaller canister. No genuine CAD parent; 600 cc does not authorize a600 mL bag/canister. |

## Conditional future research, NOT permission to build now
P09 tubing, P10 small/large fingertip, P14 short/long trolley are source-supported size families, but each needs its own genuine CAD parent and a verified dimension/construction map. P20 adult/child also needs internal-functional confirmation; do not treat it as a simple size variant. Filter/no-powder/primary-versus-final bag configurations are not newly authorized size-only products. Do not invent0.5/4/5/8 L liners, alternate tube units, or substitute unrelated geometry. Stop after P03 and report.
