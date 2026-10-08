import { test, expect } from '@playwright/test';

test('send invoice and generate PDF', async ({ page }) => {
  await page.goto('/invoices/new');
  await page.fill('[data-testid="customer-search"]', 'Acme Corp');
  await page.click('[data-testid="customer-acme-corp"]');
  await page.fill('[data-testid="line-item-amount"]', '1000');
  await page.selectOption('[data-testid="tax-rate"]', '21');
  await page.click('[data-testid="save-and-send"]');
  await expect(page.locator('[data-testid="pdf-preview"]'))
    .toBeVisible({ timeout: 15000 });
});
