// web-vitals 6.x RUM collector — sends Core Web Vitals to your own endpoint.
// Install: npm i web-vitals@^6   (v4+ removed get* helpers; v5 removed onFID)
import { onCLS, onINP, onLCP, onFCP, onTTFB } from 'web-vitals';

const send = (metric) =>
  navigator.sendBeacon('/rum', JSON.stringify({
    name: metric.name,
    value: metric.value,
    rating: metric.rating,   // 'good' | 'needs-improvement' | 'poor'
    page: location.pathname,
  }));

onCLS(send);
onINP(send);   // INP replaced FID as the interaction Core Web Vital in 2024
onLCP(send);
onFCP(send);
onTTFB(send);
