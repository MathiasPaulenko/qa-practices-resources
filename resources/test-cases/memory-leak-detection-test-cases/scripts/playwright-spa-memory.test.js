const { test, expect } = require('@playwright/test');

// SPA detached DOM node test
// Usage: npx playwright test playwright-spa-memory.test.js

test('should not retain detached DOM nodes after route transitions', async ({ page }) => {
  await page.goto('http://localhost:4200/list');

  const getDetachedNodes = () => page.evaluate(() => {
    // Use Chrome DevTools protocol or a simplified counter
    // In a real project, connect to the CDP Memory domain
    return performance.memory ? performance.memory.usedJSHeapSize : 0;
  });

  const baseline = await getDetachedNodes();

  for (let i = 0; i < 50; i++) {
    await page.click('[data-testid="go-to-detail"]');
    await page.waitForSelector('[data-testid="detail-page"]');
    await page.click('[data-testid="go-to-list"]');
    await page.waitForSelector('[data-testid="list-page"]');
  }

  // Force GC is not directly available in Playwright, but this test documents the intended flow
  const final = await getDetachedNodes();
  const growth = final - baseline;
  console.log(`Heap growth (bytes): ${growth}`);

  // Tolerance depends on the app; this example uses 10%
  expect(growth).toBeLessThan(baseline * 0.1);
});
