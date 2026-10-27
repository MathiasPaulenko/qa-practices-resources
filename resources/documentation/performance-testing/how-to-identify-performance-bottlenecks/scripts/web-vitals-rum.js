// Collect real-user Web Vitals and send them to your metrics endpoint.
// Requires: web-vitals 4.x — npm install web-vitals
// Use in production RUM, not lab tests: this captures what users actually feel.
import { onCLS, onLCP, onINP, onFCP, onTTFB } from 'web-vitals';

function sendToAnalytics(metric) {
  // Keep payloads small; batch if you have a collector.
  const payload = JSON.stringify({
    name: metric.name,
    value: metric.value,
    rating: metric.rating,
    id: metric.id,
  });
  // sendBeacon survives page unload better than fetch.
  navigator.sendBeacon('/api/metrics', payload);
}

onLCP(sendToAnalytics);
onINP(sendToAnalytics);
onCLS(sendToAnalytics);
onFCP(sendToAnalytics);
onTTFB(sendToAnalytics);
