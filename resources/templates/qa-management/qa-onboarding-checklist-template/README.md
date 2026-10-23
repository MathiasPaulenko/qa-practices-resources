# QA Onboarding Checklist — Runnable Companion

Small artifacts used during week one of the [QA Onboarding Checklist Template: New Hire 30-60-90](https://qapractices.com/templates/qa-onboarding-checklist-template/) on QAPractices.

## Contents

| File | Purpose |
|---|---|
| `env-check.sh` | Verifies a new hire's machine has Node, Git, Python, Docker and Playwright browsers installed. Fails on the first broken tool (`set -e`) so problems surface before the first standup. |
| `first-ticket.yml` | GitHub issue-form template for the new hire's first independent task. |

## Usage

```bash
bash env-check.sh
```

Expected output looks like:

```text
== QA onboarding environment check ==
Node v20.11.0
Git 2.43.0
Python 3.11.x
Hello from Docker!
All checks passed.
```

Copy `first-ticket.yml` into `.github/ISSUE_TEMPLATE/` of your repo to get a ready-made onboarding task form.

Source resource: https://qapractices.com/templates/qa-onboarding-checklist-template/
