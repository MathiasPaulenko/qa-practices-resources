// k6 1.x — stress profile: incremental ramping-vus past the expected maximum.
// Watch where http_req_failed crosses your error budget — that is the breaking point.
// Run: k6 run --env BASE_URL=https://your-staging.dev k6/stress-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';

const BASE_URL = __ENV.BASE_URL || 'https://api.staging.acme-shop.dev'; // Placeholder: replace with your staging URL

export const options = {
  scenarios: {
    stress: {
      executor: 'ramping-vus',
      startVUs: 50,
      stages: [
        { duration: '2m', target: 100 },  // above expected load
        { duration: '3m', target: 200 },
        { duration: '3m', target: 400 },
        { duration: '3m', target: 800 },  // push toward failure
        { duration: '5m', target: 800 },  // hold at overload, observe degradation
        { duration: '2m', target: 0 },    // drop load, measure recovery time
      ],
      gracefulRampDown: '30s',
    },
  },
  // Deliberately no abort thresholds: a stress test is supposed to reach failure.
};

export default function () {
  const res = http.get(`${BASE_URL}/api/v1/products`);
  check(res, {
    'status is 200': (r) => r.status === 200,
    'responds under 2s': (r) => r.timings.duration < 2000,
  });
  sleep(1);
}
