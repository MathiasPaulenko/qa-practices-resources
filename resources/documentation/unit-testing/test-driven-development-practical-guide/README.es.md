# TDD Kata — Companion

Recurso companion de [Test-Driven Development (TDD): Guía Práctica](https://qapractices.com/es/documentation/test-driven-development-practical-guide).

## Contenido

- `kata/package.json` — Vitest 3.2 como única devDependency; setup ESM sin configuración
- `kata/src/password.js` — el validador de la sección red-green-refactor de la guía, extendido con reglas de mayúscula y dígito
- `kata/src/fizzbuzz.js` — el FizzBuzz refactorizado final del paso 9 de la guía
- `kata/__tests__/password.test.js` — el test de longitud de la guía más dos reglas adicionales para continuar la kata
- `kata/__tests__/fizzbuzz.test.js` — los cuatro tests del recorrido, en el orden en que fueron escritos

## Requisitos

- Node 20+
- npm

## Uso

```bash
cd kata
npm install

npm test            # Vitest 3.2 — todos los tests en verde
npm run test:watch  # modo watch: editá el código y mirá el ciclo en vivo
npm run coverage    # reporte de cobertura v8
```

## Reproducir el ciclo red-green-refactor

El punto de la kata es ver los tests fallar antes de pasar:

1. Comentá una regla en `src/fizzbuzz.js` (por ejemplo la línea `isMultipleOf(n, 3)`) y ejecutá `npm test` — el test correspondiente pasa a **rojo**.
2. Restaurá apenas el código necesario para que pase — **verde**.
3. Probá una implementación alternativa (por ejemplo `if` anidados en lugar de concatenación de strings) — los tests siguen verdes mientras el diseño cambia. Eso es **refactor**.

Para `password.js`, cada regla (longitud, mayúscula, dígito) mapea a un test. Borrá una regla, mirá su test fallar, volvela a agregar.

Mirá la guía para el recorrido completo, la comparativa TDD vs test-first y la guía sobre dónde encaja la disciplina.
