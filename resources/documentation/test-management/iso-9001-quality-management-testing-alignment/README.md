# ISO 9001 Testing Alignment — Companion Files

Companion artifacts for the guide [ISO 9001 Testing Alignment: Quality Management Guide](https://qapractices.com/documentation/iso-9001-quality-management-testing-alignment/).

## What's here

| File | What it is |
|---|---|
| `traceability-matrix-template.csv` | Requirements → test cases → defects matrix with sample rows, including an unfilled "gap" row showing what an audit finding looks like |
| `iso-9001-clause-mapping.csv` | Clause-by-clause worksheet (clauses 4–10) mapping ISO requirements to QA artifacts and evidence |
| `audit-evidence-checklist.md` / `.es.md` | Pre-audit evidence checklist — every item should be producible in under 15 minutes |

## How to use

1. Copy `iso-9001-clause-mapping.csv` and fill the `owner` column — one named person per clause, not "the team".
2. Use `traceability-matrix-template.csv` as the shape for your real RTM; the `linked_defects` column is what auditors check first.
3. Run `audit-evidence-checklist.md` 4–6 weeks before the audit, not the week before — gaps take time to close.

These are templates, not turnkey compliance. Adapt artifact names and IDs to your tracker (Jira, Azure DevOps, TestRail, whatever you use).
