const puppeteer = require('puppeteer');

describe('Login Page', () => {
  let browser;
  let page;

  beforeAll(async () => {
    browser = await puppeteer.launch({ headless: true });
    page = await browser.newPage();
  });

  afterAll(async () => {
    await browser.close();
  });

  it('should login with valid credentials', async () => {
    await page.goto('https://staging.myapp.com/login');

    await page.type('#email', 'jane@staging.myapp.com');
    await page.type('#password', 'validpass123');
    await page.click('button[type="submit"]');

    await page.waitForSelector('h1');
    const headingText = await page.$eval('h1', el => el.textContent);
    expect(headingText).toBe('Dashboard');
  });

  it('should show error on invalid credentials', async () => {
    await page.goto('https://staging.myapp.com/login');

    await page.type('#email', 'jane@staging.myapp.com');
    await page.type('#password', 'wrongpass');
    await page.click('button[type="submit"]');

    await page.waitForSelector('.error-message');
    const errorText = await page.$eval('.error-message', el => el.textContent);
    expect(errorText).toBe('Invalid credentials');
  });
});
