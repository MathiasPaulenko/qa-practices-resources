// Runs on node:test (Node 18+), not Jest — msw 2.x is ESM-only and resolves
// cleanly under Node's own module system, where msw/node is designed to run.
// Same API as the guide: http + HttpResponse (the rest.* API from MSW 1.x is gone).
import { describe, it, before, after, beforeEach } from 'node:test';
import assert from 'node:assert/strict';
import { http, HttpResponse } from 'msw';
import { setupServer } from 'msw/node';

const FLAGS_URL = 'https://flags.internal/api/flags';

// The app code under test: fetch the flag service and fall back to the
// safe default (feature hidden) on any failure.
async function getPromoBannerState() {
  try {
    const res = await fetch(FLAGS_URL);
    if (!res.ok) return false;
    const data = await res.json();
    return data.promoBanner === true;
  } catch {
    return false;
  }
}

const server = setupServer(
  http.get(FLAGS_URL, () => HttpResponse.json({ promoBanner: true }))
);

before(() => server.listen());
beforeEach(() => server.resetHandlers());
after(() => server.close());

describe('flag service integration', () => {
  it('shows the banner when the flag resolves true', async () => {
    assert.equal(await getPromoBannerState(), true);
  });

  it('hides the banner when the flag resolves false', async () => {
    server.use(
      http.get(FLAGS_URL, () => HttpResponse.json({ promoBanner: false }))
    );
    assert.equal(await getPromoBannerState(), false);
  });

  it('hides the banner when the flag service returns 503', async () => {
    server.use(
      http.get(FLAGS_URL, () => new HttpResponse(null, { status: 503 }))
    );
    assert.equal(await getPromoBannerState(), false);
  });

  it('hides the banner when the flag service is unreachable', async () => {
    server.use(http.get(FLAGS_URL, () => HttpResponse.error()));
    assert.equal(await getPromoBannerState(), false);
  });
});
