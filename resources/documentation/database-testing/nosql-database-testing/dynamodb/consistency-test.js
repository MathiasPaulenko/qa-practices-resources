// DynamoDB consistency test — AWS SDK v3 against DynamoDB Local.
// Start local: docker run -p 8000:8000 amazon/dynamodb-local
// Run: node consistency-test.js
// Verifies strong reads return the value and documents eventual-read behavior.

const {
  DynamoDBClient, CreateTableCommand, PutItemCommand, GetItemCommand, DeleteTableCommand
} = require("@aws-sdk/client-dynamodb");

const client = new DynamoDBClient({
  region: "us-east-1",
  endpoint: process.env.DYNAMODB_ENDPOINT || "http://localhost:8000",
  credentials: { accessKeyId: "local", secretAccessKey: "local" }
});

const TABLE = "ConsistencyTest";

async function main() {
  await client.send(new CreateTableCommand({
    TableName: TABLE,
    KeySchema: [{ AttributeName: "id", KeyType: "HASH" }],
    AttributeDefinitions: [{ AttributeName: "id", AttributeType: "S" }],
    BillingMode: "PAY_PER_REQUEST"
  }));

  await client.send(new PutItemCommand({
    TableName: TABLE,
    Item: { id: { S: "1" }, name: { S: "Ana" }, version: { N: "2" } }
  }));

  const strong = await client.send(new GetItemCommand({
    TableName: TABLE,
    Key: { id: { S: "1" } },
    ConsistentRead: true
  }));
  const strongOk = strong.Item && strong.Item.version.N === "2";
  console.log(`strong read: ${strongOk ? 'PASS (value visible)' : 'FAIL'}`);

  // Eventual read on DynamoDB Local returns immediately; against real DynamoDB
  // it may lag. Assert tolerance, not absence.
  const eventual = await client.send(new GetItemCommand({
    TableName: TABLE,
    Key: { id: { S: "1" } },
    ConsistentRead: false
  }));
  const eventualOk = !eventual.Item || eventual.Item.version.N === "2" || eventual.Item.version.N === "1";
  console.log(`eventual read: ${eventualOk ? 'PASS (tolerated)' : 'FAIL (unexpected state)'}`);

  await client.send(new DeleteTableCommand({ TableName: TABLE }));
  if (!strongOk || !eventualOk) process.exit(1);
}

main().catch((e) => { console.error(e); process.exit(1); });
