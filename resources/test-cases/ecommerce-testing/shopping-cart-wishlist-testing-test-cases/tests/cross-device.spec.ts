// tests/cross-device.spec.ts
// Requires: Playwright 1.48, Node.js 20+
import { test, expect, chromium, devices } from '@playwright/test';

const BASE_URL = 'https://staging.qa.local';

test('TC-10: cart syncs across desktop and mobile', async () => {
  // Desktop browser
  const desktop = await chromium.launch();
  const desktopCtx = await desktop.newContext();
  const desktopPage = await desktopCtx.newPage();

  // Mobile browser (emulated)
  const mobile = await chromium.launch();
  const mobileCtx = await mobile.newContext({ ...devices['iPhone 14'] });
  const mobilePage = await mobileCtx.newPage();

  // Login on both
  for (const page of [desktopPage, mobilePage]) {
    await page.goto(`${BASE_URL}/login`);
    await page.getByTestId('email').fill('user@qa.local');
    await page.getByTestId('password').fill('test-password');
    await page.getByTestId('submit').click();
  }

  // Add item on desktop
  await desktopPage.goto(`${BASE_URL}/products/SKU-12345`);
  await desktopPage.getByTestId('add-to-cart').click();

  // Refresh mobile cart
  await mobilePage.goto(`${BASE_URL}/cart`);
  await mobilePage.reload();

  const mobileItems = await mobilePage.locator('[data-testid="cart-item"]').count();
  expect(mobileItems).toBe(1);

  await desktop.close();
  await mobile.close();
});
