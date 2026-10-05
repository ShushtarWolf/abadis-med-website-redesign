# Abadis Med — Management Handoff

**Date:** 2026-09-26  
**Purpose:** Short pack for management — paths + status only. Full detail lives in the Master Spec.

---

## Three deliverables

| # | Deliverable | Path |
|---|---|---|
| 1 | Updated Master Specification (authority) | `docs/abadis/ABADIS-MASTER-SPECIFICATION.md` |
| 2 | Phase 1 execution plan (stages, costs, timeline rules) | `docs/abadis/PHASE-1-EXECUTION-PLAN.md` |
| 3 | Management-facing audit summary | `docs/abadis/ABADIS-AUDIT-SUMMARY-MGMT.md` |

Related: Boss sheets `docs/abadis/BOSS-DECISION-SHEET-FA.md`, WhatsApp FA/EN; evidence `docs/abadis/ABADIS-AUDIT.json`.

---

## Completed

- Live-site discovery pass (Manus, 21 Sep) and n8n evidence pack (25 Sep): **718** URLs inventoried; WP REST totals; media sitemap **1053** `image:loc`; **10**-page HTML sample; **0** broken-link checks in final run  
- Architecture/spec/decision sheets authored; management responses recorded into Master Spec §2.5  
- Phase 1 vs Phase 2 boundary and base extras exclusions documented  
- Calendar discovery window so far: **~5–6 days** (21–26 Sep) — not billable person-days  

## Management has now decided (high level)

- Phase 1 **now**; Phase 2 PayamGostar **portal** = **separate contract**  
- Headless WordPress lean accepted; **Liara first to examine** (final host after cost/location/backup/recovery/access)  
- Abadis owns domain/hosting/GitHub/accounts; RBAC; staging approval before prod  
- Design sequence; **`concept-preview/` not approved**  
- Preserve URL/SEO/media; FA/EN/AR; Abadis approves content/products  
- Store leads **before** notify; PayamGostar write only if API/access/cost/workload approved  
- Chatbot / Experiences / anniversary / 3D viewer **out of base Phase 1** unless separately approved  
- Launch/rollback/backup/restore; **60-day** bug-fix; analytics + monitoring principles  
- First visible: **structure/content model → homepage + product designs**  
- Development fee **$0**; Liara floor **4M tomans/mo**; Cursor Pro+ **$60/mo (verify)**; n8n = existing config (plan price unknown)

## Still open (blocks full implementation)

Final host plan after Liara review; approved visual system; content matrix; product list/fields; About timeline; apex vs `www`; sales owner/SLA/channel; formulas for calculator/impact if in scope; analytics tool; numeric perf budgets; monitoring owner; optional PayamGostar lead-API yes/no.

## Can proceed without waiting for everything

- Draft **page structure + content model** (using inventory + brief priorities) and send for Abadis review  
- Clarify OPEN questionnaire for products/matrix/sales/host  

## Still blocks production Nuxt implementation

- Approved designs (not concept-preview)  
- Content/product freeze inputs  
- Final host after review  
- Lead notify ownership/channel  

**Status:** **Not READY FOR IMPLEMENTATION** of production Nuxt.

## First visible deliverable

1. Page structure and content model  
2. Homepage + product-page designs for approval  

**Dependency:** Reliable design dates need Abadis product list, content matrix, and brand/design direction. Structure draft can start from existing inventory before all OPEN items close.

## Provisional next sequence

1. Abadis returns remaining OPEN inputs (esp. products, matrix, sales channel, Liara plan choice)  
2. Team delivers structure/content model → Abadis approve  
3. Homepage + product designs → Abadis approve  
4. Only then: foundation (host/staging) → migration → build → harden → launch → 60-day warranty  

No project completion date is claimed.
