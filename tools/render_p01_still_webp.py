#!/usr/bin/env python3
"""Render P01 v12 hero frame with CSS studio + GLB (t=0), 2× WebP."""
import base64
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "site/assets/img/products/3d/p01-cinematic-v12-still-studio.webp"
URL = "http://127.0.0.1:8080/3d-sketches/p01-cinematic/still-export.html"
W, H = 900, 1338


def main():
    tmp = OUT.with_suffix(".png")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={"width": W, "height": H}, device_scale_factor=2)
        page = ctx.new_page()
        page.goto(URL, wait_until="load", timeout=120000)
        page.wait_for_function("() => window.__still_capture === true", timeout=120000)
        page.wait_for_timeout(400)
        clip = page.evaluate("""() => {
          const el = document.querySelector('.cin-stage');
          const r = el.getBoundingClientRect();
          return { x: r.x, y: r.y, width: r.width, height: r.height };
        }""")
        page.screenshot(path=str(tmp), clip=clip)
        ctx.close()
        browser.close()
    im = Image.open(tmp).convert("RGB")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    im.save(OUT, "WEBP", quality=92, method=6)
    tmp.unlink(missing_ok=True)
    print("wrote", OUT, im.size, "bytes", OUT.stat().st_size)


if __name__ == "__main__":
    main()
