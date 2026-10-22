"""Tests for the billing reference functions (mirrors the site's test cases)."""

from datetime import date

import pytest

from conftest import (
    Ledger,
    cancel_state,
    dunning_schedule,
    prorate,
    trial_status,
    upgrade_proration,
)


# --- Proration ------------------------------------------------------------

def test_prorate_upgrade_mid_cycle():
    r = upgrade_proration(old_cents=1000, new_cents=3000, days_remaining=15, cycle_days=30)
    assert r["credit"] == 500
    assert r["charge"] == 1500
    assert r["net"] == 1000  # customer pays a net $10.00


def test_prorate_last_day_of_cycle():
    r = upgrade_proration(old_cents=1000, new_cents=3000, days_remaining=0, cycle_days=30)
    assert r == {"credit": 0, "charge": 0, "net": 0}


def test_prorate_first_day_of_cycle():
    r = upgrade_proration(old_cents=1000, new_cents=3000, days_remaining=30, cycle_days=30)
    assert r["net"] == 2000  # full difference


def test_prorate_rounds_half_up():
    # $9.99 * 1/3 days -> 333.0 -> 333 cents; a float impl would drift
    assert prorate(999, days_remaining=10, cycle_days=30) == 333


def test_prorate_invalid_window_rejected():
    with pytest.raises(ValueError):
        prorate(1000, days_remaining=-1, cycle_days=30)
    with pytest.raises(ValueError):
        prorate(1000, days_remaining=5, cycle_days=0)


def test_annual_to_monthly_credit():
    # $100/yr, ~8 months unused -> 243/365 days of credit = $66.58
    credit = prorate(10000, days_remaining=243, cycle_days=365)
    assert credit == 6658


# --- Dunning --------------------------------------------------------------

def test_dunning_schedule_day_1_3_5():
    r = dunning_schedule("2026-10-01", retries=[1, 3, 5])
    assert r == ["2026-10-02", "2026-10-04", "2026-10-06"]


def test_dunning_schedule_empty():
    assert dunning_schedule("2026-10-01", retries=[]) == []


# --- Webhook idempotency --------------------------------------------------

def test_duplicate_webhook_is_noop():
    ledger = Ledger()
    assert ledger.apply("evt_1", "charge", 3000) is True
    assert ledger.apply("evt_1", "charge", 3000) is False
    assert ledger.charges == [3000]
    assert "duplicate:evt_1" in ledger.log


def test_out_of_order_events_reconcile():
    ledger = Ledger()
    ledger.apply("evt_paid", "charge", 3000)     # paid arrives first
    ledger.apply("evt_created", "charge", 0)     # created arrives second
    assert len(ledger.applied_events) == 2


def test_charge_and_credit_independent():
    ledger = Ledger()
    ledger.apply("evt_charge", "charge", 3000)
    ledger.apply("evt_refund", "credit", 1500)
    assert ledger.charges == [3000]
    assert ledger.credits == [1500]


# --- Trial and cancel state ----------------------------------------------

def test_trial_active_before_end():
    assert trial_status(date(2026, 10, 15), date(2026, 10, 10), has_card=False) == "trialing"


def test_trial_expired_without_card_suspends():
    assert trial_status(date(2026, 10, 1), date(2026, 10, 2), has_card=False) == "suspended"


def test_trial_expired_with_card_activates():
    assert trial_status(date(2026, 10, 1), date(2026, 10, 2), has_card=True) == "active"


def test_cancel_immediate():
    assert cancel_state(False, date(2026, 11, 1), date(2026, 10, 15)) == "cancelled"


def test_cancel_at_period_end_keeps_access():
    assert cancel_state(True, date(2026, 11, 1), date(2026, 10, 15)) == "canceling"
    assert cancel_state(True, date(2026, 11, 1), date(2026, 11, 2)) == "cancelled"
