# News and academy cutover — keep publishing

The team keeps publishing news and academy articles on the live WordPress site (`abadis-med.com`). Do not freeze the editorial calendar for the redesign cutover.

`scripts/sync-abadis-news.mjs` compares the live posts with this repo and, when you ask it to, copies only what is new or modified.

## Commands

```bash
node scripts/sync-abadis-news.mjs --help
node scripts/sync-abadis-news.mjs --check
node scripts/sync-abadis-news.mjs --dry-run
node scripts/sync-abadis-news.mjs --sync
node scripts/sync-abadis-news.mjs --self-test
```

`--check` is the default when no mode flag is given. `--check` and `--dry-run` never write files. Add `--locale fa`, `--locale en`, or `--locale ar` to limit the comparison. Add `--json` for a machine-readable report.

`--sync` writes only the delta:

- `content/<lang>/<news|articles>/<id>.md` — Nuxt Content
- `tools/redesign/data/posts.json` — Persian generator archive
- `tools/redesign/data/en_posts.json` and `tools/redesign/data/ar_posts.json`
- `tools/redesign/data/news-sync-state.json` and `news-delta.json` — last run

A second `--sync` with no newer live edits leaves those files unchanged.

After a sync that changed the manifests, regenerate the HTML:

```bash
python3 tools/redesign/build.py posts
```

Featured images that are not already in `tools/redesign/data/imgmap.json` still need the existing image fetch (`tools/redesign/fetch_posts_rest.py`) before the generator can show them. The sync records the live media URL; it does not download binaries.

## What it compares

For each language it reads the WordPress REST API over plain HTTP:

- Persian: `http://abadis-med.com/wp-json/wp/v2/posts`
- English: `http://abadis-med.com/en/wp-json/wp/v2/posts`
- Arabic: `http://abadis-med.com/arabic/wp-json/wp/v2/posts`

If REST is unreachable it falls back to the post sitemap, then the RSS feed. Sitemap and feed hits that have no WordPress id are listed as unmatched and are not written.

A post is **new** when its id is missing from the language manifest and (for Persian) from `site/news/<id>/` and `site/articles/<id>/`. It is **modified** when the live `modified` time is more than two seconds newer than the copy in the manifest. Ads are skipped. News versus academy follows the live category (`newss` / `blog` and the Persian category ids already used by the generator).

`--check` reporting a delta is expected while the live site stays ahead of the last archive. That is the point of the command: publishing continues, and the delta is pulled at cutover.
