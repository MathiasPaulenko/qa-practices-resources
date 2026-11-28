```text
METRIC: Defect Escape Rate
Business question: Are releases leaking bugs into production?
Formula: (prod bugs within 7d of release / total bugs) × 100
Source: Jira — bugs labeled prod-escape; freshness: daily 6am ETL
Visualization: trend line per release + threshold band
Threshold: green <8% · yellow 8-12% · red >12%
Gaming scenario: team stops tagging prod bugs as escapes
Guardrail: monthly sample audit of untagged prod bugs by QA lead
Owner: QA Director

METRIC: Flaky Test Ratio
Business question: Can we trust a green build?
Formula: (tests with ≥1 retry-pass in last 30d / total suite) × 100
Source: GitHub Actions test reporter; freshness: per pipeline run
Visualization: stacked bar per squad, sorted desc
Threshold: green <3% · yellow 3-7% · red >7%
Gaming scenario: deleting flaky tests to improve the ratio
Guardrail: test-count tracked as a paired metric — ratio up with
count down triggers review
Owner: Platform squad lead

MONDAY WORKFLOW
09:00 VP sees: escape rate 9.4% (yellow, trending up 2 releases),
  driver: payment-service flakiness at 8.1% (red) → action: freeze
  new payment tests, assign flaky-test quarantine to platform squad
```
