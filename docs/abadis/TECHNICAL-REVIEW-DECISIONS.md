# Technical Review — Decisions Register

**Purpose:** Answer every explicit question, unresolved choice, and required approval in  
`docs/abadis/references/Abadis_WordPress_to_Nuxt_Migration_Technical_Review_FA.pdf`  
using current evidence and project direction — **without implementing anything**.

**Sources used**
- Technical Review PDF (primary question source)
- `docs/abadis/ABADIS-MASTER-SPECIFICATION.md`
- `docs/abadis/ABADIS-AUDIT.json`
- `docs/abadis/MASTER-MIGRATION-PLAN.md` (non-authoritative where unsupported)
- Design brief docx (business wants; Phase boundaries)

**Project direction respected (not all CONFIRMED by boss documents)**
- Frontend target: **Nuxt 4** (project direction; PDF cites Nuxt 4.x docs)
- WordPress is the **current** CMS (**FACT**)
- **n8n** required for automation (**BRIEF REQUIREMENT** in PDF + project direction)
- **Liara** = intended hosting from project discussion → **PROPOSED**, not CONFIRMED unless boss docs say so (they do not)
- `concept-preview/` = rejected visual reference only
- Preserve SEO, valuable URLs, content, media, downloads, functionality
- Phase 2 PayamGostar CRM ≠ Phase 1 unless approved
- No invented product CPT, claims, formulas, CRM capabilities, or readiness claims

**Status values**
| Status | Meaning |
|---|---|
| **CONFIRMED** | Locked by evidence + explicit technical/business direction that does not need further choice |
| **PROPOSED** | Reasonable technical proposal supported by evidence + project direction; still needs stakeholder ack if it spends money/scope |
| **HUMAN DECISION** | Requires Abadis/boss/content/sales approval |
| **UNKNOWN** | Evidence insufficient to propose safely |

---

## D01 — Is the six-part development proposal enough to start, or must it become an executable statement of work?

1. **QUESTION**  
   PDF §1: The six-part proposal (content migrate, SEO preserve, file migrate, forms, periodic monitoring, AI) is directionally correct but is **not** yet an executable SOW. Before start, each part needs deliverable, test method, cost, time, and owner.

2. **WHAT THE CURRENT EVIDENCE SHOWS**  
   - Master Specification exists and maps Phase 1/2, acceptance themes, and unknowns.  
   - No signed per-phase commercial SOW with owners/costs is in the repo evidence.  
   - Audit inventories exist (718 URLs, WP totals) but HTML sample is limited (10 pages).

3. **RECOMMENDED PROJECT DECISION**  
   Treat `ABADIS-MASTER-SPECIFICATION.md` + this decisions register as the **technical baseline**, then produce a commercial SOW table (deliverable / test / cost / duration / owner) before coding production Nuxt.

4. **WHY**  
   Matches PDF §1 and §13 request to development team; avoids starting build on an incomplete brief.

5. **WHAT REQUIRES BOSS/ABADIS APPROVAL**  
   Budget, timeline, named owners, and which Phase 1 extras (chatbot, Experiences, anniversary) are in-contract.

6. **STATUS:** **HUMAN DECISION** (SOW commercial lock) · technical baseline **PROPOSED**

---

## D02 — What is the primary project goal beyond visual redesign?

1. **QUESTION**  
   PDF §1: Confirm goal = preserve valuable information/URLs, keep CMS simple, ensure customer requests reach sales without loss — not appearance-only.

2. **WHAT THE CURRENT EVIDENCE SHOWS**  
   - Design brief also asks structural/content redesign + gradual ordering tool.  
   - Audit shows real SEO/lang/form surface that must be preserved/fixed.  
   - Forms observed in HTML; durable CRM path **not** verified.

3. **RECOMMENDED PROJECT DECISION**  
   **CONFIRMED as project principle:** migration + redesign must preserve SEO equity, content value, media/downloads, and durable lead capture. Visual redesign alone is out of compliance with the Technical Review.

4. **WHY**  
   Explicit PDF goal; aligned with design brief “not just color/skin” and Master Spec.

5. **WHAT REQUIRES BOSS/ABADIS APPROVAL**  
   Relative priority if schedule forces tradeoffs (e.g. ship SEO-safe migrate first vs full redesign extras).

6. **STATUS:** **CONFIRMED** (principle) · prioritization under constraint → **HUMAN DECISION**

---

## D03 — Architecture responsibility split (Nuxt / CMS / Migration tool / n8n)?

1. **QUESTION**  
   PDF §2: Confirm roles: Nuxt = site; CMS/DB = source of truth; Migration tool = extract/transform/validate; n8n = automation.

2. **WHAT THE CURRENT EVIDENCE SHOWS**  
   - Current public site is WordPress + Elementor/JetEngine/Yoast (**FACT**).  
   - n8n already used for audit automation (project), not production lead pipelines.  
   - PDF diagrams:  
     `WP → Migration Tool → CMS/DB → Nuxt → CDN`  
     `Site/DB → API/Webhook → n8n → CRM/AI/Notifications`

3. **RECOMMENDED PROJECT DECISION**  
   **Adopt PDF split as architecture policy:**  
   - Nuxt 4 = public frontend  
   - CMS/DB = content source of truth (see D05 for which CMS)  
   - Dedicated migration tooling (scripted, testable)  
   - n8n = forms/notifications/monitoring/AI-assist queues  

4. **WHY**  
   Explicit Technical Review architecture; matches project direction (Nuxt 4, n8n).

5. **WHAT REQUIRES BOSS/ABADIS APPROVAL**  
   None for the split itself; CMS/host choices separate (D05, D06).

6. **STATUS:** **CONFIRMED** (responsibility split)

---

## D04 — Exact Nuxt version?

1. **QUESTION**  
   PDF §2 “انتخاب نسخه و ابزار / نسخه دقیق”: choose exact Nuxt version; old versions need justification and support plan. PDF references Nuxt 4.x rendering docs and Nuxt roadmap/support pages.

2. **WHAT THE CURRENT EVIDENCE SHOWS**  
   - Project direction: Nuxt 4.  
   - PDF links `nuxt.com/docs/4.x/...`.  
   - No live Nuxt app evidenced on production (current site is WP).

3. **RECOMMENDED PROJECT DECISION**  
   **Use Nuxt 4.x (current stable 4.x line at implementation start)** for the new frontend. Document exact patched version in the architecture register at kickoff. Do not start on Nuxt 2; Nuxt 3 only if 4.x is blocked (would need written justification per PDF).

4. **WHY**  
   Project direction + PDF 4.x documentation reference; avoids unsupported old major.

5. **WHAT REQUIRES BOSS/ABADIS APPROVAL**  
   Ack only if commercial SOW must freeze a major version; otherwise engineering can pin patch versions.

6. **STATUS:** **PROPOSED** (Nuxt 4.x) — treat as project-confirmed direction pending SOW freeze

---

## D05 — Final CMS / source of truth?

1. **QUESTION**  
   PDF §2–§3: Final CMS choice after current-site review. Options compared by cost and content-team need: headless WordPress, independent CMS, or custom system. CMS/DB must be source of truth for products and pages; editing roles must be defined.

2. **WHAT THE CURRENT EVIDENCE SHOWS**  
   - WordPress is current CMS with rich plugin stack (Elementor Pro, JetEngine, Yoast) — **FACT**.  
   - Public types include pages/posts/attachments and JetEngine CPTs (`_customers`, `_franchise`, `_downloadcenter`, `_joboffers`) — **FACT**.  
   - No public REST type named `product` — **FACT** (absence).  
   - PDF leaves CMS choice open.  
   - Master Spec recommends headless WP as a proposal, not confirmed.

3. **RECOMMENDED PROJECT DECISION**  
   **PROPOSED default:** keep **WordPress as headless CMS / source of truth** for Phase 1 (content editors already on WP; REST + Yoast/JetEngine already present), with Nuxt consuming WP (or a cleaned WP content layer).  
   Evaluate independent CMS only if headless WP cannot expose required product fields cleanly after a spike.

4. **WHY**  
   Minimizes editor retraining and reuses existing content store; matches “WordPress is currently the CMS” direction. PDF requires comparison — proposal is the default pending cost/editor decision.

5. **WHAT REQUIRES BOSS/ABADIS APPROVAL**  
   Final CMS choice (headless WP vs new CMS vs custom), editor workflow, and licensing implications.

6. **STATUS:** **HUMAN DECISION** (final CMS) · default technical lean **PROPOSED** (headless WP)

---

## D06 — Hosting / CDN?

1. **QUESTION**  
   PDF §2: Final host selection after current-site review. Architecture includes CDN. Storage/CDN/naming for media must be specified (§5).

2. **WHAT THE CURRENT EVIDENCE SHOWS**  
   - Boss brief/PDF do **not** name Liara.  
   - Project discussion intends Liara.  
   - Audit does not validate any target host readiness.  
   - MASTER plan “Liara ready” is **unsupported** → ignored as FACT.

3. **RECOMMENDED PROJECT DECISION**  
   **PROPOSED:** plan deployment toward **Liara** for Nuxt (+ WP if headless WP remains), with CDN for media as required by PDF. Mark host **unconfirmed** until Abadis approves environment and cost.

4. **WHY**  
   Respects project discussion without falsely confirming boss-document lock-in.

5. **WHAT REQUIRES BOSS/ABADIS APPROVAL**  
   Host vendor (Liara vs other), environments (prod/staging), CDN product, and who pays/operates.

6. **STATUS:** **PROPOSED** (Liara direction) · **HUMAN DECISION** (final host) · readiness **UNKNOWN**

---

## D07 — Performance criteria before delivery?

1. **QUESTION**  
   PDF §2 & §7: Performance metrics, sample pages, devices, and test conditions must be agreed before delivery. Cache freshness policy must prevent stale content.

2. **WHAT THE CURRENT EVIDENCE SHOWS**  
   - No CWV numbers in `ABADIS-AUDIT.json`.  
   - Sample pages are heavy (home FA: 117 images).  
   - No agreed LCP/INP/CLS budgets in sources.

3. **RECOMMENDED PROJECT DECISION**  
   **PROPOSED engineering defaults** (subject to approval): measure LCP/INP/CLS on agreed sample set (home FA/EN/AR, one product-like page, calculator, contact) on mobile + desktop; define numeric budgets in SOW. Prefer SSR/ISR for main product/content HTML; cache policy with revalidation on publish.

4. **WHY**  
   PDF forbids delivering without agreed criteria; evidence shows image-heavy pages need budgets.

5. **WHAT REQUIRES BOSS/ABADIS APPROVAL**  
   Sample URL list and pass/fail numeric thresholds.

6. **STATUS:** **HUMAN DECISION** (budgets) · approach **PROPOSED** · current CWV **UNKNOWN**

---

## D08 — Data model before migration?

1. **QUESTION**  
   PDF §3: Define content types, product fields, relations, SEO fields, and roles before transfer.

2. **WHAT THE CURRENT EVIDENCE SHOWS**  
   - Required types in PDF: product, page, article, category, catalog, download file.  
   - WP totals known; product CPT not evidenced.  
   - JetEngine CPTs map to non-product business objects.

3. **RECOMMENDED PROJECT DECISION**  
   **PROPOSED model to draft next (not inventing SKUs):**  
   - Types: `Page`, `Post/Article`, `Product` (target), `Category`, `Download/Catalog`, plus migrate existing `_customers`, `_franchise`, `_joboffers`, `_downloadcenter`, `_citynmg` as structured content or related types.  
   - Product fields per PDF: name, model, specs, use-case, images, files, publish status + SEO fields.  
   - Roles: author, reviewer, publisher, admin.  
   - Language variants linked explicitly (FA/EN/AR).

4. **WHY**  
   PDF gate before migration; audit proves WP surface but not product schema.

5. **WHAT REQUIRES BOSS/ABADIS APPROVAL**  
   Canonical product list/source; which JetEngine types remain public; who holds which roles.

6. **STATUS:** **PROPOSED** (model outline) · product source **HUMAN DECISION** · full field schema **UNKNOWN** until WP custom-field inventory

---

## D09 — Where do “products” come from in the current site?

1. **QUESTION**  
   PDF §3–§4: Products must be modeled; do not assume default REST exposes all product/custom/SEO fields.

2. **WHAT THE CURRENT EVIDENCE SHOWS**  
   - No `product` in public types list — **FACT**.  
   - Product-like pages/URLs exist (INFERENCE from audit relationships/sample).  
   - Design brief centers products as Priority 1.

3. **RECOMMENDED PROJECT DECISION**  
   **Do not assume a product CPT exists.** Run a dedicated product-source inventory (pages under محصولات, Elementor templates, any private meta). Then map into target `Product` type with human validation per URL.

4. **WHY**  
   Evidence contradicts assuming a clean CPT; brief still requires product IA.

5. **WHAT REQUIRES BOSS/ABADIS APPROVAL**  
   Approved product URL/SKU list and which fields are mandatory on launch.

6. **STATUS:** **UNKNOWN** (source schema) · approach **PROPOSED** · list **HUMAN DECISION**

---

## D10 — Migration tooling method?

1. **QUESTION**  
   PDF §4: Use testable migration approach with dry-run, old/new IDs, idempotent re-run, count/field compare, backup + rollback. WP REST OK for pages/media; custom fields & SEO plugins need separate checks.

2. **WHAT THE CURRENT EVIDENCE SHOWS**  
   - WP REST reachable; Yoast/JetEngine namespaces present — **FACT**.  
   - Items fetched in audit were capped (309) vs totals — full extract not done.  
   - n8n audit workflow ≠ content migration tool.

3. **RECOMMENDED PROJECT DECISION**  
   **PROPOSED:** build/use a dedicated, testable migration script/pipeline (not one-off manual copy) that:  
   - Dry-runs without writing destination  
   - Stores `legacy_id → new_id`  
   - Is idempotent  
   - Emits reconcile reports  
   - Treats Yoast/`yoast_head_json` and JetEngine meta as first-class extract tasks  

4. **WHY**  
   Exact PDF method; evidence shows REST alone is incomplete for plugins.

5. **WHAT REQUIRES BOSS/ABADIS APPROVAL**  
   Access credentials for staging WP; acceptance of reconcile diffs (what may be dropped).

6. **STATUS:** **PROPOSED** (method) · credentials/access **HUMAN DECISION**

---

## D11 — Media, catalogs, downloads, GLB?

1. **QUESTION**  
   PDF §5: Preserve original files, alt, captions, product links; important URLs must not break on rename; define storage/CDN/naming; GLB files are part of migration; delivery = transferred list + failures + approved diffs; spot-checks ≠ full reconcile.

2. **WHAT THE CURRENT EVIDENCE SHOWS**  
   - Attachments total **1727**; media sitemap **1053**; `_downloadcenter` **9** — **FACT**.  
   - Many missing alts on sampled pages — **FACT**.  
   - **0** GLB/Three.js mentions in audit JSON — **FACT** (not found in this evidence).  
   - Design brief wants new factory video + 2D install animations (assets), separate from GLB.

3. **RECOMMENDED PROJECT DECISION**  
   - **PROPOSED:** migrate all WP media + download-center files with stable URL strategy (prefer preserve paths or 301 map).  
   - **PROPOSED:** during full media extract, search library for `.glb`/`.gltf`; if found, migrate binaries.  
   - **Do not claim** 3D viewers are required until boss decides.  
   - Alt repair is in-scope for Priority pages at minimum.

4. **WHY**  
   Honors PDF file migration + evidence of large media corpus without inventing live 3D presence.

5. **WHAT REQUIRES BOSS/ABADIS APPROVAL**  
   Whether Phase 1 includes interactive 3D/GLB viewers; CDN/naming policy; asset production for video/2D animations.

6. **STATUS:** **PROPOSED** (migrate files) · 3D viewer **HUMAN DECISION** · live GLB presence **UNKNOWN** (not in HTML evidence; library not fully scanned)

---

## D12 — SEO / URL preservation rules?

1. **QUESTION**  
   PDF §6: Keep URLs where possible; pre-launch mapping file; sources = crawl, sitemap, content export, Search Console; matrix columns Old/New/Action/Status/Test; 301 vs 404/410 rules; control meta/H1/canonical/OG/alt/internal links/JSON-LD/sitemap/robots/hreflang; multilingual language links; SEO preserve ≠ ranking guarantee; monitor traffic/index post-launch.

2. **WHAT THE CURRENT EVIDENCE SHOWS**  
   - 718 URL inventory complete — **FACT**.  
   - Sample defects: missing H1s, missing alts, Arabic `lang=fa-IR`, empty hreflang, apex vs `www` — **FACT**.  
   - Link-check count 0 this audit — orphan census incomplete — **FACT**.  
   - EN root redirect chain length 2 — **FACT**.

3. **RECOMMENDED PROJECT DECISION**  
   **CONFIRMED policy:** preserve URLs by default; build full redirect map before launch; never soft-404 to homepage; fix language/hreflang/H1/alt issues in new templates; post-launch SEO monitoring required.  
   **PROPOSED:** use audit inventory + Search Console export (when provided) as map sources.

4. **WHY**  
   Core PDF requirement; evidence already shows multilingual/SEO defects to fix.

5. **WHAT REQUIRES BOSS/ABADIS APPROVAL**  
   Search Console access; apex vs `www` canonical host; which URLs may intentionally change.

6. **STATUS:** **CONFIRMED** (policy) · host canonicalization **HUMAN DECISION** · Search Console data **UNKNOWN** until access

---

## D13 — Deleted pages: 404 vs 410?

1. **QUESTION**  
   PDF §6 + §14 clarification: removed pages without replacement may correctly return **404**; **410** is not the only option; do not redirect unrelated URLs to home.

2. **WHAT THE CURRENT EVIDENCE SHOWS**  
   - No approved deletion list yet.  
   - PDF explicitly corrected earlier absolute 410 guidance.

3. **RECOMMENDED PROJECT DECISION**  
   **PROPOSED default:** use **404** for removed URLs without replacement unless SEO counsel requests 410 for deliberately purged content. Never 301 removed URLs to homepage as a dump.

4. **WHY**  
   Matches PDF §14 correction.

5. **WHAT REQUIRES BOSS/ABADIS APPROVAL**  
   Deletion list (if any) and whether any URL warrants 410.

6. **STATUS:** **PROPOSED** (404 default) · deletion list **HUMAN DECISION**

---

## D14 — Page rendering strategy (SSR / SSG / hybrid) + cache?

1. **QUESTION**  
   PDF §7: Main product/content text should be server-rendered or hybrid with suitable cache; cache update policy must avoid stale content; optimize images/fonts; defer noncritical assets; check SSR/CSR mismatches.

2. **WHAT THE CURRENT EVIDENCE SHOWS**  
   - Current site is WP/Elementor (client-heavy patterns inferred from stack signals).  
   - No Nuxt rendering choice locked in boss PDF beyond recommendation.

3. **RECOMMENDED PROJECT DECISION**  
   **PROPOSED for Nuxt 4:**  
   - Default **SSR or ISR** for product, article, key marketing pages.  
   - Static generation where content is rarely changed (if beneficial).  
   - On-demand/revalidate on CMS publish.  
   - Image optimization pipeline + font subsetting for FA/EN/AR.

4. **WHY**  
   Aligns with PDF §7 and Nuxt 4 rendering capabilities cited by PDF.

5. **WHAT REQUIRES BOSS/ABADIS APPROVAL**  
   None for default approach; only if a specific page must be fully client-only for a business reason.

6. **STATUS:** **PROPOSED**

---

## D15 — Forms & lead preservation design?

1. **QUESTION**  
   PDF §8: Persist first, then notify; success UI only after durable save; server validation; spam/rate limits; timestamp/source/UTM; dedupe/retry/alerts; owner + response SLA + outcome; full path test to sales visibility even if notification fails.

2. **WHAT THE CURRENT EVIDENCE SHOWS**  
   - Sample forms: collaboration, FA/EN calculator (Gravity), EN contact (Elementor), comment forms — **FACT**.  
   - Backend persistence/CRM routing **not** verified — **UNKNOWN**.  
   - Design brief Phase 2 wants PayamGostar; Phase 1 must still not lose leads.

3. **RECOMMENDED PROJECT DECISION**  
   **PROPOSED Phase 1:**  
   `Form → server validate → durable DB record → n8n queue → email/Telegram sales notify (+ optional CRM lead create if credentials exist)`  
   Success message only after DB write.  
   **Do not** assume full PayamGostar order portal in Phase 1.

4. **WHY**  
   Exact PDF pipeline; separates Phase 2 CRM portal from Phase 1 lead safety.

5. **WHAT REQUIRES BOSS/ABADIS APPROVAL**  
   Sales owner, response SLA, notification channel, which forms are lead-critical, whether Phase 1 creates CRM leads.

6. **STATUS:** **PROPOSED** (architecture) · owners/SLA/channels **HUMAN DECISION** · current persistence **UNKNOWN**

---

## D16 — Monitoring / periodic automations?

1. **QUESTION**  
   PDF §9: Monitoring shorter than daily may be required; exact interval and alert thresholds must be agreed; cover uptime, 5xx, API health, failed forms, missing assets/broken links, SSL/domain/sitemap/automations, speed/index/traffic anomalies; tooling may run checks; owner per error class required.

2. **WHAT THE CURRENT EVIDENCE SHOWS**  
   - n8n available in project; production monitors not evidenced.  
   - Broken-link audit count = 0 in last evidence run.

3. **RECOMMENDED PROJECT DECISION**  
   **PROPOSED:** n8n (and/or uptime tool) schedules:  
   - Frequent checks for homepage + form endpoints + SSL  
   - Daily sitemap/form-failure/broken critical-asset checks  
   Thresholds and on-call owner set in SOW.

4. **WHY**  
   PDF requires agreed intervals/owners; n8n already in stack direction.

5. **WHAT REQUIRES BOSS/ABADIS APPROVAL**  
   Interval, thresholds, alert destination, named fixer per class.

6. **STATUS:** **HUMAN DECISION** (ops parameters) · tooling approach **PROPOSED**

---

## D17 — AI content generation controls?

1. **QUESTION**  
   PDF §10: AI only from verified data → structured draft → validation → human approval → publish; no invented product claims; log prompt version, model, source, approver; allow edit/reject/regenerate; review FA and EN separately (AR implied by trilingual site).

2. **WHAT THE CURRENT EVIDENCE SHOWS**  
   - Design brief wants chatbot (separate from CMS AI drafting).  
   - PDF rule is about **content publishing**, not unconstrained generation.

3. **RECOMMENDED PROJECT DECISION**  
   **CONFIRMED policy:** no AI-published product specs without human approval; verified-data-only pipeline.  
   Chatbot (if built) must use the same grounding rule.

4. **WHY**  
   Explicit PDF; prevents medical/product hallucination risk.

5. **WHAT REQUIRES BOSS/ABADIS APPROVAL**  
   Named human approver(s); whether AI drafting is in Phase 1 SOW at all.

6. **STATUS:** **CONFIRMED** (policy) · approver naming **HUMAN DECISION**

---

## D18 — Chatbot (from design brief, intersecting PDF AI/CRM automation)?

1. **QUESTION**  
   Not a PDF numbered “choose X”, but PDF automation path includes AI/notifications and design brief requires chatbot functions. Decision: in Phase 1 scope?

2. **WHAT THE CURRENT EVIDENCE SHOWS**  
   - Brief lists allowed chatbot functions.  
   - No chatbot evidenced on current site.  
   - Master Spec marks Phase 1 inclusion as human decision.

3. **RECOMMENDED PROJECT DECISION**  
   **PROPOSED:** treat chatbot as **optional Phase 1 module** — implement only if SOW includes it; otherwise backlog. If included, ground on verified CMS/FAQ/download content only.

4. **WHY**  
   Avoid assuming Phase 1 scope creep; still respect brief.

5. **WHAT REQUIRES BOSS/ABADIS APPROVAL**  
   In/out of Phase 1; vendor vs custom; languages; handoff to sales.

6. **STATUS:** **HUMAN DECISION**

---

## D19 — PayamGostar / CRM?

1. **QUESTION**  
   PDF diagrams include `n8n → CRM`. Design brief Phase 2 specifies PayamGostar customer portal features. Decision: what CRM work is in which phase?

2. **WHAT THE CURRENT EVIDENCE SHOWS**  
   - PayamGostar is a **brief Phase 2** want.  
   - Form→CRM not verified on current site.  
   - Must not assume Phase 2 inside Phase 1.

3. **RECOMMENDED PROJECT DECISION**  
   - **Phase 1 PROPOSED:** durable leads + n8n notify sales; optional “create CRM lead” if API ready.  
   - **Phase 2:** full PayamGostar account/order/invoice/dashboard per brief — only if contracted.

4. **WHY**  
   Honors phase split; satisfies PDF “don’t lose requests” without inventing CRM portal in Phase 1.

5. **WHAT REQUIRES BOSS/ABADIS APPROVAL**  
   Phase 2 in contract?; API access; which objects; whether Phase 1 writes leads to PayamGostar.

6. **STATUS:** **HUMAN DECISION** (scope/API) · phase split **PROPOSED**

---

## D20 — Authentication / “Our Experiences”?

1. **QUESTION**  
   PDF requires access control generally; design brief requires passworded Experiences area. Not specified in PDF architecture detail.

2. **WHAT THE CURRENT EVIDENCE SHOWS**  
   - Brief lists Experiences domains.  
   - No evidence of such area on current site.

3. **RECOMMENDED PROJECT DECISION**  
   **PROPOSED:** out of critical path unless SOW includes it; if included, noindex authenticated area with explicit auth model chosen by Abadis.

4. **WHY**  
   Avoid blocking migration/SEO core on an undefined private portal.

5. **WHAT REQUIRES BOSS/ABADIS APPROVAL**  
   In/out of Phase 1; auth model; user list; content owners.

6. **STATUS:** **HUMAN DECISION**

---

## D21 — Staging environment?

1. **QUESTION**  
   PDF §11: Separate staging from production; controlled access; prevent accidental indexing.

2. **WHAT THE CURRENT EVIDENCE SHOWS**  
   - Required by PDF; no staging details in audit.

3. **RECOMMENDED PROJECT DECISION**  
   **CONFIRMED requirement:** staging for Nuxt (+ CMS) with `noindex`, basic auth or VPN, separate secrets.  
   **PROPOSED:** host staging on same intended platform family as prod (e.g. Liara staging) once host chosen.

4. **WHY**  
   Non-negotiable PDF acceptance item.

5. **WHAT REQUIRES BOSS/ABADIS APPROVAL**  
   Who gets staging access; domain names.

6. **STATUS:** **CONFIRMED** (must have staging) · access list **HUMAN DECISION**

---

## D22 — Security baseline?

1. **QUESTION**  
   PDF §11 & acceptance: secrets management, access levels, dependency updates, input controls; access + backup/restore confirmed at acceptance.

2. **WHAT THE CURRENT EVIDENCE SHOWS**  
   - Current WP security posture **not** audited in JSON.  
   - MASTER “security verified” is invalid.

3. **RECOMMENDED PROJECT DECISION**  
   **PROPOSED baseline:** env-based secrets, least-privilege tokens, server-side form validation, dependency update policy, staging isolation.  
   Do **not** claim current site is secure.

4. **WHY**  
   PDF minimum; evidence gap on current security.

5. **WHAT REQUIRES BOSS/ABADIS APPROVAL**  
   Who holds production secrets; SSO/VPN requirements if any.

6. **STATUS:** **PROPOSED** (baseline) · current posture **UNKNOWN**

---

## D23 — Backup & restore?

1. **QUESTION**  
   PDF §11: Defined backup plan with **real restore test**; acceptance requires proven restore.

2. **WHAT THE CURRENT EVIDENCE SHOWS**  
   - No backup/restore evidence in audit.

3. **RECOMMENDED PROJECT DECISION**  
   **CONFIRMED requirement:** automated backups of CMS DB, media, and app config; schedule restore drill before launch; document RPO/RTO targets in SOW.

4. **WHY**  
   Explicit PDF acceptance criterion.

5. **WHAT REQUIRES BOSS/ABADIS APPROVAL**  
   RPO/RTO numbers and who signs the restore drill.

6. **STATUS:** **CONFIRMED** (must do) · numeric RPO/RTO **HUMAN DECISION**

---

## D24 — Analytics / measurement?

1. **QUESTION**  
   PDF §11: Configure visit analytics, form-submit events, needed conversions.

2. **WHAT THE CURRENT EVIDENCE SHOWS**  
   - No analytics configuration captured in audit JSON.

3. **RECOMMENDED PROJECT DECISION**  
   **PROPOSED minimum events:** page_view, cta_click, form_submit_success/error, calculator_complete, file_download. Tool choice TBD.

4. **WHY**  
   PDF requires measurement; tool not mandated.

5. **WHAT REQUIRES BOSS/ABADIS APPROVAL**  
   Analytics vendor/account; conversion definitions; privacy alignment.

6. **STATUS:** **HUMAN DECISION** (tool/account) · event set **PROPOSED** · current setup **UNKNOWN**

---

## D25 — Privacy / data retention?

1. **QUESTION**  
   PDF §11: Define collectable data, access, retention suited to project needs.

2. **WHAT THE CURRENT EVIDENCE SHOWS**  
   - Forms collect personal data (names/emails etc. on samples).  
   - No retention policy in sources.

3. **RECOMMENDED PROJECT DECISION**  
   **PROPOSED:** document data inventory for forms/chat/CRM; retention periods; access roles — before Phase 1 launch of new forms.

4. **WHY**  
   PDF requirement; cannot invent legal policy.

5. **WHAT REQUIRES BOSS/ABADIS APPROVAL**  
   Retention periods, lawful basis text, DPO/owner.

6. **STATUS:** **HUMAN DECISION**

---

## D26 — Handover deliverables?

1. **QUESTION**  
   PDF §11: Deliver code repo, hosting access, docs, training, bugfix period.

2. **WHAT THE CURRENT EVIDENCE SHOWS**  
   - Standard PDF requirement; no dispute in other sources.

3. **RECOMMENDED PROJECT DECISION**  
   **CONFIRMED:** include handover pack in SOW (repo, envs, runbooks, training, warranty window).

4. **WHY**  
   Explicit PDF deliverable.

5. **WHAT REQUIRES BOSS/ABADIS APPROVAL**  
   Training audience, warranty duration, support response times (also acceptance “پشتیبانی”).

6. **STATUS:** **CONFIRMED** (must include) · commercial terms **HUMAN DECISION**

---

## D27 — Acceptance checklist adoption?

1. **QUESTION**  
   PDF §12: Formal acceptance domains — architecture, data transfer, URLs/SEO, images/files, forms, automation, display quality (mobile/browsers/RTL/a11y/speed), security/recovery, launch, support.

2. **WHAT THE CURRENT EVIDENCE SHOWS**  
   - Master Spec §25 already mirrors this list.  
   - Current audit incomplete for several domains (links, CWV, security).

3. **RECOMMENDED PROJECT DECISION**  
   **CONFIRMED:** use PDF §12 checklist as mandatory launch gate; attach test evidence per row.

4. **WHY**  
   Non-negotiable Technical Review acceptance frame.

5. **WHAT REQUIRES BOSS/ABADIS APPROVAL**  
   Named acceptor per domain; sign-off meeting.

6. **STATUS:** **CONFIRMED**

---

## D28 — Project phases / timeline / owners / cost?

1. **QUESTION**  
   PDF §13: Proposed phases — discovery/design; build + trial migrate; connect/test; launch/stabilize. Asks development team to specify per phase: deliverable, duration, cost, dependencies, owner, acceptance; list out-of-scope and recurring service costs separately.

2. **WHAT THE CURRENT EVIDENCE SHOWS**  
   - Master Spec §28 proposes technical phases A–H.  
   - No cost/owner table filled.

3. **RECOMMENDED PROJECT DECISION**  
   **PROPOSED phase mapping:**  
   1. Discovery/design lock (decisions + data model)  
   2. Foundation (Nuxt 4 + CMS + staging)  
   3. Migration tooling + trial load  
   4. Phase 1 templates/forms/SEO  
   5. Hardening (perf/security/backup/monitor)  
   6. Launch  
   7. Optional Phase 2 CRM (separate SOW line)  

4. **WHY**  
   Answers PDF request structure without inventing prices.

5. **WHAT REQUIRES BOSS/ABADIS APPROVAL**  
   Durations, costs, named Abadis owners, out-of-scope list, recurring fees (hosting/CDN/CRM/monitoring).

6. **STATUS:** **HUMAN DECISION** (commercial) · technical phase order **PROPOSED**

---

## D29 — Rollback / launch stop criteria?

1. **QUESTION**  
   PDF acceptance “انتشار”: execution owner, final cutover time, stop criteria, and rollback plan must be specified.

2. **WHAT THE CURRENT EVIDENCE SHOWS**  
   - Required by PDF; MASTER rollback text was thin/UNKNOWN — correctly downgraded in Master Spec.

3. **RECOMMENDED PROJECT DECISION**  
   **PROPOSED rollback:** keep WP production recoverable until soak period ends; DNS/CDN switch with documented revert; DB/media snapshots pre-cutover; stop criteria examples = critical form failure, widespread 500s, major SEO mapping failure.

4. **WHY**  
   Meets PDF launch gate without pretending a detailed runbook already exists.

5. **WHAT REQUIRES BOSS/ABADIS APPROVAL**  
   Cutover window, go/no-go authority, maximum downtime, rollback authority.

6. **STATUS:** **PROPOSED** (approach) · authority/window **HUMAN DECISION**

---

## D30 — Multilingual (FA/EN/AR) technical choices?

1. **QUESTION**  
   PDF §6: In multilingual sites, control language-version links/settings. (Design brief requires FA/EN/AR.)

2. **WHAT THE CURRENT EVIDENCE SHOWS**  
   - Inventory langs fa 540 / en 101 / ar 77 — **FACT**.  
   - Arabic root `html_lang=fa-IR`; empty hreflang on sample — **FACT**.  
   - EN/AR deep discovery +177 — **FACT**.  
   - Multilingual “fully verified” is **false claim** if asserted.

3. **RECOMMENDED PROJECT DECISION**  
   **CONFIRMED:** ship FA/EN/AR with correct `lang`, hreflang/alternate links, and localized templates.  
   **PROPOSED:** fix Arabic language metadata as a launch blocker.  
   Parity matrix of which pages exist in all languages = approval item.

4. **WHY**  
   Evidence shows defects; brief requires three languages.

5. **WHAT REQUIRES BOSS/ABADIS APPROVAL**  
   Required language coverage matrix; translation ownership.

6. **STATUS:** **CONFIRMED** (must be trilingual + correct metadata) · coverage matrix **HUMAN DECISION** · overall quality verification still **UNKNOWN** beyond sample

---

## D31 — CDN / media naming / image formats?

1. **QUESTION**  
   PDF §5: Specify storage location, CDN, naming policy; mobile/desktop sizes; compression; modern formats (text truncated in extract but intent clear).

2. **WHAT THE CURRENT EVIDENCE SHOWS**  
   - Large media corpus; many missing alts.  
   - No CDN policy documented.

3. **RECOMMENDED PROJECT DECISION**  
   **PROPOSED:** CDN in front of media; preserve legacy public URLs via redirect or path-stable storage; generate responsive derivatives; prefer modern formats where compatible.

4. **WHY**  
   PDF delivery requirement; supports performance goals.

5. **WHAT REQUIRES BOSS/ABADIS APPROVAL**  
   CDN vendor (may follow host choice) and whether public media URL changes are allowed.

6. **STATUS:** **PROPOSED** · vendor **HUMAN DECISION**

---

## D32 — Design system / concept-preview?

1. **QUESTION**  
   Not asked as a PDF bullet, but architecture/delivery implies a UI; project constraint forbids treating rejected concept as approved. Included because it affects “how pages are produced.”

2. **WHAT THE CURRENT EVIDENCE SHOWS**  
   - `concept-preview/` explicitly rejected.  
   - Design brief gives brand attributes + page priorities, not a finished UI kit.

3. **RECOMMENDED PROJECT DECISION**  
   **CONFIRMED:** do not implement from `concept-preview/`. New approved designs required before UI build.

4. **WHY**  
   Hard project constraint + brief still open on final look.

5. **WHAT REQUIRES BOSS/ABADIS APPROVAL**  
   Approved design direction / think-tank outcomes.

6. **STATUS:** **CONFIRMED** (rejection) · new design approval **HUMAN DECISION**

---

## Summary table

| ID | Topic | Status |
|---|---|---|
| D01 | SOW completeness | HUMAN DECISION / baseline PROPOSED |
| D02 | Goal beyond visuals | CONFIRMED |
| D03 | Architecture split | CONFIRMED |
| D04 | Nuxt version | PROPOSED (Nuxt 4.x) |
| D05 | CMS source of truth | HUMAN DECISION / lean PROPOSED headless WP |
| D06 | Hosting (Liara) | PROPOSED / HUMAN DECISION / readiness UNKNOWN |
| D07 | Performance budgets | HUMAN DECISION / approach PROPOSED |
| D08 | Data model | PROPOSED / product source HUMAN DECISION |
| D09 | Product source | UNKNOWN / HUMAN DECISION |
| D10 | Migration tooling | PROPOSED |
| D11 | Media/GLB | PROPOSED / 3D viewer HUMAN DECISION |
| D12 | SEO/URL policy | CONFIRMED |
| D13 | 404 vs 410 | PROPOSED |
| D14 | SSR/ISR/cache | PROPOSED |
| D15 | Forms/leads | PROPOSED / owners HUMAN DECISION |
| D16 | Monitoring | HUMAN DECISION / tooling PROPOSED |
| D17 | AI publish controls | CONFIRMED |
| D18 | Chatbot scope | HUMAN DECISION |
| D19 | PayamGostar/CRM phase | HUMAN DECISION |
| D20 | Experiences auth | HUMAN DECISION |
| D21 | Staging | CONFIRMED |
| D22 | Security baseline | PROPOSED / current UNKNOWN |
| D23 | Backup/restore | CONFIRMED / RPO HUMAN DECISION |
| D24 | Analytics | HUMAN DECISION |
| D25 | Privacy retention | HUMAN DECISION |
| D26 | Handover | CONFIRMED / terms HUMAN DECISION |
| D27 | Acceptance checklist | CONFIRMED |
| D28 | Phases/cost/owners | HUMAN DECISION |
| D29 | Rollback authority | PROPOSED / HUMAN DECISION |
| D30 | Multilingual | CONFIRMED + HUMAN DECISION matrix |
| D31 | CDN/naming | PROPOSED |
| D32 | Design / concept-preview | CONFIRMED rejection + HUMAN DECISION new design |

---

## WHAT I NEED FROM THE BOSS

Only decisions that genuinely need Abadis/business approval (not pure engineering defaults):

1. **Approve commercial SOW** — per-phase deliverables, duration, cost, Abadis owner, acceptance signer (D01, D28).  
2. **Confirm Phase boundary** — Phase 1 only vs include Phase 2 PayamGostar portal (D19).  
3. **Choose final CMS** — keep headless WordPress vs move to another CMS (D05).  
4. **Choose hosting** — confirm or reject **Liara**, plus staging/prod access (D06, D21).  
5. **Approve design direction** — what replaces rejected `concept-preview/` after think-tank (D32).  
6. **Canonical host** — apex `abadis-med.com` vs `www` (D12).  
7. **Product source of truth** — approved product URL/SKU list and mandatory fields (D09, D08).  
8. **Language coverage matrix** — which pages must exist in FA/EN/AR (D30).  
9. **Content change matrix** — rewrite vs visual-only pages (from design brief tension; affects migration acceptance).  
10. **Lead operations** — sales owner, response SLA, notification channel; whether Phase 1 writes CRM leads (D15).  
11. **Monitoring ops** — alert channel, thresholds, on-call names (D16).  
12. **Analytics account + conversions** (D24).  
13. **Privacy retention** for forms/chat/CRM data (D25).  
14. **Backup RPO/RTO** and who signs restore drill (D23).  
15. **Launch authority** — cutover window, go/no-go person, rollback authority (D29).  
16. **Performance pass/fail budgets** and sample URLs (D07).  
17. **Optional Phase 1 modules** — chatbot, Experiences portal, anniversary game: in or out (D18, D20).  
18. **3D/GLB viewer** at launch: yes/no (D11).  
19. **Support terms** — bugfix length and response times (D26).  
20. **Search Console access** for URL mapping completeness (D12).

Engineering may proceed to **planning and spikes** on PROPOSED items after these approvals start landing; **production implementation remains gated** on the starred commercial/architecture choices (especially 1–5, 7, 10, 15).
