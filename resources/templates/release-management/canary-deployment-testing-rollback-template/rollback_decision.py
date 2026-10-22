"""Rollback decision evaluator for canary deployments.

Implements the trigger thresholds and the decision matrix from the
QAPractices canary deployment testing and rollback template:

- Auto-rollback triggers: error rate > 1% for 2 min, p99 > 500 ms for 3 min,
  pod crashes, 2 consecutive failed evaluations, max canary time exceeded.
- Decision matrix severities: Critical / High / Medium with the matching
  action and decision maker.

Stdlib only.
"""

from dataclasses import dataclass
from enum import Enum


class Decision(Enum):
    PROMOTE = "promote"
    HOLD = "hold"
    ROLLBACK = "rollback"


@dataclass(frozen=True)
class Thresholds:
    error_rate: float = 1.0          # percent
    p99_latency_ms: int = 500
    cpu_usage: float = 80.0          # percent
    memory_usage: float = 75.0       # percent
    min_request_rate: float = 10.0   # req/s
    consecutive_failures: int = 2
    max_canary_minutes: int = 120


@dataclass(frozen=True)
class Metrics:
    error_rate: float = 0.0
    p99_latency_ms: int = 0
    cpu_usage: float = 0.0
    memory_usage: float = 0.0
    request_rate: float = 0.0
    pod_restarts: int = 0
    consecutive_failed_evals: int = 0
    canary_minutes: int = 0
    business_drop_pct: float = 0.0  # percent below baseline


@dataclass(frozen=True)
class Verdict:
    decision: Decision
    reason: str
    severity: str
    decision_maker: str


def evaluate(metrics: Metrics, thresholds: Thresholds | None = None) -> Verdict:
    """Evaluate canary metrics and return a promote/hold/rollback verdict."""
    t = thresholds or Thresholds()

    # Hard auto-rollback triggers, evaluated in severity order.
    if metrics.error_rate > 5.0:
        return Verdict(Decision.ROLLBACK, "error rate above 5%", "Critical", "Auto-rollback")
    if metrics.pod_restarts > 0:
        return Verdict(Decision.ROLLBACK, "pod crash loop detected", "Critical", "Auto-rollback")
    if metrics.consecutive_failed_evals >= t.consecutive_failures:
        return Verdict(Decision.ROLLBACK, f"{metrics.consecutive_failed_evals} consecutive failed evaluations", "High", "Auto-rollback")
    if metrics.canary_minutes >= t.max_canary_minutes:
        return Verdict(Decision.ROLLBACK, "max canary time exceeded", "High", "Auto-rollback")
    if metrics.error_rate > t.error_rate:
        return Verdict(Decision.ROLLBACK, f"error rate {metrics.error_rate}% above threshold {t.error_rate}%", "High", "SRE on-call")
    if metrics.p99_latency_ms > 2 * t.p99_latency_ms:
        return Verdict(Decision.ROLLBACK, f"p99 {metrics.p99_latency_ms}ms above 2x baseline", "High", "SRE on-call")
    if metrics.business_drop_pct > 10.0:
        return Verdict(Decision.ROLLBACK, f"business metric dropped {metrics.business_drop_pct}%", "High", "Product + SRE")

    # Watch conditions — hold rather than promote.
    if metrics.p99_latency_ms > t.p99_latency_ms:
        return Verdict(Decision.HOLD, f"p99 {metrics.p99_latency_ms}ms above threshold", "Medium", "SRE on-call")
    if metrics.request_rate < t.min_request_rate:
        return Verdict(Decision.HOLD, f"only {metrics.request_rate} req/s — below statistical floor", "Medium", "SRE on-call")
    if metrics.cpu_usage > t.cpu_usage or metrics.memory_usage > t.memory_usage:
        return Verdict(Decision.HOLD, "resource usage above threshold", "Medium", "SRE on-call")

    return Verdict(Decision.PROMOTE, "all metrics within thresholds", "None", "Pipeline")
