import { test, expect } from '@playwright/test';

test('age field rejects below minimum, accepts boundary', async ({ page }) => {
  await page.goto('login-form.html');
  await page.fill('[data-testid="age"]', '17');
  await page.click('[data-testid="save"]');
  await expect(page.locator('[data-testid="age-error"]')).toContainText('must be at least 18');

  await page.fill('[data-testid="age"]', '18');
  await page.click('[data-testid="save"]');
  await expect(page.locator('[data-testid="age-error"]')).not.toBeVisible();
});

test('user logs in with valid credentials', async ({ page }) => {
  await page.goto('login-form.html');
  await page.fill('[data-testid="email"]', process.env.TEST_USER_EMAIL!);
  await page.fill('[data-testid="password"]', process.env.TEST_USER_PASSWORD!);
  await page.click('[data-testid="login-button"]');
  await expect(page).toHaveURL(/dashboard/);
});
