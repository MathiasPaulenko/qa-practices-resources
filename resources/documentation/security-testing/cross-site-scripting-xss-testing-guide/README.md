# XSS Testing Guide — Companion Scripts and Payloads

> Companion resource for [XSS Testing Guide: Reflected, Stored & DOM-Based Attacks](https://qapractices.com/documentation/cross-site-scripting-xss-testing-guide) on QAPractices.com.

Scripts, payload library and CI workflow for testing reflected, stored and DOM-based XSS with Python 3.12, OWASP ZAP 2.15 and dalfox 2.x.

## Requirements

- Python 3.12+
- `requests` 2.32
- OWASP ZAP 2.15 (optional, for automated scans)
- dalfox 2.x (optional, for CLI scanning)

## Setup

```bash
# Install Python dependencies
pip install requests==2.32

# Optional: install dalfox (Go required)
go install github.com/hahwul/dalfox/v2@latest

# Run the reflected XSS probe
python scripts/reflected_xss_probe.py --url https://staging.qa.local/search

# Run the CSP verifier
python scripts/csp_verifier.py --url https://staging.qa.local

# Run dalfox against a target
dalfox url "https://staging.qa.local/search?q=test" --blind https://xss-receiver.qa.local
```

## Files

| File | Purpose |
| ------ | --------- |
| `scripts/reflected_xss_probe.py` | Python script to test a search endpoint for reflected XSS |
| `scripts/csp_verifier.py` | Verify CSP headers and test payload blocking |
| `scripts/stored_xss_probe.py` | Post a payload and verify it renders unencoded on retrieval |
| `payloads/basic_probes.txt` | Basic probe payloads (alert, console.log) |
| `payloads/context_specific.txt` | Context-specific payloads (HTML, JS, URL, DOM) |
| `payloads/filter_evasion.txt` | Filter evasion payloads (nested tags, event handlers) |
| `.github/workflows/xss-regression.yml` | CI workflow for XSS regression tests |

## Payload Library

The `payloads/` directory contains reusable payload lists organized by context:

- `basic_probes.txt` — safe, observable payloads for confirming execution
- `context_specific.txt` — payloads for HTML, JavaScript, URL and DOM contexts
- `filter_evasion.txt` — payloads for bypassing common filters (nested tags, case variations, double encoding)

## License

MIT — free to use, modify, and distribute. Never test XSS against systems you do not own or do not have explicit authorization to test.
