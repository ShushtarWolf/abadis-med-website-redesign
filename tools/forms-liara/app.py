"""Abadis Med forms backend for Liara (Flask).

Receives the static site's contact, cooperation, export-quote and solution
forms and emails them to info@abadis-med.com (or FORM_TO). Secrets stay in
environment variables. Spam: honeypot `_gotcha` plus a per-IP rate limit.
"""
import os, re, smtplib, ssl, threading, time
from email.message import EmailMessage
from flask import Flask, request, jsonify

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = int(os.environ.get('MAX_UPLOAD_MB', '8')) * 1024 * 1024

def _env(*keys):
    for key in keys:
        value = os.environ.get(key, '').strip()
        if value:
            return value
    return ''

ALLOWED_ORIGINS = [o.strip() for o in os.environ.get(
    'ALLOWED_ORIGINS', 'https://abadis-med.com,https://www.abadis-med.com').split(',') if o.strip()]
SMTP_HOST = os.environ.get('SMTP_HOST', '')
SMTP_PORT = int(os.environ.get('SMTP_PORT', '587'))
SMTP_USER = os.environ.get('SMTP_USER', '')
SMTP_PASS = os.environ.get('SMTP_PASS', '')
SMTP_TLS = os.environ.get('SMTP_TLS', 'starttls')  # starttls | ssl | none
MAIL_FROM = _env('MAIL_FROM', 'SMTP_USER') or SMTP_USER
MAIL_TO = _env('FORM_TO', 'MAIL_TO')
MAIL_TO_CONTACT = _env('FORM_TO_CONTACT', 'MAIL_TO_CONTACT')
MAIL_TO_CAREERS = _env('FORM_TO_CAREERS', 'MAIL_TO_CAREERS')
MAIL_TO_EXPORT = _env('FORM_TO_EXPORT', 'MAIL_TO_EXPORT')
RATE_PER_MIN = int(os.environ.get('RATE_PER_MIN', '5'))
MAX_FIELD = int(os.environ.get('MAX_FIELD_CHARS', '4000'))

SKIP = {'_gotcha', 'form_name'}
KNOWN = {'contact', 'careers', 'export', 'quote', 'solution'}
REQUIRED = {
    'contact': ['name', 'phone'],
    'careers': [
        'عنوان شغلی', 'نام', 'نام خانوادگی', 'نام پدر', 'وضعیت نظام وظیفه',
        'تاریخ تولد', 'محل تولد', 'شماره شناسنامه', 'محل صدور', 'وضعیت تاهل',
        'بیماری خاص یا سابقه بستری', 'تلفن ثابت', 'تلفن همراه', 'آدرس محل سکونت',
        'سوابق تحصیلی — مقطع تحصیلی', 'سوابق تحصیلی — نام موسسه آموزشی',
        'سوابق تحصیلی — نوع مدرک آموزشی', 'سوابق تحصیلی — نام گرایش یا رشته',
        'سوابق تحصیلی — زمان آموزش (شروع - خاتمه)', 'سوابق تحصیلی — معدل',
        'سوابق کاری — نام سازمان', 'سوابق کاری — عنوان شغل',
        'سوابق کاری — مدت همکاری(شروع-خاتمه)', 'سوابق کاری — آخرین دریافتی',
        'سوابق کاری — نام مدیر', 'سوابق کاری — تلفن تماس', 'سوابق کاری — علت قطع همکاری',
        'شغل فعلی — نام سازمان', 'شغل فعلی — عنوان شغل',
        'شغل فعلی — مدت همکاری(شروع-خاتمه)', 'شغل فعلی — آخرین دریافتی',
        'شغل فعلی — نام مدیر', 'شغل فعلی — تلفن تماس', 'شغل فعلی — علت قطع همکاری',
        'آخرین حقوق دریافتی', 'حقوق درخواستی', 'طریق مراجعه به شرکت جهت استخدام',
        'آشنایی با کامپیوتر — نوع نرم افزار',
        'آشنایی با کامپیوتر — میزان آشنایی (متوسط-خوب-عالی)',
        'آشنایی با کامپیوتر — توضیحات',
    ],
    'export': ['name', 'company', 'country', 'email', 'product'],
    'quote': ['name', 'company', 'country', 'email', 'product'],
    'solution': ['dept', 'system', 'center', 'person', 'phone'],
}
EMAIL_KEYS = {'email'}
PHONE_KEYS = {'phone', 'تلفن ثابت', 'تلفن همراه', 'سوابق کاری — تلفن تماس', 'شغل فعلی — تلفن تماس'}
SUBJECTS = {
    'contact': 'Contact form',
    'careers': 'Cooperation application',
    'export': 'Export quote',
    'quote': 'Export quote',
    'solution': 'Solution request',
}
EMAIL_RE = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')
_hits = {}
_lock = threading.Lock()


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
    with _lock:
        if len(_hits) > 5000:
            stale = [k for k, vals in _hits.items() if not vals or now - vals[-1] >= 60]
            for k in stale:
                _hits.pop(k, None)
        hits = [t for t in _hits.get(ip, []) if now - t < 60]
        hits.append(now)
        _hits[ip] = hits
        return len(hits) > RATE_PER_MIN


def recipient_for(form_name):
    key = (form_name or '').strip().lower()
    specific = {
        'contact': MAIL_TO_CONTACT,
        'careers': MAIL_TO_CAREERS,
        'export': MAIL_TO_EXPORT,
        'quote': MAIL_TO_EXPORT,
        'solution': MAIL_TO_CONTACT,
    }.get(key, '')
    return specific or MAIL_TO


def digits(value):
    trans = str.maketrans('۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩', '01234567890123456789')
    return ''.join(ch for ch in value.translate(trans) if ch.isdigit())


def joined(form, key):
    return ', '.join(v.strip() for v in form.getlist(key) if v and v.strip())


def validate(form):
    name = (form.get('form_name') or '').strip().lower()
    errors = {}
    if name not in KNOWN:
        errors['form_name'] = 'invalid'
        return name, errors
    for key in form.keys():
        if key in SKIP:
            continue
        for value in form.getlist(key):
            if len(value) > MAX_FIELD:
                errors[key] = 'invalid'
    for key in REQUIRED[name]:
        if not joined(form, key):
            errors[key] = 'required'
    for key in EMAIL_KEYS:
        value = joined(form, key)
        if value and not EMAIL_RE.match(value):
            errors[key] = 'email'
    for key in PHONE_KEYS:
        value = joined(form, key)
        if not value:
            continue
        if len(digits(value)) < 6:
            errors[key] = 'phone'
    return name, errors


def send_mail(subject, body, files, reply_to, to):
    if not SMTP_HOST:
        raise RuntimeError('SMTP_HOST not set')
    dest = (to or '').strip()
    if not dest:
        raise RuntimeError('FORM_TO not set')
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = MAIL_FROM or dest
    msg['To'] = dest
    if reply_to and EMAIL_RE.match(reply_to):
        msg['Reply-To'] = reply_to
    msg.set_content(body)
    for f in files:
        data = f.read()
        if not data:
            continue
        maintype, _, subtype = (f.mimetype or 'application/octet-stream').partition('/')
        filename = os.path.basename(f.filename or 'attachment')[:180] or 'attachment'
        msg.add_attachment(data, maintype=maintype or 'application', subtype=subtype or 'octet-stream', filename=filename)
    ctx = ssl.create_default_context()
    if SMTP_TLS == 'ssl':
        smtp = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=ctx, timeout=12)
    else:
        smtp = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=12)
        if SMTP_TLS == 'starttls':
            smtp.starttls(context=ctx)
    with smtp:
        if SMTP_USER:
            smtp.login(SMTP_USER, SMTP_PASS)
        smtp.send_message(msg)


def body_of(form, ip, origin):
    lines = []
    for key in form.keys():
        if key in SKIP:
            continue
        value = joined(form, key)
        if value:
            lines.append(f'{key}: {value}')
    lines.append('')
    lines.append(f'IP: {ip}')
    lines.append(f'Origin: {origin}')
    return '\n'.join(lines)


@app.get('/health')
def health():
    return jsonify(ok=True, smtp=bool(SMTP_HOST and MAIL_TO))


@app.route('/submit', methods=['POST', 'OPTIONS'])
def submit():
    if request.method == 'OPTIONS':
        return ('', 204)
    origin = request.headers.get('Origin', '')
    if origin and origin not in ALLOWED_ORIGINS:
        return jsonify(ok=False, error='origin'), 403
    ip = request.headers.get('X-Forwarded-For', request.remote_addr or '').split(',')[0].strip()
    if limited(ip):
        return jsonify(ok=False, error='rate'), 429
    form = request.form
    if (form.get('_gotcha') or '').strip():
        return jsonify(ok=True)
    name, errors = validate(form)
    if errors:
        return jsonify(ok=False, error='validation', fields=errors), 400
    lang = (form.get('lang') or '').strip()[:8]
    subject = f'[abadis-med.com] {SUBJECTS.get(name, name)}'
    if lang:
        subject += f' ({lang})'
    topic = joined(form, 'topic') or joined(form, 'company') or joined(form, 'center') or joined(form, 'عنوان شغلی')
    if topic:
        subject += ' — ' + topic[:80]
    reply = joined(form, 'email')
    try:
        send_mail(subject, body_of(form, ip, origin), list(request.files.values()), reply, recipient_for(name))
    except Exception as exc:
        app.logger.error('mail failed: %s', type(exc).__name__)
        return jsonify(ok=False, error='mail'), 502
    return jsonify(ok=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', '8000')))
