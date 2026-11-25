# Mobile Testing Troubleshooting — Companion Repo

> Companion repository for the [Mobile Testing Troubleshooting Guide](https://qapractices.com/documentation/mobile-testing-troubleshooting) on QAPractices.com.

## What's inside

- **`check-emulator-acceleration.sh`** — Windows HAXM status check and Android emulator hardware-acceleration verification (Problem 1).
- **`locator-strategies.js`** — fragile XPath vs stable accessibility ID, plus a `waitUntil` pattern for slow-rendering elements (Problem 2).
- **`os-version-permissions.js`** — capability-driven branching for Android 13+ granular media permissions vs legacy permission flow (Problem 3).
- **`network-throttling.js`** — BrowserStack network profiles (`2g`/`3g`/`4g`/`offline`/`intermittent`) applied before triggering sync actions (Problem 4).
- **`browserstack.yml`** — cloud device matrix example: real device vs emulator builds with per-arch APKs (Problem 5).

## Stack

| Tool | Version |
| --- | --- |
| Appium Server | 2.x |
| WebdriverIO | 8.x |
| Node.js | 20 LTS |
| BrowserStack App Automate | any current plan |

## Usage

The `.js` snippets assume a running Appium 2.x session created through WebdriverIO (remote or local). They are extracted from the guide as reference code — wire them into your specs and adjust selectors to your app's accessibility IDs.

```bash
# Local run against an emulator
npm install -g appium
appium driver install uiautomator2
appium
```
