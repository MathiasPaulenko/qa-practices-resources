// spike-test.js
// Jumps to a high load quickly and ramps down just as quickly.
// Use it for flash-sale or notification bursts.
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  scenarios: {
    spike: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '10s', target: 1000 },
        { duration: '1m', target: 1000 },
        { duration: '10s', target: 0 },
      ],
    },
  },
  thresholds: {
    http_req_failed: ['rate<0.01'],
  },
};

const BASE_URL = __ENV.BASE_URL || 'https://staging.qapractices.com/api/v1';

export default function () {
  const res = http.get(`${BASE_URL}/health`);
  check(res, {
    'health 200': (r) => r.status === 200,
  });
  sleep(0.5);
}
