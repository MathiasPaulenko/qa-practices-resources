// @playwright/test 1.x — route interception and request waiting
await page.route('**/api/users', (route) => {
  route.fulfill({ json: { id: 1, name: 'Test' } });
});

await page.route('**/api/users', (route) => route.abort());
await page.route('**/api/**', (route) => route.continue());

const responsePromise = page.waitForResponse('**/api/users');
await page.locator('#load').click();
const response = await responsePromise;

const apiResponse = await page.request.get('/api/health');
const postResponse = await page.request.post('/api/login', {
  data: { email: 'test@test.com', password: 'pass' }
});
