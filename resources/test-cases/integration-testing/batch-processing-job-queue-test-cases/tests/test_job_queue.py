import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from job_queue import (  # noqa: E402
    Job,
    JobQueue,
    PermanentError,
    Status,
    TransientError,
    flaky_handler,
)

EMAIL = {"type": "send_email", "data": {"to": "user@qapractices.dev"}}


@pytest.fixture()
def q() -> JobQueue:
    queue = JobQueue(max_retries=3)
    queue.register("send_email", lambda job: {"sent": job.payload["data"]["to"]})
    return queue


# TC-001: single job, queued -> processing -> completed
def test_single_job_completes(q):
    job = q.submit(EMAIL)
    q.run(job)
    assert job.status == Status.COMPLETED
    assert job.attempts == 1
    assert job.result == {"sent": "user@qapractices.dev"}


# TC-002: FIFO ordering preserved
def test_fifo_order(q):
    jobs = [q.submit(EMAIL) for _ in range(5)]
    order = []
    q.register(
        "track", lambda job: order.append(job.payload["data"]["n"]) or True
    )
    jobs = [q.submit({"type": "track", "data": {"n": i}}) for i in range(5)]
    q.drain()
    assert order == [0, 1, 2, 3, 4]


# TC-004: transient failure retries then succeeds (TC-028 partial)
def test_transient_retry_then_success():
    q = JobQueue(max_retries=3)
    q.register("flaky", flaky_handler(fail_times=1))
    job = q.run(q.submit({"type": "flaky", "data": {}}))
    assert job.status == Status.COMPLETED
    assert job.attempts == 2
    assert len(job.errors) == 1


# TC-008/TC-019: max retries exhausted -> dead lettered, all attempts recorded
def test_max_retries_dead_letters():
    q = JobQueue(max_retries=3)
    q.register("always", flaky_handler(fail_times=99))
    job = q.run(q.submit({"type": "always", "data": {}}))
    assert job.status == Status.DEAD_LETTERED
    assert job.attempts == 4  # 1 initial + 3 retries
    assert job in q.dlq
    assert len(job.errors) == 4


# TC-028: permanent error dead-letters immediately, no retry
def test_permanent_error_no_retry():
    q = JobQueue(max_retries=3)

    def bad(job):
        raise PermanentError("400 bad request")

    q.register("bad", bad)
    job = q.run(q.submit({"type": "bad", "data": {}}))
    assert job.status == Status.DEAD_LETTERED
    assert job.attempts == 1


# TC-012: idempotency key dedupes duplicate submissions
def test_idempotency_key_dedupes(q):
    a = q.submit(EMAIL, idempotency_key="order-123-export")
    b = q.submit(EMAIL, idempotency_key="order-123-export")
    assert a.id == b.id
    q.drain()
    assert a.attempts == 1


# TC-016: invalid payload rejected before queueing
def test_invalid_payload_rejected(q):
    with pytest.raises(ValueError):
        q.submit({"type": "send_email"})


# TC-017: unknown job type rejected
def test_unknown_type_rejected(q):
    with pytest.raises(ValueError, match="unknown_job_type"):
        q.submit({"type": "unknown_job_type", "data": {}})


# TC-018/TC-026: worker crash requeues; job is picked up and completes once
def test_crash_requeues_and_completes(q):
    job = q.submit(EMAIL)
    q.crash_mid_job(job)
    assert job.status == Status.QUEUED
    q.run(job)
    assert job.status == Status.COMPLETED


# TC-037: replay a dead-lettered job after the fix
def test_dlq_replay():
    q = JobQueue(max_retries=0)
    calls = {"n": 0}

    def handler(job):
        calls["n"] += 1
        if calls["n"] == 1:
            raise TransientError("down")
        return "ok"

    q.register("re", handler)
    job = q.run(q.submit({"type": "re", "data": {}}))
    assert job.status == Status.DEAD_LETTERED
    fixed = q.replay_dlq(job.id)
    assert fixed.status == Status.COMPLETED
    assert job not in q.dlq
