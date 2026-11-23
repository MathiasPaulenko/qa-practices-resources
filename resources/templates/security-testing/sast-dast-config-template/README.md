# SAST/DAST Configuration Template — Companion

Source article: [SAST/DAST Configuration Template](https://qapractices.com/templates/sast-dast-config-template/)

Two files, ready to drop into a repository:

- `scan-config-template.yaml` — the blank configuration document with placeholders for every decision (tool inventory, rule sets, severity thresholds, exclusions, scan scope, CI gate, triage).
- `scan-config-sample.yaml` — the same document filled out for a fictional fintech payments API running Semgrep 1.99 (SAST on PRs) and OWASP ZAP 2.16 (baseline + nightly api-scan on staging).

## Usage

1. Copy `scan-config-template.yaml` into your repo — `security/scan-config.yaml` is a common home.
2. Replace every `[bracketed]` placeholder. Keep the `owner` and `last review` lines honest.
3. Diff it against `scan-config-sample.yaml` to see what "done" looks like.
4. Changes go through PR review — this file is policy, not documentation.
