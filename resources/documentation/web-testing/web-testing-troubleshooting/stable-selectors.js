// Problem 2 — browser-agnostic selectors that survive rendering differences

// Bad: pseudo-class with uneven browser support
// await page.click('article:has(h2)');

// Good: stable test attribute added to the markup
async function openFeaturedArticle(page) {
  await page.click('[data-testid="featured-article"]');
}

module.exports = { openFeaturedArticle };
