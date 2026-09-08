// tests/e2e/auth/login.spec.ts
import { test, expect } from '@playwright/test';
import { LoginPage } from '../../../pages/LoginPage';

test('registered user logs in and reaches dashboard', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.open();
  await loginPage.login('ana@qa.local', 'ValidPass1');
  await expect(page).toHaveURL(/.*\/dashboard$/);
});

test('failed login shows error message', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.open();
  await loginPage.login('ana@qa.local', 'wrongpassword');
  const error = await loginPage.getErrorMessage();
  expect(error).toContain('Invalid email or password');
});
