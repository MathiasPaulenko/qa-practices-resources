const { isFeatureEnabled, bucket, flags } = require('../featureFlags');

const FLAG = 'new-dashboard';

describe('percentage rollout', () => {
  afterEach(() => {
    flags[FLAG].enabled = true;
    flags[FLAG].percentage = 50;
  });

  it('assigns the same user to the same bucket on every call', () => {
    const user = { userId: 'user-123' };
    const first = isFeatureEnabled(FLAG, user);
    for (let i = 0; i < 10; i++) {
      expect(isFeatureEnabled(FLAG, user)).toBe(first);
    }
  });

  it('is deterministic across evaluator instances', () => {
    expect(bucket(FLAG, 'user-123')).toBe(bucket(FLAG, 'user-123'));
  });

  it('never enables the feature without a user context', () => {
    expect(isFeatureEnabled(FLAG, {})).toBe(false);
  });

  it('respects the master switch even inside the percentage', () => {
    flags[FLAG].enabled = false;
    expect(isFeatureEnabled(FLAG, { userId: 'user-123' })).toBe(false);
  });

  it('splits a plausible ~50/50 share at percentage 50', () => {
    let on = 0;
    for (let i = 0; i < 1000; i++) {
      if (isFeatureEnabled(FLAG, { userId: `user-${i}` })) on++;
    }
    expect(on).toBeGreaterThan(400);
    expect(on).toBeLessThan(600);
  });

  it('is monotonic: everyone on at 25% stays on at 50%', () => {
    flags[FLAG].percentage = 25;
    const onAt25 = [];
    for (let i = 0; i < 500; i++) {
      const userId = `user-${i}`;
      if (isFeatureEnabled(FLAG, { userId })) onAt25.push(userId);
    }
    flags[FLAG].percentage = 50;
    for (const userId of onAt25) {
      expect(isFeatureEnabled(FLAG, { userId })).toBe(true);
    }
  });

  it('covers nobody at 0% and everybody at 100%', () => {
    flags[FLAG].percentage = 0;
    expect(isFeatureEnabled(FLAG, { userId: 'user-1' })).toBe(false);
    flags[FLAG].percentage = 100;
    expect(isFeatureEnabled(FLAG, { userId: 'user-1' })).toBe(true);
  });
});
