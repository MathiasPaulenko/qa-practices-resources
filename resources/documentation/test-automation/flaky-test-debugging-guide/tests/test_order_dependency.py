"""Order-dependent tests: only fail when the suite runs them in the wrong order.

`pytest-randomly` shuffles test order on every run. Run several times (or
with `--randomly-seed`) and `test_b` fails whenever it executes before
`test_a` — shared mutable state leaking between tests.
"""

import pytest

pytestmark = pytest.mark.flaky

_shared_users = []


def test_a_creates_user():
    _shared_users.append("test@example.com")
    assert len(_shared_users) == 1


def test_b_expects_empty_db():
    assert len(_shared_users) == 0, f"expected empty, found {_shared_users}"
