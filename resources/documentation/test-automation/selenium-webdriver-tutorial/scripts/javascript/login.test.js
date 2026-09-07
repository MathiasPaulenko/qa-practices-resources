const { Builder, By, until } = require('selenium-webdriver');
const assert = require('assert');

describe('Login', () => {
  let driver;

  beforeEach(async () => {
    driver = await new Builder().forBrowser('chrome').build();
    await driver.manage().window().maximize();
  });

  afterEach(async () => {
    await driver.quit();
  });

  it('logs in successfully', async () => {
    await driver.get('https://staging.qa.local/login');
    await driver.findElement(By.id('email')).sendKeys('jane@qa.local');
    await driver.findElement(By.id('password')).sendKeys('validpass123');
    await driver.findElement(By.css("[data-testid='login-button']")).click();

    await driver.wait(until.urlContains('/dashboard'), 5000);
    const currentUrl = await driver.getCurrentUrl();
    assert.ok(currentUrl.includes('/dashboard'));

    const welcome = await driver.findElement(By.xpath("//h1[contains(text(), 'Welcome')]"));
    assert.ok(await welcome.isDisplayed());
  });
});
