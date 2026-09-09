// checkout.spec.js
// End-to-end test for guest checkout — Test Pyramid layer: E2E
// Run with: npx playwright test src/checkout.spec.js
// Requires: app running at http://localhost:3000

import { test, expect } from '@playwright/test';

test('guest can complete checkout', async ({ page }) => {
  await page.goto('http://localhost:3000/products');
  await page.locator('[data-testid="add-to-cart"]').first().click();
  await page.locator('[data-testid="checkout"]').click();
  await page.fill('[data-testid="email"]', 'qa@qapractices.com');
  await page.fill('[data-testid="card"]', '4242424242424242');
  await page.locator('[data-testid="place-order"]').click();
  await expect(page.locator('[data-testid="confirmation"]'))
    .toContainText('Order confirmed');
});
