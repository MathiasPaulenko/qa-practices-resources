// Fixture service worker for the Playwright spec in the article.
// Implements the handlers every TC assumes: install precache, activate
// cache purge, push -> showNotification (inside waitUntil),
// notificationclick routing, notificationclose analytics beacon.

const CACHE_NAME = 'shell-v1';
const SHELL = ['/', '/index.html', '/app.css', '/app.js', '/offline.html'];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(SHELL))
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((names) => Promise.all(
        names.filter((n) => n !== CACHE_NAME).map((n) => caches.delete(n))
      ))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  if (event.request.mode === 'navigate') {
    event.respondWith(
      fetch(event.request).catch(() =>
        caches.match('/offline.html').then((res) => res || caches.match('/index.html'))
      )
    );
    return;
  }
  event.respondWith(caches.match(event.request).then((res) => res || fetch(event.request)));
});

self.addEventListener('push', (event) => {
  let data = {};
  try {
    data = event.data ? event.data.json() : {};
  } catch (_err) {
    data = {};
  }
  event.waitUntil(
    self.registration.showNotification(data.title || 'New update', {
      body: data.body || '',
      icon: '/icon-192.png',
      badge: '/badge-72.png',
      data: { url: data.url || '/' },
      actions: data.actions || [],
    })
  );
});

self.addEventListener('notificationclick', (event) => {
  event.notification.close();
  if (event.action === 'dismiss') return;
  const url = event.notification.data?.url || '/';
  event.waitUntil(
    self.clients.matchAll({ type: 'window', includeUncontrolled: true }).then((list) => {
      const client = list.find((c) => c.url.includes(url) && 'focus' in c);
      if (client) return client.focus();
      return self.clients.openWindow(url);
    })
  );
});

self.addEventListener('notificationclose', (event) => {
  event.waitUntil(fetch('/analytics', {
    method: 'POST',
    body: JSON.stringify({ event: 'notificationclose', tag: event.notification.tag }),
  }));
});
