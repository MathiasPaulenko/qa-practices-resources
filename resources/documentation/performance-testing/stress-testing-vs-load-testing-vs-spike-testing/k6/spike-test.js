// k6 1.x — spike profile: 100 rps baseline, instant jump to 1,000 rps.
// Run: k6 run --env BASE_URL=https://your-staging.dev k6/spike-test.js
import http from 'k6/http';
import { check } from 'k6';

const BASE_URL = __ENV.BASE_URL || 'https://api.staging.acme-shop.dev'; // Placeholder: replace with your staging URL

export const options = {
  scenarios: {
    spike: {
      executor: 'ramping-arrival-rate',
      startRate: 100,
      timeUnit: '1s',
      preAllocatedVUs: 200,
      maxVUs: 1500,
      stages: [
        { duration: '1m', target: 100 },   // baseline
        { duration: '10s', target: 1000 }, // spike up
        { duration: '2m', target: 1000 },  // hold the spike
        { duration: '10s', target: 100 },  // drop back
        { duration: '2m', target: 100 },   // observe recovery
      ],
    },
  },
};

export default function () {
  const res = http.get(`${BASE_URL}/api/v1/products`);
  check(res, { 'status is 200': (r) => r.status === 200 });
}
