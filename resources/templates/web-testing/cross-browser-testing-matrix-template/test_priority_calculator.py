"""Tests for priority_calculator — traffic-share thresholds and scope mapping."""

import csv
import io

from priority_calculator import SCOPE_BY_PRIORITY, assign_priorities, priority_for

DEFAULT = {"P1": 30.0, "P2": 5.0, "P3": 2.0}


def test_p1_boundary_inclusive():
    assert priority_for(30.0, DEFAULT) == "P1"


def test_p1_above_threshold():
    assert priority_for(65.0, DEFAULT) == "P1"


def test_p2_range():
    assert priority_for(10.0, DEFAULT) == "P2"
    assert priority_for(5.0, DEFAULT) == "P2"


def test_p3_range():
    assert priority_for(2.5, DEFAULT) == "P3"
    assert priority_for(2.0, DEFAULT) == "P3"


def test_p4_below_threshold():
    assert priority_for(1.9, DEFAULT) == "P4"
    assert priority_for(0.1, DEFAULT) == "P4"


def test_custom_thresholds_shift_assignment():
    strict = {"P1": 50.0, "P2": 10.0, "P3": 5.0}
    assert priority_for(30.0, strict) == "P2"
    assert priority_for(42.0, strict) == "P2"
    assert priority_for(51.0, strict) == "P1"


def test_assign_priorities_attaches_scope():
    rows = [{"os": "iOS 17", "browser": "Safari", "traffic_share": "18.7"}]
    out = assign_priorities(rows, DEFAULT)
    assert out[0]["priority"] == "P2"
    assert out[0]["scope"] == SCOPE_BY_PRIORITY["P2"]


def test_sample_csv_assignments():
    with open("traffic-sample.csv", newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    result = {f"{r['os']}/{r['browser']}": r["priority"] for r in assign_priorities(rows, DEFAULT)}
    assert result["Windows 11/Chrome"] == "P1"
    assert result["iOS 17/Safari"] == "P2"
    assert result["Android 14/Samsung Internet"] == "P3"
    assert result["Windows 11/Opera"] == "P4"
