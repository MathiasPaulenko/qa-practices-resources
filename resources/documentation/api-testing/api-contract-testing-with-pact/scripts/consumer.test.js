// consumer.test.js
// Requires: @pact-foundation/pact 13.x
const { PactV3, MatchersV3 } = require('@pact-foundation/pact');
const path = require('path');

const provider = new PactV3({
  consumer: 'BillingServiceClient',
  provider: 'UserService',
  dir: path.resolve(process.cwd(), 'pacts'),
});

describe('Billing Service Client', () => {
  test('get user by ID', async () => {
    await provider
      .given('user with ID 123 exists')
      .uponReceiving('a request for user 123')
      .withRequest({
        method: 'GET',
        path: '/users/123',
        headers: { Accept: 'application/json' },
      })
      .willRespondWith({
        status: 200,
        headers: { 'Content-Type': 'application/json' },
        body: {
          id: MatchersV3.integer(123),
          name: MatchersV3.string('Jane Doe'),
          email: MatchersV3.string('jane@qa.local'),
        },
      });

    await provider.executeTest(async (mockServer) => {
      const response = await fetch(`${mockServer.url}/users/123`);
      const user = await response.json();
      expect(user.name).toBe('Jane Doe');
    });
  });
});
