#!/usr/bin/env python3
"""Header stability mid hero scroll @ 390 light."""
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

ART = Path("/opt/cursor/artifacts")
BASE = "http://127.0.0.1:8080/products/suction-bag/?theme=light"
IPHONE = {
    "viewport": {"width": 390, "height": 844},
    "device_scale_factor": 3,
    "is_mobile": True,
    "has_touch": True,
}
PREP = """() => {
  try { localStorage.setItem('abadis-consent', 'accepted'); } catch (e) {}
  document.querySelectorAll('.consent-bar').forEach(el => el.remove());
}"""

with sync_playwright() as p:
    browser = p.chromium.launch()
    ctx = browser.new_context(**IPHONE)
    page = ctx.new_page()
    page.goto(BASE, wait_until="load", timeout=120000)
    page.evaluate(PREP)
    page.wait_for_function("() => window.__ready === true", timeout=120000)
    page.evaluate("""() => {
      const film = document.getElementById('film');
      const y = Math.round((film.offsetHeight - innerHeight) * 0.35);
      window.scrollTo(0, y);
    }""")
    page.wait_for_timeout(700)
    out = ART / "studio-390-light-header-midscroll.png"
    page.locator(".header").screenshot(path=str(out))
    ctx.close()
    browser.close()

(ART / "header-midscroll.json").write_text(json.dumps({"shot": str(out)}, indent=2))
print(str(out))
