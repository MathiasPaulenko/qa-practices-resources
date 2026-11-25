describe('Network interception', () => {
  it('blocks images for faster tests', async () => {
    await page.setRequestInterception(true);

    page.on('request', (request) => {
      if (request.resourceType() === 'image') {
        request.abort();
      } else {
        request.continue();
      }
    });

    await page.goto('https://staging.myapp.com');
  });

  it('mocks API responses', async () => {
    await page.setRequestInterception(true);

    page.on('request', (request) => {
      if (request.url().includes('/api/users')) {
        request.respond({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify([{ id: 1, name: 'Jane' }]),
        });
      } else {
        request.continue();
      }
    });

    await page.goto('https://staging.myapp.com/users');
    const userName = await page.$eval('.user-name', el => el.textContent);
    expect(userName).toBe('Jane');
  });

  it('logs API calls', async () => {
    const requests = [];

    page.on('request', (request) => {
      if (request.url().includes('/api/')) {
        requests.push({
          url: request.url(),
          method: request.method(),
        });
      }
    });

    await page.goto('https://staging.myapp.com');
    expect(requests.length).toBeGreaterThan(0);
  });
});
