// MongoDB 8 — explain() assertions for the top queries (mongosh script).
// Run: mongosh mongodb://localhost:27017/nosql_test explain-check.js
// Seeds ~5k orders, builds the index, and asserts IXSCAN + bounded docs examined.

db.orders.drop();

const bulk = [];
for (let i = 0; i < 5000; i++) {
  bulk.push({
    customerId: "cust_" + (i % 100),
    status: i % 5 === 0 ? "pending" : "completed",
    amount: Math.round(Math.random() * 500),
    createdAt: new Date(Date.now() - (i % 30) * 86400000)
  });
}
db.orders.insertMany(bulk);

db.orders.createIndex({ customerId: 1, status: 1, createdAt: -1 });

function assertPlan(name, query) {
  const plan = query.explain("executionStats");
  const exec = plan.executionStats;
  const stage = JSON.stringify(plan.queryPlanner.winningPlan);
  const usedIndex = stage.includes('"IXSCAN"');
  const ratio = exec.nReturned === 0 ? 1 : exec.totalDocsExamined / exec.nReturned;
  print(`${name}`);
  print(`  stage: ${usedIndex ? 'IXSCAN' : 'NO INDEX (check winningPlan)'} | ` +
        `docsExamined: ${exec.totalDocsExamined} | nReturned: ${exec.nReturned} | ` +
        `time: ${exec.executionTimeMillis} ms`);
  if (!usedIndex) { print(`  FAIL: query did not use an index`); quit(1); }
  if (ratio > 10) { print(`  FAIL: examined ${ratio.toFixed(0)}x more docs than returned`); quit(1); }
  print(`  PASS`);
}

assertPlan("customer + status + recent", db.orders.find({
  customerId: "cust_42",
  status: "completed",
  createdAt: { $gt: new Date(Date.now() - 7 * 86400000) }
}));

assertPlan("customer + pending", db.orders.find({
  customerId: "cust_7",
  status: "pending"
}));
