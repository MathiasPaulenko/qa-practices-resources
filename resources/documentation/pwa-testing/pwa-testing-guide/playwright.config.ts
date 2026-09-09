import { defineConfig } from '@playwright/test'

export default defineConfig({
  testDir: './tests',
  timeout: 30000,
  use: {
    browserName: 'chromium',
    serviceWorkers: 'allow',
    baseURL: 'http://localhost:4173',
  },
  projects: [
    {
      name: 'pwa-chromium',
      use: { channel: 'chrome' },
    },
  ],
})
