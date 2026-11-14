import http from 'k6/http';
import { check, sleep } from 'k6';
import { SharedArray } from 'k6/data';
import { Rate } from 'k6/metrics';

const errorRate = new Rate('checkout_errors');

const users = new SharedArray('users', () =>
  JSON.parse(open('./users.json'))
);

export const options = {
  scenarios: {
    spike: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '10s', target: 100 },
        { duration: '10s', target: 1000 },
        { duration: '1m', target: 1000 },
        { duration: '10s', target: 100 },
        { duration: '1m', target: 100 },
        { duration: '10s', target: 0 },
      ],
    },
  },
  thresholds: {
    http_req_duration: ['p(95)<300', 'p(99)<800'],
    http_req_failed: ['rate<0.005'],
    checkout_errors: ['rate<0.005'],
  },
};

export function setup() {
  const res = http.post(`${__ENV.BASE_URL}/oauth/token`, {
    client_id: __ENV.CLIENT_ID,
    client_secret: __ENV.CLIENT_SECRET,
    grant_type: 'client_credentials',
  });
  return { token: res.json('access_token') };
}

export default function (data) {
  const headers = { Authorization: `Bearer ${data.token}` };
  const user = users[Math.floor(Math.random() * users.length)];

  const list = http.get(`${__ENV.BASE_URL}/products`, { headers });
  check(list, { 'products 200': (r) => r.status === 200 });
  sleep(1 + Math.random() * 2);

  const cart = http.post(
    `${__ENV.BASE_URL}/cart`,
    JSON.stringify({ userId: user.id, items: [{ sku: 'SKU-1042', qty: 1 }] }),
    { headers: { ...headers, 'Content-Type': 'application/json' } }
  );
  const cartId = cart.json('id');

  const checkout = http.post(
    `${__ENV.BASE_URL}/checkout`,
    JSON.stringify({ cartId, userId: user.id }),
    { headers: { ...headers, 'Content-Type': 'application/json' } }
  );
  const ok = check(checkout, { 'checkout 201': (r) => r.status === 201 });
  errorRate.add(!ok);
  sleep(1 + Math.random() * 2);
}
