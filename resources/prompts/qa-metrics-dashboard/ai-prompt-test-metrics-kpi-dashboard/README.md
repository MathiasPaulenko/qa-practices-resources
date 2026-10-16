# AI Prompt: Test Metrics and KPI Dashboard — Sample Output Pack

Companion to the QAPractices resource [AI Prompt: Build a Test Metrics and KPI Dashboard](https://qapractices.com/prompts/ai-prompt-test-metrics-kpi-dashboard/).

The reference output the prompt should produce for the guide's Example Input (healthtech API team: 4 QA, 12 devs, 2 SDETs, weekly releases, GitHub Actions, Playwright 1.42, Jira Cloud, Datadog, Grafana 10).

## Files

```text
├── grafana-dashboard.json   # Grafana 10 dashboard skeleton: 5 panels, targets, thresholds, 4-week window
├── executive-summary.md     # Filled one-page executive summary from the guide's template
├── meta.json
└── README.es.md
```

## Mapping to the guide

| Guide section | File | What it shows |
|---|---|---|
| Example Output — metric table | `grafana-dashboard.json` | The 5 metrics as Grafana panels with thresholds and the 28-day trend window |
| Example Output — executive summary | `executive-summary.md` | The narrative format: top risks, recommended actions, plain-language story |

## Usage

Import `grafana-dashboard.json` in Grafana (Dashboards → New → Import) and rewire the `expr` fields to your real data sources — the expressions are placeholders matching Jira/GitHub Actions/Datadog-shaped metrics. `executive-summary.md` is meant to be copied and filled per sprint.

## Notes

- Versions aligned with the article: Grafana 10, Playwright 1.42.
- Spanish version: `README.es.md`.
