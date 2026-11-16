# Serverless Functions Testing — Companion

Runnable companion for the guide [How to Test Serverless Functions: AWS Lambda, Azure](https://qapractices.com/documentation/serverless-functions-testing).

A `GET /orders/{id}` Lambda backed by DynamoDB, with everything needed to exercise the three testing layers from the guide:

- `template.yaml` — SAM template: `nodejs22.x` function, least-privilege `DynamoDBReadPolicy`, API Gateway event, and the table definition.
- `src/handler.mjs` — the handler under test.
- `events/get-order.json` — synthetic API Gateway proxy event for local invocation.
- `env.json` — environment variables for `sam local`.
- `tests/handler.test.mjs` — Jest 30 unit tests with `aws-sdk-client-mock`, no AWS credentials required.

## Run the unit tests

```bash
npm install
npm test
```

## Invoke the function locally

Requires AWS SAM CLI 1.172 and Docker running:

```bash
sam build && sam local invoke OrdersFunction \
  --event events/get-order.json \
  --env-vars env.json
```

`sam local` executes the handler but not DynamoDB — for a full local round trip, point the SDK endpoint at LocalStack 2026.10 or deploy to a test account with `sam deploy --guided`.
