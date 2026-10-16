# Executive Summary — Sprint 42 quality snapshot

**Primary decision:** where to invest the next unit of QA effort.

## Top risks

1. **Flaky tests are eroding CI trust** — ratio 4.1% vs 2% target; developers rerun suites and merge with uncertainty.
2. **Defect escapes concentrate in payment reconciliation** — 5.2% vs 3% target; the last two production rollbacks both started there.

## Recommended actions

- Quarantine Playwright tests with a pass rate below 85% over the last 14 days; assign an owner before re-enabling.
- Add one exploratory session per release on the payment reconciliation flow — half a day of effort against two rollbacks.

## Quality narrative

Build lead time p90 sits at 14 minutes (target 12) — a drag on iteration, not a release blocker. Coverage delta is green and stable. Quality investment should go to test reliability first: the flaky ratio is the root of the rework loop, and fixing it also shortens perceived build time.
