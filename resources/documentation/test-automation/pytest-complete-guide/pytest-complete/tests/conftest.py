import os
import pytest

from src.calculator import Calculator


@pytest.fixture(scope="session")
def db_engine():
    """Simulate a session-scoped database engine."""
    engine = {"connected": True}
    yield engine
    engine["connected"] = False


@pytest.fixture
def calculator():
    return Calculator()


@pytest.fixture
def make_user():
    def _make_user(email="alice@example.com", role="reader"):
        return {"id": 1, "email": email, "role": role}
    return _make_user


@pytest.fixture
def temp_file(tmp_path):
    file_path = tmp_path / "test_data.txt"
    file_path.write_text("test content")
    return file_path
