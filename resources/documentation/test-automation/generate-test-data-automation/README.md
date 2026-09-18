# How to Generate Test Data for Automation — Companion

Runnable companion for the guide
[How to Generate Test Data for Automation](https://qapractices.com/documentation/generate-test-data-automation).

Three self-contained examples covering the guide's steps — no external services needed.

## Contents

| Folder | Stack | What it covers |
|--------|-------|----------------|
| `javascript/` | @faker-js/faker 10.6.0 + Jest 30 | Steps 1, 3, 6-7: Faker basics, factory pattern, deterministic seeds, CSV/JSON output |
| `python/` | faker 40.39.0 + pytest 8.4 | Steps 2, 5-6: Faker Python, database seeding fixture (sqlite), CSV generation |
| `java/` | JDK only (no dependencies) | Step 4: fluent `UserBuilder` with assertions in `main` |

## Run

```bash
# JavaScript (installs deps, then runs Jest + the file generators)
cd javascript && npm ci && npm test && npm run generate

# Python
cd python && pip install -r requirements.txt && pytest -v

# Java
cd java && javac UserBuilder.java && java UserBuilder
```

## Notes

- `faker.seed(12345)` makes every run deterministic — the same generated values on CI and local.
- The Python seeding example uses sqlite via `tmp_path`, so it demonstrates the real
  yield-fixture cleanup pattern without needing a running database.
- `generate.js` writes `test-data.json` and `test_users.csv` next to itself; both are gitignored.

Companion of <https://qapractices.com/documentation/generate-test-data-automation>
