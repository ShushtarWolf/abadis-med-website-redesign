#!/usr/bin/env python3
"""Round 4 screenshots: hero (wait for WebGL), fallback, use chips."""
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


def wait_model(page, webgl=True):
    if webgl:
        page.wait_for_function("() => window.__ready === true", timeout=120000)
        page.wait_for_function(
            """() => new Promise((res) => {
              if (window.__cin_frame) return res(true);
              const r = document.querySelector('[data-cin-root]');
              if (!r) return res(false);
              r.addEventListener('cin-frame', () => res(true), { once: true });
              setTimeout(() => res(!!window.__cin_frame), 8000);
            })""",
            timeout=15000,
        )
        page.wait_for_timeout(400)
    else:
        page.wait_for_selector('[data-cin-root].is-still', timeout=30000)


def overflow_ok(page):
    sw = page.evaluate("document.documentElement.scrollWidth")
    iw = page.evaluate("window.innerWidth")
    return {"ok": sw <= iw, "scrollWidth": sw, "innerWidth": iw}


shots = []
overflow = []


def hero_shot(page, path):
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(200)
    page.locator(".cin-stage").screenshot(path=str(path))


with sync_playwright() as p:
    browser = p.chromium.launch()
    for theme in ("light", "dark"):
        ctx = browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
        page = ctx.new_page()
        page.goto(BASE + f"/products/suction-bag/?theme={theme}", wait_until="load", timeout=120000)
        page.evaluate(PREP)
        wait_model(page, webgl=True)
        overflow.append({"page": f"fa-{theme}-1440", **overflow_ok(page)})
        hero_shot(page, ART / f"r4c-fa-1440-{theme}-hero-webgl.png")
        shots.append(str(ART / f"r4c-fa-1440-{theme}-hero-webgl.png"))
        ctx.close()

    ctx = browser.new_context(
        viewport={"width": 1440, "height": 900},
        device_scale_factor=1,
        java_script_enabled=True,
    )
    # Force still fallback: disable WebGL before any page script runs
    ctx.add_init_script("""(() => {
      const proto = HTMLCanvasElement.prototype;
      const orig = proto.getContext;
      proto.getContext = function(type, attrs) {
        if (type && String(type).includes('webgl')) return null;
        return orig.call(this, type, attrs);
      };
    })();""")
    page = ctx.new_page()
    page.goto(BASE + "/products/suction-bag/?theme=light", wait_until="load", timeout=120000)
    page.evaluate(PREP)
    wait_model(page, webgl=False)
    hero_shot(page, ART / "r4c-fa-1440-light-hero-still-fallback.png")
    shots.append(str(ART / "r4c-fa-1440-light-hero-still-fallback.png"))
    page.goto(BASE + "/products/suction-bag/?theme=dark", wait_until="load", timeout=120000)
    page.evaluate(PREP)
    wait_model(page, webgl=False)
    hero_shot(page, ART / "r4c-fa-1440-dark-hero-still-fallback.png")
    shots.append(str(ART / "r4c-fa-1440-dark-hero-still-fallback.png"))
    ctx.close()

    ctx = browser.new_context(
        viewport={"width": 390, "height": 844},
        device_scale_factor=2,
    )
    ctx.add_init_script("""(() => {
      const proto = HTMLCanvasElement.prototype;
      const orig = proto.getContext;
      proto.getContext = function(type, attrs) {
        if (type && String(type).includes('webgl')) return null;
        return orig.call(this, type, attrs);
      };
    })();""")
    page = ctx.new_page()
    page.goto(BASE + "/products/suction-bag/?theme=light", wait_until="load", timeout=120000)
    page.evaluate(PREP)
    wait_model(page, webgl=False)
    overflow.append({"page": "fa-light-390-fallback", **overflow_ok(page)})
    page.locator(".cin-stage").screenshot(path=str(ART / "r4c-fa-390-light-hero-still-fallback.png"))
    shots.append(str(ART / "r4c-fa-390-light-hero-still-fallback.png"))
    ctx.close()

    for w, lang, tag in ((390, "fa", "fa"), (320, "en", "en")):
        ctx = browser.new_context(viewport={"width": w, "height": 844}, device_scale_factor=2)
        page = ctx.new_page()
        route = "/products/suction-bag/" if lang == "fa" else "/en/products/suction-bag/"
        page.goto(BASE + route + "?theme=light", wait_until="load", timeout=120000)
        page.evaluate(PREP)
        overflow.append({"page": f"{tag}-light-{w}", **overflow_ok(page)})
        page.locator("#uses .use-tier").nth(1).screenshot(path=str(ART / f"r4c-{tag}-{w}-light-uses.png"))
        shots.append(str(ART / f"r4c-{tag}-{w}-light-uses.png"))
        ctx.close()

    browser.close()

out = {"overflow": overflow, "shots": shots}
(ART / "suction-bag-round4c.json").write_text(json.dumps(out, indent=2))
print(json.dumps(out, indent=2))
