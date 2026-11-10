# Test Automation ROI Calculator — Companion

Runnable version of the [ROI calculator template](https://qapractices.com/templates/test-automation-roi-calculator-template/): a dependency-free Python script plus a CSV that mirrors Sections 1–2 of the template.

## Files

- `roi_calculator.py` — computes projected savings, ROI metrics, and the ±20% sensitivity table.
- `inputs.csv` — the worked e-commerce example (500 cases, 80% automated, 2 runs/release). Edit the values and re-run to model your own suite.

## Usage

```bash
python roi_calculator.py            # runs the built-in worked example
python roi_calculator.py inputs.csv # runs your own numbers
```

Expected output for the shipped example: $128,000 manual cost eliminated, $176,000 gross savings, $159,500 net, payback 2.7 months, first-year ROI 343%.

## Notes

- Automated execution has no labor line — CI runs are machine time. If you pay per runner-minute, extend `Inputs` with an execution cost.
- Maintenance is modeled as annual engineer hours (15–25% of the initial effort is a sane range).
