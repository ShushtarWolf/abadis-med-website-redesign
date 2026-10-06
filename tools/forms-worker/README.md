# Abadis forms Worker (optional)

Cloudflare Worker that accepts `multipart/form-data` or `application/x-www-form-urlencoded` from the static site and emails the inbox via [Resend](https://resend.com).

## Deploy

```bash
cd tools/forms-worker
npm i -g wrangler   # once
wrangler login
wrangler secret put INBOX_TO          # e.g. info@abadis-med.com
wrangler secret put RESEND_API_KEY
# optional: wrangler secret put INBOX_FROM  # verified sender on Resend
wrangler deploy
```

Put the Worker URL into `FORM_ENDPOINT` (see `docs/abadis/FORMS-BACKEND.md`), rebuild, done.

## Local

```bash
INBOX_TO=you@example.com RESEND_API_KEY=re_xxx wrangler dev
```

No secrets are stored in this directory.
