# Skeleton Loading Placeholder Test Lab

Runnable companion for [Skeleton Loading Placeholder Test Cases](https://qapractices.com/test-cases/skeleton-loading-placeholder-test-cases/) — a stdlib-only Python state machine that mirrors the skeleton lifecycle (mount → min display time → success/error/timeout, retry, reduced-motion) plus a pytest suite exercising the failure modes from the resource.

## Run

```bash
pip install -r requirements.txt
pytest -v
```

## What it covers

| Test | Suite case |
|---|---|
| `test_skeleton_never_stays_loading` | TC-007/013/014 every outcome exits LOADING |
| `test_min_display_time_holds` | TC-009/016 flash floor at 300ms |
| `test_slow_load_shows_natural_duration` | TC-010 long load |
| `test_shimmer_runs_while_loading` | TC-002 shimmer active |
| `test_reduced_motion_disables_shimmer` | TC-022 static placeholder keeps ARIA |
| `test_content_exit_is_single_clean_swap` | TC-013 one swap, no double resolve |
| `test_error_exit_sets_aria_busy_false` | TC-007 error exit clears busy |
| `test_timeout_exit_is_retryable` | TC-014 timeout → retry → LOADING |
| `test_retry_restores_shimmer_and_busy` | TC-014 retry semantics |
| `test_no_retry_from_content` | Success is terminal |
| `test_analytics_event_fires_once` | TC-028 display-time event |
| `test_layout_match_within_tolerance` | TC-001 bounding-box ±2px |
| `test_layout_match_rejects_drift` | TC-011 geometry drift caught |
| `test_layout_match_rejects_count_mismatch` | TC-004 count contract |
| `test_aria_contract_while_loading` / `_after_exit` | TC-021 aria-busy + aria-hidden |
