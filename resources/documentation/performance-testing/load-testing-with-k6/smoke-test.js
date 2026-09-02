// smoke-test.js
// Short, low-load run that proves the system works before a larger test.
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  scenarios: {
    smoke: {
      executor: 'constant-vus',
      vus: 5,
      duration: '1m',
    },
  },
  thresholds: {
    http_req_duration: ['p(95)<300'],
    http_req_failed: ['rate<0.01'],
  },
};

const BASE_URL = __ENV.BASE_URL || 'https://staging.qapractices.com/api/v1';

export default function () {
  const res = http.get(`${BASE_URL}/health`);
  check(res, {
    'health check 200': (r) => r.status === 200,
  });
  sleep(1);
}
