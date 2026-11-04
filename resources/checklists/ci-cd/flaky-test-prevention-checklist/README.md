# Flaky Test Prevention Checklist — Companion

Runnable assets for the [Flaky Test Prevention Checklist](https://qapractices.com/checklists/flaky-test-prevention-checklist/).

## Files

| File | What it does |
|---|---|
| `auto-wait.spec.ts` | Playwright 1.48 spec showing the auto-waiting pattern — `toBeEnabled()` polls instead of `waitForTimeout(500)`. Includes an anti-pattern comment for contrast. |
| `repeat-until-failure.sh` | Loops a spec up to N times (default 20) and stops at the first failure — the deterministic-proof script from the checklist, with the `{1..20}` brace expansion that actually iterates. |
| `quarantine-workflow.md` | The quarantine process the CI-management items imply: tag → ticket → owner → SLA → fix-or-delete, with retry visibility kept. |

## Run

```bash
npx playwright test auto-wait.spec.ts        # auto-waiting demo
./repeat-until-failure.sh login.spec.ts 20   # prove a test is deterministic
```

## What it demonstrates

- **Conditions beat durations** — polling assertions replace every `sleep()`.
- **Flakiness is provable** — a loop that never fails beats a hunch that it does.
- **Quarantine is a process** — owner, SLA, and a fix-or-delete exit, not a `// TODO` forever.
