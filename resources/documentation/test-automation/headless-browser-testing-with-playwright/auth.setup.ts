import { test as setup } from '@playwright/test';

setup('authenticate', async ({ page }) => {
  await page.goto('https://staging.qapractices.com/login');
  await page.fill('[data-testid="email"]', 'qa@qapractices.com');
  await page.fill('[data-testid="password"]', 'Str0ngP@ss!');
  await page.click('button[type="submit"]');
  await page.waitForURL(/\/dashboard/);
  await page.context().storageState({ path: 'auth.json' });
});
