# Abadis forms backend (Liara, Flask)

The static site posts every delivery form to `POST /submit` on this app. The app checks a honeypot and a per-IP rate limit, validates the fields, and emails `FORM_TO` (default inbox `info@abadis-med.com`) over SMTP. No secrets belong in git. `.env.example` has placeholders only.

Service name in `liara.json`: `abadis-forms` (Flask, port 8000).

- `POST /submit` — multipart or urlencoded. File fields are attached to the email.
- `GET /health` — `{"ok": true, "smtp": true}` when `SMTP_HOST` and `FORM_TO` are set.
- Spam: honeypot `_gotcha` (silent success, nothing is sent) and `RATE_PER_MIN` per IP.
- CORS: only origins listed in `ALLOWED_ORIGINS`.
- Forms: `contact`, `careers` (cooperation), `export` / `quote`, `solution`.

## Environment variables

Set these on the Liara app. Never commit them.

| Variable | Required | Purpose |
| --- | --- | --- |
| `SMTP_HOST` | yes | SMTP server reachable from Iran |
| `SMTP_PORT` | yes | Usually `587` |
| `SMTP_TLS` | yes | `starttls`, `ssl`, or `none` |
| `SMTP_USER` | yes, if the server requires login | SMTP username |
| `SMTP_PASS` | yes, if the server requires login | SMTP password |
| `MAIL_FROM` | recommended | From address. Falls back to `SMTP_USER` |
| `FORM_TO` | yes | Inbox. Use `info@abadis-med.com` |
| `FORM_TO_CONTACT` | no | Overrides `FORM_TO` for the contact and solution forms |
| `FORM_TO_CAREERS` | no | Overrides `FORM_TO` for the cooperation form |
| `FORM_TO_EXPORT` | no | Overrides `FORM_TO` for the export quote form |
| `ALLOWED_ORIGINS` | yes | `https://abadis-med.com,https://www.abadis-med.com` |
| `RATE_PER_MIN` | no | Default `5` |
| `MAX_UPLOAD_MB` | no | Default `8` |
| `MAX_FIELD_CHARS` | no | Default `4000` |

`MAIL_TO`, `MAIL_TO_CONTACT`, `MAIL_TO_CAREERS` and `MAIL_TO_EXPORT` are accepted aliases of the `FORM_TO*` variables.

## Deploy on Liara

1. In the Liara panel, create a Flask app named `abadis-forms` (the name in `liara.json`). Do not deploy this folder into the static `abadis-med` app.
2. Set the variables above in the Liara panel.
3. From `tools/forms-liara/`: `npm i -g @liara/cli && liara login && liara deploy`.
4. Open `https://abadis-forms.liara.run/health` and expect `{"ok": true, "smtp": true}`.

The static site posts to `https://abadis-forms.liara.run/submit`. That URL is the default of `FORM_ENDPOINT` in `tools/redesign/lib.py`, written into `<meta name="abadis-form-endpoint">`. A rebuild or a WordPress publish keeps it. Set `ABADIS_FORM_ENDPOINT` to another URL to override, or `ABADIS_FORMS_ENABLED=0` to clear the meta tag.

## Local test

```
pip install -r requirements.txt
python3 test_local.py
```

`test_local.py` starts a debugging SMTP server and posts one message for each form.
