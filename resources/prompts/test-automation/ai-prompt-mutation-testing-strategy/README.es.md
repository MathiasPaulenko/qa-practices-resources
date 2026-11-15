# Prompt de IA: Estrategia de Mutation Testing — Companion

Archivos complementarios del recurso [Prompt de IA: Estrategia de Mutation Testing](https://qapractices.com/es/prompts/ai-prompt-mutation-testing-strategy).

## Archivos

| Archivo | Propósito |
| --- | --- |
| `prompt-template.txt` | El prompt de estrategia completo, listo para copiar y pegar en cualquier LLM. |
| `example-input.txt` | Entrada de ejemplo: un módulo de pagos en Java 21 medido con PIT en GitHub Actions. |
| `pitest-pom.xml` | Bloque del plugin PIT (pitest-maven 1.30.x) con mutadores STRONGER, gate del 75% y archivos de historial. |
| `stryker.conf.json` | Configuración de StrykerJS 10.x con `thresholds.break`, modo incremental y lista `mutate` acotada. |
| `mutmut-setup.cfg` | Sección `setup.cfg` de mutmut 3.x acotada a un paquete, con rutas excluidas. |

## Uso

1. Copia `prompt-template.txt` en tu LLM.
2. Reemplaza los placeholders entre corchetes usando `example-input.txt` como referencia de nivel de detalle.
3. Toma el archivo de configuración de tu stack y adapta nombres de paquetes, umbrales y rutas.
4. Corre una primera ejecución acotada a un módulo crítico antes de activar el gate de CI — esa línea base te dice dónde viven los mutantes equivalentes.
5. Conecta `thresholds.break` / `mutationThreshold` al CI solo después del primer triaje, o el gate bloquea por ruido.

## Requisitos

- Java/JVM: Maven o Gradle más pitest-maven 1.30.x.
- JS/TS: Node.js 22+ y `@stryker-mutator/core` 10.x con el plugin de tu test runner.
- Python: mutmut 3.x (`pip install mutmut`) y pytest.
- Un runner de CI donde el job de mutación pueda correr en hilos paralelos (`threads` en PIT, `concurrency` en Stryker).

## Notas

- Los mutantes equivalentes son esperables (aproximadamente un 5-15% de los supervivientes): documéntalos y exclúyelos en lugar de escribir tests para trivialidades.
- Mantén el gate sobre el delta del score por módulo, no sobre un número plano para todo el repositorio.
- Nunca pegues credenciales reales, PII ni datos de producción en el prompt.
