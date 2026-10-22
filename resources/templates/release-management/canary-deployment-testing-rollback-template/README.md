# Canary Rollback Decision — Runnable Companion

Runnable companion for the [Canary Deployment Testing and Rollback Template](https://qapractices.com/templates/canary-deployment-testing-rollback-template/) on QAPractices.

`rollback_decision.py` is a stdlib evaluator that takes canary metrics and returns a `promote` / `hold` / `rollback` verdict with severity and the decision maker — the same rules as the template's automated rollback triggers (Section 6.1) and rollback decision matrix (Section 7.2).

## Run the tests

```bash
pip install -r requirements.txt
pytest tests/ -v
```

11 tests cover: happy-path promotion, error-rate rollback (threshold and critical), pod crash loop, consecutive failed evaluations, max canary time, latency 2x baseline vs above threshold (rollback vs hold), low-traffic hold, business-metric drop, and custom thresholds.

## Example

```python
from rollback_decision import Metrics, evaluate

verdict = evaluate(Metrics(error_rate=2.1, p99_latency_ms=390, request_rate=250))
# Decision.ROLLBACK — "error rate 2.1% above threshold 1.0%" (High, SRE on-call)
```
