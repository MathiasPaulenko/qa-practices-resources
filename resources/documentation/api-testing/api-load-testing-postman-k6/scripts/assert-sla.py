#!/usr/bin/env python3
"""Assert SLA thresholds from k6 JSON output.

Usage:
    python scripts/assert-sla.py results.json

Exits with code 1 if any threshold is breached.
"""
import json
import sys
import argparse


def assert_sla(results_file: str) -> int:
    p95_threshold_ms = 500
    error_rate_threshold = 0.01  # 1%

    with open(results_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    p95_values = []
    error_count = 0
    total_count = 0

    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue

        if entry.get("metric") == "http_req_duration" and "p(95)" in entry.get("data", {}):
            p95_values.append(entry["data"]["p(95)"])

        if entry.get("metric") == "http_req_failed":
            data = entry.get("data", {})
            if "rate" in data:
                error_rate = data["rate"]
                total_count = data.get("count", 0)
                error_count = int(error_rate * total_count) if total_count else 0

    failures = []

    if p95_values:
        max_p95 = max(p95_values)
        if max_p95 > p95_threshold_ms:
            failures.append(f"p95={max_p95}ms exceeds threshold of {p95_threshold_ms}ms")
        else:
            print(f"PASS: p95={max_p95}ms (threshold: {p95_threshold_ms}ms)")
    else:
        print("WARN: no p95 data found in results")

    if total_count > 0:
        actual_error_rate = error_count / total_count
        if actual_error_rate > error_rate_threshold:
            failures.append(
                f"error_rate={actual_error_rate:.4f} exceeds threshold of {error_rate_threshold:.4f}"
            )
        else:
            print(f"PASS: error_rate={actual_error_rate:.4f} (threshold: {error_rate_threshold:.4f})")
    else:
        print("WARN: no error rate data found in results")

    if failures:
        for f in failures:
            print(f"FAIL: {f}")
        return 1

    print("All SLA thresholds passed.")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Assert SLA thresholds from k6 JSON output.")
    parser.add_argument("results_file", help="Path to k6 JSON results file")
    args = parser.parse_args()

    exit_code = assert_sla(args.results_file)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()