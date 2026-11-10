# Payment PCI-DSS Compliance Testing Checklist — Companion

Companion assets for the QAPractices checklist:
[Payment PCI-DSS Compliance Testing Checklist](https://qapractices.com/checklists/payment-pci-dss-compliance-testing-checklist/)

All items are aligned to **PCI DSS v4.0.1** (the current version; v4.0 was retired on December 31, 2024).

## Contents

| File | Purpose |
|------|---------|
| `checklist.csv` | All 107 items as a spreadsheet — import into Sheets/Excel/Jira and use the `status` and `evidence` columns during the assessment run. |
| `checklist.json` | Same items in structured form for tooling — filter by `section`, `requirement` or `risk`, or pipe into a tracker. |
| `pan_log_check.py` | Stdlib-only scanner that finds Luhn-valid 13-19 digit card numbers in logs and dumps. Maps to the checklist's most common real-world failure: PAN leaking into logs. |

## Usage

Work the checklist in the format that fits the run:

```bash
# open in a spreadsheet and fill evidence/status per item
checklist.csv

# list all High-risk items for a release gate
python -c "import json; [print(i['item']) for i in json.load(open('checklist.json'))['items'] if i['risk']=='High']"
```

Scan logs for PAN leaks (exit code 1 on findings — usable as a CI gate):

```bash
python pan_log_check.py /var/log/myapp/
python pan_log_check.py /var/log/myapp/ --quiet   # summary only
```

The scanner flags Luhn-valid digit sequences. Known test cards (Stripe `4242…`, etc.) are excluded from findings; treat everything else as a Req 3 finding until proven a false positive.

## Notes

- Requirement numbers in `checklist.csv` cite PCI DSS v4.0.1 (e.g., `Req 8.3.4` lockout, `Req 10.5.1` log retention, `Req 11.6.1` payment-page tamper detection).
- Six edge-case items have no single-requirement mapping — they verify general payment hygiene.
- Keep evidence per item (screenshot, test output, config export) — it is what the assessor samples.
