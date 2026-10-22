import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  testMatch: /.*\.pw\.spec\.ts/,
  fullyParallel: true,
  workers: 4,
  timeout: 60000,
  use: {
    baseURL: 'https://staging.vitacare.io',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
  ],
  reporter: [['list'], ['html', { outputFolder: 'playwright-report' }]],
});
