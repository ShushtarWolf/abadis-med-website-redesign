# Abadis — Audit ↔ Technical Requirements Reconciliation

**Purpose:** Reconcile existing site-audit evidence with the technical migration PDF and official references.  
**Not:** a final migration plan, architecture change, or implementation brief.  
**Rule:** Evidence first. No invented answers. Current-state facts ≠ future requirements.

**Reconciliation date:** 2026-09-25 (aligned with audit pack date)

---

## 1. Source inventory

### Found and used

| Source | Path | Used as |
|---|---|---|
| Audit README | `docs/abadis/AUDIT-README.md` | Scope, status, human-review list |
| Migration master plan (audit pack) | `docs/abadis/ABADIS-MIGRATION-MASTER-PLAN.md` | Discovery facts, content model notes |
| Architecture notes | `docs/abadis/ARCHITECTURE.md` | Observed stack + known target decisions |
| Technology / plugin audit | `docs/abadis/TECHNOLOGY-PLUGIN-AUDIT.md` | WP/plugins/i18n/forms/analytics facts |
| Content migration map | `docs/abadis/CONTENT-MIGRATION-MAP.csv` | CPT/type totals and actions |
| URL migration map | `docs/abadis/URL-MIGRATION-MAP.csv` | ~542 URL rows; actions PRESERVE/REVIEW |
| SEO audit (sample) | `docs/abadis/SEO-AUDIT.csv` | FA/EN/AR roots + sample pages |
| Media inventory | `docs/abadis/MEDIA-INVENTORY.csv` | Upload URL inventory (~1128 rows) |
| Machine evidence pack | `docs/abadis/ABADIS-AUDIT.json` | Crawl samples, links, schema, hreflang empty |
| Risks / human review | `docs/abadis/MIGRATION-RISKS.md`, `HUMAN-REVIEW-REQUIRED.md` | Gaps already flagged |
| Open questions tracker | `docs/abadis/ABADIS-OPEN-QUESTIONS.md` | Decision backlog + known decisions |
| Technical migration PDF | `docs/abadis/references/Abadis_WordPress_to_Nuxt_Migration_Technical_Review_FA.pdf` | Requirements to reconcile |
| Site design brief | `docs/abadis/references/Abadis_Website_Design_Brief_Editable.docx` | Business/design/content intents |
| Brand book PDF | `docs/abadis/references/مخازن طبی آبادیس.pdf` | Confirmed present (6 pages); **no extractable text** (image-based) |
| Logo asset | `docs/abadis/references/logo - Copy22new.ai` | Confirmed present; `file` reports PDF 1.6 (Illustrator/PDF wrapper) |
| Live evidence samples | `audit-raw/live/` (robots, REST headers/bodies, HTML) | Corroboration of REST/sitemap facts |

### Found but not treated as authoritative design

| Source | Note |
|---|---|
| `concept-preview/` | **REJECTED CONCEPT — VISUAL REFERENCE ONLY** (AUDIT-README) |
| `ABADIS_AUDIT_AND_MIGRATION_PLAN.md` (repo root) | Earlier plan; not used as primary evidence pack |

### Not available / not readable as text

| Gap | Impact |
|---|---|
| Brand book text/OCR | Visual identity rules not machine-readable from this pass |
| Search Console export | Not in repo |
| Authenticated JetEngine/ACF field schema | Public REST shows empty `acf: []` on samples |
| Full EN/AR URL inventory | Only language roots + a few EN links in HTML samples; not in Yoast sitemaps |

---

## 2. Current site facts

Facts below are from the 2026-09-25 audit pack unless noted. Classification follows the audit convention.

### URLs and URL structures

- Live site: `https://abadis-med.com/` (FACT).
- Yoast sitemap index: `https://abadis-med.com/sitemap_index.xml`; robots allow all + sitemap pointer (FACT).
- ~539 locs across 11 child sitemaps (post, page, jet-menu, CPTs, taxonomies, author) (FACT).
- URL map has **542** rows; languages in map: **fa 539 / en 2 / ar 1** (FACT of inventory coverage, not of all live pages).
- Default migration stance in maps: **PRESERVE** or **REVIEW**; no auto-DELETE (FACT of local maps).
- Persian product paths observed in navigation/content (e.g. `/محصولات/...`); English product paths under `/en/products/...` appear in EN homepage HTML (FACT of samples). EN/AR product URLs are **not** in Yoast child sitemaps (FACT).

### Languages

- Roots live and HTTP 200: `/` (fa), `/en/` (en), `/arabic/` (ar) (FACT).
- Yoast child sitemaps contain **0** `/en/` or `/arabic/` locs (FACT).
- Sampled FA/EN/AR homepages: **no `hreflang`** (FACT).
- Arabic homepage `html lang="fa-IR"` (incorrect for AR) (FACT).
- Multilingual plugin (WPML/Polylang/etc.): **UNKNOWN** from public namespaces.

### WordPress / CMS

- WordPress with public REST (`wp/v2`, `link: api.w.org`) (FACT).
- Elementor + Elementor Pro namespaces; Elementor templates on samples (FACT).
- JetEngine CPTs: `_customers`, `_franchise`, `_downloadcenter`, `_joboffers`; taxonomy `_citynmg` (FACT).
- JetMenu + `jet-menu` type / sitemap (FACT).
- Yoast SEO (`yoast_head_json`, sitemap XSL) (FACT).
- UIkit / BDThemes Element Pack class patterns on HTML (FACT).
- Jet Reviews API namespace present; business use UNKNOWN (FACT namespace / UNKNOWN usage).

### Content types (REST totals, FACT 2026-09-25)

| Type | Approx. total |
|---|---:|
| pages | 26 |
| posts | 221 |
| media | 1727 |
| `_customers` | 155 |
| `_franchise` | 26 |
| `_downloadcenter` | 9 |
| `_joboffers` | 9 |
| `_citynmg` | 31 |
| categories | 8 |
| tags | 76 |

### Products

- No dedicated public `product` CPT in content map (FACT of types observed).
- Master plan **infers** products are primarily **pages** under `/محصولات/...` (and EN nav paths) — INFERENCE pending field export.
- Product categories appear in IA (suction bag, filters, canisters, connections, etc.) from HTML samples (FACT of nav labels).

### Posts / pages

- 26 pages, 221 posts (FACT).
- News/articles and company pages exist; brief confirms base page set is largely present (brief claim; aligns with sitemap page/post counts).

### Media / downloads

- Large media library (1727) (FACT).
- Download center CPT `_downloadcenter` (~9–10 public URLs) (FACT).
- Media inventory seeded from sitemap images + uploads URLs; preserve-upload-URL stance in audit (FACT/RECOMMENDATION).

### Forms / integrations

- Homepages: WhatsApp present; no `<form>` on those three samples (FACT).
- SEO sample: form signals on `/فرصت-های-همکاری/` and `/محاسبه-گر/` (FACT of sample crawl).
- CRM / email destinations / Elementor form backends: **UNKNOWN** from public HTML.
- Analytics (GTM/GA/Clarity): **not** detected in sampled homepage HTML (FACT samples only).

### SEO metadata / schema / canonicals

- FA/EN samples: WebSite / WebPage / BreadcrumbList / ImageObject schema present; AR sample weak/absent (FACT).
- Sampled key pages: **H1 count 0** on home, calculator, careers samples (FACT) — matches brief SEO critique.
- Many images missing `alt` on samples (FACT).
- EN sample canonical host inconsistency: **www** vs non-www used elsewhere (FACT / risk R11).
- Attachment pages often noindex (noted in content map) (FACT).

### Redirects

- Full historical redirect inventory: **NOT FOUND** in audit pack.
- EN language root www vs non-www both observed (FACT); canonical host decision still open in human-review list.

### Internal links

- Dense nav/footer links on FA/EN/AR samples (FACT in `ABADIS-AUDIT.json`).
- Orphan/redirect-chain audit: incomplete (smoke crawl / partial URL map).

### Plugins / CPTs

See Technology audit: WP, Yoast, Elementor(+Pro), JetEngine, JetMenu, Jet Reviews API, UIkit/Element Pack patterns (FACT).

### Performance

- No agreed CWV budgets in audit (NOT FOUND as measured targets).
- Local experimental GLBs: oversized source vs web-sized (`AMR_4894-web.glb`) (FACT local files; not live-site CWV proof).
- Intermittent TLS/HTTP2 failures during auditor crawl (FACT auditor path).

### Security / hosting / infrastructure

- Public WP admin not audited as a penetration test (NOT in scope).
- Current production host provider for WordPress: **not named** in audit evidence (UNKNOWN).
- Known project decision (not live-site fact): Nuxt on **Liara**; WP may remain on current host initially (`ARCHITECTURE.md`).

### Other migration-relevant

- `concept-preview/` exists and is **rejected** as design direction (FACT process).
- Calculator page exists and is strategically important per brief (FACT URL + brief).
- Brief Phase 2: Payamgostar CRM portal — **future requirement**, not current-site fact.

---

## 3. Requirement-to-audit reconciliation

Mapped from technical migration PDF sections + open-question IDs. Statuses: `CONFIRMED` | `PARTIALLY CONFIRMED` | `NOT FOUND` | `CONFLICT` | `NEEDS DECISION`.

| ID | Requirement / Question | Audit Evidence | Status | Conflict / Gap | Can Be Answered From Audit? | Needs Abadis Decision? |
|---|---|---|---|---|---|---|
| PDF-§1 / N3 | Before start: per-workstream outputs, test method, cost, time, owner | No SOW table in audit | NOT FOUND | Gap: commercial SOW | No | Yes (approve after tech draft) |
| PDF-§2 / C1 | Choose CMS (headless WP / other / custom) | Live CMS is WordPress; project decision: keep WP + Nuxt front | CONFIRMED (decision) | PDF deferred choice; project already decided | Yes (decision recorded) | No (already decided) |
| PDF-§2 / N1 | Register exact Nuxt version | Project decision: Nuxt 4 | CONFIRMED (decision) | — | Yes (decision) | No |
| PDF-§2 / H1 | Final host | Project decision: Liara (Nuxt); WP host UNKNOWN | PARTIALLY CONFIRMED | WP production host still unknown | Partial | Yes for WP host retention |
| PDF-§2 | Performance criteria after site review | No agreed CWV targets | NOT FOUND | — | No | Yes (with tech) |
| PDF-§3 / C2 | Data model: types, product fields, relations, SEO fields, roles | Types/CPTs known; product = pages (inference); meta schema missing; roles not audited | PARTIALLY CONFIRMED | Product modeling vs pages storage | Partial only | Yes (confirm model) |
| PDF-§3 product fields | name, model, specs, use, images, files, publish status | Public REST incomplete for meta (`acf: []`) | NOT FOUND (field schema) | Cannot map fields yet | No | Yes + tech export |
| PDF-§3 / L1 | Language-version relationships | Three roots exist; no hreflang; plugin UNKNOWN; EN/AR not in sitemaps | PARTIALLY CONFIRMED | Pairing rules missing | No (structure only) | Yes |
| PDF-§4 / C3 | Don’t assume products/custom fields/SEO plugin data in default REST | Pages/media REST OK; `yoast_head_json` present; CPT lists work; custom fields empty publicly | PARTIALLY CONFIRMED | Confirms PDF warning | **Yes — partial answer** | Auth export still needed |
| PDF-§4 migration controls | Dry-run, ID map, idempotent re-run, field compare, backup/rollback | Requirements only; not implemented in audit | NOT FOUND (as executed migration) | — | No | Tech owns design |
| PDF-§5 / H2 | Preserve files/alt/captions/product links; define storage/CDN/naming | Uploads URLs inventoried; preserve recommended; CDN/naming policy absent | PARTIALLY CONFIRMED | Policy open | Partial (current paths) | Yes (policy) |
| PDF-§6 SEO URL preserve + mapping file | Prefer keep URLs; mapping for changes | URL-MIGRATION-MAP exists (~542); mostly PRESERVE/REVIEW; EN/AR incomplete | PARTIALLY CONFIRMED | Map incomplete for locales | Partial | Yes for REVIEW rows |
| PDF-§6 Search Console as map source / S1 | Use GSC if available | No GSC export in repo | NOT FOUND | — | No | **Yes** |
| PDF-§6 redirects 301/404/410 rules | Correct status by case | No full redirect matrix | NOT FOUND | — | No | Joint when URLs change |
| PDF-§6 SEO controls | title, meta, H1, canonical, robots, OG, alt, internal links, schema, sitemap, robots.txt, hreflang | Sampled: gaps on H1/alt/hreflang/AR SEO; robots/sitemap exist; schema partial | PARTIALLY CONFIRMED | Debt to fix, not “preserve broken” | Partial | Yes for indexability policies |
| PDF-§6 post-launch monitoring | Traffic/index watch | Not configured in audit | NOT FOUND | — | No | Yes |
| PDF-§7 HTML-first content + SSR/SSG/cache | Requirement for new front | Current site is WP/Elementor HTML (exists); Nuxt rendering not live | PARTIALLY CONFIRMED | Future architecture | N/A as live Nuxt | Tech |
| PDF-§7 / N2 | Agree speed criteria, sample pages, devices, conditions | Not agreed | NOT FOUND | — | No | **Yes** |
| PDF-§8 forms durable store then notify | Lead must not be lost if email/n8n fails | Form destinations UNKNOWN | NOT FOUND | — | No | **Yes** (ops) |
| PDF-§8 / F1 | Follow-up owner, SLA, call outcome recording | Not in audit | NOT FOUND | — | No | **Yes** |
| PDF-§9 / F2–F3 | Monitoring interval, thresholds, alert channel/owners | Not defined | NOT FOUND | — | No | **Yes** |
| PDF-§10 / F4 | AI drafts from verified data; human approver | Brief wants AI chatbot (future); no approver named | NOT FOUND | — | No | **Yes** |
| PDF-§11 privacy / B3 | Collectable data, access, retention | Not documented | NOT FOUND | — | No | **Yes** |
| PDF-§11 analytics / B4 | Required conversions/events | Tags not seen on homepage samples | NOT FOUND | — | No | **Yes** |
| PDF-§11–12 / O1–O2 / B5–B6 | Backup/restore; training; support; go-live owners | Rollback *idea* in docs; no signed policy | NOT FOUND | — | No | **Yes** |
| PDF-§13 / B1–B2 | Phase deliverables, cost, OOS, recurring costs | Not present | NOT FOUND | — | No | Yes (approve) |
| Known | n8n as complementary automation | Project decision + PDF allows n8n with controls | CONFIRMED (decision) | Migration script still preferred by PDF for complex one-shot | Yes | No |
| Brief | Trilingual redesign FA/EN/AR | Roots exist; EN/AR SEO discovery weak | PARTIALLY CONFIRMED | Quality gap | Partial | Yes on content rewrite scope |
| Brief | Preserve most page *content*, redesign UX | Aligns with URL PRESERVE stance | PARTIALLY CONFIRMED | About/home rewrite called out in brief | — | Yes on which pages rewrite |
| Brief Phase 2 | Payamgostar CRM portal | Not on live site | NOT FOUND (current) | Future scope vs Phase 1 | No | Yes (phase boundary) |

---

## 4. Conflicts

Only **genuine** conflicts (not “improvements the new site should make”).

### Conflict 1 — Canonical host (www vs non-www)

#### Investigation (2026-09-25) — evidence

Live HTTP first-hop probes + audit HTML/sitemaps (`audit-raw/live/*`, FA/EN Yoast sitemaps, `ABADIS-AUDIT.json`).

| Question | Finding | Evidence |
|---|---|---|
| **1. FA preferred / canonical host** | **`abadis-med.com` (non-www)** | Canonical `https://abadis-med.com/` on FA home; product canonical `https://abadis-med.com/محصولات/کیسه-ساکشن/`; `https://abadis-med.com/` → **200** (no redirect) |
| **2. EN preferred / canonical host** | **`www.abadis-med.com`** | Canonical `https://www.abadis-med.com/en/`; product canonical `https://www.abadis-med.com/en/products/suction-bag/`; `https://www.abadis-med.com/en/` → **200** |
| **3. AR preferred / canonical host** | **`abadis-med.com` (non-www)** | Canonical `https://abadis-med.com/arabic/`; product canonical under non-www; `https://abadis-med.com/arabic/` → **200** |
| **4. www ↔ non-www direction** | **Split by locale path** — not one global rule | See redirect table below |
| **5. Redirect status** | **301** (`X-Redirect-By: WordPress`); **not** 308 in samples | Live response headers 2026-09-25 |
| **6. Canonical vs preferred host** | **Consistent within each locale** | FA/AR canonicals = non-www; EN canonicals = www (homes + suction-bag product samples) |
| **7. Sitemap hostnames** | FA sitemap locs = **non-www**; EN sitemap locs = **www** | `https://abadis-med.com/sitemap_index.xml` / `page-sitemap.xml`; `https://www.abadis-med.com/en/sitemap_index.xml` / `page-sitemap.xml`. Apex `robots.txt` (both `abadis-med.com` and `www.abadis-med.com`) points Sitemap → `https://abadis-med.com/sitemap_index.xml` (FA only). |
| **8. Internal link mix** | **Yes, lightly on FA; EN/AR internally clean** | FA home HTML: ~169 `abadis-med.com` hrefs vs **4** `www.abadis-med.com` (language-switcher links to `www…/en/` and incorrectly `www…/arabic/`). EN home/product: **all** `www`. AR home/product: **all** non-www. |
| **9. Real conflict vs audit-only?** | **Real migration/SEO conflict** (locale-split preferred host), **not** a false alarm | Redirects + canonicals + sitemaps agree per locale; the conflict is **cross-locale host policy**, not measurement noise |

**Redirect matrix (FACT, live 2026-09-25):**

| Request | Status | Location / result |
|---|---|---|
| `https://www.abadis-med.com/` | **301** | `https://abadis-med.com/` |
| `https://abadis-med.com/` | **200** | (stays non-www) |
| `http://abadis-med.com/` / `http://www.abadis-med.com/` | **301** | `https://abadis-med.com/` |
| `https://abadis-med.com/en/` (+ EN deep paths sampled) | **301** | `https://www.abadis-med.com/en/…` |
| `https://www.abadis-med.com/en/` | **200** | (stays www) |
| `https://www.abadis-med.com/arabic/` (+ AR deep path sampled) | **301** | `https://abadis-med.com/arabic/…` |
| `https://abadis-med.com/arabic/` | **200** | (stays non-www) |
| `https://www.abadis-med.com/محصولات/کیسه-ساکشن/` | **301** | `https://abadis-med.com/محصولات/کیسه-ساکشن/` |

#### Conclusion

- **Current state:** The site intentionally uses **non-www for FA and AR** and **www for EN**. Within each locale, 301s and canonical tags align with that preference. FA Yoast sitemaps/robots use non-www; EN Yoast sitemaps use www.
- **Required/planned (PDF §6 / human-review):** A coherent host policy for migration (often framed as “one sitewide canonical host”).
- **Why it still conflicts:** Preferring different hosts by language is a **real SEO/ops split** (two apex identities, mixed switcher links, separate sitemap hostnames). It is **not** merely an audit inconsistency. Unifying to a single host later would need locale-aware 301s; keeping the split is also a valid decision but must be documented and preserved in Nuxt/Liara.
- **Decision needed:** Abadis + tech — either (A) keep FA/AR=non-www and EN=www and encode that in the migration URL map, or (B) converge all locales to one host with reciprocal 301s and sitemap/canonical rewrites. Do not “fix” by guessing; current live behavior is the baseline to preserve or deliberately change.

### Conflict 2 — Arabic language metadata vs Arabic site

- **Current:** `/arabic/` content is Arabic but `html lang="fa-IR"`; weak/missing Yoast robots/schema on sample (FACT).
- **Required/planned:** Correct language signals + hreflang for multilingual site (PDF §6; brief trilingual goal).
- **Why it conflicts:** Shipping “preserve as-is” for AR metadata would preserve incorrect language identity.
- **Decision needed:** Treat AR SEO metadata as **must-fix at migration**, not blind preserve; confirm AR content ownership/QA.

### Conflict 3 — Product storage model vs PDF data-model expectation

- **Current:** No product CPT in REST types; products inferred as **pages** (+ Elementor); JetEngine used for other CPTs (FACT + INFERENCE).
- **Required/planned:** PDF §3 expects explicit product type with fields, relations to category/article/catalog/language versions.
- **Why it conflicts:** “Preserve pages” vs “model products” are different migration shapes; choosing wrong one breaks editors or SEO URLs.
- **Decision needed:** Keep products as WP pages with meta **or** introduce product CPT while preserving public URLs (301/same path). Joint Abadis + tech.

### Conflict 4 — Known stack decisions vs PDF “decide after audit” wording

- **Current/planned decisions:** WordPress CMS + Nuxt 4 front + Liara + n8n (`ABADIS-OPEN-QUESTIONS` / `ARCHITECTURE.md`).
- **PDF wording:** Final CMS/host/performance criteria after reviewing current site (§2).
- **Why it conflicts:** Soft process conflict only if someone re-opens CMS/host choice; evidence supports WP+Nuxt path, but WP **host** and **performance criteria** remain open.
- **Decision needed:** Confirm decisions stay locked for CMS/Nuxt/Liara(Nuxt); separately decide WP hosting location and CWV acceptance targets.

### Conflict 5 — Design brief vs rejected concept vs unread brand book

- **Current:** `concept-preview/` rejected; brief asks Medical/Tech/Industrial/Premium, green-white fit claimed; brand book PDF present but **not text-extractable** this pass.
- **Required:** Approved visual system before Nuxt UI build (AUDIT-README / HUMAN-REVIEW).
- **Why it conflicts:** Three design sources are not reconciled; implementing any one risks wrong brand.
- **Decision needed:** Abadis approve official visual system from brand book + brief (not concept-preview).

### Not listed as conflicts

- Missing H1/alt, thin homepage, calculator UX, EN/AR sitemap gaps → **defects / debts** to fix, not conflicts between requirement docs.
- Brief Phase 2 CRM portal → **future scope**, not a conflict with PDF Phase-1 technical controls.

---

## 5. Questions already answered

From `ABADIS-OPEN-QUESTIONS.md`, only items with **sufficient audit evidence** (or already recorded project decisions). No invented fills.

| Question ID | Evidence | Proposed answer |
|---|---|---|
| **C1** | Live WP stack (FACT); `ABADIS-OPEN-QUESTIONS` / `ARCHITECTURE.md` | **Already decided:** WordPress remains CMS; Nuxt 4 is display layer. |
| **H1** | `ABADIS-OPEN-QUESTIONS` / `ARCHITECTURE.md` | **Already decided:** Nuxt hosting on Liara. *(WP production host still UNKNOWN — not answered.)* |
| **N1** | `ABADIS-OPEN-QUESTIONS` / master plan target | **Already decided:** Nuxt 4. |
| **C3** | TECHNOLOGY-PLUGIN-AUDIT; CONTENT map; REST samples (`acf: []`); `yoast_head_json` on REST; no product CPT | **Partial answer:** Default public REST is **enough** for pages, posts, media lists, CPT listings, and much Yoast head JSON — and **not enough** for JetEngine/ACF product/custom field payloads (empty in public samples). Products are not exposed as a dedicated product REST type. **Remaining:** authenticated meta schema export. |

**Not marked answered (insufficient evidence):** B1–B6, C2, S1, L1, F1–F4, H2 (policy), N2–N3, O1–O2.

**Related non-ID decision:** n8n complementary automation — already recorded in open-questions file; PDF permits n8n if migration controls are met.

---

## 6. Questions still requiring a human/business decision

### A. Abadis / business decision

- **B3** Privacy: collectable data, access, retention  
- **B4** Required analytics conversions / events  
- **F1** Form follow-up owner, response time, outcome logging  
- **F4** Human approver for AI-generated product/content claims  
- **S1** Search Console access / export availability  
- Canonical host (**www vs non-www**)  
- Indexability of `_customers` / `_franchise` / `_citynmg` archives  
- Which `_joboffers` are still active  
- Design system approval (brand book + brief; not concept-preview)  
- Phase 1 vs Phase 2 boundary (Payamgostar portal, chatbot, gated “experiences” area, 10th-anniversary game)

### B. Technical team decision

- **N3 / B1–B2** Draft phase SOW: deliverables, tests, cost, time, owners, OOS, recurring costs (Abadis approves)  
- Migration tool choice (testable Python/TS script vs n8n) meeting PDF §4 controls  
- Authenticated export of JetEngine/Elementor-only fields  
- Staging/`noindex` strategy; backup/restore test design (**O1** proposal)  
- Full EN/AR crawl + hreflang pair discovery method  

### C. Joint Abadis + technical decision

- **C2 / L1 / Conflict 3** Final content model (especially products) + language pairing rules  
- **H2** Media storage/CDN/naming policy while preserving upload URLs at launch  
- **N2** Performance acceptance: metrics, sample URLs, devices, conditions  
- **F2–F3** Monitoring intervals, thresholds, alert channels, owners  
- **B5–B6 / O2** Support window, go-live owner, stop criteria, rollback, training/handoff  
- WP remains on current host vs move with Nuxt to Liara  
- Calculator formulas/claims legal review (brief + medical risk)

---

## 7. Migration requirements

Things that **MUST be preserved** (or explicitly remapped with tested redirects) based on audit + technical PDF. Future redesign may change presentation; it must not silently drop these.

1. **Indexed / sitemap URLs** — default **PRESERVE**; no silent DELETE (PDF §6; URL map policy).  
2. **URL structures** — keep FA root `/`, EN `/en/`, AR `/arabic/` unless mapped 301s exist (FACT IA + PDF).  
3. **Redirect discipline** — equivalent content → 301; removed with no replacement → 404/410; never soft-404 to homepage (PDF §6).  
4. **SEO metadata** — titles, meta descriptions, robots, social meta where they exist in Yoast/REST; improve H1/alt/AR lang without discarding valuable titles (PDF §6 + audit gaps).  
5. **Schema** — recreate truthful WebSite/WebPage/BreadcrumbList/ImageObject; do not invent Product/Organization until verified (master plan).  
6. **Canonical URLs** — emit one chosen host; fix www inconsistency (PDF §6 + Conflict 1).  
7. **Multilingual relationships** — implement hreflang only for **verified** FA↔EN↔AR pairs; inventory EN/AR beyond roots (PDF §6; audit gap).  
8. **Images / files / downloads** — preserve `/wp-content/uploads/...` and download-center public URLs; keep alt/caption/product linkage when present (PDF §5).  
9. **Internal links** — migrate meaningful nav/footer/in-content links; report broken links (PDF §6).  
10. **WordPress content** — pages, posts, CPT records, media as system of record under decided CMS (C1).  
11. **Custom post types** — `_downloadcenter`, `_joboffers`, `_customers`, `_franchise`, `_citynmg` data must be accounted for (even if some become noindex later) (FACT).  
12. **Custom fields** — must be exported before product/page rebuild; do not assume public REST completeness (PDF §4; C3).  
13. **Forms / lead paths** — every contact/quote/job/download/WhatsApp path must work at cutover; durable store before notify (PDF §8).  
14. **Analytics** — reinstall agreed tags/events (B4); absence on samples ≠ proof none exist elsewhere.  
15. **Search visibility tooling** — sitemap coverage for **all** public locales; robots.txt; Search Console connection post-launch (PDF §6).  
16. **Editorial SEO source** — Yoast fields usable as CMS metadata input to Nuxt (tech audit).  
17. **Calculator & certification/trust pages** — preserve URLs and verifiable claims; formulas need human/legal confirmation (brief + risks).

---

## 8. Missing audit evidence

Blockers / near-blockers before a **final** migration plan:

1. **Complete EN/AR URL inventory** (crawl + GSC) — currently almost absent from sitemaps/maps.  
2. **Search Console** indexed-URL / query / 404 export (**S1**).  
3. **Authenticated JetEngine / Elementor field schema** for products and key pages (**C3 remainder / C2**).  
4. **Form inventory** on contact, jobs, downloads, calculator — endpoints, CRM, email, spam controls (**F1**).  
5. **Analytics/tag** confirmation beyond homepage samples (**B4**).  
6. **Full redirect / host canonical** map (www policy).  
7. **hreflang / translation pairing** table (plugin mechanism UNKNOWN).  
8. **Measured performance baseline** (CWV) on agreed sample URLs (**N2**).  
9. **Brand book readable rules** (OCR/design review) + approved UI direction.  
10. **WP production hosting** details (provider, TLS, backup current state) for cutover/rollback.  
11. **Active vs archived** jobs/customers/franchise SEO policy.  
12. **Download file** completeness (PDF/catalog/cert) and any gating.  
13. Broader-than-smoke **internal link / orphan** crawl (n8n full run).  
14. **Organization/Product/Article** schema presence on non-home templates.

---

## 9. Recommended next investigation

**Single most important next step:**  
Produce a **complete multilingual URL + translation-pair inventory** (full crawl of `/`, `/en/`, `/arabic/` + Search Console export if Abadis can provide it), then merge into `URL-MIGRATION-MAP.csv`.

**Why this first:** EN/AR are live but missing from Yoast sitemaps; without that inventory, SEO preservation (PDF §6), hreflang (L1), and any final migration plan are incomplete by construction. Field-schema export is the close second, but URL discovery unblocks redirect/SEO acceptance criteria for all locales.
