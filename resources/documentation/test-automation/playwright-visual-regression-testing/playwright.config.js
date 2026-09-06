// playwright.config.js
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  use: {
    baseURL: 'https://staging.qa.local',
  },
  snapshotPathTemplate: '{testDir}/__screenshots__/{testFilePath}/{arg}{ext}',
  expect: {
    toHaveScreenshot: {
      maxDiffPixels: 100,
      threshold: 0.2,
      animations: 'disabled',
    },
  },
  projects: [
    {
      name: 'visual-mobile',
      use: { viewport: { width: 375, height: 667 } },
    },
    {
      name: 'visual-tablet',
      use: { viewport: { width: 768, height: 1024 } },
    },
    {
      name: 'visual-desktop',
      use: { viewport: { width: 1920, height: 1080 } },
    },
  ],
});
