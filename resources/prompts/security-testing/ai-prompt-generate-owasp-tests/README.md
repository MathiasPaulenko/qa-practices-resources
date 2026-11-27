# AI Prompt: OWASP Top 10 Test Cases

Copy-ready files for the
[AI Prompt: OWASP Top 10 Test Cases](https://qapractices.com/prompts/ai-prompt-generate-owasp-tests/)
resource on QAPractices.com.

## Files

- `prompt-template.txt` — the full prompt; fill the bracketed placeholders
  with your application, stack, auth model and scope.
- `example-input.txt` — a filled-in example (invoicing web app,
  React + Node.js + PostgreSQL, JWT auth).
- `example-output.md` — a sample of the case table the prompt produces
  (OWASP-001 to OWASP-008 plus a gap note).
- `owasp-probes.csv` — a seed list of safe, non-destructive probes per
  category for fuzzers or data-driven suites.

## Safety

Payloads are fixture strings and detection probes meant for staging
environments. Never run them against production or third-party services
without written authorization.
