# Abadis redesign — TEST REPORT

- **Date:** 2026-10-07T13:37:00.621Z
- **SHA:** `ae3ea53bc8ac06788b7a164b31f4e2b4180d8376`
- **Base:** http://127.0.0.1:8080
- **Pages:** 403
- **Totals:** ✅ 14 · ❌ 0 · ⚠️ 2 · ❓ 0

## Results

| # | Test | Scope | Result | Details / shots |
|---|------|-------|--------|-----------------|
| 1 | Internal links (linkinator) | full recurse | ✅ pass | total=1658; broken=0; livePostHrefs=0 |
| 2 | 404 and broken assets | 403 pages | ✅ pass | bad=0 |
| 3 | Console / page errors | 403 pages | ✅ pass | console=0 |
| 4 | Three themes + color contrast | 7 pages × 3 themes | ✅ pass | {"themeOk":true,"contrastFails":[],"themeFails":[]} |
| 5 | Responsive / no horizontal scroll | 8 pages × viewports | ✅ pass | overflow=0 |
| 6 | Lighthouse mobile | 5 key pages | ⚠️ warn | SEO may be low due to noindex (warn, not fail alone); lh-calc.json: a11y 100 / perf 89 / seo 50; lh-csr.json: a11y 100 / perf 72 / seo 54; lh-home.json: a11y 100 / perf 76 / seo 54; lh-news.json: a11y 98 / perf 81 / seo 50; lh-suction.json: a11y 100 / perf 78 / seo 54 |
| 7 | RTL / LTR lang+dir | representative FA + EN + AR pages | ✅ pass | fails=0 |
| 8 | Kalameh font | home/about/news/products | ✅ pass | fails=0 |
| 9 | Calculator formulas | /calculator/ + 5 designs have ABADIS_FORMULAS | ✅ pass | formulas=ok |
| 10 | CSR Zagros scroll | 375 + 1440 | ✅ pass | {"results":[{"vp":{"w":375,"h":812},"s0":{"scrollY":80,"mid":0,"green":0},"s50":{"scrollY":1218,"mid":1,"green":0.028},"s100":{"scrollY":2436,"mid":1,"green":1},"progressed":tru… |
| 11 | Suction-bag 3D viewer | 375 + 1440 + WebGL-off probe | ✅ pass | {"results":[{"vp":{"w":375,"h":812},"hasCanvas":true,"w":375,"h":812,"overflow":false,"glbStatus":200,"ok":true},{"vp":{"w":1440,"h":900},"hasCanvas":true,"w":1440,"h":900,"over… |
| 12 | Theme toggle cycle + persist | home | ✅ pass | {"seq":["dark","noir","light"],"stored":"light","after":"light","rmTheme":"dark","cycleOk":true,"persistOk":true} |
| 13 | Header transparent / scrolled / on-light | home about products news (light) | ✅ pass | fails=0 |
| 14 | Forms contact + careers | /contact/ /careers/ | ✅ pass | {"hasLead":true,"endpointEmpty":true,"contactEmptyBlocked":true,"contactMailto":null,"contactStatus":"برنامهٔ ایمیل شما باز شد؛ پیام بعد از ارسال از همان‌جا به دست ما می‌رسد.","… |
| 15 | Brand rules | nav order, footer certs, yellow CSS, pointermove | ✅ pass | yellow=0; pointermove=0 |
| 16 | Meta title/description/h1/alt | 403 pages | ⚠️ warn | dupTitles=0; missingAltPages=0 |

## Bugs (do not fix in this prompt)

_None recorded._

## Lighthouse (mobile)

| Page | Perf | a11y | Best practices | SEO |
|------|------|------|----------------|-----|
| http://127.0.0.1:8080/calculator/ | 89 | 100 | 100 | 50 |
| http://127.0.0.1:8080/csr/ | 72 | 100 | 100 | 54 |
| http://127.0.0.1:8080/ | 76 | 100 | 100 | 54 |
| http://127.0.0.1:8080/news/ | 81 | 98 | 100 | 50 |
| http://127.0.0.1:8080/products/suction-bag/ | 78 | 100 | 96 | 54 |

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
