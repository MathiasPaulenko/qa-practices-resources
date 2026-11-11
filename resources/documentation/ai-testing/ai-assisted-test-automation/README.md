# AI-Assisted Test Automation — Companion

Companion files for the [AI-Assisted Test Automation Guide](https://qapractices.com/documentation/ai-assisted-test-automation).

## Files

| File | Purpose |
| --- | --- |
| `src/self_healing.py` | Fallback locator pattern: tries the primary selector, then stable alternatives in order. |
| `tests/test_self_healing.py` | Pytest suite verifying the healing logic with a fake driver — no browser needed. |

## Requirements

- Python 3.10+
- selenium 4.x
- pytest 8.3+

## Usage

1. Install dependencies: `pip install -r requirements.txt`.
2. Run `pytest tests/ -v` — the fake driver exercises primary hit, fallback order, and total-miss paths.
3. In a real suite, swap `FakeDriver` for your WebDriver instance and log which fallback fired so a human can review it later.

## CI Integration

```yaml
- run: pip install -r requirements.txt && pytest tests/ -v --tb=short
```
