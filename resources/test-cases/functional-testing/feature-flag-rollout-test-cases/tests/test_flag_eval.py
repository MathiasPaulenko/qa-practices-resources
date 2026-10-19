"""Pytest suite for the flag evaluator, mapped to the resource's TCs."""

import time

import pytest

from flag_eval import FlagRule, bucket, evaluate


@pytest.fixture
def flags():
    """A flag set mirroring the TaskFlow examples in the resource."""
    return {
        "new-checkout-flow": FlagRule(key="new-checkout-flow", enabled=True),
        "new-dashboard": FlagRule(key="new-dashboard", enabled=True, percentage=50),
        "beta-feature": FlagRule(
            key="beta-feature",
            enabled=True,
            users_on=frozenset({"alice@taskflow.io", "bob@taskflow.io"}),
            users_off=frozenset({"carol@taskflow.io"}),
            segments_on=frozenset({"beta-testers"}),
        ),
        "new-reporting": FlagRule(
            key="new-reporting", enabled=True, prerequisites=("new-dashboard",)
        ),
        "checkout-design": FlagRule(
            key="checkout-design",
            enabled=True,
            percentage=100,
            variants=("control", "variant-a", "variant-b"),
        ),
    }


# TC-004 — percentage rollout determinism
def test_rollout_is_deterministic(flags):
    results = {
        evaluate("new-dashboard", flags, "user-0042")[0] for _ in range(100)
    }
    assert len(results) == 1


# TC-004 — a 50% rollout lands near 50%
def test_rollout_distribution_is_plausible(flags):
    enabled = sum(
        evaluate("new-dashboard", flags, f"user-{i}")[0] for i in range(500)
    )
    assert 200 < enabled < 300  # ~50% of 500, wide band for hash noise


# TC-005 — 0% and 100% are true bounds
def test_zero_and_hundred_percent_boundaries(flags):
    users = [f"user-{i}" for i in range(200)]
    zero = FlagRule(key="f", enabled=True, percentage=0)
    hundred = FlagRule(key="f", enabled=True, percentage=100)
    for f in (zero, hundred):
        flags["f"] = f
        vals = {evaluate("f", flags, u)[0] for u in users}
        assert vals == ({False} if f.percentage == 0 else {True})


# TC-006 — explicit user targeting
def test_user_targeting_hits_and_misses(flags):
    assert evaluate("beta-feature", flags, "alice@taskflow.io") == (True, "TARGETING_MATCH")
    assert evaluate("beta-feature", flags, "bob@taskflow.io")[0] is True
    assert evaluate("beta-feature", flags, "dave@taskflow.io")[0] is False


# TC-007 — segment targeting
def test_segment_targeting(flags):
    assert evaluate(
        "beta-feature", flags, "carla@taskflow.io", frozenset({"beta-testers"})
    ) == (True, "TARGETING_MATCH")
    assert evaluate("beta-feature", flags, "carla@taskflow.io")[0] is False


# TC-010 — rollout increases are monotonic
def test_rollout_increase_is_monotonic():
    users = [f"user-{i}" for i in range(300)]
    f10 = {"f": FlagRule(key="f", enabled=True, percentage=10)}
    f50 = {"f": FlagRule(key="f", enabled=True, percentage=50)}
    at_10 = {u for u in users if evaluate("f", f10, u)[0]}
    at_50 = {u for u in users if evaluate("f", f50, u)[0]}
    assert at_10 <= at_50


# TC-011 — missing flag returns the documented default
def test_missing_flag_returns_default(flags):
    assert evaluate("does-not-exist", flags, "user-0042") == (False, "DEFAULT")


# TC-012 — anonymous evaluation is deterministic and off
def test_anonymous_user_gets_default(flags):
    first = evaluate("new-dashboard", flags, None)
    second = evaluate("new-dashboard", flags, None)
    assert first == second == (False, "DEFAULT")


# TC-013 — bucket == percentage boundary follows the documented rule
def test_bucket_boundary_is_exclusive(flags):
    target = next(u for u in (f"u{i}" for i in range(10_000)) if bucket("new-dashboard", u) == 50)
    at_50 = FlagRule(key="new-dashboard", enabled=True, percentage=50)
    at_51 = FlagRule(key="new-dashboard", enabled=True, percentage=51)
    flags["new-dashboard"] = at_50
    assert evaluate("new-dashboard", flags, target)[0] is False
    flags["new-dashboard"] = at_51
    assert evaluate("new-dashboard", flags, target)[0] is True


# TC-014 — user deny rule beats segment allow rule
def test_user_deny_beats_segment_allow(flags):
    value, reason = evaluate(
        "beta-feature", flags, "carol@taskflow.io", frozenset({"beta-testers"})
    )
    assert (value, reason) == (False, "TARGETING_MATCH")


# TC-016 / TC-017 — prerequisites gate the child flag
def test_prerequisite_unmet_blocks_child(flags):
    flags["new-dashboard"].enabled = False
    value, reason = evaluate("new-reporting", flags, "user-0042")
    assert (value, reason) == (False, "PREREQUISITE_UNMET")


def test_prerequisite_met_lets_child_evaluate(flags):
    flags["new-dashboard"].percentage = 100
    value, _ = evaluate("new-reporting", flags, "user-0042")
    assert value is True


# TC-018 — last toggle wins
def test_rapid_toggling_last_write_wins(flags):
    flag = flags["new-checkout-flow"]
    flag.enabled = True
    flag.enabled = False
    flag.enabled = True
    assert evaluate("new-checkout-flow", flags, "user-0042")[0] is True


# TC-023 — A/B variant assignment is stable per user
def test_ab_variant_is_stable(flags):
    first = evaluate("checkout-design", flags, "user-0042")[0]
    for _ in range(100):
        assert evaluate("checkout-design", flags, "user-0042")[0] == first


def test_ab_variants_distribute(flags):
    seen = {
        evaluate("checkout-design", flags, f"user-{i}")[0] for i in range(600)
    }
    assert seen == {"control", "variant-a", "variant-b"}


# Latency — 1000 local evaluations stay well under 100 ms
def test_flag_evaluation_latency(flags):
    start = time.perf_counter()
    for i in range(1000):
        evaluate("new-dashboard", flags, f"user-{i}")
    elapsed_ms = (time.perf_counter() - start) * 1000
    assert elapsed_ms < 100
