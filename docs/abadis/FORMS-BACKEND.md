# Forms backend — contact + careers

Static `site/` cannot receive POSTs by itself. Both forms (`#leadForm` on `/contact/` and the careers form on `/careers/`) share one client handler in `site/assets/js/site.js`:

1. Read `<meta name="abadis-form-endpoint" content="…">` (from `FORM_ENDPOINT` in `tools/redesign/lib.py`, overridable with env `ABADIS_FORM_ENDPOINT`).
2. If set → `fetch(endpoint, { method: 'POST', body: FormData, headers: { Accept: 'application/json' } })` with hidden `form_name` (`contact` | `careers`) and honeypot `_gotcha`.
3. If empty, or network/HTTP error → open `mailto:` to `<meta name="abadis-form-mailto">` (default `info@abadis-med.com`) with the same fields.

Offline hints (`.form-offline-hint`) hide automatically when the endpoint meta is non-empty.

**Do not commit API keys, Formspree private hashes you want secret, or Worker secrets.** Only a public POST URL may go in `FORM_ENDPOINT`.

---

## Option A — Formspree (simplest)

| | |
|---|---|
| Cost | Free tier: limited submissions/month; file uploads need a paid plan |
| Upload | Careers form on the live site has **no** resume file field — free tier is enough today |
| Setup | 1) Create form at [formspree.io](https://formspree.io) → copy endpoint `https://formspree.io/f/xxxxxxxx` 2) Set notification email (inbox) 3) Put that URL in `FORM_ENDPOINT` 4) Rebuild |

```bash
export ABADIS_FORM_ENDPOINT='https://formspree.io/f/xxxxxxxx'
python3 tools/redesign/build.py careers contact
python3 tools/redesign/apply_shell.py
# or set FORM_ENDPOINT in tools/redesign/lib.py before build (public URL only)
```

Formspree accepts `FormData` and `Accept: application/json`. Honeypot field name `_gotcha` is supported.

---

## Option B — Cloudflare Worker + email

| | |
|---|---|
| Cost | Workers free tier is usually enough; email via Resend (free tier) or Email Routing |
| Upload | Add R2 later if you add a resume field |
| Setup | 1) Deploy `tools/forms-worker/` with `wrangler` 2) Set secrets `INBOX_TO`, `RESEND_API_KEY` (or SMTP) 3) Put the Worker URL in `FORM_ENDPOINT` |

Sample Worker (no secrets in repo): `tools/forms-worker/`. Bindings/env only.

---

## Option C — n8n webhook

Existing audit workflow notes live in `docs/abadis/N8N-WORKFLOW.md` (unrelated to forms). For forms: create a **Webhook** node (POST), then **Email** / Gmail / SMTP to your inbox. Put the production webhook URL in `FORM_ENDPOINT`. Protect with a header or obscure path; still no secrets in git.

---

## Where to set the endpoint

| Place | Use |
|---|---|
| `tools/redesign/lib.py` → `FORM_ENDPOINT = 'https://…'` | Permanent public URL for production builds |
| Env `ABADIS_FORM_ENDPOINT` | CI / local override without editing the file |
| Leave empty | Mailto-only preview (current default) |

After changing it: `python3 tools/redesign/build.py` (at least `careers`) and `python3 tools/redesign/apply_shell.py` so hand-built `/contact/` gets the meta tag.

---

## Careers form notes

Fields mirror live Gravity Form #2 on `فرصت-های-همکاری` (WP REST, Oct 2026): personal data, address, phones, education/work/current-job list rows, salary, referral, workplace expectations (rank 1–8), languages, computer skills, free-text paragraph.

**No file upload** on the live form — if you add a résumé `<input type="file">` later, Formspree free tier and a plain mailto fallback will not carry the file; use a paid Formspree plan, Worker+R2, or n8n binary handling.
