import http from 'k6/http';
import { check, sleep } from 'k6';
import { SharedArray } from 'k6/data';

const users = new SharedArray('test users', function () {
  return JSON.parse(open('../data/test-users.json'));
});

export const options = {
  scenarios: {
    checkout_journey: {
      executor: 'ramping-vus',
      stages: [
        { duration: '10m', target: 250 },
        { duration: '60m', target: 250 },
        { duration: '5m', target: 0 },
      ],
    },
  },
  thresholds: {
    http_req_duration: ['p(95)<2000'],
    http_req_failed: ['rate<0.01'],
    'checks{journey:checkout}': ['rate>0.98'],
  },
};

const BASE_URL = __ENV.BASE_URL || 'https://staging.your-app.internal';

export default function () {
  const user = users[__VU % users.length];
  const params = { headers: { 'Content-Type': 'application/json' } };

  const productRes = http.get(`${BASE_URL}/product/wool-coat-black`, {
    tags: { journey: 'checkout' },
  });
  check(productRes, { 'product page 200': (r) => r.status === 200 });
  sleep(5 + Math.random() * 10);

  const cartRes = http.post(`${BASE_URL}/api/cart/add`,
    JSON.stringify({ productId: 'wc-black-m', quantity: 1, userId: user.id }),
    { ...params, tags: { journey: 'checkout' } });
  check(cartRes, { 'add to cart 200': (r) => r.status === 200 });
  sleep(2 + Math.random() * 3);

  const checkoutRes = http.post(`${BASE_URL}/api/checkout/place`,
    JSON.stringify({
      shippingAddress: { city: 'Madrid', zip: '28001' },
      paymentMethod: 'stripe_test_card',
      userId: user.id,
    }),
    { ...params, tags: { journey: 'checkout' } });
  check(checkoutRes, { 'checkout 200': (r) => r.status === 200 });
  sleep(3 + Math.random() * 7);
}
