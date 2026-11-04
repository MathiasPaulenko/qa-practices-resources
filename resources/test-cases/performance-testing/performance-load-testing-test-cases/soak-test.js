// Soak configuration — moderate load held for hours to expose memory leaks,
// connection leaks and metric drift. Maps to TC-PL-12.
// Run: k6 run soak-test.js   (shorten the hold for a smoke pass)
import http from 'k6/http';
import { check, sleep } from 'k6';

const BASE_URL = __ENV.BASE_URL || 'http://localhost:8080';

export const options = {
  stages: [
    { duration: '5m', target: 35 },   // gentle ramp
    { duration: '4h', target: 35 },   // hold ~70% of normal load
    { duration: '5m', target: 0 },
  ],
  thresholds: {
    // tighter than the spike profile — soak should stay boring
    http_req_duration: ['p(95)<400'],
    http_req_failed: ['rate<0.005'],
  },
};

export default function () {
  const res = http.get(`${BASE_URL}/api/products`);
  check(res, { 'status is 200': (r) => r.status === 200 });
  sleep(1);
}
