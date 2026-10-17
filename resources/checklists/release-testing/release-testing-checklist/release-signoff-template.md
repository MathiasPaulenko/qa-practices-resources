# Release Sign-Off — {version} — {YYYY-MM-DD}

**Release captain:** {name} · **Window:** {start–end, timezone} · **Rollback owner:** {name}

## Gate 1 — Pre-Release (before deploy)

- [ ] CI green on release branch — no quarantined tests without sign-off — **Owner:** ___ — **Time:** ___
- [ ] Artifact tagged and traceable (SHA/semver): ___ — **Owner:** ___ — **Time:** ___
- [ ] Dependency + container scans clean or exceptions documented — **Owner:** ___ — **Time:** ___
- [ ] Migrations reviewed, rollback scripts tested in staging — **Owner:** ___ — **Time:** ___
- [ ] Env vars/secrets exist in production — **Owner:** ___ — **Time:** ___
- [ ] Monitoring + on-call confirmed for the window — **Owner:** ___ — **Time:** ___
- [ ] Rollback criteria agreed in numbers — **Owner:** ___ — **Time:** ___

## Gate 2 — Deployment (during)

- [ ] Deploy via pipeline only — **Owner:** ___ — **Time:** ___
- [ ] Health/readiness green before traffic shift — **Owner:** ___ — **Time:** ___
- [ ] Error rate / p95 / saturation watched during shift — **Owner:** ___ — **Time:** ___

## Gate 3 — Post-Release (first hour)

- [ ] Smoke script all green — **Owner:** ___ — **Time:** ___
- [ ] Critical journeys verified in production — **Owner:** ___ — **Time:** ___
- [ ] Metrics within normal bounds — **Owner:** ___ — **Time:** ___
- [ ] Stakeholders + support notified — **Owner:** ___ — **Time:** ___

## Rollback Record (fill only if triggered)

- Triggered by (criteria breached): ___
- Rolled back at: ___ · Verified healthy at: ___
- Root cause: ___
- Checklist item to add/change: ___

## Sign-off

- Release captain: ___ (date/time) ___
- Final status: ☐ Healthy ☐ Rolled back ☐ Degraded — follow-up ___
