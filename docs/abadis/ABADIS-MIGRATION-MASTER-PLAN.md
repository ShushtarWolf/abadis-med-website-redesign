# Abadis Med — Migration Master Plan

**Domain:** https://abadis-med.com/  
**Target:** Nuxt 4 + Headless WordPress + Tailwind/Nuxt UI + Three.js/GLB + Liara + n8n  
**This document classifies statements as FACT / INFERENCE / RECOMMENDATION / UNKNOWN-HUMAN-REVIEW.**  
**Rejected local concept:** `concept-preview/` = **REJECTED CONCEPT — VISUAL REFERENCE ONLY** (do not treat as approved design).

---

## 0. Executive verdict

**FACT:** The live site is a substantial WordPress property with Yoast sitemaps (~539 URL records across 11 child sitemaps), Elementor rendering, JetEngine CPTs (customers, franchise, downloads, jobs), and live Persian/English/Arabic entry points.

**RECOMMENDATION:** Migrate by modernizing the frontend (Nuxt 4) while preserving URLs, media paths, content meaning, and business workflows. Do **not** clean-slate replace indexed content.

**FACT:** A prior concept page exists in-repo and was not approved. Keep it only as technical/visual reference.

---

## 1. Local project assessment

| Item | Finding | Class |
|---|---|---|
| Framework in repo | Static Nuxt build in `concept-preview/` (not full Nuxt 4 source app) | FACT |
| 3D | Multiple GLBs including web-sized and very large source exports | FACT |
| Fonts | Kalameh woff2 under `concept-preview/brand/fonts` | FACT |
| Prior audit | `ABADIS_AUDIT_AND_MIGRATION_PLAN.md`, `audit-raw/`, scripts | FACT |
| Approved UI | None in this repo | FACT |

**Technically reusable later:** font loading, GLB compression workflow, Persian typography doc, audit scripts.  
**Not reusable as requirements:** concept page layout, motion, palette-as-final-brand, copy.

---

## 2. Discovery evidence (live)

### robots.txt (FACT)
Yoast block; `User-agent: *` / `Disallow:` empty; Sitemap `https://abadis-med.com/sitemap_index.xml`.

### Sitemap index children (FACT)
`post`, `page`, `jet-menu`, `_joboffers`, `_downloadcenter`, `_customers`, `_franchise`, `category`, `post_tag`, `_citynmg`, `author`.

### Approximate URL counts from local sitemap copies (FACT)
| Sitemap | locs |
|---|---:|
| post | 207 |
| _customers | 156 |
| post_tag | 63 |
| _franchise | 27 |
| page | 26 |
| _citynmg | 25 |
| _downloadcenter | 10 |
| _joboffers | 10 |
| category | 8 |
| author | 4 |
| jet-menu | 3 |

### Critical multilingual sitemap gap (FACT)
Child sitemaps inspected in this audit contain **no** `/en/` or `/arabic/` `<loc>` entries, yet both language roots respond live. EN/AR discovery for crawlers is incomplete relative to Persian.

### WordPress REST (FACT)
Namespaces include: `yoast/v1`, `elementor/v1`, `elementor-pro/v1`, `jet-engine/v2`, `jet-menu-api/v2`, `jet-reviews-api/v1`, `wp/v2`.

**Totals from `X-WP-Total` headers (FACT, 2026-09-25 samples):** pages 26, posts 221, media 1727, `_customers` 155, `_franchise` 26, `_downloadcenter` 9, `_joboffers` 9, `_citynmg` 31, categories 8, tags 76.

---

## 3. Page-level observations (sampled)

| URL | Title | lang | H1 | hreflang | Schema | Notes | Class |
|---|---|---|---|---|---|---|---|
| `/` | صفحه اصلی » مخازن طبی آبادیس | fa-IR | none found | none | WebPage, ImageObject, BreadcrumbList, WebSite | many imgs missing alt | FACT |
| `/en/` | Home \| Abadis Med | en-US | none found | none | WebSite, ImageObject, WebPage, BreadcrumbList | canonical on www host | FACT |
| `/arabic/` | مخزن طبی ابادیس | **fa-IR** | none found | none | none observed | robots only `max-image-preview:large` | FACT |

**INFERENCE:** Arabic template SEO is materially weaker than FA/EN.

---

## 4. Content model (CURRENT → TARGET)

| Current | Storage (observed) | Target WP model | Nuxt surface | Class |
|---|---|---|---|---|
| Pages | WP `page` + Elementor template | `page` + structured sections fields (**proposed**) | `[...slug]` / locale layouts | FACT + RECOMMENDATION |
| Posts | WP `post` + categories/tags | `post` | `/مقالات`, news routes | FACT + RECOMMENDATION |
| Products | Currently **pages** under `/محصولات/...` (and EN nav paths) | **Proposed** CPT `product` + tax `product_category` OR keep pages with product meta | Product template + optional 3D | INFERENCE + RECOMMENDATION |
| Downloads | `_downloadcenter` | keep CPT + file URL fields | Download center | FACT + RECOMMENDATION |
| Jobs | `_joboffers` | keep CPT | Careers | FACT + RECOMMENDATION |
| Customers | `_customers` | keep CPT | Customers (indexability TBD) | FACT + HUMAN REVIEW |
| Franchise | `_franchise` + `_citynmg` | keep + city taxonomy | Representatives | FACT + RECOMMENDATION |
| Media | `attachment` (often noindex) | media library | `<NuxtImg>` / direct upload URLs | FACT |
| Menus | JetMenu | WP menus or JSON config | Nuxt nav components | FACT + RECOMMENDATION |

**Do not invent product SKUs/specs.** Mark all new fields as **proposed** until JetEngine meta is exported.

---

## 5. Product + 3D requirements (RECOMMENDATION)

- Store GLB in object storage or `/public/models/` with WP product field `glb_url` + `poster_image`.
- Nuxt loads Three.js viewer client-only; SSR outputs poster + specs HTML.
- Requirements: correct scale, compressed GLB, mobile budget, `prefers-reduced-motion`, keyboard fallback, no content exclusive to canvas.
- Local note (FACT): `AMR_4894 (1).glb` ~60MB unsuitable for web; prefer web-optimized GLB class (~0.5MB observed for `AMR_4894-web.glb`).

---

## 6. SEO migration rules

1. Default action: **PRESERVE** URL.  
2. Never auto-DELETE. Uncertain → **REVIEW**.  
3. Rebuild templates behind same URLs where possible.  
4. One-to-one 301 only with content equivalence.  
5. Preserve upload/document URLs.  
6. Implement hreflang only for verified pairs.  
7. Fix Arabic language/SEO debt before celebrating parity.  
8. Nuxt must emit sitemap coverage for **all** public locales.

Details: `SEO-AUDIT.csv`, `URL-MIGRATION-MAP.csv`.

---

## 7. Structured data

| Current schema | Migration action | Class |
|---|---|---|
| WebSite | Recreate in Nuxt from site settings | FACT → RECOMMENDATION |
| WebPage | Per-route | FACT → RECOMMENDATION |
| BreadcrumbList | From IA | FACT → RECOMMENDATION |
| ImageObject | Only with real primary image | FACT → RECOMMENDATION |
| Organization / Product / Article | Not observed on sampled homepages | UNKNOWN on other templates — verify, do not invent |

---

## 8. Multilingual plan

**Preserve URL roots:** `/`, `/en/`, `/arabic/`.

**RECOMMENDATION:** Explicit locale from path; no forced IP redirect for crawlers or deep links. Optional soft language suggestion only.

**HUMAN REVIEW:** Map every FA↔EN↔AR pair; document missing translations without silently duplicating content.

---

## 9. Navigation (RECOMMENDATION)

Replace JetMenu mega-menu with Nuxt navigation fed by WP menus or versioned config:

- Primary, footer, language switcher, product taxonomy, mobile drawer, breadcrumbs.
- CTA paths: products, contact, calculator, downloads, representatives.

---

## 10. Forms & business functionality

**FACT:** Homepages show WhatsApp and contact affordances; `<form>` not present on those three samples.  
**UNKNOWN:** Elementor forms on contact/jobs/download pages, CRM, email routing.  
**RECOMMENDATION:** Keep all lead paths working at cutover; prefer Nuxt form → n8n webhook → existing inbox/CRM.

---

## 11. Nuxt 4 architecture (RECOMMENDATION)

- Routes mirror current path structure (Persian slugs included).  
- Layouts: `default`, `product`, `article`, `minimal`.  
- Composables: `useWp()`, `useSeo()`, `useHreflang()`, `useProductGlb()`.  
- Caching: ISR/SWR for CMS pages; strict for products.  
- Error pages: localized 404/500.  
- Accessibility + responsive mandatory; 3D progressive.

Compatible Nuxt 4 patterns only (no Nuxt 2 assumptions).

---

## 12. Performance requirements (RECOMMENDATION)

- CWV budgets on home + product (+ 3D product) mobile.  
- Image optimization, font `font-display: swap`, code-split Three.js.  
- Respect Persian typography guidance in `docs/persian-typography.md`.

---

## 13. Security (RECOMMENDATION)

- Public REST only from browser.  
- Secrets in Liara/n8n credentials.  
- CORS allowlist.  
- Form spam controls.  
- No crawling of WP admin in audit workflow.

---

## 14. Testing matrix (summary)

Content / SEO / functional / visual / performance — see launch section. Full matrix must include **every language root**, every product page, downloads, redirects, hreflang, schema, forms.

---

## 15. Launch stages

1. Audit (this pack + n8n full crawl)  
2. Architecture sign-off  
3. Content model + field export  
4. Nuxt foundation on Liara staging  
5. CMS preparation  
6. Components (after approved design)  
7. Page migration  
8. Product migration (+ optional 3D)  
9. SEO implementation  
10. Testing  
11. Staging  
12. Redirect verification  
13. Production  
14. Monitoring  

**Rollback:** revert edge/DNS to WordPress theme; keep CMS data intact.

---

## 16. AI quality control (n8n)

Workflow stages: evidence normalize → AI draft plan → AI QA (gaps/risks) → AI final plan → export.  
Human remains authority on HUMAN-REVIEW items.

---

## 17. What another agent should do next

1. Run n8n **Abadis Website Audit** with `maxCrawlUrls` raised after smoke test.  
2. Refresh CSVs from workflow output.  
3. Complete EN/AR URL inventory beyond language roots.  
4. Export JetEngine field schema with auth.  
5. Wait for approved design before UI implementation.  
6. Never delete `concept-preview/`.
