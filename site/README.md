# Abadis Med — redesign preview (static)

Plain HTML/CSS/JS, no build step needed to serve. Persian RTL, Kalameh.

| Page | Path |
|---|---|
| Home | `/` |
| Products hub | `/products/` |
| Suction bag (product) | `/products/suction-bag/` |
| CSR — نجات زاگرس | `/csr/` |
| Contact | `/contact/` |
| (+ generated pages) | `about/`, `news/`, `articles/`, `dealers/`, `customers/`, … |

- Themes: light / dark / noir — header switch, saved in `localStorage["abadis-theme"]`, or `?theme=noir` in the URL.
- Mosaic video heroes, CSR painting fade-in, no mouse-move effects — details in `docs/abadis/redesign-context/`.
- **Generator:** `python3 tools/redesign/build.py` (Pillow required). Hand-built chrome: `python3 tools/redesign/apply_shell.py`.
- **Do not run** `tools/build_site.py` — that is the legacy phase-1 generator.
- Local: `python3 -m http.server 8080 --directory site` → http://localhost:8080/
- `noindex,nofollow` on every page — preview only; contact form hands off to email (no backend yet).
