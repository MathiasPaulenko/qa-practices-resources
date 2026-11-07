# Defect Lifecycle Tracking — Workflow Files

Machine-readable versions of the [Defect Lifecycle Tracking Template](https://qapractices.com/templates/defect-lifecycle-tracking-template/) on QAPractices. Use them to configure your issue tracker instead of copying tables by hand.

## Files

| File | What it contains |
|---|---|
| `jira-workflow.json` | Statuses, status categories, transitions, required fields per transition and the automation rules (block missing build number, auto-close after 48h, SLA warning at 80%). Maps the template's 12 states to a JIRA-style workflow. |
| `sla-targets.json` | Resolution SLA per severity, breach escalation actions, and quality indicator thresholds (reopen rate, SLA compliance, escape rate...). |

## How to use

1. Import or reproduce `jira-workflow.json` in your tracker: JIRA (Settings → Issues → Workflows), Linear, Azure DevOps or YouTrack.
2. Configure each transition's `required_fields` — that's what stops defects reaching verification without a build number or repro steps.
3. Set up the automation rules in `automation_rules` with your tracker's automation engine.
4. Load `sla-targets.json` into your reporting or alerting layer; start with these numbers, then tighten them against your measured cycle times.

## Spanish

La [versión en español](README.es.md) describe los mismos archivos.
