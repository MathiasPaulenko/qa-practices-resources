// Mock a response
await page.route('**/api/users', (route) => {
  route.fulfill({ json: { users: [{ id: 1, name: 'Mock User' }] } })
})

// Modify a request
await page.route('**/api/*', (route) => {
  route.continue({ headers: { ...route.request().headers(), 'X-Test': 'true' } })
})

// Abort requests
await page.route('**/*.{png,jpg}', (route) => route.abort())