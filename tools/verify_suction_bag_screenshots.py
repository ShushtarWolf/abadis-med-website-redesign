#!/usr/bin/env python3
"""Viewport screenshots + horizontal overflow check for suction-bag pages."""
import json
import sys
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sys.exit("playwright not installed")

ART = Path("/opt/cursor/artifacts")
ART.mkdir(parents=True, exist_ok=True)

PAGES = [
    ("fa", "/products/suction-bag/", "rtl"),
    ("en", "/en/products/suction-bag/", "ltr"),
    ("ar", "/arabic/%D9%83%D9%8A%D8%B3-%D8%A7%D9%84%D8%B4%D9%81%D8%B7/", "rtl"),
]
VIEWPORTS = [(390, 844), (1440, 900)]
THEMES = ["light", "noir"]
BASE = "http://127.0.0.1:8080"

MOBILE_SECTIONS = [
    ("gallery", "#gallery"),
    ("sizes", "#sizes"),
    ("powder", "#s1 .code-table-wrap"),
    ("carton", "#packaging .pack-tier:first-child .spec-card:last-child"),
    ("uses", "#uses"),
    ("filters", "#filters"),
]

shots = []
overflow = []


def dismiss_consent(page):
  page.evaluate("""() => {
    try { localStorage.setItem('abadis-consent', 'accepted'); } catch (e) {}
    document.querySelectorAll('.consent-bar').forEach(el => el.remove());
    const geo = document.querySelector('.lang-suggest');
    if (geo) geo.style.bottom = '0px';
  }""")


def snap_section(page, path, selector):
  page.evaluate(
      """(sel) => {
        const el = document.querySelector(sel);
        if (el) el.scrollIntoView({block: 'center', inline: 'nearest'});
        else window.scrollTo(0, 0);
      }""",
      selector,
  )
  page.wait_for_timeout(450)
  page.screenshot(path=str(path), full_page=False)


def snap_top(page, path):
  page.evaluate("window.scrollTo(0, 0)")
  page.wait_for_timeout(300)
  page.screenshot(path=str(path), full_page=False)


with sync_playwright() as p:
    browser = p.chromium.launch()
    for lang, route, _ in PAGES:
        for theme in THEMES:
            for w, h in VIEWPORTS:
                ctx = browser.new_context(viewport={"width": w, "height": h})
                page = ctx.new_page()
                page.add_init_script(
                    "try{localStorage.setItem('abadis-consent','accepted');}catch(e){}"
                )
                page.goto(f"{BASE}{route}?theme={theme}", wait_until="load", timeout=60000)
                dismiss_consent(page)
                sw = page.evaluate("document.documentElement.scrollWidth")
                iw = page.evaluate("window.innerWidth")
                overflow.append(
                    {
                        "lang": lang,
                        "theme": theme,
                        "viewport": f"{w}x{h}",
                        "ok": sw <= iw,
                        "scrollWidth": sw,
                        "innerWidth": iw,
                    }
                )
                tag = f"{lang}-{w}-{theme}"
                snap_top(page, ART / f"{tag}-hero.png")
                shots.append(str(ART / f"{tag}-hero.png"))
                if w == 390:
                    for name, sel in MOBILE_SECTIONS:
                        path = ART / f"{tag}-{name}.png"
                        snap_section(page, path, sel)
                        shots.append(str(path))
                elif w == 1440:
                    path = ART / f"{tag}-mid.png"
                    snap_section(page, path, "#sizes")
                    shots.append(str(path))
                ctx.close()
    browser.close()

(ART / "suction-bag-overflow.json").write_text(json.dumps(overflow, indent=2), encoding="utf-8")
(ART / "suction-bag-screenshots.json").write_text(json.dumps(shots, indent=2), encoding="utf-8")
print(json.dumps({"overflow": overflow, "shots": len(shots)}, indent=2))
