"""Tests for the blue-green metric gate."""
import metric_gate

BASELINE = {
    "error_rate": 0.001,
    "p99_latency_ms": 120,
    "cpu_pct": 45,
    "mem_pct": 60,
}


def _evaluate(candidate):
    return metric_gate.evaluate(BASELINE, candidate)


def test_all_within_threshold_promotes():
    assert metric_gate.gate(_evaluate({
        "error_rate": 0.0015,
        "p99_latency_ms": 140,
        "cpu_pct": 50,
        "mem_pct": 65,
    }))


def test_latency_breach_triggers_rollback():
    results = _evaluate({
        "error_rate": 0.001,
        "p99_latency_ms": 150,  # +25% > +20% allowed
        "cpu_pct": 45,
        "mem_pct": 60,
    })
    assert not metric_gate.gate(results)
    latency = next(r for r in results if r.name == "p99_latency_ms")
    assert not latency.passed


def test_error_rate_uses_absolute_delta():
    # +0.11pp absolute: fails the +0.1pp abs threshold even though the
    # relative jump (+110%) looks worse.
    results = _evaluate({
        "error_rate": 0.0021,
        "p99_latency_ms": 120,
        "cpu_pct": 45,
        "mem_pct": 60,
    })
    assert not metric_gate.gate(results)


def test_missing_metric_raises():
    try:
        metric_gate.evaluate(BASELINE, {"error_rate": 0.001})
    except KeyError as exc:
        assert "p99_latency_ms" in str(exc)
    else:
        raise AssertionError("expected KeyError for missing metrics")


def test_identical_metrics_promote():
    assert metric_gate.gate(_evaluate(dict(BASELINE)))
