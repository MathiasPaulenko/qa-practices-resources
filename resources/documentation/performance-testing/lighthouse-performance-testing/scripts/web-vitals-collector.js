// Production RUM collector using web-vitals 4
// Install: npm install web-vitals@4
import { onLCP, onINP, onCLS, onFCP, onTTFB } from 'web-vitals';

function sendToAnalytics(metric) {
    // Use sendBeacon for reliability on page unload
    const body = JSON.stringify({
        name: metric.name,
        value: metric.value,
        id: metric.id,
        delta: metric.delta,
        rating: metric.rating,
    });

    if (navigator.sendBeacon) {
        navigator.sendBeacon('/api/vitals', body);
    } else {
        fetch('/api/vitals', {
            method: 'POST',
            body,
            keepalive: true,
        }).catch(() => {});
    }
}

onLCP(sendToAnalytics);
onINP(sendToAnalytics);
onCLS(sendToAnalytics);
onFCP(sendToAnalytics);
onTTFB(sendToAnalytics);
