# Hallucination Detection Test Cases — Companion

Companion resource for [Hallucination Detection Test Cases: 20 Scenarios](https://qapractices.com/test-cases/hallucination-detection-test-cases/).

## Contents

- `claim_verifier.py` — stdlib-only model of the detection pipeline: `extract_claims` splits generated output into atomic sentences, `verify_claim` checks each claim against the retrieved sources (token coverage stands in for the embedding/NLI call from the article, so everything runs offline), and `verify` scores supported/total claims and returns a ship-or-review decision. `Verdict` distinguishes `SUPPORTED`, `UNSUPPORTED` and `CONTRADICTED` — the last one covers numeric conflicts and disagreeing sources.
- `tests/conftest.py` — puts the engine on `sys.path`.
- `tests/test_claim_verifier.py` — executable subset of the article's cases: nonexistent person (TC-01), nonexistent founding year (TC-02), unsupported statistic (TC-03), post-cutoff event (TC-04), fabricated citation (TC-05), numeric contradiction (TC-06), parametric override (TC-07), invented list item (TC-09), domain-term definition (TC-10), relationship inference (TC-12), unstated geography (TC-13), conflicting sources (TC-16), empty source set (TC-17) and minimal context (TC-18).

## Requirements

- Python 3.10+
- pip

## Usage

```bash
pip install -r requirements.txt
pytest tests/ -v
```

Expected output: `17 passed`.

The verifier is deliberately stdlib-only. In production swap `_coverage` for an embedding cosine similarity (sentence-transformers) or an NLI cross-encoder like `cross-encoder/nli-deberta-v3-large`, as described in the article.

## Related

- Article EN: https://qapractices.com/test-cases/hallucination-detection-test-cases/
- Article ES: https://qapractices.com/es/test-cases/hallucination-detection-test-cases/
