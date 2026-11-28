"""Open each delivery form in FA/EN/AR, submit it to the local backend, and save screenshots."""
import json
import urllib.error
import urllib.request
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path('/agent/repos/abadis-med-website-redesign/docs/screenshots/forms')
OUT.mkdir(parents=True, exist_ok=True)
BASE = 'http://127.0.0.1:8080'
CHROME = '/usr/local/bin/google-chrome'
PAGES = [
    ('contact', 'fa', '/ارتباط-با-ما/', '#leadForm', False),
    ('contact', 'en', '/en/contact-us/', '#leadForm', False),
    ('contact', 'ar', '/arabic/اتصل-بنا/', '#leadForm', False),
    ('cooperation', 'fa', '/فرصت-های-همکاری/', '#c1-form', False),
    ('cooperation', 'en', '/en/collaboration-opportunities/', '#c1-form', False),
    ('cooperation', 'ar', '/arabic/careers/', '#c1-form', False),
    ('export', 'fa', '/export/', '#quote', False),
    ('export', 'en', '/en/export/', '#quote', False),
    ('export', 'ar', '/arabic/export/', '#quote', False),
    ('solution', 'fa', '/solutions/airway-care/', '[data-sol-form]', True),
    ('solution', 'en', '/en/solutions/airway-care/', '[data-sol-form]', True),
    ('solution', 'ar', '/arabic/الحلول/airway-care/', '[data-sol-form]', True),
]
FILL = """
(sel) => {
  const form = document.querySelector(sel);
  form.querySelectorAll('input, select, textarea').forEach((el) => {
    if (!el.name || el.name === '_gotcha' || el.type === 'hidden') return;
    if (el.type === 'checkbox' || el.type === 'radio') { el.checked = false; return; }
    if (el.tagName === 'SELECT') {
      const opt = Array.from(el.options).find((o) => o.value);
      if (opt) el.value = opt.value;
      return;
    }
    const name = el.name || '';
    if (el.type === 'email') el.value = 'buyer@example.com';
    else if (el.type === 'tel' || name === 'phone' || name.indexOf('تلفن') !== -1) el.value = '02192001017';
    else if (el.dataset && 'numMin' in el.dataset) el.value = '3';
    else if (name.indexOf('شناسنامه') !== -1) el.value = '1234567890';
    else el.value = 'آزمایش';
    el.dispatchEvent(new Event('input', { bubbles: true }));
    el.dispatchEvent(new Event('change', { bubbles: true }));
  });
}
"""

def shoot(page, name):
    page.screenshot(path=str(OUT / name), type='jpeg', quality=60)


def run_forms(browser):
    for width, height, tag in ((1440, 900, '1440'), (390, 844, '390')):
        context = browser.new_context(viewport={'width': width, 'height': height}, locale='fa-IR')
        page = context.new_page()
        def forward(route):
            req = route.request
            origin = req.headers.get('origin', 'http://127.0.0.1:8080')
            cors = {
                'Access-Control-Allow-Origin': origin,
                'Access-Control-Allow-Headers': 'Content-Type, Accept',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
            }
            if req.method == 'OPTIONS':
                route.fulfill(status=204, headers=cors)
                return
            upstream = urllib.request.Request(
                'http://127.0.0.1:8000/submit',
                data=req.post_data_buffer,
                headers={
                    'Content-Type': req.headers.get('content-type', ''),
                    'Origin': origin,
                    'Accept': 'application/json',
                },
                method='POST',
            )
            try:
                with urllib.request.urlopen(upstream, timeout=15) as resp:
                    body, status = resp.read(), resp.status
            except urllib.error.HTTPError as exc:
                body, status = exc.read(), exc.code
            route.fulfill(status=status, content_type='application/json', body=body, headers=cors)
        page.route('https://abadis-forms.liara.run/**', forward)
        for kind, lang, path, sel, dialog in PAGES:
            page.goto(BASE + path, wait_until='load', timeout=60000)
            page.wait_for_timeout(300)
            page.evaluate("""() => {
              document.querySelectorAll('.consent-bar, .lang-suggest, .abadis-chat-launcher').forEach((el) => el.remove());
            }""")
            if dialog:
                page.evaluate("""() => {
                  const d = document.getElementById('sol-config');
                  if (d && d.showModal) d.showModal();
                }""")
                page.wait_for_selector(sel, state='visible')
            else:
                page.eval_on_selector(sel, """(el) => {
                  document.documentElement.style.scrollBehavior = 'auto';
                  const field = el.querySelector('.cf-pane-head, .qf-grid, h2') || el;
                  const y = field.getBoundingClientRect().top + window.scrollY - 96;
                  window.scrollTo(0, Math.max(0, y));
                }""")
                page.wait_for_timeout(250)
            shoot(page, f'{kind}-{lang}-{tag}-form.jpg')
            page.evaluate(FILL, sel)
            page.evaluate("""(sel) => {
              const form = document.querySelector(sel);
              const tabs = form.querySelectorAll('[data-step-btn]');
              if (tabs.length) tabs[tabs.length - 1].click();
            }""", sel)
            page.evaluate("(sel) => document.querySelector(sel).requestSubmit()", sel)
            try:
                page.wait_for_selector(sel + ' .form-status.is-success', timeout=15000)
                page.eval_on_selector(sel + ' .form-status.is-success', """(el) => {
                  document.documentElement.style.scrollBehavior = 'auto';
                  el.scrollIntoView({ block: 'center', behavior: 'auto' });
                }""")
            except Exception:
                info = page.evaluate("""(sel) => {
                  const form = document.querySelector(sel);
                  const status = form && form.querySelector('.form-status');
                  const bad = form ? Array.from(form.querySelectorAll('.is-invalid')).map((el) => el.name) : [];
                  return { status: status ? status.textContent : '', bad: bad };
                }""", sel)
                raise SystemExit(f'no success {kind} {lang} {tag} {info}')
            page.wait_for_timeout(250)
            shoot(page, f'{kind}-{lang}-{tag}-success.jpg')
            print('ok', kind, lang, tag, flush=True)
        context.close()


def ga_log(browser):
    lines = []
    def watch(page, label):
        hits = []
        page.on('request', lambda req: hits.append(req.url) if ('googletagmanager.com' in req.url or 'google-analytics.com' in req.url or 'gtag/js' in req.url) else None)
        return hits
    # Real build: measurement ID is empty.
    context = browser.new_context(viewport={'width': 1440, 'height': 900})
    page = context.new_page()
    hits = watch(page, 'empty')
    page.goto(BASE + '/en/contact-us/', wait_until='domcontentloaded')
    page.wait_for_timeout(300)
    before = list(hits)
    page.click('.consent-accept')
    page.wait_for_timeout(500)
    lines.append('EMPTY_ID before accept: ' + json.dumps(before))
    lines.append('EMPTY_ID after accept: ' + json.dumps(hits))
    context.close()

    context = browser.new_context(viewport={'width': 1440, 'height': 900})
    page = context.new_page()
    hits = watch(page, 'reject')
    page.goto(BASE + '/en/contact-us/', wait_until='domcontentloaded')
    page.click('.consent-reject')
    page.wait_for_timeout(500)
    lines.append('EMPTY_ID after reject: ' + json.dumps(hits))
    context.close()

    # Throwaway id, only inside this browser session, to prove the consent gate.
    def swap(route):
        body = route.fetch().text()
        body = body.replace("var ABADIS_GA_MEASUREMENT_ID = '';", "var ABADIS_GA_MEASUREMENT_ID = 'G-TESTPLACE';", 1)
        route.fulfill(status=200, content_type='application/javascript', body=body)
    for choice, expect in (('reject', False), ('accept', True)):
        context = browser.new_context(viewport={'width': 1440, 'height': 900})
        page = context.new_page()
        page.route('**/assets/js/site.js*', swap)
        page.route('https://www.googletagmanager.com/**', lambda route: route.fulfill(status=200, content_type='application/javascript', body=''))
        hits = []
        page.on('request', lambda req: hits.append(req.url) if 'googletagmanager' in req.url or 'google-analytics' in req.url else None)
        page.goto(BASE + '/en/contact-us/', wait_until='domcontentloaded')
        page.wait_for_timeout(300)
        pre = list(hits)
        page.click('.consent-' + choice)
        page.wait_for_timeout(600)
        lines.append(f'GATE {choice} before click: ' + json.dumps(pre))
        lines.append(f'GATE {choice} after click: ' + json.dumps(hits))
        if expect and not any('G-TESTPLACE' in u for u in hits):
            raise SystemExit('GA did not load after accept')
        if not expect and hits:
            raise SystemExit('GA loaded after reject: ' + repr(hits))
        if choice == 'accept' and pre:
            raise SystemExit('GA loaded before accept')
        context.close()
    text = '\n'.join(lines) + '\n'
    (OUT / 'ga-network.log').write_text(text, encoding='utf-8')
    print(text)


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME, headless=True, args=['--no-sandbox', '--disable-dev-shm-usage'])
        run_forms(browser)
        ga_log(browser)
        browser.close()

if __name__ == '__main__':
    main()
