# Chaos Engineering Experiment Document — CE-042 (Completed Sample)

Filled example: a pod-kill experiment on the payments API gateway at Northline Commerce, run in staging on a Friday morning game day.

## 1. Experiment Details

| Field | Details |
|---|---|
| **Experiment name** | API gateway pod-kill — HPA response |
| **Experiment ID** | CE-042 |
| **System under test** | api-gateway (Kubernetes, 12 replicas) |
| **Environment** | Staging |
| **Date** | 2026-11-13 |
| **Duration** | 12 minutes |
| **Experiment lead** | Dimitri Sokolov / QA Lead |
| **Chaos tool** | Chaos Mesh 2.7 |
| **Game day?** | Yes |

## 2. Hypothesis

> When we terminate 30% of the api-gateway pods in staging, P95 latency stays under 200 ms because the HPA replaces pods within 60 s and the load balancer drains unhealthy endpoints in under 5 s.

## 3. Blast Radius Control

| Control | Setting | Notes |
|---|---|---|
| **Affected traffic** | 5% of staging traffic | Synthetic load generator only |
| **Affected users** | None — staging | Synthetic users |
| **Affected services** | api-gateway only | Namespace-scoped selector |
| **Rollback method** | `kubectl annotate ... pause=true` | Tested before the run |
| **Max duration** | 10 minutes | Auto-abort after |
| **Business hours only** | Yes (10:00-12:00 UTC) | On-call notified |

## 4. Steady State Metrics (during experiment)

| Metric | Normal Value | During Experiment |
|---|---|---|
| **Error rate** | < 0.5% | 0.8% (pass) |
| **P95 latency** | < 200 ms | 310 ms for 40 s (breach) |
| **Throughput** | > 1000 req/s | 920 req/s (breach) |
| **Recovery time** | < 60 s | 92 s (fail) |

## 8. Findings and Actions

| Finding ID | Category | Description | Severity | Action Item | Owner | Due Date | Status |
|---|---|---|---|---|---|---|---|
| F-001 | Auto-scaler | HPA scaled on CPU only; pod count replaced in 92 s, not 60 s | Medium | Add custom metric on request rate | Ravi Iyer | 2026-11-27 | Open |
| F-002 | Alerting | Pod-termination alert fired 3 min late | High | Lower alert `for:` window to 30 s | Fatima Al-Rashid | 2026-11-20 | Open |

## 9. Sign-off

| Role | Name | Date | Decision |
|---|---|---|---|
| **Experiment Lead** | Dimitri Sokolov | 2026-11-13 | Completed — hypothesis partially failed |
| **SRE Lead** | Hannah Kim | 2026-11-13 | Findings acknowledged |
| **Engineering Manager** | Ana Gómez | 2026-11-14 | Actions approved |
