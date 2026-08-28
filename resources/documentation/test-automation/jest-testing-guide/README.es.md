# Proyecto Ejemplo con Jest 29: React y Node.js

Proyecto de acompañamiento para la [Guía de Pruebas con Jest](https://qapractices.com/es/documentation/jest-testing-guide/) en QAPractices.

Es un setup ejecutable de Jest 29 que sigue los ejemplos de la guía. Incluye dos configuraciones de Jest:

- `jest.config.js` — Tests de Node.js con soporte de TypeScript.
- `jest.config.react.js` — Tests de componentes React con `jest-environment-jsdom` y React Testing Library.

## Requisitos

- Node.js 20 LTS o 22 LTS
- npm 10+

## Instalación

```bash
cd jest-react-node
npm install
```

## Correr los tests

Ejemplos de Node.js:

```bash
npm test
```

Ejemplos de React:

```bash
npm run test:react
```

Con cobertura:

```bash
npm run test:coverage
```

## Estructura del proyecto

```text
jest-react-node/
├── jest.config.js          # Node.js + TypeScript
├── jest.config.react.js    # React + jsdom
├── jest.setup.js           # Matchers de jest-dom de Testing Library
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

## Qué demuestra cada test

| Test | Concepto |
| --- | --- |
| `calculator.test.js` | Matchers y `toThrow` |
| `fetchUser.test.js` | Tests async y mocking de `global.fetch` |
| `user.service.test.js` | `jest.mock` para módulos |
| `UserCard.test.jsx` | Snapshot testing con React |
| `LoginForm.test.jsx` | React Testing Library, `fireEvent`, `waitFor` |

## CI/CD

El archivo `.github/workflows/test.yml` corre el suite de Node.js con una matriz de Node 20/22, lint, tests, subida de cobertura y build.
