"""Scene assets for hero-test/birds (v2): the painted sky above the Zagros scene, the ridge
foreground layer that hides birds flying behind the mountains, and the ridge polyline.

  * sky.webp / sky-1280.webp: the Zagros painting (bg-dry) continued upward, v1 approach: its top
    cloud band mirrored so the sky's last row equals the painting's first row (seamless), higher
    bands re-use the same clouds, lifted slightly toward a uniform cream.
  * ridge.webp: bg-dry with alpha only below the mountain ridge (feathered, raised a few px), drawn
    above the bird canvas. It is the same pixels as the backdrop, so it is invisible except that
    birds disappear behind the mountains.
  * ridge.js: the ridge line in painting px (for take-off / landing paths).

    python3 tools/redesign/make_birds_scene.py
"""
import json
import os
from PIL import Image, ImageFilter, ImageChops, ImageOps

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SRC = os.path.join(ROOT, 'site', 'csr', 'img', 'hero', 'bg-dry.jpg')
OUT = os.path.join(ROOT, 'site', 'hero-test', 'birds')
W, H = 1920, 1080
HORIZON = 672          # where the hazy plain meets the sky at the far left / right


def vmask(h, a, b, invert=False):
    """Vertical smoothstep mask (L, 1 x h): 0 above row a, 255 below row b."""
    m = Image.new('L', (1, h))
    px = m.load()
    for y in range(h):
        t = min(1.0, max(0.0, (y - a) / float(max(1, b - a))))
        t = t * t * (3 - 2 * t)
        px[0, y] = int(round(255 * ((1 - t) if invert else t)))
    return m


def sky():
    src = Image.open(SRC).convert('RGB')
    band = src.crop((0, 0, W, 260))                    # clouds above the mountain peak (~row 320)

    def grown(img, k, x_shift=0):
        """Enlarge a cloud band (nearer clouds higher up), keep the brush grain crisp."""
        w2 = int(W * k)
        big = img.resize((w2, int(img.height * k)), Image.LANCZOS)
        big = big.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=1))
        x0 = (w2 - W) // 2 + x_shift
        return big.crop((x0, 0, x0 + W, big.height))

    # bottom -> top; each band cross-fades into the one below it
    layers = [
        (ImageOps.flip(band), H - 260),                               # A: row 1079 == painting row 0
        (grown(ImageOps.mirror(band), 1.15, 90), H - 260 - 230),     # B
        (grown(ImageOps.flip(ImageOps.mirror(band)), 1.3, -160), 330),  # C
        (grown(band, 1.6, 120), 0),                                   # D
    ]
    out = Image.new('RGB', (W, H))
    # paint top-down so lower bands overlap (and win over) the ones above
    for img, y in reversed(layers):
        lay = out.copy()
        lay.paste(img, (0, y))
        out = Image.composite(lay, out, vmask(H, y, y + 70).resize((W, H))) if y else lay

    # daylight lift toward the top (keeps the bottom 300 rows untouched)
    light = Image.new('RGB', (W, H), (244, 246, 242))
    top = vmask(H, 0, H - 300, invert=True).point(lambda v: int(v * 0.30)).resize((W, H))
    out = Image.composite(light, out, top)
    # soft warm sun-glow behind the logo area
    glow = Image.new('L', (W, H), 0)
    g = Image.new('L', (900, 520), 0)
    gp = g.load()
    for y in range(520):
        for x in range(900):
            d = ((x - 450) / 450.0) ** 2 + ((y - 260) / 260.0) ** 2
            gp[x, y] = int(max(0.0, 1 - d) ** 2 * 120)
    glow.paste(g, (W // 2 - 450, 150))
    out = Image.composite(Image.new('RGB', (W, H), (252, 249, 242)), out, glow)
    return out



def ridge_line():
    """Mountain silhouette per column: first row where the painting's brush texture starts."""
    g = Image.open(SRC).convert('L')
    tex = ImageChops.difference(g, g.filter(ImageFilter.GaussianBlur(3))).filter(ImageFilter.GaussianBlur(6))
    px = tex.load()
    raw = []
    for x in range(W):
        r = HORIZON
        for y in range(150, HORIZON):
            if px[x, y] > 1:
                r = y
                break
        raw.append(r)
    # the hazy far foothills have no texture: ease them down to the horizon instead of a cliff
    left = next(x for x in range(W) if x > 200 and raw[x] < 560)
    right = next(x for x in range(W - 1, 0, -1) if x < W - 100 and raw[x] < 560)
    for x in range(0, left):
        t = x / float(left)
        raw[x] = int(HORIZON + (raw[left] - HORIZON) * (t * t * (3 - 2 * t)))
    for x in range(right + 1, W):
        t = (W - 1 - x) / float(W - 1 - right)
        raw[x] = int(HORIZON + (raw[right] - HORIZON) * (t * t * (3 - 2 * t)))
    # median, then keep the highest point within a small window and lift a little: the occluder
    # may include a few px of sky (identical pixels), but never lets a bird show in front of rock
    med = [sorted(raw[max(0, x - 6):x + 7])[len(raw[max(0, x - 6):x + 7]) // 2] for x in range(W)]
    return [min(med[max(0, x - 10):x + 11]) - 10 for x in range(W)]


def ridge_layer(line):
    src = Image.open(SRC).convert('RGB')
    m = Image.new('L', (W, H), 0)
    mp = m.load()
    for x in range(W):
        top = line[x]
        for y in range(max(0, top - 6), H):
            mp[x, y] = 255 if y >= top + 6 else int(255 * (y - (top - 6)) / 12.0)
    m = m.filter(ImageFilter.GaussianBlur(1.5))
    out = src.copy()
    out.putalpha(m)
    return out


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    s = sky()
    s.save(os.path.join(OUT, 'sky.webp'), 'WEBP', quality=88, method=6)
    s.resize((1280, 720), Image.LANCZOS).save(os.path.join(OUT, 'sky-1280.webp'), 'WEBP', quality=86, method=6)
    line = ridge_line()
    ridge_layer(line).save(os.path.join(OUT, 'ridge.webp'), 'WEBP', quality=74, method=6)
    pts = [[x, line[x]] for x in range(0, W, 32)] + [[W - 1, line[W - 1]]]
    with open(os.path.join(OUT, 'ridge.js'), 'w') as f:
        f.write('/* generated by tools/redesign/make_birds_scene.py: ridge line in bg-dry px */\n')
        f.write('window.ZAGROS_RIDGE = ' + json.dumps(pts, separators=(',', ':')) + ';\n')
    for n in ('sky.webp', 'sky-1280.webp', 'ridge.webp', 'ridge.js'):
        print(n, os.path.getsize(os.path.join(OUT, n)))
