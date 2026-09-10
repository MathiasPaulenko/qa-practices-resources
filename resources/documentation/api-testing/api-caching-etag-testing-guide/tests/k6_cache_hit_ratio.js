import http from 'k6/http';
import { check } from 'k6';

export const options = {
  vus: 50,
  duration: '2m',
  thresholds: {
    http_req_duration: ['p(95)<200'],
    http_req_failed: ['rate<0.01'],
  },
};

export default function () {
  const res = http.get('https://api.staging.local/products/123');

  check(res, {
    'status is 200 or 304': (r) => r.status === 200 || r.status === 304,
    'has Cache-Control or ETag': (r) =>
      r.headers['Cache-Control'] !== undefined || r.headers['ETag'] !== undefined,
    'cache hit is fast': (r) => r.status === 304 || r.timings.waiting < 50,
  });
}