# Abadis Med — Management Audit Summary

**Source evidence only:** `docs/abadis/ABADIS-AUDIT.json` (generated `2026-09-25T15:24:58.690Z`)  
**Domain:** `https://abadis-med.com`  
**Audience:** Management  
**Note:** This is **not** a claim that all 718 URLs were individually HTML-crawled or that broken links were fully tested.

---

## 1. Headline figures (FACT)

| Inventory | Complete? | Count / note |
|---|---|---|
| URL inventory | **Yes** | **718** URLs (union of sitemaps + language roots + EN/AR link discovery) |
| Language mix in URL inventory | Yes | fa **540**, en **101**, ar **77** |
| EN/AR deep discovery adds | Yes | **+177** URLs from `/en/` and `/arabic/` HTML (not sitemap-only) |
| Media sitemap `image:loc` | Yes | **1053** image locations from child sitemaps |
| WordPress REST totals (`X-WP-Total`) | Yes | See §3 |
| WP REST items downloaded this run | **No** | **309** items (capped) — totals above are the complete counts |
| HTML / SEO page audits | **No** | **10** pages only (`maxCrawlUrls=10`) |
| Forms observed | **No** | **6** on the crawled HTML sample |
| Broken-link HEAD checks | **No** | **0** this run |

**Explicit limitation:** This was **not** a full 718-page HTML crawl and **not** a complete broken-link audit.

---

## 2. URL inventory breakdown (from `urlInventory` content_type)

These are inventory classifications in the audit JSON — **not** proof each URL’s HTML was fetched:

| Type / bucket | Count |
|---|---:|
| post | 208 |
| page | 25 |
| language_root | 3 |
| `_customers` | 156 |
| `_franchise` | 27 |
| `_citynmg` | 25 |
| post_tag | 63 |
| category | 8 |
| `_joboffers` | 10 |
| `_downloadcenter` | 10 |
| jet-menu | 3 |
| author | 4 |
| lang_discovered | 176 |
| **Total** | **718** |

**Images / files:** Media sitemap reports **1053** `image:loc` entries. WordPress REST reports **1727** attachments (type total). These are **counts**, not a verified binary integrity or “all files migrated” claim.

---

## 3. WordPress REST inventory (FACT — headers)

| Key | total | kind |
|---|---:|---|
| post | 221 | type |
| page | 26 | type |
| attachment | 1727 | type |
| `_customers` | 155 | type |
| `_franchise` | 26 | type |
| `_downloadcenter` | 9 | type |
| `_joboffers` | 9 | type |
| category | 8 | taxonomy |
| post_tag | 76 | taxonomy |
| `_citynmg` | 31 | taxonomy |

Namespaces observed include `yoast/v1`, `elementor/v1`, `elementor-pro/v1`, `jet-engine/v2`, `jet-menu-api/v2`, `wp/v2`.  
**No** dedicated public REST type named `product` appeared in the audited types list (product content may live as pages/Elementor compositions).

---

## 4. Limited 10-page HTML / SEO sample (FACT)

Pages sampled include home FA, `/en/`, `/arabic/`, selected product/guide/calculator/contact/news-like URLs.

Notable sample findings:

- Home FA: missing H1; many images missing alt  
- EN root: redirect hops; canonical on `www`; empty hreflang on sample  
- Arabic root: **`html lang=fa-IR`** (incorrect); weak SEO signals vs FA/EN samples  
- Forms present (Gravity Forms / Elementor-style field names on samples)

These defects are **sample evidence**, not a site-wide census.

---

## 5. Broken links

Broken-link checking was **implemented but not completed** in the final successful audit execution (`link_checks.count = 0`, `complete: false`).  
**Do not** claim the site’s links were fully validated.

---

## 6. Other documented limitations

- Instance execution timeout (~180s) forced smoke tradeoffs  
- WP item download capped vs full totals  
- Orphan/relationship analysis labeled INFERENCE where present  
- No GLB/Three.js matches in the live HTML audit payload  
- `concept-preview/` is rejected visual reference only — not live-site evidence  

Full technical detail: `ABADIS-MASTER-SPECIFICATION.md` §2 and `N8N-WORKFLOW.md`.
