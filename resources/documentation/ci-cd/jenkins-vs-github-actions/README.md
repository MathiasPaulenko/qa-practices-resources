# Jenkins vs GitHub Actions: Same Pipeline in Both Tools

Companion to the QAPractices guide [Jenkins vs GitHub Actions: CI/CD Comparison](https://qapractices.com/documentation/jenkins-vs-github-actions/).

The `same-pipeline/` folder implements one identical Node.js CI pipeline twice — once as a declarative `Jenkinsfile`, once as a GitHub Actions workflow — so you can compare the two DSLs line by line.

## Project structure

```text
same-pipeline/
├── Jenkinsfile
└── .github/
    └── workflows/
        └── ci.yml
```

## Concept mapping

| Jenkins | GitHub Actions | Notes |
|---------|----------------|-------|
| `pipeline { stages { stage } }` | `jobs.<id>.steps` | Jenkins groups work in stages; Actions groups work in jobs |
| `agent any` | `runs-on: ubuntu-latest` | Jenkins picks any online agent; Actions picks a hosted or self-hosted runner |
| `environment { CI = 'true' }` | implicit (`CI=true` is set by Actions) | Hosted runners export `CI=true` automatically |
| `post { always { junit ... } }` | `if: always()` + `dorny/test-reporter` | Result publishing is a plugin in Jenkins, an action in Actions |
| `post { failure { archiveArtifacts } }` | `if: failure()` + `actions/upload-artifact` | Same semantics, different mechanism |
| `options { timestamps(); buildDiscarder }` | built into the Actions UI | Retention configured at repo/org level |
| Jenkins credential store | `secrets.*` + environments / OIDC | OIDC removes long-lived cloud credentials entirely |

## Requirements

- A Node.js project with `npm run test:unit` and `npm run test:e2e` scripts, Jest with the `jest-junit` reporter, and a Playwright (or equivalent) E2E suite that writes `playwright-report/`.
- For the Jenkinsfile: a Jenkins controller with an agent running Node.js 20 (or a `docker { image 'node:20-bookworm' }` agent) and the JUnit plugin.
- For the workflow: nothing extra — the hosted `ubuntu-latest` runner covers it.

## Usage

Drop the file for the tool you are evaluating into a real repo and run a few PRs against it. The point of the comparison is felt, not read: watch the queue wait on Jenkins agents versus the runner spin-up time on Actions before deciding.
