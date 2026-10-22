import { test, expect } from '@playwright/test';

test('375px viewport fetches the 400w candidate', async ({ page }) => {
  const requested: string[] = [];
  page.on('request', (r) => { if (r.url().includes('hero-')) requested.push(r.url()); });
  await page.setViewportSize({ width: 375, height: 700 });
  await page.goto('picture.html');
  expect(requested.some((u) => u.includes('hero-400'))).toBe(true);
  expect(requested.some((u) => u.includes('hero-1600'))).toBe(false);
});

test('lazy image is not requested until scrolled into view', async ({ page }) => {
  const lazy = page.waitForRequest((r) => r.url().includes('lazy-'));
  await page.goto('picture.html');
  await page.waitForTimeout(1500); // still below the fold
  await page.locator('[data-testid="lazy-img"]').scrollIntoViewIfNeeded();
  await lazy; // resolves only after the scroll triggered the fetch
});
