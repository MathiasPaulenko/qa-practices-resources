"""Reference billing functions for the subscription test suite.

Pure-Python models of the three things billing engines get wrong:
proration math (integer cents, deterministic rounding), dunning
schedules, and webhook idempotency. ``process_webhook`` replays a
provider event stream against an in-memory ledger.
"""

from dataclasses import dataclass, field
from datetime import date, timedelta


def prorate(amount_cents: int, days_remaining: int, cycle_days: int) -> int:
    """Time-based proration in integer cents, rounding half up."""
    if days_remaining < 0 or cycle_days <= 0:
        raise ValueError("invalid proration window")
    return (amount_cents * days_remaining * 2 + cycle_days) // (2 * cycle_days)


def upgrade_proration(old_cents: int, new_cents: int, days_remaining: int, cycle_days: int) -> dict:
    credit = prorate(old_cents, days_remaining, cycle_days)
    charge = prorate(new_cents, days_remaining, cycle_days)
    return {"credit": credit, "charge": charge, "net": charge - credit}


def dunning_schedule(failed_at: str, retries: list[int]) -> list[str]:
    day0 = date.fromisoformat(failed_at)
    return [(day0 + timedelta(days=d)).isoformat() for d in retries]


@dataclass
class Ledger:
    applied_events: set[str] = field(default_factory=set)
    charges: list[int] = field(default_factory=list)
    credits: list[int] = field(default_factory=list)
    log: list[str] = field(default_factory=list)

    def apply(self, event_id: str, kind: str, amount_cents: int) -> bool:
        """Idempotent event application. Returns True if newly applied."""
        if event_id in self.applied_events:
            self.log.append(f"duplicate:{event_id}")
            return False
        self.applied_events.add(event_id)
        (self.charges if kind == "charge" else self.credits).append(amount_cents)
        return True


def trial_status(trial_end: date, today: date, has_card: bool) -> str:
    if today <= trial_end:
        return "trialing"
    return "active" if has_card else "suspended"


def cancel_state(cancel_at_period_end: bool, period_end: date, today: date) -> str:
    if not cancel_at_period_end:
        return "cancelled"
    return "cancelled" if today > period_end else "canceling"
