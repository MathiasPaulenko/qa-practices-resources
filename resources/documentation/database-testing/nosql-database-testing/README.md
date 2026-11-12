# NoSQL Database Testing Companion

Runnable checks for the [NoSQL Database Testing guide](https://qapractices.com/documentation/nosql-database-testing/) on qapractices.com — a MongoDB `$jsonSchema` validation suite, an `explain()` assertion script, and a DynamoDB consistency test against DynamoDB Local.

## Structure

```text
nosql-database-testing/
├── mongo/
│   ├── schema-validation-tests.js   # PASS/FAIL suite: valid + 4 invalid inserts vs $jsonSchema
│   └── explain-check.js             # Seeds 5k orders, asserts IXSCAN + bounded docs examined
├── dynamodb/
│   ├── consistency-test.js          # Strong vs eventual read assertions (AWS SDK v3)
│   └── package.json
└── meta.json
```

## Requirements

- **MongoDB**: local MongoDB 8 (or 7) with `mongosh` — `docker run -d -p 27017:27017 mongo:8`
- **DynamoDB**: DynamoDB Local — `docker run -p 8000:8000 amazon/dynamodb-local` — plus Node 18+

## Run the MongoDB checks

```bash
mongosh mongodb://localhost:27017/nosql_test mongo/schema-validation-tests.js
```

Expected output:

```text
PASS  valid document
PASS  missing required field (createdAt): rejected (121)
PASS  invalid type (age as string): rejected (121)
PASS  role outside enum: rejected (121)
PASS  direct insert bypasses nothing: rejected (121)

5 passed, 0 failed
```

The last case proves the rule lives in the database, not the ORM: a direct insert without `email` is rejected by the server-side validator.

```bash
mongosh mongodb://localhost:27017/nosql_test mongo/explain-check.js
```

Expected output:

```text
customer + status + recent
  stage: IXSCAN | docsExamined: ~50 | nReturned: ~50 | time: ~1 ms
  PASS
customer + pending
  stage: IXSCAN | docsExamined: ~20 | nReturned: ~20 | time: ~1 ms
  PASS
```

If either plan shows `NO INDEX`, the script exits non-zero — wire it into CI to catch index regressions.

## Run the DynamoDB consistency test

```bash
cd dynamodb
npm install
docker run -d -p 8000:8000 amazon/dynamodb-local
node consistency-test.js
```

Expected output:

```text
strong read: PASS (value visible)
eventual read: PASS (tolerated)
```

`Set DYNAMODB_ENDPOINT` to point at a different local endpoint. The eventual-read assertion tolerates stale values on purpose — against real DynamoDB an immediate eventual read may lag; the test documents the expected tolerance rather than asserting freshness it cannot guarantee.

## Notes

- Error code `121` is MongoDB's `DocumentValidationFailure` — the assertion accepts any error object so older server versions still pass.
- Both mongosh scripts call `quit(1)` on failure, so `echo $?` (or your CI runner) picks up regressions without parsing output.
