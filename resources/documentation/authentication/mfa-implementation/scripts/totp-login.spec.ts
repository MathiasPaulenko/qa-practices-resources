import { test, expect } from '@playwright/test';
import { authenticator } from 'otplib';

// Seeded per test user in staging; never a real secret.
const SEED = process.env.TEST_TOTP_SEED ?? 'JBSWY3DPEHPK3PXP';

test('login completes the TOTP challenge', async ({ page }) => {
  await page.goto('https://staging.qapractices.com/login');
  await page.fill('#email', 'mfa-test-user@qapractices.test');
  await page.fill('#password', process.env.TEST_USER_PASSWORD ?? '');
  await page.click('button[type="submit"]');

  await page.fill('#otp-code', authenticator.generate(SEED));
  await page.click('#verify-otp');

  await expect(page).toHaveURL(/dashboard/);
});

test('rejects a replayed TOTP code', async ({ page }) => {
  const code = authenticator.generate(SEED);
  await page.goto('https://staging.qapractices.com/login/mfa');
  // First attempt succeeds.
  await page.fill('#otp-code', code);
  await page.click('#verify-otp');
  // Second attempt with the same code must fail.
  await page.goto('https://staging.qapractices.com/login/mfa');
  await page.fill('#otp-code', code);
  await page.click('#verify-otp');
  await expect(page.locator('.error')).toBeVisible();
});
