// RUM collector for Core Web Vitals — mirror of the article snippet.
// Requires: npm install web-vitals@^5
// Ships LCP, INP and CLS to your analytics endpoint; metric.id groups
// reports by page view instead of double-counting per session.
import { onLCP, onINP, onCLS } from 'web-vitals';

const ENDPOINT = '/analytics/web-vitals'; // replace with your collector

function sendToAnalytics(metric) {
  const body = JSON.stringify({
    name: metric.name,
    value: Math.round(metric.value),
    id: metric.id,
    rating: metric.rating, // 'good' | 'needs-improvement' | 'poor'
    delta: metric.delta,
  });
  // sendBeacon survives page unload; fetch keepalive as fallback
  if (navigator.sendBeacon) {
    navigator.sendBeacon(ENDPOINT, body);
  } else {
    fetch(ENDPOINT, { body, method: 'POST', keepalive: true });
  }
}

onLCP(sendToAnalytics);
onINP(sendToAnalytics);
onCLS(sendToAnalytics);
