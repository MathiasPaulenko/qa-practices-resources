# Guía de Componentes con Cypress — Ejemplos

Recurso companion para [Guía de Componentes con Cypress: React, Vue y Angular](https://qapractices.com/es/documentation/cypress-component-testing-guide/).

Tres proyectos ejecutables de Cypress 15 component testing:

- **React** — Componente Button con props, eventos y wrapper de provider
- **Vue 3** — Componente Stepper con props y eventos de clic
- **Angular** — Componente Stepper con componentProperties y output spies

## Prerrequisitos

- Node.js 22+
- Cypress 15.21.0+

## Ejecutar ejemplos de React

```bash
cd react
npm install
npx cypress open --component
# o headless:
npx cypress run --component
```

## Ejecutar ejemplos de Vue

```bash
cd vue
npm install
npx cypress open --component
```

## Ejecutar ejemplos de Angular

```bash
cd angular
npm install
npx cypress open --component
```

## CI

El workflow en `.github/workflows/cypress-ct.yml` corre las tres suites en GitHub Actions.

## Versiones

| Herramienta | Versión |
| --- | --- |
| Cypress | 15.21.0 |
| React | 18-19 |
| Vue | 3+ |
| Angular | 18-21 |
