// tests/wishlist.spec.ts
// Requires: Playwright 1.48, Node.js 20+
import { test, expect } from '@playwright/test';

const BASE_URL = 'https://staging.qa.local';

test('TC-06: add item to wishlist', async ({ page }) => {
  await page.goto(`${BASE_URL}/products/SKU-67890`);
  await page.getByTestId('wishlist-heart').click();
  await page.goto(`${BASE_URL}/wishlist`);

  await expect(page.locator('[data-testid="wishlist-item"]')).toHaveCount(1);
  const counter = await page.getByTestId('wishlist-counter').textContent();
  expect(counter).toBe('1');
});

test('TC-07: move wishlist item to cart', async ({ page }) => {
  await page.goto(`${BASE_URL}/products/SKU-67890`);
  await page.getByTestId('wishlist-heart').click();
  await page.goto(`${BASE_URL}/wishlist`);
  await page.getByTestId('add-to-cart').click();

  await expect(page.locator('[data-testid="cart-badge"]')).toHaveText('1');
});

test('TC-08: out-of-stock item cannot move from wishlist to cart', async ({ page }) => {
  // Precondition: SKU-OUTOFSTOCK has 0 units in stock
  await page.goto(`${BASE_URL}/products/SKU-OUTOFSTOCK`);
  await page.getByTestId('wishlist-heart').click();
  await page.goto(`${BASE_URL}/wishlist`);
  await page.getByTestId('add-to-cart').click();

  await expect(page.getByText('Out of stock')).toBeVisible();
  await expect(page.locator('[data-testid="cart-badge"]')).toHaveText('0');
});
