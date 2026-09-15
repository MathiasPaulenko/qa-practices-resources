# Mocking and Stubbing in Unit Tests — Companion (ES)

Recurso companion para [Guía de Mocking y Stubbing en Unit Tests](https://qapractices.com/es/documentation/mocking-and-stubbing-in-unit-tests-guide).

## Contenido

- `src/stub_repository.ts` — Stub en Jest 30.5: `mockReturnValue` en un repositorio
- `src/mock_logger.ts` — Mock en Jest 30.5: verificar que `logger.error` fue llamado con el mensaje correcto
- `src/fake_repository.ts` — Repositorio fake en memoria implementando la interfaz `UserRepository`

## Requisitos

- Node.js 20+
- Jest 30.5+

## Uso

Son snippets de referencia, no un proyecto ejecutable. Copia el patrón en tu propio archivo de test:

```typescript
// Stub: devuelve un valor fijo
const repo = { findById: jest.fn().mockReturnValue({ id: 1 }) };

// Mock: verifica que una llamada ocurrió
expect(logger.error).toHaveBeenCalledWith(expect.stringContaining('Invalid'));

// Fake: implementación en memoria
const repo = new FakeUserRepository();
```

Consulta la guía para saber cuándo usar stubs vs mocks vs fakes vs spies.
