"""Generate the painted light-mode sky that sits above the home Zagros hero.

The sky is continued *from* the Zagros painting itself (site/csr/img/hero/bg-dry.jpg) so the
brush texture and palette are identical:
  * the bottom band is the painting's top cloud band mirrored vertically, so the sky's last row
    is pixel-identical to the painting's first row (no seam at the hand-off);
  * higher bands re-use the same painted clouds (flipped / enlarged for perspective), cross-faded;
  * toward the top the sky lifts into a softer, airier daylight (warm cream -> faint mint).
Also cuts two soft-edged cloud sprites from the same painting for the gentle drift layer.

    python3 tools/redesign/make_sky.py
"""
import os
import random
from PIL import Image, ImageChops, ImageFilter, ImageOps

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SRC = os.path.join(ROOT, 'site', 'csr', 'img', 'hero', 'bg-dry.jpg')
OUT = os.path.join(ROOT, 'site', 'assets', 'img', 'sky')
W, H = 1920, 1080


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


def cloud(seed, size):
    """A soft painted cloud sprite: texture from the painting, alpha from a lumpy blob."""
    rnd = random.Random(seed)
    w, h = size
    src = Image.open(SRC).convert('RGB')
    x0 = rnd.randint(200, 1000)
    tex = src.crop((x0, 10, x0 + 700, 210)).resize((w, h), Image.LANCZOS)
    tex = Image.blend(tex, Image.new('RGB', (w, h), (253, 251, 246)), 0.55)
    # painted underside: a faint warm-grey shade toward the base, lit top
    shade = Image.new('RGB', (w, h), (214, 204, 192))
    tex = Image.composite(shade, tex, vmask(h, int(h * 0.45), h).point(lambda v: v * 45 // 255).resize((w, h)))
    alpha = Image.new('L', (w, h), 0)
    blobs = Image.new('L', (w, h), 0)
    from PIL import ImageDraw
    d = ImageDraw.Draw(blobs)
    n = 9
    for i in range(n):
        cx = int(w * (0.18 + 0.64 * i / (n - 1)) + rnd.randint(-20, 20))
        r = int(h * (0.20 + 0.22 * (1 - abs(i - (n - 1) / 2) / ((n - 1) / 2))) * rnd.uniform(0.85, 1.15))
        cy = int(h * 0.62 - r * 0.45)
        d.ellipse((cx - r * 1.3, cy - r, cx + r * 1.3, cy + r), fill=255)
    d.rectangle((int(w * 0.16), int(h * 0.55), int(w * 0.84), int(h * 0.72)), fill=255)
    blobs = blobs.filter(ImageFilter.GaussianBlur(h * 0.09))
    # brushy edge: modulate by the painting's own luminance texture
    lum = ImageOps.autocontrast(tex.convert('L'), cutoff=2).filter(ImageFilter.GaussianBlur(2))
    alpha = ImageChops.multiply(blobs, lum.point(lambda v: 170 + v * 85 // 255))
    alpha = alpha.point(lambda v: min(255, int(v * 0.8)))
    tex.putalpha(alpha)
    return tex


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    s = sky()
    s.save(os.path.join(OUT, 'sky.webp'), 'WEBP', quality=88, method=6)
    s.resize((1280, 720), Image.LANCZOS).save(os.path.join(OUT, 'sky-1280.webp'), 'WEBP', quality=86, method=6)
    cloud(7, (720, 260)).save(os.path.join(OUT, 'cloud-a.webp'), 'WEBP', quality=70, method=6)
    cloud(23, (560, 220)).save(os.path.join(OUT, 'cloud-b.webp'), 'WEBP', quality=70, method=6)
    for f in sorted(os.listdir(OUT)):
        print(f, os.path.getsize(os.path.join(OUT, f)))
