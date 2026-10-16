import pytest

from audit_log import AuditLog


@pytest.fixture
def log(tmp_path):
    """Fresh audit log per test — file-backed so threads can share it."""
    db = str(tmp_path / "audit.db")
    inst = AuditLog(db)
    yield inst
    inst.conn.close()
