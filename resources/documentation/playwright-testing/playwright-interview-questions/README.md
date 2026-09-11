# Playwright Interview Questions — Companion

This companion provides runnable files for the [Top 20 Playwright Interview Questions](https://qapractices.com/documentation/playwright-interview-questions) guide.

## Files

| File | Purpose |
|------|---------|
| `src/custom-fixture.js` | Custom Playwright fixture with authenticated page |
| `src/storage-state.js` | Save and restore browser state (cookies, localStorage) |
| `src/network-mock.js` | Intercept and mock network requests with page.route() |
| `src/api-test.js` | API testing with the request fixture |
| `src/popup-handling.js` | Multiple tabs and popup handling |
| `src/file-download.js` | File download handling |
| `src/file-upload.js` | File upload handling with setInputFiles() |
| `src/trace-config.js` | Trace Viewer configuration |
| `src/ci-workflow.yml` | GitHub Actions CI workflow for Playwright |
| `src/retries-config.js` | Test retries configuration |
| `src/projects-config.js` | Playwright projects configuration |

## Quick Start

```bash
npm init -y && npm install @playwright/test
npx playwright install --with-deps
npx playwright test
```