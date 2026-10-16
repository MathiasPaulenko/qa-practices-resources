# Testing de Biblioteca de Componentes — Companion

Companion ejecutable del [Checklist de Testing de Biblioteca de Componentes](https://qapractices.com/es/checklists/component-library-testing-checklist/). Un componente `Button` mock mínimo más los tres artefactos que la checklist referencia:

| Archivo | Qué muestra |
|---|---|
| `Button.tsx` | Un componente de biblioteca con estados `variant`, `loading` y `disabled` y comportamiento correcto de `aria-busy`/`disabled`. |
| `Button.stories.tsx` | Stories CSF3 de Storybook 8 con tests `play` usando `storybook/test` (`userEvent`, `expect`, `within`). |
| `Button.axe.test.tsx` | Aserciones de `jest-axe` que prueban que el componente pasa axe en todos los estados — default, disabled, primary y loading. |
| `chromatic.config.json` | Config de Chromatic en CI: `onlyChanged`, `exitZeroOnChanges`, directorio del build de Storybook. |
| `package.json` | Versiones de dependencias: Storybook 8.x, jest-axe 10.x, Chromatic 13.x. |

## Ejecutar

```bash
npm install
npm test                                # suite de accesibilidad con jest-axe
npx storybook dev                       # stories + tests de interacción en el panel
npx chromatic --project-token=$CHROMATIC_PROJECT_TOKEN   # regresión visual en CI
```

El token de Chromatic va en una variable de entorno — nunca en el repositorio. Estos archivos ejercitan tres de las ocho capas de la checklist (comportamiento unitario, regresión visual, accesibilidad); el resto son verificaciones de proceso, no de código.
