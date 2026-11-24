# Accessibility Testing Troubleshooting — Companion

Runnable snippets referenced in the [Accessibility Testing Troubleshooting Guide](https://qapractices.com/documentation/accessibility-testing-troubleshooting/) on QAPractices.

## Files

| File | Problem it solves |
|---|---|
| `contrast-tokens.css` | WCAG 2.2 AA contrast-verified design tokens + `.sr-only` helper (Problem 1) |
| `aria-labels.html` | Accessible names for icon-only buttons and form labels (Problem 2) |
| `live-regions.html` | `aria-live` / `role="alert"` patterns for dynamic content (Problem 4) |
| `focus-trap.js` | Vanilla-JS focus trap for modal dialogs (Problem 3) |
| `spa-focus.ts` | Angular `NavigationEnd` focus management for SPAs (Problem 5) |

## Usage

- `focus-trap.js`: call `trapFocus(dialogElement)` when opening a modal; call `triggerElement.focus()` when closing it.
- `spa-focus.ts`: drop the `NavigationEnd` subscription into your root component so every route change moves focus to the `h1`.
- `contrast-tokens.css`: verify each token's ratio with a contrast checker before shipping; the comments list the measured ratios on white.

No dependencies — everything runs in the browser as-is except `spa-focus.ts`, which needs `@angular/router` and `rxjs`.
