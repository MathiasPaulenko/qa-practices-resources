"""Weighted scoring and tier assignment for regression test suite selection.

Reads a CSV of test cases scored on five criteria (each 0-3) and writes a
selection plan with the weighted score and the tier (T0-T3) each case lands in.

Score = BC*0.30 + DH*0.25 + CI*0.20 + AU*0.15 + ET*0.10

Usage:
    python regression_selector.py test_cases.csv selection_plan.csv
"""
from __future__ import annotations

import argparse
import csv
import sys
from dataclasses import dataclass

WEIGHTS = {"bc": 0.30, "dh": 0.25, "ci": 0.20, "au": 0.15, "et": 0.10}

TIER_RANGES = [
    (2.50, 3.00, "T0"),
    (2.00, 2.49, "T1"),
    (1.50, 1.99, "T2"),
    (0.00, 1.49, "T3"),
]


@dataclass
class TestCase:
    id: str
    feature: str
    bc: int
    dh: int
    ci: int
    au: int
    et: int

    @property
    def weighted_score(self) -> float:
        return (
            self.bc * WEIGHTS["bc"]
            + self.dh * WEIGHTS["dh"]
            + self.ci * WEIGHTS["ci"]
            + self.au * WEIGHTS["au"]
            + self.et * WEIGHTS["et"]
        )


def assign_tier(score: float) -> str:
    for low, high, tier in TIER_RANGES:
        if low <= score <= high:
            return tier
    raise ValueError(f"score {score} out of range 0.00-3.00")


def load_cases(path: str) -> list[TestCase]:
    cases: list[TestCase] = []
    with open(path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            try:
                scores = {k: int(row[k].strip()) for k in WEIGHTS}
            except (KeyError, ValueError) as exc:
                raise ValueError(f"bad row for {row.get('id', '?')}: {exc}") from exc
            for key, val in scores.items():
                if not 0 <= val <= 3:
                    raise ValueError(f"{row['id']}: {key}={val} outside 0-3")
            cases.append(
                TestCase(row["id"].strip(), row["feature"].strip(), **scores)
            )
    return cases


def write_plan(cases: list[TestCase], path: str) -> None:
    rows = sorted(cases, key=lambda c: c.weighted_score, reverse=True)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["id", "feature", "weighted_score", "tier"])
        for case in rows:
            writer.writerow(
                [case.id, case.feature, f"{case.weighted_score:.2f}", assign_tier(case.weighted_score)]
            )


def tier_summary(cases: list[TestCase]) -> dict[str, int]:
    counts = {"T0": 0, "T1": 0, "T2": 0, "T3": 0}
    for case in cases:
        counts[assign_tier(case.weighted_score)] += 1
    return counts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_csv", help="CSV with columns id,feature,bc,dh,ci,au,et")
    parser.add_argument("output_csv", help="Where to write the selection plan")
    args = parser.parse_args()

    cases = load_cases(args.input_csv)
    if not cases:
        print("no test cases found", file=sys.stderr)
        return 1
    write_plan(cases, args.output_csv)
    summary = tier_summary(cases)
    print(
        " ".join(f"{tier}:{count}" for tier, count in summary.items())
        + f"  ({len(cases)} total)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
