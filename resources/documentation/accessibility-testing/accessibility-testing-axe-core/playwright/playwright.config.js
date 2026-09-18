// Uses the locally installed Chrome (channel: 'chrome') so the suite runs
// without `npx playwright install`. For CI, drop the channel option and let
// Playwright use its bundled chromium.
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  use: { channel: 'chrome' },
});
