// Load profile from the resource: ramp-up → steady → spike → ramp-down.
// Maps to TC-PL-01 (normal load), TC-PL-04 (peak) and TC-PL-07 (recovery).
// Run: k6 run load-profile.js
import http from 'k6/http';
import { check, sleep } from 'k6';

const BASE_URL = __ENV.BASE_URL || 'http://localhost:8080';

export const options = {
  stages: [
    { duration: '2m', target: 50 },   // ramp-up to normal
    { duration: '5m', target: 50 },   // steady state — p95 vs SLO
    { duration: '1m', target: 200 },  // spike — flash sale
    { duration: '3m', target: 200 },  // hold spike
    { duration: '2m', target: 0 },    // ramp-down — recovery window
  ],
  thresholds: {
    http_req_duration: ['p(95)<500', 'p(99)<1000'],
    http_req_failed: ['rate<0.01'],
  },
};

export default function () {
  const res = http.get(`${BASE_URL}/api/products`);
  check(res, { 'status is 200': (r) => r.status === 200 });
  sleep(1);
}
