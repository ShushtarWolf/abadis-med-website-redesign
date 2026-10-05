# «نجات زاگرس» — CSR page notes

Source (verbatim copy): https://abadis-med.com/نجات-زاگرس،مسئولیت-اجتماعی-آبادیس/

## Facts (as published by Abadis)
- In 1395 over 75 fires destroyed ~950 ha of Zagros forest.
- Abadis, with **ایده‌پردازان نواندیش فردا (Dpaper)**, planted oaks on Arbor Day — one per member of its family of **400+ medical centres** — targeting **1000** saplings by Ordibehesht 1403, so a place named «آبادیس» is registered in the Zagros highlands.
- **15 Esfand 1402** (Arbor Day): «همایش نجات زاگرس» at the University of Science and Culture international conference centre; ~**800** participants in person + online. Co-sponsors: Shatel, other private brands, artists.
- Abadis managers gave oak-planting plaques to hospitals leading in infection control.
- **30 Tir 1403**: Abadis backed and signed the «کارزار درخواست نجات زاگرس» (letter to the president, 8 proposals) — full text is in the page under a `<details>` toggle.
- Slogan: «ما به اندازه یک سرانگشت اثر می‌گذاریم، به شما، به طبیعت، به جهان.»
- Species often named in demo copy: Persian oak *Quercus brantii* (not stated on the live page — keep as context only).
- The demo's "4,000 by end of 1405" goal is **not** on the live page; it was dropped from the redesign.

## Painting
- `site/assets/img/zagros-koh.jpg` — latest painted koh (Tak-Macaron-style: mint watercolour peaks + baked-in oaks), from scroll-scrub `zagros/img/zagros-koh.jpg` @ `5abc281`.
- Rejected directions (don't revisit): photo-wash filters, sticker seedlings, separate animated sapling overlays.
- Future: a human illustrator can redraw it with layered PNGs (mountain + separate oaks) for gentle animation.

## Background behaviour on `/csr/`
- Full-page fixed background. Starts at `opacity: 0`; after the image is decoded it **fades in** over 2.4s (`cubic-bezier(.22,.61,.36,1)`). No pop, no scale, no parallax, no mouse tracking.
- A theme-aware veil sits above it (light: mint wash; dark: deep teal; noir: purple-black) so text stays readable.
