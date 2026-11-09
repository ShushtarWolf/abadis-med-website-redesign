#!/usr/bin/env python3
"""Knock out the studio black from the v12 still → transparent WebP for hero fallback."""
from pathlib import Path

from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "site/assets/img/products/3d/p01-cinematic-v12-still.webp"
OUT = ROOT / "site/assets/img/products/3d/p01-cinematic-v12-still-alpha.webp"


def main():
    im = Image.open(SRC).convert("RGBA")
    px = im.load()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
            if lum < 18:
                px[x, y] = (r, g, b, 0)
            elif lum < 42:
                alpha = int((lum - 18) / 24 * 255)
                px[x, y] = (r, g, b, alpha)
    # soften alpha halos
    r, g, b, a = im.split()
    a = a.filter(ImageFilter.GaussianBlur(radius=0.6))
    im = Image.merge("RGBA", (r, g, b, a))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    im.save(OUT, "WEBP", lossless=True, quality=95, method=6)
    print("wrote", OUT, "bytes", OUT.stat().st_size)


if __name__ == "__main__":
    main()
