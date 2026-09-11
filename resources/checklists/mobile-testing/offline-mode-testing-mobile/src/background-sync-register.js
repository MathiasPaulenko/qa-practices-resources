async function queueDelayReport(report) {
  await saveToIndexedDB(report);

  const registration = await navigator.serviceWorker.ready;
  await registration.sync.register('sync-delay-reports');
}