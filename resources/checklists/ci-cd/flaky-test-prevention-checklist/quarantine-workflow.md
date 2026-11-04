# Flaky Test Quarantine Workflow

The process the checklist's CI Management items imply — quarantine is a process, not a graveyard.

## On detection (test passes on retry = flaky)

1. Tag the test `flaky` in the suite (`test.describe('x', { tag: '@flaky' })`).
2. Open a ticket: spec path, failure signature, first-seen date, CI link.
3. Assign an owner — a name, not "the team".
4. Set the SLA: quarantined tests get fixed or deleted within 2 sprints.

## While quarantined

- The test runs in a separate non-blocking CI job — visible, not hidden.
- Retry counts stay in the report — masking stays visible.
- Weekly 15-min flake review: fix it, or escalate the deletion decision.

## On fix

- Reproduce locally with `repeat-until-failure.sh` — 20+ clean runs required.
- Identify the layer (isolation / timing / async / data / env / CI) and check the matching checklist section — the fix pattern is there.
- Remove the `@flaky` tag, close the ticket with the root cause written down.

## On expiry

SLA passed with no fix → escalate: either schedule real fix time or delete the test with the coverage loss documented in the PR description.
