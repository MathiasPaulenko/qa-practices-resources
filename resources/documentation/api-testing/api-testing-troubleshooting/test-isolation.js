// Reliable API test isolation: each test creates and cleans up its own data.
// Requires: supertest 7, a test runner (jest/vitest), and a valid bearer token.
const request = require('./api-client'); // supertest agent bound to the API base URL

describe('Payment API', () => {
  let paymentId;

  beforeEach(async () => {
    const response = await request.post('/api/payments')
      .set('Authorization', `Bearer ${token}`)
      .send({ amount: 100, currency: 'USD' });
    paymentId = response.body.id;
  });

  afterEach(async () => {
    if (paymentId) {
      await request.delete(`/api/payments/${paymentId}`)
        .set('Authorization', `Bearer ${token}`);
    }
  });

  test('retrieves payment by id', async () => {
    const response = await request.get(`/api/payments/${paymentId}`)
      .set('Authorization', `Bearer ${token}`);
    expect(response.status).toBe(200);
    expect(response.body.amount).toBe(100);
  });
});
