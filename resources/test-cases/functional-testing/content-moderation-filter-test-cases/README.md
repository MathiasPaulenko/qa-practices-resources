# Content Moderation Filter — Companion

Executable pytest suite for the [Content Moderation Filter Test Cases](https://qapractices.com/test-cases/content-moderation-filter-test-cases/) resource on QAPractices.

`conftest.py` ships a small rule-based `moderate()` reference implementation: NFKC normalization, homoglyph mapping, leet-speak folding, emoji/punctuation stripping, and word-boundary blocklist matching. The suite exercises the cases that trip real filters — substring false positives, bypass attempts, threshold determinism, empty and oversized input.

## Run

```bash
pip install -r requirements.txt
pytest tests/ -v          # 24 tests
```

## Covers

- Positive: profanity detection, clean pass-through, repeated-link spam, high/low toxicity scores
- False positives: Scunthorpe-problem dictionary terms, academic sensitive discussion
- Bypass: leet speak, Cyrillic homoglyphs, spacing/punctuation, emoji insertion, NFC/NFD equivalence
- Boundaries: score exactly at threshold, whitespace-only input, 80k-char content, link-count edge
