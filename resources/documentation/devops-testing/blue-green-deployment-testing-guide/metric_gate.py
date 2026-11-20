"""Compare green metrics against the blue baseline and decide promote or rollback.

Reads two JSON snapshots with the same keys:

    {"error_rate": 0.001, "p99_latency_ms": 120, "cpu_pct": 45, "mem_pct": 60}

Thresholds express the maximum allowed *relative* increase over baseline
(e.g. 0.20 = green may be at most 20% worse than blue). ``error_rate`` is
compared as an absolute delta instead, since relative deltas on tiny
rates are meaningless.

Usage:
    python metric_gate.py metrics_baseline.json metrics_green_sample.json
"""
import json
import sys
from dataclasses import dataclass
from pathlib import Path

# metric -> (max allowed delta, mode). mode "rel" = relative, "abs" = absolute.
THRESHOLDS = {
    "error_rate": (0.001, "abs"),   # +0.1 percentage point
    "p99_latency_ms": (0.20, "rel"),  # +20%
    "cpu_pct": (0.15, "rel"),       # +15%
    "mem_pct": (0.10, "rel"),       # +10%
}


@dataclass
class MetricResult:
    name: str
    baseline: float
    candidate: float
    delta: float
    mode: str
    passed: bool


def _delta(baseline: float, candidate: float, mode: str) -> float:
    if mode == "abs":
        return candidate - baseline
    if baseline == 0:
        return 0.0 if candidate == 0 else float("inf")
    return (candidate - baseline) / baseline


def evaluate(baseline: dict, candidate: dict) -> list[MetricResult]:
    results = []
    for name, (limit, mode) in THRESHOLDS.items():
        if name not in baseline or name not in candidate:
            raise KeyError(f"missing metric '{name}' in a snapshot")
        d = _delta(baseline[name], candidate[name], mode)
        results.append(
            MetricResult(
                name=name,
                baseline=baseline[name],
                candidate=candidate[name],
                delta=d,
                mode=mode,
                passed=d <= limit,
            )
        )
    return results


def gate(results: list[MetricResult]) -> bool:
    return all(r.passed for r in results)


def _fmt_delta(r: MetricResult) -> str:
    if r.mode == "abs":
        return f"{r.delta:+.4f}"
    return f"{r.delta * 100:+.1f}%"


def main(argv: list[str]) -> int:
    baseline = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    candidate = json.loads(Path(argv[2]).read_text(encoding="utf-8"))
    results = evaluate(baseline, candidate)
    for r in results:
        verdict = "PASS" if r.passed else "FAIL"
        print(f"{verdict} {r.name}: blue={r.baseline} green={r.candidate} delta={_fmt_delta(r)}")
    if gate(results):
        print("GATE: promote green")
        return 0
    print("GATE: rollback to blue")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
