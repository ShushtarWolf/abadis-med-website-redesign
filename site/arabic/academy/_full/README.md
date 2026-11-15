# Full page backup (not linked from the site)

This folder holds the complete previous version of the page, kept so nothing is deleted.

- It is not linked from the header, footer, or language switcher.
- Search engines should ignore it (`noindex`, and a local robots.txt).
- To restore it, copy `index.html` (and any siblings) back to the parent folder and, for Academy pages only, shorten each relative `href`/`src`/`content` that was given an extra `../`.

The public Coming Soon page lives in the parent folder.
