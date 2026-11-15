import { test, expect } from '@playwright/test';

// Rate-limit verification on the login endpoint.
// Point BASE_URL at a staging environment — never run this against production.

const BASE_URL = process.env.BASE_URL ?? 'https://staging.qapractices.com';

test('locks account after five failed attempts', async ({ page }) => {
  await page.goto(`${BASE_URL}/login`);
  for (let i = 0; i < 5; i++) {
    await page.fill('[name="email"]', 'qa-tester@qapractices.com');
    await page.fill('[name="password"]', 'wrong-password');
    await page.click('button[type="submit"]');
  }
  await expect(page.locator('text=Too many attempts')).toBeVisible();
});

test('shows a generic error that does not reveal account existence', async ({ page }) => {
  await page.goto(`${BASE_URL}/login`);
  await page.fill('[name="email"]', 'not-a-user@qapractices.com');
  await page.fill('[name="password"]', 'wrong-password');
  await page.click('button[type="submit"]');
  // The message must not say "user not found" vs "wrong password".
  await expect(page.locator('text=Invalid credentials')).toBeVisible();
});
