/* Iran province map + searchable center table.
   Z3 (2026-10-27): zoom/pan, province and city clusters, ID card, table sync.
   Dataset: cleaned workbook (1,242 hospitals + 42 surgery centers). */
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
      search: 'جستجوی نام، شهر، استان یا مالکیت',
      allProv: 'همه استان‌ها', allType: 'همه انواع', allOwn: 'همه مالکیت‌ها', allCity: 'همه شهرها',
      hospital: 'بیمارستان', surgery: 'مرکز جراحی',
      name: 'نام مرکز', city: 'شهر', prov: 'استان', type: 'نوع', own: 'مالکیت',
      empty: 'موردی یافت نشد.', map: 'نقشه ایران؛ هر نشان یک مرکز درمانی است', count: 'مرکز',
      zoomIn: 'بزرگ‌نمایی', zoomOut: 'کوچک‌نمایی', reset: 'بازنشانی نما',
      route: 'مسیریابی روی نقشه', google: 'گوگل مپ', close: 'بستن',
      unknown: 'نامشخص', legendH: 'بیمارستان', legendS: 'مرکز جراحی'
    },
    en: {
      search: 'Search name, city, province or ownership',
      allProv: 'All provinces', allType: 'All types', allOwn: 'All ownership', allCity: 'All cities',
      hospital: 'Hospital', surgery: 'Surgery center',
      hospitalStat: 'hospitals', surgeryStat: 'surgery centers',
      name: 'Center', city: 'City', prov: 'Province', type: 'Type', own: 'Ownership',
      empty: 'No match found.', map: 'Map of Iran; each mark is a center', count: 'centers',
      zoomIn: 'Zoom in', zoomOut: 'Zoom out', reset: 'Reset view',
      route: 'Directions on the map', google: 'Google Maps', close: 'Close',
      unknown: 'Unspecified', legendH: 'Hospital', legendS: 'Surgery center'
    },
    ar: {
      search: 'ابحث بالاسم أو المدينة أو المحافظة أو الملكية',
      allProv: 'كل المحافظات', allType: 'كل الأنواع', allOwn: 'كل الملكيات', allCity: 'كل المدن',
      hospital: 'مستشفى', surgery: 'مركز جراحة',
      name: 'المركز', city: 'المدينة', prov: 'المحافظة', type: 'النوع', own: 'الملكية',
      empty: 'لا توجد نتائج.', map: 'خريطة إيران؛ كل علامة مركز', count: 'مركزاً',
      zoomIn: 'تكبير', zoomOut: 'تصغير', reset: 'إعادة العرض',
      route: 'التوجيه على الخريطة', google: 'خرائط غوغل', close: 'إغلاق',
      unknown: 'غير محدد', legendH: 'مستشفى', legendS: 'مركز جراحة'
    }
  };

  function digits(n, lang) {
    var s = String(n);
    var map = lang === 'fa' ? '۰۱۲۳۴۵۶۷۸۹' : (lang === 'ar' ? '٠١٢٣٤٥٦٧٨٩' : '');
    if (!map) return s.replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    var out = '', i;
    for (i = 0; i < s.length; i++) {
      if (i && (s.length - i) % 3 === 0) out += '\u066C';
      out += map.charAt(+s.charAt(i));
    }
    return out;
  }
  function norm(s) {
    return String(s || '').replace(/[يى]/g, 'ی').replace(/ك/g, 'ک').replace(/[أإآ]/g, 'ا').replace(/[\u200c\s]+/g, ' ').trim().toLowerCase();
  }
  function esc(s) {
    return String(s || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }
  function cityLabel(c) { return c.city_fa || c.city || ''; }
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

  function mount(root) {
    var lang = root.getAttribute('data-lang') || document.documentElement.lang || 'fa';
    if (lang.indexOf('en') === 0) lang = 'en';
    else if (lang.indexOf('ar') === 0) lang = 'ar';
    else lang = 'fa';
    var T = COPY[lang] || COPY.fa;
    var src = root.getAttribute('data-src');
    var mapSrc = root.getAttribute('data-map');
    if (!src || !mapSrc) return;
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
    function project(lon, lat) {
      return { x: ax[0] * lon + ax[1] * lat + ax[2], y: ay[0] * lon + ay[1] * lat + ay[2] };
    }
    var byProv = {};
    centers.forEach(function (c) { byProv[c.province] = (byProv[c.province] || 0) + 1; });
    var paths = Object.keys(provs).map(function (name) {
      var on = byProv[name] ? ' is-on' : '';
      var n = byProv[name] || 0;
      return '<path class="ir-prov' + on + '" data-prov="' + esc(name) + '" data-n="' + n + '" d="' + provs[name].d + '"><title>' + esc(name) + ' — ' + digits(n, lang) + '</title></path>';
    }).join('');
    var lights = centers.map(function (c, i) {
      var p = project(+c.lon, +c.lat);
      var kind = c.type === 'surgery' ? 'surgery' : 'hospital';
      var mark = kind === 'surgery'
        ? '<rect class="ir-dot" x="-3.1" y="-3.1" width="6.2" height="6.2" transform="rotate(45)"/>'
        : '<circle class="ir-dot" r="3.15"/>';
      return '<g class="ir-pin ir-pin--' + kind + '" data-i="' + i + '" data-prov="' + esc(c.province) + '" data-city="' + esc(cityLabel(c)) + '" data-own="' + esc(c.ownership || '') + '" transform="translate(' + p.x.toFixed(1) + ' ' + p.y.toFixed(1) + ')">' +
        '<circle class="ir-hit" r="8"/>' + mark +
        '<title>' + esc(c.name) + '</title></g>';
    }).join('');
    var provOpts = Object.keys(byProv).sort(function (a, b) { return a.localeCompare(b, 'fa'); }).map(function (name) {
      return '<option value="' + esc(name) + '">' + esc(name) + '</option>';
    }).join('');
    var ownSeen = {};
    centers.forEach(function (c) { if (c.ownership) ownSeen[c.ownership] = 1; });
    var ownOpts = Object.keys(ownSeen).sort(function (a, b) { return a.localeCompare(b, 'fa'); }).map(function (name) {
      return '<option value="' + esc(name) + '">' + esc(name) + '</option>';
    }).join('');
    var counts = data.counts || {};
    var nHospital = counts.hospital != null ? counts.hospital : centers.filter(function (c) { return c.type === 'hospital'; }).length;
    var nSurgery = counts.surgery != null ? counts.surgery : centers.filter(function (c) { return c.type === 'surgery'; }).length;
    var nTotal = counts.total != null ? counts.total : centers.length;
    var stats = digits(nTotal, lang) + ' ' + T.count + ' · ' + digits(nHospital, lang) + ' ' + (T.hospitalStat || T.hospital) + ' · ' + digits(nSurgery, lang) + ' ' + (T.surgeryStat || T.surgery);

    root.innerHTML =
      '<div class="iran-layout">' +
        '<div class="iran-map-col">' +
          '<figure class="iran-map">' +
            '<div class="ir-zoom" role="group" aria-label="' + T.reset + '">' +
              '<button type="button" data-zoom="in" aria-label="' + T.zoomIn + '">+</button>' +
              '<button type="button" data-zoom="out" aria-label="' + T.zoomOut + '">−</button>' +
              '<button type="button" data-zoom="reset" aria-label="' + T.reset + '">' + T.reset + '</button>' +
            '</div>' +
            '<svg viewBox="0 0 ' + map.w + ' ' + map.h + '" role="img" aria-label="' + T.map + '">' +
              '<g class="ir-provs">' + paths + '</g>' +
              '<g class="ir-cities"></g>' +
              '<g class="ir-lights">' + lights + '</g>' +
            '</svg>' +
            '<article class="ir-card" data-ir-card hidden>' +
              '<button type="button" class="ir-card-x" data-ir-close aria-label="' + T.close + '">×</button>' +
              '<p class="ir-card-kicker" data-ir-kicker></p>' +
              '<h3 data-ir-name></h3>' +
              '<p class="ir-card-place" data-ir-place></p>' +
              '<p class="ir-badges"><span class="ir-badge" data-ir-type></span><span class="ir-badge ir-badge--own" data-ir-own></span></p>' +
              '<p class="ir-routes"><a data-ir-osm target="_blank" rel="noopener">' + T.route + '</a>' +
                '<a data-ir-g target="_blank" rel="noopener">' + T.google + '</a></p>' +
            '</article>' +
            '<figcaption class="ir-legend"><span><i class="ir-lg ir-lg--h"></i>' + T.legendH + '</span><span><i class="ir-lg ir-lg--s"></i>' + T.legendS + '</span></figcaption>' +
          '</figure>' +
        '</div>' +
        '<div class="iran-table-wrap">' +
          '<p class="iran-stats" data-iran-stats>' + stats + '</p>' +
          '<div class="list-tools iran-tools">' +
            '<input class="search" type="search" data-iran-q placeholder="' + T.search + '" aria-label="' + T.search + '">' +
            '<select data-iran-prov aria-label="' + T.prov + '"><option value="">' + T.allProv + '</option>' + provOpts + '</select>' +
            '<select data-iran-type aria-label="' + T.type + '"><option value="">' + T.allType + '</option>' +
              '<option value="hospital">' + T.hospital + '</option><option value="surgery">' + T.surgery + '</option></select>' +
            '<select data-iran-own aria-label="' + T.own + '"><option value="">' + T.allOwn + '</option>' + ownOpts + '</select>' +
            '<span class="count" data-iran-n aria-live="polite"></span>' +
          '</div>' +
          '<div class="ir-pills" data-iran-pills hidden></div>' +
          '<div class="iran-scroll"><table class="iran-table"><thead><tr><th>' + T.name + '</th><th>' + T.city + '</th><th>' + T.prov + '</th><th>' + T.type + '</th><th>' + T.own + '</th></tr></thead><tbody data-iran-body></tbody></table></div>' +
          '<p class="empty-msg" data-iran-empty hidden>' + T.empty + '</p>' +
        '</div></div>';

    var q = root.querySelector('[data-iran-q]');
    var prov = root.querySelector('[data-iran-prov]');
    var type = root.querySelector('[data-iran-type]');
    var own = root.querySelector('[data-iran-own]');
    var body = root.querySelector('[data-iran-body]');
    var count = root.querySelector('[data-iran-n]');
    var empty = root.querySelector('[data-iran-empty]');
    var svg = root.querySelector('svg');
    var figure = root.querySelector('.iran-map');
    var card = root.querySelector('[data-ir-card]');
    var pills = root.querySelector('[data-iran-pills]');
    var cityLayer = svg.querySelector('.ir-cities');
    var rows = centers.map(function (c, i) {
      c._i = i;
      c._p = project(+c.lon, +c.lat);
      return { c: c, n: norm([c.name, cityLabel(c), c.province, c.ownership].join(' ')) };
    });
    var city = '';
    var selected = -1;
    var cam = { x: 0, y: 0, w: map.w, h: map.h };
    var anim = 0;
    var aspect = map.h / map.w;
    var minW = 48;

    function typeLabel(t) { return t === 'surgery' ? T.surgery : T.hospital; }
    function ownLabel(v) { return v ? v : T.unknown; }

    function applyCam(c) {
      cam = c;
      svg.setAttribute('viewBox', c.x.toFixed(2) + ' ' + c.y.toFixed(2) + ' ' + c.w.toFixed(2) + ' ' + c.h.toFixed(2));
      placeCard();
    }
    function clamp(x, y, w) {
      w = Math.max(minW, Math.min(map.w, w));
      var h = w * aspect;
      if (h > map.h) { h = map.h; w = h / aspect; }
      if (x < 0) x = 0;
      if (y < 0) y = 0;
      if (x + w > map.w) x = Math.max(0, map.w - w);
      if (y + h > map.h) y = Math.max(0, map.h - h);
      return { x: x, y: y, w: w, h: h };
    }
    function setCam(x, y, w, animate) {
      var to = clamp(x, y, w);
      if (anim) cancelAnimationFrame(anim);
      if (!animate) { applyCam(to); return; }
      var from = { x: cam.x, y: cam.y, w: cam.w, h: cam.h };
      var t0 = performance.now();
      function step(now) {
        var t = Math.min(1, (now - t0) / 520);
        var e = 1 - Math.pow(1 - t, 3);
        applyCam({
          x: from.x + (to.x - from.x) * e,
          y: from.y + (to.y - from.y) * e,
          w: from.w + (to.w - from.w) * e,
          h: from.h + (to.h - from.h) * e
        });
        if (t < 1) anim = requestAnimationFrame(step);
        else anim = 0;
      }
      anim = requestAnimationFrame(step);
    }
    function zoomAt(px, py, factor) {
      var w2 = cam.w * factor;
      var nx = cam.x + px * cam.w;
      var ny = cam.y + py * cam.h;
      setCam(nx - px * w2, ny - py * w2 * aspect, w2, false);
    }
    function frameBox(box, pad) {
      var w = Math.max(box.w, 28) + pad * 2;
      var h = Math.max(box.h, 28) + pad * 2;
      var need = Math.max(w, h / aspect);
      var cx = box.x + box.w / 2;
      var cy = box.y + box.h / 2;
      setCam(cx - need / 2, cy - (need * aspect) / 2, need, true);
    }
    function frameProvince(name) {
      var path = svg.querySelector('.ir-prov[data-prov="' + CSS.escape(name) + '"]');
      if (!path) return;
      var b = path.getBBox();
      frameBox({ x: b.x, y: b.y, w: b.width, h: b.height }, 16);
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
      frameBox({ x: minX, y: minY, w: Math.max(8, maxX - minX), h: Math.max(8, maxY - minY) }, 28);
    }
    function resetView() {
      if (prov.value) frameProvince(prov.value);
      else setCam(0, 0, map.w, true);
    }

    function matchBase(c, row, skipCity) {
      if (prov.value && c.province !== prov.value) return false;
      if (!skipCity && city && cityLabel(c) !== city) return false;
      if (type.value && c.type !== type.value) return false;
      if (own.value && (c.ownership || '') !== own.value) return false;
      if (norm(q.value) && row.n.indexOf(norm(q.value)) < 0) return false;
      return true;
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
      var html = '<button type="button" data-city="" aria-pressed="' + (city ? 'false' : 'true') + '">' + T.allCity + '</button>';
      names.forEach(function (label) {
        html += '<button type="button" data-city="' + esc(label) + '" aria-pressed="' + (city === label ? 'true' : 'false') + '">' +
          esc(label) + ' <b>' + digits(bag[label], lang) + '</b></button>';
      });
      pills.innerHTML = html;
      pills.hidden = names.length === 0;
      var badges = names.slice(0, 14).map(function (label) {
        var p = pts[label];
        var x = p.x / p.n;
        var y = p.y / p.n;
        var text = label + ' ' + digits(bag[label], lang);
        var w = Math.max(46, text.length * 7.2 + 16);
        return '<g class="ir-city' + (city === label ? ' is-on' : '') + '" data-city="' + esc(label) + '" transform="translate(' + x.toFixed(1) + ' ' + y.toFixed(1) + ')">' +
          '<rect x="' + (-w / 2).toFixed(1) + '" y="-11" width="' + w.toFixed(1) + '" height="22" rx="11"/>' +
          '<text text-anchor="middle" y="4">' + esc(text) + '</text></g>';
      }).join('');
      cityLayer.innerHTML = badges;
    }

    function paint() {
      var html = '';
      var n = 0;
      var lit = {};
      for (var i = 0; i < rows.length; i++) {
        var c = rows[i].c;
        var typeOk = !type.value || c.type === type.value;
        var ownOk = !own.value || (c.ownership || '') === own.value;
        var queryOk = !norm(q.value) || rows[i].n.indexOf(norm(q.value)) >= 0;
        if (typeOk && ownOk && queryOk) lit[c.province] = (lit[c.province] || 0) + 1;
        if (!matchBase(c, rows[i], false)) continue;
        n++;
        html += '<tr data-i="' + i + '"' + (i === selected ? ' class="is-on"' : '') + ' tabindex="0"><td>' + esc(c.name) + '</td><td>' + esc(cityLabel(c)) + '</td><td>' + esc(c.province) + '</td><td>' + typeLabel(c.type) + '</td><td>' + esc(ownLabel(c.ownership)) + '</td></tr>';
      }
      body.innerHTML = html;
      count.textContent = digits(n, lang) + ' ' + T.count;
      empty.hidden = n > 0;
      svg.querySelectorAll('.ir-prov').forEach(function (el) {
        var pname = el.getAttribute('data-prov');
        var provinceCount = lit[pname] || 0;
        var on = (!prov.value || pname === prov.value) && provinceCount > 0;
        el.classList.toggle('is-dim', !on);
        el.classList.toggle('is-hot', !!prov.value && pname === prov.value);
        var title = el.querySelector('title');
        if (title) title.textContent = pname + ' — ' + digits(provinceCount, lang);
      });
      svg.querySelectorAll('.ir-pin').forEach(function (el) {
        var i = +el.getAttribute('data-i');
        var on = matchBase(centers[i], rows[i], false);
        el.classList.toggle('is-dim', !on);
        el.classList.toggle('is-on', i === selected);
      });
      paintCities();
      placeCard();
    }

    function placeCard() {
      if (card.hidden || selected < 0) return;
      var p = centers[selected]._p;
      var svgRect = svg.getBoundingClientRect();
      var figRect = figure.getBoundingClientRect();
      var vx = (p.x - cam.x) / cam.w;
      var vy = (p.y - cam.y) / cam.h;
      var left = vx * svgRect.width + (svgRect.left - figRect.left);
      var top = vy * svgRect.height + (svgRect.top - figRect.top);
      var cardW = Math.min(280, figRect.width - 16);
      var x = Math.max(8, Math.min(left + 12, figRect.width - cardW - 8));
      var y = Math.max(8, Math.min(top - 12, figRect.height - 168));
      card.style.left = x + 'px';
      card.style.top = y + 'px';
      card.style.maxWidth = cardW + 'px';
    }

    function fillCard(i) {
      var c = centers[i];
      var lat = (+c.lat).toFixed(5);
      var lon = (+c.lon).toFixed(5);
      card.hidden = false;
      card.querySelector('[data-ir-kicker]').textContent = c.province + ' · ' + cityLabel(c);
      card.querySelector('[data-ir-name]').textContent = c.name;
      card.querySelector('[data-ir-place]').textContent = T.prov + ' ' + c.province + ' · ' + T.city + ' ' + cityLabel(c);
      card.querySelector('[data-ir-type]').textContent = typeLabel(c.type);
      card.querySelector('[data-ir-own]').textContent = ownLabel(c.ownership);
      var osm = card.querySelector('[data-ir-osm]');
      osm.href = 'https://www.openstreetmap.org/directions?to=' + lat + '%2C' + lon;
      card.querySelector('[data-ir-g]').href = 'https://www.google.com/maps/search/?api=1&query=' + lat + '%2C' + lon;
      placeCard();
    }

    function scrollRow(i) {
      var row = body.querySelector('tr[data-i="' + i + '"]');
      if (!row) return;
      var scroller = root.querySelector('.iran-scroll');
      var delta = row.getBoundingClientRect().top - scroller.getBoundingClientRect().top;
      scroller.scrollTop += delta - 42;
    }

    function focusIndex(i, fromRow) {
      var c = centers[i];
      if (!fromRow) {
        if (norm(q.value) && rows[i].n.indexOf(norm(q.value)) < 0) q.value = '';
        if (type.value && c.type !== type.value) type.value = '';
        if (own.value && (c.ownership || '') !== own.value) own.value = '';
        if (prov.value !== c.province) prov.value = c.province;
        city = cityLabel(c);
      }
      selected = i;
      paint();
      fillCard(i);
      scrollRow(i);
      if (cam.w > 240) frameIndexes([i]);
      else placeCard();
    }

    function chooseProvince(name, toggle) {
      if (toggle && prov.value === name) {
        prov.value = '';
        city = '';
        setCam(0, 0, map.w, true);
      } else {
        prov.value = name;
        city = '';
        frameProvince(name);
      }
      paint();
    }

    q.addEventListener('input', paint);
    prov.addEventListener('change', function () {
      city = '';
      if (prov.value) frameProvince(prov.value);
      else setCam(0, 0, map.w, true);
      paint();
    });
    type.addEventListener('change', paint);
    own.addEventListener('change', paint);
    pills.addEventListener('click', function (e) {
      var btn = e.target.closest('[data-city]');
      if (!btn) return;
      city = btn.getAttribute('data-city') || '';
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
      if (mode === 'reset') resetView();
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
      try { svg.setPointerCapture(e.pointerId); } catch (err) { /* capture is optional */ }
    });
    svg.addEventListener('pointermove', function (e) {
      if (!pointers[e.pointerId]) return;
      pointers[e.pointerId] = { x: e.clientX, y: e.clientY };
      var ids = Object.keys(pointers);
      if (ids.length >= 2) {
        var a = pointers[ids[0]], b = pointers[ids[1]];
        var dist = Math.hypot(a.x - b.x, a.y - b.y);
        if (!svg._pinch) svg._pinch = { dist: dist, w: cam.w };
        var factor = svg._pinch.w / Math.max(12, dist) * (svg._pinch.dist / svg._pinch.w);
        var w2 = svg._pinch.w * (svg._pinch.dist / Math.max(12, dist));
        setCam(cam.x + (cam.w - w2) / 2, cam.y + (cam.h - w2 * aspect) / 2, w2, false);
        return;
      }
      if (!drag || drag.pid !== e.pointerId) return;
      var rect = svg.getBoundingClientRect();
      var dx = e.clientX - drag.x;
      var dy = e.clientY - drag.y;
      if (Math.hypot(dx, dy) > 4) drag.moved = true;
      if (!drag.moved) return;
      var vx = dx / rect.width * cam.w;
      var vy = dy / rect.height * cam.h;
      applyCam(clamp(drag.ox - vx, drag.oy - vy, cam.w));
    });
    function endPointer(e) {
      var was = drag && drag.pid === e.pointerId ? drag : null;
      delete pointers[e.pointerId];
      if (Object.keys(pointers).length < 2) svg._pinch = null;
      if (!was) return;
      drag = null;
      if (was.moved) return;
      // setPointerCapture retargets pointerup to the svg, so use the pointerdown target.
      var origin = was.target && was.target.closest ? was.target : e.target;
      var pin = origin.closest('.ir-pin');
      if (pin) { focusIndex(+pin.getAttribute('data-i'), false); return; }
      var cityG = origin.closest('.ir-city');
      if (cityG) {
        city = cityG.getAttribute('data-city') || '';
        paint();
        var ids = [];
        rows.forEach(function (row, i) { if (matchBase(row.c, row, false)) ids.push(i); });
        frameIndexes(ids);
        return;
      }
      var path = origin.closest('.ir-prov');
      if (path) chooseProvince(path.getAttribute('data-prov'), true);
    }
    svg.addEventListener('pointerup', endPointer);
    svg.addEventListener('pointercancel', endPointer);
    svg.addEventListener('wheel', function (e) {
      e.preventDefault();
      var rect = svg.getBoundingClientRect();
      var px = (e.clientX - rect.left) / rect.width;
      var py = (e.clientY - rect.top) / rect.height;
      var factor = Math.exp(e.deltaY * 0.00115);
      zoomAt(px, py, factor);
    }, { passive: false });
    window.addEventListener('resize', placeCard);
    paint();
  }

  document.querySelectorAll('[data-iran-centers]').forEach(mount);
})();
