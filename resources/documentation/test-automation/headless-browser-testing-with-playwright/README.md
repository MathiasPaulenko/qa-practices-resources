# Headless Browser Testing with Playwright — Companion

Runnable Playwright v1.61 headless test config, auth setup, Dockerfile, GitHub Actions workflow and example tests for the [Headless Browser Testing with Playwright Guide](https://qapractices.com/documentation/headless-browser-testing-with-playwright/).

## Contents

| File | What it does |
| --- | --- |
| `playwright.config.ts` | Headless projects for Chromium, Firefox and WebKit with tracing and screenshots |
| `auth.setup.ts` | Authentication setup that saves `auth.json` for reuse |
| `Dockerfile.test` | Pinned Playwright Docker image for CI |
| `tests/login.spec.ts` | Example login test using `data-testid` selectors |
| `.github/workflows/playwright.yml` | GitHub Actions workflow with artifact upload on failure |

## Quick Start

```bash
# 1. Install dependencies
npm init -y && npm install -D @playwright/test@1.61.1
npx playwright install --with-deps

# 2. Copy the config files from this companion
# 3. Run headless tests
npx playwright test --project=chromium-headless --trace=on

# 4. View trace on failure
npx playwright show-trace test-results/trace.zip
```

## Docker

```bash
docker build -f Dockerfile.test -t playwright-tests .
docker run --rm --ipc=host playwright-tests
```

Use `--ipc=host` when running 4+ workers to prevent OOM kills from shared memory limits.

## CI

The `.github/workflows/playwright.yml` file runs headless tests on every push and pull request, uploading the Playwright report and test results as artifacts on failure.

## License

MIT — see the main repository for details.
