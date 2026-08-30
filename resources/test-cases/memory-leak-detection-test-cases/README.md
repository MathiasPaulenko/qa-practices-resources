# Memory Leak Detection Test Cases

> Printable companion and runnable examples for [Memory Leak Detection Test Cases](https://qapractices.com/test-cases/memory-leak-detection-test-cases).

This repository contains a printable version of the test case set plus example scripts you can adapt for your own project.

## Files

- `memory-leak-detection-test-cases.md` — Markdown version, ready to paste into a test management tool.
- `memory-leak-detection-test-cases.json` — Structured JSON with all test cases, edge cases and priorities.
- `scripts/` — Example scripts:
  - `node-heap-baseline.js` — Capture a baseline `heapUsed` reading.
  - `node-heap-monitor.js` — Monitor `process.memoryUsage()` over time.
  - `playwright-spa-memory.test.js` — Playwright test for detached DOM nodes.

## How to use

1. Open `memory-leak-detection-test-cases.md` in your test management tool.
2. Run `node scripts/node-heap-baseline.js` to establish a baseline in your environment.
3. Run `node scripts/node-heap-monitor.js` while applying load.
4. Use `playwright-spa-memory.test.js` as a starting point for SPA memory tests.

## Requirements

- Node.js 20+ (for `--heapsnapshot-near-heap-limit` and `process.memoryUsage()`)
- Playwright 1.48+ (for SPA tests)
- Chrome / Chromium (for DevTools heap snapshots)
