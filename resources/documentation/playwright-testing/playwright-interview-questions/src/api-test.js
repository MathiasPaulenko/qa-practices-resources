test('API test', async ({ request }) => {
  const response = await request.post('/api/users', {
    data: { name: 'Test User', email: 'test@test.com' }
  })
  expect(response.ok()).toBeTruthy()
  const body = await response.json()
  expect(body.id).toBeDefined()
})