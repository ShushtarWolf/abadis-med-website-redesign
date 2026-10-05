# Phase 1 — Homepage & Product Page Design Specification

**Status: DRAFT — FOR MANAGEMENT / DESIGN REVIEW**  
**Date:** 2026-09-26  
**Type:** Design specification only — **no mockups, no Nuxt, no components coded**

| | |
|---|---|
| **Depends on** | `PHASE-1-PAGE-STRUCTURE-CONTENT-MODEL.md`, `ABADIS-MASTER-SPECIFICATION.md`, design brief, brand materials |
| **Does not replace** | Master Specification |
| **Forbidden reference** | `concept-preview/` — **rejected**; do not imitate its layout, palette, motion, or composition |

### How to read labels in this document

| Label | Meaning |
|---|---|
| **REQUIREMENT** | From brief, Master Spec, or management decisions — must be respected |
| **DESIGN DECISION** | Proposal for the first visual pass — open to designer/management choice |
| **CONTENT GATE** | Layout may reserve space, but copy/numbers/claims cannot ship without Abadis approval |
| **OUT OF BASE PHASE 1** | Explicitly excluded unless separately approved (e.g. interactive 3D viewer) |

**Do not invent** product specifications, certifications, statistics, medical claims, impact formulas, or company facts. Where the brief suggests metrics or counters, the design shows **structure**; values remain placeholders until approved.

---

## 1. Design goals and brand principles

### 1.1 Goals (REQUIREMENT)

Within a few seconds, Home must answer (brief):

1. What company is Abadis?  
2. What problem does it solve?  
3. What products does it make?  
4. Why should hospitals choose Abadis?  
5. What is the impact on water, cost, and waste? *(only with approved metrics/formula)*

Also (project goals):

- Present Abadis as a specialized, knowledge-based manufacturer of suction / hospital fluid-management solutions.  
- Professional product and production capability presentation.  
- Build trust for hospitals, customers, and foreign representatives.  
- Preserve important information — **do not sacrifice facts for decoration** (brief critique of “Apple-like” emptiness).  
- Support FA / EN / AR with correct direction and language metadata.  
- Primary CTAs that lead to products, partnership, consultation, and credible content — not dead ends.

Product page goal: let a clinical / procurement visitor understand **what the product is**, **where it fits**, **how to evaluate it**, and **how to act** (download / inquire) without invented claims.

### 1.2 Brand attributes (REQUIREMENT — brief)

Beautiful/minimal · clean/medical · young/energetic · dignified/trustworthy · knowledge-based · modern/high-tech · impactful · international.

### 1.3 Visual identity direction (REQUIREMENT — brief)

Overall style: **Medical · Technology · Industrial · Premium**; **minimal, formal, international**.

Brief observation (not a locked palette system): existing green + white is said to fit medical / environmental domains.  

**DESIGN DECISION:** Final color tokens, type scale, and surface treatments are defined in the visual design pass from Abadis brand materials (logo / brand book) + this direction — **not** from `concept-preview/`.

### 1.4 Explicit non-goals for this visual package

- Not a full design system delivery for every page.  
- Not Calculator, About, or Representatives final UI (those follow).  
- Not interactive 3D at launch (**OUT OF BASE PHASE 1**).  
- Not chatbot / Experiences / anniversary UI.  
- Not copying rejected concept-preview composition (teal product-hero theatrics, etc.).

---

## 2. Global chrome: header, footer, navigation

### 2.1 Header (REQUIREMENT structure from IA)

| Element | Requirement | Design notes |
|---|---|---|
| Logo | Brand mark + wordmark access to Home | Always visible; high contrast |
| Primary nav | Products, Calculator, About, Impact, Representatives, Knowledge, News, Downloads, Contact (Careers may sit in utility/footer if nav density is high — **DESIGN DECISION**) | Collapse to drawer on mobile |
| Language switcher | FA / EN / AR | Prefer **equivalent page**; fallback language home only if no variant (**REQUIREMENT**) |
| Primary CTA in header | e.g. Contact / Consultation or View products — **DESIGN DECISION** which one is sticky | One clear priority CTA, not a cluster |
| Search | Optional Phase 1 — **DESIGN DECISION** | If deferred, do not fake an empty search |

**Out of header (REQUIREMENT):** chatbot launcher, Experiences login, 3D demo badge.

### 2.2 Footer (REQUIREMENT modules — IA)

Contact channels · key downloads · verified certifications only · legal/privacy · careers · language links · social if approved.

**CONTENT GATE:** Certification logos and claim lines only when Abadis verifies.

### 2.3 CTA strategy (REQUIREMENT + DESIGN DECISION)

| Priority | CTA intent (brief) | Typical destination |
|---|---|---|
| Primary | View products | Products hub / category |
| Primary | Consultation / contact sales or export | Contact or lead form |
| Secondary | Partnership / agency request | Collaboration page |
| Secondary | Calculator | Calculator |
| Tertiary | Latest news / articles | News or Articles hubs |
| Contextual (product page) | Download catalog/manual · Request quote · Related products | Download / Lead / Product |

**DESIGN DECISION:** Limit visible competing CTAs per viewport to **one primary + one secondary** in the hero; other CTAs appear later in the scroll.

**REQUIREMENT:** Forms that produce leads must support durable store-before-notify (behavior in build; design must not imply “sent” without success state tied to persistence).

---

## 3. Homepage — information hierarchy

### 3.1 Hierarchy (top → bottom)

1. **Brand + problem + primary action** (hero)  
2. **Product discovery** (what Abadis makes)  
3. **Why Abadis / credibility** (trust without overclaiming)  
4. **Impact / sustainability** (structure only until formula approved)  
5. **Calculator invitation** (differentiator — brief)  
6. **Proof network** (representatives / customers — verified items only)  
7. **Knowledge & news** (separated types)  
8. **Final CTA band** (consultation / partnership / contact)  

**REQUIREMENT:** One clear H1 per page (audit: missing H1 on current home).  
**REQUIREMENT:** Important information must remain scannable — avoid empty “cinematic void” that the brief criticizes.

### 3.2 Homepage sections

| # | Section | Purpose | Content / data requirements | Label |
|---|---|---|---|---|
| H0 | Skip link + lang/dir shell | A11y + correct `lang`/`dir` | `lang=fa\|en\|ar`, `dir=rtl\|ltr` | REQUIREMENT |
| H1 | **Hero** | Answer who / problem / products tease / primary CTA | Language-specific headline (**CONTENT GATE**); short supporting line; slogan if approved; **one** dominant real visual (product, factory, or clinical context — **not** decorative abstract alone); CTAs: View products + one secondary (partnership **or** consultation — **DESIGN DECISION**) | REQUIREMENT structure |
| H2 | **Product families** | Show what Abadis manufactures | Cards/links for approved families from IA (e.g. suction bag, canisters, filters, connections, holders, suction tube, other) — **names only as Abadis confirms**; image + short plain descriptor; link to category/product | REQUIREMENT |
| H3 | **Solutions / applications** (optional on Home) | Path from clinical context → products | Application labels **CONTENT GATE**; if Abadis prefers fewer Home modules, fold into H2 — **DESIGN DECISION / OPEN** | DESIGN DECISION |
| H4 | **Why Abadis** | Trust & differentiation | Short bullets from approved About/value props only; link to About | CONTENT GATE |
| H5 | **Credibility strip** | Memberships / certificates | Logos + titles **only verified**; link to Downloads/About | CONTENT GATE |
| H6 | **Stats** | Covered centers / markets / export countries | Numbers **CONTENT GATE**; if unapproved, **omit section or show labeled placeholders in design review only** | REQUIREMENT if shown |
| H7 | **Impact counter** | Water / washes / cost-time reduction | **CONTENT GATE:** formula + owner required; until then design may show **wireframe state** “Impact metrics — pending approved formula” — do **not** invent numbers | REQUIREMENT if included |
| H8 | **Calculator teaser** | Drive to interactive savings tool | Plain explanation of what the tool estimates; CTA to Calculator; no fake results | REQUIREMENT |
| H9 | **Factory / capability** | Production credibility | Prefer approved factory media; brief asks about factory video (**OPEN**); **never** use outdated “Coming Soon” factory messaging (brief weakness) | CONTENT GATE |
| H10 | **Representatives / markets** | International & distribution trust | Link to Representatives; optional map/list teaser with verified markets only | CONTENT GATE |
| H11 | **Customers** | Social proof | Optional; prominence **OPEN** in IA; logos only if verified & approved to display | OPEN |
| H12 | **News** | Company updates | Latest **News** items only (not educational mixed) | REQUIREMENT separation |
| H13 | **Educational articles** | Specialist/SEO | Separate module from News | REQUIREMENT separation |
| H14 | **Final CTA band** | Consultation / agency / sales-export contact | Clear form or deep-link; no chatbot required | REQUIREMENT |

**DESIGN DECISION:** Exact section order may swap H4–H9 for rhythm, but H1 → H2 must remain first content after chrome so product discovery is early.

### 3.3 Homepage content/data checklist (for CMS later)

- Hero: `headline`, `subline`, `slogan?`, `primary_cta`, `secondary_cta`, `hero_media`, `language`  
- Product family list: relations to Product Category  
- Why Abadis: approved rich text or bullets  
- Credibility: certificate entries (verified flag)  
- Stats: labeled metrics with source/approval  
- Impact: formula reference id + display values (approved only)  
- Calculator teaser: copy + link  
- Factory media: asset + caption + approval  
- News / Article collections: typed queries  
- CTA band: destination + copy  

---

## 4. Product detail page — information hierarchy

### 4.1 Hierarchy (top → bottom)

1. **Identity** — name, code/model (if approved), category breadcrumb  
2. **Primary visual** — approved product photography (or approved still); space reserved for future 3D (not required)  
3. **Summary** — what it is + primary applications (approved copy)  
4. **Actions** — download / inquire / related category  
5. **Technical specifications** — structured, source-backed  
6. **Variants / capacity / packaging** — if available  
7. **Compatibility / accessories** — relations only  
8. **Downloads & certificates** — linked Download objects  
9. **FAQ** — product-scoped  
10. **Related products**  
11. **Educational links** — optional, clearly “Learn more” not News  
12. **Inquiry CTA**  

**REQUIREMENT:** One H1 = product name.  
**REQUIREMENT:** Do not present unverified certifications or clinical claims as facts.

### 4.2 Product page sections

| # | Section | Purpose | Required fields / content | Label |
|---|---|---|---|---|
| P0 | Breadcrumb | Orientation | Home → Products → Category → Product | REQUIREMENT |
| P1 | **Title block** | Identity | `name`, `code_model` (if approved), category link, language | REQUIREMENT |
| P2 | **Media stage** | See the product | Primary image(s), gallery, alt text; optional video if approved | REQUIREMENT |
| P2b | **3D slot (optional future)** | Later interactivity | Empty/hidden in Phase 1 base; do not imply live 3D | OUT OF BASE PHASE 1 |
| P3 | **Short description** | Comprehension | Approved description; applications | CONTENT GATE |
| P4 | **Primary actions** | Conversion | Download (if file exists), Request quote / consultation, Contact | REQUIREMENT |
| P5 | **Specifications table** | Evaluation | `technical_specs` key/value from approved source | CONTENT GATE |
| P6 | **Models / capacity** | Variant clarity | Only if Abadis supplies | CONTENT GATE |
| P7 | **Packaging** | Logistics | If available | CONTENT GATE |
| P8 | **Compatibility** | System fit | Related products / accessories | CONTENT GATE |
| P9 | **Downloads** | Docs | Catalog, IFU, certificates (verified) | REQUIREMENT if files exist |
| P10 | **FAQ** | Objections | Product FAQ items | Optional |
| P11 | **Related products** | Discovery | Same category / accessories | REQUIREMENT pattern |
| P12 | **Inquiry** | Lead | Lead form fields per content model; source_product context | REQUIREMENT |

### 4.3 Product discovery / navigation (REQUIREMENT)

- From Home product families → category → product.  
- On product page: clear path back to category and Products hub.  
- Related products must not dump unrelated educational posts.  
- Language switcher: jump to translated product when pair exists (multilingual inventory shows pairs for core families).

### 4.4 Design states for incomplete product data (REQUIREMENT for honest UI)

| State | UI behavior |
|---|---|
| Missing `code_model` | Hide code row; do not show “TBD” as if real |
| Specs not approved | Show “Specifications under review” or omit table — **DESIGN DECISION** which; never fabricate rows |
| No downloads | Hide downloads block |
| No secondary images | Single image; no empty carousel dots |
| Unverified certificate | Do not render badge |
| Translation missing | Do not publish empty language page; switcher falls back per language rules |

---

## 5. Desktop / mobile behavior

| Concern | Desktop | Mobile |
|---|---|---|
| Hero | Full-bleed or near full-bleed visual plane; brand + headline + one short support + CTA group (**REQUIREMENT** spirit: strong first viewport; avoid clutter) | Same hierarchy; stacked; CTAs full-width; media below or behind text with readable contrast |
| Nav | Horizontal primary | Drawer / sheet; language + CTA accessible |
| Product media | Gallery beside or above title block — **DESIGN DECISION** | Gallery on top; swipe; specs below |
| Specs | Table or definition list | Stacked definition list; horizontal scroll only if unavoidable |
| Sticky CTA | Optional sticky inquire on scroll — **DESIGN DECISION** | Preferred sticky inquire/download after title |
| Touch | — | 44px-class targets; no hover-only info |
| Performance | Optimize hero media; defer below-fold | Same; avoid autoplaying heavy video unmuted |

**REQUIREMENT:** Layout must not rely on hover for essential specs or CTAs.  
**DESIGN DECISION:** Exact breakpoints follow the eventual design system; specify at least phone and desktop in the review package.

---

## 6. FA / EN / AR — RTL / LTR

| Locale | `lang` | `dir` | Notes |
|---|---|---|---|
| FA | `fa` (or `fa-IR` if Abadis standardizes) | `rtl` | Persian typography per `docs/persian-typography.md`; Persian digits where appropriate |
| AR | `ar` (**not** `fa-IR` — audit defect to fix) | `rtl` | Mirror layout; Arabic-capable font; avoid Persian-only glyphs |
| EN | `en` | `ltr` | Mirror of RTL structure; do not leave RTL artifacts |

**REQUIREMENT**

- Logical CSS (inline-start/end) so one template serves RTL/LTR.  
- Language-specific hero headline.  
- Mixed Latin product codes inside FA/AR: keep code LTR isolates where needed.  
- hreflang / equivalent URLs for published variants.  
- No empty translated shells.

**DESIGN DECISION:** Whether EN uses the same denser industrial tone or slightly more international marketing voice — copy approved by Abadis.

---

## 7. SEO and accessibility (design-affecting)

| Topic | Requirement |
|---|---|
| H1 | Exactly one meaningful H1 (home: brand/problem statement; product: product name) |
| Heading order | H2 per major section; no skipping for style |
| Images | Meaningful `alt`; decorative images empty alt |
| Contrast | Text on hero media must meet readable contrast (overlay/scrim if needed) |
| Focus | Visible focus for nav, CTAs, form fields |
| Forms | Labels, errors, success states; don’t imply submit success without durable save (build) |
| Motion | Respect `prefers-reduced-motion` |
| LCP | Hero media budgeted; no competing autoplay video in first viewport by default — **DESIGN DECISION** if factory video is below fold |

---

## 8. Motion / interaction principles

**REQUIREMENT:** Motion supports hierarchy and presence — not noise.

**DESIGN DECISION (first visual pass):**

- 2–3 intentional motions max on Home (e.g. hero fade/slide, subtle CTA emphasis, section reveal).  
- Product page: restrained gallery transitions; no continuous spinning product unless future 3D is approved.  
- Impact counter animation **only** when values are approved; otherwise static placeholder state.  
- No chatbot bounce, no sticker badges, no fake “live” metrics.

---

## 9. Where 3D could fit later (not Phase 1 launch)

**OUT OF BASE PHASE 1 (management):** interactive 3D viewer not required.

**DESIGN DECISION for readiness:** On the product media stage, designers may reserve a **neutral media frame** that can later host a 3D viewer toggle (“View 3D”) **hidden or absent** in Phase 1 comps. Do **not** show a fake 3D canvas or imply GLB availability. Media migration of any future GLB files is separate from shipping a viewer.

---

## 10. Image / video / media requirements

| Asset | Rule |
|---|---|
| Hero / product photography | Real product, factory, or clinical context — **REQUIREMENT** spirit; no stock that invents claims |
| Factory video | Brief interest (**OPEN**); if used, place below fold or secondary; replace obsolete Coming Soon |
| Install video | Brief dislikes current install videos; prefer future clean 2D animations — **not required** for first Home/Product comps |
| Certificates / logos | Verified only |
| Compression | Design for responsive sources; avoid multi-megabyte hero in comps notes |

**CONTENT GATE:** Every shown product photo should map to an approved product/family.

---

## 11. Missing / unapproved content states

Design comps for review may use clearly labeled placeholders:

- `[Headline — Abadis to approve]`  
- `[Metric — pending formula]`  
- `[Certificate — pending verification]`  
- `[Product code — pending official list]`  

Placeholders must be visually distinct from real content (e.g. muted dashed label) so management does not mistake them for final claims.

---

## 12. Reusable design-system patterns (to extract from these two pages)

These should become shared patterns after the visual pass is approved:

1. **Site header** (logo, nav, language, CTA)  
2. **Site footer**  
3. **Hero** (media + title + support + CTA group)  
4. **Section heading block** (H2 + optional support)  
5. **Product family card**  
6. **Primary / secondary / tertiary button**  
7. **Credibility logo strip**  
8. **Metric / stat cell** (with approved-only data)  
9. **CTA band**  
10. **Content teaser card** (News vs Article variants — visually distinct labels)  
11. **Breadcrumb**  
12. **Product media gallery**  
13. **Specifications definition list / table**  
14. **Download list row**  
15. **Lead / inquiry form** (shared field styling)  
16. **Empty / pending-approval inline notice**  
17. **Language switch control**  

---

## 13. Distinguishing brief requirements vs new design decisions

| Item | Source |
|---|---|
| Medical / tech / industrial / premium; minimal formal international | REQUIREMENT (brief) |
| Home must communicate who / problem / products / why / impact | REQUIREMENT (brief) |
| Home CTAs include products, partnership, news, articles, consultation, etc. | REQUIREMENT (brief intents); **which appear in hero** = DESIGN DECISION |
| Stats + dynamic impact counter | REQUIREMENT **if included**; numbers/formula = CONTENT GATE |
| Factory video on Home | OPEN question in brief → DESIGN DECISION placement if Abadis says yes |
| Do not sacrifice information for aesthetics | REQUIREMENT |
| Green/white suitability | Brief observation of current identity — not a locked token set |
| Single strong first viewport composition | DESIGN DECISION informed by project design rules + brief anti-emptiness critique |
| Section order after product families | DESIGN DECISION |
| Sticky mobile inquire on product | DESIGN DECISION |
| 3D on product page | OUT OF BASE PHASE 1; optional future slot only |

---

## Management approvals required

Only items that genuinely block **final** (not exploratory) Home + Product visuals:

| # | Approval needed | Why |
|---|---|---|
| 1 | Directional acceptance of this design spec (or marked edits) | Locks what the comps will contain |
| 2 | Hero message direction per language (or assign copy owner) | Home H1/subline |
| 3 | Product families to feature on Home (confirm/correct IA §2.4 list) | Product discovery module |
| 4 | Whether Home includes Solutions block, Stats, Impact counter, Customers, Factory video | Section scope |
| 5 | Approved impact/stats formulas **or** explicit “omit metrics from v1 comps” | Prevents fake numbers |
| 6 | One sample product (or family page) for the first Product detail comp — which URL/name | Product page subject |
| 7 | Whether Product comps are **category/family** page or **SKU** page | Template depth |
| 8 | Brand book constraints for color/type (what is mandatory vs free) | Visual system |
| 9 | Which header CTA is primary (Products vs Consultation) | Chrome consistency |
| 10 | Verified certificate/logo set allowed on Home | Credibility strip |

Copywriting of final FA/EN/AR strings can proceed in parallel once owners are named; comps may use labeled placeholders.

---

## First visual review package

Show management **exactly** these four frames (static design — Figma/Penpot/PDF equivalent):

| # | Frame | Must demonstrate |
|---|---|---|
| 1 | **Homepage — desktop** | Header/nav/language; hero hierarchy; product families; at least one trust module; calculator teaser; separated news vs articles; final CTA; footer |
| 2 | **Homepage — mobile** | Drawer nav; stacked hero; same section intent; thumb-reachable CTAs |
| 3 | **Product page — desktop** | Breadcrumb; title/code state; media stage (**no** fake 3D); summary; actions; specs (or pending state); downloads; related; inquiry |
| 4 | **Product page — mobile** | Media first; sticky or repeated inquire; readable specs |

**Annotation layer (required on the package):**

- Mark **REQUIREMENT** vs **placeholder CONTENT GATE** regions.  
- Note language shown (recommend **FA RTL** as primary review + one EN LTR variant if capacity allows — EN/AR can be follow-up if Abadis accepts FA-first).  
- Explicit caption: “Not based on `concept-preview/`.”

**Out of package:** Calculator full UI, About page, chatbot, 3D viewer, animation prototypes beyond simple motion notes.

---

## Document control

| | |
|---|---|
| Next step after approval | Produce the four-frame visual package |
| Then | Iterate → approve → only then implement in Nuxt |
| Authority on conflicts | `ABADIS-MASTER-SPECIFICATION.md` |
