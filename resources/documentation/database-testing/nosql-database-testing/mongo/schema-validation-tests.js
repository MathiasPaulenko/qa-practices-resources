// MongoDB 8 — $jsonSchema validation test suite (mongosh script).
// Run: mongosh mongodb://localhost:27017/nosql_test schema-validation-tests.js
// Expected: PASS lines for valid/invalid inserts and a final summary.

db.users.drop();

db.createCollection("users", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["email", "createdAt"],
      properties: {
        email: { bsonType: "string", pattern: "^.+@.+$" },
        age: { bsonType: "int", minimum: 0, maximum: 150 },
        roles: { bsonType: "array", items: { enum: ["admin", "user", "guest"] } }
      }
    }
  },
  validationLevel: "strict"
});

let passed = 0, failed = 0;

function check(name, fn, shouldFail) {
  try {
    fn();
    if (shouldFail) { print(`FAIL  ${name}: insert accepted but should fail`); failed++; }
    else { print(`PASS  ${name}`); passed++; }
  } catch (e) {
    if (shouldFail) { print(`PASS  ${name}: rejected (${e.code || e.codeName || 'validation error'})`); passed++; }
    else { print(`FAIL  ${name}: unexpected error ${e}`); failed++; }
  }
}

check("valid document", () => db.users.insertOne(
  { email: "a@b.com", createdAt: new Date(), age: 30, roles: ["user"] }), false);

check("missing required field (createdAt)", () => db.users.insertOne(
  { email: "a@b.com" }), true);

check("invalid type (age as string)", () => db.users.insertOne(
  { email: "a@b.com", createdAt: new Date(), age: "old" }), true);

check("role outside enum", () => db.users.insertOne(
  { email: "a@b.com", createdAt: new Date(), roles: ["superadmin"] }), true);

// Direct-collection insert: proves the rule lives in the DB, not the ORM.
check("direct insert bypasses nothing", () => db.users.insertOne(
  { createdAt: new Date() }), true);

print(`\n${passed} passed, ${failed} failed`);
if (failed > 0) quit(1);
