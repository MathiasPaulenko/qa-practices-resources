# Jest 29 Example Project: React & Node.js

Companion project for the [Jest Testing Guide](https://qapractices.com/documentation/jest-testing-guide/) on QAPractices.

This is a runnable Jest 29 setup that follows the examples in the guide. It includes two Jest configurations:

- `jest.config.js` — Node.js backend tests with TypeScript support.
- `jest.config.react.js` — React component tests with `jest-environment-jsdom` and React Testing Library.

## Requirements

- Node.js 20 LTS or 22 LTS
- npm 10+

## Install

```bash
cd jest-react-node
npm install
```

## Run the tests

Node.js examples:

```bash
npm test
```

React examples:

```bash
npm run test:react
```

Run with coverage:

```bash
npm run test:coverage
```

## Project structure

```text
jest-react-node/
├── jest.config.js          # Node.js + TypeScript
├── jest.config.react.js    # React + jsdom
├── jest.setup.js           # Testing Library jest-dom matchers
├── src/
│   ├── calculator.js
│   ├── fetchUser.js
│   ├── user.service.js
│   ├── api.js
│   └── components/
│       ├── UserCard.jsx
│       └── LoginForm.jsx
├── __tests__/
│   ├── calculator.test.js
│   ├── fetchUser.test.js
│   ├── user.service.test.js
│   ├── UserCard.test.jsx
│   └── LoginForm.test.jsx
└── .github/workflows/test.yml
```

## What each test demonstrates

| Test | Concept |
| --- | --- |
| `calculator.test.js` | Matchers and `toThrow` |
| `fetchUser.test.js` | Async testing and `global.fetch` mocking |
| `user.service.test.js` | `jest.mock` for modules |
| `UserCard.test.jsx` | Snapshot testing with React |
| `LoginForm.test.jsx` | React Testing Library, `fireEvent`, `waitFor` |

## CI/CD

The included `.github/workflows/test.yml` runs the Node.js suite with a Node 20/22 matrix, lint, tests, coverage upload and build.
