# Guía de Vitest — Companion

Companion para [Guía de Vitest para Testing en Frontend Moderno](https://qapractices.com/es/documentation/vitest-testing-guide).

## Contenido

- `src/calculator.ts` — Funciones de dominio usadas en los ejemplos
- `src/calculator.test.ts` — Test básico con `describe`, `it`, `expect`
- `src/mocking.test.ts` — `vi.fn()`, `vi.mock()`, `mockImplementationOnce`
- `src/snapshot.test.ts` — `toMatchSnapshot`, `toMatchInlineSnapshot`
- `vite.config.ts` — Config de Vitest con coverage thresholds y jsdom

## Requisitos

- Node.js 18+
- Vitest 3+
- Un proyecto Vite (o el `vite.config.ts` incluido)

## Uso

Son snippets de referencia, no un proyecto ejecutable. Copia los archivos de test a tu proyecto Vite e instala Vitest:

```bash
npm install --save-dev vitest@3 @vitest/ui@3
```

Agrega a tu `vite.config.ts`:

```typescript
test: {
  globals: true,
  environment: 'jsdom',
  coverage: { provider: 'v8' },
}
```

Consulta la guía para tests de componentes, integración CI/CD y errores comunes.
