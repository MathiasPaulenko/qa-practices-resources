// Run: npx playwright test a11y.spec.ts
// Loads the local fixture via file:// — no server needed.
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
import { fileURLToPath } from 'node:url';

const fixture = 'file://' + fileURLToPath(new URL('./fixture-modal.html', import.meta.url));

test('fixture has no critical or serious axe violations', async ({ page }) => {
  await page.goto(fixture);
  await page.getByRole('button', { name: 'Open modal' }).click();
  const results = await new AxeBuilder({ page }).include('[role="dialog"]').analyze();
  expect(results.violations.filter(v => ['critical', 'serious'].includes(v.impact))).toHaveLength(0);
});

test('modal traps focus and returns it to the trigger', async ({ page }) => {
  await page.goto(fixture);
  await page.getByRole('button', { name: 'Open modal' }).click();
  const dialog = page.getByRole('dialog');
  await expect(dialog.locator(':focus')).toHaveCount(1);

  for (let i = 0; i < 8; i++) {
    await page.keyboard.press('Tab');
    expect(await dialog.evaluate(el => el.contains(document.activeElement))).toBe(true);
  }

  await page.keyboard.press('Escape');
  await expect(page.locator(':focus')).toHaveText('Open modal');
});
