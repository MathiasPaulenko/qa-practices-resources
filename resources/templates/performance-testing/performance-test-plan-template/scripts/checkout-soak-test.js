// checkout-soak-test.js — k6 0.54 soak test: 200 VUs for 12 hours
// Run: k6 run scripts/checkout-soak-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
    vus: 200,
    duration: '12h',
    thresholds: {
        http_req_duration: ['p(95)<300'],
        http_req_failed: ['rate<0.01'],
    },
};

const BASE_URL = 'https://staging.qapractices.com';

export default function () {
    const res = http.get(`${BASE_URL}/api/v1/products`, {
        headers: { 'Accept': 'application/json' },
    });
    check(res, {
        'status is 200': (r) => r.status === 200,
    });
    sleep(2);
}
