# Mobile Deep Link Testing Matrix Template — Companion

Standalone files for the [Mobile Deep Link Testing Matrix Template](https://qapractices.com/templates/mobile-deep-link-testing-matrix-template/) on QAPractices. Copy the blank matrix into your wiki, Notion or test management tool and start filling rows — no copy-paste from the browser needed.

## Files

| File | What it is |
|---|---|
| `deep-link-testing-matrix.md` | The blank matrix: deep link details, universal links, app links, custom URI scheme, deferred links, fallback, cross-platform routing, analytics, defect tracking and sign-off |
| `deep-link-testing-matrix-sample.md` | The same matrix completed for a fictional e-commerce app (`shop.example.io`, Branch for deferred links) |
| `deep-link-commands.sh` | The `adb` and `xcrun simctl` commands used to fire deep links and check Android domain verification, with comments |

## Usage

1. Fill the **Deep Link Details** table with your app name, link types and domains.
2. Replace `example.com` URLs and the `myapp://` scheme with your real routes.
3. Test each row in all three app states: foreground, background, not installed.
4. Use `deep-link-commands.sh` as a starting point for manual checks on real devices.

## Related

- [Mobile Deep Link Testing Matrix Template](https://qapractices.com/templates/mobile-deep-link-testing-matrix-template/) — the full template with checklists, best practices and FAQ
- [Deep Link and Universal Link Test Cases](https://qapractices.com/test-cases/deep-link-universal-link-testing/) — executable test cases built on the same scenarios
