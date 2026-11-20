# Framework Setup Document

## 1. Header

| Field | Value |
|---|---|
| **Project** | [Product or app name] |
| **Framework codename** | [Internal name] |
| **Owner** | [Person accountable] |
| **Created / Last review** | [YYYY-MM-DD / YYYY-MM-DD] |
| **Status** | [Draft / Active / Deprecated] |

## 2. Scope

- **Application under test:** [Name plus URL or repo]
- **Test types in scope:** [e.g. UI E2E smoke + regression]
- **Browsers / environments:** [e.g. Chromium + Firefox on staging]

## 3. Stack Decision

| Layer | Choice | Version | Rationale |
|---|---|---|---|
| Language | [e.g. TypeScript] | [e.g. 5.4] | [Why this over alternatives] |
| Test runner | [e.g. Playwright Test] | [e.g. 1.44] | [Why this runner] |
| Assertion library | [e.g. bundled expect] | [bundled] | [Why] |
| Reporting | [e.g. built-in HTML report] | [version or bundled] | [Why] |
| CI runner | [e.g. GitHub Actions] | [runner image] | [Why] |

## 4. Repository Layout

Paste the real output of `tree -L 3`, not an aspirational diagram:

```text
[repo-root]/
├── tests/              # Spec files, grouped by feature
│   └── e2e/
├── pages/              # Page objects, one class per page or component
├── core/
│   ├── config/         # Environment config, base URLs, timeouts
│   └── fixtures/       # Shared fixtures and test data factories
├── infra/              # Runner config, Docker, CI workflow
└── docs/
    └── framework-setup.md   # This document
```

## 5. Configuration Files

- `[runner config]` — [projects, timeouts, retries, base URL]
- `[.env.example]` — [committed placeholder env file; secrets never committed]
- `[CI workflow]` — [pipeline stage that runs the suite]
- `[lint config]` — [rules enforcing the coding standards]

## 6. Environment Variables

| Variable | Purpose | Example |
|---|---|---|
| [BASE_URL] | [Target environment] | [https://staging.internal/app] |
| [TEST_USER_EMAIL] | [Seeded test account] | [qa-bot@yourco.test] |
| [API_TOKEN] | [Auth for API seeding] | [never committed — CI secret] |

## 7. Coding Standards

- File naming: [e.g. `feature-name.spec.ts`; page objects `PascalCase.ts`]
- Selectors: [e.g. `data-testid` attributes only, no CSS/XPath in specs]
- Test data: [e.g. factories in `core/fixtures/`, no hardcoded IDs in specs]
- Waits: [e.g. auto-waiting assertions only, no `waitForTimeout`]

## 8. Setup Definition of Done

- [ ] Repo scaffolded with the layout above and one passing smoke spec
- [ ] Config files committed: runner config, env template, lint rules
- [ ] CI job green on `main` and required on pull requests
- [ ] One real test written following the standards, reviewed via PR
- [ ] This document reviewed by the team and merged
