// k6 throughput saturation ramp — TC-02 of
// https://qapractices.com/test-cases/api-latency-throughput-test-cases/
// Ramps RPS until the p95 threshold or the error-rate abort kicks in.
// Run: k6 run k6-throughput-ramp.js

import http from 'k6/http';
import { check } from 'k6';

export const options = {
  scenarios: {
    saturation_ramp: {
      executor: 'ramping-arrival-rate',
      startRate: 10,
      timeUnit: '1s',
      preAllocatedVUs: 50,
      maxVUs: 500,
      stages: [
        { target: 50, duration: '30s' },
        { target: 100, duration: '30s' },
        { target: 150, duration: '30s' },
        { target: 200, duration: '30s' },
        { target: 0, duration: '30s' },
      ],
    },
  },
  thresholds: {
    http_req_duration: ['p(95)<500'],
    http_req_failed: ['rate<0.01'],
  },
};

const API_BASE_URL = __ENV.API_BASE_URL || 'https://api.example.com';

export default function () {
  const resp = http.get(`${API_BASE_URL}/orders`);
  check(resp, { 'status is 200': r => r.status === 200 });
}
