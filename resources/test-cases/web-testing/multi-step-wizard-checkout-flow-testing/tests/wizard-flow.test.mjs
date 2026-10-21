import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { WizardFlow, checkoutSteps } from '../wizard-flow.mjs';

const details = { email: 'qa@qapractices.test', firstName: 'Ada' };
const shipping = { method: 'express' };
const payment = { card: '4242424242424242' };

function completedFlow() {
  const flow = new WizardFlow(checkoutSteps());
  flow.next(details);
  flow.next(shipping);
  flow.next(payment);
  return flow;
}

const okPay = () => ({ ok: true, orderId: 'ord_1' });

describe('wizard sequential navigation (TC-01)', () => {
  it('advances one step at a time through the chain', () => {
    const flow = new WizardFlow(checkoutSteps());
    assert.equal(flow.current.id, 'details');
    flow.next(details);
    assert.equal(flow.current.id, 'shipping');
    flow.next(shipping);
    assert.equal(flow.current.id, 'payment');
    flow.next(payment);
    assert.equal(flow.index, 2); // stays on last step, ready to submit
  });
});

describe('per-step validation gate (TC-02)', () => {
  it('blocks forward movement on invalid data', () => {
    const flow = new WizardFlow(checkoutSteps());
    const res = flow.next({ email: 'not-an-email', firstName: 'Ada' });
    assert.equal(res.ok, false);
    assert.equal(res.reason, 'validation');
    assert.equal(flow.index, 0);
  });

  it('does not store partial invalid data', () => {
    const flow = new WizardFlow(checkoutSteps());
    flow.next({ email: 'not-an-email', firstName: 'Ada' });
    assert.deepEqual(flow.data, {});
  });
});

describe('back navigation retains data (TC-03)', () => {
  it('keeps entered values after going back and forward', () => {
    const flow = new WizardFlow(checkoutSteps());
    flow.next(details);
    flow.next(shipping);
    flow.back();
    flow.back();
    assert.equal(flow.current.id, 'details');
    assert.deepEqual(flow.data.details, details);
    assert.deepEqual(flow.data.shipping, shipping);
  });
});

describe('deep-link prerequisite gate (TC-04, TC-15)', () => {
  it('redirects a mid-step deep link to the first missing step', () => {
    const flow = new WizardFlow(checkoutSteps());
    flow.next(details);
    const res = flow.goto('payment');
    assert.equal(res.ok, false);
    assert.equal(res.reason, 'prerequisite');
    assert.equal(res.redirectedTo, 'shipping');
  });

  it('opens the step when all prerequisites are complete', () => {
    const flow = new WizardFlow(checkoutSteps());
    flow.next(details);
    flow.next(shipping);
    const res = flow.goto('payment');
    assert.equal(res.ok, true);
    assert.equal(flow.current.id, 'payment');
  });
});

describe('refresh recovery (TC-05)', () => {
  it('restores position and data from a serialized draft', () => {
    const flow = new WizardFlow(checkoutSteps());
    flow.next(details);
    flow.next(shipping);
    const restored = WizardFlow.restore(flow.serialize(), checkoutSteps());
    assert.equal(restored.index, flow.index);
    assert.deepEqual(restored.data, flow.data);
  });
});

describe('payment outcomes (TC-06, TC-07)', () => {
  it('creates exactly one order on success', () => {
    const flow = completedFlow();
    const res = flow.submit(okPay, { idempotencyKey: 'k-1' });
    assert.deepEqual(res, { ok: true, orderId: 'ord_1' });
    assert.equal(flow.submitted, true);
  });

  it('a declined payment keeps cart and step data intact', () => {
    const flow = completedFlow();
    const res = flow.submit(() => ({ ok: false, reason: 'declined' }));
    assert.equal(res.ok, false);
    assert.equal(flow.submitted, false);
    assert.deepEqual(flow.data.details, details);
    assert.deepEqual(flow.data.shipping, shipping);
  });
});

describe('double-submit protection (TC-13)', () => {
  it('rejects a second submit after success', () => {
    const flow = completedFlow();
    flow.submit(okPay, { idempotencyKey: 'k-1' });
    const res = flow.submit(okPay, { idempotencyKey: 'k-2' });
    assert.equal(res.ok, false);
    assert.equal(res.reason, 'already-submitted');
  });

  it('rejects a replayed idempotency key', () => {
    const flow = completedFlow();
    const pay = () => ({ ok: false, reason: 'timeout' }); // outcome unknown
    flow.submit(pay, { idempotencyKey: 'k-1' });
    const res = flow.submit(okPay, { idempotencyKey: 'k-1' });
    assert.equal(res.ok, false);
    assert.equal(res.reason, 'duplicate-key');
  });
});

describe('step skipping (TC-15)', () => {
  it('refuses submit while any step is incomplete', () => {
    const flow = new WizardFlow(checkoutSteps());
    flow.next(details);
    flow.next(shipping); // payment never filled
    const res = flow.submit(okPay);
    assert.equal(res.ok, false);
    assert.equal(res.reason, 'incomplete');
  });
});
