describe('Screenshots', () => {
  it('takes a full page screenshot', async () => {
    await page.goto('https://staging.myapp.com');
    await page.screenshot({
      path: 'screenshots/full-page.png',
      fullPage: true,
    });
  });

  it('takes element screenshot', async () => {
    const element = await page.$('.hero-section');
    await element.screenshot({
      path: 'screenshots/hero.png',
    });
  });

  it('takes screenshot on failure', async () => {
    try {
      await page.waitForSelector('.nonexistent', { timeout: 5000 });
    } catch (error) {
      await page.screenshot({
        path: 'screenshots/failure.png',
      });
      throw error;
    }
  });
});
