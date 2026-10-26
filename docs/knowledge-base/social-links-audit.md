# Social links audit — 26 Oct 2026

Fetched live HTML over `http://abadis-med.com` (homepage FA, homepage EN, FA contact, EN contact, AR contact). Redesign footers are the shared pill row from `tools/redesign/layout.py` (`footer_pills_html`), painted into FA, EN, and AR pages. Commit `20263638` / `task-35-footer-menu-fixes` is not in this clone; the icon row that is here is the one already on `siamak/redesign`.

Pinterest has **no profile URL** anywhere in those live pages. Elementor only ships a `.elementor-social-icon-pinterest` color rule and a share-button config key. The redesign shows the icon as a non-link placeholder: `data-social="pi"`, `data-status="placeholder"`, `data-official-url=""`, `data-note="no official Pinterest URL on abadis-med.com"`, no `href`.

## Instagram, LinkedIn, Facebook, Pinterest

| Network | On abadis-med.com (26 Oct 2026) | Wired in the redesign |
| --- | --- | --- |
| Instagram | Homepage FA and EN icon row: `https://www.instagram.com/abadis.med/` · EN contact body and AR contact body: `https://www.instagram.com/abadismedical.co` | Footer FA / EN / AR and FA contact list: `https://www.instagram.com/abadismedical.co` (the contact-page handle). Homepage handle `abadis.med` is real and is **not** the footer href. |
| LinkedIn | Homepage FA and EN icon row: `https://www.linkedin.com/company/abadis-medical-co/` · EN and AR contact bodies: **absent** | Footer FA / EN / AR: `https://www.linkedin.com/company/abadis-medical-co/` · FA contact list and EN/AR contact `soc-links`: same URL, copied from the live homepage row |
| Facebook | Icon row: `https://fb.com/AbadisMedCo` · one extra homepage href `https://www.facebook.com/AbadisMedCo/` · EN and AR contact bodies: `https://fb.com/AbadisMedCo` | Footer FA / EN / AR and FA / EN / AR contact bodies: `https://fb.com/AbadisMedCo` |
| Pinterest | **No profile URL** | Placeholder only. Footer class `foot-pill--pi foot-pill--placeholder`. Contact bodies: `<span class="soc-placeholder" data-social="pinterest" data-status="placeholder" data-official-url="">` |

## Other footer icons

| Network | On abadis-med.com | Wired in the redesign footer (FA, EN, AR) |
| --- | --- | --- |
| WhatsApp | `https://wa.me/+989100145809` | `https://wa.me/989100145809` |
| Telegram | `https://t.me/abadis_med` | `https://t.me/abadis_med` |
| Aparat | FA homepage and AR contact: `https://www.aparat.com/abadismed` · EN homepage icon row in this fetch: absent | `https://www.aparat.com/abadismed` |
| YouTube | `https://www.youtube.com/channel/UC2J9yTFmf6fHLhKQ6y3gdCw/featured?view_as=subscriber` | same |
| X / Twitter | `https://twitter.com/abadismed` | `https://twitter.com/abadismed` |
| Threads | FA homepage icon row: `https://www.threads.net/@abadis.med?igshid=MzRlODBiNWFlZA==` | not in the redesign pill row |
| Medium | FA homepage: `https://medium.com/@abadismedical` | not in the redesign pill row |
| Virgool | FA homepage: `https://virgool.io/@m_13865698` | not in the redesign pill row |
| yek.link | FA / EN / AR contact “social networks” line: `https://yek.link/abadis.med` | kept where the contact page already had it; not a footer pill |

Phone pill `tel:+982192001017` and mail pill `mailto:info@abadis-med.com` sit in the same row. They are not social profiles.
