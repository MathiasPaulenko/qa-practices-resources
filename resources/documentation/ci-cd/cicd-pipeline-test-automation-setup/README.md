# CI/CD Test Automation Pipeline Setup

Runnable CI configs from the QAPractices guide [How to Set Up CI/CD Pipeline for Test Automation](https://qapractices.com/documentation/cicd-pipeline-test-automation-setup/).

The `pipeline-setup/` folder contains the three platform configurations the guide walks through, plus a sharded E2E variant with merged Playwright reports.

## Project structure

```text
pipeline-setup/
├── .github/
│   └── workflows/
│       ├── test-pipeline.yml   # unit → integration (postgres service) → E2E + JUnit publish
│       └── e2e-sharded.yml     # 4-way Playwright sharding + merge-reports job
├── Jenkinsfile                 # declarative pipeline: lint → unit → E2E, coverage gate, email on failure
└── .gitlab-ci.yml              # stages lint/test/e2e/deploy with JUnit + cobertura reports
```

## What it demonstrates

- `test-pipeline.yml` orders stages cheapest-first: unit tests with coverage, then integration tests against a `postgres:16` service container, then Playwright E2E gated behind `needs:`. A final `dorny/test-reporter@v1` job publishes JUnit results to the PR.
- `e2e-sharded.yml` runs `npx playwright test --shard=N/4` across four runners and merges the per-shard reports with `npx playwright merge-reports`.
- `Jenkinsfile` is the declarative equivalent: `nodejs 'Node20'` tool, `junit` + `publishHTML` post-actions, archived Playwright artifacts, and `emailext` failure notification via `${env.QA_TEAM_EMAIL}`.
- `.gitlab-ci.yml` uses `artifacts:reports:junit` and `coverage_report` so failures and coverage show in the merge request widget; the E2E job runs inside the pinned `mcr.microsoft.com/playwright:v1.45.0-jammy` image.

## Usage

Copy the file matching your platform into your repo:

- GitHub: `.github/workflows/test-pipeline.yml` (and `e2e-sharded.yml` when the E2E suite passes ~10 minutes)
- Jenkins: `Jenkinsfile` at the repo root — requires the NodeJS, JUnit, HTML Publisher and Email Extension plugins
- GitLab: `.gitlab-ci.yml` at the repo root

Adjust `npm test`, `npm run test:integration` and `npm run lint` to match your project's scripts. Every version tag is pinned — keep it that way.

## Related resource

- EN: https://qapractices.com/documentation/cicd-pipeline-test-automation-setup/
- ES: https://qapractices.com/es/documentation/cicd-pipeline-test-automation-setup/
