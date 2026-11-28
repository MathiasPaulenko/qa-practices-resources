```text
EVALUATION MATRIX (excerpt)
context_precision | retrieval | % of retrieved chunks that are relevant
  | ≥ 0.80 | BM25 keywords drag irrelevant docs into top-5
faithfulness | generation | % of claims in the answer supported by context
  | ≥ 0.90 | model fills gaps instead of saying "not in the docs"
hallucination_rate | generation | answers containing a fabricated fact,
  entity, number or citation | = 0 | any fabricated refund amount or
  policy clause

SCENARIO RAG-RET-003 — Ambiguous product name
Query: "Does the Pro plan cover returns?"
Ground truth needed: pricing.md section 3 (Pro plan), returns_policy.md
  section 2 — both chunks expected in top-5
Metric: context_recall ≥ 0.80
Why it isolates a layer: two correct documents must both be retrieved;
  if recall drops, generation can't be blamed for a partial answer.

SCENARIO RAG-HAL-002 — Fabricated policy detail
Query: "Can I return opened software?"
Ground truth needed: returns_policy.md section 5 says opened software is
  not returnable unless defective
Metric: faithfulness ≥ 0.90, hallucination_rate = 0
Failure it provokes: model invents a reasonable-sounding "30-day window"
  that doesn't exist in the policy.

GROUND-TRUTH SPEC (first suite)
Fields per entry: query | expected_answer | expected_chunk_ids |
  difficulty (easy/paraphrase/multi-hop/adversarial)
Size: 80-120 labeled pairs — enough to catch regressions, small enough
  to label in a week of support-desk mining.
```
