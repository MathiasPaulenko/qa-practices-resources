"""Data quality check runner for the validation rules template.

Runs the eight check types from the register against a SQLite database:
completeness, uniqueness, format, range, referential integrity,
consistency, business rules, and a weighted DQ score plus a min-rows
load gate. Everything runs on the standard library so it executes
anywhere Python 3.9+ is available.
"""

from __future__ import annotations

import re
import sqlite3
from dataclasses import dataclass

ALLOWED_STATUS = {"pending", "paid", "shipped", "delivered", "cancelled", "refunded"}
ALLOWED_METHODS = {"credit_card", "paypal", "apple_pay", "google_pay", "bank_transfer"}
CRITICAL_COLUMNS = ("order_id", "customer_id", "order_date", "customer_email")

WEIGHTS = {
    "completeness": 0.20,
    "uniqueness": 0.15,
    "format": 0.15,
    "range": 0.15,
    "consistency": 0.15,
    "referential": 0.10,
    "business_rules": 0.10,
}

STATUS_PASS, STATUS_WARN, STATUS_FAIL = "PASS", "WARN", "FAIL"


@dataclass
class CheckResult:
    name: str
    actual: int | float
    threshold: str
    status: str


def status_for(count: int, warn_at: int = 0) -> str:
    if count == 0:
        return STATUS_PASS
    if count <= warn_at:
        return STATUS_WARN
    return STATUS_FAIL


def seed(conn: sqlite3.Connection, clean: bool = False) -> None:
    """Load a small orders dataset; `clean=False` seeds one defect per check type."""
    conn.executescript(
        """
        CREATE TABLE customers(
            customer_id INTEGER PRIMARY KEY,
            email TEXT, phone TEXT, tier TEXT
        );
        CREATE TABLE orders(
            order_id INTEGER, customer_id INTEGER, order_date TEXT,
            customer_email TEXT, order_status TEXT, payment_method TEXT,
            quantity INTEGER, total_amount REAL, amount_paid REAL,
            shipping_country TEXT, customs_form INTEGER,
            cancelled_reason TEXT
        );
        """
    )
    conn.executemany(
        "INSERT INTO customers VALUES (?,?,?,?)",
        [
            (i, f"customer{i}@qapractices.dev", f"+1555000{i:03d}", "gold" if i == 1 else "bronze")
            for i in range(1, 11)
        ],
    )
    base_orders = []
    for i in range(1, 21):
        cust = (i % 10) + 1
        base_orders.append(
            (
                100 + i, cust, "2026-07-14", f"customer{cust}@qapractices.dev",
                "paid", "credit_card", 2, 50.0, 50.0, "US", 0, None,
            )
        )
    conn.executemany("INSERT INTO orders VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", base_orders)

    if clean:
        return

    defects = [
        # null on a critical column (completeness)
        (121, 2, "2026-07-14", None, "paid", "credit_card", 1, 30.0, 30.0, "US", 0, None),
        # duplicate PK + duplicate natural key (uniqueness)
        (103, 3, "2026-07-14", "customer3@qapractices.dev", "paid", "paypal", 1, 25.0, 25.0, "US", 0, None),
        # malformed email (format)
        (122, 4, "2026-07-14", "not-an-email", "paid", "credit_card", 1, 20.0, 20.0, "US", 0, None),
        # quantity below range (range)
        (123, 5, "2026-07-14", "customer5@qapractices.dev", "paid", "credit_card", 0, 40.0, 40.0, "US", 0, None),
        # invalid enum values (format/enums)
        (124, 6, "2026-07-14", "customer6@qapractices.dev", "processing", "check", 1, 60.0, 60.0, "US", 0, None),
        # orphan FK — customer 999 does not exist (referential)
        (125, 999, "2026-07-14", "ghost@qapractices.dev", "paid", "credit_card", 1, 15.0, 15.0, "US", 0, None),
        # total mismatch: paid but amount_paid differs (consistency)
        (126, 7, "2026-07-14", "customer7@qapractices.dev", "paid", "credit_card", 1, 100.0, 90.0, "US", 0, None),
        # international order without customs form (business rule)
        (127, 8, "2026-07-14", "customer8@qapractices.dev", "paid", "credit_card", 1, 80.0, 80.0, "DE", 0, None),
        # cancelled without a reason (business rule)
        (128, 9, "2026-07-14", "customer9@qapractices.dev", "cancelled", "credit_card", 1, 35.0, 0.0, "US", 0, None),
    ]
    conn.executemany("INSERT INTO orders VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", defects)


def check_min_rows(conn) -> CheckResult:
    count = conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
    return CheckResult("min_rows_loaded", count, "> 0", STATUS_PASS if count > 0 else STATUS_FAIL)


def check_completeness(conn) -> list[CheckResult]:
    results = []
    for col in CRITICAL_COLUMNS:
        n = conn.execute(f"SELECT COUNT(*) FROM orders WHERE {col} IS NULL").fetchone()[0]
        results.append(CheckResult(f"nulls:{col}", n, "0", status_for(n)))
    return results


def check_uniqueness(conn) -> list[CheckResult]:
    dup_pk = conn.execute(
        "SELECT COUNT(*) - COUNT(DISTINCT order_id) FROM orders"
    ).fetchone()[0]
    dup_email = conn.execute(
        """SELECT COUNT(*) FROM (
               SELECT email FROM customers WHERE email IS NOT NULL
               GROUP BY email HAVING COUNT(*) > 1)"""
    ).fetchone()[0]
    return [
        CheckResult("duplicate:order_id", dup_pk, "0", status_for(dup_pk)),
        CheckResult("duplicate:email", dup_email, "0", status_for(dup_email)),
    ]


EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def check_format(conn) -> list[CheckResult]:
    rows = conn.execute(
        "SELECT customer_email, order_status, payment_method FROM orders"
    ).fetchall()
    bad_email = sum(1 for e, _, _ in rows if e is not None and not EMAIL_RE.match(e))
    bad_status = sum(1 for _, s, _ in rows if s not in ALLOWED_STATUS)
    bad_method = sum(1 for _, _, m in rows if m not in ALLOWED_METHODS)
    return [
        CheckResult("format:email", bad_email, "0", status_for(bad_email)),
        CheckResult("enum:order_status", bad_status, "0", status_for(bad_status)),
        CheckResult("enum:payment_method", bad_method, "0", status_for(bad_method)),
    ]


def check_range(conn) -> list[CheckResult]:
    out = conn.execute(
        """SELECT COUNT(*) FROM orders
           WHERE quantity < 1 OR quantity > 999 OR total_amount < 0.01"""
    ).fetchone()[0]
    return [CheckResult("range:quantity+total", out, "0", status_for(out))]


def check_referential(conn) -> list[CheckResult]:
    orphans = conn.execute(
        """SELECT COUNT(*) FROM orders o
           LEFT JOIN customers c ON o.customer_id = c.customer_id
           WHERE c.customer_id IS NULL"""
    ).fetchone()[0]
    return [CheckResult("orphans:orders.customer_id", orphans, "0", status_for(orphans))]


def check_consistency(conn) -> list[CheckResult]:
    mismatch = conn.execute(
        """SELECT COUNT(*) FROM orders
           WHERE order_status = 'paid' AND ABS(total_amount - amount_paid) > 0.01"""
    ).fetchone()[0]
    return [CheckResult("consistency:paid_total", mismatch, "0", status_for(mismatch))]


def check_business_rules(conn) -> list[CheckResult]:
    customs = conn.execute(
        """SELECT COUNT(*) FROM orders
           WHERE shipping_country NOT IN ('US','CA','MX') AND customs_form = 0"""
    ).fetchone()[0]
    reasons = conn.execute(
        """SELECT COUNT(*) FROM orders
           WHERE order_status = 'cancelled' AND cancelled_reason IS NULL"""
    ).fetchone()[0]
    return [
        CheckResult("BR:intl_customs", customs, "0", status_for(customs)),
        CheckResult("BR:cancel_reason", reasons, "0", status_for(reasons, warn_at=2)),
    ]


def section_score(results: list[CheckResult]) -> float:
    if not results:
        return 100.0
    passed = sum(1 for r in results if r.status == STATUS_PASS)
    warned = sum(1 for r in results if r.status == STATUS_WARN)
    return round(100.0 * (passed + 0.5 * warned) / len(results), 1)


def run_all(conn) -> dict:
    sections = {
        "load_gate": [check_min_rows(conn)],
        "completeness": check_completeness(conn),
        "uniqueness": check_uniqueness(conn),
        "format": check_format(conn),
        "range": check_range(conn),
        "referential": check_referential(conn),
        "consistency": check_consistency(conn),
        "business_rules": check_business_rules(conn),
    }
    scores = {k: section_score(v) for k, v in sections.items() if k in WEIGHTS}
    overall = round(sum(WEIGHTS[k] * scores[k] for k in WEIGHTS), 1)
    return {"sections": sections, "scores": scores, "overall": overall}


def main() -> int:
    conn = sqlite3.connect(":memory:")
    seed(conn, clean=False)
    report = run_all(conn)
    for name, results in report["sections"].items():
        for r in results:
            print(f"[{r.status}] {name}/{r.name}: actual={r.actual} threshold={r.threshold}")
    print(f"\nDimension scores: {report['scores']}")
    print(f"Overall DQ score: {report['overall']}")
    failed = any(
        r.status == STATUS_FAIL
        for results in report["sections"].values()
        for r in results
    )
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
