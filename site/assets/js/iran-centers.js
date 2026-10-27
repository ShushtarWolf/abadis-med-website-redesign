/* Iran province map + searchable center table.
   Z3 (2026-10-27): interactive Iran choropleth map, zoom/pan, collision-free province & city clusters, facility ID card, table sync.
   Dataset: cleaned workbook (1,242 hospitals + 42 surgery centers = 1,284 centers). */
(function () {
  'use strict';
  var GEO = {
    'آذربایجان شرقی': [38.08, 46.29],
    'آذربایجان غربی': [37.55, 45.08],
    'اردبیل': [38.25, 48.30],
    'اصفهان': [32.65, 51.67],
    'البرز': [35.84, 50.94],
    'ایلام': [33.64, 46.42],
    'بوشهر': [28.92, 50.82],
    'تهران': [35.69, 51.39],
    'چهارمحال و بختیاری': [32.33, 50.86],
    'خراسان جنوبی': [32.86, 59.22],
    'خراسان رضوی': [36.30, 59.61],
    'خراسان شمالی': [37.47, 57.33],
    'خوزستان': [31.32, 48.69],
    'زنجان': [36.67, 48.48],
    'سمنان': [35.57, 53.40],
    'سیستان و بلوچستان': [29.50, 60.86],
    'فارس': [29.59, 52.58],
    'قزوین': [36.27, 50.00],
    'قم': [34.64, 50.88],
    'کردستان': [35.31, 46.99],
    'کرمان': [30.28, 57.08],
    'کرمانشاه': [34.31, 47.07],
    'کهگیلویه و بویراحمد': [30.67, 51.60],
    'گلستان': [36.84, 54.43],
    'گیلان': [37.28, 49.59],
    'لرستان': [33.49, 48.36],
    'مازندران': [36.56, 53.06],
    'مرکزی': [34.09, 49.70],
    'هرمزگان': [27.18, 56.27],
    'همدان': [34.80, 48.51],
    'یزد': [31.90, 54.37]
  };

  var COPY = {
    fa: {
      search: 'جستجوی نام مرکز، شهر، استان یا مالکیت...',
      allProv: 'همه استان‌ها (۳۱ استان)',
      allType: 'همه انواع مراکز',
      allOwn: 'همه مالکیت‌ها',
      allCity: 'همه شهرهای استان',
      hospital: 'بیمارستان',
      surgery: 'مرکز جراحی',
      hospitalStat: 'بیمارستان',
      surgeryStat: 'مرکز جراحی',
      name: 'نام مرکز درمانی',
      city: 'شهر',
      prov: 'استان',
      type: 'نوع مرکز',
      own: 'مالکیت',
      empty: 'موردی با این فیلتر یافت نشد.',
      map: 'نقشه تعاملی ایران — خانواده سبز آبادیس',
      count: 'مرکز',
      zoomIn: 'بزرگ‌نمایی',
      zoomOut: 'کوچک‌نمایی',
      reset: 'کل نقشه ایران',
      route: 'مسیریابی نقشه',
      google: 'گوگل مپ',
      close: 'بستن',
      unknown: 'ثبت‌نشده',
      legendH: 'بیمارستان',
      legendS: 'مرکز جراحی',
      hint: 'روی هر استان یا نشانگر کلیک کنید',
      countryTitle: 'نقشه جامع ایران · ۳۱ استان',
      provPrefix: 'استان ',
      stage1: '۱. انتخاب استان روی نقشه ایران',
      stage2: '۲. تفکیک شهرها و مراکز استان',
      stage3: '۳. شناسنامه و مسیریابی مرکز',
      caspian: 'دریای خزر',
      persianGulf: 'خلیج فارس',
      omanSea: 'دریای عمان'
    },
    en: {
      search: 'Search facility name, city, province, or ownership...',
      allProv: 'All provinces (31)',
      allType: 'All facility types',
      allOwn: 'All ownership',
      allCity: 'All cities',
      hospital: 'Hospital',
      surgery: 'Surgery center',
      hospitalStat: 'hospitals',
      surgeryStat: 'surgery centers',
      name: 'Facility Name',
      city: 'City',
      prov: 'Province',
      type: 'Type',
      own: 'Ownership',
      empty: 'No matching centers found.',
      map: 'Interactive Map of Iran — Abadis Green Family',
      count: 'centers',
      zoomIn: 'Zoom in',
      zoomOut: 'Zoom out',
      reset: 'Full Iran Map',
      route: 'OSM Directions',
      google: 'Google Maps',
      close: 'Close',
      unknown: 'Unspecified',
      legendH: 'Hospital',
      legendS: 'Surgery center',
      hint: 'Click any province or pin to inspect',
      countryTitle: 'Full Map of Iran · 31 Provinces',
      provPrefix: 'Province: ',
      stage1: '1. Select Province on Iran Map',
      stage2: '2. Filter Cities & Centers',
      stage3: '3. Facility ID & Directions',
      caspian: 'Caspian Sea',
      persianGulf: 'Persian Gulf',
      omanSea: 'Sea of Oman'
    },
    ar: {
      search: 'ابحث بالاسم أو المدينة أو المحافظة أو الملكية...',
      allProv: 'كل المحافظات (٣١)',
      allType: 'كل الأنواع',
      allOwn: 'كل الملكيات',
      allCity: 'كل المدن',
      hospital: 'مستشفى',
      surgery: 'مركز جراحة',
      hospitalStat: 'مستشفى',
      surgeryStat: 'مركز جراحة',
      name: 'المركز العلاجي',
      city: 'المدينة',
      prov: 'المحافظة',
      type: 'النوع',
      own: 'الملكية',
      empty: 'لا توجد نتائج مطابقة.',
      map: 'خريطة إيران التفاعلية — عائلة آباديس الخضراء',
      count: 'مركزاً',
      zoomIn: 'تكبير',
      zoomOut: 'تصغير',
      reset: 'خريطة إيران الكاملة',
      route: 'مسار الخريطة',
      google: 'خرائط غوغل',
      close: 'إغلاق',
      unknown: 'غير محدد',
      legendH: 'مستشفى',
      legendS: 'مركز جراحة',
      hint: 'انقر على أي محافظة أو علامة للتفاصيل',
      countryTitle: 'خريطة إيران الكاملة · ٣١ محافظة',
      provPrefix: 'محافظة ',
      stage1: '١. اختر المحافظة على خريطة إيران',
      stage2: '٢. تصفية المدن والمراكز',
      stage3: '٣. بطاقة المركز والاتجاهات',
      caspian: 'بحر قزوين',
      persianGulf: 'الخليج الفارسي',
      omanSea: 'بحر عمان'
    }
  };

  function digits(n, lang) {
    var s = String(n == null ? 0 : n);
    var map = lang === 'fa' ? '۰۱۲۳۴۵۶۷۸۹' : (lang === 'ar' ? '٠١٢٣٤٥٦٧٨٩' : '');
    if (!map) return s.replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    var out = '', i;
    for (i = 0; i < s.length; i++) {
      if (i && (s.length - i) % 3 === 0) out += '\u066C';
      var ch = s.charAt(i);
      out += (ch >= '0' && ch <= '9') ? map.charAt(+ch) : ch;
    }
    return out;
  }

  function norm(s) {
    return String(s || '')
      .replace(/[يى]/g, 'ی')
      .replace(/ك/g, 'ک')
      .replace(/[أإآ]/g, 'ا')
      .replace(/[\u200c\s]+/g, ' ')
      .trim()
      .toLowerCase();
  }

  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function getName(c) { return c.name || c.n || ''; }
  function getProv(c) { return c.province || c.p || ''; }
  function cityLabel(c) { return c.city_fa || c.city || c.c || ''; }
  function getKind(c) { return (c.type === 'surgery' || c.t === 's') ? 'surgery' : 'hospital'; }
  function getOwn(c) {
    var o = c.ownership != null ? c.ownership : (c.o || '');
    if (!o || o === 'نامشخص') return '';
    return String(o).replace(/\s*;\s*/g, ' · ');
  }
  function getLon(c) { return +(c.lon != null ? c.lon : c.lo); }
  function getLat(c) { return +(c.lat != null ? c.lat : c.la); }

  function solve3(A, b) {
    var m = [A[0].concat(b[0]), A[1].concat(b[1]), A[2].concat(b[2])];
    var i, j, k, f;
    for (i = 0; i < 3; i++) {
      var piv = i;
      for (j = i + 1; j < 3; j++) if (Math.abs(m[j][i]) > Math.abs(m[piv][i])) piv = j;
      var tmp = m[i]; m[i] = m[piv]; m[piv] = tmp;
      f = m[i][i] || 1e-9;
      for (k = i; k < 4; k++) m[i][k] /= f;
      for (j = 0; j < 3; j++) if (j !== i) {
        f = m[j][i];
        for (k = i; k < 4; k++) m[j][k] -= f * m[i][k];
      }
    }
    return [m[0][3], m[1][3], m[2][3]];
  }

  function fit(pairs, axis) {
    var s = [[0, 0, 0], [0, 0, 0], [0, 0, 0]];
    var t = [0, 0, 0];
    pairs.forEach(function (p) {
      var row = [p.lon, p.lat, 1];
      var y = axis === 'x' ? p.x : p.y;
      for (var i = 0; i < 3; i++) {
        t[i] += row[i] * y;
        for (var j = 0; j < 3; j++) s[i][j] += row[i] * row[j];
      }
    });
    return solve3(s, t);
  }

  function boxesOverlap(a, b, pad) {
    var p = pad || 0;
    return !(
      a.x + a.w + p < b.x ||
      b.x + b.w + p < a.x ||
      a.y + a.h + p < b.y ||
      b.y + b.h + p < a.y
    );
  }

  function mount(root) {
    var lang = root.getAttribute('data-lang') || document.documentElement.lang || 'fa';
    if (lang.indexOf('en') === 0) lang = 'en';
    else if (lang.indexOf('ar') === 0) lang = 'ar';
    else lang = 'fa';
    var T = COPY[lang] || COPY.fa;
    var src = root.getAttribute('data-src') || '../assets/data/iran-hospitals-centers.json';
    var mapSrc = root.getAttribute('data-map') || '../assets/data/iran-provinces.json';
    Promise.all([
      fetch(src).then(function (r) { if (!r.ok) throw new Error('centers'); return r.json(); }),
      fetch(mapSrc).then(function (r) { if (!r.ok) throw new Error('map'); return r.json(); })
    ]).then(function (pair) {
      render(root, T, lang, pair[0], pair[1]);
    }).catch(function () {
      root.insertAdjacentHTML('beforeend', '<p class="iran-empty">' + T.empty + '</p>');
    });
  }

  function render(root, T, lang, data, map) {
    var centers = data.centers || [];
    var provs = map.p || {};
    var pairs = [];
    Object.keys(provs).forEach(function (name) {
      var g = GEO[name];
      var c = provs[name].c;
      if (!g || !c) return;
      pairs.push({ lon: g[1], lat: g[0], x: c[0], y: c[1] });
    });
    var ax = fit(pairs, 'x');
    var ay = fit(pairs, 'y');

    function project(lon, lat, provName, idx) {
      var pObj = provs[provName];
      var pc = (pObj && pObj.c) ? pObj.c : [400, 350];
      if (!isFinite(lon) || !isFinite(lat) || lat < 24 || lat > 40.5 || lon < 43.5 || lon > 64) {
        var ang = ((idx * 137.5) % 360) * (Math.PI / 180);
        var rad = 6 + (idx % 14);
        return { x: pc[0] + Math.cos(ang) * rad, y: pc[1] + Math.sin(ang) * rad };
      }
      var x = ax[0] * lon + ax[1] * lat + ax[2];
      var y = ay[0] * lon + ay[1] * lat + ay[2];
      var dx = x - pc[0], dy = y - pc[1];
      if (dx * dx + dy * dy > 145 * 145) {
        x = pc[0] + dx * 0.28;
        y = pc[1] + dy * 0.28;
      }
      x = Math.max(24, Math.min((map.w || 800) - 24, x));
      y = Math.max(22, Math.min((map.h || 702) - 22, y));
      return { x: x, y: y };
    }

    var byProv = {};
    var ownCounts = {};
    centers.forEach(function (c, i) {
      var pName = getProv(c);
      byProv[pName] = (byProv[pName] || 0) + 1;
      var oName = getOwn(c);
      if (oName) ownCounts[oName] = (ownCounts[oName] || 0) + 1;
      c._i = i;
      c._p = project(getLon(c), getLat(c), pName, i);
    });

    var paths = Object.keys(provs).map(function (name) {
      var n = byProv[name] || 0;
      var tier = n >= 80 ? '4' : (n >= 40 ? '3' : (n >= 20 ? '2' : '1'));
      return '<path class="ir-prov tier-' + tier + '" data-prov="' + esc(name) + '" data-tier="' + tier + '" data-n="' + n + '" d="' + provs[name].d + '">' +
        '<title>' + esc(name) + ' — ' + digits(n, lang) + ' ' + T.count + '</title></path>';
    }).join('');

    var textDir = (lang === 'fa' || lang === 'ar')
      ? ' direction="rtl" style="direction:rtl;unicode-bidi:normal;letter-spacing:0"'
      : ' style="letter-spacing:0"';
    // Non-overlapping province count badges for full-country overview (top 10 hubs, generous spacing)
    var provOrder = Object.keys(byProv).sort(function (a, b) { return byProv[b] - byProv[a]; });
    var placedProvBoxes = [];
    var provBadgesHtml = provOrder.slice(0, 8).map(function (name) {
      var pObj = provs[name];
      if (!pObj || !pObj.c) return '';
      var n = byProv[name] || 0;
      var cx = pObj.c[0], cy = pObj.c[1];
      var label = name + ' (' + digits(n, lang) + ')';
      var bw = Math.max(48, Math.min(96, label.length * 4.5 + 12));
      var bh = 16;
      var box = { x: cx - bw / 2, y: cy - bh / 2, w: bw, h: bh };
      if (placedProvBoxes.some(function (pb) { return boxesOverlap(box, pb, 16); })) return '';
      placedProvBoxes.push(box);
      return '<g class="ir-prov-badge" data-prov="' + esc(name) + '" transform="translate(' + cx.toFixed(1) + ' ' + cy.toFixed(1) + ')">' +
        '<rect x="' + (-bw / 2).toFixed(1) + '" y="' + (-bh / 2).toFixed(1) + '" width="' + bw.toFixed(1) + '" height="' + bh + '" rx="8"/>' +
        '<text text-anchor="middle" y="3.2"' + textDir + '>' + esc(label) + '</text></g>';
    }).join('');

    var lights = centers.map(function (c, i) {
      var p = c._p;
      var kind = getKind(c);
      var phase = ((i * 0.19) % 3.2).toFixed(2);
      var mark = kind === 'surgery'
        ? '<rect class="ir-dot" x="-2.2" y="-2.2" width="4.4" height="4.4" transform="rotate(45)"/>'
        : '<circle class="ir-dot" r="2.2"/>';
      return '<g class="ir-pin ir-pin--' + kind + '" data-i="' + i + '" data-prov="' + esc(getProv(c)) + '" data-city="' + esc(cityLabel(c)) + '" data-own="' + esc(getOwn(c)) + '" style="--pulse-d:-' + phase + 's" transform="translate(' + p.x.toFixed(1) + ' ' + p.y.toFixed(1) + ')">' +
        '<g class="ir-bulb"><circle class="ir-glow" r="4.8"/>' + mark + '</g>' +
        '<circle class="ir-hit" r="7"/>' +
        '<title>' + esc(getName(c)) + ' (' + esc(getProv(c)) + ' · ' + esc(cityLabel(c)) + ')</title></g>';
    }).join('');

    var provOpts = provOrder.map(function (name) {
      return '<option value="' + esc(name) + '">' + esc(name) + ' (' + digits(byProv[name], lang) + ')</option>';
    }).join('');

    var ownOpts = Object.keys(ownCounts).sort(function (a, b) { return ownCounts[b] - ownCounts[a]; }).map(function (name) {
      return '<option value="' + esc(name) + '">' + esc(name) + ' (' + digits(ownCounts[name], lang) + ')</option>';
    }).join('');

    var counts = data.counts || {};
    var nHospital = counts.hospital != null ? counts.hospital : (data.hospitals || centers.filter(function (c) { return getKind(c) === 'hospital'; }).length);
    var nSurgery = counts.surgery != null ? counts.surgery : (data.surgeryCenters || centers.filter(function (c) { return getKind(c) === 'surgery'; }).length);
    var nTotal = counts.total != null ? counts.total : centers.length;
    var stats = digits(nTotal, lang) + ' ' + T.count + ' · ' + digits(nHospital, lang) + ' ' + (T.hospitalStat || T.hospital) + ' · ' + digits(nSurgery, lang) + ' ' + (T.surgeryStat || T.surgery);

    var seaLabels =
      '<g class="ir-sea-layer" aria-hidden="true">' +
        '<text class="ir-sea-label" x="418" y="92" text-anchor="middle"' + textDir + '>' + esc(T.caspian) + '</text>' +
        '<text class="ir-sea-label" x="255" y="628" text-anchor="middle"' + textDir + '>' + esc(T.persianGulf) + '</text>' +
        '<text class="ir-sea-label" x="555" y="688" text-anchor="middle"' + textDir + '>' + esc(T.omanSea) + '</text>' +
      '</g>';

    root.innerHTML =
      '<div class="ir-stage-bar" data-ir-stages>' +
        '<div class="ir-stage is-active" data-stage="1"><span class="ir-stage-dot"></span><span>' + esc(T.stage1) + '</span></div>' +
        '<span class="ir-stage-sep" aria-hidden="true">←</span>' +
        '<div class="ir-stage" data-stage="2"><span class="ir-stage-dot"></span><span>' + esc(T.stage2) + '</span></div>' +
        '<span class="ir-stage-sep" aria-hidden="true">←</span>' +
        '<div class="ir-stage" data-stage="3"><span class="ir-stage-dot"></span><span>' + esc(T.stage3) + '</span></div>' +
      '</div>' +
      '<div class="iran-layout">' +
        '<div class="iran-map-col">' +
          '<figure class="iran-map">' +
            '<div class="ir-map-topbar">' +
              '<span class="ir-region-pill" data-ir-region>' + esc(T.countryTitle) + ' · ' + digits(nTotal, lang) + ' ' + esc(T.count) + '</span>' +
              '<div class="ir-zoom" role="group" aria-label="' + esc(T.reset) + '">' +
                '<button type="button" data-zoom="in" title="' + esc(T.zoomIn) + '" aria-label="' + esc(T.zoomIn) + '">+</button>' +
                '<button type="button" data-zoom="out" title="' + esc(T.zoomOut) + '" aria-label="' + esc(T.zoomOut) + '">−</button>' +
                '<button type="button" class="ir-zoom-reset" data-zoom="reset" title="' + esc(T.reset) + '" aria-label="' + esc(T.reset) + '">' + esc(T.reset) + ' ⟲</button>' +
              '</div>' +
            '</div>' +
            '<div class="ir-svg-wrap">' +
              '<svg viewBox="-28 -24 ' + (map.w + 56) + ' ' + (map.h + 48) + '" role="img" aria-label="' + esc(T.map) + '">' +
                seaLabels +
                '<g class="ir-provs">' + paths + '</g>' +
                '<g class="ir-lights">' + lights + '</g>' +
                '<g class="ir-prov-badges">' + provBadgesHtml + '</g>' +
                '<g class="ir-cities"></g>' +
              '</svg>' +
              '<article class="ir-card" data-ir-card hidden>' +
                '<button type="button" class="ir-card-x" data-ir-close aria-label="' + esc(T.close) + '">×</button>' +
                '<p class="ir-card-kicker" data-ir-kicker></p>' +
                '<h3 data-ir-name></h3>' +
                '<p class="ir-card-place" data-ir-place></p>' +
                '<p class="ir-badges"><span class="ir-badge" data-ir-type></span><span class="ir-badge ir-badge--own" data-ir-own></span></p>' +
                '<p class="ir-routes">' +
                  '<a class="ir-route-btn ir-route-btn--primary" data-ir-g target="_blank" rel="noopener">' + esc(T.google) + '</a>' +
                  '<a class="ir-route-btn" data-ir-osm target="_blank" rel="noopener">' + esc(T.route) + '</a>' +
                '</p>' +
              '</article>' +
            '</div>' +
            '<figcaption class="ir-legend">' +
              '<span><i class="ir-lg ir-lg--h"></i>' + esc(T.legendH) + ' (' + digits(nHospital, lang) + ')</span>' +
              '<span><i class="ir-lg ir-lg--s"></i>' + esc(T.legendS) + ' (' + digits(nSurgery, lang) + ')</span>' +
              '<span class="ir-legend-hint">' + esc(T.hint) + '</span>' +
            '</figcaption>' +
          '</figure>' +
        '</div>' +
        '<div class="iran-table-wrap">' +
          '<div class="iran-tools">' +
            '<div class="iran-tools-row1">' +
              '<input class="search" type="search" data-iran-q placeholder="' + esc(T.search) + '" aria-label="' + esc(T.search) + '">' +
              '<span class="count" data-iran-n aria-live="polite">' + stats + '</span>' +
            '</div>' +
            '<div class="iran-tools-row2">' +
              '<select data-iran-prov aria-label="' + esc(T.prov) + '"><option value="">' + esc(T.allProv) + '</option>' + provOpts + '</select>' +
              '<select data-iran-type aria-label="' + esc(T.type) + '"><option value="">' + esc(T.allType) + '</option>' +
                '<option value="hospital">' + esc(T.hospital) + ' (' + digits(nHospital, lang) + ')</option>' +
                '<option value="surgery">' + esc(T.surgery) + ' (' + digits(nSurgery, lang) + ')</option></select>' +
              '<select data-iran-own aria-label="' + esc(T.own) + '"><option value="">' + esc(T.allOwn) + '</option>' + ownOpts + '</select>' +
            '</div>' +
          '</div>' +
          '<div class="ir-pills" data-iran-pills hidden></div>' +
          '<div class="iran-scroll"><table class="iran-table"><thead><tr><th>' + esc(T.name) + '</th><th>' + esc(T.city) + '</th><th>' + esc(T.prov) + '</th><th>' + esc(T.type) + '</th><th>' + esc(T.own) + '</th></tr></thead><tbody data-iran-body></tbody></table></div>' +
          '<p class="empty-msg" data-iran-empty hidden>' + esc(T.empty) + '</p>' +
        '</div>' +
      '</div>';

    var q = root.querySelector('[data-iran-q]');
    var prov = root.querySelector('[data-iran-prov]');
    var type = root.querySelector('[data-iran-type]');
    var own = root.querySelector('[data-iran-own]');
    var body = root.querySelector('[data-iran-body]');
    var count = root.querySelector('[data-iran-n]');
    var empty = root.querySelector('[data-iran-empty]');
    var svg = root.querySelector('svg');
    var card = root.querySelector('[data-ir-card]');
    var pills = root.querySelector('[data-iran-pills]');
    var cityLayer = svg.querySelector('.ir-cities');
    var provBadgeGroup = svg.querySelector('.ir-prov-badges');
    var regionPill = root.querySelector('[data-ir-region]');
    var stagesWrap = root.querySelector('[data-ir-stages]');

    var rows = centers.map(function (c) {
      return { c: c, n: norm([getName(c), cityLabel(c), getProv(c), getOwn(c)].join(' ')) };
    }).sort(function (a, b) {
      var oa = getOwn(a.c) ? 0 : 1;
      var ob = getOwn(b.c) ? 0 : 1;
      if (oa !== ob) return oa - ob;
      return getName(a.c).localeCompare(getName(b.c), 'fa');
    });
    var city = '';
    var selected = -1;
    var fullX = -28, fullY = -24, fullW = map.w + 56, fullH = map.h + 48;
    var cam = { x: fullX, y: fullY, w: fullW, h: fullH };
    var anim = 0;
    var aspect = fullH / fullW;
    // Keep minimum zoom window >= 165 so surrounding Iranian provinces remain visible
    var minW = 165;

    function typeLabel(t) { return t === 'surgery' ? T.surgery : T.hospital; }
    function ownLabel(v) { return v ? v : T.unknown; }

    function updateVisualScale() {
      var zScale = cam.w / fullW;
      svg.style.setProperty('--ir-z', zScale.toFixed(4));
      var isCountryView = !prov.value && zScale > 0.72;
      if (provBadgeGroup) {
        if (isCountryView) provBadgeGroup.removeAttribute('display');
        else provBadgeGroup.setAttribute('display', 'none');
      }
    }

    function setView(c) {
      cam = c;
      svg.setAttribute('viewBox', c.x.toFixed(2) + ' ' + c.y.toFixed(2) + ' ' + c.w.toFixed(2) + ' ' + c.h.toFixed(2));
    }

    function applyCam(c) {
      setView(c);
      updateVisualScale();
      paintCities();
    }

    function clampCam(x, y, w) {
      w = Math.max(minW, Math.min(fullW, w));
      var h = w * aspect;
      if (h > fullH) { h = fullH; w = h / aspect; }
      if (x < fullX) x = fullX;
      if (y < fullY) y = fullY;
      if (x + w > fullX + fullW) x = Math.max(fullX, fullX + fullW - w);
      if (y + h > fullY + fullH) y = Math.max(fullY, fullY + fullH - h);
      return { x: x, y: y, w: w, h: h };
    }

    function setCam(x, y, w, animate) {
      var to = clampCam(x, y, w);
      if (anim) cancelAnimationFrame(anim);
      if (!animate) { applyCam(to); return; }
      var from = { x: cam.x, y: cam.y, w: cam.w, h: cam.h };
      var t0 = performance.now();
      function step(now) {
        var t = Math.min(1, (now - t0) / 380);
        var e = 1 - Math.pow(1 - t, 3);
        var frame = {
          x: from.x + (to.x - from.x) * e,
          y: from.y + (to.y - from.y) * e,
          w: from.w + (to.w - from.w) * e,
          h: from.h + (to.h - from.h) * e
        };
        if (t < 1) {
          setView(frame);
          anim = requestAnimationFrame(step);
        } else {
          applyCam(to);
          anim = 0;
        }
      }
      anim = requestAnimationFrame(step);
    }

    function zoomAt(px, py, factor) {
      var w2 = cam.w * factor;
      var nx = cam.x + px * cam.w;
      var ny = cam.y + py * cam.h;
      setCam(nx - px * w2, ny - py * w2 * aspect, w2, false);
    }

    function frameBox(box, pad, minWidthOverride) {
      var floorW = minWidthOverride || 220;
      var w = Math.max(box.w + pad * 2, floorW);
      var h = Math.max(box.h + pad * 2, floorW * aspect);
      var need = Math.max(w, h / aspect);
      var cx = box.x + box.w / 2;
      var cy = box.y + box.h / 2;
      setCam(cx - need / 2, cy - (need * aspect) / 2, need, true);
    }

    function boxFromPath(path) {
      var b = null;
      try { b = path.getBBox(); } catch (err) { b = null; }
      if (b && b.width > 1 && b.height > 1) return { x: b.x, y: b.y, w: b.width, h: b.height };
      var d = path.getAttribute('d') || '';
      var nums = d.match(/-?\d*\.?\d+/g);
      if (nums && nums.length >= 4) {
        var minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
        for (var i = 0; i + 1 < nums.length; i += 2) {
          var x = +nums[i], y = +nums[i + 1];
          if (x < minX) minX = x;
          if (y < minY) minY = y;
          if (x > maxX) maxX = x;
          if (y > maxY) maxY = y;
        }
        if (isFinite(minX) && maxX > minX && maxY > minY) {
          return { x: minX, y: minY, w: maxX - minX, h: maxY - minY };
        }
      }
      var c = provs[path.getAttribute('data-prov')];
      if (c && c.c) return { x: c.c[0] - 36, y: c.c[1] - 36, w: 72, h: 72 };
      return { x: fullX, y: fullY, w: fullW, h: fullH };
    }

    function frameProvince(name) {
      drag = null;
      pointers = {};
      var path = svg.querySelector('.ir-prov[data-prov="' + CSS.escape(name) + '"]');
      if (!path) return;
      var b = boxFromPath(path);
      frameBox(b, Math.max(b.w, b.h) * 0.28 + 18, 175);
    }

    function frameIndexes(list) {
      if (!list.length) return;
      var minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
      list.forEach(function (i) {
        var p = centers[i]._p;
        if (p.x < minX) minX = p.x;
        if (p.y < minY) minY = p.y;
        if (p.x > maxX) maxX = p.x;
        if (p.y > maxY) maxY = p.y;
      });
      frameBox({ x: minX, y: minY, w: Math.max(12, maxX - minX), h: Math.max(12, maxY - minY) }, 42, 185);
    }

    function resetAllToCountry() {
      prov.value = '';
      city = '';
      selected = -1;
      card.hidden = true;
      setCam(fullX, fullY, fullW, true);
      paint();
    }

    function matchBase(c, row, skipCity) {
      if (prov.value && getProv(c) !== prov.value) return false;
      if (!skipCity && city && cityLabel(c) !== city) return false;
      if (type.value && getKind(c) !== type.value) return false;
      if (own.value && getOwn(c) !== own.value) return false;
      if (norm(q.value) && row.n.indexOf(norm(q.value)) < 0) return false;
      return true;
    }

    function updateStageIndicator() {
      if (!stagesWrap) return;
      var activeStage = selected >= 0 ? 3 : (prov.value ? 2 : 1);
      Array.prototype.forEach.call(stagesWrap.querySelectorAll('.ir-stage'), function (stEl) {
        var stNum = +stEl.getAttribute('data-stage');
        stEl.classList.toggle('is-active', stNum === activeStage);
        stEl.classList.toggle('is-done', stNum < activeStage);
      });
    }

    function paintCities() {
      var name = prov.value;
      if (!name) {
        pills.hidden = true;
        pills.innerHTML = '';
        cityLayer.innerHTML = '';
        return;
      }
      var bag = {};
      var pts = {};
      rows.forEach(function (row) {
        var c = row.c;
        if (!matchBase(c, row, true)) return;
        var label = cityLabel(c) || '—';
        bag[label] = (bag[label] || 0) + 1;
        if (!pts[label]) pts[label] = { x: 0, y: 0, n: 0 };
        pts[label].x += c._p.x;
        pts[label].y += c._p.y;
        pts[label].n += 1;
      });
      var names = Object.keys(bag).sort(function (a, b) { return bag[b] - bag[a] || a.localeCompare(b, 'fa'); });
      var totalInProv = Object.keys(bag).reduce(function (acc, k) { return acc + bag[k]; }, 0);
      var html = '<button type="button" data-city="" aria-pressed="' + (city ? 'false' : 'true') + '">' +
        esc(T.allCity) + ' <b>' + digits(totalInProv, lang) + '</b></button>';
      names.forEach(function (label) {
        html += '<button type="button" data-city="' + esc(label) + '" aria-pressed="' + (city === label ? 'true' : 'false') + '">' +
          esc(label) + ' <b>' + digits(bag[label], lang) + '</b></button>';
      });
      pills.innerHTML = html;
      pills.hidden = names.length === 0;

      // Scale city badges by current camera zoom factor and enforce strict 2D bounding-box non-overlap
      var zScale = cam.w / fullW;
      var placedBoxes = [];
      var badges = [];
      for (var idx = 0; idx < names.length && badges.length < 9; idx++) {
        var label = names[idx];
        var p = pts[label];
        var x = p.x / p.n;
        var y = p.y / p.n;
        var text = label + ' · ' + digits(bag[label], lang);
        var bw = Math.max(46, Math.min(96, text.length * 4.8 + 14)) * zScale;
        var bh = 17.5 * zScale;
        var yOff = -9 * zScale;
        var candidate = { x: x - bw / 2, y: y + yOff - bh / 2, w: bw, h: bh };
        if (placedBoxes.some(function (pb) { return boxesOverlap(candidate, pb, 4.5 * zScale); })) {
          continue;
        }
        placedBoxes.push(candidate);
        var rx = (8.5 * zScale).toFixed(2);
        var fSize = Math.max(2.6, 9.2 * zScale).toFixed(2);
        var sWidth = Math.max(0.35, 1.1 * zScale).toFixed(2);
        badges.push(
          '<g class="ir-city' + (city === label ? ' is-on' : '') + '" data-city="' + esc(label) + '" transform="translate(' + x.toFixed(1) + ' ' + (y + yOff).toFixed(1) + ')">' +
            '<rect x="' + (-bw / 2).toFixed(2) + '" y="' + (-bh / 2).toFixed(2) + '" width="' + bw.toFixed(2) + '" height="' + bh.toFixed(2) + '" rx="' + rx + '" style="stroke-width:' + sWidth + 'px"/>' +
            '<text text-anchor="middle" y="' + (3.2 * zScale).toFixed(2) + '" style="font-size:' + fSize + 'px;letter-spacing:0;' + (lang === 'fa' || lang === 'ar' ? 'direction:rtl;unicode-bidi:normal;' : '') + '"' + (lang === 'fa' || lang === 'ar' ? ' direction="rtl"' : '') + '>' + esc(text) + '</text>' +
          '</g>'
        );
      }
      cityLayer.innerHTML = badges.join('');
    }

    function paint() {
      var html = '';
      var n = 0;
      var lit = {};
      for (var i = 0; i < rows.length; i++) {
        var c = rows[i].c;
        var typeOk = !type.value || getKind(c) === type.value;
        var ownOk = !own.value || getOwn(c) === own.value;
        var queryOk = !norm(q.value) || rows[i].n.indexOf(norm(q.value)) >= 0;
        if (typeOk && ownOk && queryOk) lit[getProv(c)] = (lit[getProv(c)] || 0) + 1;
        if (!matchBase(c, rows[i], false)) continue;
        n++;
        var oText = ownLabel(getOwn(c));
        var kType = getKind(c);
        html += '<tr data-i="' + i + '"' + (i === selected ? ' class="is-on"' : '') + ' tabindex="0">' +
          '<td><strong>' + esc(getName(c)) + '</strong></td>' +
          '<td>' + esc(cityLabel(c)) + '</td>' +
          '<td>' + esc(getProv(c)) + '</td>' +
          '<td><span class="ir-tbl-badge ir-tbl-badge--' + kType + '">' + esc(typeLabel(kType)) + '</span></td>' +
          '<td><span class="ir-tbl-own' + (getOwn(c) ? '' : ' is-muted') + '">' + esc(oText) + '</span></td>' +
        '</tr>';
      }
      body.innerHTML = html;
      count.textContent = digits(n, lang) + ' ' + T.count;
      empty.hidden = n > 0;

      if (regionPill) {
        if (prov.value) {
          regionPill.textContent = T.provPrefix + prov.value + (city ? ' · ' + city : '') + ' · ' + digits(n, lang) + ' ' + T.count;
        } else {
          regionPill.textContent = T.countryTitle + ' · ' + digits(n, lang) + ' ' + T.count;
        }
      }

      svg.querySelectorAll('.ir-prov').forEach(function (el) {
        var pname = el.getAttribute('data-prov');
        var provinceCount = lit[pname] || 0;
        var isSelectedProv = !!prov.value && pname === prov.value;
        var isOtherWhenSelected = !!prov.value && pname !== prov.value;
        el.classList.toggle('is-hot', isSelectedProv);
        el.classList.toggle('is-dim', isOtherWhenSelected || (!prov.value && provinceCount === 0));
        var title = el.querySelector('title');
        if (title) title.textContent = pname + ' — ' + digits(provinceCount, lang) + ' ' + T.count;
      });

      svg.querySelectorAll('.ir-pin').forEach(function (el) {
        var i = +el.getAttribute('data-i');
        var on = matchBase(centers[i], rows[i], false);
        el.classList.toggle('is-dim', !on);
        el.classList.toggle('is-on', i === selected);
      });

      updateVisualScale();
      paintCities();
      updateStageIndicator();
    }

    function fillCard(i) {
      var c = centers[i];
      var lat = getLat(c).toFixed(5);
      var lon = getLon(c).toFixed(5);
      card.hidden = false;
      card.querySelector('[data-ir-kicker]').textContent = getProv(c) + ' · ' + cityLabel(c);
      card.querySelector('[data-ir-name]').textContent = getName(c);
      card.querySelector('[data-ir-place]').textContent = T.prov + ': ' + getProv(c) + ' · ' + T.city + ': ' + cityLabel(c);
      card.querySelector('[data-ir-type]').textContent = typeLabel(getKind(c));
      card.querySelector('[data-ir-own]').textContent = T.own + ': ' + ownLabel(getOwn(c));
      var osm = card.querySelector('[data-ir-osm]');
      osm.href = c.osm || ('https://www.openstreetmap.org/directions?to=' + lat + '%2C' + lon);
      card.querySelector('[data-ir-g]').href = 'https://www.google.com/maps/search/?api=1&query=' + lat + '%2C' + lon;
    }

    function scrollRow(i) {
      var row = body.querySelector('tr[data-i="' + i + '"]');
      if (!row) return;
      var scroller = root.querySelector('.iran-scroll');
      var delta = row.getBoundingClientRect().top - scroller.getBoundingClientRect().top;
      scroller.scrollTop += delta - 48;
    }

    function focusIndex(i, fromRow) {
      var c = centers[i];
      if (!fromRow) {
        if (norm(q.value) && rows[i].n.indexOf(norm(q.value)) < 0) q.value = '';
        if (type.value && getKind(c) !== type.value) type.value = '';
        if (own.value && getOwn(c) !== own.value) own.value = '';
        if (prov.value !== getProv(c)) prov.value = getProv(c);
        city = cityLabel(c);
      }
      selected = i;
      paint();
      fillCard(i);
      scrollRow(i);
      if (cam.w > 260) frameIndexes([i]);
    }

    function chooseProvince(name, toggle) {
      selected = -1;
      card.hidden = true;
      if (toggle && prov.value === name) {
        prov.value = '';
        city = '';
        setCam(fullX, fullY, fullW, true);
      } else {
        prov.value = name;
        city = '';
        frameProvince(name);
      }
      paint();
    }

    q.addEventListener('input', function () {
      selected = -1;
      card.hidden = true;
      paint();
    });
    prov.addEventListener('change', function () {
      city = '';
      selected = -1;
      card.hidden = true;
      if (prov.value) frameProvince(prov.value);
      else setCam(fullX, fullY, fullW, true);
      paint();
    });
    type.addEventListener('change', function () {
      selected = -1;
      card.hidden = true;
      paint();
    });
    own.addEventListener('change', function () {
      selected = -1;
      card.hidden = true;
      paint();
    });
    pills.addEventListener('click', function (e) {
      var btn = e.target.closest('[data-city]');
      if (!btn) return;
      city = btn.getAttribute('data-city') || '';
      selected = -1;
      card.hidden = true;
      paint();
      if (city) {
        var ids = [];
        rows.forEach(function (row, i) { if (matchBase(row.c, row, false)) ids.push(i); });
        frameIndexes(ids);
      } else if (prov.value) frameProvince(prov.value);
    });
    body.addEventListener('click', function (e) {
      var tr = e.target.closest('tr[data-i]');
      if (!tr) return;
      focusIndex(+tr.getAttribute('data-i'), true);
    });
    body.addEventListener('keydown', function (e) {
      if (e.key !== 'Enter' && e.key !== ' ') return;
      var tr = e.target.closest('tr[data-i]');
      if (!tr) return;
      e.preventDefault();
      focusIndex(+tr.getAttribute('data-i'), true);
    });
    card.querySelector('[data-ir-close]').addEventListener('click', function () {
      card.hidden = true;
      selected = -1;
      paint();
    });
    root.querySelector('.ir-zoom').addEventListener('click', function (e) {
      var btn = e.target.closest('[data-zoom]');
      if (!btn) return;
      var mode = btn.getAttribute('data-zoom');
      if (mode === 'reset') resetAllToCountry();
      else zoomAt(0.5, 0.5, mode === 'in' ? 0.78 : 1.28);
    });

    var drag = null;
    var pointers = {};
    svg.addEventListener('pointerdown', function (e) {
      if (e.button !== undefined && e.button !== 0) return;
      pointers[e.pointerId] = { x: e.clientX, y: e.clientY };
      var ids = Object.keys(pointers);
      if (ids.length === 1) {
        drag = { x: e.clientX, y: e.clientY, ox: cam.x, oy: cam.y, moved: false, pid: e.pointerId, target: e.target };
        if (anim) cancelAnimationFrame(anim);
      }
    });
    svg.addEventListener('pointermove', function (e) {
      if (!pointers[e.pointerId]) return;
      pointers[e.pointerId] = { x: e.clientX, y: e.clientY };
      var ids = Object.keys(pointers);
      if (ids.length >= 2) {
        var a = pointers[ids[0]], b = pointers[ids[1]];
        var dist = Math.hypot(a.x - b.x, a.y - b.y);
        if (!svg._pinch) svg._pinch = { dist: dist, w: cam.w };
        var w2 = svg._pinch.w * (svg._pinch.dist / Math.max(12, dist));
        setView(clampCam(cam.x + (cam.w - w2) / 2, cam.y + (cam.h - w2 * aspect) / 2, w2));
        svg._pinch.moved = true;
        return;
      }
      if (!drag || drag.pid !== e.pointerId) return;
      var rect = svg.getBoundingClientRect();
      var dx = e.clientX - drag.x;
      var dy = e.clientY - drag.y;
      if (!drag.moved && Math.hypot(dx, dy) > 9) {
        drag.moved = true;
        try { svg.setPointerCapture(e.pointerId); } catch (err) { /* capture is optional */ }
      }
      if (!drag.moved) return;
      var vx = dx / rect.width * cam.w;
      var vy = dy / rect.height * cam.h;
      setView(clampCam(drag.ox - vx, drag.oy - vy, cam.w));
    });
    function endPointer(e) {
      var was = drag && drag.pid === e.pointerId ? drag : null;
      var pinchMoved = !!(svg._pinch && svg._pinch.moved);
      delete pointers[e.pointerId];
      if (Object.keys(pointers).length < 2) svg._pinch = null;
      if (pinchMoved && Object.keys(pointers).length < 2) {
        updateVisualScale();
        paintCities();
      }
      if (!was) return;
      drag = null;
      if (was.moved) {
        updateVisualScale();
        paintCities();
        return;
      }
      var origin = was.target && was.target.closest ? was.target : e.target;
      var pin = origin.closest('.ir-pin');
      if (pin) { focusIndex(+pin.getAttribute('data-i'), false); return; }
      var provBadge = origin.closest('.ir-prov-badge');
      if (provBadge) {
        chooseProvince(provBadge.getAttribute('data-prov'), false);
        return;
      }
      var cityG = origin.closest('.ir-city');
      if (cityG) {
        var clickedCity = cityG.getAttribute('data-city') || '';
        city = (city === clickedCity) ? '' : clickedCity;
        selected = -1;
        card.hidden = true;
        paint();
        if (city) {
          var ids = [];
          rows.forEach(function (row, i) { if (matchBase(row.c, row, false)) ids.push(i); });
          frameIndexes(ids);
        } else if (prov.value) {
          frameProvince(prov.value);
        }
        return;
      }
      var path = origin.closest('.ir-prov');
      if (path) chooseProvince(path.getAttribute('data-prov'), true);
    }
    svg.addEventListener('pointerup', endPointer);
    svg.addEventListener('pointercancel', endPointer);
    svg.addEventListener('wheel', function (e) {
      if (!e.ctrlKey && !e.metaKey && Math.abs(e.deltaY) < 4) return;
      e.preventDefault();
      var rect = svg.getBoundingClientRect();
      var px = (e.clientX - rect.left) / rect.width;
      var py = (e.clientY - rect.top) / rect.height;
      var factor = Math.exp(e.deltaY * 0.00115);
      zoomAt(px, py, factor);
    }, { passive: false });

    svg.addEventListener('pointerover', function (e) {
      if (prov.value || !regionPill) return;
      var pEl = e.target.closest('.ir-prov, .ir-prov-badge');
      if (!pEl) return;
      var pname = pEl.getAttribute('data-prov');
      if (pname && byProv[pname] != null) {
        regionPill.textContent = T.provPrefix + pname + ' · ' + digits(byProv[pname], lang) + ' ' + T.count;
      }
    });
    svg.addEventListener('pointerleave', function () {
      if (!prov.value && regionPill) {
        regionPill.textContent = T.countryTitle + ' · ' + digits(centers.length, lang) + ' ' + T.count;
      }
    });
    paint();
  }

  document.querySelectorAll('[data-iran-centers]').forEach(mount);
})();
