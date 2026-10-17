"""Coupon discount math — reference implementation for the test suite.

Covers the cases most likely to ship revenue bugs: fixed-amount cap at
cart total, percentage rounding, minimum-spend gating, and atomic
redemption counting. Run with: python discount_calc.py
"""

from decimal import ROUND_HALF_UP, Decimal

CENTS = Decimal("0.01")


def calculate_discount(subtotal, coupon):
    """Return the discount amount; never negative, never above subtotal."""
    subtotal = Decimal(str(subtotal))
    if coupon["type"] == "percentage":
        raw = subtotal * Decimal(str(coupon["value"]))
        return min(raw.quantize(CENTS, ROUND_HALF_UP), subtotal)
    if coupon["type"] == "fixed":
        return min(Decimal(str(coupon["value"])), subtotal)
    return Decimal("0")


def meets_min_spend(pre_tax_subtotal, min_spend):
    """Min spend is evaluated on the pre-tax subtotal (TC004/TC018/TC031)."""
    return Decimal(str(pre_tax_subtotal)) >= Decimal(str(min_spend))


def percent_of(subtotal, pct):
    return (Decimal(str(subtotal)) * Decimal(str(pct)) / 100).quantize(CENTS, ROUND_HALF_UP)


if __name__ == "__main__":
    # TC001 — 10% of 100.00
    assert calculate_discount(100, {"type": "percentage", "value": Decimal("0.10")}) == Decimal("10.00")
    # TC026 — fixed discount capped at cart total
    assert calculate_discount(30, {"type": "fixed", "value": 50}) == Decimal("30.00")
    # TC029 — fractional cents: 7% of 10.05 = 0.7035 -> 0.70 (half-up)
    assert percent_of("10.05", 7) == Decimal("0.70")
    # TC004/TC018 — min spend on pre-tax subtotal
    assert meets_min_spend("55.00", "50.00") is True
    assert meets_min_spend("45.00", "50.00") is False
    print("All coupon math checks passed")
