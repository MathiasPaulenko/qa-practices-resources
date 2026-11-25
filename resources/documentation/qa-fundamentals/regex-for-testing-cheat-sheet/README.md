# Regex for Testing Cheat Sheet — Companion

Runnable files from the [Regular Expressions for Testing Cheat Sheet](https://qapractices.com/documentation/regex-for-testing-cheat-sheet/) on QAPractices.com.

## Contents

| File | What it is |
|---|---|
| `src/patterns.txt` | Every pattern from the guide, organized by section, with dialect notes |
| `src/patterns.test.js` | Zero-dependency Node script that runs each validation pattern against positive and negative samples |

## Usage

```bash
node src/patterns.test.js    # prints "12 patterns checked, 0 failure(s)"
```

Copy the pattern lines you need from `patterns.txt` into your assertions. If you
adapt a pattern, add a matching sample to `patterns.test.js` so the change is
verified, not assumed.
