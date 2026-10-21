/**
 * Dependency-free model of a multi-step wizard/checkout flow.
 *
 * The rules under test mirror the TC suite on qapractices.com:
 * forward moves are gated by per-step validation, back retains data,
 * serialize/restore covers refresh recovery, deep links are gated
 * server-side on prerequisites, and submit is idempotent.
 */

export class WizardFlow {
  /**
   * @param {Array<{id: string, validate: (data: object) => boolean}>} steps
   */
  constructor(steps) {
    if (!steps?.length) throw new Error('WizardFlow needs at least one step');
    this.steps = steps;
    this.index = 0;
    this.data = {};
    this.submitted = false;
    this.idempotencyKeys = new Set();
  }

  get current() {
    return this.steps[this.index];
  }

  isComplete(index) {
    return this.steps[index].validate(this.data[this.steps[index].id] ?? {});
  }

  /** Advance one step if the current step's merged data validates. */
  next(patch = {}) {
    const merged = { ...(this.data[this.current.id] ?? {}), ...patch };
    if (!this.current.validate(merged)) return { ok: false, reason: 'validation' };
    this.data[this.current.id] = merged;
    if (this.index < this.steps.length - 1) this.index += 1;
    return { ok: true, index: this.index };
  }

  /** Move back; previously entered data stays in `this.data`. */
  back() {
    if (this.index > 0) this.index -= 1;
    return this.current;
  }

  /**
   * Deep-link to a step. Prerequisites are enforced server-side:
   * the user lands on the first missing step, never a half-built page.
   */
  goto(stepId) {
    const target = this.steps.findIndex((s) => s.id === stepId);
    if (target === -1) return { ok: false, reason: 'unknown-step' };
    for (let i = 0; i < target; i += 1) {
      if (!this.isComplete(i)) {
        this.index = i;
        return { ok: false, reason: 'prerequisite', redirectedTo: this.steps[i].id };
      }
    }
    this.index = target;
    return { ok: true };
  }

  /** Persisted draft for refresh recovery (TC-05). */
  serialize() {
    return JSON.stringify({ index: this.index, data: this.data });
  }

  static restore(json, steps) {
    const parsed = JSON.parse(json);
    const flow = new WizardFlow(steps);
    flow.index = Math.min(Math.max(parsed.index, 0), steps.length - 1);
    flow.data = parsed.data ?? {};
    return flow;
  }

  /**
   * Final submit. Idempotent: a repeated call with the same key — or any
   * call after a successful submit — cannot create a second order.
   */
  submit(payFn, { idempotencyKey } = {}) {
    if (this.submitted) return { ok: false, reason: 'already-submitted' };
    if (idempotencyKey && this.idempotencyKeys.has(idempotencyKey)) {
      return { ok: false, reason: 'duplicate-key' };
    }
    if (!this.steps.every((_, i) => this.isComplete(i))) {
      return { ok: false, reason: 'incomplete' };
    }
    if (idempotencyKey) this.idempotencyKeys.add(idempotencyKey);
    const result = payFn(this.data);
    if (result.ok) this.submitted = true;
    return result;
  }
}

/** Sample step definition used by the tests and the README example. */
export function checkoutSteps() {
  return [
    {
      id: 'details',
      validate: (d) => typeof d.email === 'string' && d.email.includes('@')
        && typeof d.firstName === 'string' && d.firstName.length > 0,
    },
    {
      id: 'shipping',
      validate: (d) => ['standard', 'express'].includes(d.method),
    },
    {
      id: 'payment',
      validate: (d) => typeof d.card === 'string' && d.card.length >= 15,
    },
  ];
}
