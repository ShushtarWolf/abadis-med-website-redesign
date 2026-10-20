# Angry Bags — leaderboard backend (Google Apps Script + Google Sheet)

The game is a static site, so scores go to a tiny free backend: a Google Sheet
with an Apps Script web app attached. No server, no paid account, no keys in
the site. Until an endpoint URL is set in `../config.json`, the game shows
"coming soon" for the form and the leaderboard and **sends/stores nothing**.

## What is stored
One row per phone per month (`Asia/Tehran` calendar month, Gregorian `yyyy-MM`):
`month, phone, name, score, level, updated, consent, lang, attempts`. Only the
best score of the month is kept. The sheet is private to its owner.
The public leaderboard (`GET ?action=board`) returns only a **masked name**
(e.g. `حم…د`) and the score — never the phone. The game never saves the phone
in the browser.

## Setup (≈10 minutes, Abadis Google account)
1. Go to <https://sheets.google.com> → create a blank sheet, name it
   `Angry Bags leaderboard`. Keep it private (do not share it publicly).
2. In the sheet: **Extensions → Apps Script**. Delete the sample code and paste
   the whole of `Code.gs` from this folder. Click **Save**.
3. In the editor, choose function `setup` → **Run**. Approve the permission
   prompt (Google will warn "unverified app" — it is your own script: Advanced →
   Go to project). The log should print `9300`, and a tab `entries` appears.
4. **Deploy → New deployment** → type **Web app**.
   - Description: `angry-bags v1`
   - Execute as: **Me**
   - Who has access: **Anyone**
   Click **Deploy** and copy the **Web app URL** (ends in `/exec`).
5. Test it in a browser: `<URL>?action=board` → `{"ok":true,"month":"…","rows":[]}`.
6. Put the URL into `site/seed-slingshot/config.json`:
   ```json
   "leaderboard": { "endpoint": "https://script.google.com/macros/s/XXXX/exec", ... }
   ```
   commit and push. The form and leaderboard switch on automatically.
7. Updating the script later: **Deploy → Manage deployments → Edit (pencil) →
   Version: New version → Deploy**. The URL stays the same.

## Picking winners
Filter the `entries` sheet by month, sort by score. Before giving a prize,
sanity-check the top rows (attempts, timing) — see limits below. Delete rows
older than you need (privacy).

## Anti-abuse (what it does)
- One submission per phone per 20 s; at most 120 submissions per minute total.
- Score is recomputed on the server from its parts (jars, nurses, oaks, stars,
  bags left) with per-level caps; impossible combinations, too-fast runs
  (< 1.5 s per bag) and mismatching scores are rejected.
- One row per phone per month, best score kept.

## Limits (be honest with the prize rules)
- The game runs in the browser, so someone who reads the code can send a
  plausible maximum score by hand. Checks only make it harder. Treat the board
  as fun, and verify winners (e.g. call them, ask for a screenshot).
- Apps Script cannot see IP addresses, so the rate limit is per phone + global.
- Apps Script quotas (free account): ~20k URL calls/day, 6 min/execution —
  ample for this game.
- If `LEVELS`/`SCORE` in `config.json` change, update the same tables at the top
  of `Code.gs` and redeploy.
