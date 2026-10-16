# ISO 9001 Testing Alignment — Audit Evidence Checklist

Use this before a certification or surveillance audit. Every item should be producible within 15 minutes of request — if you have to build it, it's not audit-ready.

## Documentation

- [ ] Test strategy document with defined scope and out-of-scope statement
- [ ] Test plan approved and dated within the last release cycle
- [ ] RACI matrix for test activities, published and current
- [ ] Controlled document list covering all test artifacts

## Traceability

- [ ] Every requirement maps to at least one test case
- [ ] Test cases link back to requirement IDs
- [ ] Defects link to the test cases that found them
- [ ] Traceability matrix shows no orphaned requirements or tests

## Execution Records

- [ ] Run logs include: result, environment, build version, tester, date
- [ ] Failed runs show follow-up (retest result or linked defect)
- [ ] Release decision has a signed test summary report

## Metrics & Review

- [ ] Escaped-defect rate tracked per release
- [ ] Test coverage tracked against requirements
- [ ] Internal audit of the QA process completed within the cycle
- [ ] Management review minutes include testing performance data

## Improvement

- [ ] Non-conformances have logged corrective actions
- [ ] Corrective actions verified closed (not just assigned)
- [ ] Continuous improvement items tracked to completion

## Red flags auditors catch

- Traceability matrix updated the week before the audit (dates expose it)
- Defects closed without retest evidence
- Test plans referencing tools or people that no longer exist
- Metrics that exist but have never been reviewed by anyone
