# AI Prompt: Executive QA Metrics Dashboard — Companion

Companion files for the [AI Prompt: Build an Executive QA Metrics Dashboard](https://qapractices.com/prompts/ai-prompt-qa-metrics-dashboard) resource.

## Files

| File | Purpose |
| --- | --- |
| `prompt-template.txt` | The full dashboard design prompt, ready to copy into an LLM. |
| `example-input.txt` | A filled-in context: MedTrack, 12-person QA team, Jira + TestRail + GitHub Actions + Grafana. |
| `example-output.md` | A realistic output fragment: two metric cards (escape rate, flaky ratio) with formulas, thresholds, gaming scenarios and guardrails, plus the Monday workflow. |

## Usage

1. Copy `prompt-template.txt` into your LLM.
2. Fill the context block with your product, data sources, tooling versions and — most importantly — the one weekly decision the dashboard must change.
3. Compare the response shape with `example-output.md`; every metric should carry formula, threshold, gaming scenario and guardrail.
4. Ship the anti-gaming checklist with the dashboard, not after it.
5. Re-run quarterly to recalibrate thresholds against your own baseline.
