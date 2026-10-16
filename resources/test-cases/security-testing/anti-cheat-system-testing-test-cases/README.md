# Anti-Cheat System Testing — Companion

Reference server-side checks used in the article
[Anti-Cheat System Testing](https://qapractices.com/test-cases/anti-cheat-system-testing-test-cases/):

- `validate_move` — flags position updates faster than the physics model
  allows, with a jitter margin so high-latency players are not flagged.
- `aim_snap_rate` — fraction of aim snaps below a humanly plausible
  threshold (TC-02 metric).
- `bans_missing_evidence` — audit helper mirroring the SQL query in the
  article: every ban needs a confidence score and a replay link (TC-07).

## Run

```bash
pip install -r requirements.txt
pytest tests/
```

Covered test cases: TC-01 (speed hack), the high-latency edge case,
TC-02 (aimbot snap rate) and TC-07 (ban evidence audit).
