// Check a Lighthouse JSON report against lighthouse-budget.json.
// Usage: node check-budget.js <report.json> [lighthouse-budget.json]
// Exits 1 if any budget is breached — wire it into CI after `lighthouse --output=json`.
const fs = require('fs');

const reportPath = process.argv[2] || 'sample-report.json';
const budgetPath = process.argv[3] || 'lighthouse-budget.json';

const report = JSON.parse(fs.readFileSync(reportPath, 'utf8'));
const budgets = JSON.parse(fs.readFileSync(budgetPath, 'utf8')).budgets[0];
const audits = report.audits;

const items = (audits['resource-summary'] && audits['resource-summary'].details.items) || [];
const sizeKb = (type) =>
  items.filter((i) => i.resourceType === type).reduce((s, i) => s + i.transferSize, 0) / 1024;

const timingMs = (id) => (audits[id] ? audits[id].numericValue : null);
const METRIC_AUDITS = {
  'largest-contentful-paint': 'largest-contentful-paint',
  'interactive': 'interactive',
};

let failures = 0;
const check = (label, actual, limit, unit) => {
  if (actual === null || actual === undefined) {
    console.log(`SKIP  ${label.padEnd(28)} audit not present in report`);
    return;
  }
  const ok = actual <= limit;
  if (!ok) failures++;
  console.log(`${ok ? 'PASS' : 'FAIL'}  ${label.padEnd(28)} ${actual.toFixed(unit === 'KB' ? 0 : 0)} ${unit}  (budget ${limit} ${unit})`);
};

console.log(`Budget check: ${reportPath} vs ${budgetPath}\n`);

for (const rule of budgets.resourceSizes || []) {
  check(`size:${rule.resourceType}`, sizeKb(rule.resourceType), rule.budget, 'KB');
}

for (const rule of budgets.resourceCounts || []) {
  if (rule.resourceType === 'third-party') {
    const tps = audits['third-party-summary'];
    const count = tps && tps.details && tps.details.items ? tps.details.items.length : null;
    check('count:third-party', count, rule.budget, 'items');
  }
}

for (const rule of budgets.timings || []) {
  const auditId = METRIC_AUDITS[rule.metric] || rule.metric;
  check(`timing:${rule.metric}`, timingMs(auditId), rule.budget, 'ms');
}

console.log(`\n${failures === 0 ? 'All budgets satisfied.' : `${failures} budget(s) breached.`}`);
process.exit(failures === 0 ? 0 : 1);
