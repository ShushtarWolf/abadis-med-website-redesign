# Abadis Management Decisions — WhatsApp version

To move the project forward and lock an executable statement of work, please answer these **7 groups**. Without these answers, the build phase for the new site does not start.

Detail source: `BOSS-DECISION-SHEET-FA.md` · Project authority: `ABADIS-MASTER-SPECIFICATION.md`

---

## Already confirmed (no management decision needed)

- The goal is not a visual reskin only: preserve URLs, SEO, valuable content, media/downloads, and durable capture of customer requests.
- Current display-layer direction: **Nuxt 4**
- Automation layer: **n8n**
- Live CMS today: **WordPress**
- `concept-preview` is **not** approved design (rejected visual reference only).
- Full customer club / ordering via **PayamGostar = Phase 2**; not in Phase 1 unless explicitly included in the contract.

## Current technical proposals (not yet management-confirmed)

These are not final choices; they only record the current technical proposal status:

- Content: headless WordPress
- Hosting: Liara direction
- Phase 1: durable form storage, then notify sales; full PayamGostar portal stays in Phase 2

---

## Group 1 — Scope, phases, and contract

Please specify:

1. Current contract scope?  
   a) Phase 1 only  
   b) Phase 1 + Phase 2 in one contract  
   c) Phase 1 now; Phase 2 as a separate contract
2. Per phase: deliverables, duration, cost, Abadis acceptance owner?
3. Post-launch support length and bug-response times?

*Phase 1 (baseline):* trilingual site, SEO/URL preservation, content & media migration, durable forms, priority pages.  
*Phase 2:* accounts, orders, invoices, customer dashboard on PayamGostar — only if contracted.

---

## Group 2 — CMS and hosting

1. Final CMS?  
   a) Headless WordPress  
   b) Another CMS (name it)  
   c) Custom system
2. Final host?  
   a) Liara  
   b) Alternative (name it)
3. Who gets staging and production access?

---

## Group 3 — Design direction

1. What is the approved design reference for building pages? (think-tank output / agency / designer — name or link)
2. Design approval calendar?
3. Does `concept-preview` remain rejected as the UI build source? (yes / no + note)

---

## Group 4 — Content, products, languages, domain

1. Page matrix: which pages get full rewrite / light edit / visual-only?
2. Approve the About timeline and copy from the brief? (yes / no + corrections)
3. Official product list (URL or SKU) and mandatory fields?
4. Which pages must exist in all three languages (FA / EN / AR)?
5. Canonical domain: apex or `www`?
6. Search Console access for the URL map? (yes / no / owner)

---

## Group 5 — Customer requests and leads (Phase 1)

1. Abadis follow-up owner and expected response time?
2. Notification channel? email / messenger / other
3. Which forms count as sales leads?
4. Phase 1 CRM depth?  
   a) Notify sales only  
   b) Create PayamGostar leads (if API available)  
   c) No CRM connection until Phase 2

---

## Group 6 — Optional Phase 1 extras

For each item separately: **in Phase 1** / **later phase** / **out of scope**

1. Product/FAQ AI chatbot
2. “Our Experiences” area (username/password)
3. 10th-anniversary campaign/game
4. Interactive 3D product viewer at launch

*Note:* Migrating media files is separate from shipping a 3D viewer.

---

## Group 7 — Launch, monitoring, data, operations

1. Launch window; go / no-go decision-maker; rollback authority?
2. Max acceptable downtime; how many hours of data loss / site recovery are acceptable?
3. Analytics tool/account + key events (forms, downloads, calculator)?
4. Retention period for form/chat data and access owner?
5. Monitoring alert channel and responder?
6. Speed acceptance criteria at management level?

---

## Quick reply template (copy and fill)

```
1) Scope: a/b/c — cost/time/acceptance owner: … — support: …
2) CMS: … — host: … — staging/prod access: …
3) Design reference: … — calendar: … — reject concept-preview: yes/no
4) Content matrix: … — About: … — products: … — languages: … — domain: … — Search Console: …
5) Sales owner: … — SLA: … — channel: … — Phase 1 CRM: a/b/c — lead forms: …
6) Chatbot: … | Experiences: … | Anniversary: … | 3D viewer: …
7) go/no-go: … — downtime/recovery: … — analytics: … — retention: … — monitoring: … — speed: …
```

Once these answers are in, the technical team can lock the executable SOW and start the build phase.

---

## Estimated Tools & Infrastructure

This section lists only accounts/services that may need to be purchased for the project. Separate from development work. Amounts and plans are estimates and must be confirmed before purchase; final choices depend on technical and management decisions.

1. **Cursor Pro+** — development / AI coding assistant · required for the development workflow · price: estimated / current pricing to be confirmed
2. **n8n** — automation / integrations · required by the agreed architecture · price: estimated / current pricing to be confirmed (no specific plan assumed)
3. **Liara** — hosting / deployment · technical proposal; pending management confirmation · price: estimated / current pricing to be confirmed
