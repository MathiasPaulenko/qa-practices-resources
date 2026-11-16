// Orders lookup handler — nodejs22.x runtime.
// Serves GET /orders/{id} backed by DynamoDB.
import { DynamoDBClient, GetItemCommand } from '@aws-sdk/client-dynamodb';
import { unmarshall } from '@aws-sdk/util-dynamodb';

const db = new DynamoDBClient({});
const TABLE = process.env.ORDERS_TABLE;

export const handler = async (event) => {
  const orderId = event.pathParameters?.id;
  if (!orderId) {
    return { statusCode: 400, body: JSON.stringify({ error: 'missing order id' }) };
  }
  const { Item } = await db.send(new GetItemCommand({
    TableName: TABLE,
    Key: { orderId: { S: orderId } },
  }));
  if (!Item) {
    return { statusCode: 404, body: JSON.stringify({ error: 'order not found' }) };
  }
  return { statusCode: 200, body: JSON.stringify(unmarshall(Item)) };
};
