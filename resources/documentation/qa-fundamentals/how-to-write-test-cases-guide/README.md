# How to Write Test Cases — Nimbus Cart Suite

Companion for [How to Write Test Cases: From Scenarios to Steps](https://qapractices.com/documentation/how-to-write-test-cases-guide/) on QAPractices.

```text
nimbus-cart-3-2-6-test-cases.csv   the 8 worked cases (TC-EC-02-001..005, TC-EC-03-001..003)
test-case-template.md              reusable template with the same fields
```

## Import the suite

The CSV uses a TestRail/Xray-friendly layout: `ID, Title, Scenario ID, Requirement, Priority, Tags, Preconditions, Steps, Expected Result, Actual Result, Status`. Import it into your TMS as-is, or copy rows into the template when writing new cases.

## Traceability chain

Each row maps `REQ-EC-xx` (requirement) → `SC-EC-xx` (scenario) → `TC-EC-xx-NNN` (case) — the same chain the guide builds step by step. Use it to see how requirement-level coverage reporting works in practice.

Nimbus Cart 3.2.6 is a fictional grocery app; all users, environments and data are illustrative.
