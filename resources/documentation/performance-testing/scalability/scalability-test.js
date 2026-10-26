// scalability-test.js — k6 v2.3: stepped load to locate the saturation point
// Usage: BASE_URL=https://staging.qapractices.com k6 run scalability-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  scenarios: {
    stepped_load: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '3m', target: 100 },   // ramp to baseline
        { duration: '10m', target: 100 },  // hold: measure baseline
        { duration: '3m', target: 500 },
        { duration: '10m', target: 500 },  // hold: is throughput ~5x?
        { duration: '3m', target: 1000 },
        { duration: '10m', target: 1000 }, // hold: efficiency maintained?
        { duration: '3m', target: 2000 },
        { duration: '10m', target: 2000 }, // hold: where does it saturate?
        { duration: '3m', target: 5000 },
        { duration: '10m', target: 5000 }, // hold: document degradation
        { duration: '5m', target: 0 },     // scale-in / recovery
      ],
    },
  },
  thresholds: {
    http_req_duration: ['p(95)<800'],
    http_req_failed: ['rate<0.01'],
  },
};

const BASE_URL = __ENV.BASE_URL || 'https://staging.qapractices.com';

export default function () {
  const res = http.get(`${BASE_URL}/api/v1/products?limit=50`);
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response within latency budget': (r) => r.timings.duration < 800,
  });
  sleep(1);
}
