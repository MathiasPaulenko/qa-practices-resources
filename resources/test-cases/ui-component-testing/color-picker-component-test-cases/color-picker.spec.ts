import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test.describe('color picker component', () => {
  test.beforeEach(async ({ page, context }) => {
    await context.grantPermissions(['clipboard-read', 'clipboard-write']);
    await page.goto('/editor/palette');
    await page.getByTestId('color-picker-trigger').click();
  });

  test('hex input updates preview and emitted value', async ({ page }) => {
    await page.getByTestId('hex-input').fill('#FF5733');
    await page.getByTestId('hex-input').press('Enter');
    await expect(page.getByTestId('color-preview')).toHaveAttribute('data-color', '#FF5733');
  });

  test('invalid hex keeps the previous color', async ({ page }) => {
    await page.getByTestId('hex-input').fill('#GGGGGG');
    await page.getByTestId('hex-input').press('Enter');
    await expect(page.getByTestId('hex-error')).toBeVisible();
    await expect(page.getByTestId('color-preview')).not.toHaveAttribute('data-color', '#GGGGGG');
  });

  test('copy button writes hex to clipboard', async ({ page }) => {
    await page.getByTestId('hex-input').fill('#FF5733');
    await page.getByTestId('hex-input').press('Enter');
    await page.getByTestId('copy-color').click();
    const clip = await page.evaluate(() => navigator.clipboard.readText());
    expect(clip).toBe('#FF5733');
  });

  test('open picker has no serious axe violations', async ({ page }) => {
    const results = await new AxeBuilder({ page })
      .include('[data-testid="color-picker"]')
      .analyze();
    expect(results.violations.filter(v => v.impact === 'critical' || v.impact === 'serious')).toEqual([]);
  });
});
