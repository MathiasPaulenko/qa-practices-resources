#!/usr/bin/env bash
# Runs pa11y 10 against the same URL at WCAG2AA and WCAG2AAA,
# then prints a violation count per level so you can size the delta.
# Usage: BASE_URL=https://staging.qapractices.com ./run-audit.sh /checkout
set -euo pipefail

BASE="${BASE_URL:-https://staging.qapractices.com}"
PATH_ARG="${1:-/}"

echo "== WCAG2AA scan: ${BASE}${PATH_ARG}"
npx pa11y@10 "${BASE}${PATH_ARG}" --standard WCAG2AA --reporter json > aa-report.json || true

echo "== WCAG2AAA scan: ${BASE}${PATH_ARG}"
npx pa11y@10 "${BASE}${PATH_ARG}" --standard WCAG2AAA --reporter json > aaa-report.json || true

node -e "
const aa = require('./aa-report.json');
const aaa = require('./aaa-report.json');
console.log('AA issues:  ' + (aa.issues ? aa.issues.length : 0));
console.log('AAA issues: ' + (aaa.issues ? aaa.issues.length : 0));
const aaCodes = new Set((aa.issues||[]).map(i => i.code));
const extra = (aaa.issues||[]).filter(i => !aaCodes.has(i.code));
console.log('AAA-only rules hit: ' + new Set(extra.map(i => i.code)).size);
"
