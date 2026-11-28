```text
INT001 | Automation | Hard
Question: Your Playwright suite has 300 tests and a 12% flake rate. How do
you bring it under control?
Model answer: I'd start by classifying flakes — in my experience most fall
into timing issues, test data collisions, or environment drift. I'd add
Playwright trace capture on retries to see actual failures, quarantine the
worst offenders into a separate job so they stop blocking the pipeline, and
fix from the top of the flake leaderboard rather than randomly. In my last
project this took the flake rate from ~10% to under 2% in six weeks.
Interviewer's lens: they want a systematic method, not "add retries".
Follow-ups: "How do you decide between fixing and deleting a flaky test?"
Red flags: blaming the tool, suggesting retry-count increases as the fix.

INT002 | API | Medium
Question: What's the difference between contract testing and schema
validation, and when do you need each?
Model answer: Schema validation checks that a response matches a declared
structure — types, required fields. Contract testing, like Pact, goes
further: it verifies the consumer and provider agree on the interaction,
including fields the consumer actually uses. I'd use schema validation as
a smoke gate on every API response, and contract tests between services
that deploy independently.
Interviewer's lens: do they understand consumer-driven contracts or just
know the buzzword?
Follow-ups: "Who owns the contract — consumer or provider?"
Red flags: treating them as interchangeable terms.
```
