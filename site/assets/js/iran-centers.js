/* Iran province map + searchable center table.
   Default dataset is the cleaned workbook (1,242 hospitals + 42 surgery centers). */
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
      allProv: 'همه استان‌ها',
      allType: 'همه انواع',
      allOwn: 'همه مالکیت‌ها',
      hospital: 'بیمارستان',
      surgery: 'مرکز جراحی',
      name: 'نام مرکز',
      city: 'شهر',
      prov: 'استان',
      type: 'نوع',
      own: 'مالکیت',
      empty: 'موردی یافت نشد.',
      map: 'نقشه ایران؛ هر چراغ یک مرکز درمانی است',
      count: 'مرکز'
    },
    en: {
      search: 'Search name, city, province or ownership',
      allProv: 'All provinces',
      allType: 'All types',
      allOwn: 'All ownership',
      hospital: 'Hospital',
      surgery: 'Surgery center',
      hospitalStat: 'hospitals',
      surgeryStat: 'surgery centers',
      name: 'Center',
      city: 'City',
      prov: 'Province',
      type: 'Type',
      own: 'Ownership',
      empty: 'No match found.',
      map: 'Map of Iran; each light is a center',
      count: 'centers'
    },
    ar: {
      search: 'ابحث بالاسم أو المدينة أو المحافظة أو الملكية',
      allProv: 'كل المحافظات',
      allType: 'كل الأنواع',
      allOwn: 'كل الملكيات',
      hospital: 'مستشفى',
      surgery: 'مركز جراحة',
      name: 'المركز',
      city: 'المدينة',
      prov: 'المحافظة',
      type: 'النوع',
      own: 'الملكية',
      empty: 'لا توجد نتائج.',
      map: 'خريطة إيران؛ كل ضوء مركز',
      count: 'مركزاً'
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
    return String(s || '')
      .replace(/[يى]/g, 'ی').replace(/ك/g, 'ک').replace(/[أإآ]/g, 'ا')
      .replace(/[\u200c\s]+/g, ' ').trim().toLowerCase();
  }

  function esc(s) {
    return String(s || '')
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  function cityLabel(c) {
    return c.city_fa || c.city || '';
  }

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
      var p = project(c.lon, c.lat);
      var delay = (i % 18) * 0.12;
      return '<circle class="ir-led ir-led--' + c.type + '" data-prov="' + esc(c.province) + '" data-own="' + esc(c.ownership || '') + '" cx="' + p.x.toFixed(1) + '" cy="' + p.y.toFixed(1) + '" r="2.4" style="animation-delay:' + delay.toFixed(2) + 's"><title>' + esc(c.name) + '</title></circle>';
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
        '<figure class="iran-map"><svg viewBox="0 0 ' + map.w + ' ' + map.h + '" role="img" aria-label="' + T.map + '">' +
          '<g class="ir-provs">' + paths + '</g><g class="ir-lights">' + lights + '</g></svg></figure>' +
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
    var rows = centers.map(function (c) {
      return { c: c, n: norm([c.name, c.city, c.city_fa, c.province, c.ownership].join(' ')) };
    });
    function typeLabel(t) { return t === 'surgery' ? T.surgery : T.hospital; }
    function ownLabel(v) { return v ? v : '—'; }
    function paint() {
      var query = norm(q.value);
      var pv = prov.value;
      var tp = type.value;
      var ow = own.value;
      var html = '';
      var n = 0;
      var lit = {};
      for (var i = 0; i < rows.length; i++) {
        var c = rows[i].c;
        var typeOk = !tp || c.type === tp;
        var ownOk = !ow || (c.ownership || '') === ow;
        if (typeOk && ownOk) lit[c.province] = (lit[c.province] || 0) + 1;
        if (pv && c.province !== pv) continue;
        if (!typeOk || !ownOk) continue;
        if (query && rows[i].n.indexOf(query) < 0) continue;
        n++;
        if (n <= 80) {
          html += '<tr><td>' + esc(c.name) + '</td><td>' + esc(cityLabel(c)) + '</td><td>' + esc(c.province) + '</td><td>' + typeLabel(c.type) + '</td><td>' + esc(ownLabel(c.ownership)) + '</td></tr>';
        }
      }
      body.innerHTML = html;
      var shown = digits(n, lang);
      count.textContent = shown + ' ' + T.count;
      empty.hidden = n > 0;
      svg.querySelectorAll('.ir-prov').forEach(function (el) {
        var name = el.getAttribute('data-prov');
        var provinceCount = lit[name] || 0;
        var on = (!pv || name === pv) && provinceCount > 0;
        el.classList.toggle('is-dim', !on);
        var title = el.querySelector('title');
        if (title) title.textContent = name + ' — ' + digits(provinceCount, lang);
      });
      svg.querySelectorAll('.ir-led').forEach(function (el) {
        var on = !pv || el.getAttribute('data-prov') === pv;
        if (tp) on = on && el.classList.contains('ir-led--' + tp);
        if (ow) on = on && el.getAttribute('data-own') === ow;
        el.classList.toggle('is-dim', !on);
      });
    }
    q.addEventListener('input', paint);
    prov.addEventListener('change', paint);
    type.addEventListener('change', paint);
    own.addEventListener('change', paint);
    svg.addEventListener('click', function (e) {
      var path = e.target.closest('.ir-prov');
      if (!path) return;
      var name = path.getAttribute('data-prov');
      prov.value = prov.value === name ? '' : name;
      paint();
    });
    paint();
  }

  document.querySelectorAll('[data-iran-centers]').forEach(mount);
})();
