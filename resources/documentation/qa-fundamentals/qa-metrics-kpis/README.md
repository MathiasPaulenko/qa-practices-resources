# QA Metrics and KPIs — Companion

This companion provides runnable files for the [QA Metrics and KPIs: What to Track and Why](https://qapractices.com/documentation/qa-metrics-kpis) guide.

## Files

| File | Purpose |
|------|---------|
| `data/bugs.csv` | Sample bug-tracker export (60 rows: environment, priority, module, created/closed dates) |
| `scripts/metrics_report.py` | Computes defect escape rate and MTTR for P1/P2 defects |
| `scripts/defect_density.py` | Defect density per module (defects per KLOC) — the hotspot finder |
| `requirements.txt` | `pandas` only |

## Quick Start

```bash
pip install -r requirements.txt
python scripts/metrics_report.py
python scripts/defect_density.py
```

Expected output (against the sample data):

```text
Defect Escape Rate: 20.0%  (12/60 bugs reached production)
MTTR (P1/P2): 1.6 days  (n=43)

Density by module:
  auth       3.38 defects/KLOC (27 defects)  <- hotspot
  profile    1.33 defects/KLOC (8 defects)   <- hotspot
  checkout   0.87 defects/KLOC (13 defects)
  search     0.55 defects/KLOC (12 defects)
```

## Notes

Swap `data/bugs.csv` for a real export from Jira, Linear or Azure DevOps —
keep the same column names (`environment`, `priority`, `module`,
`created_date`, `closed_date`) and both scripts work unchanged.

The numbers in the guide's NorthLoop scenario are illustrative; these files
are the real, runnable machinery behind the dashboard.
