# Component Testing Guide — Companion Scripts

Companion scripts for the [Component Testing Guide](https://qapractices.com/documentation/component-testing-guide).

## Files

| File | Purpose |
| --- | --- |
| `scripts/useCounter.js` | React custom hook for testing state logic. |
| `scripts/useCounter.test.js` | Unit test for the useCounter hook using React Testing Library 16 `renderHook`. |
| `scripts/Button.jsx` | React Button component with variant, disabled, loading and onClick props. |
| `scripts/Button.test.js` | Complete Button test suite: rendering, interaction, keyboard, loading and a11y with jest-axe 9. |
| `scripts/Button.stories.js` | Storybook 8 stories for Primary, Disabled and Loading variants. |

## Usage

```bash
# Install dependencies
npm install react react-dom
npm install -D @testing-library/react@16 @testing-library/user-event@14 jest@29 jest-axe@9
npm install -D storybook@8 @storybook/react@8

# Run tests
npx jest scripts/Button.test.js scripts/useCounter.test.js

# Run Storybook
npx storybook dev -p 6006
```

## Requirements

- Node.js 20+
- React 18+
- React Testing Library 16+
- Jest 29+ or Vitest 2+
- jest-axe 9+
- Storybook 8+
