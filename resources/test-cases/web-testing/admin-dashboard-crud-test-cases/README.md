# Admin Dashboard CRUD Testing — Companion

Companion resource for [Admin Dashboard CRUD Test Cases: TaskFlow Example](https://qapractices.com/test-cases/admin-dashboard-crud-test-cases/).

## Contents

- `mock_server.py` — stdlib-only TaskFlow admin API (`/api/v1/projects`, `/users`, `/tasks`) with auth (admin/viewer Bearer tokens), CSRF enforcement, optimistic locking via `version`, soft delete with `include_deleted` view, bulk delete with partial-failure reporting, pagination/search, and a full audit log at `/api/v1/audit-log`.
- `tests/conftest.py` — spins the mock up on an ephemeral port per test.
- `tests/test_admin_crud.py` — executable subset of the 15 test cases plus edge cases: referential integrity on delete, soft-delete visibility, version conflicts, enum validation, CSRF rejection, viewer-role denial, and audit-log completeness.
- `fixtures/` — the request payloads used by the article's curl examples (`project-create.json`, `user-create.json`, `task-update.json`).

## Requirements

- Python 3.10+
- pip

## Usage

```bash
pip install -r requirements.txt
cd resources/test-cases/web-testing/admin-dashboard-crud-test-cases
pytest tests/ -v
```

Run the mock standalone for manual checks:

```bash
python mock_server.py 8080

curl -X POST http://127.0.0.1:8080/api/v1/projects \
  -H "Authorization: Bearer ADMIN_TOKEN" \
  -H "X-CSRF-Token: csrf-token-123" \
  -H "Content-Type: application/json" \
  -d @fixtures/project-create.json
```

## What this covers

- CRUD create/read/update/delete on projects, users, and tasks (TC001–TC015 API path).
- Optimistic locking: stale `version` → `409` conflict.
- Soft delete: records drop out of default lists, stay visible with `include_deleted=true`.
- Bulk delete with per-record partial-failure reporting.
- Auth boundary: viewer token reads but gets `403` on writes; missing CSRF → `403`.
- Audit log: every mutation recorded with admin identity, timestamp, entity, and changed fields.
