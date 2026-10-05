# Abadis Med — Migration Audit System

**Status:** Evidence collection + audit workflow in progress  
**Live site:** https://abadis-med.com/  
**Audit date (this pass):** 2026-09-25  
**Classification rule:** Every major conclusion must be marked **FACT**, **INFERENCE**, **RECOMMENDATION**, or **UNKNOWN / HUMAN REVIEW**.

---

## Project assessment (local Cursor repo)

### What already exists

| Asset | Role |
|---|---|
| `concept-preview/` | Static Nuxt-rendered suction-bag product concept (Vercel/Netlify artifact) |
| `concept-preview/محصولات/کیسه-ساکشن/` | Rejected concept page HTML |
| `concept-preview/models/*.glb` | Experimental 3D GLB assets (including oversized source exports) |
| `concept-preview/brand/` | Kalameh fonts + product PNG |
| `audit-raw/` | Prior sitemap downloads + fresh `live/` evidence |
| `ABADIS_AUDIT_AND_MIGRATION_PLAN.md` | Earlier Manus plan (useful context; not the final evidence pack) |
| `docs/persian-typography.md` | Persian typography rules for future Nuxt UI |
| Design brief `.docx`, logo `.ai`, CATPart | Brand/product source material |

### REJECTED CONCEPT — VISUAL REFERENCE ONLY

`concept-preview/` was shown to the client/boss and **was not approved**.

- Keep it in the repository.
- Do **not** treat its visual language as the approved Abadis design direction.
- Technically reusable pieces (Kalameh loading, GLB pipeline experiments, Nuxt static export patterns) may be reused later.
- Visual composition, teal palette, motion choreography, and copy in that page are **rejected design**, not requirements.

### Technologies present locally

- Static Nuxt build output (`_nuxt/`), not a full Nuxt 4 app source tree
- Three.js / GLB usage inside the concept page bundle
- No production WordPress theme/plugin source in this repo
- No live CMS connection from this repo today

---

## Audit outputs in this folder

| File | Purpose |
|---|---|
| `ABADIS-MIGRATION-MASTER-PLAN.md` | Full migration specification |
| `URL-MIGRATION-MAP.csv` | URL → action matrix |
| `CONTENT-MIGRATION-MAP.csv` | Content-type / CPT mapping |
| `MEDIA-INVENTORY.csv` | Media & document inventory (seeded from evidence; expandable) |
| `SEO-AUDIT.csv` | Page-level SEO observations |
| `TECHNOLOGY-PLUGIN-AUDIT.md` | Plugin/tech dependency analysis |
| `ARCHITECTURE.md` | Target Nuxt 4 + Headless WP + Liara + n8n |
| `MIGRATION-RISKS.md` | Risks with classification |
| `HUMAN-REVIEW-REQUIRED.md` | Explicit human checkpoints |
| `ABADIS-AUDIT.json` | Machine-readable evidence pack |
| `N8N-WORKFLOW.md` | How to run/re-run the n8n audit workflow |

---

## Live n8n workflow

- **Abadis Website Audit** — https://hamidafghah.app.n8n.cloud/workflow/0Qb2DIQWgXuzCVAT
- Status: **inactive** (manual runs only)
- Smoke-tested with `maxCrawlUrls=5` (execution 3 succeeded after crawl-wiring fix)

## What the n8n workflow automates

1. Load project configuration (`baseUrl`, `maxCrawlUrls`, AI on/off)
2. Discover `robots.txt`, sitemap index, child sitemaps (dynamic — not hardcoded)
3. Discover WordPress REST root, types, taxonomies
4. Build URL inventory
5. Crawl a configurable subset (test) or full inventory (production audit)
6. Extract HTTP/SEO/content/link/media signals from HTML
7. Normalize evidence JSON
8. AI draft plan → AI QA → AI final plan (via n8n Gateway OpenAI credits when available)
9. Export structured report payloads

## What still requires human verification

- Search Console indexation / traffic
- Legal claims, certifications, medical statements
- Form destinations / CRM wiring (not fully visible via public HTML)
- Whether customer/franchise archives should remain indexable
- Final visual design direction (rejected concept is not approved)
- Exact multilingual plugin strategy (EN/AR pages exist but are **absent from Yoast sitemaps** — FACT from 2026-09-25 crawl)

## Safety rules

- Do not modify the live Abadis website from this audit.
- Do not activate production redirects from this workflow.
- Do not delete `concept-preview/`.
- Do not invent URLs or business requirements.
