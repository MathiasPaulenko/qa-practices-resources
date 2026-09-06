import { test, expect } from '@playwright/test';

test('checkout summary looks correct', async ({ page }) => {
  await page.goto('/checkout');

  await page.route('/api/cart', route => {
    route.fulfill({ json: { itemCount: 3, total: 149.99 } });
  });

  await page.waitForLoadState('networkidle');

  await expect(page.locator('.checkout-summary')).toHaveScreenshot('checkout-summary.png', {
    mask: [page.locator('.cart-count')],
  });
});
