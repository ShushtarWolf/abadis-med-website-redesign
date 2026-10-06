# Phase-2 page generator (Siamak redesign)

Builds the Persian pages of the redesign preview into `site/` from crawl / REST data.

**Current generator:** `python3 tools/redesign/build.py`  
**Legacy (do not run):** `tools/build_site.py` — old phase-1 script; it would overwrite hand-built pages with the old 4-item nav.

```
python3 tools/redesign/build.py            # all groups
python3 tools/redesign/build.py products   # one group: products | about | dealers | calculator | csr |
                                           # contact | customers | experiences | downloads | install |
                                           # faq | careers | posts
python3 tools/redesign/apply_shell.py      # re-apply shared header/footer to the hand-built pages
```

Requires **Python 3.10+** and **Pillow** (`pip install pillow`).

* **Content source:** copy comes from Wayback Machine snapshots and/or the live WP REST API
  (`http://abadis-med.com/wp-json/...`), extracted into `data/pages.json`, `data/posts.json` and
  `data/jobs.json`. All copy is verbatim; nothing is invented.
* **Images:** WebP outputs live in `site/assets/img/c/` (name = `sha1(path)[:12]-{maxw}.webp`).
  `img()` reuses an existing WebP even when the raw cache is absent, so rebuilds on a PC keep
  images. Raw files (optional) go in `$ABADIS_IMG_RAW` (default `tools/redesign/.img-raw/`,
  gitignored). Only URLs marked `ok` in `data/imgmap.json` are converted from raw. Missing
  captures stay as branded tiles / letter avatars.
* **Hand-built pages** (home, suction bag, CSR story, contact) are only patched in marked blocks
  (`<!-- phase2:… -->`) and links/footers.
* **News vs articles:** WordPress category where known (`newss` → news, `blog` → articles),
  otherwise a title-keyword heuristic in `cats.py`. Old job ads (`ads`) are not republished as posts.
* Posts that exist on the live site but were never archived are listed and linked to the live URL.
