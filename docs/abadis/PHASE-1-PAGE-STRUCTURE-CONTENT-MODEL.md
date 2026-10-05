# Phase 1 — Page Structure & Content Model

**Status: DRAFT — FOR MANAGEMENT REVIEW**

| | |
|---|---|
| **Deliverable** | First visible Phase 1 output (structure + content model) |
| **Date** | 2026-09-26 |
| **Authority** | Does **not** replace `ABADIS-MASTER-SPECIFICATION.md` |
| **Based on** | Existing audit/evidence (`ABADIS-AUDIT.json`, multilingual inventory, Master Spec, Boss responses, migration maps) |
| **Not this document** | Final visual design · production Nuxt code · approved product/company claims · a finished URL-by-URL redirect table |

**Explicit limits**

- Product facts, clinical claims, certifications, statistics, and About timeline remain subject to **Abadis approval**.
- Official SKU/model list is still **OPEN** — this document proposes a **model**, not a finished product catalog.
- `concept-preview/` is **not** an approved visual reference.
- Architecture here is **proposed for review**, not finally approved.

**Next visible deliverable:** Homepage + Product Page **design** (after this structure/model is approved enough to design against).

---

## 1. Proposed Phase 1 information architecture

### 1.1 Primary navigation (header — proposed)

Structural labels (language-neutral intent). Final wording FA/EN/AR needs Abadis copy approval.

| Nav item | Target | Notes |
|---|---|---|
| Products | Products hub → categories → products | Priority 1 |
| Solutions / Applications | Application landing(s) → related products | May start as sections on Products/Home if Abadis prefers fewer top-level items (**OPEN**) |
| Calculator | Calculator tool page | Priority 1 |
| About | About Abadis | Priority 1 |
| Impact | Sustainability + CSR (linked, **not mixed** as one content type) | Priority 2 |
| Representatives | Representatives list + inquiry | Priority 2 |
| Knowledge | Guides / FAQ / educational articles (clear sub-separation) | Utility + SEO |
| News | Company news & events only | Separate from educational articles |
| Downloads | Download center / catalogs / certificates | Utility |
| Contact | Contact + consultation / quotation CTAs | Utility |
| Careers | Jobs listing | FA exists; EN/AR parity **OPEN** |
| Language switcher | FA / EN / AR | Must resolve to **equivalent page** when a variant exists (today switcher often goes to language home only — FACT gap to fix) |

**Footer (proposed modules):** contact channels, key downloads, certifications (verified only), legal/privacy, careers, language links, social if approved.

**Out of primary nav (Phase 1 base):** Experiences login, chatbot entry, anniversary campaign, interactive 3D viewer (management excluded unless separately approved).

### 1.2 Site map (page families)

```
Home
├── Products
│   ├── Product category pages
│   └── Individual product pages (SKU/model — after official list)
├── Solutions / Applications   ← may be hub or product-linked landings
├── Calculator
├── About Abadis
├── Sustainability (impact / SDG-style)
├── CSR (social responsibility projects)   ← separate type from Sustainability & News
├── Representatives
├── Guides & Installation
│   └── Guide articles / install manuals
├── FAQ
├── Downloads / Catalogs / Certificates
├── News (company news & events)
├── Educational articles (specialist / SEO)
├── Customers (logo/reference wall — indexability OPEN)
├── Collaboration / Partnership inquiry
├── Contact / Consultation / Quotation
└── Careers / Jobs
```

### 1.3 Content types that must stay separated

| Type | Purpose | Must not mix with |
|---|---|---|
| **News** | Company announcements, events, exhibitions, awards announcements | Educational how-to / clinical education; CSR project stories as “news” only when truly news |
| **Educational article** | Evergreen specialist/SEO education (e.g. “what is suction bag”) | Breaking company news |
| **CSR** | Social-responsibility projects & community programs | Sustainability metrics pages; news feed |
| **Sustainability / impact** | Environmental / water / infection-control impact narrative | CSR project gallery |
| **Product** | Sellable / specified Abadis products | Educational posts that only *mention* products |
| **Download** | Files (PDF/catalog/certificate/manual) | Product page body text |
| **Guide / FAQ** | How-to, install, end-user help | News |

Brief requirement (Master Spec): News IA must separate company news, educational articles, and CSR.

---

## 2. URL / page mapping logic

### 2.1 Inventory reality (FACT)

| Bucket in audit inventory | Count | Mapping approach |
|---|---:|---|
| URL inventory total | **718** | Classify by family — do **not** dump all URLs here |
| `page` | 25 (FA sitemap/inventory slice) | Core templates — mostly **preserve URL** |
| `post` | 208 (inventory) / WP total posts **221** | Split News vs Educational vs other — **human review** for borderline titles |
| `_customers` | 156 | Customer records — often **archive / low prominence**; SEO indexability **OPEN** |
| `_franchise` | 27 | Map → Representative |
| `_citynmg` | 25 | City/market taxonomy for representatives |
| `_downloadcenter` | 10 | Map → Download |
| `_joboffers` | 10 | Map → Job |
| `post_tag` / `category` / `author` | 63+8+4 | Archive or utility; generally **not** primary nav |
| `lang_discovered` | 176 | Many are assets/feeds/CSS — **filter out** of page map; keep real EN/AR HTML pages |
| `jet-menu` | 3 | Navigation config only — **do not** treat as public content pages |
| Media sitemap images | 1053 | Media migration, not standalone pages |
| WP attachments | 1727 | Preserve file URLs; attachment *pages* often noindex — **REVIEW** |

**Limitation:** Final audit run HTML-crawled **10** pages and completed **0** broken-link checks. Mapping below is inventory + multilingual evidence based, not a proven site-wide link graph.

### 2.2 Classification legend

| Action | Meaning |
|---|---|
| **KEEP** | Preserve public URL path (preferred default) |
| **MAP** | Same content intent; may normalize path later with 301 from old |
| **REDIRECT** | Old URL → replacement (only with approved target) |
| **ARCHIVE** | Keep data / redirects if needed; do not promote in primary IA |
| **DECISION** | Needs Abadis choice before freeze |
| **UNKNOWN** | Evidence insufficient |

### 2.3 Core marketing / utility pages (FA — keep unless Abadis decides otherwise)

Evidence: FA page inventory + multilingual pair table.

| Existing FA URL (examples) | Proposed Phase 1 role | Action |
|---|---|---|
| `/` | Home | KEEP |
| `/درباره-ما/` | About | KEEP (content rewrite — brief) |
| `/محصولات/` | Products hub | KEEP |
| `/محصولات/کیسه-ساکشن/` | Product **category/family** page (today) | KEEP path; confirm whether category vs SKU (**DECISION**) |
| `/محصولات/مخزن/`, `/فیلترها/`, `/اتصالات/`, `/پایه/`, `/ساکشن-تیوب/`, `/سایر-محصولات/` | Product family pages | KEEP |
| `/محاسبه-گر/` | Calculator | KEEP |
| `/توسعه-پایدار/` | Sustainability | KEEP |
| `/مسئولیت-اجتماعی/` | CSR | KEEP (separate type) |
| `/لیست-نمایندگان/` | Representatives hub | KEEP |
| `/راهنمای-نصب/` (+ child guides) | Guides hub | KEEP |
| `/پرسش-های-متداول/` | FAQ | KEEP |
| `/کاتالوگ/` (download center title) | Downloads hub | KEEP path; clarify label Catalog vs Download Center (**DECISION** copy) |
| `/آخرین-اخبار/` | News hub | KEEP |
| `/مقالات/` | Educational articles hub | KEEP |
| `/ارتباط-با-ما/` | Contact | KEEP |
| `/فرصت-های-همکاری/` | Partnership / collaboration inquiry | KEEP |
| `/موقعیت-های-شغلی/` | Careers hub | KEEP |
| `/مشتریان-ما/` | Customers / references | KEEP or ARCHIVE prominence — **DECISION** |
| `/تجارب-ما/` | Experiences (auth area) | **ARCHIVE from Phase 1 nav** (out of base scope); URL disposition **DECISION** |

### 2.4 Product families observed (not a final SKU list)

Observed under `/محصولات/` (FA pages) with EN/AR semantic pairs (multilingual inventory — high confidence for core set):

| FA family path | EN pair (observed) | AR pair (observed) |
|---|---|---|
| `/محصولات/کیسه-ساکشن/` | `/en/products/suction-bag/` | `/arabic/كيس-الشفط/` |
| `/محصولات/مخزن/` | `/en/products/canisters/` | `/arabic/خزانات/` |
| `/محصولات/فیلترها/` | `/en/products/filters/` | `/arabic/الفلتر/` |
| `/محصولات/اتصالات/` | `/en/products/connections/` | `/arabic/الوصلات/` |
| `/محصولات/پایه/` | `/en/products/base-and-holder/` | `/arabic/تثبیت/` |
| `/محصولات/ساکشن-تیوب/` | `/en/suction-tube/` (path **not** under `/products/`) | `/arabic/أنبوب-الشفط/` |
| `/محصولات/سایر-محصولات/` | `/en/products/other-products/` | `/arabic/منتجات-اخری/` |

**DECISION:** Confirm whether these remain **category hubs** only, or whether Phase 1 also publishes **individual model/SKU pages**. Official codes/models = Abadis input (still OPEN).

### 2.5 CPT / JetEngine families

| Source | Proposed target type | Action |
|---|---|---|
| `_franchise` + `_citynmg` | Representative + Market/City | KEEP/MAP public list URLs; verify contact fields |
| `_downloadcenter` | Download | KEEP/MAP; preserve file URLs |
| `_joboffers` | Job | KEEP/MAP; REVIEW active vs closed |
| `_customers` | Customer / logo reference | ARCHIVE or low-SEO listing — **DECISION** |
| `jet-menu` | Nav config | Do not publish as pages |

### 2.6 Posts (news vs education)

| Pattern (INFERENCE from titles/paths — not final tagging) | Proposed type | Action |
|---|---|---|
| Event / exhibition / award / company announcement | News | KEEP URL; tag as News |
| “چیست؟” / standards / clinical education / how-to | Educational article | KEEP URL; tag as Article |
| CSR project storytelling | CSR **or** News | **DECISION** per item |
| Hiring posts that duplicate Jobs CPT | Job-related | Prefer Job CPT; post may REDIRECT/ARCHIVE |

Full post-by-post classification needs Abadis editorial pass (221 WP posts) — **not** completed in this deliverable.

### 2.7 Language URL roots

| Language | Root (observed) | Host note | Action |
|---|---|---|---|
| FA | `https://abadis-med.com/` | apex common | KEEP language root |
| EN | `https://www.abadis-med.com/en/` | **www** often forced | KEEP `/en/` prefix; **apex vs www DECISION** |
| AR | `https://abadis-med.com/arabic/` | apex | KEEP `/arabic/` prefix; fix `lang` metadata |

hreflang: required by Master Spec; **currently empty on samples (FACT)** — implement pairwise links for pages that have approved language variants.

### 2.8 Non-page noise to exclude from IA

From `lang_discovered` and feeds: CSS/JS/plugin assets, `/feed/`, oEmbed, theme files — **not** Phase 1 pages. Preserve hosting of needed static assets; do not list in sitemap as content.

---

## 3. Content model (target CMS — headless WordPress lean)

Shared publishing fields (all publishable types): `status` (draft/review/published), `approval_owner`, `updated_at`, `seo_title`, `seo_description`, `slug`, `canonical`, `og_image`, `hreflang_refs`, `language`.

Roles (from tech requirements): author, reviewer, publisher, admin.

### 3.1 Product

| Field | Required? | Notes |
|---|---|---|
| `name` | Yes | Localized |
| `code_model` | Yes* | *Required once Abadis supplies official list; do not invent |
| `category` | Yes | Relation to Product Category |
| `application` | Recommended | Use-cases / departments (Abadis-approved wording) |
| `description` | Yes | Approved copy only |
| `technical_specs` | Yes* | Structured list; source ERP/MIS/brief — **OPEN source** |
| `capacity_models` | If applicable | Variants/sizes |
| `compatible_accessories` | If applicable | Relations to other Products |
| `images_media` | Yes | Alts required |
| `packaging` | If available | Do not invent |
| `downloads` | Recommended | Relations to Download |
| `certifications_claims` | Only if verified | Never invent CE/claims |
| `related_products` | Recommended | |
| `faq_items` | Optional | Relations or embedded approved Q&A |
| `seo_*` | Yes | |
| `language` + variant links | Yes | |
| `status` / `approval_owner` | Yes | |

**Relations:** Product ↔ Category, Product ↔ Download, Product ↔ Article, Product ↔ Guide, Product ↔ LanguageVariant.

**Source note (FACT):** No public WP `product` CPT today; product UIs are largely **pages**. Migration maps page → Product type with human validation.

### 3.2 Product Category

| Field | Required? |
|---|---|
| `name`, `description`, `hero_media`, `child_products`, `seo_*`, `language`, `status`, `approval_owner` | Yes / as applicable |

### 3.3 About (page type or singleton)

| Field | Required? | Notes |
|---|---|---|
| `overview` | Yes | Rewrite per brief |
| `history_timeline` | Yes | **Abadis must approve** dates (دانش‌بنیان vs founding OPEN) |
| `mission_value` | If approved | |
| `manufacturing_factory` | If approved | Video asset OPEN |
| `capabilities_stats` | Only verified | Covered centers / markets — **OPEN** |
| `certifications_awards` | Only verified | |
| `media` | Recommended | |
| `seo_*`, `language`, `status`, `approval_owner` | Yes | |

### 3.4 Download

| Field | Required? |
|---|---|
| `title` | Yes |
| `type` | Yes (catalog / certificate / install guide / datasheet / other) |
| `related_product_or_category` | Recommended |
| `language` | Yes |
| `version` | Recommended |
| `date` | Recommended |
| `file` | Yes (preserve URL where possible) |
| `validity_status` | Yes (current / superseded) |
| `access_level` | If applicable (public vs gated — gated rare in Phase 1) |
| `seo_*` if landing page | Optional |
| `approval_owner` | Yes |

### 3.5 Guide / FAQ

**Guide**

| Field | Required? |
|---|---|
| `title`, `body`, `related_product_or_category`, `language`, `install_or_use_context`, `supporting_media`, `related_downloads`, `seo_*`, `status`, `approval_owner` | Yes / as applicable |

**FAQ item**

| Field | Required? |
|---|---|
| `question`, `answer`, `related_product_or_category`, `language`, `supporting_media_or_downloads`, `seo_*` (if standalone), `status`, `approval_owner` | Yes / as applicable |

### 3.6 News vs Educational Article vs CSR

| | **News** | **Educational article** | **CSR** |
|---|---|---|---|
| Intent | Time-bound company/event update | Evergreen specialist education / SEO | Social-responsibility project narrative |
| Typical fields | title, dek, body, date, location/event, media, tags, seo, language, status, approval_owner | title, body, topic, related_products, media, seo, language, status, approval_owner | title, body, project_date, partners, media, impact_notes (verified only), seo, language, status, approval_owner |
| Hub | `/آخرین-اخبار/` (FA) + EN/AR news hubs | `/مقالات/` + EN blog/articles | `/مسئولیت-اجتماعی/` (+ items) |
| Listing mix | News hub only | Articles hub only | CSR hub only |

### 3.7 Representative

| Field | Required? | Notes |
|---|---|---|
| `market_country` / city taxonomy | Yes | From `_citynmg` where applicable |
| `company_name` | Yes | |
| `contact_info` | Yes | Phone/email — verify before publish |
| `address` | If available | |
| `website_or_channel` | If verified | |
| `supported_products_or_markets` | Recommended | |
| `language` | Yes | |
| `verification_status` | Yes | unverified / verified by Abadis |
| `approval_owner` | Yes | |

### 3.8 Sustainability / Impact page

| Field | Required? | Notes |
|---|---|---|
| `narrative`, `metrics` | Metrics only with **approved formula/owner** | Impact counter formula still OPEN |
| `related_downloads`, `media`, `seo_*`, `language`, `status`, `approval_owner` | As applicable | Separate from CSR type |

### 3.9 Calculator (tool page + result lead)

| Field | Required? | Notes |
|---|---|---|
| Page: method explanation, assumptions, UI inputs, disclaimers | Yes | Formula **OPEN** |
| Result share/report fields | Per brief | |
| Optional lead capture → Lead Request | If Abadis wants | |

Normalize messy locale duplicates (EN `calculator` + `reservoir-calculator`; AR two calculator-like pages) via **DECISION** + redirects.

### 3.10 Lead / request (durable store — before notify)

Common envelope (all lead types): `created_at`, `language`, `source_page_url`, `source_product_id` (if any), `utm_*` (if allowed), `status` (new/in-progress/closed), `owner`, `notify_channel_result`, `consent_privacy`.

| Lead type | Additional fields (minimum) |
|---|---|
| **Product / price inquiry** | name, organization, role, phone/email, country/city, product/category interest, quantity/need summary, message |
| **Consultation / demo** | name, organization, phone/email, preferred contact time, topic, message |
| **Partnership / representative / export** | organization, contact name, country/market, partnership type, experience summary, phone/email, message (map from collaboration form intent — field labels need Abadis confirmation) |
| **Support / complaint** | name, contact, product/code if known, issue summary, attachments optional |
| **Recruitment** | name, contact, role applied, CV/file, message — or route to Job application object |

**Management rule:** persist first, then notify (n8n). PayamGostar write only if separately approved.

### 3.11 Job

| Field | Required? |
|---|---|
| `title`, `description`, `location`, `employment_type`, `status` (open/closed), `application_lead_type`, `language`, `approval_owner` | Yes / as applicable |

### 3.12 Customer (optional listing)

| Field | Required? | Notes |
|---|---|---|
| `name`, `logo`, `market`, `verification_status`, `indexable` | As applicable | **DECISION** whether public Phase 1 |

---

## 4. Language model (FA / EN / AR)

### 4.1 Principles

1. Ship **three languages** (management + brief).  
2. **Do not create empty translated shells.** A language variant is published only when Abadis-approved copy exists.  
3. One **canonical content record per language**; link variants explicitly (hreflang + in-page switcher to equivalent URL when present).  
4. Today’s site is **three separate WP trees** (FACT) — target headless model should use **linked translations**, not three unmanaged duplicates.  
5. Preserve existing language URL prefixes: FA `/`, EN `/en/`, AR `/arabic/` unless Abadis approves a change (then 301).  
6. Fix Arabic `lang` (sample defect `fa-IR`).  
7. Resolve **apex vs www** before launch (OPEN).

### 4.2 Must exist in all three languages (proposed — pending Abadis confirmation)

Home, About, Products hub, core product **families** listed in §2.4, Calculator (one canonical per language), Contact, Representatives hub, FAQ, key Guides hub, Downloads hub, News hub, Educational articles hub, Sustainability, CSR hub, Collaboration inquiry.

### 4.3 May remain FA-primary / untranslated in Phase 1 (proposed)

- Long-tail educational/news archive posts without EN/AR equivalents  
- Closed job posts  
- Duplicate/odd EN utility pages (`فوتر`, sample pages, etc.) → ARCHIVE  
- Experiences (out of base Phase 1)  
- Customer logo CPT volume if Abadis chooses not to promote  

### 4.4 How variants relate

| Mechanism | Phase 1 rule |
|---|---|
| Editorial pair map | Maintain translation group ID in CMS |
| hreflang | Emit for published variant sets only |
| Language switcher | Prefer equivalent URL; fallback to language home **only** if no variant |
| Sitemaps | Per-language sitemaps including only published URLs |

---

## 5. Navigation & user journeys (structural)

1. **Visitor → product → technical info → download / contact**  
   Home or Products → Category → Product → specs/downloads → Contact or inquiry lead.

2. **Visitor → application / solution → relevant products**  
   Solutions landing (or Home modules) → filtered products → Product → inquiry.

3. **Visitor → calculator → result → consultation**  
   Calculator → assumptions/result → consultation/quotation lead (persist then notify).

4. **Visitor → representative → market / contact**  
   Representatives → market/city → representative detail → contact/partnership lead.

5. **Visitor → guide / FAQ → product / support**  
   Guides/FAQ → related product → download or support lead.

6. **Visitor → About → credibility → contact**  
   About → certifications/timeline (verified) → Contact / collaboration.

Secondary: News list → article; Articles list → educational piece → related product; CSR hub → project; Careers → job → application lead.

---

## 6. Missing management inputs

| Decision / input | Why needed | Owner | Blocking? | Status |
|---|---|---|---|---|
| Official product list (names/codes/models) | Freeze Product records & design scope | Abadis — owner to be named | **Yes** for product design depth | OPEN |
| Product technical field source (ERP/MIS/sheets) | Specs without invention | Abadis — owner to be named | **Yes** for accurate product pages | OPEN |
| Content matrix (rewrite vs visual-only per URL family) | Migration effort & copy plan | Abadis — owner to be named | **Yes** for build estimates | OPEN |
| Confirm category-only vs SKU-level product pages | IA depth & URL map | Abadis — owner to be named | **Yes** for product templates | OPEN |
| Approved visual design direction | Next deliverable (home + product UI) | Abadis — owner to be named | **Yes** for visual design start* | OPEN |
| About timeline / company facts approval | About rewrite | Abadis — owner to be named | **Yes** for About design/content | OPEN |
| Domain apex vs `www` | Canonicals, hreflang, redirects | Abadis — owner to be named | **Yes** before launch; soft for wirestructure | OPEN |
| Calculator formula + assumptions | Calculator page honesty | Abadis — owner to be named | **Yes** if calculator is acceptance gate | OPEN |
| Impact-counter formula (if on Home) | Home metrics module | Abadis — owner to be named | If included on Home | OPEN |
| Which pages **must** be trilingual in Phase 1 | Language scope | Abadis — owner to be named | Soft if §4.2 accepted as default | OPEN |
| Sales owner, SLA, notify channel, which forms are leads | Lead model operations | Abadis — owner to be named | **Yes** before form acceptance | OPEN |
| Collaboration form field meanings (labels) | Map to partnership lead schema | Abadis — owner to be named | For that form only | OPEN |
| Customers CPT public? | IA prominence / SEO | Abadis — owner to be named | No for structure draft | OPEN |
| Experiences URL disposition | Out of base Phase 1 | Abadis — owner to be named | No for structure draft | OPEN |
| Analytics tool + key events | Measurement | Abadis — owner to be named | Later (hardening) | OPEN |
| Performance budgets + sample URLs | Acceptance | Abadis — owner to be named | Later (hardening) | OPEN |
| Final host after Liara review | Staging/prod | Abadis — owner to be named | Before foundation build | OPEN |
| PayamGostar lead API yes/no | Optional CRM write | Abadis — owner to be named | No for structure; yes if CRM write wanted | OPEN |

\*Visual design can begin as **exploratory** sketches only after this structure is directionally accepted; **final** homepage/product UI still needs approved visual direction and product-list clarity.

---

## 7. Relation to next deliverable

| Step | Output | Gate |
|---|---|---|
| **This document** | Page structure + content model | Management review / directional approval |
| **Next** | Homepage + Product page **designs** (not from `concept-preview/`) | Needs: directional OK on IA; product family list confirmed; brand/visual direction; sample approved product facts for one hero product if possible |
| Later | Nuxt + headless WP implementation | Master Spec §26B ★ items |

---

## 8. Approval checkbox (for management)

Please mark:

- [ ] IA / primary nav direction accepted (with notes)  
- [ ] Separation of News / Articles / CSR / Products / Downloads / Guides accepted  
- [ ] Product family list in §2.4 confirmed or corrected  
- [ ] Category-only vs SKU pages decision recorded  
- [ ] Language must-have list (§4.2) accepted or edited  
- [ ] Ready to proceed to **Homepage + Product Page design**  

**Document status remains DRAFT until Abadis records review outcome.**
