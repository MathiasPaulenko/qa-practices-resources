// Workbox 7 routing config for PWA caching strategies
// Install: npm install workbox-routing@7 workbox-strategies@7
import { registerRoute } from 'workbox-routing';
import { CacheFirst, NetworkFirst, StaleWhileRevalidate } from 'workbox-strategies';

// Pages: Network First (fresh content, offline fallback)
registerRoute(
  ({ request }) => request.mode === 'navigate',
  new NetworkFirst({
    cacheName: 'pages-v1',
    networkTimeoutSeconds: 3,
  })
);

// Static assets: Cache First (fast, immutable)
registerRoute(
  ({ request }) =>
    request.destination === 'style' ||
    request.destination === 'script' ||
    request.destination === 'image' ||
    request.destination === 'font',
  new CacheFirst({
    cacheName: 'static-v1',
  })
);

// API: Stale-While-Revalidate (fast, updated in background)
registerRoute(
  ({ url }) => url.pathname.startsWith('/api/'),
  new StaleWhileRevalidate({
    cacheName: 'api-v1',
  })
);
