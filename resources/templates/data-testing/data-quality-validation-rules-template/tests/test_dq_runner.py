"""Tests for the data quality check runner.

Each check is exercised against a seeded dataset that contains one defect
per check type, plus a clean dataset that must pass every gate.
"""

import os
import sqlite3
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dq_runner import (  # noqa: E402
    CheckResult,
    check_business_rules,
    check_completeness,
    check_consistency,
    check_format,
    check_min_rows,
    check_range,
    check_referential,
    check_uniqueness,
    run_all,
    section_score,
    seed,
    WEIGHTS,
)


def make_db(clean: bool = False) -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    seed(conn, clean=clean)
    return conn


def by_name(results, name):
    return next(r for r in results if r.name == name)


class LoadGateTests(unittest.TestCase):
    def test_zero_row_load_fails(self):
        conn = sqlite3.connect(":memory:")
        seed(conn, clean=True)
        conn.execute("DELETE FROM orders")
        result = check_min_rows(conn)
        self.assertEqual(result.status, "FAIL")
        self.assertEqual(result.actual, 0)

    def test_loaded_rows_pass(self):
        result = check_min_rows(make_db())
        self.assertEqual(result.status, "PASS")
        self.assertGreater(result.actual, 0)


class CompletenessTests(unittest.TestCase):
    def test_null_critical_column_flagged(self):
        result = by_name(check_completeness(make_db()), "nulls:customer_email")
        self.assertEqual(result.status, "FAIL")
        self.assertEqual(result.actual, 1)

    def test_clean_dataset_all_pass(self):
        for r in check_completeness(make_db(clean=True)):
            self.assertEqual(r.status, "PASS", r.name)


class UniquenessTests(unittest.TestCase):
    def test_duplicate_pk_detected(self):
        result = by_name(check_uniqueness(make_db()), "duplicate:order_id")
        self.assertEqual(result.status, "FAIL")
        self.assertEqual(result.actual, 1)

    def test_clean_dataset_unique(self):
        for r in check_uniqueness(make_db(clean=True)):
            self.assertEqual(r.status, "PASS", r.name)


class FormatTests(unittest.TestCase):
    def test_malformed_email_flagged(self):
        result = by_name(check_format(make_db()), "format:email")
        self.assertEqual(result.status, "FAIL")

    def test_invalid_enum_values_flagged(self):
        results = check_format(make_db())
        self.assertEqual(by_name(results, "enum:order_status").status, "FAIL")
        self.assertEqual(by_name(results, "enum:payment_method").status, "FAIL")


class RangeTests(unittest.TestCase):
    def test_out_of_range_quantity_flagged(self):
        result = check_range(make_db())[0]
        self.assertEqual(result.status, "FAIL")
        self.assertGreaterEqual(result.actual, 1)


class ReferentialTests(unittest.TestCase):
    def test_orphan_customer_detected(self):
        result = check_referential(make_db())[0]
        self.assertEqual(result.status, "FAIL")
        self.assertEqual(result.actual, 1)

    def test_clean_dataset_no_orphans(self):
        self.assertEqual(check_referential(make_db(clean=True))[0].status, "PASS")


class ConsistencyTests(unittest.TestCase):
    def test_paid_total_mismatch_flagged(self):
        result = check_consistency(make_db())[0]
        self.assertEqual(result.status, "FAIL")
        self.assertEqual(result.actual, 1)


class BusinessRuleTests(unittest.TestCase):
    def test_missing_customs_form_flagged(self):
        result = by_name(check_business_rules(make_db()), "BR:intl_customs")
        self.assertEqual(result.status, "FAIL")
        self.assertEqual(result.actual, 1)

    def test_missing_cancel_reason_warns(self):
        result = by_name(check_business_rules(make_db()), "BR:cancel_reason")
        self.assertEqual(result.status, "WARN")
        self.assertEqual(result.actual, 1)


class ScoreTests(unittest.TestCase):
    def test_weighted_score_uses_weights(self):
        scores = {"completeness": 100, "uniqueness": 100, "format": 100,
                  "range": 100, "consistency": 100, "referential": 100,
                  "business_rules": 100}
        overall = sum(WEIGHTS[k] * scores[k] for k in WEIGHTS)
        self.assertAlmostEqual(overall, 100.0)

    def test_section_score_warn_counts_half(self):
        results = [CheckResult("a", 0, "0", "PASS"), CheckResult("b", 1, "0", "WARN")]
        self.assertEqual(section_score(results), 75.0)

    def test_run_all_reports_every_section(self):
        report = run_all(make_db())
        self.assertIn("load_gate", report["sections"])
        self.assertEqual(set(report["scores"]), set(WEIGHTS))
        self.assertLess(report["overall"], 100.0)


if __name__ == "__main__":
    unittest.main()
