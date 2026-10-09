# Prompt de IA: Generar Escenarios BDD Gherkin

Prompt listo para copiar que convierte una user story más criterios de aceptación en un archivo `.feature` Gherkin —caminos felices, negativos, casos límite y un Scenario Outline—.

## Archivos

- `prompt.md` — el prompt completo con el ejemplo de entrada ya rellenado.
- `password-reset.feature` — el feature file que el prompt produce para esa entrada.

## Cómo usarlo

1. Abre `prompt.md` y copia el texto dentro de `## The Prompt`.
2. Sustituye los placeholders entre corchetes por tu user story, criterios de aceptación, reglas de negocio y runner BDD.
3. Pégalo en tu LLM y revisa los escenarios generados antes de commitearlos —primero los nombres, después los pasos—.
4. Compara tu salida con `password-reset.feature` para verificar estructura, tagging y fraseo declarativo.

## Recurso completo

Para la versión renderizada con mejores prácticas, errores comunes y FAQ, consulta la [página del prompt en QAPractices](https://qapractices.com/es/prompts/ai-prompt-generate-bdd-gherkin-scenarios).
