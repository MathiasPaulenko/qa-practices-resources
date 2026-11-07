import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

const BASE_URL = process.env.BASE_URL || 'http://localhost:3000';

// Run only the axe rules mapped to each POUR principle, so a failure
// tells you which WCAG principle broke instead of dumping a mixed list.
const rulesByPrinciple = {
  perceivable: ['color-contrast', 'image-alt'],
  operable: ['keyboard', 'focus-order-semantics'],
  understandable: ['label'],
  robust: ['aria-roles', 'aria-required-attr'],
};

for (const [principle, rules] of Object.entries(rulesByPrinciple)) {
  test(`WCAG ${principle} checks`, async ({ page }) => {
    await page.goto(BASE_URL);
    const results = await new AxeBuilder({ page })
      .withRules(rules)
      .analyze();
    expect(results.violations).toEqual([]);
  });
}

// Full WCAG 2.2 A/AA scan for the CI gate.
test('homepage has no WCAG 2.2 A/AA violations', async ({ page }) => {
  await page.goto(BASE_URL);
  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa', 'wcag22aa'])
    .analyze();
  expect(results.violations).toEqual([]);
});
