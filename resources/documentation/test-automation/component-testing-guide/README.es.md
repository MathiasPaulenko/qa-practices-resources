# Guía de Testing de Componentes — Scripts Companion

Scripts companion para la [Guía de Testing de Componentes](https://qapractices.com/es/documentation/component-testing-guide).

## Archivos

| Archivo | Propósito |
| --- | --- |
| `scripts/useCounter.js` | Custom hook de React para testear lógica de estado. |
| `scripts/useCounter.test.js` | Test unitario para el hook useCounter usando `renderHook` de React Testing Library 16. |
| `scripts/Button.jsx` | Componente Button de React con props variant, disabled, loading y onClick. |
| `scripts/Button.test.js` | Suite completa de tests de Button: rendering, interacción, teclado, loading y a11y con jest-axe 9. |
| `scripts/Button.stories.js` | Stories de Storybook 8 para variantes Primary, Disabled y Loading. |

## Uso

```bash
# Instalar dependencias
npm install react react-dom
npm install -D @testing-library/react@16 @testing-library/user-event@14 jest@29 jest-axe@9
npm install -D storybook@8 @storybook/react@8

# Correr tests
npx jest scripts/Button.test.js scripts/useCounter.test.js

# Correr Storybook
npx storybook dev -p 6006
```

## Requisitos

- Node.js 20+
- React 18+
- React Testing Library 16+
- Jest 29+ o Vitest 2+
- jest-axe 9+
- Storybook 8+
