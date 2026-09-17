// babel.config.js — lets Jest 30 parse the same ESM test files
// that Vitest runs natively. Vitest ignores this file.
module.exports = {
  presets: [['@babel/preset-env', { targets: { node: 'current' } }]],
};
