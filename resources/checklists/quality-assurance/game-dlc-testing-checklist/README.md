# Game DLC Testing — Companion

Runnable examples for the [Game DLC Testing Checklist](https://qapractices.com/checklists/game-dlc-testing-checklist/).

## Files

| File | What it does |
|---|---|
| `dlc-manifest.json` | DLC manifest example: platforms, regions, minimum base version and dependencies. |
| `manifest_validator_test.py` | Pytest suite validating the manifest — required fields, semver format, platform/region whitelists, no self-dependencies, exclusivity disjointness. |
| `entitlement_flow.py` | Simulation of the classic refund bug: the store revokes the entitlement but the game's cached unlock flag keeps the content visible. |

## Run

```bash
pip install -r requirements.txt
pytest manifest_validator_test.py -v   # 7 manifest validation tests
python entitlement_flow.py             # watch the stale unlock flag survive a refund
```

## What it demonstrates

- **Manifest validation beyond "does it parse"** — version format, known platforms/regions and dependency sanity are the config bugs that actually ship broken DLC.
- **The revoke path is the untested path** — `entitlement_flow.py` shows a game that only caches the unlock flag: after a refund, players keep the paid content. The fix is re-checking entitlement on load.
