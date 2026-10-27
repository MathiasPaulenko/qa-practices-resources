// Isolate the bottleneck layer under load.
// Run: k6 run k6-load-isolation.js
// Requires: k6 (https://k6.io/docs/get-started/installation/)
// Watch each layer's metrics while this runs — the layer that
// degrades first is your bottleneck.
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  // Ramp to a realistic load, hold, then ramp down.
  stages: [
    { duration: '30s', target: 10 },
    { duration: '60s', target: 25 },
    { duration: '30s', target: 0 },
  ],
};

export default function () {
  // Placeholder: replace with your staging URL.
  const res = http.get('https://staging.example.com/api/orders');
  check(res, {
    'status is 200': (r) => r.status === 200,
    'p95 response < 300ms': (r) => r.timings.duration < 300,
    'no server errors': (r) => r.status < 500,
  });
  sleep(1);
}
