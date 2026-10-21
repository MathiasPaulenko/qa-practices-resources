/**
 * Dependency-free model of a stepper wizard form.
 *
 * The rules under test mirror the stepper TC suite on qapractices.com:
 * Next is the only gated transition, Back/edit/refresh restore state,
 * the step list is derived (conditional steps appear and disappear),
 * skipped-step data never reaches the submit payload, and submit is
 * idempotent.
 */

export class StepperWizard {
  /**
   * @param {Array<{id: string, validate?: (data: object) => boolean, when?: (data: object) => boolean}>} steps
   * @param {{draftTtlMs?: number, now?: () => number}} [options]
   */
  constructor(steps, { draftTtlMs = 24 * 60 * 60 * 1000, now = Date.now } = {}) {
    if (!steps?.length) throw new Error('StepperWizard needs at least one step');
    this.steps = steps;
    this.index = 0;
    this.data = {};
    this.inactive = {};
    this.submitted = false;
    this.cancelled = false;
    this.draftTtlMs = draftTtlMs;
    this.now = now;
    this.savedAt = this.now();
    this.submissions = new Map();
  }

  /** Flat merged view of active data — what `when` conditions and submit see. */
  mergedData() {
    return Object.assign({}, ...Object.values(this.data));
  }

  /** The step list is derived: conditional steps exist only while `when` holds. */
  activeSteps() {
    const merged = this.mergedData();
    return this.steps.filter((s) => !s.when || s.when(merged));
  }

  get current() {
    const active = this.activeSteps();
    if (this.index > active.length - 1) this.index = Math.max(0, active.length - 1);
    return active[this.index];
  }

  isComplete(stepId) {
    const step = this.steps.find((s) => s.id === stepId);
    if (!step) return false;
    if (!step.validate) return true;
    return step.validate(this.data[step.id] ?? {});
  }

  /** Reconcile orphan data: steps that went inactive shed their data; returning steps recover it. */
  #reconcileInactive() {
    const activeIds = new Set(this.activeSteps().map((s) => s.id));
    for (const step of this.steps) {
      if (!activeIds.has(step.id) && this.data[step.id]) {
        this.inactive[step.id] = this.data[step.id];
        delete this.data[step.id];
      } else if (activeIds.has(step.id) && this.inactive[step.id]) {
        this.data[step.id] = this.inactive[step.id];
        delete this.inactive[step.id];
      }
    }
  }

  /** Advance one step if the current step's merged data validates. The only gated edge. */
  next(patch = {}) {
    const step = this.current;
    const merged = { ...(this.data[step.id] ?? {}), ...patch };
    if (step.validate && !step.validate(merged)) return { ok: false, reason: 'validation' };
    this.data[step.id] = merged;
    this.#reconcileInactive();
    if (this.index < this.activeSteps().length - 1) this.index += 1;
    this.savedAt = this.now();
    return { ok: true, index: this.index };
  }

  /** Move back one step. Never gated; entered data stays. */
  back() {
    if (this.index > 0) this.index -= 1;
    return { ok: true, index: this.index };
  }

  /** Review-step edit: jump straight to the owning step if it is reachable. */
  editTo(stepId) {
    const active = this.activeSteps();
    const target = active.findIndex((s) => s.id === stepId);
    if (target === -1) return { ok: false, reason: 'inactive-step' };
    this.index = target;
    return { ok: true, index: target };
  }

  /**
   * Deep-link gate: a direct jump to a later step is redirected to the
   * first incomplete active step. Only allowed when prerequisites hold.
   */
  goto(stepId) {
    const active = this.activeSteps();
    const target = active.findIndex((s) => s.id === stepId);
    if (target === -1) return { ok: false, reason: 'inactive-step' };
    const firstIncomplete = active.findIndex((s) => !this.isComplete(s.id));
    if (firstIncomplete !== -1 && firstIncomplete < target) {
      this.index = firstIncomplete;
      return { ok: false, reason: 'prerequisites', redirectedTo: active[firstIncomplete].id };
    }
    this.index = target;
    return { ok: true, index: target };
  }

  /** Progress as reached-step ratio over the derived list: 4 steps → 25/50/75/100. */
  progress() {
    const active = this.activeSteps();
    return Math.round(((this.index + 1) / active.length) * 100);
  }

  /** Draft snapshot for refresh/autosave recovery. */
  serialize() {
    return JSON.stringify({ data: this.data, inactive: this.inactive, index: this.index, savedAt: this.savedAt });
  }

  /** Restore a draft; an expired draft is rejected, not silently resumed. */
  restore(json) {
    const draft = JSON.parse(json);
    if (this.now() - draft.savedAt > this.draftTtlMs) {
      this.data = {};
      this.inactive = {};
      this.index = 0;
      return { ok: false, reason: 'expired' };
    }
    this.data = draft.data;
    this.inactive = draft.inactive ?? {};
    this.index = draft.index;
    this.savedAt = draft.savedAt;
    this.#reconcileInactive();
    return { ok: true, index: this.index };
  }

  /** Cancel must be confirmed; confirming clears the draft and exits. */
  cancel(confirmed) {
    if (!confirmed) return { ok: false, reason: 'declined' };
    this.data = {};
    this.inactive = {};
    this.index = 0;
    this.cancelled = true;
    return { ok: true };
  }

  /**
   * Submit aggregates active steps only — skipped data never ships.
   * Idempotent: a repeated idempotency key replays the stored result.
   */
  submit(handler, { idempotencyKey } = {}) {
    if (idempotencyKey && this.submissions.has(idempotencyKey)) {
      return { ...this.submissions.get(idempotencyKey), duplicate: true };
    }
    const active = this.activeSteps();
    const incomplete = active.find((s) => !this.isComplete(s.id));
    if (incomplete) return { ok: false, reason: 'incomplete', step: incomplete.id };
    const payload = { ...this.data };
    const result = handler(payload);
    if (!result?.ok) return { ok: false, reason: 'server' };
    this.submitted = true;
    const response = { ok: true, payload, result };
    if (idempotencyKey) this.submissions.set(idempotencyKey, response);
    return response;
  }
}

/** The onboarding fixture used across the TC suite: Account → Profile → Company? → Preferences → Review. */
export function onboardingSteps() {
  return [
    {
      id: 'account',
      validate: (d) => typeof d.email === 'string' && d.email.includes('@') && typeof d.password === 'string' && d.password.length >= 8,
    },
    {
      id: 'profile',
      validate: (d) => typeof d.name === 'string' && d.name.length > 0 && ['personal', 'business'].includes(d.accountType),
    },
    {
      id: 'company',
      when: (d) => d.accountType === 'business',
      validate: (d) => typeof d.companyName === 'string' && d.companyName.length > 0,
    },
    {
      id: 'preferences',
      validate: (d) => ['light', 'dark'].includes(d.theme),
    },
    { id: 'review' },
  ];
}
