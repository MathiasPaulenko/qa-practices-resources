import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

// Self-contained fixtures — no external site required.
const ACCESSIBLE_PAGE = `
  <html lang="en">
    <head><title>Login — QA App</title></head>
    <body>
      <main>
        <h1>Login</h1>
        <form>
          <label for="email">Email</label>
          <input id="email" type="email">
          <button type="submit">Sign in</button>
        </form>
      </main>
    </body>
  </html>
`;

const PAGE_WITH_VIOLATIONS = `
  <html>
    <head><title>Broken page</title></head>
    <body>
      <div>
        <h3>Welcome</h3>
        <img src="logo.png">
        <input type="text" placeholder="Search">
        <p style="color: #aaa; background: #fff">Low contrast text</p>
      </div>
    </body>
  </html>
`;

test('accessible page has no WCAG violations', async ({ page }) => {
  await page.setContent(ACCESSIBLE_PAGE);

  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
    .analyze();

  expect(results.violations).toEqual([]);
});

test('broken page reports violations with rule ids and targets', async ({ page }) => {
  await page.setContent(PAGE_WITH_VIOLATIONS);

  // wcag2a included: image-alt is a Level A rule and would be
  // filtered out by a wcag2aa-only tag set
  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa'])
    .analyze();

  expect(results.violations.length).toBeGreaterThan(0);

  const ruleIds = results.violations.map(v => v.id);
  expect(ruleIds).toContain('image-alt');
  expect(ruleIds).toContain('color-contrast');

  // Each violation points at the exact DOM node that failed
  const imageAlt = results.violations.find(v => v.id === 'image-alt');
  expect(imageAlt.nodes[0].target[0]).toBe('img');
});

test('impact filtering: gate on critical and serious only', async ({ page }) => {
  await page.setContent(PAGE_WITH_VIOLATIONS);

  const results = await new AxeBuilder({ page })
    .withTags(['wcag2aa'])
    .analyze();

  const blockers = results.violations.filter(
    v => v.impact === 'critical' || v.impact === 'serious'
  );
  expect(blockers.length).toBeGreaterThan(0);
});

test('scoped scan with include() checks a single component', async ({ page }) => {
  await page.setContent(ACCESSIBLE_PAGE);

  const results = await new AxeBuilder({ page })
    .include('form')
    .withTags(['wcag2aa'])
    .analyze();

  expect(results.violations).toEqual([]);
});
