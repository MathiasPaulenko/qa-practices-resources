// Reliable (Playwright 1.48): waits for the expected condition instead of a fixed duration
test('cart updates after adding product', async ({ page }) => {
  await page.goto('/cart');
  await page.click('#add-product');
  await expect(page.locator('.cart-count')).toHaveText('1', { timeout: 5000 });
});
