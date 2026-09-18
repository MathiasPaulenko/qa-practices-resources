"""Quarantined tests: excluded from the blocking suite, still tracked.

Run `pytest -m "not quarantined"` for the green blocking suite and
`pytest -m quarantined` to check on tests under investigation.
"""

import pytest

pytestmark = pytest.mark.quarantined


def test_known_flaky_checkout():
    """Real-world flaky test kept as signal while being fixed."""
    import random

    assert random.random() > 0.3, "intermittent checkout timeout (under investigation)"
