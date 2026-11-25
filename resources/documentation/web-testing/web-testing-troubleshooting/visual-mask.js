// Problem 4 — exclude dynamic regions from screenshot comparison (Playwright 1.65)

async function screenshotWithoutDynamicRegions(page, path) {
  await page.screenshot({
    path,
    fullPage: true,
    mask: [
      page.locator('[data-testid="ad-banner"]'),
      page.locator('[data-testid="live-timestamp"]'),
      page.locator('[data-testid="user-avatar"]'),
    ],
  });
}

module.exports = { screenshotWithoutDynamicRegions };
