// checkout-spike-test.js — k6 0.54 spike test: 100 to 1000 VUs in 1 minute
// Run: k6 run scripts/checkout-spike-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
    stages: [
        { duration: '2m', target: 100 },
        { duration: '1m', target: 1000 },
        { duration: '5m', target: 1000 },
        { duration: '2m', target: 100 },
        { duration: '1m', target: 0 },
    ],
    thresholds: {
        http_req_failed: ['rate<0.01'],
    },
};

const BASE_URL = 'https://staging.qapractices.com';

export default function () {
    const res = http.get(`${BASE_URL}/api/v1/products`, {
        headers: { 'Accept': 'application/json' },
    });
    check(res, {
        'status is 200 or 503': (r) => r.status === 200 || r.status === 503,
    });
    sleep(0.5);
}
