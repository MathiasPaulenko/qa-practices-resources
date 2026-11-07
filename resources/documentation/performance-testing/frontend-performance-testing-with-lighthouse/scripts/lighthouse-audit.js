// Run Lighthouse 12 against a URL through Puppeteer 24 and print the category scores.
// Usage: node lighthouse-audit.js https://staging.example.com
const lighthouse = require('lighthouse');
const puppeteer = require('puppeteer');

const url = process.argv[2];
if (!url) {
  console.error('Usage: node lighthouse-audit.js <url>');
  process.exit(1);
}

(async () => {
  const browser = await puppeteer.launch();
  const { port } = new URL(browser.wsEndpoint());
  const result = await lighthouse(url, {
    port,
    output: 'json',
    onlyCategories: ['performance'],
    formFactor: 'mobile',
    screenEmulation: { mobile: true },
  });
  const lhr = result.lhr;
  console.log(`Performance: ${(lhr.categories.performance.score * 100).toFixed(0)}/100`);
  for (const id of ['largest-contentful-paint', 'total-blocking-time', 'cumulative-layout-shift', 'first-contentful-paint', 'speed-index']) {
    const audit = lhr.audits[id];
    console.log(`  ${id}: ${audit.displayValue || audit.numericValue}`);
  }
  await browser.close();
})();
