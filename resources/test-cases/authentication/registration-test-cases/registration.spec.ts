import { test, expect } from '@playwright/test';
import users from './registration-data.json';

// Runnable subset of the 30 registration test cases.
// Point BASE_URL at a staging environment — never production.
// Run: npx playwright test registration.spec.ts

const BASE = process.env.BASE_URL || 'http://localhost:3000';

test.describe('registration', () => {
  test('TC-008: valid data creates the account', async ({ page }) => {
    await page.goto(`${BASE}/register`);
    await page.fill('#email', users.valid.email);
    await page.fill('#password', users.valid.password);
    await page.fill('#confirm-password', users.valid.password);
    await page.check('#terms');
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL(/welcome/);
  });

  test('TC-013: duplicate email is rejected', async ({ page }) => {
    await page.goto(`${BASE}/register`);
    await page.fill('#email', users.duplicate.email);
    await page.fill('#password', users.valid.password);
    await page.fill('#confirm-password', users.valid.password);
    await page.click('button[type="submit"]');
    await expect(page.locator('.error')).toContainText(/already registered/i);
  });

  test('TC-014: invalid email format is rejected', async ({ page }) => {
    await page.goto(`${BASE}/register`);
    await page.fill('#email', users.invalidFormat.email);
    await page.fill('#password', users.valid.password);
    await page.fill('#confirm-password', users.valid.password);
    await page.click('button[type="submit"]');
    await expect(page.locator('.error')).toBeVisible();
  });

  test('TC-010: weak password is rejected', async ({ page }) => {
    await page.goto(`${BASE}/register`);
    await page.fill('#email', users.valid.email);
    await page.fill('#password', users.weak.password);
    await page.fill('#confirm-password', users.weak.password);
    await page.click('button[type="submit"]');
    await expect(page.locator('.error')).toContainText(/password/i);
  });

  test('TC-012: unchecked terms block submission', async ({ page }) => {
    await page.goto(`${BASE}/register`);
    await page.fill('#email', users.valid.email);
    await page.fill('#password', users.valid.password);
    await page.fill('#confirm-password', users.valid.password);
    await page.click('button[type="submit"]');
    await expect(page.locator('.error')).toBeVisible();
  });
});
