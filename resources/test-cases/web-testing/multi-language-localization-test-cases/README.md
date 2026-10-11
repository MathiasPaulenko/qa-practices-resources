# Multi-Language and Localization Testing — Companion

Companion resource for [Multi-Language and Localization Test Cases](https://qapractices.com/test-cases/multi-language-localization-test-cases/).

## Contents

- `mock_server.py` — stdlib-only i18n API serving locale-aware products in `en`, `es`, `de`, `ja`, `ar` plus a cart pluralization endpoint. The `fr` locale intentionally ships a missing key (`cta`) and an empty value (`description`) to exercise fallback behavior.
- `tests/conftest.py` — starts the mock server on an ephemeral port per test session.
- `tests/test_localization.py` — executable subset of the edge cases: locale switching, Accept-Language fallback, missing/empty translation keys, currency formatting, RTL flags, and CLDR plural categories (en/es/de/ja/ru/ar).
- `requirements.txt` — pytest 8.3 + requests.

## Requirements

- Python 3.10+
- pip

## Usage

```bash
pip install -r requirements.txt
cd resources/test-cases/web-testing/multi-language-localization-test-cases
pytest tests/ -v
```

Run the mock standalone for manual checks:

```bash
python mock_server.py 8571
curl "http://127.0.0.1:8571/api/v1/products/PROD-1001?locale=ja-JP"
curl "http://127.0.0.1:8571/api/v1/products/PROD-1001?locale=fr"      # fallback demo
curl "http://127.0.0.1:8571/api/v1/cart/count?n=5&locale=ru"          # 5 товаров
```

## What this covers

- Locale switching (`en`/`es`/`de`/`ja`/`ar`) and `Accept-Language` fallback.
- Missing translation key and empty translation value → clean fallback, no raw keys.
- Locale-aware currency formatting (JPY vs EUR separators).
- RTL flag (`dir`) for Arabic.
- CLDR plural categories including Russian `one/few/many` and Arabic `zero/one/two/few/many`.
