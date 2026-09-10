import http from 'k6/http';
import { check, sleep } from 'k6';
import { SharedArray } from 'k6/data';

const users = new SharedArray('users', function () {
  return JSON.parse(open('./test-data/users.json'));
});

export const options = {
  scenarios: {
    checkout: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '2m', target: 100 },
        { duration: '5m', target: 100 },
        { duration: '2m', target: 200 },
        { duration: '5m', target: 200 },
        { duration: '2m', target: 0 },
      ],
      gracefulRampDown: '30s',
    },
  },
  thresholds: {
    http_req_duration: ['p(95)<500'],
    http_req_failed: ['rate<0.01'],
    http_reqs: ['rate>1000'],
  },
};

export default function () {
  const user = users[Math.floor(Math.random() * users.length)];

  const cart = http.post(
    'https://api.staging.local/cart',
    JSON.stringify({ userId: user.id, items: [{ sku: user.sku, qty: 1 }] }),
    { headers: { 'Content-Type': 'application/json' } }
  );

  check(cart, {
    'cart status is 201': (r) => r.status === 201,
    'cart under 200ms': (r) => r.timings.duration < 200,
  });

  const checkout = http.post(
    'https://api.staging.local/checkout',
    JSON.stringify({
      cartId: cart.json('id'),
      paymentToken: user.token,
    }),
    { headers: { 'Content-Type': 'application/json' } }
  );

  check(checkout, {
    'checkout status is 201': (r) => r.status === 201,
    'checkout under 500ms': (r) => r.timings.duration < 500,
  });

  sleep(Math.random() * 2 + 1);
}