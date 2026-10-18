// k6 latency test — concurrent load profile from TC-02/TC-03 of
// https://qapractices.com/test-cases/api-latency-throughput-test-cases/
// Run: k6 run k6-latency.js
// Replace API_BASE_URL with your test environment (api.example.com is a placeholder).

import http from 'k6/http';
import { check } from 'k6';

export const options = {
  vus: 100,
  duration: '30s',
  thresholds: {
    http_req_duration: ['p(95)<500'],
  },
};

const API_BASE_URL = __ENV.API_BASE_URL || 'https://api.example.com';

export default function () {
  const resp = http.get(`${API_BASE_URL}/orders`);
  check(resp, {
    'status is 200': r => r.status === 200,
    'p95 under 500ms': r => r.timings.duration < 500,
  });
}
