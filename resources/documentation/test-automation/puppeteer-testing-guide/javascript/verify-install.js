const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  // Placeholder: replace with your staging URL
  await page.goto('https://staging.myapp.com');
  console.log(await page.title());
  await browser.close();
})();
