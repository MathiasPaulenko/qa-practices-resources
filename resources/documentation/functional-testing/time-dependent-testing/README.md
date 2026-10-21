# Time-Dependent Testing — Runnable Companion

Companion for [How to Test Time-Dependent Features](https://qapractices.com/documentation/time-dependent-testing/) / [versión en español](https://qapractices.com/es/documentation/time-dependent-testing/).

`time-testing.mjs` implements the primitives the guide describes, with zero dependencies:

- **`makeFakeClock`** — a manually advanced clock; the unit every time test should depend on.
- **`TtlCache`** — TTL cache with exact boundary semantics: absolute expiration at insert + TTL, sliding expiration renewed on each read.
- **`shouldRunCronOnDate`** — the month-end cron rule: day 30 never fires in February, day 31 never fires in short months, day 29 only on leap Februaries.
- **`remainingBudget`** — deadline propagation: nested calls receive the remaining budget, not a fresh timeout.
- **`findDstFold`** — real DST fold detection: scans UTC instants against `America/New_York` wall time and returns the two instants where `01:30` occurs twice on fall-back Sunday.

## Run

```bash
node --test tests/time-testing.test.mjs
```

Requirements: Node.js 20+, standard library only.

## What it demonstrates

| Concept | Where |
|---|---|
| Inject the clock, never use `Date.now()` in logic | `makeFakeClock` |
| Expire exactly at TTL — T+3599 vs T+3600 | `TtlCache` + tests |
| Sliding vs absolute expiration | `TtlCache` `sliding` option |
| Cron day-of-month skip on short months | `shouldRunCronOnDate` |
| Deadlines propagate remaining budget | `remainingBudget` |
| DST fold is real and testable | `findDstFold` (2026-11-01, `America/New_York`) |
