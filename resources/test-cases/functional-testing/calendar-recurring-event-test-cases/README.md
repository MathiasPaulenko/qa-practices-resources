# Calendar Recurring Event Test Cases — Companion

Companion resource for [Calendar Recurring Event Test Cases: 30 RRULE Scenarios](https://qapractices.com/test-cases/calendar-recurring-event-test-cases/).

## Contents

- `rrule_engine.py` — thin recurrence layer over `dateutil.rrule`: `validate_rrule` enforces the RFC 5545 constraints the article tests (valid FREQ, COUNT and UNTIL mutually exclusive, UNTIL not before DTSTART), `build_ruleset` assembles an rruleset with exdates, and `occurrences_in_range` does bounded expansion via `between()` instead of materializing the series.
- `tests/conftest.py` — puts the engine on `sys.path`.
- `tests/test_rrule_engine.py` — executable subset of the article's cases: daily/weekly/monthly/yearly expansion (TC001-TC004), UNTIL bound (TC005), INTERVAL (TC006), range query (TC007), 31st-of-month skips (TC011), leap years (TC012), DST spring-forward and fall-back wall-clock invariance (TC013/TC014), invalid FREQ (TC017), COUNT+UNTIL conflict (TC018), infinite recurrence with bounded query (TC020), backdated series (TC021), BYDAY×BYMONTHDAY intersection (TC022), BYSETPOS last-Monday (TC023), exdate counts (TC010/TC029) and rrulestr round-trip (TC030).

## Requirements

- Python 3.10+
- pip

## Usage

```bash
pip install -r requirements.txt
pytest tests/ -v
```

Expected output: `21 passed`.

The engine uses `python-dateutil` for expansion and stdlib `zoneinfo` for timezones. In a real calendar app the same checks run against your persistence layer — the point here is that wall-clock invariance and exdate accounting are testable without mocking a clock.

## Related

- Article EN: https://qapractices.com/test-cases/calendar-recurring-event-test-cases/
- Article ES: https://qapractices.com/es/test-cases/calendar-recurring-event-test-cases/
