# Abadis Med — Technology & Plugin Audit

**Generated:** 2026-09-25  
**Evidence sources:** homepage HTML (fa/en/ar), `wp-json/` namespaces & types, Yoast sitemaps, REST samples  
**Rule:** FACT / INFERENCE / RECOMMENDATION / UNKNOWN-HUMAN-REVIEW

---

## Stack snapshot

| Layer | Observation | Class |
|---|---|---|
| CMS | WordPress (REST `wp/v2`, `link: api.w.org` on homepage) | FACT |
| SEO | Yoast SEO (`wordpress-seo` sitemap XSL, robots “YOAST BLOCK”, `yoast_head_json` on REST) | FACT |
| Page builder | Elementor + Elementor Pro (`elementor/v1`, `elementor-pro/v1`; page `template=elementor_header_footer`) | FACT |
| Dynamic data / CPTs | JetEngine (`jet-engine/v2`; CPTs `_customers`, `_franchise`, `_downloadcenter`, `_joboffers`) | FACT |
| Menus | JetMenu (`jet-menu-api/v2`, `jet-menu` type, `jet-menu-sitemap.xml`) | FACT |
| UI kit | UIkit class patterns (`uk-*`) on sampled HTML | FACT |
| Element Pack / BDThemes | `bdt-*` class patterns on sampled HTML | FACT |
| Reviews API | `jet-reviews-api/v1` namespace present | FACT |
| Multilingual | Live `/en/` and `/arabic/` roots; **no** `/en/` or `/arabic/` locs in Yoast child sitemaps; Arabic `html lang="fa-IR"` | FACT |
| Forms | No `<form>` on sampled homepages; Elementor form / CF7 markers not confirmed on those pages | FACT (homepages only) |
| WhatsApp | WhatsApp links/widgets present on sampled homepages | FACT |
| Analytics | GTM/GA/Clarity **not** detected in sampled homepage HTML | FACT (samples only) — UNKNOWN whether loaded via tag manager after paint |
| ACF | `acf: []` on sampled CPT REST items | FACT (public REST) — UNKNOWN private field storage |

---

## Per-technology decisions

### WordPress core
1. **Does:** CMS, media library, users, REST.  
2. **Depends:** Entire site.  
3. **Required after migration:** Yes (headless CMS).  
4. **Remain in WP:** Content editing, media, CPT data.  
5. **Replace in Nuxt:** Rendering, routing, SEO tags, menus presentation.  
6. **Alt plugin:** No.  
7. **Manual verify:** Admin plugins list, private REST fields, Application Passwords / auth for non-public data.

### Elementor (+ Pro)
1. **Does:** Layout/content composition; header/footer template.  
2. **Depends:** Most pages (sampled page uses Elementor template; HTML heavily Elementor-marked).  
3. **Required after migration:** No for frontend.  
4. **Remain in WP:** Optionally during transition for editors; long-term content should move to structured fields.  
5. **Replace in Nuxt:** Page sections/components.  
6. **Alt plugin:** Not required if content is modeled.  
7. **Manual verify:** Which content lives only inside Elementor JSON vs post_content vs JetEngine fields.

### JetEngine
1. **Does:** Custom post types/taxonomies/meta.  
2. **Depends:** Customers, franchise/reps, download center, job offers, city taxonomy.  
3. **Required after migration:** Yes until data remodeled — or keep as WP CPT backend.  
4. **Remain in WP:** CPT storage is fine for headless.  
5. **Replace in Nuxt:** Listing/detail templates.  
6. **Alt plugin:** Could later use native WP CPTs + ACF; not mandatory for launch.  
7. **Manual verify:** Meta field schema (not exposed publicly in samples).

### JetMenu
1. **Does:** Mega/advanced menus.  
2. **Depends:** Primary navigation.  
3. **Required after migration:** No.  
4. **Remain in WP:** Optional source of menu JSON if REST exposes it.  
5. **Replace in Nuxt:** Explicit nav config or WP menus API.  
6. **Alt plugin:** Core WP menus sufficient.  
7. **Manual verify:** Full menu tree + mobile behavior.

### Yoast SEO
1. **Does:** Titles, robots, sitemaps, `yoast_head_json`.  
2. **Depends:** SEO metadata sitewide (weaker on Arabic sample).  
3. **Required after migration:** Metadata must be preserved/reimplemented in Nuxt; Yoast can remain as CMS metadata source via REST.  
4. **Remain in WP:** Useful as editorial SEO fields.  
5. **Replace in Nuxt:** Final `<title>`, meta, canonical, hreflang, sitemap generation for the public site.  
6. **Alt plugin:** Rank Math etc. unnecessary if Nuxt owns public SEO.  
7. **Manual verify:** Why EN/AR are missing from sitemaps; Arabic robots/schema gaps.

### UIkit + BDThemes Element Pack + Dynamic Content for Elementor
1. **Does:** Frontend widgets/styling (class-level evidence).  
2. **Depends:** Current WP theme presentation.  
3. **Required after migration:** No.  
4. **Remain in WP:** No for headless front.  
5. **Replace in Nuxt:** Tailwind + Nuxt UI primitives.  
6. **Alt plugin:** None.  
7. **Manual verify:** Any widget-only content without HTML fallback.

### Jet Reviews
1. **Does:** Reviews API namespace present.  
2. **Depends:** UNKNOWN which pages.  
3. **Required:** UNKNOWN.  
7. **Manual verify:** Whether reviews are public/business-critical.

---

## Multilingual technology gap

| Finding | Class |
|---|---|
| Persian root `/` is primary | FACT |
| English `/en/` returns 200 (via 301 from non-www sample path observed) | FACT |
| Arabic `/arabic/` returns 200 | FACT |
| Yoast child sitemaps in this audit contain **0** `/en/` or `/arabic/` URLs | FACT |
| Arabic homepage `lang="fa-IR"` and minimal/no Yoast robots/schema | FACT |
| No `hreflang` on sampled fa/en/ar homepages | FACT |
| Plugin implementing multilingual (WPML/Polylang/TranslatePress/custom) | UNKNOWN — not determinable from public namespaces alone |

**RECOMMENDATION:** Treat multilingual as a first-class migration workstream. Do not change URL roots (`/`, `/en/`, `/arabic/`) without an evidence-backed redirect matrix.
