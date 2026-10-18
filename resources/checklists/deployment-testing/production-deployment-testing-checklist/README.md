# Thorough Production Deployment Checklist — Companion

Companion file for the [Thorough Production Deployment Checklist](https://qapractices.com/checklists/production-deployment-testing-checklist) resource.

The 71 deployment checks ship as one importable CSV so a release manager can drop them into a spreadsheet, a test-management tool or a runbook ticket without retyping.

## Files

| File | Contents |
|---|---|
| `checklist-items.csv` | All 71 checklist items across 10 phases (Pre-Deployment Verification, Infrastructure Readiness, Database Migrations, Configuration Management, Health Checks, Rollback Procedures, Monitoring, Security, Performance, Smoke Tests) with a risk level per item |

## Usage

- Import `checklist-items.csv` as tasks (Jira, TestRail, a spreadsheet) and sort by `area` — run the phases in order.
- Filter by `risk` and treat every `High` as a hard gate: no High item unchecked, no deploy.
- Scale depth to blast radius: a config-only release can skip load testing, never rollback capability or smoke tests.

Site resource: [qapractices.com/checklists/production-deployment-testing-checklist](https://qapractices.com/checklists/production-deployment-testing-checklist)
