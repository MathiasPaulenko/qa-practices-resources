"""Counter-driven flaky test: fails deterministically every 3rd run.

`pytest --count=6` always reports exactly 2 failures out of 6 — the
deterministic demo of the detection loop from the guide's triage section.
"""

import pytest

pytestmark = pytest.mark.flaky

_run_count = 0


def test_counter_flaky():
    global _run_count
    _run_count += 1
    assert _run_count % 3 != 0, f"failed on run #{_run_count} (every 3rd run fails)"


def test_stable_neighbor():
    """A deterministic neighbor so the file isn't 100% failures."""
    assert True
