# Feature Flag Testing Lab

Runnable companion for the [Feature Flags Testing Guide](https://qapractices.com/documentation/feature-flags-testing-guide/) — a stdlib-only flag evaluator covering the four flag shapes from the guide (boolean, env-var, targeting rules + allowlist, deterministic percentage rollout) plus Jest 29 suites for flag states, segmentation boundaries, rollout determinism and flag-service failure handling with MSW 2.x.

## Run

```bash
npm install
npm test
```

Node 18+ required. The three evaluator suites run on Jest 29; the flag-service suite (`tests/flags-api.test.mjs`) runs on `node:test`, because MSW 2.x is ESM-only and resolves cleanly under Node's own module system — no jest polyfills needed.

## What it covers

| Suite | Guide section | What it proves |
|---|---|---|
| `tests/featureFlags.test.js` | Unit tests + env-var vs SDK flags | On/off/undefined/non-boolean resolution, env-var fallback |
| `tests/segmentation.test.js` | Targeted segmentation testing | Rule boundaries: plan, country, device, allowlist precedence |
| `tests/rollout.test.js` | Gradual rollout monitoring | sha256 bucket determinism, ~50/50 split, monotonic upgrades, 0%/100% edges |
| `tests/flags-api.test.mjs` | Mocked flag service | Flag on, flag off, HTTP 503 and network-failure fallbacks |

## Flag shapes in `featureFlags.js`

- `checkoutV2` — plain boolean, the unit-test surface.
- `new-checkout` — env-var backed (`NEW_CHECKOUT`), resolved at boot.
- `new-dashboard` — 50% percentage rollout, `sha256(flagKey:userId) mod 100` bucketing.
- `ios-widget` — device targeting rule.
- `beta-search` — plan + country rules with an explicit allowlist.

`launchdarkly-example.js` is a reference snippet for the LaunchDarkly section — it is not executed by the suite.
