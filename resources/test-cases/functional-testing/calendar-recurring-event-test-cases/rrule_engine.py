"""Thin recurrence engine used by the calendar test-cases article.

Wraps dateutil.rrule with RFC 5545 validation, exdate support and
bounded range expansion — the three behaviours the article's test
cases exercise. Deliberately tiny: the point is to show what a
correct expansion layer does, not to reimplement a calendar.
"""

from __future__ import annotations

from datetime import datetime

from dateutil.rrule import rruleset, rrulestr

VALID_FREQS = {"SECONDLY", "MINUTELY", "HOURLY", "DAILY", "WEEKLY", "MONTHLY", "YEARLY"}


class RRULEValidationError(ValueError):
    """Raised when an RRULE string violates RFC 5545 constraints."""


def parse_rrule_parts(rrule_str: str) -> dict[str, str]:
    parts: dict[str, str] = {}
    for part in rrule_str.split(";"):
        if "=" not in part:
            raise RRULEValidationError(f"malformed rule part: {part!r}")
        key, _, value = part.partition("=")
        parts[key.upper()] = value
    return parts


def validate_rrule(rrule_str: str, dtstart: datetime | None = None) -> dict[str, str]:
    """Validate an RRULE string. Returns its parts on success."""
    parts = parse_rrule_parts(rrule_str)

    freq = parts.get("FREQ")
    if freq is None or freq.upper() not in VALID_FREQS:
        raise RRULEValidationError(f"invalid or missing FREQ: {freq!r}")

    if "COUNT" in parts and "UNTIL" in parts:
        raise RRULEValidationError("COUNT and UNTIL are mutually exclusive per RFC 5545")

    if dtstart is not None and "UNTIL" in parts:
        fmt = "%Y%m%dT%H%M%SZ" if "T" in parts["UNTIL"] else "%Y%m%d"
        until = datetime.strptime(parts["UNTIL"], fmt)
        if parts["UNTIL"].endswith("Z"):
            until = until.replace(tzinfo=dtstart.tzinfo)
        if until < dtstart.replace(tzinfo=until.tzinfo):
            raise RRULEValidationError(
                "UNTIL predates DTSTART: the rule can never produce occurrences"
            )
    return parts


def build_ruleset(
    rrule_str: str,
    dtstart: datetime,
    exdates: list[datetime] | None = None,
) -> rruleset:
    """Create an rruleset from a validated RRULE plus optional exdates."""
    validate_rrule(rrule_str, dtstart)
    rs = rruleset()
    rs.rrule(rrulestr(rrule_str, dtstart=dtstart))
    for d in exdates or []:
        rs.exdate(d)
    return rs


def occurrences_in_range(
    rs: rruleset, start: datetime, end: datetime
) -> list[datetime]:
    """Bounded expansion: only instances inside the requested window."""
    return rs.between(start, end, inc=True)
