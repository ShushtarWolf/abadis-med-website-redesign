# Abadis publish dispatch (mu-plugin)

Copy `abadis-publish-dispatch.php` to `wp-content/mu-plugins/` on `abadis-wp-test`. It does not run from this repository by itself. It sends no mail and stores no passwords.

On publish, update, unpublish (including trash), and delete of a `post`, it POSTs a signed `repository_dispatch` named `wordpress-publish` to GitHub Actions. The signature is HMAC-SHA256 over:

```
action\npost_id\nstatus\nlang\nts
```

The Actions workflow checks that signature with `ABADIS_WP_WEBHOOK_SECRET` (the same value as `ABADIS_WEBHOOK_SECRET` on the CMS). Timestamps older than 30 minutes are rejected.

## Environment variables (WordPress)

Set these in the CMS host environment, or as `define()` lines in `wp-config.php`. Do not commit the values.

| Name | Purpose |
| --- | --- |
| `ABADIS_WEBHOOK_SECRET` | Shared HMAC secret. Same value as GitHub secret `ABADIS_WP_WEBHOOK_SECRET`. |
| `ABADIS_DISPATCH_TOKEN` | GitHub PAT with `repo` scope (or a fine-grained token that can write Actions dispatches on this repo). Sent as `Authorization: Bearer`. |
| `ABADIS_DISPATCH_URL` | Optional. Default `https://api.github.com/repos/ShushtarWolf/abadis-med-website-redesign/dispatches`. Set a worker URL only if that worker forwards the same signed body to GitHub. |
| `ABADIS_WP_LANG` | Optional. `fa` (default), `en`, or `ar` when this CMS is a single-language site. Polylang is used when present. |

If `ABADIS_WEBHOOK_SECRET` or `ABADIS_DISPATCH_TOKEN` is empty, the plugin does nothing.

## Application Password (for the sync, not for this plugin)

The static sync reads the WordPress REST API from GitHub Actions. Public posts need no password. If `abadis-wp-test` is private, create an Application Password in WordPress:

1. Users, Profile, Application Passwords. Name it `abadis-static-sync`.
2. Store the generated password and the account login as GitHub Actions secrets. Do not put them in this repo.

| GitHub secret | Value |
| --- | --- |
| `ABADIS_WP_USER` | WordPress username |
| `ABADIS_WP_APP_PASSWORD` | The Application Password (spaces are fine) |

The sync sends them as Basic auth only on `/wp-json/` requests, and only when both are set. `--check` against `abadis-med.com` leaves them unset.

## Turn the Actions pipeline on

The workflow job is a no-op until the repository variable `ABADIS_PUBLISH_ENABLED` is `1`. It is off by default, including the 15-minute schedule. Set the secrets first, then set the variable.

1. Add GitHub Actions secrets `ABADIS_WP_REST` (the CMS REST base, not abadis-med.com), `ABADIS_MEDIA_ACCESS_KEY`, `ABADIS_MEDIA_SECRET_KEY`, `ABADIS_MEDIA_S3_ENDPOINT`, and `ABADIS_MEDIA_PUBLIC_BASE`. Also add `LIARA_API_TOKEN` and `ABADIS_WP_WEBHOOK_SECRET` (this plugin's `ABADIS_WEBHOOK_SECRET`). Add `ABADIS_WP_USER` and `ABADIS_WP_APP_PASSWORD` when the CMS is private.
2. Set the repository variable `ABADIS_PUBLISH_ENABLED` to `1`.

If publish is enabled and any of `ABADIS_WP_REST` or the four media secrets is missing, the sync step fails before it commits. It does not fall back to the live site and it does not hotlink wp-content images.

## Unpublish

Trash, draft, and delete of a published post send `action=unpublish` or `action=delete` with that post id and language. The next sync removes that id from the manifest, `content/<lang>/.../<id>.md`, and the slug page. A scheduled sync also drops ids this pipeline previously wrote (see `tools/redesign/data/news-sync-state.json`) when a non-empty published REST list no longer contains them. Legacy archive posts that this pipeline has never written are left in place.
