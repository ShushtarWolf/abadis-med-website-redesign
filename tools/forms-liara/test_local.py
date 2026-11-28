"""Post one valid message per form to a local debugging SMTP server."""
import os, socket, threading
from email import message_from_bytes

os.environ.setdefault('SMTP_HOST', '127.0.0.1')
os.environ.setdefault('SMTP_PORT', '1025')
os.environ.setdefault('SMTP_TLS', 'none')
os.environ.setdefault('SMTP_USER', '')
os.environ.setdefault('SMTP_PASS', '')
os.environ.setdefault('MAIL_FROM', 'forms@example.com')
os.environ.setdefault('FORM_TO', 'info@abadis-med.com')
os.environ.setdefault('ALLOWED_ORIGINS', 'http://127.0.0.1:8080,http://localhost:8080')
os.environ.setdefault('RATE_PER_MIN', '30')

import app as forms_app  # noqa: E402


class DebugSMTP(threading.Thread):
    def __init__(self, host, port):
        super().__init__(daemon=True)
        self.host, self.port = host, port
        self.messages = []
        self.ready = threading.Event()
        self._stop = threading.Event()
        self._sock = None

    def run(self):
        srv = socket.socket()
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((self.host, self.port))
        srv.listen(8)
        srv.settimeout(0.5)
        self._sock = srv
        self.ready.set()
        while not self._stop.is_set():
            try:
                conn, _ = srv.accept()
            except socket.timeout:
                continue
            threading.Thread(target=self._session, args=(conn,), daemon=True).start()

    def _session(self, conn):
        conn.settimeout(10)
        buf = b''
        data_mode = False
        lines = []

        def send(text):
            conn.sendall(text.encode('ascii'))

        def handle(line):
            nonlocal data_mode
            raw = line.rstrip('\r\n')
            if data_mode:
                if raw == '.':
                    data_mode = False
                    self.messages.append('\n'.join(lines).encode('utf-8', 'replace'))
                    lines.clear()
                    send('250 ok\r\n')
                else:
                    lines.append(raw[1:] if raw.startswith('..') else raw)
                return
            cmd = raw.split(' ', 1)[0].upper()
            if cmd in ('EHLO', 'HELO'):
                send('250-localhost\r\n250 OK\r\n')
            elif cmd == 'MAIL':
                send('250 ok\r\n')
            elif cmd == 'RCPT':
                send('250 ok\r\n')
            elif cmd == 'DATA':
                data_mode = True
                send('354 go\r\n')
            elif cmd == 'RSET':
                lines.clear()
                send('250 ok\r\n')
            elif cmd == 'QUIT':
                send('221 bye\r\n')
                conn.close()
            else:
                send('250 ok\r\n')

        send('220 localhost debug\r\n')
        try:
            while True:
                chunk = conn.recv(8192)
                if not chunk:
                    break
                buf += chunk
                while b'\n' in buf:
                    line, buf = buf.split(b'\n', 1)
                    handle(line.decode('utf-8', 'replace') + '\n')
        except OSError:
            pass

    def stop(self):
        self._stop.set()
        if self._sock:
            self._sock.close()


def careers_payload(lang):
    fields = {
        'form_name': 'careers', 'lang': lang, 'page': f'/{lang}/careers',
        'عنوان شغلی': 'Sales', 'نام': 'Test', 'نام خانوادگی': 'User', 'نام پدر': 'Ali',
        'وضعیت نظام وظیفه': 'done', 'تاریخ تولد': '1370/01/01', 'محل تولد': 'Tehran',
        'شماره شناسنامه': '1234567890', 'محل صدور': 'Tehran', 'وضعیت تاهل': 'Single',
        'بیماری خاص یا سابقه بستری': 'No', 'تلفن ثابت': '02192001017', 'تلفن همراه': '09100145809',
        'آدرس محل سکونت': 'Tehran',
        'سوابق تحصیلی — مقطع تحصیلی': 'BSc', 'سوابق تحصیلی — نام موسسه آموزشی': 'UT',
        'سوابق تحصیلی — نوع مدرک آموزشی': 'degree', 'سوابق تحصیلی — نام گرایش یا رشته': 'engineering',
        'سوابق تحصیلی — زمان آموزش (شروع - خاتمه)': '2010-2014', 'سوابق تحصیلی — معدل': '17',
        'سوابق کاری — نام سازمان': 'Org', 'سوابق کاری — عنوان شغل': 'Sales',
        'سوابق کاری — مدت همکاری(شروع-خاتمه)': '2015-2020', 'سوابق کاری — آخرین دریافتی': '1',
        'سوابق کاری — نام مدیر': 'M', 'سوابق کاری — تلفن تماس': '02100000000',
        'سوابق کاری — علت قطع همکاری': 'move',
        'شغل فعلی — نام سازمان': 'Now', 'شغل فعلی — عنوان شغل': 'Rep',
        'شغل فعلی — مدت همکاری(شروع-خاتمه)': '2020-', 'شغل فعلی — آخرین دریافتی': '1',
        'شغل فعلی — نام مدیر': 'M', 'شغل فعلی — تلفن تماس': '02100000001',
        'شغل فعلی — علت قطع همکاری': 'n/a',
        'آخرین حقوق دریافتی': '1', 'حقوق درخواستی': '2',
        'طریق مراجعه به شرکت جهت استخدام': 'website',
        'آشنایی با کامپیوتر — نوع نرم افزار': 'Excel',
        'آشنایی با کامپیوتر — میزان آشنایی (متوسط-خوب-عالی)': 'good',
        'آشنایی با کامپیوتر — توضیحات': 'daily',
    }
    return fields


CASES = [
    ('contact-fa', {'form_name': 'contact', 'lang': 'fa', 'name': 'آزمایش', 'phone': '۰۲۱۹۲۰۰۱۰۱۷', 'topic': 'نمایندگی و همکاری', 'msg': 'سلام'}),
    ('contact-en', {'form_name': 'contact', 'lang': 'en', 'name': 'Test User', 'phone': '+982192001017', 'topic': 'Dealership & Cooperation', 'msg': 'Hello'}),
    ('contact-ar', {'form_name': 'contact', 'lang': 'ar', 'name': 'اختبار', 'phone': '02192001017', 'topic': 'الوكالة والتعاون', 'msg': 'مرحبا'}),
    ('careers-fa', careers_payload('fa')),
    ('careers-en', careers_payload('en')),
    ('careers-ar', careers_payload('ar')),
    ('export-fa', {'form_name': 'export', 'lang': 'fa', 'name': 'صادرات', 'company': 'بیمارستان', 'country': 'عراق', 'email': 'buyer@example.com', 'product': 'کیسه ساکشن ۱ لیتری'}),
    ('export-en', {'form_name': 'export', 'lang': 'en', 'name': 'Export', 'company': 'Clinic', 'country': 'Oman', 'email': 'buyer@example.com', 'product': '1 L'}),
    ('export-ar', {'form_name': 'export', 'lang': 'ar', 'name': 'تصدير', 'company': 'مستشفى', 'country': 'عمان', 'email': 'buyer@example.com', 'product': '١ لتر'}),
    ('solution-fa', {'form_name': 'solution', 'lang': 'fa', 'dept': 'اتاق عمل', 'system': 'ساکشن مرکزی', 'center': 'مرکز', 'person': 'درخواست', 'phone': '09100145809'}),
    ('solution-en', {'form_name': 'solution', 'lang': 'en', 'dept': 'OR', 'system': 'Central', 'center': 'City Hospital', 'person': 'Alex', 'phone': '+989100145809'}),
    ('solution-ar', {'form_name': 'solution', 'lang': 'ar', 'dept': 'العمليات', 'system': 'مركزي', 'center': 'المستشفى', 'person': 'سامي', 'phone': '09100145809'}),
]


def main():
    smtp = DebugSMTP('127.0.0.1', int(os.environ['SMTP_PORT']))
    smtp.start()
    smtp.ready.wait(3)
    client = forms_app.app.test_client()
    failures = []
    for label, payload in CASES:
        before = len(smtp.messages)
        res = client.post('/submit', data=payload, headers={'Origin': 'http://127.0.0.1:8080'})
        body = res.get_json(silent=True) or {}
        if res.status_code != 200 or not body.get('ok') or len(smtp.messages) != before + 1:
            failures.append((label, res.status_code, body))
            print('FAIL', label, res.status_code, body)
            continue
        msg = message_from_bytes(smtp.messages[-1])
        text = msg.get_payload(decode=True).decode('utf-8', 'replace')
        print('=' * 60)
        print(label)
        print('To:', msg['To'])
        print('Subject:', msg['Subject'])
        print(text.strip())
    honeypot = client.post('/submit', data={'form_name': 'contact', '_gotcha': 'spam', 'name': 'x', 'phone': '02192001017'},
                           headers={'Origin': 'http://127.0.0.1:8080'})
    bad = client.post('/submit', data={'form_name': 'contact', 'name': 'Only'}, headers={'Origin': 'http://127.0.0.1:8080'})
    print('=' * 60)
    print('honeypot', honeypot.status_code, honeypot.get_json(), 'messages', len(smtp.messages))
    print('missing phone', bad.status_code, bad.get_json())
    if honeypot.get_json().get('ok') is not True or len(smtp.messages) != len(CASES):
        failures.append(('honeypot', honeypot.status_code, honeypot.get_json()))
    if bad.status_code != 400 or 'phone' not in (bad.get_json() or {}).get('fields', {}):
        failures.append(('validation', bad.status_code, bad.get_json()))
    smtp.stop()
    if failures:
        raise SystemExit('failures: ' + repr(failures))
    print('OK', len(CASES), 'messages delivered to', os.environ['FORM_TO'])


if __name__ == '__main__':
    main()
