// k6 0.54 performance test: ramp to 100 VUs and enforce SLA thresholds.
// Run: k6 run -e API_TOKEN=... k6-perf-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 50 },
    { duration: '1m', target: 100 },
    { duration: '30s', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<200', 'p(99)<500'],
    http_req_failed: ['rate<0.01'],
  },
};

export default function () {
  const res = http.get('https://api.paygateway.com/payments', {
    headers: { Authorization: `Bearer ${__ENV.API_TOKEN}` },
  });
  check(res, { 'status is 200': (r) => r.status === 200 });
  sleep(1);
}
