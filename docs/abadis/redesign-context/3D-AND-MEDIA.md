# 3D model and media

## GLB
- `site/assets/abadis-scrub-parts.glb` (~1.1 MB, nodes `lid` + `body`) — 2 L suction bag. Viewer: `site/assets/js/product-viewer.js` (three.js vendored in `site/assets/vendor/three/`, HDR `site/assets/env/studio_small_09_1k.hdr`).
- Other GLBs: `concept-preview/models/*.glb` (1L/2L centred, AMR_4894-web). Box copies of original/lid-body GLBs exist outside the repo.
- Rule: rotation **only by explicit drag** (pointer down → move). No hover-follow, no idle mouse tracking. Lazy-loaded when near the viewport; falls back to `product-still.webp` without WebGL.
- Phase-1 spec marks interactive 3D as optional — keep it a section, never the whole IA.

## Videos
- `site/assets/media/hero-mosaic.mp4` (OR team, 640 px, ~1 MB) and `or-mosaic.mp4` (OR loop, ~130 KB) — re-encoded small on purpose, because they are always shown as a mosaic.
- Originals (1080p, 5 MB) live in the scroll-scrub demo `abadis/media/`.

## Mosaic / square-grid effect (مربع مربعی)
`.mosaic` blocks in `site/assets/js/site.js`:
1. the `<video>` decodes off-screen;
2. each frame is drawn into a tiny canvas (1 px per tile, cover-cropped);
3. it is scaled up with smoothing off → crisp squares, then a repeating gap pattern draws a thin grid line between tiles (gap colour = `--mosaic-gap`, per theme);
4. on load the tiles **resolve coarse → fine** (≈1.8s); as the hero scrolls away tiles grow coarser again (scroll-driven, not mouse);
5. paused when off-screen; reduced-motion users get a static fine mosaic.
Tile size per block via `data-tile` (default 12 px; mobile smaller).
