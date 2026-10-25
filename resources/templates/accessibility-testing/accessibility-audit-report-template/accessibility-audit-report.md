# Accessibility Audit Report

## 1. Report Header

| Field | Value |
|---|---|
| Report ID | [e.g. AUD-2026-014] |
| Report date | [YYYY-MM-DD] |
| Auditor / organization | [Name, company or internal team] |
| Product audited | [Product name and URL] |
| Audit standard | [e.g. WCAG 2.2 Level AA] |
| Report version | [e.g. 1.0 — final] |

## 2. Executive Summary

[2-4 sentences a non-technical stakeholder can act on: the overall conformance position, the single biggest risk, and the recommended first fix.]

**Conformance statement:** Based on the audit conducted from [start date] to [end date], [product name] [conforms / partially conforms / does not conform] to WCAG 2.2 Level [A / AA / AAA]. The audit identified [n] critical, [n] major and [n] minor findings across [n] sampled pages.

## 3. Audit Scope

| Item | Detail |
|---|---|
| Pages or screens sampled | [e.g. home, search, checkout, account settings — 12 of 40 pages] |
| Sampling rationale | [e.g. WCAG-EM structured sample: every template plus high-traffic flows] |
| Out of scope | [e.g. native apps, third-party chat widget, PDF documents] |
| Audit window | [YYYY-MM-DD to YYYY-MM-DD] |

## 4. Methodology

- **Framework:** [e.g. WCAG-EM — Website Accessibility Conformance Evaluation Methodology]
- **Automated tools:** [e.g. axe DevTools 4.x, Lighthouse 12.x — always record versions]
- **Assistive technology:** [e.g. NVDA 2024.x with Firefox, VoiceOver with Safari, keyboard-only navigation]
- **Manual checks:** [e.g. contrast measurement, focus order, reflow at 200% and 400% zoom]

## 5. Findings Summary

| Severity | Count | Examples |
|---|---|---|
| Critical — blocks task completion | [n] | [e.g. checkout confirmation unreachable by keyboard] |
| Major — blocks some users or flows | [n] | [e.g. form errors not announced to screen readers] |
| Minor — degraded but usable | [n] | [e.g. skipped heading levels in article pages] |

## 6. Detailed Findings

Copy the block once per finding and fill it in:

### Finding F-NN: [Short descriptive title]

| Field | Value |
|---|---|
| WCAG criterion | [e.g. 1.4.3 Contrast (Minimum) — Level AA] |
| Severity | [Critical / Major / Minor] |
| Location | [Page and component, e.g. checkout step 2, "Pay now" button] |
| Evidence | [Screenshot ref, tool output line, or reproduction steps] |
| User impact | [Who is blocked and from what] |
| Recommended fix | [Concrete remediation, e.g. raise button contrast ratio to 4.5:1] |

## 7. Remediation Roadmap

| Priority | Finding | Owner | Effort estimate | Target date |
|---|---|---|---|---|
| P0 | [F-NN short title] | [Team or person] | [e.g. 2 days] | [YYYY-MM-DD] |
| P1 | [F-NN short title] | [Team or person] | [e.g. 1 day] | [YYYY-MM-DD] |
| P2 | [F-NN short title] | [Team or person] | [e.g. 0.5 day] | [YYYY-MM-DD] |

Re-audit of [critical and major findings] scheduled for [YYYY-MM-DD].

## 8. Sign-off

| Role | Name | Signature | Date |
|---|---|---|---|
| Lead auditor | [Name] | ____________ | [YYYY-MM-DD] |
| QA lead | [Name] | ____________ | [YYYY-MM-DD] |
| Product owner | [Name] | ____________ | [YYYY-MM-DD] |

## 9. Appendix — Evidence Log

[Screenshots, tool exports (axe JSON or HTML reports), assistive technology session notes, and the full page inventory. Name files so anyone reading can jump from F-NN to its proof without asking you.]
