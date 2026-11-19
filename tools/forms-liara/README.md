# Abadis forms backend (Liara, Flask)

Deploy-ready only. Do not create the Liara app and do not run `liara deploy` for this folder in the publishing-pipeline task. The static site keeps its mailto fallback until a human turns the flag on later.

The app receives the static site's contact and careers forms and emails them. Export quotes stay on `site/assets/js/quote-form.js` mailto. WhatsApp and CRM URLs stay empty until a provider is chosen. No analytics snippets.

- `POST /submit`: multipart or urlencoded form data (file uploads are attached to the email)
- `GET /health`: health check
- Spam: honeypot field `_gotcha` plus a per-IP rate limit
- CORS: only origins in `ALLOWED_ORIGINS`
- Recipients: `MAIL_TO_CONTACT`, `MAIL_TO_CAREERS`, and `MAIL_TO_EXPORT` when set, otherwise `MAIL_TO`
- Optional JSON copy to `WHATSAPP_WEBHOOK_URL` and `CRM_WEBHOOK_URL` (leave empty)

Every setting is an environment variable. `.env.example` has placeholders only (`smtp.example.com`, `forms-placeholder@example.com`). Do not commit real mailboxes or passwords.

## Later: deploy on Liara

A human does this after the publishing pipeline is in place. Not part of the current task.

1. In the Liara panel, create a Flask app (the name in `liara.json` is the placeholder `abadis-forms`). Do not point production forms at the test static app.
2. Set the variables from `.env.example` in the Liara panel. `ALLOWED_ORIGINS` must include `https://abadis-test.liara.run`, `https://abadis-med.com`, `https://www.abadis-med.com`, and `https://shushtarwolf.github.io`. Leave `WHATSAPP_WEBHOOK_URL` and `CRM_WEBHOOK_URL` empty.
3. From `tools/forms-liara/`: `npm i -g @liara/cli && liara login && liara deploy`.
4. Open `https://<app>.liara.run/health` and expect `{"ok": true}`.

## Later: turn the site flag on

The generator writes `<meta name="abadis-form-endpoint">` when a public URL is available:

- `ABADIS_FORM_ENDPOINT`, or `tools/redesign/data/form_endpoint.txt`
- `ABADIS_FORMS_ENABLED` is not `0` / `false` / `off` / `no`. If the variable is unset, a non-empty `form_endpoint.txt` turns forms on, so a rebuild keeps the contact and careers endpoint.

`form_endpoint.txt` holds `https://abadis-forms.vercel.app/submit`. Set `ABADIS_FORMS_ENABLED=0` to force mailto.

To point contact and careers at another inbox later:

1. Put the public POST URL in `tools/redesign/data/form_endpoint.txt`, or export `ABADIS_FORM_ENDPOINT`.
2. Leave `ABADIS_FORMS_ENABLED` unset, or export `ABADIS_FORMS_ENABLED=1`.
3. Run `python3 tools/redesign/seo_postprocess.py`, or `python3 tools/redesign/build.py posts home i18n archives`. That writes the meta tag. `site/assets/js/site.js` posts with fetch and opens mailto if the request fails.
4. Clear the URL, or set `ABADIS_FORMS_ENABLED=0`, to go back to mailto.

Do not set the flag in the WordPress publish workflow. Do not aim production forms at `abadis-test`.

## Local test

```
pip install -r requirements.txt
SMTP_HOST=localhost SMTP_PORT=1025 SMTP_TLS=none MAIL_TO=forms-placeholder@example.com python app.py
curl -F form_name=contact -F name=Test -F msg=Hi http://localhost:8000/submit
```
