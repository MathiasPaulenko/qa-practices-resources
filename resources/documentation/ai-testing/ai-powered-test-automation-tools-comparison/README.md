# AI-Powered Test Automation Tools Comparison Companion

Companion resource for the [AI-Powered Test Automation Tools Comparison](https://qapractices.com/documentation/ai-powered-test-automation-tools-comparison). Contains working examples for self-healing selectors, user story parsing, and Launchable predictive test selection.

## Files

| File | Purpose |
| ---- | ------- |
| `src/self_healing_fallback.py` | Selenium helper with fallback selector strategy |
| `src/user_story_parser.py` | Parse user stories into test outlines |
| `src/launchable_subset.sh` | Launchable CLI commands for predictive test selection |
| `.github/workflows/ai-tests.yml` | CI workflow with Launchable integration |

## Quick Start

```bash
# Self-healing fallback example
python src/self_healing_fallback.py

# User story parser
python src/user_story_parser.py

# Launchable subset (requires Launchable CLI + API key)
export LAUNCHABLE_API_KEY=your-key
bash src/launchable_subset.sh
```

## Requirements

- Python 3.11+
- Selenium (for self-healing example)
- Launchable CLI (for test selection example)
