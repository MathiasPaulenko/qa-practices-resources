"""Pytest suite for the health-check contract, mapped to checklist items."""

import pytest

from health_check import (
    CircuitBreaker,
    CircuitState,
    Dependency,
    HealthService,
    aggregate_health,
    call_dependency,
)


@pytest.fixture
def svc():
    return HealthService(
        dependencies=[
            Dependency("postgres", critical=True),
            Dependency("redis", critical=True),
            Dependency("analytics", critical=False),
        ],
        circuits={"postgres": CircuitBreaker(failure_threshold=3, cooldown_s=30)},
    )


# liveness never checks dependencies (the restart-loop guard)
def test_liveness_ignores_dependencies(svc):
    svc.dependencies[0].up = False  # postgres down
    assert svc.liveness() == 200


def test_liveness_fails_only_when_process_dead(svc):
    svc.alive = False
    assert svc.liveness() == 503


# readiness reflects critical deps only
def test_readiness_503_on_critical_dep_down(svc):
    svc.dependencies[0].up = False
    assert svc.readiness() == 503


def test_readiness_200_on_noncritical_dep_down(svc):
    svc.dependencies[2].up = False  # analytics down
    assert svc.readiness() == 200


def test_readiness_logs_every_probe(svc):
    svc.readiness(now=1.0)
    svc.readiness(now=2.0)
    assert [e["code"] for e in svc.probe_log] == [200, 200]


# circuit breaker lifecycle
def test_breaker_opens_after_threshold(svc):
    for i in range(3):
        call_dependency(svc, "postgres", lambda: False, now=float(i))
    assert svc.circuits["postgres"].state is CircuitState.OPEN


def test_open_breaker_short_circuits_calls(svc):
    cb = svc.circuits["postgres"]
    cb.state = CircuitState.OPEN
    cb.opened_at = 100.0
    calls = []
    ok = call_dependency(
        svc, "postgres", lambda: calls.append(1) or True, now=110.0
    )
    assert ok is False and calls == []  # fn never ran


def test_half_open_closes_on_success(svc):
    cb = svc.circuits["postgres"]
    cb.state = CircuitState.OPEN
    cb.opened_at = 0.0
    assert call_dependency(svc, "postgres", lambda: True, now=31.0)
    assert cb.state is CircuitState.CLOSED


def test_open_critical_breaker_degrades_readiness(svc):
    cb = svc.circuits["postgres"]
    cb.state = CircuitState.OPEN
    cb.opened_at = 0.0
    assert svc.readiness(now=5.0) == 503


# graceful shutdown
def test_sigterm_flips_readiness_but_not_liveness(svc):
    svc.shutting_down = True  # mid-drain: still alive, already unready
    assert svc.readiness(now=1001.0) == 503
    assert svc.liveness(now=1001.0) == 200
    svc.in_flight = 3
    svc.sigterm(now=1000.0)  # drain completes, process exits
    assert svc.alive is False


def test_inflight_drains_before_exit(svc):
    svc.in_flight = 5
    svc.sigterm(now=1000.0)
    assert svc.in_flight == 0


def test_shutdown_does_not_outlive_grace(svc):
    svc.in_flight = 100  # more work than the window allows
    svc.sigterm(now=0.0)
    assert svc.in_flight > 0  # hard-killed at deadline, as designed


# aggregation across services
def test_aggregate_up_when_all_ready(svc):
    aux = HealthService(name="svc-web")
    out = aggregate_health([svc, aux], now=1.0)
    assert out["status"] == "UP"


def test_aggregate_degraded_on_optional_failure(svc):
    aux = HealthService(name="svc-web", dependencies=[])
    svc.dependencies[2].up = False  # non-critical only
    out = aggregate_health([svc, aux], now=1.0)
    assert out["status"] == "UP"  # svc still ready


def test_aggregate_down_on_critical_failure(svc):
    svc.dependencies[0].up = False  # critical down
    out = aggregate_health([svc], now=1.0)
    assert out["status"] == "DOWN"
    assert out["services"]["svc-projects"] == 503
