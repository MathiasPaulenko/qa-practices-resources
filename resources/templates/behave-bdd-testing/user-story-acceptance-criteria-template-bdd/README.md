# BDD Acceptance Criteria Template for User Stories

A filled `.feature` file showing Gherkin acceptance criteria for a promo-code checkout story: a `Background` block, happy-path, negative and edge scenarios, plus a `Scenario Outline` for input validation.

## How to use

1. Copy `promo-code-checkout.feature` into your project's `features/` directory.
2. Replace the promo-code domain with your own story and adjust the steps to your application's wording.
3. Write step definitions for the steps — they map directly to Cucumber, SpecFlow or Behave.
4. Run `behave --dry-run` (or `cucumber --dry-run`) to check that every step resolves.

## Full guide

See the [QAPractices template](https://qapractices.com/templates/user-story-acceptance-criteria-template-bdd) for the skeleton, the coverage checklist and best practices.
