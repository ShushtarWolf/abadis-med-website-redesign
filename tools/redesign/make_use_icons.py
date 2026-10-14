"""Draw the missing product use-case icons (emergency, NICU/PICU, ECT) in the same style as
site/assets/img/use/*.webp: 100x100 transparent WebP, #066163 line art, ~4.6px round-capped strokes.
Theme colour comes from home/site CSS (mask), so only the alpha shape matters.

    python3 tools/redesign/make_use_icons.py
"""
import math
import os
from PIL import Image, ImageDraw

OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'site', 'assets', 'img', 'use')
S = 8                     # supersample
W = 4.6                   # stroke width in final px (matches the existing icons)
COL = (6, 97, 99)


class Pen:
    def __init__(self):
        self.im = Image.new('L', (100 * S, 100 * S), 0)
        self.d = ImageDraw.Draw(self.im)

    def dot(self, x, y, r=W / 2):
        self.d.ellipse([(x - r) * S, (y - r) * S, (x + r) * S, (y + r) * S], fill=255)

    def poly(self, pts, closed=False):
        if closed: pts = list(pts) + [pts[0]]
        for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
            self.d.line([x1 * S, y1 * S, x2 * S, y2 * S], fill=255, width=int(W * S))
        for x, y in pts: self.dot(x, y)

    def arc(self, cx, cy, rx, ry, a0, a1, n=48):
        pts = [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
                cy + ry * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]
        self.poly(pts)

    def rrect(self, x0, y0, x1, y1, r):
        self.poly([(x0 + r, y0), (x1 - r, y0)]); self.poly([(x0 + r, y1), (x1 - r, y1)])
        self.poly([(x0, y0 + r), (x0, y1 - r)]); self.poly([(x1, y0 + r), (x1, y1 - r)])
        self.arc(x0 + r, y0 + r, r, r, 180, 270); self.arc(x1 - r, y0 + r, r, r, 270, 360)
        self.arc(x1 - r, y1 - r, r, r, 0, 90); self.arc(x0 + r, y1 - r, r, r, 90, 180)

    def save(self, name):
        a = self.im.resize((100, 100), Image.LANCZOS)
        out = Image.new('RGBA', (100, 100), COL + (0,)); out.putalpha(a)
        out.save(os.path.join(OUT, name), 'WEBP', lossless=True)


def emergency():
    """Emergency beacon: dome with a medical cross, base, light rays."""
    p = Pen()
    p.arc(50, 60, 24, 26, 180, 360)                 # dome
    p.poly([(26, 60), (26, 72)]); p.poly([(74, 60), (74, 72)])
    p.rrect(16, 72, 84, 88, 4)                      # base
    p.poly([(50, 44), (50, 64)]); p.poly([(40, 54), (60, 54)])   # cross
    p.poly([(50, 10), (50, 18)])                    # rays
    p.poly([(24, 20), (29, 26)]); p.poly([(76, 20), (71, 26)])
    p.poly([(10, 40), (17, 42)]); p.poly([(90, 40), (83, 42)])
    p.save('emergency.webp')


def nicu():
    """Incubator: clear hood over a baby, on a cart base."""
    p = Pen()
    p.arc(50, 60, 38, 34, 180, 360)                 # hood
    p.poly([(12, 60), (88, 60)])                    # mattress line
    p.rrect(10, 60, 90, 74, 4)                      # tray
    p.poly([(26, 74), (26, 90)]); p.poly([(74, 74), (74, 90)])   # legs
    p.poly([(18, 90), (34, 90)]); p.poly([(66, 90), (82, 90)])
    p.arc(36, 46, 7, 7, 0, 360)                     # baby head
    p.arc(56, 50, 14, 6, 180, 360); p.poly([(42, 50), (70, 50)])  # swaddled body
    p.arc(36, 46, 0.1, 0.1, 0, 1)
    p.save('nicu.webp')


def ect():
    """Brain (top view: scalloped hemispheres, central fissure, folds) above an ECG wave."""
    p = Pen()
    cx, cy, rx, ry = 50, 36, 34, 27
    for side in (-1, 1):                            # scalloped outline per hemisphere
        pts = []
        for i in range(73):
            t = math.radians(-90 + 180 * i / 72)
            k = 1 + 0.055 * math.cos(7 * (t + math.pi / 2))
            pts.append((cx + side * (rx * k * math.cos(t) + 2), cy + ry * k * math.sin(t)))
        p.poly(pts)
    p.poly([(48, 10), (48, 62)]); p.poly([(52, 10), (52, 62)])     # fissure
    for side in (-1, 1):                            # gyri
        f = lambda x, y: (50 + side * x, y)
        p.poly([f(12, 24), f(20, 20), f(26, 26)])
        p.poly([f(8, 38), f(18, 34), f(28, 40)])
        p.poly([f(12, 52), f(22, 48), f(30, 54)])
    p.poly([(8, 84), (32, 84), (38, 76), (46, 94), (54, 70), (60, 84), (92, 84)])   # ECG
    p.save('ect.webp')


if __name__ == '__main__':
    emergency(); nicu(); ect()
    print('ok')
