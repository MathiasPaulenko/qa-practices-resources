// Flaky (Playwright 1.48): assumes the element appears within exactly 1000ms
test('cart updates after adding product', async ({ page }) => {
  await page.goto('/cart');
  await page.click('#add-product');
  await page.waitForTimeout(1000);
  await expect(page.locator('.cart-count')).toHaveText('1');
});
