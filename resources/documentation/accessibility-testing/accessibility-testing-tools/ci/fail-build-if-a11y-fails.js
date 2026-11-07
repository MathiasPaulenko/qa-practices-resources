#!/usr/bin/env node
// CI gate for axe-core 4.10 results.
// Usage: node fail-build-if-a11y-fails.js < axe-results.json
// Exit 1 if any violation has impact 'critical' or 'serious'; warn otherwise.

const fs = require('fs');

const raw = fs.readFileSync(0, 'utf8');
let results;
try {
  results = JSON.parse(raw);
} catch {
  console.error('Could not parse axe results JSON from stdin');
  process.exit(2);
}

const violations = results.violations || [];
const blocking = violations.filter(
  v => v.impact === 'critical' || v.impact === 'serious'
);
const warnings = violations.filter(
  v => v.impact === 'moderate' || v.impact === 'minor'
);

if (warnings.length > 0) {
  console.warn(`${warnings.length} non-blocking a11y violation(s):`);
  for (const w of warnings) console.warn(`  [${w.impact}] ${w.id} — ${w.help}`);
}

if (blocking.length > 0) {
  console.error(`${blocking.length} blocking a11y violation(s):`);
  for (const v of blocking) {
    console.error(`  [${v.impact}] ${v.id} — ${v.help} (${v.nodes.length} node(s))`);
  }
  process.exit(1);
}

console.log('A11y gate passed: no critical or serious violations.');
