import os, shutil, glob, base64, io, zipfile
import cairosvg
from PIL import Image

BASE = '/workspace/section-logos'
FA_DIR = f'{BASE}/final-approved'
SITE_DIR = '/workspace/lw/site/brand/section-logos'
ZIP_DIR = f'{BASE}/zipd'
os.makedirs(FA_DIR, exist_ok=True)
os.makedirs(SITE_DIR, exist_ok=True)
os.makedirs(ZIP_DIR, exist_ok=True)

# 1. Read canonical teal SVGs
why_teal = open(f'{BASE}/r5/Q2-teal.svg').read()
calc_teal = open(f'{FA_DIR}/calculator-teal.svg').read()
calc_dark = open(f'{FA_DIR}/calculator-dark.svg').read()
sust_teal = open(f'{BASE}/r9/S9a-teal.svg').read()
zagros_teal = open(f'{BASE}/r7/Z1-teal.svg').read()

why_dark = why_teal.replace('#05686b', '#e6f3f3')
sust_dark = sust_teal.replace('#05686b', '#e6f3f3')
zagros_dark = zagros_teal.replace('#05686b', '#e6f3f3')

# Save in final-approved/
svg_map = {
    'why-teal.svg': why_teal,
    'why-dark.svg': why_dark,
    'Q2-teal.svg': why_teal,
    'calculator-teal.svg': calc_teal,
    'calculator-dark.svg': calc_dark,
    'sustainable-teal.svg': sust_teal,
    'sustainable-dark.svg': sust_dark,
    'S1-teal.svg': sust_teal,
    'S1-dark.svg': sust_dark,
    'zagros-teal.svg': zagros_teal,
    'zagros-dark.svg': zagros_dark,
    'Z1-teal.svg': zagros_teal,
}
for name, content in svg_map.items():
    open(f'{FA_DIR}/{name}', 'w').write(content)

# Render 400x400 PNGs in final-approved/
for stem, svg_str in [
    ('Q2', why_teal), ('why-teal', why_teal), ('why-dark', why_dark),
    ('calculator', calc_teal), ('calculator-teal', calc_teal), ('calculator-dark', calc_dark),
    ('S1', sust_teal), ('sustainable-teal', sust_teal), ('sustainable-dark', sust_dark),
    ('Z1', zagros_teal), ('zagros-teal', zagros_teal), ('zagros-dark', zagros_dark),
]:
    cairosvg.svg2png(bytestring=svg_str.encode(), write_to=f'{FA_DIR}/{stem}.png', output_width=400, output_height=400)

# 2. Update /workspace/lw/site/brand/section-logos/ and final.py / generate.py
# Ensure impact-sign.png and impact-sign-full.webp are in both ZIP_DIR and SITE_DIR
for fn in ('impact-sign.png', 'impact-sign-full.webp'):
    if os.path.exists(f'{ZIP_DIR}/{fn}') and not os.path.exists(f'{SITE_DIR}/{fn}'):
        shutil.copy2(f'{ZIP_DIR}/{fn}', f'{SITE_DIR}/{fn}')
    elif os.path.exists(f'{SITE_DIR}/{fn}'):
        shutil.copy2(f'{SITE_DIR}/{fn}', f'{ZIP_DIR}/{fn}')

# Load text shaping helper from gen.py
ns = {}
exec(open(f'{BASE}/gen.py').read().split("for k,(fa,en,_)")[0], ns)
text = ns['text']
T = '#05686b'

def strip_svg(s):
    return s.split('>', 1)[1].rsplit('</svg>', 1)[0]

b64_impact = base64.b64encode(open(f'{SITE_DIR}/impact-sign.png', 'rb').read()).decode()
IMG_BODY = f'<image href="data:image/png;base64,{b64_impact}" x="0" y="0" width="120" height="120" style="image-rendering:auto"/>'

sets = {
    'why': ('چرا آبادیس', 'Why Abadis', strip_svg(why_teal), strip_svg(why_dark)),
    'calculator': ('محاسبه گر', 'Calculator', strip_svg(calc_teal), strip_svg(calc_dark)),
    'sustainable': ('توسعه پایدار', 'Sustainable Development', strip_svg(sust_teal), strip_svg(sust_dark)),
    'zagros': ('نجات زاگرس', 'Save Zagros', strip_svg(zagros_teal), strip_svg(zagros_dark)),
    'impact': ('اثرگذاری', 'Impact', IMG_BODY, IMG_BODY),
}

for f in glob.glob(f'{SITE_DIR}/*.svg'):
    os.remove(f)

for k, (fa, en, v_light, v_dark) in sets.items():
    for m, vv, tc, ec in [('', v_light, T, '#5a7578'), ('-dark', v_dark, '#ffffff', '#9dbdbf')]:
        open(f'{SITE_DIR}/{k}-icon{m}.svg', 'w').write(
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="240" height="240">{vv}</svg>'
        )
        _, w1 = text(fa, 'r', 46, 0, 0)
        _, w2 = text(en.upper(), 'r', 15, 0, 0, anchor='start', ls=2.5)
        W = max(w1, w2) + 150
        tx = W - 138
        p1, _ = text(fa, 'r', 46, tx, 74)
        p2, _ = text(en.upper(), 'r', 15, tx - w2, 104, anchor='start', ls=2.5)
        open(f'{SITE_DIR}/{k}-lockup{m}.svg', 'w').write(
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} 130" width="{W*2:.0f}" height="260">'
            f'<g transform="translate({W-125:.1f} 5)">{vv}</g>'
            f'<path d="{p1}" fill="{tc}"/><path d="{p2}" fill="{ec}"/></svg>'
        )

mk = lambda m: ''.join(f'<figure><img src="{k}-lockup{m}.svg"><img class="i" src="{k}-icon{m}.svg"></figure>' for k in sets)
note = '''<p class="n">اثرگذاری: تابلوی اصلی آبادیس بدون تغییر استفاده شده است (impact-sign.png / impact-sign-full.webp).</p><p class="n" dir="ltr" style="text-align:left">Impact sign: original Abadis artwork, unmodified (impact-sign.png / impact-sign-full.webp).</p>'''
open(f'{SITE_DIR}/index.html', 'w').write(
    '''<!doctype html><html lang="fa" dir="rtl"><meta charset="utf-8"><title>Abadis Med – Section Logos</title><style>body{margin:0;font-family:Tahoma,sans-serif}section{display:grid;grid-template-columns:repeat(auto-fill,minmax(420px,1fr));gap:24px;padding:32px}.l{background:#f4f8f8}.d{background:#071d20}figure{margin:0;display:flex;align-items:center;gap:20px;justify-content:space-between}figure img{height:96px}figure img.i{height:72px}.n{margin:0;padding:16px 32px;font-size:13px;line-height:1.8;color:#5a7578;background:#fff}.f{background:#fff;padding:16px 32px}</style>
<section class="l">''' + mk('') + '</section><section class="d">' + mk('-dark') + '</section><div class="f"><img src="impact-sign-full.webp" height="100"></div>' + note + '</html>'
)

# Update final-five-dark.png (replace middle icon with S9a, and also ensure all 5 are crisp)
old_dark = Image.open(f'{FA_DIR}/final-five-dark.png').convert('RGBA')
# Clear slot 2 (x=640..960) with background #071d20 and paste S9a rendered at 270x270 at (665, 45)
from PIL import ImageDraw
ImageDraw.Draw(old_dark).rectangle([640, 0, 960, 360], fill=(7, 29, 32, 255))
s9a_270 = Image.open(io.BytesIO(cairosvg.svg2png(bytestring=sust_teal.encode(), output_width=270, output_height=270))).convert('RGBA')
old_dark.alpha_composite(s9a_270, (665, 45))
old_dark.convert('RGB').save(f'{FA_DIR}/final-five-dark.png')
print("Updated final-approved, site/brand/section-logos, and final-five-dark.png")
