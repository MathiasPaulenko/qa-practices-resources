# Security Testing Guide — Runnable Companion

Companion repository for the QAPractices guide
[Security Testing Guide: OWASP Top 10 and ZAP Scans](https://qapractices.com/documentation/security-testing-guide/)
([versión en español](https://qapractices.com/es/documentation/security-testing-guide/)).

Self-contained: the mock API is a stdlib `http.server` fixture, so the BOLA
tests run without any external service. The ZAP files plug into a real
`zap-baseline.py` run when you have a staging URL.

## Layout

```text
mock_api.py            stdlib fixture API: token auth + two orders, owner-only access
tests/test_bola.py     pytest 8.2 BOLA regression suite (4 tests)
zap/zap-baseline.conf  rule policy for `zap-baseline.py -c` (ZAP 2.15.0)
zap/parse_baseline.py  stdlib report parser: exits 1 on HIGH alerts (CI gate)
requirements.txt       requests 2.31.0, pytest 8.2.0
```

## Run the BOLA suite

```bash
python -m venv venv
source venv/bin/activate    # venv\Scripts\activate on Windows
pip install -r requirements.txt
pytest tests/test_bola.py -v
```

`mock_api.py` spins up inside the pytest fixture on an ephemeral port. Order 42
belongs to alice — the suite verifies that bob's token cannot read it
(`403`), that a missing or tampered token is rejected (`401`), and that the
owner can read her own order (`200`).

## Run the ZAP baseline

```bash
docker pull zaproxy/zap-stable:2.15.0
docker run -v $(pwd):/zap/wrk:rw -t zaproxy/zap-stable:2.15.0 \
  zap-baseline.py -t https://staging.example.internal \
  -r zap-baseline-report.html -w zap-baseline.md -c zap-baseline.conf
python zap/parse_baseline.py zap-baseline.md
```

Always scan a non-production environment with written authorization.
`parse_baseline.py` returns exit code 1 when the report lists any HIGH alert,
so it can gate a pipeline step directly.
