# Agile Testing Interview Questions — Companion

Runnable artifacts referenced in the [Top 20 Agile Testing Interview Questions](https://qapractices.com/documentation/agile-testing-interview-questions/) guide on QAPractices.

## Files

| File | Concept it demonstrates |
|---|---|
| `Jenkinsfile` | Continuous testing pipeline: unit → integration → E2E smoke → staging → exploratory (Q12) |
| `sprint_burndown.py` | Track QA hours against dev tasks inside a sprint (Q4) |
| `dod_check.yaml` | Definition of Done gate usable as a build check (Q5) |
| `tdd_discount.py` | Red-green-refactor cycle with a runnable pytest-style test (Q7) |
| `login.feature` | Gherkin scenarios in Given-When-Then format (Q8) |

## Usage

- `python sprint_burndown.py` — prints QA progress for the sprint.
- `python tdd_discount.py` — runs the TDD example end to end.
- `Jenkinsfile` — drop into a Jenkins pipeline job; adjust the npm scripts to your project.
- `login.feature` — run with Behave 1.2+ (`behave login.feature`) once step definitions exist.
- `dod_check.yaml` — parse in CI and fail the build on any `false` entry.
