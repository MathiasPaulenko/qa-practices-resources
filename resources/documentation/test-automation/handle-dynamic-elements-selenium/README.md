# Handle Dynamic Web Elements in Selenium — Companion

Companion resource for [How to Handle Dynamic Web Elements in Selenium](https://qapractices.com/documentation/handle-dynamic-elements-selenium/).

Runnable Selenium 4 examples (Java + Python) covering every pattern in the guide — explicit waits, `ExpectedConditions`, custom conditions, FluentWait, dynamic IDs, AJAX content, custom dropdowns, iframes and native shadow DOM — executed against local HTML fixtures, so nothing depends on a live site.

## Requirements

- Chrome + ChromeDriver on PATH (or let Selenium Manager resolve it).
- Java 17+ with Maven, **or** Python 3.10+.

## Run the Java suite

```bash
cd java
mvn test
```

## Run the Python suite

```bash
cd python
pip install -r requirements.txt
python -m pytest -v
```

## What's inside

| Example | What it demonstrates |
|---|---|
| `dynamicId_*` | Generated IDs; `data-testid` vs `button[id^='btn_']` + `elementToBeClickable` |
| `ajaxContent_*` | Waiting for the spinner to disappear, then for the results list |
| `dynamicDropdown_*` | Click-then-wait for a custom (non-`<select>`) dropdown |
| `shadowDom_*` | Native `getShadowRoot()` / `element.shadow_root` in Selenium 4 |
| `customWait_*` | Lambda condition waiting for a class to flip to `active` |
| `fluentWait_*` (Java) | Custom polling interval, ignoring `NoSuchElementException` |
| `iframe_*` | `switchTo().frame()`, interact, `defaultContent()` back |

The fixtures live in `fixtures/`: `dynamic-page.html` reproduces generated IDs, delayed AJAX, a custom dropdown, a shadow root and a class that flips after load; `iframe-page.html` embeds an inline frame via `srcdoc`.

Versions: Selenium 4.25.0 (Java via Maven, Python via `requirements.txt`), JUnit 5.11, pytest 8.3.
