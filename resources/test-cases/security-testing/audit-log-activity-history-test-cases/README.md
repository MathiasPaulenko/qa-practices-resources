# Audit Log and Activity History Test Cases — Companion

Companion resource for [Audit Log and Activity History Test Cases](https://qapractices.com/test-cases/audit-log-activity-history-test-cases/).

## Contents

- `audit_log.py` — stdlib-only audit log on sqlite3. Append-only table, every entry embeds the SHA-256 of the previous one (hash chain), `verify_chain()` returns the first invalid index, plus filtering, CSV export, retention cleanup and legal hold. `tamper()` is a test backdoor that does a direct UPDATE to simulate database-level tampering.
- `tests/test_audit_log_cases.py` — pytest 8.3 suite mapped to the TC ids of the resource: required fields (TC001), no-password scrubbing (TC003/TC019), tamper detection (TC018), concurrent writes (TC021), deleted-user preservation (TC023), unicode (TC026), chain verification (TC029), legal hold vs retention (TC033), export completeness (TC020, scaled to 2,000 rows), filters (TC009-011), API action marking (TC025) and the JSON-serializable entry shape.
- `tests/conftest.py` — `log` fixture: fresh file-backed `AuditLog` per test (file-backed so the TC021 thread pool can share the connection).
- `requirements.txt` — pytest 8.3.4 only; everything else is stdlib.

## Requirements

- Python 3.10+
- pip

## Usage

```bash
pip install -r requirements.txt
cd resources/test-cases/security-testing/audit-log-activity-history-test-cases
pytest tests/ -v
```

Manual probe:

```bash
python - <<'PY'
from audit_log import AuditLog
log = AuditLog(":memory:")
log.append("user.login", "U-01", "login", ip_address="192.168.1.100")
log.append("admin.export", "U-01", "export", resource="report:42")
print(log.verify_chain())          # {'chainValid': True, ...}
log.tamper(1, "user_id", "U-99")   # direct DB edit
print(log.verify_chain())          # {'chainValid': False, 'firstInvalidIndex': 1}
PY
```

## What this covers

- Hash-chain tamper evidence: `hash_n = SHA-256(hash_n-1 + entry fields)`; a direct UPDATE breaks the chain at that row and everything after it.
- Sensitive-data scrubbing at the logging layer — `password`, `token`, `secret`, `api_key`, `ssn` keys never reach storage.
- Retention boundary and legal hold — entries on hold survive the purge.
- Deleted-user preservation — GDPR-style delete marks `deleted_user` but keeps the entries and the chain intact.
- Concurrent writes through a thread pool — chain stays valid.
- Filter by user / action / date range and full CSV export without truncation.

## Design notes

- Timestamps are stored as UTC ISO-8601; pass naive datetimes and they're coerced to UTC in `append()`.
- `filter()` uses parameterized queries — same contract as a real `/v1/logs` endpoint.
- The companion intentionally mirrors the resource's fictional AuditTrail API semantics (`eventType`, `userId`, `firstInvalidIndex`) so test expectations translate directly.
