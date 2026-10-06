# Abadis redesign — TEST REPORT

- **Date:** 2026-10-06T16:40:10.017Z
- **SHA:** `e8efab8` (branch tip when suite ran; site HTML unchanged since prompt 0 `20a5a37`)
- **Base:** http://127.0.0.1:8080
- **Pages:** 219
- **Totals:** ✅ 12 · ❌ 1 · ⚠️ 3 · ❓ 0

## Results

| # | Test | Scope | Result | Details / shots |
|---|------|-------|--------|-----------------|
| 1 | Internal links (linkinator) | full recurse | ⚠️ warn | broken=0 |
| 2 | 404 and broken assets | 219 pages | ✅ pass | bad=0 |
| 3 | Console / page errors | 219 pages | ✅ pass | console=0 |
| 4 | Three themes + color contrast | 7 pages × 3 themes | ⚠️ warn | {"themeOk":true,"contrastFails":[{"page":"/contact/","theme":"light","count":1,"nodes":3}],"themeFails":[]} |
| 5 | Responsive / no horizontal scroll | 8 pages × viewports | ✅ pass | overflow=0 |
| 6 | Lighthouse mobile | 5 key pages | ⚠️ warn | lh-calc.json: a11y 100 / perf 85 / seo 63; lh-csr.json: a11y 100 / perf 71 / seo 63; lh-home.json: a11y 100 / perf 74 / seo 63; lh-news.json: a11y 98 / perf 84 / seo 63; lh-suction.json: a11y 96 / perf 78 / seo 63 |
| 7 | RTL / lang=fa | representative FA pages | ✅ pass | fails=0 |
| 8 | Kalameh font | home/about/news/products | ✅ pass | fails=0 |
| 9 | Calculator formulas | /calculator/ + 5 designs have ABADIS_FORMULAS | ✅ pass | formulas=ok |
| 10 | CSR Zagros scroll | 375 + 1440 | ✅ pass | {"results":[{"vp":{"w":375,"h":812},"s0":{"scrollY":80,"mid":0,"green":0},"s50":{"scrollY":1218,"mid":1,"green":0.026},"s100":{"scrollY":2436,"mid":1,"green":1},"progressed":tru… |
| 11 | Suction-bag 3D viewer | 375 + 1440 + WebGL-off probe | ✅ pass | {"results":[{"vp":{"w":375,"h":812},"hasCanvas":true,"w":375,"h":812,"overflow":false,"glbStatus":200,"ok":true},{"vp":{"w":1440,"h":900},"hasCanvas":true,"w":1440,"h":900,"over… |
| 12 | Theme toggle cycle + persist | home | ✅ pass | {"seq":["dark","noir","light"],"stored":"light","after":"light","rmTheme":"dark","cycleOk":true,"persistOk":true} |
| 13 | Header transparent / scrolled / on-light | home about products news (light) | ✅ pass | fails=0 |
| 14 | Forms contact + careers | /contact/ /careers/ | ✅ pass | {"hasLead":true,"contactEmptyBlocked":true,"contactMailtoBuilt":true,"contactMailto":"mailto:info@abadis-med.com?subject=%D8%AF%D8%B1%D8%AE%D9%88%D8%A7%D8%B3%D8%AA%20%D8%A7%D8%B… |
| 15 | Brand rules | nav order, footer certs, yellow CSS, pointermove | ✅ pass | yellow=0; pointermove=0 |
| 16 | Meta title/description/h1/alt | 219 pages | ❌ fail | dupTitles=1; missingAltPages=0 |

## Bugs (do not fix in this prompt)

| Severity | Test | Page | Detail |
|----------|------|------|--------|
| major | 16 | /install-guide/tanks/ | duplicate title with /articles/2615/: راهنمای نصب مخازن — مخازن طبی آبادیس |
| minor | 1 | / | 25 unique hrefs to abadis-med.com (non wp-content); 18 post-card ext on news/articles indexes |
| minor | 4 | /contact/ | contrast light: 1 |
| minor | 16 | /news/1124/ | missing meta description |

## Lighthouse (mobile)

| Page | Perf | a11y | Best practices | SEO |
|------|------|------|----------------|-----|
| http://127.0.0.1:8080/calculator/ | 85 | 100 | 100 | 63 |
| http://127.0.0.1:8080/csr/ | 71 | 100 | 100 | 63 |
| http://127.0.0.1:8080/ | 74 | 100 | 100 | 63 |
| http://127.0.0.1:8080/news/ | 84 | 98 | 100 | 63 |
| http://127.0.0.1:8080/products/suction-bag/ | 78 | 96 | 96 | 63 |

## Screenshots (curated)

- `docs/abadis/test-shots/1440__light__home.png`
- `docs/abadis/test-shots/1440__dark__home.png`
- `docs/abadis/test-shots/1440__noir__home.png`
- `docs/abadis/test-shots/375__light__home.png`
- `docs/abadis/test-shots/1440__light__about.png`
- `docs/abadis/test-shots/1440__light__products__suction-bag.png`
- `docs/abadis/test-shots/375__light__suction-bag.png`
- `docs/abadis/test-shots/1440__light__csr.png`
- `docs/abadis/test-shots/1440__light__csr-scroll-0.png`
- `docs/abadis/test-shots/1440__light__csr-scroll-50.png`
- `docs/abadis/test-shots/1440__light__csr-scroll-100.png`
- `docs/abadis/test-shots/375__light__csr-scroll-0.png`
- `docs/abadis/test-shots/1440__light__news.png`
- `docs/abadis/test-shots/1440__light__calculator.png`
- `docs/abadis/test-shots/1440__light__customers.png`
- `docs/abadis/test-shots/1440__light__contact.png`
- `docs/abadis/test-shots/768__light__home.png`
- `docs/abadis/test-shots/1440__noir__csr.png`
- `docs/abadis/test-shots/375__light__products__suction-bag.png`
- `docs/abadis/test-shots/1440__light__suction-bag.png`
- `docs/abadis/test-shots/1440__light__suction-bag-scrub.png`
- `docs/abadis/test-shots/375__light__suction-bag-scrub.png`
- `docs/abadis/test-shots/1440__dark__about.png`
- `docs/abadis/test-shots/1440__noir__news.png`
- `docs/abadis/test-shots/375__light__calculator.png`
- `docs/abadis/test-shots/375__light__contact.png`
- `docs/abadis/test-shots/768__light__csr.png`
- `docs/abadis/test-shots/375__light__news.png`

## How to re-run

```bash
cd tools/test && npm i && npx playwright install chromium
# from repo root:
bash tools/test/run-all.sh
# or: cd tools/test && npx playwright test site.spec.mjs --reporter=list
```

Artifacts under `tools/test/out/` are gitignored. This report and curated shots are committed.
