#!/usr/bin/env python3
"""Render P01 v12 hero frame (t=0) via Three.js — transparent WebP, 2×."""
import base64
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "site/assets/img/products/3d/p01-cinematic-v12-still-alpha.webp"
URL = "http://127.0.0.1:8080/3d-sketches/p01-cinematic/still-export.html"
# 2× the product still slot (900×1338 nominal)
W, H = 900, 1338


def main():
    tmp = OUT.with_suffix(".png")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(
            viewport={"width": W, "height": H},
            device_scale_factor=2,
        )
        page = ctx.new_page()
        page.goto(URL, wait_until="load", timeout=120000)
        page.wait_for_function("() => window.__still_capture === true", timeout=120000)
        page.wait_for_timeout(400)
        b64 = page.evaluate(
            """() => {
            const c = document.querySelector('canvas');
            return c ? c.toDataURL('image/png') : '';
        }"""
        )
        if not b64.startswith("data:image/png;base64,"):
            raise RuntimeError("canvas toDataURL failed")
        tmp.write_bytes(base64.b64decode(b64.split(",", 1)[1]))
        ctx.close()
        browser.close()
    im = Image.open(tmp).convert("RGBA")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    im.save(OUT, "WEBP", lossless=True, quality=100, method=6, exact=True)
    tmp.unlink(missing_ok=True)
    print("wrote", OUT, im.size, "bytes", OUT.stat().st_size)


if __name__ == "__main__":
    main()
