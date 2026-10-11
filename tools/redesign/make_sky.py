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


def grain(size, seed=0, k=1.0):
    """Brush grain of the Zagros painting: high-pass of its cloud band, tiled to size (L, 128 = flat)."""
    src = Image.open(SRC).convert('L').crop((0, 0, W, 300))
    hp = ImageChops.subtract(src, src.filter(ImageFilter.GaussianBlur(10)), 1, 128)
    rnd = random.Random(seed)
    out = Image.new('L', size, 128)
    for y in range(0, size[1], 260):
        x0 = rnd.randint(0, 600)
        tile = hp.crop((x0, 20, x0 + min(W - x0, size[0]), 280))
        if rnd.random() < .5: tile = ImageOps.mirror(tile)
        out.paste(tile.resize((size[0], 260)), (0, y))
    if k != 1.0:
        out = out.point(lambda v: max(0, min(255, int(128 + (v - 128) * k))))
    return out


def add_grain(img, g, amount):
    """img + amount * (grain - 128), per channel."""
    off = g.point(lambda v: max(0, min(255, int(128 + (v - 128) * amount))))
    return Image.merge('RGB', [ImageChops.add(c, off, 1.0, -128) for c in img.split()])


def vgrad(stops, h, w=W):
    """Vertical colour gradient from [(row, (r,g,b)), ...]."""
    col = Image.new('RGB', (1, h))
    px = col.load()
    for y in range(h):
        for i in range(len(stops) - 1):
            (y0, c0), (y1, c1) = stops[i], stops[i + 1]
            if y0 <= y <= y1:
                t = (y - y0) / float(max(1, y1 - y0)); t = t * t * (3 - 2 * t)
                px[0, y] = tuple(int(round(c0[j] + (c1[j] - c0[j]) * t)) for j in range(3))
                break
    return col.resize((w, h))


def sky():
    src = Image.open(SRC).convert('RGB')
    band = src.crop((0, 0, W, 260))                    # clouds above the mountain peak (~row 320)
    # haze band: the painting's own top clouds mirrored, so row 1079 == painting row 0 (seamless)
    haze = Image.new('RGB', (W, H))
    haze.paste(ImageOps.mirror(band).resize((W, 420)), (0, H - 590))
    lay = haze.copy(); lay.paste(ImageOps.flip(band), (0, H - 260))
    haze = Image.composite(lay, haze, vmask(H, H - 260, H - 180).resize((W, H)))

    # daytime blue: deeper soft blue at the top, lightening into the painting's warm haze
    blue = vgrad([(0, (112, 160, 202)), (300, (146, 186, 218)), (600, (190, 212, 228)),
                  (820, (222, 222, 218)), (H - 1, (232, 224, 216))], H)
    blue = add_grain(blue, grain((W, H), 3), 0.55)

    # soft sun glow, upper left (light falls from the left in the Zagros painting)
    glow = Image.new('L', (W, H), 0)
    g = Image.new('L', (900, 760), 0)
    gp = g.load()
    for y in range(0, 760):
        for x in range(0, 900):
            d = ((x - 450) / 450.0) ** 2 + ((y - 380) / 380.0) ** 2
            gp[x, y] = int(max(0.0, 1 - d) ** 2.4 * 225)
    glow.paste(g, (40, -300))
    blue = Image.composite(Image.new('RGB', (W, H), (255, 252, 238)), blue, glow)

    # big painted clouds baked into the backdrop (the CSS layer adds smaller drifting ones)
    for seed, (w, h), (x, y) in [(41, (1100, 380), (980, 80)), (52, (900, 320), (-160, 330)),
                                 (63, (760, 260), (700, 520)), (74, (620, 220), (1500, 420))]:
        c = cloud(seed, (w, h))
        blue.paste(c, (x, y), c)

    # hand off to the painting's haze over the lower third; last 120 rows are 100% painting
    return Image.composite(haze, blue, vmask(H, H - 560, H - 60).resize((W, H)))


def cloud(seed, size):
    """A white painted cloud: lumpy lit top, cool-grey shaded base, Zagros brush grain, broken edges."""
    from PIL import ImageDraw
    rnd = random.Random(seed)
    w, h = size
    blobs = Image.new('L', (w, h), 0)
    d = ImageDraw.Draw(blobs)
    base = h * 0.80
    peak = rnd.uniform(0.38, 0.62)
    n = 9
    tops = []
    for i in range(n):
        f = i / (n - 1)
        cx = w * (0.15 + 0.70 * f) + rnd.uniform(-0.025, 0.025) * w
        hump = max(0.2, 1 - abs(f - peak) * 1.7)
        r = h * (0.13 + 0.22 * hump) * rnd.uniform(0.88, 1.12)
        cy = base - r * 0.75
        d.ellipse((cx - r * 1.2, cy - r, cx + r * 1.2, cy + r), fill=255)
        tops.append((cx, cy - r * 0.8, r))
    for cx, ty, r in tops:                      # cauliflower bumps along the top edge
        for _ in range(2):
            rr = r * rnd.uniform(0.35, 0.55)
            x = cx + rnd.uniform(-0.8, 0.8) * r
            y = max(rr + 4, ty + rnd.uniform(0, 0.4) * r)
            d.ellipse((x - rr, y - rr, x + rr, y + rr), fill=255)
    d.rounded_rectangle((int(w * 0.10), int(base - h * 0.12), int(w * 0.90), int(base + h * 0.04)), radius=int(h * 0.08), fill=255)
    alpha = blobs.filter(ImageFilter.GaussianBlur(h * 0.03))
    inner = blobs.filter(ImageFilter.GaussianBlur(h * 0.12))
    shade = Image.new('L', (w, h))
    sp = shade.load(); ip = inner.load()
    for y in range(h):
        t = min(1.0, max(0.0, (y - h * 0.40) / (h * 0.42)))
        for x in range(w):
            sp[x, y] = int(255 * t * 0.9 * (ip[x, y] / 255.0))
    lit = Image.new('RGB', (w, h), (255, 254, 249))
    under = Image.new('RGB', (w, h), (196, 207, 222))
    rgb = Image.composite(under, lit, shade)
    rgb = add_grain(rgb, grain((w, h), seed, 1.6), 2.2)
    edge = grain((w, h), seed + 1, 2.6).filter(ImageFilter.GaussianBlur(1.2))
    alpha = ImageChops.multiply(alpha, edge.point(lambda v: max(0, min(255, 225 + (v - 128) * 3))))
    rgb.putalpha(alpha)
    return rgb


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    s = sky()
    s.save(os.path.join(OUT, 'sky.webp'), 'WEBP', quality=88, method=6)
    s.resize((1280, 720), Image.LANCZOS).save(os.path.join(OUT, 'sky-1280.webp'), 'WEBP', quality=86, method=6)
    cloud(7, (720, 260)).save(os.path.join(OUT, 'cloud-a.webp'), 'WEBP', quality=70, method=6)
    cloud(23, (560, 220)).save(os.path.join(OUT, 'cloud-b.webp'), 'WEBP', quality=70, method=6)
    for f in sorted(os.listdir(OUT)):
        print(f, os.path.getsize(os.path.join(OUT, f)))
