// Run: npx playwright test responsive.spec.ts  (fixture via file://, no server)
import { test, expect } from '@playwright/test';
import { fileURLToPath } from 'node:url';

const fixture = 'file://' + fileURLToPath(new URL('./responsive-fixture.html', import.meta.url));

const widths = [320, 375, 767, 768, 1024, 1280];

for (const width of widths) {
  test(`TC-01/10: nav state at ${width}px`, async ({ page }) => {
    await page.setViewportSize({ width, height: 800 });
    await page.goto(fixture);
    const hamburger = page.locator('[data-testid="hamburger"]');
    const fullNav = page.locator('nav.desktop-nav');
    if (width < 768) {
      await expect(hamburger).toBeVisible();
      await expect(fullNav).toBeHidden();
    } else {
      await expect(hamburger).toBeHidden();
      await expect(fullNav).toBeVisible();
    }
  });
}

test('TC-05/06: no horizontal body scroll at 320px', async ({ page }) => {
  await page.setViewportSize({ width: 320, height: 800 });
  await page.goto(fixture);
  const bodyScrolls = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth);
  expect(bodyScrolls).toBe(false);
});
