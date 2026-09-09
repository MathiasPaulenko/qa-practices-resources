# Cypress Component Testing Guide — Examples

Companion resource for [Cypress Component Testing Guide: React, Vue & Angular](https://qapractices.com/documentation/cypress-component-testing-guide/).

Three runnable Cypress 15 component testing projects:

- **React** — Button component with props, events and provider wrapper
- **Vue 3** — Stepper component with props and click events
- **Angular** — Stepper component with componentProperties and output spies

## Prerequisites

- Node.js 22+
- Cypress 15.21.0+

## Run React examples

```bash
cd react
npm install
npx cypress open --component
# or headless:
npx cypress run --component
```

## Run Vue examples

```bash
cd vue
npm install
npx cypress open --component
```

## Run Angular examples

```bash
cd angular
npm install
npx cypress open --component
```

## CI

The workflow in `.github/workflows/cypress-ct.yml` runs all three suites in GitHub Actions.

## Versions

| Tool | Version |
| --- | --- |
| Cypress | 15.21.0 |
| React | 18-19 |
| Vue | 3+ |
| Angular | 18-21 |
