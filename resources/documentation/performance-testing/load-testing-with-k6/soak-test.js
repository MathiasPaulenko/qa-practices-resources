// soak-test.js
// Runs steady load for hours to catch memory leaks, log rotation issues
// or certificate renewal problems.
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  scenarios: {
    soak: {
      executor: 'constant-arrival-rate',
      rate: 100,
      timeUnit: '1s',
      duration: '4h',
      preAllocatedVUs: 50,
      maxVUs: 200,
    },
  },
  thresholds: {
    http_req_failed: ['rate<0.01'],
    http_req_duration: ['p(95)<500'],
  },
};

const BASE_URL = __ENV.BASE_URL || 'https://staging.qapractices.com/api/v1';

export default function () {
  const res = http.get(`${BASE_URL}/products?limit=10`);
  check(res, {
    'status 200': (r) => r.status === 200,
  });
  sleep(1);
}
