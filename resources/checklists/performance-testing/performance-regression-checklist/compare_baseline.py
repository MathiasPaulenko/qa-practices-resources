#!/usr/bin/env python3
"""Compare a candidate metrics JSON against a stored baseline.

Baseline format (produced by your load tool or extracted from APM):

    {
      "release": "v1.9.0",
      "metrics": {
        "checkout": {"p50": 120, "p95": 340, "error_rate": 0.001, "rps": 52},
        "search":   {"p50": 210, "p95": 640, "error_rate": 0.002, "rps": 48}
      }
    }

Exit code 1 when any endpoint regresses beyond --max-degradation
(relative, for latency) or --max-error-rate (absolute ceiling).

Usage:
    python compare_baseline.py \
        --baseline baselines/v1.9.0.json \
        --candidate results/candidate.json \
        --max-degradation 0.10 --max-error-rate 0.005
"""

import argparse
import json
import sys


def load(path: str) -> dict:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--baseline", required=True)
    ap.add_argument("--candidate", required=True)
    ap.add_argument("--max-degradation", type=float, default=0.10,
                    help="Max allowed relative latency regression (default 10%%)")
    ap.add_argument("--max-error-rate", type=float, default=0.005,
                    help="Absolute error-rate ceiling (default 0.5%%)")
    args = ap.parse_args()

    baseline = load(args.baseline)["metrics"]
    candidate = load(args.candidate)["metrics"]

    failures = []
    for endpoint, base in baseline.items():
        cand = candidate.get(endpoint)
        if cand is None:
            print(f"WARN  {endpoint}: missing in candidate run")
            continue
        for metric in ("p50", "p95", "p99"):
            if metric in base and metric in cand and base[metric]:
                delta = (cand[metric] - base[metric]) / base[metric]
                flag = "FAIL" if delta > args.max_degradation else "ok  "
                print(f"{flag} {endpoint:12} {metric}: {base[metric]} -> {cand[metric]} ms ({delta:+.1%})")
                if delta > args.max_degradation:
                    failures.append(f"{endpoint} {metric} regressed {delta:+.1%} (> {args.max_degradation:.0%})")
        if "error_rate" in cand and cand["error_rate"] > args.max_error_rate:
            failures.append(f"{endpoint} error_rate {cand['error_rate']:.3%} > {args.max_error_rate:.1%}")

    if failures:
        print("\nPERF GATE: FAIL")
        for f in failures:
            print(" -", f)
        return 1
    print("\nPERF GATE: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
