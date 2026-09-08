// provider.test.js
// Requires: @pact-foundation/pact 13.x
const { Verifier } = require('@pact-foundation/pact');

const app = require('./app');
const server = app.listen(8081);

describe('User Service Provider', () => {
  test('verifies consumer contracts', async () => {
    await new Verifier({
      provider: 'UserService',
      providerBaseUrl: 'http://localhost:8081',
      pactBrokerBaseUrl: process.env.PACT_BROKER_URL || 'https://pact-broker.qa.local',
      pactBrokerToken: process.env.PACT_TOKEN,
      publishVerificationResult: true,
      providerAppVersion: '2.4.1',
      providerBranch: 'main',
    }).verifyProvider();
  });

  afterAll(() => server.close());
});
