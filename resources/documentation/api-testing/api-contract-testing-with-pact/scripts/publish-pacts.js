// publish-pacts.js
// Requires: @pact-foundation/pact-node 14.x
const { Publisher } = require('@pact-foundation/pact-node');

new Publisher({
  pactBroker: process.env.PACT_BROKER_URL || 'https://pact-broker.qa.local',
  pactBrokerToken: process.env.PACT_TOKEN,
  consumerVersion: '1.3.0',
  tags: ['main', 'staging'],
  pactFilesOrDirs: ['./pacts'],
}).publishPacts();
