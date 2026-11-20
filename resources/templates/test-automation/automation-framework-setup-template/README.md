# Automation Framework Setup Template — Companion

> Companion resource for [Automation Framework Setup Template](https://qapractices.com/templates/automation-framework-setup-template) on QAPractices.com.

Copyable scaffold for the week-one setup document of a test automation framework: the blank setup document, a completed sample, and the config files it describes (Playwright config, env template, lint rules, CI workflow).

## Requirements

- Node.js 20+ and npm
- Playwright 1.44+
- TypeScript 5.4+
- GitHub Actions (for CI)

## Setup

```bash
# Install dependencies
npm install -D @playwright/test typescript dotenv
npx playwright install chromium firefox

# Copy the env template and fill in your values
cp .env.example .env

# Run the suite
npx playwright test --config infra/playwright.config.ts
```

## Files

| File | Purpose |
| ---- | ------- |
| `docs/framework-setup-template.md` | Blank setup document to copy into your repo |
| `docs/framework-setup-shoplite-sample.md` | The same document filled in for a fictional e-commerce app |
| `infra/playwright.config.ts` | Playwright config: chromium + firefox projects, retry on CI, `baseURL` from env |
| `.env.example` | Committed environment variable template — real secrets stay in CI |
| `eslint.config.mjs` | Flat config blocking `waitForTimeout` and CSS selectors in specs |
| `.github/workflows/e2e-tests.yml` | CI workflow: smoke suite on PRs, full regression nightly |

## Usage

1. Copy `docs/framework-setup-template.md` into your repo as `docs/framework-setup.md`.
2. Fill the Stack Decision table first — every other section follows from it.
3. Adjust the config files to your stack, then generate the repository layout with `tree -L 3` and paste it into section 4.
4. Open one PR with the scaffold, the config files and the filled document together.
