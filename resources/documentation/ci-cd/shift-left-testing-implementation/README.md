# Shift-Left Testing Implementation Companion

Companion resource for [Shift-Left Testing Implementation Guide](https://qapractices.com/documentation/shift-left-testing-implementation). Copy-paste artifacts for the two cheapest gates in the guide: the commit gate and the build gate.

## Files

| File | What it does | Stack |
|------|--------------|-------|
| `build-gate.yml` | GitHub Actions workflow that blocks merges on test failure or low coverage | GitHub Actions, pytest, ruff |
| `.pre-commit-config.yaml` | Commit gate: ruff lint/format + fast unit tests on every commit | pre-commit framework |
| `check_coverage.py` | Parses a Cobertura XML report and exits non-zero under a floor | Python 3.9+ stdlib |

## Quick Start

```bash
# Commit gate — install once per clone
pre-commit install

# Build gate — copy the workflow into your repo
mkdir -p .github/workflows scripts
cp build-gate.yml .github/workflows/build-gate.yml
cp check_coverage.py scripts/check_coverage.py

# Check a coverage report locally
pytest --cov=src --cov-report=xml
python scripts/check_coverage.py coverage.xml --floor 70
```

## Requirements

- Python 3.9+ (check_coverage.py runs on the standard library)
- `pre-commit` package for the commit gate
- The workflow assumes a `requirements.txt` and a `src/` layout — adjust paths to your project

## Notes

- Set `--floor` at your *current* coverage number, then ratchet up monthly. A floor set far above reality gets bypassed within a sprint.
- Mark slow tests with `@pytest.mark.slow` so the commit gate stays under two minutes.
