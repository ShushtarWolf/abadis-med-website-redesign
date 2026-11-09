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

PREP = """() => {
  try { localStorage.setItem('abadis-consent', 'accepted'); } catch (e) {}
  document.querySelectorAll('.consent-bar, .lang-suggest').forEach(el => el.remove());
  document.querySelectorAll('.reveal').forEach(el => el.classList.add('in'));
  document.querySelectorAll('.beat').forEach(b => { b.style.opacity = '1'; b.style.transform = 'none'; });
}"""


def prep_page(page):
    page.evaluate(PREP)


def wait_settled(page):
    page.wait_for_load_state("domcontentloaded")
    try:
        page.wait_for_function("() => document.fonts && document.fonts.status === 'loaded'", timeout=8000)
    except Exception:
        pass
    page.wait_for_timeout(350)


def scroll_to_y(page, y):
    page.evaluate(
        """(y) => {
        const hdr = document.querySelector('.header');
        const pad = hdr ? hdr.offsetHeight + 8 : 72;
        window.scrollTo({ top: Math.max(0, y - pad), left: 0, behavior: 'instant' });
      }""",
        int(y),
    )
    page.wait_for_timeout(400)


def section_top(page, selector):
    return page.evaluate(
        """(sel) => {
        const el = document.querySelector(sel);
        if (!el) return 0;
        return el.getBoundingClientRect().top + window.scrollY;
      }""",
        selector,
    )


def snap_viewport(page, path):
    page.screenshot(path=str(path), full_page=False, animations="disabled")


def film_mid_y(page):
    return page.evaluate(
        """() => {
        const film = document.getElementById('film');
        if (!film) return Math.round(window.innerHeight * 0.45);
        const total = Math.max(1, film.offsetHeight - window.innerHeight);
        return Math.round(total * 0.32);
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
                url = f"{BASE}{route}?theme={theme}"
                page.goto(url, wait_until="load", timeout=60000)
                prep_page(page)
                wait_settled(page)
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

                scroll_to_y(page, 0)
                snap_viewport(page, ART / f"{tag}-hero-top.png")
                shots.append(str(ART / f"{tag}-hero-top.png"))

                scroll_to_y(page, film_mid_y(page))
                snap_viewport(page, ART / f"{tag}-hero-mid.png")
                shots.append(str(ART / f"{tag}-hero-mid.png"))

                if w == 390:
                    scroll_to_y(page, section_top(page, "#stats"))
                    snap_viewport(page, ART / f"{tag}-stats.png")
                    shots.append(str(ART / f"{tag}-stats.png"))

                    cards = page.query_selector_all(".gal-card")
                    for i, _ in enumerate(cards):
                        scroll_to_y(
                            page,
                            page.evaluate(
                                """(i) => {
                                const c = document.querySelectorAll('.gal-card')[i];
                                if (!c) return 0;
                                return c.getBoundingClientRect().top + window.scrollY - 80;
                            }""",
                                i,
                            ),
                        )
                        snap_viewport(page, ART / f"{tag}-gallery-{i + 1}.png")
                        shots.append(str(ART / f"{tag}-gallery-{i + 1}.png"))

                    scroll_to_y(page, section_top(page, "#s1"))
                    snap_viewport(page, ART / f"{tag}-powder.png")
                    shots.append(str(ART / f"{tag}-powder.png"))

                elif w == 1440:
                    scroll_to_y(page, section_top(page, "#sizes"))
                    snap_viewport(page, ART / f"{tag}-mid.png")
                    shots.append(str(ART / f"{tag}-mid.png"))

                ctx.close()

    # 3× DPR crop of powder yes icon (FA light)
    ctx = browser.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=3)
    page = ctx.new_page()
    page.add_init_script(
        "try{localStorage.setItem('abadis-consent','accepted');}catch(e){}"
    )
    page.goto(f"{BASE}/products/suction-bag/?theme=light#s1", wait_until="load", timeout=60000)
    prep_page(page)
    wait_settled(page)
    scroll_to_y(page, section_top(page, "#s1"))
    loc = page.locator("#s1 .code-card").first.locator(".yn-yes")
    loc.screenshot(path=str(ART / "fa-390-light-powder-check-3x.png"))
    shots.append(str(ART / "fa-390-light-powder-check-3x.png"))
    page.locator("#stats .stat-grid").screenshot(path=str(ART / "fa-390-light-stats-grid-crop.png"))
    shots.append(str(ART / "fa-390-light-stats-grid-crop.png"))
    ctx.close()
    browser.close()

(ART / "suction-bag-overflow.json").write_text(json.dumps(overflow, indent=2), encoding="utf-8")
(ART / "suction-bag-screenshots.json").write_text(json.dumps(shots, indent=2), encoding="utf-8")
print(json.dumps({"overflow": overflow, "shots": len(shots)}, indent=2))
