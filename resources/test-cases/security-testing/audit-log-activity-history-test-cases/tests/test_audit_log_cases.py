"""Tests for the hash-chained audit log — mapped to the TC ids from
https://qapractices.com/test-cases/audit-log-activity-history-test-cases/
"""

import json
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone

UTC = timezone.utc


def test_login_event_has_required_fields(log):
    # TC001 — user.login must carry identity, timestamp, IP and UA
    row_id = log.append("user.login", "U-01", "login",
                        ip_address="192.168.1.100", user_agent="Chrome/Windows",
                        tenant_id="TENANT-077")
    row = log.conn.execute("SELECT * FROM audit_log WHERE id = ?", (row_id,)).fetchone()
    assert row[1] == "user.login"
    assert row[2] == "U-01"
    assert datetime.fromisoformat(row[5]).tzinfo is not None  # UTC
    assert row[6] == "192.168.1.100" and row[7] == "Chrome/Windows"


def test_failed_login_logs_email_not_password(log):
    # TC003 / TC019 — login_failed keeps the email, never the password
    log.append("user.login_failed", "sarah@audittrail.io", "login_failed",
               details={"email": "sarah@audittrail.io", "password": "WrongPass123"})
    raw = log.conn.execute("SELECT details FROM audit_log").fetchone()[0]
    assert "sarah@audittrail.io" in raw
    assert "WrongPass123" not in raw


def test_no_password_anywhere_in_log(log):
    # TC019 — scrub sweep across every stored field
    log.append("user.login", "U-01", "login",
               details={"password": "SecretPass123!", "remember": True})
    log.append("admin.config_change", "U-01", "config_change",
               details={"token": "abc123", "setting": "max_upload_size"})
    for row in log.conn.execute("SELECT * FROM audit_log").fetchall():
        blob = " ".join(str(v) for v in row if v)
        assert "SecretPass123!" not in blob and "abc123" not in blob


def test_verify_empty_chain_passes(log):
    # Edge table — verification on 0 entries must pass, not error
    result = log.verify_chain()
    assert result["chainValid"] is True and result["entriesVerified"] == 0


def test_tamper_detection_flags_first_invalid(log):
    # TC018 — a direct UPDATE breaks the chain at that row
    for i in range(5):
        log.append("user.login", f"U-{i}", "login")
    log.tamper(3, "user_id", "U-99")
    result = log.verify_chain()
    assert result["chainValid"] is False
    assert result["firstInvalidIndex"] == 3


def test_chain_all_valid(log):
    # TC029 — a clean chain verifies end to end
    for i in range(100):
        log.append("admin.data_access", "U-01", "data_access", resource=f"user:{i}")
    result = log.verify_chain()
    assert result["chainValid"] is True and result["entriesVerified"] == 100


def test_concurrent_writes_keep_chain(log):
    # TC021 — parallel appends must not corrupt ordering or the chain
    with ThreadPoolExecutor(max_workers=10) as pool:
        list(pool.map(
            lambda i: log.append("user.login", f"U-{i:03d}", "login"), range(50)
        ))
    assert log.verify_chain()["chainValid"] is True
    assert log.filter()["totalItems"] == 50


def test_deleted_user_entries_preserved(log):
    # TC023 — deleting the user marks it but keeps the entries
    log.append("user.login", "U-42", "login")
    log.append("admin.data_access", "U-42", "data_access", resource="doc:1")
    log.delete_user("U-42")
    rows = log.conn.execute(
        "SELECT deleted_user FROM audit_log WHERE user_id = 'U-42'"
    ).fetchall()
    assert len(rows) == 2 and all(r[0] == 1 for r in rows)
    assert log.verify_chain()["chainValid"] is True


def test_unicode_actor_name(log):
    # TC026 — unicode in user_id/details survives store and export
    log.append("user.login", "José García Müller 🚀", "login")
    assert "José García Müller 🚀" in log.export_csv()


def test_retention_boundary(log):
    # Edge table — entry at exactly the cutoff follows policy, older goes
    cutoff = datetime.now(UTC) - timedelta(days=365)
    log.append("user.login", "U-01", "login", timestamp=cutoff)                      # at boundary: kept
    log.append("user.login", "U-01", "login", timestamp=cutoff - timedelta(days=1))  # older: purged
    deleted = log.apply_retention(cutoff.isoformat())
    assert deleted == 1 and log.filter()["totalItems"] == 1


def test_legal_hold_survives_retention(log):
    # TC033 — held user's entries outlive the retention window
    old = (datetime.now(UTC) - timedelta(days=400)).isoformat()
    log.append("admin.export", "U-42", "export", timestamp=datetime.fromisoformat(old))
    log.append("admin.export", "U-99", "export", timestamp=datetime.fromisoformat(old))
    log.set_legal_hold("U-42", True)
    log.apply_retention(datetime.now(UTC).isoformat())
    remaining = log.conn.execute("SELECT user_id FROM audit_log").fetchall()
    assert [r[0] for r in remaining] == ["U-42"]


def test_export_csv_contains_all_rows(log):
    # TC020 — export must not silently truncate
    for i in range(2000):
        log.append("user.login", f"U-{i}", "login")
    lines = log.export_csv().strip().splitlines()
    assert len(lines) == 2001  # header + 2000 rows


def test_filter_by_user_action_range(log):
    # TC009/TC010/TC011 — filters return only matching entries
    log.append("user.login", "U-42", "login",
               timestamp=datetime(2026, 7, 5, tzinfo=UTC))
    log.append("admin.export", "U-42", "export",
               timestamp=datetime(2026, 7, 10, tzinfo=UTC))
    log.append("user.login", "U-99", "login",
               timestamp=datetime(2026, 7, 10, tzinfo=UTC))
    assert log.filter(user_id="U-42")["totalItems"] == 2
    assert log.filter(action="export")["totalItems"] == 1
    assert log.filter(start="2026-07-06", end="2026-07-10")["totalItems"] == 2


def test_api_action_distinguishable(log):
    # TC025 — api.action entries are marked apart from UI actions
    log.append("api.action", "key_abc123", "update", resource="user:42",
               details={"endpoint": "PUT /api/v1/users/42"})
    row = log.conn.execute("SELECT event_type, user_id FROM audit_log").fetchone()
    assert row == ("api.action", "key_abc123")


def test_sample_entry_shape(log):
    # Sample Log Entry — every stored field is JSON-serializable for the API
    log.append("user.permission_denied", "alice", "user_delete",
               resource="user:123", ip_address="203.0.113.42",
               timestamp=datetime(2026, 7, 23, 14, 30, tzinfo=UTC))
    row = log.conn.execute("SELECT * FROM audit_log").fetchone()
    cols = [c[1] for c in log.conn.execute("PRAGMA table_info(audit_log)")]
    json.dumps(dict(zip(cols, row)))
