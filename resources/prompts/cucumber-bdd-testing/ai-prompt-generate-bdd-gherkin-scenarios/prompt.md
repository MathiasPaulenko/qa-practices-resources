# AI Prompt: Generate BDD Gherkin Scenarios

Copy the block under **The Prompt**, replace the bracketed placeholders with your story, and paste it into your LLM of choice. `password-reset.feature` shows the output the prompt produces when fed the example input below.

## The Prompt

```text
You are an expert BDD practitioner specializing in writing Gherkin scenarios. I need you to generate BDD scenarios from the following user story and acceptance criteria.

## User Story
As a [role]
I want to [action]
So that [benefit]

## Acceptance Criteria
1. [AC 1 - specific, testable criterion]
2. [AC 2 - specific, testable criterion]
3. [AC 3 - specific, testable criterion]

## Feature Context
- Feature name: [Descriptive name]
- Application type: [Web / Mobile / API / Desktop]
- User roles: [List of roles involved]
- Business rules: [Relevant business rules and constraints]
- Integration points: [External systems or APIs involved]
- BDD runner: [Cucumber / Behave / SpecFlow / other]

## Scenario Requirements

1. **Happy Path Scenarios** (3-5)
   - Main flow for each acceptance criterion
   - Valid inputs and expected outcomes
   - Clear Given-When-Then structure

2. **Alternative Path Scenarios** (2-3)
   - Valid but non-standard flows
   - Different user roles or permissions
   - Optional fields and configurations

3. **Negative Scenarios** (3-5)
   - Invalid inputs
   - Missing required fields
   - Unauthorized access
   - Business rule violations

4. **Edge Case Scenarios** (2-3)
   - Boundary values
   - Empty or null inputs
   - Concurrent operations
   - Timeout scenarios

5. **Scenario Outlines** (1-2)
   - Data-driven scenarios with Examples tables
   - Multiple input combinations
   - Parameterized test cases

## Gherkin Best Practices
- Use declarative language (what, not how)
- Keep scenarios independent and atomic
- One Given-When-Then per scenario (avoid multiple When)
- Use Background for shared preconditions only
- Use And/But sparingly for additional steps
- Give each scenario a name that states the rule it proves
- Avoid implementation details and UI locators in steps
- Use business language from the story, not technical jargon

## Output Format
Generate a complete feature file:
- Feature: [name] with a one-line description
- Background: [shared preconditions if applicable]
- Scenario: [each scenario with Given-When-Then]
- Scenario Outline: [with Examples table]
- Tags: [@smoke, @regression, @negative as appropriate]

Use realistic but safe test data. Never use real PII, PHI or payment numbers.

Please generate the BDD scenarios now.
```

## Example Input

```text
User Story:
As a registered customer
I want to reset my password
So that I can access my account if I forget my password

Acceptance Criteria:
1. User can request a password reset via email
2. Reset link expires after 24 hours
3. New password must match the complexity rules
4. User receives a confirmation email after reset
5. Old password no longer works after reset

Feature Context:
- Feature name: Password reset via email
- Application type: Web
- User roles: registered customer
- Business rules: reset links are single-use and expire after 24 hours; passwords need 8+ chars, one uppercase, one digit and one symbol
- Integration points: transactional email provider (SendGrid)
- BDD runner: Cucumber
```
