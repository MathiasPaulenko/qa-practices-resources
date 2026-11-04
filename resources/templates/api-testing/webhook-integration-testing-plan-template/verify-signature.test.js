// Webhook signature verifier + tests — Stripe-style t=,v1= scheme.
// Run: node verify-signature.test.js  (uses node:test, zero deps)
const { createHmac, timingSafeEqual } = require('node:crypto');
const { test } = require('node:test');
const assert = require('node:assert');

const SECRET = 'whsec_test_key_0123456789abcdef';

function sign(payload, timestamp) {
  return createHmac('sha256', SECRET).update(`${timestamp}.${payload}`).digest('hex');
}

function header(payload, ts = Math.floor(Date.now() / 1000)) {
  return `t=${ts},v1=${sign(payload, ts)}`;
}

function verifySignature(payload, signatureHeader, secret, tolerance = 300) {
  const parts = signatureHeader.split(',');
  const tsPart = parts.find(p => p.startsWith('t='));
  const sigPart = parts.find(p => p.startsWith('v1='));
  if (!tsPart || !sigPart) return false;
  const ts = parseInt(tsPart.split('=')[1], 10);
  const provided = sigPart.split('=')[1];
  const now = Math.floor(Date.now() / 1000);
  if (Math.abs(now - ts) > tolerance) return false;
  const expected = createHmac('sha256', secret).update(`${ts}.${payload}`).digest('hex');
  const a = Buffer.from(provided), b = Buffer.from(expected);
  return a.length === b.length && timingSafeEqual(a, b);
}

const PAYLOAD = JSON.stringify({ event_id: 'evt_abc123', event_type: 'payment.succeeded', data: { object: { amount: 4999 } } });

test('valid signature accepted', () => {
  assert.strictEqual(verifySignature(PAYLOAD, header(PAYLOAD), SECRET), true);
});

test('missing signature header rejected', () => {
  assert.strictEqual(verifySignature(PAYLOAD, '', SECRET), false);
});

test('tampered payload rejected — signature covers raw body', () => {
  const tampered = PAYLOAD.replace('4999', '9999');
  assert.strictEqual(verifySignature(tampered, header(PAYLOAD), SECRET), false);
});

test('wrong secret rejected', () => {
  assert.strictEqual(verifySignature(PAYLOAD, header(PAYLOAD), 'whsec_wrong'), false);
});

test('expired timestamp rejected (outside 300s tolerance)', () => {
  const old = Math.floor(Date.now() / 1000) - 400;
  assert.strictEqual(verifySignature(PAYLOAD, header(PAYLOAD, old), SECRET), false);
});

test('malformed header rejected', () => {
  assert.strictEqual(verifySignature(PAYLOAD, 'garbage', SECRET), false);
  assert.strictEqual(verifySignature(PAYLOAD, 'v1=abc', SECRET), false);
});
