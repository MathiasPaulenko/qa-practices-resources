// stress-test.js
// Ramps past expected peak load to find the breaking point.
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  scenarios: {
    stress: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '2m', target: 100 },
        { duration: '5m', target: 100 },
        { duration: '2m', target: 200 },
        { duration: '5m', target: 200 },
        { duration: '2m', target: 400 },
        { duration: '5m', target: 400 },
        { duration: '2m', target: 0 },
      ],
    },
  },
  thresholds: {
    http_req_failed: ['rate<0.05'],
  },
};

const BASE_URL = __ENV.BASE_URL || 'https://staging.qapractices.com/api/v1';

export default function () {
  const res = http.get(`${BASE_URL}/products?limit=20`);
  check(res, {
    'status 200': (r) => r.status === 200,
  });
  sleep(1);
}
