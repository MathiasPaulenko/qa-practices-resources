# Email Notification System Test Cases — Companion

Runnable artifacts for the [Email Notification Test Cases](https://qapractices.com/test-cases/email-notification-system-test-cases/) resource on QAPractices.

## Contents

| File | Purpose | Related TC |
|---|---|---|
| `sendgrid/send-test-email.sh` | Sends a `task-assigned` email through the SendGrid API v3 | TC-001, TC-006 |
| `sendgrid/task-assigned-payload.json` | Template payload fixture with dynamic data | TC-006, TC-007 |
| `scripts/mailpit-delivery-check.sh` | Polls a Mailpit inbox and asserts subject + `List-Unsubscribe` header | TC-009, TC-017 |
| `playwright/taskflow-notifications.spec.ts` | Preference toggles and unsubscribe-flow spec skeleton (Playwright 1.55+) | TC-016, TC-018 |

## Requirements

- `SENDGRID_API_KEY` exported for `send-test-email.sh`.
- [Mailpit](https://mailpit.axllent.com/) v1.20+ running locally (`docker run -p 8025:8025 axllent/mailpit`) and `jq` for the delivery check.
- Node 20+ and `@playwright/test` 1.55+ for the spec.

## Usage

```bash
# 1. Trigger an email against staging/SendGrid
./sendgrid/send-test-email.sh

# 2. Verify it landed in the catch-all inbox with the right headers
./scripts/mailpit-delivery-check.sh ana.martinez@taskflow.io "task assigned"

# 3. Run the UI spec
npx playwright test taskflow-notifications.spec.ts --reporter=list
```

Spanish version: [README.es.md](README.es.md)
