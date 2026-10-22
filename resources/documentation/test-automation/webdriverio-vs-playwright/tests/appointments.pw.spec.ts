import { test, expect } from '@playwright/test';

test('patient can book a telehealth slot', async ({ page }) => {
  await page.route('**/v1/payments/authorize', async route => {
    await route.fulfill({
      status: 200,
      body: JSON.stringify({ authorized: true, transactionId: 'mock-123' })
    });
  });

  await page.goto('/login');
  await page.locator('#email').fill('qa-patient@vitacare.io'); // seeded test account
  await page.locator('#password').fill(process.env.E2E_PASSWORD ?? 'local-dev-password');
  await page.locator('button[type=submit]').click();

  await page.goto('/appointments');
  const slots = page.locator('.time-slot');
  await slots.nth(2).click();

  await page.locator('button#confirm-booking').click();
  await expect(page.locator('.booking-confirmation'))
    .toContainText('Your appointment is confirmed');
});
