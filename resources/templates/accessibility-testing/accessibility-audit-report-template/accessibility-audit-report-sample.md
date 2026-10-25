# Accessibility Audit Report — ClearPath Insurance (Completed Sample)

## 1. Report Header

- **Report ID:** AUD-2026-014
- **Report date:** 2026-10-09
- **Auditor:** Marina Duarte, internal accessibility QA
- **Product audited:** ClearPath Insurance quote portal (staging environment)
- **Audit standard:** WCAG 2.2 Level AA
- **Report version:** 1.0 — final

## 2. Executive Summary

The quote portal does not conform to WCAG 2.2 Level AA. One critical finding blocks keyboard users from completing a quote — the premium slider on the coverage step — and two major findings degrade screen reader users on the same flow. Fixing the slider alone unblocks the core journey; the remediation plan in Section 7 spreads the rest over the next sprint.

**Conformance statement:** Based on the audit conducted from 2026-10-05 to 2026-10-08, ClearPath quote portal partially conforms to WCAG 2.2 Level AA. The audit identified 1 critical, 2 major and 3 minor findings across 12 sampled pages.

## 3. Audit Scope

- **Sampled:** quote flow (5 steps), home, login, policy list, policy detail, claims status, FAQ, contact — 12 pages covering every template and the two highest-traffic journeys.
- **Out of scope:** agent back-office, marketing blog, third-party payment iframe, generated policy PDFs.

## 4. Methodology

WCAG-EM structured sampling; axe DevTools 4.10 automated scan per page; manual keyboard pass on every step; NVDA 2024.4 with Firefox 131 and VoiceOver with Safari 18 on the quote flow; Colour Contrast Analyser 3.5 for contrast measurements; reflow checked at 400% zoom.

## 5. Findings Summary

| Severity | Count | Examples |
|---|---|---|
| Critical — blocks task completion | 1 | Premium slider not operable by keyboard (F-01) |
| Major — blocks some users or flows | 2 | Form errors not announced (F-02), focus lost after step navigation (F-04) |
| Minor — degraded but usable | 3 | Breadcrumb current state unmarked, muted disclaimer contrast 3.8:1, decorative icon in accessibility tree |

## 6. Detailed Findings

### Finding F-01: Coverage slider not operable by keyboard

| Field | Value |
|---|---|
| WCAG criterion | 2.1.1 Keyboard — Level A |
| Severity | Critical |
| Location | Quote flow, step 3 "Coverage" — premium adjustment slider |
| Evidence | `evidence/f01-slider-keyboard.mp4`; slider uses `div` with `oninput`, no `tabindex`, no arrow-key handling |
| User impact | Keyboard-only and switch-device users cannot adjust coverage or submit the quote — the core journey stops here |
| Recommended fix | Replace with `<input type="range">` or add `role="slider"` with `aria-valuemin/max/now` and arrow-key handlers |

### Finding F-02: Form validation errors not announced

| Field | Value |
|---|---|
| WCAG criterion | 4.1.3 Status Messages — Level AA |
| Severity | Major |
| Location | Quote flow, all steps — inline error summary |
| Evidence | NVDA 2024.4 session: errors render visually but no live region announces them; `evidence/f02-nvda-transcript.txt` |
| User impact | Screen reader users submit, get no error feedback, and do not know why the form refuses to advance |
| Recommended fix | Add `role="alert"` to the error summary container and move focus to it on submit failure |

### Finding F-03: "Current step" breadcrumb not conveyed

| Field | Value |
|---|---|
| WCAG criterion | 1.3.1 Info and Relationships — Level A |
| Severity | Minor |
| Location | Quote flow breadcrumb, steps 1-5 |
| Evidence | Visual bold on the current step; no `aria-current="step"` in markup |
| User impact | Screen reader users lose their position inside the five-step flow |
| Recommended fix | Add `aria-current="step"` to the active breadcrumb item |

## 7. Remediation Roadmap

| Priority | Finding | Owner | Effort estimate | Target date |
|---|---|---|---|---|
| P0 | F-01 Coverage slider keyboard support | Frontend team — quote pod | 5 days | 2026-10-16 |
| P1 | F-02 Announce form errors via live region | Frontend team — quote pod | 2 days | 2026-10-14 |
| P1 | F-04 Restore focus after step navigation | Frontend team — quote pod | 1 day | 2026-10-15 |
| P2 | F-03 `aria-current` on breadcrumb | Frontend team | 0.5 day | 2026-10-20 |
| P2 | F-05 Disclaimer contrast to 4.5:1 | Design system | 0.5 day | 2026-10-20 |
| P3 | F-06 Hide decorative icon from AT | Frontend team | 0.5 day | 2026-10-27 |

Re-audit of F-01, F-02 and F-04 scheduled for 2026-10-19, before the v2.4 release.

## 8. Sign-off

| Role | Name | Signature | Date |
|---|---|---|---|
| Lead auditor | Marina Duarte | ____________ | 2026-10-09 |
| QA lead | Tom Okafor | ____________ | 2026-10-09 |
| Product owner | Lucía Ferrer | ____________ | 2026-10-10 |
