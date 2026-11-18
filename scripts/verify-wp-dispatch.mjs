#!/usr/bin/env node
/**
 * Verify a repository_dispatch client_payload signed by wordpress/mu-plugins/abadis-publish-dispatch.php.
 * Reads the event from GITHUB_EVENT_PATH. Exits 1 when the secret is missing or the signature does not match.
 * Does not print the secret.
 */
import crypto from 'node:crypto';
import { readFileSync } from 'node:fs';

const MAX_AGE_SEC = 30 * 60;

export function canonicalPayload(payload) {
  return [payload.action, payload.post_id, payload.status, payload.lang, payload.ts].join('\n');
}

export function signPayload(payload, secret) {
  return crypto.createHmac('sha256', secret).update(canonicalPayload(payload)).digest('hex');
}

export function verifyPayload(payload, secret, nowSec = Math.floor(Date.now() / 1000)) {
  if (!secret) return 'ABADIS_WP_WEBHOOK_SECRET is not set';
  const sig = String(payload?.sig || '');
  const expect = signPayload(payload || {}, secret);
  const a = Buffer.from(sig);
  const b = Buffer.from(expect);
  if (a.length !== b.length || !crypto.timingSafeEqual(a, b)) return 'webhook signature mismatch';
  const ts = Number(payload.ts);
  if (!Number.isFinite(ts) || Math.abs(nowSec - ts) > MAX_AGE_SEC) return 'webhook timestamp is outside 30 minutes';
  return '';
}

function selfTest() {
  const payload = { action: 'publish', post_id: 12, status: 'publish', lang: 'fa', ts: 1_700_000_000 };
  const secret = 'test-secret';
  payload.sig = signPayload(payload, secret);
  if (verifyPayload(payload, secret, payload.ts)) throw new Error('verify self-test: valid payload rejected');
  if (!verifyPayload({ ...payload, sig: '00' }, secret, payload.ts)) throw new Error('verify self-test: bad sig accepted');
  if (!verifyPayload(payload, '', payload.ts)) throw new Error('verify self-test: empty secret accepted');
  console.log('verify self-test ok');
}

if (process.argv.includes('--self-test')) {
  selfTest();
} else if (process.argv[1] && process.argv[1].endsWith('verify-wp-dispatch.mjs') && !process.argv.includes('--lib')) {
  const eventPath = process.env.GITHUB_EVENT_PATH;
  if (!eventPath) {
    console.error('GITHUB_EVENT_PATH is not set');
    process.exit(1);
  }
  const event = JSON.parse(readFileSync(eventPath, 'utf8'));
  const err = verifyPayload(event.client_payload || {}, process.env.ABADIS_WP_WEBHOOK_SECRET || '');
  if (err) {
    console.error(err);
    process.exit(1);
  }
  console.log(`webhook ok action=${event.client_payload.action} post=${event.client_payload.post_id} lang=${event.client_payload.lang}`);
}
