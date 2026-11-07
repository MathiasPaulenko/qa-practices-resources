import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

const BASE_URL = process.env.BASE_URL || 'http://localhost:3000';

test.describe('accessibility scans — @axe-core/playwright 4.10', () => {
  test('full-page scan reports zero violations', async ({ page }) => {
    await page.goto(BASE_URL);
    const results = await new AxeBuilder({ page }).analyze();
    expect(results.violations).toEqual([]);
  });

  test('scoped scan excludes third-party widgets', async ({ page }) => {
    await page.goto(BASE_URL);
    const results = await new AxeBuilder({ page })
      .include('#app-root')
      .exclude('#third-party-chat-widget')
      .withTags(['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag22aa'])
      .analyze();
    expect(results.violations).toEqual([]);
  });

  test('color contrast meets WCAG AA', async ({ page }) => {
    await page.goto(BASE_URL);
    const results = await new AxeBuilder({ page })
      .withRules(['color-contrast'])
      .analyze();
    expect(results.violations).toEqual([]);
  });
});
