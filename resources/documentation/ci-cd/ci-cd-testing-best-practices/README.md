# CI/CD Testing Pipeline Example

Runnable snippets from the QAPractices guide [CI/CD Testing: Best Practices & Quality Gates](https://qapractices.com/documentation/ci-cd-testing-best-practices/).

The `pipeline-example/` folder wires the six stages described in the guide into one GitHub Actions workflow, plus the Jenkins quality gate, a faker-based test data factory and a k6 load gate.

## Project structure

```text
pipeline-example/
├── .github/
│   └── workflows/
│       └── quality-gates.yml
├── Jenkinsfile
├── factories/
│   └── user.factory.ts
├── load-test.js
└── package.json
```

## What it demonstrates

- `.github/workflows/quality-gates.yml` runs stages cheapest-to-most-expensive: build+unit, then integration (postgres/redis services with mapped ports) and security (npm audit, Semgrep, trufflehog) in parallel, then E2E, and a performance+contract stage gated to `main`.
- `Jenkinsfile` implements the blocking coverage gate: it parses `coverage/lcov.info` and fails the build under 80%.
- `factories/user.factory.ts` is the `@faker-js/faker` v9 factory used by the test data section.
- `load-test.js` is a k6 v0.52 script whose `thresholds` block enforces the same p95 < 500 ms gate the guide defines.
- `package.json` contains the `lint-staged` 15 + `husky` 9 pre-commit setup and the `test:*` scripts every stage calls.

## Usage

Copy the pieces you need into your own repo. The workflow assumes `npm run test:unit`, `test:integration`, `test:contract` and a Cypress suite exist — adjust the script names to match your project.
