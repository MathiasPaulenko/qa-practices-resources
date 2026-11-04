import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  use: {
    // Runs your installed Chrome — no browser download needed.
    // For CI, remove `channel` and run `npx playwright install chromium`.
    channel: 'chrome',
    baseURL: process.env.BASE_URL || 'https://staging.qapractices.com'
  }
});
