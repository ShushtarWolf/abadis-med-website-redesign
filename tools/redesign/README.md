# Phase-2 page generator (Siamak redesign)

Builds the Persian pages of the redesign preview into `site/` from crawl data.

```
python3 tools/redesign/build.py            # all groups
python3 tools/redesign/build.py products   # one group: products | about | dealers | calculator | csr |
                                           # contact | customers | experiences | downloads | install |
                                           # faq | careers | posts
python3 tools/redesign/apply_shell.py      # re-apply shared header/footer to the hand-built pages
```

* **Content source:** abadis-med.com was unreachable from the build box, so copy comes from the
  Wayback Machine snapshots (Feb–Jun 2026) of each page, extracted into `data/pages.json`,
  `data/posts.json` and `data/jobs.json`. All copy is verbatim; nothing is invented.
* **Images:** downloaded from the Wayback Machine (`im_` mode, plus CDX look-ups for alternate sizes
  and the site's own `-copy.webp` re-uploads) and converted to WebP in `site/assets/img/c/`.
  The raw cache path is `$ABADIS_IMG_RAW` (default `/workspace/abadis-wb/img-raw`); only files listed as
  `ok` in `data/imgmap.json` are used. Images the archive never captured are shown as a
  neutral branded tile (products/posts), a letter tile (customers/team) or omitted.
* **Hand-built pages** (home, suction bag, CSR story, contact) are only patched in marked blocks
  (`<!-- phase2:… -->`) and links/footers.
* **News vs articles:** WordPress category where the crawl knows it (`newss` → news, `blog` → articles),
  otherwise a title-keyword heuristic in `cats.py`. Old job ads (`ads`) are not republished as posts.
* Posts that exist on the live site but were never archived are listed and linked to the live URL.
