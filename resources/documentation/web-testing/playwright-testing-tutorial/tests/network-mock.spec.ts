import { test, expect } from '@playwright/test';

test('mock an API response with page.route', async ({ page }) => {
  // Intercept before navigation — routes registered after goto() miss early requests
  await page.route('**/api/user', async (route) => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ name: 'Test User', plan: 'free' }),
    });
  });

  await page.goto('https://playwright.dev');
  // Your assertion against the stubbed payload goes here
});
