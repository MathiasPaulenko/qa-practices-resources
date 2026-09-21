const axios = require('axios');

// The same "GET user by id" scenario as the REST Assured and Karate examples,
// written with Axios 1.x and Jest 30.
const api = axios.create({
  baseURL: 'https://jsonplaceholder.typicode.com',
  headers: { Accept: 'application/json' }
});

test('GET user returns 200 with valid data', async () => {
  const response = await api.get('/users/1');

  expect(response.status).toBe(200);
  expect(response.data.id).toBe(1);
  expect(response.data.username).toBe('Bret');
  expect(response.data.email).toContain('@');
});

test('GET unknown user rejects with 404', async () => {
  await expect(api.get('/users/999999')).rejects.toMatchObject({
    response: { status: 404 }
  });
});
