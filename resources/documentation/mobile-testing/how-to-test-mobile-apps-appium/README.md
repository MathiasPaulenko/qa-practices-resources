# Mobile Apps with Appium — pytest companion

Companion for [Mobile Apps with Appium: First Tests](https://qapractices.com/documentation/how-to-test-mobile-apps-appium/).

- `tests/conftest.py` — UiAutomator2 session fixture; skips until you set `CAPABILITIES["appium:app"]`.
- `tests/test_first_appium_test.py` — the three selector strategies from Step 4 (accessibility id, resource-id, XPath) plus an explicit-wait pattern (no `Thread.sleep`).
- `.github/workflows/appium-ci.yml` — the emulator job from Step 10.
- `requirements.txt` — `appium-python-client 4.2` + `pytest 8.3`.

## Run

```bash
pip install -r requirements.txt
# Edit CAPABILITIES["appium:app"] in tests/conftest.py, then:
appium --port 4723 &
pytest tests/ -v
```
