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

Trash, unpublish, or delete sends the mu-plugin in `wordpress/mu-plugins/` with `action=unpublish` or `action=delete`. The sync removes that id from the manifest, the markdown file, and the slug page. A scheduled sync also removes ids recorded in `tools/redesign/data/news-sync-state.json` when a non-empty published REST list no longer contains them. Posts this pipeline has never written stay in the archive. An empty REST response does not wipe the archive.

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
