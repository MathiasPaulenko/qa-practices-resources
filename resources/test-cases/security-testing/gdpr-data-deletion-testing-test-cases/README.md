# GDPR Data Deletion Test Cases — Companion

Companion resource for [GDPR Data Deletion Test Cases: Right to Erasure](https://qapractices.com/test-cases/gdpr-data-deletion-testing-test-cases/).

## Contents

- `erasure_engine.py` — stdlib-only `sqlite3` model of the Article 17 flow. `request_erasure()` enforces identity verification, consults `legal_holds` (Art. 17(3) deferral), then propagates the deletion across `users`, `orders` (identifier columns nulled, amounts kept), `sessions`, `search_index`, `cache`, `app_logs` (value scrubbing) and `marketing_segments`, while writing an `audit_log` entry and one outbox message per processor. `snapshot()`/`restore()` simulate a pre-erasure backup whose resurrected rows are re-deleted by `replay_tombstones()`.
- `tests/test_erasure_cases.py` — pytest 8.3 suite with 16 tests mapped to the resource's TC ids: cascade (TC-002), index/cache cleanup (TC-003), restore replay (TC-004), audit trail (TC-005), processor notification (TC-006), legal hold deferral and resume (TC-007), anonymized aggregates (TC-008), the one-month statutory window (TC-009), rejected unverified requests (TC-010), log scrubbing (TC-011), re-identification resistance (TC-012), idempotent repeats (TC-013), consent-withdrawal scope (TC-014), confirmation content (TC-015) and the export race (TC-016).
- `tests/conftest.py` — `engine` fixture: fresh in-memory `ErasureEngine` seeded with `u-4821` / `qa-erasure-01@taskflow.test`.
- `requirements.txt` — pytest 8.3.4 only; the engine itself is pure stdlib.

## Requirements

- Python 3.10+
- pip

## Usage

```bash
pip install -r requirements.txt
cd resources/test-cases/security-testing/gdpr-data-deletion-testing-test-cases
pytest tests/ -v
```

Manual probe:

```bash
python - <<'PY'
from erasure_engine import ErasureEngine
eng = ErasureEngine()
eng.seed_user("u-4821", "qa-erasure-01@taskflow.test")
print(eng.request_erasure("u-4821"))          # {'status': 'fulfilled', ...}
print(eng.pii_residue("qa-erasure-01"))       # 0 — nothing left anywhere
snap = eng.snapshot()
eng.seed_user("u-0001", "canary@taskflow.test")
eng.request_erasure("u-0001")
eng.restore(snap)                             # resurrects u-0001, replay deletes it again
print(eng.pii_residue("canary"))              # 0
PY
```

## What this covers

- The propagation chain that real GDPR audits check: primary table, related rows, caches, search indexes, logs, processors, audit trail.
- Backup safety: a restore of pre-erasure data is followed by tombstone replay so deleted users stay deleted.
- The two legal edges most suites skip: legal-hold deferral/resume (Art. 17(3)) and identity verification before executing (Art. 12(6)).
- Anonymization semantics: order rows survive as aggregates, but every identifier column is nulled — and `reidentify()` proves no linkage back.
- Idempotency: a repeated or unknown-user erasure is a no-op, with no duplicate processor notifications or audit spam.

## Design notes

- The engine mirrors the resource's TaskFlow dataset (`u-4821`, `qa-erasure-01@taskflow.test`) so expectations translate directly.
- `pii_residue(needle)` is the grep-style canary check the resource recommends: one call sweeps every PII-bearing store.
- `confirmation_for()` models the subject-facing receipt: scope and timestamp only — it must not contain the erased values.
