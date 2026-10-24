/* Export quote request form (static site): validates, builds a mailto: to the sales inbox,
   and reports form_submit to dataLayer via window.abadisTrack (site.js). */
(function () {
  document.querySelectorAll('form[data-quote-form]').forEach(function (f) {
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!f.reportValidity()) return;
      var to = f.dataset.to, subj = f.dataset.subject, lines = [];
      f.querySelectorAll('[name]').forEach(function (el) {
        if (el.type === 'checkbox' && !el.checked) return;
        var lab = f.querySelector('label[for="' + el.id + '"]');
        if (el.value) lines.push((lab ? lab.textContent.replace('*', '').trim() : el.name) + ': ' + el.value);
      });
      var co = (f.querySelector('[name=company]') || {}).value || '';
      var href = 'mailto:' + to + '?subject=' + encodeURIComponent(subj + (co ? ' — ' + co : '')) + '&body=' + encodeURIComponent(lines.join('\n'));
      if (window.abadisTrack) window.abadisTrack('form_submit', { form: 'export_quote', lang: document.documentElement.lang });
      var ok = f.querySelector('.qf-done'); if (ok) ok.hidden = false;
      location.href = href;
    });
  });
})();
