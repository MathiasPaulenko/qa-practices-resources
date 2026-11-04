import { chromium, type FullConfig } from '@playwright/test';

export default async function globalSetup(config: FullConfig) {
  const { baseURL } = config.projects[0].use;
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto(`${baseURL}/login`);
  await page.fill('[data-testid="email"]', process.env.ADMIN_EMAIL!);
  await page.fill('[data-testid="password"]', process.env.ADMIN_PASSWORD!);
  await page.click('[data-testid="login-button"]');
  await page.waitForURL('**/dashboard');
  await page.context().storageState({ path: 'playwright/.auth/admin.json' });
  await browser.close();
}
