import csv
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from regression_selector import (  # noqa: E402
    TestCase,
    assign_tier,
    load_cases,
    tier_summary,
    write_plan,
)

CSV_PATH = Path(__file__).resolve().parents[1] / "test_cases.csv"


def test_weighted_score_matches_formula():
    case = TestCase("TC-001", "Checkout payment", 3, 3, 2, 3, 3)
    assert case.weighted_score == pytest.approx(2.80)


def test_tier_boundaries():
    assert assign_tier(3.00) == "T0"
    assert assign_tier(2.50) == "T0"
    assert assign_tier(2.49) == "T1"
    assert assign_tier(2.00) == "T1"
    assert assign_tier(1.99) == "T2"
    assert assign_tier(1.50) == "T2"
    assert assign_tier(1.49) == "T3"
    assert assign_tier(0.00) == "T3"


def test_load_sample_csv():
    cases = load_cases(str(CSV_PATH))
    assert len(cases) == 10
    by_id = {c.id: c for c in cases}
    assert by_id["TC-001"].weighted_score == pytest.approx(2.80)
    assert by_id["TC-004"].weighted_score == pytest.approx(1.25)


def test_out_of_range_score_rejected(tmp_path):
    bad = tmp_path / "bad.csv"
    bad.write_text("id,feature,bc,dh,ci,au,et\nTC-099,Oops,5,1,1,1,1\n")
    with pytest.raises(ValueError):
        load_cases(str(bad))


def test_tier_summary_counts():
    cases = load_cases(str(CSV_PATH))
    summary = tier_summary(cases)
    assert summary == {"T0": 2, "T1": 3, "T2": 3, "T3": 2}
    assert sum(summary.values()) == len(cases)


def test_write_plan_sorted(tmp_path):
    cases = load_cases(str(CSV_PATH))
    out = tmp_path / "plan.csv"
    write_plan(cases, str(out))
    rows = list(csv.DictReader(out.open()))
    assert rows[0]["id"] == "TC-001"
    assert rows[0]["tier"] == "T0"
    assert rows[-1]["tier"] == "T3"
    scores = [float(r["weighted_score"]) for r in rows]
    assert scores == sorted(scores, reverse=True)
