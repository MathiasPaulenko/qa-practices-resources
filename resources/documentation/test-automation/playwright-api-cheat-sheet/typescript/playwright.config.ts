// @playwright/test 1.x — playwright.config.ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  timeout: 30000,
  expect: { timeout: 5000 },
  retries: 2,
  workers: process.env.CI ? 2 : undefined,
  use: {
    baseURL: 'http://localhost:3000',
    headless: true,
    viewport: { width: 1280, height: 720 },
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    trace: 'on-first-retry',
  },
});
