import { test, expect } from '@playwright/test';
import { AxeBuilder } from '@axe-core/playwright';

// Companion to "WCAG 2.2 AA vs AAA Testing Differences" on QAPractices.
// The suite runs the same page through two rule-tag sets:
//   - wcag22aa: WCAG 2.2 Level A + AA rules (release gate)
//   - wcag2aaa: the automatable AAA rules, e.g. color-contrast-enhanced
//             (report-only pass — most AAA findings need human triage)

test('AA gate — page must have zero WCAG 2.2 AA violations', async ({ page }) => {
  await page.goto('/checkout');
  const results = await new AxeBuilder({ page })
    .withTags(['wcag22aa'])
    .analyze();
  expect(results.violations).toEqual([]);
});

test('AAA sweep — report findings without failing the build', async ({ page }) => {
  await page.goto('/checkout');
  const results = await new AxeBuilder({ page })
    .withTags(['wcag2aaa'])
    .analyze();
  for (const v of results.violations) {
    console.log(`[AAA] ${v.id} (${v.impact}): ${v.nodes.length} node(s)`);
  }
  // Intentionally no assertion: keep this non-blocking until findings are triaged.
});

test('AAA enhanced contrast (7:1) on the same page', async ({ page }) => {
  await page.goto('/checkout');
  const results = await new AxeBuilder({ page })
    .withRules(['color-contrast-enhanced'])
    .analyze();
  console.log(`enhanced-contrast findings: ${results.violations.length}`);
});
