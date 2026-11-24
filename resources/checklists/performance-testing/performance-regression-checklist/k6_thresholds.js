// k6 perf gate — exits non-zero when a threshold is breached.
// Run: k6 run --env BASE_URL=https://staging.example.internal k6_thresholds.js
// Baseline values below are examples; refresh them per release tag.

import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  scenarios: {
    reference_load: {
      executor: 'constant-vus',
      vus: 50,
      duration: '5m',
    },
  },
  thresholds: {
    // p95 per critical flow, derived from the stored baseline + headroom
    'http_req_duration{endpoint:checkout}': ['p(95)<400'],
    'http_req_duration{endpoint:search}': ['p(95)<800'],
    'http_req_duration{endpoint:login}': ['p(95)<350'],
    // absolute ceilings
    http_req_failed: ['rate<0.005'],
    // throughput floor from the baseline capture
    http_reqs: ['rate>45'],
  },
};

const BASE_URL = __ENV.BASE_URL || 'http://localhost:8080';

export default function () {
  const login = http.post(`${BASE_URL}/api/login`, JSON.stringify({ user: 'perf', pass: 'perf' }), {
    headers: { 'Content-Type': 'application/json' },
    tags: { endpoint: 'login' },
  });
  check(login, { 'login ok': (r) => r.status === 200 });

  const search = http.get(`${BASE_URL}/api/search?q=test`, { tags: { endpoint: 'search' } });
  check(search, { 'search ok': (r) => r.status === 200 });

  const checkout = http.post(`${BASE_URL}/api/checkout`, JSON.stringify({ cart: 'perf-fixture' }), {
    headers: { 'Content-Type': 'application/json' },
    tags: { endpoint: 'checkout' },
  });
  check(checkout, { 'checkout ok': (r) => r.status < 400 });

  sleep(1);
}
