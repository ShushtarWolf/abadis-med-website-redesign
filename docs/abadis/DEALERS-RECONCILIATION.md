# Dealers & customers reconciliation

- **Date:** 2026-10-07
- **Branch:** `siamak/redesign`
- **Sources:** WP REST `http://abadis-med.com/wp-json/wp/v2/_franchise` (26) + `_citynmg` (31) + live page `/لیست-نمایندگان/`; customers `_customers` (155) vs `pages.json` `/مشتریان-ما/`

## Summary

| Metric | Pre-fix site | Live listing | WP CPT | New site |
|--------|---------------|--------------|--------|----------|
| Dealer cards | 24 | 28 (+ duplicate قزوین heading noise) | 26 records | **29** |
| Provinces with dealers | 22 | 25 | 25 city links (+ کردستان empty) | **26** |
| Customers | 155 | — | 155 | **155** |

**Customers:** site, Wayback `pages.json`, and REST all agree at **155**. The earlier “157 vs 155” mismatch is gone (no duplicates in either source). No customer change required.

## Why 24 → 29 cards

1. Wayback `/لیست-نمایندگان/` snapshot used by the old generator was missing newer live rows (پردیس طب تجهیز, قم, کهگیلویه و بویراحمد, چهارمحال و بختیاری, …).
2. CPT has **26** `_franchise` rows; multi-province companies (e.g. شرکت نیک طب → اردبیل/زنجان/گیلان) expand to one card per province on the listing.
3. **کردستان / تجهیز گستر آبیدر** (CPT `15342`) is published and tagged `_citynmg=کردستان` but has **empty** JetEngine contact fields and does **not** appear on the public listing page. Added as a name-only card so all 26 CPT rows are represented.
4. **چهارمحال و بختیاری** appears on the live listing (مخازن طبی آبادیس) but has **no** dedicated CPT `_citynmg` link — kept because it is on the live page (verbatim).

## CPT ↔ site decisions

| id | slug | Title (REST) | Cities | On live listing? | Decision |
|----|------|--------------|--------|------------------|----------|
| 19081 | مخازن-طبی-آبادیس-4 | مخازن طبی آبادیس | کهگیلویه و بویراحمد | yes | keep from live |
| 18986 | مخازن-طبی-آبادیس-3 | مخازن طبی آبادیس | قم | yes | keep from live |
| 18905 | پردیس-طب-تجهیز | پردیس طب تجهیز | اصفهان | yes | **was missing on Wayback site — added** |
| 18070 | نیک-طب | نیک طب | آذربایجان غربی | yes | keep |
| 16656 | جهان-درمان-2 | جهان درمان | سیستان و بلوچستان | yes | keep (same company, second province) |
| 15418 | مخازن-طبی-آبادیس-2 | مخازن طبی آبادیس | البرز | yes | keep |
| 15417 | مخازن-طبی-آبادیس | مخازن طبی آبادیس | تهران | yes | keep |
| 15342 | تجهیز-گستر-آبیدر | تجهیز گستر آبیدر | کردستان | **no** (empty fields) | **added name-only** |
| 15338 | مداوا-گستر-پاسارگاد | مخازن طبی آبادیس | کرمانشاه | yes (title مخازن…) | keep live title |
| 15332 | شرکت-نیک-طب-2 | شرکت نیک طب | آذربایجان شرقی | yes | keep |
| 15324 | شرکت-نیک-طب-3 | شرکت نیک طب | قزوین | yes | keep |
| 15276 | دانش-نو-اندیشان-بهپود | دانش نو اندیشان بهپود | هرمزگان | yes | keep |
| 15261 | شرکت-نیک-طب | شرکت نیک طب | اردبیل، زنجان، گیلان | yes (×3) | expand under each province |
| 15250 | شرکت-حکیمان-فرجاد-قومس | مخازن طبی آبادیس | سمنان | yes (title مخازن…) | keep live title |
| 14248 | رادمان-تجهیز-آژمان | رادمان تجهیز آژمان | خوزستان | yes | keep |
| 13836 | تجهیزات-پزشکی-پاکان-طبیب-آرمان | … | مرکزی | yes | keep |
| 13835 | کالای-پزشکی-بوشهر-درمان | … | بوشهر | yes | keep |
| 13834 | پویا-طب-معجزه | پویا طب معجزه | تهران | yes | keep |
| 13833 | هگمتان-طب | هگمتان طب | همدان | yes | keep |
| 13831 | کاراطب | کاراطب | اصفهان | yes | keep |
| 13830 | جام-جم | جام جم | اصفهان | yes | keep |
| 13829 | جهان-درمان | جهان درمان | کرمان | yes | keep |
| 13828 | بهسان-تجهیز-آبادیس | بهسان تجهیز آبادیس | یزد | yes | keep |
| 13822 | کیمیا-گران-طب-سلامت-2 | مخازن طبی آبادیس | خراسان رضوی | yes | keep live title |
| 13819 | کران-مبتکران-طبرستان | کران مبتکر طبرستان | مازندران | yes | keep |
| 13818 | دانش-نواندیشان-بهپود | دانش نواندیشان بهپود | فارس | yes | keep |

## Implementation

- Data: `tools/redesign/data/dealers.json` (live scrape + کردستان CPT gap), `franchise_raw.json`
- Generator: `pages_company.dealers()` reads `dealers.json`; legend counts derived from data; phones use `tel:`
- Rebuild: `python3 tools/redesign/build.py dealers customers`

## Open

- کردستان contact rows (مدیر عامل / تلفن / آدرس) are empty in WP public API and single page — fill when Abadis supplies them; do not invent.
- چهارمحال listing has no CPT city link — confirm with Abadis whether it should stay.
