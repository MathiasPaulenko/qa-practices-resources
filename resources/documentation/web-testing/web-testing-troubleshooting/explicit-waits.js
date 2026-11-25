// Problem 1 — replace fixed sleeps with condition-based waits (Playwright 1.65)

// Bad: fixed sleep — flaky because the element may appear earlier or later
// await page.waitForTimeout(3000);
// await page.click('#submit');

// Good: wait for the element to actually be ready
async function submitForm(page) {
  await page.waitForSelector('#submit', { state: 'visible' });
  await page.click('#submit');
}

module.exports = { submitForm };
