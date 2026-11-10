# P14 — Portable suction base (trolley)

## Geometry source — not original factory CAD
Hamid supplied a Grok-built reconstruction at https://zinc-cliff-horizon-solar.grok.me (DuoVac 80 / “Dual-canister suction stand”). He sent it as the stand. The page is a five-caster mobile base, a square upright, two collection jars at an illustrative 2 L scale, a vacuum regulator, and yellow / green / grey tubing, matched to his photograph, plus a drawing marked 80 cm tall. It includes explode and X-ray views, and a Download GLB (true scale, metres).

This cinematic uses that published geometry as-is. No invented parts. Genuine P05 2 L canister CAD was not swapped in. Only materials, lights and cameras are presentation choices. The explode is a presentation pose of the existing parts, using the source offsets (jars part sideways, regulator lifts). Collected-volume fluid is a page slider, not a product part, and is omitted (exported at 0). Selection rings and the on-page dimension sprite are presentation-only and are omitted.

The GLB is generated in the browser from `assets/scene-TVCgftDd.js` (part constants, builders, `exportGlb`). Cached copies, Hamid’s photograph and drawing, the official product photograph, the page download `duovac-80-page.glb`, and this millimetre export live in `/workspace/_qa_stand/`.

## Official product identity
Hamid’s photograph is the same official Abadis product photograph as `assets/img/c/227665fb9960.webp` on the Stands & Holders page (`/products/stand/`, EN `/en/products/base-and-holder/`). Official names:

- FA: پایه ساکشن پرتابل (ترولی)
- EN: Portable suction base (trolley)
- Inventory: P14 (پایه ساکشن پرتابل ترولی ۴ مخزنه)
- Catalog codes: 060401 Abadis short portable suction base (trolley) / پایه ساکشن پرتابل کوتاه (ترولی) آبادیس; 060402 Abadis long portable suction base (trolley) / پایه ساکشن پرتابل بلند (ترولی) آبادیس

Official listed specifications: holds up to four 3-litre canisters (12 litres) at once; the regulator and the ON/OFF valve can be fitted; light and easy to move. The official catalog does not print a height or a base span.

This is not P06 (complete wall suction package) and not P15 / the wall canister clamp or rear portable clamp (060503, 060504).

## Shown defaults versus official catalog numbers
The DuoVac 80 page, as opened, shows:

- height 80 cm, floor to crown
- base: five casters, about 48 cm across
- jars: two, illustrative 2 L scale
- lines: yellow circuit, green overflow, grey supply
- “Other sizes are matched by eye.”
- “Jar numbers aren’t readable in the photos, so the 0.5–2.0 L marks are illustrative.”

Those are the dimensions of this mesh, with the following measured extents:

- labelled height 80 cm; model crown 80.5 cm (hose / tube radius past the 80 cm line)
- labelled base “about 48 cm”; model five-caster footprint about 50.7 × 47.3 cm (not a perfect circle)
- overall extents 76.7 × 46.8 × 80.5 cm (W × D × H), including side tubing

Mismatches with the official catalog / photo page:

- Official text: up to four 3 L jars. Official photograph (and this model) show two jars at an illustrative 2 L scale.
- Official catalog has short (060401) and long (060402) trolleys but does not print 80 cm, so this model is not silently assigned to one of those codes.
- Official photograph does show readable jar marks and the Abadis logo; the DuoVac page still treats the 0.5–2.0 L marks as illustrative because “numbers aren’t readable in the photos.” This cinematic keeps that honest label and does not invent official print.

## Grok jars versus genuine P05 2 L canister CAD
Not swapped in. The supplied jars are simple clear cylinders (body Ø 11.0 × H 24.0 cm) with a teal lid, green tick marks, and a ring-and-cross emblem. Genuine approved P05 2 L canister CAD is a wider, taller vessel (extents Ø 12.9 × H 27.0 cm) with the characteristic rear collar-mount and the official photo print. The two are visibly different in proportion and in missing / extra parts.

## Units and parts
Source download: GLB in metres. The site file `p14-suction-stand.glb` is the same mesh in millimetres (× 1000). Parts: `base`, `upright`, `canister-l`, `canister-r`, `regulator`, `lines`.

SHA256 of the millimetre GLB: `49d9cedfb888a248414f001eeddd72052311d310da3c3a6c83114916625f38e5`.
Model extents: 767 × 468 × 805 mm (W × D × H). 16,498 triangles.

## Presentation
Approved cinematic typography, vendor Three.js, 1800vh scroll track, cubic pose easing, exp(-dt*3.2) damping, no idle drift or sway. Polar camera interpolation. Materials are approximate real-time finishes, not factory optical specifications. Soft studio backdrop and contact shadow are presentation only. Jar volume marks are illustrative, as on the supplied page.
