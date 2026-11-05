const { isFeatureEnabled, getCheckoutComponent, flags } = require('../featureFlags');

describe('checkoutV2 flag', () => {
  afterEach(() => {
    flags.checkoutV2 = true;
  });

  test('returns new checkout when flag is on', () => {
    expect(getCheckoutComponent()).toBe('NewCheckout');
  });

  test('returns old checkout when flag is off', () => {
    flags.checkoutV2 = false;
    expect(getCheckoutComponent()).toBe('OldCheckout');
  });

  test('returns old checkout when flag is undefined', () => {
    delete flags.checkoutV2;
    expect(isFeatureEnabled('checkoutV2')).toBe(false);
    expect(getCheckoutComponent()).toBe('OldCheckout');
  });

  test('returns old checkout when flag is a non-boolean', () => {
    flags.checkoutV2 = 'yes';
    expect(isFeatureEnabled('checkoutV2')).toBe(false);
  });
});

describe('env-var flag: new-checkout', () => {
  const OLD = process.env.NEW_CHECKOUT;
  afterEach(() => {
    process.env.NEW_CHECKOUT = OLD;
  });

  it('resolves false when env is "false"', () => {
    process.env.NEW_CHECKOUT = 'false';
    expect(isFeatureEnabled('new-checkout')).toBe(false);
  });

  it('resolves true when env is "true"', () => {
    process.env.NEW_CHECKOUT = 'true';
    expect(isFeatureEnabled('new-checkout')).toBe(true);
  });

  it('resolves false when env is unset', () => {
    delete process.env.NEW_CHECKOUT;
    expect(isFeatureEnabled('new-checkout')).toBe(false);
  });
});
