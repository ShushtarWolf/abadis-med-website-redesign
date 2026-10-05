# Abadis Med — Master Specification

**Status:** Authoritative bridge document (evidence → requirements → implementation)  
**Created:** 2026-09-25  
**Last management-response update:** 2026-09-26  
**Does not authorize production Nuxt coding** until remaining OPEN / PENDING items that block the current stage are resolved (see §26B and end-state readiness).

### Classification legend (used throughout)

| Label | Meaning |
|---|---|
| **FACT** | Directly supported by `ABADIS-AUDIT.json` (or other cited live evidence) |
| **BRIEF REQUIREMENT** | Explicitly requested in boss design brief and/or technical migration review |
| **MANAGEMENT CONFIRMED** | Explicitly decided in management responses to the Boss Decision Sheet (2026-09) |
| **MANAGEMENT DIRECTION** | Accepted lean / preferred path from management, still subject to named conditions |
| **INFERENCE** | Reasonable interpretation of evidence or brief wording |
| **RECOMMENDATION** | Proposed implementation approach (not yet approved) |
| **UNKNOWN** | Evidence insufficient |
| **OPEN / PENDING** | Still requires Abadis / business / stakeholder input or approval |

### Sources reconciled

1. `docs/abadis/references/Abadis_Website_Design_Brief_Editable.docx` — boss design/content brief  
2. `docs/abadis/references/Abadis_WordPress_to_Nuxt_Migration_Technical_Review_FA.pdf` — technical migration review  
3. `docs/abadis/ABADIS-AUDIT.json` — current-site audit evidence (run generated `2026-09-25T15:24:58.690Z`)  
4. `docs/abadis/MASTER-MIGRATION-PLAN.md` — AI synthesis (non-authoritative where unsupported)  
5. **Management responses** to `BOSS-DECISION-SHEET-FA.md` / WhatsApp decision sheets (two responses, recorded 2026-09-26 into this specification)

### Four-way distinction (mandatory)

| Layer | Meaning |
|---|---|
| **A — EXISTS today** | Observed on current WordPress site (FACT) |
| **B — Boss WANTS** | BRIEF REQUIREMENT |
| **C — We PROPOSE to build** | RECOMMENDATION / MANAGEMENT DIRECTION |
| **D — Needs APPROVAL** | OPEN / PENDING / UNKNOWN |

### Hard constraints

- **MANAGEMENT CONFIRMED + FACT:** `concept-preview/` is **NOT** an approved visual reference. Rejected concept — visual reference only.  
- Do not invent product claims, medical claims, impact-counter formulas, CRM capabilities, chatbot answers, URLs, business processes, or unconfirmed infrastructure.  
- Unsupported statements in `MASTER-MIGRATION-PLAN.md` (e.g. “Liara ready”, “multilingual fully functional”, “security verified”, “product architecture confirmed”, “GLB present”, “form→CRM verified”) are **downgraded** below and must not be treated as FACT.  
- Do not convert **MANAGEMENT DIRECTION** or conditional preferences into final locks.

---

## 1. Executive summary

Abadis needs a **trilingual (FA/EN/AR) website migration and redesign**: preserve SEO equity and content value from the current WordPress site, while delivering a clearer brand story, stronger product presentation, durable lead capture, and (in a **separate** later contract) customer-account / CRM-connected ordering.

**FACT — EXISTS today:** Public WordPress site at `https://abadis-med.com` with Elementor/JetEngine/Yoast signals, **718** inventoried URLs (sitemap + language roots + EN/AR link discovery), public REST totals for posts/pages/attachments and JetEngine CPTs (`_customers`, `_franchise`, `_downloadcenter`, `_joboffers`), and a **10-page** HTML/SEO sample showing quality gaps (especially Arabic `lang=fa-IR`). Broken-link checks were **not** completed in the final audit run.

**MANAGEMENT CONFIRMED — contract:** **Phase 1 now; Phase 2 as a separate contract.** Full PayamGostar customer portal / ordering stays **outside** Phase 1. Phase 1 may prepare for future integration only.

**MANAGEMENT DIRECTION — architecture:** Headless WordPress + Nuxt display layer is the accepted lean for Phase 1. **Liara** is the **first hosting option to examine**; final host approval remains subject to cost, location, backup, recovery, and access review.

**MANAGEMENT CONFIRMED — first visible deliverable:** (1) page structure and content model; (2) homepage and product-page designs for approval. Do not build production UI from `concept-preview/`.

**OPEN / PENDING (still block full implementation):** approved visual design system (beyond rejecting concept-preview), page content matrix, official product list/fields, apex vs `www`, sales owner/SLA/notify channel details, numeric performance budgets, analytics tool choice, monitoring owners, final Liara (or alternate) plan after cost review, and whether Phase 1 gets any PayamGostar API lead write (only if API/access/cost/workload approved).

**Readiness:** **Not READY FOR IMPLEMENTATION** of production Nuxt. Ready for **page structure / content-model drafting** and design-approval sequencing once Abadis inputs listed in §26B are supplied.

---

## 2. Current-state evidence

Audit meta: domain `https://abadis-med.com`; `maxCrawlUrls=10` HTML sample; inventories otherwise more complete.

### 2.1 Inventories (completeness)

| Inventory | complete? | Count / notes | Label |
|---|---|---|---|
| URL inventory | yes | **718** (sitemap + language roots + EN/AR discovery) | FACT |
| Language mix in inventory | yes | fa **540**, en **101**, ar **77** | FACT |
| Child sitemaps | yes | **11** (post, page, jet-menu, joboffers, downloadcenter, customers, franchise, category, post_tag, citynmg, author) | FACT |
| EN/AR deep discovery | yes | **+177** URLs from `/en/` and `/arabic/` HTML | FACT |
| Media sitemap `image:loc` | yes | **1053** | FACT |
| WP REST totals (`X-WP-Total`) | yes | See table below | FACT |
| WP REST items downloaded | no | **309** items this run (capped) | FACT |
| HTML page audits | no | **10** pages only | FACT |
| Forms observed | no | **6** on crawled sample | FACT |
| Broken-link checks | no | **0** this run | FACT |
| GLB / Three.js on live site | — | **0** matches in audit payload | FACT (absence in this evidence) |

### 2.2 Public WordPress REST totals (FACT)

| Key | total | kind |
|---|---|---|
| post | 221 | type |
| page | 26 | type |
| attachment | 1727 | type |
| `_joboffers` | 9 | type |
| `_downloadcenter` | 9 | type |
| `_customers` | 155 | type |
| `_franchise` | 26 | type |
| category | 8 | taxonomy |
| post_tag | 76 | taxonomy |
| `_citynmg` | 31 | taxonomy |

**FACT:** Public type keys also include `jet-menu`, `jet-engine`, plus core WP types.  
**FACT:** WP namespaces observed include `yoast/v1`, `elementor/v1`, `elementor-pro/v1`, `jet-engine/v2`, `jet-menu-api/v2`, `wp/v2`.  
**INFERENCE:** There is **no** dedicated public REST type named `product` in the audited types list; product content may live as pages/Elementor compositions and/or posts.  
**UNKNOWN:** Full custom-field / ACF / JetEngine meta schemas for products.

### 2.3 Sample HTML audits (FACT — sample only, not site-wide)

Pages crawled (10): home FA, `/en/`, `/arabic/`, one news-like post, فرصت‌های همکاری, محاسبه‌گر, EN contact, EN calculator, مخزن ساکشن چیست؟, کیسه ساکشن چیست؟.

Notable observations:

| Observation | Evidence | Label |
|---|---|---|
| Home FA: no H1; 117 imgs, 69 missing alt; Yoast robots index/follow; schema WebPage/WebSite/BreadcrumbList | page audit | FACT |
| EN root: `lang=en-US`; canonical to `https://www.abadis-med.com/en/`; 2-hop redirect chain; no H1; empty hreflang | page audit | FACT |
| Arabic root: **`html_lang=fa-IR`**; robots only `max-image-preview:large`; **no schema**; no Yoast signal in tech flags; empty hreflang | page audit | FACT |
| Collaboration + calculator forms present (Gravity Forms field names `gform_*` on calculator) | forms | FACT |
| EN contact uses Elementor-style `form_fields[name|email|message]` | forms | FACT |
| Some article pages post comments to `wp-comments-post.php` | forms | FACT |
| Tech signals on samples: Elementor, Jet Menu, Jet Engine, UIKit, BdThemes; WhatsApp on samples; Yoast on most non-Arabic samples | technology | FACT |

### 2.4 Downgraded claims from MASTER-MIGRATION-PLAN.md

| Claim in MASTER plan | Correct label here |
|---|---|
| Liara platform is ready | **Downgraded** — management directs Liara as **first option to examine**; final host **OPEN** pending cost/location/backup/recovery/access (§2.5) |
| Multilingual setup is fully functional / verified | **UNKNOWN** / partial **FACT** of problems (Arabic `lang`, empty hreflang on sample) |
| Security protocols verified / “remain in effect” | **UNKNOWN** |
| Product architecture confirmed | **UNKNOWN** (only INFERENCE of product-like URLs) |
| GLB/3D present on current site | **FACT:** not found in this audit evidence |
| Form lead persistence / CRM routing verified | **UNKNOWN** (HTML forms observed; backend path not proven) |
| “Complete media inventory” as migration-ready file set | **INFERENCE** only — sitemap/REST totals exist; full file integrity not verified |

---

## 2.5 Management responses (Boss Decision Sheet) — recorded 2026-09-26

Source: two management responses to the Abadis Boss Decision Sheet / WhatsApp decision packs. Labels below distinguish **CONFIRMED**, **DIRECTION** (conditional), and items still **OPEN**.

### 2.5.1 MANAGEMENT CONFIRMED

| Topic | Decision |
|---|---|
| Contract boundary | **Phase 1 now; Phase 2 as a separate contract.** |
| Phase 1 vs Phase 2 | Phase 1 = new public site foundation (trilingual, SEO/URL/media preservation, durable leads, priority pages). **Phase 2 = PayamGostar customer portal / accounts / orders / invoices / dashboard** — not inside Phase 1 delivery. |
| Account ownership | **Abadis owns** domain, hosting, GitHub, and related service accounts. |
| Access | **Role-based access** for staging and production. |
| Staging | Staging environment required; **staging changes require Abadis approval** before production promotion. |
| Design sequence | Formal **design approval sequence**: structure/content model → homepage + product-page designs for approval → then build. Think-tank / brand brief still inform the visual system. |
| `concept-preview/` | **NOT** an approved visual reference. Must not be the UI source of truth. |
| Languages | Site remains **FA / EN / AR**; language metadata and content correctness required (including fixing known Arabic `lang` defects). |
| Content / products | Content and product materials require **Abadis approval** before publish; official product list and field requirements still to be supplied (see OPEN). |
| URL / SEO / media | **Preserve** valuable URLs, SEO equity, and media/downloads unless Abadis explicitly approves a mapped change. |
| Leads | **Durable storage before notification** — never notify-only without persistence. |
| PayamGostar in Phase 1 | Integration **only if** API access, permissions, cost, and workload are **separately approved**. Otherwise Phase 1 = durable storage + sales notification (n8n). Full portal remains Phase 2. |
| Optional extras | **Chatbot**, **Experiences login**, **anniversary campaign/game**, and **interactive 3D viewer** are **outside base Phase 1 scope** unless separately approved / contracted. Media file migration remains separate from shipping a 3D viewer. |
| Launch / recovery | Documented launch window, go/no-go owner, **rollback** plan, backups, and **tested restore** required. |
| Support | **60-day** post-launch bug-fix period (response-time SLAs still OPEN if not named). |
| Analytics / privacy | Analytics + key events required; collectable data, access, and retention must be defined (tool/retention details still OPEN where not named). |
| Performance / monitoring | Performance acceptance and monitoring with alerts are required (numeric budgets / channel / on-call still OPEN where not named). |
| First visible deliverable | **(1)** Page structure + content model; **(2)** Homepage and product-page designs for approval. |

### 2.5.2 MANAGEMENT DIRECTION (conditional — not a final lock)

| Topic | Direction | Condition / remaining approval |
|---|---|---|
| CMS | **Headless WordPress** as the accepted Phase 1 architecture lean (Nuxt as display layer) | Data model, editor workflows, and field completeness still to be confirmed during content-model stage |
| Hosting | Examine **Liara first** | Final hosting approval subject to **cost, location, backup, recovery, and access** review. Minimum budget floor communicated for planning: **4,000,000 tomans/month** (actual plan TBD). |
| Phase 1 CRM depth | Prefer durable store + notify; optional PayamGostar lead write | Only if API/access/cost/workload approved — otherwise no CRM write in Phase 1 |

### 2.5.3 Cost signals from management (infrastructure — not development fee)

| Item | Status |
|---|---|
| Development fee | **$0** (management input for this engagement’s development fee) |
| Liara | Minimum estimated budget floor **4,000,000 tomans/month** — subject to selected plan after review |
| Cursor Pro+ | **$60/month** — mark **verify current pricing** before purchase |
| n8n | Use **existing project configuration** (`hamidafghah.app.n8n.cloud`). Specific subscription plan/price **not documented** in project files — do not invent |
| DB / storage / CDN / backup / email / SMS / monitoring | Potential separate infrastructure costs — **prices unknown**; list as TBD, do not invent |

### 2.5.4 Impact on scope / cost / schedule if OPEN items stay open

| OPEN item | Impact if unresolved |
|---|---|
| Final host plan after Liara review | Blocks production/staging provisioning and launch date |
| Approved visual system (not concept-preview) | Blocks UI implementation after structure/model stage |
| Page rewrite vs visual-only matrix | Blocks migration effort and content SOW |
| Official product list + mandatory fields | Blocks product pages and content model freeze |
| apex vs `www` | Blocks canonical/hreflang/redirect map freeze |
| Sales owner / SLA / notify channel | Blocks form acceptance tests |
| Numeric perf budgets + sample URLs | Blocks performance acceptance |
| Analytics tool + retention owners | Blocks analytics/privacy acceptance |
| Monitoring channel + responder | Blocks ops acceptance |
| PayamGostar API approve/deny for Phase 1 leads | Affects Phase 1 integration workload/cost only; portal stays Phase 2 either way |

---

## 3. Confirmed business/design requirements from the boss brief

Source: design brief docx. All items in this section are **BRIEF REQUIREMENT** unless noted.

### 3.1 Project goals
- Redesign trilingual site (English, Arabic, Persian).
- Present Abadis as specialized, knowledge-based, data-driven manufacturer.
- Present products and production capabilities professionally.
- Increase trust of hospitals, customers, and foreign representatives.
- Show economic, hygiene, and environmental effects of products.
- Gradually turn the site into an ordering tool and ongoing customer channel.

### 3.2 Brand / content
- Use provided Abadis story and timeline (۱۳۹۶–۱۴۰۵) as narrative material for About / brand.
- Brand attributes: beautiful/minimal; clean/medical; young/energetic; dignified/trustworthy; knowledge-based; modern/high-tech; impactful; international.
- Stated goals: optimal management of infectious liquid/hospital waste; reduce/control related infections.
- About page needs **full rewrite** (real history, correct دانش‌بنیان timing vs founding, less repetition, professional timeline).
- EN and AR versions need rewriting.
- Content gaps called out: **new factory video**; replace current install videos with **short clean 2D animations** (Serres-like); brief states dislike of current install videos.
- Brief also states: “سایر صفحات از لحاظ محتوایی تغییری نیازی نیست … فقط نیازمند تغییر ظاهری است” — **HUMAN DECISION** needed to reconcile with “structural + content redesign” wording elsewhere in the same brief.

### 3.3 Visual identity (requested direction)
- Medical, Technology, Industrial, Premium; minimal, formal, international.
- **HUMAN DECISION:** Approve final visual system; do **not** treat `concept-preview/` as approved.

### 3.4 Features & campaigns (brief)
- AI chatbot (allowed functions listed in §15).
- 10th-anniversary campaign + simple conceptual game with prizes if high score (§16).
- New “Our Experiences” area with username/password (§17).
- Think-tank / اتاق فکر session before locking site-change decisions (**HUMAN DECISION** gate).

### 3.5 Phase 2 customer dependency (brief)
- Connect website to **PayamGostar CRM via API** (account, orders, invoices, promos, dashboard, purchased tech files, site-order discount) — see §18.

### 3.6 Calculator (brief)
- Upgrade from “simple form” to interactive savings tool — see §14.

### 3.7 Brief-cited current-site problems (treat as BRIEF REQUIREMENT to fix; some corroborated by FACT sample)
- Home lacks impact / clear CTA; old factory “Coming Soon” risk (brief claim; **UNKNOWN** whether still present in latest HTML sample — not specially extracted).
- About page narrative problems (brief).
- Calculator under-uses potential (brief; **FACT:** calculator pages/forms exist).
- Missing H1 on key pages; many missing alts (**FACT** on sampled home/EN/AR and others).
- Title/heading/slider/counter UX issues (brief; partially **FACT** for H1/alt).

---

## 4. Technical requirements from the migration review

Source: technical PDF. Items are **BRIEF REQUIREMENT** (technical).

1. Goal is **not** appearance-only: preserve valuable information and URLs; keep content management simple; **customer requests must not be lost**.
2. Responsibility split: **Nuxt** site; CMS/DB as source of truth; migration tool; **n8n** automation.  
   Flows: `WordPress → Migration Tool → CMS/DB → Nuxt → CDN` and `Website/DB → API/Webhook → n8n → CRM/AI/Notifications`.
3. Exact Nuxt version, CMS, host, and performance criteria must be decided after current-site review (**HUMAN DECISION**; PDF links Nuxt 4.x rendering docs → **INFERENCE** that Nuxt 4.x family is intended).
4. **Data model before migration** (content types, product fields, relations, SEO fields, roles).
5. Migration method: WP REST suitable for pages/media; custom fields & SEO plugin data must be checked separately; testable script; dry-run; old/new IDs; idempotent re-run; count/field compare; backup + rollback.
6. Images, catalogs, files (PDF notes **GLB** as part of migration): preserve originals, alt, captions, product links; CDN/naming; responsive/compression policy.
7. SEO migration: keep URLs where possible; mapping file before launch; Search Console + crawl + sitemap sources; redirect matrix; meta/H1/structure/canonical/OG/alt/internal links/JSON-LD/sitemap/robots/hreflang; no ranking guarantees.
8. Rendering: main content SSR/SSG/ISR hybrid with cache freshness policy; optimize images/fonts; agree speed metrics.
9. Forms: persist first, then notify — `Form → Server Validation → Database/CRM → Automation Queue → n8n → Sales…`; spam limits; UTM; no success UI before durable save; full path test.
10. Periodic monitoring automations (uptime, APIs, failed forms, missing assets, SSL, sitemap, CWV/index anomalies) with owners/thresholds (**HUMAN DECISION** on intervals).
11. AI content: `Verified Data → AI Draft → Validation → Human Approval → Publish` — no invented product specs.
12. Staging (no accidental index), security, backups + restore drill, analytics, privacy, handover/training.
13. Formal acceptance checklist and phased commercial quote (deliverable, duration, cost, owner, acceptance per phase).

---

## 5. Phase 1 scope

### In scope (base Phase 1)

| Item | Label |
|---|---|
| Trilingual public site rebuild (FA/EN/AR) on accepted lean stack | MANAGEMENT DIRECTION + BRIEF |
| Home, About, Calculator, Products as design/build priorities | BRIEF REQUIREMENT |
| Sustainability, Representatives, CSR, News (priority 2) | BRIEF REQUIREMENT |
| Utility: FAQ, Install, Contact, Download center, Jobs | BRIEF REQUIREMENT |
| Articles (SEO) | BRIEF REQUIREMENT |
| About rewrite + timeline from brief materials (Abadis must approve copy) | BRIEF + MANAGEMENT CONFIRMED (content approval) |
| EN/AR content rewrite where required | BRIEF + MANAGEMENT CONFIRMED (languages) |
| Calculator upgrade | BRIEF REQUIREMENT (formulas still OPEN) |
| SEO/a11y fixes cited in brief + evidenced gaps | BRIEF + FACT |
| URL/SEO/media preservation & migration tooling | MANAGEMENT CONFIRMED + BRIEF |
| Durable forms: **store before notify**; n8n notifications | MANAGEMENT CONFIRMED + BRIEF |
| Staging + Abadis staging approval before prod; backup + restore drill; rollback | MANAGEMENT CONFIRMED + BRIEF |
| Role-based access; Abadis-owned domain/hosting/GitHub/service accounts | MANAGEMENT CONFIRMED |
| **60-day** post-launch bug-fix | MANAGEMENT CONFIRMED |
| Analytics + key events; privacy/retention rules (details OPEN) | MANAGEMENT CONFIRMED principle |
| Performance + monitoring with alerts (numeric budgets/channel OPEN) | MANAGEMENT CONFIRMED principle |
| First visible outputs: page structure/content model → homepage + product-page designs | MANAGEMENT CONFIRMED |
| Optional PayamGostar **lead** write only if API/access/cost/workload approved | MANAGEMENT CONFIRMED (conditional) |

### Explicitly out of base Phase 1 (unless separately approved)

| Item | Label |
|---|---|
| PayamGostar customer portal / accounts / orders / invoices / dashboard | MANAGEMENT CONFIRMED — **Phase 2 separate contract** |
| AI chatbot | MANAGEMENT CONFIRMED — out of base Phase 1 |
| 10th-anniversary campaign/game | MANAGEMENT CONFIRMED — out of base Phase 1 |
| “Our Experiences” authenticated area | MANAGEMENT CONFIRMED — out of base Phase 1 |
| Interactive 3D product viewer at launch | MANAGEMENT CONFIRMED — out of base Phase 1 (media migration ≠ 3D viewer) |
| Treating `concept-preview/` as design system | MANAGEMENT CONFIRMED + FACT — forbidden |
| New factory video + 2D install animations (asset production) | BRIEF — producer/budget still OPEN; not assumed in base SOW |
| Full attachment corpus field-level migrate without tooling readiness | RECOMMENDATION — plan in migration phase, not launch-day guess |

---

## 6. Phase 2 scope

**MANAGEMENT CONFIRMED:** Phase 2 is a **separate contract**, not included in the current Phase 1 engagement.

**BRIEF REQUIREMENT** (design brief “فاز 2”, when contracted): create practical customer dependency via **PayamGostar CRM API**:

- Customer accounts  
- Purchase history  
- Direct order placement  
- Order status  
- Invoices / documents  
- Personal discounts / promotions  
- Extra discount for orders placed via site  
- Purchase/consumption dashboard  
- Access to technical files for purchased products  

**Phase 1 preparation only:** keep form/identity data structured for a future connection; do **not** build the portal in Phase 1.

**OPEN for Phase 2 (later):** API credentials, object mapping, environments, discount rules, self-registration policy.  
**UNKNOWN:** Actual PayamGostar API capabilities for this Abadis tenant (do not invent).

---

## 7. Information architecture / page priorities

### Priority 1 — special design (BRIEF REQUIREMENT)
1. Home (صفحه اول)  
2. About (درباره ما)  
3. Calculator (محاسبه‌گر)  
4. Products (محصولات)

### Priority 2 (BRIEF REQUIREMENT)
5. Sustainability (توسعه پایدار)  
6. Representatives (نمایندگان)  
7. CSR / social responsibility  
8. Latest news  

### Utility (BRIEF REQUIREMENT)
- Products, FAQ, Install guide, Contact, Download center, Jobs  

### SEO (BRIEF REQUIREMENT)
- Articles / blog  

### Home building blocks requested (BRIEF REQUIREMENT)
- Language-specific main headline  
- Introduce Abadis as suction / hospital fluid-management solutions manufacturer  
- Slogan  
- Primary CTAs: view products; partnership/agency request; latest news; latest articles  
- Stats: covered treatment centers; active provinces/markets; export countries  
- Credibility: memberships / certificates  
- **Dynamic impact counter:** estimated water saved; washes avoided; cleaning/disinfection time & cost reduction — must be updatable with **transparent, citable formula** (**HUMAN DECISION** for formula)  
- CTAs: consultation; agency request; place order; contact sales/export  
- Open brief question: factory video on home? (**HUMAN DECISION**)  
- Do not sacrifice important information for design aesthetics (BRIEF REQUIREMENT)

### News IA (BRIEF REQUIREMENT)
Separate:
- Company news & events  
- Educational / specialist articles  
- CSR projects  

### EXISTS today (FACT / INFERENCE)
- **FACT:** Language roots `/`, `/en/`, `/arabic/` exist and return 200 in sample.  
- **FACT:** Calculator URLs exist FA (`/محاسبه-گر/`) and EN (`/en/calculator/`).  
- **FACT:** Collaboration opportunities page with large form exists.  
- **INFERENCE:** IA today is Elementor/JetEngine-driven and not a clean headless content model.  
- **UNKNOWN:** Full nav tree and orphan rate site-wide (link checks = 0 this audit).

---

## 8. Content migration requirements

| Requirement | Label |
|---|---|
| Extract pages, posts, media, CPT records from WP with countable reconcile | BRIEF REQUIREMENT |
| Do not assume all product/SEO plugin fields appear in default REST | BRIEF REQUIREMENT |
| Dry-run migration; old→new ID map; idempotent reload; field compare report | BRIEF REQUIREMENT |
| Preserve valuable copy; migration is not “delete and rewrite everything” | BRIEF REQUIREMENT |
| About / EN / AR / calculator UX content: rewrite per brief, not blind copy | BRIEF REQUIREMENT |
| Other pages: brief says visual-only — confirm list with stakeholders | HUMAN DECISION |
| AI may draft only from verified data; human approve before publish | BRIEF REQUIREMENT |
| Random spot-checks do not replace full reconcile | BRIEF REQUIREMENT |

**FACT:** Inventory has 718 URLs and WP totals above; full HTML/content body migration quality is **UNKNOWN** until migration tooling runs.

---

## 9. Product / content data model requirements

### Required model entities (BRIEF REQUIREMENT — tech PDF)
- Product  
- Page  
- Article  
- Category  
- Catalog  
- Downloadable file  
- SEO fields: title, meta description, URL/slug, image alt, canonical  
- User roles: author, reviewer, publisher, admin  
- Relations: product↔category, product↔article, product↔catalog, language variants  

### Suggested product fields (BRIEF REQUIREMENT — tech PDF)
Name, model, specifications, use-case, images, files, publish status.

### Current-state mapping

| Topic | Label | Note |
|---|---|---|
| Public CPT `product` | UNKNOWN / FACT absence in types list | Types list has no `product` |
| JetEngine CPTs present | FACT | `_customers`, `_franchise`, `_downloadcenter`, `_joboffers` |
| Product-like URLs/pages | INFERENCE | e.g. suction bag / canister articles & product section links in sample |
| Authoritative product SKU/spec source | HUMAN DECISION | ERP/MIS/BI mentioned in brand story — not wired in audit |

**RECOMMENDATION:** Define a Product content type in the target CMS even if source is currently pages; map during migration with human validation of each product URL.

**Do not invent** clinical claims or specs not present in verified source data.

---

## 10. SEO + URL preservation requirements

| Requirement | Label |
|---|---|
| Keep current URLs where possible | BRIEF REQUIREMENT |
| Full Old URL → New URL → Action → HTTP status → Test result map before launch | BRIEF REQUIREMENT |
| 301 for moved URLs with relevant replacement; 404 for true removals (not junk homepage redirects) | BRIEF REQUIREMENT |
| Preserve/migrate title, meta, H1/H2 structure, canonical, OG/share meta, alt, internal links, JSON-LD aligned to real content | BRIEF REQUIREMENT |
| Sitemap + robots continuity; avoid redirect chains/loops; find orphans | BRIEF REQUIREMENT |
| Multilingual hreflang / language version links | BRIEF REQUIREMENT |
| Ranking preservation is not guaranteed | BRIEF REQUIREMENT (explicit PDF caveat) |

### Evidence-backed SEO defects to fix (FACT — sample)
- Missing H1 on home FA, EN root, Arabic root, collaboration, calculator, EN contact/calculator.  
- High missing-alt counts on home (69/117) and other samples.  
- Arabic root weak robots/schema/lang.  
- Empty `hreflang` arrays on all 10 sampled pages.  
- EN canonical host uses `www.abadis-med.com` while many FA URLs use apex — **INFERENCE:** host normalization policy needed (**HUMAN DECISION**).

**UNKNOWN:** Site-wide title quality, Search Console coverage, full orphan set (link checks not run).

---

## 11. FA / EN / AR multilingual requirements

| Requirement | Label |
|---|---|
| Ship FA, EN, AR | BRIEF REQUIREMENT |
| Correct language metadata and cross-language linking | BRIEF REQUIREMENT |
| Rewrite EN and AR content quality | BRIEF REQUIREMENT |
| Arabic root currently `lang=fa-IR` | FACT — must be fixed in new site |
| EN/AR largely absent from Yoast sitemaps historically; discovered via HTML | FACT (177 added this audit) |
| Parity of key templates across languages | RECOMMENDATION |
| Which pages must exist in all three languages | HUMAN DECISION |

**Do not claim** multilingual is “fully verified” (**UNKNOWN** beyond inventory + sample defects).

---

## 12. Media / download / GLB requirements

| Requirement | Label |
|---|---|
| Migrate media with alt/caption and product relations | BRIEF REQUIREMENT |
| Download center / catalogs / PDFs are part of migration | BRIEF REQUIREMENT + FACT (`_downloadcenter` total 9; media sitemap 1053; attachments 1727) |
| PDF explicitly includes **GLB** files in migration scope | BRIEF REQUIREMENT |
| GLB/3D found on current public site in this audit | FACT: **not found** |
| New factory video | BRIEF REQUIREMENT (asset) |
| Replace install videos with 2D animations (Serres-like) | BRIEF REQUIREMENT (asset) |
| CDN, naming, responsive sizes, compression | BRIEF REQUIREMENT |
| Delivery criterion: transferred file list, failures, approved diffs | BRIEF REQUIREMENT |

**HUMAN DECISION:** Are GLB/3D viewers required at Phase 1 launch, or only “preserve files if they appear in media library”?  
**RECOMMENDATION:** If GLB appears in WP media library during full extract, migrate binaries even if not linked in HTML sample; viewer UX is a separate decision.

---

## 13. Forms + lead preservation requirements

### EXISTS today (FACT — sample)
- Collaboration form (many fields; Gravity-like `input_*`).  
- FA calculator Gravity Form (`gform_submit`).  
- EN calculator Gravity Form.  
- EN contact Elementor fields.  
- Comment forms on some articles → `wp-comments-post.php`.  
- WhatsApp presence signaled on samples.

### Required (BRIEF REQUIREMENT — tech PDF)
- Persist lead in durable store **before** success UI.  
- Then notify via automation (`n8n` → sales).  
- Server validation, spam protection, rate limits.  
- Capture timestamp, source page, campaign params when allowed.  
- Dedup / retry / error alerts.  
- Owner, SLA, outcome recording.  
- End-to-end test: submit → sales-visible record even if email fails.

**UNKNOWN:** Current form backends (email-only vs DB vs CRM). **Do not claim** CRM routing exists today.  
**HUMAN DECISION:** Which forms are lead-critical (contact, collaboration, export, calculator lead-gate, etc.).

---

## 14. Calculator requirements

### EXISTS (FACT)
- FA and EN calculator URLs and POST forms exist in sample.

### WANTS (BRIEF REQUIREMENT)
- Explain method and assumptions.  
- Cite number sources.  
- Visually compelling results.  
- Compare traditional method vs disposable bag.  
- Share/download report.  
- Better input validation.  
- Interactive charts/animation for water, cost, time, waste reduction.

### PROPOSE (RECOMMENDATION)
- Rebuild as first-class Nuxt interactive tool with server-validated inputs; store optional lead capture per §13.  
- Formula and constants only from Abadis-approved spreadsheet/doc.

### APPROVAL (HUMAN DECISION)
- Exact formula, units, update cadence, owner of numbers.  
- Whether calculator submissions create CRM leads in Phase 1 or Phase 2.

**Do not invent** savings formulas or medical/environmental claims.

---

## 15. AI chatbot requirements

**BRIEF REQUIREMENT — allowed functions only:**
- Product selection guidance  
- FAQ answers  
- Install guidance  
- Provide catalogs / technical files  
- Register callback request  
- Route user to sales or export  

**BRIEF REQUIREMENT / tech PDF alignment:** Bot must not invent product specs; grounded on verified content; human escalation path.

| Topic | Label |
|---|---|
| Vendor vs custom build | HUMAN DECISION |
| Languages supported at launch | HUMAN DECISION |
| Knowledge sources (which CMS fields/PDFs) | HUMAN DECISION |
| Logging / privacy retention for chats | HUMAN DECISION + BRIEF privacy theme |

**UNKNOWN:** Any chatbot on current site (not evidenced).

---

## 16. 10th-anniversary campaign / game requirements

**BRIEF REQUIREMENT:**
- Campaign for 10th year of activity.  
- Simple conceptual game; high score may include prize.

| Topic | Label |
|---|---|
| In Phase 1 contract? | HUMAN DECISION |
| Prize legal/compliance | HUMAN DECISION |
| Timeline aligned to real anniversary date | HUMAN DECISION |
| Analytics events for campaign | RECOMMENDATION |

**UNKNOWN:** Exact anniversary date and prize rules (brief does not specify mechanics beyond “simple conceptual game”).

---

## 17. “Our Experiences” authenticated area requirements

**BRIEF REQUIREMENT:** New section with username/password for audience, covering domains:
- General management  
- Financial management  
- Production management  
- Sales management  
- Legal / regulations  

| Topic | Label |
|---|---|
| Auth method (simple shared users vs per-user vs SSO) | HUMAN DECISION |
| Who receives credentials | HUMAN DECISION |
| Content ownership / update process | HUMAN DECISION |
| Indexing policy (must be noindex) | RECOMMENDATION |
| In Phase 1? | HUMAN DECISION |

**UNKNOWN:** Whether any similar private area exists today.

---

## 18. PayamGostar CRM integration requirements

**BRIEF REQUIREMENT (Phase 2)** — see §6 list.

| Topic | Label |
|---|---|
| API credentials / sandbox | HUMAN DECISION |
| Object mapping (contact, company, deal, order, invoice, file) | HUMAN DECISION + UNKNOWN until API docs reviewed |
| Site-order discount rules | HUMAN DECISION |
| Identity: who can self-register | HUMAN DECISION |
| Phase 1 interim: n8n creates CRM lead only | RECOMMENDATION |

**Do not invent** PayamGostar feature availability.

---

## 19. n8n automation requirements

**BRIEF REQUIREMENT (tech PDF):**
- Form → durable store → n8n → sales notification → follow-up → recorded outcome.  
- Periodic monitoring jobs with alerts.  
- AI content pipeline optional: verified data → draft → human approval.

**FACT:** Project already operates an audit workflow in n8n; that does **not** satisfy production lead/monitoring automations.

**RECOMMENDATION:** Separate production workflows:
1. Lead ingest / CRM sync  
2. Health checks (forms, sitemap, SSL, critical URLs)  
3. Optional content draft assist  

**HUMAN DECISION:** Alert channels (email/SMS/Telegram), on-call owner, thresholds.

---

## 20. Nuxt 4 + WordPress architecture requirements

| Requirement | Label |
|---|---|
| Nuxt as public website layer | BRIEF REQUIREMENT |
| CMS/DB as content source of truth | BRIEF REQUIREMENT |
| Migration tool between WP and CMS/DB | BRIEF REQUIREMENT |
| CDN in front of site/assets | BRIEF REQUIREMENT |
| Headless WordPress as the CMS lean for Phase 1 | **MANAGEMENT DIRECTION** (accepted architecture direction; data model still OPEN) |
| Nuxt **4.x** specifically | INFERENCE from PDF Nuxt 4.x docs + project direction — exact patch version OPEN |
| Liara hosting | **MANAGEMENT DIRECTION** — first option to examine; **final host OPEN** pending cost/location/backup/recovery/access |
| Abadis owns domain, hosting, GitHub, service accounts | **MANAGEMENT CONFIRMED** |
| Role-based access; staging approval before production | **MANAGEMENT CONFIRMED** |
| Three.js / GLB viewer in Nuxt at Phase 1 launch | **MANAGEMENT CONFIRMED** — out of base Phase 1 unless separately approved |

**Accepted lean sketch (not a claim that every detail is locked):**
`WordPress (legacy) → Migration Tool → Headless WP → Nuxt 4 (SSR/ISR) → CDN (host TBD after Liara review)`  
`Nuxt/Forms API → durable DB → n8n → notify sales` (+ optional PayamGostar lead write only if approved)

**Rejected:** Building the production UI from `concept-preview/` without a newly approved design system.

---

## 21. Performance / accessibility requirements

| Requirement | Label |
|---|---|
| Agree sample pages, devices, and speed metrics before acceptance | BRIEF REQUIREMENT |
| Optimize images/fonts; defer non-critical assets; avoid SSR/CSR mismatch bugs | BRIEF REQUIREMENT |
| Fix missing H1 / alt / heading structure called out in brief | BRIEF REQUIREMENT + FACT sample |
| RTL correctness for FA/AR; basic a11y | BRIEF REQUIREMENT (acceptance checklist) |
| Persian typography standards for UI | RECOMMENDATION — follow `docs/persian-typography.md` when implementing FA UI |
| CWV targets (LCP/INP/CLS numbers) | HUMAN DECISION |

**UNKNOWN:** Current CWV on production (not in this audit JSON).

---

## 22. Security / privacy requirements

| Requirement | Label |
|---|---|
| Secrets management, least privilege, dependency updates, input validation | BRIEF REQUIREMENT |
| Staging access control; prevent accidental indexing | BRIEF REQUIREMENT |
| Define collectable data, access, retention for forms/chat/CRM | BRIEF REQUIREMENT |
| Auth for Experiences area | BRIEF REQUIREMENT + HUMAN DECISION on model |
| Current WP security posture “verified” | **UNKNOWN** — do not claim |

---

## 23. Analytics requirements

| Requirement | Label |
|---|---|
| Configure visit analytics, form submit events, needed conversions | BRIEF REQUIREMENT |
| Track campaign/UTM when lawful | BRIEF REQUIREMENT (forms section) |
| Tool choice (e.g. GA4, Matomo, Clarity) | HUMAN DECISION |
| Current analytics setup | UNKNOWN in this audit |

**RECOMMENDATION:** Event list minimum — `page_view`, `cta_click`, `form_submit_success`, `form_submit_error`, `calculator_complete`, `download_file`, `chat_started` (if chatbot ships).

---

## 24. Staging / migration / rollback requirements

| Requirement | Label |
|---|---|
| Isolated staging environment | BRIEF REQUIREMENT |
| Backup before cutover; **tested restore** | BRIEF REQUIREMENT |
| Final delta migration; freeze window; go/no-go owner | BRIEF REQUIREMENT |
| Rollback plan documented and rehearsed | BRIEF REQUIREMENT |
| Immediate post-launch checks: key pages, forms, sitemap, SSL | BRIEF REQUIREMENT |
| Immediate DNS/host rollback criteria | HUMAN DECISION |

**RECOMMENDATION:** Rollback = revert DNS/CDN to last known WP stack + restore DB/media snapshot taken pre-cutover.

---

## 25. Acceptance criteria

Derived from tech PDF checklist + brief priorities. Each row must be demonstrably tested.

| Area | Criterion | Label |
|---|---|---|
| Architecture | Stack versions, data model, CMS, deploy method documented | BRIEF REQUIREMENT |
| Data | Record counts & critical fields reconciled; diffs dispositioned | BRIEF REQUIREMENT |
| URLs/SEO | Mapping complete; status codes; index settings tested; hreflang for FA/EN/AR | BRIEF REQUIREMENT |
| Media/files | Important files & links healthy; failures reported | BRIEF REQUIREMENT |
| Forms | Durable save + sales visibility even if notify fails | BRIEF REQUIREMENT |
| Automation | n8n runs, retries, alerts, human ack tested | BRIEF REQUIREMENT |
| UX quality | Mobile/browsers/RTL/basic a11y/speed on agreed samples | BRIEF REQUIREMENT |
| Security/recovery | Access model, backup, restore drill signed | BRIEF REQUIREMENT |
| Launch | Owner, cutover time, stop criteria, rollback plan | BRIEF REQUIREMENT |
| Support | Bugfix window, response times, service owners | BRIEF REQUIREMENT |
| Phase 1 pages | P1 pages designed/built per approved direction (not concept-preview) | BRIEF REQUIREMENT + HUMAN DECISION on design |
| Calculator | Assumptions visible; validation; comparison; share/report per brief | BRIEF REQUIREMENT |
| Arabic lang | `lang` and content direction correct (fixes today’s `fa-IR` on Arabic root) | FACT defect → must pass |
| Chatbot / campaign / Experiences | Pass only if in-scope for Phase 1 acceptance | HUMAN DECISION |

---

## 26. Decisions status after management responses

### 26A — Closed by management (do not re-ask unless Abadis revises)

1. Phase boundary: **Phase 1 now; Phase 2 separate contract.**  
2. Phase 2 PayamGostar **portal** is **out of Phase 1**.  
3. Base Phase 1 excludes chatbot, Experiences login, anniversary campaign/game, and interactive 3D viewer unless separately approved.  
4. `concept-preview/` is **not** an approved visual reference.  
5. Design approval sequence starts with **page structure/content model**, then **homepage + product-page designs**.  
6. Abadis owns domain, hosting, GitHub, and service accounts; **role-based access**.  
7. Staging required; **Abadis approves** staging before production promotion.  
8. Preserve URLs / SEO / media; Abadis approves content/products before publish.  
9. FA / EN / AR required.  
10. Leads: **durable storage before notification**.  
11. PayamGostar in Phase 1 only if API/access/cost/workload approved; else store + notify.  
12. Launch/rollback/backup/**tested restore** required.  
13. **60-day** post-launch bug-fix.  
14. Analytics/events/privacy and performance/monitoring principles required.  
15. Architecture lean: **headless WordPress** + Nuxt; hosting: examine **Liara first** (final host still conditional).  
16. Development fee for this engagement: **$0** (infrastructure costs separate — §2.5.3).

### 26B — OPEN / PENDING (still required)

Blocking for **full production implementation** (★). Non-blocking for **structure/content-model drafting** marked ○.

1. ★ **Final host plan** after Liara cost/location/backup/recovery/access review (select actual plan; confirm staging/prod).  
2. ★ **Approved visual design system** (think-tank / designer / agency output) — rejection of concept-preview is not itself a design system.  
3. ★ **Content change matrix:** which URLs get full rewrite vs light edit vs visual-only.  
4. ★ **Official product list** (URL/SKU) and mandatory product fields.  
5. ★ **About timeline** approval (including دانش‌بنیان vs founding wording).  
6. ★ **apex vs `www`** canonical policy (FA/EN conflict observed in sample).  
7. ★ **Sales follow-up owner**, expected response time, notification channel, which forms are sales leads.  
8. ★ **Impact-counter** and **calculator** formulas / owners (if those ship in Phase 1).  
9. ○ Search Console access owner for URL mapping.  
10. ○ Exact Nuxt 4.x patch/support pin at project start.  
11. ○ Analytics **tool** choice + conversion event list + retention period/access owner.  
12. ○ Numeric performance budgets + sample URLs/devices.  
13. ○ Monitoring alert channel + on-call responder + thresholds.  
14. ○ Bug-fix **response-time** SLAs inside the 60-day window.  
15. ○ Whether Phase 1 gets **PayamGostar lead API** write (approve/deny with cost/workload).  
16. ○ Asset production (factory video / 2D animations) if Abadis wants them in Phase 1 despite not being base extras.  
17. ○ Privacy statement text for forms/analytics.  

---

## 27. Risks and unknowns

| Risk / unknown | Label | Why it matters |
|---|---|---|
| HTML/SEO audited on 10 pages only | FACT | Site-wide defects under-counted |
| Broken-link audit not run | FACT | Orphans/404s unknown |
| WP items fetch capped (309 vs totals) | FACT | Field-level migrate unproven |
| No public `product` CPT | FACT / INFERENCE | Product model may be messy |
| Arabic language metadata wrong on root | FACT | Trust + SEO harm |
| Form→CRM path unverified | UNKNOWN | Lead loss risk (explicit PDF concern) |
| Plugin lock-in (Elementor/JetEngine) | FACT signals | Headless extraction harder |
| GLB expected by PDF but absent in HTML evidence | BRIEF vs FACT | Scope creep or missed binaries |
| Brief wants redesign depth + “visual only” elsewhere | BRIEF tension | Scope disputes |
| MASTER plan overclaims (Liara/security/multilingual) | Downgraded | Must not drive build |
| Asset-heavy asks (video, 2D, game, chatbot) | BRIEF | Timeline/budget risk |
| Phase 2 CRM dependency | BRIEF | Can derail Phase 1 if conflated |

---

## 28. Implementation phases and dependencies

**RECOMMENDATION** — do not start coding until ★ decisions in §26 are answered.

### Phase A — Spec lock (this document + decisions)
- Dependencies: think-tank, CMS/host/design/phase-boundary decisions.  
- Exit: signed scope + IA + data model outline.

### Phase B — Foundation
- Nuxt app shell, CMS setup, auth patterns, design tokens (approved), i18n routing FA/EN/AR, staging, CI.  
- Dependencies: Phase A.

### Phase C — Migration tooling
- WP extract, ID maps, media copy, dry-runs, reconcile reports.  
- Dependencies: data model; WP access.

### Phase D — Phase 1 templates
- Priority 1–2 + utility templates; calculator; forms→DB→n8n; SEO head tags; RTL.  
- Dependencies: design approval; formulas for calculator/counter if those ship.

### Phase E — Optional extras (not base Phase 1)
- Chatbot, Experiences, anniversary game, interactive 3D viewer — **only if separately approved** (management excluded from base Phase 1).  
- Dependencies: explicit new approval + assets/budget.

### Phase F — Hardening
- Perf/a11y/security/backup restore; monitoring; analytics.  

### Phase G — Launch
- Final delta migrate, cutover, SEO checks, form tests, rollback readiness; then **60-day** bug-fix.  

### Phase H — Phase 2 (separate contract)
- PayamGostar account/order/invoice/dashboard.  
- Dependencies: separate contract + API access + Phase 1 stable.

---

## End-state readiness assessment

### A) READY FOR IMPLEMENTATION

**Not yet — production Nuxt / full Phase 1 build is not authorized.**

**Allowed next work (documentation / design gate only):**
- Draft **page structure + content model** for Abadis review (first visible deliverable, part 1).  
- After Abadis inputs for products/matrix/languages: prepare **homepage + product-page designs** for approval (part 2).  
- Do **not** treat `concept-preview/` as the design source.  
- Do **not** start production coding until §26B ★ design + content blockers for that stage are cleared.

Partially ready inputs that already exist:
- URL inventory (718) and WP REST totals  
- Sample SEO defect list (10 pages)  
- Management Phase 1/2 boundary and extras exclusions  
- Technical acceptance themes from PDF  

### B) BLOCKING OPEN DECISIONS (for full implementation)

1. Final host after Liara review  
2. Approved visual design system (beyond rejecting concept-preview)  
3. Content rewrite vs visual-only matrix  
4. Official product list + fields  
5. About timeline approval  
6. apex vs `www`  
7. Sales owner / SLA / notify channel / lead forms  
8. Impact-counter + calculator formulas if in Phase 1 acceptance  
9. Perf budgets + analytics tool + monitoring ownership (for acceptance)  

### C) NON-BLOCKING UNKNOWNs / later work

- Full site-wide broken-link / orphan census (audit run had **0** link checks)  
- Complete attachment binary integrity report  
- Whether GLB files exist only in media library  
- Current CWV numbers  
- Current analytics/GTM configuration  
- Exact PayamGostar API surface (Phase 2 / optional Phase 1 lead write)  
- Anniversary / chatbot / Experiences (out of base Phase 1 unless revived)  

---

## Appendix — Label reminders for implementers

- **EXISTS (A):** WordPress/Elementor/JetEngine/Yoast site; 718 URLs; CPT totals above; calculator & collaboration forms; Arabic `lang` bug on sample; no GLB in audit text; link checks not completed.  
- **WANTS (B):** Brief Phase 1 redesign priorities; Phase 2 CRM portal (now confirmed as separate contract); tech PDF migration/SEO/forms/n8n/acceptance rigor.  
- **CONFIRMED / DIRECTION (management):** See §2.5 — do not weaken Phase 1/2 boundary or revive base extras without new approval.  
- **PROPOSE (C):** Remaining RECOMMENDATION rows — require approval before build.  
- **OPEN (D):** §26B items.

**Document authority:** If `MASTER-MIGRATION-PLAN.md` conflicts with this specification on factual claims or management decisions, **this specification wins**. If new audit evidence appears, update §2 FACTs and re-evaluate readiness. Related execution docs: `PHASE-1-EXECUTION-PLAN.md`, `ABADIS-AUDIT-SUMMARY-MGMT.md`, `MANAGEMENT-HANDOFF.md`.
