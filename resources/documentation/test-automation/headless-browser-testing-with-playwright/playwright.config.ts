import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  workers: process.env.CI ? 4 : undefined,
  use: {
    headless: true,
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    trace: 'on-first-retry',
    bypassCSP: false,
    ignoreHTTPSErrors: false,
  },
  projects: [
    {
      name: 'setup',
      testMatch: /.*\.setup\.ts/,
    },
    {
      name: 'chromium-headless',
      dependencies: ['setup'],
      use: {
        ...devices['Desktop Chrome'],
        headless: true,
        storageState: 'auth.json',
      },
    },
    {
      name: 'firefox-headless',
      dependencies: ['setup'],
      use: {
        ...devices['Desktop Firefox'],
        headless: true,
        storageState: 'auth.json',
      },
    },
    {
      name: 'webkit-headless',
      dependencies: ['setup'],
      use: {
        ...devices['Desktop Safari'],
        headless: true,
        storageState: 'auth.json',
      },
    },
  ],
});
