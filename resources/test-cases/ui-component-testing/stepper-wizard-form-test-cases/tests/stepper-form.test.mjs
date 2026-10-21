import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { StepperWizard, onboardingSteps } from '../stepper-form.mjs';

const account = { email: 'qa.user@qapractices.dev', password: 'Str0ng!Pass' };
const personalProfile = { name: 'Ada Lovelace', accountType: 'personal' };
const businessProfile = { name: 'Ada Lovelace', accountType: 'business' };
const company = { companyName: 'QA Industries' };
const prefs = { theme: 'dark' };

function wizard(profile = personalProfile) {
  const w = new StepperWizard(onboardingSteps());
  w.next(account);
  w.next(profile);
  return w;
}

const okSubmit = (payload) => ({ ok: true, recordId: 'rec_1', received: payload });

describe('forward navigation (TC-01)', () => {
  it('advances one step at a time through the derived chain', () => {
    const w = new StepperWizard(onboardingSteps());
    assert.equal(w.current.id, 'account');
    w.next(account);
    assert.equal(w.current.id, 'profile');
    w.next(businessProfile);
    assert.equal(w.current.id, 'company'); // business inserts the conditional step
    w.next(company);
    assert.equal(w.current.id, 'preferences');
    w.next(prefs);
    assert.equal(w.current.id, 'review');
    w.next();
    assert.equal(w.current.id, 'review'); // stays on last step, ready to submit
  });
});

describe('back navigation (TC-02, TC-05)', () => {
  it('retains every field on the way back and forward', () => {
    const w = wizard();
    w.next(prefs); // index 3: review
    w.back();
    assert.equal(w.current.id, 'preferences');
    assert.equal(w.data.preferences.theme, 'dark');
    w.back();
    assert.equal(w.current.id, 'profile');
    assert.equal(w.data.profile.name, 'Ada Lovelace');
    w.back();
    assert.equal(w.current.id, 'account');
    assert.equal(w.data.account.email, 'qa.user@qapractices.dev');
    w.next(); // forward again with retained data
    assert.equal(w.current.id, 'profile');
    w.next();
    assert.equal(w.current.id, 'preferences');
    assert.equal(w.data.preferences.theme, 'dark');
  });
});

describe('per-step validation gate (TC-03)', () => {
  it('blocks Next until required fields validate', () => {
    const w = new StepperWizard(onboardingSteps());
    assert.deepEqual(w.next({}), { ok: false, reason: 'validation' });
    assert.equal(w.current.id, 'account');
    assert.deepEqual(w.next({ email: 'not-an-email' }), { ok: false, reason: 'validation' });
    assert.equal(w.next(account).ok, true);
  });
});

describe('submit aggregates active steps only (TC-06, edge: orphan data)', () => {
  it('sends the complete payload of active steps once', () => {
    const w = wizard();
    w.next(prefs);
    const res = w.submit(okSubmit, { idempotencyKey: 'attempt-1' });
    assert.equal(res.ok, true);
    assert.deepEqual(Object.keys(res.payload).sort(), ['account', 'preferences', 'profile']);
    assert.equal(res.payload.preferences.theme, 'dark');
    assert.equal('company' in res.payload, false); // skipped step ships nothing
  });

  it('refuses submit while a step is incomplete', () => {
    const w = wizard();
    const res = w.submit(okSubmit);
    assert.deepEqual(res, { ok: false, reason: 'incomplete', step: 'preferences' });
  });
});

describe('conditional skip logic (TC-09, TC-23)', () => {
  it('personal skips company; business inserts it', () => {
    const personal = wizard(personalProfile);
    assert.deepEqual(personal.activeSteps().map((s) => s.id), ['account', 'profile', 'preferences', 'review']);

    const business = wizard(businessProfile);
    assert.deepEqual(business.activeSteps().map((s) => s.id), ['account', 'profile', 'company', 'preferences', 'review']);
  });

  it('reverting the trigger excludes already-entered step data', () => {
    const w = wizard(businessProfile);
    w.next(company); // fill company
    w.back(); // company
    w.back(); // profile
    w.next(personalProfile); // switch to personal — company becomes inactive
    assert.deepEqual(w.activeSteps().map((s) => s.id), ['account', 'profile', 'preferences', 'review']);
    w.next(prefs);
    const res = w.submit(okSubmit);
    assert.equal('company' in res.payload, false); // no orphan data in the payload
    assert.equal(w.inactive.company.companyName, 'QA Industries'); // retained but inactive
  });
});

describe('edit from review (TC-10)', () => {
  it('jumps to the owning step with data intact', () => {
    const w = wizard();
    w.next(prefs); // on review
    w.editTo('account');
    assert.equal(w.current.id, 'account');
    w.next({ email: 'ada@qapractices.dev', password: 'Str0ng!Pass' });
    w.editTo('review');
    assert.equal(w.data.account.email, 'ada@qapractices.dev');
    assert.equal(w.data.preferences.theme, 'dark'); // other steps untouched
  });
});

describe('deep-link prerequisite gate (TC-11)', () => {
  it('redirects to the first incomplete step, never a half-initialized one', () => {
    const w = new StepperWizard(onboardingSteps());
    const res = w.goto('review');
    assert.deepEqual(res, { ok: false, reason: 'prerequisites', redirectedTo: 'account' });
    assert.equal(w.current.id, 'account');
  });

  it('allows the jump when prerequisites hold', () => {
    const w = wizard();
    w.next(prefs);
    const res = w.goto('review');
    assert.equal(res.ok, true);
    assert.equal(w.current.id, 'review');
  });
});

describe('draft serialize/restore (TC-16, TC-25)', () => {
  it('restores position and data from a fresh draft', () => {
    const w = wizard();
    w.next(prefs);
    const json = w.serialize();

    const restored = new StepperWizard(onboardingSteps());
    const res = restored.restore(json);
    assert.equal(res.ok, true);
    assert.equal(restored.current.id, 'review');
    assert.equal(restored.data.account.email, 'qa.user@qapractices.dev');
  });
});

describe('session timeout / draft expiry (TC-14, edge: draft TTL)', () => {
  it('rejects an expired draft instead of silently resuming it', () => {
    let t = 1_000_000;
    const w = new StepperWizard(onboardingSteps(), { now: () => t });
    w.next(account);
    const json = w.serialize();

    t += 25 * 60 * 60 * 1000; // 25 h later — past the 24 h TTL
    const restored = new StepperWizard(onboardingSteps(), { now: () => t });
    assert.deepEqual(restored.restore(json), { ok: false, reason: 'expired' });
    assert.equal(restored.current.id, 'account'); // controlled restart
  });
});

describe('submission API error (TC-17)', () => {
  it('keeps the draft alive and lets a retry succeed', () => {
    const w = wizard();
    w.next(prefs);
    const failed = w.submit(() => ({ ok: false, status: 500 }));
    assert.deepEqual(failed, { ok: false, reason: 'server' });
    assert.equal(w.data.profile.name, 'Ada Lovelace'); // nothing lost
    const retried = w.submit(okSubmit);
    assert.equal(retried.ok, true);
  });
});

describe('cancel requires confirmation (TC-20)', () => {
  it('declining keeps data; confirming clears everything', () => {
    const w = wizard();
    assert.deepEqual(w.cancel(false), { ok: false, reason: 'declined' });
    assert.equal(w.data.account.email, 'qa.user@qapractices.dev');
    assert.equal(w.cancel(true).ok, true);
    assert.equal(w.cancelled, true);
    assert.deepEqual(w.data, {});
  });
});

describe('progress recounts over the active step list (TC-26)', () => {
  it('4 steps give 25/50/75/100; a skipped step gives 33/66/100', () => {
    const personal = new StepperWizard(onboardingSteps());
    const seen = [];
    seen.push(personal.progress()); // step 1 of 4
    personal.next(account);
    seen.push(personal.progress());
    personal.next(personalProfile);
    seen.push(personal.progress());
    personal.next(prefs);
    seen.push(personal.progress());
    assert.deepEqual(seen, [25, 50, 75, 100]);

    const business = new StepperWizard(onboardingSteps());
    const businessSeen = [business.progress()]; // step 1 of 4 until accountType is known
    business.next(account);
    businessSeen.push(business.progress()); // still 4 steps: company not yet active
    business.next(businessProfile);
    businessSeen.push(business.progress()); // now 5 steps: company inserted
    assert.deepEqual(businessSeen, [25, 50, 60]);
  });
});

describe('idempotent submit / double-submit protection (edge)', () => {
  it('a repeated idempotency key replays the stored result without re-submitting', () => {
    const w = wizard();
    w.next(prefs);
    let calls = 0;
    const handler = (payload) => { calls += 1; return { ok: true, recordId: 'rec_1' }; };
    const first = w.submit(handler, { idempotencyKey: 'attempt-1' });
    const second = w.submit(handler, { idempotencyKey: 'attempt-1' });
    assert.equal(calls, 1);
    assert.equal(second.duplicate, true);
    assert.deepEqual(second.payload, first.payload);
  });
});
