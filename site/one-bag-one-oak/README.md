# یک کیسه، یک بلوط — One Bag, One Oak

A quiet, no-timer browser game. Each clean suction-bag swap plants an oak on the Zagros view from `site/zagros-names/`. Static files only; GitHub Pages publishes the whole `site/` folder from `main` (see `.github/workflows/pages.yml`).

**URL (after merge to `main`):** https://shushtarwolf.github.io/abadis-med-website-redesign/one-bag-one-oak/

Local preview from the repo root:

```bash
python3 -m http.server 8080 --directory site
```

Open http://localhost:8080/one-bag-one-oak/

## Edit text

`i18n.json` holds FA (default, RTL), EN, and AR (RTL). Keys are shared. The page reads `?lang=fa|en|ar` and remembers the choice in `localStorage["abadis-oak-lang"]`.

## Edit numbers

`savings.json` is the only place savings live.

- `formula` is copied from `site/dial-practical/common/abadis-common.js` (`F.surgery`): water `1.6 * 9.3` litres, cost `2.5 * 85000` toman, staff hours `1.7 / 60 * 2.2 * 7.1`. The game multiplies those factors per completed swap and rounds totals the way the calculator does (`Math.round`).
- `chemicals.amount` is `null` and `chemicals.showCounter` is `false`. The calculator folds wash and disinfectant into the toman figure and does not publish a bottle count. The chemicals pill stays hidden until `showCounter` is true and `amount` is a real figure. Unlabeled bottles in the old-way vignette are a picture only.
- `gameRules` (bag-size cycle, bins, seed prices, night shift, when the view greens) is pacing, not a hospital statistic. One night-shift oak uses the same per-surgery formula. The night shift plants at most one oak per `msPerTree` and never counts more than `capHours` (8) away.

## Edit links

`savings.json` → `links.calculator` and `links.zagros`.

## Embed

```html
<iframe
  title="یک کیسه، یک بلوط"
  src="https://shushtarwolf.github.io/abadis-med-website-redesign/one-bag-one-oak/"
  style="width:100%;height:100dvh;border:0"
  allow="clipboard-write"
></iframe>
```

Give the frame a real height. Vibration inside an iframe depends on the parent’s permissions policy.

## Progress

`localStorage["abadis-oak-v1"]`. Theme uses the site key `abadis-theme` (`light` / `dark` / `noir`, or `?theme=`).

## Analytics

`window.abadisOakTrack(name, detail)` emits `game_start`, `swap`, `milestone`, `cta_calculator_click`, `cta_zagros_click`, and `share`. It also dispatches a `abadis-oak` event. If `window.abadisAnalytics` exists, it is called with the same name and detail.
