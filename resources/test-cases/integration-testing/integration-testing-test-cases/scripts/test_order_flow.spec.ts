// TC-009 — E2E order flow: assert inventory state on both sides of the seam.
import { test, expect } from '@playwright/test';

test('order decrements inventory and notifies', async ({ page, request }) => {
  const before = await (await request.get('/api/inventory/123')).json();
  await page.goto('/shop/item/123');
  await page.click('[data-testid="buy-button"]');
  await expect(page.locator('[data-testid="success-message"]')).toBeVisible();
  const after = await (await request.get('/api/inventory/123')).json();
  expect(after.quantity).toBe(before.quantity - 1);
});
