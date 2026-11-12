# Localization Testing for Games Companion

Companion resource for [Localization Testing for Games](https://qapractices.com/documentation/localization-testing-for-games). Runnable scripts for the three mechanical l10n gates from the guide: pseudo-localization, expansion budgets, and hardcoded-string detection.

## Files

| File | What it does | Stack |
|------|--------------|-------|
| `pseudolocalize.py` | Accents, expands and wraps strings for pseudo-locale builds | Python 3.9+ stdlib |
| `check_expansion.py` | Flags translations over their per-area expansion budget | Python 3.9+ stdlib, CSV input |
| `find_hardcoded_strings.py` | Scans source files for UI literals that bypass the string table | Python 3.9+ stdlib |

## Quick Start

```bash
# Generate a pseudo-localized string table
python pseudolocalize.py < strings_en.txt > strings_pseudo.txt

# Check a German export against expansion budgets (exits 1 on violations)
python check_expansion.py strings_de.csv

# Find hardcoded UI strings in game source
python find_hardcoded_strings.py src/ --ext .cs .gd .cpp
```

All three run on the standard library — no dependencies. `check_expansion.py` exits non-zero when it finds violations, so it drops straight into a CI gate.

## Requirements

- Python 3.9+
- A string table CSV for `check_expansion.py` with columns `key`, `en`, `target` and optionally `ui_area` (`button`, `hud`, `paragraph`; defaults to `default`)
