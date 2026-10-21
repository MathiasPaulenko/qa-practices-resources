"""Executable subset of the article's recurring-event cases (TC001-TC030)."""

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import pytest
from dateutil.rrule import rrulestr

from rrule_engine import (
    RRULEValidationError,
    build_ruleset,
    occurrences_in_range,
)

DT = datetime(2026, 1, 1, 9, 0)
NY = ZoneInfo("America/New_York")


# --- expansion basics --------------------------------------------------------

def test_tc001_daily_count_ten():
    rs = build_ruleset("FREQ=DAILY;COUNT=10", DT)
    occ = list(rs)
    assert len(occ) == 10
    assert occ[0] == DT
    assert occ[-1] == DT + timedelta(days=9)


def test_tc002_weekly_byday():
    rs = build_ruleset("FREQ=WEEKLY;BYDAY=MO,WE,FR;COUNT=6", DT)
    occ = list(rs)
    assert len(occ) == 6
    assert all(o.weekday() in (0, 2, 4) for o in occ)


def test_tc003_monthly_bymonthday():
    rs = build_ruleset("FREQ=MONTHLY;BYMONTHDAY=15;COUNT=6", DT)
    assert all(o.day == 15 for o in rs)


def test_tc004_yearly_xmas():
    rs = build_ruleset("FREQ=YEARLY;BYMONTH=12;BYMONTHDAY=25;COUNT=5", DT)
    assert all((o.month, o.day) == (12, 25) for o in rs)


def test_tc005_until_bound():
    start = datetime(2026, 1, 1, 9, 0, tzinfo=ZoneInfo("UTC"))  # Z-terminated UNTIL requires aware DTSTART
    rs = build_ruleset("FREQ=DAILY;UNTIL=20260110T235959Z", start)
    occ = list(rs)
    assert occ[-1].date().isoformat() == "2026-01-10"


def test_tc006_interval_two_weeks():
    rs = build_ruleset("FREQ=WEEKLY;INTERVAL=2;COUNT=5", DT)
    occ = list(rs)
    assert all((b - a).days == 14 for a, b in zip(occ, occ[1:]))


def test_tc007_range_query_only():
    rs = build_ruleset("FREQ=DAILY;COUNT=365", DT)
    occ = occurrences_in_range(rs, datetime(2026, 1, 15), datetime(2026, 1, 20, 23, 59, 59))
    assert len(occ) == 6
    assert all(datetime(2026, 1, 15) <= o <= datetime(2026, 1, 21) for o in occ)


# --- negative / conflict cases ----------------------------------------------

def test_tc011_monthly_31_skips_short_months():
    rs = build_ruleset("FREQ=MONTHLY;BYMONTHDAY=31;COUNT=12", DT)
    assert all(o.month in (1, 3, 5, 7, 8, 10, 12) for o in rs)


def test_tc012_feb29_leap_years_only():
    rs = build_ruleset("FREQ=YEARLY;BYMONTH=2;BYMONTHDAY=29;COUNT=10", DT)
    years = [o.year for o in rs]
    assert all(y % 4 == 0 for y in years)


def test_tc017_invalid_freq_rejected():
    with pytest.raises(RRULEValidationError):
        build_ruleset("FREQ=INVALID;COUNT=5", DT)


def test_tc018_count_plus_until_rejected():
    with pytest.raises(RRULEValidationError, match="mutually exclusive"):
        build_ruleset("FREQ=DAILY;COUNT=10;UNTIL=20261231T000000Z", DT)


def test_until_before_dtstart_rejected():
    with pytest.raises(RRULEValidationError, match="UNTIL predates"):
        build_ruleset(
            "FREQ=DAILY;UNTIL=20260101T000000Z", datetime(2026, 3, 1, tzinfo=None)
        )


# --- DST ---------------------------------------------------------------------

def test_tc013_spring_forward_keeps_wall_clock():
    start = datetime(2026, 3, 6, 9, 0, tzinfo=NY)
    rs = build_ruleset("FREQ=DAILY;COUNT=5", start)
    occ = list(rs)
    assert all(o.astimezone(NY).hour == 9 for o in occ)
    assert occ[0].utcoffset() != occ[-1].utcoffset()


def test_tc014_fall_back_keeps_wall_clock():
    start = datetime(2026, 10, 30, 9, 0, tzinfo=NY)
    rs = build_ruleset("FREQ=DAILY;COUNT=5", start)
    occ = list(rs)
    assert all(o.astimezone(NY).hour == 9 for o in occ)
    assert occ[0].utcoffset() != occ[-1].utcoffset()


# --- exdates and series behaviour -------------------------------------------

def test_tc010_exdate_removes_one():
    all_occ = list(rrulestr("FREQ=DAILY;COUNT=10", dtstart=DT))
    rs = build_ruleset("FREQ=DAILY;COUNT=10", DT, exdates=[all_occ[4]])
    assert len(list(rs)) == 9
    assert all_occ[4] not in rs


def test_tc029_visible_count_after_two_exdates():
    all_occ = list(rrulestr("FREQ=DAILY;COUNT=10", dtstart=DT))
    rs = build_ruleset("FREQ=DAILY;COUNT=10", DT, exdates=[all_occ[2], all_occ[6]])
    assert len(list(rs)) == 8


def test_tc020_infinite_recurrence_bounded_query():
    rs = build_ruleset("FREQ=DAILY", DT)
    occ = occurrences_in_range(rs, datetime(2027, 1, 1), datetime(2027, 1, 7, 23, 59, 59))
    assert len(occ) == 7


def test_tc021_backdated_series_spans_past_and_future():
    start = DT - timedelta(days=30)
    rs = build_ruleset("FREQ=DAILY;COUNT=60", start)
    occ = list(rs)
    assert len(occ) == 60
    assert occ[0] < DT < occ[-1]


def test_tc022_byday_bymonthday_intersection():
    rs = build_ruleset("FREQ=MONTHLY;BYDAY=MO;BYMONTHDAY=15;COUNT=5", DT)
    assert all(o.day == 15 and o.weekday() == 0 for o in rs)


def test_tc023_bysetpos_last_monday():
    rs = build_ruleset("FREQ=MONTHLY;BYDAY=MO;BYSETPOS=-1;COUNT=6", DT)
    occ = list(rs)
    assert all(o.weekday() == 0 for o in occ)
    for o in occ:
        nxt = o + timedelta(days=7)
        assert nxt.month != o.month  # no Monday after it in the same month


def test_tc030_rrule_round_trip():
    original = list(rrulestr("FREQ=DAILY;COUNT=10", dtstart=DT))
    serialized = str(rrulestr("FREQ=DAILY;COUNT=10", dtstart=DT))
    reimported = list(rrulestr(serialized.splitlines()[-1], dtstart=DT))
    assert original == reimported
