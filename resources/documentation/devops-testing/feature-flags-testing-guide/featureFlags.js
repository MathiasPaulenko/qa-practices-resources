const crypto = require('node:crypto');

// In-memory flag store. Mirrors the four flag shapes from the guide:
// plain boolean, env-var backed, targeting rules + allowlist, percentage rollout.
const flags = {
  checkoutV2: true,
  'new-checkout': 'env',
  'new-dashboard': { enabled: true, percentage: 50 },
  'ios-widget': {
    enabled: true,
    rules: [{ attribute: 'device', values: ['ios'] }],
  },
  'beta-search': {
    enabled: true,
    rules: [
      { attribute: 'plan', values: ['premium', 'enterprise'] },
      { attribute: 'country', values: ['US', 'CA'] },
    ],
    allowlist: ['user-42'],
  },
};

const ENV_VARS = { 'new-checkout': 'NEW_CHECKOUT' };

// sha256(flagKey:userId) mod 100 — the same deterministic bucketing a flag
// service applies, so a user lands in the same bucket on every request.
function bucket(flagKey, userId) {
  const digest = crypto.createHash('sha256').update(`${flagKey}:${userId}`).digest();
  return digest.readUInt32BE(0) % 100;
}

function matchesRules(rules, context) {
  return rules.every((rule) => {
    const value = context[rule.attribute];
    return value !== undefined && rule.values.includes(value);
  });
}

function isFeatureEnabled(key, context = {}) {
  const flag = flags[key];

  if (flag === 'env') {
    const envName = ENV_VARS[key];
    return envName ? process.env[envName] === 'true' : false;
  }

  if (typeof flag !== 'object' || flag === null) return flag === true;
  if (!flag.enabled) return false;
  if (flag.allowlist && flag.allowlist.includes(context.userId)) return true;
  if (flag.rules && !matchesRules(flag.rules, context)) return false;
  if (typeof flag.percentage === 'number') {
    if (!context.userId) return false;
    return bucket(key, context.userId) < flag.percentage;
  }
  return true;
}

function getCheckoutComponent(context) {
  return isFeatureEnabled('checkoutV2', context) ? 'NewCheckout' : 'OldCheckout';
}

module.exports = { flags, isFeatureEnabled, getCheckoutComponent, bucket };
