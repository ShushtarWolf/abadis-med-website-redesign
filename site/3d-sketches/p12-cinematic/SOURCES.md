# P12 — Flow-stopper (inline) filter

## Geometry source — not original factory CAD
Hamid supplied a Grok-built reconstruction at https://cloud-lark-beacon-cobalt.grok.me (Clearline / “Inline filter”). The page is a clear housing with ribbed end caps, a white cartridge inside the barrel, and stems with a longer inlet and a shorter outlet, matched to his photograph, plus the official dimensioned drawing. It includes cutaway and explode views.

This cinematic uses that published geometry as-is. No invented parts (no extra fittings, no resized barbs, no new cage). Only materials, lights and cameras are presentation choices. The half-cut and exploded poses use the same source parts and the source section profiles.

The GLB is not a static file on that host; it is generated in the browser from:

- `assets/filter-geometry-DQ4iJAPj.js` — `PARTS`, `MEDIA`, `shellGeometry()`, `createMediaGeometry()`, `createSectionGeometries()`, `exportFilterGlb()`
- `assets/filter-stage-D0MXYiLz.js` — explode offsets, cutaway clip plane, part labels

Cached copies, the photograph, the drawing, `og.jpg` and this export live in `/workspace/_qa_p12/`.

## Shown defaults versus official catalog numbers
The Clearline page, as opened, shows:

- overall length 7.2 cm
- body diameter 3.0 cm (radius 1.5 cm)
- inlet stem 1.8 cm (longer)
- inlet cap 0.86 cm (ribbed)
- barrel / housing 2.28 cm
- outlet cap 0.86 cm (ribbed, mirrored)
- outlet stem 1.4 cm (shorter)
- cartridge (media) radius 1.06 cm, length 1.66 cm, centred on the barrel

Those are the dimensions of this mesh. The same official Abadis drawing used as “Drawing” on that page (site asset `assets/img/filters/stop-2.webp`, also Hamid’s `ref-drawing.jpg`) prints **Ø 3.0 cm, length 7.2 cm, weight 10.5 g**. Length and diameter therefore match the official drawing. Weight is listed only on the official drawing, not as a Clearline UI default, and is reported on the sketch but is not a modelled property.

Official product identity: فیلتر قطع کننده جریان (مسدود شونده) / Flow-stopper filter (shutoff), product code 040502, inventory P12. The photograph on the Clearline page is the same official product photograph as `assets/img/filters/stop-1.webp`. The official site describes a polycarbonate frame whose inner element is the Abadis porous filter. This is that clear inline filter, not the earlier mistaken “under-lid teal snap-fit cage” reconstruction in the old all-products catalog.

## Units and parts
Source download: GLB in centimetres (no extra scale). The site file `p12-inline-filter.glb` is the same mesh in millimetres (× 10) so it matches the other Abadis cinematics. Parts: `inlet`, `inletCap`, `barrel`, `outletCap`, `outlet` (lathed outer + inner shells) and `cartridge` (lathed media solid). The half-cut caps are the source section profiles, shown only during the mid-story cut; they are not new parts. The explode is a presentation pose of the existing parts, using the source offsets.

SHA256 of the millimetre GLB: `72ce1ff0975c76acdb8c85c7f8980ea2b1423f433f3c3216b43141fa88fbe45d`.
Model extents: 72 × 30 × 30 mm (W × H × D).

## Presentation
Approved cinematic typography, vendor Three.js, 1800vh scroll track, cubic pose easing, exp(-dt*3.2) damping, no idle drift or sway. Polar camera interpolation. Clear / transparent plastic and the white cartridge finish are approximate real-time materials matched to the photograph, not factory optical specifications. Soft studio backdrop and contact shadow are presentation only.
