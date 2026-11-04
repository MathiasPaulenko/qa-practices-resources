"""Minimal scheduling domain functions exercised by the test suite.

Mirrors the failure modes from the QAPractices resource: UTC storage with
original-timezone metadata, overlap detection, warn-vs-block conflict policy,
DST-gap handling and monthly day-31 recurrence.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo


@dataclass
class CalendarEvent:
    """An event stored in UTC with its original timezone."""

    title: str
    start_utc: datetime
    end_utc: datetime
    timezone: str
    conflict: bool = False

    def local_start(self, viewer_tz: str) -> datetime:
        return self.start_utc.astimezone(ZoneInfo(viewer_tz))


def to_utc(local_dt: datetime, timezone: str) -> datetime:
    """Convert a naive local datetime to an aware UTC datetime."""
    return local_dt.replace(tzinfo=ZoneInfo(timezone)).astimezone(ZoneInfo("UTC"))


def overlaps(a_start: datetime, a_end: datetime, b_start: datetime, b_end: datetime) -> bool:
    """Strict overlap: back-to-back events (end == start) do not conflict."""
    return a_start < b_end and a_end > b_start


def create_event(
    title: str,
    start_local: datetime,
    end_local: datetime,
    timezone: str,
    existing: list[CalendarEvent],
    policy: str = "warn",
) -> CalendarEvent:
    """Create an event applying the conflict policy used by TC018/TC029.

    policy="warn" creates the event flagged; policy="block" raises ValueError.
    """
    if end_local <= start_local:
        raise ValueError("End time must be after start time.")
    start_utc = to_utc(start_local, timezone)
    end_utc = to_utc(end_local, timezone)
    has_conflict = any(overlaps(start_utc, end_utc, e.start_utc, e.end_utc) for e in existing)
    if has_conflict and policy == "block":
        raise ValueError("This event conflicts with an existing event.")
    return CalendarEvent(title, start_utc, end_utc, timezone, conflict=has_conflict)


def resolve_dst_gap(local_dt: datetime, timezone: str) -> datetime:
    """Resolve a local datetime that may fall inside a DST gap.

    If the wall time does not exist (spring-forward), shift forward by the
    gap size so the event lands on the next valid instant.
    """
    tz = ZoneInfo(timezone)
    aware = local_dt.replace(tzinfo=tz)
    roundtrip = aware.astimezone(ZoneInfo("UTC")).astimezone(tz)
    if roundtrip.replace(tzinfo=None) == local_dt:
        return aware
    gap = roundtrip.replace(tzinfo=None) - local_dt
    return (local_dt + gap).replace(tzinfo=tz)


def monthly_day31_occurrences(year: int, months: int, clamp: bool = True) -> list[date]:
    """Occurrence dates for a monthly day-31 rule.

    clamp=True moves the event to the month's last day; clamp=False skips
    months without a 31st.
    """
    result = []
    for offset in range(months):
        month = (1 + offset - 1) % 12 + 1
        y = year + (1 + offset - 1) // 12
        next_month = date(y + (month == 12), month % 12 + 1, 1)
        last_day = (next_month - timedelta(days=1)).day
        if last_day >= 31:
            result.append(date(y, month, 31))
        elif clamp:
            result.append(date(y, month, last_day))
    return result


def reminder_fires_at(event: CalendarEvent, minutes_before: int, viewer_tz: str) -> datetime:
    """Reminder time in the viewer's timezone — never the server's."""
    if minutes_before < 0:
        raise ValueError("Reminder must be a positive value before the event.")
    return (event.start_utc - timedelta(minutes=minutes_before)).astimezone(ZoneInfo(viewer_tz))
