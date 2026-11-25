# Robot Framework Testing Guide — Companion Repo

> Companion repository for the [Robot Framework Testing Guide for Automation](https://qapractices.com/documentation/robot-framework-testing-guide) on QAPractices.com.

## What's inside

- **`tests/login_tests.robot`** — first SeleniumLibrary suite: valid/invalid login plus user keywords (Steps 1 and 3).
- **`tests/data_driven_tests.robot`** — `Test Template` example: one keyword fed by a table of input data (Step 5).
- **`tests/api_tests.robot`** — API checks through the custom Python library (Step 7).
- **`resources/common_keywords.robot`** — shared keywords: browser setup/teardown, login, verification, screenshot on failure (Step 4).
- **`libraries/CustomLibrary.py`** — Python library exposing `get_api_response`, `post_api_data` and `validate_json_field` as keywords (Step 7).
- **`.github/workflows/robot-tests.yml`** — GitHub Actions workflow: pinned versions, Chrome install, tag-filtered run, artifact upload on failure (Step 9).

## Stack

| Tool | Version |
| --- | --- |
| Robot Framework | 7.2.2 |
| SeleniumLibrary | 6.6.1 |
| Python | 3.10+ |
| webdriver-manager | latest |

## Usage

```bash
pip install robotframework==7.2.2 robotframework-seleniumlibrary==6.6.1 requests webdriver-manager

# Run a single suite
robot tests/login_tests.robot

# Run by tag
robot --include smoke tests/
```

Replace the `example.com` pl
