const { isFeatureEnabled } = require('../featureFlags');

// Boundary tests for the targeting rules table in section 3 of the guide.
describe('beta-search targeting rules', () => {
  it('shows the feature to a premium US user', () => {
    expect(
      isFeatureEnabled('beta-search', { plan: 'premium', country: 'US' })
    ).toBe(true);
  });

  it('hides the feature from a free-plan user', () => {
    expect(
      isFeatureEnabled('beta-search', { plan: 'free', country: 'US' })
    ).toBe(false);
  });

  it('hides the feature from a premium user outside US/CA', () => {
    expect(
      isFeatureEnabled('beta-search', { plan: 'premium', country: 'DE' })
    ).toBe(false);
  });

  it('hides the feature when a rule attribute is missing', () => {
    expect(isFeatureEnabled('beta-search', { plan: 'premium' })).toBe(false);
  });

  it('shows the feature to an explicitly allowlisted user regardless of rules', () => {
    expect(
      isFeatureEnabled('beta-search', { userId: 'user-42', plan: 'free', country: 'DE' })
    ).toBe(true);
  });
});

describe('ios-widget device rule', () => {
  it('is visible on iOS', () => {
    expect(isFeatureEnabled('ios-widget', { device: 'ios' })).toBe(true);
  });

  it('is hidden on Android', () => {
    expect(isFeatureEnabled('ios-widget', { device: 'android' })).toBe(false);
  });
});
