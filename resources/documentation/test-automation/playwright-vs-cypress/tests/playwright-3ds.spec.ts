import { test, expect } from '@playwright/test';

test('completes 3DS challenge for Adyen', async ({ page }) => {
  await page.goto('/checkout');
  await page.getByTestId('card-number').fill('4111 1111 1111 1111');
  await page.getByTestId('pay-button').click();

  const challenge = page.frameLocator('iframe[name=threeds-challenge]');
  await challenge.getByLabel('Password').fill('password');
  await challenge.getByRole('button', { name: 'Submit' }).click();

  await expect(page.getByText('Payment successful')).toBeVisible();
});