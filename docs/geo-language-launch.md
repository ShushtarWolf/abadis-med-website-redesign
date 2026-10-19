# English suggestion at launch (Liara / Cloudflare)

The static site already suggests English **in the browser**, once, for visitors
on a Persian page whose country is not Iran. It uses Cloudflare
`/cdn-cgi/trace` when that endpoint exists, then `https://api.country.is`
(no key, short timeout). Failure does nothing. Crawlers are not offered the
bar, and nothing redirects on its own.

At launch, do the same check **on the first HTML response** and keep the
client bar as the only language change. Do not 301/302 by country.

## Override cookie

The page sets `abadis_lang` when the visitor chooses:

| Cookie | Meaning |
|---|---|
| *(absent)* | No choice yet |
| `abadis_lang=fa` | Stay in Persian |
| `abadis_lang=en` | Visitor chose English |

`Path=/; Max-Age=31536000; SameSite=Lax`. If this cookie is present, the
server must pass the request through. That is the override: a later visit to
a Persian URL stays on that URL.

The browser also stores `abadis-lang-suggest` in `localStorage` (`seen`,
`fa`, or `en`) so the bar is not shown again.

## Cloudflare

Use this when the domain is proxied (orange-cloud), including Cloudflare in
front of Liara. A Worker or Snippet on `GET` HTML:

1. Skip anything that is not an HTML document.
2. Skip `/en/…` and `/arabic/…`.
3. Skip if the `User-Agent` looks like a crawler (Googlebot, Bingbot, and the
   usual preview bots). Never answer those with a redirect.
4. Skip if `Cookie` already contains `abadis_lang=`.
5. Read `CF-IPCountry`. If it is `IR`, empty, `XX`, or `T1`, pass through.
6. Otherwise this is the first visit from outside Iran. **Do not redirect.**
   Leave the URL alone. The existing banner can read the country from a
   cookie you set on that response, so the browser does not call a geo API:

   `Set-Cookie: abadis_geo_cc=DE; Path=/; Max-Age=86400; SameSite=Lax`

   (`DE` is whatever `CF-IPCountry` returned.) `consent.js` reads that
   cookie (or `abadis-geo-cc` in `localStorage`) and skips the browser geo
   call. It still shows the bar only once.

Set `abadis_lang` only from the visitor’s click (the page already does
this). A server must not set `abadis_lang=en` just because the IP is outside
Iran — that would hide the choice and is not a redirect, but it would also
stop the one-time suggestion.

## Liara without Cloudflare

Liara does not add a country header by itself. Put Cloudflare in front (the
steps above), or terminate TLS on nginx with `ngx_http_geoip2_module` and a
GeoLite2 Country database:

```nginx
geoip2 /usr/share/GeoIP/GeoLite2-Country.mmdb {
    auto_reload 5m;
    $geoip2_country_code country iso_code;
}
```

On `GET` of a Persian HTML page only (not `/en/` or `/arabic/`):

1. If `$http_user_agent` looks like a crawler, do nothing. Never redirect it.
2. If `$cookie_abadis_lang` is already set, do nothing.
3. If `$geoip2_country_code` is empty, `IR`, `XX`, or `T1`, do nothing.
4. Otherwise set one cookie and still return the Persian page with `200`:

   `Set-Cookie: abadis_geo_cc=DE; Path=/; Max-Age=86400; SameSite=Lax`

   (`DE` stands for whatever country code geoip2 returned.)

`consent.js` treats that cookie as the country lookup. The visitor reaches
English only from the bar or the language switcher. Both stay a click, not
a redirect.
