// Subscription lifecycle test over the graphql-ws protocol.
// Requires a reachable GraphQL endpoint; set GRAPHQL_URL (https) and QA_TOKEN.
const request = require('supertest')(
  process.env.GRAPHQL_URL || 'https://staging.qapractices.dev' // Placeholder: staging URL
);
const { createClient } = require('graphql-ws'); // graphql-ws 6.x
const WebSocket = require('ws'); // ws 8.18

const wsUrl = (process.env.GRAPHQL_URL || 'https://staging.qapractices.dev')
  .replace(/^http/, 'ws');

const wsClient = createClient({
  url: `${wsUrl}/graphql`,
  webSocketImpl: WebSocket,
  connectionParams: { authToken: process.env.QA_TOKEN },
});

test('messageAdded subscription delivers the created message', async () => {
  const events = [];
  const sub = wsClient.iterate({
    query: 'subscription { messageAdded { id text } }',
  });

  const consumer = (async () => {
    for await (const event of sub) events.push(event);
  })();

  await request.post('/graphql').send({
    query: 'mutation { addMessage(text: "hello") { id } }',
  });

  await new Promise((r) => setTimeout(r, 500));
  await sub.return();
  await consumer;

  expect(events[0].data.messageAdded.text).toBe('hello');
});

afterAll(() => wsClient.dispose());
