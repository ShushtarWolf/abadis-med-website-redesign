/* Cookie consent + optional English suggestion. One include on every page.
   Analytics (dataLayer / abadis:track in site.js) stays silent until consent is "accepted".
   The language bar is a suggestion only: it never changes location by itself. */
(function () {
  var CONSENT_KEY = 'abadis-consent';
  var LANG_KEY = 'abadis-lang-suggest';
  var GEO_KEY = 'abadis-geo-cc';
  var COOKIE = 'abadis_lang';
  var YEAR = 60 * 60 * 24 * 365;

  var COPY = {
    fa: {
      text: 'کوکی‌ها فقط برای آمار بازدید به کار می‌روند.',
      accept: 'پذیرفتن همه',
      reject: 'رد کردن',
      label: 'رضایت کوکی'
    },
    en: {
      text: 'Cookies are only used to measure visits.',
      accept: 'Accept all',
      reject: 'Reject',
      label: 'Cookie consent'
    },
    ar: {
      text: 'تُستخدم ملفات تعريف الارتباط لقياس الزيارات فقط.',
      accept: 'قبول الكل',
      reject: 'رفض',
      label: 'الموافقة على ملفات الارتباط'
    }
  };

  function read(key) {
    try { return localStorage.getItem(key); } catch (e) { return null; }
  }
  function write(key, value) {
    try { localStorage.setItem(key, value); } catch (e) {}
  }
  function consent() {
    var v = read(CONSENT_KEY);
    return (v === 'accepted' || v === 'rejected') ? v : '';
  }
  window.abadisConsent = consent;

  function uiLang() {
    var l = (document.documentElement.getAttribute('lang') || '').toLowerCase();
    if (l.indexOf('ar') === 0) return 'ar';
    if (l.indexOf('en') === 0) return 'en';
    return 'fa';
  }

  function setCookie(value) {
    try {
      document.cookie = COOKIE + '=' + value + '; Path=/; Max-Age=' + YEAR + '; SameSite=Lax';
    } catch (e) {}
  }

  function stack() {
    var cookie = document.querySelector('.consent-bar');
    var geo = document.querySelector('.lang-suggest');
    if (!geo) return;
    if (cookie) geo.style.bottom = cookie.offsetHeight + 'px';
    else geo.style.bottom = '0px';
  }

  function button(className, label) {
    var b = document.createElement('button');
    b.type = 'button';
    b.className = className;
    b.textContent = label;
    b.setAttribute('aria-label', label);
    return b;
  }

  function showConsent() {
    if (consent() || document.querySelector('.consent-bar')) return;
    var c = COPY[uiLang()];
    var bar = document.createElement('div');
    bar.className = 'consent-bar';
    bar.setAttribute('role', 'region');
    bar.setAttribute('aria-label', c.label);
    var p = document.createElement('p');
    p.textContent = c.text;
    var actions = document.createElement('div');
    actions.className = 'consent-actions';
    var accept = button('consent-accept', c.accept);
    var reject = button('consent-reject', c.reject);
    accept.addEventListener('click', function () {
      write(CONSENT_KEY, 'accepted');
      bar.remove();
      stack();
    });
    reject.addEventListener('click', function () {
      write(CONSENT_KEY, 'rejected');
      bar.remove();
      stack();
    });
    actions.appendChild(accept);
    actions.appendChild(reject);
    bar.appendChild(p);
    bar.appendChild(actions);
    document.body.appendChild(bar);
    stack();
  }

  function isCrawler() {
    var ua = navigator.userAgent || '';
    return /bot|crawler|spider|slurp|facebookexternalhit|embedly|quora|pinterestbot|slackbot|telegrambot|discordbot|linkedinbot|twitterbot|applebot|semrush|ahrefs|mj12bot|dotbot|petalbot|bytespider|gptbot|claudebot|amazonbot|lighthouse|headless|wget\/|curl\//i.test(ua);
  }

  function isPersianPage() {
    var l = (document.documentElement.getAttribute('lang') || '').toLowerCase();
    if (l.indexOf('fa') !== 0) return false;
    var path = location.pathname || '';
    if (/\/en(\/|$)/.test(path) || /\/arabic(\/|$)/.test(path)) return false;
    return true;
  }

  function englishHref() {
    var a = document.querySelector('nav.lang-switch a.lang-link[hreflang="en"]');
    if (!a) return '';
    var href = a.getAttribute('href') || '';
    if (!href || href.charAt(0) === '#') return '';
    return href;
  }

  function showSuggest(href) {
    if (read(LANG_KEY) || document.querySelector('.lang-suggest')) return;
    /* One-time: remember that this browser has been offered English. */
    write(LANG_KEY, 'seen');
    var bar = document.createElement('div');
    bar.className = 'lang-suggest';
    bar.setAttribute('role', 'region');
    bar.setAttribute('lang', 'en');
    bar.setAttribute('dir', 'ltr');
    bar.setAttribute('aria-label', 'Language suggestion');
    var p = document.createElement('p');
    p.textContent = 'View this site in English?';
    var actions = document.createElement('div');
    actions.className = 'lang-suggest-actions';
    var go = document.createElement('a');
    go.className = 'lang-suggest-go';
    go.href = href;
    go.setAttribute('hreflang', 'en');
    go.setAttribute('lang', 'en');
    go.setAttribute('data-track', 'language_switch');
    go.textContent = 'English';
    go.setAttribute('aria-label', 'English');
    go.addEventListener('click', function () {
      write(LANG_KEY, 'en');
      setCookie('en');
    });
    var stay = button('lang-suggest-stay', 'Stay in Persian');
    stay.addEventListener('click', function () {
      write(LANG_KEY, 'fa');
      setCookie('fa');
      bar.remove();
      stack();
    });
    actions.appendChild(go);
    actions.appendChild(stay);
    bar.appendChild(p);
    bar.appendChild(actions);
    /* Cookie bar is below this one; keep it later in the tab order. */
    var cookie = document.querySelector('.consent-bar');
    if (cookie) document.body.insertBefore(bar, cookie);
    else document.body.appendChild(bar);
    stack();
  }

  function withTimeout(url, ms) {
    if (typeof fetch !== 'function') return Promise.reject(new Error('nofetch'));
    var ctrl = (typeof AbortController === 'function') ? new AbortController() : null;
    var timer = setTimeout(function () { if (ctrl) ctrl.abort(); }, ms);
    var opts = { credentials: 'omit', cache: 'no-store' };
    if (ctrl) opts.signal = ctrl.signal;
    return fetch(url, opts).finally(function () { clearTimeout(timer); });
  }

  function countryFromTrace(text) {
    var m = /(?:^|\n)loc=([A-Za-z]{2})\b/.exec(text || '');
    return m ? m[1].toUpperCase() : '';
  }

  function cookieValue(name) {
    var parts = ('; ' + (document.cookie || '')).split('; ' + name + '=');
    if (parts.length < 2) return '';
    return decodeURIComponent(parts.pop().split(';').shift() || '');
  }

  function lookupCountry() {
    var fromCookie = (cookieValue('abadis_geo_cc') || '').toUpperCase();
    if (/^[A-Z]{2}$/.test(fromCookie)) {
      write(GEO_KEY, fromCookie);
      return Promise.resolve(fromCookie);
    }
    var cached = read(GEO_KEY);
    if (cached && /^[A-Z]{2}$/.test(cached)) return Promise.resolve(cached);
    try {
      if (sessionStorage.getItem('abadis-geo-fail') === '1') return Promise.reject(new Error('skip'));
    } catch (e) {}
    return withTimeout(location.origin + '/cdn-cgi/trace', 1500).then(function (r) {
      if (!r.ok) throw new Error('trace');
      return r.text();
    }).then(function (text) {
      var cc = countryFromTrace(text);
      if (!/^[A-Z]{2}$/.test(cc)) throw new Error('loc');
      return cc;
    }).catch(function () {
      return withTimeout('https://api.country.is/', 2500).then(function (r) {
        if (!r.ok) throw new Error('country');
        return r.json();
      }).then(function (data) {
        var cc = data && data.country ? String(data.country).toUpperCase() : '';
        if (!/^[A-Z]{2}$/.test(cc)) throw new Error('cc');
        return cc;
      });
    }).then(function (cc) {
      write(GEO_KEY, cc);
      return cc;
    }).catch(function (err) {
      try { sessionStorage.setItem('abadis-geo-fail', '1'); } catch (e) {}
      throw err;
    });
  }

  function bootSuggest() {
    if (isCrawler() || !isPersianPage()) return;
    if (read(LANG_KEY)) return;
    var href = englishHref();
    if (!href) return;
    var pending;
    try { pending = lookupCountry(); } catch (e) { return; }
    pending.then(function (cc) {
      if (cc && cc !== 'IR') showSuggest(href);
    }).catch(function () { /* silent: no banner, no redirect */ });
  }

  function boot() {
    showConsent();
    bootSuggest();
    window.addEventListener('resize', stack, { passive: true });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
