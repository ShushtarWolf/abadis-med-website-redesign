/**
 * Abadis contact/careers form relay.
 * Env secrets: INBOX_TO, RESEND_API_KEY, optional INBOX_FROM.
 * Public POST only — no API keys in the static site.
 */
const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Accept, Content-Type',
};

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json', ...CORS },
  });
}

export default {
  async fetch(request, env) {
    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: CORS });
    }
    if (request.method !== 'POST') {
      return json({ ok: false, error: 'method_not_allowed' }, 405);
    }

    let fields = {};
    const ctype = request.headers.get('content-type') || '';
    try {
      if (ctype.includes('multipart/form-data') || ctype.includes('application/x-www-form-urlencoded')) {
        const fd = await request.formData();
        for (const [k, v] of fd.entries()) {
          if (typeof v === 'string') {
            if (fields[k] === undefined) fields[k] = v;
            else fields[k] = [].concat(fields[k], v);
          } else {
            fields[k] = `[file: ${v.name || 'upload'}]`;
          }
        }
      } else {
        fields = await request.json();
      }
    } catch {
      return json({ ok: false, error: 'bad_body' }, 400);
    }

    // honeypot
    if ((fields._gotcha || '').toString().trim()) {
      return json({ ok: true });
    }

    const to = env.INBOX_TO;
    const key = env.RESEND_API_KEY;
    if (!to || !key) {
      return json({ ok: false, error: 'server_not_configured' }, 500);
    }

    const formName = fields.form_name || 'form';
    const lines = Object.entries(fields)
      .filter(([k]) => k !== '_gotcha')
      .map(([k, v]) => `${k}: ${Array.isArray(v) ? v.join(', ') : v}`);
    const text = lines.join('\n');
    const from = env.INBOX_FROM || 'Abadis Forms <onboarding@resend.dev>';

    const res = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${key}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        from,
        to: [to],
        subject: `[Abadis] ${formName}`,
        text,
      }),
    });

    if (!res.ok) {
      const detail = await res.text();
      return json({ ok: false, error: 'email_failed', detail: detail.slice(0, 200) }, 502);
    }
    return json({ ok: true });
  },
};
