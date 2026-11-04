# Calendar and Scheduling Test Cases — Runnable Companion

Runnable Python checks for the scheduling failure modes covered in
[Calendar and Scheduling Test Cases: 33 Scenarios](https://qapractices.com/test-cases/calendar-scheduling-feature-test-cases/)
([versión en español](https://qapractices.com/es/test-cases/calendar-scheduling-feature-test-cases/)).

`scheduler.py` implements the same rules the cases assert:

- Events stored in UTC with the original timezone.
- Strict overlap detection — back-to-back events never conflict.
- Warn-vs-block conflict policy (TC018).
- DST-gap resolution for nonexistent local times (TC027).
- Monthly day-31 recurrence with clamp-or-skip behavior (TC005).

## Setup

```bash
python -m venv .venv
.venv/Scripts/activate   # Windows
pip install -r requirements.txt
```

## Run

```bash
pytest tests/ -v
```

## Requirements

- Python 3.10+ (`zoneinfo`)
- pytest 8.3.4, python-dateutil 2.9.0, icalendar 5.0.13
