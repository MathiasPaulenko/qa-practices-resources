// interview-load-test.js — runnable companion for
// https://qapractices.com/documentation/performance-testing-interview-questions/
// Combines the Q19 stages/thresholds pattern with the Q20 SharedArray login flow.
// Run: BASE_URL=https://staging.example.internal k6 run interview-load-test.js

import http from 'k6/http';
import { check, sleep } from 'k6';
import { SharedArray } from 'k6/data';

const BASE_URL = __ENV.BASE_URL || 'https://test-api.k6.io';

const users = new SharedArray('users', function () {
  return open('./data/users.csv')
    .split('\n')
    .filter((line) => line.trim() !== '' && !line.startsWith('username'))
    .map((line) => {
      const [username, password] = line.split(',');
      return { username: username.trim(), password: password.trim() };
    });
});

export const options = {
  stages: [
    { duration: '30s', target: 20 },
    { duration: '1m', target: 20 },
    { duration: '30s', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<500', 'p(99)<2000'],
    http_req_failed: ['rate<0.01'],
  },
};

export default function () {
  const user = users[__VU % users.length];

  const login = http.post(`${BASE_URL}/login`, JSON.stringify(user), {
    headers: { 'Content-Type': 'application/json' },
  });
  check(login, {
    'login status is 200': (r) => r.status === 200,
  });

  const res = http.get(`${BASE_URL}/products`);
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });

  sleep(1);
}
