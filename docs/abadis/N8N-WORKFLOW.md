# n8n — Abadis Website Audit Workflow

## Live workflows

### v2 (current — 9 must-adds)

- **Name:** Abadis Website Audit v2
- **ID:** `jHEbjGnYNWKyI1pb`
- **URL:** https://hamidafghah.app.n8n.cloud/workflow/jHEbjGnYNWKyI1pb
- **Active:** No (manual only)
- **Source assembler:** `docs/abadis/n8n/assemble_workflow.py` + `docs/abadis/n8n/snippets/`
- **Assembled SDK file:** `docs/abadis/n8n/abadis-audit-v2.workflow.js`

### v1 (smoke predecessor)

- **Name:** Abadis Website Audit
- **ID:** `0Qb2DIQWgXuzCVAT`
- **URL:** https://hamidafghah.app.n8n.cloud/workflow/0Qb2DIQWgXuzCVAT

## Controlled smoke test — v2 execution 16 (2026-09-25) — inventory → merge → master plan

Pipeline executed:

```
718+ URLs
   ↓
complete inventories (sitemap + EN/AR + WP X-WP-Total + media)
   ↓
merge
   ↓
ONE complete evidence dataset (ABADIS-AUDIT.json)
   ↓
AI Draft → AI QA → AI Final
   ↓
MASTER MIGRATION PLAN
```

- **executionId:** `16` (~168s)
- **URL inventory complete:** 718 (`complete: true`)
- **EN/AR discoveries:** +177
- **WP REST totals complete:** post 221, page 26, attachment 1727, `_downloadcenter` 9, …
- **HTML page audits:** SAMPLE 10 (labeled `complete: false` under 180s cap)
- **Artifacts:** `docs/abadis/ABADIS-AUDIT.json`, `docs/abadis/MASTER-MIGRATION-PLAN.md`

## Purpose

Reusable workflow that discovers Abadis structure from sitemap + WordPress REST (no hardcoded URL lists), crawls a configurable URL subset/full set, normalizes evidence, runs AI plan → QA → final with explicit labeling, and exports JSON/CSV payloads.

## Safety

- Does **not** modify the live website.
- Does **not** call WP admin/private management endpoints for writes.
- Starts **inactive**; run manually.
- Use `maxCrawlUrls` for smoke tests before full audits.
- Throttle Wait nodes exist but may be disconnected/disabled under the 180s instance cap; HTTP `requestInterval` still applies on WP pagination.

## Configuration fields (Load Config)

| Field | Smoke default | Meaning |
|---|---|---|
| `baseUrl` | `https://abadis-med.com` | Site origin |
| `maxCrawlUrls` | `12` | Crawl cap (`0` = all inventory — **do not run yet** without raising timeout headroom) |
| `requestDelayMs` | `400`–`800` | Intended delay between fetches |
| `userAgent` | `AbadisAuditBot/1.0 (+migration-audit)` | UA string |
| `runAi` | `true` | Enable AI plan stages (n8n Gateway OpenAI) |
| `includeLanguageRoots` | `true` | Always include `/`, `/en/`, `/arabic/` |
| `wpPerPage` | `50` | WP REST `per_page` |
| `wpMaxPagesPerEndpoint` | `1` (smoke) / raise for full | Max pages fetched per REST endpoint |
| `maxBrokenLinkChecks` | `0` (smoke) / `20`+ | Cap HEAD checks for internal links |

## Credentials

- **Public WordPress data:** none required.
- **AI stages:** OpenAI via n8n Gateway credits (`gpt-4o-mini`). Credential ID may appear null in JSON; Gateway injects at runtime.

## v2 stages (must-adds)

1. Clear audit static state every run  
2. robots.txt + sitemap index + child sitemaps → URL inventory + sitemap images  
3. WP root / types / taxonomies → paginated public endpoints capturing `X-WP-Total` / `X-WP-TotalPages`  
4. Deep EN/AR discovery from `/en/` and `/arabic/` same-host links (not sitemap-only)  
5. Build crawl list prioritizing language roots, forms, products, downloads  
6. Per-page redirect hop walk + HTML analyze (title/meta/H1–H3/OG/Twitter/canonical/robots/hreflang/links/forms/mailto/tel/WhatsApp/docs/images/JSON-LD/headers)  
7. Batched internal broken-link HEAD checks (when `maxBrokenLinkChecks` > 0)  
8. Orphan + relationship analysis (INFERENCE labeled)  
9. Normalize evidence → AI Draft → QA → Final (FACT/INFERENCE/RECOMMENDATION/UNKNOWN)  
10. Pack exports: URL-INVENTORY, PAGE-AUDIT, MEDIA, LINKS, FORMS, SCHEMA, WP-CONTENT, TECHNOLOGY, ORPHANS, RELATIONSHIPS, ABADIS-AUDIT.json, MASTER-PLAN.json  

## How to run

1. Open v2 workflow (inactive).  
2. Confirm smoke caps under 180s, or raise `wpMaxPagesPerEndpoint` / `maxBrokenLinkChecks` / `maxCrawlUrls` only if the instance timeout allows.  
3. Execute manually.  
4. Download binary exports from Pack/Convert nodes.  
5. Do **not** set `maxCrawlUrls = 0` until timeout/throttling headroom is confirmed.

## Known gaps after smoke

- Instance `executionTimeout` max **180s** forces smoke tradeoffs (link checks off, WP pages capped, AI maxTokens lowered, some Wait/Fetch nodes disconnected).  
- Broken-link checker implemented but disabled (`maxBrokenLinkChecks=0`) in last successful smoke.  
- Full ~542+ URL audit not run (by request).  
- concept-preview remains REJECTED CONCEPT — VISUAL REFERENCE ONLY.
