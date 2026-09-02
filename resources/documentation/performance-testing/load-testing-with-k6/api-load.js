// api-load.js
// Main k6 load test script for the QAPractices k6 tutorial.
// Tests a login flow followed by an authenticated order search.
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend } from 'k6/metrics';

const loginDuration = new Trend('login_duration');
const searchErrorRate = new Rate('search_errors');

export const options = {
  scenarios: {
    load: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '1m', target: 50 },
        { duration: '3m', target: 50 },
        { duration: '1m', target: 100 },
        { duration: '3m', target: 100 },
        { duration: '1m', target: 0 },
      ],
      gracefulRampDown: '10s',
    },
  },
  thresholds: {
    http_req_duration: ['p(95)<500'],
    http_req_failed: ['rate<0.01'],
    'login_duration': ['p(95)<800'],
    'search_errors': ['rate<0.05'],
    checks: ['rate>0.99'],
  },
};

const BASE_URL = __ENV.BASE_URL || 'https://staging.qapractices.com/api/v1';
const USER = __ENV.USER || 'qa-load@qapractices.com';
const PASS = __ENV.PASS || 'Str0ngP@ss!';

export function setup() {
  const loginRes = http.post(`${BASE_URL}/auth/token`, JSON.stringify({
    email: USER,
    password: PASS,
  }), {
    headers: { 'Content-Type': 'application/json' },
  });

  check(loginRes, {
    'login returns 200': (r) => r.status === 200,
    'login returns token': (r) => r.json('access_token') !== undefined,
  });

  return { token: loginRes.json('access_token') };
}

export default function (data) {
  const start = Date.now();
  const loginRes = http.post(`${BASE_URL}/auth/token`, JSON.stringify({
    email: USER,
    password: PASS,
  }), {
    headers: { 'Content-Type': 'application/json' },
  });
  loginDuration.add(Date.now() - start);

  check(loginRes, {
    'login still returns 200': (r) => r.status === 200,
  });

  const searchRes = http.get(`${BASE_URL}/orders?status=pending&limit=20`, {
    headers: {
      Authorization: `Bearer ${data.token}`,
      'Content-Type': 'application/json',
    },
  });

  const searchOk = check(searchRes, {
    'search returns 200': (r) => r.status === 200,
    'search returns orders': (r) => r.json('data') && r.json('data').length > 0,
  });

  searchErrorRate.add(!searchOk);

  sleep(Math.random() * 2 + 1); // think time between 1 and 3 seconds
}
