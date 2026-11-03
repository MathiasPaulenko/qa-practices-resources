import { test, expect } from '@playwright/test'; // Playwright 1.48

// TC002 / TC010 — invoice PDF download from billing history
test('user can download invoice PDF', async ({ page }) => {
  await page.goto('/billing/history');
  const [download] = await Promise.all([
    page.waitForEvent('download'),
    page.click('[data-testid="download-invoice"]'),
  ]);
  expect(download.suggestedFilename()).toMatch(/invoice.*\.pdf/);
});
