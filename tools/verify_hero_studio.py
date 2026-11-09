#!/usr/bin/env python3
"""Studio hero: 390 light/dark top, transition scroll, 1440 desktop."""
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
    page.wait_for_function("() => window.__cin_frame", timeout=20000)
    page.wait_for_timeout(400)


shots = []
with sync_playwright() as p:
    browser = p.chromium.launch()
    for theme in ("light", "dark"):
        ctx = browser.new_context(**IPHONE)
        page = ctx.new_page()
        page.goto(BASE + f"/products/suction-bag/?theme={theme}", wait_until="load", timeout=120000)
        page.evaluate(PREP)
        page.evaluate("window.scrollTo(0, 0)")
        wait_gl(page)
        out = ART / f"studio-390-{theme}-hero-top.png"
        page.locator(".cin-stage").screenshot(path=str(out))
        shots.append(str(out))
        ctx.close()

    ctx = browser.new_context(**IPHONE)
    page = ctx.new_page()
    page.goto(BASE + "/products/suction-bag/?theme=dark", wait_until="load", timeout=120000)
    page.evaluate(PREP)
    wait_gl(page)
    page.evaluate("window.scrollTo(0, Math.round(window.innerHeight * 0.92))")
    page.wait_for_timeout(500)
    out = ART / "studio-390-dark-hero-transition.png"
    page.screenshot(path=str(out), full_page=False)
    shots.append(str(out))
    ctx.close()

    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    page.goto(BASE + "/products/suction-bag/?theme=dark", wait_until="load", timeout=120000)
    page.evaluate(PREP)
    wait_gl(page)
    out = ART / "studio-1440-dark-hero.png"
    page.locator(".cin-stage").screenshot(path=str(out))
    shots.append(str(out))
    ctx.close()
    browser.close()

(ART / "hero-studio.json").write_text(json.dumps({"shots": shots}, indent=2))
print(json.dumps({"shots": shots}, indent=2))
