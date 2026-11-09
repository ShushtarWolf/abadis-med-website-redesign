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

shots = []
overflow = []


def dismiss_consent(page):
    page.evaluate(
        """() => {
    try { localStorage.setItem('abadis-consent', 'accepted'); } catch (e) {}
    document.querySelectorAll('.consent-bar').forEach(el => el.remove());
    const geo = document.querySelector('.lang-suggest');
    if (geo) geo.style.bottom = '0px';
  }"""
    )


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


def snap_scroll(page, path, y):
    page.evaluate(f"window.scrollTo(0, {int(y)})")
    page.wait_for_timeout(500)
    page.screenshot(path=str(path), full_page=False)


def hero_mid_y(page):
    return page.evaluate(
        """() => {
        const t = document.getElementById('film');
        if (!t) return Math.round(window.innerHeight * 0.55);
        const h = Math.max(1, t.offsetHeight - window.innerHeight);
        return Math.round(h * 0.38);
    }"""
    )


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
                snap_scroll(page, ART / f"{tag}-hero-top.png", 0)
                shots.append(str(ART / f"{tag}-hero-top.png"))
                mid = hero_mid_y(page)
                snap_scroll(page, ART / f"{tag}-hero-mid.png", mid)
                shots.append(str(ART / f"{tag}-hero-mid.png"))
                if w == 390:
                    snap_section(page, ART / f"{tag}-stats.png", "#stats")
                    shots.append(str(ART / f"{tag}-stats.png"))
                    cards = page.query_selector_all(".gal-card")
                    for i, card in enumerate(cards):
                        card.scroll_into_view_if_needed()
                        page.wait_for_timeout(350)
                        pth = ART / f"{tag}-gallery-{i + 1}.png"
                        page.screenshot(path=str(pth), full_page=False)
                        shots.append(str(pth))
                    page.evaluate("""() => {
                        const el = document.querySelector('#s1 .code-cards')
                          || document.querySelector('#s1 .code-table-wrap');
                        if (el) el.scrollIntoView({block: 'center'});
                    }""")
                    page.wait_for_timeout(450)
                    page.screenshot(path=str(ART / f"{tag}-powder.png"), full_page=False)
                    shots.append(str(ART / f"{tag}-powder.png"))
                elif w == 1440:
                    snap_section(page, ART / f"{tag}-mid.png", "#sizes")
                    shots.append(str(ART / f"{tag}-mid.png"))
                ctx.close()

    # WebKit powder-row spot check (FA, light, phone)
    try:
        webkit = p.webkit.launch()
        ctx = webkit.new_context(viewport={"width": 390, "height": 844})
        page = ctx.new_page()
        page.add_init_script(
            "try{localStorage.setItem('abadis-consent','accepted');}catch(e){}"
        )
        page.goto(f"{BASE}/products/suction-bag/?theme=light", wait_until="load", timeout=60000)
        dismiss_consent(page)
        snap_section(page, ART / "fa-390-light-powder-webkit.png", "#s1 .code-cards")
        shots.append(str(ART / "fa-390-light-powder-webkit.png"))
        ctx.close()
        webkit.close()
    except Exception as exc:
        print("webkit skip:", exc, file=sys.stderr)

    browser.close()

(ART / "suction-bag-overflow.json").write_text(json.dumps(overflow, indent=2), encoding="utf-8")
(ART / "suction-bag-screenshots.json").write_text(json.dumps(shots, indent=2), encoding="utf-8")
print(json.dumps({"overflow": overflow, "shots": len(shots)}, indent=2))
