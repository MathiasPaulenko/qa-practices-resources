# Multi-Step Wizard / Checkout Flow — Runnable Companion

Dependency-free wizard state machine (`wizard-flow.mjs`) plus a `node:test` suite that maps the cases from [Multi-Step Wizard Test Cases: 18 Checkout Flow Scenarios](https://qapractices.com/test-cases/multi-step-wizard-checkout-flow-testing/).

The model encodes the rules under test: forward moves are gated by per-step validation, `back()` retains data, `serialize()`/`restore()` cover refresh recovery, `goto()` enforces prerequisites server-side, and `submit()` is idempotent.

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
| Per-step validation blocks progression | TC-02 |
| Back navigation retains entered data | TC-03 |
| Deep links redirect to the first missing step | TC-04, TC-15 |
| Serialize/restore for refresh recovery | TC-05 |
| Success creates one order; decline keeps state | TC-06, TC-07 |
| Idempotent submit / double-submit protection | TC-13 |
| Submit refused while a step is incomplete | TC-15 |

## Usage

```javascript
import { WizardFlow, checkoutSteps } from './wizard-flow.mjs';

const flow = new WizardFlow(checkoutSteps());
flow.next({ email: 'qa@qapractices.test', firstName: 'Ada' });
flow.next({ method: 'express' });
flow.next({ card: '4242424242424242' });
const result = flow.submit((data) => ({ ok: true, orderId: 'ord_1' }), {
  idempotencyKey: 'attempt-1',
});
```

Adapt `checkoutSteps()` to your own step definitions — each step is just `{ id, validate }`.
