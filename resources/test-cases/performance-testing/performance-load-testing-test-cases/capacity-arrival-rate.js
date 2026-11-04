// Constant arrival rate variant — proves the system sustains a request rate
// rather than just answering N concurrent VUs. Maps to TC-PL-18.
// Run: k6 run capacity-arrival-rate.js
import http from 'k6/http';
import { check, sleep } from 'k6';

const BASE_URL = __ENV.BASE_URL || 'http://localhost:8080';

export const options = {
  scenarios: {
    sustained_rate: {
      executor: 'constant-arrival-rate',
      rate: 100,               // 100 iterations per second
      timeUnit: '1s',
      duration: '10m',
      preAllocatedVUs: 50,
      maxVUs: 200,             // headroom before k6 drops iterations
    },
  },
  thresholds: {
    http_req_duration: ['p(95)<500', 'p(99)<1000'],
    http_req_failed: ['rate<0.01'],
    dropped_iterations: ['count<10'],
  },
};

export default function () {
  const res = http.get(`${BASE_URL}/api/products`);
  check(res, { 'status is 200': (r) => r.status === 200 });
  sleep(0.5);
}
