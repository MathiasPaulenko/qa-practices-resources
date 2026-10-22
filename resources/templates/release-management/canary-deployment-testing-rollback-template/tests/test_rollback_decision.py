from rollback_decision import Decision, Metrics, Thresholds, evaluate


def healthy() -> Metrics:
    return Metrics(error_rate=0.3, p99_latency_ms=340, cpu_usage=68,
                   memory_usage=62, request_rate=25)


def test_healthy_canary_promotes():
    assert evaluate(healthy()).decision is Decision.PROMOTE


def test_error_rate_above_threshold_rolls_back():
    v = evaluate(Metrics(**{**healthy().__dict__, "error_rate": 2.1}))
    assert v.decision is Decision.ROLLBACK
    assert v.severity == "High"


def test_critical_error_rate_is_auto_rollback():
    v = evaluate(Metrics(**{**healthy().__dict__, "error_rate": 6.0}))
    assert v.decision is Decision.ROLLBACK
    assert v.severity == "Critical"
    assert v.decision_maker == "Auto-rollback"


def test_pod_crash_rolls_back_immediately():
    v = evaluate(Metrics(**{**healthy().__dict__, "pod_restarts": 1}))
    assert v.decision is Decision.ROLLBACK
    assert v.severity == "Critical"


def test_consecutive_failed_evals_rolls_back():
    v = evaluate(Metrics(**{**healthy().__dict__, "consecutive_failed_evals": 2}))
    assert v.decision is Decision.ROLLBACK


def test_max_canary_time_rolls_back():
    v = evaluate(Metrics(**{**healthy().__dict__, "canary_minutes": 120}))
    assert v.decision is Decision.ROLLBACK


def test_latency_2x_baseline_rolls_back():
    v = evaluate(Metrics(**{**healthy().__dict__, "p99_latency_ms": 1100}))
    assert v.decision is Decision.ROLLBACK


def test_latency_above_threshold_holds():
    v = evaluate(Metrics(**{**healthy().__dict__, "p99_latency_ms": 520}))
    assert v.decision is Decision.HOLD


def test_low_traffic_holds_for_significance():
    v = evaluate(Metrics(**{**healthy().__dict__, "request_rate": 3.0}))
    assert v.decision is Decision.HOLD
    assert "statistical floor" in v.reason


def test_business_metric_drop_rolls_back():
    v = evaluate(Metrics(**{**healthy().__dict__, "business_drop_pct": 12.0}))
    assert v.decision is Decision.ROLLBACK
    assert v.decision_maker == "Product + SRE"


def test_custom_thresholds():
    t = Thresholds(error_rate=0.5)
    v = evaluate(Metrics(**{**healthy().__dict__, "error_rate": 0.8}), t)
    assert v.decision is Decision.ROLLBACK
    assert "0.5%" in v.reason
