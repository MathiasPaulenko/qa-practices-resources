import { test, expect } from '@playwright/test';

test('primary button', async ({ page }) => {
  await page.goto('/storybook?path=/story/button--primary');
  await expect(page.locator('[data-testid="primary-button"]')).toHaveScreenshot('primary-button.png');
});
