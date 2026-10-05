# ABADIS-DESIGN-REVIEW-V4

**Document type:** DESIGN REVIEW FINDINGS — **not** implementation instructions  
**Date of review:** 2026-10-03  
**Reviewer role:** Design decision input only  
**Decision authority:** Human / bosses  

> These are **DESIGN REVIEW FINDINGS** for boss/management decision input.  
> They are **not** implementation instructions, not a ranked winner, and not an approved visual system.  
> Do **not** modify production. Do **not** treat this as a mandate to build one of the four prototypes as-is.  
> Existing audit / specification facts in this project remain authoritative and are not replaced by this document.

### Prototype URLs reviewed

1. **ABADIS** — https://siaamak-ghodsi.github.io/abadis-scroll-scrub-demo/abadis/?v=37e3141  
2. **GLASS** — https://siaamak-ghodsi.github.io/abadis-scroll-scrub-demo/glass/?v=37e3141  
3. **NOIR** — https://siaamak-ghodsi.github.io/abadis-scroll-scrub-demo/noir/?v=37e3141  
4. **STAGE** — https://siaamak-ghodsi.github.io/abadis-scroll-scrub-demo/stage/?v=37e3141  

### Project requirements used as constraints (not invented)

| Source | Observable / documented requirement |
|---|---|
| Design brief / Master Spec | Medical · Technology · Industrial · Premium; minimal, formal, international |
| Design brief | Green + white stated as fitting medical/environmental domains (not a locked token system) |
| Design brief | Serres cited for **2D install animations** asset style |
| Project docs | `concept-preview/` is **rejected** as approved visual direction |
| Phase-1 design spec | Interactive 3D is **OUT OF BASE PHASE 1** unless separately approved |
| Phase-1 / Master Spec | FA / EN / AR; preserve content; brand materials must be respected |
| User task statement | Inspired by Serres **and** Whist — **Whist not found** in project docs (see UNKNOWN) |

### Traceability labels

| Label | Meaning |
|---|---|
| **FACT** | Directly observable in a prototype or project document |
| **INFERENCE** | Reasonable interpretation of observed evidence |
| **RECOMMENDATION** | Possible design direction for bosses to accept or reject |
| **UNKNOWN** | Requires explicit human/boss confirmation |

---

## TASK 1 — Comparison table

> LIKE / DISLIKE are relative to **observable fit with established ABADIS requirements**, not a ranking.  
> KEEP / CHANGE are design-review candidates for boss confirmation.  
> **No ranking. No winner. No overall score.**

| Prototype | LIKE | DISLIKE | KEEP | CHANGE |
|---|---|---|---|---|
| **ABADIS** | **FACT:** Light content bands + dark teal hero; brand-adjacent teal (`#05686b`, `#2ec4c6`, `#0b2e32`). **FACT:** Content-forward sections (intro, numbered features, size blocks, galleries, code tables, filters, contact). **FACT:** Header CTA “تماس با فروش” + in-page anchors. **INFERENCE:** Closest visual link to brief’s medical green/teal + white. Strong trust/readability for long product copy. | **FACT:** Hero leans on clinical photo/video with heavy teal overlay — similar theatrical full-bleed treatment that Phase-1 warns against copying from rejected concept. **INFERENCE:** Less “product-as-hero” than Stage’s orbit panel; product appears later. **UNKNOWN:** Whether teal intensity matches brand book. | Product information architecture (sizes → galleries → codes → filters → CTA). RTL/FA Kalameh. One primary header sales CTA. Spec chips/tables for clinical/procurement readers. | Confirm hero media vs product-first hero. Confirm whether teal system is brand-official. Reduce decorative drama if it conflicts with rejected-concept guidance. Ensure full-site IA (not only product anchors) when scaling beyond this demo. |
| **GLASS** | **FACT:** Dark glassmorphism header; teal accent on dark `#060d12`. **FACT:** Explicit interaction metaphor: click cards fill/empty (“استعارهٔ جمع‌آوری و تخلیه”). **FACT:** Same underlying product content deeper in page. **INFERENCE:** Strong tech/premium presence; memorable product storytelling. | **FACT:** Chip/CTAs emphasize “شیشه‌ای · تعاملی · سه‌بعدی” / “شروع تجربه” — experience-demo tone. **FACT:** Interactive fill + 3D exceed Phase-1 “no interactive 3D at launch” unless approved. **INFERENCE:** Glass/glow/cursor effects may read more consumer-demo than hospital procurement. **UNKNOWN:** Accessibility of fill animation; mobile cost. | Teal-on-dark as *an* option for med-tech contrast. Feature-card idea (if toned down). Drag-to-rotate 3D as optional later phase. | Soften “experience game” framing for B2B medical. Decide if glass header is production chrome. Gate heavy interaction behind Phase scope. Align accent with brand book (not demo palette alone). |
| **NOIR** | **FACT:** Same interaction/structure family as Glass (shared sections/classes). **FACT:** Purple accent `#a78bfa`, rose/blood `#e11d48`/`#fb7185` on near-black `#0a0a12`. **INFERENCE:** High-fashion premium/noir mood; strong contrast for white Persian type. | **FACT:** Purple/violet + rose is **not** the brief’s green/white medical identity observation. **INFERENCE:** Risk of generic “dark luxury UI” vs ABADIS brand recognition. Same interaction/3D scope issues as Glass. **FACT:** Chip still says “شیشه‌ای…” despite noir palette. | Dark high-contrast typography experiments. Numbered feature storytelling. | Palette almost certainly needs brand-book validation. Separate “mood exploration” from production colors. Same interaction gating as Glass. |
| **STAGE** | **FACT:** Numbered rail `۰۱…۰۷` + `تماس`; 7 full-viewport panels. **FACT:** Product “stage” with orbiting callout tags + drag/touch 3D. **FACT:** Horizontal feature cards; `prefers-reduced-motion` media query present. **INFERENCE:** Clearest product-as-hero / industrial showcase; strong section choreography. | **FACT:** Accent purple/rose like Noir — away from brief green/white note. **FACT:** Rail is numeric, not full site IA labels. **INFERENCE:** Panel/stage model may fight long multilingual content and standard header/footer requirements. Heavy theatrical density. | Numbered section rhythm; orbit callouts (as static or light motion); reduced-motion consideration; product-centered panel. | Map rail to real IA (Products, About, Calculator…). Confirm dark+purple vs brand. Validate horizontal-scroll + full-bleed panels on mobile. Scope 3D vs Phase-1. |

---

## TASK 2 — Common elements

| Element | Seen in which prototypes | What works | What should be changed |
|---|---|---|---|
| FA RTL + Kalameh | All four **FACT** | Meets multilingual Persian base; modern medical-tech type | Still need EN/AR layouts **UNKNOWN** in these demos (no complete language switcher observed on Stage; not verified as production-ready trilingual UI) |
| Clinical OR/ICU photography / video hero | All four **FACT** | Immediate medical context and credibility | Avoid over-reliance on theatrical full-bleed alone; product must remain findable **INFERENCE** |
| Primary sales / contact CTA | ABADIS, Glass, Noir, Stage (wording varies) **FACT** | Matches Phase-1 need for clear contact/sales action | Bosses choose header CTA: products vs consultation (already an open design question) |
| Feature storytelling (gel / hydrophobic filter / compatibility / disposable / serial) | All four **FACT** | Real product benefits, not empty marketing | Card metaphors vs static features vs horizontal stage — choose density **DISCUSS** |
| Interactive / presented 3D suction bag | All four **FACT** | Strong product understanding | Phase-1 marks interactive 3D **out of base** unless approved **FACT** |
| Size sections 1L / 2L / 3L + galleries + dimensions | All four (depth varies) **FACT** | Preserves real ABADIS content | Keep facts; don’t invent stats; polish presentation only |
| Product code tables | ABADIS, Glass/Noir, Stage **FACT** | Procurement-critical | Keep readable tables; don’t hide behind animation |
| Filters section (antibacterial / flow-stop / porous) | All four **FACT** | Content continuity | Hierarchy vs home/product page split is IA decision |
| Contact block (phones, addresses, email) | All four **FACT** | Trust + action | Confirm numbers against live site before production |
| Dark “premium” surfaces | Glass, Noir, Stage **FACT**; ABADIS mixes dark hero + light body **FACT** | Premium tech feel | Whether site is mostly light, mostly dark, or hybrid = boss decision |
| Teal/cyan accent | ABADIS, Glass **FACT** | Closer to brief green/medical note **INFERENCE** | Exact tokens need brand book **UNKNOWN** |
| Purple/rose accent | Noir, Stage **FACT** | High contrast drama | Likely conflicts with green/white brand observation unless bosses override |

---

## TASK 3 — Boss-meeting decision sheet

### KEEP

- Real ABADIS product facts: volumes, filters, gel powder, compatibility, codes, packaging, clinical use contexts **FACT**
- FA RTL + Kalameh direction for Persian UI **FACT**
- Clear primary contact/sales path **FACT**
- Product photography + technical tables (not decoration-only) **FACT**
- Medical / technology / industrial / premium brief direction **FACT**
- Content preservation (redesign ≠ rewrite of approved product data) **FACT**

### CHANGE

- Treat these four URLs as **exploratory prototypes**, not an approved production system **INFERENCE**
- Do not ship “experience demo” framing (“شروع تجربه”, fill/empty game) as default hospital UX without approval **RECOMMENDATION**
- Do not assume purple/noir palette is brand-compliant **INFERENCE**
- Do not assume interactive 3D is in Phase 1 (spec says out unless approved) **FACT**
- Numeric stage rail ≠ full site navigation required by IA **FACT**

### DISCUSS

- Light hybrid (ABADIS) vs dark glass (Glass) vs dark purple (Noir/Stage)
- Hero: clinical lifestyle full-bleed vs product-stage spotlight
- Interaction level: static → light motion → click metaphors → 3D orbit
- Feature presentation: 3 static cards vs 6 interactive cards vs horizontal stage cards
- Header: solid bar vs floating glass pill vs numbered rail
- How much Serres/Whist inspiration applies to **whole site** vs install-animation assets only

### DO NOT ASSUME

- Final brand-book color/type locks (**brand book not extractable / still OPEN** in project docs) **FACT**
- Whist as documented requirement (user-stated for this review; **not found** in brief/docs) **UNKNOWN**
- That any single prototype is “the” direction **UNKNOWN**
- EN/AR visual parity from FA-only demos **UNKNOWN**
- Production performance budgets for 3D/video/glass effects **UNKNOWN**
- That rejected `concept-preview` teal theatrics are cleared by these demos **UNKNOWN** — Phase-1 still forbids copying that rejected composition

---

## TASK 4 — Final combined design characteristics

*(Characteristics only — do **not** read as “choose ABADIS / Glass / Noir / Stage”.)*

Based on **shared useful signals** across the four prototypes and existing ABADIS project requirements:

1. **Navigation** — Persistent chrome with logo, clear primary CTA (sales/consultation *or* products — boss pick), and real IA labels; collapse on mobile. Numbered stage rails can inspire section rhythm, not replace site nav. Language switcher FA/EN/AR required in production (not proven in these demos).

2. **Hero** — One composition: brand + one headline + short support + one primary CTA group. Clinical context imagery is useful; product should not disappear. Avoid stacking demo/game CTAs in the first viewport.

3. **Product presentation** — Lead with clear size families (1/2/3L), benefits that match real specs, then galleries, dimensions, code tables, filters, downloads/contact. Prefer scannable technical truth over metaphor-only UI.

4. **Typography** — Kalameh (or brand-book Persian stack) with strong hierarchy; high contrast on both light and dark bands; Persian digits where appropriate.

5. **Animation level** — Prefer restrained motion supporting hierarchy. Gate click-fill metaphors and interactive 3D behind explicit Phase approval; keep `prefers-reduced-motion` in mind (observed on Stage).

6. **Visual density** — Premium breathing room in heroes; denser, readable modules for specs/tables (ABADIS-style content bands work for trust).

7. **Color usage** — Anchor to brand book + brief medical green/white observation; teal-cyan is the demo family closest to that note; purple/rose stays exploratory until approved.

8. **Section structure** — Intro/benefits → product sizes → technical proof → filters/accessories → CTA/contact. Optional “stage” product spotlight as a section, not the whole IA.

9. **Interaction style** — Professional, precise, hospital-credible. Interaction should explain the product, not overshadow procurement tasks.

10. **Multilingual / content** — Same structure for FA/EN/AR with correct direction; no invented claims; preserve audited content.

---

## Additional UNKNOWN / gaps

- Exact Whist reference intent (not in brief text extracted)
- Brand-book mandatory tokens
- Whether bosses want mostly light, dark, or hybrid site chrome
- Phase inclusion of interactive 3D / glass demos
- Mobile UX quality of horizontal stage + glass effects (media queries exist; full device QA not completed in this review)

---

## What the bosses need to decide

1. **Surface system:** light hybrid (teal/white) vs dark teal-glass vs dark purple/noir — relative to brand book  
2. **Hero model:** clinical lifestyle full-bleed vs product-stage spotlight (or a defined hybrid)  
3. **Motion / 3D budget for Phase 1:** static + light motion only, or approve interactive 3D / fill metaphors  
4. **Accent colors:** lock teal/green family vs allow purple exploratory accents  
5. **Header pattern:** classic bar vs glass pill vs other — and primary CTA = products or sales  
6. **Serres / Whist:** confirm what to borrow (install animation style vs overall site aesthetic)  
7. **Confirm** these findings are review input only — **no prototype is auto-selected for build**

---

## n8n / traceability note

- Related workflow context: **Abadis Website Audit v2** (`jHEbjGnYNWKyI1pb`) — audit/crawl/plan pipeline only.
- This design-review document is stored in the project docs tree. It does **not** modify audit JSON, master specification, or workflow logic.
- Optional later manual step for operators: link this file from a sticky note on the audit workflow. Do **not** overwrite audit outputs with design-review content.

### Related existing docs (unchanged)

- `docs/abadis/ABADIS-MASTER-SPECIFICATION.md`
- `docs/abadis/PHASE-1-HOMEPAGE-PRODUCT-DESIGN-SPEC.md`
- `docs/abadis/BOSS-DECISION-SHEET-FA.md`
- `docs/abadis/N8N-WORKFLOW.md`
- `docs/abadis/ABADIS-AUDIT.json`
