# Brand, themes and motion rules

## Brand colours (teal family — "colorbook")
| Token | Hex | Use |
|---|---|---|
| teal-900 | `#015F61` | primary hover / deep buttons |
| teal-800 | `#066163` | primary brand, buttons, H accents (light theme) |
| teal-750 | `#05686b` | secondary brand |
| teal-700 | `#087673` | accent dots, dark-theme buttons |
| teal-650 | `#0e7475` | tertiary |
| mint-100 | `#e8f3f3` | chips, surfaces, theme-color |
| mint-50  | `#f3fafa` | page background (light) |
| deep     | `#0b2e32` / `#071c1e` | dark bands, footer, table heads |

Rules from the user: **no blood/red accents**; on teal pages **no yellow/lime accents** (except inside noir).
Lid colours in product tables (teal / yellow / red swatches) are product facts, not UI accents.

## Three theme modes (implemented in `site/assets/css/site.css`)
- **light** (`data-theme="light"`, default) — mint background, white cards, teal brand.
- **dark** (`data-theme="dark"`) — deep teal `#061719` background, cyan-teal text accents `#5fd0d1`, buttons `#087673`.
- **noir** (`data-theme="noir"`) — purple palette from the scroll-scrub `/noir/` demo: bg `#0a0a12`, accent `#a78bfa`, deep `#6d28d9`, soft `#c4b5fd`. The demo's rose/blood colours (`#e11d48`, `#fb7185`) are intentionally **not** used.

Switcher: header segmented control «روشن / تیره / نوآر». Choice persists in `localStorage["abadis-theme"]`.
`?theme=light|dark|noir` in any URL also sets (and saves) the theme — handy for review links.
A tiny inline script in `<head>` applies the theme before paint (no flash).

## Typography
- **Kalameh** (FaNum woff2, weights 400–900) in `site/assets/fonts/kalameh/`. Also present in `concept-preview/brand/fonts/`.
- Follow `docs/persian-typography.md`: line-height ≥ 1.7, `letter-spacing: 0`, Persian digits, `dir="ltr"` only on phone numbers / codes.
- Tone: Persian, casual-professional; product copy stays **verbatim** from abadis-med.com.

## Motion rules (user decision, 2026-10-06)
- **No mouse-move / mouse-reactive effects anywhere**: no parallax, cursor blobs/trails, magnetic buttons, hover tilt, hover lift/scale.
- Allowed: scroll-driven reveal (fade-up once), click interactions (lightbox, menu, theme), drag-to-rotate on the 3D viewer only.
- Hover only changes colour on buttons (no movement).
- `prefers-reduced-motion` disables reveal and the mosaic intro.
