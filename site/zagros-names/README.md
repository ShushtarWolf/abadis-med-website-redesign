# Zagros CSR page — three samples for showing the hospital names

Deploy as `site/zagros-names/` → https://shushtarwolf.github.io/abadis-med-website-redesign/zagros-names/

Each sample is the approved «نجات زاگرس» page (text, layout, scene, themes) with only the names presentation changed.
The base page's three hard-coded name stakes are removed.

- `names.json` holds 1,253 names, from Sheet1 column B «نام مرکز درمانی» (1,270 rows), whitespace-trimmed and with exact duplicates removed. They are in the list's own order. Every counter is computed from this length (۱٬۲۵۳ مرکز درمانی).
- `1-tree-tags/`: one wooden tag at each oak's base. Scroll rotates each tree through its share of the list (tree k shows names k, k+S, k+2S…), so all 1,253 names pass by. Leaving tags drift back toward the horizon and fade, and the scene pans slowly. Each frame, tags are checked against the hero copy, the risen canister, the counter and each other.
- `2-sky-ribbons/`: 2–3 rows of names drifting right to left in the misty band between the hero copy and the grown treeline. Each row moves at its own speed, the edges are faded, and scrolling back reverses the drift. Only on-screen names exist in the DOM (pooled spans, canvas metrics).
- `3-wall-of-honor/`: a calm pinned section after the hero, with a counter, Persian-collated columns that move with scroll parallax, and a search box that dims the rest, highlights matches, scrolls to the match and lights it up. Enter jumps to the next match.
- `shared/`: template CSS/JS/images, scene art (WebP plus JPG/PNG fallbacks), and `zagros-hero.js`. The scene code is the base code plus small layout/render hooks, with the stakes removed. `names-common.js` holds the shared helpers.
- Kalameh loads from the same template host as the base page. Reduced motion shows static versions.
