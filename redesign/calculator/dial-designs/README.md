# Dial designs — Abadis Med calculator mockups

Three self-contained interactive HTML pages matching the attached dial-calculator mockups.
Each folder has `index.html` (all CSS/JS inline) and `reference.jpg` (the source mockup).

Shared assets (relative from each folder):

- `../../fonts/KalamehWeb-FaNum-*.woff2`
- `../../img/favicon-32.png`

Open any `index.html` in a browser — no build step.

## Folders

| Folder | Matches |
|--------|---------|
| `1-light-neumorphic/` | Light gray neumorphic phone UI: rotary dial with raised knob, three savings cards, bottom nav, moon theme toggle |
| `2-abadis-plus/` | Dark charcoal Abadis+ circular dial with cyan glow, four glass metric cards, preset bed labels |
| `3-cost-time-h2o/` | Dark neon COST / TIME / H2O / Summary dashboard dial with LCD bed count |

## Interaction

- Drag the dial (pointer or touch) to change bed count; numbers update live
- Click preset labels (designs 1 & 2) to jump to that value
- Design 1 only: moon button toggles light/dark neumorphic theme

## Math (demo)

- **1:** `monthly = beds × 325` Toman; annual = ×12; 3-year = ×36 (range 1 000–30 000)
- **2:** `annual = beds × 2 600`; total = ×3 years; per-bed = 2 600; ROI ≈ 18–92% (starts at 0 until first interaction)
- **3:** bed range 10–700; at 32 beds ≈ mockup (COST 28% / 1.24B, TIME 22% / 1 320h, H2O 35% / 5 600 m³, summary 31% / 2 850M Toman)
