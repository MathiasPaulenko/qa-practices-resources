// Problem 3 — CI-specific overrides for playwright.config.ts (Playwright 1.65)
// Merge these settings into your CI project to account for slower runners.

export const ciProject = {
  name: 'chromium-ci',
  timeout: 60000, // 60s in CI vs 30s locally
  retries: 2,
  use: {
    viewport: { width: 1280, height: 720 },
    launchOptions: {
      args: ['--disable-gpu', '--no-sandbox'],
    },
  },
};
