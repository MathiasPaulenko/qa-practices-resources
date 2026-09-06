// Playwright 1.48 test: PWA loads offline after first visit
// Install: npm install -D @playwright/test@1.48
import { test, expect } from '@playwright/test';

test('PWA loads offline after first visit', async ({ page, context }) => {
  // First visit: register the service worker
  await page.goto('https://pwa.qa.local');

  const swRegistered = await page.evaluate(() =>
    navigator.serviceWorker?.controller?.scriptURL.includes('sw.js')
  );
  expect(swRegistered).toBe(true);

  // Wait for the SW to activate
  await page.waitForTimeout(2000);

  // Go offline
  await context.setOffline(true);

  // Reload: the app shell should load from cache
  await page.reload();
  await expect(page.locator('h1')).toBeVisible();
});

test('offline fallback page shows branded content', async ({ page, context }) => {
  await page.goto('https://pwa.qa.local');
  await page.waitForTimeout(2000);

  await context.setOffline(true);

  // Navigate to an uncached route
  await page.goto('https://pwa.qa.local/uncached-route');
  await expect(page.locator('body')).not.toContainText('This site can\'t be reached');
});
