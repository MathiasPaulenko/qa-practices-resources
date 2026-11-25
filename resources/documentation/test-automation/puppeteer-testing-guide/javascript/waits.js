describe('Wait strategies', () => {
  it('waits for selector', async () => {
    await page.goto('https://staging.myapp.com');
    await page.waitForSelector('.dynamic-content', { timeout: 10000 });
  });

  it('waits for navigation', async () => {
    await Promise.all([
      page.waitForNavigation(),
      page.click('a[href="/about"]'),
    ]);
    expect(page.url()).toContain('/about');
  });

  it('waits for network idle', async () => {
    await page.goto('https://staging.myapp.com', {
      waitUntil: 'networkidle0',
    });
  });

  it('waits for custom condition', async () => {
    await page.waitForFunction(
      () => document.querySelector('#status').textContent === 'Complete',
      { timeout: 15000 }
    );
  });

  it('waits for a fixed delay', async () => {
    // page.waitForTimeout was removed in Puppeteer 22 — use a plain promise
    await new Promise(resolve => setTimeout(resolve, 2000));
  });
});
