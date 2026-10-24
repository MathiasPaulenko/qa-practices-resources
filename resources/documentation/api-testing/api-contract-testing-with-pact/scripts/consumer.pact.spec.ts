// Consumer contract test — generates a Pact file in ./pacts/
// Mirrors the guide's consumer example (pact-js V3 API).
import { PactV3, MatchersV3 } from '@pact-foundation/pact';
import { describe, it, expect } from '@jest/globals';

const provider = new PactV3({
  consumer: 'CheckoutService',
  provider: 'UserService',
  dir: 'pacts',
});

describe('GET /users/123 contract', () => {
  it('returns the user shape the checkout depends on', async () => {
    await provider
      .uponReceiving('a request for user 123')
      .withRequest({ method: 'GET', path: '/users/123', headers: { Accept: 'application/json' } })
      .willRespondWith({
        status: 200,
        headers: { 'Content-Type': 'application/json' },
        body: {
          id: MatchersV3.integer(123),
          name: MatchersV3.string('Jane Doe'),
          email: MatchersV3.string('jane@qa.local'),
        },
      })
      .executeTest(async (mockServer) => {
        const res = await fetch(`${mockServer.url}/users/123`, {
          headers: { Accept: 'application/json' },
        });
        const user = await res.json();
        expect(res.status).toBe(200);
        expect(user.name).toBe('Jane Doe');
      });
  });
});
