import http from 'k6/http';
import { check } from 'k6';

export const options = {
  stages: [
    { duration: '2m', target: 100 },
    { duration: '5m', target: 100 },
    { duration: '2m', target: 200 },
    { duration: '5m', target: 200 },
    { duration: '2m', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<300'],
    http_req_failed: ['rate<0.01'],
  },
};

export default function () {
  const res = http.get('https://api.staging.local/api/v1/health', {
    headers: { 'api-key': __ENV.STAGING_API_KEY || 'test-key' },
  });

  check(res, {
    'status is 200': (r) => r.status === 200,
    'p95 under 300ms': (r) => r.timings.waiting < 300,
  });
}