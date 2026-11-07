// Post-deploy smoke test with k6.
// Runs a short load pass against a critical endpoint and fails if
// latency or error rate crosses the threshold.
//
// Usage:
//   k6 run -e BASE_URL=https://api.yourdomain.com smoke-test.js
//
// Requires: k6 (https://k6.io)

import http from 'k6/http';
import { check } from 'k6';

export const options = {
  thresholds: {
    http_req_duration: ['p(95)<500'],
    http_req_failed: ['rate<0.01'],
  },
  vus: 5,
  duration: '30s',
};

export default function () {
  const res = http.get(`${__ENV.BASE_URL}/api/v1/login`);
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });
}
