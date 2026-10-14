// k6 load test — equivalent scenario across the three tools.
// Run: k6 run k6/load-test.js   (requires k6 v1.x)
import http from 'k6/http';
import { check, sleep } from 'k6';

const BASE_URL = __ENV.BASE_URL || 'https://staging.acme-shop.dev'; // Placeholder: replace with staging URL

export const options = {
  stages: [
    { duration: '30s', target: 20 },  // ramp
    { duration: '60s', target: 50 },  // sustain
    { duration: '15s', target: 0 },   // ramp-down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],
    http_req_failed: ['rate<0.01'],
  },
};

export default function () {
  const res = http.get(`${BASE_URL}/api/v1/products`);
  check(res, {
    'status is 200': (r) => r.status === 200,
    'payload is json': (r) => (r.headers['Content-Type'] || '').includes('application/json'),
  });
  sleep(1);
}
