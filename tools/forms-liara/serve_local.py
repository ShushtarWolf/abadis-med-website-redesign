"""Local form backend plus a debugging SMTP server. Not used in production."""
import os
os.environ.setdefault('SMTP_HOST', '127.0.0.1')
os.environ.setdefault('SMTP_PORT', '1025')
os.environ.setdefault('SMTP_TLS', 'none')
os.environ.setdefault('MAIL_FROM', 'forms@example.com')
os.environ.setdefault('FORM_TO', 'info@abadis-med.com')
os.environ.setdefault('ALLOWED_ORIGINS', 'http://127.0.0.1:8080,http://localhost:8080')
os.environ.setdefault('RATE_PER_MIN', '200')

from test_local import DebugSMTP
import app

def main():
    smtp = DebugSMTP('127.0.0.1', int(os.environ['SMTP_PORT']))
    smtp.start()
    smtp.ready.wait(3)
    print('smtp ready', flush=True)
    app.app.run(host='127.0.0.1', port=int(os.environ.get('PORT', '8000')), threaded=True)

if __name__ == '__main__':
    main()
