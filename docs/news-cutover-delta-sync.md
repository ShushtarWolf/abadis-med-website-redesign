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

After a sync that changed the manifests, regenerate the HTML (this set only; do not run `build.py` with no group arguments):

```bash
python3 tools/redesign/build.py posts home i18n archives
```

`--sync` also writes `content/<lang>/<news|articles>/<id>.md`. The static generator still reads `posts.json`, `en_posts.json`, and `ar_posts.json`.

## WordPress bases

`ABADIS_WP_REST`, `ABADIS_WP_SITEMAP`, and `ABADIS_WP_FEED` override the Persian base. English uses `ABADIS_WP_REST_EN`, `ABADIS_WP_SITEMAP_EN`, `ABADIS_WP_FEED_EN`. Arabic uses `ABADIS_WP_REST_AR`, `ABADIS_WP_SITEMAP_AR`, `ABADIS_WP_FEED_AR`. When a variable is unset, the URL stays on `http://abadis-med.com/...`, so `--check` still compares the live site.

`ABADIS_WP_USER` and `ABADIS_WP_APP_PASSWORD` (a WordPress Application Password) are sent as Basic auth on `/wp-json/` only, and only when both are set.

If the CMS is still Persian-only, set the FA variables to that site and leave EN/AR unset. They keep syncing from abadis-med.com. Do not point the EN or AR base at the FA REST root. A locale whose REST, sitemap, and feed all fail is reported and not written.

## Already on disk

After `url_migrate.py`, Persian posts live at `/<slug>/`, not `site/news/<id>/` or `site/articles/<id>/`. English is `/en/<slug>/` and Arabic is `/arabic/<slug>/`. A post is not new when its id or slug is in the manifest, or when that slug directory already has a real `index.html` (redirect stubs do not count).

## Media

`--sync` downloads featured and in-body images for new and modified posts, writes WebP in a temp file, and uploads to the public bucket `abadis-media` (S3-compatible). The URL map is `tools/redesign/data/media-bucket.json`. Manifests, markdown, and generated HTML then use the bucket URL. `.img-raw/` and any wp-content dump stay untracked.

Required secrets when there is a new image (the command exits 2 and writes nothing if one is missing):

- `ABADIS_MEDIA_ACCESS_KEY`
- `ABADIS_MEDIA_SECRET_KEY`
- `ABADIS_MEDIA_S3_ENDPOINT` (Liara panel; often `https://storage.iran.liara.space`)
- `ABADIS_MEDIA_PUBLIC_BASE` (public bucket origin, no trailing slash)

Optional: `ABADIS_MEDIA_BUCKET` (default `abadis-media`), `ABADIS_MEDIA_S3_REGION` (default `us-east-1`).

A second `--sync` with no newer WordPress edits does not rewrite manifests and does not upload again.

## Unpublish

Trash, unpublish, or delete sends the mu-plugin in `wordpress/mu-plugins/` with `action=unpublish` or `action=delete`. The sync removes that id from the manifest, the markdown file, `sitemap.xml`, and listing cards (news and articles indexes, category and tag pages, and the homepage carousel). It does not leave the slug as a live page.

The old URL 301s to the post's category page when that page exists, otherwise to the news hub (`/آخرین-اخبار/`) or the articles hub (`/مقالات/`). English and Arabic use `/en/latest-news/` or `/en/blog/`, and `/arabic/الاخبار/` or `/arabic/articles/`. The same target is written for `/news/<id>/`, `/articles/<id>/`, and any other path already mapped onto that slug. Example:

```
rewrite "^/sample-post/?$" "https://$host/%D8%A2%D8%AE%D8%B1%DB%8C%D9%86-%D8%A7%D8%AE%D8%A8%D8%A7%D8%B1/" permanent;
```

The rules are one marked block, `# BEGIN abadis-unpublished-posts` … `# END abadis-unpublished-posts`, in `site/liara_nginx.conf` and the same paths in `site/_redirects`. A second run replaces the block instead of duplicating it. `url_migrate.py` keeps the block when it rewrites those files. Republishing the post removes its 301; the next posts build writes the page again.

A scheduled sync also removes ids recorded in `tools/redesign/data/news-sync-state.json` when a non-empty published REST list no longer contains them. Posts this pipeline has never written stay in the archive. An empty or failed REST response does not remove anything.

## FA only, until EN and AR are switched on

`--check` and `--dry-run` still compare Persian, English, and Arabic, and they still use abadis-med.com when the overrides are unset.

`--sync` does not. It changes a language only when that language is listed in `ABADIS_SYNC_LANGS` (default `fa`) or its REST override is set (`ABADIS_WP_REST`, `ABADIS_WP_REST_EN`, `ABADIS_WP_REST_AR`). With only the Persian override set, English and Arabic are not fetched, written, or unpublished. They are not treated as missing just because the Persian CMS does not list them.

To publish English later, set `ABADIS_WP_REST_EN` (and the matching sitemap and feed if you need them), or set `ABADIS_SYNC_LANGS=fa,en`. Arabic is the same with `ABADIS_WP_REST_AR` or `ar` in `ABADIS_SYNC_LANGS`.

## One slug, CMS wins

Slugs are compared after percent-decoding and Unicode NFC, so a CMS path stored as `%D8%B3%D8%AA-...` and a legacy path stored as `ست-...` are the same page. When one post comes from `abadis-wp-test` and another was imported from `abadis-med.com`, the CMS post keeps the slug page. The legacy id is not deleted from `posts.json`. Its `/news/<id>/` and `/articles/<id>/` URLs 301 to that slug, so the old address still resolves and the legacy record is not dropped silently. Two posts that are not a CMS-plus-legacy pair still fail the build if they share a slug.

## GitHub Actions

`tools/liara/publish-wp.yml` is the workflow. If it is not already at `.github/workflows/publish-wp.yml`, copy it there (the push token may lack the workflow scope). It is registered for `repository_dispatch` type `wordpress-publish`, every 15 minutes, and `workflow_dispatch`, but the job does nothing until the repository variable `ABADIS_PUBLISH_ENABLED` is the string `1`. That variable is off by default. Schedule, dispatch, and manual runs all skip while it is unset or any other value.

Set the secrets first, then set `ABADIS_PUBLISH_ENABLED` to `1`. Required before a run will sync: `ABADIS_WP_REST`, `ABADIS_MEDIA_ACCESS_KEY`, `ABADIS_MEDIA_SECRET_KEY`, `ABADIS_MEDIA_S3_ENDPOINT`, and `ABADIS_MEDIA_PUBLIC_BASE`. If any of those is missing, the sync step exits before it writes or commits. It will not fall back to abadis-med.com and it will not publish hotlinked wp-content images. Local `--check` still uses the live site when those variables are unset. That command does not commit.

When the variable is `1` and those secrets are set, the workflow syncs, uploads media, runs the posts build, and commits each branch separately. It does not merge `main` into `liara-test`. It deploys `site/` to Liara app `abadis-test` only (`--app abadis-test`, team `6af9496176b2026d7493a542`, secret `LIARA_API_TOKEN`). It does not deploy `abadis-med`. The gzipped site must stay under 320 MB.

Other GitHub secrets: `LIARA_API_TOKEN`, `ABADIS_WP_WEBHOOK_SECRET`, and, if the CMS is private, `ABADIS_WP_USER` and `ABADIS_WP_APP_PASSWORD`. Optional URL overrides use the `ABADIS_WP_REST_EN`, `ABADIS_WP_REST_AR`, sitemap, and feed names above. The WordPress side uses `ABADIS_DISPATCH_TOKEN` and `ABADIS_WEBHOOK_SECRET` (see `wordpress/mu-plugins/README.md`).

## What it compares

For each language it reads the WordPress REST API over plain HTTP:

- Persian: `http://abadis-med.com/wp-json/wp/v2/posts`
- English: `http://abadis-med.com/en/wp-json/wp/v2/posts`
- Arabic: `http://abadis-med.com/arabic/wp-json/wp/v2/posts`

If REST is unreachable it falls back to the post sitemap, then the RSS feed. Sitemap and feed hits that have no WordPress id are listed as unmatched and are not written.

A post is **new** when its id and slug are missing from the language manifest and from the live slug page (`/<slug>/`, `/en/<slug>/`, or `/arabic/<slug>/`). Legacy `site/news/<id>/` and `site/articles/<id>/` folders still count. It is **modified** when the live `modified` time is more than two seconds newer than the copy in the manifest. Ads are skipped. News versus academy follows the live category (`newss` / `blog` and the Persian category ids already used by the generator).

`--check` reporting a delta is expected while the live site stays ahead of the last archive. That is the point of the command: publishing continues, and the delta is pulled at cutover.
