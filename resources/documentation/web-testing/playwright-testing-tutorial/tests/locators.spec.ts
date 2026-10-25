import { test, expect } from '@playwright/test';

test('get started link navigates to the intro docs', async ({ page }) => {
  await page.goto('https://playwright.dev');

  // Role locators survive text and class changes — prefer them over CSS selectors
  await page.getByRole('link', { name: 'Get started' }).click();
  await expect(page).toHaveURL(/docs\/intro/);

  // Text locators for content, test-id for app-specific hooks
  await expect(page.getByText('Playwright Test was created')).toBeVisible();
});
