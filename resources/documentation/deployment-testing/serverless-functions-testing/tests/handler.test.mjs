// Unit tests for the orders handler — Jest 30 + aws-sdk-client-mock 4.x.
// No AWS credentials needed: every DynamoDB call is mocked.
import { mockClient } from 'aws-sdk-client-mock';
import { DynamoDBClient, GetItemCommand } from '@aws-sdk/client-dynamodb';
import { handler } from '../src/handler.mjs';

const ddbMock = mockClient(DynamoDBClient);

beforeEach(() => ddbMock.reset());

test('returns 400 when the path parameter is missing', async () => {
  const res = await handler({ pathParameters: {} });
  expect(res.statusCode).toBe(400);
});

test('returns 404 when the order does not exist', async () => {
  ddbMock.on(GetItemCommand).resolves({});
  const res = await handler({ pathParameters: { id: 'ORD-999' } });
  expect(res.statusCode).toBe(404);
});

test('returns the unmarshalled order on a hit', async () => {
  ddbMock.on(GetItemCommand).resolves({
    Item: { orderId: { S: 'ORD-101' }, status: { S: 'shipped' } },
  });
  const res = await handler({ pathParameters: { id: 'ORD-101' } });
  expect(res.statusCode).toBe(200);
  expect(JSON.parse(res.body).status).toBe('shipped');
});
