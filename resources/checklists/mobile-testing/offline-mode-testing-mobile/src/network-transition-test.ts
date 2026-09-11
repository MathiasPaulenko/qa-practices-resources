import { test, expect } from '@playwright/test';

test('shows cached timetable after going offline', async ({ page, context }) => {
  await page.goto('https://pwa.staging.local/timetable/northern');

  // Wait for the service worker to register
  await page.waitForFunction(() => navigator.serviceWorker.ready);

  // Set offline
  await context.setOffline(true);
  await page.reload();

  // The page should still show the cached schedule and an offline indicator
  await expect(page.locator('[data-testid="offline-banner"]')).toBeVisible();
  await expect(page.locator('[data-testid="schedule-list"]')).not.toBeEmpty();
});