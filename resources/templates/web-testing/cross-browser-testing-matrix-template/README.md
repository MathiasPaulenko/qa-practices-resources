# Cross-Browser Testing Matrix Template — Companion

Ready-to-fill CSV of the browser matrix plus a small script that assigns
P1–P4 priorities from real traffic-share numbers — the same decision the
template's Section 1.3 encodes.

## Files

| File | What it is |
|---|---|
| `browser-matrix-template.csv` | Empty matrix (P1/P2/P3 columns) ready to import into a spreadsheet or test-management tool |
| `priority_calculator.py` | stdlib-only script: traffic share % → priority tier + recommended test scope |
| `traffic-sample.csv` | Sample traffic-share export the calculator reads |
| `test_priority_calculator.py` | pytest suite covering thresholds and scope mapping |

## Run

```bash
python priority_calculator.py traffic-sample.csv
```

```text
os,browser,version,viewport,device,traffic_share,priority,scope
Windows 11,Chrome,Latest,1920x1080,Desktop,42.5,P1,Full regression every release (CI) + real-device spot-check
macOS 14,Safari,Latest,1440x900,Desktop,11.2,P2,Smoke plus targeted regression (automated weekly)
iOS 17,Safari,Latest,390x844,Mobile (iPhone 15),18.7,P2,Smoke plus targeted regression (automated weekly)
Android 14,Chrome,Latest,360x800,Mobile (Pixel 8),14.1,P2,Smoke plus targeted regression (automated weekly)
Windows 11,Edge,Latest,1920x1080,Desktop,5.3,P2,Smoke plus targeted regression (automated weekly)
Windows 11,Firefox,Latest,1920x1080,Desktop,3.9,P3,Smoke only (monthly / quarterly)
Android 14,Samsung Internet,Latest,360x800,Mobile (Galaxy S24),2.8,P3,Smoke only (monthly / quarterly)
Windows 11,Opera,Latest,1920x1080,Desktop,1.5,P4,Not actively tested (user reports only)
```

Custom thresholds if your traffic distribution differs:

```bash
python priority_calculator.py traffic-sample.csv --p1 40 --p2 10 --p3 3
```

```bash
pytest test_priority_calculator.py
```

Back to the template: https://qapractices.com/templates/cross-browser-testing-matrix-template/
