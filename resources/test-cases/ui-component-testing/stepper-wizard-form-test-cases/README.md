# Stepper Wizard Form — Runnable Companion

Dependency-free stepper state machine (`stepper-form.mjs`) plus a `node:test` suite that maps the cases from [Stepper Wizard Form Test Cases: 30 Scenarios](https://qapractices.com/test-cases/stepper-wizard-form-test-cases/).

The model encodes the rules under test: `next()` is the only gated transition, `back()`/`editTo()` restore state, `activeSteps()` is derived so conditional steps appear and disappear, `goto()` enforces prerequisites server-side, `serialize()`/`restore()` cover draft recovery with a TTL, and `submit()` aggregates active steps only — skipped-step data never ships.

## Requirements

- Node.js 20+

## Run the tests

```bash
node --test tests/*.test.mjs
```

## What's covered

| Behavior | Maps to |
|---|---|
| Sequential navigation, one step at a time | TC-01 |
| Back navigation retains entered data | TC-02, TC-05 |
| Per-step validation blocks progression | TC-03 |
| Submit aggregates active steps, once | TC-06 |
| Conditional skip logic, both directions | TC-09, TC-23 |
| Orphan data excluded from the payload | Edge cases, TC-23 |
| Edit-from-review jumps to the owning step | TC-10 |
| Deep links redirect to the first incomplete step | TC-11 |
| Draft restore / expired-draft rejection | TC-14, TC-16, TC-25 |
| Failed submit keeps data, retry succeeds | TC-17 |
| Cancel requires confirmation | TC-20 |
| Progress recounts over the derived list | TC-26 |
| Idempotent submit / double-submit protection | Edge cases, TC-06 |

## Usage

```javascript
import { StepperWizard, onboardingSteps } from './stepper-form.mjs';

const w = new StepperWizard(onboardingSteps());
w.next({ email: 'qa.user@qapractices.dev', password: 'Str0ng!Pass' });
w.next({ name: 'Ada Lovelace', accountType: 'business' }); // inserts the Company step
w.next({ companyName: 'QA Industries' });
w.next({ theme: 'dark' });
const res = w.submit((payload) => ({ ok: true, recordId: 'rec_1' }), {
  idempotencyKey: 'attempt-1',
});
```

Adapt `onboardingSteps()` to your own step definitions — each step is `{ id, validate?, when? }`, where `when` gates the step's existence on merged data from earlier steps.
