"""Abadis Med forms backend for Liara (Flask platform).
Receives multipart or urlencoded POSTs from the static site forms, drops spam
(honeypot `_gotcha`), emails the inbox over SMTP and optionally forwards a JSON
copy to WhatsApp/CRM webhooks. All settings come from environment variables.
"""
import os, json, smtplib, ssl, time, urllib.request
from email.message import EmailMessage
from flask import Flask, request, jsonify

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = int(os.environ.get('MAX_UPLOAD_MB', '8')) * 1024 * 1024

ALLOWED_ORIGINS = [o.strip() for o in os.environ.get(
    'ALLOWED_ORIGINS', 'https://abadis-med.com,https://www.abadis-med.com').split(',') if o.strip()]
SMTP_HOST = os.environ.get('SMTP_HOST', '')
SMTP_PORT = int(os.environ.get('SMTP_PORT', '587'))
SMTP_USER = os.environ.get('SMTP_USER', '')
SMTP_PASS = os.environ.get('SMTP_PASS', '')
SMTP_TLS = os.environ.get('SMTP_TLS', 'starttls')  # starttls | ssl | none
MAIL_FROM = os.environ.get('MAIL_FROM', SMTP_USER)
MAIL_TO = os.environ.get('MAIL_TO', 'info@abadis-med.com')
WHATSAPP_WEBHOOK_URL = os.environ.get('WHATSAPP_WEBHOOK_URL', '')  # placeholder, optional
CRM_WEBHOOK_URL = os.environ.get('CRM_WEBHOOK_URL', '')            # placeholder, optional
WEBHOOK_TOKEN = os.environ.get('WEBHOOK_TOKEN', '')
RATE_PER_MIN = int(os.environ.get('RATE_PER_MIN', '5'))
_hits = {}


def cors(resp):
    origin = request.headers.get('Origin', '')
    if origin in ALLOWED_ORIGINS:
        resp.headers['Access-Control-Allow-Origin'] = origin
        resp.headers['Vary'] = 'Origin'
        resp.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        resp.headers['Access-Control-Allow-Headers'] = 'Content-Type, Accept'
        resp.headers['Access-Control-Max-Age'] = '86400'
    return resp


app.after_request(cors)


def limited(ip):
    now = time.time()
    hits = [t for t in _hits.get(ip, []) if now - t < 60]
    hits.append(now)
    _hits[ip] = hits
    return len(hits) > RATE_PER_MIN


def send_mail(subject, body, files):
    if not SMTP_HOST:
        raise RuntimeError('SMTP_HOST not set')
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = MAIL_FROM
    msg['To'] = MAIL_TO
    msg.set_content(body)
    for f in files:
        data = f.read()
        if data:
            maintype, _, subtype = (f.mimetype or 'application/octet-stream').partition('/')
            msg.add_attachment(data, maintype=maintype, subtype=subtype or 'octet-stream', filename=f.filename)
    ctx = ssl.create_default_context()
    if SMTP_TLS == 'ssl':
        s = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=ctx, timeout=20)
    else:
        s = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=20)
        if SMTP_TLS == 'starttls':
            s.starttls(context=ctx)
    with s:
        if SMTP_USER:
            s.login(SMTP_USER, SMTP_PASS)
        s.send_message(msg)


def post_webhook(url, payload):
    if not url:
        return
    req = urllib.request.Request(url, data=json.dumps(payload, ensure_ascii=False).encode('utf-8'),
                                 headers={'Content-Type': 'application/json',
                                          **({'Authorization': 'Bearer ' + WEBHOOK_TOKEN} if WEBHOOK_TOKEN else {})})
    try:
        urllib.request.urlopen(req, timeout=10).read()
    except Exception as e:  # webhook failure must not lose the email
        app.logger.warning('webhook %s failed: %s', url, e)


@app.get('/health')
def health():
    return jsonify(ok=True)


@app.route('/submit', methods=['POST', 'OPTIONS'])
def submit():
    if request.method == 'OPTIONS':
        return ('', 204)
    origin = request.headers.get('Origin', '')
    if ALLOWED_ORIGINS and origin and origin not in ALLOWED_ORIGINS:
        return jsonify(ok=False, error='origin'), 403
    ip = request.headers.get('X-Forwarded-For', request.remote_addr or '').split(',')[0].strip()
    if limited(ip):
        return jsonify(ok=False, error='rate'), 429
    form = request.form
    if form.get('_gotcha', '').strip():  # honeypot: pretend success
        return jsonify(ok=True)
    fields = {k: v for k, v in form.items() if k not in ('_gotcha',) and v.strip()}
    if not fields:
        return jsonify(ok=False, error='empty'), 400
    name = fields.get('form_name', 'form')
    subject = 'Abadis website form: ' + name + (' - ' + fields['topic'] if fields.get('topic') else '')
    body = '\n'.join(f'{k}: {v}' for k, v in fields.items()) + f'\n\nIP: {ip}\nOrigin: {origin}'
    try:
        send_mail(subject, body, list(request.files.values()))
    except Exception as e:
        app.logger.error('mail failed: %s', e)
        return jsonify(ok=False, error='mail'), 502
    payload = {'form': name, 'fields': fields, 'received_at': int(time.time())}
    post_webhook(WHATSAPP_WEBHOOK_URL, payload)
    post_webhook(CRM_WEBHOOK_URL, payload)
    return jsonify(ok=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', '8000')))
