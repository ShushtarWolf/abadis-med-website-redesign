#!/usr/bin/env python3
"""Hero top shots: 390 light/dark (iPhone WebKit or UA) + 1440 dark."""
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

ART = Path("/opt/cursor/artifacts")
ART.mkdir(parents=True, exist_ok=True)
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


def shot_hero(page, path):
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_function("() => window.__ready === true", timeout=120000)
    page.wait_for_function("() => window.__cin_frame", timeout=20000)
    page.wait_for_timeout(400)
    page.locator(".cin-stage").screenshot(path=str(path))


def launch_mobile(p):
    try:
        return p.webkit.launch(), "webkit"
    except Exception:
        return p.chromium.launch(), "chromium"


shots = []
meta = {}

with sync_playwright() as p:
    for theme in ("light", "dark"):
        browser, engine = launch_mobile(p)
        ctx = browser.new_context(**IPHONE)
        page = ctx.new_page()
        page.goto(BASE + f"/products/suction-bag/?theme={theme}", wait_until="load", timeout=120000)
        page.evaluate(PREP)
        out = ART / f"hero-390-{theme}-iphone-{engine}.png"
        shot_hero(page, out)
        band = page.evaluate("""() => {
          const stage = document.querySelector('.cin-stage');
          const copy = document.querySelector('.cin-copy');
          const sr = stage.getBoundingClientRect();
          const cr = copy.getBoundingClientRect();
          const grid = getComputedStyle(stage).display;
          const copyPos = getComputedStyle(copy).position;
          return {
            stageH: sr.height,
            innerH: window.innerHeight,
            copyBottom: cr.bottom,
            stageBottom: sr.bottom,
            copyOverlaps: cr.top < sr.bottom - 8,
            display: grid,
            copyPosition: copyPos,
            copyBg: getComputedStyle(copy).backgroundColor,
          };
        }""")
        meta[f"390-{theme}"] = {"engine": engine, **band}
        shots.append(str(out))
        ctx.close()
        browser.close()

    browser = p.chromium.launch()
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    page.goto(BASE + "/products/suction-bag/?theme=dark", wait_until="load", timeout=120000)
    page.evaluate(PREP)
    out = ART / "hero-1440-dark-webgl.png"
    shot_hero(page, out)
    shots.append(str(out))
    ctx.close()
    browser.close()

(ART / "hero-band-fix.json").write_text(json.dumps({"shots": shots, "meta": meta}, indent=2))
print(json.dumps({"shots": shots, "meta": meta}, indent=2))
