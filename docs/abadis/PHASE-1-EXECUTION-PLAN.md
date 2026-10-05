# Abadis Med — Phase 1 Execution Plan

**Audience:** Management + delivery team  
**Authority:** `ABADIS-MASTER-SPECIFICATION.md` (wins on conflicts)  
**Updated:** 2026-09-26  
**Development fee:** **$0**  
**Phase 2 PayamGostar portal:** **Excluded** from Phase 1 cost and delivery (separate contract)

This plan does **not** authorize production Nuxt coding until Master Spec §26B blocking items for the relevant stage are closed.

---

## 1. How to read durations and costs

| Kind | Meaning |
|---|---|
| **Verified (completed)** | Dates from git, audit JSON, file artifacts, or Cursor session timestamps |
| **Session wall-clock** | First→last message window in a Cursor chat — **NOT** active or billable hours |
| **PROVISIONAL estimate** | Forward-looking working-day guess for planning only; depends on Abadis inputs/approvals |
| **Unknown** | Not inventable from evidence (e.g. management approval wait length; exact n8n plan price) |

**Do not** treat any figure below as a project completion date.

---

## 2. Completed discovery / research (verified)

| Stage | Work | Deliverable | Duration | Abadis input/approval | Cost | Dependencies / Risks |
|---|---|---|---|---|---|---|
| D0 — Project start | Initial sitemap harvest + Manus audit/plan + design brief assets | Git commit `15f705a`; `ABADIS_AUDIT_AND_MIGRATION_PLAN.md` (audit date 21 Sep 2026) | **Verified calendar:** started **21 Sep 2026** (git AuthorDate 13:11:22 UTC). Manus session hours: **unknown** (no Cursor transcript) | Brief/logo materials supplied earlier | Dev fee $0 | Early plan is **not** the Master Spec |
| D1 — Concept preview (rejected) | Static suction-bag concept page | `concept-preview/` (git 21 Sep; local polish 23–24 Sep) | Verified commits 21 Sep; Cursor wall-clock windows ~23 Sep evening–24 Sep early morning (**session wall-clock only, not billable hours**) | Shown to management; **rejected** as visual source | Dev fee $0 | Must not drive Phase 1 UI |
| D2 — Local workspace | Clone + continue project in Cursor | Local repo from 23 Sep 2026 | **Verified:** local Cursor Abadis work from **23 Sep 2026** onward | — | Dev fee $0 | Docs largely untracked in git |
| D3 — n8n audit workflow | Build/run Abadis Website Audit v2 | Workflows on `hamidafghah.app.n8n.cloud`; `N8N-WORKFLOW.md` | Cursor chat windows on **25 Sep** (e.g. main audit chat ~16:08–19:24 IRST wall-clock — **not billable hours**). Smoke execution **~168s** verified | — | n8n: existing cloud instance; **plan price unknown** | 180s instance timeout forced sample caps |
| D4 — Evidence pack | Inventories + AI plan synthesis | `ABADIS-AUDIT.json` (`generated_at` **2026-09-25T15:24:58.690Z**); `MASTER-MIGRATION-PLAN.md` | **Verified:** 25 Sep 2026 | — | Dev fee $0 | HTML sample 10 pages; link checks 0 |
| D5 — Spec & decisions | Master Spec, technical decisions register, Boss sheets | `ABADIS-MASTER-SPECIFICATION.md`, `TECHNICAL-REVIEW-DECISIONS.md`, Boss WhatsApp FA/EN | **Verified:** authored **25 Sep 2026** | Management answered Boss sheet (two responses; recorded 26 Sep into Master Spec §2.5) | Dev fee $0 | Spec authority preserved |
| — | **Calendar elapsed so far** | Discovery → decision capture | **Approximately 5–6 calendar days** (21→26 Sep 2026) | — | — | Calendar ≠ person-days; **person-days/active hours not inventable** |

---

## 3. Future Phase 1 work (PROVISIONAL)

Assumes base Phase 1 scope only (no chatbot / Experiences / anniversary / 3D viewer unless separately approved).

| Stage | Work | Deliverable | Duration | Abadis input/approval | Cost | Dependencies / Risks |
|---|---|---|---|---|---|---|
| A0 — Approval wait | Await remaining §26B inputs | Filled OPEN items | **Unknown** — do not invent wait length | Product list, content matrix, About timeline, apex/www, sales owner/SLA/channel, design reference path, Liara plan choice after review | — | Blocks reliable dates for later stages |
| A1 — Page structure & content model | IA + content types/fields/relations/SEO fields; FA/EN/AR coverage map | **First visible deliverable (1):** structure + content model doc for approval | **PROVISIONAL:** ~3–5 working days *after* product list + matrix draft inputs | Official products/fields; rewrite vs visual-only matrix; which pages must be trilingual | Dev fee $0 | Without products/matrix, model is incomplete |
| A2 — Homepage + product designs | Design for approval (not from `concept-preview/`) | **First visible deliverable (2):** homepage + product-page designs | **PROVISIONAL:** ~5–10 working days *after* A1 approval + brand/think-tank direction | Approve/reject designs; brand direction; sample product content | Dev fee $0 | Design system still OPEN until approved |
| B — Foundation | Headless WP lean + Nuxt shell + i18n routing + staging + RBAC | Staging URL; access roles; CI skeleton | **PROVISIONAL:** ~5–8 working days *after* host plan + design tokens direction | Final host after Liara review; Abadis account ownership; who gets staging/prod access | Liara floor **≥ 4,000,000 tomans/mo** (plan TBD); Cursor Pro+ **$60/mo verify**; other infra TBD | Host not finally locked |
| C — Migration tooling | Extract/map/dry-run/reconcile | Migration scripts + ID maps + reconcile report | **PROVISIONAL:** ~5–10 working days *after* content model freeze | WP access; confirm field sources beyond default REST | Dev fee $0; storage/CDN TBD | WP fetch was capped in audit (309 items) |
| D — Build templates | Priority pages + calculator + forms→DB→n8n + SEO heads | Staging templates matching approved designs | **PROVISIONAL:** ~10–20 working days *after* A2 approval | Content copy approvals; calculator/impact formulas if shipping | Dev fee $0 | Formulas OPEN; Arabic lang defects must be fixed |
| E — Hardening | Perf, a11y, backup restore drill, analytics, monitoring | Signed checklist items | **PROVISIONAL:** ~3–7 working days | Perf budgets; analytics tool; monitoring channel/owner; privacy retention | Monitoring/analytics tools TBD (no invented prices) | Budgets/channel OPEN |
| F — Launch | Cutover, redirects, form tests, rollback ready | Live Phase 1 site | **PROVISIONAL:** cutover window TBD after E | Go/no-go owner; freeze window | Hosting ongoing | No completion date inventable |
| G — Warranty | Bug-fix | Fixes within warranty | **Verified policy:** **60 days** post-launch (response-time SLA still OPEN) | Named responders | Dev fee $0 | SLA details OPEN |

**Optional (not scheduled in base Phase 1):** chatbot, Experiences, anniversary game, 3D viewer — only if separately approved (cost/time TBD then).

**Phase 2:** PayamGostar portal — **out of this plan’s cost and schedule**.

---

## 4. Infrastructure / tool cost sheet (not development)

| Item | Status | Amount |
|---|---|---|
| Development fee | MANAGEMENT | **$0** |
| Liara (hosting — first option to examine) | MANAGEMENT floor + review | **Minimum budget floor 4,000,000 tomans/month**; actual plan after cost/location/backup/recovery/access review |
| Cursor Pro+ | Required for current workflow | **$60/month** — **verify current pricing** before purchase |
| n8n | Existing config: Cloud instance `hamidafghah.app.n8n.cloud` (workflows documented) | **Subscription plan/price not documented** — do not invent |
| Database / object storage / CDN / backups | Likely needed with chosen host | **Cost unknown** — list TBD after host plan |
| Email / SMS / messenger notify | May be needed for lead alerts | **Cost unknown** |
| Analytics / monitoring tools | Required in principle | **Cost unknown** until tool chosen |
| Phase 2 PayamGostar | Separate contract | **Excluded** from Phase 1 |

---

## 5. Acceptance criteria (Phase 1 base)

Aligned with Master Spec §25 + management confirmations:

- Stack, content model, deploy method documented  
- URL map + redirects + hreflang FA/EN/AR tested on agreed samples  
- Media/download critical links healthy or dispositioned  
- Forms: durable save **before** success UI; notify path tested; sales can see leads  
- Staging not accidentally indexed; RBAC demonstrated  
- Backup + **successful restore drill** signed  
- Launch go/no-go + rollback plan documented  
- Arabic root `lang` correct (fixes sample defect)  
- Designs match **approved** visual system — **not** `concept-preview/`  
- Chatbot / Experiences / anniversary / 3D **not** required for base acceptance  

---

## 6. Outstanding decisions and risks

See Master Spec §26B. Highest schedule risks:

1. Missing product list / content matrix → blocks A1–A2 reliable dates  
2. No approved visual system → blocks build  
3. Final host not chosen after Liara review → blocks staging/prod  
4. Sales notify channel/owner unresolved → blocks form acceptance  
5. Audit HTML sample only (10 pages) + **0** broken-link checks → residual SEO/404 risk until later pass  

---

## 7. Provisional project timeline (summary)

| Block | Status |
|---|---|
| Discovery / audit / spec / management capture | **Completed** calendar window **21–26 Sep 2026** (~5–6 days elapsed). Active hours **unknown**. |
| Approval / waiting for remaining OPEN inputs | **Unknown duration** |
| First visible deliverable (structure/model → home+product designs) | **PROVISIONAL** working days in table §3 — depends on Abadis inputs |
| Foundation → launch | **PROVISIONAL** only; **no completion date** claimed |
| Phase 2 PayamGostar | **Outside** Phase 1 |

**Total provisional statement:** Phase 1 cannot be given a credible end date until §26B ★ inputs and design approval land. Discovery elapsed so far is approximately **5–6 calendar days**, not billable person-days.
