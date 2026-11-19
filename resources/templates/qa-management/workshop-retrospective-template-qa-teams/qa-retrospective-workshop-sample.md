# QA Retrospective Workshop — Completed Sample

> Post-sprint retro after a rough release, facilitated for a six-person QA team.
> Companion to https://qapractices.com/templates/workshop-retrospective-template-qa-teams/

## Workshop Information

| Field | Details |
|---|---|
| **Date** | 2025-01-15 |
| **Facilitator** | Tomás Reyes |
| **Duration** | 90 minutes |
| **Participants** | Rajiv, Mateo, Maria, Svetlana, Kwame, Ana |
| **Sprint / Release** | Sprint 15 / Release 4.2 |
| **Previous Retro** | 2024-12-18 |

## Data Gathering — Key Responses

### What Went Well

- Caught the payment rounding bug pre-release.
- Triage closed in under 24h all sprint.
- Dev pairing unstuck the flaky suite.

### What Didn't Go Well

- Staging was down two afternoons, blocking exploratory testing.
- Currency formatting escaped to UAT — two defects.
- Release notes reached QA on deploy day.

### What Can We Improve

- Start: smoke suite as a CI merge gate.
- Stop: entering test cases in two tools.
- Differently: rotate who verifies fixes.

## Metrics Review

| Metric | This Sprint | Last Sprint | Trend | Discussion |
|---|---|---|---|---|
| Test coverage | 74% | 71% | ↑ | New API suite added 3pts |
| Defects found | 23 | 31 | ↓ | Earlier testing, fewer late finds |
| Defect escape rate | 4% | 7% | ↓ | Two escapes, both currency formatting |
| Automation rate | 62% | 58% | ↑ | 12 cases migrated to Playwright |
| Test pass rate | 96% | 93% | ↑ | Flaky checkout test fixed |
| Avg PR review time | 9h | 14h | ↓ | Review rotation helped |

## Action Items

| Action | Owner | Priority | Due Date | Status | Follow-up |
|---|---|---|---|---|---|
| Add smoke suite as CI merge gate | Rajiv Kapoor | High | 2025-01-29 | [x] | Done sprint 16 |
| Create currency formatting test cases | Svetlana Volkov | Medium | 2025-02-05 | [ ] | In progress |
| Document staging outage escalation path | Maria Silva | Medium | 2025-02-05 | [ ] | Drafted |

## Previous Action Items Review

| Action from Last Retro | Owner | Completed | Notes |
|---|---|---|---|
| Adopt contract tests for partner API | David Okafor | Yes | Live since sprint 14 |
| Reduce regression suite under 30min | Nina Petrova | No | Still 45min; carried over |

## Team Sentiment

| Question | Score (1-5) | Trend |
|---|---|---|
| Confidence in test coverage | 3.8 | ↑ |
| Satisfaction with processes | 3.4 | ↑ |
| Workload balance | 3.1 | → |
| Communication effectiveness | 4.0 | ↑ |
| Team morale | 3.6 | ↑ |
