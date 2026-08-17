
# AI Prompt: Generate Behave BDD Feature Files

## Overview

Translating a user story or a product requirement into a clean Behave `.feature` file takes more time than it looks. The story describes value from the user's perspective, while the feature file has to pin down the exact steps, tags and examples that Behave will execute. Done well, the `.feature` becomes a contract the whole team can read. Done poorly, it drifts into implementation language and stops being useful for product and QA.

This prompt turns a plain user story or acceptance criteria into a structured Behave feature file. You paste the story, define the domain context and the prompt returns Gherkin syntax with scenarios, tags, examples and a note on the step vocabulary. It is useful when you are starting a new Behave suite, adding coverage after a sprint or cleaning up feature files that have become too technical. For a deeper look at writing good Gherkin, see the [Gherkin Best Practices for Behave](/documentation/gherkin-best-practices-behave) guide; for the project layout that goes with these files, see the [Behave BDD Project Setup Guide](/documentation/behave-bdd-project-setup-guide).

## When to Use

- **Starting a new Behave project.** You have product requirements and need a first draft of `.feature` files that follow Behave conventions.
- **Adding scenarios after a sprint.** A new user story is ready and you want to generate the Gherkin skeleton before writing step definitions.
- **Refactoring existing feature files.** Old files are too verbose or use click-by-click UI language. The prompt rewrites them in domain terms.
- **Onboarding product owners and testers.** It gives them a concrete example of how a user story maps to executable Gherkin.
- **Preparing for a refinement session.** You walk in with a generated feature file and discuss only the examples and edge cases.

## The Prompt

```text
You are a QA engineer and BDD facilitator writing Behave (Python) feature files for a project that uses [DOMAIN, e.g. e-commerce checkout, inventory management, user authentication].

Input:
- Feature name: [FEATURE_NAME]
- User story: As a [ROLE], I want [GOAL] so that [BENEFIT].
- Acceptance criteria:
  1. [CRITERION_1]
  2. [CRITERION_2]
  3. [CRITERION_3]
- Priority scenarios: [SCENARIO_1, SCENARIO_2]
- Technical context: [TECHNICAL_CONTEXT, e.g. REST API with JSON responses, Python service layer, browser UI with Selenium]
- Step vocabulary style: [business-focused / API-focused / UI-focused]

Generate a Behave-ready .feature file that follows these rules:
1. Use Gherkin keywords: Feature, Background (if useful), Scenario, Scenario Outline, Examples, Given, When, Then, And, But.
2. Add Behave tags on scenarios and/or feature level: @smoke, @regression, @critical, @api, @ui, @priority(N) where appropriate.
3. Keep step text declarative and domain-oriented. Avoid implementation details like CSS selectors, internal method names or database table names.
4. Include positive, negative and boundary scenarios. Use Scenario Outline with Examples for parameterized cases.
5. After the feature file, list the expected Python step decorators (only signatures, no implementation) that Behave needs to match the steps.
6. Suggest a filename in kebab-case, e.g. `checkout-payment.feature`.
7. Add a one-sentence note explaining why the chosen step vocabulary style fits the technical context.

Use realistic but safe test data. Never use real PII, payment numbers or customer names. Use placeholder values like `SKU-1234`, `user-qa-01@example.com` or `4111111111111111` only if the context requires a card number and you explicitly mark it as test data.
```

## Example Input

```markdown
**Feature name:** Guest checkout with credit card

**User story:** As a guest shopper, I want to pay with a credit card so that I can complete my purchase without creating an account.

**Acceptance criteria:**
1. The checkout page accepts a valid Visa, Mastercard or Amex card.
2. The total must include taxes and shipping before payment is authorized.
3. A declined card shows a clear error message and allows retry.
4. A successful payment creates an order and shows a confirmation number.

**Priority scenarios:**
- Successful payment with a valid card.
- Declined card with retry.
- Missing CVV validation.

**Technical context:** REST API with JSON responses, Python service layer.

**Step vocabulary style:** business-focused.
```

## Example Output

```gherkin
@checkout @payment @guest
Feature: Guest checkout with credit card
  As a guest shopper
  I want to pay with a credit card
  So that I can complete my purchase without creating an account

  Background:
    Given the guest has added a product to the cart
    And the guest has entered a valid shipping address

  @smoke @critical @priority(1)
  Scenario: Successful payment with a valid card
    Given the checkout total is "$54.99"
    When the guest pays with a valid "Visa" card
    Then the payment is authorized
    And an order is created
    And the guest sees the confirmation number

  @regression @priority(2)
  Scenario: Declined card with retry
    Given the checkout total is "$54.99"
    When the guest pays with a declined "Mastercard" card
    Then the payment is declined with a clear error
    And the guest can retry with another card

  @regression
  Scenario Outline: Missing or invalid card details
    Given the checkout total is "$54.99"
    When the guest enters a card number of "<card_number>" with CVV "<cvv>"
    Then the payment request is rejected with "<error_message>"

    Examples:
      | card_number       | cvv | error_message          |
      |                   |     | Card number is required |
      | 4111111111111111  |     | CVV is required        |
      | 1234567890123456  | 999 | Card number is invalid |
```

Expected step decorators (no implementation):

```python
@given('the guest has added a product to the cart')
@given('the guest has entered a valid shipping address')
@given('the checkout total is "{total}"')
@when('the guest pays with a valid "{card_type}" card')
@when('the guest pays with a declined "{card_type}" card')
@when('the guest enters a card number of "{card_number}" with CVV "{cvv}"')
@then('the payment is authorized')
@then('an order is created')
@then('the guest sees the confirmation number')
@then('the payment is declined with a clear error')
@then('the guest can retry with another card')
@then('the payment request is rejected with "{error_message}"')
```

Suggested filename: `guest-checkout-payment.feature`

Step vocabulary note: The steps use business-focused language (`the guest pays with a valid card`) because the same `.feature` can run against the REST API today and a future UI layer without rewriting the Gherkin.

## Customization Variables

| Variable | Description | Example |
|---|---|---|
| `DOMAIN` | Business domain of the feature | `e-commerce checkout`, `inventory management`, `user authentication` |
| `FEATURE_NAME` | Short name of the feature in plain language | `Guest checkout with credit card` |
| `ROLE` / `GOAL` / `BENEFIT` | The three parts of the user story | `guest shopper`, `pay with a credit card`, `complete my purchase without creating an account` |
| `Acceptance criteria` | Numbered list of acceptance rules | `The checkout page accepts a valid Visa, Mastercard or Amex card` |
| `Priority scenarios` | Scenarios the team wants first | `Successful payment with a valid card`, `Declined card with retry` |
| `Technical context` | How the system under test is built | `REST API with JSON responses`, `Python service layer`, `browser UI with Selenium` |
| `Step vocabulary style` | Domain level of the steps | `business-focused`, `API-focused`, `UI-focused` |

## Best Practices

1. Fill in every placeholder before pasting the prompt. Incomplete context produces generic steps.
2. Keep the step vocabulary style consistent across all feature files in the same project. Mixing UI and API language in the same file confuses Behave step matching.
3. Add `@smoke` or `@critical` only to scenarios that should fail the pipeline when they break. Every tag should mean something in CI.
4. Use `Scenario Outline` only when the behavior is identical and only the data changes. If the flow differs, write separate scenarios.
5. Review the generated Gherkin with the product owner. The LLM can use implementation language that sounds right to a developer but wrong to a stakeholder.
6. Delete the expected step decorators list before committing the `.feature` file. It is only a helper for the developer who writes the step definitions.
7. Pin the Behave version and Gherkin style in the project README so the prompt stays aligned with the conventions the team uses.

## Common Mistakes

1. **Acceptance criteria that list UI actions, not business rules.** The prompt then generates `When the user clicks the pay button` instead of `When the guest pays with a valid card`.
2. **Mixing Given, When and Then in the same scenario step.** A step should be one of them, otherwise the generated file is hard to read and maintain.
3. **Forgetting boundary and negative cases.** The prompt follows the acceptance criteria; if you only list happy path, it only returns happy path.
4. **Using real customer or payment data as examples.** Even inside the prompt, real data can leak into the output. Always use test-only values.
5. **Over-tagging every scenario with `@smoke`.** Tags lose meaning when every line has one, and CI run times increase.
6. **Copying the generated file without reviewing step vocabulary.** The LLM may use synonyms across features, which creates duplicate or ambiguous step definitions.

## Prompt Variations

### Variation 1: Generate from a Jira ticket

Use this when the source of truth is a Jira or Azure DevOps ticket instead of a user story paragraph.

```text
You are a QA engineer writing Behave feature files from a Jira ticket.

Input:
- Ticket ID: [TICKET_ID]
- Ticket title: [TICKET_TITLE]
- Description: [DESCRIPTION]
- Acceptance criteria: [ACCEPTANCE_CRITERIA]
- Linked API spec: [OPENAPI_SPEC_PATH or NONE]
- Priority: [HIGH / MEDIUM / LOW]

Generate a Behave .feature file with:
1. A Feature line that matches the ticket title.
2. Scenarios that cover the acceptance criteria.
3. Tags that include @regression and a ticket reference tag like @JIRA-123.
4. At least one negative scenario and one boundary scenario.
5. A short note about which steps are likely to need HTTP step definitions if the ticket touches an API.
```

### Variation 2: Refactor an existing feature file

Use this when a `.feature` file has become too long, too technical or unreadable.

```text
You are a QA engineer refactoring an existing Behave .feature file.

Input:
- Existing feature file content:
[EXISTING_FEATURE_FILE_CONTENT]

Refactor rules:
1. Split the file into multiple feature files if it covers more than one business capability.
2. Replace implementation-focused steps with business-focused steps.
3. Add Background for shared preconditions.
4. Use Scenario Outline with Examples for repeated data.
5. Remove tags that do not map to a CI job or a test suite.
6. Output the refactored feature file(s) and a short list of deleted or renamed scenarios.
```

## Related Resources

- [Gherkin Best Practices for Behave](/documentation/gherkin-best-practices-behave)
- [Behave BDD Project Setup Guide](/documentation/behave-bdd-project-setup-guide)
- [Behave Step Definitions Best Practices](/documentation/behave-step-definitions-best-practices)
- [Gherkin Feature Quality Checklist](/checklists/gherkin-feature-quality-checklist)
- [Behave BDD Smoke Test Cases](/test-cases/behave-bdd-smoke-test-cases)

## Frequently Asked Questions

### Can this prompt generate step implementations too?

No, it only generates the `.feature` file and the expected step decorators. Step implementations depend on your project layer, so keep them separate and write them by hand or with a code-generation prompt.

### Should I run the output through `behave --dry-run`?

Yes. The LLM can produce Gherkin that looks right but has missing step matches or duplicate step text. `behave --dry-run` catches undefined or ambiguous steps without running the suite.

### What if the generated file has too many scenarios?

Trim it before committing. Keep the scenarios that the team can implement and maintain in the current sprint. The rest can move to the backlog or to a separate file.

### How do I keep the style consistent across multiple generated files?

Add a short "Domain glossary" section at the start of the prompt with allowed verbs and nouns. For example, use `customer` instead of `user`, `places an order` instead of `clicks checkout`.
