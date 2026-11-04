# Feature Flag Interaction Testing — Companion

Runnable examples for the [Feature Flag Interaction Testing Checklist](https://qapractices.com/checklists/feature-flag-interaction-testing-checklist/).

## Files

| File | What it does |
|---|---|
| `flag-config.json` | Flag definitions with targeting, dependencies and conflicts — the shape a flag evaluator reads at runtime. |
| `flag_matrix_test.py` | Pytest suite that exercises **every 2^n combination** of a 3-flag set and asserts conflicts and missing dependencies resolve correctly. |
| `kill_switch_sim.py` | Simulation of kill-switch propagation across services with cached flag values — shows why a no-TTL cache breaks the kill. |

## Run

```bash
pip install -r requirements.txt
pytest flag_matrix_test.py -v   # 10 tests: 8 matrix states + default-state + config sanity
python kill_switch_sim.py       # watch a stale-cached worker ignore the kill switch
```

## What it demonstrates

- **Combination matrix coverage** — `itertools.product` generates all flag states; each state asserts the evaluator's decision.
- **Dependency and conflict resolution** — `newCheckout` requires `payment_v2` and conflicts with `legacyCheckout`; both rules are tested exhaustively.
- **Kill switch vs cache** — the worker caches flag values with a long TTL and keeps serving the killed feature, mirroring real incidents.
