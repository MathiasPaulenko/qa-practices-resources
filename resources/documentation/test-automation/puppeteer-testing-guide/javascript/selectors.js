describe('Selectors', () => {
  it('uses CSS selectors', async () => {
    const button = await page.$('.submit-button');
    const input = await page.$('#email-field');
    const nested = await page.$('.form .input-group input');
  });

  it('uses XPath selectors', async () => {
    // Puppeteer 22+ removed page.$x — use locator with an XPath prefix
    const element = await page.locator('::-p-xpath(//button[contains(text(), "Submit")])').wait();
  });

  it('uses text selectors', async () => {
    // ::-p-text matches element text without writing XPath
    const button = await page.locator('::-p-text(Submit)').wait();
  });

  it('queries multiple elements', async () => {
    const buttons = await page.$$('button');
    expect(buttons.length).toBeGreaterThan(0);
  });

  it('uses page.evaluate for custom queries', async () => {
    const data = await page.evaluate(() => {
      const elements = document.querySelectorAll('.item');
      return Array.from(elements).map(el => el.textContent);
    });
    expect(data).toContain('Expected text');
  });
});
