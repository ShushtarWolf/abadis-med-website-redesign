"""Seam bridge for the home first screen -> Zagros scene.

Builds an "odd reflection" of bg-dry about its top row: row y -> 2*row0 - row(y). Shown vertically
mirrored at the bottom of the OR-video section (home.css .home-or-mirror), it meets the Zagros
stage's top row with the same colour AND the same vertical gradient (C1-continuous, no fold line).
Detail is blurred away from the seam so no inverted mountain shapes appear.

    python3 tools/redesign/make_home_bridge.py
"""
import os
import numpy as np
from PIL import Image, ImageFilter

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
HERO = os.path.join(ROOT, 'site', 'csr', 'img', 'hero')


def main():
    src = Image.open(os.path.join(HERO, 'bg-dry.jpg')).convert('RGB')
    a = np.asarray(src).astype(np.float32)
    h = a.shape[0]
    y = np.arange(h)[:, None, None]
    w = np.clip(y / 24.0, 0, 1)                      # exact at the seam, smooth within ~24 rows
    soft = np.asarray(src.filter(ImageFilter.GaussianBlur(30))).astype(np.float32)
    rows = a * (1 - w) + soft * w                    # reflected rows lose their detail quickly
    r0 = a[0:1]
    r0_soft = np.asarray(Image.fromarray(np.repeat(r0, 8, 0).astype(np.uint8)).filter(
        ImageFilter.GaussianBlur(40))).astype(np.float32)[0:1]
    pivot = r0 * (1 - w) + r0_soft * w               # the row-0 pivot loses its column grain too
    out = Image.fromarray(np.clip(2 * pivot - rows, 0, 255).astype(np.uint8))
    out.save(os.path.join(HERO, 'bg-dry-bridge.webp'), quality=84)
    out.resize((1280, 720), Image.LANCZOS).save(os.path.join(HERO, 'bg-dry-bridge-1280.webp'), quality=84)
    for n in ('bg-dry-bridge.webp', 'bg-dry-bridge-1280.webp'):
        print(n, os.path.getsize(os.path.join(HERO, n)))


if __name__ == '__main__':
    main()
