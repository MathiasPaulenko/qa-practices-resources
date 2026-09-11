import { test, expect } from '@playwright/test';

test('account locks after repeated failed logins', async ({ page }) => {
  await page.goto('https://auth.staging.local/login');

  for (let i = 0; i < 5; i++) {
    await page.fill('[data-testid="username"]', 'valid-user');
    await page.fill('[data-testid="password"]', 'WrongPass123');
    await page.click('[data-testid="login-button"]');
  }

  await expect(page.locator('[data-testid="lockout-message"]')).toBeVisible();
});