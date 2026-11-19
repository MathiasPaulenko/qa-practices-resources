# QA Retrospective Workshop Document

> Fill-in facilitation document for a QA team retro: timed agenda, prompts, metrics, action items, sentiment pulse.
> Companion to https://qapractices.com/templates/workshop-retrospective-template-qa-teams/

## Workshop Information

| Field | Details |
|---|---|
| **Date** | [YYYY-MM-DD, e.g. 2025-01-15] |
| **Facilitator** | [Name, e.g. Tomás Reyes] |
| **Duration** | 90 minutes |
| **Participants** | [List names] |
| **Sprint / Release** | [Sprint XX / Release X.Y] |
| **Previous Retro** | [Date, e.g. 2025-01-15] |

---

## Agenda (90 minutes)

| Time | Activity | Format | Output |
|---|---|---|---|
| 0-5 min | Welcome and ground rules | Facilitator speaks | Shared understanding |
| 5-15 min | Data gathering: What happened? | Individual silent writing | Sticky notes |
| 15-30 min | Group and theme | Small groups | Clustered themes |
| 30-50 min | Deep dive discussion | Full group | Insights and root causes |
| 50-65 min | Action items generation | Individual then group | Proposed actions |
| 65-75 min | Voting on priorities | Dot voting | Top 3 actions |
| 75-85 min | Assign owners and dates | Full group | Committed actions |
| 85-90 min | Retro on the retro | Full group | Feedback on process |

---

## Data Gathering Prompts

### What Went Well

| Prompt | Responses |
|---|---|
| What testing achievements are you proud of? | [e.g. Caught the payment rounding bug pre-release] |
| Which processes worked smoothly? | [e.g. Triage in under 24h all sprint] |
| What tools or techniques saved time? | [e.g. Contract tests replaced manual API checks] |
| Which collaborations were effective? | [e.g. Dev pairing on the flaky suite] |

### What Didn't Go Well

| Prompt | Responses |
|---|---|
| What blockers slowed testing? | [e.g. Staging down two afternoons] |
| Which defects should have been caught earlier? | [e.g. Currency formatting escaped to UAT] |
| What processes felt inefficient? | [e.g. Re-running full regression for one-line fixes] |
| Where did communication break down? | [e.g. Release notes reached QA the day of deploy] |

### What Can We Improve

| Prompt | Responses |
|---|---|
| What should we start doing? | [e.g. Smoke suite as a CI merge gate] |
| What should we stop doing? | [e.g. Manual test case entry in two tools] |
| What should we do differently? | [e.g. Rotate who verifies fixes] |
| What skills do we need to develop? | [e.g. Contract testing, DB debugging] |

---

## Metrics Review

| Metric | This Sprint | Last Sprint | Trend | Discussion |
|---|---|---|---|---|
| Test coverage | [74]% | [71]% | [↑/↓/→] | [e.g. New API suite added 3pts] |
| Defects found | [23] | [31] | [↑/↓/→] | [e.g. Earlier testing, fewer late finds] |
| Defect escape rate | [4]% | [7]% | [↑/↓/→] | [e.g. Two escapes both currency-related] |
| Automation rate | [62]% | [58]% | [↑/↓/→] | [e.g. 12 cases migrated to Playwright] |
| Test pass rate | [96]% | [93]% | [↑/↓/→] | [e.g. Flaky checkout test fixed] |
| Avg PR review time | [9]h | [14]h | [↑/↓/→] | [e.g. Review rotation helped] |

---

## Action Items

| Action | Owner | Priority | Due Date | Status | Follow-up |
|---|---|---|---|---|---|
| [e.g. Add smoke suite as CI merge gate] | [Name, e.g. Rajiv Kapoor] | High | [Date, e.g. 2025-01-29] | [ ] | Next retro |
| [e.g. Split flaky checkout spec into 3 focused tests] | [Name, e.g. Mateo Rossi] | High | [Date, e.g. 2025-01-29] | [ ] | Next retro |
| [e.g. Document staging outage escalation path] | [Name, e.g. Maria Silva] | Medium | [Date, e.g. 2025-02-05] | [ ] | Next retro |
| [e.g. Create currency formatting test cases] | [Name, e.g. Svetlana Volkov] | Medium | [Date, e.g. 2025-02-05] | [ ] | Next retro |
| [e.g. Pilot pair-testing on the billing module] | [Name, e.g. Kwame Asante] | Low | [Date, e.g. 2025-02-12] | [ ] | Next retro |

---

## Previous Action Items Review

| Action from Last Retro | Owner | Completed | Notes |
|---|---|---|---|
| [e.g. Adopt contract tests for partner API] | [Name, e.g. David Okafor] | [Yes/No, e.g. Yes] | [e.g. Live since sprint 14] |
| [e.g. Reduce regression suite runtime under 30min] | [Name, e.g. Nina Petrova] | [Yes/No, e.g. No] | [e.g. Still 45min; carried over] |
| [e.g. Add test data reset script] | [Name, e.g. Carlos Méndez] | [Yes/No, e.g. Yes] | [e.g. Saves ~1h per run] |

---

## Team Sentiment

| Question | Score (1-5) | Trend |
|---|---|---|
| How confident are you in our test coverage? | [ ] | [↑/↓/→] |
| How satisfied are you with our processes? | [ ] | [↑/↓/→] |
| How is the team workload balance? | [ ] | [↑/↓/→] |
| How effective is our communication? | [ ] | [↑/↓/→] |
| How do you feel about team morale? | [ ] | [↑/↓/→] |

---

## Ground Rules

- **Everyone participates** — all voices matter
- **No blame** — focus on process, not people
- **Be specific** — vague items cannot be actioned
- **Stay on topic** — timebox tangents
- **Commit to actions** — no action items without owners
- **Follow up** — track actions to closure

