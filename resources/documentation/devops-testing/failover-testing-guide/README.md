# Failover Testing Guide — Companion

Runnable artifacts for the [Failover Testing Guide: HA & Disaster Recovery](https://qapractices.com/documentation/failover-testing-guide/). Each file maps to an example in the guide so you can run the same checks during your own drills.

## Files

| File | Purpose |
| --- | --- |
| `litmus/chaosengine-pod-delete.yaml` | LitmusChaos 3.x `ChaosEngine` that deletes a random pod of the `payments` deployment — the automated failover test from the guide. |
| `postgres/replication-lag.sql` | `pg_stat_replication` query that measures replica lag in bytes on PostgreSQL 15+ — run it on the primary before and during the drill. |
| `scripts/lb-healthcheck-poll.sh` | Polls the load balancer every 2s while you terminate a backend; counts and flags every non-200 response. |
| `scripts/dr-drill-runbook.sh` | Timed DR drill skeleton: restore, deploy, wait for health, smoke test, report real elapsed time vs RTO. |

## Requirements

- LitmusChaos 3.x installed on the cluster + `litmus-admin` ServiceAccount (for the ChaosEngine)
- PostgreSQL 15+ with a streaming replica (for the lag query)
- `bash` and `curl` (for the scripts)

## Usage

### LitmusChaos pod-delete

```bash
kubectl apply -f litmus/chaosengine-pod-delete.yaml
kubectl get chaosresult payments-pod-delete-pod-delete -n litmus
```

### Replication lag

```bash
psql -h primary.db.internal -U readonly -d appdb -f postgres/replication-lag.sql
```

### Load balancer poll

```bash
BASE_URL=https://staging.qapractices.com/health ./scripts/lb-healthcheck-poll.sh
# In another terminal, terminate one backend instance and watch the output.
# Ctrl+C prints the total request count and how many were non-200.
```

### DR drill runbook

```bash
BACKUP_FILE=/backups/latest.dump TARGET_ENV=dr-restore ./scripts/dr-drill-runbook.sh
```

Replace the placeholder commands in `dr-drill-runbook.sh` with your actual restore, deploy and smoke-test commands — the script times the real recovery so you can compare it against your RTO target.

## Related

- Guide: <https://qapractices.com/documentation/failover-testing-guide/>
- Guía en español: <https://qapractices.com/es/documentation/failover-testing-guide/>
