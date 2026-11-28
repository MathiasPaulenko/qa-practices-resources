```text
MODULE 2 — API Testing Fundamentals (weeks 2-3, 8h)
Skill gap closed: all coverage is UI-level
Prerequisites: Module 1 (HTTP basics refresher, self-paced)
Objectives: trainee writes a parameterized API test for the checkout
  endpoints; trainee validates status, body schema and auth errors.
Delivery: 2h self-paced reading + 6h labs

LABS (all on the real stack)
1. Replay the checkout flow in Postman against staging; export the
   collection and identify the 3 riskiest endpoints (payment, stock
   hold, order confirm).
2. Port that collection to a Playwright APIRequestContext suite in
   TypeScript; add schema assertions for the order-confirm response.
3. Break auth on purpose: expired token, wrong role, missing header —
   assert the API returns the documented errors.

ASSESSMENT: the Playwright API suite runs in the GitHub Actions pipeline
against staging. If the suite doesn't pass CI, pair with the mid-level
QA in week 4's lab block before moving on.

CHECKPOINT (end of week 3): each junior has ≥1 merged API test.
If not, week 4 becomes lab-only and Module 4 slides a week.
```
