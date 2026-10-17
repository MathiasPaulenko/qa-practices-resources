# Release Testing Checklist — Companion Files

Companion for [Release Testing Checklist](https://qapractices.com/checklists/release-testing-checklist/). A runnable post-deploy smoke script and a three-gate release sign-off template matching the checklist gates.

## Files

| File | Purpose |
| ---- | ------- |
| `smoke-test.sh` | Post-deployment smoke script: parameterised with `BASE_URL`/`API_KEY`, returns non-zero on any failure so it can gate a pipeline or trigger a rollback check. |
| `release-signoff-template.md` | Printable three-gate sign-off sheet (pre-release, deployment, post-release) with owner + timestamp per item, plus a rollback record section. |

## Usage

```bash
chmod +x smoke-test.sh
BASE_URL="https://your-staging-host" API_KEY="$STAGING_TOKEN" ./smoke-test.sh
```

Copy `release-signoff-template.md` per release — fill owners and times during the deploy, then file it with the release notes.

## Requirements

- `bash`, `curl` — that's it. The script runs anywhere a pipeline can.
