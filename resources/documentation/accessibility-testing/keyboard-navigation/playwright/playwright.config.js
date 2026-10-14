import { defineConfig } from '@playwright/test';

// Uses your installed Chrome — no browser download required.
// For CI, remove `channel` and run `npx playwright install chromium`.
export default defineConfig({
  testDir: './tests',
  retries: 0,
  use: {
    channel: 'chrome',
    headless: true
  }
});
