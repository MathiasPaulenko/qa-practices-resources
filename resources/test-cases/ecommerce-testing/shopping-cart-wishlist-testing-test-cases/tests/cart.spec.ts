// tests/cart.spec.ts
// Requires: Playwright 1.48, Node.js 20+
import { test, expect } from '@playwright/test';

const BASE_URL = 'https://staging.qa.local';

test('TC-01: add item to cart and verify total', async ({ page }) => {
  await page.goto(`${BASE_URL}/products/SKU-12345`);
  await page.getByTestId('add-to-cart').click();
  await page.goto(`${BASE_URL}/cart`);

  const subtotal = await page.locator('[data-testid="cart-subtotal"]').textContent();
  expect(subtotal).toBe('$29.99');
  await expect(page.locator('[data-testid="cart-badge"]')).toHaveText('1');
});

test('TC-02: remove item from cart', async ({ page }) => {
  await page.goto(`${BASE_URL}/products/SKU-12345`);
  await page.getByTestId('add-to-cart').click();
  await page.goto(`${BASE_URL}/cart`);
  await page.getByTestId('remove-item').click();

  await expect(page.locator('[data-testid="empty-cart"]')).toBeVisible();
});

test('TC-03: update quantity and verify subtotal', async ({ page }) => {
  await page.goto(`${BASE_URL}/products/SKU-12345`);
  await page.getByTestId('add-to-cart').click();
  await page.goto(`${BASE_URL}/cart`);

  for (const [qty, expected] of [['2', '$40.00'], ['3', '$60.00'], ['1', '$20.00']]) {
    await page.getByTestId('quantity-input').fill(qty);
    const subtotal = await page.locator('[data-testid="cart-subtotal"]').textContent();
    expect(subtotal).toBe(expected);
  }
});

test('TC-05: cart persists across logout and login', async ({ page }) => {
  await page.goto(`${BASE_URL}/products/SKU-12345`);
  await page.getByTestId('add-to-cart').click();
  await page.getByTestId('quantity-input').fill('2');

  await page.getByTestId('logout').click();
  await page.getByTestId('login').click();
  await page.goto(`${BASE_URL}/cart`);

  const items = await page.locator('[data-testid="cart-item"]').count();
  expect(items).toBe(1);
  const qty = await page.getByTestId('quantity-input').inputValue();
  expect(qty).toBe('2');
});
