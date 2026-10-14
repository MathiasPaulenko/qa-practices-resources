import { test, expect } from '@playwright/test';
import path from 'node:path';

const DEMO = 'file://' + path.resolve(__dirname, '../search-demo.html');

test.beforeEach(async ({ page }) => {
  await page.goto(DEMO);
});

// TC-01: exact keyword match is case-insensitive
test('TC-01 case-insensitive match', async ({ page }) => {
  await page.locator("[data-testid='search-input']").pressSequentially('iphone', { delay: 50 });
  await page.waitForTimeout(400);
  await expect(page.locator("[data-testid='result-item']")).toHaveCount(3);
});

// TC-07: multi-select within a facet widens results (OR)
test('TC-07 OR within facet', async ({ page }) => {
  await page.locator("[data-facet='color'][value='red']").check();
  const redOnly = await page.locator("[data-testid='result-item']").count();
  await page.locator("[data-facet='color'][value='blue']").check();
  const redOrBlue = await page.locator("[data-testid='result-item']").count();
  expect(redOrBlue).toBeGreaterThan(redOnly);
});

// TC-08: cross-facet combination narrows results (AND)
test('TC-08 AND across facets', async ({ page }) => {
  await page.locator("[data-facet='category'][value='books']").check();
  const booksOnly = await page.locator("[data-testid='result-item']").count();
  await page.locator("[data-facet='color'][value='red']").check();
  const booksAndRed = await page.locator("[data-testid='result-item']").count();
  expect(booksAndRed).toBeLessThanOrEqual(booksOnly);
  expect(booksAndRed).toBe(1); // Notebook A5
});

// TC-09: search term survives a filter change
test('TC-09 query survives filter', async ({ page }) => {
  await page.locator("[data-testid='search-input']").pressSequentially('headphone', { delay: 50 });
  await page.waitForTimeout(400);
  await page.locator("[data-testid='facet-price-max']").fill('100');
  await page.locator("[data-testid='apply-filters']").click();
  await expect(page.locator("[data-testid='search-input']")).toHaveValue('headphone');
  await expect(page.locator("[data-testid='result-item']")).toHaveCount(1); // Headphone Stand $45
});

// TC-11: debounced input sends one call per pause
test('TC-11 debounce sends one call', async ({ page }) => {
  const baseline = Number((await page.locator("[data-testid='call-count']").textContent()).replace(/\D/g, ''));
  await page.locator("[data-testid='search-input']").pressSequentially('laptop', { delay: 40 });
  await page.waitForTimeout(600);
  // 6 keystrokes in ~240ms must collapse into a single extra call
  await expect(page.locator("[data-testid='call-count']")).toHaveText(`Search calls: ${baseline + 1}`);
});

// TC-13: empty results state is actionable
test('TC-13 empty state shows guidance', async ({ page }) => {
  await page.locator("[data-testid='search-input']").pressSequentially('xzqwkj', { delay: 50 });
  await page.waitForTimeout(400);
  await expect(page.locator("[data-testid='empty-state']")).toBeVisible();
  await expect(page.locator("[data-testid='result-item']")).toHaveCount(0);
});

// TC-15: URL encodes query + filters, reload restores state
test('TC-15 URL state survives reload', async ({ page, context }) => {
  await page.locator("[data-testid='search-input']").pressSequentially('iphone', { delay: 50 });
  await page.waitForTimeout(400);
  await page.locator("[data-facet='color'][value='blue']").check();
  const firstRun = await page.locator("[data-testid='result-item']").allTextContents();
  const fresh = await context.newPage();
  await fresh.goto(page.url());
  await expect(fresh.locator("[data-testid='result-item']")).toHaveText(firstRun);
});

// TC-16: clear-all resets the result set
test('TC-16 clear all resets results', async ({ page }) => {
  await page.locator("[data-facet='color'][value='red']").check();
  await page.locator("[data-facet='category'][value='books']").check();
  await page.locator("[data-testid='clear-filters']").click();
  await expect(page.locator("[data-testid='result-item']")).toHaveCount(7);
  expect(await page.locator("[data-facet]:checked").count()).toBe(0);
});
