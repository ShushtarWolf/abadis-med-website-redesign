#!/usr/bin/env bash
set -u
base='https://abadis-med.com'
mkdir -p audit-raw
curl -L --max-time 30 -A 'Abadis-Audit/1.0' -sS "$base/sitemap_index.xml" -o audit-raw/sitemap_index.xml || true
for sm in post-sitemap.xml page-sitemap.xml jet-menu-sitemap.xml _joboffers-sitemap.xml _downloadcenter-sitemap.xml _customers-sitemap.xml _franchise-sitemap.xml category-sitemap.xml post_tag-sitemap.xml _citynmg-sitemap.xml author-sitemap.xml; do
  curl -L --max-time 45 -A 'Abadis-Audit/1.0' -sS "$base/$sm" -o "audit-raw/$sm" || true
done
printf 'Sitemap byte sizes and URL counts\n'
for f in audit-raw/*sitemap.xml; do
  printf '%8s %6s %s\n' "$(wc -c < "$f")" "$(grep -o '<loc>' "$f" | wc -l)" "$f"
done
printf '\nRepresentative page status/title/meta\n'
for u in / /en/ /arabic/ /%d9%85%d8%ad%d8%a7%d8%b3%d8%a8%d9%87-%da%af%d8%b1/ /%d9%85%d8%ad%d8%b5%d9%88%d9%84%d8%a7%d8%aa/%d8%a7%d8%aa%d8%b5%d8%a7%d9%84%d8%a7%d8%aa/ /%d8%af%d8%b1%d8%a8%d8%a7%d8%b1%d9%87-%d9%85%d8%a7/; do
  out="audit-raw/page-$(echo "$u" | tr '/%' '__').html"
  curl -L --max-time 30 -A 'Abadis-Audit/1.0' -sS "$base$u" -o "$out" || true
  printf '\nURL %s\n' "$base$u"
  grep -oiE '<title>[^<]+' "$out" | head -1 || true
  grep -oiE '<meta[^>]+(name="description"|property="og:title"|rel="canonical")[^>]*>' "$out" | head -8 || true
done
