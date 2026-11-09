#!/usr/bin/env python3
"""390 light + 1440: hero bottom boundary with next section."""
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

ART = Path("/opt/cursor/artifacts")
BASE = "http://127.0.0.1:8080"
IPHONE = {
    "viewport": {"width": 390, "height": 844},
    "device_scale_factor": 3,
    "is_mobile": True,
    "has_touch": True,
    "user_agent": (
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 "
        "Mobile/15E148 Safari/604.1"
    ),
}
PREP = """() => {
  try { localStorage.setItem('abadis-consent', 'accepted'); } catch (e) {}
  document.querySelectorAll('.consent-bar').forEach(el => el.remove());
}"""


def wait_gl(page):
    page.wait_for_function("() => window.__ready === true", timeout=120000)
    page.wait_for_timeout(300)


shots = []
with sync_playwright() as p:
    browser = p.chromium.launch()

    for vw, label, mobile in ((390, "390-light-hero-boundary", True), (1440, "1440-light-hero-boundary", False)):
        kw = IPHONE if mobile else {"viewport": {"width": 1440, "height": 900}}
        ctx = browser.new_context(**kw)
        page = ctx.new_page()
        page.goto(BASE + "/products/suction-bag/?theme=light", wait_until="load", timeout=120000)
        page.evaluate(PREP)
        wait_gl(page)
        if mobile:
            page.evaluate("window.scrollTo(0, 0)")
            page.wait_for_timeout(300)
            out0 = ART / "studio-390-light-hero-fullscreen.png"
            page.screenshot(path=str(out0), full_page=False)
            shots.append(str(out0))
        page.evaluate("""() => {
          const film = document.getElementById('film');
          const y = Math.max(0, film.offsetHeight - window.innerHeight);
          window.scrollTo(0, y);
        }""")
        page.wait_for_timeout(500)
        out = ART / f"studio-{label}.png"
        page.screenshot(path=str(out), full_page=False)
        shots.append(str(out))
        ctx.close()

    browser.close()

(ART / "hero-boundary.json").write_text(json.dumps({"shots": shots}, indent=2))
print(json.dumps({"shots": shots}, indent=2))
