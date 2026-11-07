import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '5m', target: 100 },  // ramp up
    { duration: '10m', target: 100 }, // steady state
    { duration: '5m', target: 200 },  // increase load
    { duration: '10m', target: 200 }, // sustained higher load
    { duration: '5m', target: 0 },    // ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<1000'], // 95% under 1s
    http_req_failed: ['rate<0.01'],    // error rate < 1%
  },
};

const BASE_URL = __ENV.BASE_URL || 'https://staging.example.com';

export default function () {
  const res = http.get(`${BASE_URL}/products`);
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });
  sleep(Math.random() * 3 + 1); // 1-4s think time
}
