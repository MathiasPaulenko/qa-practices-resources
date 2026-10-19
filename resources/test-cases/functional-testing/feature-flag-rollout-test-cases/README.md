# Feature Flag Rollout Test Lab

Runnable companion for [Feature Flag Rollout Test Cases](https://qapractices.com/test-cases/feature-flag-rollout-test-cases/) — a stdlib-only Python flag evaluator that mirrors OpenFeature-style evaluation order (exists → enabled → prerequisites → user rule → segment rule → percentage bucket) plus a pytest suite exercising the deterministic-rollout failure modes from the resource.

## Run

```bash
pip install -r requirements.txt
pytest -v
```

## What it covers

| Test | Suite case |
|---|---|
| `test_rollout_is_deterministic` | TC-004 same user, same result |
| `test_rollout_distribution_is_plausible` | TC-004 ~50% split band |
| `test_zero_and_hundred_percent_boundaries` | TC-005 rollout bounds |
| `test_user_targeting_hits_and_misses` | TC-006 explicit user lists |
| `test_segment_targeting` | TC-007 segment membership |
| `test_rollout_increase_is_monotonic` | TC-010 nobody loses access |
| `test_missing_flag_returns_default` | TC-011 graceful default |
| `test_anonymous_user_gets_default` | TC-012 no user context |
| `test_bucket_boundary_is_exclusive` | TC-013 bucket == percentage |
| `test_user_deny_beats_segment_allow` | TC-014 rule precedence |
| `test_prerequisite_unmet_blocks_child` | TC-016 dependency gate |
| `test_prerequisite_met_lets_child_evaluate` | TC-017 dependency satisfied |
| `test_rapid_toggling_last_write_wins` | TC-018 toggle ordering |
| `test_ab_variant_is_stable` / `test_ab_variants_distribute` | TC-023 variant assignment |
| `test_flag_evaluation_latency` | Latency budget (1000 evals < 100 ms) |

## Find a boundary user (TC-013)

```bash
python tests/find_bucket.py new-dashboard 50
```

Prints the first `user-NNNNN` whose sha256 bucket is exactly 50 — the user you evaluate at 50% vs 51% to verify the inclusive/exclusive boundary.
