import http from 'k6/http';
import { check, sleep } from 'k6';

// k6 v1.x — NovaPay v2 payments flow.
// 50,000 VUs, full load inside a 12-minute ramp, 30-minute plateau.

export const options = {
  scenarios: {
    payments: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '2m', target: 5000 },
        { duration: '10m', target: 50000 },
        { duration: '30m', target: 50000 },
        { duration: '2m', target: 0 },
      ],
      gracefulRampDown: '30s',
    },
  },
  thresholds: {
    http_req_failed: ['rate<0.005'],
    http_req_duration: ['p(95)<300', 'p(99)<500'],
  },
};

// Placeholder: replace with your staging API URL.
const BASE_URL = __ENV.BASE_URL || 'https://api.novapay.example.com/v2';
const API_KEY = __ENV.NOVA_API_KEY;

export default function () {
  const paymentPayload = JSON.stringify({
    amount: 99.99,
    currency: 'USD',
    token: `tok-${__VU}-${__ITER}`,
  });

  const paymentRes = http.post(`${BASE_URL}/payments`, paymentPayload, {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${API_KEY}`,
    },
  });

  check(paymentRes, {
    'payment status is 201': (r) => r.status === 201,
    'p95 under 300ms': (r) => r.timings.duration < 300,
    'payment accepted': (r) => r.json('status') === 'ACCEPTED',
  });

  const transactionId = paymentRes.json('transactionId');
  if (transactionId) {
    const refundRes = http.post(`${BASE_URL}/refunds`, JSON.stringify({ transactionId }), {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${API_KEY}`,
      },
    });

    check(refundRes, {
      'refund status is 201': (r) => r.status === 201,
    });
  }

  // ~40 s think time keeps injection near the 2,400 req/s SLO at 50k VUs.
  sleep(40);
}
