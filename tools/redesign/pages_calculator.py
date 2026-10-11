"""Calculator: abadismedit's redesign drafts (redesign/calculator/, merged from team-assets-2026-10-06)
adapted into the site shell. Their page CSS is scoped under .gfc (and `dark` rules also apply to noir),
their header/footer/theme toggle are replaced by ours. Formulas are untouched (redesign/calculator/js/calc.js,
common/abadis-common.js) and match the live GFCalc formulas."""
import re, shutil, pathlib
from lib import ROOT, SITE
from layout import page

SRC = ROOT / 'redesign' / 'calculator'
DESC = 'محاسبه‌گر صرفه‌جویی آبادیس: صرفه‌جویی در مصرف آب، هزینه شست‌وشو و ضدعفونی و زمان کادر درمان.'
VARIANTS = [('dial', 'طرح دایال'), ('receipt', 'طرح رسید'), ('hospital', 'طرح بیمارستان'), ('scale', 'طرح ترازو'), ('flood', 'طرح سیلاب')]
# Extra dial pages shipped on main (site/dial-*, site/template-dials/*) — link only, leave pages as-is.
EXTRA_DIALS = [
    ('dial-practical/', 'دایال عملی'),
    ('dial-steppers/', 'دایال +/−'),
    ('template-dials/1-neumorphic/', 'دایال نیومورفیک'),
    ('template-dials/2-abadis-plus/', 'دایال آبادیس+'),
    ('template-dials/3-cost-time-h2o/', 'دایال COST/TIME'),
]
THEME_DARK = '[data-theme="dark"]'
THEME_ANY_DARK = ':is([data-theme="dark"],[data-theme="noir"])'
DROP = re.compile(r'(^|[\s,>+~(])(\.header\b|\.nav\b|\.logo\b|\.theme-toggle|\.header-cta|\.header-actions|\.site-footer|\.foot-(inner|brand|links|copy)\b|footer\b|\.i-sun|\.i-moon)')
RENAME = {'hero': 'gfc-hero'}   # .hero is a "dark" tone class in site.js; their hero is light

# ---------------------------------------------------------------- tiny CSS scoper
def _blocks(css):
    """yield (prelude, body) for top-level blocks; body is the text inside the braces."""
    i, n = 0, len(css)
    while i < n:
        j = css.find('{', i)
        if j < 0: break
        depth, k, q = 1, j + 1, None
        while k < n and depth:
            c = css[k]
            if q:
                if c == q and css[k - 1] != '\\': q = None
            elif c in '"\'': q = c
            elif c == '{': depth += 1
            elif c == '}': depth -= 1
            k += 1
        yield css[i:j].strip(), css[j + 1:k - 1]
        i = k

def _split_sel(s):
    out, depth, cur = [], 0, ''
    for c in s:
        if c == '(': depth += 1
        elif c == ')': depth -= 1
        if c == ',' and depth == 0: out.append(cur.strip()); cur = ''
        else: cur += c
    if cur.strip(): out.append(cur.strip())
    return out

ROOTLIKE = re.compile(r'^(?:html|:root|body)?(?P<t>' + re.escape(THEME_ANY_DARK) + r')?(?:\s+(?:html|body))?$')
def _scope_sel(s):
    if DROP.search(s): return None
    for a, b in RENAME.items(): s = re.sub(r'\.' + a + r'(?![\w-])', '.' + b, s)
    s = s.replace(THEME_DARK, THEME_ANY_DARK)
    m = ROOTLIKE.match(s)
    if m and s: return (m.group('t') + ' .gfc') if m.group('t') else '.gfc'
    if s == '*': return '.gfc *'
    pe = ''
    m = re.match(r'^(.*?)(::[\w-]+(?:\([^)]*\))?)$', s)
    if m: s, pe = m.group(1), m.group(2)
    return '.gfc :is(' + s + ')' + pe

def scope_css(css, kf):
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    out = []
    for pre, body in _blocks(css):
        if pre.startswith('@font-face'): continue
        if pre.startswith('@keyframes'):
            name = pre.split()[1]; kf.add(name)
            out.append(f'@keyframes gfc-{name} {{{body}}}'); continue
        if pre.startswith('@media') or pre.startswith('@supports'):
            inner = scope_css(body, kf)
            if inner.strip(): out.append(f'{pre} {{\n{inner}\n}}')
            continue
        sels = [x for x in (_scope_sel(s) for s in _split_sel(pre)) if x]
        if sels: out.append(', '.join(sels) + ' {' + body.strip() + '}')
    return '\n'.join(out)

def fix_keyframes(css, kf):
    def decl(m):
        d = m.group(0)
        for k in kf: d = re.sub(r'(?<![\w-])' + re.escape(k) + r'(?![\w-])', 'gfc-' + k, d)
        return d
    return re.sub(r'animation(?:-name)?\s*:[^;}]*', decl, css)

# ---------------------------------------------------------------- HTML adaptation
def adapt(html, p, here):
    styles = re.findall(r'<style>(.*?)</style>', html, re.S)
    links = re.findall(r'<link rel="stylesheet" href="([^"]+)"', html)
    css = ''
    for l in links: css += (SRC / here / l).resolve().read_text(encoding='utf-8') + '\n'
    css += '\n'.join(styles)
    kf = set(); scoped = fix_keyframes(scope_css(css, kf), kf)
    body = html[html.index('<body>') + 6: html.rindex('</body>')]
    body = re.sub(r'\s*<header class="header".*?</header>', '', body, flags=re.S)
    body = re.sub(r'\s*<footer\b.*?</footer>', '', body, flags=re.S)
    scripts = re.findall(r'<script src="([^"]+)"[^>]*></script>', body)
    body = re.sub(r'\s*<script src="[^"]+"[^>]*></script>', '', body)
    def cls(m):
        toks = [RENAME.get(t, t) for t in m.group(1).split()]
        return 'class="' + ' '.join(toks) + '"'
    body = re.sub(r'class="([^"]*)"', cls, body)
    body = body.replace('class="calc calc--dark"', 'class="calc calc--dark" data-tone="dark"')
    body = re.sub(r'href="https://abadis-med\.com/ارتباط-با-ما/" target="_blank" rel="noopener"', f'href="{p}contact/"', body)
    return scoped, body, scripts

def switcher(p, cur):
    items = [('', 'طرح اصلی')] + [(k + '/', v) for k, v in VARIANTS]
    a = ''.join(f'<a href="{p}calculator/{h}"' + (' aria-current="page"' if h == cur else '') + f'>{t}</a>' for h, t in items)
    extras = ''.join(f'<a href="{p}{h}">{t}</a>' for h, t in EXTRA_DIALS)
    return f'<nav class="gfc-switch" aria-label="طرح‌های محاسبه‌گر"><span>طرح‌های محاسبه‌گر:</span>{a}{extras}</nav>'

JS_CUTS = [  # their own header/theme handling: replaced by site.js (keeps noir + our header)
    (r"\n  /\* ---------- template header \+ anchors ---------- \*/.*?\n  \}\)\(\);\n(?=\}\)\(\);)", '\n'),
    (r"\n  /\* header \+ anchors \*/.*?(?=\n  window\.Abadis = A;)", '\n'),
]
def patch_js(src, dst):
    s = src.read_text(encoding='utf-8'); n0 = len(s)
    for a, b in JS_CUTS: s = re.sub(a, b, s, flags=re.S)
    assert len(s) < n0, src
    dst.parent.mkdir(parents=True, exist_ok=True); dst.write_text(s, encoding='utf-8')

def build(write):
    out = SITE / 'calculator'
    patch_js(SRC / 'js' / 'calc.js', out / 'calc.js')
    patch_js(SRC / 'common' / 'abadis-common.js', out / 'common' / 'abadis-common.js')
    if (out / 'flood' / 'img').exists(): shutil.rmtree(out / 'flood' / 'img')
    shutil.copytree(SRC / 'flood' / 'img', out / 'flood' / 'img')
    pages = [('', 'calculator/index.html', '../', 'محاسبه‌گر صرفه‌جویی')] + \
            [(k + '/', f'calculator/{k}/index.html', '../../', f'محاسبه‌گر صرفه‌جویی — {v}') for k, v in VARIANTS]
    for here, rel, p, title in pages:
        html = (SRC / here / 'index.html').read_text(encoding='utf-8')
        css, body, scripts = adapt(html, p, here)
        (SITE / rel).parent.mkdir(parents=True, exist_ok=True)
        (SITE / rel).parent.joinpath('calc.css' if here else 'calc-page.css').write_text(css + '\n', encoding='utf-8')
        cssname = 'calc.css' if here else 'calc-page.css'
        sw = switcher(p, here)
        main = f'<link rel="stylesheet" href="{cssname}">\n<div class="gfc">\n{body}\n{sw}\n</div>'
        js = ''.join(f'<script src="{s}" defer></script>\n' for s in
                     [('calc.js' if s.endswith('js/calc.js') else ('../common/abadis-common.js' if 'common' in s else s)) for s in scripts])
        # variant pages carry inline <script> blocks that need Abadis loaded first: keep their order
        if here:
            inline = re.findall(r'<script>.*?</script>', main, re.S)
            for blk in inline: main = main.replace(blk, '')
            js = '<script src="../common/abadis-common.js"></script>\n' + ''.join(inline) + '\n'
        write(rel, page(p, 'calculator', title, DESC, main, scripts=js))
