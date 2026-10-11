# Abadis redesign — complete work report

- **Branch:** `siamak/redesign` @ `758bd4c`
- **PR:** https://github.com/ShushtarWolf/abadis-med-website-redesign/pull/3
- **Date:** 2026-10-07
- **Preview (temporary tunnel):** https://session-assumption-overhead-vegetation.trycloudflare.com/
- **GitHub Pages (main only today):** https://shushtarwolf.github.io/abadis-med-website-redesign/

---

## 1. Scope & rules

| Rule | Status |
|------|--------|
| Work only on `siamak/redesign` | Done — no push to `main`, no force-push |
| Merge others’ commits; do not rewrite | Done — merged `origin/main` + team-assets |
| Static `site/` + generator `tools/redesign/` | Done |
| Standing rules `.cursor/rules/abadis.mdc` + prompt pack | Done |
| All pages `noindex,nofollow` (preview) | Kept |

---

## 2. Site surface (what ships in `site/`)

| Area | Delivered |
|------|-----------|
| **Home** | Phase-1 shell; theme toggle (light/dark/noir); transparent header; brand teals / Kalameh |
| **Products** | Hub + 7 families (suction bag with 3D viewer, filters, canister, stand, connectors, suction tube, other) |
| **About** | Mission/vision, history, team, partners, ISO; team member videos (Alireza, Navid) |
| **Dealers** | 29 cards / 26 provinces — reconciled with WP `_franchise` (26 CPT) + live listing |
| **Customers** | 155 medical centres (search + paging); matches WP `_customers` |
| **Calculator** | Redesign draft in site shell; formulas unchanged; dial design switcher → main dial pages |
| **CSR / Zagros** | Scroll hero (dry → sprouting → green) + CSR activities / SDG |
| **Contact** | Hours / holidays / extensions; form → configurable endpoint + mailto fallback |
| **Careers** | Openings + application form + job pages |
| **News / articles** | Lists + singles from WP REST (real categories); unique document titles |
| **Footer pages** | Experiences, downloads (9 catalogues), install guide, FAQ |
| **EN** | `/en/` — language switcher + hreflang; internal paths (no live abadis-med.com leaks) |
| **AR** | `/arabic/` — same i18n treatment |
| **Footer certs** | Live strip only: CE · ISO 13485:2016 · IMED |
| **Dial pages (from main)** | Merged `dial-*` / `template-dials`; linked from `/calculator/` switcher |

**Approximate page counts (HTML `index.html`):** FA ~260 · EN ~106 · AR ~45 · news/articles directories under `site/news/` & `site/articles/`.

---

## 3. Work completed by phase

### Phase 1 — shell
- Header/footer refresh (transparent header, zone ink, full nav, compact theme toggle with View Transitions)
- Sticky product anchors under compact mobile header
- Certificate policy → footer strip only (CE / ISO / IMED)

### Phase 2 — content & generator
- Static generator `tools/redesign/` (products, company pages, posts, i18n, layout)
- Products hub + 6 additional product family pages (suction bag already strong)
- About, dealers, calculator, CSR/SDG, contact
- Customers, experiences, downloads, install guide, FAQ, careers
- News + articles lists and single posts from crawl/REST
- Image recovery (thumbnails, customer logos, team, SDG, ISO) from live uploads / Wayback + WebP
- Zagros CSR scroll hero and calculator redesign draft embedded in site shell
- Team videos on about

### i18n & forms
- English `/en/`, Arabic `/arabic/`, language switcher, hreflang
- Rewrite EN/AR hrefs that pointed at live `abadis-med.com` → internal paths
- Forms: configurable POST endpoint + mailto fallback; careers form completed
- Contact light-theme contrast fix; sanitize bogus EN hrefs

### Data accuracy
- Dealers: Wayback 24 → **29 cards** aligned with CPT + live (see `DEALERS-RECONCILIATION.md`)
- Customers: **155** confirmed across site / Wayback / REST
- Meta descriptions + image alts filled; branded fallback thumbs for articles missing images
- Unique titles for news/articles vs same-named pages

### Main merge & dials
- Merged `origin/main` (dial design pages) into redesign
- Calculator switcher links to main dial design pages under `site/`

### Assets / local only
- `staff-photos/` — local originals download (gitignored); ~19–21 of 23 recovered; letter-avatars still missing for a few
- Prompt pack FA: `docs/cursor/CURSOR-PROMPTS-FA.md`

### QA
- Full-site Playwright + Lighthouse + linkinator suite (`tools/test/`)
- Latest committed report: `docs/abadis/TEST-REPORT.md` (SHA `ae3ea53`)
  - **14 pass · 0 fail · 2 warn** (SEO low due to intentional `noindex`; meta warn)
  - 0 broken internal links (1658 checked); 0 console errors; themes/RTL/Kalameh/calculator/CSR/3D OK

### Preview / CI
- Attempted GitHub Pages deploy from `siamak/redesign` (`pages.yml` includes branch)
- **Blocked:** `github-pages` environment deployment-branch policy allows **only `main`** (token cannot change policy)
- Temporary public preview via Cloudflare tunnel (see top)

---

## 4. Test summary (prompt 7)

| # | Test | Result |
|---|------|--------|
| 1 | Internal links | ✅ |
| 2 | 404 / broken assets | ✅ |
| 3 | Console errors | ✅ |
| 4 | Themes + contrast | ✅ |
| 5 | Responsive / no H-scroll | ✅ |
| 6 | Lighthouse mobile | ⚠️ (SEO ~50–54 from noindex) |
| 7 | RTL / LTR | ✅ |
| 8 | Kalameh | ✅ |
| 9 | Calculator formulas | ✅ |
| 10 | CSR Zagros scroll | ✅ |
| 11 | Suction-bag 3D | ✅ |
| 12 | Theme toggle persist | ✅ |
| 13 | Header transparency | ✅ |
| 14 | Contact + careers forms | ✅ |
| 15 | Brand rules | ✅ |
| 16 | Meta / alt | ⚠️ |

Lighthouse a11y on key pages: **98–100**. Perf roughly **72–89**.

---

## 5. Open / blocked

| Item | Notes |
|------|--------|
| **Durable github.io for redesign** | Add `siamak/redesign` under Settings → Environments → github-pages → Deployment branches |
| **کردستان dealer contacts** | CPT row exists; public fields empty — do not invent |
| **چهارمحال CPT city link** | On live listing; no dedicated `_citynmg` — confirm with Abadis |
| **Staff letter-avatars** | A few team photos still missing from recovery |
| **Forms backend** | Endpoint empty → mailto fallback (see `FORMS-BACKEND.md`) |
| **SEO scores** | Intentionally low while `noindex` remains for preview |
| **Merge to main** | Human decision via PR #3 — agent does not merge |

---

## 6. Key paths

| Path | Role |
|------|------|
| `site/` | Static site output |
| `tools/redesign/` | Generator (`build.py`, `layout.py`, `pages_*.py`, `i18n.py`, …) |
| `tools/redesign/data/` | dealers, franchise, posts, imgmap, i18n data |
| `tools/test/` | Playwright / Lighthouse / linkinator |
| `docs/abadis/TEST-REPORT.md` | Latest automated QA |
| `docs/abadis/DEALERS-RECONCILIATION.md` | Dealers/customers decisions |
| `.cursor/rules/abadis.mdc` | Standing agent rules |
| `docs/cursor/CURSOR-PROMPTS-FA.md` | Prompt pack (FA) |

---

## 7. How to review

1. Open preview: https://session-assumption-overhead-vegetation.trycloudflare.com/
2. Spot-check: home (3 themes) → products/suction-bag → dealers → calculator dials → CSR scroll → `/en/` + `/arabic/` → contact form
3. PR discussion: https://github.com/ShushtarWolf/abadis-med-website-redesign/pull/3

---

*Generated for stakeholders — branch `siamak/redesign`, 2026-10-07.*
