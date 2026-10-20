"""In-memory job queue with retries, DLQ and idempotency keys.

Models the lifecycle the QAPractices test cases describe:
queued -> processing -> completed | retrying -> ... -> dead_lettered.
"""
from __future__ import annotations

import itertools
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable


class Status(str, Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    RETRYING = "retrying"
    COMPLETED = "completed"
    FAILED = "failed"
    DEAD_LETTERED = "dead_lettered"
    CANCELLED = "cancelled"


class TransientError(Exception):
    """Retryable failure (500/503/timeout class)."""


class PermanentError(Exception):
    """Non-retryable failure (400 class)."""


@dataclass
class Job:
    payload: dict
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    status: Status = Status.QUEUED
    attempts: int = 0
    errors: list[str] = field(default_factory=list)
    result: object = None
    idempotency_key: str | None = None


class JobQueue:
    def __init__(self, max_retries: int = 3, backoff_base: float = 0.0):
        self.max_retries = max_retries
        self.backoff_base = backoff_base  # seconds between retries
        self.queue: list[Job] = []
        self.dlq: list[Job] = []
        self._by_key: dict[str, Job] = {}
        self.handlers: dict[str, Callable[[Job], object]] = {}

    def register(self, job_type: str, handler: Callable[[Job], object]) -> None:
        self.handlers[job_type] = handler

    def submit(self, payload: dict, idempotency_key: str | None = None) -> Job:
        if "type" not in payload or "data" not in payload:
            raise ValueError("payload must include 'type' and 'data'")
        if payload["type"] not in self.handlers:
            raise ValueError(f"unknown_job_type: {payload['type']}")
        if idempotency_key and idempotency_key in self._by_key:
            return self._by_key[idempotency_key]
        job = Job(payload=payload, idempotency_key=idempotency_key)
        if idempotency_key:
            self._by_key[idempotency_key] = job
        self.queue.append(job)
        return job

    def _run_once(self, job: Job) -> None:
        job.status = Status.PROCESSING
        job.attempts += 1
        try:
            job.result = self.handlers[job.payload["type"]](job)
            job.status = Status.COMPLETED
        except TransientError as exc:
            job.errors.append(str(exc))
            if job.attempts <= self.max_retries:
                job.status = Status.RETRYING
            else:
                job.status = Status.DEAD_LETTERED
                self.dlq.append(job)
        except PermanentError as exc:
            job.errors.append(str(exc))
            job.status = Status.DEAD_LETTERED
            self.dlq.append(job)

    def run(self, job: Job) -> Job:
        """Process a job, following retries until terminal state."""
        while True:
            self._run_once(job)
            if job.status == Status.RETRYING:
                if self.backoff_base:
                    time.sleep(self.backoff_base * (2 ** (job.attempts - 1)))
                continue
            return job

    def drain(self) -> list[Job]:
        """Process every queued job to a terminal state."""
        while self.queue:
            self.run(self.queue.pop(0))
        return [j for j in self.dlq]

    def replay_dlq(self, job_id: str) -> Job:
        job = next(j for j in self.dlq if j.id == job_id)
        self.dlq.remove(job)
        job.status = Status.QUEUED
        job.errors = []
        job.attempts = 0
        return self.run(job)

    def cancel(self, job: Job) -> None:
        job.status = Status.CANCELLED

    def crash_mid_job(self, job: Job) -> Job:
        """Simulate a worker dying after grabbing the lock."""
        job.status = Status.PROCESSING
        job.attempts += 1
        job.status = Status.QUEUED  # visibility timeout released the lock
        return job


_counter = itertools.count()


def flaky_handler(fail_times: int) -> Callable[[Job], object]:
    """Handler that raises TransientError fail_times times, then succeeds."""
    calls = {"n": 0}

    def handler(job: Job) -> object:
        calls["n"] += 1
        if calls["n"] <= fail_times:
            raise TransientError(f"downstream 500 (attempt {calls['n']})")
        return {"ok": True, "attempts": calls["n"]}

    return handler
