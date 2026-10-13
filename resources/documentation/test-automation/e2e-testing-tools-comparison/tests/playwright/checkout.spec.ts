import { test, expect } from '@playwright/test';

// Playwright 1.48 — checkout flow smoke test
// Run: npx playwright test tests/playwright/checkout.spec.ts

test('completes checkout', async ({ page }) => {
  await page.goto('https://staging.lumapay.com/checkout');
  await page.getByRole('button', { name: 'Pay now' }).click();
  await expect(page.getByText('Payment confirmed')).toBeVisible();
});

test('handles declined payment gracefully', async ({ page }) => {
  await page.goto('https://staging.lumapay.com/checkout');
  await page.route('**/api/v1/payments', route =>
    route.fulfill({ status: 402, json: { error: 'card_declined' } })
  );
  await page.getByRole('button', { name: 'Pay now' }).click();
  await expect(page.getByText('Payment failed')).toBeVisible();
});
