import { test, expect } from './fixtures/base.fixture';

test.use({ storageState: 'playwright/.auth/admin.json' });

test('dashboard loads already authenticated', async ({ page }) => {
  await page.goto('/dashboard');
  await expect(page.locator('[data-testid="user-menu"]')).toBeVisible();
});
