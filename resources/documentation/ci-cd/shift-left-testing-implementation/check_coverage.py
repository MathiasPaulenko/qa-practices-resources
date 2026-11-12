#!/usr/bin/env python3
"""Enforce a coverage floor against a pytest-cov Cobertura XML report.

Usage:
    python check_coverage.py coverage.xml --floor 70

Exits 0 when total line coverage meets the floor, 1 otherwise — drop it
straight into a CI step to make the build gate actually block.
"""

import argparse
import sys
import xml.etree.ElementTree as ET


def line_coverage(path: str) -> float:
    tree = ET.parse(path)
    root = tree.getroot()
    rate = float(root.attrib["line-rate"])
    return rate * 100


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", help="Path to the Cobertura XML report")
    parser.add_argument(
        "--floor", type=float, default=70.0, help="Minimum line coverage %%"
    )
    args = parser.parse_args()

    coverage = line_coverage(args.report)
    print(f"Line coverage: {coverage:.1f}% (floor: {args.floor:.0f}%)")

    if coverage < args.floor:
        print(f"FAIL — coverage {coverage:.1f}% is below the {args.floor:.0f}% floor")
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
