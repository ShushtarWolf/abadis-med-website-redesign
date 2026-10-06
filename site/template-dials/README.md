# Abadis template dials — real calculator variables only

Three savings-calculator dial samples built on the official Abadis website template (solid header, nav,
theme switch روشن / تیره / نوآر stored in `localStorage` key `abadis-theme`, site footer, Kalameh FaNum via `site.css`).
All three pages have identical content; only the dial styling differs.

Publish path on GitHub Pages: `site/template-dials/{1-neumorphic,2-abadis-plus,3-cost-time-h2o}/index.html`
(asset paths use depth `../../`).

## Content (mirrors https://abadis-med.com/محاسبه-گر/ exactly)

1. **بر مبنای تعداد عمل جراحی در سال** — input «تعداد عمل در سال» (0–30000, step 100; presets ۱٬۰۰۰ / ۵٬۰۰۰ / ۱۰٬۰۰۰ / ۱۵٬۰۰۰ / ۲۰٬۰۰۰ / ۲۵٬۰۰۰).
2. **بر مبنای تعداد تخت در مراکز درمانی** — two separate inputs «تعداد تخت اتاق عمل» and «تعداد تخت ICU|CCU»
   (each 0–700, step 1, its own dial + steppers; combination chips from the original dial: ۱۰+۱۰, ۲۰+۱۰, ۵۰+۲۰, ۱۰۰+۵۰, ۳۰۰+۱۰۰, ۷۰۰+۷۰۰).

Each section shows exactly three results:
«صرفه جویی در مصرف آب (لیتر)», «هزینه مربوط به شست و شو و ضد عفونی (تومان)», «صرفه جویی در زمان کادر درمان (ساعت)».
Values are rounded to whole numbers and shown in Persian digits with thousands separators. Units: liters, Toman, hours.

## Formulas

```
surgery (n):  water = n*1.6*9.3          cost = n*2.5*85000             hours = n*1.7/60*2.2*7.1
beds (a, b):  water = ((a*254)+(b*67))*1.6*9.3
              cost  = ((a*200)+(b*50))*2.5*85000
              hours = ((a*254)+(b*67))*1.7*2.2*7.1/60
```

No other metrics are shown (no monthly/multi-year splits, return-on-investment, per-bed savings, percentages, summary cards,
unit rescaling or estimated ICU counts).

## Dial styles

1. `1-neumorphic/` — light neumorphic rotary dials (270° sweep, lit tick scale).
2. `2-abadis-plus/` — Abadis+ dials with 270° arc; surgery dial keeps the magnetic presets (`applyMagnet`, `MAGNET_DIST`,
   `snapIfNear` on release — snaps only when released within `MAGNET_DIST` of a preset, so any value can still be set).
3. `3-cost-time-h2o/` — COST / TIME / H₂O monitor look; the English tags are decorative, values are the three real results.

Interaction on every page: drag/rotate the dial (mouse or touch), +/− steppers (press and hold to repeat),
arrow/PageUp/PageDown/Home/End keys on the focused dial, and the preset buttons above.
Source generator (not published): `abadis-calculator/template-dials-build/` (`node build.js`).
