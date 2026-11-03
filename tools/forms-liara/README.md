# Abadis forms backend (Liara, Flask) - not deployed

Small Flask app that receives the static site's forms and emails them. Replaces the
Cloudflare Worker in `tools/forms-worker/`, which does not run on Liara.

- `POST /submit`: multipart or urlencoded form data (file uploads are attached to the email)
- `GET /health`: health check
- Spam: honeypot field `_gotcha` (already in every site form) plus a per-IP rate limit
- CORS: only origins in `ALLOWED_ORIGINS`
- Optional: JSON copy to `WHATSAPP_WEBHOOK_URL` and `CRM_WEBHOOK_URL` (placeholders until a provider is chosen)

## Deploy on Liara (when approved)

1. Create a Flask app in the Liara panel, set its name in `liara.json` (`abadis-forms` is a placeholder).
2. Set the environment variables from `.env.example` in the Liara panel (never commit real values).
3. `npm i -g @liara/cli && liara login && liara deploy` in this folder.
4. Check `https://<app>.liara.run/health`.

## Switch the site from mailto to this backend

Until an endpoint exists, the site forms stay on `mailto:`. To switch:

1. Put the full URL (for example `https://forms.abadis-med.com/submit`) in
   `tools/redesign/data/form_endpoint.txt`, or set env `ABADIS_FORM_ENDPOINT`.
2. Run `python3 tools/redesign/seo_postprocess.py` (or the full build). It writes the URL into
   `<meta name="abadis-form-endpoint">` on every page; `site.js` then posts with fetch and falls
   back to mailto if the server fails.
3. Clear the file to go back to mailto.

## Local test

```
pip install -r requirements.txt
SMTP_HOST=localhost SMTP_PORT=1025 SMTP_TLS=none python app.py
curl -F form_name=contact -F name=Test -F msg=Hi http://localhost:8000/submit
```
