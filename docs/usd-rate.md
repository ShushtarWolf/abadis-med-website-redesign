# USD toman rate (savings calculator)

Surgery and bed **cost** uses the free-market dollar. Water and staff-hour coefficients are unchanged.

On load the page fetches TGJU symbol `price_dollar_rl` (quoted in rial):

`https://api.tgju.org/v1/market/indicator/today-table-data/price_dollar_rl?lang=fa&start=0&length=1`

`api.tgju.org` sends `Access-Control-Allow-Origin: *`, so the browser can read it with no API key and no proxy. `length=1` is the latest tick. toman = rial / 10.

`https://call.tgju.org/ajax.json` is the feed www.tgju.org polls (`current.price_dollar_rl.p`, same rial price) but it does not send CORS headers, so this site cannot read it. The static site has no same-origin proxy. The `api.tgju.org` URL above is the public endpoint that works from a browser.

Fallback order:

1. Live TGJU price. On success it is saved to `localStorage["abadis-usd-toman"]` as `{ toman, rial, updatedAt, source }`.
2. If the fetch fails (CORS, offline, HTTP error, timeout at 8s, or a price that does not parse): the last saved `abadis-usd-toman` value, when it has a positive `toman`.
3. Otherwise `LAST_KNOWN_USD_TOMAN` = 269500 (2,695,000 rial on 2026-10-25).

The page paints with step 2 or 3 immediately, then replaces the cost if step 1 returns a different rate. No weekly bot and no rate file.
