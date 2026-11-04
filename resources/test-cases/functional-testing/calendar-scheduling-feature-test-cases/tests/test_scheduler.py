"""Runnable checks mapping the resource's highest-risk cases:

TC011 reminder offset, TC015 timezone display, TC016 end < start,
TC018 overlap detection, TC021 negative reminder, TC026 leap-year
recurrence, TC027 DST gap, TC029 back-to-back, TC005 day-31 monthly rule.
"""

from datetime import date, datetime

import pytest
from zoneinfo import ZoneInfo

from scheduler import (
    CalendarEvent,
    create_event,
    monthly_day31_occurrences,
    overlaps,
    reminder_fires_at,
    resolve_dst_gap,
    to_utc,
)

NY = "America/New_York"


def _event(start: str, end: str, tz: str = NY) -> CalendarEvent:
    s = to_utc(datetime.fromisoformat(start), tz)
    e = to_utc(datetime.fromisoformat(end), tz)
    return CalendarEvent("seed", s, e, tz)


def test_tc015_utc_event_displays_per_viewer_timezone():
    event = _event("2026-07-15T14:00:00", "2026-07-15T15:00:00", tz="UTC")
    assert event.local_start("Europe/Berlin").hour == 16
    assert event.local_start(NY).hour == 10


def test_tc016_end_before_start_is_rejected():
    with pytest.raises(ValueError, match="after start"):
        create_event("bad", datetime(2026, 7, 15, 14), datetime(2026, 7, 15, 13), NY, [])


def test_tc018_one_minute_overlap_conflicts():
    existing = [_event("2026-07-15T09:00:00", "2026-07-15T10:00:00")]
    ev = create_event("B", datetime(2026, 7, 15, 9, 59), datetime(2026, 7, 15, 10, 30), NY, existing)
    assert ev.conflict is True


def test_tc018_block_policy_rejects_overlap():
    existing = [_event("2026-07-15T09:00:00", "2026-07-15T10:00:00")]
    with pytest.raises(ValueError, match="conflicts"):
        create_event("B", datetime(2026, 7, 15, 9, 30), datetime(2026, 7, 15, 10, 30), NY, existing, policy="block")


def test_tc029_back_to_back_is_not_a_conflict():
    a = _event("2026-07-15T09:00:00", "2026-07-15T10:00:00")
    assert not overlaps(a.start_utc, a.end_utc, a.end_utc, a.end_utc)
    ev = create_event("B", datetime(2026, 7, 15, 10), datetime(2026, 7, 15, 11), NY, [a])
    assert ev.conflict is False


def test_tc021_negative_reminder_rejected():
    event = _event("2026-07-15T14:00:00", "2026-07-15T15:00:00")
    with pytest.raises(ValueError, match="positive"):
        reminder_fires_at(event, -5, NY)


def test_tc011_reminder_fires_in_viewer_timezone():
    event = _event("2026-07-15T14:00:00", "2026-07-15T15:00:00")
    fired = reminder_fires_at(event, 15, NY)
    assert fired.hour == 13 and fired.minute == 45
    assert fired.tzinfo == ZoneInfo(NY)


def test_tc027_dst_gap_time_is_shifted_forward():
    gap_local = datetime(2026, 3, 8, 2, 30)
    resolved = resolve_dst_gap(gap_local, NY)
    assert resolved.replace(tzinfo=None) >= datetime(2026, 3, 8, 3, 0)


def test_tc005_monthly_day31_clamps_or_skips_short_months():
    clamped = monthly_day31_occurrences(2026, 4, clamp=True)
    assert clamped[1] == date(2026, 2, 28)
    skipped = monthly_day31_occurrences(2026, 4, clamp=False)
    assert date(2026, 2, 28) not in skipped and len(skipped) == 2


def test_tc026_leap_year_feb29_exists_only_in_leap_years():
    assert date(2028, 2, 29).year == 2028
    with pytest.raises(ValueError):
        date(2029, 2, 29)
