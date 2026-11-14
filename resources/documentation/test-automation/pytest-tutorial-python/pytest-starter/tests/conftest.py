import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from calculator import Calculator  # noqa: E402


@pytest.fixture
def calculator():
    """Provides a fresh Calculator instance for each test."""
    return Calculator()


@pytest.fixture
def sample_orders():
    return [{"id": 1, "total": 100}, {"id": 2, "total": 200}]
