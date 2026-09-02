import { test, expect } from '@playwright/test';

test('login with valid credentials', async ({ page }) => {
  await page.goto('https://staging.qapractices.com/login');
  await page.fill('[data-testid="email"]', 'qa@qapractices.com');
  await page.fill('[data-testid="password"]', 'Str0ngP@ss!');
  await page.click('button[type="submit"]');
  await expect(page).toHaveURL(/\/dashboard/);
  await expect(page.locator('h1')).toContainText('Dashboard');
});

test('checkout flow with console logging', async ({ page }) => {
  page.on('console', msg => console.log(`[console] ${msg.text()}`));
  page.on('pageerror', error => console.log(`[pageerror] ${error.message}`));

  await page.goto('https://staging.qapractices.com/checkout');
  await expect(page.locator('[data-testid="pay-button"]')).toBeVisible();
});
