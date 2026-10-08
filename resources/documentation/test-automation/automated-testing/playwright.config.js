import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  timeout: 30000,
  retries: process.env.CI ? 1 : 0,
  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:4200',
    testIdAttribute: 'data-testid'
  },
  projects: [
    { name: 'chromium', use: { browserName: 'chromium' } }
  ]
});
