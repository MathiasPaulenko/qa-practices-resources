# Session-Based Testing Companion

Companion resource for the [Session-Based Testing Guide](https://qapractices.com/documentation/session-based-testing). Contains the working templates you need to run SBTM with zero setup: a charter template, a session report template and a metrics tracker.

## Files

| File | Purpose |
| ---- | ------- |
| `src/charter-template.md` | Charter skeleton with the what/how/why structure and sizing hints. Copy one per session. |
| `src/session-report-template.md` | Full session report format: environment, chronological notes, bugs, issues and coverage checklist. |
| `src/session-metrics.csv` | Metrics tracker: sessions per day, charter completion, bug find rate, setup ratio and test/bug-investigation ratio — with target and red-flag thresholds from the guide. |

## Quick Start

1. Write a charter per session from `charter-template.md` — fill the three lines, then estimate 60-90% of a 90-minute session.
2. During the session, take chronological notes directly in a copy of `session-report-template.md`.
3. Within 24 hours, run the debrief (PROOF: Past, Results, Obstacles, Outlook, Feelings).
4. Log the session in `session-metrics.csv` and watch the red-flag thresholds weekly.

## Requirements

None. Markdown templates open anywhere; the CSV imports into Excel, Google Sheets or your wiki.
