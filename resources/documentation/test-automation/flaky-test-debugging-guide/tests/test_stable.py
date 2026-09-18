"""Deterministic tests — the control group that belongs in the blocking suite."""

import pytest

pytestmark = pytest.mark.stable


def add(a, b):
    return a + b


def test_add_positive():
    assert add(2, 3) == 5


def test_add_negative():
    assert add(-1, -1) == -2


def test_add_zero():
    assert add(0, 42) == 42
