// Retry + dead letter queue simulator — shows backoff schedule and DLQ transition
// without waiting real hours. Run: node retry-simulator.js
const CONFIG = {
  maxAttempts: 5,
  initialDelayMs: 1000,      // real world: 1s → 2s → 4s → 8s → 16s
  maxDelayMs: 24 * 3600e3,
  retryOn: [408, 429, 500, 502, 503, 504],
};

function schedule(n) {
  const delays = [];
  for (let i = 0; i < n; i++) {
    delays.push(Math.min(CONFIG.initialDelayMs * 2 ** i, CONFIG.maxDelayMs));
  }
  return delays;
}

function deliver(responses) {
  // responses: array of status codes the receiver returns per attempt
  const log = [];
  for (let attempt = 0; attempt < CONFIG.maxAttempts; attempt++) {
    const status = responses[attempt] ?? 500;
    const willRetry = CONFIG.retryOn.includes(status) && attempt < CONFIG.maxAttempts - 1;
    log.push({ attempt: attempt + 1, status, willRetry });
    if (!willRetry) break;
  }
  const last = log[log.length - 1];
  return { log, outcome: last.status < 300 ? 'delivered' : (CONFIG.retryOn.includes(last.status) ? 'dlq' : 'failed-no-retry') };
}

console.log('Backoff schedule:', schedule(CONFIG.maxAttempts - 1).map(d => `${d}ms`).join(' → '), '\n');

for (const [name, responses] of [
  ['success first try', [200]],
  ['transient 500 then 200', [500, 200]],
  ['429 rate limited then ok', [429, 429, 200]],
  ['all retries exhausted → DLQ', [500, 500, 500, 500, 500]],
  ['400 never retried', [400]],
  ['401 never retried + alert', [401]],
]) {
  const r = deliver(responses);
  console.log(`--- ${name} → ${r.outcome}`);
  for (const e of r.log) console.log(`    attempt ${e.attempt}: ${e.status}${e.willRetry ? ' → retry' : ''}`);
}
