# Desktop App Auto-Update Testing Checklist — Companion

Runnable artifacts for the [Desktop App Auto-Update Testing Checklist](https://qapractices.com/checklists/desktop-app-auto-update-testing-checklist/) on QAPractices.

## Files

| File | Purpose |
|---|---|
| `config/update_manifest.json` | Sample update-feed manifest (version, minimum, url, signature, force flag) |
| `tests/version_check.py` | Semver comparison helper: returns `force`, `available`, or `none` |
| `scripts/feed_smoke.sh` | curl + jq smoke test that validates the feed manifest shape |
| `requirements.txt` | Python dependency (`packaging`) |

## Usage

```bash
pip install -r requirements.txt
python tests/version_check.py
bash scripts/feed_smoke.sh https://your-update-server/latest.json
```

`update_manifest.json` mirrors the structure a desktop updater fetches before
downloading a package — point your app's feed URL at it (or a local static
server) to simulate update detection, forced updates, and signature checks.
