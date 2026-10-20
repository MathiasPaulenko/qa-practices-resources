# Batch Processing and Job Queue — Companion Lab

Companion for the QAPractices resource
[Batch Processing and Job Queue Test Cases](https://qapractices.com/test-cases/batch-processing-job-queue-test-cases/).

`job_queue.py` is a dependency-free in-memory job queue that models the
lifecycle the test cases cover:

```text
queued → processing → completed
                    ↘ retrying → processing (backoff) → dead_lettered
                    ↘ cancelled / failed
dead_lettered → queued (replay after fix)
```

- `submit()` validates payloads, rejects unknown job types and dedupes on
  `idempotency_key`.
- `run()` follows the retry loop to a terminal state.
- `replay_dlq()` requeues a dead-lettered job after the root cause is fixed.
- `crash_mid_job()` simulates a worker dying after grabbing the lock —
  the visibility-timeout path.

## Usage

```bash
pip install -r requirements.txt
pytest -v
```

The suite exercises TC-001 (single job), TC-002 (FIFO), TC-004 (transient
retry), TC-008/TC-019 (max retries → DLQ), TC-012 (idempotency), TC-016/17
(payload validation), TC-018/TC-026 (crash requeue), TC-028 (permanent vs
transient) and TC-037 (DLQ replay).
