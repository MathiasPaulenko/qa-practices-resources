# Pagination Test Cases: Runnable pytest Suite

Companion to the QAPractices guide [Pagination Test Cases: Offset, Cursor, and Infinite Scroll](https://qapractices.com/test-cases/pagination-test-cases/).

A Flask mini-app that serves both offset (`?page&limit`) and cursor (`?limit&cursor`) pagination over a seeded dataset, plus a pytest 8.3 suite implementing the API-side test cases TC-01–TC-05 and TC-08–TC-10. TC-06/TC-07 (infinite scroll) are UI cases — the Playwright snippet in the guide covers those.

## Project structure

```text
├── app.py            # Flask app: seeded dataset, offset + cursor strategies
├── test_pagination.py
└── requirements.txt
```

## Concept mapping

| Test case | What it proves | Function |
|---|---|---|
| TC-01/02/08 | Offset metadata: `total`, `totalPages`, `hasNextPage` | `test_tc01_*`, `test_tc02_*`, `test_tc08_*` |
| Boundary rows | `page=0`, `limit>max`, negative, beyond-last | `test_page_*` |
| TC-03/04 | Cursor traversal + invalid cursor 400 | `test_tc03_*`, `test_tc04_*` |
| TC-05 | Stable sort at page boundary (id tiebreak) | `test_tc05_*` |
| TC-10 | Offset shift vs cursor stability under insert | `test_tc10_*` |

## Requirements

- Python 3.10+, `pip install -r requirements.txt` (Flask 3.x, pytest 8.3).

## Usage

```bash
pip install -r requirements.txt
pytest -v
```

No server needed — the tests use Flask's test client. To poke the API by hand:

```bash
python app.py   # serves on :5000
curl "http://localhost:5000/items?page=1&limit=10"
```
