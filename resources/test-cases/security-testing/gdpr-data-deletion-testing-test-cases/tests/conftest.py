import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from erasure_engine import ErasureEngine  # noqa: E402

USER_ID = "u-4821"
EMAIL = "qa-erasure-01@taskflow.test"


@pytest.fixture
def engine():
    eng = ErasureEngine()
    eng.seed_user(USER_ID, EMAIL)
    return eng
