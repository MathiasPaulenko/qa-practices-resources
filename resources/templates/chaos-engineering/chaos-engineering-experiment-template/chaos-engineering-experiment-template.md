# Chaos Engineering Experiment Document

## 1. Experiment Details

| Field | Details |
|---|---|
| **Experiment name** | [Short name, e.g. API gateway pod-kill] |
| **Experiment ID** | CE-[NNN] |
| **System under test** | [Service / cluster / system] |
| **Environment** | Staging / Production |
| **Date** | [YYYY-MM-DD] |
| **Duration** | [X minutes] |
| **Experiment lead** | [Name / role] |
| **Chaos tool** | [Chaos Mesh / Litmus / Gremlin / Azure Chaos Studio] |
| **Game day?** | Yes / No |

## 2. Hypothesis

| Field | Details |
|---|---|
| **Steady state** | System handles [failure type] without user-visible impact |
| **Hypothesis** | When [failure injected], then [expected behavior] because [reasoning] |
| **If hypothesis fails** | [What we learn / what action we take] |
| **Confidence level** | High / Medium / Low |

## 3. Blast Radius Control

| Control | Setting | Notes |
|---|---|---|
| **Affected traffic** | [e.g. 5% of total] | [Limit rationale] |
| **Affected users** | [e.g. Internal test users only] | |
| **Affected services** | [Service list] | |
| **Affected region** | [Region] | |
| **Rollback method** | [How to stop] | |
| **Max duration** | [X minutes] | Auto-abort after |
| **Business hours only** | Yes / No | |

## 4. Steady State Metrics

| Metric | Source | Normal Value | Abort Threshold | During Experiment |
|---|---|---|---|---|
| **Error rate** | [Source] | [Value] | [Threshold] | [ ] |
| **P95 latency** | [Source] | [Value] | [Threshold] | [ ] |
| **Throughput** | [Source] | [Value] | [Threshold] | [ ] |
| **Success rate** | [Source] | [Value] | [Threshold] | [ ] |

## 5. Failure Injection Plan

| Step | Action | Target | Duration | Expected Impact | Status |
|---|---|---|---|---|---|
| **1. Baseline** | Capture steady state metrics | All services | 5 min | None | [ ] |
| **2. Inject failure** | [Fault to inject] | [Target] | [Duration] | [Expected impact] | [ ] |
| **3. Observe** | Monitor metrics and alerts | All services | [Duration] | [What to watch] | [ ] |
| **4. Verify recovery** | Check system recovers | [Target] | [Duration] | Capacity restored | [ ] |
| **5. Stop injection** | Halt chaos tool | [Target] | Immediate | Failure removed | [ ] |
| **6. Post-experiment** | Capture final metrics | All services | 5 min | Return to steady state | [ ] |

## 6. Automated Abort Conditions

| Condition | Threshold | Action | Detection Method |
|---|---|---|---|
| [Condition] | [Threshold] | Stop experiment | [Alert source] |
| Manual abort | Experiment lead triggers | Stop immediately | Tool UI / CLI |
| Time limit | [X min] elapsed | Auto-stop | Timer |

## 7. Experiment Results

| Metric | Baseline | During Experiment | After Recovery | Hypothesis Pass? |
|---|---|---|---|---|
| [Metric] | [Value] | [Value] | [Value] | [ ] |

## 8. Findings and Actions

| Finding ID | Category | Description | Severity | Action Item | Owner | Due Date | Status |
|---|---|---|---|---|---|---|---|
| F-001 | [Category] | [What went wrong or surprised you] | [High/Med/Low] | [What to fix] | [Name] | [YYYY-MM-DD] | [ ] |

## 9. Sign-off

| Role | Name | Date | Decision |
|---|---|---|---|
| **Experiment Lead** | [Name] | [YYYY-MM-DD] | [Completed / Aborted] |
| **SRE Lead** | [Name] | [YYYY-MM-DD] | [Findings acknowledged] |
| **Engineering Manager** | [Name] | [YYYY-MM-DD] | [Actions approved] |
