#!/usr/bin/env python3
"""Round 4: hero + use-case chips screenshots and overflow check."""
import json
import sys
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sys.exit("playwright not installed")

ART = Path("/opt/cursor/artifacts")
ART.mkdir(parents=True, exist_ok=True)
BASE = "http://127.0.0.1:8080"
PREP = """() => {
  try { localStorage.setItem('abadis-consent', 'accepted'); } catch (e) {}
  document.querySelectorAll('.consent-bar').forEach(el => el.remove());
  document.querySelectorAll('.reveal').forEach(el => el.classList.add('in'));
}"""


def snap(page, path, full=False):
    page.screenshot(path=str(path), full_page=full)


def overflow_ok(page):
    sw = page.evaluate("document.documentElement.scrollWidth")
    iw = page.evaluate("window.innerWidth")
    return {"ok": sw <= iw, "scrollWidth": sw, "innerWidth": iw}


shots = []
overflow = []

PAGES = [
    ("fa", "/products/suction-bag/?theme={theme}", 390),
    ("en", "/en/products/suction-bag/?theme={theme}", 390),
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    for lang, route, w in PAGES:
        for theme in ("light", "dark"):
            ctx = browser.new_context(viewport={"width": w, "height": 844}, device_scale_factor=2)
            page = ctx.new_page()
            page.add_init_script("try{localStorage.setItem('abadis-consent','accepted');}catch(e){}")
            page.goto(BASE + route.format(theme=theme), wait_until="networkidle", timeout=90000)
            page.evaluate(PREP)
            overflow.append({"page": f"{lang}-{theme}-390", **overflow_ok(page)})
            snap(page, ART / f"r4-{lang}-390-{theme}-hero-top.png")
            shots.append(str(ART / f"r4-{lang}-390-{theme}-hero-top.png"))
            page.evaluate("window.scrollTo(0, Math.round(window.innerHeight * 0.45))")
            page.wait_for_timeout(400)
            snap(page, ART / f"r4-{lang}-390-{theme}-hero-mid.png")
            shots.append(str(ART / f"r4-{lang}-390-{theme}-hero-mid.png"))
            page.locator("#uses").scroll_into_view_if_needed()
            page.wait_for_timeout(300)
            uses = page.locator("#uses .use-tier").first
            uses.screenshot(path=str(ART / f"r4-{lang}-390-{theme}-uses.png"))
            shots.append(str(ART / f"r4-{lang}-390-{theme}-uses.png"))
            ctx.close()

    ctx = browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
    page = ctx.new_page()
    page.goto(BASE + "/products/suction-bag/?theme=light", wait_until="networkidle", timeout=90000)
    page.evaluate(PREP)
    overflow.append({"page": "fa-light-1440", **overflow_ok(page)})
    snap(page, ART / f"r4-fa-1440-light-hero.png")
    shots.append(str(ART / f"r4-fa-1440-light-hero.png"))
    ctx.close()
    browser.close()

out = {"overflow": overflow, "shots": shots}
(ART / "suction-bag-round4.json").write_text(json.dumps(out, indent=2))
print(json.dumps(out, indent=2))
