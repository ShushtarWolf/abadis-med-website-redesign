#!/usr/bin/env python3
"""Cinematic scroll render timing @ 390 (before vs after). Playwright CDP 4× throttle
often starves timers — we enable 4× during scrub, and also report unthrottled scrub."""
import json
import statistics
import subprocess
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ART = Path("/opt/cursor/artifacts")
OLD_JS = subprocess.check_output(
    ["git", "show", "728fc460:site/assets/js/p01-cinematic-page.js"],
    cwd=ROOT,
    text=True,
)
NEW_JS = (ROOT / "site/assets/js/p01-cinematic-page.js").read_text()
HOOK = (
    "if(window.__cin_profile_on){const _p=performance.now();const _g=window.__cin_profile||{frames:[]};"
    "if(_g.last)_g.frames.push(_p-_g.last);_g.last=_p;window.__cin_profile=_g;}"
)
OLD_JS = OLD_JS.replace("R.render(S,C);", HOOK + "R.render(S,C);")
BASE = "http://127.0.0.1:8080"
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
SCROLL = """async (throttleRate) => {
  const film = document.getElementById('film');
  const steps = 50;
  const total = Math.max(1, film.offsetHeight - window.innerHeight);
  window.__cin_profile_on = 1;
  window.__cin_profile = { frames: [], last: 0 };
  for (let i = 0; i <= steps; i++) {
    window.scrollTo(0, Math.round((i / steps) * total));
    await new Promise((r) => setTimeout(r, throttleRate ? 96 : 40));
  }
  await new Promise((r) => setTimeout(r, throttleRate ? 2400 : 800));
  const scrub = (window.__cin_profile.frames || []).filter((x) => x > 0 && x < 200);
  window.__cin_profile = { frames: [], last: performance.now() };
  await new Promise((r) => setTimeout(r, throttleRate ? 2400 : 1500));
  const idle = (window.__cin_profile.frames || []).filter((x) => x > 0 && x < 200);
  return { scrub, idleCount: idle.length };
}"""


def stats(frames):
    if not frames:
        return {"n": 0}
    s = sorted(frames)
    n = len(s)
    return {
        "n": n,
        "mean_ms": round(statistics.mean(s), 2),
        "p50_ms": round(s[n // 2], 2),
        "p95_ms": round(s[min(n - 1, int(n * 0.95))], 2),
        "max_ms": round(max(s), 2),
    }


def run(js_body: str, cpu4: bool):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(**IPHONE)
        page = ctx.new_page()
        if cpu4:
            ctx.new_cdp_session(page).send("Emulation.setCPUThrottlingRate", {"rate": 4})

        def route_p01(route):
            if "p01-cinematic-page.js" in route.request.url:
                route.fulfill(status=200, content_type="application/javascript", body=js_body)
            else:
                route.continue_()

        page.route("**/p01-cinematic-page.js*", route_p01)
        page.goto(BASE + "/products/suction-bag/?theme=light", wait_until="load", timeout=120000)
        page.evaluate(PREP)
        page.wait_for_function("() => window.__ready === true", timeout=120000)
        data = page.evaluate(SCROLL, cpu4)
        ctx.close()
        browser.close()
    return {
        "scrub": stats(data["scrub"]),
        "idle_render_frames_after_scrub": data["idleCount"],
    }


out = {
    "viewport": "390x844",
    "metric": "ms between R.render() during hero scrub; idle_render_frames = renders in ~1.5s after scrub ends",
    "before_728fc460": {
        "cpu_throttle_4x": run(OLD_JS, True),
        "no_throttle": run(OLD_JS, False),
    },
    "after_current": {
        "cpu_throttle_4x": run(NEW_JS, True),
        "no_throttle": run(NEW_JS, False),
    },
}
(ART / "cin-scroll-profile.json").write_text(json.dumps(out, indent=2))
print(json.dumps(out, indent=2))
