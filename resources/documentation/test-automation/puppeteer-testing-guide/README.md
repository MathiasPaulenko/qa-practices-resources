# Puppeteer Testing Guide — Runnable Companion

Runnable JavaScript companions to the [Puppeteer Testing Guide for Headless Chrome](https://qapractices.com/documentation/puppeteer-testing-guide/) on QAPractices. Written for **Puppeteer 24.x** and **jest-puppeteer 10**.

## Contents

| File | Covers |
|---|---|
| `javascript/verify-install.js` | Minimal launch → goto → title → close smoke check |
| `javascript/first-test.js` | Login spec: `type`, `click`, `waitForSelector`, `$eval` |
| `javascript/selectors.js` | CSS, `::-p-xpath`, `::-p-text`, `$$`, `page.evaluate` |
| `javascript/screenshots.js` | Full-page, element and screenshot-on-failure |
| `javascript/waits.js` | `waitForSelector`, `waitForNavigation`, `networkidle0`, `waitForFunction` |
| `javascript/network-interception.js` | Blocking images, mocking API responses, logging calls |
| `javascript/pdf.js` | `page.pdf` with A4, margins and `printBackground` |
| `javascript/jest.config.js` | `jest-puppeteer` preset + 60s timeout |
| `pages/LoginPage.js` | Page Object class for the login flow |
| `pages/login.test.js` | Spec that consumes the Page Object |
| `.github/workflows/puppeteer-tests.yml` | CI job: `npm ci` → `npx jest --ci` → upload screenshots |

## Setup

```bash
npm install puppeteer@24
npm install --save-dev jest jest-puppeteer@10
```

`staging.myapp.com` is a placeholder — replace it with your own staging URL and credentials.

## Notes

- `page.$x` and `page.waitForTimeout` were removed in Puppeteer 22; the examples use `page.locator('::-p-xpath(...)')` / `::-p-text` and plain `setTimeout` promises.
- In CI, prefer `puppeteer-core` plus `executablePath` if your image already ships Chrome — it skips the Chromium download.
- Screenshots land in `screenshots/` and the workflow uploads them as artifacts on every run (`if: always()`).
