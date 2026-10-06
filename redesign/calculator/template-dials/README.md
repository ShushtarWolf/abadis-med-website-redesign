# Abadis template dials

Three savings-calculator dial samples built **on the official Abadis website template** (header, footer, theme switch), not as standalone phone mockups.

Intended publish path on GitHub Pages:

```
site/template-dials/
  1-neumorphic/index.html
  2-abadis-plus/index.html
  3-cost-time-h2o/index.html
```

Asset paths from each dial page use depth `../../` (e.g. `../../assets/css/site.css`).

## Themes

Site chrome theme switch (persisted in `localStorage` key `abadis-theme`):

| Button | `data-theme` | Notes |
|--------|--------------|--------|
| روشن   | `light`      | Default teal light |
| تیره   | `dark`       | Teal dark |
| نوآر   | `noir`       | Vintage purple / violet |

Dial surfaces adapt via `[data-theme="dark"]` / `[data-theme="noir"]` (and CSS variables from `site.css`).

## Folders

1. **`1-neumorphic/`** — Rotary neumorphic dial, snap presets (۱۰۰۰ / ۵۰۰۰ / ۱۵۰۰۰ / ۳۰۰۰۰), monthly / annual / 3-year cost cards from Abadis `surgery(n)` formula.
2. **`2-abadis-plus/`** — Fixed 270° sweep dial with magnetic snap to ۱۰۰۰ / ۵۰۰۰ / ۱۰۰۰۰ / ۱۵۰۰۰ / ۳۰۰۰۰; four savings cards (3-year cost, water, annual cost, hours).
3. **`3-cost-time-h2o/`** — COST / TIME / H₂O / summary cards; bed dial uses Abadis `beds(a, b≈0.35a)` formula (OR + estimated ICU).

## Chrome requirements (all pages)

- Early theme boot script + `header class="header solid"`
- Nav / logos / footer / copyright identical to site template
- `../../assets/css/site.css` + `../../assets/js/site.js` (defer)
- Kalameh via site.css only

## Formulas

```
surgery: water=n*1.6*9.3, cost=n*2.5*85000, hours=n*1.7/60*2.2*7.1
beds:    water=((a*254)+(b*67))*1.6*9.3, cost=((a*200)+(b*50))*2.5*85000, hours=((a*254)+(b*67))*1.7*2.2*7.1/60
```

Dial interaction CSS/JS is inlined per page; site chrome comes from shared assets.
