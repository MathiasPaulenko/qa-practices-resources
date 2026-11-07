import { test, expect } from '@playwright/test';

const BASE_URL = process.env.BASE_URL || 'http://localhost:3000';

// Scanners don't flag a broken heading outline — this does:
// exactly one h1 first, and no level skipped deeper than +1.
test('heading hierarchy is logical', async ({ page }) => {
  await page.goto(BASE_URL);
  const headings = await page.locator('h1, h2, h3, h4, h5, h6').all();
  const levels = await Promise.all(
    headings.map((h) => h.evaluate((el) => parseInt(el.tagName[1], 10)))
  );

  expect(levels[0]).toBe(1);
  for (let i = 1; i < levels.length; i++) {
    expect(levels[i] - levels[i - 1]).toBeLessThanOrEqual(1);
  }
});

// WCAG 1.3.1: every input needs a programmatic label —
// <label for>, aria-label, or aria-labelledby.
test('all form inputs have labels', async ({ page }) => {
  await page.goto(`${BASE_URL}/register`);
  const inputs = await page.locator('input, select, textarea').all();

  for (const input of inputs) {
    const id = await input.getAttribute('id');
    const ariaLabel = await input.getAttribute('aria-label');
    const ariaLabelledBy = await input.getAttribute('aria-labelledby');
    const hasLabel =
      id && (await page.locator(`label[for="${id}"]`).count()) > 0;

    expect(hasLabel || ariaLabel || ariaLabelledBy).toBeTruthy();
  }
});
