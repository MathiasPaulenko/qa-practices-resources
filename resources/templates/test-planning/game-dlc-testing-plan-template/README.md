# Game DLC Testing Plan — Data Files

Machine-readable test matrices for the [Game DLC Testing Plan Template](https://qapractices.com/templates/game-dlc-testing-plan-template/) on QAPractices.

## Files

| File | What it contains |
|---|---|
| `save-compatibility-matrix.json` | 8 save scenarios (base/DLC × installed/not, mid-quest, cross-platform, uninstall, rollback) with expected results — the rows that catch save corruption. |
| `certification-requirements.json` | Per-platform certification check categories (TRC, XR, Lotcheck, Steamworks, Epic) plus each platform's most common first failure. |

## How to use

1. Load `save-compatibility-matrix.json` into your test management tool — each scenario has an ID, expected result and category.
2. Track certification with `certification-requirements.json`: tick each check per platform; run the `common_first_failure` check in week one on a store sandbox.
3. Apply the `sign_off_rule`: no approval while Critical/High certification defects are open without a documented decision.

## Spanish

La [versión en español](README.es.md) describe los mismos archivos.
