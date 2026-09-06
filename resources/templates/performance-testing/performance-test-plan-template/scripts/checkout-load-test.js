// checkout-load-test.js — k6 0.54 normal load test for checkout API
// Run: k6 run --vus 200 --duration 30m --out json=results.json scripts/checkout-load-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
    vus: 200,
    duration: '30m',
    thresholds: {
        http_req_duration: ['p(95)<250', 'p(99)<500'],
        http_req_failed: ['rate<0.001'],
    },
};

const BASE_URL = 'https://staging.qapractices.com';

export default function () {
    const res = http.get(`${BASE_URL}/api/v1/products`, {
        headers: { 'Accept': 'application/json' },
    });
    check(res, {
        'status is 200': (r) => r.status === 200,
        'response time < 250ms': (r) => r.timings.duration < 250,
    });
    sleep(1);
}
