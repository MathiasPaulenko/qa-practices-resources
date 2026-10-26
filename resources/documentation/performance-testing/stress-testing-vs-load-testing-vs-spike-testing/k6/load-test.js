// k6 1.x — load profile: ramp to 50 VUs, hold, ramp down, with thresholds.
// Run: k6 run --env BASE_URL=https://your-staging.dev k6/load-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';

const BASE_URL = __ENV.BASE_URL || 'https://api.staging.acme-shop.dev'; // Placeholder: replace with your staging URL

export const options = {
  stages: [
    { duration: '2m', target: 50 },  // ramp up to 50 virtual users
    { duration: '5m', target: 50 },  // sustained load
    { duration: '1m', target: 0 },   // ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],
    http_req_failed: ['rate<0.001'],
  },
};

export default function () {
  const res = http.get(`${BASE_URL}/api/v1/products`);
  check(res, { 'status is 200': (r) => r.status === 200 });
  sleep(1);
}
