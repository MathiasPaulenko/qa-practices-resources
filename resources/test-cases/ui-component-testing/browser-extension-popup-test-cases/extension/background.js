chrome.runtime.onMessage.addListener((message, _sender, sendResponse) => {
  if (message.type === 'SAVE') {
    // MV3: keep the response synchronous or return true; the popup times out
    // if sendResponse is never called.
    sendResponse({ ok: true });
    return true;
  }
  if (message.type === 'ENRICH') {
    sendResponse({ ok: true, enriched: true });
    return true;
  }
  return false;
});
