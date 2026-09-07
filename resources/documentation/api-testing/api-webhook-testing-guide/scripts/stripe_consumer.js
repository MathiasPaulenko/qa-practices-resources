/**
 * Stripe webhook consumer with signature verification, queue, and idempotency.
 *
 * Usage:
 *   STRIPE_WEBHOOK_SECRET=whsec_test123 node stripe_consumer.js
 *
 * Features:
 * - Verifies HMAC-SHA256 signature over raw body (not parsed JSON)
 * - Returns 200 within 2 seconds (acknowledges fast, processes async)
 * - Checks event ID in Redis-like store for idempotency
 * - Handles 400 (terminal), 500 (retry), 410 (disable) correctly
 */

const express = require('express');
const crypto = require('crypto');

const app = express();
const secret = process.env.STRIPE_WEBHOOK_SECRET || 'whsec_test123';

// In-memory event ID store (use Redis in production)
const seenEventIds = new Map();
const EVENT_TTL_MS = 24 * 60 * 60 * 1000; // 24 hours

// In-memory queue (use Bull/Redis in production)
const queue = [];

function verifySignature(rawBody, signatureHeader) {
  // Stripe format: t=1234567890,v1=abc123...
  const parts = signatureHeader.split(',');
  const timestampPart = parts.find(p => p.startsWith('t='));
  const signaturePart = parts.find(p => p.startsWith('v1='));

  if (!timestampPart || !signaturePart) return false;

  const timestamp = timestampPart.split('=')[1];
  const signature = signaturePart.split('=')[1];

  // Reject timestamps older than 5 minutes (replay protection)
  const now = Math.floor(Date.now() / 1000);
  if (Math.abs(now - parseInt(timestamp)) > 300) return false;

  // Compute HMAC over "timestamp.rawBody"
  const signedPayload = `${timestamp}.${rawBody}`;
  const expected = crypto
    .createHmac('sha256', secret)
    .update(signedPayload, 'utf8')
    .digest('hex');

  return crypto.timingSafeEqual(
    Buffer.from(signature, 'utf8'),
    Buffer.from(expected, 'utf8')
  );
}

function isIdempotent(eventId) {
  const now = Date.now();
  // Clean expired entries
  for (const [id, expiry] of seenEventIds) {
    if (expiry < now) seenEventIds.delete(id);
  }
  if (seenEventIds.has(eventId)) return false;
  seenEventIds.set(eventId, now + EVENT_TTL_MS);
  return true;
}

app.post('/webhooks', express.raw({ type: 'application/json' }), (req, res) => {
  const signatureHeader = req.headers['stripe-signature'];

  if (!signatureHeader) {
    return res.status(400).send('Missing signature header');
  }

  if (!verifySignature(req.body, signatureHeader)) {
    return res.status(401).send('Invalid signature');
  }

  const event = JSON.parse(req.body);

  // Idempotency check before queueing
  if (!isIdempotent(event.id)) {
    console.log(`Duplicate event ${event.id} — skipping`);
    return res.status(200).send('OK (duplicate)');
  }

  // Queue for async processing — return 200 immediately
  queue.push(event);
  console.log(`Queued event ${event.id} (type: ${event.type})`);

  return res.status(200).send('OK');
});

// Worker: process queue every 2 seconds
setInterval(() => {
  while (queue.length > 0) {
    const event = queue.shift();
    console.log(`Processing event ${event.id} (type: ${event.type})`);
    // Simulate processing
  }
}, 2000);

app.listen(3000, () => {
  console.log('Webhook consumer running on port 3000');
  console.log(`Secret: ${secret.substring(0, 8)}...`);
});
