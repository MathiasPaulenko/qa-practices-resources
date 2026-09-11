import { Workbox } from 'workbox-window';

const wb = new Workbox('/service-worker.js');

wb.addEventListener('waiting', () => {
  if (confirm('A new version is available. Reload?')) {
    wb.messageSW({ type: 'SKIP_WAITING' });
    window.location.reload();
  }
});

wb.register();