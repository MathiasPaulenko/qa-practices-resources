# Test Automation Framework Architecture Template — Companion

> Companion resource for [Test Automation Framework Architecture Template](https://qapractices.com/templates/test-automation-framework-architecture-template) on QAPractices.com.

Layered test automation framework with spec files, page objects, core utilities and CI workflow for Playwright 1.44 + TypeScript 5.4.

## Requirements

- Node.js 20+ and npm
- Playwright 1.44+
- TypeScript 5.4+
- GitHub Actions (for CI)

## Setup

```bash
# Install dependencies
npm install @playwright/test typescript
npx playwright install chromium

# Run the E2E suite
npx playwright test

# Run with a specific project
npx playwright test --project=chromium

# Run only smoke tests
npx playwright test --grep @smoke
```

## Files

| File | Layer | Purpose |
| ---- | ----- | ------- |
| `tests/e2e/auth/login.spec.ts` | Test Definition | Spec file describing login behavior |
| `pages/LoginPage.ts` | Page Object | Encapsulates login page interactions |
| `core/config/environment.ts` | Core | Environment-aware configuration |
| `infra/playwright.config.ts` | Infrastructure | Playwright configuration with projects |
| `.github/workflows/e2e-tests.yml` | Infrastructure | CI workflow for GitHub Actions |

## Project Structure

```text
tests/
└── e2e/
    └── auth/
        └── login.spec.ts

pages/
└── LoginPage.ts

core/
└── config/
    └── environment.ts

infra/
└── playwright.config.ts

.github/
└── workflows/
    └── e2e-tests.yml
```

## License

MIT — free to use, modify, and distribute. Never store production credentials in test config; always use environment variables.
