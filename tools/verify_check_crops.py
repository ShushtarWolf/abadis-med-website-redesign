#!/usr/bin/env python3
"""Crop screenshots proving unified check icons + overflow on sample pages."""
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

PAGES = [
    ("fa-suction-powder", "/products/suction-bag/?theme={theme}#codes", ".code-cards .yn-yes", 390),
    ("fa-hero-checks", "/hero-options/1-product/?theme={theme}", ".checks li:first-child", 390),
    (
        "en-article-check",
        "/en/the-critical-role-of-medical-grade-pvc-in-suction-tube-products/?theme={theme}",
        "p .ico-mask",
        390,
    ),
]

overflow = []
shots = []

PREP = """() => {
  try { localStorage.setItem('abadis-consent', 'accepted'); } catch (e) {}
  document.querySelectorAll('.consent-bar').forEach(el => el.remove());
  document.querySelectorAll('.reveal').forEach(el => el.classList.add('in'));
}"""


def scroll_to(page, sel):
    page.evaluate(
        """(s) => {
        const el = document.querySelector(s);
        if (!el) return;
        const hdr = document.querySelector('.header');
        const pad = hdr ? hdr.offsetHeight + 8 : 72;
        const y = el.getBoundingClientRect().top + window.scrollY - pad;
        window.scrollTo(0, Math.max(0, y));
    }""",
        sel,
    )
    page.wait_for_timeout(400)


with sync_playwright() as p:
    browser = p.chromium.launch()
    for theme in ("light", "noir"):
        for tag, route, sel, w in PAGES:
            ctx = browser.new_context(viewport={"width": w, "height": 844}, device_scale_factor=3)
            page = ctx.new_page()
            page.add_init_script("try{localStorage.setItem('abadis-consent','accepted');}catch(e){}")
            page.goto(BASE + route.format(theme=theme), wait_until="load", timeout=60000)
            page.evaluate(PREP)
            sw = page.evaluate("document.documentElement.scrollWidth")
            iw = page.evaluate("window.innerWidth")
            overflow.append({"page": tag, "theme": theme, "ok": sw <= iw, "scrollWidth": sw, "innerWidth": iw})
            scroll_to(page, sel)
            path = ART / f"{tag}-{theme}-check-3x.png"
            loc = page.locator(sel).first
            loc.scroll_into_view_if_needed(timeout=15000)
            page.wait_for_timeout(300)
            loc.screenshot(path=str(path), timeout=15000)
            shots.append(str(path))
            ctx.close()
    browser.close()

(ART / "check-icon-crops.json").write_text(json.dumps({"overflow": overflow, "shots": shots}, indent=2))
print(json.dumps({"overflow": overflow, "shots": shots}, indent=2))
