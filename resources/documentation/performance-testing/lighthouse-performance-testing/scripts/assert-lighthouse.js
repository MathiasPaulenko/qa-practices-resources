// Assert on a specific Lighthouse metric
// Fails the build if LCP exceeds 2500ms
// Usage: node assert-lighthouse.js ./report.json
const fs = require('fs');

const reportPath = process.argv[2];
if (!reportPath) {
    console.error('Usage: node assert-lighthouse.js <path-to-report.json>');
    process.exit(1);
}

const report = JSON.parse(fs.readFileSync(reportPath, 'utf8'));

const LCP_THRESHOLD_MS = 2500;
const INP_THRESHOLD_MS = 200;
const CLS_THRESHOLD = 0.1;

const lcp = report.audits['largest-contentful-paint'].numericValue;
const inp = report.audits['interaction-to-next-paint'].numericValue;
const cls = report.audits['cumulative-layout-shift'].numericValue;

const failures = [];

if (lcp > LCP_THRESHOLD_MS) {
    failures.push(`LCP ${lcp.toFixed(0)}ms exceeds ${LCP_THRESHOLD_MS}ms threshold`);
}
if (inp > INP_THRESHOLD_MS) {
    failures.push(`INP ${inp.toFixed(0)}ms exceeds ${INP_THRESHOLD_MS}ms threshold`);
}
if (cls > CLS_THRESHOLD) {
    failures.push(`CLS ${cls.toFixed(3)} exceeds ${CLS_THRESHOLD} threshold`);
}

if (failures.length > 0) {
    console.error('Lighthouse metric assertions failed:');
    failures.forEach((f) => console.error(`  - ${f}`));
    process.exit(1);
}

console.log(`All metrics within thresholds: LCP ${lcp.toFixed(0)}ms, INP ${inp.toFixed(0)}ms, CLS ${cls.toFixed(3)}`);
