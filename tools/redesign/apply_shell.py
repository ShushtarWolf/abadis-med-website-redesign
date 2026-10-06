"""Re-apply the shared header/footer (incl. phase-2 footer column) to the hand-built pages."""
import re, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from lib import SITE
from layout import header, footer
from lib import internal
import pages_posts; pages_posts.prepare()
def relink(s, p):
    def sub(m):
        i = internal(m.group(1))
        if i is None: return m.group(0)
        return f'href="{p}{i}"' if i else f'href="{p or "./"}"'
    return re.sub(r'href="(https://(?:www\.)?abadis-med\.com/[^"]*)"(?: target="_blank")?(?: rel="noopener")?', sub, s)
HAND = {'index.html': ('', None), 'products/suction-bag/index.html': ('../../', 'products'),
        'csr/index.html': ('../', 'csr'), 'contact/index.html': ('../', 'contact')}
for rel, (p, cur) in HAND.items():
    f = SITE / rel; s = f.read_text(encoding='utf-8')
    s, a = re.subn(r'<header class="header[^"]*" id="header">.*?</header>', lambda m: header(p, cur), s, count=1, flags=re.S)
    s, b = re.subn(r'<footer class="site-footer">.*?</footer>', lambda m: footer(p, cur), s, count=1, flags=re.S)
    # internal links that used to point at the live site
    s = s.replace('https://abadis-med.com/راهنمای-نصب/راهنمای-استفاده-کاربر-نهایی/" target="_blank" rel="noopener"', f'{p}install-guide/end-user/"')
    s = s.replace('href="https://abadis-med.com/محصولات/کیسه-ساکشن/" target="_blank" rel="noopener">صفحه محصول در سایت آبادیس</a>', f'href="{p}downloads/">مرکز دانلود</a>')
    s = s.replace('href="https://abadis-med.com/محصولات/فیلترها/" target="_blank" rel="noopener">مشاهده فیلترها در سایت آبادیس ←</a>', f'href="{p}products/filters/">مشاهده صفحه فیلترها ←</a>')
    s = relink(s, p)
    f.write_text(s, encoding='utf-8'); print(rel, a, b)
