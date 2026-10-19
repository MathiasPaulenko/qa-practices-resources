"""Minimal health-check service mirroring the checklist's contract.

Rules implemented:
- liveness() answers 200 iff the process is alive — it never touches deps
  (a dependency-aware liveness probe creates restart loops).
- readiness() answers 200 only if critical dependencies are up (cached
  status, never a synchronous call) and required circuits aren't open.
- SIGTERM flips readiness to 503 immediately while in-flight work drains;
  liveness stays 200 through the drain.
- Circuit breaker opens after `failure_threshold` failures, half-opens
  after `cooldown_s`, and its state feeds readiness for critical deps.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable


class CircuitState(Enum):
    """Circuit breaker states."""

    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


@dataclass
class Dependency:
    """A downstream the service depends on."""

    name: str
    critical: bool
    up: bool = True


@dataclass
class CircuitBreaker:
    """Simple breaker: opens after N failures, half-opens after cooldown."""

    failure_threshold: int = 3
    cooldown_s: float = 30.0
    state: CircuitState = CircuitState.CLOSED
    failures: int = 0
    opened_at: float = 0.0

    def record_failure(self, now: float) -> None:
        """Count a failure; trip when the threshold is hit."""
        self.failures += 1
        if self.failures >= self.failure_threshold:
            self.state = CircuitState.OPEN
            self.opened_at = now

    def record_success(self) -> None:
        """A success closes the circuit fully."""
        self.state = CircuitState.CLOSED
        self.failures = 0

    def probe(self, now: float) -> bool:
        """Whether a trial call is allowed right now."""
        if self.state is CircuitState.OPEN and now - self.opened_at >= self.cooldown_s:
            self.state = CircuitState.HALF_OPEN
        return self.state is not CircuitState.OPEN


@dataclass
class HealthService:
    """Service exposing liveness/readiness over dependencies + a breaker."""

    name: str = "svc-projects"
    alive: bool = True
    shutting_down: bool = False
    in_flight: int = 0
    drain_timeout_s: float = 30.0
    readiness_min_failures: int = 1
    dependencies: list[Dependency] = field(default_factory=list)
    circuits: dict[str, CircuitBreaker] = field(default_factory=dict)
    probe_log: list[dict] = field(default_factory=list)

    def liveness(self, now: float | None = None) -> int:
        """Process-only check: 200 while alive, even mid-shutdown drain."""
        code = 200 if self.alive else 503
        self._log("live", code, now)
        return code

    def readiness(self, now: float | None = None) -> int:
        """503 during shutdown or when a critical dep / open circuit fails."""
        code = 200
        if self.shutting_down:
            code = 503
        else:
            for dep in self.dependencies:
                if dep.critical and not dep.up:
                    code = 503
                cb = self.circuits.get(dep.name)
                if dep.critical and cb and cb.state is CircuitState.OPEN:
                    code = 503
        self._log("ready", code, now)
        return code

    def sigterm(self, now: float) -> None:
        """Stop accepting traffic, drain in-flight, stay live until done."""
        self.shutting_down = True
        deadline = now + self.drain_timeout_s
        while self.in_flight > 0 and now < deadline:
            now += 1.0
            self.in_flight -= 1  # each tick finishes one request
        self.alive = False

    def _log(self, probe: str, code: int, now: float | None) -> None:
        self.probe_log.append(
            {"probe": probe, "code": code, "ts": now if now is not None else time.time()}
        )


def call_dependency(
    svc: HealthService, dep: str, fn: Callable[[], bool], now: float
) -> bool:
    """Call a dependency through its breaker; returns success."""
    cb = svc.circuits[dep]
    if not cb.probe(now):
        return False  # open circuit short-circuits
    ok = fn()
    if ok:
        cb.record_success()
    else:
        cb.record_failure(now)
    return ok


def aggregate_health(services: list[HealthService], now: float) -> dict:
    """Gateway-style aggregation following the critical path."""
    statuses = {s.name: s.readiness(now) for s in services}
    critical_down = any(
        s.readiness(now) != 200 and any(d.critical for d in s.dependencies)
        for s in services
    )
    overall = "DOWN" if critical_down else "UP"
    if not critical_down and any(c != 200 for c in statuses.values()):
        overall = "DEGRADED"
    return {"status": overall, "services": statuses}
