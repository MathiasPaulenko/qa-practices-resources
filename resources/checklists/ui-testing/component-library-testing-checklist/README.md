# Component Library Testing — Companion

Runnable companion for the [Component Library Testing Checklist](https://qapractices.com/checklists/component-library-testing-checklist/). A minimal mock `Button` component plus the three artifacts the checklist references:

| File | What it shows |
|---|---|
| `Button.tsx` | A library component with `variant`, `loading` and `disabled` states and correct `aria-busy`/`disabled` behavior. |
| `Button.stories.tsx` | Storybook 8 CSF3 stories with `play` interaction tests using `storybook/test` (`userEvent`, `expect`, `within`). |
| `Button.axe.test.tsx` | `jest-axe` assertions proving the component passes axe in every state — default, disabled, primary and loading. |
| `chromatic.config.json` | Chromatic CI config: `onlyChanged`, `exitZeroOnChanges`, Storybook build dir. |
| `package.json` | Dependency versions: Storybook 8.x, jest-axe 10.x, Chromatic 13.x. |

## Run

```bash
npm install
npm test                                # jest-axe accessibility suite
npx storybook dev                       # stories + interaction tests in the panel
npx chromatic --project-token=$CHROMATIC_PROJECT_TOKEN   # visual regression in CI
```

The Chromatic token belongs in an environment variable — never in the repo. These files exercise three of the checklist's eight layers (unit behavior, visual regression, accessibility); the rest are process checks rather than code.
