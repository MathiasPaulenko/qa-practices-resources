# Plantilla de Criterios de Aceptación BDD (Gherkin)

Un archivo `.feature` rellenado que muestra criterios de aceptación en Gherkin para una historia de código promocional en el checkout: un bloque `Background`, escenarios de camino feliz, negativos y de borde, más un `Scenario Outline` para validación de entrada.

## Cómo usarlo

1. Copia `promo-code-checkout.feature` en el directorio `features/` de tu proyecto.
2. Reemplaza el dominio de código promocional por tu propia historia y ajusta los pasos al lenguaje de tu aplicación.
3. Escribe las step definitions de los pasos: mapean directamente a Cucumber, SpecFlow o Behave.
4. Ejecuta `behave --dry-run` (o `cucumber --dry-run`) para comprobar que cada paso resuelve.

## Guía completa

Consulta la [plantilla en QAPractices](https://qapractices.com/es/templates/user-story-acceptance-criteria-template-bdd) para el esqueleto, el checklist de cobertura y las mejores prácticas.
