#!/usr/bin/env python3
"""Generate a Test Exit Report from test results and open defects.

Requires: Python 3.12+
Usage:
    python generate_exit_report.py --release v2.1.0 \
        --results fixtures/test_results.json \
        --defects fixtures/open_defects.json \
        --output reports/
"""
import argparse
import json
import sys
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path


@dataclass
class TestResult:
    name: str
    status: str  # passed, failed, blocked
    duration_sec: float
    defect_id: str | None = None


@dataclass
class TestExitReport:
    release: str
    generated_at: str
    total_cases: int
    passed: int
    failed: int
    blocked: int
    pass_rate: float
    open_defects: list[dict]
    has_critical: bool
    recommendation: str


def load_results(path: str) -> list[TestResult]:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return [TestResult(**r) for r in data]


def load_defects(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def generate_exit_report(
    release: str, results: list[TestResult], open_defects: list[dict]
) -> TestExitReport:
    total = len(results)
    passed = sum(1 for r in results if r.status == "passed")
    failed = sum(1 for r in results if r.status == "failed")
    blocked = sum(1 for r in results if r.status == "blocked")
    pass_rate = (passed / total * 100) if total else 0.0
    has_critical = any(d.get("severity") == "critical" for d in open_defects)

    recommendation = "Go" if pass_rate >= 95 and not has_critical else "No-Go"

    return TestExitReport(
        release=release,
        generated_at=datetime.now(timezone.utc).isoformat(),
        total_cases=total,
        passed=passed,
        failed=failed,
        blocked=blocked,
        pass_rate=round(pass_rate, 1),
        open_defects=open_defects,
        has_critical=has_critical,
        recommendation=recommendation,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a Test Exit Report.")
    parser.add_argument("--release", required=True, help="Release version, e.g. v2.1.0")
    parser.add_argument("--results", required=True, help="Path to test results JSON")
    parser.add_argument("--defects", required=True, help="Path to open defects JSON")
    parser.add_argument("--output", default=".", help="Output directory for report")
    args = parser.parse_args()

    results = load_results(args.results)
    defects = load_defects(args.defects)
    report = generate_exit_report(args.release, results, defects)

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"test_exit_report_{args.release}.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(asdict(report), f, indent=2)

    print(f"Report generated: {output_file}")
    print(f"Recommendation: {report.recommendation} (pass rate: {report.pass_rate}%)")
    return 0 if report.recommendation == "Go" else 1


if __name__ == "__main__":
    sys.exit(main())
