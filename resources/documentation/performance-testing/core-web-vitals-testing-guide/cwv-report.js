// web-vitals 6.x — report LCP, INP and CLS to your RUM endpoint.
// npm install web-vitals@6
import { onLCP, onINP, onCLS } from 'web-vitals';

function sendToAnalytics({ name, value, rating, id }) {
  navigator.sendBeacon('/rum', JSON.stringify({
    metric: name,
    value: Math.round(name === 'CLS' ? value * 1000 : value),
    rating,           // 'good' | 'needs-improvement' | 'poor'
    id,               // deduplicates per page visit
    page: location.pathname
  }));
}

onLCP(sendToAnalytics);
onINP(sendToAnalytics);
onCLS(sendToAnalytics);
