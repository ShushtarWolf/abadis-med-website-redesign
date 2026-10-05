# Abadis — Open Questions & Decisions

Source: `docs/abadis/references/Abadis_WordPress_to_Nuxt_Migration_Technical_Review_FA.pdf`  
Scope: Unanswered items extracted from that document only. Known project decisions recorded below; no invented answers.

---

## Business / content

| ID | Question / Decision | Why It Matters | Owner | Status | Answer / Decision | Evidence / Source |
|---|---|---|---|---|---|---|
| B1 | For each project phase: deliverables, duration, cost, dependencies, owner, acceptance criteria | Turns the six-part proposal into an executable SOW | Technical team (Abadis to approve) | Unanswered | | PDF §13 |
| B2 | Items outside SOW, and recurring service costs, listed separately | Scope and ongoing budget | Technical team (Abadis to approve) | Unanswered | | PDF §13 |
| B3 | Privacy: what data may be collected, who can access it, retention period | Compliance and analytics/forms setup | Abadis | Unanswered | | PDF §11 |
| B4 | Which analytics conversions / form-submit events are required | Measurement and delivery acceptance | Abadis | Unanswered | | PDF §11 |
| B5 | Support: bugfix duration, response time, owner of each service | Post-launch operations | Abadis + technical team | Unanswered | | PDF §12 |
| B6 | Go-live: cutover owner, timing, stop criteria, rollback plan | Safe release | Abadis + technical team | Unanswered | | PDF §12 |

## WordPress / CMS

| ID | Question / Decision | Why It Matters | Owner | Status | Answer / Decision | Evidence / Source |
|---|---|---|---|---|---|---|
| C1 | Final CMS: headless WordPress vs independent CMS vs custom system (compare cost vs content-team needs) | Decides where products/pages live and how editors work | Abadis + technical team | Already decided | WordPress remains the CMS; Nuxt 4 is the frontend/display layer | Current Abadis project decision; PDF §2–§3 (was deferred) |
| C2 | Pre-migration data model: storage location, edit method, content types, product fields, relationships, SEO fields, user roles | Migration cannot proceed on “convert to required structure” alone | Technical team (Abadis confirm content needs) | Unanswered | | PDF §3 |
| C3 | Confirm whether products, custom fields, and SEO-plugin data are available beyond default WP REST | Avoid assuming incomplete source data | Technical team (Abadis may need to grant access) | Needs clarification | | PDF §4, §14 |

## SEO / URLs / redirects

| ID | Question / Decision | Why It Matters | Owner | Status | Answer / Decision | Evidence / Source |
|---|---|---|---|---|---|---|
| S1 | Whether Search Console data is available as an input for the URL mapping list | Completeness of Old→New URL plan before launch | Abadis | Needs clarification | | PDF §6 |

## Languages (FA / EN / AR)

| ID | Question / Decision | Why It Matters | Owner | Status | Answer / Decision | Evidence / Source |
|---|---|---|---|---|---|---|
| L1 | How product/page language versions relate in the data model | Correct multilingual content and SEO linking | Abadis + technical team | Unanswered | | PDF §3 (part of data model); see also C2 |

## Forms / integrations / functionality

| ID | Question / Decision | Why It Matters | Owner | Status | Answer / Decision | Evidence / Source |
|---|---|---|---|---|---|---|
| F1 | Form follow-up owner, response time, and how call outcome is recorded | Sales handoff and acceptance tests | Abadis | Unanswered | | PDF §8 |
| F2 | Monitoring: exact check interval and alert thresholds (esp. outage / critical errors) | “Daily check” is not enough as written | Abadis + technical team | Unanswered | | PDF §9 |
| F3 | Alert channel, recipients, and owner to fix each error type | Ops ownership | Abadis + technical team | Unanswered | | PDF §9 |
| F4 | AI publishing: who is the human approver; prompt/model/data-source versioning | Blocks unverified product claims going live | Abadis (+ technical team for tooling) | Unanswered | | PDF §10 |

**Related known decision (not a PDF open-question ID):** the project will use n8n as a complementary automation layer (forms, notifications, periodic jobs — not a substitute for a testable migration script unless it meets the PDF controls).

## Hosting / infrastructure

| ID | Question / Decision | Why It Matters | Owner | Status | Answer / Decision | Evidence / Source |
|---|---|---|---|---|---|---|
| H1 | Final host selection | Architecture and delivery | Abadis + technical team | Already decided | Hosting will use Liara | Current Abadis project decision; PDF §2 (was deferred) |
| H2 | File storage location, CDN, and file-naming policy | Media URLs must not break; delivery of images/PDFs | Technical team (Abadis approve) | Unanswered | | PDF §5 |

## Nuxt / technical architecture

| ID | Question / Decision | Why It Matters | Owner | Status | Answer / Decision | Evidence / Source |
|---|---|---|---|---|---|---|
| N1 | Exact Nuxt version (and support status) to register at project start; if not Nuxt 4, justification + support plan | Support lifecycle / maintenance | Technical team | Already decided | Nuxt 4 | Current Abadis project decision; PDF §2 |
| N2 | Performance criteria, sample pages, devices, and test conditions — agreed before delivery | Acceptance of speed/quality | Abadis + technical team | Unanswered | | PDF §7 |
| N3 | Per workstream: outputs, test method, cost, time, owner (needed before start) | Makes the proposal executable | Technical team (Abadis approve) | Unanswered | | PDF §1 |

## Other

| ID | Question / Decision | Why It Matters | Owner | Status | Answer / Decision | Evidence / Source |
|---|---|---|---|---|---|---|
| O1 | Backup schedule and a real restore test as part of delivery | Recovery readiness | Technical team (Abadis confirm policy) | Unanswered | | PDF §11–§12 |
| O2 | Training, hosting access handoff, and post-delivery bugfix period details | Handover acceptance | Abadis + technical team | Unanswered | | PDF §11–§12 |
