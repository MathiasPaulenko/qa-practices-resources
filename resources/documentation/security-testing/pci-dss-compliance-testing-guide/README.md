# PCI DSS Compliance Testing — Runnable Controls Kit

Companion to the [PCI DSS Compliance Testing Guide](https://qapractices.com/documentation/pci-dss-compliance-testing-guide/) on QAPractices. Pre-assessment checks you run before the ASV scan and the QSA visit, packaged so every run produces dated evidence for the audit folder.

## What's inside

| Control | PCI DSS req | Script |
|---|---|---|
| PAN sweep — finds Luhn-valid card numbers leaked into logs, responses, and dumps | 3 | `controls/pan_sweep.py` |
| TLS check — negotiated version + weak cipher detection | 4 | `controls/tls_check.py` |
| Segmentation check — proves an out-of-scope segment can't reach the CDE | 11.4.5 | `controls/segmentation_check.py` |
| Evidence pack — runs all checks and writes `evidence/evidence-YYYYMMDD.json` | all | `runner.py` |

Only the standard library is used for the checks themselves — they run on a locked-down jump host without installing anything. `pytest` and `PyYAML` are needed for tests and the config-driven runner.

## Quick start

```bash
pip install -r requirements.txt

# Point the PAN sweep at exported logs or DB dumps
python -m controls.pan_sweep sample_logs/

# Probe a CDE-facing endpoint (replace with your host)
python -m controls.tls_check staging-cde.internal 443

# Run from an out-of-scope segment — every port must be unreachable
python -m controls.segmentation_check cde-app-01.internal
```

## Evidence pack

Edit `controls.yaml` with your real targets, then:

```bash
python runner.py --config controls.yaml
```

Output lands in `evidence/evidence-YYYYMMDD.json` — one file per run, dated, with per-control pass/fail and the details an assessor samples. Run it the week before each quarterly ASV scan and before the annual assessment.

## Tests

```bash
pytest tests/ -v
```

The suite covers the Luhn validator, PAN detection vs false positives, TLS pass/fail rules (weak protocol, weak cipher, connection failure), and segmentation detection against real localhost ports — no live CDE needed.

## What this kit does not do

- It does **not** replace the quarterly ASV scan — external scans must come from a PCI SSC Approved Scanning Vendor.
- It does **not** replace the annual penetration test.
- It does not audit physical access (req 9) or policy artifacts (req 12) — those stay manual.
